"""Sign in as the people of the UAT: the parent (Singpass simulation), the School user and the MOE HQ user."""
from __future__ import annotations

import re
import string
import random
from datetime import date

from playwright.sync_api import Page, expect

from pages import real_login
from uat import env


# ------------------------------------------------------------------ parent
def clear_parent_session(page: Page) -> None:
    """Forget the parent session of this browser window (cookies and the storage of the e-Service)."""
    page.context.clear_cookies()
    try:
        page.goto(env.PARENT_URL + "/parent/login")
        page.evaluate("() => { try { sessionStorage.clear(); localStorage.clear(); } catch (e) {} }")
    except Exception:  # noqa: BLE001
        pass


def open_singpass(page: Page) -> None:
    """Open the e-Service login page and press Sign in with Singpass. Ends on the Singpass simulation page."""
    page.goto(env.PARENT_URL + "/parent/login")
    button = page.get_by_role("button", name=re.compile(r"singpass", re.I)).or_(page.get_by_role("link", name=re.compile(r"singpass", re.I)))
    button.first.click()
    page.wait_for_url(re.compile(r"/singpass/login"), timeout=45_000)


def persona_options(page: Page) -> list[str]:
    combo = page.locator("#persona-select").or_(page.get_by_role("combobox")).first
    combo.wait_for(timeout=20_000)
    return [t.strip() for t in combo.locator("option").all_inner_texts()]


def pick_persona(page: Page, nric: str) -> str:
    combo = page.locator("#persona-select").or_(page.get_by_role("combobox")).first
    options = persona_options(page)
    match = [t for t in options if nric in t]
    assert match, f"The Singpass simulation has no persona {nric}. Personas: {options}"
    combo.select_option(label=match[0])
    return match[0]


def submit_singpass(page: Page) -> None:
    button = page.locator("#btn-login-selected").or_(page.get_by_role("button", name=re.compile(r"^Log in", re.I))).first
    button.click()


def wait_home(page: Page, timeout: int = 60_000) -> None:
    page.wait_for_url(lambda u: "/parent/callback" not in u and "/singpass/" not in u and "/parent/login" not in u, timeout=timeout)
    expect(page.get_by_role("heading", name=re.compile(r"education", re.I)).first).to_be_visible(timeout=timeout)


def dismiss_tour(page: Page) -> None:
    """A fresh browser profile gets the dialog 'Welcome to E-Service' (guided tour) on Home. It covers the page and blocks every click."""
    try:
        button = page.get_by_role("button", name="Let me explore")
        button.wait_for(state="visible", timeout=4_000)
        button.click()
        expect(button).to_be_hidden(timeout=5_000)
    except Exception:  # noqa: BLE001  the dialog is not always there
        pass


def sign_in_parent(page: Page, nric: str | None = None) -> None:
    """Whole login: login page, Singpass simulation, persona, back to Home."""
    open_singpass(page)
    pick_persona(page, nric or env.PARENT_NRIC)
    submit_singpass(page)
    wait_home(page)
    dismiss_tour(page)


# ------------------------------------------------------------------ admin portal
def sign_in_admin(page: Page, role: str) -> None:
    """role is 'moe' (MOE HQ user) or 'school' (School user). Uses the login form, waits and retries when the API says Too many requests."""
    user, password = (env.HQ_USER, env.HQ_PASS) if role == "moe" else (env.SCHOOL_USER, env.SCHOOL_PASS)
    real_login.sign_in(page, env.ADMIN_URL, user, password)


def admin_base() -> str:
    return env.ADMIN_URL + "/"


# ------------------------------------------------------------------ test data
_NRIC_WEIGHTS = (2, 7, 6, 5, 4, 3, 2)
_ST = "JZIHGFEDCBA"


def make_nric(prefix: str = "S", digits: str | None = None) -> str:
    """A well formed Singapore NRIC that passes the check digit rule of the e-Service form."""
    digits = digits or "".join(random.choice(string.digits) for _ in range(7))
    total = sum(int(d) * w for d, w in zip(digits, _NRIC_WEIGHTS)) + (4 if prefix == "T" else 0)
    return f"{prefix}{digits}{_ST[total % 11]}"


def birth_date(years_old: int, extra_days: int = 40) -> str:
    """ISO date of someone who is `years_old` years and a bit more."""
    today = date.today()
    try:
        d = today.replace(year=today.year - years_old)
    except ValueError:  # 29 February
        d = today.replace(year=today.year - years_old, day=28)
    return (d.fromordinal(d.toordinal() - extra_days)).isoformat()
