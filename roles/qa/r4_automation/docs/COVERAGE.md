# Coverage of R4_Test_Cases.xlsx

Cases in the workbook: 267. Automated: 199. Not automated: 68.

| Suite | Cases | Automated | Not automated |
|---|---|---|---|
| F4.1 Submit routing | 9 | 5 | 4 |
| F4.2 MOEFAS ranking and assessment | 35 | 20 | 15 |
| F4.3 Applications list, MOE HQ | 14 | 13 | 1 |
| F4.4 Applications list, School Admin | 10 | 8 | 2 |
| F4.5 Filters and search | 27 | 25 | 2 |
| F4.6 Export | 6 | 4 | 2 |
| F4.7 Review drawer, MOEFAS | 12 | 11 | 1 |
| F4.8 Review drawer, SBFAS | 10 | 8 | 2 |
| F4.9 Approve SBFAS | 19 | 15 | 4 |
| F4.10 Reject SBFAS | 10 | 9 | 1 |
| F4.11 One decision per application | 4 | 1 | 3 |
| F4.12 Access and security | 11 | 5 | 6 |
| F4.13 FAS schemes list | 13 | 11 | 2 |
| F4.14 New scheme wizard | 33 | 31 | 2 |
| F4.15 Review and publish | 17 | 15 | 2 |
| F4.16 Add fee to a published scheme | 11 | 8 | 3 |
| F4.17 Close form now (demo) | 3 | 3 | 0 |
| F4.18 Effects after a decision | 4 | 0 | 4 |
| F4.19 ML recommendation and risk | 15 | 4 | 11 |
| F4.20 Formats | 4 | 3 | 1 |

## Automated cases

| Case | Title | Test |
|---|---|---|
| TC-001 | Waiting MOEFAS application shows Pending and System check Waiting | test_f41_submit_routing.py::test_tc_001_waiting_moefas_shows_pending_and_waiting |
| TC-002 | Waiting MOEFAS drawer explains the wait and records the submit in History | test_f41_submit_routing.py::test_tc_002_waiting_drawer_explains_wait_and_records_submit |
| TC-003 | Waiting MOEFAS application is not visible to the School Admin | test_f41_submit_routing.py::test_tc_003_waiting_moefas_not_visible_to_school_admin |
| TC-004 | International student application is SBFAS Pending for the school | test_f41_submit_routing.py::test_tc_004_international_student_is_sbfas_pending |
| TC-006 | Singapore Citizen application is not routed to SBFAS at submit | test_f41_submit_routing.py::test_tc_006_citizen_application_is_not_routed_to_sbfas |
| TC-010 | Closing the form ranks the waiting applications by lowest PCI first | test_f42_moefas_ranking_assessment.py::test_tc_010_closing_the_form_ranks_by_lowest_pci |
| TC-011 | Priority n of N is saved and shown in the Decision block | test_f42_moefas_ranking_assessment.py::test_tc_011_priority_is_saved_in_the_decision_block |
| TC-012 | Only waiting MOEFAS applications of the closing scheme are ranked | test_f42_moefas_ranking_assessment.py::test_tc_012_only_waiting_applications_of_the_closing_scheme_are_ranked |
| TC-014 | Closing a form with no waiting application changes nothing | test_f42_moefas_ranking_assessment.py::test_tc_014_closing_a_form_without_waiting_applications_changes_nothing |
| TC-016 | Ranking follows PCI and not the submit time | test_f42_moefas_ranking_assessment.py::test_tc_016_ranking_follows_pci_and_not_the_submit_time |
| TC-021 | A passing application is approved by the system | test_f42_moefas_ranking_assessment.py::test_tc_021_a_passing_application_is_approved_by_the_system |
| TC-022 | History of an automatic approval lists priority, approval and the email | test_f42_moefas_ranking_assessment.py::test_tc_022_history_of_an_automatic_approval |
| TC-023 | Effective from is the scheme Effective from when the scheme starts later | test_f42_moefas_ranking_assessment.py::test_tc_023_effective_from_is_the_scheme_start_when_later |
| TC-025 | Cards and tab counts update after the automatic decisions | test_f42_moefas_ranking_assessment.py::test_tc_025_cards_and_tabs_update_after_the_automatic_decisions |
| TC-026 | Automatically approved MOEFAS application is final and read only | test_f42_moefas_ranking_assessment.py::test_tc_026_automatic_approval_is_final_and_read_only |
| TC-027 | Both GHI and PCI within the limits pass | test_f42_moefas_ranking_assessment.py::test_tc_027_both_ghi_and_pci_within_the_limits_pass |
| TC-032 | Both GHI and PCI above the limits fail | test_f42_moefas_ranking_assessment.py::test_tc_032_ghi_and_pci_above_the_limits_fail |
| TC-034 | Limits come from the scheme of the application | test_f42_moefas_ranking_assessment.py::test_tc_034_limits_come_from_the_scheme_of_the_application |
| TC-035 | Fail with Also consider for SBFAS Yes becomes SBFAS Pending for the school | test_f42_moefas_ranking_assessment.py::test_tc_035_fail_with_sbfas_yes_becomes_sbfas_pending |
| TC-036 | The school sees the transferred application with an ML recommendation | test_f42_moefas_ranking_assessment.py::test_tc_036_school_sees_the_transferred_application_with_ml_tier |
| TC-038 | A transferred SBFAS application is not visible to other schools | test_f42_moefas_ranking_assessment.py::test_tc_038_transferred_application_is_not_visible_to_other_schools |
| TC-039 | The scheme shows Assessed and no waiting count after processing | test_f42_moefas_ranking_assessment.py::test_tc_039_scheme_shows_assessed_and_no_waiting_count |
| TC-041 | Earlier schemes keep their Assessed date and the new one starts waiting | test_f42_moefas_ranking_assessment.py::test_tc_041_earlier_schemes_keep_their_assessed_date |
| TC-042 | MOE HQ has no Approve or Reject on any application | test_f42_moefas_ranking_assessment.py::test_tc_042_moe_hq_has_no_approve_or_reject |
| TC-043 | The School Admin cannot decide a MOEFAS application | test_f42_moefas_ranking_assessment.py::test_tc_043_school_admin_cannot_decide_a_moefas_application |
| TC-045 | MOE HQ list shows the subtitle, Export button and note | test_f43_applications_list_hq.py::test_tc_045_hq_list_shows_subtitle_export_and_note |
| TC-046 | MOE HQ cards show the base counts and ignore filters and search | test_f43_applications_list_hq.py::test_tc_046_hq_cards_show_base_counts_and_ignore_filters |
| TC-047 | MOE HQ tabs show the counts and open on All | test_f43_applications_list_hq.py::test_tc_047_hq_tabs_show_counts_and_open_on_all |
| TC-048 | Tab counts stay fixed when filters or search change the rows | test_f43_applications_list_hq.py::test_tc_048_tab_counts_stay_fixed_when_filters_or_search_change |
| TC-049 | MOE HQ table has the 12 columns in the right order | test_f43_applications_list_hq.py::test_tc_049_hq_table_has_the_columns_in_order |
| TC-050 | Application and Student cells use the required formats | test_f43_applications_list_hq.py::test_tc_050_application_and_student_cells_use_the_required_formats |
| TC-051 | System check shows Waiting, Pass, Fail or a dash by scheme and status | test_f43_applications_list_hq.py::test_tc_051_system_check_by_scheme_and_status |
| TC-052 | Tier and ML recommendation follow the scheme and the decision | test_f43_applications_list_hq.py::test_tc_052_tier_and_ml_recommendation_follow_scheme_and_decision |
| TC-053 | Grade shows a dash when the student has no class | test_f43_applications_list_hq.py::test_tc_053_grade_shows_a_dash_without_class |
| TC-054 | ML risk and Status show only the allowed values | test_f43_applications_list_hq.py::test_tc_054_ml_risk_and_status_show_only_allowed_values |
| TC-055 | List is sorted by Submitted, newest first | test_f43_applications_list_hq.py::test_tc_055_list_is_sorted_by_submitted_newest_first |
| TC-056 | Footer shows the row range and paging buttons for one page | test_f43_applications_list_hq.py::test_tc_056_footer_shows_row_range_and_paging_buttons |
| TC-058 | Empty result shows the message and an empty footer | test_f43_applications_list_hq.py::test_tc_058_empty_result_shows_message_and_empty_footer |
| TC-059 | School Admin sees only SBFAS applications of the own school | test_f44_applications_list_school.py::test_tc_059_school_admin_sees_only_sbfas_of_own_school |
| TC-060 | School Admin of a school without SBFAS applications sees an empty list | test_f44_applications_list_school.py::test_tc_060_school_without_sbfas_sees_an_empty_list |
| TC-061 | School cards show Pending, SBFAS approved and SBFAS rejected for this year | test_f44_applications_list_school.py::test_tc_061_school_cards_show_pending_approved_rejected |
| TC-063 | School tabs open on Pending and show counts | test_f44_applications_list_school.py::test_tc_063_school_tabs_open_on_pending_with_counts |
| TC-065 | School table has the 9 columns with Tier before ML recommendation | test_f44_applications_list_school.py::test_tc_065_school_table_columns_tier_before_ml |
| TC-066 | Review shows for Pending SBFAS and View for decided ones | test_f44_applications_list_school.py::test_tc_066_review_for_pending_and_view_for_decided |
| TC-067 | School table values for a pending and an approved SBFAS row | test_f44_applications_list_school.py::test_tc_067_school_table_values_of_a_pending_and_an_approved_row |
| TC-068 | School list note explains Tier and MOE HQ only data | test_f44_applications_list_school.py::test_tc_068_school_note_explains_tier_and_hq_only_data |
| TC-069 | Search by Application ID finds one application | test_f45_search_and_filters.py::test_tc_069_search_by_application_id |
| TC-070 | Search by student name is a case-insensitive contains match | test_f45_search_and_filters.py::test_tc_070_search_by_name_is_case_insensitive_contains |
| TC-071 | Search by NRIC/FIN matches the whole or a part of the number | test_f45_search_and_filters.py::test_tc_071_search_by_nric_whole_or_part |
| TC-072 | Search with no match shows the empty message | test_f45_search_and_filters.py::test_tc_072_search_without_match_shows_empty_message |
| TC-073 | Search trims leading and trailing spaces | test_f45_search_and_filters.py::test_tc_073_search_trims_leading_and_trailing_spaces |
| TC-074 | Search accepts up to 100 characters and warns above that | test_f45_search_and_filters.py::test_tc_074_search_accepts_100_characters_and_warns_above |
| TC-075 | Special characters and script text are searched as plain text | test_f45_search_and_filters.py::test_tc_075_special_characters_are_searched_as_plain_text |
| TC-076 | School Admin search never returns an application of another school | test_f45_search_and_filters.py::test_tc_076_school_search_never_returns_other_schools |
| TC-077 | School filter lists the four schools and narrows the rows | test_f45_search_and_filters.py::test_tc_077_school_filter_lists_four_schools_and_narrows_rows |
| TC-078 | Scheme filter separates MOEFAS and SBFAS | test_f45_search_and_filters.py::test_tc_078_scheme_filter_separates_moefas_and_sbfas |
| TC-079 | Grade filter lists P1 to P6 and S1 to S4 and matches the class grade | test_f45_search_and_filters.py::test_tc_079_grade_filter_lists_p1_to_s4_and_matches_class_grade |
| TC-080 | Tier filter matches the granted tier on decided rows and MOEFAS rows | test_f45_search_and_filters.py::test_tc_080_tier_filter_matches_granted_tier_and_moefas |
| TC-081 | Tier filter matches the ML recommended tier on pending SBFAS rows | test_f45_search_and_filters.py::test_tc_081_tier_filter_matches_ml_tier_on_pending_sbfas |
| TC-082 | Only published school scheme names appear in the HQ Tier filter | test_f45_search_and_filters.py::test_tc_082_only_published_school_scheme_names_in_hq_tier_filter |
| TC-083 | Status filter shows Pending, Approved or Rejected rows | test_f45_search_and_filters.py::test_tc_083_status_filter_shows_pending_approved_rejected |
| TC-084 | ML risk filter shows Low, Medium or High rows | test_f45_search_and_filters.py::test_tc_084_ml_risk_filter_shows_low_medium_high |
| TC-085 | Submitted filter defaults to Any time and limits the range | test_f45_search_and_filters.py::test_tc_085_submitted_filter_defaults_to_any_time_and_limits_range |
| TC-087 | School filters are Search, Grade, Tier, Status, ML risk and Submitted | test_f45_search_and_filters.py::test_tc_087_school_filters_are_the_six_and_have_no_school_or_scheme |
| TC-088 | Grade options follow the grades the school offers | test_f45_search_and_filters.py::test_tc_088_grade_options_follow_the_grades_the_school_offers |
| TC-089 | Tier options are the names of the school SBFAS schemes | test_f45_search_and_filters.py::test_tc_089_tier_options_are_the_school_sbfas_scheme_names |
| TC-090 | School Tier filter matches the ML recommended tier on pending rows | test_f45_search_and_filters.py::test_tc_090_school_tier_filter_matches_ml_tier_on_pending_rows |
| TC-091 | School Status, ML risk and Submitted filters narrow the school rows | test_f45_search_and_filters.py::test_tc_091_school_status_risk_and_submitted_filters |
| TC-092 | Filters combine with AND | test_f45_search_and_filters.py::test_tc_092_filters_combine_with_and |
| TC-093 | A tab and the Status filter combine with AND | test_f45_search_and_filters.py::test_tc_093_tab_and_status_filter_combine_with_and |
| TC-094 | Clearing a filter restores the rows | test_f45_search_and_filters.py::test_tc_094_clearing_a_filter_restores_the_rows |
| TC-096 | Export file holds the columns of 3.4 and every row of the list | test_f46_export.py::test_tc_096_export_holds_the_columns_and_every_row |
| TC-097 | Export holds only the filtered and searched rows | test_f46_export.py::test_tc_097_export_holds_only_the_filtered_and_searched_rows |
| TC-099 | School Admin export omits School, Scheme and System check | test_f46_export.py::test_tc_099_school_export_omits_school_scheme_and_system_check |
| TC-100 | Export of an empty list writes the header only | test_f46_export.py::test_tc_100_export_of_an_empty_list_writes_the_header_only |
| TC-102 | Pending MOEFAS drawer shows the header and the waiting note | test_f47_review_drawer_moefas.py::test_tc_102_pending_moefas_drawer_shows_header_and_waiting_note |
| TC-103 | Eligibility check rows show scheme, level, nationality, GHI and PCI with Pass or Fail | test_f47_review_drawer_moefas.py::test_tc_103_eligibility_rows_show_values_limits_and_pass_or_fail<br>test_f47_review_drawer_moefas.py::test_tc_103_pci_shows_two_decimals_and_no_extra_text |
| TC-104 | Household and income, context and documents are shown for MOEFAS | test_f47_review_drawer_moefas.py::test_tc_104_household_context_and_documents_for_moefas |
| TC-105 | MOEFAS drawer has no student, parent or ML block | test_f47_review_drawer_moefas.py::test_tc_105_moefas_drawer_has_no_student_parent_or_ml_block |
| TC-106 | Approved MOEFAS drawer shows Granted, Priority and Decided by | test_f47_review_drawer_moefas.py::test_tc_106_approved_moefas_drawer_shows_granted_priority_and_decided_by |
| TC-107 | Rejected MOEFAS drawer shows the reason and the system as decider | test_f47_review_drawer_moefas.py::test_tc_107_rejected_moefas_drawer_shows_reason_and_system_as_decider |
| TC-109 | Decision block is not shown while the application is pending | test_f47_review_drawer_moefas.py::test_tc_109_decision_block_is_not_shown_while_pending |
| TC-110 | Drawer closes with the X button | test_f47_review_drawer_moefas.py::test_tc_110_drawer_closes_with_the_x_button |
| TC-111 | Drawer closes when the user clicks outside it | test_f47_review_drawer_moefas.py::test_tc_111_drawer_closes_when_clicking_outside |
| TC-112 | Reopening the drawer shows the data of the clicked row | test_f47_review_drawer_moefas.py::test_tc_112_reopening_shows_the_data_of_the_clicked_row |
| TC-113 | Filters and search stay after the drawer closes | test_f47_review_drawer_moefas.py::test_tc_113_filters_and_search_stay_after_the_drawer_closes |
| TC-114 | School Admin drawer shows student, parent, household, context, ML, documents and history | test_f48_review_drawer_sbfas.py::test_tc_114_school_drawer_shows_all_blocks |
| TC-115 | MOE HQ drawer for SBFAS shows the school in the header and the student block | test_f48_review_drawer_sbfas.py::test_tc_115_hq_drawer_for_sbfas_shows_school_and_student_block |
| TC-116 | Decided SBFAS drawer shows Tier, from date, reason, comment and decider | test_f48_review_drawer_sbfas.py::test_tc_116_decided_sbfas_drawer_shows_tier_decider_and_history |
| TC-117 | Parent relationship and citizenship use readable labels | test_f48_review_drawer_sbfas.py::test_tc_117_parent_relationship_and_citizenship_use_readable_labels |
| TC-118 | ML recommendation block shows the tier only with the tag Recommendation only | test_f48_review_drawer_sbfas.py::test_tc_118_ml_block_shows_tier_with_recommendation_only_tag |
| TC-120 | ML recommendation is information only and does not block a choice | test_f48_review_drawer_sbfas.py::test_tc_120_ml_recommendation_does_not_block_a_choice |
| TC-121 | Reject and Approve show only for the School Admin of the school on a Pending SBFAS | test_f48_review_drawer_sbfas.py::test_tc_121_reject_and_approve_show_only_on_a_pending_sbfas |
| TC-122 | MOE HQ drawers have no decision button for SBFAS | test_f48_review_drawer_sbfas.py::test_tc_122_hq_drawers_have_no_decision_button_for_sbfas |
| TC-124 | Approve dialog shows the subtitle, the candidate tiers and the buttons | test_f49_approve_sbfas.py::test_tc_124_approve_dialog_shows_subtitle_candidate_tiers_and_buttons |
| TC-127 | Candidate tiers are sorted by name | test_f49_approve_sbfas.py::test_tc_127_candidate_tiers_are_sorted_by_name |
| TC-128 | Cancel closes the dialog and changes nothing | test_f49_approve_sbfas.py::test_tc_128_cancel_closes_the_dialog_and_changes_nothing |
| TC-129 | ML tier is pre-selected with a hint | test_f49_approve_sbfas.py::test_tc_129_ml_tier_is_preselected_with_a_hint |
| TC-130 | Without an ML tier the last scheme is pre-selected and no hint is shown | test_f49_approve_sbfas.py::test_tc_130_without_ml_tier_last_scheme_is_preselected_and_no_hint |
| TC-131 | The School Admin may choose a tier other than the recommendation | test_f49_approve_sbfas.py::test_tc_131_school_admin_may_choose_a_tier_other_than_the_recommendation |
| TC-132 | A household that meets no scheme can still be approved by the school | test_f49_approve_sbfas.py::test_tc_132_household_that_meets_no_scheme_can_still_be_approved |
| TC-134 | Comment is optional | test_f49_approve_sbfas.py::test_tc_134_comment_is_optional |
| TC-135 | Comment accepts 500 characters and blocks 501 | test_f49_approve_sbfas.py::test_tc_135_comment_accepts_500_characters_and_blocks_501 |
| TC-136 | Comment with markup is saved as plain text | test_f49_approve_sbfas.py::test_tc_136_comment_with_markup_is_saved_as_plain_text |
| TC-137 | Confirm approval saves the tier, the date and the decider | test_f49_approve_sbfas.py::test_tc_137_confirm_approval_saves_tier_date_and_decider |
| TC-139 | History lists the approval and the email | test_f49_approve_sbfas.py::test_tc_139_history_lists_the_approval_and_the_email |
| TC-140 | Cards and tab counts update after the approval | test_f49_approve_sbfas.py::test_tc_140_cards_and_tab_counts_update_after_the_approval |
| TC-141 | MOE HQ counts update after a school approval | test_f49_approve_sbfas.py::test_tc_141_hq_counts_update_after_a_school_approval |
| TC-142 | An approved application is read only | test_f49_approve_sbfas.py::test_tc_142_an_approved_application_is_read_only |
| TC-143 | Reject dialog shows the reasons, the hint and the disabled button | test_f410_reject_sbfas.py::test_tc_143_reject_dialog_shows_reasons_hint_and_disabled_button |
| TC-144 | Reject stays disabled until both reason and comment are filled | test_f410_reject_sbfas.py::test_tc_144_reject_stays_disabled_until_reason_and_comment_are_filled |
| TC-145 | Reject comment accepts 500 characters and blocks 501 | test_f410_reject_sbfas.py::test_tc_145_reject_comment_accepts_500_characters_and_blocks_501 |
| TC-146 | Each reason value is accepted | test_f410_reject_sbfas.py::test_tc_146_each_reason_value_is_accepted |
| TC-147 | Cancel closes the reject dialog and changes nothing | test_f410_reject_sbfas.py::test_tc_147_cancel_closes_the_reject_dialog_and_changes_nothing |
| TC-148 | Reject saves the reason, the comment and the decider | test_f410_reject_sbfas.py::test_tc_148_reject_saves_reason_comment_and_decider |
| TC-149 | History lists the rejection and the email with the reason | test_f410_reject_sbfas.py::test_tc_149_history_lists_the_rejection_and_the_email_with_reason |
| TC-150 | Cards and tabs update after the rejection | test_f410_reject_sbfas.py::test_tc_150_cards_and_tabs_update_after_the_rejection |
| TC-152 | A rejected application is read only | test_f410_reject_sbfas.py::test_tc_152_a_rejected_application_is_read_only |
| TC-155 | Double click on Confirm approval saves one decision | test_f411_one_decision.py::test_tc_155_double_click_on_confirm_approval_saves_one_decision |
| TC-157 | MOE HQ menu has FAS applications and MOEFAS schemes and no SBFAS schemes | test_f412_access_and_security.py::test_tc_157_hq_menu_has_fas_applications_and_moefas_schemes_only |
| TC-158 | School menu has FAS applications and SBFAS schemes and no MOEFAS schemes | test_f412_access_and_security.py::test_tc_158_school_menu_has_fas_applications_and_sbfas_schemes_only |
| TC-159 | Each role sees the data and actions of FS 1.2 and nothing else | test_f412_access_and_security.py::test_tc_159_each_role_sees_the_data_and_actions_of_its_role |
| TC-166 | Reject comment with markup is stored and shown as text | test_f412_access_and_security.py::test_tc_166_reject_comment_with_markup_is_shown_as_text |
| TC-167 | Scheme name with markup is shown as text | test_f412_access_and_security.py::test_tc_167_scheme_name_with_markup_is_shown_as_text |
| TC-168 | MOE HQ sees the three MOEFAS schemes only | test_f413_fas_schemes_list.py::test_tc_168_hq_sees_the_three_moefas_schemes_only |
| TC-169 | A School Admin sees the own SBFAS schemes only | test_f413_fas_schemes_list.py::test_tc_169_school_admin_sees_the_own_sbfas_schemes_only |
| TC-170 | The page subtitle states the role scope | test_f413_fas_schemes_list.py::test_tc_170_page_subtitle_states_the_role_scope |
| TC-171 | Scheme cards count Active, Upcoming, Closed and Draft | test_f413_fas_schemes_list.py::test_tc_171_scheme_cards_count_active_upcoming_closed_and_draft |
| TC-172 | Table columns and cell contents of the MOEFAS scheme list | test_f413_fas_schemes_list.py::test_tc_172_columns_and_cells_of_the_moefas_scheme_list<br>test_f413_fas_schemes_list.py::test_tc_172_effective_from_is_shown_as_dd_mm_yyyy |
| TC-173 | SBFAS list shows Approved by school and the PCI band | test_f413_fas_schemes_list.py::test_tc_173_sbfas_list_shows_approved_by_school_and_the_pci_band |
| TC-174 | Sort is Effective from newest first, then name | test_f413_fas_schemes_list.py::test_tc_174_sort_is_effective_from_newest_first_then_name |
| TC-177 | MOEFAS rows show waiting count or Assessed date | test_f413_fas_schemes_list.py::test_tc_177_moefas_rows_show_waiting_count_or_assessed_date |
| TC-178 | Actions follow the scheme status | test_f413_fas_schemes_list.py::test_tc_178_actions_follow_the_scheme_status |
| TC-179 | Close form now (demo) shows only for HQ on a MOEFAS scheme with the form Open | test_f413_fas_schemes_list.py::test_tc_179_close_form_now_shows_only_for_hq_on_an_open_moefas_form |
| TC-180 | New scheme creates MOEFAS for HQ and SBFAS for a school with no type choice | test_f413_fas_schemes_list.py::test_tc_180_new_scheme_has_no_type_or_level_field |
| TC-181 | Step 1 shows the fields, the defaults and the blue note | test_f414_new_scheme_wizard.py::test_tc_181_step_1_shows_the_fields_the_defaults_and_the_blue_note |
| TC-182 | The blue note follows the dates | test_f414_new_scheme_wizard.py::test_tc_182_the_blue_note_follows_the_dates |
| TC-183 | Scheme name is required | test_f414_new_scheme_wizard.py::test_tc_183_scheme_name_is_required |
| TC-184 | Form opens and Form closes are required | test_f414_new_scheme_wizard.py::test_tc_184_form_opens_and_form_closes_are_required |
| TC-185 | Form closes may equal Form opens but not be earlier | test_f414_new_scheme_wizard.py::test_tc_185_form_closes_may_equal_form_opens_but_not_be_earlier |
| TC-186 | Effective from must be after Form closes | test_f414_new_scheme_wizard.py::test_tc_186_effective_from_must_be_after_form_closes |
| TC-187 | Effective to must be after Effective from and may be empty | test_f414_new_scheme_wizard.py::test_tc_187_effective_to_must_be_after_effective_from_and_may_be_empty |
| TC-188 | Text that is not a real date is rejected | test_f414_new_scheme_wizard.py::test_tc_188_text_that_is_not_a_real_date_is_rejected |
| TC-189 | Messages show again at View and Publish and the step gets a warning mark | test_f414_new_scheme_wizard.py::test_tc_189_messages_show_again_at_view_and_the_steps_get_a_warning_mark |
| TC-190 | Step 2 shows nationalities, bands and match rule with defaults | test_f414_new_scheme_wizard.py::test_tc_190_step_2_shows_nationalities_bands_and_match_rule_with_defaults |
| TC-191 | At least one nationality is required | test_f414_new_scheme_wizard.py::test_tc_191_at_least_one_nationality_is_required |
| TC-192 | At least one income band is required | test_f414_new_scheme_wizard.py::test_tc_192_at_least_one_income_band_is_required |
| TC-193 | A band needs From and To may be empty for no upper limit | test_f414_new_scheme_wizard.py::test_tc_193_a_band_needs_from_and_to_may_be_empty |
| TC-194 | From greater than To is not allowed | test_f414_new_scheme_wizard.py::test_tc_194_from_greater_than_to_is_not_allowed |
| TC-196 | MOEFAS step 3 shows the three levels and the value type | test_f414_new_scheme_wizard.py::test_tc_196_moefas_step_3_shows_the_three_levels_and_the_value_type |
| TC-197 | Choosing a fee component adds a column at once with 0 in every row | test_f414_new_scheme_wizard.py::test_tc_197_choosing_a_fee_component_adds_a_column_with_zero_in_every_row |
| TC-198 | Several components can be added and a column can be removed with the cross | test_f414_new_scheme_wizard.py::test_tc_198_components_can_be_added_and_removed_with_the_cross |
| TC-200 | Changing the value type changes the unit of the cells | test_f414_new_scheme_wizard.py::test_tc_200_changing_the_value_type_changes_the_unit_of_the_cells |
| TC-201 | SBFAS step 3 shows one row per grade the school offers | test_f414_new_scheme_wizard.py::test_tc_201_sbfas_step_3_shows_one_row_per_grade_of_the_school |
| TC-202 | SBFAS component columns behave like MOEFAS | test_f414_new_scheme_wizard.py::test_tc_202_sbfas_component_columns_behave_like_moefas |
| TC-203 | SBFAS step 1 uses a tier name and the same dates as MOEFAS | test_f414_new_scheme_wizard.py::test_tc_203_sbfas_step_1_uses_a_tier_name_and_the_same_dates |
| TC-204 | Percentage cells accept 0 and 100 | test_f414_new_scheme_wizard.py::test_tc_204_percentage_cells_accept_0_and_100 |
| TC-205 | Percentage cells reject values below 0 and above 100 and empty cells | test_f414_new_scheme_wizard.py::test_tc_205_percentage_cells_reject_values_below_0_above_100_and_empty |
| TC-206 | Percentage cells accept at most two decimals | test_f414_new_scheme_wizard.py::test_tc_206_percentage_cells_accept_at_most_two_decimals |
| TC-207 | Fixed amount cells accept 0 or more and reject negative values | test_f414_new_scheme_wizard.py::test_tc_207_fixed_amount_cells_accept_0_or_more_and_reject_negative_values |
| TC-208 | An empty fixed amount cell is rejected | test_f414_new_scheme_wizard.py::test_tc_208_an_empty_fixed_amount_cell_is_rejected |
| TC-209 | Steps can be opened in any order and keep their values | test_f414_new_scheme_wizard.py::test_tc_209_steps_open_in_any_order_and_keep_their_values |
| TC-210 | Save draft with a name creates a Draft row | test_f414_new_scheme_wizard.py::test_tc_210_save_draft_with_a_name_creates_a_draft_row |
| TC-211 | Draft without a name is not saved | test_f414_new_scheme_wizard.py::test_tc_211_draft_without_a_name_is_not_saved |
| TC-212 | Edit reopens the draft with the saved values | test_f414_new_scheme_wizard.py::test_tc_212_edit_reopens_the_draft_with_the_saved_values |
| TC-213 | Discard and Cancel leave the wizard without saving | test_f414_new_scheme_wizard.py::test_tc_213_discard_and_cancel_leave_the_wizard_without_saving |
| TC-214 | View opens the review with General, Eligibility and Subsidy | test_f415_review_and_publish.py::test_tc_214_view_opens_the_review_with_general_eligibility_and_subsidy |
| TC-215 | Publish makes the scheme view only and adds an Upcoming row | test_f415_review_and_publish.py::test_tc_215_publish_makes_the_scheme_view_only_and_adds_an_upcoming_row |
| TC-216 | Back to edit returns to the wizard with the values kept | test_f415_review_and_publish.py::test_tc_216_back_to_edit_returns_to_the_wizard_with_the_values_kept |
| TC-217 | A scheme with errors cannot be published | test_f415_review_and_publish.py::test_tc_217_a_scheme_with_errors_cannot_be_published |
| TC-219 | A MOEFAS scheme overlapping the effective period of another is blocked | test_f415_review_and_publish.py::test_tc_219_a_moefas_scheme_overlapping_the_effective_period_is_blocked |
| TC-220 | A MOEFAS form period overlapping another form period is blocked | test_f415_review_and_publish.py::test_tc_220_a_moefas_form_period_overlapping_another_form_period_is_blocked |
| TC-221 | Periods that touch without overlapping are allowed | test_f415_review_and_publish.py::test_tc_221_periods_that_touch_without_overlapping_are_allowed |
| TC-222 | SBFAS with the same name and an overlapping period is blocked | test_f415_review_and_publish.py::test_tc_222_sbfas_with_the_same_name_and_an_overlapping_period_is_blocked |
| TC-223 | SBFAS with a different name in the same period is allowed | test_f415_review_and_publish.py::test_tc_223_sbfas_with_a_different_name_in_the_same_period_is_allowed |
| TC-224 | The same SBFAS name in another school is allowed | test_f415_review_and_publish.py::test_tc_224_the_same_sbfas_name_in_another_school_is_allowed |
| TC-225 | A draft with overlapping dates can be saved and fails only at Publish | test_f415_review_and_publish.py::test_tc_225_a_draft_with_overlapping_dates_fails_only_at_publish |
| TC-226 | Publishing sets the Effective to of an earlier scheme with no end date | test_f415_review_and_publish.py::test_tc_226_publishing_sets_the_effective_to_of_an_earlier_scheme_with_no_end_date |
| TC-227 | An earlier scheme that already has an end date is left unchanged | test_f415_review_and_publish.py::test_tc_227_an_earlier_scheme_that_already_has_an_end_date_is_left_unchanged |
| TC-228 | An earlier SBFAS scheme of the same name gets the day before as Effective to | test_f415_review_and_publish.py::test_tc_228_an_earlier_sbfas_scheme_of_the_same_name_gets_the_day_before_as_effective_to |
| TC-229 | Published rows offer View and Add fee and no Edit | test_f415_review_and_publish.py::test_tc_229_published_rows_offer_view_and_add_fee_and_no_edit |
| TC-231 | Add fee is offered on Active and Upcoming schemes only | test_f416_add_fee.py::test_tc_231_add_fee_is_offered_on_active_and_upcoming_schemes_only |
| TC-232 | Add fee dialog lists only components not yet in the scheme and shows the others read only | test_f416_add_fee.py::test_tc_232_add_fee_dialog_lists_missing_components_and_shows_the_others_read_only |
| TC-233 | Choosing a component adds an editable column that can be removed | test_f416_add_fee.py::test_tc_233_choosing_a_component_adds_an_editable_column_that_can_be_removed |
| TC-234 | Add to scheme stays disabled for invalid new cells | test_f416_add_fee.py::test_tc_234_add_to_scheme_stays_disabled_for_invalid_new_cells<br>test_f416_add_fee.py::test_tc_234_the_limits_0_and_100_are_accepted |
| TC-236 | Add to scheme saves the new component and shows the toast | test_f416_add_fee.py::test_tc_236_add_to_scheme_saves_the_new_component_and_shows_the_toast |
| TC-237 | The addition is recorded with the date and the user | test_f416_add_fee.py::test_tc_237_the_addition_is_recorded_with_the_date_and_the_user |
| TC-238 | Existing components cannot be changed after the addition | test_f416_add_fee.py::test_tc_238_existing_components_cannot_be_changed_after_the_addition |
| TC-241 | Add fee works the same on an SBFAS scheme | test_f416_add_fee.py::test_tc_241_add_fee_works_the_same_on_an_sbfas_scheme |
| TC-242 | Close form now (demo) dialog explains what will happen | test_f417_close_form_demo.py::test_tc_242_close_form_dialog_explains_what_will_happen |
| TC-243 | The button sets Form closes to today and runs the assessment | test_f417_close_form_demo.py::test_tc_243_the_button_sets_form_closes_to_today_and_runs_the_assessment |
| TC-244 | The button is offered only while the form is Open | test_f417_close_form_demo.py::test_tc_244_the_button_is_offered_only_while_the_form_is_open |
| TC-249 | The recommended tier is the first candidate scheme the household meets | test_f419_ml_recommendation.py::test_tc_249_recommended_tier_is_the_first_candidate_scheme_the_household_meets |
| TC-250 | A household above the lower bands gets Tier 3 | test_f419_ml_recommendation.py::test_tc_250_a_household_above_the_lower_bands_gets_tier_3 |
| TC-251 | No tier is recommended when the nationality is not allowed | test_f419_ml_recommendation.py::test_tc_251_no_tier_is_recommended_when_the_nationality_is_not_allowed |
| TC-255 | ML risk of the sample rows follows their Need Score | test_f419_ml_recommendation.py::test_tc_255_ml_risk_of_the_sample_rows_follows_their_need_score |
| TC-264 | Money shows as S$ with thousands separator and two decimals | test_f420_formats.py::test_tc_264_money_shows_as_s_dollar_with_thousands_separator_and_two_decimals<br>test_f420_formats.py::test_tc_264_sbfas_bands_use_two_decimals_too |
| TC-265 | Dates show as DD/MM/YYYY everywhere | test_f420_formats.py::test_tc_265_dates_show_as_dd_mm_yyyy_in_the_list_and_the_drawer<br>test_f420_formats.py::test_tc_265_the_scheme_list_shows_effective_dates_as_dd_mm_yyyy |
| TC-266 | Times show as HH:mm and use Singapore time | test_f420_formats.py::test_tc_266_times_show_as_hh_mm_on_a_24_hour_clock |

## Not automated

| Case | Title | Reason |
|---|---|---|
| TC-005 | Singapore PR application is SBFAS Pending for the school | Needs extra seed data: ENV-R4-01, SEED-R4-N9 |
| TC-007 | Submit is blocked when no form is open | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N22 |
| TC-008 | Submit is allowed when only the school SBFAS form is open | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N22 |
| TC-009 | Submit is allowed while the MOEFAS form is open and the application waits | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-013 | A form with one waiting application ranks 1 of 1 | Needs extra seed data: ENV-R4-01, SEED-R4-N11 |
| TC-015 | The form-close job runs by itself at the end of Form closes | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04 |
| TC-017 | Equal PCI: lower GHI ranks first | Needs extra seed data: ENV-R4-01, SEED-R4-N5 |
| TC-018 | Equal PCI and GHI: earliest submitted ranks first | Needs extra seed data: ENV-R4-01, SEED-R4-N6 |
| TC-019 | Equal PCI, GHI and submit time still gives one stable order | Needs extra seed data: ENV-R4-01, SEED-R4-N23 |
| TC-020 | Ranking uses the exact PCI and not the rounded display | Needs extra seed data: ENV-R4-01, SEED-R4-N12 |
| TC-024 | Effective from is today when the assessment runs after the scheme start | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N24 |
| TC-028 | Only PCI within its limit passes when the match rule is any | Needs extra seed data: ENV-R4-01, SEED-R4-N2 |
| TC-029 | Only GHI within its limit passes when the match rule is any | Needs extra seed data: ENV-R4-01, SEED-R4-N3 |
| TC-030 | Values equal to the limits pass | Needs extra seed data: ENV-R4-01, SEED-R4-N1 |
| TC-031 | Values just above the limits fail | Needs extra seed data: ENV-R4-01, SEED-R4-N4 |
| TC-033 | Match rule all needs every selected band to pass | Needs extra seed data: ENV-R4-01, SEED-R4-N8 |
| TC-037 | Fail with Also consider for SBFAS No is Rejected with the reason and an email | Needs extra seed data: ENV-R4-01, SEED-R4-N7 |
| TC-040 | No more MOEFAS applications are accepted after the assessment | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04 |
| TC-044 | Decide requests on a MOEFAS application are rejected by the server | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-057 | Ten rows fit on one page and the eleventh opens page 2 | Needs extra seed data: ENV-R4-01, SEED-R4-N25 |
| TC-062 | This year counts decisions of the current calendar year only | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N14 |
| TC-064 | A student who moved to another school is listed by the new school only | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N13 |
| TC-086 | Submitted filter includes the day 7 and the day 30 and excludes the day before | Needs extra seed data: ENV-R4-01, SEED-R4-N10 |
| TC-095 | Changing a filter or the search returns to page 1 | Needs extra seed data: ENV-R4-01, SEED-R4-N25 |
| TC-098 | Export includes the rows of every page | Needs extra seed data: ENV-R4-01, SEED-R4-N25 |
| TC-101 | A student name that starts with = is exported as text | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N26 |
| TC-108 | Two applications of one student under the same MOEFAS scheme | Blocked: no BA rule yet, the expected result cannot be written (see the assumption of the case) |
| TC-119 | A red note appears when the school has no SBFAS scheme for the period | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N15 |
| TC-123 | A School Admin of another school cannot decide the application | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-125 | Candidate tiers are the published school schemes whose form period holds the submit date | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N16 |
| TC-126 | When no scheme has the submit date in its form period the schemes in effect today are listed | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N16 |
| TC-133 | Approve cannot be confirmed when the school has no candidate scheme | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N15 |
| TC-138 | Effective from is the scheme start or today when the scheme is already in effect | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N16 |
| TC-151 | Parent receives an email with the reason | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-05 |
| TC-153 | A second user deciding the same application gets the already decided message | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-03 |
| TC-154 | Two approvals at the same moment save one decision | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-03 |
| TC-156 | A failed save leaves the application Pending | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-160 | A Parent cannot open the F4 screens | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-161 | An unauthenticated user is sent to sign in | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-162 | A School Admin opening an application of another school is refused | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-163 | The list API ignores a changed school filter for a School Admin | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-164 | A School Admin cannot open a MOEFAS application | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-165 | MOE HQ cannot open SBFAS schemes and a School Admin cannot open MOEFAS schemes | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-175 | Scheme status follows the effective dates | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N17 |
| TC-176 | Application form badge follows the form period | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N17 |
| TC-195 | Allowed nationalities decide where a new application goes | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N9 |
| TC-199 | Only active fee components of Function 3 are offered | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N19 |
| TC-218 | The published scheme drives the limits of later applications | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04 |
| TC-230 | A published scheme cannot be changed through the API | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-235 | Add fee is not offered for a Closed scheme by any route | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02 |
| TC-239 | Students already granted the scheme get the new subsidy on open fees | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N20 |
| TC-240 | Future fees of the added component follow the scheme automatically | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N20 |
| TC-245 | MOEFAS approval applies the level subsidy to outstanding and later fees | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-07, ENV-R4-04, SEED-R4-N21 |
| TC-246 | SBFAS approval applies the grade subsidy of the chosen scheme | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N21 |
| TC-247 | Every decision sends one email to the parent | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-05 |
| TC-248 | A MOEFAS application that goes to SBFAS does not send a rejection email | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-05, SEED-R4-N7 |
| TC-252 | The last tier within 5 % of its limit is recommended when none is met | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N27 |
| TC-253 | Candidates are the schemes whose form period holds the submit date | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N16 |
| TC-254 | Without a scheme the recommendation is a dash and the drawer shows the red note | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, SEED-R4-N15 |
| TC-256 | Need Score 75.00 is High and 74.99 is Medium | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-257 | Need Score 50.00 is Medium and 49.99 is Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-258 | Deny rule DENY-NO-CHILDREN gives Need Score 0 and ML risk Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-259 | Deny rule DENY-ONLY-CHILDREN gives Need Score 0 and ML risk Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-260 | Deny rule DENY-INVALID-SIZE gives Need Score 0 and ML risk Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-261 | Deny rule DENY-WORKERS-EXCEED-SIZE gives Need Score 0 and ML risk Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-262 | Deny rule DENY-NEGATIVE-MONTHS gives Need Score 0 and ML risk Low | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-263 | Need Score weights are 0.70, 0.05, 0.10, 0.10 and 0.05 | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-06 |
| TC-267 | Times follow Singapore time whatever the browser time zone is | Needs the F4 build: F4 build with API (not available yet) Chrome (latest) Build: to be recorded at execution Needs: ENV-R4-02, ENV-R4-04 |
