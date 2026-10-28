# SESSION 02 — PROJECT STRUCTURE AND SETUP

Continue from Session 01 and preserve all completed analysis.

## Objective
Create the Playwright + Pytest project foundation.

## Create

```text
pages/
tests/
data/
data/fixtures/
artifacts/screenshots/
artifacts/traces/
artifacts/reports/
conftest.py
pytest.ini
requirements.txt
README.md
.gitignore
```

## Requirements

### requirements.txt
Include at minimum:

```text
pytest
pytest-playwright
pytest-html
```

### pytest.ini
Configure test discovery and useful markers if needed. If Session 01 found
an official test case library, register one marker per suite (`ts01`,
`ts02`, ...) here now, plus a `known_defect` marker — Session 04 will rely
on both existing already.

### conftest.py
Use Playwright Pytest fixtures. Add reusable fixtures only where useful.

### README.md
Document installation, browser installation, project structure, execution, reports, screenshots, traces, and assumptions.

### HTML handling
Use the actual supplied HTML file. If direct file loading works, use `Path.as_uri()`. If a local server is required, implement a simple documented approach.

## Do not
- duplicate browser setup in every test;
- create unnecessary framework layers;
- write final test cases before the Page Object design is ready.

## End condition
The project should have a clean skeleton and be ready for Session 03.
