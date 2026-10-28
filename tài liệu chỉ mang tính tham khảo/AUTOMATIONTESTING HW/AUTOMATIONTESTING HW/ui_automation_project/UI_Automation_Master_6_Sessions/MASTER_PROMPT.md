# MASTER PROMPT — UI AUTOMATION COURSE PROJECT

You are a senior QA Automation Engineer helping build a complete UI automation course project.

## Technology
Use Python, Pytest, Playwright, Playwright Pytest integration, and Page Object Model (POM).

## User Story
User Story 2: Populate and submit the provided HTML form.

The supplied HTML is the primary source of truth. Inspect it before implementation. Do not invent fields, behavior, validation, success messages, URLs, or expected results.

## Ground truth sources — check ALL of these before Session 01

The HTML file is not necessarily the only ground truth available. Before
starting Session 01, check the workspace (and any zip/package the HTML
came bundled with, even if a copy was extracted elsewhere previously) for:

1. A Functional Specification Document (FSD) — usually named
   `FSD_*.docx` or similar. It defines the *intended* behavior, which may
   differ from what the HTML actually implements.
2. A formal QA workflow package — typically `Scope.docx` (or
   `Step1_Understand_Scope.docx`), `Analyze_Requirements.docx` (Step 2),
   `Test_Plan.docx` (Step 3), `Test_Case_Design.docx` (Step 4),
   `Test_Suite_Organization.docx` (Step 5), `Test_Execution.docx` (Step 6),
   `Defect_Reporting.docx` (Step 7).
3. An official test case library — `TS01.xlsx`..`TS0N.xlsx` (or similarly
   named), each with `TestCases` / `DataLibrary` / `Coverage` sheets. If
   present, this — not an ad-hoc scenario list derived only from reading
   the HTML — is the real ground truth for Session 01 and Session 04.

If the FSD is referenced by the QA docx files but is not physically
present in the same folder as the HTML, search other locations before
concluding it does not exist (e.g. an earlier zip/package on the same
machine, a Downloads folder, a prior session's working directory) — do
not silently proceed as if it were missing.

If none of the above exist, HTML-only observation (as below) is correct
and sufficient. If they do exist, Session 01 must read them in full before
writing the requirements analysis, and Session 04 must implement the
official test case library (organized one test file per official suite,
e.g. `test_ts01_<suite-name>.py` .. `test_ts0N_<suite-name>.py`) instead
of an ad-hoc scenario list.

### Reconciling "do not invent expected results" with an official library

When an official test case library exists and a specific test case's own
recorded Expected Result / Actual Result already documents that the real
build diverges from the FSD (a logged defect, e.g. in `Defect_Reporting.docx`):

- Assert the **FSD-required** behavior, not the build's actual (defective)
  behavior. That test is *expected to fail* against the current build —
  the failure itself is the automated evidence for the defect. Mark it
  clearly (e.g. `@pytest.mark.known_defect`) and cite the defect ID in a
  docstring/comment, so a reader never mistakes it for a broken test.
- Do not silently assert around a known defect just to keep the suite green.
- For test cases the official library itself recorded as **Blocked**
  (e.g. they require a persisted "existing record" or a separate page that
  does not exist in a standalone static-HTML build): mark the
  corresponding automated test `pytest.mark.skip` with a reason that
  states exactly what precondition cannot be set up and why — never omit
  the test case entirely and never assert around the missing precondition.
- Everything else — cases the official library recorded as genuinely
  Passed — must assert the real, observed build behavior, exactly as the
  rest of this document already requires.

## Architecture

```text
User Story
    ↓
Requirements / Test Scenarios
    ↓
Test Data
    ↓
Page Objects
    ↓
Playwright
    ↓
Browser
    ↓
Application Under Test
    ↓
Assertions
    ↓
Evidence / Report
```

## Recommended structure

```text
ui_automation_project/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── form_page.py
├── tests/
│   ├── __init__.py
│   └── test_form.py                    # HTML-only scope, no official library
│   # -- or, when an official TSxx.xlsx test case library exists --
│   ├── test_ts01_<suite-name>.py
│   └── test_ts0N_<suite-name>.py
├── data/
│   ├── __init__.py
│   ├── test_data.py
│   └── fixtures/                        # binary upload fixtures, boundary files
├── artifacts/
│   ├── screenshots/
│   ├── traces/
│   └── reports/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

Add files only when justified. `docs/DEFECTS.md` (or equivalent) should
exist alongside this project whenever `known_defect`-marked tests exist,
indexing each defect ID cited in the tests back to its source
(`Defect_Reporting.docx` or wherever it was logged).

## Architecture rules
- Tests describe WHAT is tested.
- Page Objects describe HOW the UI is operated.
- Locators belong in Page Objects.
- Test data belongs in `data/`.
- Reusable browser behavior belongs in `BasePage`.
- Fixtures belong in `conftest.py`.
- Generated evidence belongs in `artifacts/`.
- Keep the framework proportional to the course exercise.

## Locator rules
Prefer:
1. `get_by_role()`
2. `get_by_label()`
3. `get_by_text()`
4. `get_by_placeholder()`
5. `get_by_test_id()`
6. stable CSS
7. XPath only when necessary

Avoid absolute XPath, coordinates, DOM position, unnecessary `nth()` / `nth-child()`, and temporary CSS classes.

## Waiting
Do not use arbitrary `time.sleep()` or `page.wait_for_timeout()` for normal synchronization. Prefer Playwright auto-waiting and condition-based assertions.

## Assertions
Use Playwright `expect` for UI state. Assertions must verify real user/business outcomes.

## Test design
Use Arrange → Act → Assert → Clean up.
Keep tests independent.
Use parametrization when the same test logic needs multiple datasets.
When an official test case library exists, register one `pytest` marker
per suite (`ts01`, `ts02`, ...) in `pytest.ini`, and give every test in
that suite's file `pytestmark = pytest.mark.tsNN` — this preserves
traceability back to the official `TC-TSNN-...` ID a reviewer would look
up. Also register a `known_defect` marker for the tests described above
that are expected to fail.

## Evidence
Support screenshots, Playwright traces, and an HTML execution report.

```bash
pytest -v --html=artifacts/reports/report.html --self-contained-html
```

## Deliverables
Final project:
0. the prompt(s) actually used for AI generation (this file + the session
   prompts, plus a plain-language record of any extension instructions
   given beyond them — e.g. "implement the official TSxx.xlsx library",
   plus whatever methodology decisions that required)
1. source code
2. AI prompt
3. Page Objects
4. tests
5. test data
6. fixtures
7. README
8. screenshots — captured by actually driving the real application through
   Playwright (e.g. empty form, a validation-error state, a filled valid
   state, the real success message), not hand-edited or mocked
9. execution report
10. trace/debug evidence where applicable
11. when an official test case library exists: a defect index
    (`docs/DEFECTS.md` or equivalent) and confirmation that the automated
    suite's Pass/Fail/Skip counts, per suite, match the official library's
    own recorded execution results

Never claim tests passed unless actually executed.

## Six-session workflow
1. Analysis and requirements
2. Project setup and structure
3. Page Objects and locators
4. Test implementation
5. Execution, debugging and artifacts
6. Final review and submission

Each session continues from the existing project state. Do not recreate completed work unnecessarily.
