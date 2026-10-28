# R4 automation — assertion and coverage audit (2026-10-28)

Static review only (no pytest run — no localhost/UI reachable from this environment). Goal: find tests that go
green ("PASS" or expected `known_defect` XFAIL) without actually checking the specific Expected Result of their
case, and find cases whose coverage status in the docs no longer matches the current `R4_Test_Cases.xlsx`
(confirmed 331 cases via openpyxl, header row + 331 data rows — not the 267 the generated docs still claim).

## Scope read
- All 18 mock-suite files `tests/test_f4*.py`, `tests/test_00_smoke.py`, `tests/test_not_automated.py` — 9 read
  in full depth (f410, f412, f414, f419, f420, f42, f49, plus conftest.py), the rest spot-checked by grep for
  risk patterns (see Method).
- All 8 real-suite files `tests/real/*.py` — conftest.py and `test_real_f4v_validation.py` (672 lines, 47 test
  functions) read in full; `test_real_f415_review_and_publish.py` read in full; others spot-checked.
- Helpers: `pages/real_api.py`, `pages/portal.py` read in full; others grepped for `except Exception`, `xfail`,
  `pytest.skip`.
- `data/not_automated.py`, `tools/build_coverage.py`, `docs/COVERAGE.md`, `docs/REAL_COVERAGE.md`.
- `R4_Test_Cases.xlsx` (sheet `Test cases `, `Defect Reports`) via openpyxl — row counts, Execution
  Status/Actual Result/Defect ID for a sample of TC ids, and the 11 `BUG-R4-0xx` rows cited by `known_defect`
  reasons in the real suite.

## Method (whole-tree static checks, not just the sampled files)
- AST scan of every `tests/**/*.py` and `pages/**/*.py` for an `assert` statement nested inside a `try` block
  that has an `except` (would silently swallow a failing assertion): **0 found**. The one hit the scan flagged
  (`tests/real/test_real_f4v_validation.py:638`) is a `try/finally`, which does not suppress exceptions.
- grep for `assert True`, `assert 1`, loose status checks (`!= 200`, `status not in`, `status_code`), bare
  `pass` outside an `except`: **0 found**.
- grep for `except Exception` (23 hits across `pages/*.py`, `tests/real/conftest.py`,
  `tests/real/test_real_f4v_validation.py`, `tests/real/test_real_f414_wizard.py`,
  `tests/real/test_real_f415_review_and_publish.py`): every one read in context. All guard setup/cache
  mechanics only — reusing a saved login-cookie file, best-effort `localStorage.clear()`, best-effort saving
  auth state after sign-in, retrying a 429. None wraps an `assert`/`expect()` or the action a test is actually
  verifying.

## Verdict on "pass giả" (false positive PASS)
**Not found in the sampled ~40% of test functions, and the whole-tree AST/grep sweep above found none of the
mechanical patterns that would cause it elsewhere either.** Every "should fail" assertion sampled checks both a
specific status/error code **and** a message fragment naming the exact reason, via the shared helper
`tests/real/test_real_f4v_validation.py::refused(r, fragment, status=...)` (line 142) and the equivalent
`expect(message)` checks in the mock-suite wizard tests. Example: `refused(sb.post(isPciEnabled=True,
pciFrom=None, pciTo=1000), "pciFrom is required")` — not `assert not r.created`. `accepted()` (line 147) checks
`r.created` (HTTP 200/201), which is the correct minimal check for a "should succeed" case.

`known_defect` tests (the XFAIL mechanism) were cross-checked against `R4_All_Defects_26-10-2026.xlsx`: all 11
`BUG-R4-0xx` ids cited in the real suite's `reason=` strings exist in the `Defect Reports` sheet with
**Status: Open**, and their titles match the reason text (e.g. `BUG-R4-007` reason "the NotNull check of pciFrom
never runs" ↔ defect title "PCI From and GHI From are not required when their band is on"). No case where a
`known_defect` reason refers to a defect that is actually already fixed.

## Payment-fail-style checks specifically (the pattern anh lo ngại)
R4 has no payment flow (that is R9). The closest analogue — "a thing that must be *refused*, not merely not-
created" — is the SBFAS/MOEFAS reject flow (`tests/test_f410_reject_sbfas.py`), the validation `refused()`
calls above, and the publish/overlap block in `tests/real/test_real_f415_review_and_publish.py` (TC-219/220:
`assert not ok, f"second scheme with the same periods was accepted ({data.get('code')})"` — paired with a
`known_defect` reason naming the exact missing check in `FASService`/`validation.ts`). In every sampled case the
test names the specific reason for the failure, not just "something went wrong". **No instance found of a test
that would pass merely because *any* error occurred.**

## Real findings (coverage/accounting, not assertion logic)

### 1. `tools/build_coverage.py` never scans `tests/real/` — HIGH
`automated_map()` (line 35) does `(ROOT / "tests").glob("test_f*.py")`, a **non-recursive** glob. It cannot see
any file under `tests/real/`. Any TC automated only in the real suite is therefore invisible to this tool and
gets written into `data/not_automated.py` / `docs/COVERAGE.md` as "Not automated", even though it has a real,
executed test.

Confirmed concretely:
- `data/not_automated.py:43` — `"TC-161": 'Needs the F4 build...'`
- `data/not_automated.py:47` — `"TC-165": 'Needs the F4 build...'`
- but `tests/real/test_real_f4v_validation.py:632-648` has `test_tc_161_calls_without_a_session_return_401` and
  `test_tc_165_school_user_cannot_read_moefas`, both of which actually ran: `R4_Test_Cases.xlsx` row TC-161 =
  Execution Status **Passed**, TC-165 = **Failed** / Defect `BUG-R4-013`, both dated 26/10/2026.
- `tests/test_not_automated.py` turns every key of `NOT_AUTOMATED` into a parametrized `pytest.skip(...)` test.
  So a pytest run today reports `test_not_automated[TC-161]` and `test_not_automated[TC-165]` as **SKIPPED**
  ("needs the F4 build") in the same report where, if the real suite also ran, `test_tc_161_...` and
  `test_tc_165_...` show as executed. Anyone reading `docs/COVERAGE.md` or the skip list alone is told these two
  cases are not automated; they are.
- By contrast `TC-219`, `TC-220`, `TC-225` (also real-suite-only) are correctly **absent** from
  `not_automated.py` — meaning the file was hand-pruned for those three after a manual coverage pass, but
  `TC-161`/`TC-165` were missed, and the generator itself still can't find any of them if rerun.

Recommendation: fix `automated_map()` to `rglob` (or explicitly also glob `tests/real/*.py`), rerun
`build_coverage.py` against the current `R4_Test_Cases.xlsx`, and treat its output as ground truth again.

### 2. `docs/COVERAGE.md` / `data/not_automated.py` are stale by 64 cases — HIGH
`docs/COVERAGE.md:3` states "Cases in the workbook: 267. Automated: 199. Not automated: 68." The live
`R4_Test_Cases.xlsx` (sheet `Test cases `) has **331** data rows (confirmed via openpyxl: `ws.max_row == 332`,
header + 331). The 64 newest cases, `TC-268` to `TC-331` (the validation-rules suite added 2026-10-26, per
`tests/real/test_real_f4v_validation.py`'s own docstring), do not appear in `COVERAGE.md` at all — not as
automated, not as not-automated. `data/not_automated.py`'s last entry is `TC-267`.

This means today's coverage report undercounts total scope by 64 cases and cannot tell anyone that `TC-315` to
`TC-331` (17 cases, confirmed genuinely un-automated — they need the FAS-application screens, per the test
file's own header: "Text and screen cases TC-315 to TC-331 need the FAS applications screens and are not
automated") are still open, because the file simply doesn't mention them.

Recommendation: rerun `tools/build_coverage.py` (after fixing finding 1) against the current workbook.

### 3. `known_defect` → `xfail(strict=False)` unconditionally — MEDIUM
`conftest.py:76` (mock suite) turns every `known_defect` marker into `pytest.mark.xfail(reason=..., strict=False)`
with no option to make it strict. Verified today's behavior is correct for every sampled case (the cited
`BUG-R4-0xx` is Open and the reason matches), so this is not a current false-pass. But with `strict=False`, if a
defect is fixed later, the test reports **XPASS**, not a failure — nothing forces CI or a report reader to
notice and remove the stale marker. Over many sprints this is the structural version of the "pass giả" anh is
worried about: a case can keep reporting green (now via XFAIL, later via silently-ignored XPASS) without anyone
re-confirming the Expected Result still holds.

Recommendation: either flip to `strict=True` once defects are tracked individually (so a fix forces a build
failure that prompts removing the marker), or add a periodic check that greps the junit XML for `XPASS` and
files a reminder to re-verify/close the matching `BUG-R4-0xx`.

### 4. Informational — broad `except Exception: pass` in helpers
23 occurrences across `pages/portal.py`, `pages/real_login.py`, `pages/real_sbfas.py`, `pages/real_schemes.py`,
`pages/real_api.py`, `tests/real/conftest.py`. All read in context; all guard login-cache/cleanup mechanics
only (cached cookie reuse, best-effort `localStorage.clear()`, best-effort state save, delete-on-teardown). None
wraps an assertion or the primary action under test. No action needed; noted for completeness since the parent
task asked specifically about swallowed failures.

## Not re-verified here (handed to the R9 fork / anh)
Anh's original example ("case test fail-payment pass vì đúng expected") describes a payment flow, which belongs
to R9 (Outstanding Fees and Payment), not R4 (FAS Applications) — R4 has no payment step. This audit is R4-only
by directive; the equivalent check for R9's payment-fail/webhook/reconciliation assertions should be done
against `roles/qa/r9_automation` separately.
