"""BasePage providing common browser interactions and utilities."""
from pathlib import Path
from playwright.sync_api import Page


class BasePage:
    """Base class for all Page Objects in the suite."""

    def __init__(self, page: Page):
        self.page = page

    @property
    def url(self) -> str:
        """Current page URL."""
        return self.page.url

    @property
    def title(self) -> str:
        """Current page title."""
        return self.page.title()

    def take_screenshot(self, name: str, directory: str = "artifacts/screenshots") -> Path:
        """Capture screenshot for execution evidence."""
        dest_dir = Path(directory)
        dest_dir.mkdir(parents=True, exist_ok=True)
        file_path = dest_dir / f"{name}.png"
        self.page.screenshot(path=str(file_path), full_page=False)
        return file_path

    def handle_cookie_consent(self, timeout: int = 3000) -> None:
        """Handle cookie-consent banner if it appears and blocks user interactions."""
        try:
            accept_button = self.page.get_by_role("button", name="Accept All")
            if accept_button.is_visible():
                accept_button.click()
                accept_button.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass
