---
name: fact-check
description: Mandatory pre-publish verification pass for a draft newsletter issue. Use before every commit of a newsletter, or when auditing an already-published issue for errors. Verifies every claim against primary sources, kills rumor-based stories, and checks links, numbers, and dates.
---

# Fact-check a newsletter issue

You are the fact-checker of record. Your job is to try to **kill** stories, not
to confirm them. A story survives only if it withstands your attempt to refute
it. The bar: *a false story is worse than no issue*.

Input: a draft at `newsletters/YYYY-MM-DD.md` (or a published issue to audit).

## Process

Work through the issue item by item — every Top Story, Research item, Product
item, and Quick Hit. For each item, do all four checks:

### 1. Event check (did it actually happen?)

- For any **launch, release, or announcement**: fetch the company's own
  channel — blog, newsroom, changelog, model docs, GitHub, or official social
  post. If the company's own surface has no trace of it, the story is false or
  premature. **Drop it.** Third-party articles claiming a launch are not
  evidence a launch happened.
- For **funding/M&A**: confirm on the company's announcement or a dated
  article from a first-tier outlet (Bloomberg, Reuters, FT, WSJ, TechCrunch,
  The Information). One SEO blog repeating a number is not confirmation.
- For **papers/models**: fetch the arXiv page / model card and confirm it
  exists and says what the item claims.

### 2. Source-quality check

Kill the story (or find a better source) if the cited page matches the
rumor-pattern list:

- Titles like "what to expect", "release date", "everything we know",
  "rumors & leaks", "targets \<date\>", "(Updated \<month\>)".
- Local/regional news domains or content farms covering global tech events.
- Prediction blogs, AI-generated news mills, aggregator/leaderboard feeds,
  rolling list pages ("latest deals", "/ai-news").
- Anything where the page's own text hedges ("expected", "reportedly",
  "rumored", "slated", "could") while the newsletter item states it as done.

### 3. Number-and-detail check

Fetch the cited source and confirm the specific figures in the item appear in
it: parameter counts, context windows, valuations, round sizes, dates, names
of investors/partners. A detail the source doesn't contain gets removed from
the item even if the story itself is real.

### 4. Link check

- The URL resolves and the page covers **this** story (not a homepage,
  category feed, or different article).
- The link is a dated, single-story page — never a rolling aggregator.
- Prefer swapping in the primary source if the check surfaced one.

## Issue-level checks (after the per-item pass)

- Header: day-of-week matches the date; date is today (UTC); title format
  matches CLAUDE.md.
- The editor's note only references stories that survived.
- Cross-references between items still make sense (e.g. "hours before X's
  launch" must not reference a story you just killed).
- README "Latest issue" line and archive row match the surviving top story.

## Verdict and output

Produce a short report before publishing:

```
FACT-CHECK: newsletters/YYYY-MM-DD.md
✔ kept:    N items (verified against primary/first-tier sources)
✎ edited:  list items whose text or link changed, with reason
✘ dropped: list killed stories, each with the one-line reason
```

Rules of engagement:

- **Drop, don't soften.** A story that fails verification is removed entirely
  — never downgraded to hedged wording ("reportedly launched").
- **When uncertain, drop.** A thinner issue is fine; a wrong one is not.
- If fact-checking an **already-published** issue and something fails: fix the
  file, fix README, and append a dated `*Correction (…):*` note at the bottom
  of the issue. Never silently rewrite history.
