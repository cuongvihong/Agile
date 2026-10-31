"""UAT-031, UAT-031-E1 and UAT-033 (Gavin, FAS assessment). Design of 31 Oct 2026 (uat-master_v4_chain.xlsx), written against the screens of the current build.

The flow that these cases check (client rule of 30 Oct 2026): the parent submits a FAS application, MOE HQ evaluates it against the MOEFAS rule
(Singapore Citizen, GHI up to S$4,000 or PCI up to S$1,100), an application that MOEFAS does not approve moves to the school SBFAS list as
Pending School Review, and an approved application gives a subsidy on the charge of the child from the effective date of the scheme.

UAT-031     MOE HQ FAS applications: every row agrees with the rule (expected table written from the scheme), read only, no duplicate on rerun.
UAT-031-E1  Not approved by MOEFAS: HQ shows Not approved, the school list shows the application once as Pending School Review.
UAT-033     Parent view of a subsidised charge: Gross, Subsidy, Amount due; pay the net by the Education Account only.

Environment facts that decide what can be seen today: the MOEFAS scheme is effective from 1 Dec 2026, so before that date no allocation is granted and the
subsidy steps of UAT-033 are BLOCKED. There is one school user (no School B) and no household with Permanent Resident status in the data.
Nothing is created here, so there is nothing to clean up.
"""
from __future__ import annotations

import re
from datetime import date

import pytest
from playwright.sync_api import expect

from data import seed_plan as plan
from pages import real_api
from pages.billing_page import BillingPage
from pages.real_schemes import Detail
from pages.result_page import ResultPage
from tests.test_uat_moe import _moe_page
from tests.test_uat_sch import _school_page
from uat import env
from uat.actors import sign_in_parent
from uat.admin_flows import base, sidebar

DEFAULT_GHI, DEFAULT_PCI = 4000, 1100
SUBSIDY_FROM = date(2026, 12, 1)


def _num(text: str):
    digits = re.sub(r"[^0-9.]", "", text or "")
    try:
        return float(digits) if digits else None
    except ValueError:
        return None


def _table(page) -> tuple[list[str], list[dict[str, str]]]:
    """Headers and one dict per row of the main table. The empty-state row is skipped."""
    heads = [" ".join(h.split()) for h in page.locator("main table thead th").all_inner_texts()]
    rows = []
    for tr in page.locator("main table tbody tr").all():
        cells = [" ".join(c.split()) for c in tr.locator("td").all_inner_texts()]
        if len(cells) == len(heads):
            rows.append(dict(zip(heads, cells)))
    return heads, rows


def _col(heads: list[str], *words: str) -> str:
    return next((h for h in heads if all(w in h.lower() for w in words)), "")


def _open_hq_applications(page) -> None:
    sidebar(page, "FAS applications")
    page.wait_for_load_state("networkidle")
    expect(page.locator("main table").first).to_be_visible(timeout=30_000)


def _rule_limits(uat, page) -> tuple[int, int, str]:
    """GHI and PCI limits of the MOEFAS scheme, read from its detail screen (the seeded scheme). Falls back to the client rule if the text is not found."""
    try:
        Detail(page, base()).open(real_api.SEEDED_MOE_SCHEME_ID)
        text = " ".join(page.locator("main").inner_text().split())
    except Exception as exc:  # noqa: BLE001
        text = ""
        uat.note(f"The scheme detail did not open ({type(exc).__name__}); the client rule is used.")
    ghi = re.search(r"GHI[^0-9]{0,20}([\d,]{3,})", text)
    pci = re.search(r"PCI[^0-9]{0,20}([\d,]{3,})", text)
    g = int(ghi.group(1).replace(",", "")) if ghi else DEFAULT_GHI
    p = int(pci.group(1).replace(",", "")) if pci else DEFAULT_PCI
    return g, p, ("read from the scheme detail" if ghi and pci else "client rule (not found on the detail screen)")


def _passes(ghi, pci, g_limit: int, p_limit: int) -> bool:
    """MOEFAS rule: GHI up to the limit OR PCI up to the limit (exact limit included)."""
    return (ghi is not None and ghi <= g_limit) or (pci is not None and pci <= p_limit)


def _says_not_eligible(text: str) -> bool:
    return bool(re.search(r"\bnot\b|ineligible|fail|reject|declin", text, re.I))


# ======================================================================= UAT-031
@pytest.mark.case("UAT-031")
def test_uat_031_assess_fas_applications_against_the_moefas_rule(uat):
    page = _moe_page(uat)
    g_limit, p_limit, source = _rule_limits(uat, page)

    with uat.step("Write the expected table from the MOEFAS scheme rule", "One expected result for GHI only, PCI only, neither and exact limit households"):
        table = [("GHI under the limit, PCI over", g_limit - 1, p_limit + 1), ("GHI over, PCI under the limit", g_limit + 1, p_limit - 1),
                 ("both over the limits", g_limit + 1, p_limit + 1), ("GHI exactly at the limit", g_limit, p_limit + 1), ("PCI exactly at the limit", g_limit + 1, p_limit)]
        want = [True, True, False, True, True]
        uat.check(f"the rule is read ({source}): GHI up to {g_limit} or PCI up to {p_limit}", g_limit > 0 and p_limit > 0, f"{g_limit} / {p_limit}")
        uat.check_all(*[(f"expected for '{name}' (GHI {g}, PCI {p}) is {'eligible' if w else 'not eligible'}", _passes(g, p, g_limit, p_limit) == w, f"{g}/{p}")
                        for (name, g, p), w in zip(table, want)])
        uat.note("The table is the independent expectation. Step 2 compares every application of the build with the same rule.")

    with uat.step("As MOE HQ open FAS applications and read the cards and the columns", "Read only list with the cards Total, Submitted, Pending MOE review, Approved by MOE, Not approved and the GHI, PCI, Evaluation result and Status columns"):
        _open_hq_applications(page)
        heads, rows = _table(page)
        main = " ".join(page.locator("main").inner_text().split())
        buttons = page.get_by_role("button", name=re.compile(r"^(Approve|Reject)", re.I)).count()
        uat.check_all(*[(f"the page shows the card {card}", card.lower() in main.lower(), main[:240]) for card in ("Total applications", "Submitted", "Pending MOE review", "Approved by MOE", "Not approved")])
        uat.check_all(*[(f"the table has the column {col}", bool(_col(heads, *col.lower().split())), str(heads)) for col in ("GHI", "PCI", "Evaluation result", "Status")])
        uat.check("there is no Approve or Reject button (read only)", buttons == 0, f"{buttons} found")
        ghi_c, pci_c, ev_c = _col(heads, "ghi"), _col(heads, "pci"), _col(heads, "evaluation")
        checked = 0
        for r in rows:
            ghi, pci, ev = _num(r.get(ghi_c, "")), _num(r.get(pci_c, "")), r.get(ev_c, "")
            if not ev or (ghi is None and pci is None):
                continue
            checked += 1
            expect_ok = _passes(ghi, pci, g_limit, p_limit)
            uat.check(f"{r.get(heads[0], '?')}: GHI {ghi}, PCI {pci} gives {'eligible' if expect_ok else 'not eligible'} and the list says '{ev}'",
                      (not _says_not_eligible(ev)) == expect_ok, f"{r}")
        if checked == 0:
            uat.blocked("Compare every application with the rule", "The list has no application with both incomes and an evaluation result yet. Run the precondition UAT-PRE-03 first.", "Each result agrees with the rule")
        else:
            uat.note(f"{checked} application(s) compared. The list shows the first page only. The evaluation text is read as not eligible when it contains not, ineligible, fail, reject or decline.")

    uat.blocked("Control: a Permanent Resident household and a household of School B",
                "The data has no Permanent Resident household and the environment has one school user (no School B). The rule says Singapore Citizen only.",
                "A Permanent Resident is not eligible for MOEFAS; School B does not see the applications of School A")

    with uat.step("Rerun the evaluation by reloading the list", "No duplicate application and the cards keep the same counts"):
        before_codes = [r.get(heads[0]) for r in rows]
        before_cards = main[:400]
        page.reload()
        page.wait_for_load_state("networkidle")
        expect(page.locator("main table").first).to_be_visible(timeout=30_000)
        _, rows2 = _table(page)
        codes2 = [r.get(heads[0]) for r in rows2]
        uat.check("the same applications are listed after the reload", sorted(map(str, codes2)) == sorted(map(str, before_codes)), f"{before_codes} / {codes2}")
        uat.check("no application appears twice", len(codes2) == len(set(codes2)), str(codes2))
        uat.check("the cards keep the same counts", " ".join(page.locator("main").inner_text().split())[:400] == before_cards)
    uat.conclude()


# ======================================================================= UAT-031-E1
@pytest.mark.case("UAT-031-E1")
def test_uat_031_e1_not_approved_by_moefas_moves_to_school_sbfas(uat):
    moe = _moe_page(uat)
    _open_hq_applications(moe)
    heads, rows = _table(moe)
    code_c, st_c, ev_c, stu_c = heads[0] if heads else "", _col(heads, "status"), _col(heads, "evaluation"), _col(heads, "student")
    not_approved = [r for r in rows if re.search(r"not approved", r.get(st_c, ""), re.I)]
    approved = [r for r in rows if re.search(r"approved by moe", r.get(st_c, ""), re.I)]

    with uat.step("As MOE HQ check the status of the applications on FAS applications", "An application that MOEFAS does not approve shows Not approved; an approved one shows Approved by MOE; the cards agree"):
        main = " ".join(moe.locator("main").inner_text().split())
        uat.check("the column Status is on the list", bool(st_c), str(heads))
        uat.check("every Not approved row has a not eligible evaluation result", all(_says_not_eligible(r.get(ev_c, "")) for r in not_approved), str([(r.get(code_c), r.get(ev_c)) for r in not_approved]))
        uat.check("no Approved by MOE row has a not eligible evaluation result", not any(_says_not_eligible(r.get(ev_c, "")) for r in approved), str([(r.get(code_c), r.get(ev_c)) for r in approved]))
        uat.check_all(*[(f"the page shows the card {card}", card.lower() in main.lower(), main[:240]) for card in ("Approved by MOE", "Not approved")])
        uat.note(f"On the first page: {len(approved)} Approved by MOE and {len(not_approved)} Not approved.")
    if not not_approved:
        uat.blocked("The school list shows the Not approved application once as Pending School Review",
                    "No application is Not approved in the data. The seeded household has PCI at the limit, so it passes. A household over both limits has to be submitted by the parent first (UAT-PAR-02 chain).",
                    "Pending School Review, once")
    else:
        school = _school_page(uat)
        sidebar(school, "FAS applications")
        school.wait_for_load_state("networkidle")
        expect(school.locator("main").first).to_be_visible(timeout=30_000)

        def seen(app) -> tuple[int, str]:
            text = " ".join(school.locator("main").inner_text().split())
            key = app.get(code_c) or app.get(stu_c) or ""
            hits = school.locator("main table tbody tr").filter(has_text=key) if key else school.locator("main table tbody tr").filter(has_text="__none__")
            return hits.count(), " ".join(hits.first.inner_text().split()) if hits.count() else text[:200]

        with uat.step("As the School A user open FAS Applications", "Each Not approved application is listed once and its status is Pending School Review, with no SBFAS scheme choice needed"):
            for app in not_approved:
                n, row_text = seen(app)
                if n == 0:
                    uat.note(f"{app.get(code_c)} is not on the school list. It may belong to another school (one school user only) or to another page.")
                    continue
                uat.check(f"{app.get(code_c)} is listed once", n == 1, f"{n} row(s): {row_text}")
                uat.check(f"{app.get(code_c)} has the status Pending School Review", bool(re.search(r"pending school review", row_text, re.I)), row_text)
            uat.check("the school list has a Pending School Review status for the not approved applications", bool(re.search(r"pending school review", school.locator("main").inner_text(), re.I)))
        with uat.step("Reload the school list", "Still once per application; no duplicate"):
            school.reload()
            school.wait_for_load_state("networkidle")
            for app in not_approved:
                n, row_text = seen(app)
                if n:
                    uat.check(f"{app.get(code_c)} is still listed once", n == 1, f"{n} row(s): {row_text}")
    uat.blocked("Control: an application of another school, a Permanent Resident and a school with no SBFAS scheme",
                "The environment has one school user, the data has no Permanent Resident household and no published SBFAS scheme for School A.",
                "Another school does not see it; a Permanent Resident goes straight to the school; no scheme still gives Pending School Review")
    uat.conclude()


# ======================================================================= UAT-033
@pytest.mark.case("UAT-033")
@pytest.mark.mutating
def test_uat_033_subsidy_shows_on_the_charge_and_is_paid_net(uat):
    sophia = plan.STUDENTS["sophia"]
    page = uat.actor("parent")
    billing, result = BillingPage(page, env.PARENT_URL), ResultPage(page, env.PARENT_URL)
    sign_in_parent(page, sophia["parent"])
    billing.open(sophia["code"])
    charges = billing.read_all_charges()
    granted = [c for c in charges if c.subsidy > 0]
    today = date.today()

    if not granted:
        why = (f"No charge of {sophia['name']} carries a subsidy. The MOEFAS scheme is effective from {SUBSIDY_FROM:%d %b %Y} "
               f"(today {today:%d %b %Y}) and the HQ can confirm allocations only from that date. Run on or after {SUBSIDY_FROM:%d %b %Y}, with a charge of 100.00 for the child.")
        main = " ".join(page.locator("main").inner_text().split())
        with uat.step("Open the parent Pay fees list of the child and read the amount columns", "Gross amount, Subsidy, Subsidy reason and Amount due columns are on the list"):
            heads = [" ".join(h.split()) for h in page.locator("main table thead th").all_inner_texts()]
            uat.check_all(*[(f"the table has the column {col}", any(h.lower() == col.lower() for h in heads), str(heads)) for col in ("Gross amount", "Subsidy", "Subsidy reason", "Amount due")])
            uat.check("without a granted subsidy Amount due equals Gross amount", all(c.net == c.gross for c in charges), str([(c.description, str(c.gross), str(c.net)) for c in charges]))
        uat.blocked("Charge of 100.00 shows Gross 100.00, Subsidy 40.00, Amount due 60.00 with the Details", why, "Gross 100.00, Subsidy 40.00, Amount due 60.00, Details show the grant")
        uat.blocked("Capped control: a fixed subsidy above the supported part of the charge", why + " The cap is arithmetic of the backend and needs the same grant.", "Subsidy is capped at the supported part, Amount due is never negative")
        uat.blocked("Pay the Amount due by the Education Account only and read the receipt", why, "One debit of the Amount due; the receipt shows Gross, Subsidy and Amount due")
        uat.blocked("Controls: a paid charge, a component outside the scheme and a charge before the effective date; repeat the grant", why, "No subsidy on those charges; a repeat does not give a second subsidy")
        uat.note(f"Visible today on the list: {main[:200]}")
        uat.conclude()

    sub = granted[0]
    with uat.step("Read the charge row with the subsidy", "Gross minus Subsidy equals Amount due, with a Subsidy reason and Details"):
        row = page.locator("main table tbody tr").filter(has_text=sub.description).first
        row_text = " ".join(row.inner_text().split())
        uat.check("Gross minus Subsidy equals Amount due", sub.gross - sub.subsidy == sub.net, f"{sub.gross} - {sub.subsidy} = {sub.net}")
        uat.check("a Details control is on the row", row.get_by_role("button", name=re.compile(r"detail", re.I)).count() + row.get_by_role("link", name=re.compile(r"detail", re.I)).count() > 0, row_text)
        uat.check("a Subsidy reason is shown", bool(re.search(r"MOEFAS|FAS|subsid", row_text, re.I)), row_text)
    with uat.step("Select the charge and read the Selected total", "Selected total equals Amount due"):
        billing.select([sub.description])
        main = " ".join(page.locator("main").inner_text().split())
        uat.check(f"Selected total is {sub.net:,.2f}", bool(re.search(rf"Selected total\s*SGD\s*{re.escape(f'{sub.net:,.2f}')}", main)), main[:300])
    bal = billing.balance()
    if bal < sub.net:
        uat.blocked("Pay the Amount due by the Education Account only", f"The balance {bal:,.2f} does not cover the Amount due {sub.net:,.2f}. Top up the child first (UAT-PRE-01).", "One debit of the Amount due")
    else:
        with uat.step("Pay the Amount due by the Education Account only and open the receipt", "One debit of the Amount due; the receipt shows Gross, Subsidy and Amount due"):
            billing.to_method()
            billing.choose_method("Education Account")
            billing.to_review()
            billing.authorize()
            page.wait_for_url(re.compile(r"/payment-result"), timeout=45_000)
            result.wait_final()
            text = result.text()
            uat.check("the result is Payment successful", result.title() == "Payment successful", result.title())
            uat.check("the receipt shows the subsidy", f"{sub.subsidy:,.2f}" in text, text[:300])
            uat.check("the receipt shows the Amount due", f"{sub.net:,.2f}" in text, text[:300])
            billing.open(sophia["code"])
            uat.check(f"the balance dropped by the Amount due ({sub.net:,.2f}), not by the Gross", billing.balance() == bal - sub.net, str(billing.balance()))
    uat.blocked("Controls: a paid charge, a component outside the scheme and a charge before the effective date; repeat the grant", "The data has no charge for these controls yet.", "No subsidy on those charges; a repeat does not give a second subsidy")
    uat.conclude()
