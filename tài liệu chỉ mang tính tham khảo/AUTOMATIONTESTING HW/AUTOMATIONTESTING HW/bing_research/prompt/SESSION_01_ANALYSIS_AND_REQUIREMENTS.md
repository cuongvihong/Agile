# SESSION 01 — ANALYSIS AND REQUIREMENTS

Continue using `MASTER_PROMPT.md`.

## Objective
Analyze the exact User Story 1 workflow before writing automation code.

## Current User Story

```text
Bing
→ Search "MaivenPoint"
→ Verify search results
→ Find MaivenPoint website result
→ Open MaivenPoint
→ Wait for page load
→ Handle cookie consent if blocking
→ Click "Community"
→ Community opens a NEW page/tab
→ Wait for new page to load
→ Locate "Enter keywords to search..."
→ Enter "Hi"
→ Press Enter
→ Verify observable search result/state
```

There is NO second Bing keyword in the current User Story.

## Tasks

1. Inspect the actual User Story and supporting documents.
2. Confirm the official test ID, currently expected to be `TS01-001` when supported by the supplied test data.
3. Confirm `MaivenPoint` as the Bing keyword.
4. Confirm `maivenpoint.com` as the target-domain requirement.
5. Confirm `Hi` as the Community search keyword.
6. Identify the exact Community navigation behavior, including the new page/tab.
7. Identify the cookie-consent behavior observed on MaivenPoint.
8. Identify stable locators from the actual DOM.
9. Identify expected results after each action.
10. Identify loading, popup, redirect, and consent risks.

## Required Output

Document:

- ground-truth sources;
- exact workflow;
- test data;
- page/action inventory;
- expected results;
- locator candidates;
- new-page/popup behavior;
- cookie-consent behavior;
- risks and constraints;
- open questions.

Do not invent a second keyword or additional page actions.

## End Condition
Do not implement final automation until the exact workflow and expected results are understood.
