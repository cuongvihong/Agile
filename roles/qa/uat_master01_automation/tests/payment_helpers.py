"""Shared steps of the payment cases (UAT-PAR-01 family)."""
from __future__ import annotations

from decimal import Decimal

from core import config
from core.util import money
from pages import admin, auth, eservice

MSG_0801 = "We could not find any student linked to your account. Please contact your child's school."
MSG_0802 = "Login was not completed. Try again."
MSG_0809 = "We could not retrieve your information. Please try again later."


def topup_precondition(uat, nric: str, amount: Decimal, why: str) -> dict:
    """Credit an EA through HQ Individual Top-Up (team decision 30/10/2026: we create our own top-up data)."""
    if not config.ALLOW_TOPUP:
        raise RuntimeError("top-up forbidden by UAT_NO_TOPUP=1")
    hq = uat.actor("moe")
    if "/login" in hq.url or hq.url == "about:blank":
        auth.admin_login(hq, "hq")
    res = admin.topup(hq, nric, f"{amount:.2f}", f"UAT master 01 precondition {uat.case_id}: {why}")
    uat.map_data(f"Precondition top-up of SGD {amount:.2f} to {nric} through HQ Individual Top-Up ({why})")
    return res


def open_fees(page, child: str) -> list[dict]:
    eservice.go_home(page)
    eservice.open_account(page, child)
    eservice.open_pay(page, child)
    return eservice.all_charges(page)


def payable(charges: list[dict]) -> list[dict]:
    return [c for c in charges if c["due"] is not None and c["due"] > 0 and not c["disabled"]]


def pick_le(charges: list[dict], limit: Decimal, target: Decimal) -> dict | None:
    """Payable charge with amount due <= limit, the closest to the master amount."""
    ok = [c for c in payable(charges) if c["due"] <= limit]
    return min(ok, key=lambda c: (abs(c["due"] - target), c["due"])) if ok else None


def pick_gt(charges: list[dict], limit: Decimal) -> dict | None:
    """Smallest payable charge with amount due > limit."""
    ok = [c for c in payable(charges) if c["due"] > limit]
    return min(ok, key=lambda c: c["due"]) if ok else None


def go_to_gateway(page) -> None:
    eservice.click_continue(page)          # charges -> payment method
    eservice.choose_method(page, "Both")
    eservice.click_continue(page)          # payment method -> review
    eservice.authorize(page)


def balance_now(uat, child: str) -> Decimal | None:
    """Balance read in a separate window of the parent session (does not disturb the main page)."""
    page = uat.actors["parent"]["page"]
    extra = page.context.new_page()
    try:
        extra.goto(config.PARENT_URL + "/")
        extra.get_by_text("Education wallets").first.wait_for()
        extra.wait_for_function("() => !document.body.innerText.includes('Loading education accounts')", timeout=30000)
        c = eservice.card_of(extra, child)
        return c["balance"] if c else None
    finally:
        extra.close()


def receipt_sources(text: str) -> dict:
    """Amount per funding source on the receipt (Source / Amount table)."""
    out = {}
    t = text.replace(" ", " ")
    i = t.find("Source")
    part = t[i:] if i >= 0 else t
    for src in ("Education Account", "Online Gateway"):
        j = part.find(src)
        if j >= 0:
            out[src] = money(part[j + len(src): j + len(src) + 40])
    return out
