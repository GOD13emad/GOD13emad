#!/usr/bin/env python3
"""Generate a reproducible Excel pilot from 12 FICTIONAL rows; NOT a client deliverable.

Requires an environment with artifact_tool (the same workbook engine used for this
verified demonstration). No SQL, network, customer data, or credentials are accessed.
"""
from pathlib import Path
import argparse
from artifact_tool import Workbook, SpreadsheetFile

ROWS = [
    ("2026-10-01", "Parts", "SYN-001", 2, 480000),
    ("2026-10-02", "Services", "SYN-002", 1, 670000),
    ("2026-10-03", "Tools", "SYN-003", 3, 120000),
    ("2026-10-04", "Parts", "SYN-004", 1, 950000),
    ("2026-10-06", "Services", "SYN-005", 2, 375000),
    ("2026-10-07", "Tools", "SYN-006", 4, 98000),
    ("2026-10-09", "Parts", "SYN-007", 2, 320000),
    ("2026-10-11", "Services", "SYN-008", 3, 225000),
    ("2026-10-12", "Tools", "SYN-009", 1, 710000),
    ("2026-10-14", "Parts", "SYN-010", 5, 89000),
    ("2026-10-18", "Services", "SYN-011", 1, 1250000),
    ("2026-10-21", "Tools", "SYN-012", 2, 145000),
]
EXPECTED_TOMAN = sum(qty * price for _, _, _, qty, price in ROWS)
assert len(ROWS) == len({row[2] for row in ROWS}) == 12
assert EXPECTED_TOMAN == 8092000

def create_workbook(output: Path) -> None:
    wb = Workbook.create()
    info = wb.worksheets.add("Scope_And_Readme")
    source = wb.worksheets.add("Synthetic_Inputs")
    report = wb.worksheets.add("One_Report_Pilot")
    dark = {"fill": "#17456C", "font": {"bold": True, "color": "#FFFFFF"}}
    for sh in (info, source, report):
        sh.get_range("A1:G1").format = dark
        sh.freeze_panes.freeze_rows(3)
    info.get_range("A1").values = [["Synthetic SQL-to-Excel reporting pilot - NOT client data"]]
    info.get_range("A3:B9").values = [
        ["Field", "Evidence or gate"],
        ["Input", "12 fictional transaction records only"],
        ["Output", "One by-category Excel report, formula-based"],
        ["No access", "No SARB/SQL Server, credentials or private schema"],
        ["Test", "Gross sums, record counts and unique references"],
        ["Not implemented", "Scheduler, four client reports or deployment"],
        ["Commercial prerequisite", "Approved inputs, escrow and written acceptance"],
    ]
    info.get_range("A3:B3").format = dark
    info.get_range("A3:A9").format.column_width = 26
    info.get_range("B3:B9").format.column_width = 67
    info.get_range("B3:B9").format.wrap_text = True
    info.get_range("A3:B9").format.row_height = 26
    source.get_range("A1").values = [["Only SYNTHETIC rows - no real financial information"]]
    source.get_range("A3:G3").values = [[
        "Date", "Category", "Reference", "Quantity", "Unit price (toman)", "Gross", "State",
    ]]
    source.get_range("A3:G3").format = dark
    for index, (date, category, ref, qty, price) in enumerate(ROWS, 4):
        source.get_range(f"A{index}:E{index}").values = [[date, category, ref, qty, price]]
        source.get_range(f"F{index}").formulas = [[f"=D{index}*E{index}"]]
        source.get_range(f"G{index}").values = [["Posted"]]
    source.get_range("A17").values = [["Synthetic gross total"]]
    source.get_range("F17").formulas = [["=SUM(F4:F15)"]]
    source.get_range("A3:A17").format.column_width = 19
    source.get_range("B3:C17").format.column_width = 19
    source.get_range("D3:D17").format.column_width = 13
    source.get_range("E3:F17").format.column_width = 24
    source.get_range("E4:F17").set_number_format("#,##0")
    report.get_range("A1").values = [["One-report paid-pilot demonstration - FICTIONAL"]]
    report.get_range("A3:D3").values = [[
        "Category", "Records", "Units", "Gross sales (toman)",
    ]]
    report.get_range("A3:D3").format = dark
    for index, cat in enumerate(("Parts", "Services", "Tools"), 4):
        report.get_range(f"A{index}").values = [[cat]]
        report.get_range(f"B{index}").formulas = [[f"=COUNTIF(Synthetic_Inputs!$B$4:$B$15,A{index})"]]
        report.get_range(f"C{index}").formulas = [[f"=SUMIF(Synthetic_Inputs!$B$4:$B$15,A{index},Synthetic_Inputs!$D$4:$D$15)"]]
        report.get_range(f"D{index}").formulas = [[f"=SUMIF(Synthetic_Inputs!$B$4:$B$15,A{index},Synthetic_Inputs!$F$4:$F$15)"]]
    report.get_range("A8").values = [["All categories"]]
    report.get_range("B8:D8").formulas = [["=SUM(B4:B6)", "=SUM(C4:C6)", "=SUM(D4:D6)"]]
    report.get_range("A11").values = [["Total reconciliation"]]
    report.get_range("B11").formulas = [['=IF(Synthetic_Inputs!F17=D8,"PASS","FAIL")']]
    report.get_range("A12").values = [["12 records reconciled"]]
    report.get_range("B12").formulas = [['=IF(COUNTA(Synthetic_Inputs!C4:C15)=B8,"PASS","FAIL")']]
    report.get_range("A13").values = [["Reference IDs unique"]]
    checks = ",".join(
        f"COUNTIF(Synthetic_Inputs!$C$4:$C$15,Synthetic_Inputs!C{i})=1"
        for i in range(4, 16)
    )
    report.get_range("B13").formulas = [[f'=IF(AND({checks}),"PASS","FAIL")']]
    report.get_range("A3:A13").format.column_width = 29
    report.get_range("B3:C13").format.column_width = 16
    report.get_range("D3:D13").format.column_width = 27
    report.get_range("D4:D8").set_number_format("#,##0")
    output.parent.mkdir(parents=True, exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(output))
    print(f"GENERATED {output} | SYNTHETIC_GROSS_TOMAN={EXPECTED_TOMAN} | ROWS={len(ROWS)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("synthetic_one_report.xlsx"))
    create_workbook(parser.parse_args().output)
