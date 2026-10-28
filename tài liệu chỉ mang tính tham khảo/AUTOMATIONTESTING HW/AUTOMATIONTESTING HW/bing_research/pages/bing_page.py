"""Bing search Page Object."""
import re
from playwright.sync_api import Locator, Page, expect
from pages.base_page import BasePage


class BingPage(BasePage):
    """Page object representing the Bing search engine homepage and results."""

    SEARCH_INPUT = "#sb_form_q"
    RESULTS_CONTAINER = "#b_results"
    ORGANIC_RESULTS = "#b_results li.b_algo"

    def open(self, url: str = "https://www.bing.com/") -> "BingPage":
        """Navigate to Bing homepage and wait for the search input to be ready."""
        self.page.goto(url)
        search_box = self.page.locator(self.SEARCH_INPUT)
        search_box.wait_for(state="visible", timeout=10000)
        return self

    def search(self, keyword: str) -> "BingPage":
        """Enter search keyword and submit search."""
        search_box = self.page.locator(self.SEARCH_INPUT)
        search_box.fill(keyword)
        search_box.press("Enter")
        self.wait_for_results()
        return self

    def wait_for_results(self) -> None:
        """Wait until Bing search results container and items are visible."""
        self.page.wait_for_selector(self.RESULTS_CONTAINER, state="visible", timeout=15000)
        self.page.locator(self.ORGANIC_RESULTS).first.wait_for(state="visible", timeout=15000)

    def find_maivenpoint_result(self, domain: str = "maivenpoint.com") -> Locator:
        """Find the organic search result corresponding to the given domain or brand.

        Identifies results dynamically based on meaningful domain/brand text
        rather than relying on a fixed index.
        """
        # Ensure organic results are present
        self.wait_for_results()
        
        # Filter b_algo items by domain in cite/text
        match = self.page.locator(self.ORGANIC_RESULTS).filter(has_text=re.compile(domain, re.IGNORECASE)).first
        if match.count() == 0:
            match = self.page.locator(self.ORGANIC_RESULTS).filter(has_text=re.compile("maivenpoint", re.IGNORECASE)).first
            
        expect(match).to_be_visible(timeout=10000)
        return match

    def open_result(self, result_locator: Locator) -> Page:
        """Click the result link, handle new tab/popup if opened, and return the destination Page."""
        link = result_locator.locator("h2 a").first
        if link.count() == 0:
            link = result_locator.locator("a").first

        target_attr = link.get_attribute("target")
        if target_attr == "_blank":
            with self.page.context.expect_page() as new_page_info:
                link.click()
            dest_page = new_page_info.value
        else:
            try:
                with self.page.context.expect_page(timeout=4000) as new_page_info:
                    link.click()
                dest_page = new_page_info.value
            except Exception:
                dest_page = self.page

        # Wait for redirection to complete
        dest_page.wait_for_load_state("domcontentloaded")
        expect(dest_page).to_have_url(re.compile(r"maivenpoint\.com", re.IGNORECASE), timeout=15000)
        return dest_page
