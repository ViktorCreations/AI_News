# Session handoff — 2026-09-14 11:14 UTC

## Current task
None in flight. Daily publishing is steady-state and current: an issue exists
for every date 2026-07-18 through 2026-09-14, latest commit `e94ed71`, working
tree clean, branch `main`, pushed.

**Publishing works. Email delivery does not, without manual fallback.** This is
still the single most important thing for a fresh session to know:

- `~/.zoho_mail_api` does not exist and no Zoho environment variables are set.
  `scripts/zoho_send.sh` therefore fails on every run with a message naming the
  six missing variables (CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, FROM_ADDRESS,
  TO_ADDRESS, REFRESH_TOKEN). It has failed on every run since 2026-09-06.
- Expect that failure. Fall back to the ZohoMCP connector:
  `mcp__ZohoMCP__ZohoMail_sendEmail` (load via ToolSearch) with `accountId`
  6087715000000008002, from the Zoho mailbox to the configured notification
  email, body rendered by `python3 scripts/md2email.py newsletters/YYYY-MM-DD.md`,
  subject = the issue's H1. This has worked every day 2026-09-03 to 09-14.
- If neither path works: publish steps 1–6 anyway and state the email failure
  plainly in the run summary. Do not silently skip it.

**Backlog: closed, no action needed.** The 17 issues from 2026-08-17 to 09-02
that were published but never emailed were covered by a single catch-up digest
on 09-03, at the owner's choice. Do not re-send them.

## Routine registry (live state, verify on resume)
| Name | Trigger ID | Cron (UTC) | Binding | Notifications | Prompt gist |
|---|---|---|---|---|---|
| Daily AI newsletter | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` (fires ~11:05–11:08) | session-bound to `session_01JHEXp6dpeg5hK3DQGdj4eK` | none | Run the CLAUDE.md daily process; research, select ~10 stories, write today's UTC issue, update README, commit `Newsletter: YYYY-MM-DD`, push to default branch, work autonomously, don't redo a published date, close with the top-3 paragraph |

Enabled, environment `env_01HPAanz6q11rUSsDu3MubpC`, no routine-level
environment variables, no MCP connections attached. Last fired
2026-09-14T11:06:29Z (last_run SUCCEEDED); next 2026-09-15T11:04:56Z. Because
it is session-bound, a container reclaim orphans it — see `docs/OPERATIONS.md`
§1 for the rebind procedure.

## Decisions & constraints in force
- Repo is public: no secrets, tokens, or personal data in committed files. Zoho
  OAuth credentials live outside git only.
- The `fact-check` skill is mandatory before every publish. A story that fails
  verification is dropped, never softened.
- Prefer a fuller issue (~12–15 stories); on slow days widen the net before
  shortening, and never pad with stale or unverifiable items. A short issue is
  acceptable — 2026-09-14 ran five items on a genuinely quiet weekend.
- Thematic sections are exclusive homes, each capped at five: money-led →
  Capital & Deals, government/regulatory action → Regulation & Policy,
  physical buildout and chips → Compute & Data Centers.
- **AI in Real Estate** (added 2026-09-10) is the last section and outranks the
  other thematic sections for property stories; data centers stay in Compute.
  30-day window, explicit dates, `Context:` labels allowed, hard sourcing bar
  against vendor SEO. Full rules in CLAUDE.md.
- Commit trailer is `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
  followed by the `Claude-Session:` line.
- Do not create pull requests unless explicitly asked.
- Process changes ship as commits to `CLAUDE.md`, not as edits to the routine
  prompt.

## Recently changed
- `CLAUDE.md` + `.claude/skills/fact-check/SKILL.md` (`b308ef8`) — added the
  AI in Real Estate section, its precedence and beat-specific rules, a daily
  real-estate research angle, and a harder source pass in the fact-check skill.
- `newsletters/2026-09-10.md` — carried a one-time seven-item backfill of the
  year to date for the new section's launch, at the owner's request. Recorded
  in CLAUDE.md as a one-off; do not repeat it.
- `newsletters/2026-09-06` … `2026-09-14` and `README.md` — daily issues.

## Open questions / risks
- **Open question the owner has not answered:** AI in Real Estate has come in
  at or below one qualifying item for three consecutive days (09-12 one item
  slightly outside the window, 09-13 one item, 09-14 omitted entirely). The
  recommendation put to the owner is to change the floor from "two to four" to
  "omit if nothing qualifies, otherwise one to four" rather than keep
  stretching the 30-day window. Until answered, do not pad the section.
- **Live failure mode, new on 2026-09-14:** a run completed research and
  fact-check, then skipped steps 5–7 (README, commit, push, email) while
  reporting as though published. A stop hook caught the untracked file. Before
  ending any run, verify: `git status` clean, both `<!-- latest -->` and
  `<!-- archive -->` markers present in README.md, and an email messageId.
- **README markers are fragile.** An edit on 09-13 removed `<!-- archive -->`
  and had to be restored. Always `grep -c` both markers before committing.
- **Email delivery depends on the ZohoMCP connector loading.** The durable fix
  is the owner setting the six credential variables in the CCR environment
  config (`env_01HPAanz6q11rUSsDu3MubpC`); only they can generate the Self
  Client credentials and grant code.
- **Unverified lead worth chasing:** a second mathematician, Andreas Thom, is
  reported to allege OpenAI trained Astra on his unpublished work with Gábor
  Kun on Gromov's soficity conjecture — one of the ten problems Astra was
  announced to have solved on 2026-08-03. Dropped on 09-10 because the only
  route to it was a third party's relay of a Mastodon post and x.com returns
  402 from this container. If a first-tier outlet picks it up, it is a major
  story.
- **Running threads to keep dated:** the Navier-Stokes priority dispute (Clay
  Institute review is "deliberately unhurried", no timeline); the pacing /
  slowdown thread (Amodei's essay, Altman's national-framework ask, Christiano
  on the safety committee, and the unresolved Sherman Act question OpenAI put
  to Congress); Anthropic's IPO (~$100B at ~$2T, Nvidia reportedly in talks for
  up to $10B, nothing signed).
- **Resolved discrepancy, for the record:** Dwelly raised £69M in February 2026
  *and* $170M in July 2026. These are two separate rounds, not a conflict.
- Several sites return 403/402 to this container (openai.com, forbes.com,
  cnbc.com, bbc.com, x.com, SSRN, HousingWire, Zillow newsroom). That is a bot
  block, not a dead link — verify content via an accessible mirror, and only
  link the blocked primary when its existence is independently confirmed.
