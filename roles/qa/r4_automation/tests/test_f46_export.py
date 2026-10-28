"""F4.6 Export (TC-096 to TC-100). Source: FS F4 v1.3 section 3.4. All cases are Draft: ASM-R4-08.
TC-098 needs 11 applications (SEED-R4-N25) and is listed in data/not_automated.py."""
from __future__ import annotations

import pytest

from data import seed

pytestmark = [pytest.mark.f46, pytest.mark.draft]

HQ_HEADER = ["Application", "Student", "NRIC", "School", "Grade", "Scheme", "Submitted", "System check",
             "Tier", "ML recommendation", "ML risk", "Status"]
SCHOOL_HEADER = ["Application", "Student", "NRIC", "Grade", "Submitted", "Tier", "ML recommendation",
                 "ML risk", "Status"]


def short_ids(rows):
    """Application column of the data rows as short ids."""
    return [row[0].rsplit("-", 1)[-1] for row in rows[1:]]


def test_tc_096_export_holds_the_columns_and_every_row(hq_apps):
    """TC-096 Export file holds the columns of 3.4 and every row of the list, newest first."""
    name, rows = hq_apps.export_csv()
    assert name == "fas-applications.csv"
    assert rows[0] == HQ_HEADER
    assert short_ids(rows) == seed.ALL_IDS


def test_tc_097_export_holds_only_the_filtered_and_searched_rows(hq_apps):
    """TC-097 Export holds only the filtered and searched rows."""
    hq_apps.set_filter("Scheme", "SBFAS")
    _, first = hq_apps.export_csv()
    assert short_ids(first) == ["00398", "00386"]
    hq_apps.set_filter("Scheme", "All")
    hq_apps.open_tab("Approved")
    hq_apps.do_search("lee")
    hq_apps.expect_ids(["00381"])
    _, second = hq_apps.export_csv()
    assert short_ids(second) == ["00381"]


def test_tc_099_school_export_omits_school_scheme_and_system_check(bvp_apps):
    """TC-099 School Admin export omits School, Scheme and System check."""
    bvp_apps.open_tab("All")
    bvp_apps.expect_ids(seed.BVP_IDS)
    _, rows = bvp_apps.export_csv()
    assert rows[0] == SCHOOL_HEADER
    assert short_ids(rows) == seed.BVP_IDS


def test_tc_100_export_of_an_empty_list_writes_the_header_only(hq_apps):
    """TC-100 Export of an empty list writes the header only."""
    hq_apps.do_search("zzzz")
    hq_apps.expect_empty()
    _, rows = hq_apps.export_csv()
    assert rows == [HQ_HEADER]
