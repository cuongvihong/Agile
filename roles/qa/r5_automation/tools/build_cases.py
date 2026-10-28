"""Generate data/cases.py from the case workbook (R5_Test_Cases.xlsx)."""
from __future__ import annotations

import pprint
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT.parent / "R5_Test_Cases.xlsx"

def build():
    wb = openpyxl.load_workbook(str(XLSX_PATH), data_only=True)
    ws = wb["Test cases "]
    cases = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        cid = str(row[0] or "").strip()
        if cid.startswith("TC-"):
            cases[cid] = {
                "id": cid,
                "scenario_id": str(row[1] or "").strip(),
                "title": str(row[2] or "").strip(),
                "suite": str(row[3] or "").strip(),
                "page": str(row[4] or "").strip(),
                "severity": str(row[5] or "").strip(),
                "priority": str(row[6] or "").strip(),
                "env": str(row[9] or "").strip(),
                "preconditions": str(row[10] or "").strip(),
                "test_data": str(row[11] or "").strip(),
                "steps": str(row[12] or "").strip(),
                "expected": str(row[13] or "").strip(),
                "review": str(row[19] or "").strip()
            }

    out_file = ROOT / "data" / "cases.py"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write('"""Metadata for all 261 test cases from R5_Test_Cases.xlsx."""\nfrom __future__ import annotations\n\nCASES = ')
        pprint.pprint(cases, stream=f, sort_dicts=False, width=120)
    print(f"Generated {out_file} with {len(cases)} cases.")

if __name__ == "__main__":
    build()
