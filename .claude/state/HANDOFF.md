# Session handoff — 2026-09-05 22:48 UTC

## Current task
None in flight. Daily publishing is steady-state and current: issues exist for
every date 2026-07-18 through 2026-09-05, latest commit `5c1dc63`. Working tree
clean, branch `main`, pushed.

**Publishing works. Email delivery does not, without manual fallback.** This is
the single most important thing for a fresh session to know:

- `~/.zoho_mail_api` does not exist and no Zoho environment variables are set.
  `scripts/zoho_send.sh` therefore fails on every run with a message naming the
  six missing variables (CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, FROM_ADDRESS,
  TO_ADDRESS, REFRESH_TOKEN).
- Expect that failure. Fall back to the ZohoMCP connector when it is loaded:
  `mcp__ZohoMCP__ZohoMail_sendEmail` with `accountId` 6087715000000008002,
  from the Zoho mailbox to the configured notification email, body rendered by
  `python3 scripts/md2email.py newsletters/YYYY-MM-DD.md`, subject = the issue's
  H1. Used successfully on 09-03, 09-04 and 09-05.
- If neither path works: publish steps 1–6 anyway and state the email failure
  plainly in the run summary. Do not silently skip it.

**Backlog: closed, no action needed.** A container reclaim destroyed the
credentials file after the 2026-08-16 send. Issues 2026-08-17 through
2026-09-02 (17 of them) were written, fact-checked, committed and pushed but
never emailed. On 09-03 the owner chose a single catch-up digest over 17
individual re-sends; that digest was sent and the gap is settled. Do not
re-send those issues.

## Routine registry (live state, verify on resume)
| Name | Trigger ID | Cron (UTC) | Binding | Notifications | Prompt gist |
|---|---|---|---|---|---|
| Daily AI newsletter | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` (fires ~11:05–11:08) | session-bound to `session_01JHEXp6dpeg5hK3DQGdj4eK` | none | Run the CLAUDE.md daily process; research, select ~10 stories, write today's UTC issue, update README, commit `Newsletter: YYYY-MM-DD`, push to default branch, work autonomously, don't redo a published date, close with the top-3 paragraph |

Enabled, environment `env_01HPAanz6q11rUSsDu3MubpC`, no routine-level
environment variables set, no MCP connections attached. Last fired
2026-09-05T11:05:40Z; next 2026-09-06T11:04:56Z. Because it is session-bound,
a container reclaim orphans it — see `docs/OPERATIONS.md` §1 for the rebind
procedure.

## Decisions & constraints in force
- Repo is public: no secrets, tokens, or personal data in committed files. Zoho
  OAuth credentials live outside git only.
- The `fact-check` skill is mandatory before every publish. A story that fails
  verification is dropped, never softened.
- Prefer a fuller issue (~12–15 stories); on slow days widen the net before
  shortening, and never pad with stale or unverifiable items.
- Thematic sections are exclusive homes: money-led → Capital & Deals,
  government/regulatory action → Regulation & Policy, physical buildout and
  chips → Compute & Data Centers. Each capped at five.
- Commit trailer is now `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
  followed by the `Claude-Session:` line (changed from Opus 4.8 on 2026-09-02).
- Do not create pull requests unless explicitly asked.
- Process changes ship as commits to `CLAUDE.md`, not as edits to the routine
  prompt.

## Recently changed
- `scripts/zoho_send.sh` (`88c1708`) — reads credentials from environment
  variables when the file is absent, and names the missing ones on failure.
- `docs/OPERATIONS.md` §2 (`88c1708`) — documents the environment-variable path
  as the durable one, records the 17-issue delivery gap, and corrects the old
  claim that the ZohoMCP connector never loads in headless scheduled fires (it
  loaded on 2026-09-03, 09-04 and 09-05).
- `newsletters/2026-08-17` … `2026-09-05` and `README.md` — daily issues.

## Open questions / risks
- **Live failure mode:** email delivery depends on the ZohoMCP connector
  happening to load. It is not guaranteed on any given fire. The durable fix is
  the owner setting the six credential variables in the CCR environment config
  (`env_01HPAanz6q11rUSsDu3MubpC`); only they can generate the Self Client
  credentials and grant code. Until then, every run needs the fallback.
- Session-bound routine: if this session's container is reclaimed the routine
  fires into nothing and publishing stops silently. Recovery in
  `docs/OPERATIONS.md` §1.
- The-decoder has become the dominant source for daily research. Keep pulling
  from TechCrunch, The Register, Hacker News, arXiv and lab blogs directly so
  the issue does not become one outlet's rewrite.
- Recurring trap, caught repeatedly: aggregators resurface weeks-old papers and
  funding rounds as new. Check the date on the *event*, not the article.
