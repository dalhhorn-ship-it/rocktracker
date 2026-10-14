# Product portfolio hub: deployment package

Version 0.1.0 · built 14 Oct 2026 · tests: 30 passed in 0.26s

This package holds everything needed to put the workbook live and build its portal.

## What is in it

| File | What it is | Who uses it |
| :--- | :--- | :--- |
| `Product portfolio hub.xlsx` | The workbook (backend). Lookups filled in, no sample data. | Upload to the shared drive |
| `PORTAL_BUILD.md` | Complete build instructions for the portal | Give to Copilot Cowork |
| `preview.html` | What the portal should look like, on sample data | Open in a browser; give to Copilot Cowork |
| `DESIGN_SYSTEM.md` | Full design system reference | Copilot Cowork, and you when checking |

## Steps

### 1. Put the workbook live
1. Upload `Product portfolio hub.xlsx` to the shared drive (SharePoint, Teams or OneDrive). Keep the file name as it is.
2. Give edit rights only to the people who maintain the data; everyone else read only.
3. Check version history is on (it is by default on SharePoint and OneDrive).
4. Open the About sheet: it lists every sheet, its owner and the editing rules.
5. Enter or paste the first real data. Use the dropdowns; pink cells are required and still empty.

### 2. Build the portal in Copilot Cowork
1. Open Copilot Cowork.
2. Attach `PORTAL_BUILD.md` and `preview.html`, and link the live workbook (not a local copy).
3. Ask: *Build the portal described in PORTAL_BUILD.md.*
4. Check the result against `preview.html` and the checklist in section 6 of `PORTAL_BUILD.md`.
5. If Cowork lists anything under "Could not build", note it for the next `/retro`.

### 3. Keep it running
* Edit data in the workbook only; the portal follows after refresh.
* Never rename, reorder or delete sheets or columns: the portal depends on them.
* Need a new column, sheet or page? Ask for it in the factory repository. You will get a new
  package with a migrated copy of your live workbook, so no data is lost.

## Contents at a glance

| Sheet | Purpose | Owner |
| :--- | :--- | :--- |
| lkp_Status | Allowed status values | architect |
| Goals | Strategic goals the team commits to | Head of Product |
| Initiatives | Work that delivers a goal | Product Managers |

| Portal page | Question it answers |
| :--- | :--- |
| 1 | Where do we stand? |
| 2 | The full list |
