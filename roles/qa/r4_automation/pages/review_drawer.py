"""ReviewDrawer: the side panel that opens from View or Review (FS F4 section 4 and 5)."""
from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from data import ui_text as T
from .base_page import BasePage, norm


class ReviewDrawer(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # the drawer is <aside class="drawer"> next to the sidebar <aside>
        self.root = page.locator("aside.drawer")
        self.overlay = page.locator(".drawer-overlay")
        self.eyebrow = self.root.locator(".eyebrow")
        self.title = self.root.get_by_role("heading", level=2)
        self.subtitle = self.root.locator(".drawer-head p")
        self.close_button = self.root.get_by_role("button", name=T.TIMES, exact=True)
        self.approve_button = self.root.get_by_role("button", name="Approve", exact=True)
        self.reject_button = self.root.get_by_role("button", name="Reject", exact=True)
        self.blue_note = self.root.locator(".note.blue")
        self.yellow_note = self.root.locator(".note.yellow")
        self.ml_tier = self.root.locator(".ml-box b")
        self.ml_tag = self.root.locator(".ml-box .ml-tag")

    # --------------------------------------------------------------- content
    def text(self) -> str:
        return norm(self.root.inner_text())

    def section(self, heading: str) -> Locator:
        """A block of the drawer found by its heading, for example 'ELIGIBILITY CHECK'."""
        h = self.page.get_by_role("heading", level=3, name=re.compile("^" + re.escape(heading) + "$", re.I))
        return self.root.locator("section.drawer-section").filter(has=h)

    def section_names(self) -> list[str]:
        return [norm(t).upper() for t in self.root.get_by_role("heading", level=3).all_inner_texts()]

    def row(self, section: str, label: str) -> Locator:
        """One 'label: value' line of a block."""
        label_span = self.page.locator("span", has_text=re.compile("^" + re.escape(label) + "$"))
        return self.section(section).locator(".info-row").filter(has=label_span)

    def value(self, section: str, label: str) -> Locator:
        return self.row(section, label).locator("strong")

    def badge(self, section: str, label: str) -> Locator:
        return self.row(section, label).locator(".badge")

    def expect_value(self, section: str, label: str, text: str) -> None:
        expect(self.value(section, label)).to_have_text(text)

    def history(self) -> list[tuple[str, str]]:
        """History lines as (date and time, event), oldest first as the drawer shows them."""
        out = []
        for r in self.section("HISTORY").locator(".info-row").all():
            out.append((norm(r.locator("span").first.inner_text()), norm(r.locator("strong").inner_text())))
        return out

    def history_events(self) -> list[str]:
        return [e for _, e in self.history()]

    def expect_history_contains(self, text: str) -> None:
        expect(self.section("HISTORY")).to_contain_text(text)

    def expect_history_order(self, events: list[str]) -> None:
        """The given events appear in the History in this order (other rows may sit between them)."""
        expect(self.section("HISTORY")).to_be_visible()
        got = self.history_events()
        pos = -1
        for wanted in events:
            nxt = next((i for i in range(pos + 1, len(got)) if wanted in got[i]), None)
            assert nxt is not None, f"History row {wanted!r} not found after position {pos}. History: {got}"
            pos = nxt

    def decision(self, label: str) -> Locator:
        return self.value("DECISION", label)

    def action_buttons(self) -> list[str]:
        """Names of the action buttons of the drawer. The close X and the View links of the
        Documents block (class link) are not decision buttons and are left out."""
        names = self.root.locator("button:not(.close):not(.link)").all_inner_texts()
        return [norm(n) for n in names]

    # --------------------------------------------------------------- closing
    def close(self) -> None:
        self.close_button.click()
        expect(self.root).to_have_count(0)

    def close_by_overlay(self) -> None:
        # click on the dimmed area on the left side, away from the drawer panel
        self.overlay.click(position={"x": 5, "y": 300})
        expect(self.root).to_have_count(0)
