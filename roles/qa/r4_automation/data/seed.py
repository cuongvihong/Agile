"""Base state of the prototype (sample date 18/10/2026) as the MOE HQ list shows it.

Source: sheet "Seed Data" of roles/qa/R4_Test_Cases.xlsx, read from the prototype by QA.
Every value is sample data. Use Reset data (or a fresh browser context) to get back here.
"""
from __future__ import annotations

from .ui_text import EMDASH

SAMPLE_TODAY = "18/10/2026"

# Columns of the MOE HQ list, in the order of the table header.
HQ_COLUMNS = [
    "APPLICATION", "STUDENT", "SCHOOL", "GRADE", "SCHEME", "SUBMITTED",
    "SYSTEM CHECK", "TIER", "ML RECOMMENDATION", "ML RISK", "STATUS",
]
# Columns of the School Admin list.
SCHOOL_COLUMNS = [
    "APPLICATION", "STUDENT", "GRADE", "SUBMITTED", "TIER",
    "ML RECOMMENDATION", "ML RISK", "STATUS",
]

D = EMDASH

# id -> values as the HQ list shows them
APPS = {
    "00377": dict(student="Nur Aisyah", nric="T1688001L", school="Meridian Secondary", grade="S3",
                  scheme="MOEFAS", submitted="17/10/2026", check="Waiting", tier=D, ml=D,
                  risk="Medium", status="Pending"),
    "00412": dict(student="Aisha Rahman", nric="T1801177H", school="Bukit View Primary", grade="P3",
                  scheme="MOEFAS", submitted="17/10/2026", check="Waiting", tier=D, ml=D,
                  risk="Medium", status="Pending"),
    "00410": dict(student="Ryan Lim", nric="T1790221G", school="Bukit View Primary", grade="P5",
                  scheme="MOEFAS", submitted="16/10/2026", check="Waiting", tier=D, ml=D,
                  risk="Medium", status="Pending"),
    "00398": dict(student="Daniel Ong", nric="T1755501Q", school="Bukit View Primary", grade="P2",
                  scheme="SBFAS", submitted="14/10/2026", check=D, tier="", ml=D,
                  risk="Medium", status="Pending"),
    "00390": dict(student="Chen Xin Yi", nric="T1775532J", school="Bukit View Primary", grade="P4",
                  scheme="MOEFAS", submitted="14/11/2025", check="Pass", tier=D, ml=D,
                  risk="High", status="Approved"),
    "00386": dict(student="Lucas Teo", nric="T1780445K", school="Bukit View Primary", grade="P4",
                  scheme="SBFAS", submitted="12/11/2025", check=D, tier="Tier 3", ml="Tier 2",
                  risk="Medium", status="Approved"),
    "00328": dict(student="Lee Zhi Hao", nric="T1702215M", school="Riverside Secondary", grade=D,
                  scheme="MOEFAS", submitted="07/11/2025", check="Fail", tier=D, ml=D,
                  risk="Low", status="Rejected"),
    "00381": dict(student="Lee Zhi Hao", nric="T1702215M", school="Riverside Secondary", grade=D,
                  scheme="MOEFAS", submitted="16/10/2025", check="Pass", tier=D, ml=D,
                  risk="Medium", status="Approved"),
    "00301": dict(student="Siti Amina", nric="T1822335E", school="Bukit View Primary", grade="P3",
                  scheme="MOEFAS", submitted="20/09/2025", check="Pass", tier=D, ml=D,
                  risk="Medium", status="Approved"),
}

ALL_IDS = list(APPS)                                  # order of the list, newest submitted first
WAITING_MOEFAS = ["00377", "00412", "00410"]          # MOEFAS 2027, form Open
BVP_IDS = ["00398", "00386"]                          # SBFAS rows of Bukit View Primary

# Priority of the first assessment of MOEFAS 2026 (4 applications), as the History shows it.
PRIORITY_2026 = {"00390": 1, "00301": 2, "00381": 3, "00328": 4}

# Base state counts
HQ_CARDS = {"Total applications": "9", "MOEFAS approved": "3", "Approved": "4", "Rejected": "1"}
HQ_TABS = {"Pending": 4, "All": 9, "Approved": 4, "Rejected": 1}
BVP_CARDS = {"Pending": "1", "SBFAS approved": "1", "SBFAS rejected": "0"}

# After Close form now (demo) on MOEFAS 2027
HQ_CARDS_AFTER_CLOSE = {"Total applications": "9", "MOEFAS approved": "4", "Approved": "5", "Rejected": "1"}
HQ_TABS_AFTER_CLOSE = {"Pending": 3, "All": 9, "Approved": 5, "Rejected": 1}
BVP_CARDS_AFTER_CLOSE = {"Pending": "3", "SBFAS approved": "1", "SBFAS rejected": "0"}

SCHOOLS = ["Bukit View Primary", "Meridian Secondary", "North Vista Primary", "Riverside Secondary"]

# MOEFAS schemes at the base state
MOEFAS = {
    "MOEFAS 2027": dict(form="01/08/2026 – 31/12/2026", eff_from="1 Jan 2027", eff_to="No end date", status="Upcoming"),
    "MOEFAS 2026": dict(form="01/08/2025 – 31/12/2025", eff_from="1 Jan 2026", eff_to="31 Dec 2026", status="Active"),
    "MOEFAS 2025": dict(form="01/08/2024 – 31/12/2024", eff_from="1 Jan 2025", eff_to="31 Dec 2025", status="Closed"),
}

USERS = {
    "BVP-0012": dict(name="Lan Nguyen", school="Bukit View Primary"),
    "MRS-0012": dict(name="Farah Tan", school="Meridian Secondary"),
}
