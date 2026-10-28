"""F4.5 Search and filters (TC-069 to TC-094). Source: FS F4 v1.3 section 3.2 and 3.3.
TC-086 and TC-095 need extra seed rows (SEED-R4-N10, SEED-R4-N25) and are listed in data/not_automated.py."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import seed
from pages.applications_page import ApplicationsPage
from pages.schemes_page import SchemesPage

pytestmark = pytest.mark.f45

GRADES_ALL = ["P1", "P2", "P3", "P4", "P5", "P6", "S1", "S2", "S3", "S4"]
MOEFAS_ROWS = ["00377", "00412", "00410", "00390", "00328", "00381", "00301"]


def options_without_all(apps: ApplicationsPage, name: str) -> list[str]:
    """Options of a filter without the first one, which reads '<name>: All' (or 'Any time' for Submitted)."""
    options = apps.filter_options(name)
    assert options[0].startswith(name + ":"), options
    return options[1:]


# ------------------------------------------------------------------- search
def test_tc_069_search_by_application_id(hq_apps):
    """TC-069 Search by Application ID finds one application."""
    for term in ("00412", "APP-2026-00412", "app-2026-00412"):
        hq_apps.do_search(term)
        hq_apps.expect_ids(["00412"])


def test_tc_070_search_by_name_is_case_insensitive_contains(hq_apps):
    """TC-070 Search by student name is a case-insensitive contains match."""
    for term in ("aisha", "AISHA", "Rahman"):
        hq_apps.do_search(term)
        hq_apps.expect_ids(["00412"])
    hq_apps.do_search("lee zhi")
    hq_apps.expect_ids(["00328", "00381"])


def test_tc_071_search_by_nric_whole_or_part(hq_apps):
    """TC-071 Search by NRIC/FIN matches the whole or a part of the number."""
    for term in ("T1801177H", "t1801177h", "1801177"):
        hq_apps.do_search(term)
        hq_apps.expect_ids(["00412"])


def test_tc_072_search_without_match_shows_empty_message(hq_apps):
    """TC-072 Search with no match shows the empty message, clearing restores 9 rows."""
    hq_apps.do_search("zzzz")
    hq_apps.expect_empty()
    hq_apps.do_search("")
    hq_apps.expect_ids(seed.ALL_IDS)


@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-15: the prototype does not trim the search text (ASM-R4-07)")
def test_tc_073_search_trims_leading_and_trailing_spaces(hq_apps):
    """TC-073 Search trims leading and trailing spaces. ASM-R4-07."""
    hq_apps.do_search("  aisha  ")
    hq_apps.expect_ids(["00412"])


@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-15: the prototype accepts 120 characters and shows no helper text (ASM-R4-07)")
def test_tc_074_search_accepts_100_characters_and_warns_above(hq_apps):
    """TC-074 Search accepts up to 100 characters and warns above that. ASM-R4-07."""
    hq_apps.do_search("a" * 100)
    hq_apps.expect_empty()
    hq_apps.do_search("a" * 101)
    # the helper text is not specified word by word: any text in the filter bar that names the limit of 100
    expect(hq_apps.page.locator("main .filters").get_by_text(re.compile(r"100"))).to_be_visible()


@pytest.mark.draft
def test_tc_075_special_characters_are_searched_as_plain_text(hq_apps):
    """TC-075 Special characters and script text are searched as plain text. ASM-R4-07, ASM-R4-18."""
    dialogs = []
    hq_apps.page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    for term in ("' OR 1=1 --", "<script>alert(1)</script>", "%", "_"):
        hq_apps.do_search(term)
        hq_apps.expect_empty()
    assert dialogs == []


def test_tc_076_school_search_never_returns_other_schools(bvp_apps):
    """TC-076 School Admin search never returns an application of another school."""
    bvp_apps.open_tab("All")
    for term in ("00377", "00328", "00412", "Nur Aisyah"):
        bvp_apps.do_search(term)
        bvp_apps.expect_empty()


# ----------------------------------------------------------- filters (HQ)
def test_tc_077_school_filter_lists_four_schools_and_narrows_rows(hq_apps):
    """TC-077 School filter lists the four schools and narrows the rows."""
    assert options_without_all(hq_apps, "School") == seed.SCHOOLS
    expected = {
        "Bukit View Primary": ["00412", "00410", "00398", "00390", "00386", "00301"],
        "Meridian Secondary": ["00377"],
        "Riverside Secondary": ["00328", "00381"],
    }
    for school, ids in expected.items():
        hq_apps.set_filter("School", school)
        hq_apps.expect_ids(ids)
    hq_apps.set_filter("School", "North Vista Primary")
    hq_apps.expect_empty()


def test_tc_078_scheme_filter_separates_moefas_and_sbfas(hq_apps):
    """TC-078 Scheme filter separates MOEFAS and SBFAS."""
    hq_apps.set_filter("Scheme", "MOEFAS")
    hq_apps.expect_ids(MOEFAS_ROWS)
    hq_apps.set_filter("Scheme", "SBFAS")
    hq_apps.expect_ids(["00398", "00386"])


def test_tc_079_grade_filter_lists_p1_to_s4_and_matches_class_grade(hq_apps):
    """TC-079 Grade filter lists P1 to P6 and S1 to S4 and matches the class grade."""
    assert options_without_all(hq_apps, "Grade") == GRADES_ALL
    for grade, ids in (("P3", ["00412", "00301"]), ("P4", ["00390", "00386"]), ("P5", ["00410"]), ("S3", ["00377"])):
        hq_apps.set_filter("Grade", grade)
        hq_apps.expect_ids(ids)
    hq_apps.set_filter("Grade", "P1")
    hq_apps.expect_empty()
    for grade in GRADES_ALL:
        hq_apps.set_filter("Grade", grade)
        expect(hq_apps.id_cells.filter(has_text=re.compile("00328|00381"))).to_have_count(0)


def test_tc_080_tier_filter_matches_granted_tier_and_moefas(hq_apps):
    """TC-080 Tier filter matches the granted tier on decided rows and MOEFAS rows."""
    options = hq_apps.filter_options("Tier")
    assert [re.sub(r"\s+[-–]\s+", " - ", o) for o in options[1:]] == [
        "MOEFAS", "SBFAS - Tier 1", "SBFAS - Tier 2", "SBFAS - Tier 3"]
    hq_apps.set_filter("Tier", "MOEFAS")
    hq_apps.expect_ids(MOEFAS_ROWS)
    for tier in options[2:4]:          # SBFAS - Tier 1 and Tier 2: 00386 is decided, its ML Tier 2 is not used
        hq_apps.set_filter("Tier", tier)
        hq_apps.expect_empty()
    hq_apps.set_filter("Tier", options[4])
    hq_apps.expect_ids(["00386"])


def test_tc_081_tier_filter_matches_ml_tier_on_pending_sbfas(hq_closed):
    """TC-081 Tier filter matches the ML recommended tier on pending SBFAS rows (after the demo close)."""
    options = hq_closed.filter_options("Tier")
    tier2, tier3 = options[3], options[4]
    hq_closed.set_filter("Tier", tier3)
    hq_closed.expect_ids(["00412", "00410", "00386"])
    hq_closed.set_filter("Tier", tier2)
    hq_closed.expect_empty()
    assert "00398" not in hq_closed.short_ids()


@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-12: the prototype lists the Draft scheme name in the HQ Tier filter (ASM-R4-05)")
def test_tc_082_only_published_school_scheme_names_in_hq_tier_filter(bvp):
    """TC-082 Only published school scheme names appear in the HQ Tier filter. ASM-R4-05."""
    bvp.go("SBFAS schemes")
    wizard = SchemesPage(bvp.page, "SBFAS schemes").new_scheme()
    wizard.name_input.fill("Tier 4")
    wizard.save_draft()
    bvp.log_out()
    bvp.sign_in_hq()
    bvp.go("FAS applications")
    apps = ApplicationsPage(bvp.page)
    options = apps.filter_options("Tier")
    assert len(options) == 5, options
    assert not any("Tier 4" in o for o in options)


def test_tc_083_status_filter_shows_pending_approved_rejected(hq_apps):
    """TC-083 Status filter shows Pending, Approved or Rejected rows."""
    assert options_without_all(hq_apps, "Status") == ["Pending", "Approved", "Rejected"]
    hq_apps.set_filter("Status", "Pending")
    hq_apps.expect_ids(["00377", "00412", "00410", "00398"])
    hq_apps.set_filter("Status", "Approved")
    hq_apps.expect_ids(["00390", "00386", "00381", "00301"])
    hq_apps.set_filter("Status", "Rejected")
    hq_apps.expect_ids(["00328"])


def test_tc_084_ml_risk_filter_shows_low_medium_high(hq_apps):
    """TC-084 ML risk filter shows Low, Medium or High rows."""
    hq_apps.set_filter("ML risk", "High")
    hq_apps.expect_ids(["00390"])
    hq_apps.set_filter("ML risk", "Low")
    hq_apps.expect_ids(["00328"])
    hq_apps.set_filter("ML risk", "Medium")
    hq_apps.expect_ids([i for i in seed.ALL_IDS if i not in ("00390", "00328")])


def test_tc_085_submitted_filter_defaults_to_any_time_and_limits_range(hq_apps):
    """TC-085 Submitted filter defaults to Any time and limits the range."""
    expect(hq_apps.filter("Submitted").locator("option:checked")).to_have_text(re.compile(r"Any time"))
    hq_apps.expect_ids(seed.ALL_IDS)
    recent = ["00377", "00412", "00410", "00398"]
    hq_apps.set_filter("Submitted", "Last 7 days")
    hq_apps.expect_ids(recent)
    hq_apps.set_filter("Submitted", "Last 30 days")
    hq_apps.expect_ids(recent)
    hq_apps.set_filter("Submitted", "Any time")
    hq_apps.expect_ids(seed.ALL_IDS)


# ------------------------------------------------------- filters (School Admin)
def test_tc_087_school_filters_are_the_six_and_have_no_school_or_scheme(bvp_apps):
    """TC-087 School filters are Search, Grade, Tier, Status, ML risk and Submitted."""
    expect(bvp_apps.search).to_be_visible()
    assert bvp_apps.filter_names() == ["Grade", "Tier", "Status", "ML risk", "Submitted"]


def test_tc_088_grade_options_follow_the_grades_the_school_offers(bvp, bvp_apps):
    """TC-088 Grade options follow the grades the school offers (P1 to P6, then S1 to S4)."""
    assert options_without_all(bvp_apps, "Grade") == GRADES_ALL[:6]
    bvp.log_out()
    bvp.sign_in_school("MRS-0012")
    bvp.go("FAS applications")
    meridian = ApplicationsPage(bvp.page)
    assert options_without_all(meridian, "Grade") == GRADES_ALL[6:]


def test_tc_089_tier_options_are_the_school_sbfas_scheme_names(bvp_apps):
    """TC-089 Tier options are the names of the school SBFAS schemes."""
    assert options_without_all(bvp_apps, "Tier") == ["Tier 1", "Tier 2", "Tier 3"]
    bvp_apps.open_tab("All")
    bvp_apps.set_filter("Tier", "Tier 3")
    bvp_apps.expect_ids(["00386"])
    for tier in ("Tier 2", "Tier 1"):
        bvp_apps.set_filter("Tier", tier)
        bvp_apps.expect_empty()


def test_tc_090_school_tier_filter_matches_ml_tier_on_pending_rows(bvp_apps_after_close):
    """TC-090 School Tier filter matches the ML recommended tier on pending rows (after the demo close)."""
    apps = bvp_apps_after_close
    apps.open_tab("All")
    apps.set_filter("Tier", "Tier 3")
    apps.expect_ids(["00412", "00410", "00386"])
    apps.set_filter("Tier", "Tier 2")
    apps.expect_empty()


def test_tc_091_school_status_risk_and_submitted_filters(bvp_apps):
    """TC-091 School Status, ML risk and Submitted filters narrow the school rows."""
    bvp_apps.open_tab("All")
    bvp_apps.set_filter("Status", "Approved")
    bvp_apps.expect_ids(["00386"])
    bvp_apps.set_filter("Status", "All")
    bvp_apps.set_filter("ML risk", "High")
    bvp_apps.expect_empty()
    bvp_apps.set_filter("ML risk", "All")
    bvp_apps.set_filter("Submitted", "Last 7 days")
    bvp_apps.expect_ids(["00398"])


# ------------------------------------------------------------ combinations
def test_tc_092_filters_combine_with_and(hq_apps):
    """TC-092 Filters combine with AND."""
    hq_apps.set_filter("School", "Bukit View Primary")
    hq_apps.set_filter("Status", "Pending")
    hq_apps.expect_ids(["00412", "00410", "00398"])
    hq_apps.clear_filters()
    hq_apps.set_filter("Scheme", "SBFAS")
    hq_apps.set_filter("Status", "Pending")
    hq_apps.expect_ids(["00398"])
    hq_apps.clear_filters()
    hq_apps.set_filter("Grade", "P3")
    hq_apps.set_filter("Scheme", "MOEFAS")
    hq_apps.expect_ids(["00412", "00301"])
    hq_apps.clear_filters()
    hq_apps.set_filter("Status", "Approved")
    hq_apps.set_filter("ML risk", "Low")
    hq_apps.expect_empty()


@pytest.mark.draft
def test_tc_093_tab_and_status_filter_combine_with_and(hq_apps):
    """TC-093 A tab and the Status filter combine with AND, tab counts stay fixed. ASM-R4-06."""
    hq_apps.open_tab("Pending")
    hq_apps.set_filter("Status", "Approved")
    hq_apps.expect_empty()
    hq_apps.open_tab("Approved")
    hq_apps.set_filter("Status", "All")
    hq_apps.do_search("lee")
    hq_apps.expect_ids(["00381"])
    hq_apps.expect_tabs(seed.HQ_TABS)


def test_tc_094_clearing_a_filter_restores_the_rows(hq_apps):
    """TC-094 Clearing a filter restores the rows."""
    hq_apps.set_filter("Scheme", "SBFAS")
    hq_apps.expect_ids(["00398", "00386"])
    hq_apps.set_filter("Scheme", "All")
    hq_apps.expect_ids(seed.ALL_IDS)
