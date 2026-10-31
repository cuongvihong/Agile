"""UatRun: runs the steps of one master case, records evidence and decides the result.

Results of a step
  PASS     every check of the step is true
  FAIL     a check is false (kind=check) or the step could not be driven (kind=error)
  GAP      the master describes a screen, button or field that the build does not have.
           Rule of 30/10/2026: GAP is approved as FAIL. The label GAP is kept to tell it from a wrong value.
  BLOCKED  the step cannot run on this environment (time driven job, needs the tech team, data the
           master needs is missing, a previous step it depends on did not pass)
  PASS + EQUIV  the function exists under another screen name or layout. Shown in the report.

Case result priority: FAIL, GAP, BLOCKED, PASS.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path

from . import config

PASS, FAIL, GAP, BLOCKED = "PASS", "FAIL", "GAP", "BLOCKED"
COLORS = {PASS: "#1b7f3b", FAIL: "#b3261e", GAP: "#6a1b9a", BLOCKED: "#c25e00", "RUN": "#1f3a93"}


class StepBlocked(Exception):
    pass


class StepGap(Exception):
    pass


@dataclass
class Check:
    ok: bool
    label: str
    actual: str = ""


@dataclass
class Step:
    n: int
    title: str
    expected: str
    status: str = ""
    checks: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    gaps: list = field(default_factory=list)
    equiv: list = field(default_factory=list)
    error: str = ""
    blocked_reason: str = ""
    shots: list = field(default_factory=list)
    api_errors: list = field(default_factory=list)
    started: float = 0.0
    seconds: float = 0.0

    # ---- used inside a step -------------------------------------------------
    def check(self, ok, label: str, actual="") -> bool:
        self.checks.append(Check(bool(ok), label, _short(actual)))
        return bool(ok)

    def note(self, text: str) -> None:
        self.notes.append(_short(text, 600))

    def gap(self, text: str, stop: bool = False) -> None:
        """The master describes something the build does not have."""
        self.gaps.append(_short(text, 600))
        if stop:
            raise StepGap(text)

    def same_function(self, text: str) -> None:
        """The function exists under another name or layout (EQUIV). GAP in strict mode."""
        if config.STRICT_NAMES:
            self.gaps.append("STRICT NAMES: " + _short(text, 600))
        else:
            self.equiv.append(_short(text, 600))

    def blocked(self, text: str):
        raise StepBlocked(text)

    def require(self, ok, label: str, actual=""):
        """A check that the next actions need. False ends the step as FAIL."""
        if not self.check(ok, label, actual):
            raise AssertionError(f"{label}. Actual: {_short(actual)}")


def _short(value, limit: int = 400) -> str:
    text = value if isinstance(value, str) else repr(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


class UatRun:
    def __init__(self, case_id: str, browser, master: dict):
        self.case_id = case_id
        self.browser = browser
        self.master = master or {}
        self.title = self.master.get("title", "")
        self.steps: list[Step] = []
        self.actors: dict = {}
        self.focus = None
        self.started = time.time()
        self.data_mapping: list[str] = []
        self.shot_dir = config.SHOTS_DIR / case_id
        if self.shot_dir.exists():
            shutil.rmtree(self.shot_dir, ignore_errors=True)
        self.shot_dir.mkdir(parents=True, exist_ok=True)

    # ---- actors (one browser context, one window and one video per user) ----
    def actor(self, name: str):
        if name in self.actors:
            self.focus = self.actors[name]["page"]
            return self.focus
        raw = config.RAW_VIDEOS_DIR / f"{self.case_id}__{name}"
        raw.mkdir(parents=True, exist_ok=True)
        ctx = self.browser.new_context(
            viewport=config.VIEWPORT,
            record_video_dir=str(raw),
            record_video_size=config.VIEWPORT,
            ignore_https_errors=False,
            locale="en-SG",
            timezone_id="Asia/Singapore",
        )
        ctx.set_default_timeout(20000)
        page = ctx.new_page()
        api_errors: list = []

        def on_response(resp, _errs=api_errors):
            try:
                if "/api/" in resp.url and resp.status >= 400:
                    _errs.append(f"{resp.request.method} {resp.url.split('?')[0]} -> HTTP {resp.status}")
            except Exception:
                pass

        page.on("response", on_response)
        self.actors[name] = {"context": ctx, "page": page, "raw": raw, "api_errors": api_errors}
        self.focus = page
        return page

    def map_data(self, text: str) -> None:
        """Record how a master value was mapped to environment data (shown in the report)."""
        self.data_mapping.append(text)

    # ---- steps ----------------------------------------------------------------
    def step(self, n: int, title: str, expected: str = "", needs: tuple = (), page=None):
        """Decorator that runs the step now. The decorated name receives the return value.

            @uat.step(2, "On Home choose the child card", "Home shows ...")
            def card(s):
                ...
                return value
        """

        def run(fn):
            s = Step(n=n, title=title, expected=expected)
            s.started = time.time()
            self.steps.append(s)
            target = page or self.focus
            unmet = [d for d in needs if self._status_of(d) not in (PASS,)]
            if unmet:
                s.status = BLOCKED
                s.blocked_reason = f"Depends on step {', '.join(map(str, unmet))}, which did not pass."
                self._finish_step(s, target)
                return None
            self._banner(target, s, "RUN")
            api_before = {k: len(v["api_errors"]) for k, v in self.actors.items()}
            value = None
            try:
                value = fn(s)
            except StepBlocked as e:
                s.blocked_reason = str(e)
            except StepGap:
                pass
            except AssertionError as e:
                s.error = f"AssertionError: {e}"
            except Exception as e:  # the step could not be driven
                s.error = f"{type(e).__name__}: {_short(str(e), 500)}"
                s.notes.append("TRACE " + _short(traceback.format_exc(limit=3), 800))
            for k, v in self.actors.items():
                s.api_errors.extend(v["api_errors"][api_before.get(k, 0):])
            s.status = self._decide(s)
            self._finish_step(s, page or self.focus)
            return value

        return run

    def _status_of(self, n: int) -> str:
        for s in self.steps:
            if s.n == n:
                return s.status
        return ""

    @staticmethod
    def _decide(s: Step) -> str:
        if s.error or any(not c.ok for c in s.checks):
            return FAIL
        if s.gaps:
            return GAP
        if s.blocked_reason:
            return BLOCKED
        return PASS

    def _finish_step(self, s: Step, page) -> None:
        s.seconds = round(time.time() - s.started, 1)
        pages = [page] if page is not None else []
        # also capture the other actors that are open, so each video shows the result
        for a in self.actors.values():
            if a["page"] not in pages:
                pages.append(a["page"])
        for i, p in enumerate(pages):
            self._banner(p, s, s.status)
            try:
                p.wait_for_timeout(config.STEP_PAUSE_MS)
                actor = next((k for k, v in self.actors.items() if v["page"] is p), f"p{i}")
                path = self.shot_dir / f"{s.n:02d}-{_slug(s.title)}-{actor}-{s.status.lower()}.png"
                p.screenshot(path=str(path), full_page=False)
                s.shots.append(str(path.relative_to(config.ROOT)))
            except Exception:
                pass

    def _banner(self, page, s: Step, status: str) -> None:
        if page is None:
            return
        lines = [f"<b>{html.escape(self.case_id)}</b> &nbsp;STEP {s.n} &nbsp;[{status if status != 'RUN' else 'RUNNING'}] &nbsp;{html.escape(s.title)}"]
        if s.expected:
            lines.append("EXPECTED " + html.escape(_short(s.expected, 220)))
        for c in s.checks[-4:]:
            lines.append(("OK " if c.ok else "NOT OK ") + html.escape(_short(f"{c.label} ({c.actual})", 200)))
        for g in s.gaps[-2:]:
            lines.append("GAP " + html.escape(_short(g, 200)))
        for q in s.equiv[-1:]:
            lines.append("EQUIV " + html.escape(_short(q, 200)))
        if s.blocked_reason:
            lines.append("BLOCKED " + html.escape(_short(s.blocked_reason, 220)))
        if s.error:
            lines.append("ERROR " + html.escape(_short(s.error, 220)))
        js = """([h, c]) => {
            let b = document.getElementById('__uat_banner');
            if (!b) { b = document.createElement('div'); b.id='__uat_banner';
              b.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:2147483647;color:#fff;font:12px/1.35 Segoe UI,Arial,sans-serif;padding:6px 10px;pointer-events:none;opacity:.94';
              document.documentElement.appendChild(b); }
            b.style.background = c; b.innerHTML = h; }"""
        try:
            page.evaluate(js, ["<br>".join(lines), COLORS.get(status, "#333")])
        except Exception:
            pass

    # ---- end of the case --------------------------------------------------------
    def conclude(self):
        import pytest

        statuses = [s.status for s in self.steps]
        if FAIL in statuses:
            result = FAIL
        elif GAP in statuses:
            result = GAP
        elif BLOCKED in statuses or not statuses:
            result = BLOCKED
        else:
            result = PASS
        self._close()
        self._save(result)
        summary = "; ".join(
            f"step {s.n} {s.status}: " + (s.error or s.blocked_reason or "; ".join(s.gaps) or
                                          "; ".join(f"NOT OK {c.label} ({c.actual})" for c in s.checks if not c.ok))
            for s in self.steps if s.status != PASS
        )
        if result in (FAIL, GAP):
            pytest.fail(f"{self.case_id} {result}. {summary}", pytrace=False)
        if result == BLOCKED:
            pytest.skip(f"{self.case_id} BLOCKED. {summary}")
        return result

    def _close(self) -> None:
        names = list(self.actors)
        for name, a in self.actors.items():
            video = None
            try:
                video = a["page"].video
            except Exception:
                pass
            try:
                a["context"].close()
            except Exception:
                pass
            try:
                src = Path(video.path()) if video else None
                if src and src.exists():
                    dst_name = f"{self.case_id}.webm" if len(names) == 1 else f"{self.case_id}__{name}.webm"
                    dst = config.VIDEOS_DIR / dst_name
                    shutil.move(str(src), str(dst))
                    a["video"] = str(dst.relative_to(config.ROOT))
            except Exception:
                pass
            shutil.rmtree(a["raw"], ignore_errors=True)

    def _save(self, result: str) -> None:
        try:
            all_results = json.loads(config.RESULTS_JSON.read_text(encoding="utf-8"))
        except Exception:
            all_results = {}
        all_results[self.case_id] = {
            "case": self.case_id,
            "title": self.title,
            "owner": self.master.get("owner", ""),
            "severity1": "Severity 1" in (self.master.get("setup", "") or ""),
            "result": result,
            "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "seconds": round(time.time() - self.started, 1),
            "env": {"admin": config.ADMIN_URL, "eservice": config.PARENT_URL, "run_tag": config.RUN_TAG},
            "data_mapping": self.data_mapping,
            "videos": [a.get("video") for a in self.actors.values() if a.get("video")],
            "steps": [
                {
                    "n": s.n, "title": s.title, "expected": s.expected, "status": s.status,
                    "checks": [{"ok": c.ok, "label": c.label, "actual": c.actual} for c in s.checks],
                    "gaps": s.gaps, "equiv": s.equiv, "notes": s.notes, "error": s.error,
                    "blocked": s.blocked_reason, "api_errors": s.api_errors[:10], "shots": s.shots,
                    "seconds": s.seconds,
                }
                for s in self.steps
            ],
        }
        config.RESULTS_JSON.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")
