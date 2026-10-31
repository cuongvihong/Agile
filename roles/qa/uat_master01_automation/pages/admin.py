"""Admin Portal pages for MOE HQ and the school (DOM read on 31/10/2026: element ids of the scheme wizards)."""
from __future__ import annotations

import re
from core import config
from core.util import amount_after, norm


def main_text(page) -> str:
    try:
        return page.locator("main").first.inner_text(timeout=10000)
    except Exception:
        return page.locator("body").inner_text()


def settle(page, ms: int = 800) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(ms)


def goto(page, path: str, wait_text: str | None = None) -> None:
    page.goto(f"{config.ADMIN_URL}{path}")
    if wait_text:
        page.get_by_text(wait_text).first.wait_for(timeout=30000)
    settle(page)


def toast_text(page) -> str:
    try:
        return norm(" ".join(page.locator("[role=status], [role=alert], [data-sonner-toast], .toast").all_inner_texts()))
    except Exception:
        return ""


def table_rows(page) -> list[str]:
    return [norm(t) for t in page.locator("main tbody tr").all_inner_texts()]


def table_headers(page) -> list[str]:
    return [norm(t) for t in page.locator("main thead th").all_inner_texts()]


def click_tab(page, name_pattern: str) -> None:
    page.get_by_role("tab", name=re.compile(name_pattern, re.I)).first.click()
    settle(page, 1200)


def dialog(page):
    return page.locator("[role=dialog]").last


# ---- MOEFAS (HQ) -----------------------------------------------------------------

def moefas_list(page) -> None:
    goto(page, "/moe-hq/moe-fas", "MOEFAS schemes")


def moefas_rows(page) -> list[str]:
    return table_rows(page)


def moefas_new(page) -> None:
    goto(page, "/moe-hq/moe-fas/new", "Create new scheme")
    page.locator("#moefas-create-name").wait_for()


def moefas_general(page, name: str, form_opens: str, form_closes: str, effective_from: str,
                   budget: str, effective_to: str = "") -> None:
    page.locator("#moefas-create-name").fill(name)
    page.locator("#moefas-create-form-opens").fill(form_opens)
    page.locator("#moefas-create-form-closes").fill(form_closes)
    page.locator("#moefas-create-effective-from").fill(effective_from)
    if effective_to:
        page.locator("#moefas-create-effective-to").fill(effective_to)
    page.locator("#moefas-create-total-budget").fill(budget)
    page.locator("#moefas-create-total-budget").blur()


def wizard_next(page) -> None:
    page.get_by_role("button", name="Next", exact=True).click()
    page.wait_for_timeout(900)


def moefas_eligibility(page, nationality: str, ghi_to: str, pci_to: str) -> None:
    page.get_by_label(nationality, exact=True).check()
    page.locator("#moefas-create-ghi-to").fill(ghi_to)
    page.locator("#moefas-create-pci-to").fill(pci_to)


def moefas_pick_fee_component(page, preferred: str | None = None) -> str:
    """Open the Fee Components picker, tick one component, Apply. Returns the component name."""
    if page.locator("main input[type=checkbox]").count() == 0:
        page.get_by_role("button", name="Fee Components").click()
        page.wait_for_timeout(500)
    boxes = page.locator("main label:has(input[type=checkbox])")
    names = [norm(t) for t in boxes.all_inner_texts()]
    if not names:
        raise AssertionError("The Fee Components picker lists no active fee component")
    choice = preferred if preferred in names else names[0]
    page.locator("main label", has_text=re.compile(rf"^\s*{re.escape(choice)}\s*$")).first.locator("input").check()
    page.get_by_role("button", name="Apply", exact=True).click()
    page.wait_for_timeout(600)
    return choice


def moefas_rates(page, component: str, rates: dict) -> None:
    for level, value in rates.items():
        page.get_by_label(f"{component} – {level}", exact=True).fill(str(value))


def review_text(page) -> str:
    return main_text(page)


def click_button(page, name: str, exact: bool = True) -> None:
    page.get_by_role("button", name=name, exact=exact).first.click()
    settle(page, 1200)


def open_moefas_scheme(page, name: str) -> None:
    moefas_list(page)
    link = page.get_by_role("link", name=re.compile(rf"Inspect scheme {re.escape(name)}"))
    if link.count():
        link.first.click()
    else:
        page.get_by_role("button", name=f"Actions for {name}").click()
        page.get_by_role("menuitem", name="View").click()
    page.get_by_text("Back to schemes").first.wait_for()
    settle(page)


def row_actions(page, aria_label: str) -> list[str]:
    page.get_by_role("button", name=aria_label).click()
    page.wait_for_timeout(500)
    items = [norm(t) for t in page.get_by_role("menuitem").all_inner_texts()]
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    return items


def budget_numbers(text: str) -> dict:
    return {
        "total": amount_after("Total budget", text) or amount_after("Total Budget", text),
        "used": amount_after("Used budget", text) or amount_after("Used Budget", text),
        "remaining": amount_after("Remaining budget", text) or amount_after("Remaining Budget", text),
    }


def moefas_scheme_names_with_status(page) -> list[tuple[str, str]]:
    out = []
    for r in moefas_rows(page):
        m = re.match(r"(.+?)\s+(Singapore|International)", r)
        st = re.search(r"(Draft|Published|Application open|Application closed|Effective|Suspended|Closed)\s*$", r)
        if m:
            out.append((m.group(1).strip(), st.group(1) if st else ""))
    return out


# ---- HQ FAS applications -------------------------------------------------------------

def hq_fas_applications(page) -> None:
    goto(page, "/moe-hq/fas-applications", "FAS applications")
    page.locator("main tbody tr").first.wait_for(timeout=30000)


# ---- HQ top-up (precondition) ----------------------------------------------------------

def topup(page, nric: str, amount: str, note: str) -> dict:
    goto(page, "/top-up?tab=individual", "Individual Account Top-Up")
    page.locator("#student-search-input").fill(nric)
    page.get_by_role("button", name="Search", exact=True).click()
    page.get_by_text("Current Balance").first.wait_for(timeout=20000)
    before = amount_after("Current Balance", main_text(page))
    page.get_by_role("button", name=re.compile(r"^Next")).click()
    page.locator("#top-up-amount").fill(amount)
    page.locator("#top-up-reason").fill(note)
    page.get_by_role("button", name="Next", exact=True).click()
    page.get_by_role("button", name="Confirm & Credit Account").click()
    settle(page, 2500)
    return {"before": before, "text": norm(main_text(page))[:400]}


# ---- School management (HQ) --------------------------------------------------------------

def school_names(page) -> list[str]:
    goto(page, "/school-management", "School management")
    names = []
    for r in page.locator("main tbody tr").all():
        cells = r.locator("td").all_inner_texts()
        if len(cells) > 1:
            names.append(norm(cells[1]))
    return names


# ---- SBFAS (school) --------------------------------------------------------------------

def sbfas_list(page, search: str | None = None) -> None:
    goto(page, "/sbfas-schemes", "SBFAS schemes")
    per_page = page.locator("main select").filter(has_text="50").last
    try:
        per_page.select_option("50")
        settle(page, 1000)
    except Exception:
        pass
    if search:
        page.get_by_placeholder("Search by name or code").fill(search)
        page.get_by_role("button", name="Apply", exact=True).click()
        settle(page, 1200)


def sbfas_new(page) -> None:
    goto(page, "/sbfas-schemes/new", "Create SBFAS scheme")
    page.locator("#sbfas-name").wait_for()


def sbfas_general(page, name: str, open_from: str, open_to: str, eff_from: str, eff_to: str, budget: str) -> None:
    page.locator("#sbfas-name").fill(name)
    page.locator("#sbfas-open-from").fill(open_from)
    page.locator("#sbfas-open-to").fill(open_to)
    page.locator("#sbfas-effective-from").fill(eff_from)
    if eff_to:
        page.locator("#sbfas-effective-to").fill(eff_to)
    page.locator("#sbfas-budget").fill(budget)
    page.locator("#sbfas-budget").blur()


def sbfas_eligibility(page, ghi_to: str, pci_to: str, nationality_id: str = "SC") -> None:
    page.locator(f"#sbfas-nationality-{nationality_id}").check()
    for cid in ("#sbfas-ghi-enabled", "#sbfas-pci-enabled"):
        if not page.locator(cid).is_checked():
            page.locator(cid).check()
    page.locator("#sbfas-ghi-to").fill(ghi_to)
    page.locator("#sbfas-pci-to").fill(pci_to)


def sbfas_pick_component(page) -> str:
    page.get_by_role("button", name="Add fee components").click()
    dlg = dialog(page)
    dlg.locator("input[type=checkbox]").first.wait_for()
    label = norm(dlg.locator("label:has(input[type=checkbox])").first.inner_text()).split(" COMP_")[0]
    dlg.locator("input[type=checkbox]").first.check()
    dlg.get_by_role("button", name="Apply", exact=True).click()
    page.wait_for_timeout(600)
    return label


def sbfas_rates(page, rates: list[str]) -> list[str]:
    """Fill the percentage inputs in grade order. Grades beyond the master values get 0."""
    inputs = page.locator("main input[type=number]")
    labels = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        labels.append(el.get_attribute("aria-label") or "")
        el.fill(rates[i] if i < len(rates) else "0")
    return labels


def sbfas_actions(page, name: str) -> list[str]:
    return row_actions(page, f"Actions — {name}")


def sbfas_rows(page) -> list[str]:
    return table_rows(page)


def open_sbfas_scheme(page, name: str) -> None:
    sbfas_list(page, name)
    page.get_by_role("button", name=f"Actions — {name}").click()
    page.get_by_role("menuitem", name="View").click()
    page.get_by_text("Back to schemes").first.wait_for()
    settle(page)


def school_fas_applications(page) -> None:
    goto(page, "/fas-applications", "FAS Applications")


def pending_allocation_rows(page) -> list[str]:
    return [r for r in table_rows(page) if r]


# ---- Pending allocations (approve or reject) ------------------------------------------

def select_allocation(page, app_code: str) -> bool:
    row = page.locator("main tbody tr", has_text=app_code).first
    if row.count() == 0:
        return False
    row.locator("input[type=checkbox]").check()
    page.wait_for_timeout(300)
    return True


def approve_selected(page) -> str:
    page.get_by_role("button", name="Preview and confirm").click()
    dlg = dialog(page)
    dlg.wait_for(timeout=15000)
    preview = norm(dlg.inner_text())
    dlg.get_by_role("button", name=re.compile(r"confirm|approve", re.I)).last.click()
    settle(page, 2000)
    return preview + " || " + toast_text(page)


def open_reject_dialog(page):
    page.get_by_role("button", name="Reject selected").click()
    dlg = dialog(page)
    dlg.wait_for(timeout=15000)
    return dlg


# ---- Record a paper application (school) ------------------------------------------------

def paper_find_parent(page, nric: str) -> str:
    goto(page, "/fas-applications/physical/new")
    dlg = dialog(page)
    dlg.get_by_label(re.compile(r"Parent NRIC")).fill(nric)
    dlg.get_by_role("button", name="Find parent").click()
    settle(page, 2500)
    if page.locator("[role=dialog]").count() and page.locator("[role=dialog]").last.is_visible():
        return norm(dialog(page).inner_text())
    return ""
