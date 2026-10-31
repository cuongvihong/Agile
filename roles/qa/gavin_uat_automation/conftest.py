"""Fixtures of the Gavin UAT suite. One fixture, `uat`, gives a test the recorder with video, banner and step evidence.

Run from this folder:   python -m pytest -q --alluredir artifacts/allure-results
Headed (watch it live): python -m pytest -q --headed
One case:               python -m pytest -q -k UAT_PAR_01_N3     (or  -m "case" with the marker text)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import allure
import pytest

from data.pre_cases_meta import PRE_CASES
from data.uat_cases_meta import UAT_CASES
from uat import env
from uat.recorder import BLOCKED, FAIL, GAP, PASS, UatRun


def pytest_addoption(parser):
    parser.addoption("--uat-case", action="store", default="",
                     help="Run only these UAT cases. Comma separated, wildcards allowed: UAT-PAR-01, UAT-PAR-*, UAT-MOE-05*")


def pytest_collection_modifyitems(config, items):
    import fnmatch
    import os
    wanted = [w.strip() for w in config.getoption("--uat-case").split(",") if w.strip()]

    def case_of(item):
        marker = item.get_closest_marker("case")
        return marker.args[0] if marker and marker.args else ""

    if wanted:
        keep, drop = [], []
        for item in items:
            cid = case_of(item)
            # The precondition cases (UAT-PRE-*) always come along unless UAT_SEED=0, because the UAT cases rely on their data.
            pre = cid.startswith("UAT-PRE") and os.environ.get("UAT_SEED", "1") != "0"
            (keep if pre or any(fnmatch.fnmatchcase(cid.upper(), w.upper()) for w in wanted) else drop).append(item)
        if not any(not case_of(i).startswith("UAT-PRE") for i in keep) and not any(w.upper().startswith("UAT-PRE") for w in wanted):
            raise pytest.UsageError(f"--uat-case {wanted} matches no case. Ids look like UAT-PAR-01 or UAT-SCH-03-N1.")
        config.hook.pytest_deselected(items=drop)
        items[:] = keep
    items.sort(key=lambda i: 0 if case_of(i).startswith("UAT-PRE") else 1)  # stable: preconditions first


def pytest_sessionstart(session):
    try:
        env.assert_all_local()
    except RuntimeError as exc:
        raise pytest.UsageError(str(exc)) from exc


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Slow every action a little so that the video is easy to follow."""
    return {**browser_type_launch_args, "slow_mo": env.SLOW_MO_MS}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def uat(request, browser):
    marker = request.node.get_closest_marker("case")
    if marker is None or not marker.args:
        pytest.fail("A UAT test needs @pytest.mark.case('UAT-...')", pytrace=False)
    case_id = marker.args[0]
    meta = UAT_CASES.get(case_id) or PRE_CASES[case_id]
    allure.dynamic.title(f"{case_id}: {meta['title']}")
    allure.dynamic.feature(meta["area"])
    allure.dynamic.story(meta["role"])
    allure.dynamic.severity(allure.severity_level.BLOCKER if meta["severity1"] else allure.severity_level.NORMAL)
    allure.dynamic.description(
        f"Setup and data (master)\n{meta['setup']}\n\nGate\n{meta['gate']}\n\n"
        "Steps (master)\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(meta["steps"], 1)) + "\n\n"
        "Expected (master)\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(meta["expected"], 1)))
    run = UatRun(case_id, meta, browser, planned_steps=len(meta["steps"]))
    # Environment gate: when the address of this case does not answer, the case is BLOCKED (not FAIL), because no product behaviour was seen.
    need = env.ADMIN_URL if case_id.startswith(("UAT-MOE", "UAT-SCH", "UAT-PRE", "UAT-031", "UAT-033")) else env.PARENT_URL
    down = env.unreachable_reason(need)
    if down:
        try:
            run.blocked("The test environment answers", down, expected="The address of this case opens.")
            run.conclude()
        except BaseException:
            run.close()
            raise
    yield run
    call = getattr(request.node, "rep_call", None)
    run.close(failed=bool(call and call.failed))


def pytest_terminal_summary(terminalreporter):
    import json
    if not env.RESULTS_JSON.exists():
        return
    try:
        data = json.loads(env.RESULTS_JSON.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return
    counts = {PASS: 0, FAIL: 0, BLOCKED: 0, GAP: 0}
    for row in data.values():
        counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1
    terminalreporter.section("UAT verdicts (artifacts/uat_results.json)")
    terminalreporter.write_line(
        f"cases recorded: {len(data)}   PASS {counts[PASS]}   FAIL {counts[FAIL]}   BLOCKED {counts[BLOCKED]}   GAP {counts[GAP]}")
    for row in sorted(data.values(), key=lambda r: r["id"]):
        if row["verdict"] != PASS:
            terminalreporter.write_line(
                f"  {row['verdict']:<8}{row['id']:<18}steps {row['steps_pass']}/{row['steps_total']} pass")
