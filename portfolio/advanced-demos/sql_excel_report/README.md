# SQL-to-Excel reporting: runnable synthetic one-report example

**Status:** A self-authored demonstration with 12 fictional transactions. This is **not** an accepted customer contract, an implementation of the customer's SQL schema, a paid delivery or evidence of collected revenue.

The program creates three Excel worksheets: `Scope_And_Readme`, `Synthetic_Inputs` and `One_Report_Pilot`. The report contains category summaries, formula-based totals and three reconciliation indicators. Python independently checks the exact fictional input records, sums and spreadsheet formula structure.

## Reproduce

Requires Python 3.10+ and `openpyxl` (tested on the owner's Windows machine with Python 3.14.7 and openpyxl 3.1.5).

```bash
python -m pip install openpyxl
python build_synthetic_pilot.py --output synthetic_one_report.xlsx
```

**Verified owner-machine run, 30 Oct 2026:** Script executed successfully, produced an 8,080-byte workbook containing 3 worksheets and 12 fictional input records. Independent Python assertions checked 27 units and the synthetic gross of **8,092,000 toman**; workbook formulas and report-acceptance cell structure were verified by reading the saved file. Output: `PASS`. Formula *results* are set to calculate when opened in Excel; the Python run checks formula presence and internal data but does not execute Excel's calculation engine.

[Review the full Python generator and validation](build_synthetic_pilot.py).

## Scope and commercial prerequisites

The sample uses only invented records: no SQL Server, SARB accounting instance, confidential ledger, customer credentials, automatic scheduler or real client source files. It implements one illustrative Excel report, not four custom financial reports.

A genuine **paid** pilot requires the prospective buyer's authorized sanitized input sample or restricted read-only SQL view, target template, written acceptance and error tolerances, license/rights confirmation, viable fixed price and funded escrow/approved prepayment before substantive client work. Further reports are separate milestones unless explicitly contracted.

[Engineering services and professional contact](../../../ENGINEERING_SERVICES.md).
