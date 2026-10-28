"""Fixtures of the REAL UI suite (admin portal on localhost, MOE HQ user).

Rules
  1. Runs on localhost only. Any other host (for example *.vercel.app) fails the test at once.
  2. Signs in once per session with the seeded MOE HQ account and keeps the cookies in artifacts/auth/moehq.json.
     R4_HQ_USER / R4_HQ_PASS / R4_SCHOOL_USER / R4_SCHOOL_PASS override the defaults of the IAM seed (04_SeedUsers.sql).
  3. Data created by a test has the name prefix R4-AUTO (see pages/real_api.py). There is no delete API for MOEFAS,
     so tools/cleanup_r4_auto.sql soft-deletes them afterwards.
  4. Tests marked `mutating` write data. `readonly` tests only read.
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest

from pages import real_api
from pages.real_login import HQ_PASS, HQ_USER, SCHOOL_PASS, SCHOOL_USER, is_local, sign_in
from pages.real_schemes import AddFee, Detail, SchemeList, Wizard
from pages.real_sbfas import SbfasAddFee, SbfasList, SbfasWizard

ROOT = Path(__file__).resolve().parents[2]
AUTH_DIR = ROOT / "artifacts" / "auth"


def pytest_collection_modifyitems(items):
    for item in items:
        if "tests/real" in str(item.fspath).replace("\\", "/") or "tests\\real" in str(item.fspath):
            item.add_marker(pytest.mark.real)
            if not item.get_closest_marker("mutating"):
                item.add_marker(pytest.mark.readonly)


# ------------------------------------------------------------------ guard
@pytest.fixture(autouse=True)
def _localhost_only(base_url):
    if not is_local(base_url):
        pytest.fail(f"The real UI suite runs on localhost only. base_url is {base_url!r}. Never run it on Vercel.", pytrace=False)


# ------------------------------------------------------------------ sign in
STATE_MAX_AGE_S = 15 * 60


def _state_for(browser, base_url: str, file_name: str, user: str, password: str) -> str:
    """Cookies of a signed-in user. Reuse the saved file when it is fresh and the backend still accepts it,
    otherwise sign in once. This keeps the number of logins low (the login API limits requests per minute)."""
    if not is_local(base_url):
        pytest.fail(f"The real UI suite runs on localhost only. base_url is {base_url!r}.", pytrace=False)
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    path = AUTH_DIR / file_name
    if path.exists() and time.time() - path.stat().st_mtime < STATE_MAX_AGE_S:
        ctx = browser.new_context(storage_state=str(path), locale="en-US")
        try:
            resp = ctx.request.get(base_url.rstrip("/") + "/" + real_api.SCHEMES + "?pageNumber=1&pageSize=1")
            if resp.ok:
                return str(path)
        except Exception:
            pass
        finally:
            ctx.close()
    context = browser.new_context(locale="en-US", viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        sign_in(page, base_url, user, password)
        context.storage_state(path=str(path))
    finally:
        context.close()
    return str(path)


@pytest.fixture(scope="session")
def hq_state(browser, base_url) -> str:
    """MOE HQ cookies (one login per 15 minutes at most)."""
    return _state_for(browser, base_url, "moehq.json", HQ_USER, HQ_PASS)


@pytest.fixture(scope="session")
def school_state(browser, base_url) -> str:
    """School user cookies, only created when a school test asks for them."""
    return _state_for(browser, base_url, "school.json", SCHOOL_USER, SCHOOL_PASS)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, hq_state):
    """Every real test starts signed in as MOE HQ, in English."""
    return {**browser_context_args, "storage_state": hq_state, "locale": "en-US"}


# ------------------------------------------------------------------ api
@pytest.fixture(scope="session")
def api(playwright, hq_state):
    ctx = playwright.request.new_context(storage_state=hq_state, ignore_https_errors=True)
    yield ctx
    ctx.dispose()


@pytest.fixture(scope="session")
def base(base_url) -> str:
    return base_url.rstrip("/") + "/"


@pytest.fixture(scope="session")
def components(api, base) -> list[dict]:
    """Active fee components of Function 3 as the wizard offers them."""
    return real_api.fee_components(api, base)


@pytest.fixture
def need_components(components):
    def _need(count: int = 1) -> list[dict]:
        if len(components) < count:
            pytest.skip(f"needs {count} active fee component(s) of Function 3, the stack has {len(components)}")
        return components
    return _need


@pytest.fixture
def make_scheme(api, base, components):
    """Create a scheme through the API with a free period. Returns dict(id, name, win, component_ids, status)."""
    def _make(tag: str, *, status: str = "Draft", n_components: int = 1, win: dict | None = None) -> dict:
        if len(components) < n_components:
            pytest.skip(f"needs {n_components} active fee component(s) of Function 3")
        ids = [c["id"] for c in components[:n_components]]
        for attempt in range(4):
            period = win or real_api.window(attempt)
            name = real_api.unique_name(tag)
            ok, data, message = real_api.create_scheme(api, base, name=name, win=period, component_ids=ids, status=status)
            if ok:
                return {"id": data.get("id"), "name": name, "win": period, "component_ids": ids,
                        "component_names": [c["name"] for c in components[:n_components]], "status": status}
            if win:
                break
        pytest.fail(f"Could not create the {status} scheme through the API: {message}", pytrace=False)
    return _make


# ------------------------------------------------------------------ pages
@pytest.fixture
def lst(page, base) -> SchemeList:
    return SchemeList(page, base).open()


@pytest.fixture
def wiz(page, base) -> Wizard:
    return Wizard(page, base).open()


@pytest.fixture
def detail(page, base) -> Detail:
    return Detail(page, base)


@pytest.fixture
def add_fee(page, base) -> AddFee:
    return AddFee(page, base)


# ------------------------------------------------------------------ School user (SBFAS)
@pytest.fixture(scope="session")
def school_api(playwright, school_state):
    ctx = playwright.request.new_context(storage_state=school_state, ignore_https_errors=True)
    yield ctx
    ctx.dispose()


@pytest.fixture
def school_page(browser, school_state):
    """A page signed in as the School user, English."""
    context = browser.new_context(storage_state=school_state, locale="en-US", viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.set_default_timeout(15_000)
    yield page
    context.close()


@pytest.fixture(scope="session")
def offerings(school_api, base) -> list[dict]:
    """Active grades of the school of the School user, in wizard order."""
    return real_api.school_offerings(school_api, base)


@pytest.fixture(scope="session")
def school_fees(school_api, base) -> list[dict]:
    return real_api.school_fee_components(school_api, base)


@pytest.fixture
def need_school_data(offerings, school_fees):
    def _need(fees: int = 1) -> None:
        if not offerings:
            pytest.skip("the school of the School user has no active grade (offerings)")
        if len(school_fees) < fees:
            pytest.skip(f"needs {fees} active fee component(s) for the school")
    return _need


@pytest.fixture
def make_sbfas(school_api, base, offerings, school_fees, need_school_data):
    """Create a SBFAS scheme through the API as the School user. Returns dict(id, name, win, fee_ids, status)."""
    created: list[str] = []

    def _make(tag: str, *, publish: bool = False, n_fees: int = 1, win: dict | None = None, name: str | None = None) -> dict:
        need_school_data(n_fees)
        fee_ids = [f["id"] for f in school_fees[:n_fees]]
        message = ""
        for slot in range(1, 6):
            period = win or real_api.sbfas_window(slot + (int(__import__("time").time()) % 20) * 5)
            scheme_name = name or real_api.unique_name(tag)
            ok, data, message = real_api.create_sbfas(school_api, base, name=scheme_name, win=period, fee_ids=fee_ids, offerings=offerings, publish=publish)
            if ok:
                created.append(data.get("id"))
                return {"id": data.get("id"), "name": scheme_name, "win": period, "fee_ids": fee_ids, "fee_names": [f["name"] for f in school_fees[:n_fees]], "publish": publish}
            if win or name:
                break
        pytest.fail(f"Could not create the SBFAS scheme through the API: {message}", pytrace=False)
    yield _make
    for scheme_id in created:  # Draft schemes can be deleted, published ones stay until tools/cleanup_r4_auto.sql
        try:
            real_api.delete_sbfas(school_api, base, scheme_id)
        except Exception:
            pass


@pytest.fixture
def sbfas_list(school_page, base) -> SbfasList:
    return SbfasList(school_page, base).open()


@pytest.fixture
def sbfas_wiz(school_page, base) -> SbfasWizard:
    return SbfasWizard(school_page, base).open()


@pytest.fixture
def sbfas_add_fee(school_page) -> SbfasAddFee:
    return SbfasAddFee(school_page)
