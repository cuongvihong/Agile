# SESSION 04 — TEST DATA AND TEST IMPLEMENTATION

Continue from Sessions 01–03 and `MASTER_PROMPT.md`.

## Objective
Implement the actual User Story 1 test.

## Test Data

Use:

```python
TEST_CASES = [
    {
        "id": "TS01-001",
        "bing_keyword": "MaivenPoint",
        "target_domain": "maivenpoint.com",
        "community_search": "Hi",
    }
]
```

Do not add `keyword2` because it is not part of the current User Story.

## Main Test Flow

1. Navigate to Bing.
2. Search `MaivenPoint`.
3. Verify Bing results.
4. Find the MaivenPoint result.
5. Open the result.
6. Verify the MaivenPoint domain/page.
7. Wait for the page to be usable.
8. Handle cookie consent if it blocks the Community link.
9. Click Community.
10. Capture the NEW page/tab.
11. Wait for the Community page to load.
12. Locate the Community search field.
13. Enter `Hi`.
14. Press Enter.
15. Verify the actual post-search UI/URL/result.

## Test Structure

Use Arrange → Act → Assert.

## Important Rule

The test must not:

- directly navigate to MaivenPoint;
- search a second keyword on Bing;
- reuse the original page for Community after a new tab is opened;
- use arbitrary sleeps to wait for the Community page;
- invent a post-search result.

## Parametrization

Keep Pytest parametrization if additional approved datasets are introduced.

## End Condition
The exact current User Story 1 is implemented and ready for real execution.
