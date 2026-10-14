Open each file in Excel for the web, in this order, and note which ones show a repair or critical issues message.
1_full is the real deployment workbook; 6_bare has no dynamic arrays, conditional formats, validation, names or notes.
2 has no dynamic array formulas, 3 no conditional formats, 4 no data validation, 5 no defined names (and no dropdown lists).
The variant that opens cleanly while 1_full does not points at the cause; if only 6_bare opens, the cause is in sheets, tables or styles.
Reply with the list of file names that asked for repair (and, if Excel shows it, the repair log text), and say whether 1_full still does.
