"""e-Service FAS pages of the parent: My FAS Applications (/fas-application), the single form Apply for Financial Assistance
(/fas-application/new) and the confirmation. English labels come from apps/e-service/src/features/fas-application/resource.ts.

The build has ONE form, not the five step wizard of the UAT master. Applicant fields have fixed ids (applicant-fullName ...).
Beneficiary and family member rows have generated ids, so they are found by their section (aria-labelledby).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from playwright.sync_api import Locator, Page, expect

from pages.base_page import norm, read_dl

H_LIST = "My FAS Applications"
H_FORM = "Apply for Financial Assistance"
H_DONE = "Application submitted"


@dataclass
class Person:
    full_name: str
    nric: str
    dob: str          # ISO yyyy-mm-dd
    gender: str       # MALE, FEMALE, OTHER


@dataclass
class Applicant(Person):
    nationality: str = "SC"          # SC, PR, IS_ASEAN, IS_NON_ASEAN
    race: str = "CHINESE"
    relationship: str = "MOTHER"
    phone: str = "91234567"
    employment: str = "Employed"
    email: str = "uat.parent@example.com"
    address: str = "Blk 418 Serangoon Central #09-321, Singapore 550418"


@dataclass
class Beneficiary(Person):
    school: str = "UAT Primary School"
    level: str = "PRIMARY"           # PRIMARY, SECONDARY, PRE_UNIVERSITY
    grade: str = "P4"


@dataclass
class FamilyMember(Person):
    relationship: str = "FATHER"
    has_income: bool = False
    income: str = ""


@dataclass
class Submission:
    code: str = ""
    status: str = ""
    submitted_at: str = ""
    facts: list[tuple[str, str]] = field(default_factory=list)


class FasPages:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base = base_url.rstrip("/")

    # ---------------------------------------------------------------- list
    def open_list(self) -> "FasPages":
        self.page.goto(f"{self.base}/fas-application")
        expect(self.page.get_by_role("heading", name=H_LIST).first).to_be_visible(timeout=20_000)
        self._wait_list_loaded()
        return self

    def _wait_list_loaded(self) -> None:
        loaded = self.page.locator("[data-tour-page='fas-applications'][data-tour-state]")
        try:
            self.page.wait_for_function(
                "() => { const e = document.querySelector(\"[data-tour-page='fas-applications']\"); return !e || e.getAttribute('data-tour-state') !== 'loading'; }",
                timeout=15_000)
        except Exception:  # noqa: BLE001
            pass

    @property
    def new_button(self) -> Locator:
        return self.page.get_by_role("button", name="New Application")

    def application_codes(self) -> list[str]:
        """Codes shown on the cards of the list (the bold text of each card)."""
        return [norm(t) for t in self.page.locator("main strong").all_inner_texts() if re.match(r"^[A-Z]{2,}[-A-Z0-9]*\d", norm(t))]

    def card_texts(self) -> list[str]:
        return [norm(c.inner_text()) for c in self.page.locator("main [class*='appCard']").all()]

    # ---------------------------------------------------------------- form
    def open_form(self) -> "FasPages":
        self.page.goto(f"{self.base}/fas-application/new")
        expect(self.page.get_by_role("heading", name=H_FORM).first).to_be_visible(timeout=20_000)
        self.wait_form_ready()
        return self

    def wait_form_ready(self, timeout: int = 40_000) -> None:
        """The form shows 'Loading your saved details' while the prefill call runs. When the call fails it shows
        'Saved details are unavailable' and a blank form (this is what happens when the prefill service answers 502)."""
        expect(self.page.locator("#applicant-fullName")).to_be_visible(timeout=timeout)

    def prefill_state(self) -> str:
        """'prefilled' when applicant fields are locked or filled, 'blank' otherwise."""
        if self.page.get_by_text("Saved details are unavailable").count() > 0:
            return "unavailable"
        value = self.page.locator("#applicant-fullName").input_value()
        return "prefilled" if value.strip() else "blank"

    def _set(self, locator: Locator, value: str) -> None:
        if locator.is_disabled() or locator.get_attribute("readonly") is not None:
            return  # locked by the prefill, keep the system value
        locator.fill(value)

    def fill_applicant(self, a: Applicant, academic_year: str) -> None:
        p = self.page
        self._set(p.locator("#fas-academic-year"), academic_year)
        self._set(p.locator("#applicant-fullName"), a.full_name)
        self._set(p.locator("#applicant-nric"), a.nric)
        self._set(p.locator("#applicant-dateOfBirth"), a.dob)
        for field_id, value in (("gender", a.gender), ("nationality", a.nationality), ("race", a.race), ("relationship", a.relationship)):
            sel = p.locator(f"#applicant-{field_id}")
            if sel.is_enabled():
                sel.select_option(value)
        self._fill_if_empty(p.locator("#applicant-employmentStatus"), a.employment)
        self._set(p.locator("#applicant-phoneNumber"), a.phone)
        self._set(p.locator("#applicant-email"), a.email)
        self._set(p.locator("#applicant-address"), a.address)

    def tick_commitment(self) -> None:
        box = self.page.locator("#applicant-commitmentAgreed")
        if not box.is_checked():
            box.check(force=True)

    @property
    def beneficiaries(self) -> Locator:
        return self.page.locator("section[aria-labelledby='beneficiaries-heading']")

    @property
    def family_members(self) -> Locator:
        return self.page.locator("section[aria-labelledby='family-members-heading']")

    def _rows(self, section: Locator) -> Locator:
        return section.locator("article, fieldset, [class*='row']").filter(has=self.page.get_by_label("Full name", exact=False))

    # ---- rows. The form opens with the children and the spouse of the parent already filled from system records (locked).
    # Rows have generated ids <uuid>-fullName, <uuid>-nric, <uuid>-dateOfBirth, <uuid>-gender, <uuid>-schoolName, <uuid>-classLevel,
    # <uuid>-grade (beneficiary) and <uuid>-fullName ... <uuid>-relationship, radios named <uuid>-hasIncome (family member).
    def _row_ids(self, section: Locator) -> list[str]:
        return section.locator("input[id$='-fullName']").evaluate_all("els => els.map(e => e.id.slice(0, e.id.length - '-fullName'.length))")

    def beneficiary_count(self) -> int:
        return len(self._row_ids(self.beneficiaries))

    def family_count(self) -> int:
        return len(self._row_ids(self.family_members))

    def _field(self, prefix: str, key: str) -> Locator:
        return self.page.locator(f"[id='{prefix}-{key}']")

    def _is_locked(self, loc: Locator) -> bool:
        return loc.count() == 0 or loc.is_disabled() or loc.get_attribute("readonly") is not None

    def _fill_if_empty(self, loc: Locator, value: str) -> bool:
        """Fill an open field that is still empty. A locked field or a field that already has a value is left alone."""
        if loc.count() == 0 or self._is_locked(loc):
            return False
        if loc.evaluate("e => e.tagName") == "SELECT":
            if not loc.input_value():
                loc.select_option(value)
        elif not loc.input_value().strip():
            loc.fill(value)
        return True

    def row_is_locked(self, section: Locator, index: int) -> bool:
        prefix = self._row_ids(section)[index]
        return self._is_locked(self._field(prefix, "fullName"))

    def fill_beneficiary(self, b: Beneficiary, index: int = 0) -> None:
        prefix = self._row_ids(self.beneficiaries)[index]
        for key, value in (("fullName", b.full_name), ("nric", b.nric), ("dateOfBirth", b.dob), ("gender", b.gender),
                           ("schoolName", b.school), ("classLevel", b.level), ("grade", b.grade)):
            self._fill_if_empty(self._field(prefix, key), value)

    def complete_open_fields(self) -> None:
        """Give a value to every open empty required field of the rows filled from system records (for example Gender)."""
        for index in range(self.beneficiary_count()):
            prefix = self._row_ids(self.beneficiaries)[index]
            self._fill_if_empty(self._field(prefix, "gender"), "MALE")
        for index in range(self.family_count()):
            prefix = self._row_ids(self.family_members)[index]
            self._fill_if_empty(self._field(prefix, "gender"), "FEMALE")

    def add_beneficiary(self) -> None:
        self.page.get_by_role("button", name="Add beneficiary").click()

    def add_family_member(self) -> None:
        self.page.get_by_role("button", name="Add family member").click()

    def _remove_row(self, section_id: str, prefix: str, button: str) -> None:
        card = self._field(prefix, "fullName").locator(f"xpath=ancestor::*[.//button[normalize-space()='{button}']][1]")
        card.get_by_role("button", name=button).click()

    def use_only_typed_beneficiaries(self, children: list[Beneficiary]) -> None:
        """The children of the system records are locked and cannot be edited. To test the form with chosen data: add one blank row per child,
        fill it, then remove the locked rows."""
        locked = [i for i in range(self.beneficiary_count()) if self.row_is_locked(self.beneficiaries, i)]
        for _ in children:
            self.add_beneficiary()
        ids = self._row_ids(self.beneficiaries)
        typed = [prefix for prefix in ids if not self._is_locked(self._field(prefix, "fullName"))]
        for prefix, child in zip(typed, children):
            for key, value in (("fullName", child.full_name), ("nric", child.nric), ("dateOfBirth", child.dob), ("gender", child.gender),
                               ("schoolName", child.school), ("classLevel", child.level), ("grade", child.grade)):
                self._fill_if_empty(self._field(prefix, key), value)
        for prefix in [p for p in ids if self._is_locked(self._field(p, "fullName"))]:
            self._remove_row("beneficiaries-heading", prefix, "Remove beneficiary")
        del locked

    def fill_family_member(self, m: FamilyMember, index: int = 0) -> None:
        prefix = self._row_ids(self.family_members)[index]
        for key, value in (("fullName", m.full_name), ("nric", m.nric), ("dateOfBirth", m.dob), ("gender", m.gender), ("relationship", m.relationship)):
            self._fill_if_empty(self._field(prefix, key), value)
        radio = self.page.locator(f"input[name='{prefix}-hasIncome'][value='{'yes' if m.has_income else 'no'}']")
        if radio.count() and radio.is_enabled() and not self.page.locator(f"input[name='{prefix}-hasIncome']:checked").count():
            radio.check(force=True)
        if m.has_income and m.income:
            self._fill_if_empty(self._field(prefix, "monthlyIncome"), m.income)

    def ensure_family_member(self, m: FamilyMember) -> None:
        """The spouse comes from the system records when the parent has one. Add a row only when there is none."""
        if self.family_count() == 0:
            self.add_family_member()
        self.fill_family_member(m, 0)

    @property
    def submit_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"^Submit application"))

    def submit(self) -> None:
        self.submit_button.click()

    def form_errors(self) -> list[str]:
        """Texts of the error summary and the field errors after a failed submit."""
        out = [norm(t) for t in self.page.locator("[role='alert'], [aria-invalid='true'] ~ *, [id$='-error']").all_inner_texts()]
        return [t for t in out if t]

    def wait_outcome(self, timeout: int = 40_000):
        """After Submit: ('done', Submission) when the confirmation opens, ('error', text) when the form shows an alert, ('none', '') on timeout."""
        import time
        end = time.time() + timeout / 1000
        while time.time() < end:
            if self.page.get_by_role("heading", name=H_DONE).count() > 0:
                return "done", self.wait_confirmation(5_000)
            alerts = [norm(t) for t in self.page.locator("[role='alert']").all_inner_texts() if norm(t)]
            if alerts:
                return "error", " | ".join(alerts)
            self.page.wait_for_timeout(500)
        return "none", ""

    def nationality(self) -> str:
        loc = self.page.locator("#applicant-nationality")
        return loc.input_value() if loc.count() else ""

    # ---------------------------------------------------------------- confirmation
    def wait_confirmation(self, timeout: int = 40_000) -> Submission:
        expect(self.page.get_by_role("heading", name=H_DONE)).to_be_visible(timeout=timeout)
        facts = read_dl(self.page.locator("main"))
        by = {k.lower(): v for k, v in facts}
        return Submission(code=by.get("application reference", ""), status=by.get("status", ""), submitted_at=by.get("submitted at", ""), facts=facts)
