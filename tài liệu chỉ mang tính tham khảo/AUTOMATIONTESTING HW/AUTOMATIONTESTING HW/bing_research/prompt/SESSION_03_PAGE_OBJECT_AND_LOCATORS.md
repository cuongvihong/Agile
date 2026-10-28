# SESSION 03 — PAGE OBJECTS AND LOCATORS

Continue from Sessions 01–02 and `MASTER_PROMPT.md`.

## Objective
Implement Page Objects for the exact current workflow using stable, verified locators.

## Page Objects

Create:

```text
BasePage
BingPage
MaivenPointPage
CommunityPage
```

## BingPage Responsibilities

Implement only:

- `open()`
- `search(keyword)`
- wait for Bing results
- `find_maivenpoint_result()` or an equivalent intent-based method
- `open_result(result)`

The MaivenPoint result must be identified by meaningful domain/text/URL information, not by result position.

## MaivenPointPage Responsibilities

Implement only:

- page-load verification/wait;
- cookie-consent handling when the banner blocks interaction;
- locate the `Community` link;
- click Community and capture the newly opened page/tab.

The observed cookie banner may contain `Accept All`. Handle it conditionally so the test does not fail when the banner is absent.

## CommunityPage Responsibilities

Implement:

- page-load waiting;
- locate the search field using the observed placeholder `Enter keywords to search...`;
- `search(keyword)`;
- submit with Enter;
- verify the actual observable post-search state.

## New Page Handling

Community opens a new page/tab. Use a popup/new-page wait around the click. Return the new `Page` object or construct a `CommunityPage` around it.

Do not continue searching on the original MaivenPoint page.

## Waiting

Use Playwright conditions instead of arbitrary sleeps. In particular:

```text
Community click
→ wait for new page
→ wait for page load
→ wait for search field visible
→ enter Hi
→ press Enter
```

## End Condition
The test can express the workflow clearly without exposing raw selectors:

```text
bing.open()
→ bing.search("MaivenPoint")
→ bing.find_maivenpoint_result()
→ bing.open_result()
→ maivenpoint.click_community()
→ community.search("Hi")
→ verify result
```
