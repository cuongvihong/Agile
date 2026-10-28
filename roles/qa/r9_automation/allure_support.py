"""Báo cáo Allure và video từng case cho R9, cùng kiểu với r4_automation.

Làm ba việc:
  1. Gắn nội dung case của R9_Test_Cases_final_FS09.xlsx (suite, màn hình, severity, tiền điều kiện, dữ liệu, bước,
     kết quả mong đợi, giả định) vào báo cáo Allure, lấy từ data/cases.py do tools/build_coverage.py sinh.
  2. Quay video 1280x720 cho từng test có trình duyệt, kéo dài tối thiểu R9_MIN_VIDEO_SECONDS giây (mặc định 5, đặt 0 để tắt) để xem được thao tác.
  3. Lưu video thành artifacts/videos/<mã case>__<tên test>.webm và đính vào báo cáo Allure.

Allure chỉ đọc dữ liệu có sẵn, không đổi kết quả test. Báo cáo dựng bằng: allure generate artifacts/allure-results -o artifacts/allure-report --clean --single-file
(run_r9_automation.cmd tự làm bước này nếu máy có lệnh allure). Video chỉ có trong báo cáo khi test chạy bằng trình duyệt; test chỉ gọi SQL hoặc API thì không có video.
"""
from __future__ import annotations

import os
import re
import shutil
import time
from pathlib import Path

import allure
import pytest

ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "artifacts" / "videos"
VIDEO_ARGS = {"record_video_dir": str(VIDEOS_DIR), "record_video_size": {"width": 1280, "height": 720}}
MIN_SECONDS = float(os.environ.get("R9_MIN_VIDEO_SECONDS", "5"))

try:
    from data.cases import CASES
except Exception:  # noqa: BLE001
    CASES = {}

SEVERITY = {"S1": allure.severity_level.BLOCKER, "S2": allure.severity_level.CRITICAL, "S4": allure.severity_level.MINOR}
KIND_MARKERS = ("mocked", "api", "mutating", "online", "admin", "destructive", "draft", "known_defect", "extra")
CASE_HEAD = re.compile(r"((?:test_)?(?:tc_\d{3}_?)+)")


def case_ids(item) -> list[str]:
    spec = getattr(item, "callspec", None)
    if spec is not None and "case_id" in spec.params:  # tests/test_not_automated.py
        return [str(spec.params["case_id"])]
    name = getattr(item, "originalname", None) or item.name
    match = CASE_HEAD.match(name)
    return ["TC-" + n for n in re.findall(r"tc_(\d{3})", match.group(1))] if match else []


def _safe(text: str, limit: int = 110) -> str:
    return re.sub(r"[^A-Za-z0-9._\[\]-]+", "_", text).strip("_")[:limit]


def _describe(case_id: str, info: dict) -> str:
    parts = [f"### {case_id}: {info.get('title')}", "",
             f"- **Suite**: {info.get('suite')}", f"- **Page / Screen**: {info.get('page')}",
             f"- **Target Environment**: {info.get('env')}",
             f"- **Severity / Priority**: {str(info.get('severity', '')).split(' ')[0]} / {str(info.get('priority', '')).split(' ')[0]}",
             f"- **Review Status**: {info.get('review')}"]
    if info.get("assumption"):
        parts.append(f"- **Assumption**: {info['assumption']}")
    for heading, key in (("Preconditions", "preconditions"), ("Test Data", "test_data"), ("Test Steps", "steps"),
                         ("Expected Result", "expected")):
        if info.get(key):
            parts += ["", f"#### {heading}", str(info[key])]
    return "\n".join(parts)


@pytest.fixture(autouse=True)
def _case_allure_metadata(request):
    """Gắn nội dung case vào báo cáo Allure. Không cần trình duyệt nên chạy cho mọi test."""
    node = request.node
    ids = case_ids(node)
    if node.get_closest_marker("not_automated") and hasattr(node, "callspec"):
        ids = [str(node.callspec.params.get("case_id", ""))]
    ids = [i for i in ids if i in CASES]
    if ids:
        info = CASES[ids[0]]
        allure.dynamic.parent_suite("R9 FS09 Fees & Payments")
        allure.dynamic.feature(info.get("suite") or "R9")
        allure.dynamic.story(info.get("page") or "")
        allure.dynamic.severity(next((v for k, v in SEVERITY.items() if k in str(info.get("severity", ""))), allure.severity_level.NORMAL))
        allure.dynamic.description("\n\n---\n\n".join(_describe(i, CASES[i]) for i in ids))
        for i in ids:
            allure.dynamic.tag(i)
    for marker in KIND_MARKERS:
        if node.get_closest_marker(marker):
            allure.dynamic.tag(marker)
    yield


def pytest_itemcollected(item):
    """Tên hiển thị trong Allure: 'TC-xxx: tiêu đề case'. Phải đặt lúc thu thập vì allure-pytest ghi đè tên ở giai đoạn call."""
    spec = getattr(item, "callspec", None)
    if spec is not None and "case_id" in spec.params:  # cùng một hàm cho nhiều case: giữ tên test[TC-xxx]
        return
    ids = [i for i in case_ids(item) if i in CASES]
    obj = getattr(item, "obj", None)
    if ids and obj is not None and not hasattr(obj, "__allure_display_name__"):
        title = f"{' + '.join(ids)}: {CASES[ids[0]].get('title')}"
        try:
            obj.__allure_display_name__ = title.replace("{", "{{").replace("}", "}}")
        except Exception:  # noqa: BLE001
            pass


def pytest_runtest_setup(item):
    item.stash_start = time.time()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """Trước khi pytest dọn fixture: bù thời gian cho đủ video, đóng trang, đổi tên video và đính vào Allure.
    Chạy sau bước chụp ảnh khi thất bại (ở bước báo cáo của giai đoạn call) nên ảnh và trace không mất."""
    try:
        _finish_video(item)
    except Exception as err:  # noqa: BLE001  báo cáo không được làm hỏng test
        print(f"[allure_support] không xử lý được video của {item.name}: {err}")
    yield


def _finish_video(item) -> None:
    funcargs = getattr(item, "funcargs", {}) or {}
    page = funcargs.get("page") or funcargs.get("anon_page")
    if page is None or page.is_closed():
        return
    elapsed = time.time() - getattr(item, "stash_start", time.time())
    if MIN_SECONDS > 0 and elapsed < MIN_SECONDS:
        try:
            page.wait_for_timeout(int((MIN_SECONDS - elapsed) * 1000))
        except Exception:  # noqa: BLE001
            pass
    video = page.video
    page.close()
    if video is None:
        return
    raw = video.path()
    if not raw or not os.path.exists(raw):
        return
    ids = case_ids(item)
    stem = (ids[0] + "__" if ids else "") + _safe(item.name)
    dest = VIDEOS_DIR / f"{stem}.webm"
    dest.unlink(missing_ok=True)
    try:
        shutil.move(raw, dest)
    except Exception:  # noqa: BLE001
        shutil.copy2(raw, dest)
    allure.attach.file(str(dest), name=f"Execution video, {stem}", attachment_type=allure.attachment_type.WEBM)
