"""Parent payment cases of UAT Master 01: UAT-PAR-01, N1, N2, E1, N3, A1, N4, E2."""
from __future__ import annotations

import re
from decimal import Decimal
from urllib.parse import parse_qs, urlparse

from core import config
from core.util import all_money, money, norm
from core.recorder import StepBlocked
from pages import auth, eservice
from payment_helpers import (MSG_0801, MSG_0802, MSG_0809, balance_now, go_to_gateway, open_fees, pick_gt,
                             pick_le, receipt_sources, topup_precondition)

PERSONA = config.data("pay", "persona")
CHILD = config.data("pay", "child")
CHILD_NRIC = config.data("pay", "child_nric")
CHILD2 = config.data("pay", "second_child")
CHILD2_NRIC = config.data("pay", "second_child_nric")
LOW = Decimal(config.data("pay", "low_balance", default="20.00"))


def test_UAT_PAR_01(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Open e-Service and click Log in with SingPass", "Home shows a card with the child name, EA code and balance")
    def _(s):
        auth.parent_login(par, PERSONA)
        uat.map_data(f"parent.test01 / student.test01 / EA-001 -> persona {PERSONA}, child {CHILD}")
        eservice.go_home(par)
        card = eservice.card_of(par, CHILD)
        s.require(card, f"Home has the card of {CHILD}", [c['name'] for c in eservice.home_cards(par)])
        s.check(re.fullmatch(r"EDU-\d+", card["code"] or ""), "the card shows the EA code", card["code"])
        s.check(card["balance"] is not None, "the card shows the balance", card["text"][:160])
        ctx["before"] = card["balance"]

    @uat.step(2, "On Home choose the child Edu Account card", "The Edu Account Detail of the child opens", needs=(1,))
    def _(s):
        charges = open_fees(par, CHILD)  # look at the fees first to set the precondition
        target = Decimal("50.00")
        ch = pick_le(charges, ctx["before"], target)
        if ch is None and config.ALLOW_TOPUP:
            smallest = min((c["due"] for c in charges if c["due"]), default=None)
            if smallest is not None:
                topup_precondition(uat, CHILD_NRIC, smallest - ctx["before"] + Decimal("0.00"), "balance must cover one invoice")
                uat.actor("parent")
                eservice.go_home(par)
                ctx["before"] = eservice.card_of(par, CHILD)["balance"]
                charges = open_fees(par, CHILD)
                ch = pick_le(charges, ctx["before"], target)
        if ch is None:
            s.blocked(f"No payable charge of {CHILD} is covered by the EA balance {ctx['before']} (master: balance 100.00, invoice 50.00).")
        ctx["charge"] = ch
        uat.map_data(f"Master balance 100.00 and invoice 50.00 -> balance {ctx['before']} and charge '{ch['name']}' {ch['due']}")
        eservice.go_home(par)
        eservice.open_account(par, CHILD)
        info = eservice.account_info(par)
        s.check(CHILD in info["text"], "the Edu Account Detail shows the child", info["text"][:120])
        s.check(info["balance"] == ctx["before"], "the detail shows the same balance as the card", f"{info['balance']} / {ctx['before']}")

    @uat.step(3, "On Edu Account Detail choose Pay fees",
              "The fee list belongs to the selected child, with no need to choose the student again", needs=(2,))
    def _(s):
        if par.get_by_role("link", name=re.compile(r"^Pay fees", re.I)).count() == 0:
            s.same_function(f"The link is 'View billing for {CHILD}' (page 'Pay education charges'), not 'Pay fees'.")
        eservice.open_pay(par, CHILD)
        txt = eservice.main_text(par)
        s.check(f"for {CHILD}" in txt, "the fee list is for the selected child", txt[:160])
        combos = [norm(t) for t in par.locator("main select").all_inner_texts()]
        s.check(not any(CHILD in c for c in combos), "there is no student chooser on the page", combos)

    @uat.step(4, "Choose the invoice", "The selected total equals the invoice amount", needs=(3,))
    def _(s):
        eservice.select_charge(par, ctx["charge"])
        s.check(eservice.selected_count(par) == 1, "one charge is selected", eservice.selected_count(par))
        s.check(eservice.tile(par, "Selected total") == ctx["charge"]["due"], "Selected total equals the amount due",
                f"{eservice.tile(par, 'Selected total')} / {ctx['charge']['due']}")

    @uat.step(5, "Choose to pay with the EA and confirm", "The EA is debited exactly once", needs=(4,))
    def _(s):
        eservice.click_continue(par)
        m = eservice.payment_methods(par)
        s.require(m.get("EducationAccount") and not m["EducationAccount"]["disabled"], "EA only is offered", m)
        eservice.choose_method(par, "EducationAccount")
        eservice.click_continue(par)
        review = eservice.main_text(par)
        s.check(ctx["charge"]["due"] in all_money(review.split("Review & authorize")[-1]),
                "the review shows the invoice amount paid from the EA", review[-300:])
        eservice.authorize(par)
        ctx["result"] = eservice.wait_result(par)
        s.check(eservice.result_headline(ctx["result"]).lower() == "payment successful", "the result is Payment successful",
                eservice.result_headline(ctx["result"]))

    @uat.step(6, "Open the receipt",
              "Invoice Paid; receipt shows invoice code, total, method and amount per source; a way back to the child; "
              "EA debited once leaving balance - invoice", needs=(5,))
    def _(s):
        r = ctx["result"]
        inv = eservice.invoice_number(r)
        s.check(inv, "the receipt shows the invoice code", r[:200])
        s.check(money(r[r.find("Amount due"):]) == ctx["charge"]["due"] if "Amount due" in r else False,
                "the receipt shows the total", r[:400])
        s.check(re.search(r"Payment method\s*\n?\s*Education Account", r), "the receipt shows the method Education Account", r[:400])
        src = receipt_sources(r)
        s.check(src.get("Education Account") == ctx["charge"]["due"], "the receipt shows the amount per source", src)
        if not re.search(r"\bPaid\b", r):
            s.gap("The receipt does not show the invoice status Paid (it says 'Payment successful'). "
                  "Invoices & payments has no status column either.")
        back = par.get_by_role("link", name=CHILD)
        s.check(back.count() > 0, "the receipt has a way back to the child", "breadcrumb links: " + str(par.locator("main a").all_inner_texts()[:6]))
        if back.count():
            back.first.click()
            par.get_by_text("Education Account details").first.wait_for()
            info = eservice.account_info(par)
            s.check(CHILD in info["text"], "the way back opens the correct child", info["url"])
            expected = ctx["before"] - ctx["charge"]["due"]
            s.check(info["balance"] == expected, "the EA is debited once (balance before - invoice)",
                    f"before {ctx['before']}, invoice {ctx['charge']['due']}, now {info['balance']}")
            eservice.open_invoices(par, CHILD)
            rows = [x for x in eservice.invoice_rows(par) if inv and inv in x]
            s.check(len(rows) == 1, "the invoice is listed exactly once in Invoices & payments", rows)

    uat.conclude()


def test_UAT_PAR_01_N1(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Open e-Service and click Log in with SingPass", "The Singpass page opens")
    def _(s):
        auth.open_parent_login(par)
        q = parse_qs(urlparse(par.url).query)
        ctx["state"] = (q.get("state") or [""])[0]
        s.check("/singpass/login" in par.url and ctx["state"], "the Singpass login page opens with a state", par.url[:140])

    @uat.step(2, "Cancel at SingPass or let SingPass return an error",
              f"MSG-0802 '{MSG_0802}', back on the login page, Home cannot be entered", needs=(1,))
    def _(s):
        has_cancel = par.get_by_role("button", name=re.compile(r"cancel", re.I)).count()
        if has_cancel:
            par.get_by_role("button", name=re.compile(r"cancel", re.I)).first.click()
        else:
            s.note("The Singpass simulator has no Cancel button. The suite sends the OIDC cancel answer "
                   "(error=access_denied) to the e-Service callback, which is what Singpass returns on cancel.")
            par.goto(f"{config.PARENT_URL}/parent/callback?error=access_denied&error_description=User%20cancelled&state={ctx['state']}")
        par.wait_for_timeout(2500)
        shown = eservice.main_text(par)
        s.check(MSG_0802 in shown or "MSG-0802" in shown, f"MSG-0802 is shown ('{MSG_0802}')", shown[:200])
        par.wait_for_timeout(5000)
        s.check("/parent/login" in par.url, "the user is back on the login page", par.url)
        par.goto(f"{config.PARENT_URL}/")
        par.wait_for_timeout(2500)
        s.check("/parent/login" in par.url or par.get_by_text("Education wallets").count() == 0,
                "Home cannot be entered", par.url)

    uat.conclude()


def test_UAT_PAR_01_N2(uat):
    par = uat.actor("parent")
    nric, pwd = config.data("not_found", "nric"), config.data("not_found", "password")

    @uat.step(1, "Open e-Service and click Log in with SingPass", "The Singpass page opens")
    def _(s):
        auth.open_parent_login(par)
        s.check("/singpass/login" in par.url, "the Singpass page opens", par.url[:120])

    @uat.step(2, f"Authenticate successfully at SingPass as {nric} (no record in the Government API mock)",
              f"MSG-0801 '{MSG_0801}' or MSG-0809, the parent cannot enter Home", needs=(1,))
    def _(s):
        uat.map_data(f"parent.test99 -> NRIC {nric} on the Password login tab of the Singpass simulator")
        par.get_by_role("tab", name="Password login").click()
        par.get_by_placeholder("e.g. S1234567A").fill(nric)
        par.get_by_placeholder("Enter password").fill(pwd)
        par.get_by_role("button", name="Log in", exact=True).click()
        par.wait_for_timeout(6000)
        if "/singpass/" in par.url:
            s.blocked(f"The Singpass simulator does not authenticate {nric} (it stays on its own page: "
                      f"{norm(par.locator('body').inner_text())[:160]}). The case needs a Singpass identity without a record in the Government API mock.")
        shown = eservice.main_text(par)
        s.check(any(m in shown for m in (MSG_0801, MSG_0809, "MSG-0801", "MSG-0809")), "MSG-0801 or MSG-0809 is shown", shown[:200])
        s.check(par.get_by_text("Education wallets").count() == 0, "the parent is not on Home", par.url)

    uat.conclude()


def test_UAT_PAR_01_E1(uat, discovery):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "On Home choose the child card (child has just turned 16, EA Due for closure)", "Home shows the child")
    def _(s):
        hit = None
        for fam in discovery:
            for c in fam["children"]:
                if (c.get("age") or 0) >= 16 or re.search(r"closure", c.get("status", ""), re.I):
                    hit = (fam["persona"], c)
                    break
            if hit:
                break
        if not hit:
            s.blocked("No child of 16 or with EA status Due for closure exists under any Singpass test persona "
                      f"({len(discovery)} personas scanned). student.test16 / EA-016 must be seeded.")
        ctx["persona"], ctx["child"] = hit
        uat.map_data(f"student.test16 -> {hit[1]['name']} ({hit[1]['dob']}, {hit[1]['status']}) of persona {hit[0]}")
        auth.parent_login(par, ctx["persona"])
        eservice.go_home(par)
        card = eservice.card_of(par, ctx["child"]["name"])
        s.require(card, "Home shows the child card")
        s.check(re.search(r"closure", card["status"], re.I), "the card shows the EA as Due for closure", card["status"])

    @uat.step(2, "View the EA, fees and history", "EA, fees and history can be viewed", needs=(1,))
    def _(s):
        name = ctx["child"]["name"]
        eservice.open_account(par, name)
        s.check(eservice.account_info(par)["balance"] is not None, "the EA can be viewed")
        eservice.open_invoices(par, name)
        s.check("Invoices" in eservice.main_text(par), "the history can be viewed")

    @uat.step(3, "Try to pay fees and try to submit an FAS application", "Payment and FAS submission are not possible", needs=(1,))
    def _(s):
        name = ctx["child"]["name"]
        eservice.go_home(par)
        eservice.open_account(par, name)
        link = par.get_by_role("link", name=f"View billing for {name}")
        if link.count() == 0:
            s.check(True, "there is no way to pay fees for the child")
        else:
            eservice.open_pay(par, name)
            charges = eservice.charges_on_page(par)
            selectable = [c for c in charges if not c["disabled"]]
            if selectable:
                eservice.select_charge(par, selectable[0])
                cont = par.get_by_role("button", name="Continue", exact=True)
                s.check(cont.is_disabled(), "payment cannot start (Continue disabled)",
                        f"{len(selectable)} selectable charge(s), Continue enabled={not cont.is_disabled()}")
            else:
                s.check(True, "no charge can be selected for payment")
        eservice.open_my_fas(par)
        eservice.open_new_application(par)
        bens = eservice.beneficiary_names(par)
        if name in bens:
            sec = eservice.beneficiary_section(par, name).inner_text()
            s.check(re.search(r"16|not eligible|closure|cannot", sec, re.I), "the FAS form blocks the child of 16", norm(sec)[:200])
        else:
            s.check(True, "the child is not offered on the FAS form")

    uat.conclude()


def test_UAT_PAR_01_N3(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Go to the child's fees and choose the invoice (amount above the EA balance)", "The invoice is selected")
    def _(s):
        auth.parent_login(par, PERSONA)
        eservice.go_home(par)
        ctx["balance"] = eservice.card_of(par, CHILD)["balance"]
        charges = open_fees(par, CHILD)
        ch = pick_gt(charges, ctx["balance"])
        if ch is None:
            s.blocked(f"No payable charge of {CHILD} is above the EA balance {ctx['balance']} (master: balance 20.00, invoice 50.00).")
        ctx["charge"] = ch
        ctx["outstanding"] = eservice.tile(par, "Outstanding fees")
        ctx["invoices"] = None
        uat.map_data(f"Master balance 20.00, invoice 50.00 -> balance {ctx['balance']}, charge '{ch['name']}' {ch['due']}")
        eservice.select_charge(par, ch)
        s.check(eservice.tile(par, "Selected total") == ch["due"], "the selected total is the invoice amount",
                eservice.tile(par, "Selected total"))

    @uat.step(2, "Open the payment method step", "EA only is disabled with the reason; Online or Both is suggested; no data changes", needs=(1,))
    def _(s):
        eservice.click_continue(par)
        m = eservice.payment_methods(par)
        ea = m.get("EducationAccount", {})
        s.check(ea.get("disabled") is True, "the EA only option is disabled", m)
        txt = eservice.main_text(par)
        s.check(re.search(r"not enough|insufficient", txt, re.I), "the reason is shown", re.findall(r"[^\n]*(?:not enough|insufficient)[^\n]*", txt, re.I))
        s.check(m.get("OnlineGateway", {}).get("disabled") is False and m.get("Both", {}).get("disabled") is False,
                "Online and Both are offered", m)
        s.check(re.search(r"select Online Gateway or Both", txt, re.I) or m.get("Both", {}).get("checked"),
                "the system suggests Online or Both", txt[-300:])
        par.reload()
        par.wait_for_timeout(2500)
        bal = balance_now(uat, CHILD)
        s.check(bal == ctx["balance"], "the EA balance is unchanged", f"{bal} / {ctx['balance']}")
        open_fees(par, CHILD)
        s.check(eservice.tile(par, "Outstanding fees") == ctx["outstanding"], "the outstanding fees are unchanged",
                f"{eservice.tile(par, 'Outstanding fees')} / {ctx['outstanding']}")

    uat.conclude()


def _prepare_split(uat, s, par, child: str, nric: str, ctx: dict) -> None:
    """Balance > 0 and a charge above the balance. Tops up 20.00 (master value) when the EA is empty."""
    eservice.go_home(par)
    card = eservice.card_of(par, child)
    s.require(card, f"Home has the card of {child}")
    bal = card["balance"]
    if bal == 0:
        topup_precondition(uat, nric, LOW, "EA balance 20.00 of the master")
        uat.actor("parent")
        eservice.go_home(par)
        bal = eservice.card_of(par, child)["balance"]
    if not bal or bal <= 0:
        s.blocked(f"The EA of {child} is empty and the precondition top-up is not allowed.")
    charges = open_fees(par, child)
    ch = pick_gt(charges, bal)
    if ch is None:
        s.blocked(f"No payable charge of {child} is above the EA balance {bal}.")
    ctx.update(child=child, balance=bal, charge=ch)
    uat.map_data(f"Master EA 20.00 + online 30.00 on invoice 50.00 -> {child}: balance {bal}, charge '{ch['name']}' {ch['due']}")


def _prepare_any(uat, s, par, ctx: dict) -> None:
    """N4 and E2 use the second child first (topped up to 20.00), then the first child."""
    last = None
    for child, nric in ((CHILD2, CHILD2_NRIC), (CHILD, CHILD_NRIC)):
        try:
            _prepare_split(uat, s, par, child, nric, ctx)
            return
        except StepBlocked as e:
            last = e
    raise last


def test_UAT_PAR_01_A1(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Go to the child's fees and choose the invoice", "The invoice is selected")
    def _(s):
        auth.parent_login(par, PERSONA)
        _prepare_split(uat, s, par, CHILD, CHILD_NRIC, ctx)
        eservice.select_charge(par, ctx["charge"])
        s.check(eservice.selected_count(par) == 1, "one invoice is selected")

    @uat.step(2, "Choose Both and confirm", "EA part = whole balance, Online part = remainder; the EA is debited first, then the gateway opens", needs=(1,))
    def _(s):
        eservice.click_continue(par)
        eservice.choose_method(par, "Both")
        sp = eservice.split_amounts(par)
        s.check(sp["ea"] == ctx["balance"], "the EA part equals the whole balance", f"{sp['ea']} / {ctx['balance']}")
        s.check(sp["online"] == ctx["charge"]["due"] - ctx["balance"], "the Online part is the remainder",
                f"{sp['online']} / {ctx['charge']['due'] - ctx['balance']}")
        eservice.click_continue(par)
        eservice.authorize(par)
        par.wait_for_url(re.compile(re.escape(config.GATEWAY_HOST)), timeout=45000)
        s.check(eservice.on_gateway(par), "the Online gateway opens", par.url[:100])
        bal = balance_now(uat, CHILD)
        s.check(bal == 0, "the EA is debited before the gateway payment", bal)

    @uat.step(3, "Complete payment on the Online gateway", "The payment succeeds", needs=(2,))
    def _(s):
        eservice.gateway_pay(par, "Succeeded")
        ctx["result"] = eservice.wait_result(par)
        s.check(eservice.result_headline(ctx["result"]).lower() == "payment successful", "Payment successful",
                eservice.result_headline(ctx["result"]))

    @uat.step(4, "Open the receipt", "Invoice Paid; the receipt lists both sources, total = invoice; EA balance 0.00", needs=(3,))
    def _(s):
        r = ctx["result"]
        src = receipt_sources(r)
        s.check(src.get("Education Account") == ctx["balance"], "the receipt lists the EA part", src)
        s.check(src.get("Online Gateway") == ctx["charge"]["due"] - ctx["balance"], "the receipt lists the Online part", src)
        s.check(money(r[r.find("Amount due"):]) == ctx["charge"]["due"] if "Amount due" in r else False, "the total is the invoice amount", r[:300])
        s.check(eservice.invoice_number(r), "the receipt has an invoice number")
        if not re.search(r"\bPaid\b", r):
            s.gap("The receipt does not show the invoice status Paid.")
        s.check(balance_now(uat, CHILD) == 0, "the EA balance is 0.00")

    uat.conclude()


def _fail_online(uat, s, par, ctx: dict) -> str:
    eservice.select_charge(par, ctx["charge"])
    go_to_gateway(par)
    eservice.gateway_pay(par, "Failed")
    return eservice.wait_result(par)


def test_UAT_PAR_01_N4(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Choose Both and confirm", "The EA part is debited and the gateway opens")
    def _(s):
        auth.parent_login(par, PERSONA)
        _prepare_any(uat, s, par, ctx)

    @uat.step(2, "At the Online gateway choose failure", "The online payment fails", needs=(1,))
    def _(s):
        s.note("The gateway simulator has only Succeeded and Failed; Failed is used (master: failure or cancel).")
        ctx["result"] = _fail_online(uat, s, par, ctx)
        s.check(re.search(r"failed|needs review", eservice.result_headline(ctx["result"]), re.I),
                "the result is not successful", eservice.result_headline(ctx["result"]))

    @uat.step(3, "Return to e-Service and open the invoice",
              "The EA part is refunded; the invoice returns to Issued and can be retried; the EA balance is back", needs=(2,))
    def _(s):
        par.wait_for_timeout(5000)
        bal = balance_now(uat, ctx['child'])
        s.check(bal == ctx["balance"], "the EA part is refunded (balance back to the value before)",
                f"before {ctx['balance']}, now {bal}. Result page: {eservice.result_headline(ctx['result'])}")
        charges = open_fees(par, ctx['child'])
        again = [c for c in charges if c["name"] == ctx["charge"]["name"]]
        s.check(again and not again[0]["disabled"], "the invoice is payable again (retry possible)",
                f"charge '{ctx['charge']['name']}' in the list: {bool(again)}")
        s.note("Agreement of 31/10/2026 recorded in the other UAT flow (no automatic refund, manual reconciliation) "
               "differs from master 01. This case follows master 01.")

    uat.conclude()


def test_UAT_PAR_01_E2(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Choose Both and confirm", "The EA part is debited and the gateway opens")
    def _(s):
        auth.parent_login(par, PERSONA)
        _prepare_any(uat, s, par, ctx)

    @uat.step(2, "At the Online gateway choose failure (the tech team makes the EA refund command fail)",
              "The online payment fails and the refund command fails", needs=(1,))
    def _(s):
        ctx["result"] = _fail_online(uat, s, par, ctx)
        s.check(re.search(r"failed|needs review", eservice.result_headline(ctx["result"]), re.I),
                "the online payment fails", eservice.result_headline(ctx["result"]))
        s.blocked("The failed EA refund command must be simulated by the tech team; the UI cannot make it fail. "
                  "Step 3 records what the parent sees.")

    @uat.step(3, "Open the invoice after the refund command fails",
              "ReconciliationRequired, invoice PaymentPending, the parent sees a verifying status, operations alerted", needs=(1,))
    def _(s):
        r = ctx.get("result", "")
        s.check(re.search(r"needs review|verif|being processed|reconcil", r, re.I), "the parent sees a verifying status",
                eservice.result_headline(r))
        s.check(not eservice.invoice_number(r), "no invoice number is issued (payment pending)", eservice.invoice_number(r))
        charges = open_fees(par, ctx['child'])
        s.check(not any(c["name"] == ctx["charge"]["name"] and not c["disabled"] for c in charges),
                "the invoice is held (not payable while pending)")
        s.blocked("The operations alert goes to the operations tools, which are not part of the product screens.")

    uat.conclude()
