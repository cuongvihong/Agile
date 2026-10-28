# Bing Research — MaivenPoint Community UI Automation Project

End-to-end UI automation testing suite for **User Story 1: Bing Search to MaivenPoint Community Portal Workflow**. Built with **Python**, **Pytest**, **Playwright**, and the **Page Object Model (POM)** pattern, including **pytest-html** and **Allure** reporting.

---

## 1. User Story 1 Workflow

```text
Bing (https://www.bing.com/)
 └── Search "MaivenPoint"
      └── Verify Bing search results (#b_results)
           └── Locate & click MaivenPoint result (maivenpoint.com)
                └── Wait for MaivenPoint page load
                     └── Handle cookie-consent banner (Accept All) if present
                          └── Click "Community" link
                               └── [NEW PAGE / TAB] opens
                                    └── Wait for Community page load
                                         └── Locate search field ("Enter keywords to search...")
                                              └── Enter "Hi" and press Enter
                                                   └── Verify observable post-search result / state
```

### Key Ground Truth Rules Followed
- **Single Bing Keyword**: Searches `MaivenPoint` only (no arbitrary secondary search).
- **Target Link Resolution**: Dynamic brand/domain matching (`maivenpoint.com`) instead of brittle fixed indices.
- **Multi-Tab / Popup Handling**: Explicitly captures new pages spawned with `target="_blank"` using `expect_page()`.
- **Dynamic Waiting**: Zero arbitrary `time.sleep()`. Relies on Playwright auto-waiting, visibility assertions, and URL matching.

---

## 2. Project Architecture

```text
bing_research/
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base Page Object with screenshot & cookie handlers
│   ├── bing_page.py             # Bing navigation, search, and dynamic result finder
│   ├── maivenpoint_page.py      # MaivenPoint page, cookie consent, and Community link
│   └── community_page.py        # Community portal, search submission, and result assertions
├── tests/
│   ├── __init__.py
│   └── test_user_story_01.py    # E2E test with Allure steps & screenshot attachments
├── data/
│   ├── __init__.py
│   └── test_data.py             # Parametrized test data definition (TS01-001)
├── artifacts/
│   ├── screenshots/             # Step-by-step PNG screenshots
│   ├── reports/                 # Standalone self-contained HTML report
│   ├── allure-results/          # Allure raw JSON & attached PNG artifacts
│   └── allure-report/           # Compiled static Allure HTML report
├── prompt/                      # Original master prompt and 6 session specifications
├── conftest.py                  # Pytest fixtures and browser context options
├── pytest.ini                   # Pytest runner configuration
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## 3. Technology Stack & Prerequisites

- **Python**: 3.10+ (tested with Python 3.14)
- **Pytest**: >= 8.0
- **Playwright**: >= 1.40
- **pytest-playwright**: Playwright integration for Pytest
- **pytest-html**: Self-contained HTML report generator
- **allure-pytest & Allure CLI**: Interactive test execution reporting and analytics

---

## 4. Setup & Installation

### Step 1: Activate Virtual Environment
From workspace root:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r bing_research/requirements.txt
```

### Step 3: Install Playwright Browsers
```powershell
playwright install chromium
```

---

## 5. Running the Tests

Navigate to `bing_research/`:
```powershell
cd d:\AIQA\AUTOMATIONTESTING HW\bing_research
```

### Run All Tests
```powershell
pytest -v
```

### Generate Standalone HTML Report
Configured automatically via `pytest.ini`:
```powershell
pytest -v --html=artifacts/reports/report.html --self-contained-html
```

### Generate & View Allure Report
1. Execute tests and record Allure results:
   ```powershell
   pytest -v --alluredir=artifacts/allure-results
   ```
2. Build the Allure static report:
   ```powershell
   allure generate artifacts/allure-results -o artifacts/allure-report --clean
   ```
3. Open/serve the Allure report in your browser:
   ```powershell
   allure open artifacts/allure-report
   ```

---

## 6. Execution Evidence & Artifacts

All test runs automatically capture and store evidence:
- **Screenshots** (`artifacts/screenshots/`):
  - `01_bing_results.png`: Bing search results page.
  - `02_maivenpoint_homepage.png`: Official MaivenPoint homepage.
  - `03_community_portal.png`: MaivenPoint Community homepage in new tab.
  - `04_community_search_results.png`: Post-search page with keyword query and discussion items.
- **HTML Report**: [report.html](artifacts/reports/report.html)
- **Allure Report**: [index.html](artifacts/allure-report/index.html)
