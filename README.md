# Claude Central

A reusable GitHub template for building work applications for the product team with a
small team of Claude agents.

* **Backend:** one shared Excel workbook, the single source of truth.
* **Frontend:** a portal you build yourself in Microsoft Copilot Cowork once the workbook
  is deployed, in the Editorial Portfolio design system (`design/DESIGN_SYSTEM.md`).
* **Factory:** agents that brainstorm, plan, design, build, test and review, using the
  cheapest model that can do each job well.

**Who builds what**

| Claude (this repository) | You |
| :--- | :--- |
| Brainstorm, PRD, plan, data model | Answer brainstorm questions, approve the plan |
| The Excel workbook, ready to deploy (`dist/`) | Upload it to the shared drive, set permissions |
| `PORTAL_BUILD.md`: complete build instructions for Copilot Cowork | Build the portal in Copilot Cowork |
| Tests, reviews, tech debt overview, migrations | Report what worked into `/retro` |

The full operating model lives in `CLAUDE.md`. This README is the how to.

---

## 1. One time setup of this template

1. Merge the setup work into the default branch (`main`) of `dalhhorn-ship-it/claudecentral`.
2. On GitHub open **Settings → General** and tick **Template repository**.
   You now get a green **Use this template** button on the repository page.

---

## 2. Start a new project

1. **Create the project repository.** On `dalhhorn-ship-it/claudecentral` click
   **Use this template → Create a new repository**. Give it a clear name
   (for example `roadmap-hub`). Keep it private.
2. **Open it in Claude Code.** Either on the web at claude.ai/code (pick the new
   repository) or locally:
   ```
   git clone https://github.com/<you>/<project>.git
   cd <project>
   claude
   ```
3. **Fill in the brief.** Edit `docs/BRIEF.md`: idea, users, requirements, where the
   workbook will live, upkeep budget, deadline. Rough is fine; the brainstorm will challenge it.
4. **Run `/kickoff`.** This runs, in order:
   * `brainstorm`: purpose, objective, goals, options and challenges. It stops and asks you
     questions. Answer them and pick a direction.
   * `pm`: writes the PRD and the task plan from your chosen direction.
   * `architect`: designs the workbook schema and the portal spec.
   * `reviewer`: checks it all, then you get a summary and approve.
5. **Run `/build`** to build the next ready tasks. Repeat until the plan is done.
   Each task is built, tested and reviewed before it counts as done.
6. **Run `/review`** at each milestone for a full review and a reprioritised plan.
7. **Run `/handoff`.** Claude runs all tests and builds the standard handoff package in
   `dist/<title>/` (and a zip of it). Download the zip.
8. **Deploy the workbook.** Follow the package `README.md`: upload the workbook to the shared
   drive (SharePoint, Teams or OneDrive), set editors and readers, enter the first real data.
9. **Build the portal in Copilot Cowork.** Attach `PORTAL_BUILD.md` and `preview.html`, link
   the live workbook and ask: *Build the portal described in PORTAL_BUILD.md.* Check the
   result with the checklist at the end of that file.
10. **Run `/retro`** at the end (or after a big milestone) to feed learnings back into this
   template. See section 5.

---

## 3. Daily use

| You want to | Do this | Runs on |
| :--- | :--- | :--- |
| Think through a new idea or major feature | `/brainstorm <topic>` | opus |
| Start a project from the brief | `/kickoff` | opus |
| Build the next tasks | `/build` | sonnet |
| Review recent work or the whole project | `/review` or `/review T7` | sonnet (milestone review on opus) |
| Build the handoff package | `/handoff` | sonnet |
| Change the structure after deployment | change via `/build`, then `/handoff "<downloaded live file>"` | sonnet |
| Capture learnings, improve the template | `/retro` | opus |
| Run all tests | `./scripts/test.sh` | none |
| Rebuild sample workbook | `python3 scripts/build_workbook.py` | none |
| Rebuild deployment workbook | `python3 scripts/build_workbook.py --deploy` | none |
| Regenerate portal preview | `python3 scripts/render_preview.py` | none |

### The team

| Agent | Role | Model |
| :--- | :--- | :--- |
| `brainstorm` | Purpose, objective, goals, options and challenges before the PRD | opus |
| `pm` | Product Manager: admin light systems, strategic clarity, PRD and plan | opus |
| `architect` | Solution Architect: workbook schema, portal spec, decisions | opus |
| `developer` | Builds, owns and runs the test system, keeps the tech debt overview | sonnet |
| `reviewer` | Review loop: verifies every task before it counts as done | sonnet |
| `scout` | Mechanical work: lookups, test runs, status updates | haiku |

### Keeping token spend low

The routing rules are in `CLAUDE.md` under "Model and agent routing". In practice:
* Small, clear edits are done inline, without spinning up an agent.
* Mechanical work goes to `scout` on haiku.
* Opus is used for direction setting (brainstorm, PRD, architecture, milestone reviews)
  and as an escalation after a real failure, not by default.
* If you start a session yourself, sonnet is a good default; switch to opus with `/model`
  for kickoff and retro if your command did not already do it.

---

## 4. What is where

| Path | What | Who changes it |
| :--- | :--- | :--- |
| `docs/BRIEF.md` | Your input | you |
| `docs/BRAINSTORM.md` | Purpose, goals, challenges, chosen direction | `brainstorm` |
| `docs/PRD.md`, `docs/PLAN.md` | What we build and the task graph | `pm` |
| `schema/workbook.schema.json` | The workbook contract | `architect` |
| `portal/portal.spec.json` | The portal contract (tabs, KPIs, charts) | `architect` |
| `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` | Design and decision log | `architect` |
| `data/sample.json`, `data/workbook.xlsx` | Sample data and sample workbook, synthetic only | `developer` |
| `dist/<title>/` and `.zip` | The handoff package (generated, see below) | `developer` (via `/handoff`) |
| `docs/DEPLOY.md` | Deployment log and how to change the live workbook | `developer` (via `/handoff`) |
| `tests/`, `scripts/` | Test system and generators | `developer` |
| `docs/TECH_DEBT.md` | Tech debt overview | `developer` |
| `docs/REVIEW_LOG.md` | Review verdicts | `reviewer` |
| `design/` | Design system and tokens | template (change via `/retro`) |
| `CLAUDE.md`, `.claude/` | Operating model, agents, commands | template (change via `/retro`) |

Never put real personal data or secrets in the repository. The live workbook stays in
SharePoint or OneDrive.

### The standard handoff package

Every project ends with the same package in `dist/<title>/`:

| File | What it is | Use it for |
| :--- | :--- | :--- |
| `<title>.xlsx` | The workbook: tables, dropdowns, About sheet, lookups filled in | Upload to the shared drive |
| `README.md` | What is in the package and the steps to go live | Read first |
| `PORTAL_BUILD.md` | Complete portal build instructions: data model, pages, KPIs, charts, colours, checklist | Give to Copilot Cowork |
| `preview.html` | What the portal should look like, on sample data | Visual reference for you and Cowork |
| `DESIGN_SYSTEM.md` | Full design system reference | Detail when checking the portal |

The package is generated from the schema and portal spec, so it always matches what was
built and tested.

### After the workbook is live

The live workbook holds real data, so it is never replaced by a fresh build. To change
its structure: make the change here (schema first), download the live file, and run
`/handoff "<downloaded file>"`. Claude migrates your data into the new structure, warns
about anything that would be dropped, and you upload the result as a new version of the
same file. Details in `docs/DEPLOY.md`.

---

## 5. Improving this template from project learnings

Every project should make the next one easier. There are two levels of learning:

* **Project level:** lessons specific to one app. They live in the project's
  `CLAUDE.md` under "Lessons learned" and in its `docs/`.
* **Template level:** lessons that would help every future project. They are promoted
  into this repository and logged in `TEMPLATE_LEARNINGS.md`.

### How to do it

1. While you work, add lessons to "Lessons learned" in the project's `CLAUDE.md`
   (the agents do this too when something fails).
2. At the end of the project, or after a big milestone, run `/retro` in the project.
   You can add your own notes: `/retro the portal tabs were too many for leadership`.
3. `/retro` reads the lessons, review log, tech debt and decisions, sorts each learning
   into "project only" or "template", and writes `docs/RETRO.md` with concrete proposed
   changes to template files.
4. You choose which proposals to accept. For those, Claude opens a pull request on
   `dalhhorn-ship-it/claudecentral` titled `Retro: <project>` and logs them in
   `TEMPLATE_LEARNINGS.md`. If it cannot reach the template repository, it leaves a
   patch with instructions in `docs/RETRO.md`.
5. Review and merge the pull request. Every new project created from the template
   after that gets the improvement.

Good candidates for the template: a test you wished existed, an agent rule that kept being
broken, a better default schema or portal pattern, a design system gap, a routing rule that
wasted tokens. Poor candidates: anything about one specific dataset or team.

### Pulling template improvements into an existing project (optional)

Projects created with **Use this template** do not share git history with it. To bring the
latest template files into a running project:

```
git remote add template https://github.com/dalhhorn-ship-it/claudecentral.git
git fetch template
git checkout template/main -- .claude design scripts tests/conftest.py tests/test_schema.py \
  tests/test_workbook.py tests/test_portal.py tests/test_deploy.py tests/test_handoff.py
./scripts/test.sh
```

Then compare `CLAUDE.md` by hand (keep your project's "Lessons learned" section) and commit.

---

## 6. Tests

```
pip install -r requirements.txt
python3 scripts/build_workbook.py
./scripts/test.sh
```

The test system has six automated layers: schema, workbook against schema, business
rules from the PRD, portal spec against the workbook and design system, the deployment
workbook (dropdowns, About sheet, migration keeps every row), and the handoff package
(PORTAL_BUILD.md covers every table, column, page, KPI and chart). You smoke test the portal in
Copilot Cowork.
