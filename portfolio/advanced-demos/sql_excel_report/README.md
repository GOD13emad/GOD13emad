# SQL-to-Excel reporting: synthetic one-report example

**Demo only.** This work uses 12 fictional transactions, not information from a customer, and was not sold or delivered under contract.

The example builds an Excel workbook containing the synthetic input rows, a category-level report, and reconciliation formulas. The expected aggregate is 12 records, 27 units, and 8,092,000 fictional toman. The original workbook was checked with three passing reconciliations.

[Python source code](build_synthetic_pilot.py)

The script uses `artifact_tool` and can be run in an environment with that dependency:

```bash
python build_synthetic_pilot.py --output synthetic_one_report.xlsx
```

The public code is a simplified source variant of the tested workbook and should be run again in the intended execution environment. It does not connect to SQL Server, operate a scheduler, or implement the four financial reports described in a separate marketplace listing.

## One independently priced pilot

After a client supplies an authorized, sanitized sample, a target Excel format and a written acceptance rule, a one-report extraction/mapping/checking milestone can be scoped. Commercial rates, timing, data rights and payment terms are determined before execution.

[Engineering services and professional contact](../../../ENGINEERING_SERVICES.md)
