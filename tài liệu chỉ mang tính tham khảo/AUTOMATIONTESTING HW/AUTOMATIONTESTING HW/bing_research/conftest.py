"""Shared fixtures and pytest configuration for bing_research automation."""
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with standard desktop resolution and English locale."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }
