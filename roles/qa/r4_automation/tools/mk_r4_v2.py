# -*- coding: utf-8 -*-
"""Builds the R4 defect file (BUG-R4-001..015 with evidence images) and extends the case workbook with the validation cases TC-268..TC-331.
Run from roles/qa:  python3 r4_automation/tools/mk_r4_v2.py
Needs: r4_automation/tools/mk_r4_defects_base.py (defects 001 to 006) and r4_automation/tools/r4_new_cases.py (the new cases)."""
import os, sys, re, math, shutil, textwrap, copy as _copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
base_src = open(os.path.join(HERE, "mk_r4_defects_base.py"), encoding="utf-8").read()
exec(base_src.split("# ------------------------------------------------ 1.")[0])   # imports, ENV, D (001..006), HDR, need_pt

import r4_new_cases as NC
from openpyxl.formula.translate import Translator
from openpyxl.formatting.formatting import ConditionalFormattingList
from openpyxl.worksheet.cell_range import MultiCellRange
from PIL import ImageDraw, ImageFont

WORK = "R4_Test_Cases.xlsx"
DEF_OUT = "R4_All_Defects_26-10-2026.xlsx"
BEFORE = "R4_Test_Cases_before_validation_cases_26-10.xlsx"

# --------------------------------------------------------------------------- evidence images (drawn from the captured text)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def card(path, title, panels, footer, width=640, fs=15):
    """panels: list of (heading, [lines], ok) where ok True=green, False=red, None=grey."""
    f = ImageFont.truetype(FONT, fs); fb = ImageFont.truetype(FONTB, fs)
    cw = f.getlength("M"); cols = int((width - 24) / cw)
    lh = fs + 6
    body = []
    for head, lines, ok in panels:
        wrapped = []
        for l in lines:
            wrapped += textwrap.wrap(l, cols - 2, subsequent_indent="  ", break_long_words=True) or [""]
        body.append((head, wrapped, ok))
    ft = textwrap.wrap(footer, cols)
    h = 40 + sum(lh * (len(w) + 1) + 14 for _, w, _ in body) + lh * len(ft) + 16
    im = Image.new("RGB", (width, h), "#F7F9FC"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, width, 30], fill="#1F3A5F"); d.text((10, 6), title[:cols], font=fb, fill="white")
    y = 40
    col = {True: "#0B6B2A", False: "#B00020", None: "#444444"}
    for head, wrapped, ok in body:
        d.text((10, y), head, font=fb, fill=col[ok]); y += lh
        for l in wrapped:
            d.text((18, y), l, font=f, fill="#111111"); y += lh
        y += 14
    for l in ft:
        d.text((10, y), l, font=f, fill="#666666"); y += lh
    im.save(path)

FOOT = "Drawn from the text captured on 26/10/2026 (built-in browser, localhost build). Not a screenshot."
SC = "School user school, Raffles Institution"
HQ = "MOE HQ user moehq"
IMG = {
 "evidence_10_BUG-R4-007.png": ("BUG-R4-007  SBFAS create, PCI on, pciFrom empty", [
   ("Request (" + SC + ")", ["POST /api/v1/fas/sbfas-schemes", "isPciEnabled: true, pciFrom: null, pciTo: 1000", "publish: false (other fields valid)"], None),
   ("Response", ["HTTP 201", "message: SBFAS scheme saved as draft."], False),
   ("Expected", ["HTTP 400  pciFrom is required when PCI is enabled."], True)], FOOT),
 "evidence_11_BUG-R4-007.png": ("BUG-R4-007  SBFAS create, GHI on, ghiFrom empty", [
   ("Request (" + SC + ")", ["POST /api/v1/fas/sbfas-schemes", "isGhiEnabled: true, ghiFrom: null, ghiTo: 100, incomeOperator: OR", "publish: false (other fields valid)"], None),
   ("Response", ["HTTP 201", "message: SBFAS scheme saved as draft."], False),
   ("Expected", ["HTTP 400  ghiFrom is required when GHI is enabled."], True)], FOOT),
 "evidence_12_BUG-R4-008.png": ("BUG-R4-008  Unknown fee component is accepted", [
   ("SBFAS create (" + SC + ")", ["feeComponentId: 00000000-0000-0000-0000-000000000099", "Response: HTTP 201 (saved)"], False),
   ("MOEFAS create (" + HQ + ")", ["subsidies[0].feeComponentId: 00000000-0000-0000-0000-000000000099", "Response: HTTP 201 MOE FAS scheme created successfully."], False),
   ("Expected", ["HTTP 400 or 404: the fee component does not exist"], True)], FOOT),
 "evidence_13_BUG-R4-008.png": ("BUG-R4-008  Unknown grade is accepted", [
   ("SBFAS create (" + SC + ")", ["items[0].academicLevelId: AL-NOPE", "Response: HTTP 201 (saved)"], False),
   ("SBFAS Add fee on a Published scheme", ["POST /api/v1/fas/sbfas-schemes/{id}/fee-components", "items[0].academicLevelId: AL-NOPE", "Response: HTTP 201 (saved)"], False),
   ("Expected", ["HTTP 400 or 404: the grade is not offered by the school"], True)], FOOT),
 "evidence_14_BUG-R4-009.png": ("BUG-R4-009  A grade without a value is accepted", [
   ("Request (" + SC + ")", ["School grades: Junior College 1, Secondary 1", "feeComponents[0].items: Junior College 1 only (10 percent)"], None),
   ("Response", ["HTTP 201 (saved as draft)"], False),
   ("Expected", ["HTTP 400: every active grade needs a value (VR-WIZ-17)", "The wizard blocks it: Enter a subsidy percentage for every active level."], True)], FOOT),
 "evidence_15_BUG-R4-010.png": ("BUG-R4-010  MOEFAS accepts dates in the past", [
   ("MOEFAS create (" + HQ + ")", ["openFrom 2020-01-01, openTo 2020-06-30, effectiveFrom 2021-01-01", "Response: HTTP 201 MOE FAS scheme created successfully."], False),
   ("SBFAS create with past dates (" + SC + ")", ["openFrom yesterday (UTC)", "Response: HTTP 400 openFrom must be today or later."], True)], FOOT),
 "evidence_16_BUG-R4-011.png": ("BUG-R4-011  Same name, later period is refused", [
   ("Step 1", ["Published scheme R4-AUTO-succ, Effective from year Y"], None),
   ("Step 2: same name, Effective from year Y + 5 (" + SC + ")", ["Response: HTTP 409", "A scheme with this name already exists for this school."], False),
   ("Expected (FS 7.3, VR-PUB-07)", ["The later scheme is accepted. The earlier scheme gets Effective to = the day before the new Effective from."], True)], FOOT),
 "evidence_17_BUG-R4-012.png": ("BUG-R4-012  SBFAS list row (School user)", [
   ("Row text read from the screen", ["qqq SBF-00002", "Singapore citizen · GHI ≤ S$1,000.00 OR PCI ≤ S$1,000.00", "2026-10-23 – 2026-10-24    2026-10-30 – 2027-01-28", "Application closed    3"], False),
   ("Expected (FS 7.1 and case book TC-173)", ["Dates as DD/MM/YYYY, the text Approved by school, Open badge and No end date text"], True)], FOOT),
 "evidence_18_BUG-R4-013.png": ("BUG-R4-013  School user can read MOEFAS schemes", [
   ("School user (" + SC + ")", ["GET /api/fas/v1/fas/moe-schemes  ->  HTTP 200, 80 rows", "GET /api/fas/v1/fas/moe-schemes/{id}  ->  HTTP 200", "POST /api/fas/v1/fas/moe-schemes  ->  HTTP 403"], False),
   ("Contrast", ["MOE HQ calling GET /api/v1/fas/sbfas-schemes  ->  HTTP 403", "No session, GET moe-schemes and sbfas-schemes  ->  HTTP 401"], True),
   ("Expected", ["HTTP 403 for the School user on every MOEFAS endpoint"], True)], FOOT),
 "evidence_19_BUG-R4-014.png": ("BUG-R4-014  Misleading wizard messages", [
   ("Step General, Total budget", ["abc  ->  Budget cannot be negative.", "empty  ->  Budget cannot be negative.", "-1  ->  Budget cannot be negative.  (correct)"], False),
   ("Step Subsidy, percentage cells", ["-1, 101 or empty  ->  Enter a subsidy percentage for every active level.", "(no range 0 to 100 named)"], False),
   ("Expected", ["A message for each cause: a number is needed; the percentage must be from 0 to 100"], True)], FOOT),
 "evidence_21_BUG-R4-016.png": ("BUG-R4-016  MOEFAS list is not sorted by Effective from", [
   ("GET /api/fas/v1/fas/moe-schemes, " + HQ + ", 95 rows, Effective from year in response order", ["2527, 2527, 2527, 2509, 2431, 2427, 2423, 2419, 2415, 2411, 2407, 2403, 2399, 2387, 2377, 3401, 3401, 3293, 3285, 3221, 3209, 2217, 2213, 2207 ... 2028, 2027, 2026-10-22, 2026-10-01"], False),
   ("Expected (FS 7.1 item 5)", ["Effective from newest first, then by name: 3401, 3401, 3293, 3285 ... 2527 ... 2026-10-01"], True)], FOOT),
 "evidence_20_BUG-R4-015.png": ("BUG-R4-015  Duplicate name hides the reason", [
   ("Wizard, Save draft or Publish with an existing name", ["Toast: Unable to create scheme", "The scheme could not be created. Please try again."], False),
   ("Same request through the API", ["HTTP 409  A scheme with this name already exists for this school."], None),
   ("Expected", ["The screen shows that the name already exists, so the user can change it"], True)], FOOT),
}
for n, (t, p, f_) in IMG.items():
    card(os.path.join(EV, n), t, p, f_)

for dct in D:
    if dct["id"] == "BUG-R4-002": dct["tcs"] = "TC-206, TC-301"
    if dct["id"] == "BUG-R4-003": dct["tcs"] = "TC-219, TC-220, TC-225"

ENV_SB = ("SIT (Local QA Stack)\nAdmin portal: http://localhost:5173\nAPI gateway: http://localhost:5273\n"
          "User: school (School Admin, Raffles Institution), seed password of the IAM seed\nBuilt-in browser, requests sent with fetch through the admin portal proxy\n"
          "Build: local branch codesprint2ending, run of 26/10/2026")
ENV_HQ = ENV_SB.replace("User: school (School Admin, Raffles Institution)", "User: moehq (MOE HQ)")
ENV_MIX = ENV_SB.replace("User: school (School Admin, Raffles Institution)", "Users: school (School Admin) and moehq (MOE HQ)")
def bug(id_, summary, sev, pri, typ, env, pre, steps, exp, act, tcs, imgs, notes):
    D.append(dict(id=id_, summary=summary, sev=sev, pri=pri, status="Open", typ=typ, env=env, pre=pre, steps=steps, exp=exp, act=act, tcs=tcs, imgs=imgs, notes=notes))

bug("BUG-R4-007", "[SBFAS API] PCI From and GHI From are not required when their band is on", "S3", "Medium", "Functional", ENV_SB,
    "Signed in as school. The school has two active grades and at least one active fee component.",
    "1. Sign in as school.\n2. Send POST /api/v1/fas/sbfas-schemes with a valid body, isPciEnabled true, pciFrom null and pciTo 1000.\n3. Repeat with isGhiEnabled true, ghiFrom null, ghiTo 100 and incomeOperator OR.",
    "Both requests are refused with 400: pciFrom is required when PCI is enabled. / ghiFrom is required when GHI is enabled.",
    "Both requests are accepted (HTTP 201) and the scheme is saved as a draft. The wizard blocks an empty From (Enter a value of zero or more.), only a direct API call gets through.",
    "TC-277, TC-278", [("evidence_10_BUG-R4-007.png", "TC-277, pciFrom empty"), ("evidence_11_BUG-R4-007.png", "TC-278, ghiFrom empty")],
    "Root cause (code): CreateSbfasSchemeValidator has the rule NotNull for pciFrom and ghiFrom, but it sits in the same chain as the When(HasValue) condition, so it never runs. Dev to move the NotNull check out of that condition. The same check for the band To is correctly optional. Automated tests: test_tc_277 and test_tc_278, marked known_defect (xfail).")
bug("BUG-R4-008", "[SBFAS and MOEFAS API] A fee component or a grade that does not exist is accepted", "S2", "High", "Functional", ENV_MIX,
    "Signed in as school (SBFAS) or moehq (MOEFAS). A Published SBFAS scheme exists for the Add fee request.",
    "1. Send POST /api/v1/fas/sbfas-schemes with feeComponentId 00000000-0000-0000-0000-000000000099.\n2. Send POST /api/fas/v1/fas/moe-schemes (as moehq) with the same unknown feeComponentId.\n3. Send POST /api/v1/fas/sbfas-schemes with academicLevelId AL-NOPE.\n4. On a Published SBFAS scheme send POST fee-components with an unknown feeComponentId, then with academicLevelId AL-NOPE.",
    "Each request is refused with 400 or 404 and a message that the fee component or the grade does not exist. Nothing is saved.",
    "All requests are accepted (HTTP 201) and the unknown ids are stored with the scheme, also on a Published scheme.",
    "TC-286, TC-287, TC-292", [("evidence_12_BUG-R4-008.png", "TC-286, unknown fee component"), ("evidence_13_BUG-R4-008.png", "TC-287 and TC-292, unknown grade")],
    "The wizard offers only existing fees and grades, so the user cannot send these values from the screen. The risk is a direct API call or a stale screen. Dev to check the ids against the fee components of Function 3 and the offerings of the school before saving. Automated tests: test_tc_286, test_tc_287 and test_tc_292, marked known_defect (xfail).")
bug("BUG-R4-009", "[SBFAS API] A scheme that leaves one grade without a value is accepted", "S3", "Medium", "Functional", ENV_SB,
    "Signed in as school. The school has two active grades (Junior College 1 and Secondary 1).",
    "1. Sign in as school.\n2. Send POST /api/v1/fas/sbfas-schemes with one fee component that has an item for Junior College 1 only.",
    "The request is refused: every active grade needs a value, 0 percent if there is no subsidy (rules document VR-WIZ-17).",
    "The request is accepted (HTTP 201). The scheme prices one grade only. The wizard blocks it with Enter a subsidy percentage for every active level.",
    "TC-288", [("evidence_14_BUG-R4-009.png", "TC-288, one grade of two")],
    "Dev to confirm whether a missing grade means no subsidy for that grade or an error. The rules document says every grade needs a value. Automated test: test_tc_288, marked known_defect (xfail).")
bug("BUG-R4-010", "[MOEFAS API] A scheme with all dates in the past is accepted, SBFAS refuses the same", "S3", "Medium", "Functional", ENV_HQ,
    "Signed in as moehq. At least one active fee component of Function 3 exists.",
    "1. Sign in as moehq.\n2. Send POST /api/fas/v1/fas/moe-schemes with Form opens 2020-01-01, Form closes 2020-06-30 and Effective from 2021-01-01.",
    "The request is refused: a new scheme cannot start in the past, as the SBFAS API does (openFrom must be today or later).",
    "The request is accepted (HTTP 201 MOE FAS scheme created successfully.).",
    "TC-295", [("evidence_15_BUG-R4-010.png", "TC-295, MOEFAS 2020 accepted, SBFAS refused")],
    "The rules document VR-WIZ-08 says Effective from must not be in the past for a new scheme. BA to confirm the rule for MOEFAS. Automated test: test_tc_295, marked known_defect (xfail). The test schemes are Drafts named R4-AUTO and stay until the cleanup command.")
bug("BUG-R4-011", "[SBFAS publish] A later scheme with the same name is refused, so the earlier scheme is never ended", "S2", "High", "Functional", ENV_SB,
    "Signed in as school. A Published SBFAS scheme named X exists with Effective from in year Y.",
    "1. Sign in as school.\n2. Create and publish a scheme with the same name X and Effective from five years later.\n3. Read the list.",
    "The later scheme is accepted. The earlier scheme gets Effective to = the day before the new Effective from (FS 7.3, rules document VR-PUB-07).",
    "The request is refused with HTTP 409: A scheme with this name already exists for this school. The earlier scheme keeps no end date.",
    "TC-228", [("evidence_16_BUG-R4-011.png", "TC-228, same name later period")],
    "Root cause (code): the create handler checks the name in the school without looking at the period. TC-226 and TC-227 depend on the same rule and stay Not Run. TC-222 and TC-223 pass. Automated test: test_tc_228, marked known_defect (xfail). BA and Dev to confirm the succession rule.")
bug("BUG-R4-012", "[SBFAS list] Dates and row content differ from the FS and the final prototype", "S3", "Medium", "UI", ENV_SB,
    "Signed in as school. The school has at least one SBFAS scheme.",
    "1. Sign in as school.\n2. Open SBFAS schemes.\n3. Read the date columns and the text under the scheme name.",
    "Dates as DD/MM/YYYY (BR13), the text Approved by school under the name, the Open badge and No end date when Effective to is empty (case book TC-173).",
    "Dates are shown as YYYY-MM-DD (2026-10-23 – 2026-10-24). There is no Approved by school text, no Open badge and no No end date text.",
    "TC-173", [("evidence_17_BUG-R4-012.png", "TC-173, list row")],
    "Counts, status and fee count match the API. The difference is the format and the extra texts. BA to decide whether the build or the case book changes. Reject this defect if the build is accepted. Automated test: test_tc_173, marked known_defect (xfail).")
bug("BUG-R4-013", "[MOEFAS API] The School user can read all MOEFAS schemes", "S2", "High", "Security", ENV_SB,
    "Signed in as school (role SCHOOL).",
    "1. Sign in as school.\n2. Send GET /api/fas/v1/fas/moe-schemes.\n3. Send GET /api/fas/v1/fas/moe-schemes/{id} for one scheme.\n4. Send POST /api/fas/v1/fas/moe-schemes.",
    "403 Forbidden on every MOEFAS endpoint. MOEFAS is for MOE HQ only (FS 3.2, case book TC-165).",
    "GET list returns 200 with 80 rows. GET of one scheme returns 200. Only POST is refused (403). The menu hides MOEFAS from the school, the API does not. MOE HQ calling the SBFAS list gets 403 correctly.",
    "TC-165", [("evidence_18_BUG-R4-013.png", "TC-165, School user reads MOEFAS")],
    "The data are scheme definitions (names, bands, subsidy), no student data. Still an access control gap: Dev to add the role check on the MOEFAS read endpoints. Automated test: test_tc_165, marked known_defect (xfail).")
bug("BUG-R4-014", "[SBFAS wizard] Misleading messages for the budget and the percentage cells", "S4", "Low", "UI", ENV_SB,
    "Signed in as school.",
    "1. Open SBFAS schemes, click New scheme and fill the dates.\n2. Type abc, then leave empty, then -1 in Total budget and click Next.\n3. On Subsidy pick a fee, type -1, then 101, then clear the cell, and click Review.",
    "A message for each cause: a number is needed for abc and empty, the percentage must be from 0 to 100 for the cells (rules document VR-WIZ-15).",
    "abc and empty show Budget cannot be negative. The cells with -1, 101 or empty show Enter a subsidy percentage for every active level., which does not name the range. The values are blocked correctly.",
    "TC-307, TC-309", [("evidence_19_BUG-R4-014.png", "TC-307 and TC-309, messages")],
    "Only the text is wrong, the blocking works. Automated tests: test_tc_307 and test_tc_309, marked known_defect (xfail).")
bug("BUG-R4-015", "[SBFAS wizard] A duplicate scheme name shows a generic error", "S3", "Medium", "Usability", ENV_SB,
    "Signed in as school. A scheme named X exists for the school.",
    "1. Sign in as school.\n2. Complete the four steps of a new scheme with the name X.\n3. Click Save draft, then click Publish.",
    "The screen says that a scheme with this name already exists so the user can change the name (rules document VR-WIZ-03).",
    "The toast says Unable to create scheme. The scheme could not be created. Please try again. The API answers 409 A scheme with this name already exists for this school., the screen does not show it.",
    "TC-310", [("evidence_20_BUG-R4-015.png", "TC-310, toast and API answer")],
    "The scheme is correctly not created. The user cannot tell why. Automated test: test_tc_310, marked known_defect (xfail).")

bug("BUG-R4-016", "[MOEFAS list] Schemes are not sorted by Effective from, newest first", "S3", "Medium", "Functional", ENV_HQ,
    "Signed in as moehq. The stack holds more than 20 schemes with different Effective from dates.",
    "1. Sign in as moehq.\n2. Open MOEFAS and read the column Effective from from top to bottom (or send GET /api/fas/v1/fas/moe-schemes).",
    "Rows sorted by Effective from, newest first, then by name (FS 7.1 item 5, case TC-174).",
    "The rows come in creation order: runs of Published and Draft schemes alternate and the years jump (2527, 2509 ... 2377, then 3401, 3293 ... 2217, then 2207 ... ). The first rows are not the newest Effective from.",
    "TC-174", [("evidence_21_BUG-R4-016.png", "TC-174, order of the response")],
    "Found by the automated run of 26/10/2026: TC-174 passed while the stack had a few schemes and failed after the validation tests created more. The MOEFAS list code has no sort control, the order is the one the API returns. Automated test: test_tc_174, marked known_defect (xfail).")

def row_values(d, evidence_text):
    return [d["id"], d["summary"], d["sev"], d["pri"], d["status"], d["typ"], d.get("env", ENV), d["pre"], d["steps"], d["exp"], d["act"], d["tcs"], evidence_text, d["notes"]]

TEMPLATE = WORK
# --------------------------------------------------------------------------- 1. standalone defect file with images in the same sheet
wb = openpyxl.load_workbook(TEMPLATE)
for n in wb.sheetnames:
    if n != "Defect Reports": del wb[n]
ws = wb["Defect Reports"]
for r in range(2, ws.max_row + 1):
    for c in range(1, 15): ws.cell(r, c).value = None
ws._images = []
ws.column_dimensions["M"].width = 54
widths = [(ws.column_dimensions[c].width or 13) for c in "ABCDEFGHIJKLMN"]
for i, d in enumerate(D):
    r = i + 2
    ev = "\n".join(["The images are embedded below in this cell. Files:"] + [f"{n}  ({cap})" for n, cap in d["imgs"]])
    vals = row_values(d, ev)
    for c, v in enumerate(vals, 1): ws.cell(r, c).value = v
    if r > 7:   # copy the style of row 2 for the new rows
        for c in range(1, 15):
            s, t = ws.cell(2, c), ws.cell(r, c)
            t.font = _copy.copy(s.font); t.fill = _copy.copy(s.fill); t.border = _copy.copy(s.border); t.alignment = _copy.copy(s.alignment); t.number_format = s.number_format
    text_px = max(int((len(d["imgs"]) + 1) * 3.6 * 14.5 / 0.75 * 0.28) + 34, 72)
    sizes = [Image.open(os.path.join(EV, n)).size for n, _ in d["imgs"]]
    tw = 372
    while True:
        hs = [int(tw * h0 / w0) for (w0, h0) in sizes]
        total = text_px + sum(h + 6 for h in hs)
        if total <= 540 or tw <= 240: break
        tw -= 12
    y = text_px
    for (n, cap), h in zip(d["imgs"], hs):
        im = XLImage(os.path.join(EV, n)); im.width, im.height = tw, h
        im.anchor = OneCellAnchor(_from=AnchorMarker(col=12, row=r - 1, colOff=pixels_to_EMU(6), rowOff=pixels_to_EMU(y)),
                                  ext=XDRPositiveSize2D(pixels_to_EMU(tw), pixels_to_EMU(h)))
        ws.add_image(im); y += h + 6
    h_img = y * 0.75 + 6
    ws.row_dimensions[r].height = min(409, max(h_img, need_pt(vals, widths)))
    if h_img > 409: print("WARN image area exceeds 409pt for", d["id"], round(h_img))
ws.freeze_panes = "B2"
wb.save(DEF_OUT); print("saved", DEF_OUT, len(D), "defects")

# --------------------------------------------------------------------------- 2. case workbook
# one file only: no backup copy is made (rule of 26/10/2026)
wb = openpyxl.load_workbook(WORK)
ws = wb["Test cases "]
col = {c.value: i for i, c in enumerate(ws[1])}
RUN_MAN = "Run 26/10/2026 (manual run in the built-in browser and through the API, localhost build). "
OLD_LAST = ws.max_row
assert OLD_LAST in (268, 332), OLD_LAST
extended = OLD_LAST == 332

# 2a. status of the older cases
by_id = {}
for row in ws.iter_rows(min_row=2):
    by_id[row[0].value] = row
for k, (status, actual, defect) in NC.U.items():
    row = by_id["TC-" + k]
    row[col["Execution Status"]].value = status
    row[col["Actual Result"]].value = RUN_MAN + actual
    if defect: row[col["Defect ID"]].value = defect
if True:   # the cases run by the earlier automation keep their text; nothing else changes

    pass

if not extended:
    # 2b. new rows
    widths = [ws.column_dimensions[c.column_letter].width or 13 for c in ws[1]]
    tmpl = ws[OLD_LAST]
    rows_new = []
    for i, t in enumerate(NC.N):
        suite, ts, title, page, sev, pri, typ, env, pre, data, steps, exp, status, actual, defect, trace, note = t
        tid = f"TC-{268 + i:03d}"
        vals = [tid, ts, title, suite, page, sev, pri, status, typ, env, pre, data, steps, exp, actual, "N/A", defect, trace, note, "Approve"]
        r = OLD_LAST + 1 + i
        for c, v in enumerate(vals):
            cell = ws.cell(r, c + 1); cell.value = v
            s = tmpl[c]
            cell.font = _copy.copy(s.font); cell.fill = _copy.copy(s.fill); cell.border = _copy.copy(s.border); cell.alignment = _copy.copy(s.alignment); cell.number_format = s.number_format
        ws.row_dimensions[r].height = min(409, max(106.5, need_pt(vals, widths)))
        rows_new.append(vals)
    LAST = OLD_LAST + len(NC.N)          # 332
    assert LAST == 332, LAST

    # 2c. ranges: data validations, conditional formats, filter
    for dv in ws.data_validations.dataValidation:
        dv.sqref = MultiCellRange(str(dv.sqref).replace("268", str(LAST)))
    cfl = ConditionalFormattingList()
    for cf in ws.conditional_formatting:
        rng = str(cf.sqref).replace("268", str(LAST))
        for rule in cf.rules: cfl.add(rng, rule)
    ws.conditional_formatting = cfl
    ws.auto_filter.ref = f"A1:T{LAST}"

    # 2d. scenarios
    sc = wb["Scenarios"]
    SC_ROWS = [
     ("TS-057", "F4.14 New scheme wizard", "SBFAS general step: name, dates and budget", "The SBFAS name, the four dates and the budget follow the validation rules, in the API and in the wizard.", "Boundary value analysis", "Rules document VR-WIZ-01 to 08, FS 7.3"),
     ("TS-058", "F4.14 New scheme wizard", "SBFAS eligibility: nationality and income bands", "Nationality, GHI and PCI bands, the match rule and the scheme context follow the validation rules.", "Boundary value analysis", "Rules document VR-WIZ-09 to 13, FS 7.2 step 2"),
     ("TS-059", "F4.14 New scheme wizard", "SBFAS subsidy: fee components, grades and percentages", "Fee components, grades and percentages (0 to 100, two decimals) are checked in the API and in the wizard.", "Boundary value analysis", "Rules document VR-WIZ-14, 15, 17, FS 7.2 step 3"),
     ("TS-060", "F4.14 New scheme wizard", "MOEFAS wizard validation", "The MOEFAS API and wizard apply the name, date, eligibility, subsidy and budget rules.", "Boundary value analysis", "Rules document VR-WIZ-01 to 15, FS 7.3"),
     ("TS-061", "F4.16 Add fee to a published scheme", "Add fee validation", "The Add fee request and dialog refuse wrong percentages, repeated grades and fees already in the scheme.", "Boundary value analysis", "Rules document VR-FEE-03, VR-FEE-04, FS 7.4"),
     ("TS-062", "F4.5 Filters and search", "Search box text handling", "The search box trims spaces, removes control characters and treats special text as plain text.", "Error guessing", "Rules document, search box (A4, B4)"),
     ("TS-063", "F4.9 Approve SBFAS", "Approve comment text handling", "The approve comment is limited to 500 characters, trimmed, cleaned and kept as plain text.", "Error guessing", "Rules document, approve comment (E2, F2)"),
     ("TS-064", "F4.10 Reject SBFAS", "Reject comment text handling", "The reject comment is required, limited to 500 characters, cleaned and safe in the export.", "Error guessing", "Rules document, reject comment (G2)"),
     ("TS-065", "F4.9 Approve SBFAS", "Shared messages", "The shared messages of the approve and reject dialogs and of failures appear with the specified wording.", "Equivalence partitioning", "Rules document, shared messages (section 15)"),
    ]
    src_row = sc.max_row
    assert sc.cell(src_row, 1).value == "TS-056", sc.cell(src_row, 1).value
    for i, vals in enumerate(SC_ROWS):
        r = src_row + 1 + i
        for c in range(1, 12):
            s, t = sc.cell(src_row, c), sc.cell(r, c)
            t.font = _copy.copy(s.font); t.fill = _copy.copy(s.fill); t.border = _copy.copy(s.border); t.alignment = _copy.copy(s.alignment); t.number_format = s.number_format
            if c <= 6: t.value = vals[c - 1]
            else: t.value = Translator(s.value, origin=s.coordinate).translate_formula(t.coordinate)
        sc.row_dimensions[r].height = sc.row_dimensions[src_row].height
    SC_LAST = src_row + len(SC_ROWS)

    def retarget(v):
        return v.replace("$268", f"${LAST}") if isinstance(v, str) and v.startswith("=") else v
    for w in wb:
        for row in w.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    nv = c.value.replace("$B$268", f"$B${LAST}").replace("$268", f"${LAST}")
                    if w.title == "Scenarios": pass
                    c.value = nv
    sm = wb["Summary"]
    sm["B8"].value = f"=COUNTA(Scenarios!$A$2:$A${SC_LAST})"
    for dv in sc.data_validations.dataValidation:
        dv.sqref = MultiCellRange(str(dv.sqref).replace("57", str(SC_LAST)))

    # 2e. FS Trace
    ft = wb["FS Trace"]
    last = ft.max_row
    for i, (item, stmt, tcs) in enumerate(NC.VR):
        r = last + 1 + i
        for c in range(1, 7):
            s, t = ft.cell(last, c), ft.cell(r, c)
            t.font = _copy.copy(s.font); t.fill = _copy.copy(s.fill); t.border = _copy.copy(s.border); t.alignment = _copy.copy(s.alignment); t.number_format = s.number_format
        ft.cell(r, 1).value = item; ft.cell(r, 2).value = "Validation rule"; ft.cell(r, 3).value = stmt; ft.cell(r, 4).value = tcs
        ft.cell(r, 5).value = Translator(ft.cell(last, 5).value, origin=ft.cell(last, 5).coordinate).translate_formula(ft.cell(r, 5).coordinate)
        ft.cell(r, 6).value = Translator(ft.cell(last, 6).value, origin=ft.cell(last, 6).coordinate).translate_formula(ft.cell(r, 6).coordinate)
        ft.row_dimensions[r].height = ft.row_dimensions[last].height
    if ft.auto_filter.ref: ft.auto_filter.ref = f"A1:F{last + len(NC.VR)}"

LAST = 332

# 2f. Defect Reports sheet of the case workbook
wd = wb["Defect Reports"]
wdw = [(wd.column_dimensions[c].width or 13) for c in "ABCDEFGHIJKLMN"]
for i, d in enumerate(D):
    r = i + 2
    vals = row_values(d, f"See {DEF_OUT}, sheet Defect Reports, column Evidence (images embedded).\n" + "\n".join(n for n, _ in d["imgs"]))
    for c, v in enumerate(vals, 1):
        cell = wd.cell(r, c); cell.value = v
        if r > 7:
            s = wd.cell(2, c)
            cell.font = _copy.copy(s.font); cell.fill = _copy.copy(s.fill); cell.border = _copy.copy(s.border); cell.alignment = _copy.copy(s.alignment); cell.number_format = s.number_format
    wd.row_dimensions[r].height = min(409, need_pt(vals, wdw))

# 2g. counts and text
sm = wb["Summary"]
cnt = {"Passed": 0, "Failed": 0, "Not Run": 0, "Blocked": 0}
for row in ws.iter_rows(min_row=2, max_row=LAST):
    cnt[row[col["Execution Status"]].value] += 1
total = sum(cnt.values())
if "Cases TC-268" not in sm["A2"].value:
    sm["A2"].value = sm["A2"].value + " Cases TC-268 to TC-331 cover the validation rules of the schemes wizard, the Add fee dialog, the search box and the approve and reject comments (R4_FAS_Validation_Rules_EN.docx)."
sm["A76"].value = ("Execution Status was updated after the run of 26/10/2026 on the localhost build. Cases that were not run stay Not Run with an empty Actual Result. "
                   "Defect ID is filled for every Failed case. Run with .\\run_r4_automation.cmd to repeat the cases that have a test.")
if "Exception: the rules" not in sm["A84"].value:
    sm["A84"].value = (sm["A84"].value + " Exception: the rules for the schemes wizard, Add fee, the search box and the comments in R4_FAS_Validation_Rules_EN.docx still hold, and cases TC-268 to TC-331 cover them.")
sm["A85"].value = (f"{total} cases after the run of 26/10/2026 on the localhost build: {cnt['Passed']} Passed, {cnt['Failed']} Failed and {cnt['Not Run']} Not Run. "
                   "The Not Run cases test the FAS applications list, the review drawer, the approve and reject dialogs, the decision engine, the export and the email, "
                   "which the localhost build does not contain yet, or need a controllable clock or failing requests (ENV-R4-02 to ENV-R4-04). They run when those items exist.")
for r in (76, 85, 84, 2):
    sm.row_dimensions[r].height = max(sm.row_dimensions[r].height or 15, 15 * math.ceil(len(sm.cell(r, 1).value) / 150))
try:
    wb.save(WORK); print("updated", WORK, cnt, "total", total)
except PermissionError:
    alt = WORK.replace(".xlsx", "_v2.xlsx"); wb.save(alt); print("LOCKED, saved", alt, cnt, "total", total)
