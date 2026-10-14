---
description: Start a new project from docs/BRIEF.md (plan, design, first tasks)
model: opus
---

Kick off the software factory for this project. Follow CLAUDE.md.

1. Read `docs/BRIEF.md`. If the idea or users are missing, ask me before continuing.
2. Run the `brainstorm` agent to write `docs/BRAINSTORM.md`: purpose, objective, goals,
   options and challenges. Show me the recommendation, the main challenges and the
   questions, and wait for my answers. Record my answers and the chosen direction at the
   bottom of `docs/BRAINSTORM.md`.
3. Run the `pm` agent to write `docs/PRD.md` and a first `docs/PLAN.md` from the brainstorm.
4. Run the `architect` agent to write `schema/workbook.schema.json`, `docs/ARCHITECTURE.md`
   and `docs/DECISIONS.md`, and to refine the PLAN with acceptance criteria.
5. Run the `reviewer` agent on the PRD, schema and PLAN (spec, admin load, clarity).
6. Fix anything marked CHANGES, then show me: the PRD summary, the data model,
   the task graph, open questions and the upkeep budget. Wait for my go before `/build`.

$ARGUMENTS
