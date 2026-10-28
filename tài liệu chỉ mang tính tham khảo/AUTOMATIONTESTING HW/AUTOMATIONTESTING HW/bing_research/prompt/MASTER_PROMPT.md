# MASTER PROMPT — MAIVENPOINT COMMUNITY UI AUTOMATION PROJECT

You are a senior QA Automation Engineer helping build a complete UI automation project named `bing_research`.

## Technology
Use Python, Pytest, Playwright, pytest-playwright, and Page Object Model (POM).

## User Story 1 — Current Ground Truth

Automate the following exact workflow:

1. Navigate to `https://www.bing.com/`.
2. Search for `MaivenPoint`.
3. Verify Bing search results are displayed.
4. Find the search result for the MaivenPoint website (`maivenpoint.com`).
5. Open the MaivenPoint website from the Bing result. Do not bypass Bing by directly navigating to the MaivenPoint URL.
6. Wait until the MaivenPoint page has loaded sufficiently for the Community link to be usable.
7. Handle the MaivenPoint cookie-consent banner if it blocks interaction. The observed banner contains `Accept All`, `Reject Non-Essential`, and `Manage Preferences`.
8. Click the `Community` link.
9. `Community` opens a new browser page/tab. Capture the newly opened page instead of continuing to use the original MaivenPoint page.
10. Wait for the new Community page to finish loading and for its search field to become visible.
11. Locate the Community search field with placeholder `Enter keywords to search...`.
12. Enter `Hi`.
13. Press `Enter` to submit the Community search.
14. Verify the search action produces the expected observable UI/navigation result available on the actual Community page.

### Workflow

```text
Bing
 ↓
Search "MaivenPoint"
 ↓
Verify Bing results
 ↓
Find MaivenPoint result
 ↓
Open MaivenPoint
 ↓
Wait for page load
 ↓
Handle cookie consent if blocking
 ↓
Click Community
 ↓
NEW PAGE / TAB
 ↓
Wait for Community page load
 ↓
Search "Hi"
 ↓
Press Enter
 ↓
Verify observable result
```

Do not add a second Bing keyword. The current User Story 1 has only one Bing search keyword: `MaivenPoint`.

## Ground Truth Rules

Before implementation, inspect the workspace and supplied files. Use the actual User Story, official test cases, supplied website behavior, and supplied project files as the source of truth.

Do not invent:

- a second Bing keyword;
- result positions;
- page elements;
- URLs not observed or required;
- expected results that cannot be observed;
- additional user actions.

If actual website behavior differs from the requirement, document the difference and adapt the automation only when necessary to execute the defined workflow.

## Current Observed Website Behavior

The following behavior has been observed during execution and may be implemented directly:

### Bing
- Bing search input may be identified using `#sb_form_q` or a more stable verified locator.
- Bing result container has been observed as `#b_results`.
- The MaivenPoint result should be identified by meaningful link/domain information, not a fixed result position.

### MaivenPoint
- The target site is the MaivenPoint website.
- The page contains a visible `Community` link.
- The Community link points to the Community site and opens a new page/tab in the current workflow.
- A cookie consent banner can block interaction on the MaivenPoint homepage.
- The banner can contain an `Accept All` button.

### Community
- The Community page is a separate page/tab.
- The search field placeholder is:

```text
Enter keywords to search...
```

- The required search keyword is:

```text
Hi
```

Use Playwright waiting and assertions rather than arbitrary sleeps.

## Page Object Architecture

Use page objects that match the actual workflow:

```text
pages/
├── __init__.py
├── base_page.py
├── bing_page.py
├── maivenpoint_page.py
└── community_page.py
```

Responsibilities:

- `BingPage`: open Bing, search MaivenPoint, wait for results, identify/open MaivenPoint result.
- `MaivenPointPage`: verify/load MaivenPoint, handle cookie consent, click Community, capture the new page.
- `CommunityPage`: wait for Community page, locate search field, enter keyword, submit search, verify the resulting observable state.
- `BasePage`: only reusable generic browser/page behavior that is actually needed.

Do not use a generic `TargetPage` when a site-specific Page Object makes the workflow clearer.

## New Page / Popup Handling

The Community link opens a new page/tab. Handle this explicitly.

Use Playwright's popup/page waiting mechanism, for example:

```python
with page.expect_popup() as popup_info:
    community_link.click()
community_page = popup_info.value
```

The exact mechanism must match the actual browser behavior observed during execution.

Do not assume that the original MaivenPoint page becomes the Community page.

## Waiting Rules

Do not use `time.sleep()` or arbitrary `page.wait_for_timeout()` for normal synchronization.

Prefer:

- Playwright auto-waiting;
- `expect(...).to_be_visible()`;
- `expect(page).to_have_url(...)`;
- `page.wait_for_load_state(...)` when appropriate;
- explicit waiting for a new page/popup;
- waiting for the Community search field to become visible.

A page-load delay requirement means the automation must wait for a reliable condition, not simply sleep for an arbitrary number of seconds.

## Locator Rules

Prefer, in order:

1. `get_by_role()`
2. `get_by_label()`
3. `get_by_text()`
4. `get_by_placeholder()`
5. `get_by_test_id()`
6. stable CSS
7. XPath only when necessary

Avoid:

- absolute XPath;
- coordinates;
- unnecessary `nth()`;
- `nth-child()`;
- temporary CSS classes;
- fixed result positions.

## Test Data

Keep reusable data in `data/test_data.py`:

```python
{
    "id": "TS01-001",
    "bing_keyword": "MaivenPoint",
    "target_domain": "maivenpoint.com",
    "community_search": "Hi"
}
```

Use Pytest parametrization if the project contains multiple datasets using the same workflow.

## Assertions

Verify meaningful observable outcomes:

- Bing search results are visible after searching `MaivenPoint`;
- the MaivenPoint result exists;
- the MaivenPoint page is opened;
- the Community link is available;
- a new Community page/tab is opened;
- the Community search field is visible after page loading;
- `Hi` is entered and submitted;
- the expected post-search UI/URL/result is observable.

Do not use unsupported assumptions as assertions.

## Test Structure

Use:

```text
Arrange
↓
Act
↓
Assert
↓
Clean up
```

Keep tests independent.

## Artifacts

The project must support real execution evidence:

```text
artifacts/
├── screenshots/
├── traces/
└── reports/
```

Support an HTML report, screenshots for meaningful states/failures, and Playwright traces when debugging or when the project requires trace evidence.

Example report command:

```bash
pytest -v --html=artifacts/reports/report.html --self-contained-html
```

If trace recording is configured, save traces under `artifacts/traces/`.

Never fabricate evidence or claim an artifact exists unless it was actually generated.

## Six-Session Workflow

1. Analysis and requirements
2. Project structure and setup
3. Page Objects and locators
4. Test implementation
5. Execution, debugging and artifacts
6. Final review and deliverables

Each session continues from the existing project state. Do not recreate completed work unnecessarily.
