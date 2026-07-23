# Session handoff — 2026-07-22 (evening UTC)

## Current task
None in flight. Pipeline fully operational end-to-end: research → write →
fact-check → publish → **email via `scripts/zoho_send.sh`** (Zoho Mail REST
API over HTTPS; OAuth refresh token obtained 2026-07-22; test email of the
07-22 issue delivered to the owner's gmail). Watch item: the next 11:00 UTC
run is the first fully headless publish→email — verify a `Newsletter:`
commit AND email arrival.

## Routine registry (live state, verify on resume)
| Routine | Trigger ID | Cron (UTC) | Binding | Notifications |
|---|---|---|---|---|
| Daily AI newsletter (publish) | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` | session-bound → `session_01JHEXp6dpeg5hK3DQGdj4eK` | none |

(The 07:15 relay routine `trig_01GbxBCjF5dZrHiwk6MjbgPD` was DELETED
2026-07-22 — notification email never delivered; publish emails directly.)

## Decisions & constraints in force
- Routines only; no Anthropic API key, no paid credits, no GitHub Actions AI
  pipeline.
- Default branch `main`; publish pushes straight to it, no PRs.
- Email == published issue byte-for-byte in content, sent by the publish run
  via `scripts/zoho_send.sh` (NOT routine notifications — proven
  undelivered; NOT SMTP — ports blocked by egress proxy; NOT the connector
  in scheduled runs — absent headless).
- Issue target ~12–15 stories; widen the net on slow days.
- Thematic sections, exclusive-home + top-5 each: Capital & Deals,
  Regulation & Policy, Compute & Data Centers (precedence: deal-value →
  Capital; chip regulation → Regulation; buildout → Compute). Omit empty
  sections; <3 Top Stories acceptable.
- No-repeat rule: grep last 7 issues before selecting; covered stories
  return only with a dated delta that leads the item.
- Repo is public: no secrets or personal data in committed files. Zoho
  OAuth creds live ONLY in `~/.zoho_mail_api` (mode 600, outside repo).
- Fact-check skill pass is mandatory before every publish.
- The "fable trailer history rewrite" idea was explicitly cancelled — do
  not raise it again.

## Recently changed (this session era)
- Issues 07-19 … 07-22 published; corrections appended to 07-18 (Gemini
  3.5 Pro) and 07-19 (GPT-5.6 GA staleness).
- `scripts/zoho_send.sh` + `scripts/md2email.py` — email pipeline.
- `~/.zoho_mail_api` — created + authorized (refresh token stored).
- Relay routine deleted; OPERATIONS.md rewritten for single-routine
  architecture.

## Open questions / risks
- Publish routine is session-bound: container reclaim silently stops
  publishing AND deletes `~/.zoho_mail_api`. Symptoms: no `Newsletter:`
  commit / no email. Recovery: OPERATIONS.md §1 (rebind routine) and §2
  (3-minute grant-code redo for email creds).
- Zoho free-tier sender reputation: if an email lands in spam, mark "Not
  spam" to train gmail.
