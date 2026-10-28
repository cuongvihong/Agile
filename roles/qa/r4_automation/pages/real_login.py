"""Sign in to the real admin portal (localhost). Credentials default to the accounts of the IAM seed (04_SeedUsers.sql)."""
from __future__ import annotations

import os
import re
import urllib.parse

from playwright.sync_api import Page, expect

LOCAL_HOSTS = {"localhost", "127.0.0.1", "[::1]"}

HQ_USER = os.environ.get("R4_HQ_USER", "moehq")
HQ_PASS = os.environ.get("R4_HQ_PASS", "123456")
SCHOOL_USER = os.environ.get("R4_SCHOOL_USER", "school")
SCHOOL_PASS = os.environ.get("R4_SCHOOL_PASS", "123456")


def is_local(url: str) -> bool:
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return (
        host in LOCAL_HOSTS
        or host.endswith(".localhost")
        or host.endswith(".test")
        or host.endswith(".devtunnels.ms")
        or "devtunnels" in host
        or "pinggy" in host
    )


RATE_LIMIT_WAIT_MS = 65_000


def sign_in(page: Page, base_url: str, user: str, password: str, retries: int = 3) -> None:
    """Sign in through the login form. The login API answers 'Too many requests' when it is called many times in a
    minute, so wait and try again instead of failing the whole run."""
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        page.goto(base_url.rstrip("/") + "/login")
        if _left_login(page, 2_000):
            return  # the session was still valid, the portal moved on by itself
        page.locator("input[autocomplete='username']").fill(user)
        page.locator("input[autocomplete='current-password']").fill(password)
        page.locator("form button[type='submit']").click()
        try:
            expect(page).not_to_have_url(re.compile(r"/login"), timeout=20_000)
            expect(page.locator("nav").first).to_be_visible(timeout=20_000)
            return
        except AssertionError as err:
            last_error = err
            if page.get_by_text("Too many requests").count() and attempt < retries:
                page.wait_for_timeout(RATE_LIMIT_WAIT_MS)
                continue
            break
    raise AssertionError(
        f"Sign in as {user!r} failed on {base_url}. Check that the stack runs (login API) and that the account exists "
        f"in IAM seed 04_SeedUsers.sql. Set R4_HQ_USER and R4_HQ_PASS when the password differs. "
        f"If the screen says 'Too many requests', wait one minute and run again."
    ) from last_error


def _left_login(page: Page, timeout_ms: int) -> bool:
    try:
        page.wait_for_url(lambda url: "/login" not in url, timeout=timeout_ms)
        return True
    except Exception:
        return False


def goto_signed_in(page: Page, base_url: str, path: str, user: str = HQ_USER, password: str = HQ_PASS) -> None:
    """Open a page. The portal checks the session after the page has loaded. It may show /login for a moment while it
    renews the session and then land on the home page, or it may stay on /login when the cookies are dead.
    So: wait for the check to finish, sign in only if /login stays, and reopen the target until we are on it."""
    target = base_url.rstrip("/") + "/" + path.lstrip("/")
    want = "/" + path.strip("/")
    for _ in range(3):
        page.goto(target)
        try:
            page.wait_for_load_state("networkidle", timeout=10_000)
        except Exception:
            pass
        if "/login" in page.url and not want.endswith("/login"):
            if not _left_login(page, 6_000):
                sign_in(page, base_url, user, password)
        if page.url.split("?")[0].rstrip("/").endswith(want.rstrip("/")):
            return
    page.goto(target)
