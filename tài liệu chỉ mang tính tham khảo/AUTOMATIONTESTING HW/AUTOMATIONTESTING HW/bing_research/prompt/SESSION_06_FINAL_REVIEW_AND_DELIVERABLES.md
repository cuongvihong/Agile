# SESSION 06 — FINAL REVIEW AND SUBMISSION

Continue from Sessions 01–05 and `MASTER_PROMPT.md`.

## Objective
Perform a final QA review of the current User Story 1 implementation.

## 1. Architecture Review

Verify:

- tests contain workflow intent;
- `BingPage` contains Bing behavior;
- `MaivenPointPage` contains MaivenPoint behavior;
- `CommunityPage` contains Community behavior;
- new-page handling is implemented in the correct layer;
- test data is separated;
- fixtures are centralized;
- artifacts are separated.

## 2. Locator Review

Verify:

- semantic/user-facing locators are preferred;
- MaivenPoint result is identified by meaningful information;
- Community uses a stable locator;
- Community search uses the observed placeholder;
- no unnecessary `nth()` or absolute XPath exists.

## 3. Workflow Review

Confirm the final workflow is exactly:

```text
Bing
→ Search MaivenPoint
→ Open MaivenPoint result
→ Handle cookie consent if necessary
→ Click Community
→ NEW PAGE/TAB
→ Wait for load
→ Search Hi
→ Enter
→ Verify result/state
```

There must be no second Bing keyword.

## 4. Waiting Review

Check:

- no arbitrary sleeps;
- popup/new-page waiting is explicit;
- Community page loading is condition-based;
- search field visibility is waited for.

## 5. Assertion Review

Verify:

- Bing results;
- MaivenPoint result;
- target URL/domain;
- Community new page;
- Community search field;
- post-search observable result/state.

## 6. Final Execution

Run:

```bash
pytest -v
```

Record only actual results:

```text
Total:
Passed:
Failed:
Skipped:
Duration:
```

## 7. Artifact Review

Verify actual files under:

```text
artifacts/
├── screenshots/
├── traces/
└── reports/
```

## 8. README Review

README must document:

- User Story 1 workflow;
- prerequisites;
- installation;
- browser installation;
- project structure;
- test data;
- test execution;
- report generation;
- debugging;
- artifacts;
- limitations such as cookie banners or external-site behavior.

## 9. Final Response

Provide:

- final project structure;
- test-case ID and scenario;
- actual execution result;
- exact run commands;
- artifact locations;
- known limitations.

Never claim an artifact, pass result, or completion status that was not actually produced.
