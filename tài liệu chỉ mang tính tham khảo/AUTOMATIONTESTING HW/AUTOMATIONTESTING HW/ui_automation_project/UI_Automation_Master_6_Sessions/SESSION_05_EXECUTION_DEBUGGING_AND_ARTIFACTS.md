# SESSION 05 — EXECUTION, DEBUGGING AND ARTIFACTS

Continue from Sessions 01–04.

## Objective
Run the project, diagnose failures, and generate real execution evidence.

## Step 1 — Install

```bash
pip install -r requirements.txt
playwright install
```

## Step 2 — Run all tests

```bash
pytest -v
```

## Step 3 — Run the HTML report

```bash
pytest -v --html=artifacts/reports/report.html --self-contained-html
```

## Step 4 — Debug failures

If Session 04 implemented an official test case library with
`known_defect`-marked tests: a failure in one of those is expected and
correct — it is the automated evidence for a real, already-logged
defect. Do not debug it as if it were a bug in the suite; only apply the
steps below to a failure that is genuinely unexpected (i.e. not
`known_defect`, and not matching the official library's own recorded
Failed/Blocked status for that case).

For every unexpected failure:

1. read the failure message;
2. identify the exact failing action/assertion;
3. inspect the locator;
4. inspect the actual HTML;
5. check visibility/enabled state;
6. check timing;
7. check test data;
8. rerun only the failing test;
9. use headed mode if necessary;
10. inspect screenshot/trace.

Do not automatically solve failures with sleeps, huge timeouts, or retries.

## Evidence

Generate useful screenshots under:

```text
artifacts/screenshots/
```

Use meaningful filenames.

`pytest-playwright`'s own `--screenshot=only-on-failure`/`--tracing=retain-on-failure`
flags bundle a failing test's screenshot and trace together per-test under
one `--output` folder — there is no built-in flag to split them
automatically into separate `artifacts/screenshots/`/`artifacts/traces/`
trees. Document this limitation rather than silently working around it:
use the plugin's own output folder for transient on-failure capture, and
hand-copy meaningful evidence (with a descriptive name) into
`artifacts/screenshots/`/`artifacts/traces/` for anything worth keeping
permanently.

Beyond failure evidence, also capture at least one set of screenshots
showing the automation actually executing the real happy path end to end —
e.g. the form freshly loaded, a validation-error state, the form filled
with valid data, and the real success message after Save (with whatever
value the application actually generated, not a placeholder). A short
one-off script driving the real `FormPage` through Playwright and calling
`.screenshot()` at each stage is sufficient; these do not need to be
wired into the pytest suite itself.

Configure/use Playwright traces under:

```text
artifacts/traces/
```

## Important rule

Only report results that were actually observed.

If a test fails, preserve the real failure information.

Do not fabricate:
- screenshots;
- reports;
- pass results;
- trace results.

## End condition

The project should have:
- a reproducible test command;
- real test results;
- screenshots where useful;
- an HTML report;
- trace evidence when debugging was required.
