# SESSION 04 — TEST DATA AND TEST IMPLEMENTATION

Continue from Sessions 01–03.

## Objective
Implement the actual test cases.

## If an official test case library exists (from Session 01)

This changes the scope of this session from "implement a reasonable
scenario list" to "implement the official library faithfully":

- Create one test file per official suite (`test_ts01_<suite-name>.py` ..
  `test_ts0N_<suite-name>.py`), mirroring the library's own suite names
  and TC IDs in test function names/docstrings — a reviewer should be able
  to find `TC-TS01-PI-005` by searching for it in the test file directly.
- Transcribe the official `DataLibrary` sheet's datasets into
  `data/test_data.py` verbatim (keep the same dataset IDs, e.g.
  `TD_TRAINER_001`), not a reinvented equivalent. If a dataset is missing
  a field the real form requires (a real gap found in one project: the
  library omitted 3 mandatory fields entirely), fill the gap explicitly
  and say so in a comment — do not silently invent unrelated values.
- For each official TC: implement the interaction it describes, then
  assert per the "Reconciling..." rules in the Master Prompt (FSD-required
  behavior + `known_defect` marker for cases the library recorded Failed;
  `pytest.mark.skip` with a cited reason for cases recorded Blocked;
  real observed behavior for everything else).
- Run each suite for real as soon as it's written and compare its
  Pass/Fail/Skip counts against the official library's own execution
  record (`Test_Execution.docx` or equivalent) before moving to the next
  suite — do not write all suites first and check numbers only at the end.
- It is normal and expected for a boundary-value test case to reveal that
  an HTML `maxlength` attribute coincides with (and defeats) the exact
  boundary being tested through `.fill()` — see Session 03's raw-value
  escape hatch. Check for this whenever a boundary test's real result
  doesn't match the official library's recorded result: it is more likely
  a testability issue in the automation than an error in the official
  record.

If no official test case library exists, proceed with the sections below
exactly as written (HTML-only scope).

## Test data

Create `data/test_data.py`.

Keep reusable test data outside test functions.

Use fake data only.

## Test structure

Tests must follow:

```text
Arrange
↓
Act
↓
Assert
```

## Minimum test

Implement the valid form submission scenario:

1. open form;
2. populate valid data;
3. select/check required controls;
4. submit;
5. verify the actual expected result.

## Additional tests

Implement validation tests only when supported by the actual HTML, such as:
- required field missing;
- invalid email;
- invalid format;
- boundary values.

Do not invent requirements.

## Parametrization

Use `pytest.mark.parametrize` where multiple datasets share identical logic.

## Assertions

Use:

```python
from playwright.sync_api import expect
```

Prefer UI-aware assertions such as:

```python
expect(locator).to_be_visible()
expect(locator).to_be_enabled()
expect(page).to_have_url(...)
```

## Test independence

Each test must establish its own required state.

## Code quality

Avoid:
- duplicated locators;
- duplicated form-filling code;
- fixed sleeps;
- broad exception swallowing;
- giant test functions.

At the end of this session, the complete test suite should be implemented and ready to execute.
