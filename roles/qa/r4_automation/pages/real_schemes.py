"""Page objects for the REAL MOEFAS screens of the admin portal (MOE HQ), localhost:5173.

Screens (apps/admin-portal/src/features/moe-hq-fas-schemes):
  list     /moe-hq/moe-fas                 table, status cards, row menu (View, Publish, Add fees, Reactivate)
  wizard   /moe-hq/moe-fas/new             4 steps General, Eligibility, Subsidy, Review, buttons Discard, Draft, Back, Next/Publish
  detail   /moe-hq/moe-fas/<id>            read only view
  add fee  /moe-hq/moe-fas/<id>/add-fee    subsidy matrix, existing components read only, Cancel and Confirm

Locators use ids set by the front end (moefas-create-*), roles and the English labels of resource.ts.
The browser runs with locale en-US, so dates read MM/DD/YYYY and short dates read like "Jan 1, 2101".
"""
from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from . import real_api
from .real_login import goto_signed_in
from .base_page import BasePage, norm

EN_DASH = "–"
LIST_PATH = "moe-hq/moe-fas"
LEVELS = ["Primary", "Secondary", "Pre-University"]


def us_date(iso: str) -> str:
    """2101-01-31 -> 01/31/2101 (what formatNumericDate shows with en-US)."""
    y, m, d = iso.split("-")
    return f"{m}/{d}/{y}"


def short_date(iso: str) -> re.Pattern:
    """2101-01-05 -> regex for 'Jan 5, 2101' (formatShortDate with en-US)."""
    y, m, d = iso.split("-")
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
    return re.compile(rf"{month}\w*\.? {int(d)}, {y}")


def label_of(box) -> str:
    """Text of the label of a checkbox, whatever the markup (wrapping label or for=)."""
    return norm(box.evaluate("e => (e.labels && e.labels.length ? e.labels[0].innerText : (e.closest('label') ? e.closest('label').innerText : ''))"))


def tick(box) -> None:
    """Check a custom checkbox. The input can be visually hidden, so retry with force."""
    try:
        box.check(timeout=2_000)
    except Exception:
        box.check(force=True)


def untick(box) -> None:
    try:
        box.uncheck(timeout=2_000)
    except Exception:
        box.uncheck(force=True)


# ====================================================================== list
class SchemeList(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"
        self.heading = page.get_by_role("heading", level=1, name="MOEFAS", exact=True)
        self.table = page.get_by_role("table")
        self.new_scheme = page.get_by_role("link", name="New scheme")

    def open(self) -> "SchemeList":
        goto_signed_in(self.page, self.base, LIST_PATH)
        expect(self.heading).to_be_visible()
        self.wait_loaded()
        return self

    def wait_loaded(self) -> None:
        expect(self.table).to_be_visible()
        try:   # skeleton rows disappear when the list is loaded
            self.page.wait_for_function("() => !document.querySelector('table [class*=skeleton]')", timeout=15_000)
        except Exception:
            pass

    def subtitle(self) -> str:
        return norm(self.page.locator("section[aria-labelledby='moefas-schemes-title'] > header p").first.inner_text())

    def headers(self) -> list[str]:
        return [norm(t) for t in self.table.locator("thead th").all_inner_texts()]

    def rows(self) -> list[dict[str, str]]:
        """One dict per scheme row, keyed by the column header. The empty-state row is skipped."""
        heads = self.headers()
        out = []
        for tr in self.table.locator("tbody tr").all():
            cells = [norm(c) for c in tr.locator("td").all_inner_texts()]
            if len(cells) == len(heads):
                out.append(dict(zip(heads, cells)))
        return out

    def names(self) -> list[str]:
        return [r["Scheme"] for r in self.rows()]

    def row(self, name: str):
        return self.table.locator("tbody tr").filter(has=self.page.get_by_text(name, exact=True))

    def cards(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for li in self.page.get_by_role("list", name="MOEFAS schemes by status").locator("li").all():
            label = norm(li.locator("span").first.inner_text())
            count_str = norm(li.locator("strong").first.inner_text())
            if label == "Total schemes":
                continue
            out[label] = int(count_str)
        return out

    def menu_button(self, name: str):
        return self.page.get_by_role("button", name=f"Actions for {name}", exact=True)

    def actions(self, name: str) -> list[str]:
        self.menu_button(name).click()
        items = [norm(t) for t in self.page.get_by_role("menuitem").all_inner_texts()]
        self.page.keyboard.press("Escape")
        return items

    def do_action(self, name: str, label: str) -> None:
        self.menu_button(name).click()
        self.page.get_by_role("menuitem", name=label, exact=True).click()


# ==================================================================== wizard
class Wizard(BasePage):
    PATH = f"{LIST_PATH}/new"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"
        self.title = page.get_by_role("heading", level=1, name="Create new scheme")
        self.stepper = page.get_by_role("list", name="Create scheme progress")
        self.name = page.locator("#moefas-create-name")
        self.form_opens = page.locator("#moefas-create-form-opens")
        self.form_closes = page.locator("#moefas-create-form-closes")
        self.eff_from = page.locator("#moefas-create-effective-from")
        self.eff_to = page.locator("#moefas-create-effective-to")
        self.budget = page.locator("#moefas-create-total-budget")
        self.description = page.locator("#moefas-create-context")
        self.next_btn = page.get_by_role("button", name="Next", exact=True)
        self.back_btn = page.get_by_role("button", name="Back", exact=True)
        self.draft_btn = page.get_by_role("button", name="Draft", exact=True)
        self.discard_btn = page.get_by_role("button", name="Discard", exact=True)
        self.publish_btn = page.get_by_role("button", name="Publish", exact=True)
        self.save_failed = page.get_by_text("Could not save the scheme")

    # ------------------------------------------------------------ navigation
    def open(self) -> "Wizard":
        goto_signed_in(self.page, self.base, self.PATH)
        expect(self.title).to_be_visible()
        return self

    def step_labels(self) -> list[str]:
        # text_content: the labels are shown in capitals by CSS (text-transform), the DOM text is "General"
        return [norm(li.locator("span").nth(1).text_content()) for li in self.stepper.locator("li").all()]

    def current_step(self) -> str:
        return norm(self.stepper.locator("li[aria-current='step'] span").nth(1).text_content())

    def step_has_error_mark(self, label: str, timeout: int = 3_000) -> bool:
        loc = self.stepper.locator("li").filter(has_text=label).get_by_text("This step has errors")
        try:
            expect(loc).to_be_attached(timeout=timeout)
            return True
        except AssertionError:
            return False

    def go_next(self) -> None:
        self.next_btn.click()

    def error(self, text: str):
        """A visible message with this text (field errors and Alert)."""
        return self.page.get_by_text(text, exact=True)

    # --------------------------------------------------------------- step 1
    def fill_general(self, name: str, win: dict, budget: str = "1000", description: str | None = None) -> None:
        self.name.fill(name)
        self.form_opens.fill(win["opens"])
        self.form_closes.fill(win["closes"])
        self.eff_from.fill(win["eff_from"])
        if win.get("eff_to"):
            self.eff_to.fill(win["eff_to"])
        self.budget.fill(budget)
        if description is not None:
            self.description.fill(description)

    # --------------------------------------------------------------- step 2
    def nationality(self, label: str):
        return self.page.get_by_label(label, exact=True)

    def band_group(self, which: str):
        title = "Household income band" if which == "ghi" else "Per capita income band"
        return self.page.get_by_role("group", name=re.compile("^" + title))

    def use_band(self, which: str, from_: str = "0", to: str | None = "1000") -> None:
        group = self.band_group(which)
        tick(group.get_by_label("Use this criterion"))
        self.page.locator(f"#moefas-create-{which}-from").fill(from_)
        if to is not None:
            self.page.locator(f"#moefas-create-{which}-to").fill(to)

    def fill_eligibility(self, nationalities=("Singapore Citizen",), pci_to: str = "1100") -> None:
        for label in nationalities:
            tick(self.nationality(label))
        self.use_band("pci", "0", pci_to)

    # --------------------------------------------------------------- step 3
    @property
    def picker_button(self):
        return self.page.get_by_role("button", name="Fee Components", exact=True)

    @property
    def picker(self):
        return self.page.get_by_role("dialog", name="Select fee components")

    def open_picker(self):
        self.picker_button.click()
        expect(self.picker).to_be_visible()
        self.picker.evaluate("d => d.querySelectorAll('details').forEach(x => { x.open = true; })")
        return self.picker

    def picker_options(self) -> list[tuple[str, bool, bool]]:
        """[(name, checked, disabled)] for every component in the open picker."""
        out = []
        for box in self.picker.get_by_role("checkbox").all():
            out.append((label_of(box), box.is_checked(), box.is_disabled()))
        return out

    def pick(self, count: int = 1) -> list[str]:
        """Tick the first `count` components that are free to tick and press Apply. Returns their names."""
        self.open_picker()
        chosen: list[str] = []
        for box in self.picker.get_by_role("checkbox").all():
            if len(chosen) == count:
                break
            if box.is_checked() or box.is_disabled():
                continue
            chosen.append(label_of(box))
            tick(box)
        self.picker.get_by_role("button", name="Apply", exact=True).click()
        expect(self.picker).to_be_hidden()
        return chosen

    def cell(self, component: str, level: str):
        return self.page.get_by_label(f"{component} {EN_DASH} {level}", exact=True)

    def fill_levels(self, component: str, pct=("10", "20", "30")) -> None:
        for level, value in zip(LEVELS, pct):
            self.cell(component, level).fill(value)

    def column_headers(self) -> list[str]:
        heads = [norm(t) for t in self.page.get_by_role("table").locator("thead th").all_inner_texts()]
        return heads[1:]   # first header is Level

    def remove_button(self, component: str):
        return self.page.get_by_role("button", name=f"Remove {component}", exact=True)

    # ----------------------------------------------------------------- flows
    def to_eligibility(self) -> dict:
        """Fill a valid step 1 and move to step 2. Returns the period used."""
        win = real_api.window()
        self.fill_general(real_api.unique_name("wiz"), win)
        self.go_next()
        expect(self.page.get_by_role("heading", level=2, name="Eligibility", exact=True)).to_be_visible()
        return win

    def to_subsidy(self) -> None:
        """Valid steps 1 and 2, then step 3 (no component chosen yet)."""
        self.to_eligibility()
        self.fill_eligibility()
        self.go_next()
        expect(self.page.get_by_role("heading", level=2, name="Subsidy", exact=True)).to_be_visible()

    def complete(self, name: str, win: dict, components: int = 1, pct=("10", "20", "30")) -> list[str]:
        """Fill the three steps and stop on the Review step. Returns the chosen component names."""
        self.fill_general(name, win)
        self.go_next()
        self.fill_eligibility()
        self.go_next()
        chosen = self.pick(components)
        for comp in chosen:
            self.fill_levels(comp, pct)
        self.go_next()
        expect(self.page.get_by_role("heading", name="Review", exact=True)).to_be_visible()
        return chosen


# =================================================================== detail
class Detail(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"

    def open(self, scheme_id: str) -> "Detail":
        goto_signed_in(self.page, self.base, f"{LIST_PATH}/{scheme_id}")
        expect(self.page.get_by_role("heading", level=2, name="Subsidy", exact=True)).to_be_visible()
        return self

    def subsidy_table(self):
        return self.page.get_by_role("table")

    def columns(self) -> list[str]:
        return [norm(t) for t in self.subsidy_table().locator("thead th").all_inner_texts()][1:]

    def percent(self, component: str, level: str) -> str:
        idx = self.columns().index(component)
        row = self.subsidy_table().locator("tbody tr").filter(has=self.page.get_by_role("rowheader", name=level, exact=True))
        return norm(row.locator("td").nth(idx).inner_text())


# =================================================================== add fee
class AddFee(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base = base_url.rstrip("/") + "/"
        self.title = page.get_by_role("heading", level=1, name="Add fee", exact=True)
        self.confirm = page.get_by_role("button", name="Confirm", exact=True)
        self.cancel = page.get_by_role("button", name="Cancel", exact=True)

    def open(self, scheme_id: str) -> "AddFee":
        goto_signed_in(self.page, self.base, f"{LIST_PATH}/{scheme_id}/add-fee")
        expect(self.title).to_be_visible()
        expect(self.page.get_by_role("button", name="Fee Components", exact=True)).to_be_enabled()
        return self

    # the picker and the matrix are the same components as in the wizard
    def wizard_like(self) -> Wizard:
        return Wizard(self.page, self.base)
