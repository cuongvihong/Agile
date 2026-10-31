"""WHAT the precondition seed creates (UAT-PRE-01 and UAT-PRE-02). Edit this file to change the data, the code does not change.

The host (Azure) cannot be reset, so the seed only ADDS and is idempotent: artifacts/seed_state.json remembers what was created, and names
are checked on the host before creating. Everything carries the prefix UAT-SEED.

Master (uat-master.xlsx, sheet Test data): DATA-TOPUP (three eligible EAs, top-up SGD 20), DATA-FEES (known charge SGD 100),
DATA-PAY (EA-only, split, cancel). EA balances on the host are 500 or more and there is no debit API, so a balance of SGD 10 cannot be built;
the plan uses a charge bigger than the balance for the split case.
"""
PREFIX = "UAT-SEED"

# Active EAs that are not used by the payment UAT cases. nric = student, parent = Singpass persona that can see the child in the e-Service.
STUDENTS = {
    "ethan":  {"name": "Ethan Rahman",  "nric": "S3678638G", "code": "STU-004", "ea": "EDU-01004", "parent": "S8901234H"},
    "leo":    {"name": "Leo Rahman",    "nric": "S5918715F", "code": "STU-007", "ea": "EDU-01007", "parent": "S8901234H"},
    "isaac":  {"name": "Isaac Chen",    "nric": "S3320821H", "code": "STU-015", "ea": "EDU-01015", "parent": "S6789012F"},
    "sophia": {"name": "Sophia Chen",   "nric": "S1192619B", "code": "STU-017", "ea": "EDU-01017", "parent": "S6789012F"},
    "grace":  {"name": "Grace Pham",    "nric": "S6159230D", "code": "STU-022", "ea": "EDU-01022", "parent": "S7654321B"},
}

TOPUPS = [  # individual top-ups, SGD per account
    {"key": "ethan", "amount": 20},
    {"key": "leo",   "amount": 20},
    {"key": "isaac", "amount": 20},
]

# A payment that succeeds (or is held for reconciliation) uses the EA of the child up, and a new UAT_SEED_ROUND only adds new fees. From round 2 the seed
# tops these EAs up to the target again, so the payment cases have the 520 they were written for. Round 1 never changes balances this way.
EA_TARGET = 520.00
RESTORE_EA = ["ethan", "leo", "isaac", "grace"]

CAMPAIGNS = [  # created, not run (UAT_SEED_RUN_CAMPAIGN=1 runs it). The backend only accepts ages 7 to 15 (CreateCampaignValidator).
    {"name": f"{PREFIX} Bulk 20 age 10", "amount": 20, "min_age": 10, "max_age": 10, "description": "Seed for UAT top-up cases. Targets age 10 only (4 EAs)."},
]

FEE_TYPE_CODE = "MISC"
# A payment that succeeds uses up the charge and drains the EA, so a second UAT run needs fresh charges: UAT_SEED_ROUND=2 (3, ...) creates a new set
# of components and batches next to the old ones. Round 1 keeps the plain names.
import os as _os
ROUND = _os.environ.get("UAT_SEED_ROUND", "1").strip() or "1"
SUFFIX = "" if ROUND == "1" else f" r{ROUND}"
COMPONENTS = [  # MOE level components, rate PRIMARY and SC
    {"name": f"{PREFIX} Fee 100{SUFFIX}", "price": 100.00, "tax": False, "students": ["ethan", "leo"], "use": "EA-only payment: charge 100 against an EA of 520"},
    {"name": f"{PREFIX} Fee 600{SUFFIX}", "price": 600.00, "tax": False, "students": ["isaac", "grace", "leo"], "use": "Charge bigger than the EA balance: split payment (Isaac), failed online part (Grace), EA only disabled (Leo)"},
    {"name": f"{PREFIX} Fee 50{SUFFIX}",  "price": 50.00,  "tax": False, "students": ["grace", "sophia"], "use": "Online only payment (Sophia succeeds, Grace fails)"},
    {"name": f"{PREFIX} Fee 700{SUFFIX}", "price": 700.00, "tax": False, "students": ["leo"], "use": "Split payment whose online part fails and the EA part is held for reconciliation (Leo, UAT-PAR-01-E2)"},
    {"name": f"{PREFIX} Fee S100{SUFFIX}", "price": 100.00, "tax": False, "students": ["sophia"], "use": "A charge of 100.00 for Sophia, the granted child of UAT-033 (a subsidy shows on it only when the MOEFAS scheme covers this component)"},
]
# Which seeded child, parent persona and charge each payment case uses. Every case has its own child so one case does not use up the data of another.
PAY_CASES = {
    "UAT-PAR-01":        {"student": "ethan",  "component": f"{PREFIX} Fee 100{SUFFIX}"},   # EA only, succeeds (EA 520 to 420)
    "UAT-PAR-01-N3":     {"student": "leo",    "component": f"{PREFIX} Fee 600{SUFFIX}"},   # read only: EA only is disabled
    "UAT-PAR-01-A1":     {"student": "isaac",  "component": f"{PREFIX} Fee 600{SUFFIX}"},   # split EA 520 + online 80, succeeds
    "UAT-PAR-01-A1-ON":  {"student": "sophia", "component": f"{PREFIX} Fee 50{SUFFIX}"},    # online only, succeeds
    "UAT-PAR-01-N4":     {"student": "grace",  "component": f"{PREFIX} Fee 600{SUFFIX}"},   # split, the online part fails; the build has no EA refund, the payment goes to reconciliation
    "UAT-PAR-01-N4-ON":  {"student": "grace",  "component": f"{PREFIX} Fee 50{SUFFIX}"},    # online only, fails, no EA debit
    "UAT-PAR-01-E2":     {"student": "leo",    "component": f"{PREFIX} Fee 700{SUFFIX}"},   # split EA 520 + online 180, the online part fails, the EA part is held for reconciliation
}
RATE_FROM = "2026-01-01"
PERIOD_START = "2026-11-01"
PERIOD_END_EXCLUSIVE = "2026-12-01"
DUE_DATE = "2026-12-31"

# FAS precondition (UAT-PRE-03). The REAL MOEFAS scheme is used: the Admin portal and the API refuse a second scheme with an overlapping form
# or effective period (HasOverlappingApplicationPeriod / HasOverlappingEffectivePeriod), so a near term test scheme cannot be created.
# The parent applies while the form is open. HQ can confirm only from the scheme effective date, so the approval step runs by itself from that day.
# Isaac Chen and Sophia Chen already have an Approved allocation (APP-01003) and cannot apply again. Lim, Pham and Bui children already have a Pending one.
FAS = {
    "parent": "S8901234H",                                  # Ahmad Bin Rahman, father of Ethan and Leo Rahman
    "children": ["ethan", "leo"],                           # keys of STUDENTS
    "phone": "91234567",
    "email": "ahmad.rahman.s8901234h@example.com",
    "relationship": "FATHER",
    "scheme_exclude_prefixes": ["UAT-GAVIN", "R6-AUTO", PREFIX],  # never use an automation scheme as the real one
    "remarks": f"{PREFIX} approval of seeded application",
}


# School B and its school user (UAT-PRE-04). QA creates them the way MOE HQ does in the Admin portal: School management, Create school
# (POST /api/academic-resources/v1/schools) and School Users, Create school user, tab Single (POST /api/users/v1/school-users/single).
# The portal form has the fields MOE school code, School name, School type and School users. The academic levels of a school are not on that form.
# The password of the school user is never written down: the portal shows how the user logs in after it is created.
SCHOOL_B = {"moe_code": "UATB01", "name": f"{PREFIX} School B", "type": "GOVERNMENT"}
SCHOOL_B_USER = {"nric": "S9000042Z", "first": "UAT", "last": "SchoolB", "email": "uat.schoolb@example.com", "moe_code": "UATB01"}
