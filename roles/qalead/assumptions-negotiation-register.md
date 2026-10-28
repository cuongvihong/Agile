# Finance System for MOE — Assumptions & Negotiation Register

Document ID: ANR-MOE-FINANCE-001
Owner: QA Lead. Built directly from tender analysis (`groundtruth/592ba6ad-image.png`) and kickoff transcript — a shift-left QA activity, not a BA deliverable. Purpose: surface what must be negotiated/confirmed with the customer (MOE), ranked so PM/customer know what to answer first.

Two separate tables, not merged, per explicit instruction:

- **Table 1 — Blocking Register**: items where missing information stops delivery work from proceeding correctly, or forces an architecture/design decision. Ranked by urgency = how much of the whole project (not just one track) is blocked.
- **Table 2 — Business Impact Register**: items where delivery can proceed either way, but an unconfirmed assumption carries financial, fairness, or compliance consequence for real families/schools if it turns out wrong. Ranked by severity of that consequence, independent of delivery urgency.

An item appears in exactly one table — the one that reflects its primary risk.

## Table 1 — Blocking Register (ranked by project-wide delivery urgency)

| Rank | Tender # | Open Item | Why It Blocks | Scope of Block | Severity |
|---|---|---|---|---|---|
| 1 | #8 / Admin login | SingPass (parent login) and AD/SSO (HQ/School login) sandbox access not confirmed | Neither Track A nor Track B can build or test any login-gated flow without it | Both tracks, Sprint 1 Day 1 | Critical |
| 2 | #9 | No payment gateway/provider named anywhere in tender | Track B has nothing to integrate or mock against for online payment | Track B, Sprint 2-3 | Critical |
| 3 | #4 | Third-party income API — contract status and sandbox availability unconfirmed | FAS (#4) is the highest-complexity item and the critical-path dependency for #5, #6, #10 | Track A Sprint 2, cascades to Track B Sprint 3 | Critical |
| 4 | Overall | No explicit out-of-scope statement in the tender | PO cannot lock the backlog with confidence; risk of scope dispute mid-project | Whole project, backlog planning | High |
| 5 | #7 | HQ "simulate school/parent view" — view-only or able to act on behalf of the user | These are two different security/audit architectures, not a detail that can be patched in later | Track A, design + build | High |
| 6 | #4 | ML risk-tier model — recommendation only, or authorized to auto-decide | Determines whether FAS approval flow needs a human-review step; changes the design | Track A, Sprint 2 design | High |
| 7 | #1 | Source system for child DOB and citizenship verification not named | #1 is foundational — #2, #3, #9 all depend on a correctly created account | Track A, Sprint 1, foundational | High |
| 8 | #1 | **[PARTIALLY RESOLVED 2026-10-11]** Account creation trigger for a child who becomes a Singapore Citizen *after* age 7 is still undefined (creation side). Deactivation side now confirmed: account deactivates 1 day before the student turns 16, OR immediately on loss of Singapore Citizenship, whichever occurs — so the account lifecycle is confirmed event-driven for closure, not date-driven only. Still open: (a) what happens to the balance on deactivation — see Table 2 rank 2; (b) whether gaining citizenship after age 7 also creates the account immediately (creation side still unanswered) | Confirms #1 needs to listen for a citizenship-status-change event, not just a scheduled age check — settles part of the architecture question, the rest still blocks detailed design | Track A, Sprint 1 design | High |
| 9 | Overall | Whether a separate customer UAT phase exists after Sprint 3, or acceptance happens within it | Affects whether Sprint 3's plan (integration + regression) leaves room for UAT, or UAT is unaccounted for | Whole project, Sprint 3 schedule | Medium |
| 10 | #2 | Where top-up funds originate from is not modeled anywhere in the tender — only "HQ performs top-up" and, for ad hoc, "government budget approval" (external, per kickoff transcript) is mentioned. Unlike FAS (#4, #6 budget tracking exists), #2 has no budget/source entity at all | Decides whether #2 needs a source ledger/budget entity that gets debited when a top-up is made (with its own balance, limit, audit trail), or whether top-up is simply a credit with no in-system source tracked (money assumed to come from MOE's external government budget, outside this system — the simpler, more likely default based on how the real Edusave scheme works) | Track A, Sprint 1 design (#2 is a Sprint 1 item) | High |

## Table 2 — Business Impact Register (ranked by consequence if the assumption is wrong, independent of delivery urgency)

| Rank | Tender # | Open Item | Business Impact If Wrong | Who Is Affected | Impact Level |
|---|---|---|---|---|---|
| 1 | Overall | Whether a formal PDPA / data-protection review is required (system holds income, nationality, citizenship data) | Legal/regulatory exposure for MOE and the vendor; reputational risk if a breach or non-compliant handling surfaces post-release | MOE, vendor, all citizen families | Critical |
| 2 | #1 | **[Trigger confirmed 2026-10-11, balance disposition still open]** Deactivation now confirmed to trigger 1 day before age 16, OR on loss of Singapore Citizenship. What happens to the remaining balance at that point is still not defined | Families could lose real money with no defined recourse if silently forfeited | Every family with a closing account | High |
| 3 | #4 | How a FAS application is resolved when siblings attend different schools | Risk of double-subsidy (cost to MOE/schools) or a sibling missing subsidy entirely (harm to a needy family) | Multi-child families, school FAS budgets | High |
| 4 | #10 | Whether one family FAS application auto-applies to every child or needs per-child confirmation | Same fairness/financial risk as above — a wrong default either over- or under-grants per child | Multi-child families | High |
| 5 | #2 | Exact batch top-up rule operators, and whether ad-hoc top-up needs an in-system approval step. "Schooling status" specifically is undefined — candidate meanings: (a) currently enrolled vs not, (b) MOE-funded vs non-MOE-funded school (the real Edusave scheme treats these two very differently — see `giai-thich/04-doi-chieu-thuc-te.md`), (c) education level (primary/secondary/pre-university) | Wrong accounts could receive top-ups, or intended recipients could be missed — real money movement | Account holders targeted by batch rules | Medium |
| 6 | #3 | Who owns fee-amount configuration (HQ vs. school) and whether it varies by cohort/class | Incorrect fee configuration leads to over- or under-billing a student | Students/families billed incorrectly | Medium |
| 7 | #6 | Whether the system hard-blocks grants beyond budget, or only reports after the fact | A school or MOE could overspend its FAS budget before anyone notices | School/MOE finance governance | Medium |
| 8 | #9 | How a combined balance + online payment splits between the two sources | Parent disputes over how much was deducted from each source | Parents paying by combination method | Medium |
| 9 | #8 | Whether the AI chatbot may explain FAS eligibility rules, or is limited to navigation help | A chatbot that states eligibility outcomes a family relies on, if wrong, causes real financial expectation-setting harm | Parents asking the chatbot about FAS | Medium |
| 10 | #5 | Whether OCR auto-extraction is expected for hardcopy FAS forms, or manual entry by school staff is sufficient | Lower stakes — affects school-user effort and transcription-error risk, not the subsidy outcome itself | School users processing hardcopy forms | Low |
| 11 | #9 | Whether paying for multiple children must be supported in a single transaction | Convenience/reconciliation only; a parent can submit separate payments as a workaround | Parents with multiple children | Low |

## Real-World Reference Note (added after reviewing Singapore MOE's actual Student Finance System)

For Table 2, rank 2 (account balance disposition at closure): the real-world system this tender is modeled on (MOE's Edusave scheme, `studentfinance.moe.gov.sg/sfs`) closes the account at age 17 (not 16) or when the student leaves an MOE-funded school, whichever is later, and **automatically transfers the remaining balance to a follow-on account (PSEA)** rather than forfeiting it. The tender has no equivalent follow-on account, so this doesn't resolve the open item, but it gives PO/customer a sensible real-world default to consider instead of designing from scratch. Also noted: the tender's age-16 closure differs from the real scheme's age-17 — worth flagging as a possible intentional simplification, not assumed to be an error. Full comparison in `giai-thich/04-doi-chieu-thuc-te.md` (Vietnamese, written for the user, not a team doc).

For Table 1, rank 1 (SingPass sandbox): Singpass's own onboarding prerequisites require every integrating service to offer at least one non-SingPass alternative (manual entry, document upload, etc.) — the tender's hardcopy FAS path (#5) already satisfies this real-world constraint, which is a good sign the tender's shape is sound even though this project's SingPass integration itself is simulated per PO's backlog.

## How to Use This Register

- Table 1 items should be raised with the customer before or during Sprint 1 planning — each one either blocks a track outright or forces a design decision that is expensive to reverse later.
- Table 2 items can be raised on a slightly longer fuse, but should all be confirmed before the feature they affect reaches release exit (see `roles/qalead/test-plan.md` §2.3 release exit criteria) — shipping on an unconfirmed Table 2 assumption means shipping a financial or compliance risk, not just a delivery risk.
- Cross-reference: `roles/pm/project-plan.md` Risk Register (R1-R5) covers project-execution risk (timeline, team split, contract drift) — a different axis from this register, which is about tender/requirement ambiguity specifically.
