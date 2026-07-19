---
name: handoff
description: Write durable session state to .claude/state/HANDOFF.md so work survives context compaction, session loss, or container reclaim. Use before/after compaction, when ending a work session mid-task, after changing any routine, or whenever significant decisions were made that a future session must know.
---

# Write a session handoff

Context compaction and container reclaim silently destroy conversational
memory. This skill persists what matters to `.claude/state/HANDOFF.md` in the
repo, so any future session (or this one, post-compact) can pick up exactly
where things stand. The companion skill is `resume`.

## When to run

- Before a `/compact`, or right after one (while the summary is still fresh).
- Before ending a session with work in flight.
- Immediately after changing anything about the scheduled routines
  (create/delete/update) — routine state lives outside the repo and is
  otherwise invisible to future sessions.
- After any decision with the user that changes how the project operates.

## What to write

Overwrite `.claude/state/HANDOFF.md` with exactly these sections (omit a
section only if truly empty):

```markdown
# Session handoff — YYYY-MM-DD HH:MM UTC

## Current task
What is being worked on right now, and its precise status. "Done" is a
status. Include the concrete next action if mid-task.

## Routine registry (live state, verify on resume)
One row per scheduled routine: name | trigger ID | cron (UTC) | binding
(session-bound / fresh-session) | notifications | prompt gist.

## Decisions & constraints in force
Standing decisions from the user that a fresh session must not re-litigate
or violate. Keep each to one line with the reason.

## Recently changed
Files/routines touched this session and why (one line each).

## Open questions / risks
Anything unresolved, plus known failure modes currently live.
```

## Rules

- **Overwrite, don't append** — the file is current state, not a log. History
  lives in git.
- **No secrets, tokens, or personal data** (no email addresses — refer to
  "the configured notification email" instead). The repo is public.
- **Facts, not narrative.** Write for a reader with zero conversational
  context. Name things fully (trigger IDs, file paths, branch names).
- **Commit and push** the file to the default branch with message
  `Handoff: YYYY-MM-DD HH:MM UTC`. An unpushed handoff dies with the
  container. If unrelated work is also uncommitted, commit the handoff file
  separately.
