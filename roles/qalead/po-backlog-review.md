# QA Lead Review — PO Initial Product Backlog v0.1

Reviewed: `roles/po/EAFAMS_Initial_Product_Backlog_v0.1.xlsx` (30 PBIs, sheets: Overview, Product Backlog, Sprint 1 Candidates, Requirement Coverage). Purpose: flag items for the team before this afternoon's estimation session — not a rewrite of the backlog, QA Lead review only.

## Overall

Structurally sound: vertical-slice sprint goals (not per-portal), explicit MoSCoW priority, dependency chain per PBI, "Pending clarification" readiness flag used honestly on risky items, a minimum-demo-slice fallback for Sprint 1, and a Definition of Done checklist. Reasonable to estimate against, with the findings below addressed or at least acknowledged first.

## Finding 1 — Changes the severity of 3 items in my Blocking Register (important)

The backlog's Overview sheet states this is explicitly a **training prototype with mock/simulated integrations**: "Mock citizen/student data and simulated Singpass, income API and online payment are allowed for the training prototype."

`roles/qalead/assumptions-negotiation-register.md` Table 1 currently ranks SingPass/AD sandbox (#1), payment gateway (#2), and third-party income API (#3) as **Critical, whole-project blockers** — written under the assumption that these need real customer-provided access. If they are meant to be simulated/mocked throughout, as PO's backlog states, those 3 items drop from "blocks the whole project" to "internal design decision: agree on mock behavior and data shape" — much lower urgency, no customer dependency at all.

This is a real conflict between what I assumed (real integrations, customer must provide sandbox access) and what PO has written (simulated integrations by design). **I have not changed the register yet** — flagging first since it changes risk framing for the whole project, not just a QA document. Recommend confirming with PM/PO before this afternoon's estimation, since team capacity planning differs a lot between "wait on customer sandbox access" and "agree on a mock spec ourselves."

## Finding 2 — Priority/dependency inconsistency in Sprint 2

PB-09 (fee types/components, **Must**) depends on PB-08 (school/class/student CRUD, **Should**). If PB-08 gets deprioritized under time pressure (it's only "Should"), PB-09 and PB-10 (both "Must", both depending on PB-08 or its data) are blocked by a lower-priority item. Recommend either raising PB-08 to Must, or explicitly noting PB-08 is a de facto Must because Must-priority items depend on it.

## Finding 3 — Sprint 3 risk concentration, no buffer

All 6 FAS-related PBIs (PB-18 to PB-23) sit in Sprint 3, the last sprint. 4 of them (PB-18, PB-19, PB-21, PB-22, PB-23) are marked "Pending clarification", and PB-18/19/20/21/23 are "Must". This is the same concern as PM's Risk R1 (`roles/pm/project-plan.md`), but concretely: the least-clarified, most interdependent cluster of the whole backlog lands in the sprint with no following sprint to absorb slip. Recommend the team treat Sprint 3 estimation with extra caution and flag early if FAS clarifications aren't resolved by end of Sprint 2.

## Finding 4 — New open item to add to the Negotiation Register

PB-21's open question — "Auto-grant trigger: submitted application or proactive grant?" — is not yet in `roles/qalead/assumptions-negotiation-register.md`. It's architecture-blocking in the same way as the already-listed "ML risk tier: recommendation vs auto-decide" item (Table 1, rank 6): whether MOEFAS grant is triggered by an application event or runs proactively changes the FAS engine's design. Recommend adding to Table 1.

## Finding 5 — Sprint 1 cross-track coupling is tighter than previously documented

`roles/pm/project-plan.md` (kept as reference only, not authoritative per the current PO backlog) described Track B building against mocks through Sprint 1-2 before integrating in Sprint 3. PO's actual Sprint 1 Candidates sheet has PB-04/PB-05 (Parent view account — Track B/eService side) depending directly on PB-03 (account creation — Track A/Admin side) **within the same sprint**. That means Track A must deliver #1's core logic very early in Sprint 1 for Track B to build against it at all (real or mocked) — not a Sprint-3-only integration point. Worth confirming with PM/Dev Lead whether the contract-freeze timing (day 1-2 of Sprint 1, per PM's plan) is still tight enough given this.

## Not a concern (noted for completeness)

- AI items (PB-28/29/30) are all "Unrefined", "Later", "Could" — consistent with `roles/qalead/test-strategy.md` §6 (rule-based path first, AI as enhancement). No conflict.
- PB-06's "Must*" flag for account-closure/balance ambiguity matches `roles/qalead/assumptions-negotiation-register.md` Table 2, rank 2, almost exactly — good independent confirmation from PO's side that this is a real open item, not QA overthinking it.
