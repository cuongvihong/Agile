"""Read the 35 Gavin cases of UAT Master 01 into data/master01_cases.json.

Usage (from the suite folder):  python tools/extract_master.py ["..\\uat-master_1 (1).xlsx"]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT.parent / "uat-master_1 (1).xlsx"


def main(path: Path) -> None:
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb["Tests"]
    cases = {}
    for row in ws.iter_rows(values_only=True):
        if not row or not row[0] or not str(row[0]).startswith("UAT"):
            continue
        if "Gavin" not in str(row[3] or ""):
            continue
        cases[str(row[0]).strip()] = {
            "title": row[1], "area": row[2], "owner": row[3], "role": row[4],
            "setup": row[5], "steps": row[6], "status_in_master": row[7],
        }
    out = ROOT / "data" / "master01_cases.json"
    out.write_text(json.dumps(cases, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(cases)} cases written to {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT)
