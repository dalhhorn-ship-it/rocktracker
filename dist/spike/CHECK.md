# Spike check: consolidation in Excel for the web (5 minutes)

Needed by Thu 15 Oct 2026, 12:00. File: `consolidation_spike.xlsx` (test data only).

1. Upload `consolidation_spike.xlsx` to the SharePoint site where Rock Tracker will live. Open it in the browser (Excel for the web), not the desktop app.
2. Look at the opening. Note whether Excel shows any message such as "We found a problem with some content" or "repaired".
3. Open sheet `Epics`. Expected: header row Key, Title, Status, Rock, then four rows below it (R01-E01, R01-E02, R02-E01, R02-E02) spilled from cell A2. Click A2: the formula bar shows one formula starting `=LET(`. Note any `#NAME?`, `#VALUE!`, `#SPILL!` or `#CALC!`.
4. Open sheet `Epics_C2`. Expected: the same four rows. Note errors the same way.
5. Open sheet `RockTemplate`, right click the tab, choose Duplicate (Move or Copy, create a copy). Check the copy sits between `RockTemplate` and `RocksEnd`; if not, drag it there.
6. On the copy, type `TEST-1` in cell A5, then a title in B5. Go to `Epics` and check a fifth row `TEST-1` appears within a few seconds. Do the same check on `Epics_C2` (this one only sees the copy after you type its tab name in `RockTabs`, cell A4).
7. Only if step 3 failed or the file was repaired: on `Epics`, click A2, delete it, then type this into A2 and press Enter: `=LET(d,VSTACK(RockTemplate:RocksEnd!A5:D9),k,CHOOSECOLS(d,1),FILTER(d,ISTEXT(k)*(k<>""),""))`. Note whether it spills four rows or shows an error (copy the exact text).

## What to report back

* **A**: opens with no repair, `Epics` spills 4 rows, the duplicated tab adds row `TEST-1`. Reply "A". Plan A stays.
* **A2**: Excel repaired the file or `Epics` did not spill, but typing the formula in step 7 works and spills. Reply "A2" and say which (repair message or no spill).
* **C**: typing the formula in step 7 is rejected or errors (for example `#NAME?` or "formula has a problem" on the 3D reference). Reply "C" with the exact error text or a screenshot. If `Epics_C2` works, say so: that tells us C2 is available.
* **C2**: `Epics` fails as in C, and Power Automate is blocked in your tenant (you cannot create flows) or you know it will be. Reply "C2" and say whether `Epics_C2` showed the four rows.

No answer by 12:00 means we continue with A plus A2 and flag the risk in the deploy notes.
