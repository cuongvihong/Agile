"""SchemesPage and SchemeWizard: MOEFAS schemes (MOE HQ) and SBFAS schemes (School Admin), FS F4 sections 6 and 7."""
from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from data import ui_text as T
from .base_page import BasePage, norm


class SchemesPage(BasePage):
    def __init__(self, page: Page, title: str = "MOEFAS schemes"):
        super().__init__(page)
        self.title = title
        self.heading = page.get_by_role("heading", level=1, name=title)
        self.subtitle = page.locator("main .page-intro p")
        self.new_button = page.get_by_role("button", name="New scheme")
        self.cards = page.locator("main .stats .stat")
        self.table = page.locator("main table")
        self.headers = self.table.locator("thead th")
        self.rows = self.table.locator("tbody tr")
        self.note = page.locator("main p.muted")

    # ----------------------------------------------------------------- cards
    def card_value(self, label: str) -> Locator:
        card = self.cards.filter(has=self.page.locator("span", has_text=re.compile(r"^" + re.escape(label) + r"$")))
        return card.locator("strong")

    def card_hint(self, label: str) -> Locator:
        card = self.cards.filter(has=self.page.locator("span", has_text=re.compile(r"^" + re.escape(label) + r"$")))
        return card.locator("small")

    # ------------------------------------------------------------------ rows
    def names(self) -> list[str]:
        return [norm(t) for t in self.rows.locator("td:first-child strong").all_inner_texts()]

    def row(self, name: str, eff_from: str | None = None, index: int = 0) -> Locator:
        """Row of a scheme. The same SBFAS name exists for two years, so pass eff_from or index."""
        rows = self.rows.filter(has=self.page.locator("strong", has_text=re.compile(r"^" + re.escape(name) + r"$")))
        if eff_from:
            rows = rows.filter(has_text=eff_from)
        return rows.nth(index)

    def cells(self, name: str, eff_from: str | None = None, index: int = 0) -> list[str]:
        return [norm(t) for t in self.row(name, eff_from, index).locator("td").all_inner_texts()]

    def action(self, name: str, label: str, eff_from: str | None = None, index: int = 0) -> Locator:
        return self.row(name, eff_from, index).get_by_role("button", name=label, exact=True)

    def actions(self, name: str, eff_from: str | None = None, index: int = 0) -> list[str]:
        return [norm(t) for t in self.row(name, eff_from, index).get_by_role("button").all_inner_texts()]

    def column_names(self) -> list[str]:
        return [norm(t).upper() for t in self.headers.all_inner_texts()]

    def cell(self, name: str, column: str, eff_from: str | None = None, index: int = 0) -> Locator:
        i = self.column_names().index(column.upper())
        return self.row(name, eff_from, index).locator("td").nth(i)

    # --------------------------------------------------------------- actions
    def open_view(self, name: str, eff_from: str | None = None, index: int = 0):
        from .dialogs import SchemeViewDialog
        self.action(name, "View", eff_from, index).click()
        dlg = SchemeViewDialog(self.page)
        dlg.expect_open()
        return dlg

    def new_scheme(self) -> "SchemeWizard":
        self.new_button.click()
        wiz = SchemeWizard(self.page)
        expect(wiz.heading).to_be_visible()
        return wiz


class SchemeWizard(BasePage):
    """The three step wizard. It is a page, not a dialog. The top bar and the bottom bar both
    hold Cancel or Next buttons, so the bottom ones are picked with .last."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.main = page.locator("main")
        self.heading = page.get_by_role("heading", level=1, name="Create new scheme")
        self.step_general = self.main.get_by_role("button", name=re.compile(r"^1 General"))
        self.step_eligibility = self.main.get_by_role("button", name=re.compile(r"^2 Eligibility"))
        self.step_subsidy = self.main.get_by_role("button", name=re.compile(r"^3 Subsidy"))
        self.cancel_button = self.main.get_by_role("button", name="Cancel", exact=True)
        self.back_button = self.main.get_by_role("button", name="Back", exact=True)
        self.next_button = self.main.get_by_role("button", name="Next", exact=True).last
        self.discard_button = self.main.get_by_role("button", name="Discard", exact=True)
        self.draft_button = self.main.get_by_role("button", name="Draft", exact=True)
        self.view_button = self.main.get_by_role("button", name="View", exact=True)
        self.blue_note = self.main.locator(".note.blue")
        self.errors = self.main.locator(".note.red")
        self.valid_note = self.main.locator(".note.green")

    # ----------------------------------------------------------------- steps
    def step(self, number: int) -> Locator:
        return {1: self.step_general, 2: self.step_eligibility, 3: self.step_subsidy}[number]

    def go_step(self, number: int) -> None:
        self.step(number).click()

    def step_label(self, number: int) -> str:
        return norm(self.step(number).inner_text())

    def has_warning(self, number: int) -> bool:
        return T.WARN in self.step_label(number)

    # --------------------------------------------------------------- step 1
    @property
    def name_input(self) -> Locator:
        return self.page.get_by_placeholder(re.compile(r"^e\.g\. "))

    def field(self, label: str) -> Locator:
        """A field of step 1 found by the start of its label. The text must start with the label, because the
        hint of Effective from also contains the words 'Form closes'."""
        return self.main.locator("label").filter(has_text=re.compile(r"^\s*" + re.escape(label)))

    def date_text(self, label: str) -> Locator:
        """Typed date field of one label: 'Form opens', 'Form closes', 'Effective from' or 'Effective to'."""
        return self.field(label).get_by_placeholder("DD/MM/YYYY")

    def date_picker(self, label: str) -> Locator:
        return self.field(label).locator("input[type=date]")

    def set_dates(self, form_opens: str | None = None, form_closes: str | None = None,
                  eff_from: str | None = None, eff_to: str | None = None) -> None:
        for label, value in (("Form opens", form_opens), ("Form closes", form_closes),
                             ("Effective from", eff_from), ("Effective to", eff_to)):
            if value is not None:
                self.date_text(label).fill(value)
                self.date_text(label).blur()

    def message(self, text: str) -> Locator:
        """Any text on the page, for example a field message under a date."""
        return self.main.get_by_text(text, exact=False)

    def error(self, text: str) -> Locator:
        """A red note of the wizard (name, fee component, cell errors)."""
        return self.errors.filter(has_text=text)

    def set_date(self, label: str, value: str) -> None:
        field = self.date_text(label)
        field.fill(value)
        field.blur()

    # --------------------------------------------------------------- step 2
    def nationality(self, label: str) -> Locator:
        return self.main.get_by_role("checkbox", name=label)

    @property
    def numbers(self) -> Locator:
        return self.main.locator("input[type=number]")

    @property
    def ghi_use(self) -> Locator:
        return self.main.get_by_label("Use this criterion").nth(0)

    @property
    def pci_use(self) -> Locator:
        return self.main.get_by_label("Use this criterion").nth(1)

    @property
    def ghi_from(self) -> Locator:
        return self.numbers.nth(0)

    @property
    def ghi_to(self) -> Locator:
        return self.numbers.nth(1)

    @property
    def pci_from(self) -> Locator:
        return self.numbers.nth(2)

    @property
    def pci_to(self) -> Locator:
        return self.numbers.nth(3)

    @property
    def match_rule(self) -> Locator:
        return self.main.locator("select").filter(has=self.page.locator("option[value=ALL]"))

    # --------------------------------------------------------------- step 3
    @property
    def value_type(self) -> Locator:
        return self.main.locator("select").filter(has=self.page.locator("option[value=P]"))

    @property
    def component_select(self) -> Locator:
        return self.main.locator("select").filter(has=self.page.locator("option", has_text="Select to add"))

    @property
    def subsidy_table(self) -> Locator:
        return self.main.locator("table")

    def add_component(self, label: str) -> None:
        self.component_select.select_option(label=label)

    def level_names(self) -> list:
        """Rows of the subsidy grid: Primary, Secondary, Pre-University for MOEFAS, the grades for SBFAS."""
        return [norm(t) for t in self.subsidy_table.locator("tbody tr td:first-child strong").all_inner_texts()]

    def component_columns(self) -> list[str]:
        heads = [norm(t).replace(T.CROSS, "").strip() for t in self.subsidy_table.locator("thead th").all_inner_texts()]
        return heads[1:]

    def remove_component(self, label: str) -> None:
        head = self.subsidy_table.locator("thead th").filter(has_text=re.compile(re.escape(label), re.I))
        head.get_by_title("Remove fee component").click()

    def level_row(self, level: str) -> Locator:
        return self.subsidy_table.locator("tbody tr").filter(has=self.page.locator("strong", has_text=level))

    def cell_input(self, level: str, column_index: int = 0) -> Locator:
        """Input in the row of a level or grade. column_index 0 is the first fee component column."""
        return self.level_row(level).locator("td").nth(column_index + 1).locator("input")

    def unit(self, level: str, column_index: int = 0) -> Locator:
        return self.level_row(level).locator("td").nth(column_index + 1).locator(".cell-edit span")

    def fill_all_cells(self, value: str, levels: list[str]) -> None:
        for level in levels:
            for i in range(len(self.component_columns())):
                self.cell_input(level, i).fill(value)

    # --------------------------------------------------------------- shortcuts
    def fill_valid_moefas(self, name: str, component: str = "School fee") -> None:
        """Name the scheme, add one component with 100/70/50 percent. Dates and eligibility keep their defaults."""
        self.name_input.fill(name)
        self.go_step(3)
        self.add_component(component)
        for level, value in (("Primary", "100"), ("Secondary", "70"), ("Pre-University", "50")):
            self.cell_input(level, 0).fill(value)

    def fill_valid_sbfas(self, name: str, component: str = "School fee", grades=("P1", "P2", "P3", "P4", "P5", "P6"),
                         value: str = "80") -> None:
        self.name_input.fill(name)
        self.go_step(3)
        self.add_component(component)
        for g in grades:
            self.cell_input(g, 0).fill(value)

    def open_review(self):
        from .dialogs import SchemeViewDialog
        self.go_step(3)
        self.view_button.click()
        dlg = SchemeViewDialog(self.page)
        dlg.expect_open()
        return dlg

    def save_draft(self) -> None:
        self.draft_button.click()
