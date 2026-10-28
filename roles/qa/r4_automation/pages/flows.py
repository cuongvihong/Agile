"""Flows: short sequences that several test cases share (close the form, approve, reject)."""
from __future__ import annotations

from playwright.sync_api import expect

from data import ui_text as T
from .applications_page import ApplicationsPage
from .dialogs import ApproveDialog, CloseFormDialog, RejectDialog
from .portal import Portal
from .schemes_page import SchemeWizard, SchemesPage


def close_form_now(portal: Portal, scheme: str = "MOEFAS 2027") -> SchemesPage:
    """MOE HQ: MOEFAS schemes, Close form now (demo) on one scheme, confirm, wait for the toast."""
    portal.go("MOEFAS schemes")
    schemes = SchemesPage(portal.page, "MOEFAS schemes")
    schemes.action(scheme, "Close form now (demo)").click()
    dialog = CloseFormDialog(portal.page)
    dialog.expect_open()
    dialog.confirm()
    dialog.expect_closed()
    portal.expect_toast(T.TOAST_FORM_CLOSED)
    return schemes


def open_hq_list(portal: Portal) -> ApplicationsPage:
    portal.go("FAS applications")
    apps = ApplicationsPage(portal.page)
    expect(apps.heading).to_be_visible()
    return apps


def approve_sbfas(portal: Portal, app_id: str, tier: str | None = None, comment: str | None = None) -> None:
    """School Admin: open the pending application, approve with a tier and an optional comment."""
    apps = ApplicationsPage(portal.page)
    drawer = apps.open(app_id)
    drawer.approve_button.click()
    dialog = ApproveDialog(portal.page)
    dialog.expect_open()
    if tier:
        dialog.choose_tier(tier)
    if comment is not None:
        dialog.comment.fill(comment)
    dialog.confirm()
    dialog.expect_closed()


def reject_sbfas(portal: Portal, app_id: str, reason: str = "Income above limit",
                 comment: str = "Household income is above the tier limits.") -> None:
    apps = ApplicationsPage(portal.page)
    drawer = apps.open(app_id)
    drawer.reject_button.click()
    dialog = RejectDialog(portal.page)
    dialog.expect_open()
    dialog.choose_reason(reason)
    dialog.comment.fill(comment)
    dialog.reject()
    dialog.expect_closed()
    portal.expect_toast(T.TOAST_REJECTED)


def open_approve_dialog(apps: ApplicationsPage, app_id: str = "00398") -> ApproveDialog:
    """School Admin: Review on a pending application, then Approve. Returns the open dialog."""
    drawer = apps.open(app_id)
    drawer.approve_button.click()
    dialog = ApproveDialog(apps.page)
    dialog.expect_open()
    return dialog


def open_reject_dialog(apps: ApplicationsPage, app_id: str = "00398") -> RejectDialog:
    drawer = apps.open(app_id)
    drawer.reject_button.click()
    dialog = RejectDialog(apps.page)
    dialog.expect_open()
    return dialog


def build_moefas(schemes: SchemesPage, name: str, form_opens: str | None = None, form_closes: str | None = None,
                 eff_from: str | None = None, eff_to: str | None = None) -> SchemeWizard:
    """HQ: New scheme, optional dates, School fee at 100/70/50 percent. Nothing is saved yet."""
    wizard = schemes.new_scheme()
    wizard.set_dates(form_opens, form_closes, eff_from, eff_to)
    wizard.fill_valid_moefas(name)
    return wizard


def build_sbfas(schemes: SchemesPage, name: str, form_opens: str | None = None, form_closes: str | None = None,
                eff_from: str | None = None, eff_to: str | None = None, grades=("P1", "P2", "P3", "P4", "P5", "P6")
                ) -> SchemeWizard:
    """School Admin: New scheme, optional dates, School fee at 80 percent for every grade."""
    wizard = schemes.new_scheme()
    wizard.set_dates(form_opens, form_closes, eff_from, eff_to)
    wizard.fill_valid_sbfas(name, grades=grades)
    return wizard


def publish(portal: Portal, wizard: SchemeWizard) -> None:
    """View, Publish and wait for the toast."""
    dialog = wizard.open_review()
    dialog.publish_button.click()
    dialog.expect_closed()
    portal.expect_toast(T.TOAST_PUBLISHED)
