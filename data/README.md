# Data

The workbook lives here as `workbook.xlsx` (path set in `schema/workbook.schema.json`).
Synthetic sample data only. The live workbook stays in SharePoint or OneDrive.

## sample.json (schema 2.1.0)

Rocks hold profile, update with Attention1 to 3, and the blocks Milestones, Risks,
CallOuts, Decisions and Teams. Snapshots are RockSnapshots and MilestoneSnapshots in
schema column order. Today is 2026-10-14 (MC26Q3 current, MC26Q4 next). Cases:
R01 has 6 open requests and an express pay milestone completed today; R02 a Completed
milestone without an actual date and a decided row with open follow up; R03 an overdue
MC26Q2 milestone, an Off track slip into MC26Q4, a milestone in MC27Q1 and a team over
budget; R04 is half filled with no attention lines and a team with Budgeted 0; R05 is
inactive. Full list in `tests/test_sample.py`.
