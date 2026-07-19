# AI_News — Daily AI Newsletter

This repo publishes a concise daily newsletter about the day's key AI news.
A scheduled Claude Code session runs every morning, researches the news, and
commits the issue. If you are that session, follow the process below exactly.

## Daily newsletter process

1. **Research the last 24 hours of AI news** using web search and web fetch.
   Cover these angles (run multiple searches — one angle won't find everything):
   - Major AI lab announcements: Anthropic, OpenAI, Google DeepMind, Meta AI,
     Mistral, xAI, Hugging Face (check their blogs/newsrooms)
   - Tech press: TechCrunch, VentureBeat, The Verge, Ars Technica, MIT Tech Review
   - Industry/business: funding rounds, acquisitions, chips (NVIDIA etc.),
     regulation and policy
   - Research: notable new papers, benchmarks, open-source model releases
   - Community: what's trending on Hacker News about AI/LLMs
2. **Select the ~10 most important stories.** Prefer primary sources. Skip
   rumors, reposts, and incremental minor updates. Deduplicate stories covered
   by multiple outlets — link the best single source.
3. **Write the issue** to `newsletters/YYYY-MM-DD.md` (today's date, UTC).
   If the file already exists, overwrite it.
4. **Fact-check the draft (mandatory — run the `fact-check` skill).** Every
   claim in the issue must survive verification before publishing. A story
   that fails is removed, not softened. See "Fact-checking rules" below.
5. **Update the index in `README.md`**: set the "Latest issue" link and add a
   row to the top of the Archive table.
6. **Commit and push** to the repository's default branch with the message
   `Newsletter: YYYY-MM-DD`.

## Issue format

```markdown
# AI News — Monday, July 20, 2026

> One- or two-sentence editor's note: the single biggest theme of the day.

## Top Stories

### [Story headline](https://source-link)
2–3 sentences: what happened and why it matters. Plain language, no hype.

(3–5 top stories)

## Research & Models

- **[Paper/model name](link)** — one sentence on what it is and why it's notable.

## Product & Industry

- **[Item](link)** — one sentence.

## Quick Hits

- [Headline](link) — a few words of context.
```

## Fact-checking rules (strict — a false story is worse than no issue)

A published error already happened once: an issue led with "Google launches
Gemini 3.5 Pro" sourced from SEO articles speculating about a *rumored* launch
date. Google had launched nothing. These rules exist so that never repeats.

- **Verify the event, not just the link.** For every launch/release/funding
  claim, confirm it on a primary source (the company's own blog, changelog,
  press release, or paper) before publishing. "An article says X happened" is
  not confirmation that X happened.
- **The primary-source test for launches**: if a company supposedly shipped
  something and there is no trace on the company's own site, the story is
  false or premature — drop it.
- **Rumor-pattern kill list.** Never source a story from pages matching these
  patterns; their presence is a red flag for the whole story:
  - "What to expect", "release date: everything we know", "rumors & leaks",
    "targets \<date\>", "(Updated \<month\>)" evergreen-SEO pages
  - Local-news or content-farm domains covering global tech (e.g. a regional
    outlet "reporting" a Google launch)
  - Prediction/aggregator sites (coursiv, cometapi, findskill-style blogs)
- **Cross-check numbers.** Parameter counts, valuations, round sizes, dates:
  confirm the number appears in the cited source itself, not just somewhere.
- **Future-dated ≠ happened.** "X is expected/slated/targeted for \<date\>"
  never becomes "X launched" — even if the date has passed. Only report a
  launch after confirming it occurred.
- **The header date must be right**: the day-of-week must match the date, and
  the date must be today (UTC).
- **If a published issue is later found wrong**: fix the story (usually remove
  it), update README lines that reference it, and append a dated *Correction*
  note at the bottom of the issue. Never silently rewrite history.

## Link rules (strict — a wrong link is worse than no story)

- **Verify every link before publishing**: fetch each URL (web fetch) and confirm
  the page actually covers the story it's cited for. If it doesn't, find a
  better source or drop the story.
- **Never link rolling aggregator or list pages** (news roundups, "latest deals"
  trackers, leaderboard/news feeds like `.../ai-news`, `.../latest-vc-deals`,
  weekly "biggest rounds" posts). Their content changes daily, so the link rots
  immediately. Link a dated, single-story article instead.
- **Prefer primary sources**: the company's own announcement/blog post, the
  paper, or the official press release; otherwise a dated article from a
  reputable outlet.

## Style rules

- Concise beats complete: the whole issue should be readable in ~3 minutes.
- Every item links to its source. No item without a link.
- Neutral, factual tone. No breathless hype, no editorializing beyond the
  editor's note.
- If it's a genuinely slow news day, a shorter issue is fine — never pad.

## README index format

`README.md` contains two markers the daily session must maintain:

- The line after `<!-- latest -->` holds the link to the newest issue.
- New archive rows go directly under `<!-- archive -->` (newest first), as
  `| YYYY-MM-DD | [Read](newsletters/YYYY-MM-DD.md) | one-line top story |`.

## Project skills & operations

Project skills live in `.claude/skills/` (invoke with `/<name>`):

- `onboard` — start here in any fresh session: loads full project expertise
  (editorial craft, architecture, constraints).
- `fact-check` — the mandatory pre-publish verification pass (step 4 above).
- `handoff` — write durable session state to `.claude/state/HANDOFF.md` before
  compaction or ending a work session mid-task.
- `resume` — restore state from the handoff file when continuing work.

`docs/OPERATIONS.md` is the runbook for the automation itself: the scheduled
routines, their IDs and schedules, failure modes, and recovery steps. Read it
before touching any routine, and update it whenever a routine changes.
