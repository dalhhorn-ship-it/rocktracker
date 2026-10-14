// Weekly snapshot (DECISIONS 0007). Appends one row per active rock to tbl_RockSnapshots and
// one row per epic of an active rock to tbl_EpicSnapshots. Safe to run twice on the same day:
// SnapshotIDs already present are skipped. Python mirror: scripts/snapshot.py.
// Names below must match schema/workbook.schema.json (tests/test_snapshot.py checks it).

const ROCKS_SHEET = "Rocks";
const EPICS_SHEET = "Epics";
const ROCK_SNAP_SHEET = "RockSnapshots";
const EPIC_SNAP_SHEET = "EpicSnapshots";
const ROCK_SNAP_TABLE = "tbl_RockSnapshots";
const EPIC_SNAP_TABLE = "tbl_EpicSnapshots";

// Columns copied from the Rocks sheet (same name in the snapshot table).
const ROCK_COPY_COLUMNS = [
  "RockID", "Rock", "GPM", "UpdateDate", "State", "MainMessage",
  "EpicsCommitted", "EpicsSlipped", "EpicsDelivered",
  "PositionsPlanned", "PositionsFilled", "OpenHighRisks"
];
// Rocks sheet column that feeds snapshot column "Rock".
const ROCK_NAME_SOURCE = "RockName";
// Columns copied from the Epics sheet.
const EPIC_COPY_COLUMNS = [
  "EpicKey", "RockID", "Title", "Commitment", "PlannedDate", "ForecastDate", "Status"
];
const ACTIVE_COLUMN = "Active";
const ACTIVE_VALUE = "Yes";
const ID_COLUMN = "SnapshotID";
const DATE_COLUMN = "SnapshotDate";

type Row = ExcelScript.RangeValue[];

function main(workbook: ExcelScript.Workbook): string {
  const now = new Date();
  const isoDay = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
  // Excel serial date of today (whole days).
  const serial = Math.round(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) / 86400000) + 25569;

  const rocks = readSheet(workbook, ROCKS_SHEET);
  const epics = readSheet(workbook, EPICS_SHEET);

  const activeRockIds = new Set<string>();
  const rockRows: Row[] = [];
  for (const r of rocks.rows) {
    const id = String(r[rocks.col(ROCKS_KEY())]);
    if (id === "" || String(r[rocks.col(ACTIVE_COLUMN)]) !== ACTIVE_VALUE) continue;
    activeRockIds.add(id);
    const out: Row = [isoDay + "|" + id, serial];
    for (const name of ROCK_COPY_COLUMNS) {
      const source = name === "Rock" ? ROCK_NAME_SOURCE : name;
      out.push(r[rocks.col(source)]);
    }
    rockRows.push(out);
  }

  const epicRows: Row[] = [];
  for (const r of epics.rows) {
    const key = String(r[epics.col("EpicKey")]);
    if (key === "" || !activeRockIds.has(String(r[epics.col("RockID")]))) continue;
    const out: Row = [isoDay + "|" + key, serial];
    for (const name of EPIC_COPY_COLUMNS) out.push(r[epics.col(name)]);
    epicRows.push(out);
  }

  const addedRocks = append(workbook, ROCK_SNAP_SHEET, ROCK_SNAP_TABLE, rockRows);
  const addedEpics = append(workbook, EPIC_SNAP_SHEET, EPIC_SNAP_TABLE, epicRows);
  return "Snapshot " + isoDay + ": " + addedRocks + " rock rows and " + addedEpics + " epic rows added.";
}

function ROCKS_KEY(): string {
  return "RockID";
}

function pad(n: number): string {
  return n < 10 ? "0" + n : String(n);
}

// Reads a consolidated sheet (header in row 1, spill below). Columns are found by header name.
function readSheet(workbook: ExcelScript.Workbook, sheetName: string) {
  const sheet = workbook.getWorksheet(sheetName);
  if (!sheet) throw new Error("Sheet not found: " + sheetName);
  const range = sheet.getUsedRange();
  const values = range ? range.getValues() : [];
  if (values.length === 0) throw new Error("Sheet is empty: " + sheetName);
  const header = values[0].map(v => String(v));
  return {
    rows: values.slice(1),
    col: (name: string): number => {
      const i = header.indexOf(name);
      if (i < 0) throw new Error("Column not found on " + sheetName + ": " + name);
      return i;
    }
  };
}

// Appends rows whose SnapshotID is not in the table yet. Returns the number added.
// Unprotects the sheet for the write and always protects it again.
function append(workbook: ExcelScript.Workbook, sheetName: string, tableName: string, rows: Row[]): number {
  const sheet = workbook.getWorksheet(sheetName);
  const table = workbook.getTable(tableName);
  if (!sheet) throw new Error("Sheet not found: " + sheetName);
  if (!table) throw new Error("Table not found: " + tableName);
  const idColumn = table.getColumnByName(ID_COLUMN);
  if (!idColumn) throw new Error("Column not found on " + tableName + ": " + ID_COLUMN);
  const existing = new Set<string>(idColumn.getRangeBetweenHeaderAndTotal().getValues().map(r => String(r[0])));
  const fresh = rows.filter(r => !existing.has(String(r[0])));
  if (fresh.length === 0) return 0;

  const wasProtected = sheet.getProtection().getProtected();
  if (wasProtected) sheet.getProtection().unprotect();
  try {
    table.addRows(null, fresh);
  } finally {
    sheet.getProtection().protect({ allowAutoFilter: true, allowSort: true });
  }
  return fresh.length;
}
