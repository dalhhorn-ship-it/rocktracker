// Minimal ExcelScript declarations, only what snapshot.ts uses (enough for tsc --noEmit).
// The real Office Scripts runtime provides the full API.
declare namespace ExcelScript {
  type RangeValue = string | number | boolean;
  interface ProtectionOptions {
    allowAutoFilter?: boolean;
    allowSort?: boolean;
    allowFormatCells?: boolean;
  }
  interface WorksheetProtection {
    getProtected(): boolean;
    protect(options?: ProtectionOptions, password?: string): void;
    unprotect(password?: string): void;
  }
  interface Range {
    getValues(): RangeValue[][];
  }
  interface TableColumn {
    getName(): string;
    getRangeBetweenHeaderAndTotal(): Range;
  }
  interface Table {
    getName(): string;
    getHeaderRowRange(): Range;
    getColumnByName(name: string): TableColumn | undefined;
    addRows(index: number | null, values: RangeValue[][]): void;
  }
  interface Worksheet {
    getName(): string;
    getUsedRange(): Range | undefined;
    getProtection(): WorksheetProtection;
  }
  interface Workbook {
    getWorksheet(name: string): Worksheet | undefined;
    getTable(name: string): Table | undefined;
  }
}
