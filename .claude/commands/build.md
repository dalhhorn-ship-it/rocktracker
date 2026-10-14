---
description: Run the execution loop on the next ready tasks in docs/PLAN.md
model: sonnet
---

Run the execution loop from CLAUDE.md:

1. Read `docs/PLAN.md` and pick the next tasks whose dependencies are `done`.
2. Route each task with the "Model and agent routing" table in CLAUDE.md: inline for
   small edits, `scout` for mechanical work, `developer` for real build work.
   Run independent tasks in parallel. Give each agent the task id and file paths only.
3. For each result run the `reviewer` agent (review loop, max 3 rounds).
4. APPROVED: update the task to `done` in PLAN.md and commit.
   CHANGES: send findings back to the developer.
   BLOCKED: stop and bring the decision to me with options.
5. Repeat until no ready tasks remain or something is blocked.
6. Apply all PLAN status and debt count updates in one `scout` call.
7. Report: tasks done, test summary, tech debt changes, any model escalations, what is next.

$ARGUMENTS
