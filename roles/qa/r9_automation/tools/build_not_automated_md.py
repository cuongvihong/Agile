"""Sinh docs/NOT_AUTOMATED.md: bảng markdown các case chưa tự động hóa, để chép sang Excel.
Chạy sau tools/build_coverage.py:  python tools/build_not_automated_md.py"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from data.cases import CASES  # noqa: E402
from data.not_automated import NOT_AUTOMATED  # noqa: E402

OVERRIDE = {"TC-027": "FS theo hóa đơn, UI theo khoản phí", "TC-134": "FS theo hóa đơn, UI theo khoản phí",
            "TC-160": "UI hoặc API không có phần EA do client đặt"}


def group(case_id: str, reason: str) -> str:
    if case_id in OVERRIDE:
        return OVERRIDE[case_id]
    t = reason.lower()
    if "cơ sở dữ liệu" in t:
        return "Ràng buộc cơ sở dữ liệu, cần SQL"
    if "tiêm lỗi" in t:
        return "Cần tiêm lỗi vào cổng thanh toán hoặc hạ tầng"
    if "f9.6" in t:
        return "F9.6 webhook và đối soát"
    if "ô nhập phần education account" in t or "số tiền từng phần" in t or "ui không cho chỉnh" in t:
        return "UI hoặc API không có phần EA do client đặt"
    if "mô hình hóa đơn" in t:
        return "FS theo hóa đơn, UI theo khoản phí"
    if "phụ huynh thứ hai" in t or "persona" in t or "guardian thứ hai" in t or "hai phụ huynh" in t:
        return "Cần phụ huynh hoặc persona thứ hai"
    if "dữ liệu" in t:
        return "Thiếu dữ liệu mẫu"
    return "Khác"


def cell(x) -> str:
    return re.sub(r"\s+", " ", str(x or "")).replace("|", "/").strip()


def main() -> None:
    rows = sorted(NOT_AUTOMATED.items(), key=lambda kv: int(kv[0].split("-")[1]))
    out = [f"# Danh sách {len(rows)} case R9 chưa tự động hóa", "",
           f"Nguồn case: sổ test case R9 hiện hành ({len(CASES)} case, `data/cases.py`). Nguồn lý do: `data/not_automated.py`. "
           "Mỗi dòng ứng với một case, chép bảng sang Excel được ngay.", "",
           "| STT | ID | Tiêu đề | Test Suite | Severity | Review Status | Assumption Ref | Nhóm lý do | Lý do chi tiết |",
           "|---|---|---|---|---|---|---|---|---|"]
    counts: collections.Counter = collections.Counter()
    for i, (case_id, reason) in enumerate(rows, 1):
        m = CASES.get(case_id, {})
        g = group(case_id, reason)
        counts[g] += 1
        out.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            i, case_id, cell(m.get("title")), cell(m.get("suite")), cell(str(m.get("severity", "")).split(" ")[0]),
            cell(m.get("review")), cell(m.get("assumption"))[:60], g, cell(reason)))
    out += ["", "## Tổng theo nhóm lý do", "", "| Nhóm lý do | Số case |", "|---|---|"]
    out += [f"| {g} | {n} |" for g, n in counts.most_common()]
    out.append(f"| Tổng | {sum(counts.values())} |")
    (ROOT / "docs" / "NOT_AUTOMATED.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"đã ghi docs/NOT_AUTOMATED.md ({len(rows)} case)")


if __name__ == "__main__":
    main()
