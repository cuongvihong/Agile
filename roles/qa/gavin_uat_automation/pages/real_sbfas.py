"""Page objects for the REAL SBFAS screens of the admin portal (School user), localhost:5173.

Screens (apps/admin-portal/src/features/sbfas-schemes):
  list    /sbfas-schemes       four summary cards (Draft, Upcoming, Active, Closed schemes), table, row menu (View, Add fee, Publish, Suspend, Reactivate, Delete)
  wizard  /sbfas-schemes/new   steps General, Eligibility, Subsidy, Review. Buttons Cancel, Back, Next or Review, then Back to edit, Save draft, Publish
  dialogs View (details) and Add fee component (one fee, one percentage per active grade)

Ids set by the front end: sbfas-name, sbfas-open-from, sbfas-open-to, sbfas-effective-from, sbfas-effective-to, sbfas-budget,
sbfas-eligibility-description, sbfas-nationality-<code>. The browser runs with locale en-US.
"""
from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from . import real_api
from .admin_base import BasePage, norm
from .real_login import SCHOOL_PASS, SCHOOL_USER, goto_signed_in
from .real_schemes import tick

LIST_PATH = "sbfas-schemes"


class SbfasList(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"
        self.heading = page.get_by_role("heading", level=1, name="SBFAS schemes", exact=True)
        self.table = page.get_by_role("table", name="SBFAS schemes")

    def open(self) -> "SbfasList":
        goto_signed_in(self.page, self.base, LIST_PATH, SCHOOL_USER, SCHOOL_PASS)
        expect(self.heading).to_be_visible()
        expect(self.table).to_be_visible()
        try:
            self.page.wait_for_function("() => !document.querySelector('table [class*=skeleton]')", timeout=15_000)
        except Exception:
            pass
        return self

    def search(self, text: str) -> None:
        self.page.get_by_placeholder("Search by name or code").fill(text)
        self.page.get_by_role("button", name="Apply").click()
        self.page.wait_for_load_state("networkidle")

    def headers(self) -> list[str]:
        return [norm(t) for t in self.table.locator("thead th").all_inner_texts()]

    def rows(self) -> list[dict[str, str]]:
        heads = self.headers()
        out = []
        for tr in self.table.locator("tbody tr").all():
            cells = [norm(c) for c in tr.locator("td").all_inner_texts()]
            if len(cells) == len(heads):
                out.append(dict(zip(heads, cells)))
        return out

    def _next_button(self):
        """The enabled Next button of the table pagination, or None on the last page. The control stays disabled while the page is loading, so wait a moment before giving up."""
        nxt = self.page.get_by_role("button", name=re.compile(r"next", re.I))
        if nxt.count() == 0:
            return None
        try:
            expect(nxt.first).to_be_enabled(timeout=3_000)
        except AssertionError:
            return None
        return nxt.first

    def row(self, name: str):
        """The row of a scheme. The list shows 10 rows a page and the stack keeps schemes of earlier runs, so this goes to the page that holds the name."""
        target = self.table.locator("tbody tr").filter(has=self.page.get_by_text(name, exact=True))
        for _ in range(30):
            if target.count() > 0:
                break
            nxt = self._next_button()
            if nxt is None:
                break
            nxt.click()
            self.page.wait_for_timeout(600)
        return target

    def cards(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for art in self.page.get_by_label("Scheme summary").locator("article").all():
            parts = [p.strip() for p in art.inner_text().splitlines() if p.strip()]
            out[parts[0]] = int(parts[-1])
        return out

    def menu_button(self, name: str):
        return self.page.get_by_role("button", name=re.compile(rf"^Actions.*{re.escape(name)}"))

    def actions(self, name: str) -> list[str]:
        self.menu_button(name).click()
        items = [norm(t) for t in self.page.get_by_role("menuitem").all_inner_texts()]
        self.page.keyboard.press("Escape")
        return items

    def do_action(self, name: str, label: str) -> None:
        self.menu_button(name).click()
        self.page.get_by_role("menuitem", name=label, exact=True).click()


class SbfasWizard(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"
        self.title = page.get_by_role("heading", level=1, name="Create SBFAS scheme")
        self.stepper = page.get_by_role("navigation", name="Create SBFAS scheme")
        self.name = page.locator("#sbfas-name")
        self.open_from = page.locator("#sbfas-open-from")
        self.open_to = page.locator("#sbfas-open-to")
        self.eff_from = page.locator("#sbfas-effective-from")
        self.eff_to = page.locator("#sbfas-effective-to")
        self.budget = page.locator("#sbfas-budget")
        self.context = page.locator("#sbfas-eligibility-description")
        self.picker_button = page.get_by_role("button", name="Add fee components")

    def open(self) -> "SbfasWizard":
        goto_signed_in(self.page, self.base, f"{LIST_PATH}/new", SCHOOL_USER, SCHOOL_PASS)
        expect(self.title).to_be_visible()
        return self

    # ---- steps
    def step_labels(self) -> list[str]:
        return [norm(t) for t in self.stepper.locator("li span[class*='stepLabel']").all_text_contents()]

    def current_step(self) -> str:
        return norm(self.stepper.locator("[aria-current='step']").first.text_content())

    def fill_income_bands(self, ghi_to: str = "20000", pci_to: str = "5000") -> None:
        """Build 30/10/2026: GHI and PCI are both enabled by default and an empty To is refused ("Enter the upper value of the income band."). Fill To of every enabled band."""
        for key, to in (("ghi", ghi_to), ("pci", pci_to)):
            enabled = self.page.locator(f"#sbfas-{key}-enabled")
            if enabled.count() and enabled.is_checked():
                if not self.page.locator(f"#sbfas-{key}-from").input_value():
                    self.page.locator(f"#sbfas-{key}-from").fill("0")
                if not self.page.locator(f"#sbfas-{key}-to").input_value():
                    self.page.locator(f"#sbfas-{key}-to").fill(to)

    def go_next(self) -> None:
        self.page.get_by_role("button", name=re.compile("^(Next|Review)$")).click()

    def fill_general(self, name: str, win: dict, budget: str = "1000") -> None:
        self.name.fill(name)
        self.open_from.fill(win["opens"])
        self.open_to.fill(win["closes"])
        self.eff_from.fill(win["eff_from"])
        self.eff_to.fill(win["eff_to"])
        self.budget.fill(budget)

    def to_eligibility(self, name: str | None = None, win: dict | None = None) -> dict:
        win = win or real_api.sbfas_window(0)
        self.fill_general(name or real_api.unique_name("sbf"), win)
        self.go_next()
        expect(self.page.get_by_text("Eligible nationalities")).to_be_visible()
        return win

    def to_subsidy(self, name: str | None = None, win: dict | None = None) -> dict:
        win = self.to_eligibility(name, win)
        tick(self.page.locator("#sbfas-nationality-SC"))
        self.fill_income_bands()
        self.go_next()
        expect(self.page.get_by_role("heading", name="Active fee components")).to_be_visible()
        expect(self.page.get_by_role("table")).to_be_visible()
        return win

    # ---- subsidy step
    def levels(self) -> list[str]:
        return [norm(t) for t in self.page.locator("table tbody th[scope='row']").all_text_contents()]

    def pick(self, fee_name: str) -> None:
        self.picker_button.click()
        dialog = self.page.get_by_role("dialog", name="Add fee components")
        expect(dialog).to_be_visible()
        tick(dialog.locator("label").filter(has_text=fee_name).first.locator("input[type='checkbox']"))
        dialog.get_by_role("button", name="Apply").click()
        expect(dialog).to_have_count(0)

    def fee_headers(self) -> list[str]:
        return [norm(t) for t in self.page.locator("table thead th[aria-label]").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")]

    def cell(self, fee_name: str, level_name: str):
        return self.page.get_by_role("spinbutton", name=f"{fee_name} percentage for {level_name}", exact=True)

    def remove_button(self, fee_name: str):
        return self.page.get_by_role("button", name=f"Remove {fee_name}", exact=True)

    # ---- review step
    def review(self) -> None:
        self.go_next()
        expect(self.page.get_by_role("heading", name="Review SBFAS scheme")).to_be_visible()

    def save_draft(self) -> None:
        self.page.get_by_role("button", name="Save draft").click()

    def publish(self) -> None:
        self.page.get_by_role("button", name="Publish", exact=True).click()


class SbfasAddFee(BasePage):
    """The Add fee component dialog opened from the row menu."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.dialog = page.get_by_role("dialog", name="Add fee component")
        self.fee_select = self.dialog.get_by_label("Fee component")
        self.submit = self.dialog.get_by_role("button", name="Add fee", exact=True)
        self.cancel = self.dialog.get_by_role("button", name="Cancel")

    def options(self) -> list[str]:
        try:
            expect(self.fee_select).to_be_enabled(timeout=10_000)
            self.fee_select.locator("option:not([value=''])").first.wait_for(state="attached", timeout=5_000)
        except Exception:
            pass
        return [norm(o) for o in self.fee_select.locator("option").all_text_contents() if norm(o) != "Choose a fee"]

    def level_rows(self) -> list[str]:
        return [norm(t) for t in self.dialog.locator("[class*='feeRow'] > span").all_text_contents()]

    def percentage(self, level_name: str):
        return self.dialog.get_by_role("spinbutton", name=f"{level_name} subsidy percentage", exact=True)
