"""Turn artifacts/uat_results.json into two CSV files and a summary line.

  artifacts/uat_summary.csv   one row per case: verdict, step counts, videos, run time
  artifacts/uat_steps.csv     one row per step: verdict, what was checked, why it is BLOCKED or GAP, screenshot

Run:  python tools/export_results.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "artifacts" / "uat_results.json"


def main() -> int:
    if not SRC.exists():
        print(f"No results yet: {SRC} does not exist. Run the suite first.")
        return 1
    data = json.loads(SRC.read_text(encoding="utf-8"))
    cases = [data[k] for k in sorted(data)]
    with (ROOT / "artifacts" / "uat_summary.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["Case", "Title", "Verdict", "Steps", "Pass", "Fail", "Blocked", "Gap", "Seconds", "Ran at", "Videos"])
        for c in cases:
            w.writerow([c["id"], c["title"], c["verdict"], c["steps_total"], c["steps_pass"], c["steps_fail"], c["steps_blocked"], c["steps_gap"],
                        c["seconds"], c.get("ran_at", ""), "; ".join(c.get("videos", []))])
    with (ROOT / "artifacts" / "uat_steps.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["Case", "Step", "Actor", "Title", "Expected (master)", "Verdict", "Checks", "Why", "Screenshot", "Seconds"])
        for c in cases:
            for s in c["steps"]:
                w.writerow([c["id"], s["index"], s["actor"], s["title"], s["expected"], s["verdict"], " | ".join(s["checks"]), s["note"], s["screenshot"], s["seconds"]])
    counts = Counter(c["verdict"] for c in cases)
    steps = Counter(s["verdict"] for c in cases for s in c["steps"])
    print(f"{len(cases)} cases: " + ", ".join(f"{k} {counts.get(k, 0)}" for k in ("PASS", "FAIL", "BLOCKED", "GAP")))
    print(f"{sum(steps.values())} steps: " + ", ".join(f"{k} {steps.get(k, 0)}" for k in ("PASS", "FAIL", "BLOCKED", "GAP")))
    print(f"Written: {ROOT / 'artifacts' / 'uat_summary.csv'} and uat_steps.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
