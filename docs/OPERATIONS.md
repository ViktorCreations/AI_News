# Operations runbook — AI_News automation

How the daily pipeline actually runs, what its IDs are, how it fails, and how
to fix it. **Update this file whenever a routine changes**, and run the
`handoff` skill afterwards. (Editorial process lives in `CLAUDE.md`; this file
is only about the machinery.)

## Architecture

Two scheduled Routines (Claude Code Remote triggers), deliberately split so a
single research pass feeds both the repo and the email:

```
07:00 local (11:00 UTC)  PUBLISH  — session-bound routine in a persistent
                                    Claude Code session with git auth.
                                    Follows CLAUDE.md: research → write →
                                    fact-check → update README → commit
                                    "Newsletter: YYYY-MM-DD" → push to main
                                    → email the issue via the Zoho Mail
                                    connector (scripts/md2email.py → HTML →
                                    ZohoMail_sendEmail to the owner's gmail).
07:15 local (11:15 UTC)  RELAY    — DEPRECATED fallback (see below). Fresh-
                                    session routine with email notifications
                                    on; its notification-based email was
                                    proven undelivered on 2026-07-19, so it
                                    is not a real delivery path. Scheduled
                                    for deletion once the Zoho email step
                                    succeeds in a scheduled (headless) run.
```

Design invariants:

- **Email == repo, byte for byte.** The relay only echoes what publish pushed.
- **Publish is prompt-thin.** Its trigger prompt says "follow CLAUDE.md" —
  process changes ship as commits to CLAUDE.md, not trigger edits.
- **No Anthropic API key anywhere.** Everything is session/Routine-based; no
  per-token billing, no GitHub Actions calling the API.

## Routine registry

| Routine | Trigger ID | Cron (UTC) | Binding | Notifications |
|---|---|---|---|---|
| Daily AI newsletter (publish) | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` | session-bound → `session_01JHEXp6dpeg5hK3DQGdj4eK` | none (server rejects notifications on session-bound routines) |
| Daily AI newsletter — email (relay, DEPRECATED) | `trig_01GbxBCjF5dZrHiwk6MjbgPD` | `15 11 * * *` | fresh session per fire, environment `env_01HPAanz6q11rUSsDu3MubpC` | email on, push off — never delivers; delete after Zoho step proves out headless |

(A spent one-shot `send_later` trigger from initial setup may also appear in
`list_triggers` with `ended_reason: run_once_fired` — inert, ignorable.)

## Platform facts that bite

- **Cron is UTC**; the user thinks in local time (UTC−4 in summer). Hourly-
  style crons at minute 0 get anchored to the creation minute, so actual fire
  times can drift a few minutes past the hour.
- **`update_trigger` cannot change a prompt.** Prompt change = `delete_trigger`
  + `create_trigger`. After any errored create call (e.g. MCP stream
  AbortError), run `list_triggers` before retrying — the create may or may
  not have registered, and blind retries make duplicates.
- **Binding trade-off**: session-bound routines inherit the session's git
  auth (can push) but cannot carry notifications; fresh-session routines can
  carry notifications but have no push auth. This is *why* there are two
  routines.
- **Egress policy blocks non-MCP GitHub writes** (repo settings, branch
  renames → HTTP 403 from the proxy). Don't retry policy 403/407s; those
  operations belong to the user in the GitHub UI.
- **The repo is public** — raw URLs work unauthenticated (the relay depends
  on this), and nothing sensitive may be committed.

## Failure modes & recovery

### 1. No newsletter commit today (publish didn't run or died)

Check: `git log origin/main --oneline -3` for today's `Newsletter:` commit.

- The publish routine is **session-bound**; if its container was reclaimed,
  the routine is orphaned and fires into nothing. Recovery: from a live
  Claude Code session on this repo, run the `onboard` skill, then recreate
  the publish routine bound to the *current* session (create with
  `persistent_session_id` omitted = self-bind), delete the orphaned trigger,
  and update this registry.
- If the routine fired but the run failed mid-way, re-fire it manually
  (`fire_trigger`) or write the issue by hand following CLAUDE.md.
- The relay is self-healing for this case: it emails the newest existing
  issue with a "not published yet" note.

### 2. Email didn't arrive

Delivery is the Zoho Mail step at the end of the publish run (CLAUDE.md
step 7), NOT platform notifications — routine notification email was tested
2026-07-19 and never delivered (the platform's "noteworthy" heuristic is not
a reliable channel; the relay routine exists only as a deprecated vestige).

- **Primary path (headless-capable)**: `scripts/zoho_send.sh
  newsletters/YYYY-MM-DD.md` sends via the Zoho Mail REST API over HTTPS
  using OAuth credentials in `~/.zoho_mail_api` (mode 600, OUTSIDE the repo
  — never commit it). The file holds CLIENT_ID / CLIENT_SECRET /
  REFRESH_TOKEN from a Zoho **Self Client** (api-console.zoho.com, scope
  `ZohoMail.messages.CREATE,ZohoMail.accounts.READ`); the script exchanges
  a one-time GRANT_CODE for the permanent refresh token on first run.
- **Why not SMTP**: tested 2026-07-22 — the egress proxy only passes
  HTTPS; smtp.zoho.com:465 is reset and :587 times out. App passwords are
  useless here; only the HTTPS REST API works headless.
- **Why not the connector**: confirmed 2026-07-20 — `mcp__ZohoMCP__*` tools
  do NOT load in headless scheduled fires (they need the owner's
  interactive claude.ai client). Connector remains the fallback for manual
  re-sends from live sessions.
- **If email fails**: check `~/.zoho_mail_api` exists and has REFRESH_TOKEN
  (container reclaim DELETES it — the file must be re-created from the
  template in this section and re-authorized with a fresh grant code, since
  it lives outside git). Then check the script's error output (token
  refresh vs send step).
- If Zoho auth expired, the user must re-authenticate the connector in the
  claude.ai connector settings.
- Sender reputation: mail comes from a fresh zohomail.com address — check
  the gmail spam folder and mark "Not spam".

### 3. A published issue contains a factual error

Run the `fact-check` skill against the published file. Fix = remove/correct
the story, update README's latest line and archive row, append a dated
`*Correction:*` note at the bottom of the issue, commit and push. Precedent:
the 2026-07-18 issue's fabricated "Gemini 3.5 Pro launch" correction.

### 4. Duplicate or missing routines after an errored MCP call

`list_triggers` is the source of truth. Delete duplicates by ID; recreate
missing ones from the registry above (prompts: publish = "follow CLAUDE.md
process, work autonomously, don't redo published dates"; relay = "fetch
today's raw newsletter URL from main, output verbatim, fallback to newest
with a note").

### 5. Schedule changes

`update_trigger` handles cron/name/enabled without touching the prompt. Keep
publish ≥15 minutes ahead of relay, and update the registry table here.

## Standing decisions (user-confirmed; don't re-litigate)

- Routines only — **no API key, no paid credits, no GitHub Actions pipeline**.
- Default branch is `main`; newsletters push straight to it, no PRs.
- One research pass per day; the emailed issue must match the published file
  byte-for-byte in content.
- Email delivery via the Zoho Mail connector at the end of the publish run
  (from `viktor.lanovliuk@zohomail.com` to the owner's gmail), not via
  routine notifications — those were proven undelivered 2026-07-19.
- Issue size target is ~12–15 stories (owner request, 2026-07-19): widen the
  net on slow days rather than shorten.
