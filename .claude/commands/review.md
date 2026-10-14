---
description: Run the review loop on recent work or the whole project
model: sonnet
---

Run the `reviewer` agent.

* With no arguments: full milestone review across the whole project, including a Top 5.
  Run the reviewer with the model override `opus` for this one.
* With a task id or path in the arguments: review only that.

Then run the `pm` agent to reprioritise `docs/PLAN.md` from the findings, and give me
a short summary: verdicts, top findings, plan changes, tech debt trend.

$ARGUMENTS
