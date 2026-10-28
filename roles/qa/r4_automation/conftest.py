"""Fixtures for the R4 (FS F4 v1.3) UI automation suite.

The prototype keeps all data in the browser. A new browser context per test is
therefore the same as Reset data: every test starts from the base state of the
sheet "Seed Data" in roles/qa/R4_Test_Cases.xlsx.
"""
from __future__ import annotations

import os
import re
import shutil
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from data import seed
from data.cases import CASES
from pages.applications_page import ApplicationsPage
from pages.flows import close_form_now, open_hq_list
from pages.portal import Portal
from pages.schemes_page import SchemesPage

ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "artifacts" / "videos"
ALLURE_RESULTS_DIR = ROOT / "artifacts" / "allure-results"


# ------------------------------------------------------------------ settings
@pytest.fixture(scope="session")
def base_url(base_url):
    """pytest-base-url gives the --base-url or the base_url of pytest.ini. R4_BASE_URL overrides both."""
    return os.environ.get("R4_BASE_URL") or base_url or "http://localhost:5173"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-SG",
        "timezone_id": "Asia/Singapore",
        "accept_downloads": True,
        "record_video_dir": str(VIDEOS_DIR),
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def launch_options(launch_options):
    """Pace actions so interaction is clearly visible in the recorded video."""
    slow_mo_ms = int(os.environ.get("R4_SLOW_MO", "100"))
    return {
        **launch_options,
        "slow_mo": slow_mo_ms,
    }


@pytest.fixture(autouse=True)
def _default_timeout(request):
    if "page" in request.fixturenames:
        page = request.getfixturevalue("page")
        page.set_default_timeout(15_000)
        page.set_default_navigation_timeout(45_000)


def pytest_collection_modifyitems(items):
    """known_defect(reason=...) means: the test asserts the FS rule, the prototype is expected to break it."""
    for item in items:
        marker = item.get_closest_marker("known_defect")
        if marker is not None:
            reason = marker.kwargs.get("reason") or (marker.args[0] if marker.args else "known defect")
            item.add_marker(pytest.mark.xfail(reason=reason, strict=False))


# -------------------------------------------------- Case Metadata & Video Pacing (~5s)
@pytest.fixture(autouse=True)
def _case_pacing_and_allure(request):
    """Enrich Allure report with R4_Test_Cases metadata, pace runtime to ~5s, and attach video."""
    if request.node.get_closest_marker("not_automated"):
        yield
        return

    # Extract case ID from test name, e.g. test_tc_001_... -> TC-001
    case_id = None
    match = re.search(r"tc_(\d{3})", request.node.name)
    if match:
        case_id = f"TC-{match.group(1)}"

    # Enrich Allure report with test case metadata
    if case_id and case_id in CASES:
        cinfo = CASES[case_id]
        allure.dynamic.feature(cinfo.get("suite", "R4 FAS Applications"))
        allure.dynamic.story(cinfo.get("page", "FAS"))
        allure.dynamic.title(f"{case_id}: {cinfo.get('title')}")

        sev = cinfo.get("severity", "S3")
        if "S1" in sev:
            allure.dynamic.severity(allure.severity_level.BLOCKER)
        elif "S2" in sev:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        elif "S4" in sev:
            allure.dynamic.severity(allure.severity_level.MINOR)
        else:
            allure.dynamic.severity(allure.severity_level.NORMAL)

        desc = (
            f"### {case_id}: {cinfo.get('title')}\n\n"
            f"- **Suite**: {cinfo.get('suite')}\n"
            f"- **Page / Screen**: {cinfo.get('page')}\n"
            f"- **Target Environment**: {cinfo.get('env')}\n"
            f"- **Severity / Priority**: {cinfo.get('severity')} / {cinfo.get('priority')}\n\n"
            f"#### Preconditions\n{cinfo.get('preconditions')}\n\n"
            f"#### Test Data\n{cinfo.get('test_data')}\n\n"
            f"#### Test Steps\n{cinfo.get('steps')}\n\n"
            f"#### Expected Result\n{cinfo.get('expected')}"
        )
        allure.dynamic.description(desc)

    start_time = time.time()
    page = None
    if "page" in request.fixturenames:
        page = request.getfixturevalue("page")

    try:
        yield
    finally:
        if page and not page.is_closed():
            # Yêu cầu: mỗi case phải có video run tầm 5s để kiểm tra UI/automation
            elapsed = time.time() - start_time
            target_duration = 5.0
            if elapsed < target_duration:
                try:
                    page.wait_for_timeout(int((target_duration - elapsed) * 1000))
                except Exception:
                    pass

            # Finalize video recording
            video = page.video
            try:
                page.close()
            except Exception:
                pass

            if video:
                try:
                    raw_path = video.path()
                    if raw_path and os.path.exists(raw_path):
                        name_label = case_id or request.node.name
                        dest_file = VIDEOS_DIR / f"{name_label}.webm"
                        if dest_file.exists():
                            try:
                                dest_file.unlink()
                            except Exception:
                                pass
                        try:
                            shutil.move(raw_path, dest_file)
                        except Exception:
                            shutil.copy2(raw_path, dest_file)

                        allure.attach.file(
                            str(dest_file),
                            name=f"Execution Video - {name_label} (~5s)",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                except Exception as ex:
                    print(f"Warning attaching video to Allure: {ex}")


# ------------------------------------------------------------------- portals
@pytest.fixture
def portal(page, base_url) -> Portal:
    """Prototype opened at the base state, nobody signed in."""
    return Portal(page, base_url).open()


@pytest.fixture
def hq(portal) -> Portal:
    """Signed in as MOE HQ (Mei Lin Tan)."""
    return portal.sign_in_hq()


@pytest.fixture
def hq_apps(hq) -> ApplicationsPage:
    return open_hq_list(hq)


@pytest.fixture
def hq_schemes(hq) -> SchemesPage:
    hq.go("MOEFAS schemes")
    return SchemesPage(hq.page, "MOEFAS schemes")


@pytest.fixture
def bvp(portal) -> Portal:
    """Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary."""
    return portal.sign_in_school("BVP-0012")


@pytest.fixture
def bvp_apps(bvp) -> ApplicationsPage:
    bvp.go("FAS applications")
    return ApplicationsPage(bvp.page)


@pytest.fixture
def bvp_schemes(bvp) -> SchemesPage:
    bvp.go("SBFAS schemes")
    return SchemesPage(bvp.page, "SBFAS schemes")


@pytest.fixture
def mrs(portal) -> Portal:
    """Signed in as School user Farah Tan (MRS-0012), Meridian Secondary."""
    return portal.sign_in_school("MRS-0012")


@pytest.fixture
def mrs_apps(mrs) -> ApplicationsPage:
    mrs.go("FAS applications")
    return ApplicationsPage(mrs.page)


@pytest.fixture
def hq_closed(hq) -> ApplicationsPage:
    """MOE HQ closed the MOEFAS 2027 form with Close form now (demo); the list is open."""
    close_form_now(hq)
    return open_hq_list(hq)


@pytest.fixture
def bvp_apps_after_close(hq) -> ApplicationsPage:
    """MOE HQ closed the MOEFAS 2027 form (demo). Then School user Lan Nguyen (BVP-0012) opens FAS applications."""
    close_form_now(hq)
    hq.sign_in_school("BVP-0012")
    hq.go("FAS applications")
    return ApplicationsPage(hq.page)
