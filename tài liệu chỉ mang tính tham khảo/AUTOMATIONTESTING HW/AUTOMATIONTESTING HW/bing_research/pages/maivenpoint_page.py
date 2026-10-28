"""MaivenPoint Page Object."""
from playwright.sync_api import Locator, Page, expect
from pages.base_page import BasePage


class MaivenPointPage(BasePage):
    """Page object representing the MaivenPoint homepage."""

    def wait_until_loaded(self) -> "MaivenPointPage":
        """Wait for the MaivenPoint page to complete DOM content loading."""
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def handle_cookie_consent(self, timeout: int = 5000) -> "MaivenPointPage":
        """Handle cookie-consent banner if it appears and blocks user interactions.

        Conditionally handles the 'Accept All' action so tests do not fail
        if the banner has already been dismissed or is not displayed.
        """
        accept_button = self.page.get_by_role("button", name="Accept All")
        try:
            if accept_button.is_visible():
                accept_button.click()
                accept_button.wait_for(state="hidden", timeout=timeout)
        except Exception:
            # Banner was either not present or closed automatically
            pass
        return self

    def get_community_link(self) -> Locator:
        """Locate the Community link in header navigation."""
        link = self.page.get_by_role("link", name="Community", exact=False).first
        if not link.is_visible():
            link = self.page.locator("a", has_text="Community").first
        return link

    def click_community(self) -> Page:
        """Click the Community navigation link and capture the newly opened page/tab.

        User Story 1 dictates Community opens in a new page/tab. This method
        explicitly captures and returns the new Playwright Page.
        """
        community_link = self.get_community_link()
        expect(community_link).to_be_visible(timeout=10000)

        with self.page.context.expect_page() as popup_info:
            community_link.click()

        new_page = popup_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page
