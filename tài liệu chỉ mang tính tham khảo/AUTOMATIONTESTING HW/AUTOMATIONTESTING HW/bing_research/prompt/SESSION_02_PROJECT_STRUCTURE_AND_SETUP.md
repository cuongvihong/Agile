# SESSION 02 — PROJECT STRUCTURE AND SETUP

Continue from Session 01 and `MASTER_PROMPT.md`.

## Objective
Create/configure the `bing_research` Playwright + Pytest project for the current User Story 1.

## Recommended Structure

```text
bing_research/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── bing_page.py
│   ├── maivenpoint_page.py
│   └── community_page.py
├── tests/
│   ├── __init__.py
│   └── test_user_story_01.py
├── data/
│   ├── __init__.py
│   └── test_data.py
├── artifacts/
│   ├── screenshots/
│   ├── traces/
│   └── reports/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

Add files only when justified by the actual workflow.

## Setup Tasks

Configure:

- Python virtual environment;
- Pytest;
- Playwright;
- pytest-playwright if used;
- browser installation;
- fixtures;
- test discovery;
- HTML reporting;
- trace/screenshot support.

## Browser Fixture Requirements

The fixture must allow the test to observe and handle a new page/tab created when Community is clicked.

Do not close the original page before the Community page is finished.

## Validation

Verify:

```bash
pytest --version
playwright --version
pytest --collect-only
```

Then run a minimal browser check.

## End Condition
The project can discover the User Story 1 test and launch Playwright successfully.
