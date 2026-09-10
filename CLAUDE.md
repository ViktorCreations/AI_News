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
   - Real estate: AI in property — valuation and appraisal standards,
     mortgage/underwriting rules from the GSEs and housing regulators,
     rent-setting and its litigation, property management and tenant
     operations, proptech funding. Search this angle separately every day;
     it rarely surfaces in general AI coverage.
2. **Select the ~12–15 most important stories** (owner preference: a fuller
   issue beats a minimal one). Prefer primary sources. Skip rumors, reposts,
   and incremental minor updates. Deduplicate stories covered by multiple
   outlets — link the best single source. On slow days widen the net —
   research papers, policy, embodied AI/robotics, community items, and
   well-dated context for running stories — before shortening the issue;
   never fill the quota with unverifiable or stale-as-new items.
   **No-repeat rule**: before selecting, read the last 7 issues in
   `newsletters/` (and grep them for each candidate's company/product
   names). A story covered in a prior issue may return ONLY if there is a
   genuinely new development — and then the item must lead with the delta
   ("weights released, as promised July 18", "the talks reported Sunday
   have closed") and link a source for the new event, not the old one.
   Aggregator roundups constantly re-surface old news as fresh; a date on
   the event itself, not on the article, is what counts.
3. **Write the issue** to `newsletters/YYYY-MM-DD.md` (today's date, UTC).
   If the file already exists, overwrite it.
4. **Fact-check the draft (mandatory — run the `fact-check` skill).** Every
   claim in the issue must survive verification before publishing. A story
   that fails is removed, not softened. See "Fact-checking rules" below.
5. **Update the index in `README.md`**: set the "Latest issue" link and add a
   row to the top of the Archive table.
6. **Commit and push** to the repository's default branch with the message
   `Newsletter: YYYY-MM-DD`.
7. **Email the issue**: run
   `scripts/zoho_send.sh newsletters/YYYY-MM-DD.md` — it converts the issue
   to HTML (via `scripts/md2email.py`) and sends it through the Zoho Mail
   REST API using OAuth credentials in `~/.zoho_mail_api` (outside the
   repo; see `docs/OPERATIONS.md` for setup/recovery). The email body must
   be the published issue, byte-for-byte in content. Fallback if the script
   fails: the Zoho Mail connector tools (`mcp__ZohoMCP__ZohoMail_*` via
   ToolSearch) when available in an interactive session. If neither path
   works, still publish steps 1–6 and note the email failure in the run
   summary.

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

## Compute & Data Centers

- **[Item](link)** — one sentence (capacity, hardware, location, timeline).

## Regulation & Policy

- **[Item](link)** — one sentence (who ordered/proposed what, scope, deadlines).

## Capital & Deals

- **[Item](link)** — one sentence (round size, valuation, acquirer/target, key terms).

## Quick Hits

- [Headline](link) — a few words of context.

## AI in Real Estate

- **[Item](link)** — one sentence (what changed, for whom, dated).
```

**Thematic section rules** (Compute & Data Centers, Regulation & Policy,
Capital & Deals, AI in Real Estate): each is the EXCLUSIVE home for its
beat, capped at the **top 5** by importance (AI in Real Estate: top 4) —
drop the rest, never overflow into other sections. Omit any section with
no fresh qualifying items, except AI in Real Estate, which has its own
rules below.

- **Capital & Deals**: every money-led story — funding rounds, M&A, IPOs,
  valuations, market-cap moves, and deals whose substance is the contract
  value.
- **Regulation & Policy**: government and regulatory action — legislation,
  binding orders, export controls, standards/oversight bodies, government
  model reviews, intergovernmental AI organizations.
- **Compute & Data Centers**: the physical buildout — data-center
  construction and capacity milestones, chip/fab news, AI supercomputer
  deployments, energy for AI. (If the story is the deal value, it goes to
  Capital & Deals instead; if it's regulatory action about chips, it goes
  to Regulation & Policy.)
- **AI in Real Estate**: the last section in the issue, and the exclusive
  home for AI in the property business — it **outranks the other thematic
  sections** when the story is about real estate, so a proptech round goes
  here rather than Capital & Deals and a GSE or housing-agency AI rule goes
  here rather than Regulation & Policy. Covers: valuation and pricing
  (AVMs, appraisal standards), market trend and forecasting claims,
  mortgage and underwriting (lender AI governance, credit models, rates),
  day-to-day management (leasing, rent-setting, tenant screening,
  maintenance triage, service charges and other tenant expense, arrears and
  eviction), AI acting as agent or virtual property manager, brokerage and
  listing portals, construction tech, and the litigation and regulation
  specific to these. **Data centers stay in Compute & Data Centers** even
  though they are land, power and buildings — siting, capacity and energy
  are AI infrastructure, not the real-estate business. A housing-market
  story with no AI in it does not belong in this newsletter at all.

**AI in Real Estate — beat-specific rules.** This beat moves far slower
than frontier AI and will not produce a story every day. Do not pad it.

- **Window**: draw from the **last 30 days**, not 24 hours, and date every
  item explicitly ("effective August 6", "filed May 14"). Two to four items.
- **Context items**: when there is no fresh news, up to two items may be
  labelled `Context:` and give dated background on a live issue — a rule
  already on the books, an active case, a deadline coming up, a funded
  company's actual operating numbers. Never undated evergreen assertion.
- **Sourcing is the hard part here.** This query space is dominated by
  vendor content marketing and affiliate SEO: "best AI property management
  software 2026", "the complete guide to AI in real estate", consultancy
  market-size reports with CAGRs. All of it is auto-kill under the
  rumor-pattern list, and none of its statistics may be quoted — including
  market-size and "AVM median error rate" figures, which trace back to
  research mills. Require a dated primary source (a GSE lender letter or
  announcement, a regulator or agency document, a court filing, a company
  press release or earnings call) or a bylined, dated article from
  first-tier press or established trade press (Inman, HousingWire,
  Multifamily Dive, National Mortgage News, The Real Deal, Bisnow, Sifted,
  The Negotiator).

Top Stories, Research & Models, Product & Industry, and Quick Hits carry
the rest: product/model launches, research, security, community. Judgment
call: when money or policy is incidental to a strategic/product event, the
story may live elsewhere with the fact mentioned in passing. On days when
the thematic sections absorb most of the news, fewer than 3 Top Stories is
acceptable.

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
- If it's a genuinely slow news day, widen the net (step 2) before shortening;
  a somewhat shorter issue is a last resort — never pad with weak items.

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
