---
description: Capture project learnings and propose improvements to the Claude Central template
model: opus
---

Run a retrospective and decide what this project should teach the template.

## 1. Gather (use `scout` for the reading)
* "Lessons learned" in `CLAUDE.md`
* `docs/REVIEW_LOG.md` (repeated findings, BLOCKED verdicts, round 3 reviews)
* `docs/TECH_DEBT.md` (debt that came from the template, not the project)
* `docs/DECISIONS.md` (decisions you would make the same way on every project)
* Model escalations and agents that kept failing, from build reports
* Anything I tell you in the arguments below

## 2. Sort each learning into one bucket
* **Project only:** specific to this app or data. Stays in this repo.
* **Template:** would help every future project. Examples: a missing test, an agent
  rule that kept being broken, a better default in the schema or portal spec, a
  design system gap, a routing rule that wasted tokens, a missing doc template.

Be strict: only promote a learning that you would expect to hit again on a different project.

## 3. Write `docs/RETRO.md`
For each template learning: the evidence (where it bit us), the proposed change,
the exact files in the template to change, and the expected effect. Keep project
only learnings in a short list at the bottom.

## 4. Propose the template change
Template files are: `CLAUDE.md` (everything except "Lessons learned"), `.claude/`,
`design/`, `scripts/`, `tests/` (except `test_business_rules.py`),
the empty doc templates in `docs/` and `README.md`.

Show me the proposals and ask which to send. For the approved ones:
1. Ask me for the template repository if it is not in `TEMPLATE_LEARNINGS.md` (default `dalhhorn-ship-it/claudecentral`).
2. Make the changes on a new branch of the template repository, never in this project's history.
3. Add one entry per learning to `TEMPLATE_LEARNINGS.md` in the template.
4. Run the template's `./scripts/test.sh` and open a pull request titled `Retro: <project name>`.
   If you cannot reach the template repository, leave the changes as a patch in
   `docs/RETRO.md` with instructions so I can apply them myself.

$ARGUMENTS
