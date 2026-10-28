"""F4.20 Formats (TC-264 to TC-267). Source: FS F4 v1.3 section 10.
TC-267 needs the build (language of the email)."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import seed
from pages.flows import close_form_now, open_hq_list
from pages.schemes_page import SchemesPage

pytestmark = pytest.mark.f420

MONEY = r"S\$ \d{1,3}(,\d{3})*\.\d{2}"
DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
DATE_TIME = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")


def test_tc_264_money_shows_as_s_dollar_with_thousands_separator_and_two_decimals(hq_apps, hq):
    """TC-264 Money shows as S$ with thousands separator and two decimals (drawer and MOEFAS scheme list)."""
    drawer = hq_apps.open("00412")
    S = "ELIGIBILITY CHECK"
    expect(drawer.value(S, "Gross household income")).to_contain_text("S$ 4,350.00")
    expect(drawer.value(S, "Gross household income")).to_contain_text("S$ 4,200.00")
    expect(drawer.value(S, "Per capita income")).to_contain_text("S$ 1,050.00")
    drawer.close()
    hq.go("MOEFAS schemes")
    schemes = SchemesPage(hq.page, "MOEFAS schemes")
    for name in schemes.names():
        expect(schemes.cell(name, "ELIGIBILITY")).to_have_text(
            re.compile(r"^Singapore Citizen · GHI ≤ " + MONEY + r" or PCI ≤ " + MONEY + "$"))


@pytest.mark.draft
@pytest.mark.known_defect(reason="TC-173 and TC-264 conflict: the SBFAS list shows 'PCI S$ 601 - 1,000' without decimals")
def test_tc_264_sbfas_bands_use_two_decimals_too(bvp_schemes):
    """TC-264 (SBFAS part) The Eligibility column shows the same money format for every band."""
    expect(bvp_schemes.cell("Tier 2", "ELIGIBILITY", index=0)).to_have_text(
        re.compile(r"PCI " + MONEY + " – " + MONEY))


def test_tc_265_dates_show_as_dd_mm_yyyy_in_the_list_and_the_drawer(hq_apps):
    """TC-265 Dates show as DD/MM/YYYY in the list and in the drawer History."""
    for app_id in seed.ALL_IDS:
        expect(hq_apps.cell(app_id, "SUBMITTED")).to_have_text(DATE)
    drawer = hq_apps.open("00377")
    for stamp, _ in drawer.history():
        assert DATE_TIME.match(stamp), stamp


@pytest.mark.known_defect(reason="TC-265: the scheme list shows dates as 1 Jan 2027, not DD/MM/YYYY")
def test_tc_265_the_scheme_list_shows_effective_dates_as_dd_mm_yyyy(hq_schemes):
    """TC-265 (scheme list part) Effective from and Effective to in the same form."""
    for name in hq_schemes.names():
        expect(hq_schemes.cell(name, "EFFECTIVE FROM")).to_have_text(DATE)


def test_tc_266_times_show_as_hh_mm_on_a_24_hour_clock(hq):
    """TC-266 Times show as HH:mm on a 24-hour clock in History and Decided by (after the demo close)."""
    close_form_now(hq)
    apps = open_hq_list(hq)
    drawer = apps.open("00377")
    stamps = [stamp for stamp, _ in drawer.history()]
    assert stamps and all(DATE_TIME.match(s) for s in stamps), stamps
    expect(drawer.value("DECISION", "Decided by")).to_have_text(re.compile(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}$"))
