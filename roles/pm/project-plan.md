# PM — Project Plan: Finance System for MOE

Source: `groundtruth/592ba6ad-image.png` (tender, 10 requirements) + `groundtruth/MOE_Finance_System_Agile_Kick-off_Transcript.md` (context only — see CLAUDE.md Project Facts for precedence rule).

## Overview

- Project: Finance System for Ministry of Education (MOE), Singapore.
- Components: Admin Portal (HQ users, School users) + eService Portal (Parents), with AI features on top of base functionality.
- Delivery model: Agile, 3 sprints, 1 week each.

## Timeline

- Start: 2026-10-11. Total duration: 3 weeks.

| Sprint | Dates |
|---|---|
| Sprint 1 | 2026-10-11 - 2026-10-17 |
| Sprint 2 | 2026-10-18 - 2026-10-24 |
| Sprint 3 | 2026-10-25 - 2026-10-31 |

## Team Structure — 2 parallel tracks

Decision: Admin Portal and eService Portal run in parallel, not sequentially, using 2 sub-teams. Total hands-on engineering: 9 Dev + 5 QA, plus 1 Dev Lead and 1 QA Lead shared across both tracks (architecture, API contract, cross-track test strategy).

| Track | Dev | QA | Scope (tender #) |
|---|---|---|---|
| Track A — Admin Portal | 5 | 3 | #1, #2, #3, #4, #5, #6, #7 (7 items, heavier backend + FAS/AI engine) |
| Track B — eService Portal | 4 | 2 | #8, #9, #10 (3 items, but includes SingPass integration + 2 AI features) |

Rationale for 5/4 dev split: Track A owns the FAS rule + ML risk-tier engine, the heaviest single item, plus 6 other items. Track B has fewer items but is blocked on Track A's data/logic for 2 of its 3 items, so it needs enough capacity to build against mocks and switch to real integration quickly once Track A delivers.

**Dependency rule (critical for parallel execution):** Track B cannot build #8/#9/#10 against real backend from day 1. Dev Lead must publish API contracts for account, billing, and FAS status by day 1-2 of Sprint 1, so Track B builds against mocks matching that contract instead of waiting.

## Draft Scope Allocation by Sprint

Draft only — pending refinement with PO during backlog grooming. Numbering follows tender row (Sc#).

| Sprint | Track A — Admin Portal | Track B — eService Portal |
|---|---|---|
| 1 | SSO/AD login, environment/architecture setup, API contract definition (Dev Lead, day 1-2). #1 Education account (auto create/close). #2 Top-up (batch + individual). #3 School/cohort/class/student/fee master data. | SingPass login, UI scaffold. #8 (partial) view account/balance/transactions, update profile — built against mock API per contract from Track A. |
| 2 | #4 FAS engine (multi-scheme, rule-based eligibility + ML risk tier) — full sprint, highest complexity. #5 Hardcopy FAS capture. #6 Budget tracking (MOE FAS, SBFAS). #7 HQ simulate school/parent view. | #9 View outstanding charges, pay via balance / online / combination — still against mock billing where needed. #8 (continued) AI Q&A chatbot. |
| 3 | Integration support for Track B (real FAS/account/billing APIs), AI risk-tier model tuning, fixes from integration testing. | #10 Apply FAS as family unit + AI auto-fill application form — now against real FAS engine from Track A. Switch all mocked integrations (#8, #9) to real APIs. Full end-to-end test with Track A QA. |

## Risk Register (initial)

| ID | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| R1 | 3 weeks / 3 sprints is tight for 10 requirements + 3 AI features (ML risk tier, AI chatbot, AI auto-fill) | High | High | Build rule-based path first in each AI item, treat ML/AI as enhancement on top. Confirm with customer which AI feature can slip to a later phase if needed. |
| R2 | Third-party income API (for household/per-capita income) — availability and contract not confirmed in tender or transcript | Medium | Medium | BA to raise as open question before Sprint 1 planning. Stub/mock if sandbox not ready by Sprint 2. |
| R3 | SingPass and AD/SSO integration — sandbox credentials and access not confirmed | Medium | Medium | Request sandbox access from customer on Day 1 of Sprint 1. |
| R4 | No explicit out-of-scope statement in tender | Medium | High | BA to compile clarification question list, confirm with customer before Sprint 1 ends. |
| R5 | Track B (eService) builds against mock APIs in Sprint 1-2; if Track A's real contract drifts from the mock, integration in Sprint 3 breaks late with little buffer left | High | Medium | Dev Lead freezes API contract by day 2 of Sprint 1, any change goes through Dev Lead + both track leads. Add a mid-Sprint-2 contract-check sync between tracks, not just at Sprint 3 start. |

## Assumptions

- Third-party income API will be reachable (sandbox or mock) by start of Sprint 2.
- SingPass and AD/SSO test environment available by start of Sprint 1.
- No requirement outside the 10 tender items unless customer adds one explicitly.

## Communication Plan

| Ceremony | Cadence | Audience |
|---|---|---|
| Daily standup | Daily, 15 min | Delivery team only |
| Sprint planning | Monday, start of each sprint | Delivery team |
| Sprint review / demo | Friday, end of each sprint | Delivery team + customer |
| Retro | Friday, end of each sprint | Delivery team only |
| Status report | End of each sprint (sprint review doubles as report) | Customer |

## Open Questions to Customer

1. Confirm items explicitly out of scope for this engagement.
2. Confirm third-party income API: contract status, sandbox availability date.
3. Confirm SingPass / AD-SSO sandbox environment readiness date.
4. If the 3-sprint timeline is at risk, which items can be descoped or deferred first — priority order from customer side?
