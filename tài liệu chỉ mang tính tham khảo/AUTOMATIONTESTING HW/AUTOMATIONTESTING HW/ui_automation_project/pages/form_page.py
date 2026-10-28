"""FormPage: Page Object for curricula_trainer_account.html
("Curricula - Create Trainer Account").

Locator strategy follows docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md, §3:
most <label> elements in the AUT are NOT programmatically associated with
their inputs (no `for` attribute, input not wrapped) — verified by reading
the raw markup, not assumed. get_by_label() therefore does not resolve most
fields. Real <button>s and the radio/checkbox inputs that ARE wrapped by
their <label> use get_by_role(); every other input/select falls back to the
AUT's own hardcoded element id, which is stable because the app's own inline
script depends on those exact ids via document.getElementById.
"""
from __future__ import annotations

from typing import Optional

from .base_page import BasePage

# Mirrors the HTML's own `data-for` attribute values on each `.error` div.
ERROR_KEYS = (
    "preferredName", "gender", "idType", "idNumber", "idDocument",
    "nationality", "dob", "race", "birthCountry", "taxResident",
    "primaryEmail", "primaryPhone", "secondaryPhone",
    "emergencyName", "emergencyRelationship", "emergencyPhone",
    "postalCode", "blockNumber", "streetName", "floorUnit",
    "address1", "city", "countryRegion",
)


class FormPage(BasePage):
    """Page Object for the Trainer Account form."""

    def __init__(self, page):
        super().__init__(page)

        # --- Personal information ---
        self.preferred_name_input = page.locator("#preferredName")
        self.id_type_select = page.locator("#idType")
        self.id_number_input = page.locator("#idNumber")
        self.id_document_input = page.locator("#idDocument")
        self.nationality_select = page.locator("#nationality")
        self.dob_input = page.locator("#dob")
        self.race_select = page.locator("#race")
        self.birth_country_select = page.locator("#birthCountry")

        # --- Contact information ---
        self.primary_email_input = page.locator("#primaryEmail")
        self.primary_code_select = page.locator("#primaryCode")
        self.primary_phone_input = page.locator("#primaryPhone")
        self.secondary_code_select = page.locator("#secondaryCode")
        self.secondary_phone_input = page.locator("#secondaryPhone")

        # --- Emergency contact information ---
        self.emergency_name_input = page.locator("#emergencyName")
        self.emergency_relationship_select = page.locator("#emergencyRelationship")
        self.emergency_code_select = page.locator("#emergencyCode")
        self.emergency_phone_input = page.locator("#emergencyPhone")

        # --- Residential address ---
        self.country_region_select = page.locator("#countryRegion")
        self.postal_code_input = page.locator("#postalCode")
        self.block_number_input = page.locator("#blockNumber")
        self.building_name_input = page.locator("#buildingName")
        self.street_name_input = page.locator("#streetName")
        self.floor_number_input = page.locator("#floorNumber")
        self.unit_number_input = page.locator("#unitNumber")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.city_input = page.locator("#city")
        self.state_province_input = page.locator("#stateProvince")

        # --- Actions / result ---
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.success_box = page.locator("#successBox")

    # ------------------------------------------------------- role helpers --
    def _radio(self, accessible_name: str):
        # Radio <label>s wrap their <input>, so the accessible name equals
        # the visible label text (which is also the option's own value:
        # "Male"/"Female", "Yes"/"No", "Singapore"/"Non-Singapore").
        # exact=True is required: Playwright's default name match is a
        # substring match, so name="Singapore" would otherwise also match
        # the "Non-Singapore" radio (found by running this for real).
        return self.page.get_by_role("radio", name=accessible_name, exact=True)

    def _floor_not_applicable_checkbox(self):
        return self.page.get_by_role(
            "checkbox", name="Floor/Unit number is not applicable"
        )

    def error_locator(self, key: str):
        if key not in ERROR_KEYS:
            raise ValueError(f"Unknown error key: {key!r}")
        return self.page.locator(f'[data-for="{key}"]')

    def set_raw_value(self, locator, value: str) -> None:
        """Set an input's DOM value directly via JS, bypassing the browser's
        own HTML `maxlength` enforcement.

        `.fill()` (used everywhere else in this class) respects `maxlength`
        exactly like a real user typing would — confirmed empirically
        (found while testing TC-TS02-PPHONE-009: a 16-digit `.fill()` on
        `primaryPhone`, which has `maxlength="15"`, silently truncates to
        15 chars, making the 16-char boundary untestable through normal
        interaction). Some official test cases specifically target the
        underlying JS validation logic at a boundary that coincides with an
        HTML length cap — this method exists only for that narrow purpose,
        not as a general-purpose replacement for `.fill()`.
        """
        locator.evaluate("(el, v) => { el.value = v; }", value)

    def is_radio_checked(self, accessible_name: str) -> bool:
        """Public reader for a radio's checked state, by its visible label
        text (exact match — see `_radio()`). Used by tests that only need to
        confirm a selection stuck, without necessarily submitting the form.
        """
        return self._radio(accessible_name).is_checked()

    # ---------------------------------------------------------------- open --
    def open(self, url: str) -> "FormPage":
        super().open(url)
        return self

    # ------------------------------------------------------- field setters --
    def set_preferred_name(self, value: str) -> None:
        self.preferred_name_input.fill(value)

    def select_gender(self, value: str) -> None:
        self._radio(value).check()

    def select_id_type(self, value: str) -> None:
        self.id_type_select.select_option(label=value)

    def set_id_number(self, value: str) -> None:
        self.id_number_input.fill(value)

    def upload_id_document(self, file_path: str) -> None:
        self.id_document_input.set_input_files(file_path)

    def select_nationality(self, value: str) -> None:
        self.nationality_select.select_option(label=value)

    def set_dob(self, value: str) -> None:
        """value: 'YYYY-MM-DD', the format input[type=date].fill() expects."""
        self.dob_input.fill(value)

    def select_race(self, value: str) -> None:
        self.race_select.select_option(label=value)

    def select_birth_country(self, value: str) -> None:
        self.birth_country_select.select_option(label=value)

    def select_tax_resident(self, value: str) -> None:
        self._radio(value).check()

    def set_primary_email(self, value: str) -> None:
        self.primary_email_input.fill(value)

    def set_primary_phone(self, code: Optional[str], number: str) -> None:
        if code:
            self.primary_code_select.select_option(value=code)
        self.primary_phone_input.fill(number)

    def set_secondary_phone(self, code: Optional[str], number: str) -> None:
        if code:
            self.secondary_code_select.select_option(value=code)
        self.secondary_phone_input.fill(number)

    def set_emergency_name(self, value: str) -> None:
        self.emergency_name_input.fill(value)

    def select_emergency_relationship(self, value: str) -> None:
        self.emergency_relationship_select.select_option(label=value)

    def set_emergency_phone(self, code: Optional[str], number: str) -> None:
        if code:
            self.emergency_code_select.select_option(value=code)
        self.emergency_phone_input.fill(number)

    def select_residential_type(self, value: str) -> None:
        """value: 'Singapore' or 'Non-Singapore'. Triggers the AUT's own
        show/hide + disable/auto-value logic (Session 01 doc, §2)."""
        self._radio(value).check()

    def select_country_region(self, value: str) -> None:
        self.country_region_select.select_option(label=value)

    def set_postal_code(self, value: str) -> None:
        self.postal_code_input.fill(value)
        # The AUT auto-fills block/street on blur for 3 hardcoded SG postal
        # codes (Session 01 doc, §2) — force a real blur so that behavior
        # actually fires, matching real user interaction.
        self.postal_code_input.blur()

    def set_block_number(self, value: str) -> None:
        self.block_number_input.fill(value)

    def set_building_name(self, value: str) -> None:
        self.building_name_input.fill(value)

    def set_street_name(self, value: str) -> None:
        self.street_name_input.fill(value)

    def set_floor_unit(self, floor: str, unit: str) -> None:
        self.floor_number_input.fill(floor)
        self.unit_number_input.fill(unit)

    def set_floor_not_applicable(self, checked: bool = True) -> None:
        checkbox = self._floor_not_applicable_checkbox()
        if checked:
            checkbox.check()
        else:
            checkbox.uncheck()

    def set_address1(self, value: str) -> None:
        self.address1_input.fill(value)

    def set_address2(self, value: str) -> None:
        self.address2_input.fill(value)

    def set_city(self, value: str) -> None:
        self.city_input.fill(value)

    def set_state_province(self, value: str) -> None:
        self.state_province_input.fill(value)

    # ------------------------------------------------------------ fill_form --
    def fill_form(self, data: dict) -> None:
        """Fill only the keys present in `data` — a test builds only the
        subset it needs (e.g. omitting fields on purpose for negative
        scenarios), so this method never fills a default for a missing key.

        Field order intentionally mirrors real user interaction:
        1. residential_type first, since it decides which fields further
           down are even visible/required (Session 01 doc, §2).
        2. postal_code next (if SG), so its on-blur auto-fill side effect
           runs BEFORE any explicit block_number/street_name below — an
           explicit value in `data` always wins over the auto-fill.
        3. everything else, in the AUT's own top-to-bottom field order.
        """
        if "residential_type" in data:
            self.select_residential_type(data["residential_type"])

        if "postal_code" in data:
            self.set_postal_code(data["postal_code"])

        simple_setters = {
            "preferred_name": self.set_preferred_name,
            "id_number": self.set_id_number,
            "dob": self.set_dob,
            "primary_email": self.set_primary_email,
            "emergency_name": self.set_emergency_name,
            "block_number": self.set_block_number,
            "building_name": self.set_building_name,
            "street_name": self.set_street_name,
            "address1": self.set_address1,
            "address2": self.set_address2,
            "city": self.set_city,
            "state_province": self.set_state_province,
        }
        for key, setter in simple_setters.items():
            if key in data:
                setter(data[key])

        select_setters = {
            "id_type": self.select_id_type,
            "nationality": self.select_nationality,
            "race": self.select_race,
            "birth_country": self.select_birth_country,
            "country_region": self.select_country_region,
            "emergency_relationship": self.select_emergency_relationship,
        }
        for key, setter in select_setters.items():
            if key in data:
                setter(data[key])

        radio_setters = {
            "gender": self.select_gender,
            "tax_resident": self.select_tax_resident,
        }
        for key, setter in radio_setters.items():
            if key in data:
                setter(data[key])

        if "id_document_path" in data:
            self.upload_id_document(data["id_document_path"])

        if "primary_phone" in data:
            self.set_primary_phone(data.get("primary_phone_code"), data["primary_phone"])

        if "secondary_phone" in data:
            self.set_secondary_phone(data.get("secondary_phone_code"), data["secondary_phone"])

        if "emergency_phone" in data:
            self.set_emergency_phone(data.get("emergency_phone_code"), data["emergency_phone"])

        if "floor_number" in data or "unit_number" in data:
            self.set_floor_unit(data.get("floor_number", ""), data.get("unit_number", ""))

        if "floor_not_applicable" in data:
            self.set_floor_not_applicable(data["floor_not_applicable"])

    # ---------------------------------------------------------------- submit --
    def submit(self) -> None:
        self.save_button.click()

    def cancel(self) -> None:
        self.cancel_button.click()

    # ------------------------------------------------------------ result readers --
    def is_success_visible(self) -> bool:
        return self.success_box.is_visible()

    def success_text(self) -> str:
        return self.success_box.inner_text()

    def is_field_error_visible(self, key: str) -> bool:
        return self.error_locator(key).is_visible()

    def field_error_text(self, key: str) -> str:
        return self.error_locator(key).inner_text()

    def is_input_invalid(self, input_locator) -> bool:
        classes = input_locator.get_attribute("class") or ""
        return "invalid" in classes.split()
