# Session handoff — 2026-09-23 12:35 UTC

## Current task
None in flight. Daily publishing is steady-state and current: an issue exists
for every date 2026-07-18 through 2026-09-23 (68 issues), latest commit
`3656cda`, working tree clean, pushed to both `main` and the session's
designated branch.

**Publishing works. Email delivery does not, without manual fallback.** Still
the single most important thing for a fresh session to know:

- `~/.zoho_mail_api` does not exist and all six Zoho variables are unset, so
  `scripts/zoho_send.sh` fails on every run naming CLIENT_ID, CLIENT_SECRET,
  ACCOUNT_ID, FROM_ADDRESS, TO_ADDRESS, REFRESH_TOKEN. It has failed on every
  run since 2026-09-06.
- Expect that failure. Fall back to the ZohoMCP connector:
  `mcp__ZohoMCP__ZohoMail_sendEmail` (load via ToolSearch) with `accountId`
  6087715000000008002, from the Zoho mailbox to the configured notification
  email, body from `python3 scripts/md2email.py newsletters/YYYY-MM-DD.md`,
  subject = the issue's H1. This has worked every day since 2026-09-03.
- If neither path works: publish steps 1–6 anyway and say so plainly in the
  run summary. Do not silently skip it.

**Order of operations matters.** Commit and push BEFORE the email step. On
2026-09-16 a container restart mid-run destroyed a finished, fact-checked
issue that had not yet been committed, and it had to be rebuilt from context.
Containers here restart most days — `cat /proc/uptime` frequently reads 0
minutes at the start of a run.

## Routine registry (live state, verified this session)
| Name | Trigger ID | Cron (UTC) | Binding | Notifications | Prompt gist |
|---|---|---|---|---|---|
| Daily AI newsletter | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` (fires ~11:05–11:16) | session-bound to `session_01JHEXp6dpeg5hK3DQGdj4eK` | none | Run the CLAUDE.md daily process; research, select ~10 stories, write today's UTC issue, update README, commit `Newsletter: YYYY-MM-DD`, push to default branch, work autonomously, don't redo a published date, close with the top-3 paragraph |

Enabled, no routine-level environment variables, no MCP connections attached.
Last fired 2026-09-23T11:16:04Z (last_run SUCCEEDED); next 2026-09-24T11:14:56Z.
Session-bound, so a container reclaim orphans it — see `docs/OPERATIONS.md` §1
for the rebind procedure.

## Git topology — read before pushing
The session runs on branch `claude/ai-news-daily-newsletter-b67lp0`, not
`main`. Publish to **both**:

```
git push origin HEAD:main      # what readers see; CLAUDE.md step 6
git push origin HEAD           # satisfies the stop hook, which counts
                               # unpushed commits on the current branch
```

Local `main` drifts behind `origin/main` and has twice been left stranded
(at 2026-09-11, then 2026-09-16), which makes a bare `git push -u origin main`
fail as non-fast-forward. It was resynced to `3656cda` this session. If a push
is rejected, fetch first and confirm `git merge-base --is-ancestor origin/main
HEAD` before doing anything else; never force. GitHub also reports a
server-side rule renaming pushes to that branch toward `main`, which is
probably why the container keeps coming back on it.

## Decisions & constraints in force
- Repo is public: no secrets, tokens, or personal data in committed files.
  Zoho OAuth credentials live outside git only.
- The `fact-check` skill is mandatory before every publish. A story that fails
  verification is dropped, never softened.
- Prefer a fuller issue; on slow days widen the net before shortening, and
  never pad. Six to eight well-sourced items is an acceptable issue.
- Thematic sections are exclusive homes, and this binds even when it buries a
  lead: intergovernmental or government action goes to Regulation & Policy
  (the UN panel, Newsom, Abbott, von der Leyen all did), money-led to Capital
  & Deals, physical buildout to Compute & Data Centers. Carry the story in the
  editor's note instead. Section order follows the CLAUDE.md template — this
  was got wrong once on 2026-09-23 and fixed pre-publish.
- **AI in Real Estate** is the last section and outranks the other thematic
  sections for property stories. 30-day window, explicit dates, `Context:`
  labels allowed, hard sourcing bar against vendor SEO. Full rules in
  CLAUDE.md.
- Commit trailer is `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
  followed by the `Claude-Session:` line.
- Do not create pull requests unless explicitly asked.
- Process changes ship as commits to `CLAUDE.md`, not edits to the routine
  prompt.

## Recently changed
- `scripts/fetch.py` + `docs/SOURCES.md` (`3ddd8ac`, updated `7725523`) — the
  fetch helper and source-access map. Most "blocked" sources were origin bot
  edges, not egress policy; the script routes around them without spoofing a
  browser. Ars Technica article pages began 403ing on 2026-09-19 and are
  recorded as feed-only.
- `CLAUDE.md` + `.claude/skills/fact-check/SKILL.md` (`3ddd8ac`) — link rules
  for bot-blocked sources, and what a feed-only route does and does not
  license.
- `newsletters/2026-09-14` … `2026-09-23` and `README.md` — daily issues.

## Open questions / risks
- **Open question the owner has not answered:** whether to change the AI in
  Real Estate floor from "two to four items" to "omit if nothing qualifies,
  otherwise one to four." The section has now been omitted six days running
  (2026-09-18 through 09-23) after two strong days before that. The beat is
  real but genuinely intermittent. Until answered, do not pad it.
- **Running threads worth continuing:** the pacing debate and what it has
  actually changed (both labs shipped cheaper models 90 minutes apart on
  09-22, Anthropic's with safety training described as broadly unchanged);
  embedded evaluators (Anthropic's first is Accenture at $1B/5yr, not the
  safety nonprofits); the Trump–Xi summit on 09-24 with AI safety on the
  agenda; data-center permitting halts spreading across states (New York,
  then Texas on 09-21); the mathematicians' objection versus OpenAI's
  advisory group; Anthropic's IPO, reportedly pushed to November.
- **Source hygiene that keeps mattering:** third-party page summaries from
  search results are not verification — several items have been cut because
  figures appeared only in a search snippet and not in any page read in full.
  Feed-only routes confirm that a thing was announced and when, nothing more.
- **Watch for source monoculture.** The 2026-09-20 issue went out with seven
  of eight links from one outlet. Check the spread before publishing;
  weekends are when it happens.
- **Email deliverability is unverified.** Sends succeed and report
  `mailDeliveryStatus: success`, but the owner asked on 09-16 whether an
  issue had arrived. Worth confirming it is not being spam-filtered; the
  Zoho domain has had no DKIM/SPF alignment work done from here.
- **README markers are fragile.** An edit once removed `<!-- archive -->`.
  Always `grep -c` both markers before committing.
- Several sites return 403 to one client and 200 to another; `docs/SOURCES.md`
  is the current map and `scripts/fetch.py --route <url>` answers per host.
  Genuinely unreachable: Inman, SSRN, x.com, AP, Reuters, WSJ, Bloomberg.
