"""Sign in: parent through the Singpass simulator, MOE HQ and school through the Entra ID simulator."""
from __future__ import annotations

import re

from core import config


def open_parent_login(page) -> None:
    page.goto(f"{config.PARENT_URL}/parent/login")
    page.locator("button", has_text=re.compile(r"Sign in with Singpass", re.I)).first.click()
    page.wait_for_url(re.compile(r"/singpass/login"), timeout=30000)


def persona_options(page) -> list[str]:
    """Labels of the test personas offered by the Singpass simulator (deduplicated)."""
    sel = page.locator("select").first
    sel.wait_for(state="visible")
    seen, out = set(), []
    for label in sel.locator("option").all_inner_texts():
        label = label.strip()
        if label and label not in seen:
            seen.add(label)
            out.append(label)
    return out


def choose_persona_and_login(page, nric: str) -> None:
    sel = page.locator("select").first
    label = next((o for o in persona_options(page) if o.startswith(nric)), None)
    if not label:
        raise AssertionError(f"Persona {nric} is not offered by the Singpass simulator")
    sel.select_option(label=label)
    page.get_by_role("button", name="Log in with Singpass").click()
    page.wait_for_url(lambda u: "/singpass/" not in u and "/callback" not in u, timeout=45000)
    page.wait_for_load_state("networkidle")


def parent_login(page, nric: str) -> None:
    open_parent_login(page)
    choose_persona_and_login(page, nric)
    page.get_by_text("Education wallets").first.wait_for(timeout=30000)


def parent_logout(page) -> None:
    try:
        page.get_by_role("button", name="Open user options").click()
        page.get_by_role("button", name="Log out").click()
        page.wait_for_url(re.compile(r"/parent/login"), timeout=15000)
    except Exception:
        page.context.clear_cookies()


def admin_login(page, role: str) -> None:
    """role = 'hq' or 'school'."""
    page.goto(f"{config.ADMIN_URL}/login")
    if config.ADMIN_LOGIN_MODE == "password":
        user, pwd = (config.HQ_USER, config.HQ_PASS) if role == "hq" else (config.SCHOOL_USER, config.SCHOOL_PASS)
        page.get_by_placeholder(re.compile("username", re.I)).fill(user)
        page.get_by_placeholder(re.compile("password", re.I)).fill(pwd)
        page.get_by_role("button", name=re.compile(r"^Sign in$", re.I)).click()
    else:
        account = config.HQ_ACCOUNT if role == "hq" else config.SCHOOL_ACCOUNT
        page.locator("button", has_text=re.compile(r"Sign in with Microsoft", re.I)).first.click()
        page.wait_for_url(re.compile(r"login\."), timeout=30000)
        page.locator(".account-tile, [role=option]", has_text=account).first.click()
    page.wait_for_url(lambda u: u.startswith(config.ADMIN_URL) and "/login" not in u, timeout=45000)
    page.get_by_role("button", name="Sign out").wait_for(timeout=30000)
