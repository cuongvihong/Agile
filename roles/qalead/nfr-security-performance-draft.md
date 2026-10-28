# Security & Performance Requirements (NFR) — Draft for Dev

Status: **DRAFT / PROPOSAL by QA Lead — not yet confirmed by BA/PM/customer.**

Per course Lesson 9 (`qa-course` §4, "Performance Requirement không phải Opinion"): a performance requirement must trace to Requirement/Contract/Tender/NFR/SLA-SLO/Approved Test Plan. The tender (`groundtruth/592ba6ad-image.png`) and kickoff transcript state **zero** NFR — no response time, concurrency, or security standard anywhere in the 10 items. Everything below is QA Lead's proposed baseline so Dev is not blocked, built from: the tender's own content, this project's confirmed facts (training prototype, simulated integrations — see `CLAUDE.md`), course Lessons 1 and 9, and general practice where the course has no depth (flagged). **Must be reviewed and confirmed by PM/BA before Dev treats any number here as fixed.**

## Why Dev needs this now

Dev cannot size the data model or API contracts without a target (L9 §105: Requirement → User Model → Data Model → Load Model → Test Plan). Security controls (access scoping, encryption) are cheap to design in from day 1 and expensive to retrofit — so this goes to Dev before Sprint 1 coding starts, not after.

---

## Part 1 — Performance (NFR)

Structure per course L9: scope, load model, data model, acceptance criteria. Given this is a confirmed **training prototype** (not a real national-scale MOE deployment), the load numbers below are sized for a demo/training system, not production Singapore scale — flagged as `[A-P1]`.

### 1.1 Scope — which flows get a performance target

Risk-based selection (per L9 §87, pick flows that matter, not just login/logout):

| Tender # | Flow | Why it's in scope |
|---|---|---|
| #2 | Batch top-up (bulk operation) | Could touch many accounts at once — a batch-window concern, not a per-request one (L9 §44) |
| #4 | FAS eligibility evaluation | Involves rule engine + optional AI risk-tier call — highest compute cost in the system |
| #8 | SingPass login + view account | Most frequent parent-facing flow |
| #9 | View charges + submit payment | Financial transaction, needs to stay responsive under load |
| #7 | HQ simulation | Lower traffic, included for completeness, lowest priority of the five |

Out of scope for now (per L9 §38, state exclusions explicitly): hardcopy FAS capture (#5, manual/offline process), budget tracking reports (#6, not latency-sensitive), AI chatbot response time (#8 AI — treated separately since AI latency has different acceptance norms, not covered here).

### 1.2 Response Time / Throughput targets `[A-P1]`

| Flow | P95 | P99 | Error rate |
|---|---|---|---|
| #8 Login + view account | ≤ 2s | ≤ 4s | ≤ 1% |
| #9 View charges / submit payment | ≤ 3s | ≤ 5s | ≤ 1% |
| #4 FAS eligibility evaluation (single application) | ≤ 5s | ≤ 8s | ≤ 1% |
| #7 HQ simulation | ≤ 3s | ≤ 5s | ≤ 1% |

Per L9 §15/43: these are **percentile** targets, not averages — do not report "average was fine" as a pass.

### 1.3 Batch window (not a response-time metric — L9 §44)

| Flow | Target |
|---|---|
| #2 Batch top-up | 1,000 accounts processed within 10 minutes |

### 1.4 Load model `[A-P2]`

Training-prototype scale, not production MOE scale:

- Normal load (Benchmark/Load test, L9 §21): **50 concurrent virtual users**, mixed across the 4 in-scope interactive flows (#8, #9, #4, #7).
- Of the course's 6 performance test types, only **Benchmark/Load** is proposed in scope for this 3-sprint engagement. Stress, Endurance, Volume, Scalability, and Breakpoint are **not** proposed — disproportionate to a training prototype's timeline and purpose. Flag to PM if that changes.

### 1.5 Data set `[A-P3]`

Ties to `roles/qalead/test-plan.md` §3.4: ~500 student accounts across ~10 schools, enough to exercise cross-school FAS scenarios (register Table 2 rank 3) without needing large synthetic volume.

---

## Part 2 — Security (NFR)

Course L1 names 5 categories for Security Testing with no further depth: Authentication, Authorization, Sensitive Data, Session, Access Control. Items below map to these 5, specialized to this project; anything beyond the 5 categories is general practice, not course content, marked `[External]`.

### 2.1 Authentication

- SingPass (parent) and AD/SSO (HQ/School) sessions must be validated server-side on every request; expired or tampered tokens rejected, not just hidden in the UI.
- Simulated SingPass/AD (per PO's training-prototype note) must still enforce the same validation logic as a real integration would — the simulation should not skip auth checks for convenience. `[A-S1]`

### 2.2 Authorization / Access Control

- Parent sees only their own linked children's accounts (ties directly to PB-04's "resolve authorized Parent-Child relationships" and tender #8).
- School user sees only their own school's students/fees/FAS data, not other schools'.
- HQ user has elevated read access across schools; the #7 "simulate school/parent view" feature must write an **audit log entry** every time it's used, regardless of whether it ends up view-only or act-on-behalf (this is already Table 1 rank 5 in `assumptions-negotiation-register.md` — still open, this NFR assumes audit logging either way as the safer default). `[A-S2]`

### 2.3 Sensitive Data Protection

- Fields treated as sensitive by default: nationality, citizenship status, household income, per-capita income (ties to Table 2 rank 1 in the Register — PDPA question still open, this NFR assumes "treat as sensitive" regardless of the answer).
- Encrypted at rest; never written to application logs in plaintext; masked in any error message or support/debug tooling.

### 2.4 Session Management

- Idle session timeout: 30 minutes, for both eService (parent) and Admin Portal (HQ/School) sessions. `[External]`
- Session token invalidated on logout; no token reuse after logout or timeout.

### 2.5 Additional controls `[External, OWASP-adjacent — not in the course]`

- Input validation / parameterized queries on every API endpoint handling user input (injection prevention).
- Rate limiting on login and FAS-application endpoints (brute-force / abuse prevention).
- TLS enforced on all traffic (course glossary defines TLS in L6/L8/L9 but doesn't prescribe this as a requirement — added here as standard practice).

---

## Assumption Log

| ID | Assumption | Why assumed | Basis | Impact if wrong | How to confirm |
|---|---|---|---|---|---|
| A-P1 | Response time targets (2-5s range) sized for a training prototype, not production MOE scale | Tender has zero NFR; numbers must come from somewhere defensible | QA Lead judgment, informed by L9 §4 (criteria must be explicit, not opinion) | Dev may over- or under-engineer for the wrong target | PM/customer confirms or adjusts before Sprint 1 ends |
| A-P2 | Load model = 50 concurrent VUs, Benchmark/Load only (no Stress/Endurance/Volume/Scalability/Breakpoint) | Matches training-prototype scope per PO's backlog note; full 6-type campaign disproportionate to 3-sprint timeline | QA Lead judgment from L9 §21, §113 decision tree | Team under-invests in a performance test type that turns out to matter | PM confirms scope is still "training prototype" through Sprint 3 |
| A-P3 | Test data: ~500 accounts, ~10 schools | Enough to exercise cross-school FAS edge case already in the Register | QA Lead, ties to `test-plan.md` §3.4 | Too little data to catch volume-related bugs | Confirm with Dev Lead during Sprint 1 data setup |
| A-S1 | Simulated SingPass/AD must still enforce real auth logic | Prevents a "fake login" shortcut that would never work if the project later integrates real SingPass | QA Lead judgment | Security gap invisible until real integration attempted | Confirm with Dev Lead at Sprint 1 design |
| A-S2 | #7 HQ simulation gets audit logging regardless of view-only vs act-on-behalf outcome | Safer default while Table 1 rank 5 (view-only vs act-on-behalf) is still unresolved | QA Lead judgment | Minor extra Dev effort if the eventual answer made logging unnecessary (unlikely) | Resolves automatically once Table 1 rank 5 is answered |

## Rules Applied

| Rule | Source | Applies to |
|---|---|---|
| Percentile (P95/P99) acceptance criteria, not average | Course L9 §15, §43 | Part 1.2 |
| Batch jobs use a batch-window criterion, not response time | Course L9 §44 | Part 1.3 |
| Only test types that match actual need, state exclusions explicitly | Course L9 §38, §113 | Part 1.1, 1.4 |
| Security Testing's 5 categories (Auth, Authz, Sensitive Data, Session, Access Control) | Course L1 §7 | Part 2 structure |
| PII/PDPA treated as sensitive by default pending confirmation | QA Lead's own Register (Table 2 rank 1) | Part 2.3 |
| Audit-log the #7 simulation feature regardless of resolution | QA Lead's own Register (Table 1 rank 5) | Part 2.2 |

## References

1. Tender — `groundtruth/592ba6ad-image.png`
2. Course Lesson 9 (Performance Testing) and Lesson 1 (QA Foundations, Security Testing section)
3. `roles/qalead/assumptions-negotiation-register.md`
4. `roles/qalead/test-plan.md` §3.4
5. `CLAUDE.md` Project Facts (training prototype, simulated integrations)
