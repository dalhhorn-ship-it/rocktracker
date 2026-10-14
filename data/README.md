# Data

The workbook lives here as `workbook.xlsx` (path set in `schema/workbook.schema.json`).
Synthetic sample data only. The live workbook stays in SharePoint or OneDrive.

## sample.json (schema 2.3.0)

Rocks hold profile, update with Attention1 to 3, and the blocks Milestones, Risks,
CallOuts, Decisions and Teams. Snapshots are RockSnapshots and MilestoneSnapshots in
schema column order. Today is 2026-10-14 (MC26Q3 current, MC26Q4 next). Cases:
R01 has 6 open requests and an express pay milestone completed today; R02 a Completed
milestone without an actual date and a decided row with open follow up; R03 an overdue
MC26Q2 milestone, an Off track slip into MC26Q4, a milestone in MC27Q1 and a team over
budget; R04 is half filled with no attention lines and a team with Budgeted 0; R05 is
inactive. Full list in `tests/test_sample.py`.

Schema 2.3.0 cases (checked by `test_sample_covers_every_quarter_ahead_and_slip_severity`):
* QuarterAhead covers 1, 2, 3 and 4 and blank. 1 is the current MC quarter (MC26Q3, and an
  overdue milestone from an earlier quarter), 4 is MC27Q2; a milestone beyond the horizon and an
  undated one have a blank QuarterAhead (the undated one stays visible as Not dated yet).
* SlipSeverity covers Major (a Slipped milestone whose forecast falls in a later MC quarter than
  planned, for example the R03 slip into MC26Q4), Minor (Slipped within the same quarter) and
  blank (every milestone that is not Slipped).
* The sample also carries Progress and Owner values (schema 2.2.0), including a typed 0.
