"""F9.8 Quy tắc dữ liệu và ràng buộc toàn vẹn trong DB/API (TC-145 đến TC-171).
Tất cả phép thử SQL đều chạy trong giao dịch có ROLLBACK hoàn toàn qua pages.db.sql_check_steps,
không để lại bất kỳ thay đổi nào trong cơ sở dữ liệu."""
from __future__ import annotations

import uuid
import pytest

from pages import db

pytestmark = [pytest.mark.f98]

SETUP_BASE = """
DECLARE @stu varchar(50) = (SELECT TOP 1 sc0.student_id FROM dbo.student_charges sc0 WHERE sc0.status = 'POSTED' AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items ii0 WHERE ii0.student_charge_id = sc0.id) ORDER BY sc0.student_id);
DECLARE @sch varchar(50) = (SELECT TOP 1 school_id FROM dbo.student_charges WHERE student_id = @stu);
DECLARE @chg1 varchar(50) = (
    SELECT TOP 1 sc.id FROM dbo.student_charges sc
    WHERE sc.student_id = @stu AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items ii WHERE ii.student_charge_id = sc.id)
);
DECLARE @inv varchar(50) = CONVERT(varchar(50), NEWID());
INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
VALUES (@inv, @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 3, SYSUTCDATETIME(), '2026-12-15');
DECLARE @tx varchar(50) = CONVERT(varchar(50), NEWID());
INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
VALUES (@tx, @inv, 'qa-user', CONCAT('TRX-QA-', CONVERT(varchar(36), NEWID())), CONCAT('idem-qa-', CONVERT(varchar(36), NEWID())), 100.00, 'SGD', 1);
"""


def test_tc_145_issued_invoice_zero_net_amount_refused():
    """TC-145: Hóa đơn đã phát hành (status != Draft) có net_amount = 0.00 bị từ chối bởi CK_invoices_IssuedAmount."""
    res = db.sql_check_steps(
        steps=[
            ("draft_zero_ok", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status)
                VALUES (NEWID(), @stu, @sch, 'SGD', 0.00, 0.00, 0.00, 1);
            """),
            ("issued_zero_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (NEWID(), @stu, @sch, 'SGD', 0.00, 0.00, 0.00, 2, SYSUTCDATETIME(), '2026-12-15');
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["draft_zero_ok"] == "OK"
    assert "CK_invoices_IssuedAmount" in res["issued_zero_err"]


def test_tc_146_invoice_line_amount_rules():
    """TC-146: Dòng hóa đơn bắt buộc gross > 0, subsidy >= 0, subsidy < gross, net = gross - subsidy > 0."""
    res = db.sql_check_steps(
        steps=[
            ("gross_zero", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 0.00, 0.00, 0.00);"),
            ("sub_neg", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 100.00, -5.00, 105.00);"),
            ("sub_eq_gross", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 100.00, 100.00, 0.00);"),
            ("sub_gt_gross", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 100.00, 120.00, -20.00);"),
            ("net_mismatch", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 100.00, 20.00, 75.00);"),
            ("valid_line", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 100.00, 20.00, 80.00);"),
        ],
        setup_sql=SETUP_BASE,
    )
    for k in ("gross_zero", "sub_neg", "sub_eq_gross", "sub_gt_gross", "net_mismatch"):
        assert "CK_invoice_items_Amounts" in res[k], f"{k} phải bị chặn: {res[k]}"
    assert res["valid_line"] == "OK"


def test_tc_147_charge_cannot_be_on_two_invoice_lines():
    """TC-147: Một student_charge_id không thể nằm trên hai dòng hóa đơn (UQ_invoice_items_StudentCharge)."""
    res = db.sql_check_steps(
        steps=[
            ("first_line", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 50.00, 0.00, 50.00);"),
            ("dup_charge", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 2, @chg1, 50.00, 0.00, 50.00);"),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["first_line"] == "OK"
    assert "UQ_invoice_items_StudentCharge" in res["dup_charge"]


@pytest.mark.api
def test_tc_148_line_for_charge_of_another_child_refused(api):
    """TC-148: Gửi yêu cầu tạo hóa đơn/checkout chứa khoản phí của học sinh khác sẽ bị từ chối."""
    own = db.sql_rows("SELECT TOP 1 student_id FROM dbo.student_charges WHERE status = 'POSTED' ORDER BY student_id")
    assert own, "Cần ít nhất 1 khoản phí POSTED trong DB"
    own_id = own[0]["student_id"]
    other_row = db.sql_rows(f"""
        SELECT TOP 1 student_id, id AS charge_id
        FROM dbo.student_charges
        WHERE student_id <> '{own_id}' AND status = 'POSTED'
    """)
    assert other_row, "Cần ít nhất 1 khoản phí POSTED của học sinh khác trong DB"
    other_charge_id = other_row[0]["charge_id"]

    res = api.post(
        "/billing/v1/checkout",
        {
            "studentId": own_id,
            "chargeIds": [other_charge_id],
            "method": "EducationAccount",
        },
        key=f"qa-tc148-{uuid.uuid4()}",
    )
    assert res.status in (400, 404, 422), f"Khoản phí của con khác phải bị từ chối: {res.status} {res.text()}"


@pytest.mark.known_defect(reason="DB và CheckoutPlanner chưa kiểm tra student_charges.school_id phải trùng với invoices.school_id")
def test_tc_149_line_from_another_school_than_invoice_refused():
    """TC-149: Dòng hóa đơn lấy khoản phí từ trường khác với school_id của hóa đơn phải bị từ chối."""
    res = db.sql_check_steps(
        steps=[
            ("other_school_line", """
                DECLARE @other_school varchar(50) = CONVERT(varchar(50), NEWID());
                DECLARE @inv_other varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (@inv_other, @stu, @other_school, 'SGD', 50.00, 0.00, 50.00, 3, SYSUTCDATETIME(), '2026-12-15');
                INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount)
                VALUES (NEWID(), @inv_other, 1, @chg1, 50.00, 0.00, 50.00);
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["other_school_line"] != "OK", "Hệ thống cho phép gắn khoản phí của trường khác vào hóa đơn mà không từ chối"


def test_tc_150_invoice_totals_and_net_formula_enforced():
    """TC-150: Hóa đơn bắt buộc gross >= 0, subsidy >= 0, subsidy <= gross và net = gross - subsidy (CK_invoices_Amounts)."""
    res = db.sql_check_steps(
        steps=[
            ("net_wrong", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (NEWID(), @stu, @sch, 'SGD', 250.00, 30.00, 200.00, 2, SYSUTCDATETIME(), '2026-12-15');
            """),
            ("sub_gt_gross", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 120.00, -20.00, 1);
            """),
            ("valid_totals", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (NEWID(), @stu, @sch, 'SGD', 250.00, 30.00, 220.00, 2, SYSUTCDATETIME(), '2026-12-15');
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert "CK_invoices_Amounts" in res["net_wrong"]
    assert "CK_invoices_Amounts" in res["sub_gt_gross"]
    assert res["valid_totals"] == "OK"


def test_tc_151_invoice_status_dates_rules():
    """TC-151: Các cột ngày (issued_at, due_date, paid_at, cancelled_at) phải khớp với status (CK_invoices_StatusDates)."""
    res = db.sql_check_steps(
        steps=[
            ("draft_with_issued_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 1, SYSUTCDATETIME());
            """),
            ("issued_no_due_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 2, SYSUTCDATETIME(), NULL);
            """),
            ("paid_no_paid_at_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date, paid_at)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 4, SYSUTCDATETIME(), '2026-12-15', NULL);
            """),
            ("cancelled_with_paid_at_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date, paid_at, cancelled_at)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 5, SYSUTCDATETIME(), '2026-12-15', SYSUTCDATETIME(), SYSUTCDATETIME());
            """),
            ("paid_valid_ok", """
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date, paid_at)
                VALUES (NEWID(), @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 4, SYSUTCDATETIME(), '2026-12-15', SYSUTCDATETIME());
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    for k in ("draft_with_issued_err", "issued_no_due_err", "paid_no_paid_at_err", "cancelled_with_paid_at_err"):
        assert "CK_invoices_StatusDates" in res[k], f"{k} phải bị chặn: {res[k]}"
    assert res["paid_valid_ok"] == "OK"


def test_tc_152_invoice_cannot_have_two_open_transactions():
    """TC-152: Một hóa đơn không thể có hai giao dịch đang mở (completed_at IS NULL) cùng lúc (UX_transactions_Invoice_Open)."""
    res = db.sql_check_steps(
        steps=[
            ("second_open_err", """
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
                VALUES (NEWID(), @inv, 'qa-user', 'TRX-QA-OPEN-2', 'idem-qa-open-2', 100.00, 'SGD', 1);
            """),
            ("close_first_then_open_ok", """
                UPDATE dbo.transactions SET status = 3, completed_at = SYSUTCDATETIME() WHERE id = @tx;
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
                VALUES (NEWID(), @inv, 'qa-user', 'TRX-QA-OPEN-3', 'idem-qa-open-3', 100.00, 'SGD', 1);
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert "UX_transactions_Invoice_Open" in res["second_open_err"]
    assert res["close_first_then_open_ok"] == "OK"


def test_tc_153_invoice_cannot_have_two_succeeded_transactions():
    """TC-153: Một hóa đơn không thể có hai giao dịch Succeeded (UX_transactions_Invoice_Succeeded)."""
    res = db.sql_check_steps(
        steps=[
            ("first_succeeded_ok", """
                UPDATE dbo.transactions SET status = 2, settled_amount = 100.00, completed_at = SYSUTCDATETIME() WHERE id = @tx;
            """),
            ("second_succeeded_err", """
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, settled_amount, currency_code, status, completed_at)
                VALUES (NEWID(), @inv, 'qa-user', 'TRX-QA-SUCC-2', 'idem-qa-succ-2', 100.00, 100.00, 'SGD', 2, SYSUTCDATETIME());
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["first_succeeded_ok"] == "OK"
    assert "UX_transactions_Invoice_Succeeded" in res["second_succeeded_err"]


def test_tc_154_same_user_and_idempotency_key_refused():
    """TC-154: Cùng một user và idempotency_key không thể tạo giao dịch thứ hai (UQ_transactions_User_Idempotency)."""
    res = db.sql_check_steps(
        steps=[
            ("first_idem_ok", """
                DECLARE @inv2 varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (@inv2, @stu, @sch, 'SGD', 80.00, 0.00, 80.00, 3, SYSUTCDATETIME(), '2026-12-15');
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
                VALUES (NEWID(), @inv2, 'parent-A', 'TRX-IDEM-1', 'shared-idem-key', 80.00, 'SGD', 1);
            """),
            ("same_user_same_key_err", """
                DECLARE @inv3 varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (@inv3, @stu, @sch, 'SGD', 80.00, 0.00, 80.00, 3, SYSUTCDATETIME(), '2026-12-15');
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
                VALUES (NEWID(), @inv3, 'parent-A', 'TRX-IDEM-2', 'shared-idem-key', 80.00, 'SGD', 1);
            """),
            ("other_user_same_key_ok", """
                DECLARE @inv4 varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (@inv4, @stu, @sch, 'SGD', 80.00, 0.00, 80.00, 3, SYSUTCDATETIME(), '2026-12-15');
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, currency_code, status)
                VALUES (NEWID(), @inv4, 'parent-B', 'TRX-IDEM-3', 'shared-idem-key', 80.00, 'SGD', 1);
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["first_idem_ok"] == "OK"
    assert "UQ_transactions_User_Idempotency" in res["same_user_same_key_err"]
    assert res["other_user_same_key_ok"] == "OK"


def test_tc_155_funding_reference_unique():
    """TC-155: Mỗi phần thanh toán có funding_reference duy nhất (UQ_tfs_FundingReference)."""
    res = db.sql_check_steps(
        steps=[
            ("first_leg_ok", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id)
                VALUES (NEWID(), @tx, 1, 'FND-DUP-REF-1', 1, 50.00, 1, NEWID());
            """),
            ("dup_ref_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code)
                VALUES (NEWID(), @tx, 2, 'FND-DUP-REF-1', 2, 50.00, 1, 'PAYOS_SIM');
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["first_leg_ok"] == "OK"
    assert "UQ_tfs_FundingReference" in res["dup_ref_err"]


def test_tc_156_ea_leg_requires_wallet_and_no_provider_fields():
    """TC-156: Phần thanh toán EA (method=1) bắt buộc có wallet_id và không được có provider_code/provider_transaction_id (CK_tfs_MethodReferences)."""
    res = db.sql_check_steps(
        steps=[
            ("no_wallet_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id)
                VALUES (NEWID(), @tx, 1, 'FND-EA-1', 1, 50.00, 1, NULL);
            """),
            ("with_provider_code_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id, provider_code)
                VALUES (NEWID(), @tx, 1, 'FND-EA-2', 1, 50.00, 1, NEWID(), 'PAYOS_SIM');
            """),
            ("with_provider_tx_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id, provider_transaction_id)
                VALUES (NEWID(), @tx, 1, 'FND-EA-3', 1, 50.00, 1, NEWID(), 'PTX-1');
            """),
            ("valid_ea_ok", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id)
                VALUES (NEWID(), @tx, 1, 'FND-EA-OK', 1, 50.00, 1, NEWID());
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    for k in ("no_wallet_err", "with_provider_code_err", "with_provider_tx_err"):
        assert "CK_tfs_MethodReferences" in res[k], f"{k} phải bị chặn: {res[k]}"
    assert res["valid_ea_ok"] == "OK"


def test_tc_157_online_leg_requires_provider_and_no_wallet_fields():
    """TC-157: Phần thanh toán Online (method=2) bắt buộc có provider_code và không được có wallet_id hoặc EA tx IDs (CK_tfs_MethodReferences)."""
    res = db.sql_check_steps(
        steps=[
            ("no_provider_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code)
                VALUES (NEWID(), @tx, 1, 'FND-ONL-1', 2, 50.00, 1, NULL);
            """),
            ("with_wallet_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, wallet_id, provider_code)
                VALUES (NEWID(), @tx, 1, 'FND-ONL-2', 2, 50.00, 1, NEWID(), 'PAYOS_SIM');
            """),
            ("with_ea_tx_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code, education_account_transaction_id)
                VALUES (NEWID(), @tx, 1, 'FND-ONL-3', 2, 50.00, 1, 'PAYOS_SIM', NEWID());
            """),
            ("valid_online_ok", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code)
                VALUES (NEWID(), @tx, 1, 'FND-ONL-OK', 2, 50.00, 1, 'PAYOS_SIM');
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    for k in ("no_provider_err", "with_wallet_err", "with_ea_tx_err"):
        assert "CK_tfs_MethodReferences" in res[k], f"{k} phải bị chặn: {res[k]}"
    assert res["valid_online_ok"] == "OK"


def test_tc_158_external_transaction_ids_unique_across_funding_legs():
    """TC-158: Mỗi education_account_transaction_id, education_account_reversal_transaction_id và (provider_code, provider_transaction_id) chỉ dùng tối đa 1 lần."""
    res = db.sql_check_steps(
        steps=[
            ("setup_first_legs", """
                DECLARE @ea_tx varchar(50) = '11111111-2222-3333-4444-555555555555';
                DECLARE @ea_rev varchar(50) = '66666666-7777-8888-9999-aaaaaaaaaaaa';
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, wallet_id, completed_at, education_account_transaction_id)
                VALUES (NEWID(), @tx, 1, 'FND-158-1', 1, 40.00, 40.00, 2, NEWID(), SYSUTCDATETIME(), @ea_tx);
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, wallet_id, completed_at, education_account_transaction_id, education_account_reversal_transaction_id)
                VALUES (NEWID(), @tx, 2, 'FND-158-2', 1, 30.00, 0.00, 4, NEWID(), SYSUTCDATETIME(), NEWID(), @ea_rev);
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, provider_code, provider_transaction_id, completed_at)
                VALUES (NEWID(), @tx, 3, 'FND-158-3', 2, 30.00, 30.00, 2, 'PAYOS_SIM', 'PTX-DUP-158', SYSUTCDATETIME());
            """),
            ("dup_ea_tx_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, wallet_id, completed_at, education_account_transaction_id)
                VALUES (NEWID(), @tx, 4, 'FND-158-4', 1, 10.00, 10.00, 2, NEWID(), SYSUTCDATETIME(), '11111111-2222-3333-4444-555555555555');
            """),
            ("dup_ea_rev_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, wallet_id, completed_at, education_account_transaction_id, education_account_reversal_transaction_id)
                VALUES (NEWID(), @tx, 5, 'FND-158-5', 1, 10.00, 0.00, 4, NEWID(), SYSUTCDATETIME(), NEWID(), '66666666-7777-8888-9999-aaaaaaaaaaaa');
            """),
            ("dup_provider_tx_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, provider_code, provider_transaction_id, completed_at)
                VALUES (NEWID(), @tx, 6, 'FND-158-6', 2, 10.00, 10.00, 2, 'PAYOS_SIM', 'PTX-DUP-158', SYSUTCDATETIME());
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["setup_first_legs"] == "OK"
    assert "UX_tfs_EducationAccountTransaction" in res["dup_ea_tx_err"]
    assert "UX_tfs_EducationAccountReversal" in res["dup_ea_rev_err"]
    assert "UX_tfs_Provider_Transaction" in res["dup_provider_tx_err"]


def test_tc_159_funding_leg_settled_amount_bounds():
    """TC-159: Số tiền settled_amount trên phần thanh toán nằm trong [0, requested_amount] và requested_amount > 0."""
    res = db.sql_check_steps(
        steps=[
            ("req_zero_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code)
                VALUES (NEWID(), @tx, 1, 'FND-159-1', 2, 0.00, 1, 'PAYOS_SIM');
            """),
            ("settled_neg_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, provider_code, completed_at)
                VALUES (NEWID(), @tx, 1, 'FND-159-2', 2, 50.00, -1.00, 3, 'PAYOS_SIM', SYSUTCDATETIME());
            """),
            ("settled_gt_req_err", """
                INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount, status, provider_code, provider_transaction_id, completed_at)
                VALUES (NEWID(), @tx, 1, 'FND-159-3', 2, 50.00, 60.00, 2, 'PAYOS_SIM', 'PTX-159', SYSUTCDATETIME());
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert "CK_tfs_RequestedAmount" in res["req_zero_err"]
    assert "CK_tfs_SettledAmount" in res["settled_neg_err"] or "CK_tfs_StatusAmounts" in res["settled_neg_err"]
    assert "CK_tfs_SettledAmount" in res["settled_gt_req_err"] or "CK_tfs_StatusAmounts" in res["settled_gt_req_err"]


def test_tc_160_transaction_status_amounts_and_completed_at_rules():
    """TC-160: settled_amount và completed_at của giao dịch phải khớp với status (CK_transactions_StatusAmounts)."""
    res = db.sql_check_steps(
        steps=[
            ("pending_with_settled_err", "UPDATE dbo.transactions SET settled_amount = 50.00 WHERE id = @tx;"),
            ("succeeded_mismatch_err", "UPDATE dbo.transactions SET status = 2, settled_amount = 80.00, completed_at = SYSUTCDATETIME() WHERE id = @tx;"),
            ("failed_no_completed_err", "UPDATE dbo.transactions SET status = 3, completed_at = NULL WHERE id = @tx;"),
            ("recon_with_completed_err", "UPDATE dbo.transactions SET status = 5, completed_at = SYSUTCDATETIME() WHERE id = @tx;"),
            ("succeeded_valid_ok", "UPDATE dbo.transactions SET status = 2, settled_amount = 100.00, completed_at = SYSUTCDATETIME() WHERE id = @tx;"),
        ],
        setup_sql=SETUP_BASE,
    )
    for k in ("pending_with_settled_err", "succeeded_mismatch_err", "failed_no_completed_err", "recon_with_completed_err"):
        assert "CK_transactions_StatusAmounts" in res[k], f"{k} phải bị chặn: {res[k]}"
    assert res["succeeded_valid_ok"] == "OK"


def test_tc_161_currency_code_defaults_to_sgd():
    """TC-161: Cột currency_code mặc định là 'SGD' (3 ký tự in hoa) khi không truyền lúc tạo hóa đơn."""
    res = db.sql_check_steps(
        steps=[
            ("default_sgd_ok", """
                DECLARE @inv_def varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, gross_amount, subsidy_amount, net_amount, status)
                VALUES (@inv_def, @stu, @sch, 100.00, 0.00, 100.00, 1);
                IF (SELECT currency_code FROM dbo.invoices WHERE id = @inv_def) <> 'SGD'
                    THROW 50001, 'Default currency is not SGD', 1;
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["default_sgd_ok"] == "OK"


def test_tc_162_money_columns_store_two_decimal_places():
    """TC-162: Mọi cột tiền tệ trên invoices, invoice_items, transactions, transaction_funding_sources và student_charges đều có scale = 2."""
    rows = db.sql_rows("""
        SELECT t.name AS tbl, c.name AS col, c.scale
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        WHERE t.name IN ('invoices', 'invoice_items', 'transactions', 'transaction_funding_sources', 'student_charges')
          AND c.name IN ('gross_amount', 'subsidy_amount', 'net_amount', 'requested_amount', 'settled_amount', 'base_amount', 'tax_amount', 'total_amount')
    """)
    assert len(rows) >= 13
    for r in rows:
        assert r["scale"] == "2", f"Cột {r['tbl']}.{r['col']} có scale={r['scale']} khác 2"


def test_tc_168_invoice_number_unique_when_set():
    """TC-168: invoice_number là duy nhất khi có giá trị nhưng cho phép nhiều dòng NULL (UQ_invoices_InvoiceNumber)."""
    res = db.sql_check_steps(
        steps=[
            ("two_nulls_ok", """
                INSERT INTO dbo.invoices (id, student_id, school_id, invoice_number, gross_amount, subsidy_amount, net_amount, status)
                VALUES (NEWID(), @stu, @sch, NULL, 50.00, 0.00, 50.00, 1),
                       (NEWID(), @stu, @sch, NULL, 60.00, 0.00, 60.00, 1);
            """),
            ("first_num_ok", """
                INSERT INTO dbo.invoices (id, student_id, school_id, invoice_number, gross_amount, subsidy_amount, net_amount, status)
                VALUES (NEWID(), @stu, @sch, 'INV-QA-2026-0001', 50.00, 0.00, 50.00, 1);
            """),
            ("dup_num_err", """
                INSERT INTO dbo.invoices (id, student_id, school_id, invoice_number, gross_amount, subsidy_amount, net_amount, status)
                VALUES (NEWID(), @stu, @sch, 'INV-QA-2026-0001', 70.00, 0.00, 70.00, 1);
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert res["two_nulls_ok"] == "OK"
    assert res["first_num_ok"] == "OK"
    assert "UQ_invoices_InvoiceNumber" in res["dup_num_err"]


def test_tc_169_invoice_line_numbers_positive_and_unique_per_invoice():
    """TC-169: line_number trên hóa đơn phải > 0 và duy nhất trong cùng một hóa đơn."""
    res = db.sql_check_steps(
        steps=[
            ("line_zero_err", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 0, @chg1, 50.00, 0.00, 50.00);"),
            ("line_neg_err", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, -1, @chg1, 50.00, 0.00, 50.00);"),
            ("line_1_ok", "INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg1, 50.00, 0.00, 50.00);"),
            ("dup_line_1_err", """
                DECLARE @chg2 varchar(50) = (SELECT TOP 1 id FROM dbo.student_charges WHERE id <> @chg1);
                INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount) VALUES (NEWID(), @inv, 1, @chg2, 50.00, 0.00, 50.00);
            """),
        ],
        setup_sql=SETUP_BASE,
    )
    assert "CK_invoice_items_LineNumber" in res["line_zero_err"]
    assert "CK_invoice_items_LineNumber" in res["line_neg_err"]
    assert res["line_1_ok"] == "OK"
    assert "UQ_invoice_items_Invoice_Line" in res["dup_line_1_err"]


def test_tc_171_funding_sequence_numbers_positive_and_unique_per_transaction():
    """TC-171: sequence_number trên phần thanh toán phải > 0 và duy nhất trong cùng một giao dịch."""
    res = db.sql_check_steps(
        steps=[
            ("seq_zero_err", "INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code) VALUES (NEWID(), @tx, 0, 'FND-171-0', 2, 50.00, 1, 'PAYOS_SIM');"),
            ("seq_1_ok", "INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code) VALUES (NEWID(), @tx, 1, 'FND-171-1', 2, 50.00, 1, 'PAYOS_SIM');"),
            ("dup_seq_1_err", "INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, status, provider_code) VALUES (NEWID(), @tx, 1, 'FND-171-2', 2, 50.00, 1, 'PAYOS_SIM');"),
        ],
        setup_sql=SETUP_BASE,
    )
    assert "CK_tfs_SequenceNumber" in res["seq_zero_err"]
    assert res["seq_1_ok"] == "OK"
    assert "UQ_tfs_Transaction_Sequence" in res["dup_seq_1_err"]
