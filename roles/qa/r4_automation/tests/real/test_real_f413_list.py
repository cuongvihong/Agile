"""F4.13 MOEFAS scheme list on the real admin portal (localhost).

The case book was written for the prototype. Where the real screen differs on purpose (two Form columns, seven status
cards, Add fees rule), the test checks the behavior of the real screen and carries the marker `draft`, so BA can confirm
the rule. The comparison with the API is the main value: what the table shows must match what the backend holds.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_schemes import short_date, us_date

pytestmark = [pytest.mark.f413]

STATUS_LABEL = {   # features.moeHqMoeFas.status.* in resource.ts
    "DRAFT": "Draft", "PUBLISHED": "Published", "APPLICATION_OPEN": "Application open",
    "APPLICATION_CLOSED": "Application closed", "EFFECTIVE": "Effective", "SUSPENDED": "Suspended", "CLOSED": "Closed",
}


def test_tc_168_list_matches_the_backend(lst, api, base):
    """TC-168 The MOEFAS list shows exactly the schemes the backend holds (not deleted), and no SBFAS scheme."""
    expected = sorted(s["name"] for s in real_api.list_schemes(api, base))
    shown = sorted(lst.names())
    assert shown == expected, f"table shows {len(shown)} rows, API has {len(expected)}"


@pytest.mark.draft
def test_tc_170_page_subtitle(lst):
    """TC-170 The page subtitle explains the screen. Real text has only the first sentence of the case book (ASM: BA to confirm the long text)."""
    assert lst.subtitle().startswith("View existing MOEFAS schemes and create a new one when changes are needed.")


@pytest.mark.draft
def test_tc_171_cards_count_every_status(lst):
    """TC-171 Every status card counts the rows with that status. Real screen has seven status cards, the case book has four."""
    cards = lst.cards()
    rows = lst.rows()
    assert set(cards) == set(STATUS_LABEL.values()), f"cards: {list(cards)}"
    for label, count in cards.items():
        in_table = sum(1 for r in rows if r["Status"] == label)
        assert count == in_table, f"card {label!r} says {count}, table has {in_table}"
    assert sum(cards.values()) == len(rows)


def test_tc_172_columns_and_cells_follow_the_data(lst, api, base):
    """TC-172 The table has the FS columns and every cell shows what the backend holds (name, eligibility, dates, status)."""
    heads = lst.headers()
    for must in ("Scheme", "Eligibility", "Effective from", "Effective to", "Status"):
        assert must in heads, f"column {must!r} missing, header is {heads}"
    by_name = {s["name"]: s for s in real_api.list_schemes(api, base)}
    if not by_name:
        pytest.skip("no scheme in the stack")
    problems = []
    for row in lst.rows()[:15]:
        s = by_name.get(row["Scheme"])
        if s is None:
            problems.append(f"{row['Scheme']}: not in API")
            continue
        if not short_date(s["effectiveFrom"][:10]).search(row["Effective from"]):
            problems.append(f"{row['Scheme']}: Effective from {row['Effective from']!r} vs {s['effectiveFrom'][:10]}")
        if s.get("effectiveTo"):
            if not short_date(s["effectiveTo"][:10]).search(row["Effective to"]):
                problems.append(f"{row['Scheme']}: Effective to {row['Effective to']!r} vs {s['effectiveTo'][:10]}")
        elif row["Effective to"] != "No end date":
            problems.append(f"{row['Scheme']}: no end date expected, shows {row['Effective to']!r}")
        if "Form from" in row and row["Form from"] != us_date(s["openFrom"][:10]):
            problems.append(f"{row['Scheme']}: Form from {row['Form from']!r} vs {s['openFrom'][:10]}")
        if "Form to" in row and row["Form to"] != us_date(s["openTo"][:10]):
            problems.append(f"{row['Scheme']}: Form to {row['Form to']!r} vs {s['openTo'][:10]}")
        if s["isPciEnabled"] and "PCI" not in row["Eligibility"]:
            problems.append(f"{row['Scheme']}: PCI band missing in {row['Eligibility']!r}")
        if s["isGhiEnabled"] and "GHI" not in row["Eligibility"]:
            problems.append(f"{row['Scheme']}: GHI band missing in {row['Eligibility']!r}")
        if row["Status"] != STATUS_LABEL.get(s["status"].upper(), "Closed"):
            problems.append(f"{row['Scheme']}: status {row['Status']!r} vs API {s['status']}")
    assert not problems, "\n".join(problems)


@pytest.mark.known_defect(reason="BUG-R4-016: the list comes back in creation order, not sorted by Effective from newest first (FS 7.1 item 5)")
def test_tc_174_sort_is_effective_from_newest_first(lst):
    """TC-174 Rows are sorted by Effective from, newest first, then by name (FS)."""
    rows = lst.rows()
    if len(rows) < 2:
        pytest.skip("needs two schemes")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def day(r):
        m = re.match(r"(\w{3})\w*\.? (\d+), (\d{4})", r["Effective from"])
        return int(m[3]) * 10000 + (months.index(m[1]) + 1) * 100 + int(m[2])

    days = [day(r) for r in rows]
    # Only the Effective from order is asserted. Schemes with the same date (for example the overlap test data) may come in any order.
    assert days == sorted(days, reverse=True), f"Effective from is not newest first: {[r['Effective from'] for r in rows]}"


@pytest.mark.draft
def test_tc_178_row_actions_follow_the_status(lst):
    """TC-178/229/231 Row actions follow the status. Real rule (resource.ts suspendDialog: fee can be added until a day before the effective day):
    View always; Publish for Draft; Add fees for Draft, Published, Application open, Application closed, Suspended; Reactivate for Suspended;
    never Edit. Case book says Add fee for Active and Upcoming: BA to confirm which rule is right."""
    expected_add = {"Draft", "Published", "Application open", "Application closed", "Suspended"}
    seen: set[str] = set()
    problems = []
    for row in lst.rows():
        status = row["Status"]
        if status in seen:
            continue   # one row per status is enough
        seen.add(status)
        items = lst.actions(row["Scheme"])
        if "View" not in items:
            problems.append(f"{row['Scheme']} ({status}): no View in {items}")
        if any(i.startswith("Edit") for i in items):
            problems.append(f"{row['Scheme']} ({status}): has Edit {items}")
        if (status in expected_add) != ("Add fees" in items):
            problems.append(f"{row['Scheme']} ({status}): Add fees {'missing' if status in expected_add else 'should not show'} in {items}")
        if (status == "Draft") != ("Publish" in items):
            problems.append(f"{row['Scheme']} ({status}): Publish wrong in {items}")
        if (status == "Suspended") != ("Reactivate" in items):
            problems.append(f"{row['Scheme']} ({status}): Reactivate wrong in {items}")
    assert not problems, "\n".join(problems)


def test_tc_229_view_opens_the_read_only_detail(lst, page):
    """TC-229 View opens the scheme detail with General, Eligibility, Budget and Subsidy, and no edit control."""
    rows = lst.rows()
    if not rows:
        pytest.skip("no scheme in the stack")
    name = rows[0]["Scheme"]
    lst.do_action(name, "View")
    page.wait_for_url(re.compile(r"/moe-hq/moe-fas/[^/]+$"))
    for section in ("General", "Eligibility", "Budget", "Subsidy"):
        expect(page.get_by_role("heading", level=2, name=section, exact=True)).to_be_visible()
    expect(page.get_by_role("heading", level=1, name=name)).to_be_visible()
    expect(page.get_by_role("link", name=re.compile("^Back to schemes"))).to_be_visible()
    assert page.get_by_role("button", name=re.compile("^Edit", re.I)).count() == 0
