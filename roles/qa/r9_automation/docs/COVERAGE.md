# Độ phủ của R9_Test_Cases_final_FS09.xlsx

Số case trong sổ: 187. Đã tự động hóa: 185. Chưa tự động hóa: 2.

Một case tính là đã tự động hóa khi có ít nhất một test chạy được cho nó, kể cả test nhãn `known_defect` (kỳ vọng thất bại vì bản build lệch với R9),
`mocked` (giả phản hồi), `mutating` (ghi dữ liệu thật) và `draft` (phụ thuộc giả định). Xem README để biết ý nghĩa từng nhãn.

| Suite | Số case | Đã tự động hóa | Chưa |
|---|---|---|---|
| F9.1 Access and child list | 24 | 23 | 1 |
| F9.2 Outstanding invoices and EA balance | 24 | 24 | 0 |
| F9.3 Payment method and eligibility | 31 | 31 | 0 |
| F9.4 Pay with Education Account | 14 | 14 | 0 |
| F9.4 and F9.5 Idempotency and concurrency | 12 | 12 | 0 |
| F9.5 Pay online | 9 | 9 | 0 |
| F9.4 and F9.5 Split payment | 14 | 14 | 0 |
| F9.6 Webhook and reconciliation | 13 | 12 | 1 |
| F9.7 Result, receipt and retry | 23 | 23 | 0 |
| Data rules and constraints | 23 | 23 | 0 |

## Case đã tự động hóa

| Case | Tiêu đề | Test |
|---|---|---|
| TC-001 | Parent signs in with Singpass and reaches the child list | test_f91_access_and_child_list.py::test_tc_001_sign_in_with_singpass_reaches_child_list |
| TC-002 | Failed Singpass sign in creates no session | test_f91_access_and_child_list.py::test_tc_002_failed_singpass_sign_in_does_not_create_session |
| TC-003 | Cancelled Singpass sign in creates no session | test_f91_access_and_child_list.py::test_tc_003_cancelled_singpass_sign_in_returns_without_session |
| TC-004 | Child list shows name, school, level, class and outstanding label | test_f91_access_and_child_list.py::test_tc_004_tc_005_child_card_shows_school_level_class_and_outstanding_label |
| TC-005 | Label shows no outstanding invoices for a child without any | test_f91_access_and_child_list.py::test_tc_004_tc_005_child_card_shows_school_level_class_and_outstanding_label |
| TC-006 | Child list contains only the children linked to the Parent | test_f91_access_and_child_list.py::test_tc_006_child_list_contains_only_linked_children |
| TC-007 | Parent without any linked child sees the empty state | test_f91_access_and_child_list.py::test_tc_007_parent_without_linked_child_sees_empty_state |
| TC-008 | Parent with one child reaches that child | test_f91_access_and_child_list.py::test_tc_008_parent_with_one_child_sees_only_that_child |
| TC-009 | Second guardian linked to the same child sees the same child and invoices | test_f91_access_and_child_list.py::test_tc_009_second_guardian_of_same_child_can_view_and_start_payment |
| TC-010 | System error while loading the child list shows a safe message | test_f91_access_and_child_list.py::test_tc_010_system_error_on_child_list_shows_safe_message_and_retry |
| TC-011 | Changing the student ID in the address is refused | test_f91_access_and_child_list.py::test_tc_011_invalid_student_id_in_address_is_refused |
| TC-012 | API call for the invoices of an unlinked student is refused | test_f91_access_and_child_list.py::test_tc_012_api_for_charges_of_unlinked_student_is_refused |
| TC-013 | API call to read an invoice of another family is refused | test_f91_access_and_child_list.py::test_tc_013_api_for_invoice_of_another_family_is_refused |
| TC-014 | API call to pay an invoice of another family is refused and nothing is debited | test_f91_access_and_child_list.py::test_tc_014_api_to_pay_for_unlinked_student_is_refused |
| TC-015 | API call for the status or receipt of another family's payment is refused | test_f91_access_and_child_list.py::test_tc_015_api_for_transaction_of_another_family_is_refused |
| TC-016 | A guardian cannot open a child who is linked only to another Parent | test_f91_access_and_child_list.py::test_tc_016_changing_student_id_in_address_to_another_child_shows_access_denied |
| TC-017 | Request without a session is sent to the sign in | test_f91_access_and_child_list.py::test_tc_017_request_without_session_is_sent_to_sign_in<br>test_f91_access_and_child_list.py::test_tc_017_protected_api_rejects_call_without_session |
| TC-018 | Open invoices of the chosen child are listed with number, due date, status and amount | test_f92_outstanding_and_balance.py::test_tc_018_open_charges_are_listed_with_description_due_date_and_amounts |
| TC-019 | An invoice opens to its lines grouped by fee type with fee components and GST | test_f92_outstanding_and_balance.py::test_tc_019_invoice_lines_grouped_by_fee_type_and_show_gst |
| TC-020 | Invoice totals show Gross, Subsidy 0.00 and Net equal to Gross | test_f92_outstanding_and_balance.py::test_tc_020_gross_subsidy_zero_and_net_equal_gross |
| TC-021 | Amounts are shown in SGD with two decimals | test_f92_outstanding_and_balance.py::test_tc_021_amounts_are_in_sgd_with_two_decimals |
| TC-022 | Invoice due date is the earliest due date of its lines | test_f92_outstanding_and_balance.py::test_tc_022_invoice_with_several_lines_shows_sum_and_earliest_due_date |
| TC-023 | Switching to another child changes the invoice list | test_f92_outstanding_and_balance.py::test_tc_023_switching_to_another_child_changes_the_charge_list |
| TC-024 | Paid, Cancelled and Draft invoices are not in the list | test_f92_outstanding_and_balance.py::test_tc_024_paid_cancelled_and_draft_items_not_shown_in_open_list |
| TC-025 | An invoice waiting for payment is shown as Pending and cannot be selected | test_f92_outstanding_and_balance.py::test_tc_025_payment_pending_item_shown_as_pending_and_disabled |
| TC-027 | Demo data is labelled as sample data | test_f92_outstanding_and_balance.py::test_tc_027_sample_data_notice_is_visible_on_fees_and_balance_screen |
| TC-028 | A child with an Active EA shows balance and status | test_f92_outstanding_and_balance.py::test_tc_028_active_account_shows_balance_and_status |
| TC-029 | A child without an EA shows no balance and a note | test_f92_outstanding_and_balance.py::test_tc_029_child_without_education_account_shows_a_note_instead_of_balance |
| TC-030 | A child with a Closed EA shows the status Closed | test_f92_outstanding_and_balance.py::test_tc_030_closed_education_account_shows_status_closed |
| TC-031 | A zero EA balance is shown as 0.00 | test_f92_outstanding_and_balance.py::test_tc_031_zero_balance_is_shown_as_0_00 |
| TC-032 | A child with no Issued invoice shows the empty state | test_f92_outstanding_and_balance.py::test_tc_032_child_without_charges_shows_empty_state_and_no_payment_option<br>test_f92_outstanding_and_balance.py::test_tc_032_real_child_without_charges_shows_empty_state_and_no_payment_option<br>test_f92_outstanding_and_balance.py::test_tc_032_tc_033_real_empty_state_links_back_to_child_list<br>test_f92_outstanding_and_balance.py::test_tc_032_tc_033_empty_state_links_back_to_child_list |
| TC-033 | The empty state links back to the child list and another child can be chosen | test_f92_outstanding_and_balance.py::test_tc_032_tc_033_real_empty_state_links_back_to_child_list<br>test_f92_outstanding_and_balance.py::test_tc_032_tc_033_empty_state_links_back_to_child_list |
| TC-034 | A child whose only open invoice is waiting for payment is not shown the empty state | test_f92_outstanding_and_balance.py::test_tc_034_child_with_only_payment_pending_invoice_does_not_see_empty_state |
| TC-035 | Selecting an Issued invoice opens the payment method screen with its summary | test_f93_method_and_eligibility.py::test_tc_035_selecting_a_charge_opens_method_screen_with_its_summary |
| TC-036 | Only one whole invoice can be selected and lines cannot be paid separately | test_f93_method_and_eligibility.py::test_tc_036_several_charges_can_be_selected_for_one_payment |
| TC-038 | Student without an EA can pay online only | test_f93_method_and_eligibility.py::test_tc_038_student_without_education_account_can_still_pay_online |
| TC-039 | Student with a Closed EA can pay online only | test_f93_method_and_eligibility.py::test_tc_039_closed_education_account_cannot_be_used_for_payment |
| TC-040 | Active EA with zero balance offers online payment only | test_f93_method_and_eligibility.py::test_tc_040_zero_balance_offers_online_payment_only<br>test_f93_method_and_eligibility.py::test_tc_040_zero_balance_offers_online_payment_only_simulated_wallet |
| TC-041 | Balance below the amount to pay disables EA and suggests split | test_f93_method_and_eligibility.py::test_tc_041_tc_046_low_balance_shows_reason_to_pay_the_rest_online<br>test_f93_method_and_eligibility.py::test_tc_041_balance_below_amount_disables_education_account_and_offers_both |
| TC-042 | Balance equal to the amount to pay allows EA and online but not split | test_f93_method_and_eligibility.py::test_tc_042_balance_equal_to_amount_allows_education_account_and_online_but_not_both |
| TC-043 | Balance above the amount to pay allows EA and online but not split | test_f93_method_and_eligibility.py::test_tc_043_balance_above_amount_allows_education_account_and_online_but_not_both |
| TC-045 | The EA is suggested when the balance is enough but nothing is debited until the Parent confirms | test_f93_method_and_eligibility.py::test_tc_045_education_account_is_suggested_but_nothing_is_debited_before_confirm |
| TC-046 | Selecting EA with a low balance is refused with the reason and nothing changes | test_f93_method_and_eligibility.py::test_tc_041_tc_046_low_balance_shows_reason_to_pay_the_rest_online<br>test_f93_method_and_eligibility.py::test_tc_046_education_account_cannot_be_chosen_when_balance_is_low |
| TC-047 | API refuses the EA method when the balance is too low | test_f93_method_and_eligibility.py::test_tc_047_api_refuses_education_account_method_when_balance_is_too_low |
| TC-048 | API refuses EA and split for a student without an EA | test_f93_method_and_eligibility.py::test_tc_048_api_refuses_ea_and_both_when_student_has_no_education_account |
| TC-049 | API refuses EA and split when the EA is Closed | test_f93_method_and_eligibility.py::test_tc_049_api_refuses_ea_and_both_when_education_account_is_closed |
| TC-050 | Default split proposes the whole balance as the EA part and calculates the online part | test_f93_method_and_eligibility.py::test_tc_050_default_both_proposes_whole_balance_as_education_account_part |
| TC-051 | The Parent can lower the EA part and the online part updates | test_f93_method_and_eligibility.py::test_tc_051_parent_can_lower_the_education_account_part |
| TC-052 | The online part cannot be typed by the Parent | test_f93_method_and_eligibility.py::test_tc_052_online_part_cannot_be_typed |
| TC-053 | An EA part of zero is refused and the Parent stays on the screen | test_f93_method_and_eligibility.py::test_tc_053_in_both_setting_ea_part_to_zero_is_refused |
| TC-054 | API refuses a split with an online part of zero | test_f93_method_and_eligibility.py::test_tc_054_in_both_online_part_of_zero_is_refused |
| TC-055 | API refuses a split whose parts add up to less than the amount to pay | test_f93_method_and_eligibility.py::test_tc_055_api_refuses_both_when_two_parts_add_up_to_less_than_invoice |
| TC-056 | API refuses a split whose parts add up to more than the amount to pay | test_f93_method_and_eligibility.py::test_tc_056_api_refuses_both_when_two_parts_add_up_to_more_than_invoice |
| TC-057 | API refuses an EA part above the available balance | test_f93_method_and_eligibility.py::test_tc_057_setting_ea_part_above_balance_is_refused |
| TC-058 | API refuses a negative EA part | test_f93_method_and_eligibility.py::test_tc_058_api_refuses_negative_amount_on_payment_part |
| TC-062 | A very small EA part is accepted because the EA part has no minimum | test_f93_method_and_eligibility.py::test_tc_062_lowering_ea_part_to_0_01_in_both_is_accepted |
| TC-063 | Review screen for an EA payment shows the amounts and the balance after payment | test_f93_method_and_eligibility.py::test_tc_063_review_screen_shows_balance_after_payment<br>test_f93_method_and_eligibility.py::test_tc_063_review_screen_of_education_account_payment_debits_nothing |
| TC-065 | Paying a 27.25 invoice with the EA debits the balance once and marks the invoice Paid | test_f94_pay_with_ea.py::test_tc_065_tc_070_tc_129_pay_one_charge_with_education_account_end_to_end<br>test_f94_pay_with_ea.py::test_tc_065_tc_070_pay_invoice_in_full_with_ea_when_balance_greater_self_cleaning |
| TC-066 | Status changes of an EA payment follow Appendix A and are written to the audit log | test_f94_pay_with_ea.py::test_tc_066_pay_invoice_in_full_with_ea_when_balance_equals_invoice |
| TC-067 | Paying a two line invoice of 22.23 (Gross 47.23 less the FAS subsidy 25.00) debits the full Net amount | test_f94_pay_with_ea.py::test_tc_067_two_charges_in_one_payment_create_one_invoice_with_two_lines<br>test_f94_pay_with_ea.py::test_tc_067_two_charges_in_one_payment_create_one_invoice_with_two_lines_self_cleaning |
| TC-068 | Balance equal to the amount to pay is paid and the balance becomes 0.00 | test_f94_pay_with_ea.py::test_tc_068_paying_one_of_two_open_charges_leaves_the_other_open |
| TC-070 | After an EA payment the list shows the new balance and no longer shows the invoice | test_f94_pay_with_ea.py::test_tc_065_tc_070_tc_129_pay_one_charge_with_education_account_end_to_end<br>test_f94_pay_with_ea.py::test_tc_065_tc_070_pay_invoice_in_full_with_ea_when_balance_greater_self_cleaning |
| TC-071 | Balance falling below the amount before confirm fails the EA leg and changes nothing | test_f94_pay_with_ea.py::test_tc_071_audit_entry_written_when_ea_payment_succeeds |
| TC-072 | Function 1 error during the debit fails the payment and the invoice is not Paid | test_f94_pay_with_ea.py::test_tc_072_when_ea_service_rejects_deduction_nothing_is_charged |
| TC-073 | Unclear debit result with Function 1 confirming nothing was debited fails the leg | test_f94_pay_with_ea.py::test_tc_073_when_ea_service_unreachable_payment_shows_safe_message |
| TC-074 | Unclear debit result with Function 1 confirming the debit leads to a reversal | test_f94_pay_with_ea.py::test_tc_074_if_saving_payment_fails_after_ea_deducted_deduction_is_reversed |
| TC-075 | Unclear debit result that stays unclear moves to ReconciliationRequired | test_f94_pay_with_ea.py::test_tc_075_if_ea_reversal_also_fails_payment_marked_for_manual_review |
| TC-076 | Function 1 treats the same FundingReference as one debit | test_f94_pay_with_ea.py::test_tc_076_audit_entry_written_when_ea_deduction_is_reversed |
| TC-077 | Double click on Confirm creates one transaction and debits once | test_f94_pay_with_ea.py::test_tc_077_double_click_on_authorize_sends_one_checkout_request<br>test_f94_pay_with_ea.py::test_tc_077_double_click_confirm_sends_one_request_self_cleaning |
| TC-078 | The same request sent again with the same key returns the first result | test_f94_pay_with_ea.py::test_tc_078_tc_080_same_idempotency_key_returns_first_result_and_pays_once<br>test_f94_pay_with_ea.py::test_tc_078_tc_080_same_100_char_idempotency_key_returns_first_result_self_cleaning |
| TC-079 | The same key can be used by two different Parents | test_f94_pay_with_ea.py::test_tc_079_new_idempotency_key_used_for_separate_payment_of_another_charge |
| TC-080 | A key of 100 characters is accepted | test_f94_pay_with_ea.py::test_tc_078_tc_080_same_idempotency_key_returns_first_result_and_pays_once<br>test_f94_pay_with_ea.py::test_tc_078_tc_080_same_100_char_idempotency_key_returns_first_result_self_cleaning |
| TC-081 | A key that is missing, empty or 101 characters long is refused | test_f93_method_and_eligibility.py::test_tc_081_api_refuses_missing_empty_or_too_long_idempotency_key<br>test_f93_method_and_eligibility.py::test_tc_081_refused_key_on_a_real_charge_creates_nothing_and_keeps_balance |
| TC-082 | Two requests at the same time for one invoice give one payment and one refusal | test_f94_pay_with_ea.py::test_tc_082_two_parents_using_same_idempotency_key_string_do_not_collide |
| TC-083 | Two guardians confirming the same invoice at the same time give one payment | test_f94_pay_with_ea.py::test_tc_083_concurrent_confirm_with_same_idempotency_key_creates_one_transaction |
| TC-084 | Confirming an invoice that was paid meanwhile is refused | test_f94_pay_with_ea.py::test_tc_084_charge_already_paid_in_another_tab_is_refused_without_double_charge<br>test_f94_pay_with_ea.py::test_tc_084_tc_086_stale_checkout_clears_selection_and_reloads_the_list |
| TC-085 | Confirming an invoice that is waiting for another payment is refused | test_f94_pay_with_ea.py::test_tc_085_two_payment_attempts_for_same_charge_with_different_keys_only_one_succeeds |
| TC-086 | Confirming an invoice that was cancelled meanwhile is refused | test_f94_pay_with_ea.py::test_tc_084_tc_086_stale_checkout_clears_selection_and_reloads_the_list |
| TC-087 | Review screen for an online payment has no EA part | test_f95_online_and_split.py::test_tc_087_tc_088_tc_089_pay_one_charge_online_leaves_education_account_untouched<br>test_f95_online_and_split.py::test_tc_087_review_screen_for_online_only_payment_shows_full_amount_online_and_touches_nothing |
| TC-088 | A student without an EA pays online and the invoice becomes Paid | test_f95_online_and_split.py::test_tc_087_tc_088_tc_089_pay_one_charge_online_leaves_education_account_untouched<br>test_f95_online_and_split.py::test_tc_088_pay_invoice_online_for_student_without_education_account |
| TC-089 | A student with an EA who pays online keeps the EA balance | test_f95_online_and_split.py::test_tc_087_tc_088_tc_089_pay_one_charge_online_leaves_education_account_untouched<br>test_f95_online_and_split.py::test_tc_089_pay_invoice_online_when_child_has_active_ea_leaves_wallet_untouched |
| TC-090 | Provider failure returns the invoice to Issued and nothing is charged | test_f95_online_and_split.py::test_tc_090_tc_139_charge_is_available_again_after_online_failure<br>test_f95_online_and_split.py::test_tc_090_tc_139_online_payment_failure_leaves_invoice_open_for_retry_self_cleaning |
| TC-091 | Cancel on the provider page returns the invoice to Issued | test_f95_online_and_split.py::test_tc_091_cancelling_on_provider_page_cancels_attempt_and_restores_invoice |
| TC-092 | An expired provider payment session fails the online leg | test_f95_online_and_split.py::test_tc_092_provider_session_expiry_marks_online_attempt_failed_and_restores_invoice |
| TC-094 | Closing the browser on the provider page keeps the payment Pending until the result arrives | test_f95_online_and_split.py::test_tc_094_when_provider_cannot_create_session_payment_fails_cleanly |
| TC-095 | A provider timeout keeps the leg Pending and does not mark it Failed | test_f95_online_and_split.py::test_tc_095_returning_from_provider_before_webhook_shows_pending_not_paid |
| TC-096 | No card data is stored after an online payment | test_f95_online_and_split.py::test_tc_096_tc_097_pay_with_both_full_or_custom_ea_amount_and_online_remainder |
| TC-097 | Split of EA 20.00 and online 50.63 pays a 70.63 invoice | test_f95_online_and_split.py::test_tc_097_tc_130_split_payment_succeeds_with_both_funding_sources<br>test_f95_online_and_split.py::test_tc_096_tc_097_pay_with_both_full_or_custom_ea_amount_and_online_remainder |
| TC-098 | The EA is debited before the online payment session is created | test_f95_online_and_split.py::test_tc_098_funding_parts_and_audit_entries_for_both_recorded_in_order |
| TC-099 | Split with a lowered EA part of 10.00 and an online part of 60.63 pays the invoice | test_f95_online_and_split.py::test_tc_099_in_both_ea_part_is_deducted_before_redirect_to_provider |
| TC-100 | Review screen for a split shows both parts and the balance after payment | test_f93_method_and_eligibility.py::test_tc_100_review_of_split_payment_shows_both_parts |
| TC-101 | While the online part is pending the waiting screen says the EA part is already taken | test_f97_result_and_receipt.py::test_tc_101_pending_split_says_education_account_part_is_already_taken |
| TC-102 | EA debit fails before the online part: no payment session and no online charge | test_f95_online_and_split.py::test_tc_102_in_both_if_ea_deduction_fails_online_session_is_never_created |
| TC-103 | Online failure after the EA debit returns the EA part | test_f95_online_and_split.py::test_tc_103_tc_137_failed_online_part_returns_the_education_account_part<br>test_f95_online_and_split.py::test_tc_103_tc_108_in_both_online_failure_reverses_ea_deduction_with_reversal_id |
| TC-104 | Cancel at the provider after the EA debit returns the EA part | test_f95_online_and_split.py::test_tc_104_in_both_parent_cancel_on_provider_reverses_ea_deduction |
| TC-105 | An expired provider session after the EA debit returns the EA part | test_f95_online_and_split.py::test_tc_105_in_both_if_provider_session_fails_after_ea_deducted_ea_is_reversed |
| TC-107 | A failed reversal moves the payment to ReconciliationRequired | test_f95_online_and_split.py::test_tc_107_in_both_online_timeout_reverses_ea_deduction |
| TC-108 | A failure after the EA debit and before the online session is cleaned up by the sweep | test_f95_online_and_split.py::test_tc_103_tc_108_in_both_online_failure_reverses_ea_deduction_with_reversal_id |
| TC-109 | The sweep leaves a split payment alone when the online leg exists | test_f95_online_and_split.py::test_tc_109_in_both_when_ea_not_reversed_payment_marked_reconciliation_required |
| TC-110 | A late provider success after the EA was returned is not paid and goes to manual handling | test_f95_online_and_split.py::test_tc_110_when_payment_in_reconciliation_required_invoice_stays_locked |
| TC-111 | A valid callback is recorded at once and processed later | test_f96_webhook_and_reconciliation.py::test_tc_111_webhook_without_signature_rejected |
| TC-112 | A callback with a wrong signature is rejected and changes nothing | test_f96_webhook_and_reconciliation.py::test_tc_112_webhook_with_bad_signature_rejected |
| TC-113 | A callback without a signature is rejected | test_f96_webhook_and_reconciliation.py::test_tc_113_webhook_altered_after_signing_rejected |
| TC-114 | A callback whose content was changed after signing is rejected | test_f96_webhook_and_reconciliation.py::test_tc_114_webhook_timestamp_outside_window_rejected |
| TC-115 | The same event sent twice is applied once | test_f96_webhook_and_reconciliation.py::test_tc_115_valid_webhook_saved_and_processed_with_full_metadata |
| TC-119 | Only a hash of the callback is stored | test_f96_webhook_and_reconciliation.py::test_tc_119_same_webhook_event_delivered_twice_processed_once |
| TC-120 | A lost webhook is replaced by the provider status query: success | test_f96_webhook_and_reconciliation.py::test_tc_120_second_webhook_different_event_id_for_settled_leg_ignored |
| TC-121 | A lost webhook is replaced by the provider status query: failure | test_f96_webhook_and_reconciliation.py::test_tc_121_webhook_with_unknown_funding_reference_ignored |
| TC-122 | A Pending leg that stays unclear beyond the threshold moves to ReconciliationRequired | test_f96_webhook_and_reconciliation.py::test_tc_122_webhook_amount_mismatch_marked_failed_and_not_settled |
| TC-123 | A webhook and a status query that arrive together are applied once | test_f96_webhook_and_reconciliation.py::test_tc_123_webhook_currency_not_sgd_marked_failed_and_not_settled |
| TC-125 | The waiting screen shows the pending notice, a temporary reference and the actions | test_f97_result_and_receipt.py::test_tc_125_pending_screen_says_processing_and_offers_no_failure_or_retry |
| TC-126 | Refreshing the waiting screen shows the success screen after the result arrives | test_f97_result_and_receipt.py::test_tc_126_waiting_screen_turns_into_success_without_reload |
| TC-127 | A Parent who comes back to a pending invoice cannot start a second payment | test_f97_result_and_receipt.py::test_tc_127_coming_back_to_pending_invoice_cannot_start_second_payment |
| TC-128 | The verifying state does not say the payment failed and offers no retry | test_f97_result_and_receipt.py::test_tc_128_verifying_state_does_not_say_the_payment_failed_and_offers_no_retry<br>test_f97_result_and_receipt.py::test_tc_128_verifying_state_names_the_education_account_part_that_was_taken |
| TC-129 | The success screen of an EA payment shows reference, time, part and total | test_f94_pay_with_ea.py::test_tc_065_tc_070_tc_129_pay_one_charge_with_education_account_end_to_end<br>test_f97_result_and_receipt.py::test_tc_129_success_screen_of_education_account_payment_shows_reference_time_part_and_total |
| TC-130 | The success screen of a split payment shows both parts | test_f95_online_and_split.py::test_tc_097_tc_130_split_payment_succeeds_with_both_funding_sources<br>test_f97_result_and_receipt.py::test_tc_130_success_screen_of_split_payment_shows_both_parts |
| TC-131 | The receipt PDF of an EA payment can be downloaded | test_f97_result_and_receipt.py::test_tc_131_tc_132_receipt_pdf_can_be_downloaded |
| TC-132 | The receipt PDF of a split payment shows two parts | test_f97_result_and_receipt.py::test_tc_131_tc_132_receipt_pdf_can_be_downloaded |
| TC-133 | The receipt can be printed | test_f97_result_and_receipt.py::test_tc_133_print_receipt_opens_the_print_dialog |
| TC-135 | The paid at time is shown in Singapore time | test_f97_result_and_receipt.py::test_tc_135_completed_time_is_shown_in_singapore_time |
| TC-136 | The failure screen of an online payment shows the message, the reason and the actions | test_f95_online_and_split.py::test_tc_136_online_payment_failure_shows_failed_result_and_keeps_balance<br>test_f97_result_and_receipt.py::test_tc_136_failure_screen_shows_message_and_actions_without_receipt<br>test_f97_result_and_receipt.py::test_tc_136_failure_screen_shows_the_reason |
| TC-137 | The failure screen of a split payment says the EA part was returned | test_f95_online_and_split.py::test_tc_103_tc_137_failed_online_part_returns_the_education_account_part<br>test_f97_result_and_receipt.py::test_tc_137_failed_split_with_returned_education_account_part_says_the_amount_was_returned |
| TC-138 | The failure message hides technical details | test_f97_result_and_receipt.py::test_tc_138_server_error_on_result_hides_technical_details |
| TC-139 | Exit on the failure screen returns to the invoice list with the invoice still Issued | test_f95_online_and_split.py::test_tc_090_tc_139_charge_is_available_again_after_online_failure<br>test_f95_online_and_split.py::test_tc_090_tc_139_online_payment_failure_leaves_invoice_open_for_retry_self_cleaning |
| TC-140 | Try again after a failure creates a new transaction with a new key and can succeed | test_f97_result_and_receipt.py::test_tc_140_failure_screen_offers_try_again |
| TC-141 | No retry is possible while the EA part has not been returned | test_f97_result_and_receipt.py::test_tc_141_reconciliation_with_education_account_still_taken_warns_and_offers_no_retry |
| TC-142 | A session that ends before the confirm creates no transaction | test_f91_access_and_child_list.py::test_tc_142_session_ended_before_confirm_creates_no_transaction |
| TC-143 | A session that ends after the confirm does not stop the payment | test_f97_result_and_receipt.py::test_tc_143_session_ending_after_confirm_does_not_stop_payment_from_finishing |
| TC-144 | A system error on confirm shows a safe message and changes no data | test_f97_result_and_receipt.py::test_tc_144_server_error_on_confirm_shows_safe_message_and_creates_nothing |
| TC-145 | The seed data follows every invoice rule of BR-F9-12 | test_f98_data_rules_and_constraints.py::test_tc_145_issued_invoice_zero_net_amount_refused |
| TC-146 | An Issued invoice with Net 0.00 is refused and a Draft with Net 0.00 is accepted | test_f98_data_rules_and_constraints.py::test_tc_146_invoice_line_amount_rules |
| TC-147 | A line with Subsidy equal to Gross is refused and Subsidy just below Gross is accepted | test_f98_data_rules_and_constraints.py::test_tc_147_charge_cannot_be_on_two_invoice_lines |
| TC-148 | A student charge cannot be placed on two invoices | test_f98_data_rules_and_constraints.py::test_tc_148_line_for_charge_of_another_child_refused |
| TC-149 | A line from another school than the invoice is refused | test_f98_data_rules_and_constraints.py::test_tc_149_line_from_another_school_than_invoice_refused |
| TC-150 | Negative amounts are refused | test_f98_data_rules_and_constraints.py::test_tc_150_invoice_totals_and_net_formula_enforced |
| TC-151 | Date fields follow the invoice status | test_f98_data_rules_and_constraints.py::test_tc_151_invoice_status_dates_rules |
| TC-152 | The currency defaults to SGD | test_f98_data_rules_and_constraints.py::test_tc_152_invoice_cannot_have_two_open_transactions |
| TC-153 | A second open transaction for an invoice is refused by the database | test_f98_data_rules_and_constraints.py::test_tc_153_invoice_cannot_have_two_succeeded_transactions |
| TC-154 | A second Succeeded transaction for an invoice is refused | test_f98_data_rules_and_constraints.py::test_tc_154_same_user_and_idempotency_key_refused |
| TC-155 | An idempotency key is unique for a Parent and can repeat across Parents | test_f98_data_rules_and_constraints.py::test_tc_155_funding_reference_unique |
| TC-156 | A FundingReference is unique and a split uses two different references | test_f98_data_rules_and_constraints.py::test_tc_156_ea_leg_requires_wallet_and_no_provider_fields |
| TC-157 | Wallet and provider fields depend on the leg method | test_f98_data_rules_and_constraints.py::test_tc_157_online_leg_requires_provider_and_no_wallet_fields |
| TC-158 | Ledger and provider IDs are stored when they must be and are unique | test_f98_data_rules_and_constraints.py::test_tc_158_external_transaction_ids_unique_across_funding_legs |
| TC-159 | Leg amounts add up to the transaction and the transaction equals the invoice Net | test_f98_data_rules_and_constraints.py::test_tc_159_funding_leg_settled_amount_bounds |
| TC-160 | An amount other than the invoice Net cannot be requested | test_f98_data_rules_and_constraints.py::test_tc_160_transaction_status_amounts_and_completed_at_rules |
| TC-161 | Settled above Requested and a leg amount of zero are refused | test_f98_data_rules_and_constraints.py::test_tc_161_currency_code_defaults_to_sgd |
| TC-162 | CompletedAt is empty while processing and filled when the transaction is final | test_f98_data_rules_and_constraints.py::test_tc_162_money_columns_store_two_decimal_places |
| TC-164 | System error while loading the invoice list shows a safe message | test_f92_outstanding_and_balance.py::test_tc_164_system_error_on_charge_list_shows_safe_message_and_retry |
| TC-166 | A second guardian pays an invoice of the shared child and the payment is recorded for that guardian | test_f94_pay_with_ea.py::test_tc_166_editing_invoice_while_payment_in_progress_triggers_ea_reversal |
| TC-167 | Status changes of a split payment that is returned are written to the audit log | test_f95_online_and_split.py::test_tc_167_late_payment_succeeded_webhook_after_failed_is_flagged_for_review |
| TC-168 | Two invoices cannot share an invoice number | test_f98_data_rules_and_constraints.py::test_tc_168_invoice_number_unique_when_set |
| TC-169 | The line number of an invoice line is above 0 and unique inside its invoice | test_f98_data_rules_and_constraints.py::test_tc_169_invoice_line_numbers_positive_and_unique_per_invoice |
| TC-171 | The sequence number of a funding leg is above 0 and unique inside its transaction | test_f98_data_rules_and_constraints.py::test_tc_171_funding_sequence_numbers_positive_and_unique_per_transaction |
| TC-173 | The FAS subsidy of each line is shown and Net is Gross minus subsidy, rounded half up | test_f99_validation_rules.py::test_tc_173_subsidy_is_shown_and_net_is_gross_minus_subsidy |
| TC-174 | An invoice with a 100% FAS subsidy still has the GST to pay and is payable by EA | test_f99_validation_rules.py::test_tc_174_charge_fully_covered_by_subsidy_still_has_amount_to_pay_and_ea_option |
| TC-176 | Children are listed in alphabetical order of name | test_f99_validation_rules.py::test_tc_176_children_are_listed_in_alphabetical_order |
| TC-177 | A double click on a child card opens the invoice list once | test_f99_validation_rules.py::test_tc_177_double_click_on_child_card_opens_the_fee_page_once |
| TC-178 | The debt label counts Issued invoices only | test_f99_validation_rules.py::test_tc_178_debt_label_counts_issued_invoices_only |
| TC-179 | A loading state is shown while the child list loads | test_f99_validation_rules.py::test_tc_179_loading_state_is_shown_while_the_child_list_loads |
| TC-180 | Malformed or hostile IDs in a request are refused without a server error | test_f99_validation_rules.py::test_tc_180_malformed_or_hostile_ids_are_refused_without_a_server_error |
| TC-181 | The answer for an ID of another family is the same as for an ID that does not exist | test_f99_validation_rules.py::test_tc_181_answer_for_another_family_equals_answer_for_unknown_id |
| TC-182 | A line description with HTML is shown as text and is not executed | test_f99_validation_rules.py::test_tc_182_html_in_a_line_description_is_shown_as_text |
| TC-183 | A double click on Pay opens the payment method screen once | test_f99_validation_rules.py::test_tc_183_double_click_on_continue_moves_to_the_method_step_once |
| TC-184 | The back to child list button works on the invoice list and on the empty state | test_f99_validation_rules.py::test_tc_184_back_to_child_list_link_works_on_the_fee_page<br>test_f99_validation_rules.py::test_tc_184_back_to_child_list_link_works_on_the_empty_state |
| TC-185 | A loading state is shown while the invoice list loads | test_f99_validation_rules.py::test_tc_185_loading_state_is_shown_while_the_fee_list_loads |
| TC-186 | A payment method is preselected for each state and Continue needs a method | test_f99_validation_rules.py::test_tc_186_education_account_is_preselected_when_the_balance_is_enough<br>test_f99_validation_rules.py::test_tc_186_both_is_preselected_and_ea_only_is_disabled_when_the_balance_is_short<br>test_f99_validation_rules.py::test_tc_186_online_is_the_only_and_selected_method_when_there_is_no_balance |
| TC-187 | The EA part rejects values that are not numbers | test_f99_validation_rules.py::test_tc_187_ea_part_rejects_values_that_are_not_numbers |
| TC-188 | The EA part follows the length, decimal and space rules | test_f99_validation_rules.py::test_tc_188_ea_part_follows_length_decimal_and_space_rules |
| TC-189 | The EA part treats script, SQL and special characters as text | test_f99_validation_rules.py::test_tc_189_ea_part_treats_script_and_special_characters_as_text |
| TC-190 | The EA part and the online part go back to the default when the method or the invoice changes | test_f99_validation_rules.py::test_tc_190_ea_part_goes_back_to_default_when_method_changes |
| TC-191 | A failed check on Continue keeps the screen and changes no data, and a double click opens the next screen once | test_f99_validation_rules.py::test_tc_191_double_click_on_continue_opens_the_review_step_once<br>test_f99_validation_rules.py::test_tc_191_failed_check_on_continue_keeps_the_screen_and_changes_nothing |
| TC-192 | Back on the payment method screen returns to the invoice list and changes nothing | test_f99_validation_rules.py::test_tc_192_back_on_the_method_step_returns_to_the_charge_list_and_changes_nothing |
| TC-193 | Cancel on the review screen leaves without paying and is disabled after Confirm | test_f99_validation_rules.py::test_tc_193_cancel_on_the_review_step_leaves_without_paying |
| TC-194 | An idempotency key with characters that are not allowed is refused and not corrected | test_f99_validation_rules.py::test_tc_194_idempotency_key_with_not_allowed_characters_is_refused |
| TC-195 | The same key with different content is refused | test_f99_validation_rules.py::test_tc_195_same_key_with_different_content_is_refused |
| TC-196 | The waiting screen shows only Pending or ReconciliationRequired, the leg statuses and the reference | test_f99_validation_rules.py::test_tc_196_waiting_screen_shows_pending_status_and_leg<br>test_f99_validation_rules.py::test_tc_196_reconciliation_required_screen_says_being_checked_not_failed<br>test_f99_validation_rules.py::test_tc_196_waiting_screen_shows_the_payment_reference |
| TC-197 | Refresh status only reads the status and is disabled for a few seconds after a click | test_f99_validation_rules.py::test_tc_197_refresh_status_button_is_disabled_for_a_moment_after_a_click |
| TC-198 | Back to the fee list after a payment shows the empty state when no fee is left | test_f99_validation_rules.py::test_tc_198_success_screen_has_a_button_back_to_the_fee_list |
| TC-199 | The receipt button exists only for a Succeeded payment and the file is named receipt_reference.pdf | test_f99_validation_rules.py::test_tc_199_receipt_button_exists_only_for_a_succeeded_payment<br>test_f99_validation_rules.py::test_tc_199_receipt_file_is_named_receipt_reference_pdf |
| TC-200 | Amounts and dates follow one format on every screen | test_f99_validation_rules.py::test_tc_200_balance_is_shown_with_thousand_separator_and_two_decimals<br>test_f99_validation_rules.py::test_tc_200_due_dates_follow_dd_mm_yyyy<br>test_f99_validation_rules.py::test_tc_200_paid_at_time_is_shown_as_dd_mm_yyyy_hh_mm_in_singapore_time |
| TC-201 | A request with the wrong number or order of legs, or a wrong method, is refused | test_f99_validation_rules.py::test_tc_201_wrong_method_values_are_refused_and_create_nothing |
| TC-202 | A valid callback that matches no leg is ignored and a callback with another amount needs reconciliation | test_f99_validation_rules.py::test_tc_202_callback_that_matches_no_leg_is_ignored_and_changes_nothing<br>test_f99_validation_rules.py::test_tc_202_callback_with_another_amount_needs_reconciliation |
| TC-203 | The callback text fields accept their maximum length and refuse one more character | test_f99_validation_rules.py::test_tc_203_callback_text_field_accepts_its_maximum_length<br>test_f99_validation_rules.py::test_tc_203_callback_text_field_refuses_one_more_character |
| TC-205 | An invoice number can have 50 characters and not 51 | test_f99_validation_rules.py::test_tc_205_invoice_number_accepts_50_characters_and_refuses_51 |
| TC-206 | A transaction reference is unique and the transaction status accepts only 1 to 5 | test_f99_validation_rules.py::test_tc_206_transaction_reference_is_unique_and_status_accepts_only_1_to_5 |

## Case chưa tự động hóa

| Case | Tiêu đề | Lý do |
|---|---|---|
| TC-175 | A child aged 16 or older is listed with the invoice but the Pay button is not offered | UI không hiện ngày sinh hay tuổi của con và chưa có quy tắc 'từ 16 tuổi không có nút Pay' (quy tắc R8, điểm mở O22 trong tài liệu validation rules). Không có dữ liệu để kiểm, làm lại khi FS chốt quy tắc. |
| TC-204 | The stored error text of a failed callback is cleaned and at most 500 characters | Cần cách làm hỏng xử lý một callback hợp lệ để đọc thông báo lỗi được lưu (ENV-R9-05), Dev chưa cung cấp. Ngoài phạm vi kiểm thử qua giao diện và API. |
