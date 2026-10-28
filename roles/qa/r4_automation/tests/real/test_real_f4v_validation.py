"""Validation rules of R4 (R4_FAS_Validation_Rules_EN.docx) on the real stack, localhost only.

API cases (TC-268 to TC-303) send requests with the session cookie of the user: the School user for SBFAS, MOE HQ for MOEFAS.
UI cases (TC-304 to TC-314) type into the wizard. TC-161, TC-165 and TC-225 close three gaps of the earlier suites.
Rules
  * Every scheme name starts with R4-AUTO (tools/cleanup_r4_auto.sql removes them). SBFAS drafts are deleted at the end of the test.
  * One `def test_tc_NNN` per case. Several requests of one case are steps of the same test.
  * known_defect(reason) asserts the rule of the rules document. The test is XFAIL while the defect is open, XPASS when it is fixed.
Text and screen cases TC-315 to TC-331 need the FAS applications screens and are not automated (see test_not_automated.py).
"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_schemes import tick, untick

pytestmark = [pytest.mark.real, pytest.mark.f414, pytest.mark.validation]

UNKNOWN_ID = "00000000-0000-0000-0000-000000000099"
UNKNOWN_GRADE = "AL-NOPE"


# ====================================================================== helpers
class Result:
    def __init__(self, resp):
        self.status = resp.status
        try:
            body = resp.json()
        except Exception:
            body = {}
        self.body = body if isinstance(body, dict) else {}
        self.data = self.body.get("data") or {}
        self.text = f"{self.status} {self.body.get('message') or ''} " + " ".join(str(e) for e in (self.body.get("errors") or []))

    @property
    def created(self) -> bool:
        return self.status in (200, 201)

    def has(self, fragment: str) -> bool:
        return fragment.lower() in self.text.lower()


def _utc_today() -> date:
    return datetime.now(timezone.utc).date()


def _win(opens: date) -> dict:
    return {"opens": opens.isoformat(), "closes": (opens + timedelta(days=30)).isoformat(),
            "eff_from": (opens + timedelta(days=60)).isoformat(), "eff_to": (opens + timedelta(days=425)).isoformat()}


def _name(tag: str, size: int | None = None) -> str:
    n = real_api.unique_name(tag)
    return n if size is None else (n + "x" * size)[:size]


class SbApi:
    """Requests to the SBFAS API as the School user. Drafts are deleted by the fixture at the end."""

    def __init__(self, req, base, offerings, fees):
        self.req, self.base, self.offerings, self.fees = req, base, offerings, fees
        self.ids: list[str] = []

    def items(self, pct=10):
        return [{"academicLevelId": o["academicLevelId"], "subsidyPercentage": pct} for o in self.offerings]

    def payload(self, **over) -> dict:
        win = over.pop("win", None) or real_api.sbfas_window(0)
        p = {
            "name": _name("v"), "openFrom": win["opens"], "openTo": win["closes"],
            "effectiveFrom": win["eff_from"], "effectiveTo": win["eff_to"], "totalBudgetAmount": 1000,
            "nationalities": ["SC"], "isGhiEnabled": False, "ghiFrom": None, "ghiTo": None,
            "isPciEnabled": True, "pciFrom": 0, "pciTo": 1000, "incomeOperator": None,
            "eligibilityDescription": None,
            "feeComponents": [{"feeComponentId": self.fees[0]["id"], "items": self.items()}],
            "publish": False,
        }
        p.update(over)
        return p

    def post(self, **over) -> Result:
        resp = real_api.post_retry(self.req, f"{self.base}{real_api.SBFAS}", self.payload(**over))
        r = Result(resp)
        if r.created and r.data.get("id"):
            self.ids.append(r.data["id"])
        return r

    def add_fee(self, scheme_id: str, fee_id: str, items: list[dict]) -> Result:
        resp = real_api.post_retry(self.req, f"{self.base}{real_api.SBFAS}/{scheme_id}/fee-components", {"feeComponentId": fee_id, "items": items})
        return Result(resp)


class HqApi:
    """Requests to the MOEFAS API as MOE HQ. There is no delete API: the schemes are Drafts named R4-AUTO."""

    def __init__(self, req, base, components):
        self.req, self.base, self.components = req, base, components

    def payload(self, **over) -> dict:
        win = over.pop("win", None) or real_api.window()
        stages = ["PRIMARY", "SECONDARY", "PRE_UNIVERSITY"]
        p = {
            "status": "Draft", "name": _name("v"), "description": None,
            "openFrom": f"{win['opens']}T00:00:00", "openTo": f"{win['closes']}T23:59:59",
            "effectiveFrom": f"{win['eff_from']}T00:00:00", "effectiveTo": f"{win['eff_to']}T23:59:59",
            "isGhiEnabled": False, "ghiFrom": 0, "ghiTo": 0, "isPciEnabled": True, "pciFrom": 0, "pciTo": 1100,
            "incomeOperator": "OR", "nationalities": ["SC"],
            "subsidies": [{"educationStage": s, "feeComponentId": self.components[0]["id"], "subsidyPercentage": 10} for s in stages],
            "totalBudgetAmount": 1000,
        }
        p.update(over)
        return p

    def post(self, **over) -> Result:
        return Result(real_api.post_retry(self.req, f"{self.base}{real_api.SCHEMES}", self.payload(**over)))


@pytest.fixture
def sb(school_api, base, offerings, school_fees, need_school_data):
    need_school_data(1)
    api = SbApi(school_api, base, offerings, school_fees)
    yield api
    for scheme_id in api.ids:   # Draft schemes can be deleted, published ones stay until the cleanup SQL
        try:
            real_api.delete_sbfas(school_api, base, scheme_id)
        except Exception:
            pass


@pytest.fixture
def hq(api, base, components):
    if not components:
        pytest.skip("needs an active fee component of Function 3")
    return HqApi(api, base, components)


def refused(r: Result, fragment: str, status: int | tuple[int, ...] = (400, 409)) -> None:
    expected = (status,) if isinstance(status, int) else status
    assert r.status in expected and r.has(fragment), f"expected {status} with {fragment!r}, got: {r.status} {r.text}"


def accepted(r: Result) -> None:
    assert r.created, f"expected 201, got: {r.text}"


# ====================================================================== SBFAS API: general step (School user)
def test_tc_268_sbfas_name_is_required(sb):
    """TC-268 Empty name and a name of spaces are refused."""
    for bad in ("", "   "):
        refused(sb.post(name=bad), "name is required")


def test_tc_269_sbfas_name_accepts_150_and_refuses_151(sb):
    """TC-269 Name of 150 characters is accepted, 151 is refused."""
    accepted(sb.post(name=_name("n150", 150)))
    refused(sb.post(name=_name("n151", 151)), "150 characters")


def test_tc_270_sbfas_open_from_today_or_later(sb):
    """TC-270 Application open from today is accepted, yesterday is refused."""
    accepted(sb.post(win=_win(_utc_today())))
    refused(sb.post(win=_win(_utc_today() - timedelta(days=1))), "today or later")


def test_tc_271_sbfas_open_to_after_open_from(sb):
    """TC-271 Application open to equal to Application open from is refused."""
    win = _win(_utc_today() + timedelta(days=10))
    refused(sb.post(win={**win, "closes": win["opens"]}), "openTo must be after openFrom")


def test_tc_272_sbfas_effective_from_after_open_to(sb):
    """TC-272 Effective from equal to Application open to is refused."""
    win = _win(_utc_today() + timedelta(days=10))
    refused(sb.post(win={**win, "eff_from": win["closes"]}), "effectiveFrom must be after openTo")


def test_tc_273_sbfas_effective_to_after_effective_from_and_may_be_empty(sb):
    """TC-273 Effective to equal to Effective from is refused, empty is accepted."""
    win = _win(_utc_today() + timedelta(days=10))
    refused(sb.post(win={**win, "eff_to": win["eff_from"]}), "effectiveTo must be after effectiveFrom")
    accepted(sb.post(effectiveTo=None))


def test_tc_274_sbfas_budget_rules(sb):
    """TC-274 Budget -1 is refused, 0 is accepted as a draft and refused with publish."""
    refused(sb.post(totalBudgetAmount=-1), "totalBudgetAmount")
    accepted(sb.post(totalBudgetAmount=0))
    refused(sb.post(totalBudgetAmount=0, publish=True), "greater than 0 when publishing")


# ====================================================================== SBFAS API: eligibility
def test_tc_275_sbfas_nationality_required_valid_unique(sb):
    """TC-275 Empty list, unknown code and duplicates are refused. All four codes are accepted."""
    refused(sb.post(nationalities=[]), "At least one nationality")
    refused(sb.post(nationalities=["XX"]), "nationality must be one of")
    refused(sb.post(nationalities=["SC", "SC"]), "duplicates")
    accepted(sb.post(nationalities=["SC", "PR", "IS_ASEAN", "IS_NON_ASEAN"]))


def test_tc_276_sbfas_needs_ghi_or_pci(sb):
    """TC-276 Both income bands off is refused."""
    refused(sb.post(isGhiEnabled=False, isPciEnabled=False), "At least one of GHI or PCI")


@pytest.mark.known_defect(reason="BUG-R4-007: the NotNull check of pciFrom never runs (When(HasValue) covers the whole chain), the API saves the scheme")
def test_tc_277_sbfas_pci_from_required_when_pci_on(sb):
    """TC-277 PCI on with an empty From is refused."""
    refused(sb.post(isPciEnabled=True, pciFrom=None, pciTo=1000), "pciFrom is required")


@pytest.mark.known_defect(reason="BUG-R4-007: the NotNull check of ghiFrom never runs (When(HasValue) covers the whole chain), the API saves the scheme")
def test_tc_278_sbfas_ghi_from_required_when_ghi_on(sb):
    """TC-278 GHI on with an empty From is refused."""
    refused(sb.post(isGhiEnabled=True, ghiFrom=None, ghiTo=100, incomeOperator="OR"), "ghiFrom is required")


def test_tc_279_sbfas_band_values_not_negative_and_to_not_below_from(sb):
    """TC-279 Negative From and To below From are refused, an empty To is accepted."""
    ghi = dict(isGhiEnabled=True, incomeOperator="OR")
    refused(sb.post(**ghi, ghiFrom=-5, ghiTo=100), "ghiFrom must be")
    refused(sb.post(pciFrom=-1, pciTo=100), "pciFrom must be")
    refused(sb.post(pciFrom=500, pciTo=100), "pciTo must be")
    refused(sb.post(**ghi, ghiFrom=500, ghiTo=100), "ghiTo must be")
    accepted(sb.post(pciFrom=0, pciTo=None))


def test_tc_280_sbfas_match_rule_needed_with_two_bands(sb):
    """TC-280 Both bands on: no rule and an unknown rule are refused, AND is accepted."""
    both = dict(isGhiEnabled=True, ghiFrom=0, ghiTo=100, isPciEnabled=True, pciFrom=0, pciTo=1000)
    refused(sb.post(**both, incomeOperator=None), "incomeOperator is required")
    refused(sb.post(**both, incomeOperator="XOR"), "'AND' or 'OR'")
    accepted(sb.post(**both, incomeOperator="AND"))


def test_tc_281_sbfas_scheme_context_max_1000(sb):
    """TC-281 Scheme context of 1000 characters is accepted, 1001 is refused."""
    accepted(sb.post(eligibilityDescription="c" * 1000))
    refused(sb.post(eligibilityDescription="c" * 1001), "1000 characters")


# ====================================================================== SBFAS API: subsidy
def test_tc_282_sbfas_needs_a_fee_component_with_an_item(sb):
    """TC-282 No fee component and a component without item are refused."""
    refused(sb.post(feeComponents=[]), "At least one fee component")
    refused(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": []}]), "at least one item")


def test_tc_283_sbfas_percentage_0_to_100(sb):
    """TC-283 -1 and 101 are refused, 0 and 100 are accepted."""
    for bad in (-1, 101):
        refused(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": sb.items(bad)}]), "between 0 and 100")
    items = sb.items(0)
    items[-1]["subsidyPercentage"] = 100
    accepted(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": items}]))


def test_tc_284_sbfas_percentage_at_most_two_decimals(sb):
    """TC-284 33.333 is refused, 33.33 is accepted."""
    refused(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": sb.items(33.333)}]), "2 decimals")
    accepted(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": sb.items(33.33)}]))


def test_tc_285_sbfas_duplicate_fee_or_grade_refused(sb):
    """TC-285 The same fee twice and the same grade twice in one fee are refused."""
    fee = {"feeComponentId": sb.fees[0]["id"], "items": sb.items()}
    refused(sb.post(feeComponents=[fee, fee]), "duplicate feeComponentId")
    refused(sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": sb.items() + sb.items()[:1]}]), "must not be duplicated")


@pytest.mark.known_defect(reason="BUG-R4-008: an unknown fee component id is saved (SBFAS and MOEFAS), nothing checks it against Function 3")
def test_tc_286_unknown_fee_component_is_refused(sb, hq):
    """TC-286 A fee component that does not exist is refused by the SBFAS and the MOEFAS API."""
    r = sb.post(feeComponents=[{"feeComponentId": UNKNOWN_ID, "items": sb.items()}])
    assert r.status in (400, 404), f"SBFAS: {r.text}"
    stages = ["PRIMARY", "SECONDARY", "PRE_UNIVERSITY"]
    r2 = hq.post(subsidies=[{"educationStage": s, "feeComponentId": UNKNOWN_ID, "subsidyPercentage": 10} for s in stages])
    assert r2.status in (400, 404), f"MOEFAS: {r2.text}"


@pytest.mark.known_defect(reason="BUG-R4-008: an unknown academicLevelId is saved, nothing checks it against the offerings of the school")
def test_tc_287_unknown_grade_is_refused(sb):
    """TC-287 A grade that the school does not offer is refused."""
    items = sb.items()
    items[0]["academicLevelId"] = UNKNOWN_GRADE
    r = sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": items}])
    assert r.status in (400, 404), r.text


@pytest.mark.known_defect(reason="BUG-R4-009: a scheme that prices one grade only is saved, the wizard blocks it")
def test_tc_288_every_grade_needs_a_value(sb):
    """TC-288 Items for one grade of two are refused."""
    if len(sb.offerings) < 2:
        pytest.skip("needs a school with two active grades")
    r = sb.post(feeComponents=[{"feeComponentId": sb.fees[0]["id"], "items": sb.items()[:1]}])
    assert r.status == 400, r.text


# ====================================================================== SBFAS API: Add fee to a published scheme
@pytest.fixture
def published(make_sbfas, school_fees):
    """A published SBFAS scheme with the first fee. Returns (scheme, a fee id that is not in it or the same id)."""
    scheme = make_sbfas("vfee", publish=True)
    other = next((f["id"] for f in school_fees if f["id"] not in scheme["fee_ids"]), scheme["fee_ids"][0])
    return scheme, other


def test_tc_289_add_fee_percentage_range_and_decimals(sb, published):
    """TC-289 Add fee API: -1 and 101 are refused with the range message, 33.333 with the decimals message."""
    scheme, other = published
    for bad in (-1, 101):
        refused(sb.add_fee(scheme["id"], other, sb.items(bad)), "between 0 and 100")
    refused(sb.add_fee(scheme["id"], other, sb.items(33.333)), "2 decimals")


def test_tc_290_add_fee_needs_an_item_and_no_repeated_grade(sb, published):
    """TC-290 Add fee API: no item and a repeated grade are refused."""
    scheme, other = published
    refused(sb.add_fee(scheme["id"], other, []), "At least one item")
    refused(sb.add_fee(scheme["id"], other, sb.items() + sb.items()[:1]), "must not be duplicated")


def test_tc_291_add_fee_existing_fee_is_refused(sb, published):
    """TC-291 Add fee API: a fee already in the scheme gives 409."""
    scheme, _ = published
    refused(sb.add_fee(scheme["id"], scheme["fee_ids"][0], sb.items()), "already configured", status=409)


@pytest.mark.known_defect(reason="BUG-R4-008: Add fee saves an unknown fee component or grade on a Published scheme")
def test_tc_292_add_fee_unknown_fee_or_grade_is_refused(sb, published):
    """TC-292 Add fee API: an unknown fee component and an unknown grade are refused."""
    scheme, other = published
    r = sb.add_fee(scheme["id"], UNKNOWN_ID, sb.items())
    assert r.status in (400, 404), f"unknown fee: {r.text}"
    items = sb.items()
    items[0]["academicLevelId"] = UNKNOWN_GRADE
    r2 = sb.add_fee(scheme["id"], other, items)
    assert r2.status in (400, 404), f"unknown grade: {r2.text}"


# ====================================================================== MOEFAS API (MOE HQ)
def test_tc_293_moefas_name_required_and_150(hq):
    """TC-293 Empty name is refused, 150 characters accepted, 151 refused."""
    refused(hq.post(name=""), "Scheme name is required")
    accepted(hq.post(name=_name("m150", 150)))
    refused(hq.post(name=_name("m151", 151)), "cannot exceed 150")


def test_tc_294_moefas_date_order(hq):
    """TC-294 Closes = opens, effective = closes and effective to = effective from are refused. Closing the same day at 23:59:59 is accepted."""
    d = "2400-01-01"
    base = dict(openFrom=f"{d}T00:00:00", openTo=f"{d}T00:00:00", effectiveFrom="2400-03-01T00:00:00", effectiveTo="2400-12-31T23:59:59")
    refused(hq.post(**base), "OpenTo must be later")
    accepted(hq.post(**{**base, "openTo": f"{d}T23:59:59"}))
    refused(hq.post(**{**base, "openTo": f"{d}T23:59:59", "effectiveFrom": f"{d}T23:59:59"}), "EffectiveFrom must be later")
    refused(hq.post(**{**base, "openTo": f"{d}T23:59:59", "effectiveTo": base["effectiveFrom"]}), "EffectiveTo must be later")


@pytest.mark.known_defect(reason="BUG-R4-010: MOEFAS saves a scheme whose dates are all in the past, the SBFAS API refuses the same dates")
def test_tc_295_moefas_dates_in_the_past_are_refused(hq):
    """TC-295 A scheme with all dates in 2020 and 2021 is refused."""
    r = hq.post(openFrom="2020-01-01T00:00:00", openTo="2020-06-30T23:59:59", effectiveFrom="2021-01-01T00:00:00", effectiveTo="2021-12-31T23:59:59")
    assert r.status == 400, r.text


def test_tc_296_moefas_status_draft_or_published(hq):
    """TC-296 Status Archived is refused."""
    refused(hq.post(status="Archived"), "Draft or Published")


def test_tc_297_moefas_income_rules(hq):
    """TC-297 Both bands off, negative From, To below From and no rule with two bands are refused."""
    refused(hq.post(isGhiEnabled=False, isPciEnabled=False), "At least one income")
    refused(hq.post(isGhiEnabled=True, ghiFrom=-1, ghiTo=100), "GhiFrom cannot be negative")
    refused(hq.post(pciFrom=500, pciTo=100), "PciTo must be greater")
    refused(hq.post(isGhiEnabled=True, ghiFrom=0, ghiTo=100, incomeOperator=None), "IncomeOperator")


def test_tc_298_moefas_nationality_rules(hq):
    """TC-298 Empty list, unknown code and duplicates are refused."""
    refused(hq.post(nationalities=[]), "At least one eligible nationality")
    refused(hq.post(nationalities=["XX"]), "Invalid nationality")
    refused(hq.post(nationalities=["SC", "SC"]), "duplicates")


def test_tc_299_moefas_subsidy_rules(hq):
    """TC-299 No subsidy, an unknown stage and a repeated stage with the same fee are refused."""
    fee = hq.components[0]["id"]
    refused(hq.post(subsidies=[]), "At least one subsidy")
    refused(hq.post(subsidies=[{"educationStage": "KINDER", "feeComponentId": fee, "subsidyPercentage": 10}]), "EducationStage must be")
    row = {"educationStage": "PRIMARY", "feeComponentId": fee, "subsidyPercentage": 10}
    refused(hq.post(subsidies=[row, row]), "duplicate combinations")


def test_tc_300_moefas_percentage_range(hq):
    """TC-300 -1 and 101 are refused."""
    fee = hq.components[0]["id"]
    for bad in (-1, 101):
        refused(hq.post(subsidies=[{"educationStage": "PRIMARY", "feeComponentId": fee, "subsidyPercentage": bad}]), "between 0.00% and 100.00%")


@pytest.mark.known_defect(reason="BUG-R4-002: MOEFAS accepts a percentage with three decimals, the SBFAS API refuses it")
def test_tc_301_moefas_percentage_at_most_two_decimals(hq):
    """TC-301 33.333 is refused."""
    fee = hq.components[0]["id"]
    r = hq.post(subsidies=[{"educationStage": "PRIMARY", "feeComponentId": fee, "subsidyPercentage": 33.333}])
    assert r.status == 400, r.text


def test_tc_302_moefas_budget_not_negative(hq):
    """TC-302 Budget -1 is refused."""
    refused(hq.post(totalBudgetAmount=-1), "TotalBudgetAmount cannot be negative")


def test_tc_303_moefas_duplicate_name_refused(hq):
    """TC-303 A second scheme with the same name is refused."""
    name = _name("mdup")
    accepted(hq.post(name=name))
    refused(hq.post(name=name), "already exists")


# ====================================================================== SBFAS wizard (School user)
FEES_LABELS = ("Name is required.", "Opening date is required.", "Closing date is required.", "Effective date is required.")


def _msg(page, text: str):
    return page.get_by_text(text, exact=True).first


def _sb_general(w, win=None, name=None, budget="1000"):
    w.fill_general(name or real_api.unique_name("sbui"), win or real_api.sbfas_window(1), budget)


def test_tc_304_sbfas_wizard_name_and_dates_required(sbfas_wiz, school_page):
    """TC-304 Next on an empty General step shows four messages. Spaces in the name give Name is required."""
    sbfas_wiz.go_next()
    for text in FEES_LABELS:
        expect(_msg(school_page, text)).to_be_visible()
    assert sbfas_wiz.current_step() == "General"
    sbfas_wiz.name.fill("   ")
    sbfas_wiz.go_next()
    expect(_msg(school_page, "Name is required.")).to_be_visible()
    assert sbfas_wiz.current_step() == "General"


def test_tc_305_sbfas_wizard_date_messages(sbfas_wiz, school_page):
    """TC-305 Closing = opening, effective = closing, effective end = effective and opening yesterday each show their message. Empty Effective to moves on."""
    win = real_api.sbfas_window(1)
    checks = [
        ("open_to", win["opens"], "Closing date must be after opening date."),
        ("eff_from", win["closes"], "Effective date must be after the closing date."),
        ("eff_to", win["eff_from"], "Effective end date must be after the effective date."),
        ("open_from", (_utc_today() - timedelta(days=1)).isoformat(), "Opening date cannot be before today."),
    ]
    for field, value, message in checks:
        _sb_general(sbfas_wiz, win)
        getattr(sbfas_wiz, field).fill(value)
        sbfas_wiz.go_next()
        expect(_msg(school_page, message)).to_be_visible()
        assert sbfas_wiz.current_step() == "General", f"{message} should block Next"
    _sb_general(sbfas_wiz, win)
    sbfas_wiz.eff_to.fill("")
    sbfas_wiz.go_next()
    expect(school_page.get_by_text("Eligible nationalities")).to_be_visible()


def test_tc_306_sbfas_wizard_name_max_150(sbfas_wiz, school_page):
    """TC-306 The name field stops at 150 characters (maxlength). If a longer value gets in, the message Name must be 150 characters or fewer shows. 150 moves on."""
    _sb_general(sbfas_wiz, name=_name("ui151", 151))
    assert sbfas_wiz.name.get_attribute("maxlength") == "150"
    assert len(sbfas_wiz.name.input_value()) <= 150, "the field accepted more than 150 characters"
    sbfas_wiz.name.fill(_name("ui150", 150))
    sbfas_wiz.go_next()
    expect(school_page.get_by_text("Eligible nationalities")).to_be_visible()


@pytest.mark.known_defect(reason="BUG-R4-014: text and an empty budget show Budget cannot be negative, which is the wrong reason")
def test_tc_307_sbfas_wizard_budget_messages(sbfas_wiz, school_page):
    """TC-307 -1 says the budget cannot be negative, text and empty say a number is needed, three decimals are refused, 0 is accepted."""
    err = school_page.locator("#sbfas-budget-error")

    def shown(value: str) -> str:
        _sb_general(sbfas_wiz, budget=value)
        sbfas_wiz.go_next()
        expect(err).to_be_visible()
        return err.inner_text().strip()

    assert shown("-1") == "Budget cannot be negative."
    assert shown("1234.567") == "Budget can have at most two decimal places."
    for value in ("abc", ""):
        assert shown(value) != "Budget cannot be negative.", f"{value!r} shows the negative-number message"
    _sb_general(sbfas_wiz, budget="0")
    sbfas_wiz.go_next()
    expect(school_page.get_by_text("Eligible nationalities")).to_be_visible()


def test_tc_308_sbfas_wizard_nationality_and_band_messages(sbfas_wiz, school_page):
    """TC-308 No nationality, both bands off, empty From, To below From and negative From are refused. From 0 with an empty To moves on."""
    sbfas_wiz.to_eligibility()
    sbfas_wiz.go_next()
    expect(_msg(school_page, "Select at least one nationality.")).to_be_visible()
    tick(school_page.locator("#sbfas-nationality-SC"))
    untick(school_page.locator("#sbfas-ghi-enabled"))
    untick(school_page.locator("#sbfas-pci-enabled"))
    sbfas_wiz.go_next()
    expect(_msg(school_page, "Enable at least one income band.")).to_be_visible()
    tick(school_page.locator("#sbfas-pci-enabled"))
    for frm, to, message in (("", "1000", "Enter a value of zero or more."), ("500", "100", "The upper value must be at least the lower value."), ("-1", "1000", "Enter a value of zero or more.")):
        school_page.locator("#sbfas-pci-from").fill(frm)
        school_page.locator("#sbfas-pci-to").fill(to)
        sbfas_wiz.go_next()
        expect(_msg(school_page, message)).to_be_visible()
    school_page.locator("#sbfas-pci-from").fill("0")
    school_page.locator("#sbfas-pci-to").fill("")
    sbfas_wiz.go_next()
    expect(school_page.get_by_role("heading", name="Active fee components")).to_be_visible()


@pytest.mark.known_defect(reason="BUG-R4-014: -1, 101 and an empty cell show Enter a subsidy percentage for every active level, which does not name the range 0 to 100")
def test_tc_309_sbfas_wizard_percentage_cells(sbfas_wiz, school_page, school_fees, offerings, need_school_data):
    """TC-309 -1, 101 and an empty cell block Review with a message that names 0 to 100. 33.333 names the decimals. 0 and 100 open Review."""
    need_school_data(1)
    sbfas_wiz.to_subsidy()
    fee = school_fees[0]["name"]
    sbfas_wiz.pick(fee)
    first, last = offerings[0]["levelName"], offerings[-1]["levelName"]
    for level in (o["levelName"] for o in offerings):
        sbfas_wiz.cell(fee, level).fill("10")

    def blocked_text(value: str) -> str:
        sbfas_wiz.cell(fee, first).fill(value)
        sbfas_wiz.go_next()
        assert sbfas_wiz.page.get_by_role("heading", name="Review SBFAS scheme").count() == 0, f"{value!r} did not block Review"
        return " ".join(school_page.locator("[id*='error'], [role='alert']").all_inner_texts())

    texts = {v: blocked_text(v) for v in ("-1", "101", "", "33.333")}
    assert "decimal" in texts["33.333"].lower(), texts["33.333"]
    for value in ("-1", "101", ""):
        assert re.search(r"0\D+100", texts[value]), f"{value!r} shows {texts[value]!r}"
    sbfas_wiz.cell(fee, first).fill("0")
    sbfas_wiz.cell(fee, last).fill("100")
    sbfas_wiz.review()


@pytest.mark.known_defect(reason="BUG-R4-015: a duplicate name shows the generic toast Unable to create scheme, the reason is hidden")
def test_tc_310_sbfas_wizard_duplicate_name_message(sbfas_wiz, school_page, make_sbfas, school_fees, offerings, need_school_data):
    """TC-310 Save draft with the name of an existing scheme says that the name already exists."""
    need_school_data(1)
    existing = make_sbfas("uidup")
    sbfas_wiz.to_subsidy(name=existing["name"])
    fee = school_fees[0]["name"]
    sbfas_wiz.pick(fee)
    for o in offerings:
        sbfas_wiz.cell(fee, o["levelName"]).fill("10")
    sbfas_wiz.review()
    sbfas_wiz.save_draft()
    expect(school_page.get_by_text("Unable to create scheme").first).to_be_visible()
    assert school_page.get_by_text(re.compile("already exists", re.I)).count() > 0, "the screen does not say that the name already exists"


def test_tc_311_sbfas_add_fee_dialog_validation(published, sbfas_list, sbfas_add_fee, school_page, school_api, base, offerings, school_fees):
    """TC-311 Add fee dialog: 101, -1 and 33.333 keep the dialog open and save nothing, an empty cell shows the toast, 15 saved."""
    scheme, other = published
    if other == scheme["fee_ids"][0]:
        pytest.skip("needs a second active fee component for the school")
    sbfas_list.open()
    sbfas_list.search(scheme["name"])
    sbfas_list.do_action(scheme["name"], "Add fee")
    expect(sbfas_add_fee.dialog).to_be_visible()
    new_fee = next(f["name"] for f in school_fees if f["id"] == other)
    sbfas_add_fee.fee_select.select_option(label=new_fee)
    levels = [o["levelName"] for o in offerings]
    for bad in ("101", "-1", "33.333"):
        for lvl in levels:
            sbfas_add_fee.percentage(lvl).fill("10")
        sbfas_add_fee.percentage(levels[0]).fill(bad)
        sbfas_add_fee.submit.click()
        expect(sbfas_add_fee.dialog).to_be_visible()
    count = next(s for s in real_api.list_sbfas(school_api, base) if s["id"] == scheme["id"])["feeComponentCount"]
    assert count == 1, f"a wrong value was saved, fee count is {count}"
    sbfas_add_fee.percentage(levels[0]).fill("")
    sbfas_add_fee.submit.click()
    expect(school_page.get_by_text("Check the fee details").first).to_be_visible()
    for lvl in levels:
        sbfas_add_fee.percentage(lvl).fill("15")
    sbfas_add_fee.submit.click()
    expect(school_page.get_by_text("Fee added", exact=False).first).to_be_visible()


# ====================================================================== MOEFAS wizard (MOE HQ)
def test_tc_312_moefas_wizard_name_max_150(wiz, page):
    """TC-312 A name of 151 characters shows the 150 message, 150 moves on."""
    win = real_api.window()
    wiz.fill_general(_name("hq151", 151), win)
    wiz.go_next()
    expect(wiz.error("Scheme name must not exceed 150 characters.")).to_be_visible()
    wiz.name.fill(_name("hq150", 150))
    wiz.go_next()
    expect(page.get_by_role("heading", level=2, name="Eligibility", exact=True)).to_be_visible()


def test_tc_313_moefas_wizard_negative_band_and_to_below_from(wiz, page):
    """TC-313 Negative From shows the number message, To below From shows the To message."""
    wiz.to_eligibility()
    tick(wiz.nationality("Singapore Citizen"))
    wiz.use_band("ghi", "-1", "100")
    wiz.use_band("pci", "-5", "100")
    wiz.go_next()
    expect(page.get_by_text("Enter a valid number of 0 or more.", exact=True).first).to_be_visible()
    page.locator("#moefas-create-ghi-from").fill("500")
    page.locator("#moefas-create-pci-from").fill("0")
    wiz.go_next()
    expect(page.get_by_text("To must not be less than From.", exact=True).first).to_be_visible()


@pytest.mark.draft
def test_tc_314_moefas_wizard_duplicate_name_message(wiz, page, make_scheme, need_components):
    """TC-314 Draft with the name of an existing scheme says that the name already exists. Draft: the case book has no wording for this message."""
    need_components(1)
    existing = make_scheme("hqdup")
    wiz.complete(existing["name"], real_api.window(3))
    wiz.draft_btn.click()
    expect(page.get_by_text(re.compile("already exists", re.I)).first).to_be_visible()


# ====================================================================== earlier gaps: TC-161, TC-165, TC-225
@pytest.mark.readonly
def test_tc_161_calls_without_a_session_return_401(playwright, base):
    """TC-161 Without a session both scheme lists answer 401."""
    anonymous = playwright.request.new_context()
    try:
        for path in (real_api.SCHEMES, real_api.SBFAS):
            status = anonymous.get(f"{base}{path}?pageNumber=1&pageSize=1").status
            assert status == 401, f"{path} answered {status} without a session"
    finally:
        anonymous.dispose()


@pytest.mark.readonly
@pytest.mark.known_defect(reason="BUG-R4-013: the School user can GET the MOEFAS schemes (200), only POST is refused")
def test_tc_165_school_user_cannot_read_moefas(school_api, api, base):
    """TC-165 The School user gets 403 on the MOEFAS list and MOE HQ gets 403 on the SBFAS list."""
    assert api.get(f"{base}{real_api.SBFAS}?pageNumber=1&pageSize=1").status == 403, "MOE HQ must not read SBFAS"
    assert school_api.get(f"{base}{real_api.SCHEMES}?pageNumber=1&pageSize=1").status == 403, "the School user reads MOEFAS"


@pytest.mark.known_defect(reason="BUG-R4-003: Publish does not check overlaps, so the second Published scheme with the same period is accepted")
def test_tc_225_draft_overlap_allowed_overlap_refused_at_publish(api, base, components):
    """TC-225 Two Drafts with the same period are accepted. A Published scheme on the same period of a Published one is refused."""
    if not components:
        pytest.skip("needs an active fee component of Function 3")
    ids = [components[0]["id"]]
    win = real_api.window(7)
    ok_a, _, msg_a = real_api.create_scheme(api, base, name=real_api.unique_name("ovA"), win=win, component_ids=ids, status="Published")
    assert ok_a, f"setup: {msg_a}"
    ok_b, _, msg_b = real_api.create_scheme(api, base, name=real_api.unique_name("ovB"), win=win, component_ids=ids, status="Draft")
    assert ok_b, f"a Draft with an overlapping period must be accepted: {msg_b}"
    ok_c, _, msg_c = real_api.create_scheme(api, base, name=real_api.unique_name("ovC"), win=win, component_ids=ids, status="Published")
    assert not ok_c, "the overlapping Published scheme was accepted"


# ====================================================================== markers
# Tests that only type into a form or only read are `readonly`, the others create data and are `mutating`.
_READONLY = {161, 165, 304, 305, 306, 307, 308, 309, 312, 313}
for _test_name, _fn in list(globals().items()):
    _m = re.match(r"test_tc_(\d{3})_", _test_name)
    if _m and int(_m.group(1)) not in _READONLY:
        pytest.mark.mutating(_fn)
