# SESSION 05 — EXECUTION, DEBUGGING AND ARTIFACTS

Continue from Sessions 01–04 and `MASTER_PROMPT.md`.

## Objective
Run the current User Story 1, diagnose failures, and generate real evidence.

## Run

```bash
pytest -v
```

## HTML Report

```bash
pytest -v --html=artifacts/reports/report.html --self-contained-html
```

## Debugging Order

For each failure:

1. Read the failure message.
2. Identify the exact workflow step.
3. Inspect the actual page/DOM.
4. Verify the locator.
5. Verify page navigation and URL.
6. Verify cookie-consent state.
7. Verify whether Community opened a new page/tab.
8. Verify that the test switched to the new page.
9. Verify that the Community search field is visible.
10. Verify that `Hi` was entered and submitted.
11. Rerun the failing test.

## Common Current Workflow Failure Points

### Bing

Check:

- search input;
- `MaivenPoint` submission;
- results container;
- MaivenPoint result locator.

Do not rely on a fixed result index.

### MaivenPoint

Check:

- target URL/domain;
- page loading;
- cookie banner;
- `Community` link;
- whether Community opens a new tab/page.

### Community

Check:

- new page object;
- page load state;
- placeholder `Enter keywords to search...`;
- `Hi` input;
- Enter submission;
- actual post-search state.

## Waiting

Do not fix failures by adding arbitrary `sleep()` calls. Wait for reliable UI/navigation conditions.

## Evidence

Store real evidence under:

```text
artifacts/
├── screenshots/
├── traces/
└── reports/
```

Capture useful states such as:

```text
Bing search results
→ MaivenPoint page
→ Community new page
→ Community search result/state
```

Never fabricate evidence or pass results.
