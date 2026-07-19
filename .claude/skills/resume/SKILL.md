---
name: resume
description: Restore working state from .claude/state/HANDOFF.md at the start of a session or after context compaction. Reads the handoff, verifies it against reality (git, routines, repo files), and continues the task. Use when starting a fresh session on this project or when post-compact context feels incomplete.
---

# Resume from a handoff

The companion skill to `handoff`. Reconstructs working state from
`.claude/state/HANDOFF.md`, then verifies it before acting — a handoff is a
snapshot and may be stale.

## Process

1. **Read the handoff**: `.claude/state/HANDOFF.md`. If it's missing, fall
   back to: `git log --oneline -15`, `README.md`, `docs/OPERATIONS.md`, and
   the routine list (step 3) — then tell the user there was no handoff and
   summarize the state you reconstructed.

2. **Check its age.** The header carries a timestamp. If the handoff is older
   than the most recent git commits, the commits win — read them
   (`git log --stat` since the handoff date) and note what changed after the
   handoff was written.

3. **Verify the routine registry against live state.** List the actual
   triggers (Claude Code Remote `list_triggers`) and diff against the
   handoff's registry: IDs, cron, enabled state, next_run. Routines are the
   part of this system that silently drifts (a fired run_once disables
   itself; a reclaimed container orphans session-bound routines). Report any
   mismatch — and check `docs/OPERATIONS.md` for the recovery recipe.

4. **Verify repo state**: `git status` + `git log --oneline -5`; confirm the
   branch is the default branch and in sync with origin. Confirm the newest
   `newsletters/` file matches README's "Latest issue" line.

5. **Continue the task.** The handoff's "Current task" section names the next
   action. Re-state to the user in one short paragraph: what the state is,
   what you verified, any drift found, and what you're doing next — then do
   it. Honor everything under "Decisions & constraints in force" without
   re-asking.

## Rules

- **Never trust the handoff over observed reality.** Verified live state
  always wins; say so when they disagree.
- **Don't re-litigate settled decisions** listed in the handoff. The user
  already decided them.
- If you complete the resumed task or materially change state, finish by
  running `handoff` again so the file stays current.
