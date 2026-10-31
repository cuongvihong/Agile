"""Parent e-Service pages, as seen in the evidence and the DOM of 31/10/2026."""
from __future__ import annotations

import re
from decimal import Decimal

from core import config
from core.util import amount_after, money, norm

CARD_JS = """() => [...document.querySelectorAll('a[aria-label^="View education account details for "]')].map(a => {
  const name = a.getAttribute('aria-label').replace('View education account details for ', '').trim();
  let el = a;
  for (let i = 0; i < 8 && el.parentElement; i++) {
    el = el.parentElement;
    if (el.innerText && el.innerText.includes('Available balance') && el.innerText.includes(name)) break;
  }
  return {name, href: a.getAttribute('href'), text: el.innerText};
})"""


def wait_ready(page, text: str | None = None, timeout: int = 30000) -> None:
    page.wait_for_load_state("domcontentloaded")
    if text:
        page.get_by_text(text, exact=False).first.wait_for(timeout=timeout)
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass


def main_text(page) -> str:
    try:
        return page.locator("main").first.inner_text(timeout=10000)
    except Exception:
        return page.locator("body").inner_text()


# ---- Home ---------------------------------------------------------------------

def go_home(page) -> None:
    page.goto(f"{config.PARENT_URL}/")
    wait_ready(page, "Education wallets")
    page.wait_for_function("() => !document.body.innerText.includes('Loading education accounts')", timeout=30000)


def home_cards(page) -> list[dict]:
    cards = []
    for c in page.evaluate(CARD_JS):
        text = c["text"]
        code = re.search(r"\bEDU-\d+\b", text)
        status = re.search(r"\b(Active|Inactive|Closed|Due for closure|Suspended|Pending closure)\b", text)
        cards.append({
            "name": c["name"], "href": c["href"], "code": code.group(0) if code else "",
            "balance": amount_after("Available balance", text), "status": status.group(0) if status else "",
            "text": norm(text),
        })
    return cards


def card_of(page, child: str) -> dict | None:
    return next((c for c in home_cards(page) if c["name"] == child), None)


def open_account(page, child: str) -> None:
    page.get_by_role("link", name=f"View education account details for {child}").click()
    wait_ready(page, "Education Account details")
    page.get_by_text("EA BALANCE").first.wait_for()


def account_info(page) -> dict:
    t = main_text(page)
    dob = re.search(r"DATE OF BIRTH\s*\n\s*([A-Z][a-z]{2} \d{1,2}, \d{4})", t)
    cit = re.search(r"CITIZENSHIP\s*\n\s*(\S[^\n]*)", t)
    return {"balance": amount_after("EA BALANCE", t), "dob": dob.group(1) if dob else "",
            "citizenship": cit.group(1).strip() if cit else "", "text": norm(t), "url": page.url}


def balance_of(page, child: str) -> Decimal | None:
    go_home(page)
    c = card_of(page, child)
    return c["balance"] if c else None


# ---- Pay education charges ------------------------------------------------------

def open_pay(page, child: str) -> None:
    page.get_by_role("link", name=f"View billing for {child}").click()
    wait_ready(page, "Outstanding charges")
    page.wait_for_function("() => !document.body.innerText.includes('Loading outstanding charges')", timeout=30000)


ROWS_JS = """() => [...document.querySelectorAll('main tbody tr')].map(tr => {
  const cb = tr.querySelector('input[type=checkbox]');
  return {label: cb ? cb.getAttribute('aria-label') : null, disabled: cb ? cb.disabled : null,
          cells: [...tr.querySelectorAll('td')].map(td => td.innerText.trim())};
}).filter(r => r.label && r.label.startsWith('Select charge: '))"""


def charges_on_page(page) -> list[dict]:
    out = []
    for r in page.evaluate(ROWS_JS):
        cells = r["cells"]
        name = r["label"].replace("Select charge: ", "")
        out.append({
            "name": name,
            "gross": money(cells[2]) if len(cells) > 2 else None,
            "subsidy": money(cells[3]) if len(cells) > 3 else None,
            "due": money(cells[5]) if len(cells) > 5 else None,
            "status": cells[7] if len(cells) > 7 else "",
            "disabled": r["disabled"],
        })
    return out


def all_charges(page, max_pages: int = 6) -> list[dict]:
    """Charges of every page of the list; leaves the list on page 1."""
    seen = []
    for i in range(max_pages):
        rows = charges_on_page(page)
        for r in rows:
            r["page"] = i + 1
        seen.extend(rows)
        nxt = page.get_by_role("button", name="Next")
        if nxt.count() == 0 or nxt.first.is_disabled():
            break
        nxt.first.click()
        page.wait_for_timeout(800)
    first = page.get_by_role("button", name="Go to page 1")
    if first.count() and not first.first.is_disabled():
        first.first.click()
        page.wait_for_timeout(800)
    return seen


def goto_charge_page(page, number: int) -> None:
    if number <= 1:
        return
    page.get_by_role("button", name=f"Go to page {number}").click()
    page.wait_for_timeout(800)


def select_charge(page, charge: dict) -> None:
    goto_charge_page(page, charge.get("page", 1))
    page.get_by_label(f"Select charge: {charge['name']}", exact=True).check()


def tile(page, label: str) -> Decimal | None:
    return amount_after(label, main_text(page))


def selected_count(page) -> int:
    m = re.search(r"(\d+) charge\(s\) selected", main_text(page))
    return int(m.group(1)) if m else -1


def click_continue(page) -> None:
    page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_timeout(800)


METHOD_JS = """() => Object.fromEntries([...document.querySelectorAll('input[name="billing-payment-method"]')].map(r => [r.value, {disabled: r.disabled, checked: r.checked}]))"""


def payment_methods(page) -> dict:
    page.locator('input[name="billing-payment-method"]').first.wait_for()
    return page.evaluate(METHOD_JS)


def choose_method(page, value: str) -> None:
    page.locator(f'input[name="billing-payment-method"][value="{value}"]').check()
    page.wait_for_timeout(400)


def split_amounts(page) -> dict:
    t = main_text(page)
    return {"ea": amount_after("Education Account amount", t.split("Choose the amount")[-1]) or amount_after("Education Account amount", t),
            "online": amount_after("Online amount", t)}


def authorize(page) -> None:
    page.get_by_role("button", name="Authorize & pay").click()


def on_gateway(page) -> bool:
    return config.GATEWAY_HOST in page.url


def gateway_pay(page, outcome: str = "Succeeded") -> None:
    """The simulator has one button 'Pay' and a hidden field outcome (Succeeded | Failed)."""
    page.wait_for_url(re.compile(re.escape(config.GATEWAY_HOST)), timeout=45000)
    page.get_by_role("button", name="Pay", exact=True).wait_for(timeout=30000)
    if outcome != "Succeeded":
        page.evaluate("v => { const i = document.querySelector('input[name=outcome]'); if (!i) throw new Error('no outcome field'); i.value = v; }", outcome)
    page.get_by_role("button", name="Pay", exact=True).click()


def wait_result(page, timeout: int = 60000) -> str:
    page.wait_for_url(re.compile(re.escape(config.PARENT_URL)), timeout=timeout)
    page.get_by_text("Payment result").first.wait_for(timeout=timeout)
    page.wait_for_function(
        "() => /Payment (successful|failed|needs review|cancelled|is being processed)/i.test(document.body.innerText)",
        timeout=timeout)
    return main_text(page)


def result_headline(text: str) -> str:
    m = re.search(r"Payment (successful|failed|needs review|cancelled|is being processed)", text, re.I)
    return m.group(0) if m else ""


def invoice_number(text: str) -> str:
    m = re.search(r"\bINV\d{4,}\b", text)
    return m.group(0) if m else ""


# ---- Invoices & payments, Top-up history -----------------------------------------

def open_invoices(page, child: str) -> None:
    page.get_by_role("link", name=f"View invoices and payments for {child}").click()
    wait_ready(page, "Invoices")


def invoice_rows(page) -> list[str]:
    return [norm(t) for t in page.locator("main tbody tr").all_inner_texts() if re.search(r"INV\d+", t)]


def open_topup_history(page, child: str) -> None:
    page.get_by_role("link", name=f"View Top-Up for {child}").click()
    wait_ready(page, "Top-Up")


# ---- FAS -----------------------------------------------------------------------

def open_my_fas(page) -> None:
    page.get_by_role("button", name="Open user options").click()
    page.get_by_role("link", name="FAS Application").click()
    wait_ready(page, "My FAS Applications")


def my_fas_cards(page) -> list[dict]:
    t = main_text(page)
    cards = []
    for m in re.finditer(r"(APP-[A-Z0-9-]+)\s*\n\s*([A-Z_ ]{4,40}|[A-Z][a-z][^\n]{2,40})\s*\n\s*Beneficiaries:\s*([^\n]*)", t):
        cards.append({"code": m.group(1), "status": m.group(2).strip(), "beneficiaries": [b.strip() for b in m.group(3).split(",")]})
    return cards


def open_new_application(page) -> None:
    page.get_by_role("button", name="New Application").click()
    page.wait_for_url(re.compile(r"/fas-application/new"))
    page.get_by_label("Full name *").first.wait_for()
    page.wait_for_function("() => { const i = document.querySelector('main input[type=text][readonly], main input[readonly]'); return i && i.value; }", timeout=30000)
    page.wait_for_timeout(1500)


def beneficiary_names(page) -> list[str]:
    heads = page.locator("main h1, main h2, main h3, main h4").all_inner_texts()
    return [h.split(":", 1)[1].strip() for h in heads if h.startswith("Beneficiary details:")]


def beneficiary_section(page, name: str):
    head = page.locator("main h1, main h2, main h3, main h4", has_text=f"Beneficiary details: {name}").first
    return head.locator("xpath=ancestor::*[.//button[normalize-space()='Remove beneficiary']][1]")


def remove_beneficiary(page, name: str) -> None:
    beneficiary_section(page, name).get_by_role("button", name="Remove beneficiary").click()
    page.wait_for_timeout(400)


def fill_empty_required_selects(page) -> list[str]:
    """Pick the first real option of every empty, enabled required select (Gender, Race ...)."""
    filled = []
    selects = page.locator("main select")
    for i in range(selects.count()):
        s = selects.nth(i)
        try:
            if s.is_disabled() or s.input_value():
                continue
            sid = s.get_attribute("id") or ""
            label = page.locator(f'label[for="{sid}"]').first.inner_text() if sid else ""
            s.select_option(index=1)
            filled.append(label or f"select {i}")
        except Exception:
            continue
    return filled


def readonly_state(page, label: str) -> dict:
    loc = page.get_by_label(label).first
    return {"value": loc.input_value(), "readonly": loc.evaluate("e => e.readOnly || e.disabled")}


def submit_application(page) -> str:
    page.get_by_role("button", name="Submit application").click()
    page.wait_for_timeout(3000)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    return main_text(page)


def validation_messages(page) -> list[str]:
    js = """() => [...document.querySelectorAll('[role=alert], [aria-invalid=true] ~ *, .error, [class*=error], [class*=Error]')]
        .map(e => e.innerText && e.innerText.trim()).filter(Boolean)"""
    try:
        return list(dict.fromkeys(page.evaluate(js)))[:12]
    except Exception:
        return []
