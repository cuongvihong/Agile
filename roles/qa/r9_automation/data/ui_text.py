"""Chuỗi cố định của UI e-service (tiếng Anh), lấy từ packages/i18n/src/resources.ts, mục features.billingPayment."""
from __future__ import annotations

# Trang chọn tài khoản /billing
H_ACCOUNTS = "Choose an education account"
LIST_ACCOUNTS = "Education accounts"
ACCOUNTS_ERROR = "Unable to load education accounts"
ACCOUNTS_EMPTY = "No education accounts"
ACCOUNTS_EMPTY_DESC = "No education accounts are linked to your profile."
RETRY = "Try again"

# Trang /billing/:studentId
H_PAY = "Pay education charges"
H_CHARGES = "Outstanding charges"
H_SUMMARY = "Payment summary"
H_REVIEW = "Review payment"
H_REVIEW_AUTH = "Review & authorize"
CARD_OUTSTANDING = "Outstanding fees"
CARD_BALANCE = "Education Account balance"
CARD_CHILD = "Child"
SELECT_ALL = "Select all outstanding fees"
SELECT_CHARGE = "Select charge: {description}"
EMPTY_CHARGES = "No outstanding charges"
EMPTY_CHARGES_DESC = "There are no outstanding charges for this child."
TABLE_HEADERS = ["Select", "Description", "Gross amount", "Subsidy", "Amount due", "Status"]
TABLE_HEADERS_V3 = ["Select", "Charge name", "Gross amount", "Subsidy", "Subsidy reason", "Amount due", "Status", "Details"]
SPLIT_LABEL = "Payment split"
SELECTED_LIST = "Selected charges"
TOTAL_TO_PAY = "Total to pay"
INVALID_CONTEXT = "Payment context is invalid"
WALLET_ERROR = "Unable to load education account"
STALE_TITLE = "The selected fees are no longer available"
CHECKOUT_ERROR_TITLE = "Check your payment details"
INVALID_URL_TITLE = "Unable to open online payment"
BACK_TO_ACCOUNTS = "Back to education accounts"

METHOD_EA = "EducationAccount"
METHOD_ONLINE = "OnlineGateway"
METHOD_BOTH = "Both"
METHOD_LABEL = {METHOD_EA: "Education Account", METHOD_ONLINE: "Online Gateway", METHOD_BOTH: "Both"}

# Trang /payment-result
H_RESULT = "Payment result"
RESULT_SUCCEEDED = "Payment successful"
RESULT_FAILED = "Payment failed"
RESULT_CANCELLED = "Payment cancelled"
RESULT_PENDING = "Payment is being processed"
RESULT_REVIEW = "Payment needs review"
RESULT_MISSING = "The transaction reference is missing."
RESULT_INVALID = "The transaction reference is invalid."
EA_REVERSED = "The Education Account payment was reversed."
EA_MAY_BE_DEDUCTED = "Your Education Account may still have been deducted."
PRINT = "Print receipt"
HOME = "Back to home"

# Trang giả lập cổng thanh toán
SIM_PAY_OK = "Pay successful"
SIM_PAY_FAIL = "Pay failed"
SIM_HEADING = "Review your payment"
