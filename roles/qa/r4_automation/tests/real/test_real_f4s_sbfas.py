"""SBFAS schemes on the real admin portal (localhost), signed in as the School user (user `school`, Raffles Institution).

Screens: /sbfas-schemes (list, row menu), /sbfas-schemes/new (wizard), Add fee component dialog.
The case book was written on the prototype (Bukit View Primary, grades P1 to P6, tiers). The real school has its own grades and schemes,
so the tests compare the screen with the API of the same school instead of fixed prototype values.
Schemes are created through the API with a far future period (year 2300+) and a name that starts with R4-AUTO.
Cases that need a second school account (TC-224) are not automated.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_sbfas import LIST_PATH

pytestmark = [pytest.mark.real, pytest.mark.sbfas]


def _row_text(lst, name: str) -> str:
    row = lst.row(name)
    expect(row).to_have_count(1)
    return re.sub(r"\s+", " ", row.inner_text()).strip()


# ================================================================ F4.13 list
@pytest.mark.readonly
def test_tc_169_school_sees_only_own_sbfas_schemes(sbfas_list, school_api, base, api):
    """TC-169 The School user sees the SBFAS schemes of the own school, no MOEFAS scheme. Second school (MRS-0012) is not automated: needs another account."""
    own = real_api.list_sbfas(school_api, base)
    assert own, "the school has no SBFAS scheme to compare with"
    ui = sbfas_list.rows()
    ui_names = {r["Scheme"].split(" SBF-")[0].strip() for r in ui}
    api_names = {s["name"] for s in own}
    assert ui_names <= api_names, f"on screen but not in the API of the school: {ui_names - api_names}"
    total = int(re.search(r"(\d+) schemes?", sbfas_list.page.get_by_text(re.compile(r"^\d+ schemes?$")).first.inner_text()).group(1))
    assert total == len(own), f"footer says {total}, API of the school returns {len(own)}"
    assert all(s["code"].startswith("SBF-") for s in own)
    moefas_names = {s["name"] for s in real_api.list_schemes(api, base)}
    assert not (api_names & moefas_names), f"MOEFAS schemes listed for the school: {api_names & moefas_names}"


def _dmy(iso: str) -> str:
    year, month, day = iso.split("-")
    return f"{day}/{month}/{year}"


@pytest.mark.mutating
@pytest.mark.known_defect(reason="BUG-R4-012: the list shows dates as YYYY-MM-DD and has no Approved by school text; FS BR13 and the case book want DD/MM/YYYY")
def test_tc_173_row_shows_eligibility_periods_status_and_fee_count(make_sbfas, sbfas_list):
    """TC-173 A published SBFAS row shows name, code, eligibility (nationality and PCI band), the two periods as DD/MM/YYYY, status, the fee count and Approved by school. No Assessed or waiting text."""
    scheme = make_sbfas("row", publish=True)
    sbfas_list.open()
    sbfas_list.search(scheme["name"])
    assert sbfas_list.headers()[:7] == ["Scheme", "Eligibility", "Application period", "Effective period", "Status", "Fees", "Actions"], sbfas_list.headers()
    text = _row_text(sbfas_list, scheme["name"])
    win = scheme["win"]
    assert re.search(r"SBF-\d+", text), text
    assert "Singapore citizen" in text and "PCI" in text and "1,000.00" in text, text
    assert f"{_dmy(win['opens'])} – {_dmy(win['closes'])}" in text, text
    assert f"{_dmy(win['eff_from'])} – {_dmy(win['eff_to'])}" in text, text
    assert "Approved by school" in text, text
    assert "Published" in text, text
    assert re.search(r"\b1\b", text.split(win["eff_to"])[-1]), f"fee count 1 expected after the periods: {text}"
    assert "Assessed" not in text and "waiting" not in text.lower()


# ================================================================ F4.14 wizard
@pytest.mark.readonly
def test_tc_201_step_3_has_one_row_per_grade_of_the_school(sbfas_wiz, offerings):
    """TC-201 Step 3 lists exactly the active grades of the school of the School user (real: Junior College 1, Secondary 1; prototype: P1 to P6)."""
    if not offerings:
        pytest.skip("the school has no active grade")
    sbfas_wiz.to_subsidy()
    expected = [o["levelName"] for o in offerings]
    assert sbfas_wiz.levels() == expected, f"rows {sbfas_wiz.levels()}, grades of the school {expected}"


@pytest.mark.readonly
@pytest.mark.draft
def test_tc_202_picked_component_adds_a_column_with_a_cell_per_grade(sbfas_wiz, school_fees, offerings, need_school_data):
    """TC-202 Picking a fee adds a column with a removable header and one percentage cell per grade. Case book says 0 in every cell, MOEFAS starts empty (assumption, so draft)."""
    need_school_data(1)
    sbfas_wiz.to_subsidy()
    fee = school_fees[0]["name"]
    sbfas_wiz.pick(fee)
    expect(sbfas_wiz.remove_button(fee)).to_be_visible()
    for o in offerings:
        cell = sbfas_wiz.cell(fee, o["levelName"])
        expect(cell).to_be_editable()
        assert cell.input_value() in ("", "0"), f"start value {cell.input_value()!r}"
    sbfas_wiz.remove_button(fee).click()
    expect(sbfas_wiz.remove_button(fee)).to_have_count(0)


@pytest.mark.readonly
@pytest.mark.draft
def test_tc_203_step_1_has_the_moefas_dates_and_no_scheme_type_or_level(sbfas_wiz, school_page):
    """TC-203 Step 1 has the name, the two periods and the budget, with no Scheme type and no Level field."""
    assert sbfas_wiz.step_labels() == ["General", "Eligibility", "Subsidy", "Review"], sbfas_wiz.step_labels()
    for field in (sbfas_wiz.name, sbfas_wiz.open_from, sbfas_wiz.open_to, sbfas_wiz.eff_from, sbfas_wiz.eff_to, sbfas_wiz.budget):
        expect(field).to_be_visible()
    assert school_page.get_by_text("Scheme type").count() == 0
    assert school_page.get_by_label("Level", exact=True).count() == 0


# ================================================================ F4.15 publish rules
@pytest.mark.mutating
def test_tc_222_same_name_same_period_is_refused(make_sbfas, school_api, base, offerings, school_fees):
    """TC-222 A second scheme with the same name and the same period cannot be published."""
    first = make_sbfas("dup", publish=True)
    ok, _, _ = real_api.create_sbfas(school_api, base, name=first["name"], win=first["win"], fee_ids=first["fee_ids"], offerings=offerings, publish=True)
    assert not ok, "the second scheme with the same name and period was accepted"
    names = [s["name"] for s in real_api.list_sbfas(school_api, base)]
    assert names.count(first["name"]) == 1, f"{names.count(first['name'])} schemes named {first['name']}"


@pytest.mark.mutating
@pytest.mark.known_defect(reason="Build refuses by name only; FS 7.3 wants the overlap message 'The period overlaps with <name> (...)'")
def test_tc_222b_message_names_the_overlap(make_sbfas, school_api, base, offerings):
    """TC-222 The refusal message talks about the overlapping period and says what to change."""
    first = make_sbfas("dup-msg", publish=True)
    ok, _, message = real_api.create_sbfas(school_api, base, name=first["name"], win=first["win"], fee_ids=first["fee_ids"], offerings=offerings, publish=True)
    assert not ok
    assert re.search(r"overlap", message, re.I), f"message: {message}"


@pytest.mark.mutating
def test_tc_223_different_name_same_period_is_allowed(make_sbfas):
    """TC-223 A scheme with a different name can be published with exactly the same period."""
    first = make_sbfas("per-a", publish=True)
    second = make_sbfas("per-b", publish=True, win=first["win"])
    assert second["id"] and second["id"] != first["id"]


@pytest.mark.not_automated
def test_tc_224_same_name_in_another_school_is_allowed():
    """TC-224 Needs a School user of a second school; the seed has one School user only (school / Raffles Institution)."""
    pytest.skip("needs a second School account (MRS-0012 of the prototype does not exist in the seed)")


@pytest.mark.mutating
@pytest.mark.known_defect(reason="Build refuses a second scheme with the same name in the school; FS 7.3 lets the later one succeed and ends the earlier one the day before")
def test_tc_228_earlier_scheme_of_the_same_name_ends_the_day_before(make_sbfas, school_api, base, offerings):
    """TC-228 A later scheme of the same name is accepted and the earlier one gets Effective to = the day before the new Effective from."""
    first = make_sbfas("succ", publish=True)
    year = int(first["win"]["opens"][:4]) + 4
    later = {"opens": f"{year}-01-01", "closes": f"{year}-06-30", "eff_from": f"{year + 1}-01-01", "eff_to": f"{year + 1}-12-31"}
    ok, data, message = real_api.create_sbfas(school_api, base, name=first["name"], win=later, fee_ids=first["fee_ids"], offerings=offerings, publish=True)
    assert ok, f"the later scheme was refused: {message}"
    from datetime import date, timedelta
    expected = (date.fromisoformat(later["eff_from"]) - timedelta(days=1)).isoformat()
    earlier = next(s for s in real_api.list_sbfas(school_api, base) if s["id"] == first["id"])
    assert earlier["effectiveTo"] == expected, f"effectiveTo {earlier['effectiveTo']}, expected {expected}"


# ================================================================ F4.16 Add fee
@pytest.mark.mutating
def test_tc_241_add_fee_dialog_lists_missing_fees_and_saves(make_sbfas, sbfas_list, sbfas_add_fee, school_api, base, school_fees, offerings, need_school_data, school_page):
    """TC-241 Add fee on a published SBFAS scheme: the dialog offers the fees not yet in the scheme, one row per grade, and saving raises the fee count to 2."""
    need_school_data(2)
    scheme = make_sbfas("addfee", publish=True)
    sbfas_list.open()
    sbfas_list.search(scheme["name"])
    assert "Add fee" in sbfas_list.actions(scheme["name"]), "Add fee is not offered for a published scheme"
    sbfas_list.do_action(scheme["name"], "Add fee")
    expect(sbfas_add_fee.dialog).to_be_visible()
    options = sbfas_add_fee.options()
    assert scheme["fee_names"][0] not in options, f"existing fee offered again: {options}"
    new_fee = next(f["name"] for f in school_fees if f["id"] not in scheme["fee_ids"])
    assert new_fee in options, f"{new_fee} missing from {options}"
    sbfas_add_fee.fee_select.select_option(label=new_fee)
    assert sbfas_add_fee.level_rows() == [o["levelName"] for o in offerings] or all(o["levelName"] in " ".join(sbfas_add_fee.level_rows()) for o in offerings), sbfas_add_fee.level_rows()
    for o in offerings:
        sbfas_add_fee.percentage(o["levelName"]).fill("15")
    sbfas_add_fee.submit.click()
    expect(school_page.get_by_text("Fee added", exact=False).first).to_be_visible()
    updated = next(s for s in real_api.list_sbfas(school_api, base) if s["id"] == scheme["id"])
    assert updated["feeComponentCount"] == 2, updated["feeComponentCount"]
