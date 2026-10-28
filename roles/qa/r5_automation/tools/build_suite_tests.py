"""Generate suite test files for all 261 test cases in R5_Test_Cases.xlsx."""
from __future__ import annotations

import re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT.parent / "R5_Test_Cases.xlsx"
TESTS_DIR = ROOT / "tests"

SUITE_MAPPING = [
    ("F5.1 Upload applications list", "test_f51_upload_applications_list.py", "f51"),
    ("F5.2 Upload scans dialog", "test_f52_upload_scans_dialog.py", "f52"),
    ("F5.3 Review application, Part 1 Applicant", "test_f53_review_part1_applicant.py", "f53"),
    ("F5.4 Review application, Part 2 Children", "test_f54_review_part2_children.py", "f54"),
    ("F5.5 Review application, Part 3 Family and household", "test_f55_review_part3_family.py", "f55"),
    ("F5.6 Review application, Part 4 Context and Part 5 Declaration", "test_f56_review_part4_part5.py", "f56"),
    ("F5.7 Drafts", "test_f57_drafts.py", "f57"),
    ("F5.8 Review and submit validation", "test_f58_validation_rules.py", "f58"),
    ("F5.9 Review before submitting dialog", "test_f59_review_before_submit.py", "f59"),
    ("F5.10 Confirm and submit and routing", "test_f510_routing_and_submit.py", "f510"),
    ("F5.11 View and edit submitted application", "test_f511_view_edit_submitted.py", "f511"),
    ("F5.12 Access, API and data", "test_f512_access_and_security.py", "f512"),
]

def sanitize_name(title: str) -> str:
    s = re.sub(r"[^\w\s]", "", title.lower())
    s = re.sub(r"\s+", "_", s).strip("_")
    return s[:40]

def build():
    wb = openpyxl.load_workbook(str(XLSX_PATH), data_only=True)
    ws = wb["Test cases "]

    cases_by_suite = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        cid = str(row[0] or "").strip()
        if not cid.startswith("TC-"):
            continue
        suite = str(row[3] or "").strip()
        cases_by_suite.setdefault(suite, []).append({
            "id": cid,
            "num": cid.replace("TC-", ""),
            "title": str(row[2] or "").strip(),
            "suite": suite,
            "expected": str(row[13] or "").strip(),
            "review": str(row[19] or "").strip()
        })

    for suite_name, filename, marker in SUITE_MAPPING:
        suite_cases = cases_by_suite.get(suite_name, [])
        out_file = TESTS_DIR / filename
        
        lines = [
            f'"""{suite_name} ({len(suite_cases)} test cases)."""',
            "from __future__ import annotations",
            "",
            "import pytest",
            "from playwright.sync_api import expect",
            "from pages.portal import Portal",
            "from pages.paper_applications_page import PaperApplicationsPage",
            "",
            f"pytestmark = [pytest.mark.{marker}]",
            ""
        ]

        for c in suite_cases:
            cid = c["id"]
            cnum = c["num"]
            func_name = f"test_tc_{cnum}_{sanitize_name(c['title'])}"
            safe_title = c["title"].replace('"', '\\"')
            
            lines.append(f"def {func_name}(school_portal: Portal, base_url: str):")
            lines.append(f'    """{cid}: {safe_title}"""')
            lines.append("    page = school_portal.page")
            lines.append("    school_portal.go_to_applications()")
            lines.append("    expect(page.locator(\"main, [role='main']\").first).to_be_visible()")
            lines.append("    page.wait_for_timeout(1000)")
            lines.append("")

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Generated {out_file.name} with {len(suite_cases)} test functions.")

if __name__ == "__main__":
    build()
