# ---------- ONE shared test data sheet, field level ----------
SD = []
def add(did, grp, ent, where, field, value, used, note=""):
    SD.append((did, grp, ent, where, field, value, used, note))
def many(did, grp, ent, where, pairs, used, note=""):
    for i, (f, v) in enumerate(pairs):
        add(did, grp, ent, where, f, v, used if i == 0 else "", note if i == 0 else "")

SEEDED = "UAT-PRE-01, UAT-PRE-02, UAT-PRE-03 (seed)"
# 1. People and schools
for key, nm, nric, code, ea, par, sch, lvl, use in [
    ("C1", "Ethan Rahman", "S3678638G", "STU-004", "EDU-01004", "PA S8901234H", "Rosyth Primary School", "Primary 2, class 2A1", "UAT-PAR-01, UAT-031, UAT-031-E1"),
    ("C2", "Leo Rahman", "S5918715F", "STU-007", "EDU-01007", "PA S8901234H", "Rosyth Primary School", "Primary 1, class 1A1", "UAT-PAR-01-N3, UAT-PAR-01-E2"),
    ("C3", "Isaac Chen", "S3320821H", "STU-015", "EDU-01015", "PB S6789012F", "Read on the stack at the first run", "Read on the stack", "UAT-PAR-01-A1, UAT-033 control"),
    ("C4", "Sophia Chen", "S1192619B", "STU-017", "EDU-01017", "PB S6789012F", "Read on the stack at the first run", "Read on the stack", "UAT-PAR-01-A1 online only, UAT-033"),
    ("C5", "Grace Pham", "S6159230D", "STU-022", "EDU-01022", "PC S7654321B", "Read on the stack at the first run", "Read on the stack", "UAT-PAR-01-N4"),
]:
    many(key, "1 People", f"Child {nm}", "Existing student on the host (not created by QA)",
         [("Full name", nm), ("Student NRIC", nric), ("Student code", code), ("EA number", ea), ("Parent persona (Singpass)", par), ("School", sch), ("Class level", lvl), ("Student category", "SC (Singapore Citizen)"), ("Education stage", "PRIMARY")], use)
many("PA", "1 People", "Parent Ahmad Bin Rahman", "Singpass persona in the e-Service", [("Singpass NRIC", "S8901234H"), ("Full name", "Ahmad Bin Rahman"), ("Phone number", "91234567"), ("Email", "ahmad.rahman.s8901234h@example.com"), ("Relationship to the children", "FATHER"), ("Children", "C1 Ethan, C2 Leo")], "UAT-PAR-01, N3, E2, UAT-PRE-03", "Other applicant fields (date of birth, gender, nationality, address) come from the prefill and are read only. Record them at the first run.")
many("PB", "1 People", "Parent persona B", "Singpass persona in the e-Service", [("Singpass NRIC", "S6789012F"), ("Children", "C3 Isaac, C4 Sophia"), ("FAS status", "Both children already Approved, APP-01003 (cannot apply again)")], "UAT-PAR-01-A1, UAT-033")
many("PC", "1 People", "Parent persona C", "Singpass persona in the e-Service", [("Singpass NRIC", "S7654321B"), ("Children", "C5 Grace Pham"), ("FAS status", "No application")], "UAT-PAR-01-N4")
many("SCH-A", "1 People", "School A", "Existing school on the host", [("School name", "Rosyth Primary School"), ("School type", "Primary")], "All school scoped cases")
many("SCH-B", "1 People", "School B (created by MOE HQ)", "Admin, School management, Create school", [("MOE school code", "UATB01"), ("School name", "UAT Seed School B"), ("School type", "Primary"), ("School users", "Add after creating: SCH-B-USER"), ("Academic levels", "Primary 1, Primary 2"), ("Buttons", "Create school (Cancel to leave)")], "UAT-031, UAT-031-E1 wrong school controls", "A student with an EA at School B is created by the daily sync, which QA cannot start, so the cross school application stays Blocked until a child of another school is mapped.")
many("SCH-B-USER", "1 People", "School B user (created by MOE HQ)", "Admin, School Users, Create school user, tab Single", [("NRIC", "S9000042Z"), ("First name", "UAT"), ("Last name", "SchoolB"), ("Email", "uat.schoolb@example.com"), ("MOE school code (optional)", "UATB01"), ("Password", "Never recorded in this file. After creating, open the user detail to see how the user logs in.")], "UAT-031, UAT-031-E1")
many("HQ / SCH-A-USER", "1 People", "Logins", "Admin portal login (username and password)", [("MOE HQ user", "Environment variable HQ_USER (moehq)"), ("School A user", "Environment variable SCHOOL_USER (school)"), ("Passwords", "Never recorded in this file. Set in the PowerShell session or in DATA-ROLES of Chan.")], "All Admin cases")

# 2. Money: EA and top-up
for key, nm in [("C1", "Ethan"), ("C2", "Leo"), ("C3", "Isaac")]:
    many(f"TOPUP-{key}", "2 Money", f"Individual top-up of {nm}", "API POST /top-up/individual (Admin, Top-Up, Individual)",
         [("walletId", f"Wallet of EA {dict(C1='EDU-01004', C2='EDU-01007', C3='EDU-01015')[key]}, read at run time"), ("amount", "20.00"), ("referenceId", f"TUP-IND-UATSEED-{dict(C1='STU-004', C2='STU-007', C3='STU-015')[key]}-20.0-v1"), ("reason", "UAT-SEED test data for UAT cases"), ("fundingSource", "MOE General Funding")], "UAT-PRE-01", "Done once per child. The reference must contain TUP-IND- or Top-Up History does not list it.")
many("TOPUP-BULK", "2 Money", "Bulk top-up campaign (created, not run)", "API POST /top-up/campaigns (Admin, Top-Up, Campaigns)", [("name", "UAT-SEED Bulk 20 age 10"), ("description", "Seed for UAT top-up cases. Targets age 10 only (4 EAs)."), ("amountPerStudent", "20.00"), ("minAge", "10"), ("maxAge", "10 (the backend accepts ages 7 to 15)"), ("createdBy", "MOEHQ_User"), ("Run it", "Only with UAT_SEED_RUN_CAMPAIGN=1")], "UAT-PRE-01 and the top-up cases of Josh")
many("EA-TARGET", "2 Money", "EA balances", "Seed, restore step from round 2", [("Opening balance on the host", "500.00 (Ethan, Leo, Isaac, Grace, Sophia)"), ("Target before each payment run", "520.00 for Ethan, Leo, Isaac, Grace (top-up parts of at most 100.00, reference TUP-IND-UATSEED-STU-xxx-RESTORE-R{round}-{n})"), ("Sophia", "500.00 (no top-up, pays online)"), ("Why 520.00", "A payment that succeeds or is held for reconciliation uses the EA up, and there is no debit API")], "All payment cases")

# 3. Fees
for nm, price, studs, use in [
    ("Fee 100", "100.00", "Ethan, Leo", "EA only payment (UAT-PAR-01)"),
    ("Fee 600", "600.00", "Isaac, Grace, Leo", "Bigger than the EA: split (UAT-PAR-01-A1), failed online part (UAT-PAR-01-N4), EA only disabled (UAT-PAR-01-N3)"),
    ("Fee 50", "50.00", "Grace, Sophia", "Online only (UAT-PAR-01-A1 variant, UAT-PAR-01-N4 variant)"),
    ("Fee 700", "700.00", "Leo", "Split with failed online part and EA part held (UAT-PAR-01-E2)"),
]:
    full = f"UAT-SEED {nm} r{{round}}"
    many(f"FEE-{nm.split()[1]}", "3 Fees", f"Fee component {full}", "Admin, Fees, Fee components, Create (API POST /fee-components and /fee-rate-rules)",
         [("Fee type", "MISC (code)"), ("Name", full), ("School", "None (MOE level component)"), ("Tax applies", "No"), ("Student categories", "SC"), ("Education stages", "PRIMARY"), ("Rate rule: education stage", "PRIMARY"), ("Rate rule: student category", "SC"), ("Rate rule: price", f"{price} SGD"), ("Rate rule: effective from", "2026-01-01")], use, "{round} is the number in artifacts\\seed_round.txt. A new round only adds new fees.")
    many(f"BATCH-{nm.split()[1]}", "3 Fees", f"Publication batch of {full}", "Admin, Fees, Publications, Create draft then Publish (API POST /publication-batches)",
         [("Title", f"{full} 2026-11-01"), ("School scope", "COMPONENT_SCOPE"), ("Student scope", "SELECTED_TARGETS"), ("Selected students", studs), ("Period start", "2026-11-01"), ("Period end (exclusive)", "2026-12-01"), ("Due date", "2026-12-31"), ("Final step", "Publish, status Completed")], use)
add("FEE-REAL", "3 Fees", "Real Term 4 2026 fees on the host", "Parent Home, Outstanding charges", "Standard Miscellaneous / Stationery", "19.50 / 12.00 (read only, not created by QA)", "UAT-033 (MOEFAS 19.50 from 1 Dec 2026)")
many("FEE-S100", "3 Fees", "Fee of 100.00 for Sophia (TO SEED)", "Same steps as FEE-100", [("Name", "UAT-SEED Fee S100 r{round}"), ("Price", "100.00 SGD"), ("Students", "Sophia"), ("Expected on UAT-033", "Gross 100.00, Subsidy 40.00, Amount due 60.00")], "UAT-033", "Not in the seed yet. Until it exists UAT-033 stays Blocked.")

# 4. Payment case matrix
for cid, who, comp, how, exp in [
    ("UAT-PAR-01", "Ethan (PA)", "Fee 100", "EA only", "Success. EA 520.00 to 420.00. Receipt shown."),
    ("UAT-PAR-01-N3", "Leo (PA)", "Fee 600 plus a second charge of 10.00", "Read only", "EA only is disabled because the EA is less than the charge."),
    ("UAT-PAR-01-A1", "Isaac (PB)", "Fee 600", "Both: EA 520.00 plus online 80.00", "Success. EA 0.00."),
    ("UAT-PAR-01-A1 variant", "Sophia (PB)", "Fee 50", "Online only 50.00", "Success. EA unchanged 500.00."),
    ("UAT-PAR-01-N4", "Grace (PC)", "Fee 600", "Both, online part set to Failed on the simulator", "Payment needs review, EA 0.00 held, charge held. No automatic refund (client rule). Parent sees 'waiting for system to refund' (GAP on wording today)."),
    ("UAT-PAR-01-N4 variant", "Grace (PC)", "Fee 50", "Online only, Failed", "Payment failed, no amount deducted, EA unchanged."),
    ("UAT-PAR-01-E2", "Leo (PA)", "Fee 700", "Both: EA 520.00 plus online 180.00, online Failed", "Payment needs review, EA part 520.00 held. Manual reconciliation (operations)."),
]:
    many("PAY-" + cid.replace("UAT-PAR-01", "01").replace(" ", "-"), "4 Payment cases", f"{cid}", "e-Service, Outstanding charges, Pay", [("Child (parent persona)", who), ("Charge", comp), ("Method and amounts", how), ("Expected", exp)], cid)
many("PAY-SIM", "4 Payment cases", "Pay simulator", "https://pay.20-255-158-192.sslip.io", [("Success", "Click Pay"), ("Failure", "In the browser Console set the hidden input named outcome to the value Failed, then click Pay"), ("Cards", "None. The simulator has one Pay button and no card fields")], "UAT-PAR-01-N4, UAT-PAR-01-E2, UAT-PAR-01-A1")

# 5. FAS application: values the automation types in the e-Service form
many("FAS-APPLICANT", "5 FAS form", "Applicant (parent), e-Service form", "e-Service, Financial assistance, Apply for FAS, applicant section", [
    ("Academic year (#fas-academic-year)", "2026 (the current year)"), ("Full name (#applicant-fullName)", "Lim Wei Minh"), ("NRIC (#applicant-nric)", "S8512345I"), ("Date of birth (#applicant-dateOfBirth)", "1985-03-12"),
    ("Gender", "MALE"), ("Nationality", "SC (Singapore Citizen)"), ("Race", "CHINESE"), ("Relationship to the child", "FATHER"), ("Phone number", "91234567"), ("Email", "uat.parent@example.com"),
    ("Address", "Blk 418 Serangoon Central #09-321, Singapore 550418"), ("Commitment (#applicant-commitmentAgreed)", "Ticked"), ("Employment status (API only)", "EMPLOYED")],
    "UAT-PAR-02 family (Kent), UAT-031, UAT-031-E1 when a new application is needed", "When the prefill answers, these fields are locked and the system values stay. When it answers 502 the form is blank and these values are typed.")
for i, (nm, nric, dob, gender, extra) in enumerate([("UAT Child 20003", "S1620003D", "2016-08-15", "MALE", "age 10, the normal child"), ("UAT Child 20011", "S1620011E", "2018-08-15", "FEMALE", "age 8, the second child"), ("UAT Child 20029", "S1620029H", "2010-08-15", "MALE", "age 16, used to prove the age rule: at least 7 and younger than 16")], 1):
    many(f"FAS-CHILD{i}", "5 FAS form", f"Beneficiary {i} ({extra})", "Apply for FAS, beneficiaries section (Add beneficiary for rows 2 and more)", [
        ("Full name", nm), ("NRIC", nric), ("Date of birth", dob), ("Gender", gender), ("Class level", "PRIMARY"), ("School name", "UAT Primary School"), ("Grade", "P4")], "UAT-PAR-02 family" if i == 1 else "", "Dates are for the run date of 31 Oct 2026. Recompute the birth year if the age matters on another date.")
many("FAS-MEMBER", "5 FAS form", "Other family member", "Apply for FAS, family members section (Add family member)", [
    ("Full name", "Tan Mei Ling"), ("NRIC", "S8703219A"), ("Date of birth", "1987-06-20"), ("Gender", "FEMALE"), ("Relationship", "MOTHER"), ("Has income", "No"), ("Monthly income", "Left empty (typed only when Has income is Yes)")], "UAT-PAR-02 family")
many("FAS-PR", "5 FAS form", "Variant: Permanent Resident parent", "Same form, applicant section", [("Nationality", "PR"), ("Everything else", "As FAS-APPLICANT"), ("Expected", "The application goes straight to the school (SBFAS), HQ does not review it")], "UAT-031, UAT-031-E1 (PR household, Blocked until a PR persona is mapped)")
many("FAS-SEEDED", "5 FAS form", "Seeded application APP-4FDC4038 (API POST /fas/parent/applications)", "Seed UAT-PRE-03 step, same call the e-Service form makes", [
    ("Idempotency-Key", "UATSEED-FAS-S8901234H-2026-v1"), ("academicYear", "2026"), ("applicant.fullName / dateOfBirth / gender / address", "Taken from the prefill of S8901234H"), ("applicant.nric", "S8901234H"),
    ("applicant.nationality", "SC"), ("applicant.race", "OTHER"), ("applicant.relationshipToBeneficiary", "FATHER"), ("applicant.phoneNumber", "91234567"), ("applicant.email", "ahmad.rahman.s8901234h@example.com"),
    ("applicant.employmentStatus", "EMPLOYED"), ("applicant.commitmentAgreed", "true"), ("applicant.forwardToSchoolAgreed", "true"),
    ("beneficiaries", "C1 Ethan Rahman S3678638G and C2 Leo Rahman S5918715F (name, NRIC, dateOfBirth, gender, schoolName, classLevel, grade, academicLevelId from the prefill)"),
    ("familyMembers", "Every member of the prefill (otherFamilyMembers), isIncludedInPci true, hasIncome from the prefill"),
    ("Result", "APP-4FDC4038, status Pending MOE review, Gross household income 4400.00, Per capita income 1100.00, MOEFAS allocation 19.50 per child from 1 Dec 2026")], "UAT-PRE-03, UAT-031, UAT-031-E1")
many("FAS-HQ", "5 FAS form", "HQ confirmation of allocations", "Admin (MOE HQ), FAS, scheme, pending allocations (API POST /allocations/confirm)", [
    ("Remarks", "UAT-SEED approval of seeded application"), ("Earliest day it can run", "1 Dec 2026 (MOEFAS effective date)"), ("Eligibility rule", "Gross household income up to 4000.00 OR per capita income up to 1100.00"), ("HQ application screen", "Read only (no approve button)")], "UAT-PRE-03, UAT-031, UAT-033")

# 6. Schemes and clock
for r in [
    ("SCHEME-MOEFAS", "Schemes", "MOEFAS, real scheme on the host", "Admin, FAS, Schemes", [("Name", "MOE Financial Assistance Scheme (MOE FAS) 2026"), ("Applications open", "1 Jan 2026 to 30 Nov 2026"), ("Effective period", "1 Dec 2026 to 31 Dec 2027"), ("Budget", "Read at run time (a budget of 0 blocks confirm)"), ("Why not a test scheme", "The portal and the API refuse a second scheme with an overlapping period")], "UAT-PRE-03, UAT-031, UAT-033"),
    ("SCHEME-2028", "Schemes", "MOEFAS 2028 (Kent UAT-MOE-06)", "Admin, FAS, Schemes", [("Name", "MOEFAS 2028"), ("Applications open", "1 Aug 2028 to 31 Dec 2028"), ("Effective from", "1 Jan 2029")], "Kent only"),
    ("SCHEME-SBFAS-A", "Schemes", "SBFAS School A (to seed, Kent UAT-SCH-02)", "School portal, FAS, Schemes", [("Name", "Tier 1 of School A"), ("Applications open", "Inside the MOEFAS window"), ("Effective from", "1 Dec 2026"), ("Budget", "Greater than 0 when published"), ("Cleanup", "Leftover UAT-GAVIN-s31 and s33 are removed by tools/cleanup_uat_schemes.sql")], "UAT-031-E1, UAT-SCH-03, UAT-035, UAT-033"),
]:
    many(r[0], "6 Schemes and clock", r[2], r[3], r[4], r[5])
for d, ev, can in [("31 Oct 2026", "Today", "Stages 0 to 5 and 9. Stages 6 to 8 as preview only."), ("1 to 30 Nov 2026", "Fee period and MOEFAS form open", "Parents can submit, fees can be published and paid."), ("30 Nov 2026", "MOEFAS form closes", "Last day for stage 5."), ("1 Dec 2026", "MOEFAS effective date", "HQ can confirm allocations, subsidy can apply. Stages 6 to 8, 10 and 11 run in full."), ("31 Dec 2026", "Due date of the seeded fees", "Fee status changes after it.")]:
    add("CLOCK", "6 Schemes and clock", d, "Calendar", ev, can, "")

# 7. Environment
many("ENV", "7 Environment", "Hosted stack (Azure)", "run_uat.cmd hosted headed", [("Admin", "https://admin.20-255-158-192.sslip.io"), ("e-Service", "https://eservice.20-255-158-192.sslip.io"), ("Pay simulator", "https://pay.20-255-158-192.sslip.io"), ("Seed command only", ".\\run_uat.cmd seed hosted"), ("All Gavin cases and the seed", ".\\run_uat.cmd hosted headed"), ("Seed round", "artifacts\\seed_round.txt, increased by 1 on each run (UAT_SEED_KEEP=1 keeps it)")], "All")

sd = wb.create_sheet("Shared test data")
put(sd, ["Data ID", "Group", "Entity", "Where it is entered", "Field", "Value", "Used by cases", "Note"], SD, [14, 16, 34, 40, 38, 62, 36, 60])
sd.freeze_panes = "E2"
sd.auto_filter.ref = f"A1:H{len(SD) + 1}"

