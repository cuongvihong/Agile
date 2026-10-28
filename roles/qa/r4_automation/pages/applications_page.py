"""ApplicationsPage: FAS applications list for MOE HQ and for the School Admin (FS F4 section 3)."""
from __future__ import annotations

import csv
import re
from typing import Iterable

from playwright.sync_api import Locator, Page, expect

from data import ui_text as T
from .base_page import BasePage, norm

APP_ID = re.compile(r"APP-\d{4}-\d{5}")


def full_id(short: str) -> str:
    """'00377' -> 'APP-2026-00377'. A full id is returned unchanged."""
    return short if short.startswith("APP-") else "APP-2026-" + short


class ApplicationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", level=1, name="FAS applications")
        self.subtitle = page.locator("main .page-intro p")
        self.export_button = page.get_by_role("button", name="Export")
        self.search = page.get_by_placeholder(T.SEARCH_PLACEHOLDER)
        # stat cards are <div class="stat"><strong>9</strong><span>label</span><small>hint</small></div>
        self.cards = page.locator("main .stats .stat")
        # tabs are <div class="tabs"><button>Pending<em>4</em></button> ...
        self.tabs = page.locator("main .tabs button")
        self.table = page.locator("main table")
        self.headers = self.table.locator("thead th")
        self.rows = self.table.locator("tbody tr")
        self.id_cells = self.table.locator("tbody tr td:first-child strong")
        self.empty = page.locator("main .empty")
        self.footer = page.locator("main .table-footer")
        self.pager = page.locator("main .pager button")
        self.note = page.locator("main p.muted")

    # ----------------------------------------------------------------- cards
    def card(self, label: str) -> Locator:
        return self.cards.filter(has=self.page.locator("span", has_text=re.compile(r"^" + re.escape(label) + r"$")))

    def card_value(self, label: str) -> Locator:
        return self.card(label).locator("strong")

    def card_hint(self, label: str) -> Locator:
        return self.card(label).locator("small")

    def expect_cards(self, expected: dict) -> None:
        for label, value in expected.items():
            expect(self.card_value(label)).to_have_text(value)

    # ------------------------------------------------------------------ tabs
    def tab(self, name: str) -> Locator:
        return self.tabs.filter(has_text=re.compile(r"^" + re.escape(name) + r"\s*\d*$"))

    def tab_count(self, name: str) -> Locator:
        return self.tab(name).locator("em")

    def open_tab(self, name: str) -> None:
        self.tab(name).click()

    def expect_tabs(self, expected: dict) -> None:
        for name, count in expected.items():
            expect(self.tab_count(name)).to_have_text(str(count))

    def expect_active_tab(self, name: str) -> None:
        expect(self.tab(name)).to_have_class(re.compile(r"\bactive\b"))

    # --------------------------------------------------------------- filters
    def filter(self, name: str) -> Locator:
        """The select whose first option reads '<name>: All'. The selects have no label."""
        first_option = self.page.locator("option", has_text=re.compile(r"^" + re.escape(name) + r":"))
        return self.page.locator("main .filters select").filter(has=first_option)

    def set_filter(self, name: str, option: str) -> None:
        """option is the visible text, with or without the 'Name: ' prefix, for example 'Pending',
        'Submitted: Last 7 days' or 'Last 7 days'. The prefix is added when the option has it."""
        select = self.filter(name)
        texts = [norm(t) for t in select.locator("option").all_inner_texts()]
        wanted = (option, f"{name}: {option}")
        for index, text in enumerate(texts):
            if text in wanted:
                select.select_option(index=index)
                return
        raise AssertionError(f"Filter {name!r} has no option {option!r}. Options: {texts}")

    def filter_options(self, name: str) -> list[str]:
        return [norm(t) for t in self.filter(name).locator("option").all_inner_texts()]

    def filter_names(self) -> list[str]:
        names = []
        for sel in self.page.locator("main .filters select").all():
            first = norm(sel.locator("option").first.inner_text())
            names.append(first.split(":")[0])
        return names

    def clear_filters(self) -> None:
        self.search.fill("")
        for name in self.filter_names():
            self.set_filter(name, f"{name}: All" if name != "Submitted" else "Submitted: Any time")

    def do_search(self, text: str) -> None:
        self.search.fill(text)

    # ------------------------------------------------------------- the table
    def ids(self) -> list[str]:
        return [APP_ID.search(t).group(0) for t in self.id_cells.all_inner_texts() if APP_ID.search(t)]

    def short_ids(self) -> list[str]:
        return [i.rsplit("-", 1)[1] for i in self.ids()]

    def expect_ids(self, ids: Iterable[str]) -> None:
        expect(self.id_cells).to_have_text([full_id(i) for i in ids])

    def expect_empty(self) -> None:
        expect(self.empty).to_have_text(T.NO_RESULT)
        expect(self.id_cells).to_have_count(0)

    def row(self, app_id: str) -> Locator:
        return self.rows.filter(has=self.page.locator("strong", has_text=full_id(app_id)))

    def column_index(self, column: str) -> int:
        heads = [norm(t).upper() for t in self.headers.all_inner_texts()]
        return heads.index(column.upper())

    def column_names(self) -> list[str]:
        return [norm(t).upper() for t in self.headers.all_inner_texts()]

    def cell(self, app_id: str, column: str) -> Locator:
        return self.row(app_id).locator("td").nth(self.column_index(column))

    def cell_text(self, app_id: str, column: str) -> str:
        return norm(self.cell(app_id, column).inner_text())

    def row_values(self, app_id: str) -> dict:
        """Text of every cell of one row, keyed by the header (the student cell keeps name and NRIC apart)."""
        values = {}
        for i, head in enumerate(self.column_names()):
            values[head] = norm(self.row(app_id).locator("td").nth(i).inner_text())
        return values

    def expect_row(self, app_id: str, **columns: str) -> None:
        """Check cells of one row. Keys are the header names with spaces as underscores,
        for example expect_row('00412', SCHEME='MOEFAS', SYSTEM_CHECK='Waiting', STATUS='Pending')."""
        for key, text in columns.items():
            cell = self.cell(app_id, key.replace("_", " "))
            expect(cell).to_have_text(text if text else re.compile(r"^\s*$"))

    def row_button(self, app_id: str) -> Locator:
        return self.row(app_id).get_by_role("button")

    def open(self, app_id: str):
        """Click View or Review on a row and return the review drawer."""
        from .review_drawer import ReviewDrawer
        self.row_button(app_id).click()
        drawer = ReviewDrawer(self.page)
        expect(drawer.root).to_be_visible()
        expect(drawer.title).to_have_text(full_id(app_id))
        return drawer

    def footer_text(self) -> str:
        return norm(self.footer.locator("span").first.inner_text())

    def page_buttons(self) -> list[str]:
        return [norm(t) for t in self.pager.all_inner_texts()]

    # ---------------------------------------------------------------- export
    def export_csv(self) -> tuple:
        """Click Export and read the downloaded file. Returns (file name, rows) with the header as the first row."""
        with self.page.expect_download() as info:
            self.export_button.click()
        download = info.value
        with open(download.path(), encoding="utf-8-sig", newline="") as handle:
            return download.suggested_filename, list(csv.reader(handle))
