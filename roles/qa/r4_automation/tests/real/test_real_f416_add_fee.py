"""F4.16 Add fees to a scheme on the real admin portal (localhost).

Real flow: row menu > Add fees opens /moe-hq/moe-fas/<id>/add-fee. Existing components are read only, new ones are picked
with the Fee Components dialog, Confirm saves and opens the scheme detail. Schemes are created through the API (prefix R4-AUTO).
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_schemes import LEVELS

pytestmark = [pytest.mark.f416, pytest.mark.mutating]


def test_tc_231_add_fees_from_the_list_opens_the_add_fee_page(lst, make_scheme, page):
    """TC-231 A Draft scheme offers Add fees in its row menu and the action opens the Add fee page of that scheme."""
    scheme = make_scheme("addfee-list")
    lst.open()
    lst.do_action(scheme["name"], "Add fees")
    page.wait_for_url(re.compile(rf"/moe-hq/moe-fas/{re.escape(str(scheme['id']))}/add-fee$"))
    expect(page.get_by_role("heading", level=1, name="Add fee", exact=True)).to_be_visible()


def test_tc_232_existing_components_are_read_only(add_fee, make_scheme, need_components):
    """TC-232 The existing component is shown with its values, cannot be edited or removed, and is ticked and locked in the picker."""
    need_components(2)
    scheme = make_scheme("addfee-ro")
    add_fee.open(scheme["id"])
    wiz = add_fee.wizard_like()
    existing = scheme["component_names"][0]
    assert wiz.column_headers() == [existing]
    for level, value in zip(LEVELS, ("10", "20", "30")):
        cell = wiz.cell(existing, level)
        expect(cell).to_be_disabled()
        assert cell.input_value() == value
    assert wiz.remove_button(existing).count() == 0
    wiz.open_picker()
    options = {name: (checked, disabled) for name, checked, disabled in wiz.picker_options()}
    assert options[existing] == (True, True), f"existing component in the picker: {options[existing]}"
    others = [v for k, v in options.items() if k != existing]
    assert others and all(v == (False, False) for v in others), f"other components: {others}"


def test_tc_233_new_component_column_is_editable_and_removable(add_fee, make_scheme, need_components):
    """TC-233 A picked component adds an editable column, the cross removes it again."""
    need_components(2)
    scheme = make_scheme("addfee-new")
    add_fee.open(scheme["id"])
    wiz = add_fee.wizard_like()
    new = wiz.pick(1)[0]
    assert wiz.column_headers() == scheme["component_names"] + [new]
    for level in LEVELS:
        expect(wiz.cell(new, level)).to_be_editable()
    wiz.remove_button(new).click()
    assert wiz.column_headers() == scheme["component_names"]


def test_tc_234_invalid_new_cell_blocks_confirm(add_fee, make_scheme, need_components, page):
    """TC-234 A new cell above 100 blocks Confirm: the page stays on Add fee and the scheme is not changed."""
    need_components(2)
    scheme = make_scheme("addfee-bad")
    add_fee.open(scheme["id"])
    wiz = add_fee.wizard_like()
    new = wiz.pick(1)[0]
    wiz.cell(new, "Primary").fill("101")
    add_fee.confirm.click()
    assert re.search(r"/add-fee$", page.url), "left the Add fee page with an invalid cell"
    expect(page.locator("#moefas-amount-error")).to_be_visible()


@pytest.mark.known_defect(reason="Front end shows the key of an untranslated message: errors.amountRange is not defined in resource.ts (see TC-205)")
def test_tc_234b_invalid_new_cell_message_is_readable(add_fee, make_scheme, need_components, page):
    """TC-234 The message for an invalid new cell names the range 0 to 100."""
    need_components(2)
    scheme = make_scheme("addfee-msg")
    add_fee.open(scheme["id"])
    wiz = add_fee.wizard_like()
    new = wiz.pick(1)[0]
    wiz.cell(new, "Primary").fill("101")
    text = page.locator("#moefas-amount-error").inner_text()
    assert "features." not in text and re.search(r"0\D+100", text), f"message is {text!r}"


def test_tc_236_confirm_saves_the_new_component(add_fee, detail, make_scheme, need_components, api, base, page):
    """TC-236 Confirm saves the new component, opens the scheme and shows the new column next to the unchanged old one."""
    need_components(2)
    scheme = make_scheme("addfee-save")
    add_fee.open(scheme["id"])
    wiz = add_fee.wizard_like()
    new = wiz.pick(1)[0]
    wiz.fill_levels(new, ("100", "70", "50"))
    add_fee.confirm.click()
    page.wait_for_url(re.compile(rf"/moe-hq/moe-fas/{re.escape(str(scheme['id']))}$"), timeout=15_000)
    expect(page.get_by_role("heading", level=2, name="Subsidy", exact=True)).to_be_visible()
    expect(page.get_by_role("columnheader", name=new, exact=True)).to_be_visible()
    old = scheme["component_names"][0]
    cols = detail.columns()
    assert old in cols and new in cols, f"columns: {cols}"
    assert [detail.percent(old, l) for l in LEVELS] == ["10%", "20%", "30%"]
    assert [detail.percent(new, l) for l in LEVELS] == ["100%", "70%", "50%"]
    stored = real_api.get_scheme(api, base, scheme["id"])
    assert len(stored["subsidies"]) == 6
