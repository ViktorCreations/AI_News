# Session handoff — 2026-07-19 18:15 UTC

## Current task
2026-07-19 issue: **published, expanded to 12 items, and emailed via Zoho**.
Email architecture reworked: routine notification email proven undelivered
(both scheduled 11:15 UTC fire and manual 16:42 UTC re-fire produced no
email); Zoho Mail connector added by owner and verified working (test email
received). CLAUDE.md now has step 7 (Zoho email via
`scripts/md2email.py` + `ZohoMail_sendEmail`); story target raised to
~12–15 per owner request. **RESOLVED 2026-07-20: the Zoho connector does
NOT load in headless scheduled fires** — the 07-20 run published (commit
26fe272, 11 items + a correction to 07-19's GPT-5.6 item) but could not
email. Next action: owner to create a Zoho app-specific password and store
it as env secret `ZOHO_SMTP_PASS` in the environment; then the publish run
emails via SMTP with curl (see OPERATIONS.md §2) and the deprecated relay
routine `trig_01GbxBCjF5dZrHiwk6MjbgPD` can be deleted. Until then, email
the issue manually from any live session with the Zoho connector.

## Routine registry (live state, verify on resume)
| Routine | Trigger ID | Cron (UTC) | Binding | Notifications |
|---|---|---|---|---|
| Daily AI newsletter (publish) | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` | session-bound → `session_01JHEXp6dpeg5hK3DQGdj4eK` | none |
| Daily AI newsletter — email (relay) | `trig_01GbxBCjF5dZrHiwk6MjbgPD` | `15 11 * * *` | fresh session, env `env_01HPAanz6q11rUSsDu3MubpC` | email on, push off |

## Decisions & constraints in force
- Routines only; no Anthropic API key, no paid credits, no GitHub Actions AI
  pipeline (user has no key and won't pay per-token).
- Default branch is `main`; publish pushes straight to it, no PRs.
- Email == published issue, byte-for-byte in content; sent via Zoho Mail
  connector at the end of the publish run (NOT routine notifications —
  proven undelivered 2026-07-19).
- Issue size target ~12–15 stories (owner request 2026-07-19); widen the net
  on slow days rather than shorten.
- Repo is public: no secrets or personal data in committed files.
- Fact-check pass is mandatory before every publish (CLAUDE.md step 4).
- The "fable trailer history rewrite" idea was explicitly cancelled by the
  user — do not raise it again.

## Recently changed
- `newsletters/2026-07-18.md` — removed false Gemini 3.5 Pro story (verified
  against Google's changelog/blog: never released), rewrote editor's note,
  added correction note.
- `README.md` — latest-issue line + archive row updated to Kimi K3 top story.
- `CLAUDE.md` — added fact-check step + "Fact-checking rules" section +
  skills/operations pointers.
- `.claude/skills/{onboard,fact-check,handoff,resume}/SKILL.md` — new.
- `docs/OPERATIONS.md` — new runbook.
- Routines unchanged this session (registry above matches `list_triggers`).

## Open questions / risks
- Publish routine is session-bound: if its container is reclaimed, daily
  publishing silently stops (recovery recipe: OPERATIONS.md §1). Watch for a
  missing `Newsletter:` commit any morning.
- Tomorrow's publish run (2026-07-19 ~11:00 UTC) is the first with the
  mandatory fact-check step — worth spot-checking the issue it produces.
