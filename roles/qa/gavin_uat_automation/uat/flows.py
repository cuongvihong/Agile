"""Reusable pieces of the parent payment flows and test data for the UAT cases."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from decimal import Decimal

import pytest
from playwright.sync_api import Page, expect

from pages import db
from uat import env

# Master data (student.test01 ... EA-001) mapped to the R9 seed that really exists on the stack.
# Parent persona S7890123F owns all R9 children. Persona S9123456J owns two children.
SANDBOX = {"id": "R9-STU-14", "name": "R9 Sandbox Teo", "ea": "EDU-01044"}     # student.test01: free of charges, wallet 1000, temp charges are added
TEEN = {"id": "R9-STU-10", "name": "R9 Teen Yeo", "ea": "EDU-01040"}           # student.test16: 16 years or older
PAID = {"id": "R9-STU-07", "name": "R9 Paid Koh", "ea": "EDU-01037"}           # two Paid invoices with receipts
PENDING_TITLE = "Payment is being processed"
PENDING_REASON = ("The service that confirms the online part of a payment is not yet in this environment. The EA part was debited and the "
                  "transaction stays 'Payment is being processed' (Online Gateway shows a dash), so the final result cannot be checked here. "
                  "Re-run when the service is deployed. Note: the EA of the child stays debited until then.")
SECOND_PARENT = "S9123456J"                                                    # parent with exactly two children
SECOND_PARENT_KIDS = ("Ella Smith", "Isabella Smith")


class RequestLog:
    """Records the requests of a page, to prove that a payment was sent exactly once, or not at all."""

    def __init__(self, page: Page):
        self.items: list[tuple[str, str]] = []
        page.on("request", lambda r: self.items.append((r.method, r.url)))

    def posts(self, fragment: str) -> list[str]:
        return [u for m, u in self.items if m == "POST" and fragment in u]


def db_available() -> tuple[bool, str]:
    if not env.ALLOW_DB:
        return False, "UAT_NO_DB=1"
    try:
        code, out = db.sql_raw("SELECT 1 AS ok", db=db.BILLING_DB)
        return (code == 0 and "1" in out), out[:160]
    except Exception as exc:  # noqa: BLE001  docker is not installed
        return False, f"{type(exc).__name__}: {exc}"


def simulator_available() -> tuple[bool, str]:
    try:
        urllib.request.urlopen(env.CHECKOUT_URL + "/", timeout=4)
        return True, ""
    except urllib.error.HTTPError:
        return True, ""  # the server answered, only the path is unknown
    except Exception as exc:  # noqa: BLE001
        return False, f"{env.CHECKOUT_URL}: {exc}"


@contextmanager
def prepared_charges(uat, amounts, balance, student: dict = SANDBOX):
    """Put the child in the state of the master (wallet balance and open charges). Cleans up in the end.
    When the database cannot be reached the case is recorded as BLOCKED, never as passed."""
    ok, why = db_available()
    if not ok:
        # UI only mode: no data is prepared. The case reads the real state from the screens (see find_scenario) and runs on it.
        print(f"[uat] database not used ({why}). UI only mode: the case runs on the data that the environment already has.")
        yield None
        return
    cm = db.temp_charges(student["id"], list(amounts), balance=balance)
    try:
        ids = cm.__enter__()
    except Exception as exc:  # noqa: BLE001
        uat.blocked("Prepare the test data in the database", f"Could not create the charge: {exc}")
        uat.conclude()
        raise
    try:
        yield ids
    finally:
        try:
            cm.__exit__(None, None, None)
        except Exception as exc:  # noqa: BLE001
            print(f"[uat] cleanup of the temporary charge failed: {exc}")


def home_card(page: Page, name: str) -> str:
    """Text of the Home card of one child: name, EA code, status, balance."""
    text = page.locator("main").inner_text()
    m = re.search(rf"{re.escape(name)}\s+(EDU-\d+)\s+(.*?)View account", text, re.S)
    return re.sub(r"\s+", " ", f"{name} {m.group(1)} {m.group(2)}") if m else ""


def wait_home_card(page: Page, name: str, balance_text: str | None = None, timeout: int = 40_000) -> str:
    link = page.get_by_role("link", name=f"View education account details for {name}")
    expect(link).to_be_attached(timeout=timeout)
    try:
        link.scroll_into_view_if_needed(timeout=5_000)  # the balance sits at the bottom of the card, below the first screen of the video
    except Exception:  # noqa: BLE001
        pass
    if balance_text:
        # Wait for the balance to show on the card. A wrong or late balance must not end in a bare timeout: the caller compares the card text, so the
        # evidence shows what Home really says (the number is looked for without its currency prefix).
        number = balance_text.replace("SGD", "").replace("S$", "").replace("$", "").strip()
        try:
            page.wait_for_function(
                "([n, b]) => { const t = document.querySelector('main').innerText; const i = t.indexOf(n); return i >= 0 && t.slice(i, i + 900).includes(b); }",
                arg=[name, number], timeout=timeout)
        except Exception:  # noqa: BLE001
            pass
    return home_card(page, name)


@dataclass
class Scenario:
    """The child and the fee a payment case runs on. In database mode it is the sandbox child with the prepared charge.
    In UI only mode it is a real child of the persona that has a suitable fee, found by reading the screens."""
    student: dict
    amt: Decimal
    bal: Decimal
    desc: str | None = None
    pay_url: str | None = None

    @property
    def ui_only(self) -> bool:
        return self.desc is not None

    def open_fees(self, billing) -> None:
        if self.pay_url:
            billing.page.goto(self.pay_url)
            billing.wait_ready()
        else:
            billing.open(self.student["id"])
        if self.desc:
            billing.reveal(self.desc)

    def charge(self, billing):
        if self.desc:
            billing.reveal(self.desc)
        found = [c for c in billing.read_charges() if (c.description == self.desc if self.desc else "QA" in c.description) and c.net == self.amt]
        assert found, f"The fee {self.amt} is not on the page. Fees shown: {[(c.description, str(c.net)) for c in billing.read_charges()]}"
        return found[0]


def seed_on() -> bool:
    import os
    return os.environ.get("UAT_SEED", "1").lower() != "0"


def seed_parent(case: str, db_mode: bool = False) -> str | None:
    """The Singpass persona that owns the seeded child of this case (None: database mode or seed switched off, the default persona signs in)."""
    from data import seed_plan as plan
    use = plan.PAY_CASES.get(case)
    return plan.STUDENTS[use["student"]]["parent"] if use and not db_mode and seed_on() else None


def seed_scenario(uat, page: Page, billing, case: str) -> Scenario | None:
    """The child and the charge that the precondition UAT-PRE-02 created for this case, read from the pay screen of the child."""
    from data import seed_plan as plan
    use = plan.PAY_CASES.get(case)
    if not use or not seed_on():
        return None
    s = plan.STUDENTS[use["student"]]
    url = f"{env.PARENT_URL}/accounts/{s['code']}/pay"
    page.goto(url)
    billing.wait_ready()
    charges = billing.read_all_charges()
    hit = [c for c in charges if use["component"].lower() in c.description.lower()]
    if not hit:
        uat.blocked("Find the seeded fee of this case", f"{s['name']} has no outstanding fee '{use['component']}' on the pay screen (fees shown: "
                    f"{[(c.description, str(c.net)) for c in charges]}). Run run_uat.cmd seed, or set UAT_SEED_ROUND=2 when an earlier run used the charge up.",
                    "The child has the fee of the precondition")
        uat.conclude()
    uat.note(f"Seeded data. Child {s['name']} ({s['ea']}), fee '{hit[0].description}' {hit[0].net}, EA balance {billing.balance()}. "
             "The master uses EA 100 / invoice 50 and EA 20 / invoice 50; the amounts differ, the steps are the same.")
    billing.reveal(hit[0].description)
    return Scenario({"id": None, "name": s["name"], "ea": s["ea"]}, hit[0].net, billing.balance(), hit[0].description, url)


def find_scenario(uat, page: Page, billing, kind: str, amt: Decimal, bal: Decimal, db_mode: bool, seed: str | None = None) -> Scenario:
    """kind 'ea': a fee that the wallet covers. kind 'short': a fee larger than the balance (balance above 0 when the case splits the payment).
    Records the case as BLOCKED, with the list of what was found, when no child fits."""
    if db_mode:
        return Scenario(SANDBOX, amt, bal)
    if seed:
        found = seed_scenario(uat, page, billing, seed)
        if found:
            return found
    page.goto(env.PARENT_URL + "/")
    links = page.get_by_role("link", name=re.compile(r"^View education account details for "))
    expect(links.first).to_be_attached(timeout=40_000)
    names = [re.sub(r"^View education account details for\s+", "", (l.get_attribute("aria-label") or l.inner_text())).strip() for l in links.all()]
    seen, pick = [], None
    for name in dict.fromkeys(names):
        try:
            page.goto(env.PARENT_URL + "/")
            open_account_from_home(page, name)
            page.get_by_role("link", name=f"View billing for {name}").click()
            billing.wait_ready()
            balance = billing.balance()
            charges = billing.read_charges()
        except Exception as exc:  # noqa: BLE001
            seen.append(f"{name}: not readable ({type(exc).__name__})")
            continue
        seen.append(f"{name}: balance {balance}, fees {[str(c.net) for c in charges]}")
        if kind == "ea":
            ok = sorted((c for c in charges if 0 < c.net <= balance), key=lambda c: c.net)
        else:
            ok = sorted((c for c in charges if c.net > balance and (balance > 0 or kind == "short0")), key=lambda c: c.net)
        if ok and pick is None:
            ea = re.search(r"EDU-\d+", page.locator("main").inner_text())
            pick = Scenario({"id": None, "name": name, "ea": ea.group(0) if ea else "EDU-"}, ok[0].net, balance, ok[0].description, page.url)
    if pick is None:
        need = "a fee that the balance covers" if kind == "ea" else ("a fee larger than the balance" + ("" if kind == "short0" else " and a balance above 0"))
        uat.blocked("Find a child for this case on the environment", f"No child of the persona has {need}. Found: " + "; ".join(seen) +
                    ". Add such a fee or top up through the portals, then run again.", "A child with the right fee and balance")
        uat.conclude()
    uat.note(f"UI only mode. Child {pick.student['name']}, fee '{pick.desc}' {pick.amt}, balance {pick.bal}.")
    return pick


def resolve_child(page: Page, preferred: dict) -> dict:
    """The seed child of the master when Home has it, otherwise the first child on Home (the hosted environment has its own seed:
    persona S7890123F owns Lucas Lim and Nathan Lim there, not the R9 children). Returns {name, ea, seed}."""
    links = page.get_by_role("link", name=re.compile(r"^View education account details for "))
    expect(links.first).to_be_attached(timeout=40_000)
    if page.get_by_role("link", name=f"View education account details for {preferred['name']}").count():
        return {**preferred, "seed": True}
    label = links.first.get_attribute("aria-label") or links.first.inner_text()
    name = re.sub(r"^View education account details for\s+", "", label).strip()
    m = re.search(rf"{re.escape(name)}\s+(EDU-\d+)", page.locator("main").inner_text())
    return {"id": None, "name": name, "ea": m.group(1) if m else "EDU-", "seed": False}


def open_account_from_home(page: Page, name: str) -> None:
    link = page.get_by_role("link", name=f"View education account details for {name}")
    link.scroll_into_view_if_needed()
    link.click()
    expect(page.get_by_role("heading", name="Education Account details")).to_be_visible(timeout=20_000)
    expect(page.get_by_role("heading", name=name)).to_be_visible()


def go_online(page: Page, billing, simulator, result, outcome: str) -> None:
    """After Authorize on a payment that has an online part: simulator opens, press Pay successful or Pay failed, return to the result."""
    billing.authorize()
    simulator.wait_loaded()
    (simulator.pay_successful if outcome == "ok" else simulator.pay_failed)()
    simulator.wait_return_to_merchant()
    try:
        result.wait_final()
    except AssertionError:
        # The hosted stack has no service that confirms the online part yet: the EA part is debited and the transaction stays Pending.
        # That is a missing service of the environment, not a defect of the page, so the step is BLOCKED and not FAIL.
        if page.get_by_role("heading", name=PENDING_TITLE).count():
            pytest.skip(PENDING_REASON)
        raise


def dec(text: str) -> Decimal:
    m = re.search(r"-?[\d,]+\.\d+", text or "")
    return Decimal(m.group(0).replace(",", "")) if m else Decimal("NaN")
