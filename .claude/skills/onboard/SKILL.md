---
name: onboard
description: Bootstrap a fresh session into a project expert — newsletter editorial craft, the routine-based automation architecture, hard constraints, and operating procedures. Use at the start of any new chat on this project, before making changes to routines or process, or whenever unsure how this project works.
---

# Onboard: become the AI_News project expert

This skill turns a context-free session into one that operates this project
like its long-time maintainer. Read everything in the load order, absorb the
expertise below, then confirm readiness in one short paragraph.

## Load order (read all, in this order)

1. `CLAUDE.md` — the editorial process, format, fact-check and link rules.
2. `docs/OPERATIONS.md` — the automation runbook: routines, IDs, schedules,
   failure modes, recovery recipes.
3. `.claude/state/HANDOFF.md` — last session's state (may not exist; if
   mid-task, prefer running the `resume` skill instead of this one).
4. The two most recent files in `newsletters/` — the house voice, calibrated.

## The three hard constraints (never violate, never re-ask)

1. **No Anthropic API key, no paid credits.** Everything runs through Claude
   Code sessions and scheduled Routines (Claude Code Remote triggers). Never
   propose GitHub Actions + API-key pipelines, scripts calling the Claude
   API, or anything that bills per-token outside the session.
2. **The repo is public.** Nothing sensitive goes in any committed file — no
   tokens, no email addresses, no personal data.
3. **Egress is policy-limited.** GitHub *write* API paths outside the MCP
   toolset are blocked (403) — repo settings, branch renames, etc. must be
   done by the user in the GitHub UI. Never retry a 403/407 policy denial;
   report it and route around it.

## Editorial expertise (what "good" means here)

- **A false story is worse than no issue; a wrong link is worse than no
  story.** The fact-check pass (`fact-check` skill) is mandatory, not
  advisory. The project once published a fabricated "Gemini 3.5 Pro launch"
  sourced from SEO speculation — the whole rules system descends from that.
- **Story selection is a ranking problem, not a collection problem.** ~10
  items max. A real model release beats a benchmark blog; a primary source
  beats three outlets rewriting each other; a signed deal beats a rumor of
  one. Slow day → shorter issue, never padding.
- **Voice**: neutral, concise, plain language. The editor's note is the only
  place for a point of view, and it's one or two sentences naming the day's
  single biggest theme. Everything readable in ~3 minutes.
- **Source hierarchy**: company blog/changelog/paper > first-tier press
  (Bloomberg, Reuters, FT, WSJ, TechCrunch, The Verge, Ars, MIT TR) >
  everything else. SEO farms, "what to expect" pages, and rolling aggregator
  feeds are never citable.

## Workflow-adaptation expertise (how to change the machine safely)

- The automation is **two Routines**: a session-bound *publish* routine
  (researches, writes, fact-checks, pushes — has git auth because it lives in
  a persistent session) and a fresh-session *relay* routine (fetches the
  published issue from the public raw URL 15 minutes later and emails it
  verbatim — fresh sessions can carry email notifications; session-bound ones
  cannot). Details and IDs: `docs/OPERATIONS.md`.
- **`update_trigger` cannot change a routine's prompt.** Prompt changes =
  delete + recreate (confirm the delete registered before recreating; check
  with `list_triggers` after any errored call to avoid duplicates).
- **Cron is UTC** on the server; the user thinks in their local time. State
  both when discussing schedules.
- Prefer changing `CLAUDE.md` over changing routine prompts: the publish
  routine's prompt intentionally defers to CLAUDE.md, so process changes ship
  as commits, not trigger surgery.
- After *any* routine change: update `docs/OPERATIONS.md` and run `handoff`.

## Operating habits

- Start non-trivial work by checking git state and the live trigger list —
  never assume the handoff or your memory matches reality.
- Commit messages: `Newsletter: YYYY-MM-DD` for issues, imperative one-liners
  otherwise. Push to the default branch (`main`). No PRs unless asked.
- Run `handoff` before compaction and at the end of any session that changed
  state.

## Confirmation

After loading, reply to the user with a one-paragraph readiness summary: the
current latest issue, the live routine schedule, and any drift or risk you
noticed while loading. Then await (or continue) the actual task.
