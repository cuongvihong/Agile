"""Environment of the Gavin UAT suite. Every value can be changed with an environment variable.

DEFAULT ADDRESSES are the hosted test environment (Admin https://admin.20-255-158-192.sslip.io, e-Service https://eservice.20-255-158-192.sslip.io). Set UAT_ADMIN_URL and UAT_PARENT_URL for localhost.
OTHER HOSTS ARE REFUSED. The suite stops before it opens a browser when any address is not localhost, 127.0.0.1, [::1]
or a *.localhost name. vercel.app is refused for good. A machine in a private network (for example a Radmin IP)
is allowed only with UAT_ALLOW_REMOTE=1.
A hosted test environment is allowed host by host with UAT_ALLOW_HOSTS (comma separated exact host names), for example
UAT_ALLOW_HOSTS=admin.20-255-158-192.sslip.io,eservice.20-255-158-192.sslip.io. Any other host is still refused.
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
VIDEOS_DIR = ARTIFACTS / "videos"
SHOTS_DIR = ARTIFACTS / "screenshots"
RAW_VIDEOS_DIR = ARTIFACTS / "_raw_videos"
ALLURE_DIR = ARTIFACTS / "allure-results"
RESULTS_JSON = ARTIFACTS / "uat_results.json"

ADMIN_URL = os.environ.get("UAT_ADMIN_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
PARENT_URL = os.environ.get("UAT_PARENT_URL", "https://eservice.20-255-158-192.sslip.io").rstrip("/")
CHECKOUT_URL = os.environ.get("UAT_CHECKOUT_URL", "http://localhost:5176").rstrip("/")

# Admin Portal accounts of the IAM seed (04_SeedUsers.sql). Not real passwords of a live system.
HQ_USER = os.environ.get("UAT_HQ_USER", os.environ.get("R4_HQ_USER", "moehq"))
HQ_PASS = os.environ.get("UAT_HQ_PASS", os.environ.get("R4_HQ_PASS", "123456"))
SCHOOL_USER = os.environ.get("UAT_SCHOOL_USER", os.environ.get("R4_SCHOOL_USER", "school"))
SCHOOL_PASS = os.environ.get("UAT_SCHOOL_PASS", os.environ.get("R4_SCHOOL_PASS", "123456"))

# The page objects copied from the R4 suite read these names. Keep them equal to the UAT accounts.
os.environ.setdefault("R4_HQ_USER", HQ_USER)
os.environ.setdefault("R4_HQ_PASS", HQ_PASS)
os.environ.setdefault("R4_SCHOOL_USER", SCHOOL_USER)
os.environ.setdefault("R4_SCHOOL_PASS", SCHOOL_PASS)

# MockPass persona of the parent that owns the R9 seed children (R9-STU-01 ... R9-STU-14). A persona is not a password.
PARENT_NRIC = os.environ.get("UAT_PARENT_NRIC", "S7890123F")

# Pace of the recorded video. SLOW_MO slows every Playwright action, STEP_PAUSE holds the screen after each step
# so that the banner can be read in the video.
SLOW_MO_MS = int(os.environ.get("UAT_SLOW_MO", "250"))
STEP_PAUSE_MS = int(os.environ.get("UAT_STEP_PAUSE", "1200"))
VIEWPORT = {"width": 1366, "height": 768}
VIDEO_SIZE = {"width": 1366, "height": 768}

def _is_local_host(url: str) -> bool:
    host = (urlparse(url if "://" in url else f"http://{url}").hostname or "").lower()
    return host in {"localhost", "127.0.0.1", "::1", "[::1]"} or host.endswith(".localhost")


# Test data created or changed in the database by the payment cases. Needs Docker with edufams-qa-sqlserver, so it is off automatically when the e-Service address is not localhost.
ALLOW_DB = os.environ.get("UAT_NO_DB") != "1" and _is_local_host(PARENT_URL)

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]"}
FORBIDDEN_SUFFIXES = (".vercel.app", ".vercel.sh", ".now.sh")
ALLOW_REMOTE = os.environ.get("UAT_ALLOW_REMOTE") == "1"
DEFAULT_HOSTS = "admin.20-255-158-192.sslip.io,eservice.20-255-158-192.sslip.io,pay.20-255-158-192.sslip.io"
ALLOW_HOSTS = {h.strip().lower() for h in os.environ.get("UAT_ALLOW_HOSTS", DEFAULT_HOSTS).split(",") if h.strip()}


def _host(url: str) -> str:
    return (urlparse(url if "://" in url else f"http://{url}").hostname or "").lower()


def is_local(url: str) -> bool:
    host = _host(url)
    return host in LOCAL_HOSTS or host.endswith(".localhost")


def assert_local(name: str, url: str) -> None:
    host = _host(url)
    if host.endswith(FORBIDDEN_SUFFIXES):
        raise RuntimeError(f"{name}={url!r} is a Vercel address. The UAT suite runs on localhost only.")
    if host in ALLOW_HOSTS:
        return
    if not is_local(url) and not ALLOW_REMOTE:
        raise RuntimeError(f"{name}={url!r} is not localhost. Set UAT_ALLOW_HOSTS=<this host> for a hosted test environment you own, or UAT_ALLOW_REMOTE=1 for a machine of your own private network.")


def assert_all_local() -> None:
    for name, url in (("UAT_ADMIN_URL", ADMIN_URL), ("UAT_PARENT_URL", PARENT_URL), ("UAT_CHECKOUT_URL", CHECKOUT_URL)):
        assert_local(name, url)


_REACH_CACHE: dict[str, str] = {}


def unreachable_reason(url: str) -> str:
    """Empty string when the address answers, otherwise the reason. Checked once per address and run, so a stack that is down
    gives BLOCKED (environment) for the case instead of a FAIL that looks like a product defect."""
    import socket
    if url in _REACH_CACHE:
        return _REACH_CACHE[url]
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    reason = ""
    for _ in range(2):
        try:
            with socket.create_connection((host, port), timeout=8):
                reason = ""
                break
        except OSError as exc:
            reason = f"{host}:{port} does not answer ({exc.__class__.__name__}: {exc}). The stack is down, restarting or blocked from this computer."
    _REACH_CACHE[url] = reason
    return reason
