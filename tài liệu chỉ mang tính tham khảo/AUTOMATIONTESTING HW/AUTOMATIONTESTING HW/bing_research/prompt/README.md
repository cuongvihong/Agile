# bing_research — Revised Prompt Set

This prompt set is aligned with the current User Story 1 and the actual website behavior observed during execution.

## Current User Story 1

`Bing → Search MaivenPoint → Open MaivenPoint → Handle cookie consent → Click Community → NEW PAGE/TAB → Wait for load → Search Hi → Enter → Verify result/state`

There is no second Bing keyword.

## Prompt order

1. `MASTER_PROMPT.md`
2. `SESSION_01_ANALYSIS_AND_REQUIREMENTS.md`
3. `SESSION_02_PROJECT_STRUCTURE_AND_SETUP.md`
4. `SESSION_03_PAGE_OBJECT_AND_LOCATORS.md`
5. `SESSION_04_TEST_IMPLEMENTATION.md`
6. `SESSION_05_EXECUTION_DEBUGGING_AND_ARTIFACTS.md`
7. `SESSION_06_FINAL_REVIEW_AND_DELIVERABLES.md`

## Important observed behavior

- MaivenPoint may display a cookie-consent banner that blocks interaction.
- Clicking `Community` opens a new page/tab.
- The Community search field uses the placeholder `Enter keywords to search...`.
- The required Community search keyword is `Hi`.
- The automation should wait for reliable page/UI conditions instead of using arbitrary sleeps.
