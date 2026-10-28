"""Truy vấn và kiểm tra ràng buộc SQL Server (edufams-qa-sqlserver) cùng helper tạo khoản phí tạm tự dọn dẹp và gửi webhook."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import hmac
import json
import subprocess
import time
import urllib.error
import urllib.request
import uuid

import os

# Tên DB đổi được bằng biến môi trường. Stack QA docker dùng BillingPaymentDatabase và EducationAccountDatabase;
# bản setup cũ của Dev dùng BillingPaymentService và EduAccount. Xem tên thật bằng: SELECT name FROM sys.databases.
BILLING_DB = os.environ.get("R9_BILLING_DB", "BillingPaymentDatabase")
EA_DB = os.environ.get("R9_EA_DB", "EducationAccountDatabase")
WEBHOOK_URL = "http://localhost:5008/api/v1/payment-webhooks/gateway"
WEBHOOK_SECRET = "whsec_f9_demo_shared_secret"


# Thứ tự ưu tiên: tên do biến môi trường ép, rồi tên của stack QA docker hiện hành (đúng DB mà service đang đọc),
# cuối cùng mới đến tên cũ. Máy có cả hai DB (bản cũ còn sót) phải ưu tiên bản *Database, nếu không test ghi vào DB mà service không đọc.
_DB_ALIASES = {
    BILLING_DB: ([os.environ["R9_BILLING_DB"]] if os.environ.get("R9_BILLING_DB") else []) + ["BillingPaymentDatabase", "BillingPaymentService"],
    EA_DB: ([os.environ["R9_EA_DB"]] if os.environ.get("R9_EA_DB") else []) + ["EducationAccountDatabase", "EduAccount"],
}
_existing_dbs: set[str] | None = None


def _real_db(db: str) -> str:
    """Đổi tên DB mặc định sang tên có thật trong container (một lần hỏi sys.databases cho cả phiên)."""
    global _existing_dbs
    if db not in _DB_ALIASES:
        return db
    if _existing_dbs is None:
        cmd = ["docker", "exec", "-i", "edufams-qa-sqlserver", "bash", "-c",
               '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -h -1 -W -Q "SET NOCOUNT ON; SELECT name FROM sys.databases"']
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        _existing_dbs = {line.strip() for line in (res.stdout or "").splitlines() if line.strip()}
    for name in _DB_ALIASES[db]:
        if name in _existing_dbs:
            return name
    return db


def sql_raw(query: str, db: str = BILLING_DB) -> tuple[int, str]:
    """Chạy câu lệnh SQL trong container edufams-qa-sqlserver qua stdin."""
    db = _real_db(db)
    cmd = [
        "docker", "exec", "-i", "edufams-qa-sqlserver", "bash", "-c",
        f'/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I -W -s "|" -d {db}',
    ]
    full_sql = "SET NOCOUNT ON;\n" + query
    res = subprocess.run(cmd, input=full_sql, capture_output=True, text=True, encoding="utf-8")
    out = (res.stdout or "").strip()
    err = (res.stderr or "").strip()
    return res.returncode, (out + ("\n" + err if err else "")).strip()


def sql_rows(query: str, db: str = BILLING_DB) -> list[dict[str, str]]:
    """Chạy SELECT và trả danh sách dict theo tên cột."""
    code, out = sql_raw(query, db=db)
    if code != 0:
        raise RuntimeError(f"SQL lỗi ({db}): {out}")
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if len(lines) < 2:
        return []
    headers = [h.strip() for h in lines[0].split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        if line.startswith("(") and line.endswith("rows affected)"):
            continue
        vals = [v.strip() for v in line.split("|")]
        if len(vals) == len(headers):
            rows.append(dict(zip(headers, vals)))
    return rows


def sql_scalar(query: str, db: str = BILLING_DB) -> str:
    code, out = sql_raw(query, db=db)
    if code != 0:
        raise RuntimeError(f"SQL lỗi ({db}): {out}")
    lines = [line.strip() for line in out.splitlines() if line.strip() and not (line.strip().startswith("(") and line.strip().endswith("rows affected)"))]
    if not lines:
        return ""
    if lines[0].startswith("-") and len(lines) >= 2:
        return lines[1].split("|")[0].strip()
    if len(lines) >= 3:
        return lines[2].split("|")[0].strip()
    return ""


def get_tx_bundle(transaction_id: str) -> dict:
    """Lấy thông tin transaction, invoice và danh sách funding legs từ BillingPaymentService DB."""
    tx_rows = sql_rows(f"""
        SELECT id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key,
               requested_amount, settled_amount, currency_code, status, created_at, completed_at
        FROM dbo.transactions WHERE id = '{transaction_id}'
    """, db=BILLING_DB)
    tx = tx_rows[0] if tx_rows else {}
    inv = {}
    if tx.get("invoice_id"):
        inv_rows = sql_rows(f"""
            SELECT id, student_id, school_id, invoice_number, currency_code,
                   gross_amount, subsidy_amount, net_amount, status, issued_at, due_date, paid_at
            FROM dbo.invoices WHERE id = '{tx["invoice_id"]}'
        """, db=BILLING_DB)
        inv = inv_rows[0] if inv_rows else {}
    legs = sql_rows(f"""
        SELECT id, transaction_id, sequence_number, funding_reference, method,
               requested_amount, settled_amount, status, wallet_id, provider_code,
               provider_transaction_id, failure_code, failure_reason,
               education_account_transaction_id, education_account_reversal_transaction_id
        FROM dbo.transaction_funding_sources
        WHERE transaction_id = '{transaction_id}'
        ORDER BY sequence_number ASC
    """, db=BILLING_DB)
    return {"tx": tx, "invoice": inv, "legs": legs}


def sql_check_steps(steps: list[tuple[str, str]], setup_sql: str = "", db: str = BILLING_DB) -> dict[str, str]:
    """Chạy nhiều bước SQL trong cùng một giao dịch rồi ROLLBACK hoàn toàn để không làm bẩn dữ liệu.
    Mỗi phần tử trong steps là (nhãn, câu SQL). Trả dict {nhãn: 'OK' hoặc 'ERR:mã:thông điệp'}."""
    blocks = ["BEGIN TRAN;", setup_sql]
    for label, stmt in steps:
        blocks.append(f"""
BEGIN TRY
    {stmt}
    SELECT '{label}' AS step_label, 'OK' AS step_result;
END TRY
BEGIN CATCH
    SELECT '{label}' AS step_label, CONCAT('ERR:', ERROR_NUMBER(), ':', ERROR_MESSAGE()) AS step_result;
END CATCH;
""")
    blocks.append("IF @@TRANCOUNT > 0 ROLLBACK TRAN;")
    code, out = sql_raw("\n".join(blocks), db=db)
    results: dict[str, str] = {}
    for line in out.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 2 and parts[0] != "step_label" and not parts[0].startswith("-"):
            results[parts[0]] = parts[1]
    return results


@contextmanager
def temp_charges(student_id: str | None = None, amounts: list[float] | None = None,
                 balance: float | None = None, wallet_status: int | str | None = None,
                 charge_status: str = "POSTED"):
    """Tạo một hoặc nhiều khoản phí tạm thời trong DB, tùy chọn đặt lại số dư/trạng thái ví,
    và tự động dọn sạch mọi invoice/transaction/webhook/khoản phí tạm cùng khôi phục ví trong finally."""
    if amounts is None:
        amounts = [50.00]
    # Không truyền student_id thì dùng con "sandbox" riêng của seed R9 (R9-STU-14, thuộc persona, ví 1000.00, không khoản phí),
    # để khoản phí tạm không lẫn với con mà các test khác đang dùng. Không có thì lấy học sinh của khoản phí đầu tiên.
    if not student_id:
        sandbox = os.environ.get("R9_SANDBOX_STUDENT", "R9-STU-14")
        if sql_rows(f"SELECT id FROM dbo.students WHERE id = '{sandbox}'", db=EA_DB):
            student_id = sandbox
    where = f"WHERE student_id = '{student_id}'" if student_id else ""
    tpl_rows = sql_rows(f"""
        SELECT TOP 1 student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
               school_class_id, student_category_snapshot, fee_component_id, fee_component_name_snapshot
        FROM dbo.student_charges {where}
    """, db=BILLING_DB)
    if not tpl_rows:
        tpl_rows = sql_rows("""
            SELECT TOP 1 student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
                   school_class_id, student_category_snapshot, fee_component_id, fee_component_name_snapshot
            FROM dbo.student_charges
        """, db=BILLING_DB)
    tpl = tpl_rows[0]
    stu_id = student_id or tpl["student_id"]

    wallet_rows = sql_rows(f"""
        SELECT TOP 1 id, balance, status, CONVERT(varchar(33), SYSUTCDATETIME(), 126) AS now_utc
        FROM dbo.wallets WHERE student_id = '{stu_id}'
    """, db=EA_DB)
    orig_wallet = wallet_rows[0] if wallet_rows else None

    charge_ids = [str(uuid.uuid4()) for _ in amounts]
    try:
        if orig_wallet and (balance is not None or wallet_status is not None):
            new_bal = balance if balance is not None else float(orig_wallet["balance"])
            if wallet_status is None:
                new_st = int(orig_wallet["status"])
            elif isinstance(wallet_status, str):
                names = {"active": 1, "inactive": 2, "suspended": 3, "closed": 4}  # WalletStatus của Education Account
                new_st = names[wallet_status.lower()] if wallet_status.lower() in names else int(wallet_status)
            else:
                new_st = int(wallet_status)
            sql_raw(f"""
                UPDATE dbo.wallets
                SET balance = {new_bal:.2f}, status = {new_st}
                WHERE id = '{orig_wallet["id"]}';
            """, db=EA_DB)

        inserts = []
        for idx, (cid, amt) in enumerate(zip(charge_ids, amounts), start=1):
            sc_class = "NULL" if tpl["school_class_id"] in ("NULL", "") else f"'{tpl['school_class_id']}'"
            comp_name = tpl["fee_component_name_snapshot"].replace("'", "''")
            inserts.append(f"""
                INSERT INTO dbo.student_charges (
                    id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
                    school_class_id, student_category_snapshot, fee_component_id, fee_component_name_snapshot,
                    pricing_date, period_start, period_end_exclusive, charge_date, due_date,
                    base_amount, tax_amount, total_amount, currency_code, status, posted_at, idempotency_key
                ) VALUES (
                    '{cid}', '{stu_id}', '{tpl["enrollment_id"]}', '{tpl["school_id"]}',
                    '{tpl["academic_year_id"]}', '{tpl["academic_level_id"]}', {sc_class},
                    '{tpl["student_category_snapshot"]}', '{tpl["fee_component_id"]}', N'{comp_name} QA {idx}',
                    '2026-10-01', '2026-10-01', '2026-12-31', '2026-10-01', '2026-12-0{min(idx, 9)}',
                    {amt:.2f}, 0.00, {amt:.2f}, 'SGD', '{charge_status}', SYSUTCDATETIME(), 'qa-temp-{cid}'
                );
            """)
        code, out = sql_raw("\n".join(inserts), db=BILLING_DB)
        if code != 0:
            raise RuntimeError(f"Không tạo được khoản phí tạm: {out}")

        yield stu_id, charge_ids
    finally:
        id_list = ", ".join(f"'{c}'" for c in charge_ids)
        cleanup_sql = f"""
            DECLARE @inv TABLE (id varchar(50));
            INSERT INTO @inv SELECT DISTINCT invoice_id FROM dbo.invoice_items WHERE student_charge_id IN ({id_list});
            DECLARE @tx TABLE (id varchar(50));
            INSERT INTO @tx SELECT id FROM dbo.transactions WHERE invoice_id IN (SELECT id FROM @inv);
            DECLARE @leg TABLE (id varchar(50), ref nvarchar(128));
            INSERT INTO @leg SELECT id, funding_reference FROM dbo.transaction_funding_sources WHERE transaction_id IN (SELECT id FROM @tx);

            DELETE FROM dbo.payment_webhook_receipts WHERE funding_transaction_id IN (SELECT id FROM @leg) OR funding_reference IN (SELECT ref FROM @leg);
            DELETE FROM dbo.checkout_payment_sagas WHERE transaction_id IN (SELECT id FROM @tx) OR invoice_id IN (SELECT id FROM @inv);
            DELETE FROM dbo.transaction_funding_sources WHERE transaction_id IN (SELECT id FROM @tx);
            DELETE FROM dbo.transactions WHERE id IN (SELECT id FROM @tx);
            DELETE FROM dbo.invoice_items WHERE invoice_id IN (SELECT id FROM @inv) OR student_charge_id IN ({id_list});
            DELETE FROM dbo.invoices WHERE id IN (SELECT id FROM @inv);
            DELETE FROM dbo.student_charges WHERE id IN ({id_list});
        """
        sql_raw(cleanup_sql, db=BILLING_DB)
        if orig_wallet:
            sql_raw(f"""
                DELETE FROM dbo.wallet_transactions
                WHERE wallet_id = '{orig_wallet["id"]}' AND created_at >= '{orig_wallet["now_utc"]}';
                UPDATE dbo.wallets
                SET balance = {float(orig_wallet["balance"]):.2f}, status = {int(orig_wallet["status"])}
                WHERE id = '{orig_wallet["id"]}';
            """, db=EA_DB)


def reseed() -> tuple[bool, str]:
    """Dọn rồi nạp lại dữ liệu seed R9 (như reseed_r9.cmd): đưa mọi con R9 về trạng thái ban đầu. Trả (thành công, ghi chú)."""
    tools = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")
    cmd = ["docker", "exec", "-i", "edufams-qa-sqlserver", "bash", "-c",
           '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I']
    for name in ("seed_r9_cleanup.sql", "seed_r9_data.sql"):
        with open(os.path.join(tools, name), "rb") as fh:
            res = subprocess.run(cmd, input=fh.read(), capture_output=True)
        if res.returncode != 0:
            return False, f"{name}: {(res.stdout or b'').decode('utf-8', 'replace')[-300:]}"
    return True, "ok"


def ensure_split_state(student_id: str, balance: float = 20.00, amounts: tuple[float, ...] = (40.00, 30.00)) -> bool:
    """Đưa con về trạng thái chia khoản: ví còn tiền nhưng ít hơn tổng khoản chưa trả. Trả True nếu đã chỉnh.

    Các test Both (F9.3, F9.5, F9.9) rút cạn ví của cùng một con nên test chạy sau thấy ví 0.00 và nợ 0.00 rồi bị bỏ qua.
    Hàm này đọc lại trạng thái thật trong DB trước mỗi test chia khoản: nếu còn đúng thì không đụng gì, nếu không thì đặt ví về
    `balance` và thêm khoản phí mã R9-CHG-TOPUP-*. Các dòng này thuộc tiền tố R9 nên tools/seed_r9_cleanup.sql dọn được.
    Không có Docker hoặc DB thì bỏ qua im lặng (test tự bỏ qua theo kiểm tra trên màn).
    """
    try:
        wallet = sql_rows(f"SELECT TOP 1 id, balance FROM dbo.wallets WHERE student_id = '{student_id}'", db=EA_DB)
        if not wallet:
            return False
        owed = sql_scalar(f"""SELECT COALESCE(SUM(sc.total_amount), 0) FROM dbo.student_charges sc
                              WHERE sc.student_id = '{student_id}' AND sc.status = 'POSTED'
                                AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items ii WHERE ii.student_charge_id = sc.id)""", db=BILLING_DB)
        now_balance, owed_total = float(wallet[0]["balance"]), float(owed or 0)
        if 0 < now_balance < owed_total:
            return False
        sql_raw(f"UPDATE dbo.wallets SET balance = {balance:.2f}, status = 1 WHERE id = '{wallet[0]['id']}';", db=EA_DB)
        if balance < owed_total:
            return True
        tpl = sql_rows(f"""SELECT TOP 1 enrollment_id, school_id, academic_year_id, academic_level_id, school_class_id,
                                  student_category_snapshot, fee_component_id, fee_component_name_snapshot
                           FROM dbo.student_charges WHERE student_id = '{student_id}'""", db=BILLING_DB)
        if not tpl:
            return True
        t = tpl[0]
        sc_class = "NULL" if t["school_class_id"] in ("NULL", "") else f"'{t['school_class_id']}'"
        name = t["fee_component_name_snapshot"].replace("'", "''")
        inserts = []
        for idx, amt in enumerate(amounts, start=1):
            cid = f"R9-CHG-TOPUP-{uuid.uuid4().hex[:8]}"
            inserts.append(f"""INSERT INTO dbo.student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
                school_class_id, student_category_snapshot, fee_component_id, fee_component_name_snapshot, pricing_date, period_start,
                period_end_exclusive, charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at, idempotency_key)
                VALUES ('{cid}', '{student_id}', '{t["enrollment_id"]}', '{t["school_id"]}', '{t["academic_year_id"]}', '{t["academic_level_id"]}',
                {sc_class}, '{t["student_category_snapshot"]}', '{t["fee_component_id"]}', N'{name} TOPUP {idx}', '2026-10-01', '2026-10-01',
                '2026-12-31', '2026-10-01', '2026-12-0{min(idx, 9)}', {amt:.2f}, 0.00, {amt:.2f}, 'SGD', 'POSTED', SYSUTCDATETIME(), 'qa-topup-{cid}');""")
        sql_raw("\n".join(inserts), db=BILLING_DB)
        return True
    except Exception:  # noqa: BLE001  không có Docker: để test tự quyết định bỏ qua
        return False


def get_webhook_receipt(event_id: str) -> dict[str, str]:
    rows = sql_rows(f"""
        SELECT id, funding_transaction_id, provider_code, provider_event_id, provider_transaction_id,
               funding_reference, event_type, CONVERT(varchar(66), payload_hash, 2) AS payload_hash_hex,
               processing_status, received_at, processed_at, error_message
        FROM dbo.payment_webhook_receipts
        WHERE provider_event_id = '{event_id}'
    """, db=BILLING_DB)
    return rows[0] if rows else {}


def delete_webhook_receipt(event_id: str) -> None:
    sql_raw(f"DELETE FROM dbo.payment_webhook_receipts WHERE provider_event_id = '{event_id}';", db=BILLING_DB)


def sign_webhook(timestamp: int, raw_body: str, secret: str = WEBHOOK_SECRET) -> str:
    digest = hmac.new(secret.encode("utf-8"), f"{timestamp}.{raw_body}".encode("utf-8"), hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest.lower()}"


def post_webhook(
    reference_id: str,
    *,
    event_type: str = "payment.succeeded",
    amount_cents: int = 5000,
    currency: str = "SGD",
    event_id: str | None = None,
    provider_code: str = "PAYOS_SIM",
    provider_tx_id: str | None = None,
    metadata: dict[str, str] | None = None,
    signature: str | None = "AUTO",
    timestamp: int | None = None,
    raw_body_override: str | None = None,
) -> tuple[int, dict, str]:
    """Gửi POST tới webhook cổng thanh toán và trả (status_code, json_body, event_id)."""
    ev_id = event_id or f"EVT-QA-{uuid.uuid4().hex[:12]}"
    ptx_id = provider_tx_id or f"PTX-QA-{uuid.uuid4().hex[:12]}"
    ts = timestamp if timestamp is not None else int(time.time())
    payload = {
        "eventId": ev_id,
        "eventType": event_type,
        "providerCode": provider_code,
        "transactionId": ptx_id,
        "referenceId": reference_id,
        "amountCents": amount_cents,
        "currency": currency,
        "status": "Succeeded" if event_type == "payment.succeeded" else "Failed",
        "occurredAtUtc": "2026-10-22T03:00:00Z",
        "metadata": metadata or {},
    }
    raw_body = raw_body_override if raw_body_override is not None else json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    if signature == "AUTO":
        headers["X-Gateway-Signature"] = sign_webhook(ts, raw_body)
    elif signature is not None:
        headers["X-Gateway-Signature"] = signature

    req = urllib.request.Request(WEBHOOK_URL, data=raw_body.encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body_text = resp.read().decode("utf-8")
            return resp.status, (json.loads(body_text) if body_text else {}), ev_id
    except urllib.error.HTTPError as err:
        body_text = err.read().decode("utf-8")
        try:
            parsed = json.loads(body_text)
        except Exception:  # noqa: BLE001
            parsed = {"raw": body_text}
        return err.code, parsed, ev_id
