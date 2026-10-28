"""Dialogs of F4: approve, reject, close form (demo), scheme view, add fee.

All dialogs are <div class="modal"> inside <div class="overlay modal-overlay">.
The prototype gives them no dialog role, so they are found by the class.
"""
from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from data import ui_text as T
from .base_page import BasePage, norm


class Modal(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.locator(".modal")
        self.heading = self.root.locator(".dialog-heading")
        self.title = self.root.locator(".dialog-heading h2")
        self.subtitle = self.root.locator(".dialog-heading p")
        self.close_button = self.root.get_by_role("button", name=T.TIMES, exact=True)
        self.cancel_button = self.root.get_by_role("button", name="Cancel", exact=True)

    def text(self) -> str:
        return norm(self.root.inner_text())

    def expect_open(self) -> None:
        expect(self.root).to_be_visible()

    def expect_closed(self) -> None:
        expect(self.root).to_have_count(0)

    def cancel(self) -> None:
        self.cancel_button.click()
        self.expect_closed()

    def close(self) -> None:
        self.close_button.click()
        self.expect_closed()


class ApproveDialog(Modal):
    def __init__(self, page: Page):
        super().__init__(page)
        self.tier = self.root.get_by_role("combobox")
        self.tier_hint = self.root.locator("label.field").filter(has=page.locator("select")).locator("small")
        self.comment = self.root.get_by_placeholder("Add a note for the record")
        self.counter = self.root.get_by_text(re.compile(r"^\d+\s*/\s*500$"))
        self.confirm_button = self.root.get_by_role("button", name="Confirm approval", exact=True)

    def tier_options(self) -> list[str]:
        return [norm(t) for t in self.tier.locator("option").all_inner_texts()]

    def selected_tier(self) -> str:
        return norm(self.tier.locator("option:checked").inner_text())

    def choose_tier(self, name: str) -> None:
        self.tier.select_option(label=name)

    def confirm(self) -> None:
        self.confirm_button.click()


class RejectDialog(Modal):
    def __init__(self, page: Page):
        super().__init__(page)
        self.reason = self.root.get_by_role("combobox")
        self.reason_hint = self.root.locator("label.field").filter(has=page.locator("select")).locator("small")
        self.comment = self.root.get_by_placeholder("Explain the decision. Parent receives the reason by email.")
        self.counter = self.root.get_by_text(re.compile(r"^\d+\s*/\s*500$"))
        self.reject_button = self.root.get_by_role("button", name="Reject application", exact=True)

    def reason_options(self) -> list[str]:
        return [norm(t) for t in self.reason.locator("option").all_inner_texts()]

    def choose_reason(self, name: str) -> None:
        self.reason.select_option(label=name)

    def reject(self) -> None:
        self.reject_button.click()


class CloseFormDialog(Modal):
    def __init__(self, page: Page):
        super().__init__(page)
        self.confirm_button = self.root.get_by_role("button", name="Close form and assess", exact=True)
        self.consequences = self.root.locator("li")

    def confirm(self) -> None:
        self.confirm_button.click()


class SchemeViewDialog(Modal):
    """Read only view of a scheme, and the review step before Publish."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.footer_close = self.root.get_by_role("button", name="Close", exact=True)
        self.back_to_edit = self.root.get_by_role("button", name="Back to edit", exact=True)
        self.publish_button = self.root.get_by_role("button", name="Publish", exact=True)
        self.table = self.root.locator("table")
        self.blue_note = self.root.locator(".note.blue")
        self.errors = self.root.locator(".note.red")

    def value(self, label: str) -> Locator:
        """The value of one 'label: value' line of the General and Eligibility blocks."""
        span = self.page.locator("span", has_text=re.compile("^" + re.escape(label) + "$"))
        return self.root.locator(".info-row").filter(has=span).locator("strong")

    def sub_labels(self) -> list:
        return [norm(t).upper() for t in self.root.locator(".sub-label").all_inner_texts()]


class AddFeeDialog(Modal):
    def __init__(self, page: Page):
        super().__init__(page)
        self.component = self.root.get_by_role("combobox")
        self.table = self.root.locator("table")
        self.add_button = self.root.get_by_role("button", name="Add to scheme", exact=True)
        self.remove_buttons = self.root.get_by_title("Remove fee component")
        self.blue_note = self.root.locator(".note.blue")
        self.errors = self.root.locator(".note.red")

    def component_options(self) -> list:
        return [norm(t) for t in self.component.locator("option").all_inner_texts()
                if norm(t) and norm(t) != "Select to add"]

    def add_component(self, label: str) -> None:
        self.component.select_option(label=label)

    def column_names(self) -> list:
        return [norm(t).replace(T.CROSS, "").strip() for t in self.table.locator("thead th").all_inner_texts()]

    def cell_input(self, level: str, new_index: int = 0) -> Locator:
        """Input of the new column number new_index (0 is the first one added) in the row of a level.
        Existing columns are plain text, so only the new columns have an input."""
        row = self.table.locator("tbody tr").filter(has_text=level)
        return row.locator("input").nth(new_index)

    def level_names(self) -> list:
        return [norm(t) for t in self.table.locator("tbody tr td:first-child").all_inner_texts()]
