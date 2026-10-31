"""Step evidence for UAT cases: one video per actor, a banner burned into the video for every step, a screenshot
and an Allure step for every step, and an honest verdict for the whole case.

Why the banner: a video of a run without words is hard to review. The banner at the bottom of the page shows
"UAT-PAR-01  STEP 3/6  <what the tester does>" and "EXPECTED <what the master says>", then turns green (PASS),
red (FAIL), orange (BLOCKED) or purple (GAP) when the step ends. The same words are in the screenshot.

Verdicts of a case (one of four, never a fake pass):
  PASS     every step ran and every check held
  FAIL     a check did not hold, or an action could not be done (pytest failure, evidence is in the video)
  BLOCKED  a step cannot be run on this build or environment (daily job, tech simulation, missing data). pytest skip
  GAP      the master describes a screen or button that the build does not have, verified on screen. pytest xfail
"""
from __future__ import annotations

import json
import re
import shutil
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from uat import env

PASS, FAIL, BLOCKED, GAP = "PASS", "FAIL", "BLOCKED", "GAP"
COLORS = {"RUNNING": "#1e3a8a", PASS: "#166534", FAIL: "#991b1b", BLOCKED: "#b45309", GAP: "#6b21a8"}
MARKS = {PASS: "PASS", FAIL: "FAIL", BLOCKED: "BLOCKED", GAP: "GAP (not in this build)"}

_BANNER_JS = """(s) => {
  let d = document.getElementById('__uat_banner');
  if (!d) {
    d = document.createElement('div');
    d.id = '__uat_banner';
    d.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:2147483647;pointer-events:none;' +
      'font:600 15px/1.4 Segoe UI,Arial,sans-serif;color:#fff;padding:8px 16px;white-space:pre-wrap;' +
      'box-shadow:0 -3px 10px rgba(0,0,0,.4);border-top:3px solid rgba(255,255,255,.6)';
    (document.body || document.documentElement).appendChild(d);
  }
  d.style.background = s.bg;
  d.textContent = s.text;
}"""


def _slug(text: str, limit: int = 48) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:limit] or "step"


def _cut(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


@dataclass
class StepResult:
    index: int
    title: str
    expected: str = ""
    verdict: str = "RUNNING"
    note: str = ""
    checks: list[str] = field(default_factory=list)
    screenshot: str = ""
    actor: str = ""
    seconds: float = 0.0


class UatRun:
    """One UAT case. Created by the `uat` fixture, so a test only calls step(), check(), blocked(), gap() and conclude()."""

    def __init__(self, case_id: str, meta: dict, browser: Browser, planned_steps: int = 0):
        self.case_id = case_id
        self.meta = meta
        self.browser = browser
        self.planned = planned_steps
        self.steps: list[StepResult] = []
        self.actors: dict[str, Page] = {}
        self.contexts: dict[str, BrowserContext] = {}
        self.notes: list[str] = []
        self.verdict = "RUNNING"
        self.started = time.time()
        self._current: StepResult | None = None
        self._active = ""
        self.videos: list[str] = []
        self.shot_dir = env.SHOTS_DIR / case_id
        self.shot_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ actors
    def actor(self, name: str = "main", *, timezone: str = "Asia/Singapore") -> Page:
        """Open a browser window for one person (parent, school, moe) with its own video. Returns the page."""
        if name in self.actors and not self.actors[name].is_closed():
            self._active = name
            return self.actors[name]
        raw_dir = env.RAW_VIDEOS_DIR / self.case_id / name
        raw_dir.mkdir(parents=True, exist_ok=True)
        context = self.browser.new_context(
            viewport=env.VIEWPORT, locale="en-US", timezone_id=timezone, ignore_https_errors=True,
            record_video_dir=str(raw_dir), record_video_size=env.VIDEO_SIZE, accept_downloads=True,
        )
        # The e-Service opens the dialog "Welcome to E-Service" (guided tour) for a user that has no stored choice. It appears some seconds after
        # Home loads and blocks every click. The choice is read from localStorage, so answer "done" for it in every window of the suite.
        context.add_init_script(
            "(() => { const get = Storage.prototype.getItem; Storage.prototype.getItem = function (k) {"
            " if (typeof k === 'string' && k.startsWith('edusave.e-service-tour-choice-v1:')) return 'done';"
            " return get.call(this, k); }; })();")
        page = context.new_page()
        page.set_default_timeout(20_000)
        page.set_default_navigation_timeout(40_000)
        page.on("domcontentloaded", lambda p: self._render(p))
        page.on("load", lambda p: self._render(p))
        self.contexts[name] = context
        self.actors[name] = page
        self._active = name
        self._render(page, "RUNNING", f"{self.case_id}  actor: {name}")
        return page

    @property
    def page(self) -> Page:
        if not self._active:
            return self.actor("main")
        return self.actors[self._active]

    def use(self, name: str) -> Page:
        self._active = name
        return self.actors[name]

    def request(self, name: str | None = None):
        """APIRequestContext that shares the cookies of an actor (for cleanup and for reading numbers)."""
        return self.contexts[name or self._active].request

    # ------------------------------------------------------------------ banner
    def _banner_state(self) -> dict:
        cur = self._current
        total = max(self.planned, len(self.steps))
        if cur is None:
            return {"bg": COLORS["RUNNING"], "text": f"{self.case_id}  {self.meta.get('title', '')}"}
        head = f"{self.case_id}   STEP {cur.index}/{total}   [{MARKS.get(cur.verdict, 'RUNNING')}]" if cur.verdict != "RUNNING" \
            else f"{self.case_id}   STEP {cur.index}/{total}"
        lines = [f"{head}   {_cut(cur.title, 130)}"]
        if cur.expected:
            lines.append(f"EXPECTED  {_cut(cur.expected, 190)}")
        for c in cur.checks[-3:]:
            lines.append(_cut(c, 190))
        if cur.note and cur.verdict in (FAIL, BLOCKED, GAP):
            lines.append(_cut(cur.note, 190))
        return {"bg": COLORS.get(cur.verdict, COLORS["RUNNING"]), "text": "\n".join(lines)}

    def _render(self, page: Page | None = None, verdict: str | None = None, text: str | None = None) -> None:
        state = self._banner_state()
        if text:
            state = {"bg": COLORS.get(verdict or "RUNNING"), "text": text}
        pages = [page] if page is not None else list(self.actors.values())
        for p in pages:
            try:
                if not p.is_closed():
                    p.evaluate(_BANNER_JS, state)
            except Exception:  # noqa: BLE001 the page is moving to another address, the next load event draws it again
                pass

    def _pause(self, ms: int) -> None:
        try:
            self.page.wait_for_timeout(ms)
        except Exception:  # noqa: BLE001
            time.sleep(ms / 1000)

    def _shot(self, step: StepResult) -> None:
        path = self.shot_dir / f"{step.index:02d}-{_slug(step.title)}-{step.verdict.lower()}.png"
        try:
            self.page.screenshot(path=str(path), full_page=False)
            step.screenshot = str(path)
            allure.attach.file(str(path), name=f"{step.index:02d} {step.title} [{step.verdict}]", attachment_type=allure.attachment_type.PNG)
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------ steps
    @contextmanager
    def step(self, title: str, expected: str = ""):
        """Run one step of the master. Records the banner, screenshot and Allure step. Re-raises the error of the step."""
        step = StepResult(index=len(self.steps) + 1, title=title, expected=expected, actor=self._active)
        self.steps.append(step)
        self._current = step
        began = time.time()
        self._render()
        self._pause(700)
        try:
            with allure.step(f"Step {step.index}: {title}"):
                yield step
        except pytest.skip.Exception as exc:
            step.verdict, step.note = BLOCKED, str(exc)
            self._finish_step(step, began)
            raise
        except pytest.xfail.Exception as exc:
            step.verdict, step.note = GAP, str(exc)
            self._finish_step(step, began)
            raise
        except BaseException as exc:  # noqa: BLE001
            step.verdict, step.note = FAIL, f"{type(exc).__name__}: {exc}".splitlines()[0]
            self._finish_step(step, began)
            raise
        else:
            step.verdict = PASS
            self._finish_step(step, began)

    def _finish_step(self, step: StepResult, began: float) -> None:
        step.seconds = round(time.time() - began, 1)
        self._render()
        self._shot(step)
        self._pause(env.STEP_PAUSE_MS if step.verdict == PASS else env.STEP_PAUSE_MS + 1500)

    def check(self, what: str, ok: bool, detail: str = "") -> None:
        """One expected result. Raises AssertionError when it does not hold so the step turns red."""
        cur = self._current
        line = f"{'OK ' if ok else 'NOT OK '} {what}" + (f"  ({detail})" if detail else "")
        if cur is not None:
            cur.checks.append(line)
        self._render()
        allure.attach(line, name="check", attachment_type=allure.attachment_type.TEXT)
        if not ok:
            raise AssertionError(f"{what}" + (f". Actual: {detail}" if detail else ""))

    def check_all(self, *items: tuple) -> None:
        """Several expected results of one step. All are evaluated and shown, then one error lists every failed one.
        Each item is (what, ok) or (what, ok, detail)."""
        cur = self._current
        failed: list[str] = []
        for item in items:
            what, ok = item[0], bool(item[1])
            detail = item[2] if len(item) > 2 else ""
            line = f"{'OK ' if ok else 'NOT OK '} {what}" + (f"  ({detail})" if detail else "")
            if cur is not None:
                cur.checks.append(line)
            allure.attach(line, name="check", attachment_type=allure.attachment_type.TEXT)
            if not ok:
                failed.append(what + (f". Actual: {detail}" if detail else ""))
        self._render()
        if failed:
            raise AssertionError(" | ".join(failed))

    def blocked(self, title: str, reason: str, expected: str = "") -> None:
        """A step that cannot be run here. It is shown in the video and counted as BLOCKED, never as passed."""
        _ = self.page  # make sure a window exists so that the video shows the banner
        step = StepResult(index=len(self.steps) + 1, title=title, expected=expected, verdict=BLOCKED, note=f"BLOCKED: {reason}", actor=self._active)
        self.steps.append(step)
        self._current = step
        with allure.step(f"Step {step.index} BLOCKED: {title}"):
            allure.attach(reason, name="why blocked", attachment_type=allure.attachment_type.TEXT)
        self._render()
        self._shot(step)
        self._pause(env.STEP_PAUSE_MS + 1800)

    def gap(self, title: str, reason: str, expected: str = "") -> None:
        """The master describes a screen or control that the build does not have. Evidence of the screen is in the video."""
        _ = self.page
        step = StepResult(index=len(self.steps) + 1, title=title, expected=expected, verdict=GAP, note=f"NOT IN BUILD: {reason}", actor=self._active)
        self.steps.append(step)
        self._current = step
        with allure.step(f"Step {step.index} GAP: {title}"):
            allure.attach(reason, name="why gap", attachment_type=allure.attachment_type.TEXT)
        self._render()
        self._shot(step)
        self._pause(env.STEP_PAUSE_MS + 1800)

    def note(self, text: str) -> None:
        """A difference between the master and the build that does not stop the case (shown in the report only)."""
        self.notes.append(text)
        allure.attach(text, name="note", attachment_type=allure.attachment_type.TEXT)

    # ------------------------------------------------------------------ result
    def conclude(self) -> None:
        """Call as the last line of the test. Decides the verdict and tells pytest (pass, skip or xfail)."""
        verdicts = [s.verdict for s in self.steps]
        if FAIL in verdicts or GAP in verdicts:  # a screen or control of the master that the build lacks is approved as FAIL (user, 2026-10-30)
            self.verdict = FAIL
        elif BLOCKED in verdicts:
            self.verdict = BLOCKED
        else:
            self.verdict = PASS
        done = [s for s in self.steps if s.verdict == PASS]
        summary = f"{self.verdict}: {len(done)}/{len(self.steps)} steps passed"
        reasons = "; ".join(f"step {s.index} {s.note}" for s in self.steps if s.verdict in (BLOCKED, GAP))
        allure.dynamic.label("uat_verdict", self.verdict)
        allure.dynamic.tag(self.verdict)
        if self.verdict == FAIL:
            pytest.fail(f"{summary}. {reasons}", pytrace=False)
        if self.verdict == BLOCKED:
            pytest.skip(f"{summary}. {reasons}")

    # ------------------------------------------------------------------ teardown
    def close(self, failed: bool = False) -> None:
        if self.verdict == "RUNNING":  # conclude() was not reached: an error ended the test
            bad = [s.verdict for s in self.steps]
            self.verdict = FAIL if (failed or FAIL in bad) else (GAP if GAP in bad else BLOCKED if BLOCKED in bad else PASS)
        for name, page in list(self.actors.items()):
            video = None
            try:
                video = page.video
            except Exception:  # noqa: BLE001
                pass
            try:
                self.contexts[name].close()
            except Exception:  # noqa: BLE001
                pass
            if video is not None:
                try:
                    raw = Path(video.path())
                    if raw.exists():
                        env.VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
                        suffix = "" if len(self.actors) == 1 else f"__{name}"
                        dest = env.VIDEOS_DIR / f"{self.case_id}{suffix}.webm"
                        if dest.exists():
                            dest.unlink()
                        shutil.move(str(raw), str(dest))
                        self.videos.append(str(dest))
                        allure.attach.file(str(dest), name=f"VIDEO {name}: {dest.name}", attachment_type=allure.attachment_type.WEBM)
                except Exception as exc:  # noqa: BLE001
                    print(f"[uat] could not save the video of {self.case_id}/{name}: {exc}")
        shutil.rmtree(env.RAW_VIDEOS_DIR / self.case_id, ignore_errors=True)
        self._write_result()

    def _write_result(self) -> None:
        data = {}
        if env.RESULTS_JSON.exists():
            try:
                data = json.loads(env.RESULTS_JSON.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                data = {}
        total = len(self.steps)
        data[self.case_id] = {
            "id": self.case_id,
            "title": self.meta.get("title", ""),
            "verdict": self.verdict,
            "steps_total": total,
            "steps_pass": sum(1 for s in self.steps if s.verdict == PASS),
            "steps_fail": sum(1 for s in self.steps if s.verdict == FAIL),
            "steps_blocked": sum(1 for s in self.steps if s.verdict == BLOCKED),
            "steps_gap": sum(1 for s in self.steps if s.verdict == GAP),
            "seconds": round(time.time() - self.started, 1),
            "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "videos": [Path(v).name for v in self.videos],
            "notes": self.notes,
            "steps": [asdict(s) for s in self.steps],
        }
        env.RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
        env.RESULTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
