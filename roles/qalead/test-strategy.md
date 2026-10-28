# Finance System for MOE — Test Strategy

Document ID: TS-MOE-FINANCE-001
Project-level, strategic document — states the testing principles and approach for the whole engagement. `roles/qalead/test-plan.md` operationalizes these principles into the concrete 3-sprint schedule, RACI with headcount, and entry/exit dates — this document does not repeat those specifics, only the standards they must follow.

## 1. Purpose and Quality Objectives

Define how quality is assured across Track A (Admin Portal) and Track B (eService Portal) so both tracks test to the same standard despite running in parallel with separate QA sub-teams.

Quality objectives for this engagement:
1. Every tender item (and later FSD acceptance criterion) has verifiable test coverage with full traceability.
2. No Critical/High-severity defect reaches release exit.
3. The AI/ML-assisted features (FAS risk tier, eService chatbot, FAS auto-fill) never become the sole safety net — each has a rule-based or human-reviewable fallback that is tested independently of the AI layer.
4. Mock-based parallel development (Track B in Sprint 1-2) does not silently diverge from the real system — contract conformance is a tested property, not an assumption.

## 2. Test Levels and Ownership

| Level | Owner | Scope |
|---|---|---|
| Unit | Dev | Not in QA scope; no QA coverage target set |
| Smoke | QA | Confirms a new build is stable enough to start functional testing |
| Integration | QA | Track A/Track B API contract conformance; most important where Track B is still mock-based |
| Functional / Acceptance | QA | Primary activity — black-box verification per tender item / FSD criterion |
| System / End-to-end | QA (both tracks jointly) | Cross-track flows: e.g. account created in Admin (#1) correctly visible in eService (#8); FAS decision in Admin (#4) correctly reflected in eService fee payable (#9, #10) |
| UAT | TBD — not defined in tender/kickoff, raise with PM | Whether a separate customer UAT phase exists after Sprint 3 |

## 3. Testing Types

- **Functional** — covered per item via EP, BVA, Decision Tables, State Transition (see `roles/qalead/test-plan.md` §2.2 for the technique-selection guideline, shared by both tracks).
- **Security** — not deferred to "if time permits". FAS (#4) carries household income and nationality; #7 lets HQ view/act as another user; #8/#9 carry SingPass login and payment. Minimum bar: access control per role (HQ/School/Parent cannot see or act beyond their own scope), audit logging on #7 regardless of view-only vs act-on-behalf outcome, and no PII in logs or error messages.
- **Data protection** — treat citizenship, income, and nationality fields as sensitive by default. Test data must be synthetic; real citizen data is never used in any test environment. Flag to PM/customer whether a formal PDPA review is required (see `roles/qalead/test-plan.md` §2.9) — this strategy assumes "treat as sensitive" regardless of the answer.
- **AI/ML feature validation** — see Section 6, a dedicated approach rather than folded into generic functional testing.
- **Performance** — out of scope for the 3-sprint cycle; batch top-up (#2) and MOE-wide FAS eligibility checks (#4) are flagged as candidates for a dedicated pass after release, not silently dropped.
- **Usability** — not explicitly requested in tender; limited to confirming the eService AI chatbot's follow-up-question flow doesn't trap a parent in a loop with no way to reach a human/manual path.

## 4. Risk-Based Test Prioritization

Test effort is allocated by risk, not evenly across all 10 items. Priority drivers, cross-referenced to `roles/pm/project-plan.md` Risk Register:

| Priority | Items | Why |
|---|---|---|
| Highest | #4 FAS engine (rule + AI risk tier) | Highest complexity (PM R1), financial correctness directly affects families, feeds #6 and #10 |
| High | #1 Education account, #3 master data | Foundational — every other item depends on correct account/fee data |
| High | Track B mock/real contract conformance (#8, #9, #10) | PM R5 — late integration failure has the least buffer to fix in Sprint 3 |
| Medium | #2 Top-up, #6 Budget tracking, #5 Hardcopy capture | Important but lower downstream dependency |
| Medium | #7 HQ simulation | Blocked on BA clarification (view-only vs act-on-behalf); test depth depends on that answer |

## 5. Test Design Standard

Shared by both tracks, so a defect found in Track A's design approach is treated as a signal to re-check Track B, and vice versa:

- Equivalence Partitioning + Boundary Value Analysis for every numeric/date boundary (age 7/16, income tiers, balance thresholds).
- Decision Tables for any rule combining 2+ conditions (FAS eligibility, combined-payment split).
- State Transition for any entity with a lifecycle (education account Active/Closed, FAS application status).
- Every test case traces to a tender item # today, and to an FSD acceptance criterion once BA publishes it — no orphan test cases.

## 6. AI/ML and Conversational Feature Testing Approach

Traditional exact-match pass/fail does not apply to the ML risk-tier model or the chatbot. Strategy:

1. **Rule-based path first.** For #4, verify MOE/school FAS eligibility and subsidy calculation using the rule-based logic alone, independent of the ML risk-tier layer — this is the must-have path per PM's plan, and it must be provably correct on its own.
2. **ML layer tested as classification, not computation.** For the risk-tier model (Low/Medium/High), test with curated input sets where the expected tier is unambiguous (clearly low-risk, clearly high-risk profiles) and treat genuinely borderline cases as review items for a human (QA + BA), not as pass/fail defects.
3. **Chatbot (#8) and auto-fill (#10) tested for guardrails, not eloquence.** Confirm the chatbot does not fabricate FAS eligibility answers it isn't authorized to give (scope question raised by BA), and that auto-fill never submits without the parent reviewing pre-filled data.
4. Any AI output that is wrong in a way that could change a financial outcome (wrong subsidy tier, wrong auto-filled income figure) is treated as at least Major severity, never Minor/Trivial, regardless of how plausible the output looked.

## 7. Defect Severity and Priority

Severity table as defined in `roles/qalead/test-plan.md` §2.5 applies project-wide (Blocker/Critical/Major/Minor/Trivial). This strategy adds the priority dimension, used alongside severity to sequence fixes:

| Priority | Meaning |
|---|---|
| P1 | Fix before any further testing continues on that track |
| P2 | Fix before that sprint's exit |
| P3 | Fix before release exit (Sprint 3) |
| P4 | Backlog candidate, does not block this engagement's exit |

## 8. Environment and Data Strategy

One shared environment for both tracks (detail in Test Plan §3.2) so integration is tested continuously, not only at the Sprint 3 cutover. All test data synthetic, generated to match EP/BVA boundaries (Section 5), never sourced from real MOE/citizen records.

## 9. Metrics

Tracked per sprint and rolled up at release exit: test case pass rate, % of tender items/FSD criteria with at least one passing test case, open defect count by severity, and — specific to this project's AI features — count of AI outputs flagged for human review versus auto-accepted, to give PM visibility into how much manual oversight the AI layer still needs.

## 10. Relationship to Other QA Documents

- `roles/qalead/test-plan.md` — this cycle's concrete schedule, environment setup, and RACI with actual headcount.
- Test cases (not yet created) — designed per Section 5 of this document, registered per `test-plan.md` §5.1.
- This strategy is re-baselined only on a material change (e.g. a new test level added, a new AI feature introduced) — not every sprint.
