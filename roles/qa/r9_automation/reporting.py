"""Báo cáo theo case R9: sau mỗi lần chạy cho biết CASE nào có vấn đề để sửa.

pytest-html (report.html) liệt kê theo tên hàm test. Plugin này gom kết quả theo mã case TC-xxx của
R9_Test_Cases_final_FS09.xlsx, kèm tiêu đề, suite, severity, review status của case, rồi ghi:
  artifacts/reports/r9_case_report.html   mở bằng trình duyệt, mục "Cần xử lý" nằm trên cùng
  artifacts/reports/r9_case_report.csv    mở bằng Excel (UTF-8 có BOM)

Test gắn với case nhờ tên hàm (test_tc_046_..., test_tc_004_tc_005_...) và, với case chưa tự động hóa,
nhờ tham số case_id của tests/test_not_automated.py. Tiêu đề và severity lấy từ data/cases.py do
tools/build_coverage.py sinh từ workbook, nên báo cáo không cần openpyxl lúc chạy.
"""
from __future__ import annotations

import csv
import html
import re
from collections import defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "artifacts" / "reports"
RESULT_DIR = ROOT / "artifacts" / "test-results"

try:  # data/cases.py do tools/build_coverage.py tạo
    from data.cases import CASES
except Exception:  # noqa: BLE001
    CASES = {}

CASE_HEAD = re.compile(r"((?:test_)?(?:tc_\d{3}_?)+)")

RECS: dict[str, dict] = {}
DESELECTED: dict[str, set[str]] = {}

# (khóa, nhãn, lớp màu, thứ tự ưu tiên cần xử lý)
VERDICTS = {
    "fail": ("FAIL, cần xem", "bad", 1),
    "xpass": ("XPASS, có thể đã hết lỗi", "warn", 2),
    "known": ("LỖI ĐÃ BIẾT, chờ sửa", "known", 3),
    "pass": ("ĐẠT", "ok", 4),
    "skip": ("BỎ QUA", "muted", 5),
    "notauto": ("CHƯA TỰ ĐỘNG HÓA", "muted", 6),
    "notrun": ("KHÔNG CHẠY LẦN NÀY", "muted", 7),
}
ATTENTION = ("fail", "xpass", "known")


# ------------------------------------------------------------------ thu kết quả
def case_ids_of(item) -> list[str]:
    spec = getattr(item, "callspec", None)
    if spec is not None and item.get_closest_marker("not_automated") and "case_id" in spec.params:
        return [str(spec.params["case_id"])]
    name = getattr(item, "originalname", None) or item.name
    match = CASE_HEAD.match(name)
    if not match:
        return []
    return ["TC-" + n for n in re.findall(r"tc_(\d{3})", match.group(1))]


def _squash(text: str, limit: int = 700) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _skip_reason(rep) -> str:
    longrepr = rep.longrepr
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return _squash(str(longrepr[2]).removeprefix("Skipped: "))
    return _squash(str(longrepr))


def pytest_deselected(items):
    for item in items:
        markers = {m.name for m in item.iter_markers()}
        for case_id in case_ids_of(item):
            DESELECTED.setdefault(case_id, set()).update(markers)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    rec = RECS.setdefault(item.nodeid, dict(
        nodeid=item.nodeid, name=item.name, cases=case_ids_of(item), markers={m.name for m in item.iter_markers()},
        outcome=None, detail="", reason="", duration=0.0))
    rep.r9_cases = rec["cases"]
    rec["duration"] += rep.duration
    message = _squash(call.excinfo.exconly()) if call.excinfo is not None else ""
    wasxfail = getattr(rep, "wasxfail", None)
    if rep.when == "setup":
        if rep.failed:
            rec.update(outcome="error", detail=message or _squash(str(rep.longrepr)))
        elif rep.skipped:
            rec.update(outcome="skipped", detail=_skip_reason(rep))
    elif rep.when == "call":
        if rep.skipped and wasxfail is not None:
            rec.update(outcome="xfailed", reason=_squash(wasxfail), detail=message)
        elif rep.skipped:
            rec.update(outcome="skipped", detail=_skip_reason(rep))
        elif rep.failed:
            rec.update(outcome="failed", detail=message or _squash(str(rep.longrepr)))
        elif rep.passed:
            rec.update(outcome="xpassed" if wasxfail is not None else "passed", reason=_squash(wasxfail or ""))
    elif rep.when == "teardown" and rep.failed and rec["outcome"] in (None, "passed"):
        rec.update(outcome="error", detail="Lỗi ở bước dọn dẹp: " + (message or _squash(str(rep.longrepr))))


# ------------------------------------------------------------------ cột phụ cho report.html của pytest-html
def pytest_html_results_table_header(cells):
    try:
        cells.insert(2, '<th class="sortable" data-column-type="case">Case R9</th>')
    except Exception:  # noqa: BLE001
        pass


def pytest_html_results_table_row(report, cells):
    try:
        cells.insert(2, '<td class="col-case">%s</td>' % html.escape(", ".join(getattr(report, "r9_cases", []) or ["—"])))
    except Exception:  # noqa: BLE001
        pass


# ------------------------------------------------------------------ gom theo case
def _number(case_id: str) -> int:
    try:
        return int(case_id.split("-")[1])
    except (IndexError, ValueError):
        return 10_000


def _severity_rank(meta: dict) -> int:
    match = re.match(r"S(\d)", str(meta.get("severity", "")))
    return int(match.group(1)) if match else 9


def _slug(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", nodeid.replace("::", "-")).strip("-").lower()


def _evidence(nodeid: str) -> list[tuple[str, str]]:
    """Ảnh chụp và trace do pytest-playwright giữ khi test thất bại, nếu có."""
    if not RESULT_DIR.exists():
        return []
    slug = _slug(nodeid)
    folder = RESULT_DIR / slug
    if not folder.exists():
        near = [p for p in RESULT_DIR.iterdir() if p.is_dir() and (p.name.startswith(slug[:90]) or slug.startswith(p.name[:90]))]
        folder = near[0] if near else None
    if folder is None:
        return []
    out = []
    for pattern, label in (("*.png", "ảnh"), ("trace.zip", "trace")):
        for path in sorted(folder.glob(pattern))[:1]:
            out.append((label, "../test-results/%s/%s" % (folder.name, path.name)))
    return out


def decide(case_id: str, recs: list[dict]) -> tuple[str, str, dict]:
    """Trả về (khóa kết luận, chi tiết, bản ghi tiêu biểu) cho một case."""
    if not recs:
        kinds = DESELECTED.get(case_id, set())
        if kinds & {"mutating", "destructive", "online"}:
            return "notrun", ("Test ghi dữ liệu thật hoặc cần simulator, chế độ này không chạy. "
                              "Chạy bằng run_r9_automation.cmd pay (hoặc destructive)."), {}
        return "notrun", "Không chọn chạy trong lần này (lọc bằng -m hoặc -k).", {}
    for rec in recs:
        if "not_automated" in rec["markers"]:
            return "notauto", rec["detail"], rec
    outs = [r["outcome"] for r in recs]

    def first(kind: str) -> dict:
        return next(r for r in recs if r["outcome"] == kind)

    if "failed" in outs or "error" in outs:
        rec = first("failed" if "failed" in outs else "error")
        return "fail", rec["detail"], rec
    if "xpassed" in outs:
        rec = first("xpassed")
        return "xpass", "Test known_defect lại ĐẠT, nghĩa là lệch này có thể đã được sửa. Kiểm lại rồi gỡ nhãn known_defect. Lý do cũ: " + rec["reason"], rec
    if "xfailed" in outs:
        rec = first("xfailed")
        return "known", rec["reason"], rec
    if "passed" in outs:
        skipped = [r for r in recs if r["outcome"] == "skipped"]
        note = ""
        if skipped:
            note = "%d test của case bị bỏ qua: %s" % (len(skipped), skipped[0]["detail"])
        return "pass", note, recs[0]
    rec = recs[0]
    return "skip", rec["detail"], rec


def build():
    by_case: dict[str, list[dict]] = defaultdict(list)
    extras = []
    for rec in RECS.values():
        if rec["cases"]:
            for case_id in rec["cases"]:
                by_case[case_id].append(rec)
        else:
            extras.append(rec)
    ids = sorted(set(CASES) | set(by_case) | set(DESELECTED), key=_number)
    rows = []
    for case_id in ids:
        meta = CASES.get(case_id, {})
        recs = by_case.get(case_id, [])
        key, detail, rec = decide(case_id, recs)
        tests = [r["name"] for r in recs if "not_automated" not in r["markers"]]
        rows.append(dict(id=case_id, meta=meta, verdict=key, detail=detail, observed=rec.get("detail", "") if key == "known" else "",
                         tests=tests, nodeid=rec.get("nodeid", ""), n_tests=len(tests),
                         n_pass=sum(1 for r in recs if r["outcome"] in ("passed", "xpassed"))))
    return rows, extras


# ------------------------------------------------------------------ ghi báo cáo
def _e(text) -> str:
    return html.escape(str(text if text is not None else ""))


def _hint(row: dict) -> str:
    case_id = row["id"]
    num = case_id.split("-")[1] if "-" in case_id else case_id
    if row["verdict"] == "fail":
        return ("Chạy lại riêng: run_r9_automation.cmd tc %s. So Expected của case với màn thật. "
                "Màn đúng mà test sai thì sửa test, màn sai thì ghi lỗi cho Dev." % num)
    if row["verdict"] == "known":
        return "Màn thật lệch với R9 đúng như lý do. Đưa Dev hoặc BA quyết định sửa bản build hay sửa case."
    if row["verdict"] == "xpass":
        return "Chạy lại riêng: run_r9_automation.cmd tc %s, nếu vẫn đạt thì gỡ known_defect khỏi test." % num
    return ""


def _row_html(row: dict) -> str:
    label, css, _ = VERDICTS[row["verdict"]]
    meta = row["meta"]
    detail = _e(row["detail"])
    if row["observed"]:
        detail += '<div class="obs"><b>Quan sát lần chạy:</b> %s</div>' % _e(row["observed"])
    hint = _hint(row)
    if hint:
        detail += '<div class="hint">%s</div>' % _e(hint)
    links = " ".join('<a href="%s">%s</a>' % (_e(url), _e(name)) for name, url in _evidence(row["nodeid"])) if row["verdict"] in ("fail",) else ""
    count = "%d/%d đạt" % (row["n_pass"], row["n_tests"]) if row["n_tests"] else ""
    return ('<tr class="r-%s"><td class="id">%s</td><td>%s<div class="sub">%s</div></td><td>%s</td><td><span class="chip %s">%s</span>'
            '<div class="sub">%s</div></td><td class="detail">%s</td><td class="tests">%s%s</td></tr>') % (
        row["verdict"], _e(row["id"]), _e(meta.get("title", "(không có trong workbook)")), _e(meta.get("suite", "")),
        _e(str(meta.get("severity", "")).split(" ")[0]) + '<div class="sub">%s</div>' % _e(meta.get("review", "")),
        css, _e(label), _e(count), detail, "<br>".join(_e(t) for t in row["tests"]), ("<br>" + links) if links else "")


def _table(rows: list[dict]) -> str:
    head = ("<table><thead><tr><th>Case</th><th>Tiêu đề / Suite</th><th>Severity / Review</th><th>Kết quả</th>"
            "<th>Chi tiết</th><th>Test</th></tr></thead><tbody>%s</tbody></table>")
    return head % "\n".join(_row_html(r) for r in rows)


CSS = """
:root{--bg:#fff;--fg:#1d2733;--mut:#5d6b7a;--line:#d9e0e7;--bad:#c62828;--warn:#b26a00;--known:#9a4d00;--ok:#2e7d32;--card:#f5f7fa}
@media(prefers-color-scheme:dark){:root{--bg:#14181d;--fg:#e6ebf0;--mut:#9aa7b5;--line:#2c3540;--bad:#ef6a6a;--warn:#e0a040;--known:#e8a060;--ok:#6fbf73;--card:#1c232b}}
body{margin:0;padding:20px 16px 60px;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1280px;margin:0 auto}h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}
.meta{color:var(--mut);margin-bottom:14px}.tiles{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px;min-width:110px}
.tile b{display:block;font-size:22px}.tile.bad b{color:var(--bad)}.tile.warn b{color:var(--warn)}.tile.known b{color:var(--known)}.tile.ok b{color:var(--ok)}
table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
th{background:var(--card);position:sticky;top:0}.id{white-space:nowrap;font-weight:600}.sub{color:var(--mut);font-size:12px}
.chip{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;font-weight:600;border:1px solid currentColor}
.chip.bad{color:var(--bad)}.chip.warn{color:var(--warn)}.chip.known{color:var(--known)}.chip.ok{color:var(--ok)}.chip.muted{color:var(--mut)}
.detail{max-width:520px;word-break:break-word}.obs{margin-top:4px;color:var(--mut)}.hint{margin-top:4px;font-style:italic;color:var(--mut)}
.tests{font-size:12px;color:var(--mut);word-break:break-all;max-width:300px}details{margin-top:10px}summary{cursor:pointer;font-weight:600;padding:6px 0}
input{padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);width:min(420px,100%)}
@media(max-width:700px){.tests{display:none}}
"""

JS = """
document.getElementById('q').addEventListener('input',function(e){var t=e.target.value.toLowerCase();
document.querySelectorAll('tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(t)<0?'none':''});});
"""


def write_reports(rows: list[dict], extras: list[dict], when: str) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    counts = {k: sum(1 for r in rows if r["verdict"] == k) for k in VERDICTS}
    attention = sorted((r for r in rows if r["verdict"] in ATTENTION),
                       key=lambda r: (VERDICTS[r["verdict"]][2], _severity_rank(r["meta"]), _number(r["id"])))
    tiles = "".join('<div class="tile %s"><b>%d</b>%s</div>' % (VERDICTS[k][1], counts[k], _e(VERDICTS[k][0])) for k in VERDICTS)
    extra_rows = ""
    for rec in extras:
        outcome = {"passed": ("ĐẠT", "ok"), "failed": ("FAIL, cần xem", "bad"), "error": ("LỖI", "bad"), "xfailed": ("LỖI ĐÃ BIẾT", "known"),
                   "xpassed": ("XPASS", "warn"), "skipped": ("BỎ QUA", "muted")}.get(rec["outcome"], ("?", "muted"))
        extra_rows += '<tr><td>%s</td><td><span class="chip %s">%s</span></td><td class="detail">%s</td></tr>' % (
            _e(rec["name"]), outcome[1], _e(outcome[0]), _e(rec["detail"] or rec["reason"]))
    parts = [
        "<!doctype html><html lang=\"vi\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
        "<title>Báo cáo case R9</title><style>%s</style></head><body><div class=\"wrap\">" % CSS,
        "<h1>Báo cáo automation R9 theo từng case</h1>",
        "<div class=\"meta\">Chạy lúc %s. Nguồn case: R9_Test_Cases_final_FS09.xlsx (%d case). Mục \"Cần xử lý\" gồm case FAIL, XPASS và LỖI ĐÃ BIẾT, xếp theo mức nghiêm trọng.</div>" % (_e(when), len(CASES) or len(rows)),
        "<div class=\"tiles\">%s</div>" % tiles,
        "<p><input id=\"q\" placeholder=\"Lọc theo mã case, tiêu đề, lý do...\"></p>",
        "<h2>Cần xử lý (%d case)</h2>" % len(attention),
        _table(attention) if attention else "<p>Không có case nào cần xử lý trong lần chạy này.</p>",
    ]
    for key, title in (("pass", "Đạt"), ("skip", "Bỏ qua (có test nhưng không chạy)"), ("notauto", "Chưa tự động hóa"), ("notrun", "Không chạy lần này")):
        group = [r for r in rows if r["verdict"] == key]
        if group:
            parts.append("<details%s><summary>%s (%d case)</summary>%s</details>" % (" open" if key == "skip" else "", _e(title), len(group), _table(group)))
    if extras:
        parts.append("<details><summary>Test ngoài danh sách case R9 (%d test)</summary><table><thead><tr><th>Test</th><th>Kết quả</th><th>Chi tiết</th></tr></thead><tbody>%s</tbody></table></details>" % (len(extras), extra_rows))
    parts.append("<script>%s</script></div></body></html>" % JS)
    html_path = REPORT_DIR / "r9_case_report.html"
    html_path.write_text("\n".join(parts), encoding="utf-8")

    csv_path = REPORT_DIR / "r9_case_report.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Case", "Tiêu đề", "Suite", "Severity", "Review Status", "Kết quả", "Chi tiết", "Quan sát lần chạy", "Test"])
        for r in sorted(rows, key=lambda r: _number(r["id"])):
            m = r["meta"]
            writer.writerow([r["id"], m.get("title", ""), m.get("suite", ""), str(m.get("severity", "")).split(" ")[0], m.get("review", ""),
                             VERDICTS[r["verdict"]][0], r["detail"], r["observed"], "; ".join(r["tests"])])
    return html_path, csv_path


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not RECS:
        return
    import datetime

    rows, extras = build()
    html_path, csv_path = write_reports(rows, extras, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    tr = terminalreporter
    counts = {k: sum(1 for r in rows if r["verdict"] == k) for k in VERDICTS}
    tr.write_sep("=", "Báo cáo theo case R9")
    tr.write_line("FAIL %d | XPASS %d | LỖI ĐÃ BIẾT %d | ĐẠT %d | BỎ QUA %d | CHƯA TỰ ĐỘNG %d | KHÔNG CHẠY %d"
                  % (counts["fail"], counts["xpass"], counts["known"], counts["pass"], counts["skip"], counts["notauto"], counts["notrun"]))
    fails = [r["id"] for r in rows if r["verdict"] == "fail"]
    if fails:
        tr.write_line("Case FAIL cần xem: " + ", ".join(fails))
    tr.write_line("Mở: %s" % html_path)
    tr.write_line("Excel: %s" % csv_path)
