# Builds roles/qa/UAT_Gavin_Redesign_Flow.xlsx (design only, the master is not touched)
import re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

OUT = sys.argv[1]

CASES = []

CASES.append(dict(
ID="UAT-PAR-01", Test="Pay a published charge in full with the EA and read the receipt", Role="Parent",
Setup="""Setup: Parent has a SingPass mock account and a child under 16 with an Active EA holding 150.00 (top-up from Josh). The child has one published charge of 100.00, Subsidy 0.00, not yet paid (fee published by Kent).
Data: DATA-ROLES, DATA-FEES, DATA-PAY. Values: Charge 100.00; EA 150.00; expected EA after payment 50.00.
Gate: G2 lifecycle.
Covers: FS08 FR-08.1, FR-08.2, FS09 AC-03, AC-13.""",
Steps="""1. Open e-Service, log in with SingPass, open the child's Edu Account card on Home.
   Expected: The card shows the child name, EA number and balance 150.00. This only confirms the precondition. Card order and status rules stay with UAT-006.
2. On Edu Account Detail choose Pay fees.
   Expected: Pay education charges lists only the selected child's outstanding charges with Gross amount, Subsidy, Subsidy reason, Amount due, Due date and Status. The tiles show Outstanding fees, EA balance and Selected total 0.00. The student is not asked for again.
3. Select the 100.00 charge and compare the row with the Review & authorize panel.
   Expected: Gross 100.00 minus Subsidy 0.00 equals Amount due 100.00 equals Selected total 100.00. Only the selected child, school and period appear.
4. In Review & authorize choose Education Account only and confirm.
   Expected: The EA is debited 100.00 exactly once (150.00 to 50.00). The result shows Payment successful with an invoice number.
5. Open the receipt.
   Expected: The receipt shows Invoice number, Issued at, Completed at, Gross amount 100.00, Subsidy 0.00, Amount due 100.00, Payment method Education Account and a source table with the Education Account 100.00. It has a way back to the same child.
6. Return to Pay fees and open Invoices & payments.
   Expected: The paid charge is no longer offered for payment. Invoices & payments has one row for this invoice with the amount and the Education Account method.
7. Reload the result page and reopen the receipt.
   Expected: One 100.00 debit and one invoice and receipt. The balance stays 50.00. No repeat debit or settlement.""",
Watch="Severity 1, must Pass before go live (proposed).",
In="Josh UAT-022 (EA balance), Kent UAT-MOE-01 and UAT-021 (published charge).",
Out="UAT-PAR-01-N3 and UAT-PAR-01-A1 reuse the same login and pay flow. Howard UAT-006 reads the Fee payment row afterwards.",
NotHere="Fee publication and charge creation (Kent UAT-MOE-01, UAT-021). Top-up (Josh UAT-022). Home card order, history filters and the ledger view (Howard UAT-006).",
Change="Precondition changed from an Issued invoice of 50.00 to a published charge of 100.00, because the build lists charges and creates the invoice at payment. Step 5 expects invoice number, dates, gross, subsidy, amount due, method and sources (the fields the receipt has). The invoice status expectation is removed, the build has no invoice status field. Old step 6 split into steps 6 and 7."))

CASES.append(dict(
ID="UAT-PAR-01-N3", Test="EA only is unavailable when the selected total is above the balance", Role="Parent",
Setup="""Setup: Parent is logged in. The EA balance is 40.00. The child has two published charges of 30.00 each.
Data: DATA-PAY, DATA-ROLES. Values: Balance 40.00; Charge A 30.00; Charge B 30.00.
Covers: FS09 AC-04.""",
Steps="""1. On Pay fees select charge A only and open Review & authorize.
   Expected: Selected total 30.00 is not above the balance 40.00, so Education Account only is available.
2. Add charge B so the selected total becomes 60.00.
   Expected: Education Account only becomes disabled and shows the reason. The panel suggests Online or Both. Nothing is debited and no payment record is created.
3. Remove charge B again.
   Expected: Education Account only is available again. The Selected total, the Review & authorize amount and the EA balance still agree.
4. Reload the page with both charges selected, without confirming.
   Expected: No data change. The EA balance is still 40.00, both charges are still outstanding and Invoices & payments has no new row.""",
Watch="Severity 1, must Pass before go live (proposed).",
In="UAT-PAR-01 (login and pay flow). Josh UAT-022 for the balance, Kent UAT-021 for the two charges.",
Out="The disabled option leads the parent to Both, which UAT-PAR-01-A1 runs.",
NotHere="Charge publication (Kent). Top-up (Josh).",
Change="Two charges instead of one so the case exercises the real multi charge selection and shows the option switching on and off with the total. Invoice wording removed."))

CASES.append(dict(
ID="UAT-PAR-01-A1", Test="Pay with the EA and the Online gateway together, and online only", Role="Parent",
Setup="""Setup: Parent is logged in. Child 1 has EA 20.00 and a published charge of 50.00. Child 2 has a published charge of 50.00. The Online gateway scenario is chosen to succeed.
Data: DATA-PAY, DATA-ROLES. Values: EA part 20.00; Online part 30.00. Two different children, so the two variants do not share balance or charge.
Covers: FS09 section 3.1.2.""",
Steps="""1. For child 1 select the charge, choose Both and confirm.
   Expected: The EA part equals the whole balance 20.00 and the Online part is the remainder 30.00. The EA is debited first, then the Online gateway opens.
2. Complete the payment on the gateway.
   Expected: The result shows Payment successful with an invoice number.
3. Open the receipt for child 1.
   Expected: The receipt lists both sources, the Education Account 20.00 and the Online Gateway 30.00, with Amount due 50.00. The EA balance is 0.00 and the charge is no longer offered.
4. For child 2 choose Online only and complete the gateway payment.
   Expected: One online payment of 50.00 and no EA movement. The receipt has one source, the Online Gateway 50.00, and agrees with the charge and Invoices & payments.
5. Revisit the success page of child 1 and press Pay again on the same gateway session.
   Expected: No second debit, credit, settlement or receipt. Still one invoice and the EA balance stays 0.00.""",
Watch="Severity 1, must Pass before go live (proposed).",
In="UAT-PAR-01 (pay flow). Josh UAT-022 for the 20.00 balance, Kent UAT-021 for the charges.",
Out="The failure branch of the same payment is UAT-PAR-01-N4.",
NotHere="Settlement notification handling inside the payment service. QA has no control to replay it, so it is not claimed.",
Change="Step 5 (replay of a settled notification through a QA control) replaced by a repeat action a parent can really do. Online only moved to a second child, so no settle check is needed between the two variants. Invoice wording removed."))

CASES.append(dict(
ID="UAT-PAR-01-N4", Test="Online part fails: no automatic refund, the payment goes to review and then to manual reconciliation", Role="Parent",
Setup="""Setup: As UAT-PAR-01-A1. Child 1 has EA 20.00 and a published charge of 50.00. The Online gateway scenario is chosen to fail. Child 2 has a charge of 50.00 for the online only variant.
Data: DATA-PAY, DATA-ROLES. Values: EA part 20.00; Online part 30.00.
Agreed rule (client, 31 Oct 2026): there is no automatic refund of the EA part. A failed online part goes to Payment needs review, then the system check and a manual reconciliation.
Covers: FS09 AC-09, AC-17.""",
Steps="""1. Choose Both and confirm. At the Online gateway let the payment fail.
   Expected: The result is a waiting state: waiting for the system to refund the EA part (agreed 31 Oct 2026). There is no invoice number and no receipt. No automatic refund happens. Today the build shows Payment needs review and says the Education Account may still have been deducted, recorded as a GAP on the wording.
2. Return to the child's fees and Edu Account.
   Expected: The parent sees the waiting state. The EA part stays debited and the charge is held, not offered for payment again, until the system check and manual reconciliation.
3. For child 2 choose Online only and let the gateway fail.
   Expected: The result shows Payment failed with no amount deducted. No EA movement at all, no invoice number and no receipt.
4. System check and manual reconciliation of the EA part, then the parent pays again.
   Expected: One refund of the EA part, balance back, charge payable again, one invoice and one receipt after the new payment. Blocked: done by operations outside the product screens (record with UAT-PAR-01-E2).
5. Cancel at the gateway, and force an ambiguous timeout, then query the recorded payment outcome before any retry.
   Expected: Cancel shows Payment cancelled. An unknown outcome shows Payment is being processed and stays unresolved until an authoritative result exists, with no duplicate attempt. Blocked until the simulator offers cancel and timeout (it has Succeeded and Failed only).""",
Watch="Severity 1, must Pass before go live (proposed). Failure, cancel and timeout stay in scope, do not assume 100% completion.",
In="UAT-PAR-01-A1 (same Both flow, failure outcome).",
Out="UAT-PAR-01-E2 records the operations side (alert and manual reconciliation) of the same state.",
NotHere="Success path and receipt fields (UAT-PAR-01, UAT-PAR-01-A1). The operations alert and manual refund (UAT-PAR-01-E2).",
Change="Rewritten on 31 Oct 2026 after the client agreed that there is no automatic refund. The master expectation of a refund and an Issued invoice no longer applies. N4 now covers the parent side of every failed online part, and E2 the operations side of the same state. Open question for the lead: after an online only failure the build holds the charge, the master does not say if it must be offered again."))

CASES.append(dict(
ID="UAT-PAR-01-E2", Test="EA reversal fails: the parent sees Payment needs review and operations reconcile", Role="Parent, HQ operations",
Setup="""Setup: As UAT-PAR-01-N4 with a separate child and charge. Child has EA 20.00 and a published charge of 50.00. The Online gateway scenario is chosen to fail. The EA reversal fails, which is the behaviour of the build today because the function is not delivered.
Data: DATA-PAY, DATA-ROLES. Values: EA part 20.00; Online part 30.00.
Agreed rule (client, 31 Oct 2026): operations reconcile the EA part by hand.
Covers: FS09 AC-18.""",
Steps="""1. Choose Both and confirm. At the Online gateway let the payment fail.
   Expected: The result shows Payment needs review and says the Education Account may still have been deducted. There is no invoice number and no receipt. The payment is pending reconciliation (ReconciliationRequired).
2. Return to the child's fees and open Invoices & payments.
   Expected: The parent sees a verifying status, never Paid. The EA part of 20.00 stays debited. The charge is held and not offered for payment again, so a blind second attempt is not possible.
3. Check that operations are alerted.
   Expected: An alert or a list entry exists for operations with the amount, child and time. Not visible to QA today, recorded as blocked.
4. Operations refund the EA part of 20.00 by hand and mark the payment resolved. The parent then opens Pay fees.
   Expected: One refund of 20.00, never more. The EA balance is 20.00 again and the charge is payable again. The parent pays it and gets one invoice and one receipt. Blocked until the manual path is defined and visible to QA.""",
Watch="Severity 1, must Pass before go live (proposed). The new UX assumes 100% completion, so manual reconciliation is a go live risk to record.",
In="UAT-PAR-01-A1 (same Both flow). UAT-PAR-01-N4 is the path where the reversal works.",
Out="Howard UAT-006 reads the refund and fee payment rows in the parent history.",
NotHere="The reversal that works (UAT-PAR-01-N4). Success path (UAT-PAR-01, UAT-PAR-01-A1).",
Change="Old E2 expected a failed refund command. The build has no refund command, so it fails by itself on every online failure. Steps 1 and 2 can run for real today. Steps 3 and 4 follow the manual reconciliation the client agreed."))

CASES.append(dict(
ID="UAT-031", Test="MOEFAS assesses submitted applications against the scheme rules", Role="HQ / School user",
Setup="""Setup: The MOE FAS 2026 scheme is published (Admin Portal, MOEFAS). Its Eligibility column reads Singapore Citizen, GHI up to S$4,000.00 or PCI up to S$1,100.00, form 1 Jan to 30 Nov 2026, effective from 1 Dec 2026. Applications were submitted by parents or by the seed (Howard, UAT-PRE-03). The expected table is written independently from the scheme row before any run.
Data: DATA-FAS, DATA-SCHEME, DATA-ROLES. Households: GHI only, PCI only, neither, exact limit, plus controls for nationality (SC and PR) and wrong school (School B).
Gate: G3, D05, D06 (no guessed threshold, no assumed budget rule). HQ can confirm only from the scheme effective date.
Covers: US-044, US-045.""",
Steps="""1. Write the expected table from the scheme row: GHI only (3,900 and PCI 1,500) eligible, PCI only (4,400 and PCI 1,100) eligible, neither (4,400 and PCI 1,200) not eligible, GHI exactly 4,000 eligible if the limit is inclusive.
   Expected: The table exists before the run and states the rule used for the exact limit. The seeded application APP-4FDC4038 (GHI 4,400, PCI 1,100) is the real PCI on the limit example.
2. As MOE HQ open MOEFAS, FAS applications. Use the cards (Submitted, Pending MOE review, Approved by MOE, Not approved), search by application ID, name or NRIC, and read the GHI and PCI columns.
   Expected: Each application shows its GHI, PCI, school and state. Every row agrees with the expected table. Before 1 Dec 2026 eligible applications stay Pending MOE review. HQ has no Approve or Reject button.
3. Check the controls.
   Expected: A PR applicant is not assessed as eligible for the Singapore Citizen scheme. A School B user does not see School A applications in the school portal FAS Applications list. No wrong scope bypass.
4. Refresh the list and run the confirmation again after 1 Dec 2026.
   Expected: No duplicate allocation and no changed result. Approved by MOE and Not approved counts add up with the Total applications card. Waiting (Pending) and assessed observations are kept separate.""",
Watch="Severity 1 (proposed). HQ confirms only from the scheme effective date, so before it the case checks the Pending MOE review state only.",
In="Kent UAT-MOE-06 and UAT-SCH-02 (published schemes), Howard UAT-028 and UAT-049 (submitted applications).",
Out="UAT-031-E1 takes the applications MOEFAS did not approve down to the school SBFAS. UAT-033 uses a granted application.",
NotHere="Creating or validating schemes (Kent UAT-MOE-06, UAT-MOE-06-N1, UAT-SCH-02, UAT-SCH-02-N1). Granting or rejecting (Kent UAT-SCH-03, UAT-SCH-03-N1, UAT-035). Submitting the application (Howard UAT-028, UAT-049). Budget counting (Josh UAT-038, UAT-040).",
Change="Old UAT-031 created and validated schemes (wizard, date rules, publish) which Kent already owns in four cases. It is now the assessment of applications, which is Gavin's area in the Team sheet and DATA-FAS. Labels are taken from the screens: MOEFAS list, FAS applications cards and columns, school portal FAS Applications."))

CASES.append(dict(
ID="UAT-031-E1", Test="An application MOEFAS does not approve goes down once to the school SBFAS", Role="HQ / School user",
Setup="""Setup: As UAT-031. Two applications at School A: one that MOEFAS approves and one that it does not. School A has a published SBFAS scheme (Kent). Rule confirmed by the client on 30 Oct 2026: when MOEFAS does not approve, the application moves to the school SBFAS.
Data: DATA-FAS, DATA-SCHEME, DATA-ROLES. Variants: one child at School A and one at School B (cross school, gate G3); a PR applicant; a school with no published SBFAS scheme.
Gate: G3, D05. The MOEFAS decision runs from the scheme effective date.
Covers: FS04 routing between MOEFAS and SBFAS.""",
Steps="""1. After the MOEFAS decision open the HQ FAS applications list, then the School A portal FAS Applications list.
   Expected: The approved application shows Approved by MOE at HQ and is not in the school list. The application MOEFAS did not approve shows Not approved at HQ and appears once in the school list with the status Pending School Review, with its beneficiaries and income verification kept.
2. Run the MOEFAS decision again on the same applications.
   Expected: No second school entry and no change to the first. The Applications received count of the school does not grow. No application is lost or duplicated.
3. Cross school variant: one sibling at School A and one at School B, both not approved by MOEFAS.
   Expected: Each application appears only in the list of the child's own school. A School A user cannot see the School B one. Blocked until gate G3 settles the routing rule.
4. Variant: a PR applicant.
   Expected: The application goes straight to the school list as Pending School Review without a MOEFAS decision. This comes from the old UAT-PAR-02-A2.
5. Variant: the child's school has no published SBFAS scheme.
   Expected: The application is not lost. Its state follows the agreed rule and the observation is recorded as found.""",
Watch="Severity 1 (proposed). New case, owner to confirm with Kent and Howard that nobody else already covers the route.",
In="UAT-031 (MOEFAS decision). Kent UAT-SCH-02 (published SBFAS scheme).",
Out="Kent UAT-SCH-03, UAT-SCH-03-N1 and UAT-035 take the pending application to the school decision (View details in the school portal).",
NotHere="The school's approve or reject action (Kent UAT-SCH-03, UAT-SCH-03-N1, UAT-035). Scheme creation (Kent UAT-SCH-02). Parent result screens (Howard UAT-008).",
Change="New case. The master had no case for the route between MOEFAS and SBFAS, only the word route inside UAT-046 step 2 and UAT-049 step 4. Status labels come from the screens (Not approved, Pending School Review)."))

CASES.append(dict(
ID="UAT-033", Test="A granted subsidy lowers the amount due and the invoice is paid at the net amount", Role="Parent, HQ / School user",
Setup="""Setup: Kent's published scheme gives 50% on supported component A (80.00) and 0% on unsupported component B (20.00), so one charge has Gross 100.00. The child has an approved grant (Kent) and EA 100.00. A second child has a fixed subsidy of 100.00 against supported component A, cap 80.00. The Online gateway is not needed.
Data: DATA-SCHEME, DATA-FEES, DATA-PAY. Values: Gross 100.00; Subsidy 40.00; Amount due 60.00; EA 100.00 before and 40.00 after.
Gate: Subsidy applies from the scheme effective date (1 Dec 2026 on the stack). D05.
Covers: US-047, US-051.""",
Steps="""1. As the parent open Pay fees for the granted child.
   Expected: The charge row on Pay education charges shows Charge name, Gross amount 100.00, Subsidy 40.00, a Subsidy reason, Amount due 60.00 and Status. Details shows component A subsidy 40.00 and component B subsidy 0.00. The original amount stays 100.00.
2. Open the second child with the fixed subsidy 100.00 against component A with cap 80.00.
   Expected: Subsidy is capped at 80.00 and Amount due is 20.00. Amount due is never below 0.00. Other components are unaffected.
3. For the first child pay with the Education Account only and open the receipt.
   Expected: The invoice and the debit are the net 60.00, not 100.00 (EA 100.00 to 40.00). The receipt shows Gross amount 100.00, Subsidy 40.00, Amount due 60.00 and the source Education Account 60.00.
4. Compare controls: a paid charge, a charge of an unsupported component and a charge outside the effective period. Then repeat the grant action once (reopen or confirm again).
   Expected: Controls keep Subsidy 0.00 unless an agreed adjustment rule says otherwise. No duplicate subsidy, no negative payable, original amounts unchanged.""",
Watch="Severity 1 (proposed). Original amount is immutable, subsidy applies to eligible components only, net payable floor is 0.00.",
In="Kent UAT-SCH-02 (scheme and matrix) and UAT-SCH-03 (approved grant), Kent UAT-021 (charges), Gavin UAT-031 and UAT-031-E1 (decision and route).",
Out="UAT-PAR-01 family pays the other charges. Howard UAT-008 shows the grant to the parent. Josh UAT-038, UAT-039 and UAT-040 count the granted subsidy.",
NotHere="Configuring the subsidy matrix (Kent UAT-SCH-02). Approving the application (Kent UAT-SCH-03). Paying a subsidised fee with EA 40.00 plus online 20.00 (Howard UAT-045 step 3). Budget and statistics (Josh).",
Change="Old UAT-033 configured the matrix (Kent) and simulated the grant. It is now the effect of the grant on the charge row and on the invoice and receipt. The split payment of the subsidised fee stays in Howard UAT-045."))

STAGES = [
(0,"Foundation: EA, school, students","Josh","UAT-001, UAT-002","Chan","UAT-013, UAT-014, UAT-015, UAT-016, UAT-017, UAT-018","Active EA per child, school, class, enrolled student linked to the EA, school and HQ users","Everything below"),
(1,"MOE top-up to the child's EA","Josh","UAT-022, UAT-023, UAT-024, UAT-025, UAT-026, UAT-027","","","EA balance","Fees paid with the EA (stage 9), parent view (stage 3)"),
(2,"Fee creation by MOE and school","Kent","UAT-MOE-01, UAT-019, UAT-020, UAT-021","","","Published charges per student, with rate and original amount","Subsidy (stage 8), payment (stage 9)"),
(3,"Parent can log in and sees the children","Howard","UAT-005, UAT-007","","","Verified parent session and linked children","Application (stage 5), payment (stage 9)"),
(4,"MOEFAS and SBFAS schemes and budgets","Kent","UAT-MOE-06, UAT-MOE-06-N1, UAT-SCH-02, UAT-SCH-02-N1","Josh","UAT-MOE-04, UAT-SCH-04, UAT-038","Published MOEFAS and school SBFAS schemes with budgets","Application and decision (stages 5 to 7)"),
(5,"Parent and school submit the FAS application","Howard","UAT-028, UAT-047, UAT-049","Chan","UAT-029, UAT-030, UAT-SCH-01, UAT-SCH-01-N1, UAT-SCH-01-E1","Submitted applications (online and paper)","MOEFAS decision (stage 6)"),
(6,"MOEFAS decides, the rest goes down to SBFAS","Gavin","UAT-031, UAT-031-E1","","","Approved MOEFAS applications, and declined ones in the school pending list","School decision (stage 7), subsidy (stage 8)"),
(7,"School decides the SBFAS applications","Kent","UAT-SCH-03, UAT-SCH-03-N1, UAT-035","","","Approved or rejected SBFAS applications with tier","Subsidy (stage 8)"),
(8,"Subsidy applied to the eligible fees","Gavin","UAT-033","","","Charges with Gross, Subsidy, Amount due","Payment (stage 9)"),
(9,"Parent pays","Gavin","UAT-PAR-01, UAT-PAR-01-N3, UAT-PAR-01-A1, UAT-PAR-01-N4, UAT-PAR-01-E2","","","Invoice, receipt, EA debit, payment failed or in review","Parent reads (stage 10), budget (stage 11)"),
(10,"Parent reads the results","Howard","UAT-006, UAT-008","","","Balance, history and grant shown to the parent","Closing checks"),
(11,"Budget and statistics","Josh","UAT-039, UAT-040, UAT-MOE-05, UAT-MOE-05-E1, UAT-SCH-04-E1","","","Used and remaining budget, granted subsidy statistics","Closing checks"),
(12,"End to end rehearsal and role boundaries","Howard","UAT-045","Chan","UAT-046, UAT-048","Whole journey rehearsed once","Go live decision"),
(13,"EA closure","Josh","UAT-003, UAT-004","","","Closed EA, residual to the CPF simulator exactly once","End"),
]
OUT_OF_SCOPE = [("UAT-041","Chan","View As"),("UAT-042","Chan","View As"),("UAT-043","Howard","FAQ chatbot"),("UAT-044","Howard","FAQ chatbot")]
FLOW = []
for st,name,o1,c1,o2,c2,prov,need in STAGES:
    FLOW.append((str(st),name,o1+(" and "+o2 if o2 else ""),c1+(", "+c2 if c2 else ""),prov,need))
for cid,o,w in OUT_OF_SCOPE:
    FLOW.append(("Out",w+" (not in this release)",o,cid,"Not run now",""))

OVERLAP = [
("UAT-031 (old)","Scheme wizard, date rules, publish, School B cannot edit","Kent UAT-MOE-06, UAT-MOE-06-N1, UAT-SCH-02, UAT-SCH-02-N1","Removed from Gavin. Replaced by assessment of applications (step 4 of the old case is the part that stays)."),
("UAT-031 step 4 (old)","Expected table for GHI, PCI, neither, exact limit","None. Team sheet gives FAS assessment to Gavin and DATA-FAS to Gavin","Kept and made the whole case."),
("UAT-033 step 1 (old)","Configure the subsidy matrix 50% on component A","Kent UAT-SCH-02 step 1 and DATA-SCHEME","Removed. Uses Kent's published scheme."),
("UAT-033 steps 2 to 4 (old)","Net payable, cap, replay","None. Kent covers configuration, nobody covers the effect on the charge and invoice","Kept, and extended to the net invoice and receipt. The split payment stays with Howard UAT-045."),
("UAT-PAR-01 step 1 (old)","Home card shows child, EA code, balance","Howard UAT-006 step 1 (card order and fields)","Kept as a precondition check only, not as a display test."),
("UAT-PAR-01 step 6 (old)","Compare history after payment","Howard UAT-006 step 4 (history and View fee link)","History view stays with Howard. Gavin keeps Invoices & payments and the receipt."),
("UAT-PAR-01 data","Fee must exist before payment","Kent UAT-MOE-01, UAT-021","Not re-tested. Used as input."),
("UAT-PAR-01-N4 and E2 (old)","Reversal works (N4) and reversal fails (E2) on the same flow","Gavin only","Kept as two cases. They look contradictory but are the two outcomes of the same step. Today the build only produces the E2 outcome."),
]

MISMATCH = [
("Child has an Issued invoice","The parent selects outstanding charges on Pay education charges. The invoice is created when payment starts and its number appears on the result and the receipt.","Precondition and wording changed to charges."),
("Invoice becomes Paid","No invoice status field on the receipt or in Invoices & payments (the status filter and an invoice detail page are not checked yet).","Paid is read from Payment successful, the charge leaving the outstanding list and the Invoices & payments row."),
("N4: EA part refunded, invoice back to Issued, balance 20.00","The result page already has the strings Payment failed and The Education Account payment was reversed, but today the build shows Payment needs review because the reversal function is not delivered.","N4 keeps the master expectation. Steps 1 and 2 are a GAP until the function exists."),
("E2: failed refund command, ReconciliationRequired","No refund command exists, so every online failure ends as Payment needs review. No operations alert is visible to QA.","E2 runs for real today (steps 1 and 2). Alert and manual reconciliation are blocked."),
("A1 step 5: replay a settled notification with a QA control","No such control. The simulator has one Pay button with a hidden outcome.","Replaced by repeating on the same gateway session."),
("N4 step 3: cancel and ambiguous timeout","Simulator outcomes are Succeeded and Failed only.","Kept as a blocked step with the reason."),
("A1 split 20 + 30 and PAR-01 values 50 and 100","Stack children hold 520 after seeding and the fees are 50, 100, 600 and 700.","Case design keeps the master values. The stack mapping sits in data/seed_plan.py."),
("031: scheme wizard validations","Server messages are 'effectiveFrom must be after openTo' and 'totalBudgetAmount must be greater than 0 when publishing'. Owned by Kent.","Moved out of Gavin."),
("033: subsidy applied once a grant is linked","MOEFAS approval and subsidy follow the scheme effective date (1 Dec 2026 on the stack). Before it the case stays blocked.","Gate stated in Setup."),
]

thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
head_fill = PatternFill("solid", fgColor="1F4E79")
head_font = Font(bold=True, color="FFFFFF")
wrap = Alignment(wrap_text=True, vertical="top")

def sheet(ws, headers, rows, widths):
    ws.append(headers)
    for r in rows: ws.append(list(r))
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in ws[1]:
        c.fill = head_fill; c.font = head_font; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = border
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = wrap; c.border = border
    ws.freeze_panes = "B2"

wb = Workbook()
ws = wb.active; ws.title = "Gavin cases"
rows = []
for c in CASES:
    rows.append((c["ID"], c["Test"], "Fees and payments" if c["ID"].startswith("UAT-PAR") else "FAS assessment", "Gavin", c["Role"],
                 c["Setup"], c["Steps"] + "\n\nWatch for: " + c["Watch"], "Not Run", c["In"], c["Out"], c["NotHere"], c["Change"]))
sheet(ws, ["ID","Test","Area","Owner","Role","Setup, data and gate","Steps and expected results","Status","Comes from (other owners)","Hands on to","Not tested here (owner)","What changed from the master"],
      rows, [16,34,16,9,16,60,95,10,36,36,42,55])

ws2 = wb.create_sheet("Flow map")
sheet(ws2, ["Stage","What happens","Owners","Cases","What the stage hands on","Needed by"], FLOW, [7,40,20,70,60,45])
ws3 = wb.create_sheet("Overlap check")
sheet(ws3, ["Old Gavin case or step","What it tested","Overlaps with","Decision"], OVERLAP, [30,50,60,60])
ws4 = wb.create_sheet("Master vs build")
sheet(ws4, ["Master says","Build does","How the new case handles it"], MISMATCH, [55,80,60])
wb.save(OUT)

# no dash punctuation check
bad = []
for w in wb.worksheets:
    for row in w.iter_rows(values_only=True):
        for v in row:
            if isinstance(v, str) and re.search(r"[–—]| - ", v): bad.append((w.title, v[:60]))
print("saved", OUT, "dash problems:", bad)
