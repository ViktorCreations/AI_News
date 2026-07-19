# Session handoff — 2026-07-19 03:10 UTC

## Current task
Project-hardening pass: **done**. Fixed the fabricated "Gemini 3.5 Pro
launch" story in `newsletters/2026-07-18.md` (correction note appended, README
updated), added mandatory fact-checking to CLAUDE.md, created project skills
(`onboard`, `fact-check`, `handoff`, `resume`), and wrote
`docs/OPERATIONS.md`. No work in flight.

## Routine registry (live state, verify on resume)
| Routine | Trigger ID | Cron (UTC) | Binding | Notifications |
|---|---|---|---|---|
| Daily AI newsletter (publish) | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` | session-bound → `session_01JHEXp6dpeg5hK3DQGdj4eK` | none |
| Daily AI newsletter — email (relay) | `trig_01GbxBCjF5dZrHiwk6MjbgPD` | `15 11 * * *` | fresh session, env `env_01HPAanz6q11rUSsDu3MubpC` | email on, push off |

## Decisions & constraints in force
- Routines only; no Anthropic API key, no paid credits, no GitHub Actions AI
  pipeline (user has no key and won't pay per-token).
- Default branch is `main`; publish pushes straight to it, no PRs.
- Relay must echo the published issue verbatim (email == repo), never
  re-research.
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
