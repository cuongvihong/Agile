"""Environment and test data of the UAT Master 01 suite.

Every value comes from data/env_data.json and can be overridden by an environment variable (UAT_*).
The suite targets the hosted test environment by default. The addresses below are the ones the
team uses for UAT; nothing else is contacted.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ARTIFACTS = ROOT / "artifacts"
VIDEOS_DIR = ARTIFACTS / "videos"
RAW_VIDEOS_DIR = ARTIFACTS / "_raw_videos"
SHOTS_DIR = ARTIFACTS / "screenshots"
RESULTS_JSON = ARTIFACTS / "results.json"
STATE_JSON = ARTIFACTS / "run_state.json"
DISCOVERY_JSON = ARTIFACTS / "discovery.json"
MASTER_JSON = DATA_DIR / "master01_cases.json"

ENV_DATA: dict = json.loads((DATA_DIR / "env_data.json").read_text(encoding="utf-8"))


def _env(name: str, default):
    value = os.environ.get(name)
    return default if value in (None, "") else value


ADMIN_URL = _env("UAT_ADMIN_URL", ENV_DATA["urls"]["admin"]).rstrip("/")
PARENT_URL = _env("UAT_PARENT_URL", ENV_DATA["urls"]["eservice"]).rstrip("/")
GATEWAY_HOST = _env("UAT_GATEWAY_HOST", ENV_DATA["urls"]["gateway_host"])

ADMIN_LOGIN_MODE = _env("UAT_ADMIN_LOGIN", ENV_DATA["admin_login"]["mode"])  # microsoft | password
HQ_ACCOUNT = _env("UAT_HQ_ACCOUNT", ENV_DATA["admin_login"]["hq_account"])
SCHOOL_ACCOUNT = _env("UAT_SCHOOL_ACCOUNT", ENV_DATA["admin_login"]["school_account"])
HQ_USER = _env("UAT_HQ_USER", ENV_DATA["admin_login"]["hq_user"])
HQ_PASS = os.environ.get("UAT_HQ_PASS", "")
SCHOOL_USER = _env("UAT_SCHOOL_USER", ENV_DATA["admin_login"]["school_user"])
SCHOOL_PASS = os.environ.get("UAT_SCHOOL_PASS", "")

# Run tag: makes the names of schemes created by this run unique, so a rerun never collides.
RUN_TAG = _env("UAT_RUN_TAG", time.strftime("%m%d%H%M"))

# Pace of the recorded video.
SLOW_MO_MS = int(_env("UAT_SLOW_MO", "150"))
STEP_PAUSE_MS = int(_env("UAT_STEP_PAUSE", "900"))
HEADED = os.environ.get("UAT_HEADED") == "1"
VIEWPORT = {"width": 1366, "height": 800}

# A step whose function exists under another screen name or layout is PASS with the flag EQUIV.
# UAT_STRICT_NAMES=1 turns those into GAP (and GAP counts as FAIL, rule of 30/10/2026).
STRICT_NAMES = os.environ.get("UAT_STRICT_NAMES") == "1"

# The suite only approves or rejects FAS applications it created itself. Set to 1 to let it act on
# any pending allocation of the school (the decision cannot be undone from the UI).
ALLOW_FOREIGN_APPS = os.environ.get("UAT_ALLOW_FOREIGN_APPS") == "1" or bool(ENV_DATA.get("allow_foreign_applications"))

# Precondition top-ups (HQ Individual Top-Up). Set UAT_NO_TOPUP=1 to forbid them; the cases that need
# a low balance then become BLOCKED when the balance does not match.
ALLOW_TOPUP = os.environ.get("UAT_NO_TOPUP") != "1"

# Persona discovery (scan every Singpass test persona once to find a 16 year old child, a PR child,
# a family with two children without an application). Cached for the day in artifacts/discovery.json.
ALLOW_DISCOVERY = os.environ.get("UAT_NO_DISCOVERY") != "1"

for d in (ARTIFACTS, VIDEOS_DIR, RAW_VIDEOS_DIR, SHOTS_DIR):
    d.mkdir(parents=True, exist_ok=True)


def data(*keys, default=None):
    """Read a nested value of env_data.json, for example data('pay', 'child')."""
    node = ENV_DATA
    for k in keys:
        if not isinstance(node, dict) or k not in node:
            return default
        node = node[k]
    return node
