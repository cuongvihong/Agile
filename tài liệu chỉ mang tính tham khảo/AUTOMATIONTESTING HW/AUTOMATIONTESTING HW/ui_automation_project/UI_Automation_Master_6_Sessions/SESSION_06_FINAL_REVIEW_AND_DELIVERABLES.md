# SESSION 06 — FINAL REVIEW AND SUBMISSION

Continue from Sessions 01–05.

## Objective
Perform a final QA review of the project and prepare the course submission.

## 1. Architecture review

Verify:

- tests are separate from Page Objects;
- BasePage contains only reusable behavior;
- FormPage contains form-specific locators/actions;
- test data is separated;
- fixtures are centralized;
- artifacts are separated.

## 2. Locator review

Check that:
- semantic/user-facing locators are preferred;
- fragile selectors are avoided;
- selectors are based on actual HTML;
- no unnecessary XPath or `nth-child()` is used.

## 3. Assertion review

Check that:
- every important action has an expected result;
- assertions verify actual UI/business outcomes;
- `expect` is used appropriately;
- no meaningless assertions exist.

## 4. Waiting review

Check:
- no unnecessary `sleep`;
- no arbitrary fixed waits;
- Playwright auto-waiting is used;
- asynchronous behavior has appropriate conditions.

## 5. Test review

Check:
- test names are meaningful;
- test IDs are unique;
- tests are independent;
- parametrization is used appropriately;
- no duplicated test logic;
- no hidden exception handling.

## 6. Execution review

Run the final suite.

Record the real result:

```text
Total:
Passed:
Failed:
Skipped:
Duration:
```

Do not invent numbers.

If an official test case library exists, additionally cross-check the
Pass/Fail/Skip counts **per suite** against that library's own recorded
execution result (e.g. `Test_Execution.docx`'s execution-summary table)
and state explicitly whether they match. A mismatch means something in
the automation needs investigation before sign-off, not that the official
record is assumed wrong.

## 7. Artifact review

Verify:

```text
artifacts/
├── screenshots/
├── traces/
└── reports/
```

The HTML report must actually exist if the project was executed with report generation.

## 8. README review

README must contain:

- project purpose;
- prerequisites;
- installation;
- browser installation;
- project structure;
- test scenarios;
- execution command;
- report command;
- debugging;
- evidence locations;
- assumptions.

## 9. Submission checklist

Prepare:

```text
[ ] the prompt(s) actually used for AI generation (this file + session
    prompts, plus a plain record of any extension instructions given
    beyond them)
[ ] project source files
[ ] HTML/application file if required
[ ] screenshots (must include genuine happy-path execution evidence, not
    only failure screenshots)
[ ] execution report
[ ] trace/debug evidence if required
[ ] README
[ ] requirements.txt
[ ] defect index (docs/DEFECTS.md or equivalent), if any known_defect
    tests exist
```

## 10. Final response

Provide:

### Project structure

Tree of the final project.

### Test cases

| ID | Scenario | Result |
|---|---|---|

Use actual execution results only. If an official test case library
exists, `ID` here is the official `TC-TSNN-...` ID, not a renumbered one.

### How to run

Exact commands.

### Evidence

Exact artifact locations.

### Known limitations

List anything not supported by the supplied HTML or environment.

Do not claim completion of an item that was not actually produced.
