# Session handoff — 2026-07-24 21:38 UTC

## Current task
None in flight. The pipeline is steady-state and fully autonomous:
research → write → fact-check → publish → email, all inside one scheduled
run. Issues published daily 2026-07-18 through 2026-07-24 (latest commit
`52c15fb`). The last three runs (07-22, 07-23, 07-24) completed headlessly
with email delivered and no human intervention.

Next scheduled run: 2026-07-25 ~11:05 UTC. Nothing needs doing before then.

## Routine registry (live state, verified against `list_triggers` this session)
| Routine | Trigger ID | Cron (UTC) | Binding | Notifications | Prompt gist |
|---|---|---|---|---|---|
| Daily AI newsletter | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` (fires ~11:05) | session-bound → `session_01JHEXp6dpeg5hK3DQGdj4eK` | none | "Follow the Daily newsletter process in CLAUDE.md exactly… work autonomously… don't redo a published date… finish with a top-3 summary" |

Three spent one-shot `send_later` triggers also appear in `list_triggers`
with `ended_reason: run_once_fired` (`trig_019Ngy6iXGtGKqPLdYx8wJ3y`,
`trig_01AKZFYEMAgb3VQF7bcwttJA`, `trig_01TBrYBhrUHhXib9X3MaHkyF`) — inert,
ignorable, safe to delete.

The 07:15 email-relay routine `trig_01GbxBCjF5dZrHiwk6MjbgPD` was DELETED
2026-07-22: its notification-based delivery never actually sent anything.

## Decisions & constraints in force
- **Routines only.** No Anthropic API key, no paid per-token credits, no
  GitHub Actions AI pipeline — the owner will not pay per-token.
- **Default branch is `main`.** Newsletters push straight to it; no PRs.
- **Email == published issue**, byte-for-byte in content, sent at the end of
  the publish run via `scripts/zoho_send.sh` (Zoho Mail REST API over
  HTTPS). NOT routine notifications (proven undelivered 07-19), NOT SMTP
  (ports blocked by the egress proxy, tested 07-22), NOT the Zoho MCP
  connector (absent in headless scheduled runs, confirmed 07-20).
- **Issue size target ~12–15 stories**; widen the net on slow days rather
  than shorten, but never pad with unverifiable or stale-as-new items.
- **Thematic sections are exclusive homes, top-5 each**: Capital & Deals
  (money-led), Regulation & Policy (government action), Compute & Data
  Centers (physical buildout). Precedence: deal-value → Capital; chip
  regulation → Regulation; otherwise buildout → Compute. Omit empty
  sections; fewer than 3 Top Stories is acceptable.
- **No-repeat rule**: read/grep the last 7 issues before selecting. A
  covered story returns only with a genuinely new development, and the item
  must lead with the dated delta.
- **Fact-check skill pass is mandatory** before every publish. A story that
  fails is dropped, never softened.
- **Repo is public**: no secrets or personal data in committed files. Zoho
  OAuth credentials live only in `~/.zoho_mail_api` (mode 600, outside git).
- The "fable trailer history rewrite" idea was explicitly cancelled by the
  owner — do not raise it again.

## Recently changed
- `newsletters/2026-07-24.md` — today's issue (6 verified stories).
- `README.md` — Latest/Archive index updated through 07-24.
- `scripts/zoho_send.sh` — email sender (REST API, handles OAuth refresh);
  `scripts/md2email.py` — markdown→inline-styled-HTML converter.
- `~/.zoho_mail_api` — created and authorized 07-22 (outside the repo).
- `CLAUDE.md` — step 7 (email), fact-checking rules, no-repeat rule,
  thematic section rules, ~12–15 story target.
- `.claude/skills/fact-check/SKILL.md` — added no-repeat check (#5) and
  section-placement verification.
- `docs/OPERATIONS.md` — rewritten for the single-routine architecture.
- `.gitignore` — added for Python bytecode.
- Corrections appended to `newsletters/2026-07-18.md` (fabricated Gemini
  3.5 Pro launch) and `2026-07-19.md` (stale GPT-5.6 rollout status).

## Open questions / risks
- **Container reclaim is the main single point of failure.** The publish
  routine is session-bound, so a reclaim silently stops publishing AND
  deletes `~/.zoho_mail_api`. Symptoms: no `Newsletter:` commit in the
  morning, and/or no email. Recovery: `docs/OPERATIONS.md` §1 (rebind the
  routine to a live session) and §2 (~3-minute Zoho grant-code redo).
- **Sender reputation**: mail comes from a fresh Zoho address; if an issue
  lands in the spam folder, the owner should mark it "Not spam" once.
- **Aggregator contamination is constant.** Recent runs caught fabricated
  or misdated stories nearly every day (a phantom "Gemini 3.5 Flash Cyber",
  a "DeepSeek V4 launches July 24" that was actually an April GA, an
  Anthropic revenue figure redated from May). Never relax the primary-source
  test.
