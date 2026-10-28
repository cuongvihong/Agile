"""Community Page Object."""
import re
from playwright.sync_api import Locator, Page, expect
from pages.base_page import BasePage


class CommunityPage(BasePage):
    """Page object representing the MaivenPoint Community portal and search results."""

    SEARCH_INPUT_PLACEHOLDER = "Enter keywords to search..."

    def wait_until_loaded(self) -> "CommunityPage":
        """Wait for Community page to load and its search input to become visible."""
        self.page.wait_for_load_state("domcontentloaded")
        search_field = self.get_search_field()
        expect(search_field).to_be_visible(timeout=15000)
        return self

    def get_search_field(self) -> Locator:
        """Locate the Community search input using the verified placeholder."""
        return self.page.get_by_placeholder(self.SEARCH_INPUT_PLACEHOLDER)

    def search(self, keyword: str) -> "CommunityPage":
        """Enter search query into Community search field and press Enter."""
        search_field = self.get_search_field()
        search_field.fill(keyword)
        search_field.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def verify_search_results(self, expected_keyword: str) -> None:
        """Verify the post-search observable state on the Community site."""
        # 1. Verify URL navigated to search center / search page
        expect(self.page).to_have_url(re.compile(r"search", re.IGNORECASE), timeout=15000)

        # 2. Handle any cookie dialog if present on the new tab
        self.handle_cookie_consent()

        # 3. Verify search input retains the query keyword ("Search by Keywords" textbox)
        keyword_input = self.page.get_by_role("textbox", name="Search by Keywords")
        expect(keyword_input).to_have_value(expected_keyword, timeout=15000)

        # 4. Verify observable search content (e.g. Search Center / Discussions / results)
        expect(self.page.get_by_text(re.compile(r"Search Center", re.IGNORECASE)).first).to_be_visible(timeout=10000)
