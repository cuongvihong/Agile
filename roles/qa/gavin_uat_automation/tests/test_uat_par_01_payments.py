"""UAT-PAR-01 group: parent logs in, views the Education Account and pays fees (EA, split, failures).
Steps, data and expected results are the words of uat-master (Gavin cases).

Data map (master -> real stack):
  student.test01 / EA-001 / invoice 50.00   ->  R9 Sandbox Teo (R9-STU-14, EDU-01044) with one temporary charge of 50.00
  parent.test01                             ->  Singpass persona S7890123F (owner of the R9 children)
  student.test16 / EA-016                   ->  R9 Teen Yeo (R9-STU-10, EDU-01040)
  "invoice"                                 ->  the build pays outstanding CHARGES (the invoice is created by the payment)
The wallet balance and the charge are set in the database by db.temp_charges and put back at the end of each case.
"""
from __future__ import annotations

import re
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from pages.billing_page import BillingPage
from pages.result_page import FINAL_TITLE, ResultPage
from pages.simulator_page import SimulatorPage
from uat import env
from uat.actors import open_singpass, sign_in_parent, wait_home
from uat.flows import (PAID, SANDBOX, TEEN, RequestLog, dec, find_scenario, go_online, open_account_from_home, prepared_charges,
                       seed_on, seed_parent, simulator_available, wait_home_card)

D50, D20, D30, D0 = Decimal("50.00"), Decimal("20.00"), Decimal("30.00"), Decimal("0.00")
RESULT_URL = re.compile(r"/payment-result")


def _pages(page):
    return BillingPage(page, env.PARENT_URL), ResultPage(page, env.PARENT_URL), SimulatorPage(page, env.CHECKOUT_URL)


def _best_result_url(urls: list[str], fallback: str) -> str:
    """The address of the result page with its query. The page may drop the query after it loads, so the first address seen during the navigation is used."""
    return next((u for u in urls if "payment-result" in u and "?" in u), fallback)


def _reopen_result(page, result, url: str) -> bool:
    """Open the result page again by its address. False when the build answers 'The transaction reference is missing' (nothing to read), True when the final result shows."""
    page.goto(url)
    for _ in range(40):
        if result.missing_alert.count():
            return False
        if page.get_by_role("heading", name=FINAL_TITLE).count():
            break
        page.wait_for_timeout(500)
    result.wait_final()
    return True


def _qa_charge(billing, amount: Decimal):
    charges = [c for c in billing.read_charges() if "QA" in c.description and c.net == amount]
    assert charges, f"The temporary charge of {amount} is not on the page. Charges shown: {[(c.description, str(c.net)) for c in billing.read_charges()]}"
    return charges[0]


def _need_simulator(uat):
    ok, why = simulator_available()
    if not ok:
        uat.blocked("Online sandbox gateway is available", f"The payment checkout simulator does not answer ({why}). Start it with npm run dev:payment-checkout.")
        uat.conclude()


# ======================================================================= UAT-PAR-01
def _history_rows(page, child_name: str) -> list[str]:
    """Rows of 'Invoices & payments' of one child (Edu Account Detail, then the link)."""
    page.get_by_role("link", name=f"View invoices and payments for {child_name}").click()
    expect(page.get_by_role("heading", name=re.compile(r"Invoices & payments")).first).to_be_visible(timeout=20_000)
    try:
        page.wait_for_function("() => document.querySelectorAll('main table tbody tr').length > 0", timeout=20_000)
    except Exception:  # noqa: BLE001
        pass
    return [" ".join(r.inner_text().split()) for r in page.locator("main table tbody tr").all()]


def _check_receipt_fields(uat, result, amount: Decimal, method_word: str | None = None) -> None:
    """The fields the receipt of the build has: invoice number, issued and completed dates, gross amount, subsidy, amount due and payment method.
    The build has no invoice status field (31 Oct 2026, agreed): Paid is read from the transaction result and from the fee leaving the pay list."""
    t = " ".join(result.text().split())
    uat.check("the receipt shows an invoice number", bool(re.search(r"Invoice number\s*INV\d+", t)), t[:160])
    uat.check("the receipt shows the issued and completed dates", bool(re.search(r"Issued at\s*\S+", t)) and bool(re.search(r"Completed at\s*\S+", t)), t[:200])
    uat.check(f"the receipt shows gross amount {amount:,.2f}", bool(re.search(rf"Gross amount\s*(SGD\s*)?{re.escape(f'{amount:,.2f}')}", t)), t[:200])
    uat.check("the receipt shows the subsidy", bool(re.search(r"Subsidy\s*(SGD\s*)?[\d,]+\.\d\d", t)), t[:200])
    uat.check(f"the receipt shows amount due {amount:,.2f}", bool(re.search(rf"Amount due\s*(SGD\s*)?{re.escape(f'{amount:,.2f}')}", t)), t[:200])
    method_re = re.escape(method_word) if method_word else r"\S+"
    uat.check("the receipt shows the payment method" + (f" {method_word}" if method_word else ""),
              bool(re.search(r"Payment method\s*" + method_re, t, re.I)), t[:200])
    uat.note("The invoice is read as Paid from the result 'Payment successful' and from the fee leaving the pay list: the build receipt has no invoice status field.")


@pytest.mark.case("UAT-PAR-01")
@pytest.mark.mutating
@pytest.mark.needs_db
def test_uat_par_01_log_in_view_ea_and_pay_fees_with_ea(uat):
    with prepared_charges(uat, [50.00], balance=100.00) as ids:
        page = uat.actor("parent")
        log = RequestLog(page)
        billing, result, _ = _pages(page)
        # Singpass login is done before the first step (find_scenario may record a BLOCKED row, which cannot sit inside a step). The video shows the login.
        sign_in_parent(page, seed_parent("UAT-PAR-01", ids is not None))
        uat.note("Home is open after the Singpass login." if "/parent/" not in page.url else f"Unexpected page after login: {page.url}")
        sc = find_scenario(uat, page, billing, "ea", D50, Decimal("100.00"), ids is not None, seed="UAT-PAR-01")
        child, amt, bal = sc.student, sc.amt, sc.bal
        page.goto(env.PARENT_URL + "/")

        with uat.step("Log in with SingPass, open the child's Edu Account card on Home", "The card shows the child name, EA number and balance"):
            uat.check("Home is open after Singpass", "/parent/" not in page.url, page.url)
            card = wait_home_card(page, child["name"], f"SGD {bal:,.2f}")
            uat.check("card shows the child name", child["name"] in card, card)
            uat.check("card shows the EA code", child["ea"] in card, card)
            uat.check(f"card shows the balance SGD {bal:,.2f}", f"SGD {bal:,.2f}" in card, card)
            uat.note("Only the precondition is checked here. Card order and status rules belong to UAT-006 (Howard).")
            open_account_from_home(page, child["name"])

        with uat.step("On Edu Account Detail choose Pay fees", "Pay education charges lists only this child's outstanding charges with the amount columns and the three tiles"):
            page.get_by_role("link", name=f"View billing for {child['name']}").click()
            billing.wait_ready()
            headers = [" ".join(h.split()) for h in page.locator("main table thead th").all_inner_texts()]
            main = " ".join(page.locator("main").inner_text().split())
            uat.check("fee list is for the selected child", billing.child_name() == child["name"], billing.child_name())
            uat.check("no student chooser in between", page.get_by_role("heading", name=T.H_ACCOUNTS).count() == 0)
            uat.check_all(*[(f"the table has the column {col}", any(h.lower() == col.lower() for h in headers), str(headers))
                            for col in ("Gross amount", "Subsidy", "Subsidy reason", "Amount due", "Due date", "Status")])
            uat.check_all(*[(f"the page shows the tile {tile}", tile in main, main[:300]) for tile in ("Outstanding fees", "Education Account balance", "Selected total")])
            uat.check("Selected total is 0.00 before anything is selected", bool(re.search(r"Selected total\s*SGD\s*0\.00", main)), main[:300])
            uat.check(f"the page shows EA balance {bal:,.2f}", billing.balance() == bal, str(billing.balance()))

        with uat.step("Select the charge and compare the row with the selected total", "Gross minus Subsidy equals Amount due equals Selected total; paid or cancelled charges are not selectable"):
            charge = sc.charge(billing)
            billing.select([charge.description])
            expect(billing.selected_count).to_be_visible()
            rows = billing.read_charges()
            mine = [c for c in rows if c.description == charge.description]
            main = " ".join(page.locator("main").inner_text().split())
            uat.check("the selected fee is listed once", len(mine) == 1, str([(c.description, str(c.net)) for c in rows]))
            uat.check("Gross minus Subsidy equals Amount due", charge.gross - charge.subsidy == charge.net, f"{charge.gross} - {charge.subsidy} = {charge.net}")
            uat.check(f"Selected total is {amt:,.2f}", bool(re.search(rf"Selected total\s*SGD\s*{re.escape(f'{amt:,.2f}')}", main)), main[:300])
            uat.check("no listed fee is already Paid or Cancelled", not any(re.search(r"paid|cancel", c.due, re.I) for c in rows), str([(c.description, c.due) for c in rows]))
            uat.note("Cancelled control: the child has no cancelled fee, so the Paid control is run after the payment (step 6). A cancelled fee needs data that this suite cannot create.")

        result_url = ""
        with uat.step("In Review & authorize choose Education Account only and confirm", "The EA is debited exactly once and the result shows Payment successful with an invoice number"):
            billing.to_method()
            billing.choose_method(T.METHOD_EA)
            billing.to_review()
            seen_urls: list[str] = []
            page.on("framenavigated", lambda f: seen_urls.append(f.url) if f == page.main_frame else None)
            billing.authorize()
            page.wait_for_url(RESULT_URL, timeout=45_000)
            result.wait_final()
            result_url = _best_result_url(seen_urls, page.url)
            uat.check("result is Payment successful", result.title() == T.RESULT_SUCCEEDED, result.title())
            uat.check("an invoice number is shown", bool(re.search(r"INV\d+", result.text())), result.text()[:200])
            uat.check("exactly one payment request was sent", len(log.posts("/checkout")) == 1, str(len(log.posts("/checkout"))))

        inv_no = ""
        with uat.step("Open the receipt", "The receipt shows the invoice number, dates, gross, subsidy, amount due, method and sources, and a way back"):
            text = result.text()
            inv_no = result.fact("Invoice number") or (re.search(r"INV\d+", text).group(0) if re.search(r"INV\d+", text) else "")
            uat.check("receipt has an invoice code", bool(re.search(r"INV\d+", text)), inv_no)
            _check_receipt_fields(uat, result, amt, "Education Account")
            uat.check("receipt shows the Education Account as source", any("Education Account" in k for k, _ in result.funding_rows()), str(result.funding_rows()))
            to_child = page.locator(f"a[href*='{child['id'] or '/accounts/'}']")
            uat.check("receipt has a way back", to_child.count() > 0 or result.home_link.count() > 0)
            if to_child.count() == 0:
                uat.note("Receipt offers Back to home only. It has no link back to the paid child.")
            page.goto(f"{env.PARENT_URL}/")
            card = wait_home_card(page, child["name"], f"SGD {bal - amt:,.2f}")
            uat.check(f"EA balance on Home is now {bal - amt:,.2f} (one debit of {amt:,.2f})", f"SGD {bal - amt:,.2f}" in card, card)

        with uat.step("Return to Pay fees and open Invoices & payments", "The paid charge is no longer offered and Invoices & payments has one row for the invoice"):
            open_account_from_home(page, child["name"])
            rows = _history_rows(page, child["name"])
            mine = [r for r in rows if (inv_no and inv_no in r) or (not inv_no and f"{amt:,.2f}" in r)]
            uat.check("Invoices & payments lists the invoice exactly once", len(mine) == 1, f"{len(mine)} row(s) for {inv_no or amt}: {mine}")
            uat.check("the row shows the Education Account method", any(re.search(r"Education Account", r) for r in mine), str(mine))
            sc.open_fees(billing)
            uat.check("the paid fee is no longer payable", not any(c.description == charge.description for c in billing.read_all_charges()), str([(c.description, str(c.net)) for c in billing.read_all_charges()]))

        reopen_missing = ""
        with uat.step("Reload the result page and reopen the receipt", "One debit, one invoice and one receipt; no repeat debit or settlement"):
            if _reopen_result(page, result, result_url):
                uat.check("the result still says Payment successful", result.title() == T.RESULT_SUCCEEDED, result.title())
                uat.check("it is still the same invoice", (not inv_no) or inv_no in result.text(), inv_no)
            else:
                reopen_missing = result_url
            uat.check("no second payment request was sent", len(log.posts("/checkout")) == 1, str(len(log.posts("/checkout"))))
            sc.open_fees(billing)
            uat.check(f"the balance is still {bal - amt:,.2f} (no repeat debit)", billing.balance() == bal - amt, str(billing.balance()))
        if reopen_missing:
            uat.gap("The result page can be opened again from its address",
                    f"NOT IN BUILD: opened again by the saved address the page says 'The transaction reference is missing.' (address {'with' if '?' in reopen_missing else 'without'} a query). "
                    "The receipt can only be reached through Invoices & payments.", "The result and receipt show again, with the same invoice")
    uat.conclude()


# ======================================================================= UAT-PAR-01-N1
@pytest.mark.case("UAT-PAR-01-N1")
def test_uat_par_01_n1_singpass_error_or_cancel(uat):
    page = uat.actor("parent")
    with uat.step("Open e-Service and click Log in with SingPass", "The Singpass simulation page opens"):
        open_singpass(page)
        uat.check("on the Singpass page", "/singpass/login" in page.url, page.url)
        redirect = re.search(r"redirect_uri=([^&]+)", page.url)
        state = re.search(r"state=([^&]+)", page.url)
        uat.check("login URL carries redirect and state", bool(redirect and state), page.url)

    with uat.step("Cancel at SingPass or let SingPass return an error", "An error is shown, the user returns to the login page and cannot enter Home"):
        # The simulation page has no Cancel button. Singpass answers a cancel with error=access_denied and no code.
        from urllib.parse import unquote
        page.goto(f"{unquote(redirect.group(1))}?error=access_denied&state={state.group(1)}")
        alert = page.get_by_role("alert")
        expect(alert.first).to_be_visible(timeout=15_000)
        shown = alert.first.inner_text().strip()
        uat.check("an error message is shown", bool(shown), shown)
        if not re.search(r"MSG-0802", shown):
            uat.note(f"The build shows: '{' '.join(shown.split())}'. The code MSG-0802 of the master is not displayed.")
        page.wait_for_url(re.compile(r"/parent/login"), timeout=15_000)
        uat.check("user is back on the login page", "/parent/login" in page.url, page.url)
        page.goto(env.PARENT_URL + "/")
        page.wait_for_url(re.compile(r"/parent/login"), timeout=15_000)
        uat.check("Home cannot be opened without a session", "/parent/login" in page.url, page.url)
    uat.conclude()


# ======================================================================= UAT-PAR-01-N2
@pytest.mark.case("UAT-PAR-01-N2")
def test_uat_par_01_n2_parent_not_found_or_api_slow(uat):
    page = uat.actor("parent")
    tried: list[str] = []
    with uat.step("Open e-Service and click Log in with SingPass", "The Singpass simulation page opens"):
        open_singpass(page)
        from uat.actors import persona_options
        options = persona_options(page)
        uat.check("the simulation offers personas", len(options) > 0, str(options))
        personas = [re.match(r"(S\d{7}[A-Z])", o).group(1) for o in options if re.match(r"(S\d{7}[A-Z])", o)]
        candidates = [p for p in dict.fromkeys(personas) if p != env.PARENT_NRIC]

    with uat.step("Authenticate successfully at SingPass with a person who has no record or no child", "MSG-0801 or MSG-0809 appears and the parent cannot enter Home"):
        verdict = None
        for nric in candidates:
            tried.append(nric)
            page.context.clear_cookies()
            open_singpass(page)
            from uat.actors import pick_persona, submit_singpass
            pick_persona(page, nric)
            submit_singpass(page)
            outcome = page.get_by_role("alert").or_(page.get_by_role("heading", name=re.compile(r"education", re.I))).first
            expect(outcome).to_be_visible(timeout=30_000)
            if page.get_by_role("alert").count() > 0:
                verdict = ("error", nric, page.get_by_role("alert").first.inner_text())
                break
            page.wait_for_timeout(3_000)
            wallets = page.get_by_role("link", name=re.compile(r"^View education account details for")).count()
            if wallets == 0:
                verdict = ("empty", nric, page.locator("main").inner_text()[:200])
                break
        if verdict is None:
            pytest.skip(f"Every persona tried ({tried}) has children, so the case 'parent has no child or is not found' cannot be produced with the Singpass simulation. "
                        "It needs a persona without a record in the Government API mock.")
        kind, nric, detail = verdict
        if kind == "error":
            uat.check("an error message is shown", True, f"{nric}: {' '.join(detail.split())}")
            uat.note(f"Persona {nric}. The codes MSG-0801 and MSG-0809 of the master are not displayed by the build.")
        uat.check("the parent cannot enter Home", kind == "error",
                  f"persona {nric} signed in and sees Home with no education account. Master expects MSG-0801 and no Home.")
    uat.conclude()


# ======================================================================= UAT-PAR-01-E1
@pytest.mark.case("UAT-PAR-01-E1")
def test_uat_par_01_e1_child_has_just_turned_16(uat):
    page = uat.actor("parent")
    billing, _, _ = _pages(page)
    child = TEEN
    from pages.fas_form_page import FasPages
    from uat import fasdata

    with uat.step("Log in and choose the child card (child is 16)", "Home shows the child"):
        sign_in_parent(page)
        from uat.flows import resolve_child
        if not resolve_child(page, child)["seed"]:
            uat.blocked("Choose the child card (child is 16)",
                        f"The child {child['name']} (16 years old) is not on Home. The dev seed pack has no student near 16 (the oldest is about 9.8 years, the youngest 6.97), "
                        "so a student with a date of birth of about 15.9 years must be added (bulk import, needs the approval of the data owner).")
            uat.conclude()
        open_account_from_home(page, child["name"])
        uat.check("Education Account Detail of the 16 year old opens", child["name"] in page.locator("main").inner_text())

    with uat.step("View the EA, fees and history", "EA, fees and history can be viewed"):
        text = page.locator("main").inner_text()
        uat.check("EA details are shown", child["ea"] in text and "EA balance" in text.replace("EA BALANCE", "EA balance"), text[:120])
        page.get_by_role("link", name=f"View billing for {child['name']}").click()
        billing.wait_ready()
        uat.check("fees page opens", billing.child_name() == child["name"], billing.child_name())
        page.go_back()
        page.get_by_role("link", name=f"View invoices and payments for {child['name']}").click()
        expect(page.get_by_role("heading", name=re.compile(r"Invoices & payments")).first).to_be_visible()
        uat.check("history page opens", "/transactions" in page.url, page.url)

    with uat.step("Try to pay fees", "Payment is not possible"):
        billing.open(child["id"])
        boxes = billing.charge_boxes
        if boxes.count() == 0:
            can_pay = False
        else:
            boxes.first.check(force=True)
            can_pay = billing.continue_button.is_enabled()
        uat.check("the child cannot be paid for", not can_pay, f"{boxes.count()} charge(s) can be selected, Continue enabled = {can_pay}")

    with uat.step("Try to submit an FAS application for the 16 year old", "FAS submission is not possible"):
        fas = FasPages(page, env.PARENT_URL).open_form()
        fas.fill_applicant(fasdata.parent(), fasdata.academic_year())
        fas.fill_beneficiary(fasdata.child(age=16))
        fas.tick_commitment()
        fas.submit()
        page.wait_for_timeout(1_500)
        uat.check("no confirmation page", page.get_by_role("heading", name="Application submitted").count() == 0)
        uat.check("the age rule message is shown", page.get_by_text(re.compile(r"at least 7 and younger than 16")).count() > 0)
    uat.conclude()


# ======================================================================= UAT-PAR-01-N3
@pytest.mark.case("UAT-PAR-01-N3")
@pytest.mark.needs_db
def test_uat_par_01_n3_balance_too_low_for_ea_only(uat):
    with prepared_charges(uat, [50.00, 10.00], balance=20.00) as ids:
        page = uat.actor("parent")
        log = RequestLog(page)
        billing, _, _ = _pages(page)
        sign_in_parent(page, seed_parent("UAT-PAR-01-N3", ids is not None))
        sc = find_scenario(uat, page, billing, "short0", D50, D20, ids is not None, seed="UAT-PAR-01-N3")
        sc.open_fees(billing)
        big = sc.charge(billing)
        small = next((c for c in sorted(billing.read_all_charges(), key=lambda c: c.net) if 0 < c.net <= sc.bal and c.description != big.description), None)
        chosen = [big.description] + ([small.description] if small else [])

        def on_method(descriptions):
            sc.open_fees(billing)
            billing.select(descriptions)
            billing.to_method()
            return billing.method_state()

        if small is None:
            uat.blocked("Select a charge that the balance covers", "The child has no second outstanding charge below the balance, so the switching of EA only on and off cannot be shown. "
                        "The disabled state with the large charge is still checked in the next step.", "EA only is available while the selected total is not above the balance")
        else:
            with uat.step("Select one charge the balance covers and open Review & authorize", "The selected total is not above the balance, so Education Account only is available"):
                state = on_method([small.description])
                uat.check(f"the charge {small.net:,.2f} is not above the balance {sc.bal:,.2f}", small.net <= sc.bal, f"{small.net} / {sc.bal}")
                uat.check("EA only is available", state[T.METHOD_EA]["present"] and not state[T.METHOD_EA]["disabled"], str(state))

        with uat.step("Add the large charge so the selected total is above the balance", "EA only is disabled with a reason, Online or Both is suggested, nothing is debited and no payment record is created"):
            state = on_method(chosen)
            total = billing.total_to_pay()
            uat.check(f"the selected total {total:,.2f} is bigger than the EA balance {sc.bal:,.2f}", total > sc.bal, f"total {total}, balance {sc.bal}")
            uat.check("EA only option is disabled", state[T.METHOD_EA]["present"] and state[T.METHOD_EA]["disabled"], str(state))
            text = page.locator("main").inner_text()
            uat.check("a reason is shown", bool(re.search(r"insufficient|not enough|exceeds|cannot cover|balance", text, re.I)), text[-300:])
            uat.check("Online or Both is offered", not state[T.METHOD_ONLINE]["disabled"] or not state[T.METHOD_BOTH]["disabled"], str(state))
            uat.check("no payment was created", not log.posts("/checkout"))
            uat.check(f"balance is still {sc.bal:,.2f}", billing.method_balance() == sc.bal, str(billing.method_balance()))

        if small is not None:
            with uat.step("Remove the large charge again", "EA only is available again and the selected total, the review amount and the balance still agree"):
                sc.open_fees(billing)
                billing.select(chosen)
                page.get_by_role("checkbox", name=T.SELECT_CHARGE.format(description=big.description), exact=True).uncheck()
                billing.to_method()
                state = billing.method_state()
                uat.check("EA only is available again", state[T.METHOD_EA]["present"] and not state[T.METHOD_EA]["disabled"], str(state))
                uat.check(f"the amount to pay is {small.net:,.2f}", billing.total_to_pay() == small.net, str(billing.total_to_pay()))
                uat.check(f"the balance is {sc.bal:,.2f}", billing.method_balance() == sc.bal, str(billing.method_balance()))

        with uat.step("Reload the page with the charges selected, without confirming", "No data change: balance and charges are the same and Invoices & payments has no new row"):
            sc.open_fees(billing)
            billing.select(chosen)
            page.reload()
            billing.wait_ready()
            charges_now = [c.description for c in billing.read_all_charges()]
            uat.check("no payment request was sent", not log.posts("/checkout"))
            uat.check(f"the EA balance is still {sc.bal:,.2f}", billing.balance() == sc.bal, str(billing.balance()))
            uat.check("the charges are still outstanding", all(d in charges_now for d in chosen), str(charges_now))
    uat.conclude()


# ======================================================================= UAT-PAR-01-A1
@pytest.mark.case("UAT-PAR-01-A1")
@pytest.mark.mutating
@pytest.mark.needs_db
@pytest.mark.needs_simulator
def test_uat_par_01_a1_split_between_ea_and_online(uat):
    _need_simulator(uat)
    with prepared_charges(uat, [50.00], balance=20.00) as ids:
        page = uat.actor("parent")
        billing, result, simulator = _pages(page)
        sign_in_parent(page, seed_parent("UAT-PAR-01-A1", ids is not None))
        # the independent copy of the online only variant is read first (it needs its own seeded child), then the split child
        online_copy = None if (ids is not None or not seed_on()) else find_scenario(uat, page, billing, "online", D50, D0, False, seed="UAT-PAR-01-A1-ON")
        sc = find_scenario(uat, page, billing, "short", D50, D20, ids is not None, seed="UAT-PAR-01-A1")
        rest = sc.amt - sc.bal

        with uat.step("For child 1 select the charge, choose Both and confirm", f"The EA part equals the whole balance {sc.bal:,.2f} and the Online part is the remainder {rest:,.2f}"):
            sc.open_fees(billing)
            uat.check(f"the fee {sc.amt:,.2f} is bigger than the balance {sc.bal:,.2f}", sc.amt > sc.bal and sc.bal > 0, f"fee {sc.amt}, balance {sc.bal}")
            charge = sc.charge(billing)
            billing.select([charge.description])
            billing.to_method()
            billing.choose_method(T.METHOD_BOTH)
            ea, online = billing.split_parts()
            uat.check(f"EA part is {sc.bal:,.2f}", ea == sc.bal, str(ea))
            uat.check(f"Online part is {rest:,.2f}", online == rest, str(online))
            billing.to_review()
            split_desc = charge.description

        with uat.step("Complete the payment on the gateway", "The result shows Payment successful with an invoice number"):
            urls: list[str] = []
            page.on("framenavigated", lambda f: urls.append(f.url) if f == page.main_frame else None)
            go_online(page, billing, simulator, result, "ok")
            uat.check("result is Payment successful", result.title() == T.RESULT_SUCCEEDED, result.title())
            checkout_url = next((u for u in urls if "/checkout/" in u), "")
            result_url = _best_result_url(urls, page.url)
            m_inv = re.search(r"INV\d+", result.text())
            inv_no = result.fact("Invoice number") or (m_inv.group(0) if m_inv else "")

        with uat.step("Open the receipt for child 1", f"The receipt lists both sources with Amount due {sc.amt:,.2f}, the EA balance is 0.00 and the charge is no longer offered"):
            sources = " ".join(k for k, _ in result.funding_rows())
            uat.check("receipt lists the Education Account", "Education Account" in sources, sources)
            uat.check("receipt lists the Online Gateway", "Online Gateway" in sources, sources)
            uat.check(f"receipt shows total {sc.amt:,.2f}", f"{sc.amt:,.2f}" in result.text())
            _check_receipt_fields(uat, result, sc.amt, "Both")
            sc.open_fees(billing)
            uat.check("EA balance is 0.00", billing.balance() == D0, str(billing.balance()))

        if online_copy is None:
            uat.blocked("For child 2 choose Online only and complete the gateway payment",
                        "The independent copy needs its own seeded child and fee from the precondition UAT-PRE-02 (not available in database mode or with UAT_SEED=0).", "One online payment, no EA debit")
        else:
            with uat.step("For child 2 choose Online only and complete the gateway payment", "One online payment of the full amount, no EA movement; the receipt has one source and agrees with the charge and Invoices & payments"):
                online_copy.open_fees(billing)
                before = billing.balance()
                charge = online_copy.charge(billing)
                billing.select([charge.description])
                billing.to_method()
                billing.choose_method(T.METHOD_ONLINE)
                billing.to_review()
                go_online(page, billing, simulator, result, "ok")
                uat.check("result is Payment successful", result.title() == T.RESULT_SUCCEEDED, result.title())
                rows = dict(result.funding_rows())
                sources = " ".join(rows)
                uat.check("the receipt lists the Online Gateway", "Online Gateway" in sources, sources)
                uat.check(f"the receipt shows total {online_copy.amt:,.2f}", f"{online_copy.amt:,.2f}" in result.text())
                online_copy.open_fees(billing)
                uat.check(f"the EA balance is unchanged at {before:,.2f}", billing.balance() == before, str(billing.balance()))
                uat.check("the paid fee is gone from the pay list", not any(c.description == charge.description for c in billing.read_all_charges()))

        reopen_gap = ""
        with uat.step("Revisit the success page of child 1 and press Pay again on the same gateway session", "No second debit, credit, settlement or receipt; still one invoice and the EA balance stays 0.00"):
            uat.note("Agreed 31 Oct 2026: there is no QA control to replay the settled notification of the gateway, so the master step is replaced by what a user can do: "
                     "reopen the success page and press Pay again on the same gateway session. It does not replace a replay of the gateway notification.")
            reopened = _reopen_result(page, result, result_url)
            if reopened:
                uat.check("the success page still says Payment successful", result.title() == T.RESULT_SUCCEEDED, result.title())
                uat.check("it is still the same invoice", (not inv_no) or inv_no in result.text(), inv_no)
            else:
                reopen_gap = result_url
            if checkout_url:
                page.goto(checkout_url)
                page.wait_for_timeout(2_500)
                pay = page.get_by_role("button", name=T.SIM_PAY_OK, exact=True)
                if pay.count() and pay.first.is_enabled():
                    uat.note("The gateway session accepted a second Pay press. The checks below show whether the system moved money twice.")
                    pay.first.click()
                    page.wait_for_timeout(6_000)
                else:
                    uat.note("The gateway does not offer Pay again on a completed session, so the repeat was stopped at the gateway.")
            else:
                uat.note("The gateway address of the payment was not captured, so only the success page was revisited.")
            sc.open_fees(billing)
            uat.check("the EA balance is unchanged at 0.00 (no second debit)", billing.balance() == D0, str(billing.balance()))
            uat.check("the paid fee is not payable again", not any(c.description == split_desc for c in billing.read_all_charges()))
            page.goto(env.PARENT_URL + "/")
            open_account_from_home(page, sc.student["name"])
            rows = _history_rows(page, sc.student["name"])
            mine = [r for r in rows if inv_no and inv_no in r]
            uat.check("the history lists the invoice exactly once (no second invoice or receipt)", len(mine) == 1, f"{len(mine)} row(s) for {inv_no}: {mine}")
        if reopen_gap:
            uat.gap("The success page can be opened again from its address",
                    f"NOT IN BUILD: opened again by the saved address the page says 'The transaction reference is missing.' (address {'with' if '?' in reopen_gap else 'without'} a query). "
                    "The receipt can only be reached through Invoices & payments.", "The success page and receipt show again, with the same invoice")
    uat.conclude()


# ======================================================================= UAT-PAR-01-N4
@pytest.mark.case("UAT-PAR-01-N4")
@pytest.mark.mutating
@pytest.mark.needs_db
@pytest.mark.needs_simulator
def test_uat_par_01_n4_online_part_fails(uat):
    """Agreed with the client on 31 Oct 2026: there is no automatic refund of the EA part. A failed online part ends in Payment needs review, then the system
    check and a manual reconciliation. Expected wording: waiting for the system to refund (GAP: the build says Payment needs review). The manual part is BLOCKED (see UAT-PAR-01-E2)."""
    _need_simulator(uat)
    with prepared_charges(uat, [50.00], balance=20.00) as ids:
        page = uat.actor("parent")
        billing, result, simulator = _pages(page)
        sign_in_parent(page, seed_parent("UAT-PAR-01-N4", ids is not None))
        online_copy = None if (ids is not None or not seed_on()) else find_scenario(uat, page, billing, "online", D50, D0, False, seed="UAT-PAR-01-N4-ON")
        sc = find_scenario(uat, page, billing, "short", D50, D20, ids is not None, seed="UAT-PAR-01-N4")
        rest = sc.amt - sc.bal

        with uat.step("Choose Both and confirm. At the Online gateway let the payment fail", "The result is a negative end state with no invoice number and no receipt"):
            sc.open_fees(billing)
            charge = sc.charge(billing)
            billing.select([charge.description])
            billing.to_method()
            billing.choose_method(T.METHOD_BOTH)
            ea, online = billing.split_parts()
            uat.check(f"split is {sc.bal:,.2f} + {rest:,.2f}", (ea, online) == (sc.bal, rest), f"{ea} + {online}")
            billing.to_review()
            go_online(page, billing, simulator, result, "fail")
            title, text = result.title(), result.text()
            uat.check("result says failed or needs review", title in (T.RESULT_FAILED, T.RESULT_REVIEW), title)
            uat.check("no invoice number is shown, the invoice is not paid", bool(re.search(r"invoice number unavailable", text, re.I)) or not re.search(r"INV\d+", text), text[:300])

        with uat.step("Return to the child's fees and Edu Account", "No automatic refund (agreed 31 Oct 2026): a verifying status, the EA part stays debited and the charge is held until the system check and manual reconciliation"):
            uat.check("the result is Payment needs review (no automatic refund)", title == T.RESULT_REVIEW, title)
            uat.check("the page says the Education Account may still have been deducted", bool(re.search(r"may still have been deducted", text, re.I)), text[:300])
            sc.open_fees(billing)
            uat.check("the EA part stays debited (balance 0.00)", billing.balance() == D0, str(billing.balance()))
            uat.check("the charge is held and not offered for payment again", not any(c.description == sc.desc for c in billing.read_all_charges()), str([(c.description, str(c.net)) for c in billing.read_all_charges()]))
        uat.gap("The parent sees that the system is going to refund the EA part (Waiting for system to refund)",
                f"NOT IN BUILD: the page says '{title}' and 'Your Education Account may still have been deducted'. It does not say that a refund is awaited. The behaviour matches (no automatic refund, EA part held, charge held), the wording does not. Page text: {text[:200]}",
                "A waiting state: waiting for the system to refund the EA part")
        uat.blocked("System check and manual reconciliation of the EA part, then the parent pays again",
                    "The check and the refund are done by operations outside the product screens (agreed with the client on 31 Oct 2026). Record them by hand with UAT-PAR-01-E2.",
                    "One refund of the EA part, balance back, charge payable, one invoice and one receipt after the new payment")

        if online_copy is None:
            uat.blocked("For child 2 choose Online only and let the gateway fail", "The online only child needs its own seeded child and fee from the precondition UAT-PRE-02 (not available in database mode or with UAT_SEED=0).", "No EA movement, no receipt")
        else:
            with uat.step("For child 2 choose Online only and let the gateway fail", "Payment failed, no EA movement, no paid invoice or receipt"):
                online_copy.open_fees(billing)
                before = billing.balance()
                charge2 = online_copy.charge(billing)
                billing.select([charge2.description])
                billing.to_method()
                billing.choose_method(T.METHOD_ONLINE)
                billing.to_review()
                go_online(page, billing, simulator, result, "fail")
                title2, text2 = result.title(), result.text()
                uat.check("result says failed or needs review", title2 in (T.RESULT_FAILED, T.RESULT_REVIEW), title2)
                uat.check("no invoice number is shown", bool(re.search(r"invoice number unavailable", text2, re.I)) or not re.search(r"INV\d+", text2), text2[:300])
                online_copy.open_fees(billing)
                uat.check(f"the EA balance is unchanged at {before:,.2f} (online only never debits the EA)", billing.balance() == before, str(billing.balance()))
                after = [(c.description, str(c.net), c.due) for c in billing.read_all_charges()]
                offered = any(c.description == charge2.description for c in billing.read_all_charges())
                uat.note(f"Charges on the pay screen after the failed online payment (wanted '{charge2.description}'): {after}")
                if title2 == T.RESULT_FAILED:
                    uat.note(f"The charge is {'offered again' if offered else 'held (not offered again) after the failed online payment'}. The master does not say whether it is offered again, ask the lead.")
                else:
                    uat.note(f"The result is '{title2}', so the charge is {'still offered' if offered else 'held while the payment is reviewed'}.")
        uat.blocked("Cancel at the gateway and force an ambiguous timeout, then query the recorded payment outcome before retry",
                    "The payment simulator of the build has only the outcomes Succeeded and Failed: no cancel control and no ambiguous timeout with a queryable outcome.",
                    "Cancel shows Payment cancelled. An unknown outcome shows Payment is being processed and stays unresolved, with no blind duplicate attempt")
    uat.conclude()


# ======================================================================= UAT-PAR-01-E2
@pytest.mark.case("UAT-PAR-01-E2")
@pytest.mark.mutating
@pytest.mark.needs_db
@pytest.mark.needs_simulator
def test_uat_par_01_e2_ea_refund_fails(uat):
    """The build has no EA reversal function (agreed 31 Oct 2026), so every failed online part ends in Payment needs review. That is the state this case
    expects when the reversal fails, so steps 1 and 2 are observed on a real payment. The alert for operations and the manual reconciliation are not visible to the tester."""
    _need_simulator(uat)
    with prepared_charges(uat, [50.00], balance=20.00) as ids:
        page = uat.actor("parent")
        billing, result, simulator = _pages(page)
        sign_in_parent(page, seed_parent("UAT-PAR-01-E2", ids is not None))
        sc = find_scenario(uat, page, billing, "short", D50, D20, ids is not None, seed="UAT-PAR-01-E2")
        rest = sc.amt - sc.bal

        with uat.step("Choose Both and confirm. At the Online gateway let the payment fail", "Payment needs review: the EA may still be deducted, no invoice number, no receipt"):
            sc.open_fees(billing)
            charge = sc.charge(billing)
            billing.select([charge.description])
            billing.to_method()
            billing.choose_method(T.METHOD_BOTH)
            ea, online = billing.split_parts()
            uat.check(f"split is {sc.bal:,.2f} + {rest:,.2f}", (ea, online) == (sc.bal, rest), f"{ea} + {online}")
            billing.to_review()
            go_online(page, billing, simulator, result, "fail")
            uat.check("the result is Payment needs review (the screen of ReconciliationRequired)", result.title() == T.RESULT_REVIEW, result.title())
            text = result.text()
            uat.check("the page says the Education Account may still be deducted", bool(re.search(r"may still have been deducted", text, re.I)), text[:300])
            uat.check("no invoice number is shown, the invoice is not paid", bool(re.search(r"invoice number unavailable", text, re.I)) or not re.search(r"INV\d+", text), text[:300])
            uat.note("The master expects the EA reversal to fail. The build has no reversal function, so every failed online part ends like this.")

        with uat.step("Return to the child's fees and open Invoices & payments", "A verifying status, never Paid; the EA part stays debited; the charge is held and not offered again"):
            uat.check("the parent sees a verifying status", bool(re.search(r"reviewing this payment|needs review", result.text(), re.I)), result.text()[:300])
            sc.open_fees(billing)
            uat.check("the fee is not offered for payment again while it is under review", not any(c.description == sc.desc for c in billing.read_all_charges()), str([(c.description, str(c.net)) for c in billing.read_all_charges()]))
            uat.check("the EA part stays debited (balance 0.00)", billing.balance() == D0, str(billing.balance()))
            open_account_from_home(page, sc.student["name"]) if page.get_by_role("link", name=f"View education account details for {sc.student['name']}").count() else None
        uat.blocked("Check that operations are alerted", "The alert goes to the operations tools. The parent portal and the Admin screens the tester uses show no alert list.", "An alert or a list entry exists for operations with the amount, child and time")
        uat.blocked("Operations refund the EA part by hand and the parent pays again", "The reconciliation is done outside the product screens (no refund function, agreed 31 Oct 2026). Record it by hand: one refund of the EA part, balance back, charge payable, one invoice and one receipt after the new payment.",
                    "One refund, balance back, charge payable again, one invoice and one receipt")
    uat.conclude()
