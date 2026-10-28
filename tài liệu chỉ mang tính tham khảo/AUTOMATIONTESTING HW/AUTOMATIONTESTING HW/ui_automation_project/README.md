# Curricula Trainer Account — UI Automation Project

## Purpose

Playwright + Pytest (Page Object Model) suite automating User Story 2: populate and
submit the "Create Trainer Account" HTML form (`curricula_trainer_account.html`). Built
across 6 sessions from `../UI_Automation_Master_6_Sessions/`; full field inventory,
locator-strategy justification, and the source scenario table live in
`../docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md`.

## Prerequisites

- Python 3.10+ (this project was built and run against 3.10.12).
- Linux/macOS/Windows with a shell that supports the shared virtual environment layout
  below (no OS-specific code is used anywhere in the suite).
- No local web server, no database, no network access — the AUT is a single static
  HTML file with no `<form>`, no `fetch`/`XHR`, and no external assets, so it is loaded
  directly via a `file://` URL (Session 01 analysis, §1).

## Installation

This project reuses the shared virtual environment at the workspace root
(`../.venv`), not a venv inside this folder.

```bash
cd "AUTOMATIONTESTING HW"
./.venv/bin/pip install -r ui_automation_project/requirements.txt
```

### Browser installation

```bash
./.venv/bin/playwright install chromium
```

> **Known environment issue on this machine**: a global `PYTHONPATH` set by ROS Humble's
> shell setup leaks into every Python process regardless of venv isolation, which breaks
> pytest's plugin autodiscovery (`ModuleNotFoundError: No module named 'yaml'` from an
> unrelated `launch_testing` package). Always run pytest/python with `PYTHONPATH` unset:
> ```bash
> env -u PYTHONPATH ./.venv/bin/python -m pytest
> ```
> This is an environment quirk of this particular machine, unrelated to the project itself.

## Project structure

```text
ui_automation_project/
├── pages/
│   ├── base_page.py        # generic, reusable page operations
│   └── form_page.py        # Trainer Account form: locators, actions, result readers
├── tests/
│   └── test_form.py        # 18 test cases, see "Test scenarios" below
├── data/
│   ├── test_data.py        # VALID_SG_DATA / VALID_NON_SG_DATA + override helpers
│   └── fixtures/            # valid-id.pdf, invalid-type.txt (upload fixtures)
├── artifacts/
│   ├── screenshots/         # meaningful, hand-kept evidence (see below)
│   ├── traces/               # meaningful, hand-kept evidence (see below)
│   └── reports/              # pytest-html output
├── conftest.py               # fixtures: aut_url, form_page (a FormPage, pre-navigated)
├── pytest.ini
├── requirements.txt
└── .gitignore
```

The AUT itself is **not** copied into this project — it stays at
`../UI_Automation_Master_6_Sessions/curricula_trainer_account.html` and is loaded via a
`file://` URL resolved relative to this project's own path (`conftest.py`).

## Test scenarios

Full detail (preconditions/test data/expected result) is in
`../docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md`, §5. Implemented in
`tests/test_form.py`:

| ID | Scenario |
|---|---|
| TS-01 | Valid submission, Singapore resident (also proves the postal-code auto-fill side effect) |
| TS-02 | Valid submission, Non-Singapore resident |
| TS-03 | Submit with all required fields empty |
| TS-04 | Invalid email format |
| TS-05 | Primary phone wrong length for +65 |
| TS-06 | Secondary phone optional when left blank |
| TS-07 | Secondary phone invalid when filled |
| TS-08 | Date of birth in the future |
| TS-09 | Invalid postal code format (Singapore branch) |
| TS-10 | Floor/Unit both blank, checkbox unchecked |
| TS-11 | "Floor/Unit not applicable" checkbox bypasses that validation |
| TS-12 | Non-Singapore branch: Address line 1 / City required |
| TS-14 | ID document upload: wrong file type rejected |
| TS-15 | ID document upload: no file selected |
| TS-16 | Cancel with no data entered: no confirm dialog, direct reload |
| TS-17 | Cancel with data entered: confirm dialog dismiss keeps value / accept clears it |
| TS-18 | Postal-code auto-fill only fires for the 3 hardcoded known codes |

(TS-13 and TS-19 from the Session 01 scenario list are covered as extra assertions
inside TS-02 and were not given standalone tests, to avoid duplicating form-filling code
for a single additional assertion — see `tests/test_form.py`.)

## How to run

```bash
cd ui_automation_project
env -u PYTHONPATH ../.venv/bin/python -m pytest -v
```

`pytest.ini` already applies on every run, no extra flags needed:

```ini
addopts =
    -ra
    --html=artifacts/reports/report.html
    --self-contained-html
    --screenshot=only-on-failure
    --tracing=retain-on-failure
    --output=artifacts/test-results
```

To run a single test: `env -u PYTHONPATH ../.venv/bin/python -m pytest -v -k ts01`.

## Reports, screenshots, traces (evidence locations)

- **HTML execution report**: `artifacts/reports/report.html` — regenerated on every run.
- **On-failure capture**: `pytest-playwright` writes a bundled screenshot + trace per
  failing test under `artifacts/test-results/<test>/`. This is transient/not committed —
  there is no built-in flag to split it automatically into separate top-level
  `screenshots/`/`traces/` trees (a real limitation of the plugin, disclosed rather than
  silently worked around).
- **`artifacts/screenshots/` / `artifacts/traces/`**: hand-picked, meaningfully-named
  copies of evidence worth keeping permanently. Currently contains real evidence from a
  disclosed debugging exercise performed in Session 05 (see
  `../docs/SESSION_05_EXECUTION_DEBUGGING_AND_ARTIFACTS.md`):
  `ts01_debug-exercise_block-number-assertion-failure.png` / `.zip`.

## Debugging

If a test fails:
1. Read the pytest failure message and identify the exact failing assertion/action.
2. Re-run only that test: `pytest -v -k <test-id-or-name>`.
3. Inspect the locator involved in `pages/form_page.py` against the actual markup in
   `curricula_trainer_account.html`.
4. Check element visibility/enabled state and whether the residential-type branch
   (Singapore vs Non-Singapore) matches what the test expects.
5. Check the trace/screenshot generated automatically at
   `artifacts/test-results/<test>/` (real evidence, produced by `pytest.ini`'s
   `--screenshot=only-on-failure --tracing=retain-on-failure`).
6. Open the trace with `playwright show-trace <path-to-trace.zip>` for a full timeline
   and DOM snapshots.
7. Do not paper over a real failure with `sleep()`/bigger timeouts/retries — find the
   actual cause first (see the worked example in
   `../docs/SESSION_05_EXECUTION_DEBUGGING_AND_ARTIFACTS.md`).

## Fixtures (`conftest.py`)

- `aut_url`: resolves and returns the `file://` URI for the supplied HTML, failing
  loudly (`pytest.fail`) if the file has moved.
- `form_page`: a `FormPage` Page Object (see `pages/form_page.py`) already navigated to
  the AUT, fresh per test. Browser/context lifecycle itself is handled entirely by
  `pytest-playwright`'s built-in fixtures — no manual setup/teardown code exists in this
  project, per the rule against duplicating browser setup per test.

## Assumptions and known limitations

- Trainer ID on success is randomly generated (`TRN` + 6 digits) — tests assert the
  pattern `TRN\d{6}`, never an exact value.
- Most `<label>` elements in the AUT are **not** programmatically associated with their
  inputs (no `for` attribute, input not wrapped) — verified by reading the raw markup.
  `get_by_label()` does not resolve most fields as a result. `pages/form_page.py` uses
  CSS `id` selectors for these (justified: the AUT's own script depends on the same
  ids), and `get_by_role()` for real buttons and the radios/checkbox whose `<label>`
  does wrap the input. Full per-field table: Session 01 doc, §3.
- File-type rejection (TS-14) relies on Chromium reporting a non-allowed MIME type for
  a `.txt` file — this is environment-dependent in principle, but was verified to work
  as expected in this Chromium build (130.0.6723.31) during real test execution.
- No NRIC/postal-code/phone-number *semantic* validation exists in the AUT beyond
  digit-count and regex checks already documented in Session 01 — the suite does not
  test any stronger validation than what the app's own JavaScript actually implements.
- Single browser (Chromium) is exercised; `pytest-playwright` supports
  `--browser firefox`/`webkit` but cross-browser runs were not performed this session.
