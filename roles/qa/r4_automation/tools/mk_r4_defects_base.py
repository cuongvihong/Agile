import openpyxl, shutil, math, copy, os, sys
from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU
from PIL import Image

SRC="R4_Test_Cases.xlsx"
EV="R4_Defects_Evidence_26-10-2026"
ENV=("SIT (Local QA Stack)\nAdmin portal: http://localhost:5173\nAPI gateway: http://localhost:5273\n"
     "User: moehq (MOE HQ), seed password of the IAM seed\nChrome (Playwright, locale en-US)\n"
     "Build: local branch codesprint2ending, automated run of 26/10/2026")
D=[
dict(id="BUG-R4-001",
 summary="[MOEFAS wizard step Subsidy and Add fee page] The percentage error shows a raw message key instead of text",
 sev="S3",pri="Medium",status="Open",typ="UI",
 pre="Signed in as moehq. At least one active fee component of Function 3 exists. For the Add fee page, a Draft or Published MOEFAS scheme exists.",
 steps=("1. Sign in to the admin portal as moehq.\n2. Open MOEFAS and click New scheme.\n3. Fill General (name, Form opens, Form closes, Effective from, total budget) and click Next.\n"
        "4. On Eligibility keep the defaults and click Next.\n5. On Subsidy click Fee Components, tick one component and apply.\n"
        "6. Type 101 (or -1) in the Primary cell and read the red line under the table.\n"
        "7. Repeat on the Add fee page: MOEFAS list, row menu, Add fees, pick a new component, type 101 in a new cell."),
 exp="A readable message that names the range, for example a percentage from 0 to 100. Next (and Confirm on the Add fee page) stays blocked.",
 act=("The red line shows the raw key features.moeHqMoeFasCreate.errors.amountRange on both screens. "
      "Next and Confirm are blocked correctly, only the text is wrong."),
 tcs="TC-205, TC-234",
 imgs=[("evidence_01_BUG-R4-001.png","TC-205, New scheme, Subsidy step, value 101"),("evidence_02_BUG-R4-001.png","TC-234, Add fee page, value 101")],
 notes=("Root cause (code): SubsidyMatrix.tsx and lib/validation.ts use the key errors.amountRange, but resource.ts defines only errors.amountInvalid, so the text is missing. "
        "Automated tests: test_tc_205 (values -1 and 101) and test_tc_234b, both marked known_defect (xfail). Remove the mark when fixed. "
        "Dev to confirm the intended wording and add the key in English and Vietnamese. Run video: r4_automation/artifacts/videos/TC-205.webm and TC-234.webm.")),
dict(id="BUG-R4-002",
 summary="[MOEFAS wizard step Subsidy] A percentage with three decimals is accepted",
 sev="S3",pri="Low",status="Open",typ="Functional",
 pre="Signed in as moehq. At least one active fee component of Function 3 exists.",
 steps=("1. Sign in to the admin portal as moehq.\n2. Open MOEFAS, click New scheme, fill General and Eligibility, click Next twice.\n"
        "3. On Subsidy pick one fee component.\n4. Type 33.33 in the Primary cell, then change it to 33.333.\n5. Read the message under the table and the state of Next."),
 exp="33.33 is valid. 33.333 shows an error for that cell because only two decimals are allowed.",
 act="33.333 is accepted. The green box says All amounts are valid and Next stays enabled, so a value with three decimals can be saved.",
 tcs="TC-206",
 imgs=[("evidence_03_BUG-R4-002.png","TC-206, Subsidy step, value 33.333")],
 notes=("Root cause (code): isAmountInvalid in lib/validation.ts checks only 0 to 100, there is no decimal limit. The case book note says the prototype behaves the same (candidate finding S4). "
        "Dev to confirm what the backend stores (column precision), because the value may be rounded without notice. "
        "Automated test: test_tc_206, marked known_defect (xfail). Run video: r4_automation/artifacts/videos/TC-206.webm.")),
dict(id="BUG-R4-003",
 summary="[MOEFAS publish] Two Published schemes can have the same effective period or the same form period",
 sev="S1",pri="High",status="Open",typ="Functional",
 pre="Signed in as moehq. At least one active fee component of Function 3 exists. Use far future dates so that no real scheme is touched.",
 steps=("1. Sign in to the admin portal as moehq.\n2. Create scheme A and Publish it: Form 01/01/2176 to 30/06/2176, Effective 01/01/2177 to 31/12/2177.\n"
        "3. Create scheme B with the same Form and Effective periods and Publish it.\n"
        "4. Create scheme C with the same Form period as A but Effective 01/01/2182 to 31/12/2182 and Publish it.\n5. Open the MOEFAS list."),
 exp=("B is blocked with a message that names A and the overlapping dates (case book TC-219: The period overlaps with A, change Effective from / Effective to). "
      "C is blocked with the form period message (TC-220). No overlapping scheme is added."),
 act="B and C are accepted and every scheme is Published. No overlap message is returned, so two Published schemes cover the same period.",
 tcs="TC-219, TC-220",
 imgs=[("evidence_04_BUG-R4-003.png","TC-219, same effective period"),("evidence_05_BUG-R4-003.png","TC-220, same form period")],
 notes=("Root cause (code): CreateMOEFASSchemeHandler and its validator in FASService check only the name. The front end validation.ts has a TODO for the overlap. "
        "The automated tests create the schemes through the API, so the evidence images are drawn from the GET moe-schemes data of the run (not UI screenshots). "
        "Not yet covered: TC-221 part 2, TC-225 to TC-227 depend on the same rule. Test data of the run (names R4-AUTO) stays in the stack until the cleanup command. "
        "Automated tests: test_tc_219 and test_tc_220, marked known_defect (xfail). BA and Dev to confirm the overlap rule.")),
]

D.extend([
dict(id="BUG-R4-004",
 summary="[MOEFAS wizard and Add fee] No success message after Draft, Publish or Confirm",
 sev="S3",pri="Medium",status="Open",typ="Usability",
 pre="Signed in as moehq. At least one active fee component of Function 3 exists.",
 steps=("1. Sign in to the admin portal as moehq.\n2. Open MOEFAS, click New scheme and complete the four steps.\n3. Click Draft and look at the list.\n"
        "4. Open the new scheme from the row menu (View), or create a second scheme, and click Publish.\n5. Open a Draft scheme, Add fees, pick a component, click Confirm and look at the detail page."),
 exp="A toast confirms each action: Draft saved. / Scheme published. It is now view-only. / Fee components added to the scheme. (case book TC-210, TC-215, TC-236)",
 act="No message is shown. The portal only moves to the list or to the detail page. After Publish the row shows the status Published (case book: Upcoming).",
 tcs="TC-210, TC-215, TC-236",
 imgs=[("evidence_06_BUG-R4-004.png","TC-210, list after Draft"),("evidence_07_BUG-R4-004.png","TC-215, list after Publish")],
 notes=("The code has no toast call on these paths (confirmed in the earlier code review, REAL_COVERAGE section 3 item 5). The frames are taken from the run video about half a second after the page changed, a toast would be visible there. "
        "BA and Dev to confirm whether the prototype toasts are required. If the build is accepted as is, change the case book instead and close this defect as Rejected. "
        "The functions themselves work (Draft row created, scheme Published, new component saved).")),
dict(id="BUG-R4-005",
 summary="[MOEFAS list] Status cards, columns and row actions differ from the final prototype",
 sev="S3",pri="Medium",status="Open",typ="UI",
 pre="Signed in as moehq. The stack holds MOEFAS schemes in several statuses.",
 steps="1. Sign in to the admin portal as moehq.\n2. Open MOEFAS.\n3. Read the subtitle, the status cards, the table columns and the row menu of a Draft, a Published and a Closed scheme.",
 exp=("Subtitle with the SBFAS sentence. Four cards Active, Upcoming, Closed, Draft. Columns Scheme, Eligibility, Application form (with the Open badge), Effective from, Effective to, Status, actions. "
      "Add fee only on Active and Upcoming, Edit on Draft, Close form now (demo) on the open scheme (case book TC-170, 171, 172, 178, 231)."),
 act=("Subtitle has the first sentence only. Seven cards: Draft, Published, Application open, Application closed, Effective, Suspended, Closed. Columns Form from and Form to instead of Application form. "
      "Add fees is offered on Draft, Published, Application open, Application closed and Suspended. Publish is a row action. No Edit and no Close form now."),
 tcs="TC-170, TC-171, TC-172, TC-178, TC-231",
 imgs=[("evidence_08_BUG-R4-005.png","TC-172, list with seven cards and two form columns")],
 notes=("Counts and cell contents match the backend data, only the design differs. The case book follows the prototype edusave.vercel.app that BA fixed as the final design on 19/10/2026. "
        "BA to decide: change the build or change the case book (REAL_COVERAGE section 3 items 1 to 3). Reject this defect if the build is accepted.")),
dict(id="BUG-R4-006",
 summary="[MOEFAS wizard] Defaults, value type and step navigation differ from the final prototype",
 sev="S3",pri="Medium",status="Open",typ="UI",
 pre="Signed in as moehq.",
 steps=("1. Sign in to the admin portal as moehq.\n2. Open MOEFAS and click New scheme.\n3. Read the fields of General and click the other steps in the stepper.\n"
        "4. On Eligibility tick a band and leave To empty, then clear From.\n5. On Subsidy read the value type and the match rule."),
 exp=("Dates prefilled (Form opens 01/08/2027, Form closes 31/12/2027, Effective from 01/01/2028). No budget field. Steps can be opened in any order. "
      "Band To may be empty and From is required. Value type Percentage of fee or Fixed amount. Match rule is a choice (case book TC-181, 190, 193, 196, 209)."),
 act=("All dates start empty and Total budget (SGD) is required. The stepper is not clickable, only Back and Next move between steps. To is required and From may be empty (counts as 0). "
      "Only percentages can be entered. The match rule is a fixed text line."),
 tcs="TC-181, TC-190, TC-193, TC-196, TC-209",
 imgs=[("evidence_09_BUG-R4-006.png","TC-181, step General with empty dates and the budget field")],
 notes=("The behaviour of each step is consistent, only it differs from the prototype and from the case book. Items 4 and 6 of REAL_COVERAGE section 3 and ASM-R4-24. "
        "BA to decide whether the build or the case book changes. Reject this defect if the build is accepted.")),
])

HDR=["Defect ID","Defect Summary","Severity","Priority","Status","Defect Type","Environment","Preconditions","Steps to Reproduce","Expected Result","Actual Result","Linked Test Case(s)","Evidence","Notes"]

def row_values(d, evidence_text):
    return [d["id"],d["summary"],d["sev"],d["pri"],d["status"],d["typ"],ENV,d["pre"],d["steps"],d["exp"],d["act"],d["tcs"],evidence_text,d["notes"]]

def need_pt(vals, widths):
    best=0
    for v,w in zip(vals,widths):
        if not isinstance(v,str): continue
        lines=sum(max(1,math.ceil(len(l)*1.08/max(w,8))) for l in v.split("\n"))
        best=max(best,lines*14.5+6)
    return best

# ------------------------------------------------ 1. standalone file with the images in the same sheet
wb=openpyxl.load_workbook(SRC)
for n in wb.sheetnames:
    if n!="Defect Reports": del wb[n]
ws=wb["Defect Reports"]
ws.column_dimensions["M"].width=54
widths=[ (ws.column_dimensions[c].width or 13) for c in "ABCDEFGHIJKLMN"]
THUMB_W=300
for i,d in enumerate(D):
    r=i+2
    ev="\n".join(["The images are embedded below in this cell. Files:" for k in range(1)]+[f"{n}  ({cap})" for n,cap in d["imgs"]])
    vals=row_values(d,ev)
    for c,v in enumerate(vals,1): ws.cell(r,c).value=v
    # images
    text_px=int((len(d["imgs"])+1)*3.6*14.5/0.75*0.28)+34   # px reserved for the caption lines
    text_px=max(text_px,72)
    y=text_px; total=text_px
    for n,cap in d["imgs"]:
        im=XLImage(os.path.join(EV,n)); w0,h0=Image.open(os.path.join(EV,n)).size
        h=int(THUMB_W*h0/w0)
        im.width,im.height=THUMB_W,h
        anchor=OneCellAnchor(_from=AnchorMarker(col=12,row=r-1,colOff=pixels_to_EMU(6),rowOff=pixels_to_EMU(y)),
                             ext=XDRPositiveSize2D(pixels_to_EMU(THUMB_W),pixels_to_EMU(h)))
        im.anchor=anchor; ws.add_image(im)
        y+=h+6; total=y
    h_img=total*0.75+6
    ws.row_dimensions[r].height=min(409,max(h_img,need_pt(vals,widths)))
    if h_img>409: print("WARN image area exceeds 409pt for",d["id"],h_img)
ws.freeze_panes="B2"
OUT="R4_All_Defects_26-10-2026.xlsx"
wb.save(OUT); print("saved",OUT)

# ------------------------------------------------ 2. test case workbook: results and defect ids
BK="R4_Test_Cases_before_exec_26-10.xlsx"
m0=os.path.getmtime(SRC)
if not os.path.exists(BK): shutil.copy2(SRC,BK)
wb=openpyxl.load_workbook(SRC)
ws=wb["Test cases "]
RUN="Run 26/10/2026 (automation, localhost build). "
P={ # Passed
"168":"The list shows the same schemes as GET moe-schemes and no SBFAS scheme. The stack holds more rows than the three case book schemes (seed and R4-AUTO data).",
"174":"Effective from is sorted newest first. Rows with the same date come in API order, the name tie break was not checked.",
"182":"The blue note shows the three dates and changes when Effective from changes. The exact wording was not compared with the case book.",
"183":"Next shows Enter a scheme name., the step stays on General and gets the warning mark.",
"184":"Both fields are required and the step stays on General. Build shows two messages (Enter the date the form opens. and Enter the date the form closes.), the case book has one shared message.",
"185":"Same day is accepted, an earlier day is refused. Build wording: Form closes must not be before Form opens. (case book: must be on or after).",
"186":"The day of Form closes and the day before are refused, the day after is accepted. Build wording: The effective start date must be after the form closing date. (case book: Effective from must be after Form closes ...).",
"187":"Effective to before Effective from is refused, empty is accepted. Build wording: Effective to must not be before Effective from. The case book also refuses an equal date, the equal date was not checked.",
"189":"The warning mark appears after a failed Next and goes away when the step is valid. The footer text To publish, fix n item(s) was not checked.",
"191":"Next shows Select at least one nationality. and stays on Eligibility.",
"192":"Next stays on Eligibility. Build wording: Use at least one income criterion. (case book: Use at least one income band (GHI or PCI).).",
"194":"From 500 with To 100 is refused (To must not be less than From.) and Next stays. The equal case was not checked.",
"197":"Applying one component adds its column with a remove control and one editable cell per level. The picker list equals the active components returned by the billing API.",
"198":"Several components can be added and a column is removed with its cross. Last column removed shows the empty state again.",
"199":"The picker offers the active components of Function 3 and the list equals the billing API.",
"204":"0 and 100 are accepted and All amounts are valid. is shown.",
"211":"Draft on an empty form shows Enter a scheme name. and creates no row.",
"213":"Discard returns to the list and saves nothing. The wizard has Discard only (no Cancel button).",
"216":"Back from Review returns to Subsidy with the percentages kept. The button is Back, not Back to edit.",
"217":"Next on Subsidy without a component is blocked, so Review and Publish cannot be reached and nothing is added. The mechanism differs from the case book (no Publish attempt on a review dialog).",
}
F={ # Failed
"205":("-1 and 101 are refused and Next stays blocked, but the message under the table is the raw key features.moeHqMoeFasCreate.errors.amountRange instead of text.","BUG-R4-001"),
"206":("33.333 is accepted: All amounts are valid. is shown and Next is enabled. No limit of two decimals.","BUG-R4-002"),
"219":("Scheme B with the same effective period as the Published scheme A was accepted and is Published. No overlap message.","BUG-R4-003"),
"220":("Scheme with the same form period as a Published scheme was accepted and is Published. No overlap message.","BUG-R4-003"),
"234":("An invalid new cell (101) keeps Confirm blocked, but the message is the raw key features.moeHqMoeFasCreate.errors.amountRange instead of text. The Add fee screen is a page with Confirm, not a dialog with Add to scheme.","BUG-R4-001"),
}
N={ # executed, left Not Run because the build differs from the case book
"170":"Subtitle shows only the first sentence of the case book text (no sentence about SBFAS). BA to confirm the long text.",
"171":"The screen has seven status cards (Draft, Published, Application open, Application closed, Effective, Suspended, Closed), the case book has four (Active, Upcoming, Closed, Draft). Counts match the rows.",
"172":"Columns are Scheme, Eligibility, Form from, Form to, Effective from, Effective to, Status, Actions (case book: one Application form column with the Open badge). Cell contents match the backend data.",
"178":"Actions follow the status of the build: View always, Publish for Draft, Add fees for Draft, Published, Application open, Application closed and Suspended, Reactivate for Suspended, never Edit. The case book uses Active and Upcoming, Close form now and Edit.",
"181":"Four steps (General, Eligibility, Subsidy, Review). Dates start empty (case book prefills them) and there is a total budget field. Hints and note wording differ.",
"190":"Nationalities, GHI and PCI bands and the match rule are shown. The match rule is a fixed text line (case book: a choice of two rules).",
"193":"The build requires To (This field is required.) and accepts an empty From as 0. The case book says the opposite (see ASM-R4-24).",
"196":"Three levels, the Fee Components button and the empty state are shown. The value type is percentage only (case book: Percentage of fee and Fixed amount).",
"209":"Values are kept by Next and Back. The stepper is not clickable, so steps cannot be opened in any order as the title says.",
"210":"A Draft row is created. No toast Draft saved. is shown and the row menu has more actions than Edit.",
"214":"Review is the fourth step of the wizard with General, Eligibility and Subsidy, not a dialog named Review scheme before publishing.",
"215":"Publish creates a Published scheme and the list offers View and Add fees. No toast is shown, the status is Published (case book: Upcoming).",
"221":"Part 1 passed (a scheme starting after the earlier one ends is accepted). Part 2 (overlapping scheme blocked) depends on BUG-R4-003 and was not run separately.",
"229":"View opens the read only detail with General, Eligibility, Budget and Subsidy and no Edit control. The header and the Close button of the case book were not matched.",
"231":"Add fees is offered on Draft schemes and opens the Add fee page. The rule of the build differs from the case book (Active and Upcoming only).",
"232":"The existing component is shown read only with its values. It is a page (Add fee), not the dialog Add fee components.",
"233":"A picked component adds an editable column that can be removed. The button is Confirm (case book: Add to scheme).",
"236":"Confirm saves the component and the new column shows next to the unchanged old one. No toast Fee components added to the scheme. is shown.",
}

for k in ("214","229","232","233"):
    P[k]=N.pop(k)
    P[k]=P[k]+" Result: the function works, the differences above are only in layout and wording."
for k,dfx in {"221":"BUG-R4-003","209":"BUG-R4-006","210":"BUG-R4-004","215":"BUG-R4-004","236":"BUG-R4-004","170":"BUG-R4-005","171":"BUG-R4-005","172":"BUG-R4-005","178":"BUG-R4-005","231":"BUG-R4-005","181":"BUG-R4-006","190":"BUG-R4-006","193":"BUG-R4-006","196":"BUG-R4-006"}.items():
    F[k]=(N.pop(k),dfx)
assert not N, N
col={h:i for i,h in enumerate([c.value for c in ws[1]])}
cnt={"Passed":0,"Failed":0,"NR":0}
for row in ws.iter_rows(min_row=2):
    tid=row[0].value
    if not tid or not tid.startswith("TC-"): continue
    k=tid[3:]
    if k in P:
        row[col["Execution Status"]].value="Passed"; row[col["Actual Result"]].value=RUN+P[k]; cnt["Passed"]+=1
    elif k in F:
        row[col["Execution Status"]].value="Failed"; row[col["Actual Result"]].value=RUN+F[k][0]+(" Part 2 was not run separately, same cause as BUG-R4-003 (code review)." if k=="221" else ""); row[col["Defect ID"]].value=F[k][1]; cnt["Failed"]+=1
    elif k in N:
        row[col["Actual Result"]].value=RUN+N[k]; cnt["NR"]+=1
# fill the Defect Reports sheet of the workbook (text only, images are in the defect file)
wd=wb["Defect Reports"]
for i,d in enumerate(D):
    vals=row_values(d,"See R4_All_Defects_26-10-2026.xlsx, sheet Defect Reports, column Evidence (images embedded).\n"+"\n".join(n for n,_ in d["imgs"]))
    for c,v in enumerate(vals,1): wd.cell(i+2,c).value=v
    wd.row_dimensions[i+2].height=min(409,need_pt(vals,[ (wd.column_dimensions[c].width or 13) for c in "ABCDEFGHIJKLMN"]))
if os.path.getmtime(SRC)!=m0: sys.exit("source changed during the run, not saved")
try:
    wb.save(SRC); print("updated",SRC,cnt)
except PermissionError:
    alt="R4_Test_Cases_executed_26-10-2026.xlsx"; wb.save(alt); print("SOURCE LOCKED, saved",alt,cnt)
