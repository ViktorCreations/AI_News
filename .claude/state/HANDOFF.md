# Session handoff — 2026-10-23 13:40 UTC

## Current task
Done. The 2026-10-23 issue is published (commit `65d220c`, on `origin/main`
and the session branch), README updated, and it was emailed via the ZohoMCP
connector fallback (`mailDeliveryStatus` not returned; send call succeeded).
An issue exists for every date 2026-07-18 through 2026-10-23 (98 issues).
Next action: none until the scheduled run on 2026-10-24.

**What happened today, so the next session recognises it:** the scheduled
fire at 11:03 UTC started the run, but the container restarted mid-draft and
left an uncommitted, truncated `newsletters/2026-10-23.md` (9 lines, cut off
mid-word). A manual `resume` at ~13:00 UTC redid research, writing and
fact-check from scratch, then published. The container restarted *again*
right after the commit and push, before the email — the commit-before-email
rule below is what saved the issue. **On resume, check `git status` for an
untracked, half-written issue for today**: that is the signature of a run
killed by a restart, and the fix is to finish the run, not to trust the
fragment's content without re-verifying it.

**Publishing works. Email delivery does not, without manual fallback.**

- `~/.zoho_mail_api` does not exist and all six Zoho variables are unset, so
  `scripts/zoho_send.sh` fails on every run naming CLIENT_ID, CLIENT_SECRET,
  ACCOUNT_ID, FROM_ADDRESS, TO_ADDRESS, REFRESH_TOKEN. Still true 2026-10-23.
- Fall back to the ZohoMCP connector: `mcp__ZohoMCP__ZohoMail_sendEmail`
  (load via ToolSearch) with `accountId` 6087715000000008002, from the Zoho
  mailbox (`ZohoMail_getMailAccounts` gives it) to the configured
  notification email, body from
  `python3 scripts/md2email.py newsletters/YYYY-MM-DD.md`, subject = the
  issue's H1. Worked again 2026-10-23.
- If neither path works: publish steps 1–6 anyway and say so plainly.

**Order of operations matters.** Commit and push BEFORE the email step.
Containers here restart often — twice in one run on 2026-10-23, and on
2026-09-16 a restart destroyed a finished, uncommitted issue.

## Routine registry (live state, verified 2026-10-23)
| Name | Trigger ID | Cron (UTC) | Binding | Notifications | Prompt gist |
|---|---|---|---|---|---|
| Daily AI newsletter | `trig_013uwjDfce9Eu4RkFBEmFkfQ` | `0 11 * * *` (fires ~11:01–11:16) | session-bound to `session_01JHEXp6dpeg5hK3DQGdj4eK` | none | Run the CLAUDE.md daily process; research, select ~10 stories, write today's UTC issue, update README, commit `Newsletter: YYYY-MM-DD`, push to default branch, work autonomously, don't redo a published date, close with the top-3 paragraph |

Enabled, no MCP connections attached. Last fired 2026-10-23T11:03:45Z
(last_run SUCCEEDED, which only means the wake was delivered, not that the
run finished); next 2026-10-24T11:01:56Z. Session-bound, so a container
reclaim orphans it; see `docs/OPERATIONS.md` §1 for the rebind procedure.

## Git topology — read before pushing
The session runs on branch `claude/ai-news-daily-newsletter-b67lp0`, not
`main`. Publish to **both**:

```
git push origin HEAD:main      # what readers see; CLAUDE.md step 6
git push -u origin HEAD        # the session branch; the stop hook counts it
```

Before pushing: `git fetch origin main` and confirm
`git merge-base --is-ancestor origin/main HEAD`; never force. Local `main`
drifts; resync it with `git branch -f main HEAD` after a publish.

## Decisions & constraints in force
- Repo is public: no secrets, tokens, or personal data in committed files.
- The `fact-check` skill is mandatory before every publish. A story that
  fails verification is dropped, never softened.
- Prefer a fuller issue (~12–15 items); on slow days widen the net before
  shortening, and never pad.
- Thematic sections are exclusive homes: government action → Regulation &
  Policy, money-led → Capital & Deals, physical buildout → Compute & Data
  Centers, property → AI in Real Estate (last section; outranks the others,
  but data centres stay in Compute). Section order follows the CLAUDE.md
  template.
- Current house style (since mid-October): items are `**[Headline](link)**:
  text` (colon, not em dash); Top Stories carry a paragraph, optional
  bullets, and a closing paragraph. Copy the previous day's issue for shape.
- Commit trailer: use the attribution lines from the session's system
  reminder (currently `Co-Authored-By: Claude Opus 5.5 …` plus the
  `Claude-Session:` line). Never put a model identifier anywhere else.
- Do not create pull requests unless explicitly asked.
- Process changes ship as commits to `CLAUDE.md`, not edits to the routine
  prompt.

## Recently changed
- `newsletters/2026-10-23.md` and `README.md` (`65d220c`): today's issue.
- `.claude/state/HANDOFF.md`: this file, replacing the 2026-09-23 version
  (a month stale; issues 09-24 through 10-22 were published without a
  handoff refresh).

## Open questions / risks
- **Open question the owner has not answered:** whether to change the AI in
  Real Estate floor from "two to four items" to "omit if nothing qualifies,
  otherwise one to four." Recent issues carry one item or none; do not pad.
- **Source traps seen 2026-10-23:**
  - Aggregator summaries got the CyberCartel/Straiker story backwards (they
    said Claude refusals were rerouted to Kimi; Straiker's report says Kimi
    refusals fell back to hard-coded local code). Read the primary.
  - Primary sources that need routing: the Straiker report URL is only in
    `straiker.ai/sitemap.xml`; Microsoft Security blog bodies don't render
    to `scripts/fetch.py` (use WebFetch, it works); Anthropic posts are
    findable via `anthropic.com/sitemap.xml`.
  - canva.com newsroom 403s to both clients; Canva Craft was dropped for
    lack of a readable company source. Worth adding to `docs/SOURCES.md`.
- **Running threads:** AI-run cyberattacks (ARTEX: South Korean banks on
  10-11, ConnectWise on 10-23; CyberCartel); PHP2Shell aftermath (top story
  10-22); OpenAI's ~$30B round at $1.25T pre-money (reported, not closed);
  Anthropic's IPO (S-1 rumoured "any day"); data-centre opposition (Finland,
  UK SAIL taskforce); agents and bank logins.
- **Source monoculture:** check the spread before publishing; weekends are
  when it happens.
- **Email deliverability is unverified** (sends succeed; whether they land
  in the inbox or spam is unknown — the runbook says check the spam folder).
- **README markers are fragile.** Always `grep -c` both markers before
  committing.
- Genuinely unreachable: Inman, SSRN, x.com, AP, Reuters, WSJ, Bloomberg,
  Axios (403 to fetch.py), canva.com. `docs/SOURCES.md` is the map.
