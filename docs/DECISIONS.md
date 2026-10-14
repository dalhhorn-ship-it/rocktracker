# Decision Log

Owner: `architect`. Newest first.

## 0001 Excel workbook as backend, Copilot Cowork portal as frontend
* Context: product team apps must be cheap to run and easy for non developers to own.
* Decision: one shared workbook is the source of truth; the factory builds and tests the workbook; the product owner builds the portal
  in Copilot Cowork from the deployed workbook and the portal pack.
* Consequences: the workbook schema is the contract and is tested on every change.
