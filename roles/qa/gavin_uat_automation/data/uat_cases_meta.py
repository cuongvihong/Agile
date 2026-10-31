"""The 35 UAT cases of Gavin, copied from the Tests sheet of uat-master_1 (1).xlsx (Oct 29 version).
Title, setup and data, steps, expected results and gate are the words of the master. Do not edit by hand: change the master and regenerate.
"""
from __future__ import annotations

UAT_CASES: dict[str, dict] = {'UAT-MOE-01': {'title': 'Prepare EA, school, student and publish fees',
                'area': 'Fee and Payment',
                'role': 'MOE HQ',
                'owner': 'Gavin',
                'setup': '1. Government API mock has a Singapore citizen who has just turned 7\n'
                         '2. MOE HQ User account exists\n'
                         '3. Fee Type, Fee Component and Rate are configured\n'
                         'Data:\n'
                         'Student: student.test01, NRIC S0000001A\n'
                         'School: School Test 01\n'
                         'Class: P1A\n'
                         'Fee: Tuition fee 100.00 SGD',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['Run the daily sync job',
                          'Log in to the Admin Portal as MOE HQ User, create a School and a School User',
                          'Log in as the School User, create the class, enter the student and assign the student to the class',
                          'Log in as MOE HQ User, create a Fee Publication for that school and publish it',
                          "Open the student's Student Charge"],
                'expected': ['An Active EA is created for the student with balance 0.00',
                             'The student is linked to the EA after class assignment',
                             'Student Charge is POSTED and visible to the parent'],
                'severity1': True},
 'UAT-MOE-04': {'title': 'Set the MOEFAS budget',
                'area': 'FAS',
                'role': 'MOE HQ',
                'owner': 'Gavin',
                'setup': '1. MOE HQ User is logged in and may manage the MOEFAS budget\nData:\nBudget Amount: 1000000.00',
                'gate': 'Budget period and editing rules await client decision, items G1 and G2',
                'steps': ['Open the MOEFAS Manage Budget screen',
                          'Enter the Budget Amount',
                          'Click Save',
                          'Reopen the budget view'],
                'expected': ['The budget is saved', 'The view shows the saved Budget Amount within MOEFAS scope'],
                'severity1': False},
 'UAT-MOE-05': {'title': 'Track MOEFAS statistics and budget usage',
                'area': 'FAS',
                'role': 'MOE HQ',
                'owner': 'Gavin',
                'setup': '1. MOEFAS budget is set\n'
                         '2. Some MOEFAS subsidies are already granted\n'
                         'Data:\n'
                         'Budget Amount: 1000000.00',
                'gate': 'Subsidy calculation and the Remaining formula await decision, items G4, G6 and G8',
                'steps': ['Open the MOEFAS Subsidy Statistics page',
                          'Check Total Subsidy Amount Granted',
                          'Open the Budget Tracking page'],
                'expected': ['Total granted subsidy is correct for MOEFAS scope',
                             'The tracking page shows Budget Amount and Subsidy Amount Used',
                             'Remaining Budget equals Budget Amount minus Subsidy Amount Used, if the feature is confirmed'],
                'severity1': False},
 'UAT-MOE-05-E1': {'title': 'Budget is exhausted but grants continue',
                   'area': 'FAS',
                   'role': 'MOE HQ',
                   'owner': 'Gavin',
                   'setup': '1. Subsidy Amount Used equals or exceeds the MOEFAS Budget Amount\n'
                            'Data:\n'
                            'Budget Amount: 1000.00\n'
                            'Subsidy Amount Used: 1000.00',
                   'gate': 'Shares data and environment with UAT-MOE-05. Severity 1: must Pass before go live',
                   'steps': ['Open the Budget Tracking page', 'Let the system grant one more MOEFAS subsidy'],
                   'expected': ['The page shows a budget exhausted warning',
                                'The extra grant still goes through and is not blocked'],
                   'severity1': True},
 'UAT-MOE-06': {'title': 'Create a MOEFAS scheme and view FAS applications',
                'area': 'FAS',
                'role': 'MOE HQ',
                'owner': 'Gavin',
                'setup': '1. MOE HQ User is logged in\n'
                         '2. At least one Fee Component is Active\n'
                         'Data:\n'
                         'Name: MOEFAS 2028\n'
                         'Form: 1 Aug 2028 to 31 Dec 2028\n'
                         'Effective from: 1 Jan 2029\n'
                         'Nationality: Singapore Citizen\n'
                         'Subsidy: Primary 100%, Secondary 70%, Pre-University 50%',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['Open MOEFAS schemes and create a new scheme',
                          'General step: enter name, Form opens, Form closes, Effective from',
                          'Eligibility step: choose nationality and GHI, PCI bands',
                          'Subsidy step: enter the rate for each level',
                          'Review and Publish',
                          'Open FAS applications'],
                'expected': ['The scheme is published and becomes read only',
                             'The scheme list shows the form status label and Approved automatically',
                             'FAS applications lists applications from all schools, with no Approve or Reject button'],
                'severity1': True},
 'UAT-MOE-06-N1': {'title': 'Invalid scheme',
                   'area': 'FAS',
                   'role': 'MOE HQ',
                   'owner': 'Gavin',
                   'setup': '1. MOE HQ User is logged in\nData:\nForm closes: 31 Dec 2028\nEffective from: 31 Dec 2028',
                   'gate': 'Shares data and environment with UAT-MOE-06',
                   'steps': ['Create a new scheme and enter the Form closes date as Effective from',
                             'Go to the Review step and click Publish'],
                   'expected': ['The system shows Effective from must be after Form closes', 'The scheme is not published'],
                   'severity1': False},
 'UAT-SCH-01': {'title': "Enter a parent's paper application",
                'area': 'FAS',
                'role': 'School Admin',
                'owner': 'Gavin',
                'setup': '1. School User is logged in\n'
                         '2. The MOEFAS form is open\n'
                         '3. A Singapore Citizen parent has a 10 year old child at the school with no application this year\n'
                         '4. A PDF scan under 10 MB is available\n'
                         'Data:\n'
                         'File: paper-form-test01.pdf\n'
                         'Applicant NRIC: S0000100A\n'
                         'Child NRIC: S0000001A\n'
                         'Relationship: Mother\n'
                         'Context: Household income reduced',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['Open Upload applications, click Upload scans, add the file, click Upload and read',
                          "Enter the applicant's NRIC and the child's NRIC",
                          'Choose the relationship, declare other members, enter context, tick the declaration',
                          'Click Review and submit',
                          'Check the Review before submitting screen, then click Confirm and submit',
                          'Open the Upload applications list'],
                'expected': ['Applicant and child details are prefilled and locked',
                             'Income comes from Government data and GHI and PCI are shown',
                             'The message Application submitted for assessment appears',
                             'Each child has one application with source Paper and status Pending, and the draft is removed'],
                'severity1': True},
 'UAT-SCH-01-N1': {'title': 'Blocked when submitting a paper application',
                   'area': 'FAS',
                   'role': 'School Admin',
                   'owner': 'Gavin',
                   'setup': '1. School User is logged in\n'
                            '2. A paper application is open on the Review application screen\n'
                            'Data:\n'
                            'Child aged 17: S0000200C\n'
                            'Child with an application: S0000001A',
                   'gate': 'Shares data and environment with UAT-SCH-01. Severity 1: must Pass before go live',
                   'steps': ['Leave Phone number empty and click Review and submit',
                             'Enter a child outside the 7 to 16 age range and click Review and submit',
                             'Enter a child who already has an application this year and click Review and submit',
                             'Enter the same NRIC for applicant and child and click Review and submit'],
                   'expected': ['Each time a red note at the top of the page states what to fix', 'No application is created'],
                   'severity1': True},
 'UAT-SCH-01-E1': {'title': 'Save a draft when entry is incomplete',
                   'area': 'FAS',
                   'role': 'School Admin',
                   'owner': 'Gavin',
                   'setup': '1. School User is logged in\n'
                            '2. A paper application is open on the Review application screen and partly entered\n'
                            'Data:\n'
                            'Applicant NRIC: S0000100A',
                   'gate': 'Shares data and environment with UAT-SCH-01',
                   'steps': ['Click Save draft', 'Return to the Upload applications list', 'Click Continue on the Draft row'],
                   'expected': ['The list shows a Draft row with Application ID Not submitted',
                                'Continue reopens the data that was entered'],
                   'severity1': False},
 'UAT-SCH-02': {'title': 'Create an SBFAS scheme and add a fee',
                'area': 'FAS',
                'role': 'School Admin',
                'owner': 'Gavin',
                'setup': '1. School Admin is logged in\n'
                         '2. An Active Fee Component exists that is not yet in the scheme\n'
                         'Data:\n'
                         'Name: Tier 1\n'
                         'Nationality: Singapore Citizen\n'
                         'Subsidy: P1 100%, P2 80%, P3 60%\n'
                         'New fee component: Activity fee',
                'gate': 'UAT environment is ready and the data above is created',
                'steps': ['Open SBFAS schemes and create a new scheme named Tier 1',
                          'Enter the form period and the effective period',
                          'Choose nationality and GHI, PCI bands',
                          'Enter the subsidy rate for each level',
                          'Review and Publish',
                          'When the scheme is Active, click Add fee, choose the new component, enter a value, click Add to '
                          'scheme'],
                'expected': ['Tier 1 is published and becomes read only',
                             'Add fee is available only on Active or Upcoming schemes',
                             'The new column is added and the old columns are read only',
                             'The subsidy applies to open fees of students already granted the scheme'],
                'severity1': False},
 'UAT-SCH-02-N1': {'title': 'Invalid SBFAS scheme',
                   'area': 'FAS',
                   'role': 'School Admin',
                   'owner': 'Gavin',
                   'setup': "1. The school's Tier 1 scheme is published\n"
                            'Data:\n'
                            'Name, first attempt: Tier 1\n'
                            'Name, second attempt: Tier 2',
                   'gate': 'Shares data and environment with UAT-SCH-02',
                   'steps': ['Create another scheme also named Tier 1 with an application period overlapping the old Tier 1',
                             'Click Publish',
                             'Rename it to Tier 2 and Publish again'],
                   'expected': ['The first attempt reports an overlap with an existing scheme and cannot be published',
                                'The second attempt with a different name can be published'],
                   'severity1': False},
 'UAT-SCH-03': {'title': 'Approve an SBFAS application',
                'area': 'FAS',
                'role': 'School Admin',
                'owner': 'Gavin',
                'setup': '1. School Admin is logged in\n'
                         '2. A Pending SBFAS application exists for a student of the school\n'
                         '3. SBFAS scheme Tier 1 is published\n'
                         'Data:\n'
                         'Tier: Tier 1\n'
                         'Comment: Eligible',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['Open FAS applications, Pending tab',
                          'Click Review on the application',
                          'Check income, context and the ML recommendation in the drawer',
                          'Choose a tier, enter a Comment, click Confirm approval'],
                'expected': ["The tier list shows the school's SBFAS schemes and the ML recommended tier is preselected",
                             'The application becomes Approved with the tier and the scheme Effective from',
                             "The message Subsidy applied to the student's EA fees appears",
                             'The parent receives an email and the application becomes read only'],
                'severity1': True},
 'UAT-SCH-03-N1': {'title': 'Reject an SBFAS application',
                   'area': 'FAS',
                   'role': 'School Admin',
                   'owner': 'Gavin',
                   'setup': '1. School Admin is logged in\n'
                            '2. A Pending SBFAS application exists for a student of the school\n'
                            'Data:\n'
                            'Reason: Income above limit\n'
                            'Comment: Income above the Tier 1 limit',
                   'gate': 'Shares data and environment with UAT-SCH-03. Severity 1: must Pass before go live',
                   'steps': ['Open the application in FAS applications',
                             'Click Reject',
                             'Choose a Reason and enter a Comment',
                             'Click Reject application'],
                   'expected': ['The Reject application button stays disabled until both Reason and Comment are filled',
                                'The application becomes Rejected and shows Application rejected. Parent notified by email',
                                'The parent receives an email with the reason'],
                   'severity1': True},
 'UAT-SCH-04': {'title': 'Set and track the SBFAS budget',
                'area': 'FAS',
                'role': 'School Admin',
                'owner': 'Gavin',
                'setup': '1. School User is logged in and may manage the SBFAS budget\n'
                         '2. The school already has granted SBFAS subsidies\n'
                         'Data:\n'
                         'Budget Amount: 50000.00',
                'gate': 'The Remaining formula awaits decision, item G8',
                'steps': ['Open the SBFAS Manage Budget screen',
                          'Enter the Budget Amount and click Save',
                          'Open the Budget Tracking page'],
                'expected': ["The budget is saved and tied to the user's school",
                             "The tracking page shows the school's Budget Amount, Subsidy Amount Used and Remaining Budget",
                             'No data from another school appears'],
                'severity1': False},
 'UAT-SCH-04-E1': {'title': 'SBFAS budget is exhausted but grants continue',
                   'area': 'FAS',
                   'role': 'School Admin',
                   'owner': 'Gavin',
                   'setup': "1. The school's Subsidy Amount Used equals or exceeds the SBFAS Budget Amount\n"
                            'Data:\n'
                            'Budget Amount: 1000.00\n'
                            'Subsidy Amount Used: 1000.00',
                   'gate': 'Shares data and environment with UAT-SCH-04. Severity 1: must Pass before go live',
                   'steps': ['Open the Budget Tracking page', 'Approve one more SBFAS application'],
                   'expected': ['The page shows a budget exhausted warning',
                                'The application is still approved and the grant is not blocked'],
                   'severity1': True},
 'UAT-PAR-01': {'title': 'Log in, view the EA and pay fees with the EA',
                'area': 'Fee and Payment',
                'role': 'Parent',
                'owner': 'Gavin',
                'setup': '1. Parent has a SingPass mock account and a child under 16 linked to an EA\n'
                         '2. The Active EA has balance 100.00\n'
                         '3. The child has one Issued invoice of 50.00\n'
                         'Data:\n'
                         'Parent: parent.test01, NRIC S0000100A\n'
                         'Child: student.test01, EA code EA-001\n'
                         'Invoice: 50.00',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['Open e-Service and click Log in with SingPass',
                          'On Home choose the child Edu Account card',
                          'On Edu Account Detail choose Pay fees',
                          'Choose the invoice',
                          'Choose to pay with the EA and confirm',
                          'Open the receipt'],
                'expected': ['Home shows a card with the child name, EA code and balance',
                             'The fee list belongs to the selected child, with no need to choose the student again',
                             'The EA is debited 50.00 exactly once, leaving 50.00',
                             'The invoice becomes Paid and the receipt shows invoice code, total, method and amount per source',
                             'The receipt has a way back to the correct child'],
                'severity1': True},
 'UAT-PAR-01-N1': {'title': 'SingPass error or the parent cancels',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. The SingPass mock can return an error or allow cancel\nData:\nScenario: Parent clicks Cancel',
                   'gate': 'Shares data and environment with UAT-PAR-01',
                   'steps': ['Open e-Service and click Log in with SingPass',
                             'Cancel at SingPass or let SingPass return an error'],
                   'expected': ['The system shows MSG-0802', 'The user returns to the login page and cannot enter Home'],
                   'severity1': False},
 'UAT-PAR-01-N2': {'title': 'Parent not found or API slow',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. The Government API mock has no record of this parent, or the parent has no child, or the API '
                            'responds slower than 10 seconds\n'
                            'Data:\n'
                            'Parent: parent.test99, NRIC S0000999Z',
                   'gate': 'Shares data and environment with UAT-PAR-01',
                   'steps': ['Open e-Service and click Log in with SingPass', 'Authenticate successfully at SingPass'],
                   'expected': ['The system shows MSG-0801 or MSG-0809', 'The parent cannot enter Home'],
                   'severity1': False},
 'UAT-PAR-01-E1': {'title': 'Child has just turned 16',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\n'
                            '2. The child has just turned 16 and the EA is Due for closure\n'
                            'Data:\n'
                            'Child: student.test16, EA code EA-016',
                   'gate': 'Shares data and environment with UAT-PAR-01',
                   'steps': ['On Home choose the child card',
                             'View the EA, fees and history',
                             'Try to pay fees and try to submit an FAS application'],
                   'expected': ['EA, fees and history can be viewed',
                                'Payment is not possible and FAS submission is not possible'],
                   'severity1': False},
 'UAT-PAR-01-N3': {'title': 'Balance too low for the EA only option',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\n'
                            '2. EA balance is 20.00\n'
                            '3. The child has an Issued invoice of 50.00\n'
                            'Data:\n'
                            'Balance: 20.00\n'
                            'Invoice: 50.00',
                   'gate': 'Shares data and environment with UAT-PAR-01. Severity 1: must Pass before go live',
                   'steps': ["Go to the child's fees and choose the invoice", 'Open the payment method step'],
                   'expected': ['The EA only option is disabled and shows the reason',
                                'The system suggests Online or Both',
                                'No data changes'],
                   'severity1': True},
 'UAT-PAR-01-A1': {'title': 'Split between EA and online',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\n'
                            '2. EA balance is 20.00\n'
                            '3. The child has an Issued invoice of 50.00\n'
                            '4. The Online sandbox gateway is set to succeed\n'
                            'Data:\n'
                            'EA part: 20.00\n'
                            'Online part: 30.00',
                   'gate': 'Shares data and environment with UAT-PAR-01. Severity 1: must Pass before go live',
                   'steps': ["Go to the child's fees and choose the invoice",
                             'Choose Both and confirm',
                             'Complete payment on the Online gateway',
                             'Open the receipt'],
                   'expected': ['The EA part equals the whole balance and the Online part is the remainder',
                                'The EA is debited first, then the Online gateway opens',
                                'The invoice is Paid and the receipt lists both sources, total 50.00',
                                'The EA balance is 0.00'],
                   'severity1': True},
 'UAT-PAR-01-N4': {'title': 'Online part fails',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. As UAT-PAR-01-A1\n'
                            '2. The Online sandbox gateway is set to fail or cancel\n'
                            'Data:\n'
                            'EA part: 20.00\n'
                            'Online part: 30.00',
                   'gate': 'The new UX assumes 100% completion, decide whether to keep this branch. Severity 1: must Pass before '
                           'go live',
                   'steps': ['Choose Both and confirm',
                             'At the Online gateway choose failure or cancel',
                             'Return to e-Service and open the invoice'],
                   'expected': ['The EA part of 20.00 is refunded',
                                'The invoice returns to Issued and can be retried',
                                'The EA balance returns to 20.00'],
                   'severity1': True},
 'UAT-PAR-01-E2': {'title': 'EA refund fails',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. As UAT-PAR-01-N4\n'
                            '2. The tech team simulates a failed EA refund command\n'
                            'Data:\n'
                            'EA part: 20.00\n'
                            'Online part: 30.00',
                   'gate': 'Needs the tech team to simulate it. The new UX assumes 100% completion. Severity 1: must Pass before '
                           'go live',
                   'steps': ['Choose Both and confirm',
                             'At the Online gateway choose failure',
                             'Open the invoice after the refund command fails'],
                   'expected': ['The transaction moves to ReconciliationRequired and the invoice stays PaymentPending',
                                'The parent sees a verifying status',
                                'An alert is raised for operations'],
                   'severity1': True},
 'UAT-PAR-02': {'title': 'Submit an online FAS application, MOEFAS auto approves after the form closes',
                'area': 'FAS',
                'role': 'Parent',
                'owner': 'Gavin',
                'setup': '1. A Singapore Citizen parent is logged in, the child is 10 and has no application\n'
                         '2. The MOEFAS form is open and the scheme takes effect after the form close date\n'
                         '3. Household income from the Government API is within the scheme limit\n'
                         'Data:\n'
                         'Relationship: Mother\n'
                         'Context: Household income reduced\n'
                         'Form closes: 31 Dec 2028',
                'gate': 'UAT environment is ready and the data above is created. Severity 1: must Pass before go live',
                'steps': ['On Home go to Financial assistance and click Apply for FAS',
                          'Step 1: choose the relationship and the child, click Continue',
                          'Step 2: check members and income, click Continue',
                          'Step 3: skip documents, keep the tick to also consider SBFAS, click Continue',
                          'Step 4: enter context, click Continue',
                          'Step 5: review, tick the declaration, click Submit application',
                          'Open My applications, then open it again after the MOEFAS form closes'],
                'expected': ['Parent details are prefilled and read only',
                             'Income comes from Government data and GHI, household size and PCI are shown',
                             'The message Application submitted for assessment appears',
                             'The application is Under review with System check Waiting and the form close date',
                             'After the form closes the application is Approved MOEFAS from the scheme Effective from',
                             'The parent receives the result email'],
                'severity1': True},
 'UAT-PAR-02-N1': {'title': 'Child is locked at selection',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\n'
                            '2. One child is 16 and another child already has an application under review\n'
                            'Data:\n'
                            'Child aged 16: student.test16\n'
                            'Child with an application: student.test03',
                   'gate': 'Shares data and environment with UAT-PAR-02',
                   'steps': ['Go to Financial assistance and click Apply for FAS', 'View the children list at step 1'],
                   'expected': ['Each child is locked with the matching reason',
                                'Continue stays disabled while no child can be selected'],
                   'severity1': False},
 'UAT-PAR-02-N2': {'title': 'No FAS form is open',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\n'
                            '2. No MOEFAS or SBFAS form is open\n'
                            'Data:\n'
                            "Today's date is outside every form period",
                   'gate': 'Shares data and environment with UAT-PAR-02',
                   'steps': ['Open Financial assistance', 'Click Apply for FAS if it is still enabled'],
                   'expected': ['Apply for FAS is disabled with a note',
                                'Children are locked with application form is closed and the next form date if there is one'],
                   'severity1': False},
 'UAT-PAR-02-E1': {'title': 'Save a draft and return later',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in with no draft\nData:\nContext: Household income reduced',
                   'gate': 'Shares data and environment with UAT-PAR-02',
                   'steps': ['Go to step 4 and enter context',
                             'Click Save draft and exit',
                             'Open Financial assistance again',
                             'Click Resume draft'],
                   'expected': ['The message Draft saved. You can continue later. appears',
                                'The Draft card shows status Draft and the saved step',
                                'Resume opens step 4 with the context kept'],
                   'severity1': False},
 'UAT-PAR-02-E2': {'title': 'Submit for two children',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent has two eligible children and the MOEFAS form is open\n'
                            'Data:\n'
                            'Child 1: student.test01\n'
                            'Child 2: student.test04',
                   'gate': 'Shares data and environment with UAT-PAR-02',
                   'steps': ['Choose both children at step 1',
                             'Go through every step and click Submit application',
                             'Open My applications'],
                   'expected': ['The message Applications submitted appears',
                                'The two applications have separate Application IDs and share one family code in the format '
                                'FAM-YYYY-NNNNN'],
                   'severity1': False},
 'UAT-PAR-02-A1': {'title': 'Fails MOEFAS and moves to school SBFAS',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Household income is above the MOEFAS limit\n'
                            '2. The tick to also consider SBFAS is still ticked\n'
                            "3. The school's SBFAS scheme Tier 1 is published\n"
                            'Data:\n'
                            'Household income: 8000 per month\n'
                            'Tier: Tier 1',
                   'gate': 'Shares data and environment with UAT-PAR-02. Severity 1: must Pass before go live',
                   'steps': ['Submit the application as in UAT-PAR-02',
                             'After the MOEFAS form closes, open My applications',
                             'School Admin approves the Pending SBFAS application',
                             'Parent opens My applications again'],
                   'expected': ['The application becomes SBFAS Pending with the school and the timeline shows Sent to school',
                                'After approval it shows Approved SBFAS Tier 1 from Effective from',
                                'The parent receives an email'],
                   'severity1': True},
 'UAT-PAR-02-N3': {'title': 'Fails MOEFAS and SBFAS is not considered',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Household income is above the MOEFAS limit\n'
                            '2. The tick to also consider SBFAS is cleared\n'
                            'Data:\n'
                            'Household income: 8000 per month',
                   'gate': 'Shares data and environment with UAT-PAR-02. Severity 1: must Pass before go live',
                   'steps': ['Submit the application and clear the SBFAS tick at step 3',
                             'After the MOEFAS form closes, open My applications'],
                   'expected': ['The application becomes Rejected with reason Not eligible for MOEFAS',
                                'The parent receives an email'],
                   'severity1': True},
 'UAT-PAR-02-A2': {'title': 'PR or International student applies',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. The child is a Singapore PR\n'
                            "2. The school's SBFAS form is open\n"
                            'Data:\n'
                            'Child: student.pr01, Singapore PR',
                   'gate': 'Shares data and environment with UAT-PAR-02. Severity 1: must Pass before go live',
                   'steps': ['Submit the application for the child',
                             'Open My applications',
                             'School Admin approves the application'],
                   'expected': ['The application is SBFAS Pending as soon as it is submitted and the timeline shows Sent to '
                                'school (SBFAS)',
                                'The school approves the application and chooses the tier'],
                   'severity1': True},
 'UAT-PAR-02-N4': {'title': 'School rejects SBFAS',
                   'area': 'FAS',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. A Pending SBFAS application of a PR child at the school\nData:\nReason: Not eligible nationality',
                   'gate': 'Shares data and environment with UAT-PAR-02. Severity 1: must Pass before go live',
                   'steps': ['School Admin chooses Reject with a Reason and a Comment', 'Parent opens My applications'],
                   'expected': ['The application is Rejected and the timeline shows the reason and the comment',
                                'The parent receives an email'],
                   'severity1': True},
 'UAT-PAR-03': {'title': "View one child's EA activity",
                'area': 'Fee and Payment',
                'role': 'Parent',
                'owner': 'Gavin',
                'setup': '1. Parent has two children, and each EA already has top-up and payment transactions\n'
                         'Data:\n'
                         'Child: student.test01, EA code EA-001',
                'gate': 'UAT environment is ready and the data above is created',
                'steps': ['Log in with SingPass',
                          'On Home choose the card of one child',
                          'On Edu Account Detail choose to view EA balance activity'],
                'expected': ['The page shows the child name and EA code',
                             "The list has only this child's wallet entries, top-up shows as Money in and Description holds no "
                             'internal reason',
                             'Back returns to the correct Edu Account Detail of the child'],
                'severity1': False},
 'UAT-PAR-03-A1': {'title': "View the children's EA activity together",
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent has two children and each EA already has transactions\n'
                            'Data:\n'
                            'Child 1: student.test01\n'
                            'Child 2: student.test04',
                   'gate': 'Shares data and environment with UAT-PAR-03',
                   'steps': ['On Home click Recent EA activity of your children',
                             'Look at the rows',
                             'Choose the name of one child'],
                   'expected': ['Each row has the child name and EA code',
                                'A note states the scope is the loaded data',
                                "Choosing a child name opens that child's page"],
                   'severity1': False},
 'UAT-PAR-03-E1': {'title': 'Invoices and payments (future)',
                   'area': 'Fee and Payment',
                   'role': 'Parent',
                   'owner': 'Gavin',
                   'setup': '1. Parent is logged in\nData:\nNone',
                   'gate': 'Future branch, may be left out of this sprint UAT',
                   'steps': ['Look at the main menu on Home', 'Open Edu Account Detail and look at the options'],
                   'expected': ['The main menu has no separate Fees and Payments item',
                                'No Invoices and payments item shows until a list source exists'],
                   'severity1': False}}

# Master of 30 Oct 2026 (Sprint 3 UAT): replaces the steps of the PAR-01 family and adds UAT-031 and UAT-033.
from data.uat_master_v3 import OVERRIDES as _V3  # noqa: E402

UAT_CASES.update(_V3)
