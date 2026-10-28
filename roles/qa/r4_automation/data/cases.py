"""Metadata for all test cases from the case workbook."""
from __future__ import annotations

CASES = {'TC-001': {'id': 'TC-001',
            'scenario_id': 'TS-001',
            'title': 'Waiting MOEFAS application shows Pending and System check Waiting',
            'suite': 'F4.1 Submit routing',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412 (Aisha Rahman, T1801177H, Bukit View Primary, P3)\n'
                         'MOEFAS 2027 form is Open until 31/12/2026',
            'steps': '1. Open FAS applications.\n2. Search for 00412.\n3. Read the row.',
            'expected': '1. The row shows Scheme MOEFAS, Submitted 17/10/2026, System check Waiting and Status '
                        'Pending.\n'
                        '2. Tier and ML recommendation show a dash.',
            'review': 'Approve'},
 'TC-002': {'id': 'TC-002',
            'scenario_id': 'TS-001',
            'title': 'Waiting MOEFAS drawer explains the wait and records the submit in History',
            'suite': 'F4.1 Submit routing',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412',
            'steps': '1. Open FAS applications and click View on APP-2026-00412.\n'
                     '2. Read the Eligibility check block and the last row of History.',
            'expected': '1. The History has an "Uploaded by Lan Nguyen" row at 17/10/2026 09:12 (paper source) and a '
                        'Submitted row at 17/10/2026 09:20.\n'
                        '2. The last History row reads "Waiting for the MOEFAS form to close on 31/12/2026".\n'
                        '3. The status stays Pending and the drawer has no Approve or Reject button.',
            'review': 'Approve'},
 'TC-003': {'id': 'TC-003',
            'scenario_id': 'TS-001',
            'title': 'Waiting MOEFAS application is not visible to the School Admin',
            'suite': 'F4.1 Submit routing',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00412 (Bukit View Primary student, MOEFAS, Waiting)',
            'steps': '1. Open FAS applications.\n'
                     '2. Open the All tab.\n'
                     '3. Search for 00412.\n'
                     '4. Read the cards and the tab counts.',
            'expected': '1. The All tab lists only APP-2026-00398 and APP-2026-00386.\n'
                        '2. Searching 00412 shows "No applications found."\n'
                        '3. The Pending card shows 1 and the Pending tab shows 1.',
            'review': 'Approve'},
 'TC-004': {'id': 'TC-004',
            'scenario_id': 'TS-002',
            'title': 'International student application is SBFAS Pending for the school',
            'suite': 'F4.1 Submit routing',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00398 (Daniel Ong, T1755501Q, International Student, Bukit View '
                         'Primary)',
            'steps': '1. Open FAS applications.\n'
                     '2. Search for 00398.\n'
                     '3. Read the row and open View.\n'
                     '4. Read the last row of History.',
            'expected': '1. Scheme is SBFAS, System check is a dash, Status is Pending.\n'
                        '2. The History has the row "SBFAS application (not eligible for MOEFAS by nationality)".\n'
                        '3. No MOEFAS decision or priority is shown.',
            'review': 'Approve'},
 'TC-005': {'id': 'TC-005',
            'scenario_id': 'TS-002',
            'title': 'Singapore PR application is SBFAS Pending for the school',
            'suite': 'F4.1 Submit routing',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N9',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: a Singapore PR student with an application made while the MOEFAS form is open '
                         '(SEED-R4-N9)',
            'steps': '1. Open FAS applications.\n'
                     '2. Find the application of the PR student.\n'
                     '3. Open View and read the History.',
            'expected': "1. Scheme is SBFAS and Status is Pending for the student's school.\n"
                        '2. The History has the row "SBFAS application (not eligible for MOEFAS by nationality)".',
            'review': 'Approve'},
 'TC-006': {'id': 'TC-006',
            'scenario_id': 'TS-002',
            'title': 'Singapore Citizen application is not routed to SBFAS at submit',
            'suite': 'F4.1 Submit routing',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: APP-2026-00377, APP-2026-00412, APP-2026-00410 (all Citizens)',
            'steps': '1. Open FAS applications.\n2. Filter Scheme = MOEFAS and Status = Pending.',
            'expected': '1. The three Citizen applications show Scheme MOEFAS and System check Waiting.\n'
                        '2. None of them shows Scheme SBFAS.',
            'review': 'Approve'},
 'TC-007': {'id': 'TC-007',
            'scenario_id': 'TS-003',
            'title': 'Submit is blocked when no form is open',
            'suite': 'F4.1 Submit routing',
            'page': 'F10 Parent FAS application',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N22',
            'preconditions': '1. The F4 build is connected to F5 and F10.\n'
                             "2. Today is set to a date when neither the MOEFAS form nor the child's school SBFAS form "
                             'is open (for example 01/01/2027).\n'
                             '3. Signed in as a Parent with a Citizen child.',
            'test_data': 'Today 01/01/2027\n'
                         'MOEFAS 2027 form closed on 31/12/2026\n'
                         'Next form opens on a date given by the seed (SEED-R4-N22)',
            'steps': '1. Open the FAS application in F10.\n2. Fill the form and submit.',
            'expected': '1. The submit is blocked.\n'
                        '2. The screen shows "the FAS application form is closed (next opens DD/MM/YYYY)" with the '
                        'next opening date.\n'
                        '3. No application is created and nothing appears in F4.',
            'review': 'Approve'},
 'TC-008': {'id': 'TC-008',
            'scenario_id': 'TS-003',
            'title': 'Submit is allowed when only the school SBFAS form is open',
            'suite': 'F4.1 Submit routing',
            'page': 'F5 Paper applications',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N22',
            'preconditions': '1. The F4 build is connected to F5 and F10.\n'
                             "2. Today is set so the MOEFAS form is closed and the child's school SBFAS form is open.\n"
                             '3. Signed in as a School user entering a paper application.',
            'test_data': 'Student: a Singapore PR student of Bukit View Primary\n'
                         'School SBFAS form open, MOEFAS form closed (SEED-R4-N22)',
            'steps': '1. Enter the paper application for the PR student.\n'
                     '2. Submit.\n'
                     '3. Open FAS applications as the school.',
            'expected': '1. The submit is accepted.\n'
                        '2. An SBFAS application with Status Pending appears in the school list.',
            'review': 'Approve'},
 'TC-009': {'id': 'TC-009',
            'scenario_id': 'TS-003',
            'title': 'Submit is allowed while the MOEFAS form is open and the application waits',
            'suite': 'F4.1 Submit routing',
            'page': 'F10 Parent FAS application',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is connected to F5 and F10.\n'
                             '2. Today is 18/10/2026 and the MOEFAS 2027 form is Open.\n'
                             '3. Signed in as a Parent with a Citizen child.',
            'test_data': 'Child: a Singapore Citizen student of Bukit View Primary',
            'steps': '1. Submit a FAS application in F10.\n'
                     '2. Open FAS applications as MOE HQ and find the new application.',
            'expected': '1. The application is MOEFAS, linked to MOEFAS 2027, Status Pending and System check '
                        'Waiting.\n'
                        '2. The History has "Submitted" and "Waiting for the MOEFAS form to close on 31/12/2026".',
            'review': 'Approve'},
 'TC-010': {'id': 'TC-010',
            'scenario_id': 'TS-004',
            'title': 'Closing the form ranks the waiting applications by lowest PCI first',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme: MOEFAS 2027 (3 waiting)\n'
                         'Applications: 00377 (PCI 1,030.00), 00412 (PCI 1,087.50), 00410 (PCI 1,300.00)',
            'steps': '1. Open MOEFAS schemes.\n'
                     '2. Read the Application form cell of MOEFAS 2027.\n'
                     '3. Click Close form now (demo) and read the dialog.\n'
                     '4. Click Close form and assess.\n'
                     '5. Open View on 00377, 00412 and 00410 and read their History.',
            'expected': '1. Before: the form cell shows "Open" and "3 waiting".\n'
                        '2. The dialog "Close the application form now?" (DEMO ONLY · MOEFAS 2027) says the form '
                        'closes today and no more MOEFAS applications are accepted.\n'
                        '3. It says the system ranks the 3 waiting applications by lowest per capita income first, '
                        'then lowest household income, then earliest submitted.\n'
                        "4. It says rules met means approved from 01/01/2027 and not met means the school's SBFAS if "
                        'the parent agreed, otherwise rejected.\n'
                        '5. A toast reads "Form closed. Applications were ranked by need and assessed."\n'
                        '6. The History of 00377 has "Form closed · priority 1 of 3 (lowest per capita income '
                        'first)".\n'
                        '7. The History of 00412 has priority 2 of 3 and the History of 00410 has priority 3 of 3.',
            'review': 'Approve'},
 'TC-011': {'id': 'TC-011',
            'scenario_id': 'TS-004',
            'title': 'Priority n of N is saved and shown in the Decision block',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00377 (priority 1 of 3)',
            'steps': '1. Open FAS applications and click View on 00377.\n2. Read the Decision block.',
            'expected': '1. The Decision block shows "Priority" with "1 of 3 (lowest per capita income first)".',
            'review': 'Approve'},
 'TC-012': {'id': 'TC-012',
            'scenario_id': 'TS-004',
            'title': 'Only waiting MOEFAS applications of the closing scheme are ranked',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Unchanged applications: 00390, 00381, 00328, 00301 (MOEFAS decided earlier), 00398, 00386 '
                         '(SBFAS)',
            'steps': '1. Open FAS applications.\n'
                     '2. Open View on 00390 and 00328.\n'
                     '3. Check the status of 00398 and 00386.',
            'expected': '1. 00390 still shows "Priority 1 of 4" and 00328 still shows "Priority 4 of 4".\n'
                        '2. 00398 is still SBFAS Pending and 00386 is still SBFAS Approved Tier 3.\n'
                        '3. No decided application gets a new History row.',
            'review': 'Approve'},
 'TC-013': {'id': 'TC-013',
            'scenario_id': 'TS-004',
            'title': 'A form with one waiting application ranks 1 of 1',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N11',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme with exactly one waiting application (SEED-R4-N11)',
            'steps': '1. Open MOEFAS schemes and read the waiting count of that scheme.\n'
                     '2. Click Close form now (demo) and confirm.\n'
                     '3. Open View on the application.',
            'expected': '1. The waiting count is 1.\n'
                        '2. The History has "Form closed · priority 1 of 1 (lowest per capita income first)".\n'
                        '3. The application is assessed (Approved, SBFAS Pending or Rejected by its limits and the '
                        'parent choice).',
            'review': 'Approve'},
 'TC-014': {'id': 'TC-014',
            'scenario_id': 'TS-004',
            'title': 'Closing a form with no waiting application changes nothing',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Scheme: MOEFAS 2027 (already assessed, 0 waiting)',
            'steps': '1. Open MOEFAS schemes.\n'
                     '2. If Close form now (demo) is shown, click it and read the dialog.\n'
                     '3. Confirm.\n'
                     '4. Open FAS applications and compare the rows with the state before the click.',
            'expected': '1. The dialog says it ranks 0 waiting applications.\n'
                        '2. No application changes status and no History row is added.\n'
                        '3. No error is shown.',
            'review': 'Draft'},
 'TC-015': {'id': 'TC-015',
            'scenario_id': 'TS-004',
            'title': 'The form-close job runs by itself at the end of Form closes',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04',
            'preconditions': '1. The F4 build runs the form-close job on a schedule.\n'
                             '2. Today is set to 31/12/2026 before the end of the day.\n'
                             '3. The MOEFAS 2027 form has the 3 waiting applications of the seed.',
            'test_data': 'Scheme MOEFAS 2027, Form closes 31/12/2026\nApplications 00377, 00412, 00410',
            'steps': '1. Check the scheme and the 3 applications at 23:00 on 31/12/2026.\n'
                     '2. Move the clock past the end of 31/12/2026.\n'
                     '3. Check the scheme and the applications again.',
            'expected': '1. At 23:00 the scheme shows "Open 3 waiting" and the applications are Pending with System '
                        'check Waiting.\n'
                        '2. After the end of the day the scheme shows "Assessed 31/12/2026".\n'
                        '3. The applications show priority 1, 2 and 3 of 3 and the same outcomes as with the demo '
                        'button.',
            'review': 'Draft'},
 'TC-016': {'id': 'TC-016',
            'scenario_id': 'TS-005',
            'title': 'Ranking follows PCI and not the submit time',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Submit order: 00410 (16/10/2026), then 00412 (17/10/2026 09:20), then 00377 (17/10/2026 '
                         '10:05)\n'
                         'PCI order: 00377 (1,030.00), 00412 (1,087.50), 00410 (1,300.00)',
            'steps': '1. Open View on 00410, 00412 and 00377.\n'
                     '2. Read the priority in the History or Decision block of each.',
            'expected': '1. 00377 has priority 1 of 3, 00412 has priority 2 of 3 and 00410 has priority 3 of 3.\n'
                        '2. The earliest submitted application (00410) is last because its PCI is the highest.',
            'review': 'Approve'},
 'TC-017': {'id': 'TC-017',
            'scenario_id': 'TS-005',
            'title': 'Equal PCI: lower GHI ranks first',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N5',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Two waiting applications with the same PCI 1,000.00:\n'
                         'Application A: GHI 4,000.00, household size 4\n'
                         'Application B: GHI 3,000.00, household size 3\n'
                         '(SEED-R4-N5)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n'
                     '2. Open View on A and B and read the priority.',
            'expected': '1. B (GHI 3,000.00) has the lower priority number than A (GHI 4,000.00).\n'
                        '2. Both Histories show "Form closed · priority n of N".',
            'review': 'Approve'},
 'TC-018': {'id': 'TC-018',
            'scenario_id': 'TS-005',
            'title': 'Equal PCI and GHI: earliest submitted ranks first',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N6',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Two waiting applications with PCI 1,000.00 and GHI 4,000.00:\n'
                         'Application C submitted 10/10/2026 09:00\n'
                         'Application D submitted 10/10/2026 09:30\n'
                         '(SEED-R4-N6)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n'
                     '2. Open View on C and D and read the priority.',
            'expected': '1. C has the lower priority number than D.',
            'review': 'Approve'},
 'TC-019': {'id': 'TC-019',
            'scenario_id': 'TS-005',
            'title': 'Equal PCI, GHI and submit time still gives one stable order',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N23',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Two waiting applications with the same PCI, GHI and submit time (SEED-R4-N23)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n'
                     '2. Open View on both and read the priority.',
            'expected': '1. The two applications get different priorities, for example 1 of 2 and 2 of 2.\n'
                        '2. The lower Application ID has the lower priority number.\n'
                        '3. Repeating the setup gives the same order.',
            'review': 'Draft'},
 'TC-020': {'id': 'TC-020',
            'scenario_id': 'TS-005',
            'title': 'Ranking uses the exact PCI and not the rounded display',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N12',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application E: GHI 6,525.00, household size 6, PCI 1,087.50 (1,088 when rounded)\n'
                         'Application F: GHI 4,352.00, household size 4, PCI 1,088.00\n'
                         '(SEED-R4-N12)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n'
                     '2. Open View on E and F and read the priority.',
            'expected': '1. E has the lower priority number than F because 1,087.50 is lower than 1,088.00.\n'
                        '2. If the rounded values were used, F would rank first because its GHI is lower.',
            'review': 'Draft'},
 'TC-021': {'id': 'TC-021',
            'scenario_id': 'TS-006',
            'title': 'A passing application is approved by the system',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00377 (Nur Aisyah, GHI 4,120.00, PCI 1,030.00)\n'
                         'Scheme MOEFAS 2027 limits: GHI up to S$ 4,200.00 or PCI up to S$ 1,050.00',
            'steps': '1. Open FAS applications and read the row of 00377.\n2. Open View and read the Decision block.',
            'expected': '1. The row shows Status Approved, System check Pass, Tier and ML recommendation as a dash.\n'
                        '2. The Decision block shows Result Approved and "Granted · MOEFAS (MOEFAS 2027) · from '
                        '01/01/2027".\n'
                        '3. It shows Priority "1 of 3 (lowest per capita income first)".\n'
                        '4. Decided by shows "System (auto-approved)" with the date 18/10/2026 and a time in HH:mm.',
            'review': 'Approve'},
 'TC-022': {'id': 'TC-022',
            'scenario_id': 'TS-006',
            'title': 'History of an automatic approval lists priority, approval and the email',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00377',
            'steps': '1. Open View on 00377.\n2. Read the History from the top.',
            'expected': '1. The History is in this order (oldest first): Submitted, "Waiting for the MOEFAS form to '
                        'close on 31/12/2026", "Form closed · priority 1 of 3 (lowest per capita income first)", '
                        '"MOEFAS rules met · approved automatically", "Email with result sent to parent".',
            'review': 'Approve'},
 'TC-023': {'id': 'TC-023',
            'scenario_id': 'TS-006',
            'title': 'Effective from is the scheme Effective from when the scheme starts later',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00377 assessed on 18/10/2026\n'
                         'Scheme MOEFAS 2027 Effective from 01/01/2027',
            'steps': '1. Open View on 00377.\n2. Read the Effective from date in the Decision block.',
            'expected': '1. The Decision block shows "from 01/01/2027", not 18/10/2026.',
            'review': 'Approve'},
 'TC-024': {'id': 'TC-024',
            'scenario_id': 'TS-006',
            'title': 'Effective from is today when the assessment runs after the scheme start',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N24',
            'preconditions': '1. The F4 build runs the form-close job on a schedule.\n'
                             '2. The job is delayed until after the scheme Effective from.',
            'test_data': 'Scheme: Form closes 31/12/2026, Effective from 01/01/2027\n'
                         'The job runs on 05/01/2027 (SEED-R4-N24)\n'
                         'One waiting application that passes',
            'steps': '1. Set today to 05/01/2027 and run the form-close job.\n2. Open View on the application.',
            'expected': '1. The Decision block shows "from 05/01/2027" (today), not 01/01/2027.',
            'review': 'Approve'},
 'TC-025': {'id': 'TC-025',
            'scenario_id': 'TS-006',
            'title': 'Cards and tab counts update after the automatic decisions',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state: cards 9, 3, 4, 1. Tabs Pending 4, All 9, Approved 4, Rejected 1.',
            'steps': '1. Read the cards and tabs.\n'
                     '2. Close the MOEFAS 2027 form with Close form now (demo).\n'
                     '3. Open FAS applications again and read the cards and tabs.',
            'expected': '1. Before: Total 9, MOEFAS approved 3, Approved 4, Rejected 1. Tabs Pending 4, All 9, '
                        'Approved 4, Rejected 1.\n'
                        '2. After: Total 9, MOEFAS approved 4, Approved 5, Rejected 1. Tabs Pending 3, All 9, Approved '
                        '5, Rejected 1.',
            'review': 'Approve'},
 'TC-026': {'id': 'TC-026',
            'scenario_id': 'TS-006',
            'title': 'Automatically approved MOEFAS application is final and read only',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00377',
            'steps': '1. Open View on 00377.\n2. Look for any field to edit and any Approve or Reject button.',
            'expected': '1. The drawer shows no editable field and no button other than the close X.\n'
                        '2. The Status stays Approved.',
            'review': 'Approve'},
 'TC-027': {'id': 'TC-027',
            'scenario_id': 'TS-007',
            'title': 'Both GHI and PCI within the limits pass',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application 00377: GHI 4,120.00 (limit 4,200.00), PCI 1,030.00 (limit 1,050.00), Singapore '
                         'Citizen',
            'steps': '1. Open View on 00377.\n2. Read the Eligibility check rows.',
            'expected': '1. Nationality, GHI and PCI all show Pass.\n2. The application is Approved.',
            'review': 'Approve'},
 'TC-028': {'id': 'TC-028',
            'scenario_id': 'TS-007',
            'title': 'Only PCI within its limit passes when the match rule is any',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N2',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application G: GHI 4,201.00, household size 5, PCI 840.20, Citizen (SEED-R4-N2)\n'
                         'Scheme MOEFAS 2027, match rule any (GHI up to 4,200.00 or PCI up to 1,050.00)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n2. Open View on G.',
            'expected': '1. GHI shows Fail and PCI shows Pass.\n2. The application is Approved by the system.',
            'review': 'Approve'},
 'TC-029': {'id': 'TC-029',
            'scenario_id': 'TS-007',
            'title': 'Only GHI within its limit passes when the match rule is any',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N3',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application H: GHI 4,000.00, household size 2, PCI 2,000.00, Citizen (SEED-R4-N3)\n'
                         'Scheme MOEFAS 2027, match rule any',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n2. Open View on H.',
            'expected': '1. GHI shows Pass and PCI shows Fail.\n2. The application is Approved by the system.',
            'review': 'Approve'},
 'TC-030': {'id': 'TC-030',
            'scenario_id': 'TS-007',
            'title': 'Values equal to the limits pass',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N1',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application I: GHI 4,200.00, household size 4, PCI 1,050.00, Citizen (SEED-R4-N1)\n'
                         'Limits: GHI up to 4,200.00 or PCI up to 1,050.00',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n2. Open View on I.',
            'expected': '1. GHI shows Pass and PCI shows Pass because both limits are shown with "≤".\n'
                        '2. The application is Approved.',
            'review': 'Approve'},
 'TC-031': {'id': 'TC-031',
            'scenario_id': 'TS-007',
            'title': 'Values just above the limits fail',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N4',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application J: GHI 4,201.00, household size 4, PCI 1,050.25, Citizen (SEED-R4-N4)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n2. Open View on J.',
            'expected': '1. GHI shows Fail and PCI shows Fail.\n'
                        '2. The application is not approved and goes to SBFAS Pending or Rejected by the parent '
                        'choice.',
            'review': 'Approve'},
 'TC-032': {'id': 'TC-032',
            'scenario_id': 'TS-007',
            'title': 'Both GHI and PCI above the limits fail',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application 00412: GHI 4,350.00, PCI 1,087.50\nApplication 00410: GHI 5,200.00, PCI 1,300.00',
            'steps': '1. Open View on 00412 and 00410.\n2. Read the History.',
            'expected': '1. Both applications are no longer MOEFAS Pending.\n'
                        '2. The History of each shows the MOEFAS check as not eligible and the application sent to the '
                        "school's SBFAS.",
            'review': 'Approve'},
 'TC-033': {'id': 'TC-033',
            'scenario_id': 'TS-007',
            'title': 'Match rule all needs every selected band to pass',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N8',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme with match rule all (SEED-R4-N8)\n'
                         'Application K: GHI 4,000.00, household size 2, PCI 2,000.00',
            'steps': '1. Close the form of that scheme with Close form now (demo).\n2. Open View on K.',
            'expected': '1. GHI shows Pass and PCI shows Fail.\n'
                        '2. Because the rule is all, the application fails and is not approved.',
            'review': 'Approve'},
 'TC-034': {'id': 'TC-034',
            'scenario_id': 'TS-007',
            'title': 'Limits come from the scheme of the application',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application 00377 is linked to MOEFAS 2027 (GHI 4,200.00, PCI 1,050.00)\n'
                         'Application 00390 is linked to MOEFAS 2026 (GHI 4,000.00, PCI 1,000.00)',
            'steps': '1. Open View on 00377 and read the limits.\n2. Open View on 00390 and read the limits.',
            'expected': '1. 00377 shows the limits ≤ S$ 4,200.00 and ≤ S$ 1,050.00 and the scheme name MOEFAS 2027.\n'
                        '2. 00390 shows the limits ≤ S$ 4,000.00 and ≤ S$ 1,000.00 and the scheme name MOEFAS 2026.\n'
                        '3. 00377 passes only because the 2027 limits are used.',
            'review': 'Approve'},
 'TC-035': {'id': 'TC-035',
            'scenario_id': 'TS-008',
            'title': 'Fail with Also consider for SBFAS Yes becomes SBFAS Pending for the school',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Application: APP-2026-00412 (parent agreed to SBFAS)',
            'steps': '1. Open FAS applications and read the row of 00412.\n2. Open View and read the History.',
            'expected': '1. The row shows Scheme SBFAS, System check a dash, Status Pending, School Bukit View '
                        'Primary.\n'
                        '2. The History has "Form closed · priority 2 of 3" and the row "MOEFAS check: not eligible · '
                        'sent to the school\'s SBFAS (parent agreed)".',
            'review': 'Approve'},
 'TC-036': {'id': 'TC-036',
            'scenario_id': 'TS-008',
            'title': 'The school sees the transferred application with an ML recommendation',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Applications: 00412 (PCI 1,087.50) and 00410 (PCI 1,300.00)\n'
                         'School SBFAS 2027 schemes: Tier 1 PCI up to 600, Tier 2 601 to 1,000, Tier 3 1,001 to 1,500',
            'steps': '1. Open FAS applications.\n'
                     '2. Read the Pending tab and the Pending card.\n'
                     '3. Read the ML recommendation of 00412 and 00410.',
            'expected': '1. The Pending tab shows 3 rows: 00412, 00410 and 00398. The Pending card shows 3.\n'
                        '2. ML recommendation is Tier 3 for 00412 and for 00410.\n'
                        '3. Both rows have a Review button.',
            'review': 'Approve'},
 'TC-037': {'id': 'TC-037',
            'scenario_id': 'TS-008',
            'title': 'Fail with Also consider for SBFAS No is Rejected with the reason and an email',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N7',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application L: fails the limits and the parent did not ask for SBFAS (SEED-R4-N7)\n'
                         'Sample already in the prototype: APP-2026-00328 (Rejected, MOEFAS 2026)',
            'steps': '1. Close the MOEFAS form with Close form now (demo).\n'
                     '2. Open View on L.\n'
                     '3. Read the Decision block and the History.',
            'expected': '1. Status is Rejected and System check is Fail.\n'
                        '2. The Decision block shows Reason "Not eligible for MOEFAS" and Decided by "System".\n'
                        '3. The History has a row stating the application was closed because the parent did not ask '
                        'for SBFAS, and "Email with reason sent to parent".\n'
                        '4. No SBFAS application exists for the student.',
            'review': 'Draft'},
 'TC-038': {'id': 'TC-038',
            'scenario_id': 'TS-008',
            'title': 'A transferred SBFAS application is not visible to other schools',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo).\n'
                             '3. Signed in as School user MRS-0012, Meridian Secondary.',
            'test_data': 'Applications 00412 and 00410 belong to Bukit View Primary students',
            'steps': '1. Open FAS applications.\n2. Search for 00412 and 00410.\n3. Read the list.',
            'expected': '1. Both searches show "No applications found."\n'
                        '2. No Bukit View Primary student appears in any tab.',
            'review': 'Approve'},
 'TC-039': {'id': 'TC-039',
            'scenario_id': 'TS-009',
            'title': 'The scheme shows Assessed and no waiting count after processing',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Scheme: MOEFAS 2027',
            'steps': '1. Open MOEFAS schemes and read the Application form cell of MOEFAS 2027.',
            'expected': '1. The cell shows the form period, a badge, and "Assessed 18/10/2026".\n'
                        '2. The text "n waiting" is no longer shown.',
            'review': 'Draft'},
 'TC-040': {'id': 'TC-040',
            'scenario_id': 'TS-009',
            'title': 'No more MOEFAS applications are accepted after the assessment',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'F10 Parent FAS application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04',
            'preconditions': '1. The F4 build is connected to F5 and F10.\n'
                             '2. The MOEFAS 2027 form was assessed.\n'
                             '3. Signed in as a Parent with a Citizen child.',
            'test_data': 'Scheme MOEFAS 2027 shows Assessed 31/12/2026\nToday is 31/12/2026 after the job ran',
            'steps': '1. Try to submit a FAS application in F10 for the same year.',
            'expected': '1. The submit is blocked with the form closed message.\n'
                        '2. No MOEFAS application is added to MOEFAS 2027.',
            'review': 'Draft'},
 'TC-041': {'id': 'TC-041',
            'scenario_id': 'TS-009',
            'title': 'Earlier schemes keep their Assessed date and the new one starts waiting',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schemes MOEFAS 2025 (Closed), MOEFAS 2026 (Closed) and MOEFAS 2027 (Open, 3 waiting)',
            'steps': '1. Open MOEFAS schemes.\n2. Read the Application form cells of the 3 schemes.',
            'expected': '1. MOEFAS 2025 shows "Closed" and "Assessed 01/01/2025".\n'
                        '2. MOEFAS 2026 shows "Closed" and "Assessed 01/01/2026".\n'
                        '3. MOEFAS 2027 shows "Open" and "3 waiting".',
            'review': 'Approve'},
 'TC-042': {'id': 'TC-042',
            'scenario_id': 'TS-010',
            'title': 'MOE HQ has no Approve or Reject on any application',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: 00412 (MOEFAS Pending), 00398 (SBFAS Pending), 00386 (SBFAS Approved), 00328 '
                         '(MOEFAS Rejected)',
            'steps': '1. Open View on each of the four applications.\n2. Look at the drawer buttons.',
            'expected': '1. No drawer shows Approve or Reject.\n2. The list shows View, not Review, on every row.',
            'review': 'Approve'},
 'TC-043': {'id': 'TC-043',
            'scenario_id': 'TS-010',
            'title': 'The School Admin cannot decide a MOEFAS application',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00412 (MOEFAS Waiting)',
            'steps': '1. Open FAS applications.\n2. Search for 00412 in the All tab.',
            'expected': '1. The application is not listed.\n'
                        '2. No MOEFAS row, filter or button exists for the School Admin.',
            'review': 'Approve'},
 'TC-044': {'id': 'TC-044',
            'scenario_id': 'TS-010',
            'title': 'Decide requests on a MOEFAS application are rejected by the server',
            'suite': 'F4.2 MOEFAS ranking and assessment',
            'page': 'API (Approve and Reject)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build exposes the decision API.\n'
                             "2. Signed in as MOE HQ and as a School Admin of the student's school.",
            'test_data': 'Application: a Pending MOEFAS application (for example 00412)',
            'steps': '1. As MOE HQ, send an approve request for the MOEFAS application.\n'
                     '2. As MOE HQ, send a reject request for it.\n'
                     "3. As the School Admin of the student's school, send an approve request for it.\n"
                     '4. Open the application in the list.',
            'expected': '1. Each request is refused with HTTP 403 and no data is changed.\n'
                        '2. The application is still MOEFAS Pending with System check Waiting.',
            'review': 'Draft'},
 'TC-045': {'id': 'TC-045',
            'scenario_id': 'TS-011',
            'title': 'MOE HQ list shows the subtitle, Export button and note',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Menu path: Financial assistance > FAS applications',
            'steps': '1. Open Financial assistance > FAS applications.\n'
                     '2. Read the title, subtitle, the Export button and the note under the table.',
            'expected': '1. The subtitle reads "All schools. MOEFAS is assessed automatically by the system after its '
                        'application form closes. SBFAS is decided by each school."\n'
                        '2. The Export button is shown.\n'
                        '3. The note reads "MOEFAS has no tiers. Its applications wait until the application form '
                        'closes. The system then ranks them by need (lowest per capita income first) and approves or '
                        'rejects them automatically. SBFAS is decided by each school (view only here)."',
            'review': 'Approve'},
 'TC-046': {'id': 'TC-046',
            'scenario_id': 'TS-011',
            'title': 'MOE HQ cards show the base counts and ignore filters and search',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state: 9 applications (see Seed Data)',
            'steps': '1. Read the four cards.\n'
                     '2. Set School = Riverside Secondary and type "lee" in Search.\n'
                     '3. Read the four cards again.',
            'expected': '1. The cards read Total applications 9 (All schools), MOEFAS approved 3 (Approved '
                        'automatically), Approved 4 (MOEFAS and SBFAS), Rejected 1 (MOEFAS and SBFAS).\n'
                        '2. After the filter and the search the cards still read 9, 3, 4 and 1.',
            'review': 'Approve'},
 'TC-047': {'id': 'TC-047',
            'scenario_id': 'TS-011',
            'title': 'MOE HQ tabs show the counts and open on All',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state: Pending 4, All 9, Approved 4, Rejected 1',
            'steps': '1. Open FAS applications and note the selected tab.\n'
                     '2. Click Pending, Approved and Rejected in turn and read the rows.',
            'expected': '1. The tabs are Pending, All, Approved and Rejected with counts 4, 9, 4 and 1.\n'
                        '2. All is selected when the screen opens.\n'
                        '3. Pending lists 00377, 00412, 00410 and 00398. Approved lists 00390, 00386, 00381 and 00301. '
                        'Rejected lists 00328.',
            'review': 'Approve'},
 'TC-048': {'id': 'TC-048',
            'scenario_id': 'TS-011',
            'title': 'Tab counts stay fixed when filters or search change the rows',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Set School = Riverside Secondary.\n'
                     '2. Read the tab counts.\n'
                     '3. Type "aisha" in Search and read the tab counts again.',
            'expected': '1. The tab counts stay Pending 4, All 9, Approved 4, Rejected 1 in both steps.\n'
                        '2. The table shows only the matching rows.',
            'review': 'Draft'},
 'TC-049': {'id': 'TC-049',
            'scenario_id': 'TS-012',
            'title': 'MOE HQ table has the 12 columns in the right order',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Open FAS applications and read the table header.',
            'expected': '1. The columns are Application, Student, School, Grade, Scheme, Submitted, System check, '
                        'Tier, ML recommendation, ML risk, Status and an action column with View.',
            'review': 'Approve'},
 'TC-050': {'id': 'TC-050',
            'scenario_id': 'TS-012',
            'title': 'Application and Student cells use the required formats',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Row: APP-2026-00412, Aisha Rahman, T1801177H',
            'steps': '1. Read the Application and Student cells of 00412.',
            'expected': '1. Application reads APP-2026-00412 (APP-YYYY-NNNNN).\n'
                        '2. Student shows the name Aisha Rahman with the NRIC/FIN T1801177H under it.',
            'review': 'Approve'},
 'TC-051': {'id': 'TC-051',
            'scenario_id': 'TS-012',
            'title': 'System check shows Waiting, Pass, Fail or a dash by scheme and status',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Rows: 00377 (MOEFAS Pending), 00390 (MOEFAS Approved), 00328 (MOEFAS Rejected), 00398 (SBFAS '
                         'Pending)',
            'steps': '1. Read the System check cell of each row.',
            'expected': '1. 00377 shows Waiting.\n2. 00390 shows Pass.\n3. 00328 shows Fail.\n4. 00398 shows a dash.',
            'review': 'Approve'},
 'TC-052': {'id': 'TC-052',
            'scenario_id': 'TS-012',
            'title': 'Tier and ML recommendation follow the scheme and the decision',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Rows: 00386 (SBFAS Approved Tier 3, ML Tier 2), 00398 (SBFAS Pending, no tier fits), 00377 '
                         '(MOEFAS)',
            'steps': '1. Read the Tier and ML recommendation cells of 00386, 00398 and 00377.',
            'expected': '1. 00386 shows Tier 3 in Tier and Tier 2 in ML recommendation.\n'
                        '2. 00398 shows an empty Tier and a dash in ML recommendation.\n'
                        '3. 00377 shows a dash in both cells.',
            'review': 'Approve'},
 'TC-053': {'id': 'TC-053',
            'scenario_id': 'TS-012',
            'title': 'Grade shows a dash when the student has no class',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Rows: 00328 and 00381 (Lee Zhi Hao, Riverside Secondary, no class), 00412 (P3)',
            'steps': '1. Read the Grade cell of 00328, 00381 and 00412.',
            'expected': '1. 00328 and 00381 show a dash.\n2. 00412 shows P3.',
            'review': 'Approve'},
 'TC-054': {'id': 'TC-054',
            'scenario_id': 'TS-012',
            'title': 'ML risk and Status show only the allowed values',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Read the ML risk and Status columns for all 9 rows.',
            'expected': '1. ML risk is High for 00390, Low for 00328 and Medium for the 7 other rows.\n'
                        '2. Status is only Pending, Approved or Rejected.',
            'review': 'Approve'},
 'TC-055': {'id': 'TC-055',
            'scenario_id': 'TS-013',
            'title': 'List is sorted by Submitted, newest first',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Open FAS applications (All tab) and read the Application column from top to bottom.',
            'expected': '1. The order is 00377 (17/10/2026), 00412 (17/10/2026), 00410 (16/10/2026), 00398 '
                        '(14/10/2026), 00390 (14/11/2025), 00386 (12/11/2025), 00328 (07/11/2025), 00381 (16/10/2025), '
                        '00301 (20/09/2025).\n'
                        '2. Two rows of the same date list the later time first (00377 at 10:05 before 00412 at '
                        '09:20).',
            'review': 'Approve'},
 'TC-056': {'id': 'TC-056',
            'scenario_id': 'TS-013',
            'title': 'Footer shows the row range and paging buttons for one page',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state (9 rows)',
            'steps': '1. Read the footer under the table.',
            'expected': '1. The footer reads "Showing 1–9 of 9" with Previous and Next.\n'
                        '2. Neither button moves to another page.',
            'review': 'Approve'},
 'TC-057': {'id': 'TC-057',
            'scenario_id': 'TS-013',
            'title': 'Ten rows fit on one page and the eleventh opens page 2',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N25',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Seed A: exactly 10 applications (SEED-R4-N25)\nSeed B: 11 applications (SEED-R4-N25)',
            'steps': '1. Load seed A and open FAS applications.\n'
                     '2. Read the footer and the Next button.\n'
                     '3. Load seed B and open FAS applications.\n'
                     '4. Read the footer, click Next and read the footer again.',
            'expected': '1. With 10 rows the footer reads "Showing 1–10 of 10" and Next stays on the same page.\n'
                        '2. With 11 rows page 1 shows 10 rows and "Showing 1–10 of 11".\n'
                        '3. Page 2 shows 1 row and "Showing 11–11 of 11".',
            'review': 'Approve'},
 'TC-058': {'id': 'TC-058',
            'scenario_id': 'TS-013',
            'title': 'Empty result shows the message and an empty footer',
            'suite': 'F4.3 Applications list, MOE HQ',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search term: zzzz',
            'steps': '1. Type "zzzz" in Search.\n2. Read the table and the footer.',
            'expected': '1. The table shows "No applications found."\n'
                        '2. The footer reads "Showing 0–0 of 0".\n'
                        '3. No error appears.',
            'review': 'Approve'},
 'TC-059': {'id': 'TC-059',
            'scenario_id': 'TS-014',
            'title': 'School Admin sees only SBFAS applications of the own school',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Bukit View Primary has 6 applications (4 MOEFAS and 2 SBFAS: 00398 and 00386)',
            'steps': '1. Open FAS applications and open the All tab.\n2. Read the rows.',
            'expected': '1. Only APP-2026-00398 and APP-2026-00386 are listed.\n'
                        '2. No MOEFAS row (00412, 00410, 00390, 00301) is listed.\n'
                        '3. No application of another school is listed.',
            'review': 'Approve'},
 'TC-060': {'id': 'TC-060',
            'scenario_id': 'TS-014',
            'title': 'School Admin of a school without SBFAS applications sees an empty list',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user MRS-0012, Meridian Secondary.',
            'test_data': 'Meridian Secondary has one MOEFAS application (00377) and no SBFAS application',
            'steps': '1. Open FAS applications.\n2. Read the cards and the list.',
            'expected': '1. The list shows "No applications found."\n'
                        '2. The cards read Pending 0, SBFAS approved 0 and SBFAS rejected 0.\n'
                        '3. The MOEFAS application 00377 is not listed.',
            'review': 'Approve'},
 'TC-061': {'id': 'TC-061',
            'scenario_id': 'TS-014',
            'title': 'School cards show Pending, SBFAS approved and SBFAS rejected for this year',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary: 00398 Pending, 00386 Approved on 13/01/2026',
            'steps': '1. Read the three cards.',
            'expected': '1. The cards read Pending 1 (Pending SBFAS), SBFAS approved 1 (This year) and SBFAS rejected '
                        '0 (This year).',
            'review': 'Draft'},
 'TC-062': {'id': 'TC-062',
            'scenario_id': 'TS-014',
            'title': 'This year counts decisions of the current calendar year only',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N14',
            'preconditions': '1. The F4 build is running with a clock control.\n'
                             '2. Signed in as a School Admin of Bukit View Primary.',
            'test_data': 'Seed: one SBFAS approval decided on 31/12/2025 and one decided on 01/01/2026 (SEED-R4-N14)\n'
                         'Today 18/10/2026',
            'steps': '1. Open FAS applications and read the SBFAS approved card.\n'
                     '2. Set today to 01/01/2027 and read the card again.',
            'expected': '1. On 18/10/2026 the card counts only the decision of 01/01/2026.\n'
                        '2. On 01/01/2027 the card counts neither decision.',
            'review': 'Draft'},
 'TC-063': {'id': 'TC-063',
            'scenario_id': 'TS-014',
            'title': 'School tabs open on Pending and show counts',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary',
            'steps': '1. Open FAS applications and note the selected tab and the counts.\n'
                     '2. Click All, Approved and Rejected in turn.',
            'expected': '1. Pending is selected on opening. The counts are Pending 1, All 2, Approved 1 and Rejected '
                        'without a count.\n'
                        '2. Pending lists 00398. All lists 00398 and 00386. Approved lists 00386. Rejected shows "No '
                        'applications found."',
            'review': 'Approve'},
 'TC-064': {'id': 'TC-064',
            'scenario_id': 'TS-014',
            'title': 'A student who moved to another school is listed by the new school only',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N13',
            'preconditions': '1. The F4 build is connected to F3 (students and enrolment).\n'
                             '2. Signed in as a School Admin.',
            'test_data': 'Student: SBFAS applicant of Bukit View Primary transferred to Meridian Secondary '
                         '(SEED-R4-N13)',
            'steps': '1. Open FAS applications as a School Admin of Bukit View Primary and search for the student.\n'
                     '2. Open FAS applications as a School Admin of Meridian Secondary and search for the student.',
            'expected': '1. Bukit View Primary shows "No applications found."\n'
                        '2. Meridian Secondary lists the application, because it shows students currently enrolled in '
                        'the school.',
            'review': 'Approve'},
 'TC-065': {'id': 'TC-065',
            'scenario_id': 'TS-015',
            'title': 'School table has the 9 columns with Tier before ML recommendation',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary',
            'steps': '1. Open FAS applications and read the table header.',
            'expected': '1. The columns are Application, Student, Grade, Submitted, Tier, ML recommendation, ML risk, '
                        'Status and an action column.\n'
                        '2. There is no School, Scheme or System check column.',
            'review': 'Approve'},
 'TC-066': {'id': 'TC-066',
            'scenario_id': 'TS-015',
            'title': 'Review shows for Pending SBFAS and View for decided ones',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Rows: 00398 (Pending) and 00386 (Approved)',
            'steps': '1. Open the All tab.\n2. Read the action button of each row.\n3. Click View on 00386.',
            'expected': '1. 00398 shows Review (primary button) and 00386 shows View.\n'
                        '2. View opens the drawer for 00386 with no Approve or Reject button.',
            'review': 'Approve'},
 'TC-067': {'id': 'TC-067',
            'scenario_id': 'TS-015',
            'title': 'School table values for a pending and an approved SBFAS row',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Rows: 00398 and 00386',
            'steps': '1. Open the All tab.\n2. Read the cells of 00398 and 00386.',
            'expected': '1. 00398: Grade P2, Submitted 14/10/2026, Tier empty, ML recommendation a dash, ML risk '
                        'Medium, Status Pending.\n'
                        '2. 00386: Grade P4, Submitted 12/11/2025, Tier Tier 3, ML recommendation Tier 2, ML risk '
                        'Medium, Status Approved.',
            'review': 'Approve'},
 'TC-068': {'id': 'TC-068',
            'scenario_id': 'TS-015',
            'title': 'School list note explains Tier and MOE HQ only data',
            'suite': 'F4.4 Applications list, School Admin',
            'page': 'FAS applications (School Admin)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state',
            'steps': '1. Read the note under the table.',
            'expected': '1. The note reads "Tier is the SBFAS scheme your school grants. MOEFAS applications and '
                        'income details are visible to MOE HQ only."',
            'review': 'Approve'},
 'TC-069': {'id': 'TC-069',
            'scenario_id': 'TS-016',
            'title': 'Search by Application ID finds one application',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search terms: 00412, APP-2026-00412, app-2026-00412',
            'steps': '1. Type each search term in turn in Search.\n2. Read the rows after each term.',
            'expected': '1. Each term shows only APP-2026-00412.',
            'review': 'Approve'},
 'TC-070': {'id': 'TC-070',
            'scenario_id': 'TS-016',
            'title': 'Search by student name is a case-insensitive contains match',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search terms: aisha, AISHA, Rahman, lee zhi',
            'steps': '1. Type each search term in turn in Search.\n2. Read the rows after each term.',
            'expected': '1. aisha, AISHA and Rahman each show only 00412.\n2. lee zhi shows 00328 and 00381.',
            'review': 'Approve'},
 'TC-071': {'id': 'TC-071',
            'scenario_id': 'TS-016',
            'title': 'Search by NRIC/FIN matches the whole or a part of the number',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search terms: T1801177H, t1801177h, 1801177',
            'steps': '1. Type each search term in turn in Search.\n2. Read the rows after each term.',
            'expected': '1. Each term shows only 00412.',
            'review': 'Approve'},
 'TC-072': {'id': 'TC-072',
            'scenario_id': 'TS-016',
            'title': 'Search with no match shows the empty message',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search term: zzzz',
            'steps': '1. Type the term in Search.',
            'expected': '1. The table shows "No applications found." and no error.\n'
                        '2. Clearing the search shows all 9 rows again.',
            'review': 'Approve'},
 'TC-073': {'id': 'TC-073',
            'scenario_id': 'TS-016',
            'title': 'Search trims leading and trailing spaces',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search term: "  aisha  " (two spaces before and after)',
            'steps': '1. Type the term in Search.',
            'expected': '1. Only 00412 is shown, as for "aisha".',
            'review': 'Draft'},
 'TC-074': {'id': 'TC-074',
            'scenario_id': 'TS-016',
            'title': 'Search accepts up to 100 characters and warns above that',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Terms of 100 and 101 characters (letter a repeated)',
            'steps': '1. Type the 100-character term in Search.\n2. Type the 101-character term in Search.',
            'expected': '1. The 100-character term is accepted and shows "No applications found."\n'
                        '2. The 101-character term shows a helper text and does not run the search.',
            'review': 'Draft'},
 'TC-075': {'id': 'TC-075',
            'scenario_id': 'TS-016',
            'title': 'Special characters and script text are searched as plain text',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': "Terms: ' OR 1=1 --, <script>alert(1)</script>, %, _",
            'steps': '1. Type each term in turn in Search.\n2. Read the table after each term.',
            'expected': '1. Each term shows "No applications found." and no error.\n'
                        '2. No script runs and no alert opens.\n'
                        '3. % and _ do not match every row.',
            'review': 'Draft'},
 'TC-076': {'id': 'TC-076',
            'scenario_id': 'TS-016',
            'title': 'School Admin search never returns an application of another school',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Search terms: 00377 (Meridian), 00328 (Riverside), 00412 (Bukit View MOEFAS), Nur Aisyah',
            'steps': '1. Type each term in turn in Search.',
            'expected': '1. Each term shows "No applications found."',
            'review': 'Approve'},
 'TC-077': {'id': 'TC-077',
            'scenario_id': 'TS-017',
            'title': 'School filter lists the four schools and narrows the rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schools: Bukit View Primary, Meridian Secondary, North Vista Primary, Riverside Secondary',
            'steps': '1. Open the School filter and read the options.\n'
                     '2. Select each school in turn and read the rows.',
            'expected': '1. The options are All schools plus the four schools.\n'
                        '2. Bukit View Primary shows 00412, 00410, 00398, 00390, 00386, 00301.\n'
                        '3. Meridian Secondary shows 00377.\n'
                        '4. North Vista Primary shows "No applications found."\n'
                        '5. Riverside Secondary shows 00328 and 00381.',
            'review': 'Approve'},
 'TC-078': {'id': 'TC-078',
            'scenario_id': 'TS-017',
            'title': 'Scheme filter separates MOEFAS and SBFAS',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Select Scheme = MOEFAS and read the rows.\n2. Select Scheme = SBFAS and read the rows.',
            'expected': '1. MOEFAS shows 7 rows: 00377, 00412, 00410, 00390, 00328, 00381, 00301.\n'
                        '2. SBFAS shows 2 rows: 00398 and 00386.',
            'review': 'Approve'},
 'TC-079': {'id': 'TC-079',
            'scenario_id': 'TS-017',
            'title': 'Grade filter lists P1 to P6 and S1 to S4 and matches the class grade',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Open the Grade filter and read the options.\n'
                     '2. Select P3, P4, P5, S3 and P1 in turn and read the rows.',
            'expected': '1. The options are All plus P1 to P6 and S1 to S4.\n'
                        '2. P3 shows 00412 and 00301. P4 shows 00390 and 00386. P5 shows 00410. S3 shows 00377.\n'
                        '3. P1 shows "No applications found."\n'
                        '4. Students without a class (00328, 00381) are listed under no grade.',
            'review': 'Approve'},
 'TC-080': {'id': 'TC-080',
            'scenario_id': 'TS-017',
            'title': 'Tier filter matches the granted tier on decided rows and MOEFAS rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state. 00386 is granted Tier 3 and its ML recommendation is Tier 2.',
            'steps': '1. Open the Tier filter and read the options.\n'
                     '2. Select MOEFAS, SBFAS - Tier 1, SBFAS - Tier 2 and SBFAS - Tier 3 in turn and read the rows.',
            'expected': '1. The options are All, MOEFAS, SBFAS - Tier 1, SBFAS - Tier 2 and SBFAS - Tier 3.\n'
                        '2. MOEFAS shows the 7 MOEFAS rows.\n'
                        '3. Tier 1 and Tier 2 show "No applications found." (00386 is decided, so its ML Tier 2 is not '
                        'used).\n'
                        '4. Tier 3 shows 00386.',
            'review': 'Approve'},
 'TC-081': {'id': 'TC-081',
            'scenario_id': 'TS-017',
            'title': 'Tier filter matches the ML recommended tier on pending SBFAS rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'After the demo close: 00412 and 00410 are SBFAS Pending with ML recommendation Tier 3. 00398 '
                         'is SBFAS Pending with ML recommendation a dash.',
            'steps': '1. Select Tier = SBFAS - Tier 3 and read the rows.\n'
                     '2. Select Tier = SBFAS - Tier 2 and read the rows.',
            'expected': '1. Tier 3 shows 00412, 00410 and 00386.\n'
                        '2. Tier 2 shows "No applications found."\n'
                        '3. 00398 is not shown in any tier.',
            'review': 'Approve'},
 'TC-082': {'id': 'TC-082',
            'scenario_id': 'TS-017',
            'title': 'Only published school scheme names appear in the HQ Tier filter',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user BVP-0012.',
            'test_data': 'Draft SBFAS scheme named "Tier 4" saved by the school and never published',
            'steps': '1. In SBFAS schemes, start a new scheme named "Tier 4" and click Save draft.\n'
                     '2. Log out and sign in as MOE HQ.\n'
                     '3. Open FAS applications and open the Tier filter.',
            'expected': '1. The Tier filter lists only MOEFAS and SBFAS - Tier 1 to Tier 3.\n'
                        '2. "SBFAS - Tier 4" does not appear.',
            'review': 'Draft'},
 'TC-083': {'id': 'TC-083',
            'scenario_id': 'TS-017',
            'title': 'Status filter shows Pending, Approved or Rejected rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Select Status = Pending, Approved and Rejected in turn and read the rows.',
            'expected': '1. Pending shows 00377, 00412, 00410, 00398.\n'
                        '2. Approved shows 00390, 00386, 00381, 00301.\n'
                        '3. Rejected shows 00328.\n'
                        '4. The Status filter has only these three values.',
            'review': 'Approve'},
 'TC-084': {'id': 'TC-084',
            'scenario_id': 'TS-017',
            'title': 'ML risk filter shows Low, Medium or High rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Select ML risk = High, Low and Medium in turn and read the rows.',
            'expected': '1. High shows 00390.\n2. Low shows 00328.\n3. Medium shows the other 7 rows.',
            'review': 'Approve'},
 'TC-085': {'id': 'TC-085',
            'scenario_id': 'TS-017',
            'title': 'Submitted filter defaults to Any time and limits the range',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Today 18/10/2026',
            'steps': '1. Read the Submitted filter on opening.\n'
                     '2. Select Last 7 days and read the rows.\n'
                     '3. Select Last 30 days and read the rows.\n'
                     '4. Select Any time and read the rows.',
            'expected': '1. The filter opens on Any time and the table shows 9 rows.\n'
                        '2. Last 7 days shows 00377, 00412, 00410, 00398.\n'
                        '3. Last 30 days shows the same 4 rows.\n'
                        '4. Any time shows all 9 rows.',
            'review': 'Approve'},
 'TC-086': {'id': 'TC-086',
            'scenario_id': 'TS-017',
            'title': 'Submitted filter includes the day 7 and the day 30 and excludes the day before',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N10',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Today 18/10/2026\n'
                         'Seed applications submitted on 11/10/2026, 10/10/2026, 18/09/2026, 17/09/2026 (SEED-R4-N10)',
            'steps': '1. Select Last 7 days and read the rows.\n2. Select Last 30 days and read the rows.',
            'expected': '1. Last 7 days includes the application of 11/10/2026 and excludes the one of 10/10/2026.\n'
                        '2. Last 30 days includes the application of 18/09/2026 and excludes the one of 17/09/2026.',
            'review': 'Draft'},
 'TC-087': {'id': 'TC-087',
            'scenario_id': 'TS-018',
            'title': 'School filters are Search, Grade, Tier, Status, ML risk and Submitted',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary',
            'steps': '1. Read the filter bar.',
            'expected': '1. The filters are Search, Grade, Tier, Status, ML risk and Submitted.\n'
                        '2. There is no School filter and no Scheme filter.',
            'review': 'Approve'},
 'TC-088': {'id': 'TC-088',
            'scenario_id': 'TS-018',
            'title': 'Grade options follow the grades the school offers',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Bukit View Primary offers P1 to P6. Meridian Secondary offers S1 to S4.',
            'steps': '1. Open the Grade filter and read the options.\n'
                     '2. Log out and sign in as MRS-0012.\n'
                     '3. Open FAS applications and open the Grade filter.',
            'expected': '1. Bukit View Primary lists All and P1 to P6.\n2. Meridian Secondary lists All and S1 to S4.',
            'review': 'Approve'},
 'TC-089': {'id': 'TC-089',
            'scenario_id': 'TS-018',
            'title': 'Tier options are the names of the school SBFAS schemes',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Bukit View Primary SBFAS schemes: Tier 1, Tier 2, Tier 3',
            'steps': '1. Open the Tier filter and read the options.\n'
                     '2. Select Tier 3, Tier 2 and Tier 1 in turn and read the rows.',
            'expected': '1. The options are All, Tier 1, Tier 2 and Tier 3.\n'
                        '2. Tier 3 shows 00386 (granted Tier 3).\n'
                        '3. Tier 2 and Tier 1 show "No applications found."',
            'review': 'Approve'},
 'TC-090': {'id': 'TC-090',
            'scenario_id': 'TS-018',
            'title': 'School Tier filter matches the ML recommended tier on pending rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'After the demo close: 00412 and 00410 are Pending with ML recommendation Tier 3.',
            'steps': '1. Select Tier = Tier 3 and read the rows.\n2. Select Tier = Tier 2 and read the rows.',
            'expected': '1. Tier 3 shows 00412, 00410 and 00386.\n2. Tier 2 shows "No applications found."',
            'review': 'Approve'},
 'TC-091': {'id': 'TC-091',
            'scenario_id': 'TS-018',
            'title': 'School Status, ML risk and Submitted filters narrow the school rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Rows: 00398 (Pending, Medium, 14/10/2026) and 00386 (Approved, Medium, 12/11/2025)',
            'steps': '1. Open the All tab.\n'
                     '2. Select Status = Approved and read the rows.\n'
                     '3. Clear it and select ML risk = High and read the rows.\n'
                     '4. Clear it and select Submitted = Last 7 days and read the rows.',
            'expected': '1. Approved shows 00386.\n2. High shows "No applications found."\n3. Last 7 days shows 00398.',
            'review': 'Approve'},
 'TC-092': {'id': 'TC-092',
            'scenario_id': 'TS-019',
            'title': 'Filters combine with AND',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Select School = Bukit View Primary and Status = Pending and read the rows.\n'
                     '2. Select Scheme = SBFAS and Status = Pending and read the rows.\n'
                     '3. Select Grade = P3 and Scheme = MOEFAS and read the rows.\n'
                     '4. Select Status = Approved and ML risk = Low and read the rows.',
            'expected': '1. Bukit View Primary with Pending shows 00412, 00410, 00398.\n'
                        '2. SBFAS with Pending shows 00398.\n'
                        '3. P3 with MOEFAS shows 00412 and 00301.\n'
                        '4. Approved with Low shows "No applications found."',
            'review': 'Approve'},
 'TC-093': {'id': 'TC-093',
            'scenario_id': 'TS-019',
            'title': 'A tab and the Status filter combine with AND',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Open the Pending tab and select Status = Approved.\n'
                     '2. Open the Approved tab, clear the Status filter and type "lee" in Search.',
            'expected': '1. Pending with Approved shows "No applications found."\n'
                        '2. Approved with the search "lee" shows 00381 only.\n'
                        '3. The tab counts do not change.',
            'review': 'Draft'},
 'TC-094': {'id': 'TC-094',
            'scenario_id': 'TS-019',
            'title': 'Clearing a filter restores the rows',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Select Scheme = SBFAS.\n2. Select Scheme = All.',
            'expected': '1. After the first step 2 rows are shown. After the second step all 9 rows are shown again.',
            'review': 'Approve'},
 'TC-095': {'id': 'TC-095',
            'scenario_id': 'TS-019',
            'title': 'Changing a filter or the search returns to page 1',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N25',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Seed with 11 applications (SEED-R4-N25)',
            'steps': '1. Open FAS applications and click Next to go to page 2.\n'
                     '2. Select Scheme = MOEFAS.\n'
                     '3. Go to page 2 again if there is one, then type "a" in Search.',
            'expected': '1. After each change the table shows page 1 and the footer starts at "Showing 1".',
            'review': 'Approve'},
 'TC-096': {'id': 'TC-096',
            'scenario_id': 'TS-020',
            'title': 'Export file holds the columns of 3.4 and every row of the list',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state (9 rows). The browser asks for permission to download.',
            'steps': '1. Click Export.\n2. Open the downloaded file in a text editor.',
            'expected': '1. The file name is fas-applications.csv.\n'
                        '2. The header row is Application, Student, NRIC, School, Grade, Scheme, Submitted, System '
                        'check, Tier, ML recommendation, ML risk, Status.\n'
                        '3. The file has 9 data rows sorted by Submitted, newest first.',
            'review': 'Draft'},
 'TC-097': {'id': 'TC-097',
            'scenario_id': 'TS-020',
            'title': 'Export holds only the filtered and searched rows',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Filter Scheme = SBFAS, then the Approved tab with search "lee"',
            'steps': '1. Select Scheme = SBFAS and click Export.\n'
                     '2. Clear the filter, select the Approved tab, type "lee" in Search and click Export.\n'
                     '3. Open both files.',
            'expected': '1. The first file has the 2 SBFAS rows (00398, 00386).\n2. The second file has only 00381.',
            'review': 'Draft'},
 'TC-098': {'id': 'TC-098',
            'scenario_id': 'TS-020',
            'title': 'Export includes the rows of every page',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N25',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Seed with 11 applications (SEED-R4-N25)',
            'steps': '1. Click Export on page 1 and open the file.',
            'expected': '1. The file has 11 data rows, not only the 10 rows of page 1.',
            'review': 'Draft'},
 'TC-099': {'id': 'TC-099',
            'scenario_id': 'TS-020',
            'title': 'School Admin export omits School, Scheme and System check',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary',
            'steps': '1. Open the All tab and click Export.\n2. Open the file.',
            'expected': '1. The header row is Application, Student, NRIC, Grade, Submitted, Tier, ML recommendation, '
                        'ML risk, Status.\n'
                        '2. The file has the 2 SBFAS rows of the school and no row of another school.',
            'review': 'Draft'},
 'TC-100': {'id': 'TC-100',
            'scenario_id': 'TS-020',
            'title': 'Export of an empty list writes the header only',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Search term: zzzz',
            'steps': '1. Type the term in Search and click Export.\n2. Open the file.',
            'expected': '1. The file has the header row and no data row.',
            'review': 'Draft'},
 'TC-101': {'id': 'TC-101',
            'scenario_id': 'TS-020',
            'title': 'A student name that starts with = is exported as text',
            'suite': 'F4.6 Export',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N26',
            'preconditions': '1. The F4 build is running.\n2. Signed in as MOE HQ.',
            'test_data': 'Student named =HYPERLINK("http://example.test","x") (SEED-R4-N26)',
            'steps': '1. Click Export and open the file in a spreadsheet application.',
            'expected': '1. The cell shows the text of the name with a leading apostrophe or as plain text.\n'
                        '2. No formula runs and no link opens.',
            'review': 'Draft'},
 'TC-102': {'id': 'TC-102',
            'scenario_id': 'TS-021',
            'title': 'Pending MOEFAS drawer shows the header and the waiting note',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00377 (Nur Aisyah, Meridian Secondary, S3)',
            'steps': '1. Open FAS applications and click View on 00377.\n'
                     '2. Read the header and the blue note at the top of the Eligibility check.',
            'expected': '1. The header reads "MOEFAS REVIEW", APP-2026-00377 and "Nur Aisyah · Meridian Secondary".\n'
                        '2. The blue note reads "Waiting for the MOEFAS 2027 form to close on 31/12/2026. The system '
                        'then ranks all applications by need (lowest per capita income first) and assesses them in '
                        'that order. The check below is indicative."',
            'review': 'Approve'},
 'TC-103': {'id': 'TC-103',
            'scenario_id': 'TS-021',
            'title': 'Eligibility check rows show scheme, level, nationality, GHI and PCI with Pass or Fail',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: 00377 (all Pass) and 00412 (GHI and PCI Fail)',
            'steps': '1. Open View on 00377 and read the Eligibility check rows.\n'
                     '2. Close the drawer, open View on 00412 and read the rows.',
            'expected': '1. 00377 shows Scheme "MOEFAS 2027 · effective from 01/01/2027", Level "Secondary · S3", '
                        'Nationality Singapore Citizen Pass, Gross household income S$ 4,120.00 (limit ≤ S$ 4,200.00) '
                        'Pass, Per capita income S$ 1,030.00 (limit ≤ S$ 1,050.00) Pass.\n'
                        '2. 00412 shows Level "Primary · P3", GHI S$ 4,350.00 (limit ≤ S$ 4,200.00) Fail and PCI '
                        '(limit ≤ S$ 1,050.00) Fail.\n'
                        '3. Below the rows the drawer reads "MOEFAS is decided automatically after the form closes: '
                        "Pass → approved from Effective from, Fail → the school's SBFAS (if the parent agreed) or "
                        'rejected."',
            'review': 'Draft'},
 'TC-104': {'id': 'TC-104',
            'scenario_id': 'TS-021',
            'title': 'Household and income, context and documents are shown for MOEFAS',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: 00377 (context and one document), 00390 (no context, no document)',
            'steps': '1. Open View on 00377 and read Household and income, Context and Documents.\n'
                     '2. Close the drawer, open View on 00390 and read the same blocks.',
            'expected': '1. 00377 shows Gross household income S$ 4,120.00 / month, Household size 4, Per capita '
                        'income S$ 1,030.00, Income source API, the context text and payslips_2026.pdf with a View '
                        'link.\n'
                        '2. 00390 shows "No context given." and "No documents."',
            'review': 'Approve'},
 'TC-105': {'id': 'TC-105',
            'scenario_id': 'TS-021',
            'title': 'MOEFAS drawer has no student, parent or ML block',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412',
            'steps': '1. Open View on 00412 and list the blocks of the drawer.',
            'expected': '1. The blocks are Eligibility check, Household and income, Context, Documents and History.\n'
                        '2. There is no Student block, no Parent block and no ML recommendation block.',
            'review': 'Approve'},
 'TC-106': {'id': 'TC-106',
            'scenario_id': 'TS-022',
            'title': 'Approved MOEFAS drawer shows Granted, Priority and Decided by',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00390 (MOEFAS 2026, Approved, priority 1 of 4)',
            'steps': '1. Open View on 00390.\n2. Read the Decision block.',
            'expected': '1. The Decision block shows Result Approved, "Granted · MOEFAS (MOEFAS 2026) · from '
                        '01/01/2026" and Priority "1 of 4 (lowest per capita income first)".\n'
                        '2. Decided by shows "System (auto-approved)" with 01/01/2026 00:05.',
            'review': 'Approve'},
 'TC-107': {'id': 'TC-107',
            'scenario_id': 'TS-022',
            'title': 'Rejected MOEFAS drawer shows the reason and the system as decider',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00328 (MOEFAS 2026, Rejected, priority 4 of 4)',
            'steps': '1. Open View on 00328.\n2. Read the Decision block.',
            'expected': '1. The Decision block shows Result Rejected, Priority "4 of 4 (lowest per capita income '
                        'first)", Reason "Not eligible for MOEFAS", Comment "GHI and PCI both above MOEFAS limits." '
                        'and Decided by "System (system rejection)".\n'
                        '2. It shows no Granted line.',
            'review': 'Draft'},
 'TC-108': {'id': 'TC-108',
            'scenario_id': 'TS-022',
            'title': 'Two applications of one student under the same MOEFAS scheme',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Student: Lee Zhi Hao, T1702215M, two applications under MOEFAS 2026\n'
                         '00381: Approved, priority 3 of 4\n'
                         '00328: Rejected, priority 4 of 4',
            'steps': '1. Open View on 00381 and 00328.\n2. Compare the Decision blocks.',
            'expected': '1. The FS has no rule for a second application of the same student and scheme.\n'
                        '2. The expected result cannot be written until the BA answers the question of ASM-R4-19.',
            'review': 'Block'},
 'TC-109': {'id': 'TC-109',
            'scenario_id': 'TS-022',
            'title': 'Decision block is not shown while the application is pending',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412 (Pending)',
            'steps': '1. Open View on 00412.\n2. Look for a Decision block.',
            'expected': '1. The drawer has no Decision block.',
            'review': 'Approve'},
 'TC-110': {'id': 'TC-110',
            'scenario_id': 'TS-023',
            'title': 'Drawer closes with the X button',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412',
            'steps': '1. Open View on 00412.\n2. Click X in the drawer header.',
            'expected': '1. The drawer closes and the list stays on the same tab, filters and search.',
            'review': 'Approve'},
 'TC-111': {'id': 'TC-111',
            'scenario_id': 'TS-023',
            'title': 'Drawer closes when the user clicks outside it',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00412',
            'steps': '1. Open View on 00412.\n2. Click on the dimmed area outside the drawer.',
            'expected': '1. The drawer closes. No data is changed.',
            'review': 'Approve'},
 'TC-112': {'id': 'TC-112',
            'scenario_id': 'TS-023',
            'title': 'Reopening the drawer shows the data of the clicked row',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: 00412 and 00410',
            'steps': '1. Open View on 00412 and read the header.\n'
                     '2. Close the drawer, open View on 00410 and read the header.',
            'expected': '1. The second drawer shows APP-2026-00410, Ryan Lim and Bukit View Primary.\n'
                        '2. No data of 00412 remains in it.',
            'review': 'Approve'},
 'TC-113': {'id': 'TC-113',
            'scenario_id': 'TS-023',
            'title': 'Filters and search stay after the drawer closes',
            'suite': 'F4.7 Review drawer, MOEFAS',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Filter: Status = Pending, Search = "ryan"',
            'steps': '1. Set the filter and the search.\n2. Open View on 00410 and close the drawer.',
            'expected': '1. The filter, the search and the page are unchanged.\n2. The list shows 00410 only.',
            'review': 'Approve'},
 'TC-114': {'id': 'TC-114',
            'scenario_id': 'TS-024',
            'title': 'School Admin drawer shows student, parent, household, context, ML, documents and history',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 (Daniel Ong, International Student, P2)',
            'steps': '1. Open FAS applications and click Review on 00398.\n2. Read all blocks of the drawer.',
            'expected': '1. The header reads "SBFAS REVIEW", APP-2026-00398 and "Daniel Ong · P2".\n'
                        '2. Student shows Full name, NRIC/FIN T1755501Q, Grade P2, Class and Citizenship.\n'
                        '3. Parent shows name, NRIC/FIN, mobile and email.\n'
                        '4. Household and income shows S$ 2,600.00 / month, size 3, per capita S$ 867.00 and Income '
                        'source API.\n'
                        '5. Context shows "No context given." and Documents shows "No documents."\n'
                        '6. History shows Submitted and "SBFAS application (not eligible for MOEFAS by nationality)".',
            'review': 'Draft'},
 'TC-115': {'id': 'TC-115',
            'scenario_id': 'TS-024',
            'title': 'MOE HQ drawer for SBFAS shows the school in the header and the student block',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Open View on 00398 as MOE HQ.\n2. Read the header and the Student block.',
            'expected': '1. The header reads "SBFAS REVIEW", APP-2026-00398 and "Daniel Ong · Bukit View Primary".\n'
                        '2. The Student block shows the school Bukit View Primary.',
            'review': 'Approve'},
 'TC-116': {'id': 'TC-116',
            'scenario_id': 'TS-024',
            'title': 'Decided SBFAS drawer shows Tier, from date, reason, comment and decider',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00386 (Approved Tier 3 from 13/01/2026 by Lan Nguyen)',
            'steps': '1. Open the All tab and click View on 00386.\n2. Read the Decision block and the History.',
            'expected': '1. The Decision block shows "Tier 3 · from 13/01/2026" and Decided by "Lan Nguyen (BVP-0012)" '
                        'with 13/01/2026 09:10.\n'
                        '2. Reason and Comment lines are shown when they exist.\n'
                        '3. The History has a row "Approved · Tier 3".',
            'review': 'Approve'},
 'TC-117': {'id': 'TC-117',
            'scenario_id': 'TS-024',
            'title': 'Parent relationship and citizenship use readable labels',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Applications: 00398 (International Student) and 00386 (Citizen)',
            'steps': '1. Open View on 00398 and 00386 and read the Citizenship and Parent name.',
            'expected': '1. Citizenship reads "International Student" and "Singapore Citizen".\n'
                        '2. Parent name is followed by the relationship (for example Mother).\n'
                        '3. The mobile number is shown as stored.',
            'review': 'Draft'},
 'TC-118': {'id': 'TC-118',
            'scenario_id': 'TS-025',
            'title': 'ML recommendation block shows the tier only with the tag Recommendation only',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Applications: 00386 (ML Tier 2) and 00398 (no tier fits)',
            'steps': '1. Open the All tab and click View on 00386.\n'
                     '2. Read the ML recommendation block.\n'
                     '3. Close it, open View on 00398 and read the block.',
            'expected': '1. 00386 shows "Tier 2" and the tag "Recommendation only".\n'
                        '2. 00398 shows a dash and the tag.\n'
                        '3. No Need Score, confidence, deny rule or factor is shown in either drawer.',
            'review': 'Approve'},
 'TC-119': {'id': 'TC-119',
            'scenario_id': 'TS-025',
            'title': 'A red note appears when the school has no SBFAS scheme for the period',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N15',
            'preconditions': '1. The F4 build is running.\n'
                             '2. Signed in as a School Admin whose school has no published SBFAS scheme for the submit '
                             'date.',
            'test_data': 'Application: Pending SBFAS application of that school (SEED-R4-N15)',
            'steps': '1. Open Review on the application.\n2. Read the ML recommendation block.',
            'expected': '1. The block shows a dash and a red note that the school has no SBFAS scheme for the '
                        'application period.\n'
                        '2. The Approve button cannot be confirmed because no tier is listed.',
            'review': 'Draft'},
 'TC-120': {'id': 'TC-120',
            'scenario_id': 'TS-025',
            'title': 'ML recommendation is information only and does not block a choice',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: 00412 (ML Tier 3)',
            'steps': '1. Click Review on 00412 and click Approve.\n2. Choose Tier 1 and confirm.',
            'expected': '1. The approval is accepted with Tier 1 although ML suggested Tier 3.\n'
                        '2. The Decision block shows Tier 1.',
            'review': 'Draft'},
 'TC-121': {'id': 'TC-121',
            'scenario_id': 'TS-026',
            'title': 'Reject and Approve show only for the School Admin of the school on a Pending SBFAS',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Applications: 00398 (Pending) and 00386 (Approved)',
            'steps': '1. Click Review on 00398 and read the buttons.\n'
                     '2. Close it, open the All tab, click View on 00386 and read the buttons.',
            'expected': '1. 00398 shows Reject and Approve.\n2. 00386 shows no decision button.',
            'review': 'Approve'},
 'TC-122': {'id': 'TC-122',
            'scenario_id': 'TS-026',
            'title': 'MOE HQ drawers have no decision button for SBFAS',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Applications: 00398 (SBFAS Pending), 00386 (SBFAS Approved)',
            'steps': '1. Click View on 00398 and on 00386 and read the buttons.',
            'expected': '1. Neither drawer has Reject or Approve.',
            'review': 'Approve'},
 'TC-123': {'id': 'TC-123',
            'scenario_id': 'TS-026',
            'title': 'A School Admin of another school cannot decide the application',
            'suite': 'F4.8 Review drawer, SBFAS',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with two School Admin accounts.\n'
                             '2. Signed in as a School Admin of Meridian Secondary.',
            'test_data': 'Application: APP-2026-00398 of Bukit View Primary',
            'steps': '1. Open the link of 00398 directly.\n2. Send an approve request for 00398 to the API.',
            'expected': '1. The link shows "You do not have access."\n'
                        '2. The approve request is refused with HTTP 403 and 00398 stays Pending.',
            'review': 'Draft'},
 'TC-124': {'id': 'TC-124',
            'scenario_id': 'TS-027',
            'title': 'Approve dialog shows the subtitle, the candidate tiers and the buttons',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 (Daniel Ong, P2)\n'
                         'School SBFAS schemes: Tier 1, Tier 2, Tier 3 (form period contains the submit date)',
            'steps': '1. Click Review on 00398 and click Approve.\n2. Read the dialog.',
            'expected': '1. The title is "Approve SBFAS" and the subtitle reads "FUNCTION 4 · SBFAS · APP-2026-00398 · '
                        'Daniel Ong · P2".\n'
                        '2. Tier * lists Tier 1, Tier 2 and Tier 3.\n'
                        '3. Comment (optional) shows the counter 0/500.\n'
                        '4. The buttons are Cancel and Confirm approval.',
            'review': 'Approve'},
 'TC-125': {'id': 'TC-125',
            'scenario_id': 'TS-027',
            'title': 'Candidate tiers are the published school schemes whose form period holds the submit date',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N16',
            'preconditions': '1. The F4 build is running.\n2. Signed in as a School Admin of the seed school.',
            'test_data': 'Schemes of the school (SEED-R4-N16):\n'
                         'Tier A form 01/08/2026 to 31/12/2026, Tier B form 01/01/2027 to 30/06/2027, Draft Tier C\n'
                         'Application submitted 17/10/2026',
            'steps': '1. Open Review on the application and click Approve.\n2. Read the Tier list.',
            'expected': '1. Only Tier A is listed.\n'
                        '2. Tier B (form not yet open on the submit date) and the Draft are not listed.',
            'review': 'Approve'},
 'TC-126': {'id': 'TC-126',
            'scenario_id': 'TS-027',
            'title': 'When no scheme has the submit date in its form period the schemes in effect today are listed',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N16',
            'preconditions': '1. The F4 build is running.\n2. Signed in as a School Admin of the seed school.',
            'test_data': 'Application submitted on a date outside every form period (SEED-R4-N16)\n'
                         'Scheme in effect today: Tier A',
            'steps': '1. Open Review on the application and click Approve.\n2. Read the Tier list.',
            'expected': '1. The list shows the schemes in effect today, sorted by name.',
            'review': 'Approve'},
 'TC-127': {'id': 'TC-127',
            'scenario_id': 'TS-027',
            'title': 'Candidate tiers are sorted by name',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398 and click Approve.\n2. Read the order of the Tier options.',
            'expected': '1. The order is Tier 1, Tier 2, Tier 3.',
            'review': 'Approve'},
 'TC-128': {'id': 'TC-128',
            'scenario_id': 'TS-027',
            'title': 'Cancel closes the dialog and changes nothing',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398, click Approve, choose Tier 2, type a comment and click Cancel.\n'
                     '2. Open the All tab and read 00398.',
            'expected': '1. The dialog closes.\n2. 00398 is still Pending with no tier and no History row added.',
            'review': 'Approve'},
 'TC-129': {'id': 'TC-129',
            'scenario_id': 'TS-028',
            'title': 'ML tier is pre-selected with a hint',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00412 (ML recommendation Tier 3)',
            'steps': '1. Click Review on 00412 and click Approve.\n2. Read the Tier field and its hint.',
            'expected': '1. Tier 3 is pre-selected.\n2. The hint reads "ML suggests Tier 3".',
            'review': 'Approve'},
 'TC-130': {'id': 'TC-130',
            'scenario_id': 'TS-028',
            'title': 'Without an ML tier the last scheme is pre-selected and no hint is shown',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 (ML recommendation a dash)',
            'steps': '1. Click Review on 00398 and click Approve.\n2. Read the Tier field.',
            'expected': '1. Tier 3 (the last scheme) is pre-selected.\n2. No "ML suggests" hint is shown.',
            'review': 'Approve'},
 'TC-131': {'id': 'TC-131',
            'scenario_id': 'TS-028',
            'title': 'The School Admin may choose a tier other than the recommendation',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00412 (ML recommendation Tier 3)',
            'steps': '1. Click Review on 00412 and click Approve.\n'
                     '2. Choose Tier 2 and click Confirm approval.\n'
                     '3. Open View on 00412.',
            'expected': '1. The approval is accepted.\n'
                        '2. The Decision block shows Tier 2 and the list shows Tier 2 in the Tier column while ML '
                        'recommendation stays Tier 3.',
            'review': 'Draft'},
 'TC-132': {'id': 'TC-132',
            'scenario_id': 'TS-028',
            'title': 'A household that meets no scheme can still be approved by the school',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 (International Student, schemes accept Citizen and PR)',
            'steps': '1. Click Review on 00398 and click Approve.\n'
                     '2. Keep the default tier and click Confirm approval.',
            'expected': '1. The approval is accepted for the chosen tier and no warning is shown.\n'
                        '2. The Decision block shows the chosen tier.',
            'review': 'Draft'},
 'TC-133': {'id': 'TC-133',
            'scenario_id': 'TS-028',
            'title': 'Approve cannot be confirmed when the school has no candidate scheme',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N15',
            'preconditions': '1. The F4 build is running.\n'
                             '2. Signed in as a School Admin whose school has no candidate scheme (SEED-R4-N15).',
            'test_data': 'Pending SBFAS application of that school',
            'steps': '1. Click Review and click Approve.\n2. Read the Tier field and the Confirm approval button.',
            'expected': '1. The Tier list is empty and Confirm approval is disabled.\n'
                        '2. Reject remains available and the application stays Pending.',
            'review': 'Draft'},
 'TC-134': {'id': 'TC-134',
            'scenario_id': 'TS-029',
            'title': 'Comment is optional',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398 and click Approve.\n2. Leave Comment empty and click Confirm approval.',
            'expected': '1. The approval is accepted with no comment.\n2. The Decision block shows no Comment line.',
            'review': 'Approve'},
 'TC-135': {'id': 'TC-135',
            'scenario_id': 'TS-029',
            'title': 'Comment accepts 500 characters and blocks 501',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Comments of 499, 500 and 501 characters',
            'steps': '1. Click Review on 00398 and click Approve.\n'
                     '2. Enter the 499-character comment and read the counter and the button.\n'
                     '3. Enter 500 characters and read them.\n'
                     '4. Enter 501 characters and read them.',
            'expected': '1. The counter reads 499/500 and 500/500 and Confirm approval is enabled.\n'
                        '2. At 501 characters Confirm approval is disabled and the counter shows 501/500.',
            'review': 'Approve'},
 'TC-136': {'id': 'TC-136',
            'scenario_id': 'TS-029',
            'title': 'Comment with markup is saved as plain text',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Comment: <b>ok</b><script>alert(1)</script>',
            'steps': '1. Click Review on 00398, click Approve and enter the comment.\n'
                     '2. Confirm and open View on 00398.',
            'expected': '1. The Decision block shows the comment as text, tags included.\n2. No script runs.',
            'review': 'Draft'},
 'TC-137': {'id': 'TC-137',
            'scenario_id': 'TS-030',
            'title': 'Confirm approval saves the tier, the date and the decider',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398, Tier 2, comment "Approved after review"',
            'steps': '1. Click Review on 00398 and click Approve.\n'
                     '2. Choose Tier 2, enter the comment and click Confirm approval.\n'
                     '3. Open the All tab and click View on 00398.',
            'expected': '1. A toast reads "Subsidy applied to the student\'s EA fees."\n'
                        '2. The dialog and the drawer close.\n'
                        '3. The row shows Tier 2 in Tier, Status Approved and View.\n'
                        '4. The Decision block shows Result Approved, "Tier 2 · from 01/01/2027", Comment "Approved '
                        'after review" and Decided by "Lan Nguyen (BVP-0012)" with the date and time.',
            'review': 'Approve'},
 'TC-138': {'id': 'TC-138',
            'scenario_id': 'TS-030',
            'title': 'Effective from is the scheme start or today when the scheme is already in effect',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N16',
            'preconditions': '1. The F4 build is running with a clock control.\n2. Signed in as a School Admin.',
            'test_data': 'Scheme A starts 01/01/2027, Scheme B started 01/01/2026 and is in effect today 18/10/2026 '
                         '(SEED-R4-N16)',
            'steps': '1. Approve an application with Scheme A.\n'
                     '2. Approve another application with Scheme B.\n'
                     '3. Read both Decision blocks.',
            'expected': '1. Scheme A gives "from 01/01/2027".\n2. Scheme B gives "from 18/10/2026" (today).',
            'review': 'Approve'},
 'TC-139': {'id': 'TC-139',
            'scenario_id': 'TS-030',
            'title': 'History lists the approval and the email',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398, Tier 2',
            'steps': '1. Approve 00398 with Tier 2.\n2. Open View on 00398 and read the History.',
            'expected': '1. The last two rows are "Approved · Tier 2 · from 01/01/2027" and "Email with result sent to '
                        'parent".',
            'review': 'Draft'},
 'TC-140': {'id': 'TC-140',
            'scenario_id': 'TS-030',
            'title': 'Cards and tab counts update after the approval',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state: Pending 1, SBFAS approved 1, SBFAS rejected 0. Tabs Pending 1, All 2, Approved '
                         '1.',
            'steps': '1. Approve 00398.\n2. Read the cards and the tabs.',
            'expected': '1. Cards read Pending 0, SBFAS approved 2 and SBFAS rejected 0.\n'
                        '2. Tabs read Pending without a count, All 2, Approved 2.\n'
                        '3. The Pending tab shows "No applications found."',
            'review': 'Approve'},
 'TC-141': {'id': 'TC-141',
            'scenario_id': 'TS-030',
            'title': 'MOE HQ counts update after a school approval',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state: Total 9, MOEFAS approved 3, Approved 4, Rejected 1',
            'steps': '1. As the school, approve 00398. Log out and sign in as MOE HQ.\n'
                     '2. Read the cards.\n'
                     '3. Open View on 00398.',
            'expected': '1. Cards read Total 9, MOEFAS approved 3, Approved 5 and Rejected 1.\n'
                        '2. 00398 shows Approved with Tier 2 and the drawer has no decision button.',
            'review': 'Approve'},
 'TC-142': {'id': 'TC-142',
            'scenario_id': 'TS-030',
            'title': 'An approved application is read only',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 approved',
            'steps': '1. Approve 00398.\n2. Open View on 00398 and look for fields and buttons.',
            'expected': '1. The drawer has no Reject, no Approve and no editable field.',
            'review': 'Approve'},
 'TC-143': {'id': 'TC-143',
            'scenario_id': 'TS-031',
            'title': 'Reject dialog shows the reasons, the hint and the disabled button',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398 and click Reject.\n2. Read the dialog and open the Reason list.',
            'expected': '1. The title is "Reject application" and the subtitle reads "FUNCTION 4 · SBFAS · '
                        'APP-2026-00398 · Daniel Ong · P2".\n'
                        '2. Reason * starts on "Select reason" and lists Income above limit, Not eligible nationality, '
                        'Incomplete documents and Other.\n'
                        '3. The hint reads "Reasons: Income above limit · Not eligible nationality · Incomplete '
                        'documents · Other".\n'
                        '4. Comment * shows the placeholder "Explain the decision. Parent receives the reason by '
                        'email." and the counter 0/500.\n'
                        '5. Reject application is disabled.',
            'review': 'Approve'},
 'TC-144': {'id': 'TC-144',
            'scenario_id': 'TS-031',
            'title': 'Reject stays disabled until both reason and comment are filled',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Combinations: empty, reason only, comment only, spaces only in the comment, reason with '
                         'comment',
            'steps': '1. Click Review on 00398 and click Reject.\n'
                     '2. Try each combination and read the Reject application button.',
            'expected': '1. The button is disabled for empty, reason only, comment only and a comment of spaces only.\n'
                        '2. The button is enabled when a reason is chosen and the comment has text.',
            'review': 'Approve'},
 'TC-145': {'id': 'TC-145',
            'scenario_id': 'TS-031',
            'title': 'Reject comment accepts 500 characters and blocks 501',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Comments of 499, 500 and 501 characters',
            'steps': '1. Click Review on 00398, click Reject and choose a reason.\n'
                     '2. Enter 499, 500 and 501 characters in turn.\n'
                     '3. Read the counter and the button each time.',
            'expected': '1. At 499 and 500 characters the button is enabled and the counter reads 499/500 and '
                        '500/500.\n'
                        '2. At 501 characters the button is disabled and the counter reads 501/500.',
            'review': 'Approve'},
 'TC-146': {'id': 'TC-146',
            'scenario_id': 'TS-031',
            'title': 'Each reason value is accepted',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Reasons: Income above limit, Not eligible nationality, Incomplete documents, Other',
            'steps': '1. For each reason, reset the data, open Review on 00398, reject with that reason and a comment, '
                     'then read the Decision block.',
            'expected': '1. The Decision block shows the chosen reason each time.',
            'review': 'Approve'},
 'TC-147': {'id': 'TC-147',
            'scenario_id': 'TS-031',
            'title': 'Cancel closes the reject dialog and changes nothing',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398, click Reject, choose a reason, type a comment and click Cancel.\n'
                     '2. Read 00398 in the Pending tab.',
            'expected': '1. The dialog closes and 00398 is still Pending with no History row added.',
            'review': 'Approve'},
 'TC-148': {'id': 'TC-148',
            'scenario_id': 'TS-032',
            'title': 'Reject saves the reason, the comment and the decider',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398, reason Income above limit, comment "Household income is above '
                         'the limit of every tier."',
            'steps': '1. Click Review on 00398 and click Reject.\n'
                     '2. Choose the reason, enter the comment and click Reject application.\n'
                     '3. Open the Rejected tab and click View on 00398.',
            'expected': '1. A toast reads "Application rejected. Parent notified by email."\n'
                        '2. The row shows Status Rejected and an empty Tier.\n'
                        '3. The Decision block shows Result Rejected, Reason "Income above limit", the Comment and '
                        'Decided by "Lan Nguyen (BVP-0012)" with the date and time.',
            'review': 'Approve'},
 'TC-149': {'id': 'TC-149',
            'scenario_id': 'TS-032',
            'title': 'History lists the rejection and the email with the reason',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 rejected',
            'steps': '1. Reject 00398 as above.\n2. Open View and read the History.',
            'expected': '1. The last two rows are "Rejected · Income above limit" and "Email with reason sent to '
                        'parent".',
            'review': 'Draft'},
 'TC-150': {'id': 'TC-150',
            'scenario_id': 'TS-032',
            'title': 'Cards and tabs update after the rejection',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state: Pending 1, SBFAS approved 1, SBFAS rejected 0',
            'steps': '1. Reject 00398.\n2. Read the cards and the tabs.',
            'expected': '1. Cards read Pending 0, SBFAS approved 1 and SBFAS rejected 1.\n'
                        '2. Tabs read Pending without a count, All 2, Approved 1 and Rejected 1.',
            'review': 'Approve'},
 'TC-151': {'id': 'TC-151',
            'scenario_id': 'TS-032',
            'title': 'Parent receives an email with the reason',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-05',
            'preconditions': '1. The F4 build is connected to the email service.\n2. Signed in as a School Admin.',
            'test_data': 'Application: Pending SBFAS application of a parent with a test mailbox',
            'steps': '1. Reject the application with reason "Incomplete documents".\n'
                     '2. Open the parent mailbox (Email inbox simulation).',
            'expected': '1. One email is received.\n'
                        '2. It states the application was rejected and gives the reason and the comment.',
            'review': 'Draft'},
 'TC-152': {'id': 'TC-152',
            'scenario_id': 'TS-032',
            'title': 'A rejected application is read only',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398 rejected',
            'steps': '1. Reject 00398 and open View on it.',
            'expected': '1. The drawer has no Reject, no Approve and no editable field.',
            'review': 'Approve'},
 'TC-153': {'id': 'TC-153',
            'scenario_id': 'TS-033',
            'title': 'A second user deciding the same application gets the already decided message',
            'suite': 'F4.11 One decision per application',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-03',
            'preconditions': '1. The F4 build is running.\n2. Two School Admin sessions of the same school are open.',
            'test_data': 'Application: Pending SBFAS application of that school\n'
                         'Session A and session B both have the Review drawer open',
            'steps': '1. In session A approve the application with Tier 2.\n'
                     '2. In session B reject the application.\n'
                     '3. Read the message in session B.\n'
                     '4. Refresh session B and open View.',
            'expected': '1. Session B shows "This application was already decided by {user} on {date}." with the name '
                        'of session A and the date.\n'
                        '2. The application stays Approved with Tier 2.\n'
                        '3. No second email is sent.',
            'review': 'Approve'},
 'TC-154': {'id': 'TC-154',
            'scenario_id': 'TS-033',
            'title': 'Two approvals at the same moment save one decision',
            'suite': 'F4.11 One decision per application',
            'page': 'Approve SBFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-03',
            'preconditions': '1. The F4 build is running with two sessions and a way to delay one request.',
            'test_data': 'Application: Pending SBFAS application',
            'steps': '1. Send the approve request from both sessions at the same time with different tiers.\n'
                     '2. Read both responses and the application.',
            'expected': '1. One request succeeds. The other gets the already decided message.\n'
                        '2. The application has one decision and one email.',
            'review': 'Approve'},
 'TC-155': {'id': 'TC-155',
            'scenario_id': 'TS-033',
            'title': 'Double click on Confirm approval saves one decision',
            'suite': 'F4.11 One decision per application',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application: APP-2026-00398',
            'steps': '1. Click Review on 00398, click Approve and double click Confirm approval quickly.\n'
                     '2. Open View on 00398.',
            'expected': '1. The History has one "Approved" row and one email row.\n'
                        '2. The cards count the approval once.',
            'review': 'Approve'},
 'TC-156': {'id': 'TC-156',
            'scenario_id': 'TS-033',
            'title': 'A failed save leaves the application Pending',
            'suite': 'F4.11 One decision per application',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running.\n'
                             '2. The save request can be made to fail (network off or server error).',
            'test_data': 'Application: Pending SBFAS application',
            'steps': '1. Click Approve, choose a tier and click Confirm approval while the save fails.\n'
                     '2. Read the screen and the application.',
            'expected': '1. An error message is shown and the dialog stays open.\n'
                        '2. The application stays Pending and no History row is written.',
            'review': 'Draft'},
 'TC-157': {'id': 'TC-157',
            'scenario_id': 'TS-034',
            'title': 'MOE HQ menu has FAS applications and MOEFAS schemes and no SBFAS schemes',
            'suite': 'F4.12 Access and security',
            'page': 'FAS menu (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Menu group: Financial assistance',
            'steps': '1. Read the Financial assistance group of the left menu.',
            'expected': '1. The group lists FAS applications, MOEFAS schemes and Budget & statistics (F6).\n'
                        '2. There is no SBFAS schemes entry.',
            'review': 'Approve'},
 'TC-158': {'id': 'TC-158',
            'scenario_id': 'TS-034',
            'title': 'School menu has FAS applications and SBFAS schemes and no MOEFAS schemes',
            'suite': 'F4.12 Access and security',
            'page': 'FAS menu (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Base state of Bukit View Primary',
            'steps': '1. Read the left menu.',
            'expected': '1. The menu has FAS applications and SBFAS schemes.\n2. There is no MOEFAS schemes entry.',
            'review': 'Approve'},
 'TC-159': {'id': 'TC-159',
            'scenario_id': 'TS-034',
            'title': 'Each role sees the data and actions of FS 1.2 and nothing else',
            'suite': 'F4.12 Access and security',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Roles: MOE HQ and School Admin',
            'steps': '1. As MOE HQ, read the list and open View on a MOEFAS and an SBFAS application.\n'
                     '2. Log out, sign in as School user BVP-0012 and read the list and the drawer of 00398.',
            'expected': '1. MOE HQ sees all 9 applications of all schools, both schemes, and no decision button.\n'
                        '2. The School Admin sees 2 SBFAS applications of the own school and the decision buttons on '
                        'the Pending one only.',
            'review': 'Approve'},
 'TC-160': {'id': 'TC-160',
            'scenario_id': 'TS-034',
            'title': 'A Parent cannot open the F4 screens',
            'suite': 'F4.12 Access and security',
            'page': 'FAS applications (Parent)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with a Parent account.',
            'test_data': 'Parent signed in to the e-Service portal',
            'steps': '1. Look for the Financial assistance menu.\n2. Open the FAS applications link directly.',
            'expected': '1. The menu has no FAS applications entry for the Parent.\n'
                        '2. The direct link is refused with "You do not have access." and no application data is '
                        'returned.',
            'review': 'Draft'},
 'TC-161': {'id': 'TC-161',
            'scenario_id': 'TS-034',
            'title': 'An unauthenticated user is sent to sign in',
            'suite': 'F4.12 Access and security',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running.\n2. No user is signed in.',
            'test_data': 'Open the FAS applications link directly',
            'steps': '1. Open the link.\n2. Send a list request to the API without a token.',
            'expected': '1. The page shows the sign in screen and no data.\n2. The API answers HTTP 401 with no data.',
            'review': 'Approve'},
 'TC-162': {'id': 'TC-162',
            'scenario_id': 'TS-035',
            'title': 'A School Admin opening an application of another school is refused',
            'suite': 'F4.12 Access and security',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with two School Admin accounts.\n'
                             '2. Signed in as a School Admin of Meridian Secondary.',
            'test_data': 'Application link of 00398 (Bukit View Primary)',
            'steps': '1. Open the link directly.',
            'expected': '1. The screen shows "You do not have access." and no student, parent or income data.',
            'review': 'Draft'},
 'TC-163': {'id': 'TC-163',
            'scenario_id': 'TS-035',
            'title': 'The list API ignores a changed school filter for a School Admin',
            'suite': 'F4.12 Access and security',
            'page': 'FAS applications API',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running.\n2. Signed in as a School Admin of Meridian Secondary.',
            'test_data': 'Request parameter schoolId changed to SCH-01 (Bukit View Primary)',
            'steps': '1. Send the list request with schoolId = SCH-01.\n2. Read the response.',
            'expected': '1. The response holds only rows of Meridian Secondary (or is refused with HTTP 403).\n'
                        '2. No row of Bukit View Primary is returned.',
            'review': 'Draft'},
 'TC-164': {'id': 'TC-164',
            'scenario_id': 'TS-035',
            'title': 'A School Admin cannot open a MOEFAS application',
            'suite': 'F4.12 Access and security',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running.\n2. Signed in as a School Admin of Bukit View Primary.',
            'test_data': 'Application link of 00412 (MOEFAS, same school)',
            'steps': '1. Open the link directly.\n2. Send a get request for 00412 to the API.',
            'expected': '1. The screen shows "You do not have access."\n'
                        '2. The API refuses the request with HTTP 403 and returns no income data.',
            'review': 'Draft'},
 'TC-165': {'id': 'TC-165',
            'scenario_id': 'TS-035',
            'title': 'MOE HQ cannot open SBFAS schemes and a School Admin cannot open MOEFAS schemes',
            'suite': 'F4.12 Access and security',
            'page': 'FAS schemes',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with both accounts.',
            'test_data': 'Links to the SBFAS scheme list of Bukit View Primary and to the MOEFAS scheme list',
            'steps': '1. As MOE HQ, open the SBFAS scheme link and send a scheme list request for SBFAS.\n'
                     '2. As a School Admin, open the MOEFAS scheme link.',
            'expected': '1. Both links show "You do not have access." and the API answers HTTP 403 with no data.',
            'review': 'Draft'},
 'TC-166': {'id': 'TC-166',
            'scenario_id': 'TS-036',
            'title': 'Reject comment with markup is stored and shown as text',
            'suite': 'F4.12 Access and security',
            'page': 'Reject dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Comment: <img src=x onerror=alert(1)> & "quotes"',
            'steps': '1. Click Review on 00398, click Reject, choose a reason and enter the comment.\n'
                     '2. Confirm and open View on 00398, then open the same application as MOE HQ.',
            'expected': '1. Both Decision blocks show the comment as text, tags and quotes included.\n'
                        '2. No alert opens and the page layout is not changed.',
            'review': 'Draft'},
 'TC-167': {'id': 'TC-167',
            'scenario_id': 'TS-036',
            'title': 'Scheme name with markup is shown as text',
            'suite': 'F4.12 Access and security',
            'page': 'FAS schemes',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Scheme name: <b>Tier X</b><script>alert(1)</script>',
            'steps': '1. Open SBFAS schemes, click New scheme, enter the name and click Save draft.\n'
                     '2. Read the scheme list and the Tier filter of FAS applications.',
            'expected': '1. The name is shown as text in the list.\n2. No script runs.',
            'review': 'Draft'},
 'TC-168': {'id': 'TC-168',
            'scenario_id': 'TS-037',
            'title': 'MOE HQ sees the three MOEFAS schemes only',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schemes: MOEFAS 2027, MOEFAS 2026, MOEFAS 2025',
            'steps': '1. Open Financial assistance > MOEFAS schemes.\n2. Read the table.',
            'expected': '1. The table lists MOEFAS 2027, MOEFAS 2026 and MOEFAS 2025 only.\n'
                        '2. No SBFAS scheme of any school is listed.',
            'review': 'Approve'},
 'TC-169': {'id': 'TC-169',
            'scenario_id': 'TS-037',
            'title': 'A School Admin sees the own SBFAS schemes only',
            'suite': 'F4.13 FAS schemes list',
            'page': 'SBFAS schemes (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Bukit View Primary schemes: Tier 1, Tier 2, Tier 3 for 2026 and for 2027',
            'steps': '1. Open SBFAS schemes.\n'
                     '2. Read the table.\n'
                     '3. Log out, sign in as MRS-0012 and open SBFAS schemes.',
            'expected': '1. Bukit View Primary lists 6 schemes (Tier 1 to Tier 3, twice).\n'
                        '2. Meridian Secondary lists none of the Bukit View Primary schemes and no MOEFAS scheme.',
            'review': 'Approve'},
 'TC-170': {'id': 'TC-170',
            'scenario_id': 'TS-037',
            'title': 'The page subtitle states the role scope',
            'suite': 'F4.13 FAS schemes list',
            'page': 'FAS schemes',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Roles: MOE HQ and School Admin',
            'steps': '1. Read the subtitle of MOEFAS schemes as MOE HQ.\n'
                     '2. Read the subtitle of SBFAS schemes as a School Admin.',
            'expected': '1. MOE HQ reads "View existing MOEFAS schemes and create a new one when changes are needed. '
                        'One MOEFAS scheme covers all levels, it has no tiers. SBFAS schemes are configured by each '
                        'school for itself."\n'
                        '2. The School Admin reads "Your school\'s own SBFAS schemes. Each scheme is one tier (e.g. '
                        'Tier 1, Tier 2). View existing schemes and create a new scheme when changes are needed."',
            'review': 'Approve'},
 'TC-171': {'id': 'TC-171',
            'scenario_id': 'TS-038',
            'title': 'Scheme cards count Active, Upcoming, Closed and Draft',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Today 18/10/2026\nMOEFAS 2026 Active, MOEFAS 2027 Upcoming, MOEFAS 2025 Closed',
            'steps': '1. Read the four cards.',
            'expected': '1. The cards read Active 1, Upcoming 1 (Published, not yet in effect), Closed 1 and Draft 0.',
            'review': 'Approve'},
 'TC-172': {'id': 'TC-172',
            'scenario_id': 'TS-038',
            'title': 'Table columns and cell contents of the MOEFAS scheme list',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Row: MOEFAS 2027',
            'steps': '1. Read the header and the MOEFAS 2027 row.',
            'expected': '1. The columns are Scheme, Eligibility, Application form, Effective from, Effective to, '
                        'Status and actions.\n'
                        '2. The row shows "MOEFAS 2027" with "Approved automatically", "Singapore Citizen · GHI ≤ S$ '
                        '4,200.00 or PCI ≤ S$ 1,050.00", "01/08/2026 – 31/12/2026" with badge Open and "3 waiting", '
                        'Effective from 01/01/2027, Effective to "No end date" and Status Upcoming.',
            'review': 'Approve'},
 'TC-173': {'id': 'TC-173',
            'scenario_id': 'TS-038',
            'title': 'SBFAS list shows Approved by school and the PCI band',
            'suite': 'F4.13 FAS schemes list',
            'page': 'SBFAS schemes (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Row: Tier 2, form 2027',
            'steps': '1. Open SBFAS schemes and read the Tier 2 row of the 2027 schemes.',
            'expected': '1. The row shows "Tier 2" with "Approved by school", "Citizen and PR · PCI S$ 601 – 1,000", '
                        'form "01/08/2026 – 31/12/2026" with badge Open, Effective from 01/01/2027, "No end date" and '
                        'Upcoming.\n'
                        '2. It shows no "waiting" or "Assessed" text.',
            'review': 'Approve'},
 'TC-174': {'id': 'TC-174',
            'scenario_id': 'TS-038',
            'title': 'Sort is Effective from newest first, then name',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Read the order of the rows as MOE HQ.\n'
                     '2. Log out and read the order of the rows of SBFAS schemes as BVP-0012.',
            'expected': '1. MOE HQ: MOEFAS 2027, MOEFAS 2026, MOEFAS 2025.\n'
                        '2. School Admin: Tier 1, Tier 2, Tier 3 of 2027, then Tier 1, Tier 2, Tier 3 of 2026.',
            'review': 'Approve'},
 'TC-175': {'id': 'TC-175',
            'scenario_id': 'TS-038',
            'title': 'Scheme status follows the effective dates',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N17',
            'preconditions': '1. The F4 build is running with a clock control.\n2. Signed in as MOE HQ.',
            'test_data': 'Scheme X Effective from 19/10/2026, Scheme Y Effective to 17/10/2026, Scheme Z Effective to '
                         '18/10/2026\n'
                         'Today 18/10/2026 (SEED-R4-N17)',
            'steps': '1. Read the Status of X, Y and Z.\n2. Set today to 19/10/2026 and read them again.',
            'expected': '1. On 18/10/2026: X is Upcoming, Y is Closed, Z is Active (Effective to is the last day).\n'
                        '2. On 19/10/2026: X is Active and Z is Closed.',
            'review': 'Approve'},
 'TC-176': {'id': 'TC-176',
            'scenario_id': 'TS-038',
            'title': 'Application form badge follows the form period',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N17',
            'preconditions': '1. The F4 build is running with a clock control.\n2. Signed in as MOE HQ.',
            'test_data': 'Scheme with form 19/10/2026 to 30/11/2026 (SEED-R4-N17)',
            'steps': '1. Read the badge on 18/10/2026, on 19/10/2026, on 30/11/2026 and on 01/12/2026.',
            'expected': '1. The badge reads Not open yet, Open, Open and Closed.',
            'review': 'Draft'},
 'TC-177': {'id': 'TC-177',
            'scenario_id': 'TS-038',
            'title': 'MOEFAS rows show waiting count or Assessed date',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Base state',
            'steps': '1. Read the Application form cell of the three MOEFAS schemes.',
            'expected': '1. MOEFAS 2027 shows Open and "3 waiting".\n'
                        '2. MOEFAS 2026 shows Closed and "Assessed 01/01/2026".\n'
                        '3. MOEFAS 2025 shows Closed and "Assessed 01/01/2025".',
            'review': 'Approve'},
 'TC-178': {'id': 'TC-178',
            'scenario_id': 'TS-039',
            'title': 'Actions follow the scheme status',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N18',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schemes: MOEFAS 2027 (Upcoming), MOEFAS 2026 (Active), MOEFAS 2025 (Closed)\n'
                         'A Draft scheme saved from the wizard (SEED-R4-N18)',
            'steps': '1. Read the action cell of each row.',
            'expected': '1. MOEFAS 2027 shows View, Add fee and Close form now (demo).\n'
                        '2. MOEFAS 2026 shows View and Add fee.\n'
                        '3. MOEFAS 2025 shows View only.\n'
                        '4. The Draft row shows Edit only.',
            'review': 'Approve'},
 'TC-179': {'id': 'TC-179',
            'scenario_id': 'TS-039',
            'title': 'Close form now (demo) shows only for HQ on a MOEFAS scheme with the form Open',
            'suite': 'F4.13 FAS schemes list',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schemes: MOEFAS 2027 (form Open), MOEFAS 2026 (Closed)\n'
                         'School SBFAS schemes with the form Open',
            'steps': '1. Read the action cells as MOE HQ.\n'
                     '2. Log out and read the action cells of SBFAS schemes as a School Admin.',
            'expected': '1. The button is shown on MOEFAS 2027 only.\n2. No SBFAS row has the button.',
            'review': 'Approve'},
 'TC-180': {'id': 'TC-180',
            'scenario_id': 'TS-039',
            'title': 'New scheme creates MOEFAS for HQ and SBFAS for a school with no type choice',
            'suite': 'F4.13 FAS schemes list',
            'page': 'FAS schemes',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Roles: MOE HQ and School Admin',
            'steps': '1. Click New scheme as MOE HQ and read step 1.\n'
                     '2. Cancel. Log out, sign in as BVP-0012, open SBFAS schemes and click New scheme.',
            'expected': '1. Neither wizard shows a Scheme type or a Level field.\n'
                        '2. The HQ hint reads "One MOEFAS scheme covers Primary, Secondary and Pre-University." and '
                        'the school wizard names the scheme as a tier (for example "Tier 1").',
            'review': 'Approve'},
 'TC-181': {'id': 'TC-181',
            'scenario_id': 'TS-040',
            'title': 'Step 1 shows the fields, the defaults and the blue note',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Menu path: MOEFAS schemes > New scheme',
            'steps': '1. Open MOEFAS schemes and click New scheme.\n2. Read step 1.',
            'expected': '1. The tabs are 1 General, 2 Eligibility and 3 Subsidy.\n'
                        '2. Fields: Scheme name * (placeholder "e.g. MOEFAS 2028"), Form opens *, Form closes *, '
                        'Effective from * (hint "Must be after Form closes.") and Effective to (hint "No end date").\n'
                        '3. There is no Scheme type and no Level field.\n'
                        '4. The dates are prefilled: Form opens 01/08/2027, Form closes 31/12/2027, Effective from '
                        '01/01/2028, Effective to empty.\n'
                        '5. The blue note reads "Form open 01/08/2027 – 31/12/2027 → the system ranks and assesses all '
                        'applications after 31/12/2027 → subsidy applies from 01/01/2028."',
            'review': 'Approve'},
 'TC-182': {'id': 'TC-182',
            'scenario_id': 'TS-040',
            'title': 'The blue note follows the dates',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Form closes 30/11/2027, Effective from 01/12/2027',
            'steps': '1. Click New scheme.\n'
                     '2. Change Form closes to 30/11/2027 and Effective from to 01/12/2027.\n'
                     '3. Read the blue note.',
            'expected': '1. The note reads "Form open 01/08/2027 – 30/11/2027 → the system ranks and assesses all '
                        'applications after 30/11/2027 → subsidy applies from 01/12/2027."',
            'review': 'Approve'},
 'TC-183': {'id': 'TC-183',
            'scenario_id': 'TS-040',
            'title': 'Scheme name is required',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme name left empty',
            'steps': '1. Click New scheme and leave the name empty.\n'
                     '2. Read the message under the name and click Draft.',
            'expected': '1. "Enter a scheme name." is shown.\n2. The draft is not saved.',
            'review': 'Approve'},
 'TC-184': {'id': 'TC-184',
            'scenario_id': 'TS-040',
            'title': 'Form opens and Form closes are required',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Form opens empty, then Form closes empty',
            'steps': '1. Click New scheme and enter a name.\n'
                     '2. Clear Form opens and read the messages.\n'
                     '3. Restore it, clear Form closes and read the messages.',
            'expected': '1. "Enter Form opens and Form closes." is shown in both cases.',
            'review': 'Approve'},
 'TC-185': {'id': 'TC-185',
            'scenario_id': 'TS-040',
            'title': 'Form closes may equal Form opens but not be earlier',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Form opens 01/08/2027\nForm closes 31/07/2027, 01/08/2027, 02/08/2027',
            'steps': '1. Click New scheme and enter a name.\n'
                     '2. Enter each Form closes value in turn (keep Effective from 01/01/2028).\n'
                     '3. Read the messages.',
            'expected': '1. 31/07/2027 shows "Form closes must be on or after Form opens."\n'
                        '2. 01/08/2027 and 02/08/2027 show no message.',
            'review': 'Approve'},
 'TC-186': {'id': 'TC-186',
            'scenario_id': 'TS-040',
            'title': 'Effective from must be after Form closes',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Form closes 31/12/2027\nEffective from 30/12/2027, 31/12/2027, 01/01/2028',
            'steps': '1. Click New scheme and enter a name.\n'
                     '2. Enter each Effective from value in turn.\n'
                     '3. Read the messages.',
            'expected': '1. 30/12/2027 and 31/12/2027 show "Effective from must be after Form closes (applications are '
                        'assessed after the form closes)."\n'
                        '2. 01/01/2028 shows no message.',
            'review': 'Approve'},
 'TC-187': {'id': 'TC-187',
            'scenario_id': 'TS-040',
            'title': 'Effective to must be after Effective from and may be empty',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Effective from 01/01/2028\nEffective to empty, 31/12/2027, 01/01/2028, 02/01/2028',
            'steps': '1. Click New scheme and enter a name.\n'
                     '2. Enter each Effective to value in turn (empty first).\n'
                     '3. Read the messages.',
            'expected': '1. Empty shows no message and the hint "No end date".\n'
                        '2. 31/12/2027 and 01/01/2028 show "Effective to must be after Effective from."\n'
                        '3. 02/01/2028 shows no message.',
            'review': 'Approve'},
 'TC-188': {'id': 'TC-188',
            'scenario_id': 'TS-040',
            'title': 'Text that is not a real date is rejected',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Typed values in Form opens: 32/13/2027, abc, 1/8/2027, 2027-08-02',
            'steps': '1. Click New scheme and enter a name.\n'
                     '2. Type each value in Form opens and leave the field.\n'
                     '3. Read the field and the messages.',
            'expected': '1. Each value shows "Enter a valid date (DD/MM/YYYY)." and is not stored.\n'
                        '2. The field never shows a value that differs from the stored date.',
            'review': 'Draft'},
 'TC-189': {'id': 'TC-189',
            'scenario_id': 'TS-040',
            'title': 'Messages show again at View and Publish and the step gets a warning mark',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Wizard with an empty name and an invalid date order',
            'steps': '1. Click New scheme and leave the name empty.\n'
                     '2. Click Next on each step until View.\n'
                     '3. Click View.',
            'expected': '1. Steps with a problem show a warning mark (for example "1 General ⚠").\n'
                        '2. The footer reads "To publish, fix n item(s) (steps marked ⚠)." and the messages are shown '
                        'again.',
            'review': 'Approve'},
 'TC-190': {'id': 'TC-190',
            'scenario_id': 'TS-041',
            'title': 'Step 2 shows nationalities, bands and match rule with defaults',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Wizard of a MOEFAS scheme, step 2',
            'steps': '1. Click New scheme, enter a name and open 2 Eligibility.\n2. Read the step.',
            'expected': '1. Nationality lists Singapore Citizen (ticked), Singapore PR, International – ASEAN and '
                        'International – non-ASEAN.\n'
                        '2. The GHI band (S$ / month) has Use this criterion (not ticked), From, To and "Empty = no '
                        'upper limit".\n'
                        '3. The PCI band (S$ / month) is ticked with From 0 and To 1,100.\n'
                        '4. Match rule offers "Any selected income band is met" and "All selected income bands are '
                        'met".',
            'review': 'Approve'},
 'TC-191': {'id': 'TC-191',
            'scenario_id': 'TS-041',
            'title': 'At least one nationality is required',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'All four nationalities unticked',
            'steps': '1. Open step 2 and untick Singapore Citizen.\n2. Read the messages.',
            'expected': '1. "Select at least one nationality." is shown.',
            'review': 'Approve'},
 'TC-192': {'id': 'TC-192',
            'scenario_id': 'TS-041',
            'title': 'At least one income band is required',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Neither GHI nor PCI ticked',
            'steps': '1. Open step 2 and untick the PCI band.\n2. Read the messages.',
            'expected': '1. "Use at least one income band (GHI or PCI)." is shown.',
            'review': 'Approve'},
 'TC-193': {'id': 'TC-193',
            'scenario_id': 'TS-041',
            'title': 'A band needs From and To may be empty for no upper limit',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'PCI band From 0, To empty\nPCI band From empty, To 1,100',
            'steps': '1. Open step 2.\n'
                     '2. Clear To and read the messages.\n'
                     '3. Restore To, clear From and read the messages.',
            'expected': '1. With To empty no message is shown and the band has no upper limit.\n'
                        '2. With From empty a message asks for From.',
            'review': 'Draft'},
 'TC-194': {'id': 'TC-194',
            'scenario_id': 'TS-041',
            'title': 'From greater than To is not allowed',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'PCI band From 2,000, To 1,000\nPCI band From 1,000, To 1,000',
            'steps': '1. Open step 2 and enter each pair.\n2. Read the messages and try to publish.',
            'expected': '1. From 2,000 with To 1,000 shows an error and Publish is blocked.\n'
                        '2. From 1,000 with To 1,000 is checked against the same rule.',
            'review': 'Draft'},
 'TC-195': {'id': 'TC-195',
            'scenario_id': 'TS-041',
            'title': 'Allowed nationalities decide where a new application goes',
            'suite': 'F4.14 New scheme wizard',
            'page': 'F10 Parent FAS application',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04, SEED-R4-N9',
            'preconditions': '1. The F4 build is connected to F5 and F10 with a clock control.\n'
                             '2. A published MOEFAS scheme that allows Singapore Citizen and Singapore PR has its form '
                             'Open.',
            'test_data': 'A Singapore PR child of Bukit View Primary (SEED-R4-N9)',
            'steps': '1. Submit a FAS application for the PR child.\n2. Read the application in F4 as MOE HQ.',
            'expected': '1. The application is MOEFAS Pending with System check Waiting, because the open MOEFAS '
                        'scheme allows PR.\n'
                        '2. No SBFAS application is created.',
            'review': 'Approve'},
 'TC-196': {'id': 'TC-196',
            'scenario_id': 'TS-042',
            'title': 'MOEFAS step 3 shows the three levels and the value type',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Wizard of a MOEFAS scheme, step 3',
            'steps': '1. Click New scheme, enter a name and open 3 Subsidy.\n2. Read the step.',
            'expected': '1. Value type offers "Percentage of fee" (default) and "Fixed amount (S$)".\n'
                        '2. The grid has the column LEVEL with the rows Primary, Secondary and Pre-University.\n'
                        '3. The text "Select a fee component above to add it." and the message "Add at least one fee '
                        'component." are shown.',
            'review': 'Approve'},
 'TC-197': {'id': 'TC-197',
            'scenario_id': 'TS-042',
            'title': 'Choosing a fee component adds a column at once with 0 in every row',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Active fee components: School fee, Miscellaneous fee, Enrichment Programme Fee, Educational '
                         'Excursion Fee, School Transport Fee, School Meal Fee',
            'steps': '1. Open step 3 and read the Fee component list.\n'
                     '2. Choose School fee.\n'
                     '3. Read the grid and the list.',
            'expected': '1. The list shows the six active components.\n'
                        '2. A column SCHOOL FEE with a ✕ is added at once, with 0 in Primary, Secondary and '
                        'Pre-University.\n'
                        '3. School fee is no longer in the list and the message "Add at least one fee component." '
                        'disappears.',
            'review': 'Approve'},
 'TC-198': {'id': 'TC-198',
            'scenario_id': 'TS-042',
            'title': 'Several components can be added and a column can be removed with the cross',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Components: School fee and School Meal Fee',
            'steps': '1. Open step 3 and choose School fee, then School Meal Fee.\n'
                     '2. Click ✕ on the School fee column.\n'
                     '3. Read the grid and the list.',
            'expected': '1. Two columns are shown after the second choice.\n'
                        '2. After ✕ only SCHOOL MEAL FEE remains and School fee is back in the list.\n'
                        '3. If the last column is removed, "Add at least one fee component." shows again.',
            'review': 'Approve'},
 'TC-199': {'id': 'TC-199',
            'scenario_id': 'TS-042',
            'title': 'Only active fee components of Function 3 are offered',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N19',
            'preconditions': '1. The F4 build is connected to F3 (fee components).\n2. Signed in as MOE HQ.',
            'test_data': 'Fee component "School Meal Fee" set to inactive in F3 (SEED-R4-N19)',
            'steps': '1. Open step 3 of a new MOEFAS scheme and read the Fee component list.',
            'expected': '1. The inactive component is not listed.',
            'review': 'Approve'},
 'TC-200': {'id': 'TC-200',
            'scenario_id': 'TS-042',
            'title': 'Changing the value type changes the unit of the cells',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Component School fee with values 100, 70, 50',
            'steps': '1. Open step 3, add School fee and enter 100, 70 and 50.\n'
                     '2. Change Value type to Fixed amount (S$).\n'
                     '3. Read the unit of the cells and the values.',
            'expected': '1. The unit next to each cell changes from % to S$.\n'
                        '2. The cell values are checked against the S$ rule (0 or more) and not the 0 to 100 rule.',
            'review': 'Approve'},
 'TC-201': {'id': 'TC-201',
            'scenario_id': 'TS-043',
            'title': 'SBFAS step 3 shows one row per grade the school offers',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Bukit View Primary offers P1 to P6. Meridian Secondary offers S1 to S4.',
            'steps': '1. Open SBFAS schemes, click New scheme, enter a name and open 3 Subsidy.\n'
                     '2. Read the rows.\n'
                     '3. Cancel. Log out, sign in as MRS-0012 and repeat.',
            'expected': '1. Bukit View Primary shows the rows P1, P2, P3, P4, P5 and P6.\n'
                        '2. Meridian Secondary shows S1, S2, S3 and S4.\n'
                        '3. No Primary, Secondary or Pre-University row is shown.',
            'review': 'Approve'},
 'TC-202': {'id': 'TC-202',
            'scenario_id': 'TS-043',
            'title': 'SBFAS component columns behave like MOEFAS',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Component School fee',
            'steps': '1. Open step 3 of a new SBFAS scheme and choose School fee.\n2. Read the grid.',
            'expected': '1. A column SCHOOL FEE with a ✕ is added with 0 in every grade row.',
            'review': 'Approve'},
 'TC-203': {'id': 'TC-203',
            'scenario_id': 'TS-043',
            'title': 'SBFAS step 1 uses a tier name and the same dates as MOEFAS',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Wizard of an SBFAS scheme, step 1',
            'steps': '1. Click New scheme and read step 1.',
            'expected': '1. The fields are the same as for MOEFAS and the blue note ends with "the school reviews the '
                        'applications".\n'
                        '2. There is no Scheme type and no Level field.',
            'review': 'Approve'},
 'TC-204': {'id': 'TC-204',
            'scenario_id': 'TS-044',
            'title': 'Percentage cells accept 0 and 100',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Component School fee, Primary cell values 0 and 100',
            'steps': '1. Open step 3, add School fee and enter 0 in Primary, read the footer.\n'
                     '2. Enter 100 and read the footer.',
            'expected': '1. Both values show "All amounts are valid."',
            'review': 'Approve'},
 'TC-205': {'id': 'TC-205',
            'scenario_id': 'TS-044',
            'title': 'Percentage cells reject values below 0 and above 100 and empty cells',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Primary cell values -1, 101 and empty',
            'steps': '1. Open step 3, add School fee.\n'
                     '2. Enter -1, then 101, then clear the cell.\n'
                     '3. Read the footer each time.',
            'expected': '1. Each case shows "Primary · School fee: enter 0–100 %."\n'
                        '2. The step gets a warning mark and Publish is blocked.',
            'review': 'Approve'},
 'TC-206': {'id': 'TC-206',
            'scenario_id': 'TS-044',
            'title': 'Percentage cells accept at most two decimals',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Primary cell values 33.33 and 33.333',
            'steps': '1. Open step 3, add School fee.\n'
                     '2. Enter 33.33 and read the footer.\n'
                     '3. Enter 33.333 and read the footer.',
            'expected': '1. 33.33 is valid.\n2. 33.333 shows an error for that cell.',
            'review': 'Draft'},
 'TC-207': {'id': 'TC-207',
            'scenario_id': 'TS-044',
            'title': 'Fixed amount cells accept 0 or more and reject negative values',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Value type Fixed amount (S$), Primary cell values 0, 120.50, 1000000, -1',
            'steps': '1. Open step 3, choose Fixed amount (S$) and add School fee.\n'
                     '2. Enter each value in turn and read the footer.',
            'expected': '1. 0, 120.50 and 1000000 show "All amounts are valid."\n'
                        '2. -1 shows "Primary · School fee: enter an amount of 0 or more."',
            'review': 'Draft'},
 'TC-208': {'id': 'TC-208',
            'scenario_id': 'TS-044',
            'title': 'An empty fixed amount cell is rejected',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Fixed amount, Primary cell empty',
            'steps': '1. Open step 3, choose Fixed amount (S$) and add School fee.\n'
                     '2. Clear the Primary cell and read the footer.',
            'expected': '1. An error is shown for the Primary cell and Publish is blocked.',
            'review': 'Draft'},
 'TC-209': {'id': 'TC-209',
            'scenario_id': 'TS-045',
            'title': 'Steps can be opened in any order and keep their values',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Name "QA Test 2028", PR ticked in step 2, School fee added in step 3',
            'steps': '1. Fill the three steps.\n'
                     '2. Click 1 General, then 3 Subsidy, then 2 Eligibility.\n'
                     '3. Read each step.',
            'expected': '1. Every step shows the values entered before.\n'
                        '2. Back and Next move one step at a time and keep the values.',
            'review': 'Approve'},
 'TC-210': {'id': 'TC-210',
            'scenario_id': 'TS-045',
            'title': 'Save draft with a name creates a Draft row',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme name "QA Draft 2028", other fields as default',
            'steps': '1. Click New scheme, enter the name and click Draft.\n2. Read the toast and the scheme list.',
            'expected': '1. A toast reads "Draft saved."\n'
                        '2. The list has a new row "QA Draft 2028" with Status Draft and only the action Edit.\n'
                        '3. The Draft card reads 1.',
            'review': 'Approve'},
 'TC-211': {'id': 'TC-211',
            'scenario_id': 'TS-045',
            'title': 'Draft without a name is not saved',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme name empty',
            'steps': '1. Click New scheme and click Draft without a name.',
            'expected': '1. "Enter a scheme name." is shown and no Draft row is created.',
            'review': 'Approve'},
 'TC-212': {'id': 'TC-212',
            'scenario_id': 'TS-045',
            'title': 'Edit reopens the draft with the saved values',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Draft "QA Draft 2028" saved with a changed Form closes 30/11/2027',
            'steps': '1. Save the draft.\n2. Click Edit on the Draft row.\n3. Read the three steps.',
            'expected': '1. The wizard opens with the saved name and dates and the incomplete steps marked.\n'
                        '2. Saving again updates the same row and does not add a second Draft.',
            'review': 'Approve'},
 'TC-213': {'id': 'TC-213',
            'scenario_id': 'TS-045',
            'title': 'Discard and Cancel leave the wizard without saving',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Name typed but not saved',
            'steps': '1. Click New scheme, type a name and click Discard.\n'
                     '2. Click New scheme again, type a name and click Cancel at the top.\n'
                     '3. Read the scheme list.',
            'expected': '1. Both actions return to the list.\n'
                        '2. No new row is added and the card counts do not change.',
            'review': 'Approve'},
 'TC-214': {'id': 'TC-214',
            'scenario_id': 'TS-046',
            'title': 'View opens the review with General, Eligibility and Subsidy',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme: "QA Probe 2028" with a valid General, Eligibility (Singapore Citizen, PCI 0 to '
                         '1,100, match rule any) and Subsidy (School fee 100, 70, 50 as fixed amounts)',
            'steps': '1. Fill the wizard with the scheme above.\n2. Click View on step 3.\n3. Read the dialog.',
            'expected': '1. The dialog "Review scheme before publishing" shows 1 · GENERAL (Scheme name, Scheme type '
                        'MOEFAS, Application form 01/08/2027 – 31/12/2027, Assessment "Automatic, after the form '
                        'closes on 31/12/2027", Effective from 01/01/2028, Effective to "No end date").\n'
                        '2. It shows 2 · ELIGIBILITY (Nationality, GHI band "Not used", PCI band "S$ 0 – 1,100", Match '
                        'rule) and 3 · SUBSIDY BY LEVEL with the values entered.\n'
                        '3. The buttons are Back to edit and Publish.',
            'review': 'Approve'},
 'TC-215': {'id': 'TC-215',
            'scenario_id': 'TS-046',
            'title': 'Publish makes the scheme view only and adds an Upcoming row',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme: "QA Probe 2028", form 01/08/2027 to 31/12/2027, Effective from 01/01/2028',
            'steps': '1. Fill the wizard and click View, then Publish.\n2. Read the toast and the scheme list.',
            'expected': '1. A toast reads "Scheme published. It is now view-only."\n'
                        '2. The list has the row "QA Probe 2028" with Approved automatically, the eligibility '
                        '"Singapore Citizen · PCI ≤ S$ 1,100.00", form badge "Not open yet", Effective from '
                        '01/01/2028, "No end date", Status Upcoming and the actions View and Add fee.\n'
                        '3. The Upcoming card shows 2.',
            'review': 'Approve'},
 'TC-216': {'id': 'TC-216',
            'scenario_id': 'TS-046',
            'title': 'Back to edit returns to the wizard with the values kept',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme: "QA Probe 2028"',
            'steps': '1. Fill the wizard and click View.\n'
                     '2. Click Back to edit and read the three steps.\n'
                     '3. Check the scheme list.',
            'expected': '1. The wizard opens with all values kept.\n2. The list has no new row.',
            'review': 'Approve'},
 'TC-217': {'id': 'TC-217',
            'scenario_id': 'TS-046',
            'title': 'A scheme with errors cannot be published',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme with an empty name and no fee component',
            'steps': '1. Click New scheme and open step 3.\n'
                     '2. Click View.\n'
                     '3. Look for a Publish button and read the messages.',
            'expected': '1. Publish is not possible. The messages "Enter a scheme name." and "Add at least one fee '
                        'component." are shown and the steps carry a warning mark.\n'
                        '2. No scheme is added.',
            'review': 'Approve'},
 'TC-218': {'id': 'TC-218',
            'scenario_id': 'TS-046',
            'title': 'The published scheme drives the limits of later applications',
            'suite': 'F4.15 Review and publish',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04',
            'preconditions': '1. The F4 build is connected to F5 and F10 with a clock control.\n'
                             '2. Signed in as MOE HQ.',
            'test_data': 'New MOEFAS scheme: GHI up to S$ 5,000.00, form open today\n'
                         'Application: GHI 4,800.00, household size 4',
            'steps': '1. Publish the scheme and let the form close (run the form-close job).\n'
                     '2. Open View on the application.',
            'expected': '1. The Eligibility check shows the limit ≤ S$ 5,000.00 from the new scheme and GHI Pass.\n'
                        '2. The application is Approved.',
            'review': 'Approve'},
 'TC-219': {'id': 'TC-219',
            'scenario_id': 'TS-047',
            'title': 'A MOEFAS scheme overlapping the effective period of another is blocked',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Published scheme A "QA Test 2028": Effective 01/01/2028 to 31/12/2028, form 01/08/2027 to '
                         '31/12/2027\n'
                         'Scheme B "QA Test B": Effective from 01/06/2028, form 01/03/2029 to 30/04/2029',
            'steps': '1. Publish scheme A.\n'
                     '2. Fill scheme B in the wizard and click View, then Publish.\n'
                     '3. Read the messages.',
            'expected': '1. Publish is blocked.\n'
                        '2. The message reads "The period overlaps with QA Test 2028 (01/01/2028 – 31/12/2028). Change '
                        'Effective from / Effective to."\n'
                        '3. Scheme B is not added.',
            'review': 'Approve'},
 'TC-220': {'id': 'TC-220',
            'scenario_id': 'TS-047',
            'title': 'A MOEFAS form period overlapping another form period is blocked',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Published scheme A "QA Test 2028": form 01/08/2027 to 31/12/2027\n'
                         'Scheme C: form 01/12/2027 to 31/01/2028, Effective from 01/01/2029 to 31/12/2029 (no '
                         'effective overlap with A)',
            'steps': '1. Publish scheme A, then fill scheme C and click Publish.\n2. Read the message.',
            'expected': '1. Publish is blocked with "The application form period overlaps with QA Test 2028 '
                        '(01/08/2027 – 31/12/2027). Change Form opens / Form closes."',
            'review': 'Approve'},
 'TC-221': {'id': 'TC-221',
            'scenario_id': 'TS-047',
            'title': 'Periods that touch without overlapping are allowed',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Published scheme A: Effective 01/01/2028 to 31/12/2028\n'
                         'Scheme D: Effective from 01/01/2029 (the day after A ends), form 01/08/2028 to 31/12/2028\n'
                         'Scheme E: Effective from 31/12/2028 (the last day of A)',
            'steps': '1. Publish scheme A and then scheme D.\n2. Fill scheme E and click Publish.',
            'expected': '1. Scheme D is published.\n2. Scheme E is blocked because 31/12/2028 is inside A.',
            'review': 'Approve'},
 'TC-222': {'id': 'TC-222',
            'scenario_id': 'TS-047',
            'title': 'SBFAS with the same name and an overlapping period is blocked',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Existing published scheme "Tier 1" (01/01/2027, no end date)\n'
                         'New scheme "Tier 1" with Effective from 01/01/2027',
            'steps': '1. Open SBFAS schemes, click New scheme and name it "Tier 1".\n'
                     '2. Keep Effective from 01/01/2027 and fill the other steps.\n'
                     '3. Click View, then Publish.',
            'expected': '1. Publish is blocked with "The period overlaps with Tier 1 (01/01/2027 – no end date). '
                        'Change Effective from / Effective to."',
            'review': 'Approve'},
 'TC-223': {'id': 'TC-223',
            'scenario_id': 'TS-047',
            'title': 'SBFAS with a different name in the same period is allowed',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'New scheme "Tier 4" with dates that overlap Tier 1 to Tier 3',
            'steps': '1. Open SBFAS schemes, click New scheme and name it "Tier 4".\n'
                     '2. Fill the other steps with the same dates as Tier 1 and publish.',
            'expected': '1. Publish succeeds and the row Tier 4 is added.',
            'review': 'Approve'},
 'TC-224': {'id': 'TC-224',
            'scenario_id': 'TS-047',
            'title': 'The same SBFAS name in another school is allowed',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user MRS-0012, Meridian Secondary.',
            'test_data': 'New scheme "Tier 1" at Meridian Secondary with the same dates as Tier 1 of Bukit View '
                         'Primary',
            'steps': '1. Open SBFAS schemes, click New scheme and name it "Tier 1".\n'
                     '2. Use the dates of Bukit View Primary Tier 1, fill the other steps and publish.',
            'expected': '1. Publish succeeds because the slot is per school and name.',
            'review': 'Approve'},
 'TC-225': {'id': 'TC-225',
            'scenario_id': 'TS-047',
            'title': 'A draft with overlapping dates can be saved and fails only at Publish',
            'suite': 'F4.15 Review and publish',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Draft with the dates of a published scheme',
            'steps': '1. Click New scheme, enter a name, set Effective from inside another MOEFAS scheme and click '
                     'Draft.\n'
                     '2. Edit the draft and click View, then Publish.',
            'expected': '1. The draft is saved.\n2. Publish shows the overlap message.',
            'review': 'Approve'},
 'TC-226': {'id': 'TC-226',
            'scenario_id': 'TS-048',
            'title': 'Publishing sets the Effective to of an earlier scheme with no end date',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Earlier scheme MOEFAS 2027 (Effective from 01/01/2027, no end date)\n'
                         'New scheme "QA Probe 2028" Effective from 01/01/2028',
            'steps': '1. Fill the wizard for the new scheme and click View.\n'
                     '2. Read the blue note.\n'
                     '3. Click Publish and read the Effective to of MOEFAS 2027.',
            'expected': '1. The blue note reads "MOEFAS 2027 has no end date. Publishing sets its Effective to '
                        '31/12/2027, the day before this scheme starts."\n'
                        '2. After Publish MOEFAS 2027 shows Effective to 31/12/2027.',
            'review': 'Approve'},
 'TC-227': {'id': 'TC-227',
            'scenario_id': 'TS-048',
            'title': 'An earlier scheme that already has an end date is left unchanged',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Earlier scheme MOEFAS 2026 (Effective to 31/12/2026)\n'
                         'New scheme with Effective from 01/01/2029',
            'steps': '1. Fill and publish a scheme that starts after MOEFAS 2026 and after MOEFAS 2027 has an end '
                     'date.\n'
                     '2. Read the review and the Effective to of MOEFAS 2026.',
            'expected': '1. No blue note about MOEFAS 2026 is shown.\n2. MOEFAS 2026 keeps Effective to 31/12/2026.',
            'review': 'Approve'},
 'TC-228': {'id': 'TC-228',
            'scenario_id': 'TS-048',
            'title': 'An earlier SBFAS scheme of the same name gets the day before as Effective to',
            'suite': 'F4.15 Review and publish',
            'page': 'Review scheme dialog (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Earlier scheme Tier 1 (01/01/2027, no end date)\n'
                         'New scheme "Tier 1" with Effective from 01/01/2028',
            'steps': '1. Fill the SBFAS wizard with the name "Tier 1" and Effective from 01/01/2028.\n'
                     '2. Click View and read the blue note, then Publish.',
            'expected': '1. The note says the earlier Tier 1 has no end date and will end on 31/12/2027.\n'
                        '2. After Publish the earlier Tier 1 shows Effective to 31/12/2027 and the new Tier 1 is '
                        'Upcoming.',
            'review': 'Approve'},
 'TC-229': {'id': 'TC-229',
            'scenario_id': 'TS-049',
            'title': 'Published rows offer View and Add fee and no Edit',
            'suite': 'F4.15 Review and publish',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Published schemes MOEFAS 2027, 2026, 2025',
            'steps': '1. Read the action cell of each row.\n2. Click View on MOEFAS 2026.',
            'expected': '1. No row has Edit.\n'
                        '2. View opens "MOEFAS 2026 · Active · view-only" with General, Eligibility and Subsidy and a '
                        'Close button only.',
            'review': 'Approve'},
 'TC-230': {'id': 'TC-230',
            'scenario_id': 'TS-049',
            'title': 'A published scheme cannot be changed through the API',
            'suite': 'F4.15 Review and publish',
            'page': 'FAS schemes API',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build exposes the scheme API.\n2. Signed in as MOE HQ.',
            'test_data': 'Published scheme MOEFAS 2026',
            'steps': '1. Send an update request that changes the PCI limit of MOEFAS 2026.\n'
                     '2. Send a delete request for MOEFAS 2026.\n'
                     '3. Read the scheme again.',
            'expected': '1. Both requests are refused and the scheme is unchanged.',
            'review': 'Draft'},
 'TC-231': {'id': 'TC-231',
            'scenario_id': 'TS-050',
            'title': 'Add fee is offered on Active and Upcoming schemes only',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01, SEED-R4-N18',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Schemes: MOEFAS 2027 (Upcoming), MOEFAS 2026 (Active), MOEFAS 2025 (Closed), a Draft '
                         '(SEED-R4-N18)',
            'steps': '1. Read the action cell of each row.',
            'expected': '1. Add fee shows on MOEFAS 2027 and MOEFAS 2026.\n'
                        '2. MOEFAS 2025 (Closed) shows View only.\n'
                        '3. The Draft shows Edit only.',
            'review': 'Approve'},
 'TC-232': {'id': 'TC-232',
            'scenario_id': 'TS-050',
            'title': 'Add fee dialog lists only components not yet in the scheme and shows the others read only',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'MOEFAS 2026 has School fee, Miscellaneous fee, School Transport Fee and School Meal Fee',
            'steps': '1. Click Add fee on MOEFAS 2026.\n2. Read the dialog.',
            'expected': '1. The dialog "Add fee components" shows "FUNCTION 4 · MOEFAS 2026 · Active" and an '
                        'explanation.\n'
                        '2. The Fee component list offers Enrichment Programme Fee and Educational Excursion Fee '
                        'only.\n'
                        '3. The four existing columns are shown with their values and cannot be edited or removed.\n'
                        '4. Add to scheme is disabled.',
            'review': 'Approve'},
 'TC-233': {'id': 'TC-233',
            'scenario_id': 'TS-050',
            'title': 'Choosing a component adds an editable column that can be removed',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Component Enrichment Programme Fee',
            'steps': '1. Click Add fee on MOEFAS 2026 and choose Enrichment Programme Fee.\n'
                     '2. Read the grid and the button.\n'
                     '3. Click ✕ on the new column.',
            'expected': '1. A column ENRICHMENT PROGRAMME FEE with a ✕ is added, with an editable cell per level that '
                        'starts at 0, and the unit %.\n'
                        '2. Add to scheme is enabled because 0 is a valid value.\n'
                        '3. After ✕ the column is gone and Add to scheme is disabled again.',
            'review': 'Approve'},
 'TC-234': {'id': 'TC-234',
            'scenario_id': 'TS-050',
            'title': 'Add to scheme stays disabled for invalid new cells',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Cell values 101, -1, 100.5 and empty (percentage)',
            'steps': '1. Click Add fee on MOEFAS 2026 and add Enrichment Programme Fee.\n'
                     '2. Enter each value in the Primary cell in turn.\n'
                     '3. Read the message and the button.',
            'expected': '1. Each value shows "Enter 0–100 % for every new cell." and Add to scheme is disabled.\n'
                        '2. 100 and 0 are accepted.',
            'review': 'Approve'},
 'TC-235': {'id': 'TC-235',
            'scenario_id': 'TS-050',
            'title': 'Add fee is not offered for a Closed scheme by any route',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build exposes the scheme API.\n2. Signed in as MOE HQ.',
            'test_data': 'Closed scheme MOEFAS 2025',
            'steps': '1. Look for Add fee on the MOEFAS 2025 row.\n'
                     '2. Send an add fee request for MOEFAS 2025 to the API.',
            'expected': '1. The row has no Add fee button.\n'
                        '2. The API refuses the request and the scheme is unchanged.',
            'review': 'Draft'},
 'TC-236': {'id': 'TC-236',
            'scenario_id': 'TS-051',
            'title': 'Add to scheme saves the new component and shows the toast',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'Critical',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme MOEFAS 2026, component Enrichment Programme Fee with 100, 70, 50',
            'steps': '1. Click Add fee on MOEFAS 2026, add the component and enter 100, 70 and 50.\n'
                     '2. Click Add to scheme.\n'
                     '3. Click View on MOEFAS 2026.',
            'expected': '1. A toast reads "Fee components added to the scheme."\n'
                        '2. The view shows the new column ENRICHMENT PROGRAMME FEE with 100%, 70% and 50% next to the '
                        'four existing columns, whose values did not change.',
            'review': 'Approve'},
 'TC-237': {'id': 'TC-237',
            'scenario_id': 'TS-051',
            'title': 'The addition is recorded with the date and the user',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Audit log (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Addition on MOEFAS 2026 by Mei Lin Tan',
            'steps': '1. Add Enrichment Programme Fee to MOEFAS 2026.\n2. Open the Audit log menu.',
            'expected': '1. A row shows the date and time, "Mei Lin Tan (MOE HQ)", the action "Scheme fee components '
                        'added" and the detail "MOEFAS 2026 · Enrichment Programme Fee".',
            'review': 'Draft'},
 'TC-238': {'id': 'TC-238',
            'scenario_id': 'TS-051',
            'title': 'Existing components cannot be changed after the addition',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme MOEFAS 2026 after the addition',
            'steps': '1. Click Add fee on MOEFAS 2026 again.\n2. Try to edit or remove an existing column.',
            'expected': '1. Existing columns, including the one added before, are read only and have no ✕.\n'
                        '2. Only components still missing are offered.',
            'review': 'Approve'},
 'TC-239': {'id': 'TC-239',
            'scenario_id': 'TS-051',
            'title': 'Students already granted the scheme get the new subsidy on open fees',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'F3 Fee invoices',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N20',
            'preconditions': '1. The F4 build is connected to F3 (fee invoices).\n'
                             '2. Student granted MOEFAS 2026 with an open invoice that includes Enrichment Programme '
                             'Fee.',
            'test_data': 'Student 00390 (Primary 4) with Enrichment Programme Fee S$ 100.00 open (SEED-R4-N20)\n'
                         'Scheme level Primary, new component value 100 %',
            'steps': '1. Read the invoice.\n'
                     '2. Add Enrichment Programme Fee to MOEFAS 2026 with Primary 100 %.\n'
                     '3. Read the invoice again.',
            'expected': '1. Before: the component has no subsidy.\n'
                        '2. After: the open invoice shows the component reduced by 100 % (S$ 0.00 to pay).',
            'review': 'Approve'},
 'TC-240': {'id': 'TC-240',
            'scenario_id': 'TS-051',
            'title': 'Future fees of the added component follow the scheme automatically',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'F3 Fee invoices',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N20',
            'preconditions': '1. The F4 build is connected to F3 (fee invoices).',
            'test_data': 'Scheme MOEFAS 2026 with Enrichment Programme Fee added at Primary 100 %\n'
                         'A new fee for Enrichment Programme Fee published afterwards (SEED-R4-N20)',
            'steps': '1. Publish the new fee in F3.\n2. Read the invoice of a Primary student granted MOEFAS 2026.',
            'expected': '1. The new fee carries the subsidy of the scheme without any manual step.',
            'review': 'Approve'},
 'TC-241': {'id': 'TC-241',
            'scenario_id': 'TS-051',
            'title': 'Add fee works the same on an SBFAS scheme',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Scheme Tier 1 of 2027, component School fee already present or not',
            'steps': '1. Click Add fee on a Tier 1 row.\n'
                     '2. Read the dialog and add a component with values for every grade.',
            'expected': '1. The dialog lists the components missing from the scheme.\n'
                        '2. Rows are the grades P1 to P6.\n'
                        '3. The addition saves with the toast "Fee components added to the scheme."',
            'review': 'Approve'},
 'TC-242': {'id': 'TC-242',
            'scenario_id': 'TS-052',
            'title': 'Close form now (demo) dialog explains what will happen',
            'suite': 'F4.17 Close form now (demo)',
            'page': 'Close form dialog (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme MOEFAS 2027 with 3 waiting applications',
            'steps': '1. Click Close form now (demo) on MOEFAS 2027.\n2. Read the dialog and click Cancel.',
            'expected': '1. The dialog "Close the application form now?" shows "DEMO ONLY · MOEFAS 2027" and the three '
                        'consequences (the form closes today, the ranking rule, rules met or not met).\n'
                        '2. The buttons are Cancel and Close form and assess.\n'
                        '3. Cancel closes the dialog and changes nothing.',
            'review': 'Approve'},
 'TC-243': {'id': 'TC-243',
            'scenario_id': 'TS-052',
            'title': 'The button sets Form closes to today and runs the assessment',
            'suite': 'F4.17 Close form now (demo)',
            'page': 'Close form dialog (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Scheme MOEFAS 2027, Form closes 31/12/2026',
            'steps': '1. Click Close form now (demo) and then Close form and assess.\n'
                     '2. Read the Application form cell.',
            'expected': '1. The toast reads "Form closed. Applications were ranked by need and assessed."\n'
                        '2. The cell shows the form period ending 18/10/2026 (today) and "Assessed 18/10/2026".\n'
                        '3. The 3 applications are assessed as in TS-004 and TS-006.',
            'review': 'Approve'},
 'TC-244': {'id': 'TC-244',
            'scenario_id': 'TS-052',
            'title': 'The button is offered only while the form is Open',
            'suite': 'F4.17 Close form now (demo)',
            'page': 'MOEFAS schemes (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Scheme MOEFAS 2027 after the demo close',
            'steps': '1. Read the action cell of MOEFAS 2027.',
            'expected': '1. The button Close form now (demo) is no longer offered because the form is no longer Open.',
            'review': 'Draft'},
 'TC-245': {'id': 'TC-245',
            'scenario_id': 'TS-053',
            'title': 'MOEFAS approval applies the level subsidy to outstanding and later fees',
            'suite': 'F4.18 Effects after a decision',
            'page': 'F3 Fee invoices',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-07, ENV-R4-04, SEED-R4-N21',
            'preconditions': '1. The F4 build is connected to F3 (fee invoices).\n'
                             '2. Student 00377 (Secondary 3) with open fees due inside 01/01/2027 to 31/12/2027.',
            'test_data': 'Scheme MOEFAS 2027 Secondary 70 % on School fee (SEED-R4-N21)',
            'steps': '1. Close the MOEFAS 2027 form so 00377 is approved.\n'
                     '2. Read the open fee invoices of 00377.\n'
                     '3. Publish a new School fee afterwards and read it.',
            'expected': '1. Open fees due inside the effective period are reduced by 70 %.\n'
                        '2. A fee published later is reduced in the same way.\n'
                        '3. Fees due before 01/01/2027 are not reduced.',
            'review': 'Approve'},
 'TC-246': {'id': 'TC-246',
            'scenario_id': 'TS-053',
            'title': 'SBFAS approval applies the grade subsidy of the chosen scheme',
            'suite': 'F4.18 Effects after a decision',
            'page': 'F3 Fee invoices',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-07, SEED-R4-N21',
            'preconditions': '1. The F4 build is connected to F3 (fee invoices).\n'
                             '2. Student 00398 (P2) with open fees inside the scheme period.',
            'test_data': 'Scheme Tier 2 P2 80 % on School fee (SEED-R4-N21)',
            'steps': '1. Approve 00398 with Tier 2.\n2. Read the open fee invoices.',
            'expected': '1. Outstanding fees inside the scheme period are reduced by 80 % and future fees follow.\n'
                        '2. The toast reads "Subsidy applied to the student\'s EA fees."',
            'review': 'Approve'},
 'TC-247': {'id': 'TC-247',
            'scenario_id': 'TS-053',
            'title': 'Every decision sends one email to the parent',
            'suite': 'F4.18 Effects after a decision',
            'page': 'Email inbox',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-05',
            'preconditions': '1. The F4 build is connected to the email service.',
            'test_data': 'Decisions: one MOEFAS approval, one MOEFAS rejection, one SBFAS approval, one SBFAS '
                         'rejection',
            'steps': '1. Run the four decisions with the test parents.\n2. Open the Email inbox.',
            'expected': '1. Each decision sends exactly one email to its parent.\n'
                        '2. Approval emails give the result and the effective date. Rejection emails give the reason.',
            'review': 'Draft'},
 'TC-248': {'id': 'TC-248',
            'scenario_id': 'TS-053',
            'title': 'A MOEFAS application that goes to SBFAS does not send a rejection email',
            'suite': 'F4.18 Effects after a decision',
            'page': 'Email inbox',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-05, SEED-R4-N7',
            'preconditions': '1. The F4 build is connected to the email service.',
            'test_data': 'Application 00412 (Also consider for SBFAS = Yes) and an application with No',
            'steps': '1. Close the form so both applications fail.\n2. Open the Email inbox.',
            'expected': '1. The parent who agreed to SBFAS gets no rejection email at this step (the school decides '
                        'later).\n'
                        '2. The parent who did not agree gets one email with the reason "Not eligible for MOEFAS".',
            'review': 'Draft'},
 'TC-249': {'id': 'TC-249',
            'scenario_id': 'TS-054',
            'title': 'The recommended tier is the first candidate scheme the household meets',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Schemes 2027: Tier 1 PCI up to 600, Tier 2 601 to 1,000, Tier 3 1,001 to 1,500 (Citizen and '
                         'PR)\n'
                         'Application 00386: PCI 940.00 (Citizen)',
            'steps': '1. Open the All tab and click View on 00386.\n'
                     '2. Read the ML recommendation block and the ML recommendation cell.',
            'expected': '1. The tier is Tier 2 (the first scheme whose band holds 940.00).\n'
                        '2. The block carries the tag "Recommendation only".',
            'review': 'Approve'},
 'TC-250': {'id': 'TC-250',
            'scenario_id': 'TS-054',
            'title': 'A household above the lower bands gets Tier 3',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. MOE HQ closed the MOEFAS 2027 form with Close form now (demo), so 00412 and 00410 are '
                             'SBFAS Pending at Bukit View Primary.\n'
                             '3. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Applications after the demo close: 00412 (PCI 1,087.50) and 00410 (PCI 1,300.00)',
            'steps': '1. Read the ML recommendation cell of 00412 and 00410 in the Pending tab.',
            'expected': '1. Both rows show Tier 3.',
            'review': 'Approve'},
 'TC-251': {'id': 'TC-251',
            'scenario_id': 'TS-054',
            'title': 'No tier is recommended when the nationality is not allowed',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as School user Lan Nguyen (BVP-0012), Bukit View Primary.',
            'test_data': 'Application 00398 (International Student, schemes accept Citizen and PR)',
            'steps': '1. Read the ML recommendation cell and the drawer block of 00398.',
            'expected': '1. The cell and the block show a dash.\n2. The tag "Recommendation only" is still shown.',
            'review': 'Approve'},
 'TC-252': {'id': 'TC-252',
            'scenario_id': 'TS-054',
            'title': 'The last tier within 5 % of its limit is recommended when none is met',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N27',
            'preconditions': '1. The F4 build is running.\n2. Signed in as a School Admin of Bukit View Primary.',
            'test_data': 'Tier 3 limit PCI 1,500.00, so 5 % over is 1,575.00 (SEED-R4-N27)\n'
                         'Applications with PCI 1,575.00 and PCI 1,575.01 (Citizen)',
            'steps': '1. Open Review on each application.\n2. Read the ML recommendation.',
            'expected': '1. PCI 1,575.00 shows Tier 3 (within 5 % of the last tier).\n2. PCI 1,575.01 shows a dash.',
            'review': 'Approve'},
 'TC-253': {'id': 'TC-253',
            'scenario_id': 'TS-054',
            'title': 'Candidates are the schemes whose form period holds the submit date',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N16',
            'preconditions': '1. The F4 build is running with a clock control.\n2. Signed in as a School Admin.',
            'test_data': 'Schemes 2026 (form 01/08/2025 to 31/12/2025) and 2027 (form 01/08/2026 to 31/12/2026)\n'
                         'Applications submitted on 14/11/2025 and on 17/10/2026 (SEED-R4-N16)',
            'steps': '1. Open Review on both applications.\n2. Read the ML recommendation of each.',
            'expected': '1. The application of 14/11/2025 is judged against the 2026 schemes.\n'
                        '2. The application of 17/10/2026 is judged against the 2027 schemes.',
            'review': 'Approve'},
 'TC-254': {'id': 'TC-254',
            'scenario_id': 'TS-054',
            'title': 'Without a scheme the recommendation is a dash and the drawer shows the red note',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Review drawer (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, SEED-R4-N15',
            'preconditions': '1. The F4 build is running.\n'
                             '2. Signed in as a School Admin whose school has no published SBFAS scheme.',
            'test_data': 'Pending SBFAS application of that school (SEED-R4-N15)',
            'steps': '1. Read the ML recommendation cell and the drawer block.',
            'expected': '1. The cell shows a dash and the drawer shows a dash with the red note.',
            'review': 'Draft'},
 'TC-255': {'id': 'TC-255',
            'scenario_id': 'TS-055',
            'title': 'ML risk of the sample rows follows their Need Score',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'FAS applications (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Rows: 00377 (Need Score 59.72), 00412 (52.13), 00390 (78.67), 00328 (Low)',
            'steps': '1. Read the ML risk column.',
            'expected': '1. 00377 and 00412 show Medium, 00390 shows High, 00328 shows Low.',
            'review': 'Draft'},
 'TC-256': {'id': 'TC-256',
            'scenario_id': 'TS-055',
            'title': 'Need Score 75.00 is High and 74.99 is Medium',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN18: GHI 0, size 2, workers 2, members under 21: 1, never aided, stable, no flags\n'
                         'EN19: GHI 2, size 2, other inputs as EN18',
            'steps': '1. Call the engine with EN18.\n2. Call the engine with EN19.\n3. Read Need Score and risk.',
            'expected': '1. EN18 gives Need Score 75.00 and ML risk High.\n'
                        '2. EN19 gives Need Score 74.99 and ML risk Medium.',
            'review': 'Draft'},
 'TC-257': {'id': 'TC-257',
            'scenario_id': 'TS-055',
            'title': 'Need Score 50.00 is Medium and 49.99 is Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN20: GHI 4,500, size 4, workers 3, members under 21: 1, never aided, stable, no flags\n'
                         'EN21: GHI 4,502, other inputs as EN20',
            'steps': '1. Call the engine with EN20.\n2. Call the engine with EN21.\n3. Read Need Score and risk.',
            'expected': '1. EN20 gives Need Score 50.00 and ML risk Medium.\n'
                        '2. EN21 gives Need Score 49.99 and ML risk Low.',
            'review': 'Draft'},
 'TC-258': {'id': 'TC-258',
            'scenario_id': 'TS-055',
            'title': 'Deny rule DENY-NO-CHILDREN gives Need Score 0 and ML risk Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN41: GHI 3,000, size 3, workers 2, members under 21: 0, stable, no flags, Citizen',
            'steps': '1. Call the engine with the inputs.\n2. Read Need Score, risk and recommended tier.',
            'expected': '1. Need Score is 0 and ML risk is Low.\n'
                        '2. No tier is recommended (a dash on screen).\n'
                        '3. Only the rule DENY-NO-CHILDREN matches.',
            'review': 'Draft'},
 'TC-259': {'id': 'TC-259',
            'scenario_id': 'TS-055',
            'title': 'Deny rule DENY-ONLY-CHILDREN gives Need Score 0 and ML risk Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN42: GHI 3,000, size 3, workers 0, members under 21: 3, stable, no flags, Citizen',
            'steps': '1. Call the engine with the inputs.\n2. Read Need Score, risk and recommended tier.',
            'expected': '1. Need Score is 0 and ML risk is Low.\n'
                        '2. No tier is recommended (a dash on screen).\n'
                        '3. Only the rule DENY-ONLY-CHILDREN matches.',
            'review': 'Draft'},
 'TC-260': {'id': 'TC-260',
            'scenario_id': 'TS-055',
            'title': 'Deny rule DENY-INVALID-SIZE gives Need Score 0 and ML risk Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN43: GHI 3,000, size 0, workers 0, members under 21: 1, stable, no flags, Citizen',
            'steps': '1. Call the engine with the inputs.\n2. Read Need Score, risk and recommended tier.',
            'expected': '1. Need Score is 0 and ML risk is Low.\n'
                        '2. No tier is recommended (a dash on screen).\n'
                        '3. Only the rule DENY-INVALID-SIZE matches.',
            'review': 'Draft'},
 'TC-261': {'id': 'TC-261',
            'scenario_id': 'TS-055',
            'title': 'Deny rule DENY-WORKERS-EXCEED-SIZE gives Need Score 0 and ML risk Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN44: GHI 3,000, size 3, workers 4, members under 21: 1, stable, no flags, Citizen',
            'steps': '1. Call the engine with the inputs.\n2. Read Need Score, risk and recommended tier.',
            'expected': '1. Need Score is 0 and ML risk is Low.\n'
                        '2. No tier is recommended (a dash on screen).\n'
                        '3. Only the rule DENY-WORKERS-EXCEED-SIZE matches.',
            'review': 'Draft'},
 'TC-262': {'id': 'TC-262',
            'scenario_id': 'TS-055',
            'title': 'Deny rule DENY-NEGATIVE-MONTHS gives Need Score 0 and ML risk Low',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'EN45: GHI 3,000, size 3, workers 1, members under 21: 1, months since last aid -1, stable, '
                         'no flags, Citizen',
            'steps': '1. Call the engine with the inputs.\n2. Read Need Score, risk and recommended tier.',
            'expected': '1. Need Score is 0 and ML risk is Low.\n'
                        '2. No tier is recommended (a dash on screen).\n'
                        '3. Only the rule DENY-NEGATIVE-MONTHS matches.',
            'review': 'Draft'},
 'TC-263': {'id': 'TC-263',
            'scenario_id': 'TS-055',
            'title': 'Need Score weights are 0.70, 0.05, 0.10, 0.10 and 0.05',
            'suite': 'F4.19 ML recommendation and risk',
            'page': 'Scoring engine',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-06',
            'preconditions': '1. The engine can be called by API or unit test.',
            'test_data': 'Case EN01 (APP-2026-00377): GHI 4,120, size 4, workers 1, members under 21: 2, aided 6 '
                         'months ago, interrupted, no flags',
            'steps': '1. Call the engine with EN01.\n2. Read the five feature values and the Need Score.',
            'expected': '1. Need Score equals 100 × (0.70 × income + 0.05 × dependency + 0.10 × stability + 0.10 × '
                        'recency + 0.05 × vulnerability) and is 59.72.',
            'review': 'Draft'},
 'TC-264': {'id': 'TC-264',
            'scenario_id': 'TS-056',
            'title': 'Money shows as S$ with thousands separator and two decimals',
            'suite': 'F4.20 Formats',
            'page': 'Applications and drawers',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Rows: 00412 and the schemes MOEFAS 2027, Tier 1 to Tier 3',
            'steps': '1. Open View on 00412 and read the money values.\n'
                     '2. Open MOEFAS schemes and read the Eligibility column.',
            'expected': '1. The drawer shows S$ 4,350.00 and S$ 1,050.00 with two decimals.\n'
                        '2. The Eligibility column shows the same format for every band.',
            'review': 'Approve'},
 'TC-265': {'id': 'TC-265',
            'scenario_id': 'TS-056',
            'title': 'Dates show as DD/MM/YYYY everywhere',
            'suite': 'F4.20 Formats',
            'page': 'FAS applications and schemes',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).',
            'test_data': 'Screens: list, drawer, History, scheme list, review dialog',
            'steps': '1. Read the Submitted column of the list and the dates on the other screens.',
            'expected': '1. Every date has the form DD/MM/YYYY, for example 17/10/2026.\n'
                        '2. The Submitted column of the list shows the date in that form.\n'
                        '3. The scheme list shows Effective from and Effective to in the same form.',
            'review': 'Approve'},
 'TC-266': {'id': 'TC-266',
            'scenario_id': 'TS-056',
            'title': 'Times show as HH:mm and use Singapore time',
            'suite': 'F4.20 Formats',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Prototype: edusave.vercel.app (sample date 18/10/2026)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-01',
            'preconditions': '1. The prototype is open at the base state (use Reset data).\n'
                             '2. Signed in as MOE HQ (Mei Lin Tan).\n'
                             '3. The MOEFAS 2027 form was closed with Close form now (demo), so the 3 waiting '
                             'applications are assessed.',
            'test_data': 'Rows: 00377 History and Decided by',
            'steps': '1. Open View on 00377 and read the times in History and Decided by.',
            'expected': '1. Each time has the form HH:mm on a 24-hour clock, for example 10:05 and 09:30.',
            'review': 'Approve'},
 'TC-267': {'id': 'TC-267',
            'scenario_id': 'TS-056',
            'title': 'Times follow Singapore time whatever the browser time zone is',
            'suite': 'F4.20 Formats',
            'page': 'Review drawer (MOE HQ)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02, ENV-R4-04',
            'preconditions': '1. The F4 build is running.\n2. The computer time zone is set to UTC-5.',
            'test_data': 'An application submitted at 17/10/2026 23:30 Singapore time',
            'steps': '1. Open FAS applications and read the Submitted date.\n2. Open View and read the History time.',
            'expected': '1. The list shows 17/10/2026 and the History shows 17/10/2026 23:30.\n'
                        '2. The browser time zone has no effect.',
            'review': 'Approve'},
 'TC-268': {'id': 'TC-268',
            'scenario_id': 'TS-057',
            'title': 'SBFAS scheme name is required',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Names: empty and three spaces.',
            'steps': '1. Send the base request with name empty.\n2. Send it again with name made of three spaces.',
            'expected': '1. Both requests are refused with HTTP 400 and the message "name is required.".\n'
                        '2. No scheme is created.',
            'review': 'Approve'},
 'TC-269': {'id': 'TC-269',
            'scenario_id': 'TS-057',
            'title': 'SBFAS scheme name accepts 150 characters and refuses 151',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Names of 150 and 151 characters.',
            'steps': '1. Send the base request with a name of 150 characters.\n'
                     '2. Send it again with a name of 151 characters.',
            'expected': '1. The 150-character name is accepted (HTTP 201).\n'
                        '2. The 151-character name is refused with 400 "name must not exceed 150 characters.".',
            'review': 'Approve'},
 'TC-270': {'id': 'TC-270',
            'scenario_id': 'TS-057',
            'title': 'SBFAS Application open from must be today or later',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. openFrom: today (UTC date) and yesterday.',
            'steps': '1. Send the base request with Application open from set to today and the other dates after it.\n'
                     '2. Send it again with Application open from set to yesterday.',
            'expected': '1. Today is accepted (201).\n'
                        '2. Yesterday is refused with 400 "openFrom must be today or later.".',
            'review': 'Approve'},
 'TC-271': {'id': 'TC-271',
            'scenario_id': 'TS-057',
            'title': 'SBFAS Application open to must be after Application open from',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. openTo equal to openFrom.',
            'steps': '1. Send the base request with Application open to equal to Application open from.',
            'expected': '1. The request is refused with 400 "openTo must be after openFrom.".',
            'review': 'Approve'},
 'TC-272': {'id': 'TC-272',
            'scenario_id': 'TS-057',
            'title': 'SBFAS Effective from must be after Application open to',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. effectiveFrom equal to openTo.',
            'steps': '1. Send the base request with Effective from equal to Application open to.',
            'expected': '1. The request is refused with 400 "effectiveFrom must be after openTo.".',
            'review': 'Approve'},
 'TC-273': {'id': 'TC-273',
            'scenario_id': 'TS-057',
            'title': 'SBFAS Effective to must be after Effective from and may be empty',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. effectiveTo equal to effectiveFrom, and null.',
            'steps': '1. Send the base request with Effective to equal to Effective from.\n'
                     '2. Send it again with Effective to empty (null).',
            'expected': '1. The first request is refused with 400 "effectiveTo must be after effectiveFrom.".\n'
                        '2. The second request is accepted (no end date).',
            'review': 'Approve'},
 'TC-274': {'id': 'TC-274',
            'scenario_id': 'TS-057',
            'title': 'SBFAS total budget cannot be negative and must be above 0 to publish',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Budgets: -1, 0 as draft and 0 with publish true.',
            'steps': '1. Send the base request with budget -1.\n'
                     '2. Send it with budget 0 and publish false.\n'
                     '3. Send it with budget 0 and publish true.',
            'expected': '1. Refused with 400 "totalBudgetAmount must be greater than or equal to 0.".\n'
                        '2. Accepted as a draft.\n'
                        '3. Refused with 400 "totalBudgetAmount must be greater than 0 when publishing.".',
            'review': 'Approve'},
 'TC-275': {'id': 'TC-275',
            'scenario_id': 'TS-058',
            'title': 'SBFAS nationality list is required, valid and without duplicates',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Lists: [], [XX], [SC, SC] and all four codes.',
            'steps': '1. Send the base request with nationalities [].\n'
                     '2. Send it with ["XX"].\n'
                     '3. Send it with ["SC","SC"].\n'
                     '4. Send it with SC, PR, IS_ASEAN and IS_NON_ASEAN.',
            'expected': '1. 400 "At least one nationality is required.".\n'
                        '2. 400 "nationality must be one of: SC, PR, IS_ASEAN, IS_NON_ASEAN.".\n'
                        '3. 400 "nationalities must not contain duplicates.".\n'
                        '4. Accepted.',
            'review': 'Approve'},
 'TC-276': {'id': 'TC-276',
            'scenario_id': 'TS-058',
            'title': 'SBFAS needs at least one of the GHI band and the PCI band',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. GHI off and PCI off.',
            'steps': '1. Send the base request with isGhiEnabled false and isPciEnabled false.',
            'expected': '1. Refused with 400 "At least one of GHI or PCI criteria must be enabled.".',
            'review': 'Approve'},
 'TC-277': {'id': 'TC-277',
            'scenario_id': 'TS-058',
            'title': 'SBFAS PCI From is required when the PCI band is on',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. pciFrom null with isPciEnabled true.',
            'steps': '1. Send the base request with pciFrom null and pciTo 1000.',
            'expected': '1. Refused with 400 "pciFrom is required when PCI is enabled.".',
            'review': 'Approve'},
 'TC-278': {'id': 'TC-278',
            'scenario_id': 'TS-058',
            'title': 'SBFAS GHI From is required when the GHI band is on',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. GHI on with ghiFrom null, ghiTo 100, operator OR.',
            'steps': '1. Send the base request with isGhiEnabled true, ghiFrom null, ghiTo 100 and incomeOperator OR.',
            'expected': '1. Refused with 400 "ghiFrom is required when GHI is enabled.".',
            'review': 'Approve'},
 'TC-279': {'id': 'TC-279',
            'scenario_id': 'TS-058',
            'title': 'SBFAS band values are not negative and To is not below From',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. ghiFrom -5; pciFrom -1; pciFrom 500 with pciTo '
                         '100; ghiFrom 500 with ghiTo 100; pciTo null.',
            'steps': '1. Send each wrong value in its own request.\n2. Send pciTo null.',
            'expected': '1. Each wrong value is refused with 400: "ghiFrom must be >= 0.", "pciFrom must be >= 0.", '
                        '"pciTo must be >= pciFrom.", "ghiTo must be >= ghiFrom.".\n'
                        '2. An empty To is accepted (no upper limit).',
            'review': 'Approve'},
 'TC-280': {'id': 'TC-280',
            'scenario_id': 'TS-058',
            'title': 'SBFAS match rule is needed when both bands are on',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Operators: null, XOR, AND.',
            'steps': '1. Send the base request with GHI and PCI both on and incomeOperator null.\n'
                     '2. Send it with XOR.\n'
                     '3. Send it with AND.',
            'expected': '1. 400 "incomeOperator is required when both GHI and PCI are enabled.".\n'
                        '2. 400 "incomeOperator must be \'AND\' or \'OR\'.".\n'
                        '3. Accepted.',
            'review': 'Approve'},
 'TC-281': {'id': 'TC-281',
            'scenario_id': 'TS-058',
            'title': 'SBFAS scheme context accepts 1000 characters and refuses 1001',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. eligibilityDescription of 1000 and 1001 '
                         'characters.',
            'steps': '1. Send the base request with a context of 1000 characters.\n2. Send it with 1001 characters.',
            'expected': '1. Accepted.\n2. Refused with 400 "eligibilityDescription must not exceed 1000 characters.".',
            'review': 'Approve'},
 'TC-282': {'id': 'TC-282',
            'scenario_id': 'TS-059',
            'title': 'SBFAS scheme needs a fee component with at least one grade',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. feeComponents [] and a component with items [].',
            'steps': '1. Send the base request with feeComponents [].\n2. Send it with one component and items [].',
            'expected': '1. 400 "At least one fee component is required.".\n'
                        '2. 400 "Each fee component needs at least one item.".',
            'review': 'Approve'},
 'TC-283': {'id': 'TC-283',
            'scenario_id': 'TS-059',
            'title': 'SBFAS percentage accepts 0 to 100 and refuses values outside',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Percentages -1, 101, 0 and 100.',
            'steps': '1. Send the base request with -1 for every grade.\n'
                     '2. Send it with 101.\n'
                     '3. Send it with 0 for one grade and 100 for the other.',
            'expected': '1. and 2. Refused with 400 "subsidyPercentage must be between 0 and 100.".\n3. Accepted.',
            'review': 'Approve'},
 'TC-284': {'id': 'TC-284',
            'scenario_id': 'TS-059',
            'title': 'SBFAS percentage accepts at most two decimals',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Percentages 33.333 and 33.33.',
            'steps': '1. Send the base request with 33.333 for every grade.\n2. Send it with 33.33.',
            'expected': '1. Refused with 400 "subsidyPercentage must have at most 2 decimals.".\n2. Accepted.',
            'review': 'Approve'},
 'TC-285': {'id': 'TC-285',
            'scenario_id': 'TS-059',
            'title': 'SBFAS refuses a fee component or a grade that is listed twice',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. The same fee component twice; the same grade twice '
                         'in one component.',
            'steps': '1. Send the base request with the same feeComponentId in two entries.\n'
                     '2. Send it with one grade twice in the items of a component.',
            'expected': '1. 400 "feeComponents must not contain duplicate feeComponentId.".\n'
                        '2. 400 "academicLevelId must not be duplicated within a fee component.".',
            'review': 'Approve'},
 'TC-286': {'id': 'TC-286',
            'scenario_id': 'TS-059',
            'title': 'SBFAS refuses a fee component that does not exist',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. feeComponentId '
                         '00000000-0000-0000-0000-000000000099 (also tried on MOEFAS).',
            'steps': '1. Send the base request with an unknown feeComponentId.\n'
                     '2. Send the MOEFAS base request with an unknown feeComponentId as MOE HQ.',
            'expected': '1. Refused with a 400 or 404 that says the fee component does not exist.\n2. Same for MOEFAS.',
            'review': 'Approve'},
 'TC-287': {'id': 'TC-287',
            'scenario_id': 'TS-059',
            'title': 'SBFAS refuses a grade that is not offered by the school',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. academicLevelId AL-NOPE.',
            'steps': '1. Send the base request with one item whose academicLevelId is AL-NOPE.',
            'expected': '1. Refused with a 400 or 404 that says the grade does not exist for the school.',
            'review': 'Approve'},
 'TC-288': {'id': 'TC-288',
            'scenario_id': 'TS-059',
            'title': 'SBFAS needs a percentage for every active grade of the school',
            'suite': 'F4.14 New scheme wizard',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Items for Junior College 1 only, the school also '
                         'offers Secondary 1.',
            'steps': '1. Send the base request with items for Junior College 1 only.',
            'expected': '1. Refused: every active grade needs a value (0 percent if none).',
            'review': 'Approve'},
 'TC-289': {'id': 'TC-289',
            'scenario_id': 'TS-061',
            'title': 'Add fee API refuses percentages outside 0 to 100 and more than two decimals',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Published scheme; new fee component with -1, 101 '
                         'and 33.333.',
            'steps': '1. Create a Published scheme (publish true, budget 1000).\n'
                     '2. POST fee-components with -1 for every grade.\n'
                     '3. Repeat with 101.\n'
                     '4. Repeat with 33.333.',
            'expected': '1. and 2. 400 "subsidyPercentage must be between 0 and 100.".\n'
                        '3. 400 "subsidyPercentage must have at most 2 decimals.".',
            'review': 'Approve'},
 'TC-290': {'id': 'TC-290',
            'scenario_id': 'TS-061',
            'title': 'Add fee API needs at least one item and no repeated grade',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Items [] and one grade twice.',
            'steps': '1. POST fee-components with items [].\n2. POST with one grade twice.',
            'expected': '1. 400 "At least one item is required.".\n'
                        '2. 400 "academicLevelId must not be duplicated within the fee component.".',
            'review': 'Approve'},
 'TC-291': {'id': 'TC-291',
            'scenario_id': 'TS-061',
            'title': 'Add fee API refuses a fee component already in the scheme',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. The component of the base request posted again.',
            'steps': '1. POST fee-components with the feeComponentId that the scheme already has.',
            'expected': '1. Refused with 409 "This fee component is already configured for the scheme.".',
            'review': 'Approve'},
 'TC-292': {'id': 'TC-292',
            'scenario_id': 'TS-061',
            'title': 'Add fee API refuses a fee component or grade that does not exist',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'SBFAS scheme API (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective '
                         '2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with '
                         '10 percent for each grade, publish false. Unknown feeComponentId; unknown academicLevelId '
                         'AL-NOPE.',
            'steps': '1. POST fee-components with an unknown feeComponentId.\n'
                     '2. POST with a known component and academicLevelId AL-NOPE.',
            'expected': '1. and 2. Refused with a 400 or 404.',
            'review': 'Approve'},
 'TC-293': {'id': 'TC-293',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS scheme name is required and at most 150 characters',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Names: empty, 150 and 151 characters.',
            'steps': '1. Send the base request with name empty.\n'
                     '2. Send it with 150 characters.\n'
                     '3. Send it with 151 characters.',
            'expected': '1. 400 "Scheme name is required.".\n'
                        '2. Accepted.\n'
                        '3. 400 "Scheme name cannot exceed 150 characters.".',
            'review': 'Approve'},
 'TC-294': {'id': 'TC-294',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS dates must follow Form opens < Form closes < Effective from < Effective to',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Form closes equal to Form opens; Form closes the same day at '
                         '23:59:59; Effective from equal to Form closes; Effective to equal to Effective from.',
            'steps': '1. Send the base request with Form closes equal to Form opens (same date and time).\n'
                     '2. Send it with Form closes on the same day at 23:59:59.\n'
                     '3. Send it with Effective from equal to Form closes.\n'
                     '4. Send it with Effective to equal to Effective from.',
            'expected': '1. 400 "OpenTo must be later than OpenFrom.".\n'
                        '2. Accepted (the wizard sends the closing time 23:59:59, which explains TC-185).\n'
                        '3. 400 "EffectiveFrom must be later than OpenTo.".\n'
                        '4. 400 "EffectiveTo must be later than EffectiveFrom.".',
            'review': 'Approve'},
 'TC-295': {'id': 'TC-295',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS refuses a scheme whose dates are in the past',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Form 2020-01-01 to 2020-06-30, Effective from 2021-01-01.',
            'steps': '1. Send the base request with all dates in 2020 and 2021.',
            'expected': '1. Refused: a new scheme cannot start in the past (as the SBFAS API does with "openFrom must '
                        'be today or later.").',
            'review': 'Approve'},
 'TC-296': {'id': 'TC-296',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS status must be Draft or Published',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Status Archived.',
            'steps': '1. Send the base request with status Archived.',
            'expected': '1. Refused with 400 "Status must be Draft or Published".',
            'review': 'Approve'},
 'TC-297': {'id': 'TC-297',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS income bands follow the eligibility rules',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. GHI and PCI off; ghiFrom -1; pciFrom 500 with pciTo 100; both '
                         'bands on with operator null.',
            'steps': '1. Send the base request with both bands off.\n'
                     '2. Send it with ghiFrom -1.\n'
                     '3. Send it with pciFrom 500 and pciTo 100.\n'
                     '4. Send it with both bands on and incomeOperator null.',
            'expected': '1. 400 "At least one income evaluation criterion (GHI or PCI) must be enabled.".\n'
                        '2. 400 "GhiFrom cannot be negative.".\n'
                        '3. 400 "PciTo must be greater than or equal to PciFrom.".\n'
                        '4. 400 "IncomeOperator must be \'AND\' or \'OR\' when both GHI and PCI are enabled.".',
            'review': 'Approve'},
 'TC-298': {'id': 'TC-298',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS nationality list is required, valid and without duplicates',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Lists: [], [XX], [SC, SC].',
            'steps': '1. Send the base request with nationalities [].\n'
                     '2. Send it with ["XX"].\n'
                     '3. Send it with ["SC","SC"].',
            'expected': '1. 400 "At least one eligible nationality must be specified.".\n'
                        '2. 400 "Invalid nationality. Allowed values: SC, PR, IS_ASEAN, IS_NON_ASEAN.".\n'
                        '3. 400 "Nationalities list must not contain duplicates.".',
            'review': 'Approve'},
 'TC-299': {'id': 'TC-299',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS subsidies are required, with a valid stage and no repeated stage and component',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. subsidies []; stage KINDER; the same stage and component twice.',
            'steps': '1. Send the base request with subsidies [].\n'
                     '2. Send it with educationStage KINDER.\n'
                     '3. Send it with PRIMARY and the same component twice.',
            'expected': '1. 400 "At least one subsidy configuration is required.".\n'
                        '2. 400 "EducationStage must be PRIMARY, SECONDARY, or PRE_UNIVERSITY.".\n'
                        '3. 400 "Subsidies must not contain duplicate combinations of EducationStage and '
                        'FeeComponentId.".',
            'review': 'Approve'},
 'TC-300': {'id': 'TC-300',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS percentage accepts 0 to 100 and refuses values outside',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Percentages -1 and 101.',
            'steps': '1. Send the base request with -1 for every stage.\n2. Send it with 101.',
            'expected': '1. and 2. Refused with 400 "SubsidyPercentage must be between 0.00% and 100.00%.".',
            'review': 'Approve'},
 'TC-301': {'id': 'TC-301',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS percentage accepts at most two decimals',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S3',
            'priority': 'Low',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Percentage 33.333.',
            'steps': '1. Send the base request with 33.333 for every stage.',
            'expected': '1. Refused: only two decimals are allowed (as the SBFAS API does).',
            'review': 'Approve'},
 'TC-302': {'id': 'TC-302',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS total budget cannot be negative',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Budget -1.',
            'steps': '1. Send the base request with budget -1.',
            'expected': '1. Refused with 400 "TotalBudgetAmount cannot be negative.".',
            'review': 'Approve'},
 'TC-303': {'id': 'TC-303',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS refuses a second scheme with the same name',
            'suite': 'F4.14 New scheme wizard',
            'page': 'MOEFAS scheme API (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal '
                   'proxy\n'
                   'Requests sent with the session cookie of the signed in user\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective '
                         '3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent '
                         'for each stage, budget 1000. Name of 150 characters sent twice.',
            'steps': '1. Send the base request with a name of 150 characters.\n2. Send the same name again.',
            'expected': '1. Accepted.\n2. Refused with a message that the name already exists.',
            'review': 'Approve'},
 'TC-304': {'id': 'TC-304',
            'scenario_id': 'TS-057',
            'title': 'SBFAS wizard shows the required messages of step General',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Step General left empty; name made of spaces.',
            'steps': '1. Open SBFAS schemes and click New scheme.\n'
                     '2. Click Next without typing.\n'
                     '3. Type spaces in the name and click Next.',
            'expected': '1. The step stays on General.\n'
                        '2. Each required field shows a message: "Name is required.", "Opening date is required.", '
                        '"Closing date is required.", "Effective date is required.".\n'
                        '3. Spaces only give "Name is required.".',
            'review': 'Approve'},
 'TC-305': {'id': 'TC-305',
            'scenario_id': 'TS-057',
            'title': 'SBFAS wizard checks the order of the dates',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Closing = opening; effective date = closing; effective end = effective date; opening date '
                         'yesterday.',
            'steps': '1. Fill step General with a valid scheme.\n'
                     '2. Set Applications open to equal to Applications open from and click Next.\n'
                     '3. Set Effective from equal to Applications open to and click Next.\n'
                     '4. Set Effective to equal to Effective from and click Next.\n'
                     '5. Set Applications open from to yesterday and click Next.\n'
                     '6. Clear Effective to and click Next.',
            'expected': '1. "Closing date must be after opening date.".\n'
                        '2. "Effective date must be after the closing date.".\n'
                        '3. "Effective end date must be after the effective date.".\n'
                        '4. "Opening date cannot be before today.".\n'
                        '5. An empty Effective to is accepted and the step moves to Eligibility.',
            'review': 'Approve'},
 'TC-306': {'id': 'TC-306',
            'scenario_id': 'TS-057',
            'title': 'SBFAS wizard limits the scheme name to 150 characters',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Names of 150 and 151 characters.',
            'steps': '1. Fill step General with a name of 151 characters and click Next.\n'
                     '2. Use 150 characters and click Next.',
            'expected': '1. "Name must be 150 characters or fewer." and the step stays on General.\n'
                        '2. The step moves to Eligibility.',
            'review': 'Approve'},
 'TC-307': {'id': 'TC-307',
            'scenario_id': 'TS-057',
            'title': 'SBFAS wizard total budget accepts 0 or more with two decimals',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Budget values -1, abc, empty, 0 and 1234.567.',
            'steps': '1. Fill step General with a valid scheme.\n'
                     '2. Set Total budget to -1, then to abc, then empty, then 1234.567 and click Next each time.\n'
                     '3. Set 0 and click Next.',
            'expected': '1. -1 shows a message that the budget cannot be negative.\n'
                        '2. abc and empty show a message that a number is needed.\n'
                        '3. 1234.567 shows a message about two decimals.\n'
                        '4. 0 is accepted.',
            'review': 'Approve'},
 'TC-308': {'id': 'TC-308',
            'scenario_id': 'TS-058',
            'title': 'SBFAS wizard needs a nationality and an income band with valid values',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'No nationality; both bands off; PCI From empty; PCI From 500 with To 100; PCI From -1; To '
                         'empty.',
            'steps': '1. Open step Eligibility with a valid step General.\n'
                     '2. Click Next with no nationality ticked.\n'
                     '3. Tick Singapore citizen and switch both bands off, click Next.\n'
                     '4. Switch PCI on and clear From, click Next.\n'
                     '5. Enter From 500 and To 100, click Next.\n'
                     '6. Enter From -1, click Next.\n'
                     '7. Enter From 0 and clear To, click Next.',
            'expected': '2. "Select at least one nationality.".\n'
                        '3. "Enable at least one income band.".\n'
                        '4. and 6. A message that From must be 0 or more.\n'
                        '5. A message that To must not be below From.\n'
                        '7. Accepted, the step moves to Subsidy.',
            'review': 'Approve'},
 'TC-309': {'id': 'TC-309',
            'scenario_id': 'TS-059',
            'title': 'SBFAS wizard checks the percentage cells',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.',
            'test_data': 'Cell values -1, 101, 33.333, empty, 0 and 100.',
            'steps': '1. Open step Subsidy, add one fee component.\n'
                     '2. Type -1 in one cell and click Review.\n'
                     '3. Repeat with 101, 33.333 and an empty cell.\n'
                     '4. Enter 0 and 100 and click Review.',
            'expected': '1. Each wrong value blocks Review and names the allowed range 0 to 100 (33.333: two '
                        'decimals).\n'
                        '2. 0 and 100 are accepted and Review opens.',
            'review': 'Approve'},
 'TC-310': {'id': 'TC-310',
            'scenario_id': 'TS-057',
            'title': 'SBFAS wizard shows why a duplicate scheme name is refused',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.\n'
                             '4. A scheme named R4-AUTO-ui-probe exists as a Draft.',
            'test_data': 'Name R4-AUTO-ui-probe used twice.',
            'steps': '1. Complete the four steps of a new scheme with the name of the existing scheme.\n'
                     '2. Click Save draft.\n'
                     '3. Click Publish.',
            'expected': '1. and 2. The scheme is not created and the message says that a scheme with this name already '
                        'exists.',
            'review': 'Approve'},
 'TC-311': {'id': 'TC-311',
            'scenario_id': 'TS-061',
            'title': 'SBFAS Add fee dialog blocks invalid percentages and saves valid ones',
            'suite': 'F4.16 Add fee to a published scheme',
            'page': 'Add fee dialog (School Admin)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two '
                             'active grades: Junior College 1 and Secondary 1.\n'
                             '3. At least one active fee component exists for the school.\n'
                             '4. A Published SBFAS scheme with one fee component exists.',
            'test_data': 'Percentages 101, -1, 33.333, empty, then 15 and 20.',
            'steps': '1. Open the row menu of the Published scheme and click Add fee.\n'
                     '2. Choose a fee that is not in the scheme.\n'
                     '3. Enter 101 for one grade and click Add fee.\n'
                     '4. Repeat with -1, 33.333 and an empty field.\n'
                     '5. Enter 15 and 20 and click Add fee.',
            'expected': '1. The dialog stays open and nothing is saved for each wrong value (empty field: a message '
                        'with the range).\n'
                        '2. 15 and 20 are saved with a success message and the fee count goes up by one.',
            'review': 'Approve'},
 'TC-312': {'id': 'TC-312',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS wizard limits the scheme name to 150 characters',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'Names of 150 and 151 characters.',
            'steps': '1. Open MOEFAS and click New scheme.\n'
                     '2. Fill step General with a name of 151 characters and click Next.\n'
                     '3. Use 150 characters and click Next.',
            'expected': '1. A message that the name must not exceed 150 characters and the step stays on General.\n'
                        '2. The step moves to Eligibility.',
            'review': 'Approve'},
 'TC-313': {'id': 'TC-313',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS wizard refuses negative income bands and checks To against From',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.',
            'test_data': 'GHI From -1; PCI From -5; GHI From 500 with To 100.',
            'steps': '1. Open step Eligibility with a valid step General and tick Singapore Citizen, GHI and PCI.\n'
                     '2. Enter GHI From -1 and click Next.\n'
                     '3. Enter PCI From -5 and click Next.\n'
                     '4. Enter GHI From 500 and To 100 and click Next.',
            'expected': '2. and 3. A message that a number of 0 or more is needed.\n'
                        '4. A message that To must not be less than From.',
            'review': 'Approve'},
 'TC-314': {'id': 'TC-314',
            'scenario_id': 'TS-060',
            'title': 'MOEFAS wizard shows why a duplicate scheme name is refused',
            'suite': 'F4.14 New scheme wizard',
            'page': 'New scheme wizard (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'Localhost build (branch codesprint2ending), admin portal http://localhost:5173\n'
                   'Chrome (latest), locale en-US\n'
                   'Needs: none',
            'preconditions': '1. The localhost stack is running.\n'
                             '2. Signed in as MOE HQ user moehq.\n'
                             '3. At least one active fee component of Function 3 exists.\n'
                             '4. A MOEFAS scheme named R4-AUTO-ui-moe exists.',
            'test_data': 'Name R4-AUTO-ui-moe used twice.',
            'steps': '1. Complete the four steps of a new scheme with the name of the existing scheme.\n'
                     '2. Click Draft.',
            'expected': '1. The scheme is not created and the message says that the name already exists.',
            'review': 'Approve'},
 'TC-315': {'id': 'TC-315',
            'scenario_id': 'TS-062',
            'title': 'Search with only spaces behaves like an empty search',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ.',
            'test_data': 'Search text: five spaces.',
            'steps': '1. Open FAS applications.\n2. Type five spaces in the search box.\n3. Press Enter.',
            'expected': '1. No filter is applied and the full list stays.\n2. The box shows the spaces removed.',
            'review': 'Approve'},
 'TC-316': {'id': 'TC-316',
            'scenario_id': 'TS-062',
            'title': 'Search removes tab, line break and control characters',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ.',
            'test_data': 'Text with a tab, a line break and a null byte between two words.',
            'steps': '1. Paste the text into the search box.\n2. Press Enter.',
            'expected': '1. Tab and line break become one space.\n'
                        '2. Control characters and the null byte are removed and never reach the database.',
            'review': 'Approve'},
 'TC-317': {'id': 'TC-317',
            'scenario_id': 'TS-062',
            'title': 'Search treats SQL, script, JSON and template text as plain text',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ.',
            'test_data': '\' OR 1=1 --, <script>alert(1)</script>, {"a":1}, ${jndi:ldap://x}, %27, % and _.',
            'steps': '1. Search each text in turn.',
            'expected': '1. Each search returns "No applications found." with no error and no script is run.\n'
                        '2. % and _ are not wildcards and %27 is not decoded.',
            'review': 'Approve'},
 'TC-318': {'id': 'TC-318',
            'scenario_id': 'TS-062',
            'title': 'Search accepts emoji and letters of any script',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S4 (lowest)',
            'priority': 'Low',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ.',
            'test_data': 'Text: a smiley emoji and Vietnamese letters.',
            'steps': '1. Type the text in the search box and press Enter.',
            'expected': '1. The text is accepted and the list shows "No applications found." when nothing matches.',
            'review': 'Approve'},
 'TC-319': {'id': 'TC-319',
            'scenario_id': 'TS-062',
            'title': 'Search runs on Enter and 300 ms after the last key',
            'suite': 'F4.5 Filters and search',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ.',
            'test_data': 'Text: aisha.',
            'steps': '1. Type aisha and press Enter.\n2. Clear the box, type aisha and wait without pressing Enter.',
            'expected': '1. The list is filtered at once on Enter.\n'
                        '2. Without Enter the list is filtered about 300 ms after the last key and goes back to page '
                        '1.',
            'review': 'Approve'},
 'TC-320': {'id': 'TC-320',
            'scenario_id': 'TS-063',
            'title': 'Approve comment counter counts line breaks and emoji as one and keeps a pasted text over 500',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': 'Comment of 600 characters with a line break and an emoji.',
            'steps': '1. Open Approve on a Pending application.\n'
                     '2. Type a line break and an emoji and read the counter.\n'
                     '3. Paste 600 characters.',
            'expected': '1. The counter counts each line break and each emoji as 1.\n'
                        '2. The pasted text is kept, the counter shows 600/500 in red and Confirm approval is '
                        'disabled.',
            'review': 'Approve'},
 'TC-321': {'id': 'TC-321',
            'scenario_id': 'TS-063',
            'title': 'Approve comment trims spaces and saves a spaces-only comment as empty',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': "Comments: '  ok  ' and five spaces.",
            'steps': "1. Approve with the comment '  ok  ' and open the Decision block.\n"
                     '2. Approve another application with five spaces.',
            'expected': "1. The saved comment is 'ok'.\n"
                        '2. The spaces-only comment is saved as empty and the Decision block shows no comment.',
            'review': 'Approve'},
 'TC-322': {'id': 'TC-322',
            'scenario_id': 'TS-063',
            'title': 'Approve comment removes control characters and the null byte',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': 'Comment with U+0001, a tab, a line break and a null byte.',
            'steps': '1. Paste the comment and confirm the approval.\n'
                     '2. Read the saved comment through the drawer and the API.',
            'expected': '1. Line break and tab are kept.\n'
                        '2. Other control characters and the null byte are removed before save.',
            'review': 'Approve'},
 'TC-323': {'id': 'TC-323',
            'scenario_id': 'TS-063',
            'title': 'Approve comment keeps SQL, script, JSON and template text as plain text',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': "Comments: ' OR 1=1 --, <b>text</b>, {{7*7}}, ${7*7}.",
            'steps': '1. Approve with each text.\n2. Read the drawer, the History and the CSV export.',
            'expected': '1. The text is saved as typed and shown as plain text, encoded in the drawer, History, CSV '
                        'and parent email.\n'
                        '2. No data other than the decision changes.',
            'review': 'Approve'},
 'TC-324': {'id': 'TC-324',
            'scenario_id': 'TS-063',
            'title': 'A failed save keeps the approval dialog open with the comment',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.\n'
                             '3. The save request can be made to fail (ENV-R4-03).',
            'test_data': 'Comment: Approved after review.',
            'steps': '1. Open Approve, type the comment and make the save fail.\n2. Click Confirm approval.',
            'expected': '1. The message "Something went wrong. Please try again." is shown.\n'
                        '2. The dialog stays open with the comment and the application stays Pending.',
            'review': 'Approve'},
 'TC-325': {'id': 'TC-325',
            'scenario_id': 'TS-064',
            'title': 'Reject comment made of spaces is invalid',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject application dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': 'Reason: Income above limit. Comment: five spaces.',
            'steps': '1. Open Reject, choose the reason and type five spaces.\n2. Read the field and the button.',
            'expected': '1. "Comment is required." is shown.\n2. Reject application stays disabled.',
            'review': 'Approve'},
 'TC-326': {'id': 'TC-326',
            'scenario_id': 'TS-064',
            'title': 'Reject comment counter, paste over 500 and control characters',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject application dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': 'Comment of 600 characters; comment with a null byte and U+0001.',
            'steps': '1. Paste 600 characters and read the counter.\n'
                     '2. Paste the comment with control characters and reject.',
            'expected': '1. The text is kept, the counter shows 600/500 in red and the button is disabled.\n'
                        '2. Control characters and the null byte are removed before save.',
            'review': 'Approve'},
 'TC-327': {'id': 'TC-327',
            'scenario_id': 'TS-064',
            'title': 'A reject comment that starts with = is exported as text',
            'suite': 'F4.10 Reject SBFAS',
            'page': 'Reject application dialog',
            'severity': 'S2',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.\n'
                             '3. A rejected application has the comment =HYPERLINK("x").',
            'test_data': 'Comment: =HYPERLINK("x").',
            'steps': '1. Reject with the comment.\n2. Export the list and open the file.',
            'expected': '1. The cell value starts with an apostrophe and is shown as text, no formula runs.',
            'review': 'Approve'},
 'TC-328': {'id': 'TC-328',
            'scenario_id': 'TS-065',
            'title': 'Not enough MOEFAS budget disables Confirm approval',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve MOEFAS dialog',
            'severity': 'S1 (highest)',
            'priority': 'High',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as MOE HQ.\n'
                             '3. A MOEFAS scheme whose remaining budget is below the subsidy.',
            'test_data': 'Remaining budget S$ 100, subsidy needed S$ 250.',
            'steps': '1. Open Approve MOEFAS on the application.\n2. Read the budget note and the button.',
            'expected': '1. "Not enough MOEFAS budget. This approval needs S$ 250.00 but only S$ 100.00 is left." is '
                        'shown.\n'
                        '2. Confirm approval is disabled and nothing is saved.',
            'review': 'Approve'},
 'TC-329': {'id': 'TC-329',
            'scenario_id': 'TS-065',
            'title': 'Approve dialog says when the student has no open fee',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.\n'
                             '3. The student has no open fee.',
            'test_data': 'Student without open fee.',
            'steps': '1. Open Approve for the student.\n2. Read the list of fees.',
            'expected': '1. "No open fees right now. Fees issued later are subsidised automatically." is shown in the '
                        'fee list.',
            'review': 'Approve'},
 'TC-330': {'id': 'TC-330',
            'scenario_id': 'TS-065',
            'title': 'Confirm approval and Reject stay disabled with a message until the input is complete',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'Approve SBFAS dialog',
            'severity': 'S2',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as a School Admin with a Pending SBFAS application.',
            'test_data': 'No tier chosen; no reason chosen.',
            'steps': '1. Open Approve and clear the tier, read the message.\n'
                     '2. Open Reject without a reason, read the message.',
            'expected': '1. "Select a tier to approve." and Confirm approval is disabled.\n'
                        '2. "Select a reason to reject." and Reject application is disabled.',
            'review': 'Approve'},
 'TC-331': {'id': 'TC-331',
            'scenario_id': 'TS-065',
            'title': 'A failed export or save shows the standard error message',
            'suite': 'F4.9 Approve SBFAS',
            'page': 'FAS applications list (MOE HQ)',
            'severity': 'S3',
            'priority': 'Medium',
            'env': 'F4 build with API (FAS applications screens not available yet)\n'
                   'Chrome (latest)\n'
                   'Build: to be recorded at execution\n'
                   'Needs: ENV-R4-02',
            'preconditions': '1. The F4 build is running with the FAS applications screens.\n'
                             '2. Signed in as MOE HQ.\n'
                             '3. The export or save request can be made to fail (ENV-R4-03).',
            'test_data': 'Export and Reject save failing.',
            'steps': '1. Click Export while the export request fails.\n'
                     '2. Click Reject application while the save fails.',
            'expected': '1. and 2. "Something went wrong. Please try again." is shown, nothing is saved and the dialog '
                        'stays open.',
            'review': 'Approve'}}
