# -*- coding: utf-8 -*-
"""New R4 validation cases (TC-268 to TC-331) with the results of the run of 26/10/2026, and updates for older cases."""

RUN_API = "Run 26/10/2026 (localhost build, API through the admin portal proxy). "
RUN_UI = "Run 26/10/2026 (localhost build, built-in browser). "

E_UI = "Localhost build (branch codesprint2ending), admin portal http://localhost:5173\nChrome (latest), locale en-US\nNeeds: none"
E_API = "Localhost build (branch codesprint2ending), gateway http://localhost:5273 through the admin portal proxy\nRequests sent with the session cookie of the signed in user\nNeeds: none"
E_F4 = "F4 build with API (FAS applications screens not available yet)\nChrome (latest)\nBuild: to be recorded at execution\nNeeds: ENV-R4-02"

PRE_SB = "1. The localhost stack is running.\n2. Signed in as School user school (Thi H Bui), Raffles Institution (SCH-001) with two active grades: Junior College 1 and Secondary 1.\n3. At least one active fee component exists for the school."
PRE_HQ = "1. The localhost stack is running.\n2. Signed in as MOE HQ user moehq.\n3. At least one active fee component of Function 3 exists."
PRE_F4_SC = "1. The F4 build is running with the FAS applications screens.\n2. Signed in as a School Admin with a Pending SBFAS application."
PRE_F4_HQ = "1. The F4 build is running with the FAS applications screens.\n2. Signed in as MOE HQ."

BASE_SB = "Base request: name R4-AUTO-<unique>, Application open 2400-01-01 to 2400-06-30, Effective 2401-01-01 to 2401-12-31, budget 1000, nationality SC, PCI 0 to 1000, one fee component with 10 percent for each grade, publish false."
BASE_HQ = "Base request: status Draft, name R4-AUTO-<unique>, Form 3200-01-01 to 3200-06-30, Effective 3201-01-01 to 3201-12-31, PCI 0 to 1100, nationality SC, one fee component with 10 percent for each stage, budget 1000."

SBA = "SBFAS scheme API (School Admin)"
HQA = "MOEFAS scheme API (MOE HQ)"
SBW = "New scheme wizard (School Admin)"
HQW = "New scheme wizard (MOE HQ)"
SBD = "Add fee dialog (School Admin)"

# (suite, ts, title, page, sev, pri, type, env, pre, data, steps, expected, status, actual, defect, trace, note)
N = []
def add(*a):
    N.append(a)

def api_sb(ts, title, sev, pri, data, steps, exp, status, actual, defect=None, trace="", note="", suite="F4.14 New scheme wizard", page=SBA):
    add(suite, ts, title, page, sev, pri, "API", E_API, PRE_SB, BASE_SB + " " + data, steps, exp, status, (RUN_API + actual) if actual else None, defect, trace, note)

def api_hq(ts, title, sev, pri, data, steps, exp, status, actual, defect=None, trace="", note="", suite="F4.14 New scheme wizard", page=HQA):
    add(suite, ts, title, page, sev, pri, "API", E_API, PRE_HQ, BASE_HQ + " " + data, steps, exp, status, (RUN_API + actual) if actual else None, defect, trace, note)

def ui(ts, title, page, sev, pri, pre, data, steps, exp, status, actual, defect=None, trace="", note="", suite="F4.14 New scheme wizard"):
    add(suite, ts, title, page, sev, pri, "Functional", E_UI, pre, data, steps, exp, status, (RUN_UI + actual) if actual else None, defect, trace, note)

def txt(suite, ts, title, page, sev, pri, pre, data, steps, exp, trace, note=""):
    add(suite, ts, title, page, sev, pri, "Functional", E_F4, pre, data, steps, exp, "Not Run", None, None, trace, note)

T = "Validation rules R4 (R4_FAS_Validation_Rules_EN.docx)"

# ================================================================= SBFAS API (School user)
api_sb("TS-057", "SBFAS scheme name is required", "S2", "High", "Names: empty and three spaces.",
       "1. Send the base request with name empty.\n2. Send it again with name made of three spaces.",
       "1. Both requests are refused with HTTP 400 and the message \"name is required.\".\n2. No scheme is created.",
       "Passed", "Both requests returned 400 \"name is required.\". No scheme was created.", None, T + " VR-WIZ-01; backend CreateSbfasSchemeValidator")
api_sb("TS-057", "SBFAS scheme name accepts 150 characters and refuses 151", "S3", "Medium", "Names of 150 and 151 characters.",
       "1. Send the base request with a name of 150 characters.\n2. Send it again with a name of 151 characters.",
       "1. The 150-character name is accepted (HTTP 201).\n2. The 151-character name is refused with 400 \"name must not exceed 150 characters.\".",
       "Passed", "150 characters: 201, saved as draft. 151 characters: 400 \"name must not exceed 150 characters.\". The validation rules document says 3 to 100 characters, the build uses 150 (column NVARCHAR(150)).", None, T + " VR-WIZ-02; sbfas_schemes.name NVARCHAR(150)", "The rules document says 3 to 100 characters. BA to align the document with the build.")
api_sb("TS-057", "SBFAS Application open from must be today or later", "S2", "High", "openFrom: today (UTC date) and yesterday.",
       "1. Send the base request with Application open from set to today and the other dates after it.\n2. Send it again with Application open from set to yesterday.",
       "1. Today is accepted (201).\n2. Yesterday is refused with 400 \"openFrom must be today or later.\".",
       "Passed", "Today: 201. Yesterday: 400 \"openFrom must be today or later.\". The server compares with the UTC date.", None, T + " VR-WIZ-08; backend rule openFrom >= today")
api_sb("TS-057", "SBFAS Application open to must be after Application open from", "S2", "High", "openTo equal to openFrom.",
       "1. Send the base request with Application open to equal to Application open from.",
       "1. The request is refused with 400 \"openTo must be after openFrom.\".",
       "Passed", "400 \"openTo must be after openFrom.\". The database also has the check open_from < open_to.", None, T + " VR-WIZ-05; CK_sbfas_schemes_date_rules")
api_sb("TS-057", "SBFAS Effective from must be after Application open to", "S2", "High", "effectiveFrom equal to openTo.",
       "1. Send the base request with Effective from equal to Application open to.",
       "1. The request is refused with 400 \"effectiveFrom must be after openTo.\".",
       "Passed", "400 \"effectiveFrom must be after openTo.\".", None, T + " VR-WIZ-07")
api_sb("TS-057", "SBFAS Effective to must be after Effective from and may be empty", "S2", "High", "effectiveTo equal to effectiveFrom, and null.",
       "1. Send the base request with Effective to equal to Effective from.\n2. Send it again with Effective to empty (null).",
       "1. The first request is refused with 400 \"effectiveTo must be after effectiveFrom.\".\n2. The second request is accepted (no end date).",
       "Passed", "Equal: 400 \"effectiveTo must be after effectiveFrom.\". Null: 201.", None, T + " VR-WIZ-06")
api_sb("TS-057", "SBFAS total budget cannot be negative and must be above 0 to publish", "S2", "High", "Budgets: -1, 0 as draft and 0 with publish true.",
       "1. Send the base request with budget -1.\n2. Send it with budget 0 and publish false.\n3. Send it with budget 0 and publish true.",
       "1. Refused with 400 \"totalBudgetAmount must be greater than or equal to 0.\".\n2. Accepted as a draft.\n3. Refused with 400 \"totalBudgetAmount must be greater than 0 when publishing.\".",
       "Passed", "-1: 400 with the expected message. 0 as draft: 201. 0 with publish true: 400 \"totalBudgetAmount must be greater than 0 when publishing.\".", None, T + "; backend CreateSbfasSchemeValidator budget rules")
api_sb("TS-058", "SBFAS nationality list is required, valid and without duplicates", "S2", "High", "Lists: [], [XX], [SC, SC] and all four codes.",
       "1. Send the base request with nationalities [].\n2. Send it with [\"XX\"].\n3. Send it with [\"SC\",\"SC\"].\n4. Send it with SC, PR, IS_ASEAN and IS_NON_ASEAN.",
       "1. 400 \"At least one nationality is required.\".\n2. 400 \"nationality must be one of: SC, PR, IS_ASEAN, IS_NON_ASEAN.\".\n3. 400 \"nationalities must not contain duplicates.\".\n4. Accepted.",
       "Passed", "All four results matched: 400, 400, 400 with the listed messages and 201 for the four codes.", None, T + " VR-WIZ-09", suite="F4.14 New scheme wizard")
api_sb("TS-058", "SBFAS needs at least one of the GHI band and the PCI band", "S2", "High", "GHI off and PCI off.",
       "1. Send the base request with isGhiEnabled false and isPciEnabled false.",
       "1. Refused with 400 \"At least one of GHI or PCI criteria must be enabled.\".",
       "Passed", "400 \"At least one of GHI or PCI criteria must be enabled.\".", None, T + " VR-WIZ-13")
api_sb("TS-058", "SBFAS PCI From is required when the PCI band is on", "S2", "High", "pciFrom null with isPciEnabled true.",
       "1. Send the base request with pciFrom null and pciTo 1000.",
       "1. Refused with 400 \"pciFrom is required when PCI is enabled.\".",
       "Failed", "Accepted: 201 \"SBFAS scheme saved as draft.\". The validator has the rule but the When clause covers the whole chain, so the NotNull check never runs. The wizard blocks an empty From, only a direct API call gets through.", "BUG-R4-007", T + " VR-WIZ-11; backend rule pciFrom is required")
api_sb("TS-058", "SBFAS GHI From is required when the GHI band is on", "S2", "High", "GHI on with ghiFrom null, ghiTo 100, operator OR.",
       "1. Send the base request with isGhiEnabled true, ghiFrom null, ghiTo 100 and incomeOperator OR.",
       "1. Refused with 400 \"ghiFrom is required when GHI is enabled.\".",
       "Failed", "Accepted: 201. Same cause as the PCI case.", "BUG-R4-007", T + " VR-WIZ-10; backend rule ghiFrom is required")
api_sb("TS-058", "SBFAS band values are not negative and To is not below From", "S2", "High", "ghiFrom -5; pciFrom -1; pciFrom 500 with pciTo 100; ghiFrom 500 with ghiTo 100; pciTo null.",
       "1. Send each wrong value in its own request.\n2. Send pciTo null.",
       "1. Each wrong value is refused with 400: \"ghiFrom must be >= 0.\", \"pciFrom must be >= 0.\", \"pciTo must be >= pciFrom.\", \"ghiTo must be >= ghiFrom.\".\n2. An empty To is accepted (no upper limit).",
       "Passed", "The four wrong values returned 400 with the listed messages. pciTo null: 201.", None, T + " VR-WIZ-10, VR-WIZ-11")
api_sb("TS-058", "SBFAS match rule is needed when both bands are on", "S2", "High", "Operators: null, XOR, AND.",
       "1. Send the base request with GHI and PCI both on and incomeOperator null.\n2. Send it with XOR.\n3. Send it with AND.",
       "1. 400 \"incomeOperator is required when both GHI and PCI are enabled.\".\n2. 400 \"incomeOperator must be 'AND' or 'OR'.\".\n3. Accepted.",
       "Passed", "null and XOR returned 400 with the listed messages. AND: 201.", None, T + " VR-WIZ-12")
api_sb("TS-058", "SBFAS scheme context accepts 1000 characters and refuses 1001", "S3", "Medium", "eligibilityDescription of 1000 and 1001 characters.",
       "1. Send the base request with a context of 1000 characters.\n2. Send it with 1001 characters.",
       "1. Accepted.\n2. Refused with 400 \"eligibilityDescription must not exceed 1000 characters.\".",
       "Passed", "1000: 201. 1001: 400 \"eligibilityDescription must not exceed 1000 characters.\".", None, "Backend CreateSbfasSchemeValidator; sbfas_schemes.eligibility_description NVARCHAR(1000)")
api_sb("TS-059", "SBFAS scheme needs a fee component with at least one grade", "S2", "High", "feeComponents [] and a component with items [].",
       "1. Send the base request with feeComponents [].\n2. Send it with one component and items [].",
       "1. 400 \"At least one fee component is required.\".\n2. 400 \"Each fee component needs at least one item.\".",
       "Passed", "Both returned 400 with the listed messages.", None, T + " VR-WIZ-14")
api_sb("TS-059", "SBFAS percentage accepts 0 to 100 and refuses values outside", "S1 (highest)", "High", "Percentages -1, 101, 0 and 100.",
       "1. Send the base request with -1 for every grade.\n2. Send it with 101.\n3. Send it with 0 for one grade and 100 for the other.",
       "1. and 2. Refused with 400 \"subsidyPercentage must be between 0 and 100.\".\n3. Accepted.",
       "Passed", "-1 and 101: 400 with the expected message. 0 and 100: 201.", None, T + " VR-WIZ-15")
api_sb("TS-059", "SBFAS percentage accepts at most two decimals", "S2", "Medium", "Percentages 33.333 and 33.33.",
       "1. Send the base request with 33.333 for every grade.\n2. Send it with 33.33.",
       "1. Refused with 400 \"subsidyPercentage must have at most 2 decimals.\".\n2. Accepted.",
       "Passed", "33.333: 400 \"subsidyPercentage must have at most 2 decimals.\". 33.33: 201.", None, T + " VR-WIZ-15")
api_sb("TS-059", "SBFAS refuses a fee component or a grade that is listed twice", "S2", "Medium", "The same fee component twice; the same grade twice in one component.",
       "1. Send the base request with the same feeComponentId in two entries.\n2. Send it with one grade twice in the items of a component.",
       "1. 400 \"feeComponents must not contain duplicate feeComponentId.\".\n2. 400 \"academicLevelId must not be duplicated within a fee component.\".",
       "Passed", "Both returned 400 with the listed messages.", None, "Backend CreateSbfasSchemeValidator")
api_sb("TS-059", "SBFAS refuses a fee component that does not exist", "S2", "High", "feeComponentId 00000000-0000-0000-0000-000000000099 (also tried on MOEFAS).",
       "1. Send the base request with an unknown feeComponentId.\n2. Send the MOEFAS base request with an unknown feeComponentId as MOE HQ.",
       "1. Refused with a 400 or 404 that says the fee component does not exist.\n2. Same for MOEFAS.",
       "Failed", "SBFAS create returned 201 and saved the unknown id. MOEFAS create also returned 201. No check against the fee components of Function 3.", "BUG-R4-008", "Data integrity; FS F4 v1.3 7.2 step 3 (only active fee components of Function 3)")
api_sb("TS-059", "SBFAS refuses a grade that is not offered by the school", "S2", "High", "academicLevelId AL-NOPE.",
       "1. Send the base request with one item whose academicLevelId is AL-NOPE.",
       "1. Refused with a 400 or 404 that says the grade does not exist for the school.",
       "Failed", "Accepted: 201. The unknown grade was saved with the scheme.", "BUG-R4-008", "Data integrity; FS F4 v1.3 7.2 step 3 (grades of the school)")
api_sb("TS-059", "SBFAS needs a percentage for every active grade of the school", "S2", "Medium", "Items for Junior College 1 only, the school also offers Secondary 1.",
       "1. Send the base request with items for Junior College 1 only.",
       "1. Refused: every active grade needs a value (0 percent if none).",
       "Failed", "Accepted: 201. The wizard blocks an empty cell (\"Enter a subsidy percentage for every active level.\") but the API does not.", "BUG-R4-009", T + " VR-WIZ-17")
api_sb("TS-061", "Add fee API refuses percentages outside 0 to 100 and more than two decimals", "S2", "High", "Published scheme; new fee component with -1, 101 and 33.333.",
       "1. Create a Published scheme (publish true, budget 1000).\n2. POST fee-components with -1 for every grade.\n3. Repeat with 101.\n4. Repeat with 33.333.",
       "1. and 2. 400 \"subsidyPercentage must be between 0 and 100.\".\n3. 400 \"subsidyPercentage must have at most 2 decimals.\".",
       "Passed", "All three returned 400 with the listed messages.", None, T + " VR-FEE-04", suite="F4.16 Add fee to a published scheme", page=SBA)
api_sb("TS-061", "Add fee API needs at least one item and no repeated grade", "S3", "Medium", "Items [] and one grade twice.",
       "1. POST fee-components with items [].\n2. POST with one grade twice.",
       "1. 400 \"At least one item is required.\".\n2. 400 \"academicLevelId must not be duplicated within the fee component.\".",
       "Passed", "Both returned 400 with the listed messages.", None, T + " VR-FEE-04", suite="F4.16 Add fee to a published scheme")
api_sb("TS-061", "Add fee API refuses a fee component already in the scheme", "S2", "High", "The component of the base request posted again.",
       "1. POST fee-components with the feeComponentId that the scheme already has.",
       "1. Refused with 409 \"This fee component is already configured for the scheme.\".",
       "Passed", "409 \"This fee component is already configured for the scheme.\".", None, T + " VR-FEE-03, VR-FEE-05", suite="F4.16 Add fee to a published scheme")
api_sb("TS-061", "Add fee API refuses a fee component or grade that does not exist", "S2", "High", "Unknown feeComponentId; unknown academicLevelId AL-NOPE.",
       "1. POST fee-components with an unknown feeComponentId.\n2. POST with a known component and academicLevelId AL-NOPE.",
       "1. and 2. Refused with a 400 or 404.",
       "Failed", "Both were accepted with 201 and saved on a Published scheme.", "BUG-R4-008", "Data integrity; " + T + " VR-FEE-03", suite="F4.16 Add fee to a published scheme")

# ================================================================= MOEFAS API (MOE HQ)
api_hq("TS-060", "MOEFAS scheme name is required and at most 150 characters", "S2", "High", "Names: empty, 150 and 151 characters.",
       "1. Send the base request with name empty.\n2. Send it with 150 characters.\n3. Send it with 151 characters.",
       "1. 400 \"Scheme name is required.\".\n2. Accepted.\n3. 400 \"Scheme name cannot exceed 150 characters.\".",
       "Passed", "400, 201 and 400 with the listed messages.", None, T + " VR-WIZ-01, VR-WIZ-02")
api_hq("TS-060", "MOEFAS dates must follow Form opens < Form closes < Effective from < Effective to", "S2", "High", "Form closes equal to Form opens; Form closes the same day at 23:59:59; Effective from equal to Form closes; Effective to equal to Effective from.",
       "1. Send the base request with Form closes equal to Form opens (same date and time).\n2. Send it with Form closes on the same day at 23:59:59.\n3. Send it with Effective from equal to Form closes.\n4. Send it with Effective to equal to Effective from.",
       "1. 400 \"OpenTo must be later than OpenFrom.\".\n2. Accepted (the wizard sends the closing time 23:59:59, which explains TC-185).\n3. 400 \"EffectiveFrom must be later than OpenTo.\".\n4. 400 \"EffectiveTo must be later than EffectiveFrom.\".",
       "Passed", "400, 201, 400 and 400 with the listed messages.", None, T + " VR-WIZ-05, VR-WIZ-06, VR-WIZ-07")
api_hq("TS-060", "MOEFAS refuses a scheme whose dates are in the past", "S3", "Medium", "Form 2020-01-01 to 2020-06-30, Effective from 2021-01-01.",
       "1. Send the base request with all dates in 2020 and 2021.",
       "1. Refused: a new scheme cannot start in the past (as the SBFAS API does with \"openFrom must be today or later.\").",
       "Failed", "Accepted: 201 \"MOE FAS scheme created successfully.\". The SBFAS API refuses the same dates.", "BUG-R4-010", T + " VR-WIZ-08")
api_hq("TS-060", "MOEFAS status must be Draft or Published", "S3", "Medium", "Status Archived.",
       "1. Send the base request with status Archived.",
       "1. Refused with 400 \"Status must be Draft or Published\".",
       "Passed", "400 \"Status must be Draft or Published\".", None, "Backend CreateMOEFASSchemeValidator")
api_hq("TS-060", "MOEFAS income bands follow the eligibility rules", "S2", "High", "GHI and PCI off; ghiFrom -1; pciFrom 500 with pciTo 100; both bands on with operator null.",
       "1. Send the base request with both bands off.\n2. Send it with ghiFrom -1.\n3. Send it with pciFrom 500 and pciTo 100.\n4. Send it with both bands on and incomeOperator null.",
       "1. 400 \"At least one income evaluation criterion (GHI or PCI) must be enabled.\".\n2. 400 \"GhiFrom cannot be negative.\".\n3. 400 \"PciTo must be greater than or equal to PciFrom.\".\n4. 400 \"IncomeOperator must be 'AND' or 'OR' when both GHI and PCI are enabled.\".",
       "Passed", "All four returned 400 with the listed messages.", None, T + " VR-WIZ-10, VR-WIZ-11, VR-WIZ-12, VR-WIZ-13")
api_hq("TS-060", "MOEFAS nationality list is required, valid and without duplicates", "S2", "High", "Lists: [], [XX], [SC, SC].",
       "1. Send the base request with nationalities [].\n2. Send it with [\"XX\"].\n3. Send it with [\"SC\",\"SC\"].",
       "1. 400 \"At least one eligible nationality must be specified.\".\n2. 400 \"Invalid nationality. Allowed values: SC, PR, IS_ASEAN, IS_NON_ASEAN.\".\n3. 400 \"Nationalities list must not contain duplicates.\".",
       "Passed", "All three returned 400 with the listed messages.", None, T + " VR-WIZ-09")
api_hq("TS-060", "MOEFAS subsidies are required, with a valid stage and no repeated stage and component", "S2", "High", "subsidies []; stage KINDER; the same stage and component twice.",
       "1. Send the base request with subsidies [].\n2. Send it with educationStage KINDER.\n3. Send it with PRIMARY and the same component twice.",
       "1. 400 \"At least one subsidy configuration is required.\".\n2. 400 \"EducationStage must be PRIMARY, SECONDARY, or PRE_UNIVERSITY.\".\n3. 400 \"Subsidies must not contain duplicate combinations of EducationStage and FeeComponentId.\".",
       "Passed", "All three returned 400 with the listed messages.", None, T + " VR-WIZ-14")
api_hq("TS-060", "MOEFAS percentage accepts 0 to 100 and refuses values outside", "S1 (highest)", "High", "Percentages -1 and 101.",
       "1. Send the base request with -1 for every stage.\n2. Send it with 101.",
       "1. and 2. Refused with 400 \"SubsidyPercentage must be between 0.00% and 100.00%.\".",
       "Passed", "Both returned 400 with the expected message.", None, T + " VR-WIZ-15")
api_hq("TS-060", "MOEFAS percentage accepts at most two decimals", "S3", "Low", "Percentage 33.333.",
       "1. Send the base request with 33.333 for every stage.",
       "1. Refused: only two decimals are allowed (as the SBFAS API does).",
       "Failed", "Accepted: 201. The MOEFAS validator checks the range only. The wizard also accepts 33.333 (TC-206).", "BUG-R4-002", T + " VR-WIZ-15")
api_hq("TS-060", "MOEFAS total budget cannot be negative", "S3", "Medium", "Budget -1.",
       "1. Send the base request with budget -1.",
       "1. Refused with 400 \"TotalBudgetAmount cannot be negative.\".",
       "Passed", "400 \"TotalBudgetAmount cannot be negative.\".", None, "Backend CreateMOEFASSchemeValidator")
api_hq("TS-060", "MOEFAS refuses a second scheme with the same name", "S2", "High", "Name of 150 characters sent twice.",
       "1. Send the base request with a name of 150 characters.\n2. Send the same name again.",
       "1. Accepted.\n2. Refused with a message that the name already exists.",
       "Passed", "The second request returned 400 \"A scheme with the name '...' already exists.\".", None, T + " VR-WIZ-03")

# ================================================================= UI (browser)
ui("TS-057", "SBFAS wizard shows the required messages of step General", SBW, "S2", "High", PRE_SB,
   "Step General left empty; name made of spaces.",
   "1. Open SBFAS schemes and click New scheme.\n2. Click Next without typing.\n3. Type spaces in the name and click Next.",
   "1. The step stays on General.\n2. Each required field shows a message: \"Name is required.\", \"Opening date is required.\", \"Closing date is required.\", \"Effective date is required.\".\n3. Spaces only give \"Name is required.\".",
   "Passed", "Next stayed on General and showed \"Name is required.\", \"Opening date is required.\", \"Closing date is required.\" and \"Effective date is required.\". Spaces only: \"Name is required.\".",
   None, T + " VR-WIZ-01")
ui("TS-057", "SBFAS wizard checks the order of the dates", SBW, "S2", "High", PRE_SB,
   "Closing = opening; effective date = closing; effective end = effective date; opening date yesterday.",
   "1. Fill step General with a valid scheme.\n2. Set Applications open to equal to Applications open from and click Next.\n3. Set Effective from equal to Applications open to and click Next.\n4. Set Effective to equal to Effective from and click Next.\n5. Set Applications open from to yesterday and click Next.\n6. Clear Effective to and click Next.",
   "1. \"Closing date must be after opening date.\".\n2. \"Effective date must be after the closing date.\".\n3. \"Effective end date must be after the effective date.\".\n4. \"Opening date cannot be before today.\".\n5. An empty Effective to is accepted and the step moves to Eligibility.",
   "Passed", "Messages: \"Closing date must be after opening date.\" (equal and before), \"Effective date must be after the closing date.\" (equal and before), \"Effective end date must be after the effective date.\" (equal and before), \"Opening date cannot be before today.\" for yesterday. Today and an empty Effective to move to Eligibility.",
   None, T + " VR-WIZ-05 to VR-WIZ-08")
ui("TS-057", "SBFAS wizard limits the scheme name to 150 characters", SBW, "S3", "Medium", PRE_SB,
   "Names of 150 and 151 characters.",
   "1. Fill step General with a name of 151 characters and click Next.\n2. Use 150 characters and click Next.",
   "1. \"Name must be 150 characters or fewer.\" and the step stays on General.\n2. The step moves to Eligibility.",
   "Passed", "151 characters: \"Name must be 150 characters or fewer.\". 150 characters: Eligibility opened. The field has maxlength 150.",
   None, T + " VR-WIZ-02")
ui("TS-057", "SBFAS wizard total budget accepts 0 or more with two decimals", SBW, "S3", "Medium", PRE_SB,
   "Budget values -1, abc, empty, 0 and 1234.567.",
   "1. Fill step General with a valid scheme.\n2. Set Total budget to -1, then to abc, then empty, then 1234.567 and click Next each time.\n3. Set 0 and click Next.",
   "1. -1 shows a message that the budget cannot be negative.\n2. abc and empty show a message that a number is needed.\n3. 1234.567 shows a message about two decimals.\n4. 0 is accepted.",
   "Failed", "-1 shows \"Budget cannot be negative.\". abc and an empty field show the same \"Budget cannot be negative.\", which is the wrong reason. 1234.567 shows \"Budget can have at most two decimal places.\". 0 is accepted.",
   "BUG-R4-014", "Backend rule totalBudgetAmount >= 0; usability")
ui("TS-058", "SBFAS wizard needs a nationality and an income band with valid values", SBW, "S2", "High", PRE_SB,
   "No nationality; both bands off; PCI From empty; PCI From 500 with To 100; PCI From -1; To empty.",
   "1. Open step Eligibility with a valid step General.\n2. Click Next with no nationality ticked.\n3. Tick Singapore citizen and switch both bands off, click Next.\n4. Switch PCI on and clear From, click Next.\n5. Enter From 500 and To 100, click Next.\n6. Enter From -1, click Next.\n7. Enter From 0 and clear To, click Next.",
   "2. \"Select at least one nationality.\".\n3. \"Enable at least one income band.\".\n4. and 6. A message that From must be 0 or more.\n5. A message that To must not be below From.\n7. Accepted, the step moves to Subsidy.",
   "Passed", "\"Select at least one nationality.\", \"Enable at least one income band.\", \"Enter a value of zero or more.\" (empty and -1), \"The upper value must be at least the lower value.\" (500 and 100). From 0 with an empty To moved to Subsidy.",
   None, T + " VR-WIZ-09 to VR-WIZ-13")
ui("TS-059", "SBFAS wizard checks the percentage cells", SBW, "S2", "High", PRE_SB,
   "Cell values -1, 101, 33.333, empty, 0 and 100.",
   "1. Open step Subsidy, add one fee component.\n2. Type -1 in one cell and click Review.\n3. Repeat with 101, 33.333 and an empty cell.\n4. Enter 0 and 100 and click Review.",
   "1. Each wrong value blocks Review and names the allowed range 0 to 100 (33.333: two decimals).\n2. 0 and 100 are accepted and Review opens.",
   "Failed", "All wrong values block Review. -1, 101 and an empty cell show the same \"Enter a subsidy percentage for every active level.\", which does not say 0 to 100. 33.333 shows \"Subsidy percentages allow up to two decimal places.\". 0 and 100 open Review.",
   "BUG-R4-014", T + " VR-WIZ-15 (message of the rules document: Subsidy rate must be between 0% and 100%)")
ui("TS-057", "SBFAS wizard shows why a duplicate scheme name is refused", SBW, "S2", "High", PRE_SB + "\n4. A scheme named R4-AUTO-ui-probe exists as a Draft.",
   "Name R4-AUTO-ui-probe used twice.",
   "1. Complete the four steps of a new scheme with the name of the existing scheme.\n2. Click Save draft.\n3. Click Publish.",
   "1. and 2. The scheme is not created and the message says that a scheme with this name already exists.",
   "Failed", "The scheme was not created. The toast says \"Unable to create scheme. The scheme could not be created. Please try again.\" for both Save draft and Publish. The API answers 409 \"A scheme with this name already exists for this school.\", the screen does not show it.",
   "BUG-R4-015", T + " VR-WIZ-03, VR-PUB-04")
ui("TS-061", "SBFAS Add fee dialog blocks invalid percentages and saves valid ones", SBD, "S2", "High", PRE_SB + "\n4. A Published SBFAS scheme with one fee component exists.",
   "Percentages 101, -1, 33.333, empty, then 15 and 20.",
   "1. Open the row menu of the Published scheme and click Add fee.\n2. Choose a fee that is not in the scheme.\n3. Enter 101 for one grade and click Add fee.\n4. Repeat with -1, 33.333 and an empty field.\n5. Enter 15 and 20 and click Add fee.",
   "1. The dialog stays open and nothing is saved for each wrong value (empty field: a message with the range).\n2. 15 and 20 are saved with a success message and the fee count goes up by one.",
   "Passed", "101, -1 and 33.333 keep the dialog open (the number field uses min 0, max 100, step 0.01, so the browser blocks the submit). An empty field shows the toast \"Check the fee details. Enter a percentage from 0 to 100 with at most 2 decimal places for every active grade.\". 15 and 20 saved with the toast \"Fee added\" and the fee count went from 1 to 2.",
   None, T + " VR-FEE-04", suite="F4.16 Add fee to a published scheme")
ui("TS-060", "MOEFAS wizard limits the scheme name to 150 characters", HQW, "S3", "Medium", PRE_HQ,
   "Names of 150 and 151 characters.",
   "1. Open MOEFAS and click New scheme.\n2. Fill step General with a name of 151 characters and click Next.\n3. Use 150 characters and click Next.",
   "1. A message that the name must not exceed 150 characters and the step stays on General.\n2. The step moves to Eligibility.",
   "Passed", "151 characters: \"Scheme name must not exceed 150 characters.\" and the step shows the error mark. 150 characters: Eligibility opened.",
   None, T + " VR-WIZ-02")
ui("TS-060", "MOEFAS wizard refuses negative income bands and checks To against From", HQW, "S2", "High", PRE_HQ,
   "GHI From -1; PCI From -5; GHI From 500 with To 100.",
   "1. Open step Eligibility with a valid step General and tick Singapore Citizen, GHI and PCI.\n2. Enter GHI From -1 and click Next.\n3. Enter PCI From -5 and click Next.\n4. Enter GHI From 500 and To 100 and click Next.",
   "2. and 3. A message that a number of 0 or more is needed.\n4. A message that To must not be less than From.",
   "Passed", "\"Enter a valid number of 0 or more.\" for GHI From -1 and PCI From -5. \"To must not be less than From.\" for 500 and 100. Letters cannot be typed (number field).",
   None, T + " VR-WIZ-10, VR-WIZ-11")
ui("TS-060", "MOEFAS wizard shows why a duplicate scheme name is refused", HQW, "S2", "High", PRE_HQ + "\n4. A MOEFAS scheme named R4-AUTO-ui-moe exists.",
   "Name R4-AUTO-ui-moe used twice.",
   "1. Complete the four steps of a new scheme with the name of the existing scheme.\n2. Click Draft.",
   "1. The scheme is not created and the message says that the name already exists.",
   "Not Run", None, None, T + " VR-WIZ-03", "Automated in test_real_f4v_validation.py (test_tc_314), waits for the run on the user's machine.")

# ================================================================= not available yet (text input handling and messages)
txt("F4.5 Filters and search", "TS-062", "Search with only spaces behaves like an empty search", "FAS applications list (MOE HQ)", "S3", "Medium", PRE_F4_HQ,
    "Search text: five spaces.", "1. Open FAS applications.\n2. Type five spaces in the search box.\n3. Press Enter.",
    "1. No filter is applied and the full list stays.\n2. The box shows the spaces removed.", T + " search box (A4, B4): Spaces only")
txt("F4.5 Filters and search", "TS-062", "Search removes tab, line break and control characters", "FAS applications list (MOE HQ)", "S3", "Medium", PRE_F4_HQ,
    "Text with a tab, a line break and a null byte between two words.", "1. Paste the text into the search box.\n2. Press Enter.",
    "1. Tab and line break become one space.\n2. Control characters and the null byte are removed and never reach the database.", T + " search box: Tab or line break, Control characters, Null byte")
txt("F4.5 Filters and search", "TS-062", "Search treats SQL, script, JSON and template text as plain text", "FAS applications list (MOE HQ)", "S2", "High", PRE_F4_HQ,
    "' OR 1=1 --, <script>alert(1)</script>, {\"a\":1}, ${jndi:ldap://x}, %27, % and _.", "1. Search each text in turn.",
    "1. Each search returns \"No applications found.\" with no error and no script is run.\n2. % and _ are not wildcards and %27 is not decoded.", T + " search box: Special characters, SQL, Script, JSON, Percent code")
txt("F4.5 Filters and search", "TS-062", "Search accepts emoji and letters of any script", "FAS applications list (MOE HQ)", "S4 (lowest)", "Low", PRE_F4_HQ,
    "Text: a smiley emoji and Vietnamese letters.", "1. Type the text in the search box and press Enter.",
    "1. The text is accepted and the list shows \"No applications found.\" when nothing matches.", T + " search box: Emoji, letters of any script")
txt("F4.5 Filters and search", "TS-062", "Search runs on Enter and 300 ms after the last key", "FAS applications list (MOE HQ)", "S3", "Medium", PRE_F4_HQ,
    "Text: aisha.", "1. Type aisha and press Enter.\n2. Clear the box, type aisha and wait without pressing Enter.",
    "1. The list is filtered at once on Enter.\n2. Without Enter the list is filtered about 300 ms after the last key and goes back to page 1.", T + " search box: Trigger, Combined with")
txt("F4.9 Approve SBFAS", "TS-063", "Approve comment counter counts line breaks and emoji as one and keeps a pasted text over 500", "Approve SBFAS dialog", "S3", "Medium", PRE_F4_SC,
    "Comment of 600 characters with a line break and an emoji.", "1. Open Approve on a Pending application.\n2. Type a line break and an emoji and read the counter.\n3. Paste 600 characters.",
    "1. The counter counts each line break and each emoji as 1.\n2. The pasted text is kept, the counter shows 600/500 in red and Confirm approval is disabled.", T + " E2 and F2 Comment: Counter, Paste over 500")
txt("F4.9 Approve SBFAS", "TS-063", "Approve comment trims spaces and saves a spaces-only comment as empty", "Approve SBFAS dialog", "S3", "Medium", PRE_F4_SC,
    "Comments: '  ok  ' and five spaces.", "1. Approve with the comment '  ok  ' and open the Decision block.\n2. Approve another application with five spaces.",
    "1. The saved comment is 'ok'.\n2. The spaces-only comment is saved as empty and the Decision block shows no comment.", T + " E2 and F2 Comment: Leading and trailing spaces, Spaces only")
txt("F4.9 Approve SBFAS", "TS-063", "Approve comment removes control characters and the null byte", "Approve SBFAS dialog", "S3", "Medium", PRE_F4_SC,
    "Comment with U+0001, a tab, a line break and a null byte.", "1. Paste the comment and confirm the approval.\n2. Read the saved comment through the drawer and the API.",
    "1. Line break and tab are kept.\n2. Other control characters and the null byte are removed before save.", T + " E2 and F2 Comment: Control characters, Null byte")
txt("F4.9 Approve SBFAS", "TS-063", "Approve comment keeps SQL, script, JSON and template text as plain text", "Approve SBFAS dialog", "S2", "High", PRE_F4_SC,
    "Comments: ' OR 1=1 --, <b>text</b>, {{7*7}}, ${7*7}.", "1. Approve with each text.\n2. Read the drawer, the History and the CSV export.",
    "1. The text is saved as typed and shown as plain text, encoded in the drawer, History, CSV and parent email.\n2. No data other than the decision changes.", T + " E2 and F2 Comment: SQL, Script and HTML, JSON")
txt("F4.9 Approve SBFAS", "TS-063", "A failed save keeps the approval dialog open with the comment", "Approve SBFAS dialog", "S2", "High", PRE_F4_SC + "\n3. The save request can be made to fail (ENV-R4-03).",
    "Comment: Approved after review.", "1. Open Approve, type the comment and make the save fail.\n2. Click Confirm approval.",
    "1. The message \"Something went wrong. Please try again.\" is shown.\n2. The dialog stays open with the comment and the application stays Pending.", T + " E2 Comment: Save fails; shared messages")
txt("F4.10 Reject SBFAS", "TS-064", "Reject comment made of spaces is invalid", "Reject application dialog", "S2", "High", PRE_F4_SC,
    "Reason: Income above limit. Comment: five spaces.", "1. Open Reject, choose the reason and type five spaces.\n2. Read the field and the button.",
    "1. \"Comment is required.\" is shown.\n2. Reject application stays disabled.", T + " G2 Comment: Required, Spaces only")
txt("F4.10 Reject SBFAS", "TS-064", "Reject comment counter, paste over 500 and control characters", "Reject application dialog", "S3", "Medium", PRE_F4_SC,
    "Comment of 600 characters; comment with a null byte and U+0001.", "1. Paste 600 characters and read the counter.\n2. Paste the comment with control characters and reject.",
    "1. The text is kept, the counter shows 600/500 in red and the button is disabled.\n2. Control characters and the null byte are removed before save.", T + " G2 Comment: Counter, Paste over 500, Control characters")
txt("F4.10 Reject SBFAS", "TS-064", "A reject comment that starts with = is exported as text", "Reject application dialog", "S2", "High", PRE_F4_SC + "\n3. A rejected application has the comment =HYPERLINK(\"x\").",
    "Comment: =HYPERLINK(\"x\").", "1. Reject with the comment.\n2. Export the list and open the file.",
    "1. The cell value starts with an apostrophe and is shown as text, no formula runs.", T + " G2 Comment: CSV export")
txt("F4.9 Approve SBFAS", "TS-065", "Not enough MOEFAS budget disables Confirm approval", "Approve MOEFAS dialog", "S1 (highest)", "High", PRE_F4_HQ + "\n3. A MOEFAS scheme whose remaining budget is below the subsidy.",
    "Remaining budget S$ 100, subsidy needed S$ 250.", "1. Open Approve MOEFAS on the application.\n2. Read the budget note and the button.",
    "1. \"Not enough MOEFAS budget. This approval needs S$ 250.00 but only S$ 100.00 is left.\" is shown.\n2. Confirm approval is disabled and nothing is saved.", T + " Shared messages: Not enough MOEFAS budget")
txt("F4.9 Approve SBFAS", "TS-065", "Approve dialog says when the student has no open fee", "Approve SBFAS dialog", "S3", "Medium", PRE_F4_SC + "\n3. The student has no open fee.",
    "Student without open fee.", "1. Open Approve for the student.\n2. Read the list of fees.",
    "1. \"No open fees right now. Fees issued later are subsidised automatically.\" is shown in the fee list.", T + " Shared messages: Student has no open fee")
txt("F4.9 Approve SBFAS", "TS-065", "Confirm approval and Reject stay disabled with a message until the input is complete", "Approve SBFAS dialog", "S2", "Medium", PRE_F4_SC,
    "No tier chosen; no reason chosen.", "1. Open Approve and clear the tier, read the message.\n2. Open Reject without a reason, read the message.",
    "1. \"Select a tier to approve.\" and Confirm approval is disabled.\n2. \"Select a reason to reject.\" and Reject application is disabled.", T + " Shared messages: Confirm or Reject is not allowed yet")
txt("F4.9 Approve SBFAS", "TS-065", "A failed export or save shows the standard error message", "FAS applications list (MOE HQ)", "S3", "Medium", PRE_F4_HQ + "\n3. The export or save request can be made to fail (ENV-R4-03).",
    "Export and Reject save failing.", "1. Click Export while the export request fails.\n2. Click Reject application while the save fails.",
    "1. and 2. \"Something went wrong. Please try again.\" is shown, nothing is saved and the dialog stays open.", T + " Shared messages: System error on save or export")

# ================================================================= updates for earlier cases
U = {
 "174": ("Failed", "Automated run: the rows are not sorted by Effective from. The list comes back in creation order (95 rows: 2527, 2509 ... 2377, then 3401, 3293 ... 2217, then 2207 ...). It looked sorted while the stack held only a few schemes.", "BUG-R4-016"),
 "161": ("Passed", "Without a session GET moe-schemes and GET sbfas-schemes both return 401. The redirect of the browser to the sign in page is covered by TC-901.", None),
 "165": ("Failed", "MOE HQ calling GET sbfas-schemes gets 403 as expected. The School user calling GET moe-schemes gets 200 with 80 rows and GET of one scheme 200. Only POST is refused (403). The menu hides MOEFAS for the school, the API does not.", "BUG-R4-013"),
 "169": ("Passed", "The School user list shows the 2 schemes of Raffles Institution (SBF-00001 and SBF-00002), equal to GET sbfas-schemes (2 records), footer 2 schemes and no MOEFAS scheme. The second school (MRS-0012) was not checked, the seed has no second school account.", None),
 "173": ("Failed", "The row shows name, code SBF-00002, eligibility Singapore citizen · GHI ≤ S$1,000.00 OR PCI ≤ S$1,000.00, application period 2026-10-23 – 2026-10-24, effective period 2026-10-30 – 2027-01-28, status Application closed and 3 fees. No text Approved by school, dates as YYYY-MM-DD (case book DD/MM/YYYY), no Open badge and no No end date text.", "BUG-R4-012"),
 "201": ("Passed", "Step 3 lists Junior College 1 and Secondary 1, the 2 active grades of Raffles Institution returned by the offerings API. No Primary, Secondary or Pre-University row.", None),
 "202": ("Passed", "Picking Annual Camp Fee adds one column with a percentage cell for each grade. The cells start at 0 (min 0, max 100, step 0.01). The remove control of the column was not clicked in this run.", None),
 "203": ("Passed", "Step 1 has Scheme name, Applications open from, Applications open to, Effective from, Effective to (optional), Total budget and Scheme context (optional). There is no Scheme type and no Level field. The blue note was not compared.", None),
 "222": ("Passed", "Same name and same period: 409 \"A scheme with this name already exists for this school.\". Same name with an overlapping but different period gives the same 409. The block works, the message names the duplicate name and not the overlapping period.", None),
 "223": ("Passed", "A scheme with a different name and exactly the same period was accepted and is Published.", None),
 "225": ("Failed", "Two Draft schemes with the same effective period were saved (201 and 201), so the draft rule holds. The second half (overlap fails only at Publish) fails because Publish does not detect overlaps, see BUG-R4-003.", "BUG-R4-003"),
 "228": ("Failed", "A second scheme with the same name and a later period (Effective from one year later) is refused with 409 \"A scheme with this name already exists for this school.\". The earlier scheme is not ended and keeps no end date.", "BUG-R4-011"),
 "241": ("Passed", "The row menu of a Published scheme offers View and Add fee. The dialog lists the fees not yet in the scheme (Annual Camp Fee is not in the list) and the rows Junior College 1 and Secondary 1. Saving 15 and 20 shows the toast \"Fee added\" (\"The fee component was added successfully.\") and the fee count goes from 1 to 2. The toast wording differs from the case book.", None),
}

# Defect link additions to earlier defects (appended to the Linked Test Case(s) column of the defect report)
TC_ADD = {"BUG-R4-002": ", TC-301", "BUG-R4-003": ", TC-225"}

# Validation rule to case mapping (FS Trace rows)
VR = [
 ("VR-SCH-01", "Role data isolation: MOE HQ sees MOEFAS schemes only.", "TC-168, TC-165"),
 ("VR-SCH-02", "Role data isolation: School Admin sees the SBFAS schemes of the own school only.", "TC-169, TC-165"),
 ("VR-SCH-03", "Summary cards count the schemes by phase.", "TC-171"),
 ("VR-SCH-04", "Upcoming scheme definition.", "TC-171, TC-175"),
 ("VR-SCH-05", "Table column structure of the schemes list.", "TC-172, TC-173"),
 ("VR-SCH-06", "Row actions by scheme status.", "TC-178, TC-229, TC-231, TC-235"),
 ("VR-WIZ-01", "Scheme name is required.", "TC-183, TC-268, TC-293, TC-304"),
 ("VR-WIZ-02", "Scheme name length (rules document says 3 to 100, build allows 150).", "TC-269, TC-293, TC-306, TC-312"),
 ("VR-WIZ-03", "Scheme name is unique in its scope.", "TC-222, TC-303, TC-310, TC-314"),
 ("VR-WIZ-04", "Academic year is required (field not in the build, open point).", "None"),
 ("VR-WIZ-05", "Form closes is not before Form opens.", "TC-185, TC-271, TC-294, TC-305"),
 ("VR-WIZ-06", "Effective to is after Effective from.", "TC-187, TC-273, TC-294, TC-305"),
 ("VR-WIZ-07", "Effective from is after Form closes.", "TC-186, TC-272, TC-294, TC-305"),
 ("VR-WIZ-08", "Effective from is not in the past for a new scheme.", "TC-270, TC-295, TC-305"),
 ("VR-WIZ-09", "At least one eligible nationality.", "TC-191, TC-275, TC-298, TC-308"),
 ("VR-WIZ-10", "GHI limits are numbers of 0 or more.", "TC-194, TC-278, TC-279, TC-297, TC-313"),
 ("VR-WIZ-11", "PCI limits are numbers of 0 or more.", "TC-194, TC-277, TC-279, TC-297, TC-313"),
 ("VR-WIZ-12", "Income match rule.", "TC-190, TC-280, TC-297"),
 ("VR-WIZ-13", "At least one income band.", "TC-192, TC-276, TC-297, TC-308"),
 ("VR-WIZ-14", "At least one fee component.", "TC-196, TC-282, TC-299"),
 ("VR-WIZ-15", "Subsidy percentage from 0 to 100 with two decimals.", "TC-205, TC-206, TC-283, TC-284, TC-300, TC-301, TC-309"),
 ("VR-WIZ-16", "Fixed subsidy amount of 0 or more (value type not in the build).", "TC-207"),
 ("VR-WIZ-17", "Every grade has a value.", "TC-205, TC-288"),
 ("VR-PUB-01", "MOEFAS effective period overlap.", "TC-219"),
 ("VR-PUB-02", "MOEFAS form period overlap.", "TC-220"),
 ("VR-PUB-03", "Adjacent periods allowed.", "TC-221"),
 ("VR-PUB-04", "SBFAS same name overlap.", "TC-222"),
 ("VR-PUB-05", "SBFAS different name allowed.", "TC-223"),
 ("VR-PUB-06", "Draft with overlapping dates.", "TC-225"),
 ("VR-PUB-07", "Earlier scheme gets the day before as Effective to.", "TC-226, TC-228"),
 ("VR-PUB-08", "Published scheme is immutable.", "TC-229, TC-230"),
 ("VR-FEE-01", "Add fee is offered on the allowed statuses.", "TC-231"),
 ("VR-FEE-02", "Add fee is refused on a Closed scheme.", "TC-235"),
 ("VR-FEE-03", "Add fee lists only the missing components.", "TC-232, TC-291, TC-292"),
 ("VR-FEE-04", "Invalid rate blocks Add to scheme.", "TC-234, TC-289, TC-290, TC-311"),
 ("VR-FEE-05", "Existing components are locked.", "TC-238, TC-291"),
 ("VR-FEE-06", "New component is saved and applied to fees.", "TC-236, TC-239, TC-240, TC-241"),
 ("SRCH (A4, B4)", "Search box rules: length, trim, spaces only, control characters, special text, trigger.", "TC-069, TC-070, TC-071, TC-072, TC-073, TC-074, TC-075, TC-315, TC-316, TC-317, TC-318, TC-319"),
 ("CMT-APP (E2, F2)", "Approve comment rules.", "TC-134, TC-135, TC-136, TC-320, TC-321, TC-322, TC-323, TC-324"),
 ("CMT-REJ (G2)", "Reject comment rules.", "TC-144, TC-145, TC-166, TC-325, TC-326, TC-327"),
 ("MSG (section 15)", "Shared messages.", "TC-058, TC-072, TC-133, TC-153, TC-156, TC-162, TC-328, TC-329, TC-330, TC-331"),
]
