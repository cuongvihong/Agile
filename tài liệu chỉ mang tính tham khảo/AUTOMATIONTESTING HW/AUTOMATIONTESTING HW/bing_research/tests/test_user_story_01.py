"""User Story 1 Test Suite: Bing -> MaivenPoint -> Community Search."""
from pathlib import Path
import re
import allure
import pytest
from playwright.sync_api import Page, expect

from data.test_data import TEST_CASES
from pages.bing_page import BingPage
from pages.maivenpoint_page import MaivenPointPage
from pages.community_page import CommunityPage


def _attach_screenshot(page: Page, step_name: str, file_name: str) -> None:
    """Helper to save screenshot artifact and attach it to the Allure report."""
    dest_path = Path("artifacts/screenshots") / f"{file_name}.png"
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    screenshot_bytes = page.screenshot(path=str(dest_path))
    allure.attach(
        screenshot_bytes,
        name=step_name,
        attachment_type=allure.attachment_type.PNG,
    )


@allure.epic("UI Automation Research")
@allure.feature("Navigation and Multi-Site Search Workflow")
@allure.story("User Story 1 - Bing to MaivenPoint Community")
@pytest.mark.us01
@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[c["id"] for c in TEST_CASES],
)
def test_user_story_01_bing_to_maivenpoint_community_search(page: Page, case: dict) -> None:
    """Automate the end-to-end flow:

    Bing -> Search MaivenPoint -> Open MaivenPoint -> Handle cookie consent ->
    Click Community (opens new tab) -> Search 'Hi' -> Verify search results.
    """
    allure.dynamic.title(f"[{case['id']}] {case['name']}")
    allure.dynamic.description(
        "Verifies end-to-end navigation starting from Bing, locating the official "
        "MaivenPoint result, handling cookie consent, navigating to Community in a "
        "new tab/window, and executing a search for 'Hi'."
    )

    # -------------------------------------------------------------
    # 1. Arrange & Navigate to Bing
    # -------------------------------------------------------------
    with allure.step("1. Open Bing Homepage"):
        bing_page = BingPage(page)
        bing_page.open(case.get("bing_url", "https://www.bing.com/"))
        expect(page).to_have_title(re.compile(r"Bing", re.IGNORECASE))

    # -------------------------------------------------------------
    # 2. Act: Search MaivenPoint on Bing
    # -------------------------------------------------------------
    with allure.step(f"2. Search '{case['bing_keyword']}' on Bing"):
        bing_page.search(case["bing_keyword"])
        expect(page.locator(BingPage.RESULTS_CONTAINER)).to_be_visible()
        _attach_screenshot(page, "Bing Search Results", "01_bing_results")

    # -------------------------------------------------------------
    # 3. Locate & Open MaivenPoint result
    # -------------------------------------------------------------
    with allure.step(f"3. Find and open '{case['target_domain']}' search result"):
        result_item = bing_page.find_maivenpoint_result(case["target_domain"])
        expect(result_item).to_be_visible()
        maiven_raw_page = bing_page.open_result(result_item)
        maiven_page = MaivenPointPage(maiven_raw_page)
        maiven_page.wait_until_loaded()
        expect(maiven_raw_page).to_have_url(re.compile(case["target_domain"], re.IGNORECASE))

    # -------------------------------------------------------------
    # 4. Handle MaivenPoint Cookie Consent
    # -------------------------------------------------------------
    with allure.step("4. Handle cookie consent on MaivenPoint homepage"):
        maiven_page.handle_cookie_consent()
        _attach_screenshot(maiven_raw_page, "MaivenPoint Homepage", "02_maivenpoint_homepage")

    # -------------------------------------------------------------
    # 5. Click Community link & switch to NEW page/tab
    # -------------------------------------------------------------
    with allure.step("5. Click Community link and capture new page/tab"):
        community_raw_page = maiven_page.click_community()
        community_page = CommunityPage(community_raw_page)
        community_page.wait_until_loaded()
        expect(community_raw_page).to_have_url(re.compile(r"community\.maivenpoint\.com", re.IGNORECASE))
        _attach_screenshot(community_raw_page, "Community Portal Loaded", "03_community_portal")

    # -------------------------------------------------------------
    # 6. Act: Search 'Hi' on Community Page
    # -------------------------------------------------------------
    with allure.step(f"6. Search '{case['community_search']}' on Community"):
        community_page.search(case["community_search"])

    # -------------------------------------------------------------
    # 7. Assert: Verify post-search observable state
    # -------------------------------------------------------------
    with allure.step("7. Verify search results and observable UI state"):
        community_page.verify_search_results(case["community_search"])
        _attach_screenshot(community_raw_page, "Community Search Results", "04_community_search_results")
