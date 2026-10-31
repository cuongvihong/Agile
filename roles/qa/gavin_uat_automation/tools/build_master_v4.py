# Builds roles/qa/uat-master_v4_chain.xlsx from roles/qalead/uat-master.xlsx
# Gavin's rows are replaced, one case is added, chain columns are added to every row, shared data sheets are added.
# Other owners' text is NOT changed.
import sys, re, math, copy, os
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.formatting import ConditionalFormattingList

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
src = open(os.path.join(HERE, "build_gavin_redesign.py"), encoding="utf-8").read()
ns = {}
sys.argv = ["x", os.devnull]
exec(src[:src.index("thin = Side(")], ns)
CASES, STAGES, OVERLAP, MISMATCH = ns["CASES"], ns["STAGES"], ns["OVERLAP"], ns["MISMATCH"]

wb = load_workbook(SRC)
ws = wb["Tests"]
rowof = {ws.cell(r, 1).value: r for r in range(4, 200) if ws.cell(r, 1).value}
LAST = max(rowof.values())

# ---------- chain mapping ----------
UP = {0: [], 1: [0], 2: [0], 3: [0, 1], 4: [2], 5: [3, 4], 6: [5], 7: [6], 8: [2, 6, 7], 9: [1, 2, 8], 10: [1, 7, 9], 11: [6, 7, 8, 9], 12: list(range(12)), 13: [9]}
DOWN = {s: [t for t, ups in UP.items() if s in ups] for s in UP}
SHORT = {st[0]: st for st in STAGES}
case_stage, case_order, n = {}, {}, 0
for st in STAGES:
    ids = [x.strip() for x in (st[3] + (", " + st[5] if st[5] else "")).split(",")]
    for cid in ids:
        n += 1; case_stage[cid] = st[0]; case_order[cid] = n

def stage_label(i): return f"{i} {SHORT[i][1]}"
def owners_of(i):
    st = SHORT[i]; return st[2] + (" and " + st[4] if st[4] else "")
def ref(i): return f"Stage {i} {SHORT[i][1]} ({owners_of(i)})"
def stagelist(lst):
    if lst == list(range(12)): return "Every stage 0 to 11"
    return "; ".join(ref(i) for i in lst) if lst else "Start of the chain"

DATA_BY_STAGE = {
 0: "People table, Shared test data, groups 1 People",
 1: "C1 Ethan, C2 Leo, C3 Isaac: top-up 20.00 each (Shared test data, groups 2 to 4)",
 2: "Charges per child (Shared test data, groups 2 to 4): Fee 100, 600, 50, 700 and the real Term 4 fees",
 3: "Parents PA (S8901234H) and PB (S6789012F)",
 4: "Schemes and clock (Shared test data, group 6)",
 5: "Application APP-4FDC4038 of PA for C1 and C2 (family of two), paper variants by the school",
 6: "Same applications; controls C3, C4 (already approved APP-01003)",
 7: "Pending applications routed to School A",
 8: "Granted child and charge (Shared test data, groups 2 to 4)",
 9: "One child per payment case (Shared test data, groups 2 to 4)",
 10: "PA and PB views of the results above",
 11: "Totals of stages 6 to 9",
 12: "One child end to end, taken from the threads above",
 13: "Closure account of DATA-LIFE",
}
GAVIN_DATA = {
 "UAT-031": "C1 Ethan and C2 Leo (APP-4FDC4038). Controls: C3 Isaac and C4 Sophia (APP-01003 approved), children with a Pending application already on the host",
 "UAT-031-E1": "As UAT-031, plus a published School A SBFAS scheme (to seed) and a School B child (to map)",
 "UAT-033": "C4 Sophia as the granted child (APP-01003) with a fee of 100 to seed, C3 Isaac as the capped control (Shared test data, groups 2 to 4)",
 "UAT-PAR-01": "C1 Ethan, UAT-SEED Fee 100, EA 520.00 to 420.00",
 "UAT-PAR-01-N3": "C2 Leo, UAT-SEED Fee 600 and a small real charge, EA 520.00 unchanged",
 "UAT-PAR-01-A1": "C3 Isaac, Fee 600, Both: EA 520.00 plus Online 80.00. Second variant C4 Sophia, Fee 50, online only",
 "UAT-PAR-01-N4": "C5 Grace, Fee 600 Both with the online part failing (reversal expected), and Fee 50 online only failing",
 "UAT-PAR-01-E2": "C2 Leo, Fee 700 Both with the online part failing (own child, so it does not touch N3 or N4)",
}

# ---------- Tests sheet ----------
GAVIN_IDS = {c["ID"] for c in CASES}
pairs = {}
def heights(text, width):
    lines = 0
    for line in str(text).split("\n"): lines += max(1, math.ceil(len(line) / (width * 1.15)))
    return lines
def fit(row):
    h = max(heights(ws.cell(row, 6).value or "", 40), heights(ws.cell(row, 7).value or "", 65), heights(ws.cell(row, 11).value or "", 24), heights(ws.cell(row, 12).value or "", 40), heights(ws.cell(row, 13).value or "", 42), heights(ws.cell(row, 14).value or "", 40))
    ws.row_dimensions[row].height = min(409, max(60, h * 11.5))

newrow = LAST + 1
for c in CASES:
    cid = c["ID"]
    if cid in rowof: r = rowof[cid]
    else:
        r = newrow; newrow += 1; rowof[cid] = r
        base = rowof["UAT-031"]
        for col in range(1, 11): ws.cell(r, col)._style = copy.copy(ws.cell(base, col)._style)
    area = "Fees and payments" if cid.startswith("UAT-PAR") else "FAS assessment"
    ws.cell(r, 1, cid); ws.cell(r, 2, c["Test"]); ws.cell(r, 3, area); ws.cell(r, 4, "Gavin"); ws.cell(r, 5, c["Role"])
    ws.cell(r, 6, c["Setup"]); ws.cell(r, 7, c["Steps"] + "\n\nWatch for: " + c["Watch"]); ws.cell(r, 8, "Not Run")
LASTNEW = max(rowof.values())

HEAD = ["Stage", "Chain order", "Comes from", "Hands on to", "Shared data used"]
widths = [24, 8, 42, 40, 40]
hs = ws.cell(3, 10)
for i, (h, w) in enumerate(zip(HEAD, widths)):
    col = 11 + i
    cell = ws.cell(3, col, h); cell._style = copy.copy(hs._style)
    ws.column_dimensions[get_column_letter(col)].width = w
gv = {c["ID"]: c for c in CASES}
for cid, r in rowof.items():
    for col in range(11, 16): ws.cell(r, col)._style = copy.copy(ws.cell(r, 7)._style)
    if cid in case_stage:
        st = case_stage[cid]
        ws.cell(r, 11, stage_label(st)); ws.cell(r, 12, case_order[cid])
        if cid in gv:
            ws.cell(r, 13, gv[cid]["In"]); ws.cell(r, 14, gv[cid]["Out"])
        else:
            ws.cell(r, 13, stagelist(UP[st])); ws.cell(r, 14, stagelist(DOWN[st]) if DOWN[st] else "End of the chain")
        ws.cell(r, 15, GAVIN_DATA.get(cid, DATA_BY_STAGE[st]))
    else:
        ws.cell(r, 11, "Out of the chain"); ws.cell(r, 13, "View As and FAQ chatbot are not in this build. Keep the case, run it when the feature exists.")
    if cid in GAVIN_IDS or cid in case_stage: fit(r)
    ws.cell(r, 12).alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
    for col in (11, 13, 14, 15): ws.cell(r, col).alignment = Alignment(wrap_text=True, vertical="top")

ws.auto_filter.ref = f"A3:O{LASTNEW}"
for dv in ws.data_validations.dataValidation:
    if "H4" in str(dv.sqref): dv.sqref = type(dv.sqref)(f"H4:H{LASTNEW}")
oldcf = ws.conditional_formatting; newcf = ConditionalFormattingList()
for cf in oldcf:
    rng = str(cf.sqref)
    m = re.fullmatch(r"([A-Z]+4):([A-Z]+)64", rng)
    if m: rng = f"{m.group(1)}:{m.group(2)}{LASTNEW}"
    for rule in cf.rules: newcf.add(rng, rule)
ws.conditional_formatting = newcf
a2 = ws["A2"].value
ws["A2"].value = a2.replace("61 cases", f"{LASTNEW - 3} cases") + " Version 4 adds the chain columns K to O: every case is a precondition for a later one."

# ---------- other sheets: dangling ids, gate, data row ----------
DEAD = re.compile(r"UAT-PAR-02(?:-[A-Z]\d)?|UAT-PAR-01-E1")
cleaned = 0
for name in ["Timeline", "Gates", "Test data", "Readiness", "Team"]:
    s = wb[name]
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value, str) and DEAD.search(c.value):
                v = DEAD.sub("", c.value)
                v = re.sub(r"(,\s*){2,}", ", ", v); v = re.sub(r",\s*(?=[.;)\n]|$)", "", v); v = re.sub(r"\(\s*,", "(", v); v = re.sub(r"^\s*,\s*", "", v); v = v.replace(" ,", ",")
                c.value = v; cleaned += 1
g = wb["Gates"]
for r in range(1, 30):
    if g.cell(r, 1).value == "G3" and "UAT-031-E1" not in str(g.cell(r, 5).value):
        g.cell(r, 5).value = str(g.cell(r, 5).value).rstrip(", ") + ", UAT-031-E1"
td = wb["Test data"]
lastd = max(r for r in range(4, 60) if td.cell(r, 1).value)
td["A2"].value = re.sub(r"^12 data sets", "13 data sets", td["A2"].value) if td["A2"].value else td["A2"].value
rd = lastd + 1
for col in range(1, 6): td.cell(rd, col)._style = copy.copy(td.cell(lastd, col)._style)
td.cell(rd, 1, "DATA-CHAIN")
td.cell(rd, 2, "One shared journey data set: three parents with five children, School A and School B, MOEFAS and SBFAS schemes, charges and an EA ledger by stage. See the one sheet Shared test data (every field value the automation types).")
td.cell(rd, 3, "Chan with every owner (proposed)")
td.cell(rd, 4, "Map every case to the child threads in Shared test data. A case that spends money or a charge takes its own child. A case that only reads may reuse any child. Record the opening balance before each run.")
td.cell(rd, 5, "Restore EA balances to the opening values of Shared test data through approved setup. Add new charges per round and never delete published ones. Clean test schemes by the cleanup script.")
td.row_dimensions[rd].height = 110

# ---------- new sheets ----------
F = Font(name="Arial", size=9); FB = Font(name="Arial", size=9, bold=True, color="FFFFFF")
HF = PatternFill("solid", fgColor="1F4E79"); thin = Side(style="thin", color="BFBFBF"); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
def put(sh, headers, rows, widths, start=1, title=None):
    r0 = start
    if title:
        sh.cell(r0, 1, title).font = Font(name="Arial", size=11, bold=True); r0 += 1
    for i, h in enumerate(headers, 1):
        c = sh.cell(r0, i, h); c.font = FB; c.fill = HF; c.border = BD; c.alignment = Alignment(wrap_text=True, vertical="center")
    for k, row in enumerate(rows, r0 + 1):
        mx = 1
        for i, v in enumerate(row, 1):
            c = sh.cell(k, i, v); c.font = F; c.border = BD; c.alignment = Alignment(wrap_text=True, vertical="top")
            mx = max(mx, heights(v if v is not None else "", widths[i - 1]))
        sh.row_dimensions[k].height = min(409, max(15, mx * 11.5))
    for i, w in enumerate(widths, 1): sh.column_dimensions[get_column_letter(i)].width = w
    return r0 + len(rows) + 2

ch = wb.create_sheet("Chain")
rows = []
for st in STAGES:
    ids = [x.strip() for x in (st[3] + (", " + st[5] if st[5] else "")).split(",")]
    rows.append((st[0], st[1], owners_of(st[0]), ", ".join(ids), len(ids), st[6], stagelist(UP[st[0]]), stagelist(DOWN[st[0]]) if DOWN[st[0]] else "End"))
rows.append(("Out", "View As and FAQ chatbot, not in this build", "Chan, Howard", "UAT-041, UAT-042, UAT-043, UAT-044", 4, "Not run now", "", ""))
put(ch, ["Stage", "What happens", "Owners", "Cases", "Count", "What the stage hands on", "Needs", "Needed by"], rows, [7, 38, 18, 60, 7, 48, 55, 55])
ch.freeze_panes = "C2"

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
many("PC", "1 People", "Parent persona C", "Singpass persona in the e-Service", [("Singpass NRIC", "S7654321B"), ("Children", "C5 Grace Pham"), ("FAS status", "Grace is a beneficiary of APP-01001 (Pham, status Submitted) in the dev pack. Check the host before relying on it")], "UAT-PAR-01-N4")
many("SCH-A", "1 People", "School A", "Existing school on the host", [("School name", "Rosyth Primary School"), ("School type", "Primary")], "All school scoped cases")
many("SCH-B", "1 People", "School B (created by the seed, UAT-PRE-04)", "Admin, School management, Create school (API POST /academic-resources/v1/schools)", [("MOE school code", "UATB01"), ("School name", "UAT-SEED School B"), ("School type", "GOVERNMENT (choices: GOVERNMENT, GOVERNMENT_AIDED, AUTONOMOUS, INDEPENDENT, SPECIALISED)"), ("School users", "Optional on the form. The seed links the user through the user call (MOE school code)"), ("Buttons", "Create school (Cancel to leave)")], "UAT-031, UAT-031-E1 wrong school controls", "Created by the seed (UAT-PRE-04), idempotent by the MOE school code. The portal form has no Academic levels field. A student with an EA at School B comes from the daily sync, which QA cannot start, so the cross school application variant stays Blocked until a child of another school is mapped. The dev pack also has Nanyang Primary School NYPS-0202 with a Primary 1 offering and no students.")
many("SCH-B-USER", "1 People", "School B user (created by the seed, UAT-PRE-04)", "Admin, School Users, Create school user, tab Single (API POST /users/v1/school-users/single)", [("NRIC", "S9000042Z"), ("First name", "UAT"), ("Last name", "SchoolB"), ("Email", "uat.schoolb@example.com"), ("MOE school code (optional)", "UATB01"), ("Password", "Never recorded in this file or in the seed log. After creating, open the user detail in Admin, School Users to see how the user logs in.")], "UAT-031, UAT-031-E1", "Without the login of this user the school side controls of UAT-031 stay Blocked. The suite does not sign in as this user yet.")
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
many("FEE-S100", "3 Fees", "Fee of 100.00 for Sophia (seeded)", "Same steps as FEE-100 (UAT-PRE-02)", [("Name", "UAT-SEED Fee S100 r{round}"), ("Price", "100.00 SGD"), ("Students", "Sophia"), ("Expected on UAT-033", "Gross 100.00, Subsidy 40.00, Amount due 60.00 only when the MOEFAS scheme covers this component with 40 percent. Today the scheme covers School Fee Term 1 and Standard Miscellaneous Fee at 100 percent, so this fee carries no subsidy until HQ adds it to the scheme (Admin, MOEFAS, Add fee).")], "UAT-033")

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
    ("Remarks", "UAT-SEED approval of seeded application"), ("Earliest day it can run", "1 Dec 2026 (MOEFAS effective date)"), ("Eligibility rule", "Read from the scheme detail at run time. The host showed Gross household income up to 5000.00 OR per capita income up to 1500.00 at the run of 31 Oct 2026 (dev pack: 4000.00 and 1000.00)"), ("HQ application screen", "Read only (no approve button)")], "UAT-PRE-03, UAT-031, UAT-033")

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

import json as _json
SD += [tuple(r) for r in _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "dev_seed_pack_rows.json"), encoding="utf-8"))]
sd = wb.create_sheet("Shared test data")
put(sd, ["Data ID", "Group", "Entity", "Where it is entered", "Field", "Value", "Used by cases", "Note"], SD, [14, 16, 34, 40, 38, 62, 36, 60])
sd.freeze_panes = "E2"
sd.auto_filter.ref = f"A1:H{len(SD) + 1}"


lg = wb.create_sheet("Change log v4")
put(lg, ["Area", "Change", "Reason"], [
 ("Tests, Gavin rows", "UAT-PAR-01, N3, A1, N4, E2, UAT-031, UAT-033 rewritten.", "Match the build (charges, receipt fields, payment in review) and remove overlap with Kent and Howard."),
 ("Tests, new row", f"UAT-031-E1 added (row {rowof['UAT-031-E1']}).", "No case covered the route from MOEFAS down to SBFAS."),
 ("Tests, columns K to O", "Stage, Chain order, Comes from, Hands on to, Shared data used added to every row.", "Every case is a precondition for a later case."),
 ("Tests, other owners", "Text not changed.", "Only Gavin's rows are in Gavin's scope."),
 ("Gates", f"Ten ids that no longer exist in Tests removed (UAT-PAR-02 family, UAT-PAR-01-E1). UAT-031-E1 added to G3. {cleaned} cells touched.", "Gates pointed to cases that were dropped."),
 ("Test data", "DATA-CHAIN added.", "One shared set so the cases can chain."),
 ("New sheets", "Chain, Shared test data (one sheet), Gavin overlap, Gavin vs build.", "Show the chain, the data and the reasons."),
 ("Open decisions", "UAT-031-E1 owner to be confirmed with Kent and Howard. UAT-033 pays net by EA only, the split payment stays in Howard UAT-045. DATA-CHAIN owner proposed as Chan.", "Need agreement before the pack is frozen."),
], [24, 90, 70])
put(wb.create_sheet("Gavin overlap"), ["Old Gavin case or step", "What it tested", "Overlaps with", "Decision"], OVERLAP, [30, 50, 60, 60])
put(wb.create_sheet("Gavin vs build"), ["Master says", "Build does", "How the new case handles it"], MISMATCH, [55, 80, 60])

wb.save(OUT)

bad = []
for c in CASES:
    for k in ("Test", "Setup", "Steps", "Watch", "In", "Out", "NotHere", "Change"):
        if re.search(r"[–—]| - ", c[k]): bad.append((c["ID"], k))
print("saved", OUT, "rows", LASTNEW, "dead id cells cleaned", cleaned, "dash problems", bad)
