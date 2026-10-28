"""Reusable, deliberately fake test data for the Trainer Account form.

Every value here is synthetic, chosen only to satisfy the AUT's own
client-side validation rules documented in
docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md. No real personal data is used.
"""
from __future__ import annotations

from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
VALID_ID_DOCUMENT = str(FIXTURES_DIR / "valid-id.pdf")
INVALID_TYPE_DOCUMENT = str(FIXTURES_DIR / "invalid-type.txt")

# A complete, valid dataset for the default (Singapore) residential branch.
# Postal code 120047 deliberately hits the AUT's hardcoded auto-fill map
# (Session 01 doc, §2), so block/street are populated by the app itself —
# tests that need a *different* block/street must override both explicitly,
# since FormPage.fill_form() sets postal_code before block/street so an
# explicit override always wins over the auto-fill.
VALID_SG_DATA: dict = {
    "residential_type": "Singapore",
    "preferred_name": "Nguyen Van A",
    "gender": "Male",
    "id_type": "NRIC",
    "id_number": "S1234567A",
    "id_document_path": VALID_ID_DOCUMENT,
    "nationality": "Vietnamese",
    "dob": "1995-01-01",
    "race": "Others",
    "birth_country": "Vietnam",
    "tax_resident": "No",
    "primary_email": "trainer.a@example.com",
    "primary_phone_code": "+65",
    "primary_phone": "87654321",
    "emergency_name": "Nguyen Van B",
    "emergency_relationship": "Sibling",
    "emergency_phone_code": "+65",
    "emergency_phone": "81234567",
    "postal_code": "120047",
    "floor_number": "05",
    "unit_number": "123",
}

# A complete, valid dataset for the Non-Singapore residential branch.
VALID_NON_SG_DATA: dict = {
    "residential_type": "Non-Singapore",
    "preferred_name": "Nguyen Thi C",
    "gender": "Female",
    "id_type": "Passport",
    "id_number": "N1234567",
    "id_document_path": VALID_ID_DOCUMENT,
    "nationality": "Malaysian",
    "dob": "1990-06-15",
    "race": "Others",
    "birth_country": "Malaysia",
    "tax_resident": "No",
    "primary_email": "trainer.c@example.com",
    "primary_phone_code": "+60",
    "primary_phone": "123456789",
    "emergency_name": "Nguyen Van D",
    "emergency_relationship": "Friend",
    "emergency_phone_code": "+60",
    "emergency_phone": "123456780",
    "country_region": "Malaysia",
    "address1": "123 Jalan Test",
    "city": "Kuala Lumpur",
}


# ============================================================
# Official Test Case Library datasets (ground truth)
#
# TD_TRAINER_001 / TD_TRAINER_002 are transcribed verbatim from the
# DataLibrary sheet of TS01.xlsx..TS09.xlsx (the 186-test-case official
# library at the workspace root), NOT invented for this suite. Values are
# already synthetic/fake in the source (e.g. "John Tan", "trainer@example.com").
#
# Gap found and filled in, disclosed rather than silent: the official
# DataLibrary rows for both datasets omit Nationality, Race, and
# Country/Region of Birth entirely, even though all three are mandatory
# fields in the real build. Without them, every TS-01 case would fail from
# a missing mandatory field regardless of the field actually under test.
# Filled in with values consistent with each dataset's own name
# ("Singapore Address" / "Non-Singapore Address"):
#   TD_TRAINER_001: Nationality=Singaporean, Race=Chinese, Birth Country=Singapore
#   TD_TRAINER_002: Nationality=Malaysian,  Race=Others,  Birth Country=Malaysia
# ============================================================

TRAINER_JPG = str(FIXTURES_DIR / "trainer.jpg")
TRAINER_PNG = str(FIXTURES_DIR / "trainer.png")
TRAINER_PDF = str(FIXTURES_DIR / "trainer.pdf")
TRAINER_UNSUPPORTED = str(FIXTURES_DIR / "trainer.exe")
TRAINER_PDF_10MB = str(FIXTURES_DIR / "valid_10mb.pdf")
TRAINER_PDF_OVER_10MB = str(FIXTURES_DIR / "oversize_10mb_plus_1.pdf")

# TD_TRAINER_001 — "Valid Trainer - Singapore Address"
TD_TRAINER_001: dict = {
    "residential_type": "Singapore",
    "preferred_name": "John Tan",
    "gender": "Male",
    "id_type": "NRIC",
    "id_number": "S1234567D",
    "id_document_path": TRAINER_JPG,
    "nationality": "Singaporean",  # gap-fill, see module note above
    "dob": "1990-01-01",
    "race": "Chinese",  # gap-fill, see module note above
    "birth_country": "Singapore",  # gap-fill, see module note above
    "tax_resident": "Yes",
    "primary_email": "trainer@example.com",
    "primary_phone_code": "+65",
    "primary_phone": "91234567",
    # Secondary Contact Number: "(blank - optional field, left empty)" in source
    "emergency_name": "David Tan",
    "emergency_relationship": "Parent",  # see ID_TYPE/RELATIONSHIP note below
    "emergency_phone_code": "+65",
    "emergency_phone": "98765432",
    "postal_code": "120047",
    "block_number": "120",
    "street_name": "Bukit Merah Central",
    "floor_number": "05",
    "unit_number": "123",
    "floor_not_applicable": False,
}

# TD_TRAINER_002 — "Valid Trainer - Non-Singapore Address"
TD_TRAINER_002: dict = {
    "residential_type": "Non-Singapore",
    "preferred_name": "John Tan",
    "gender": "Male",
    "id_type": "NRIC",
    "id_number": "S1234567D",
    "id_document_path": TRAINER_JPG,
    "nationality": "Malaysian",  # gap-fill, see module note above
    "dob": "1990-01-01",
    "race": "Others",  # gap-fill, see module note above
    "birth_country": "Malaysia",  # gap-fill, see module note above
    "tax_resident": "Yes",
    "primary_email": "trainer@example.com",
    "primary_phone_code": "+65",
    "primary_phone": "91234567",
    "emergency_name": "David Tan",
    "emergency_relationship": "Parent",
    "emergency_phone_code": "+65",
    "emergency_phone": "98765432",
    "country_region": "Malaysia",
    "postal_code": "50450",
    "address1": "123 Jalan Ampang",
    "city": "Kuala Lumpur",
    "state_province": "Selangor",
}

# Relationship mapping note (BUG-06 / finding F25): the official dataset's
# Relationship value "Parent" does not exist as a dropdown option in the
# real build — the build splits it into "Father" and "Mother" instead
# (7 options total vs the FSD's 6). TS-01 does not exercise Relationship
# itself (that is TS-03's field), so TD_TRAINER_001/002 above map "Parent"
# to the build's "Father" for any test that merely needs a valid baseline.
TD_TRAINER_001["emergency_relationship"] = "Father"
TD_TRAINER_002["emergency_relationship"] = "Father"

# ID Type mapping note (BUG-05 / finding F19): the FSD/official test data
# names ("NRIC", "FIN", "Employment Pass", "Passport") do not all exist
# verbatim as dropdown options in the real build, which instead offers 5
# values: NRIC, FIN, EP, S-Pass, Passport. "Employment Pass" is mapped to
# the build's "EP" option — the closest match, and the same mapping BUG-05's
# own defect text uses ("Selecting 'EP' succeeds...").
ID_TYPE_OPTION_MAP: dict = {
    "NRIC": "NRIC",
    "FIN": "FIN",
    "Employment Pass": "EP",
    "Passport": "Passport",
}


def with_overrides(base: dict, **overrides) -> dict:
    """Copy `base` with `overrides` applied.

    Negative/boundary tests start from a known-valid dataset and break
    exactly one field, instead of duplicating a whole dataset per scenario.
    """
    data = dict(base)
    data.update(overrides)
    return data


def without_keys(base: dict, *keys: str) -> dict:
    """Copy `base` with the given keys removed entirely (not blanked).

    Used for "required field missing" scenarios where the field must never
    be filled at all — e.g. FormPage.fill_form() skips upload entirely
    rather than calling set_input_files([]).
    """
    data = dict(base)
    for key in keys:
        data.pop(key, None)
    return data
