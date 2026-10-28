"""Seed data definitions and fixtures for R5 Paper Applications."""
from __future__ import annotations

# Test personas
SCHOOL_ADMIN = {
    "username": "school",
    "password": "Password123!",
    "role": "SCHOOL",
    "school_name": "Tampines Secondary School",
    "school_code": "SCH-001"
}

MOE_HQ = {
    "username": "moehq",
    "password": "Password123!",
    "role": "MOEHQ",
}

# Seed applicants & students from SEED-R5
SEED_APPLICANTS = [
    {
        "nric": "S1234567A",
        "full_name": "Tan Ah Teck",
        "relationship": "Father",
        "contact": "91234567",
        "email": "tan.ahteck@example.sg",
        "address": "Blk 123 Tampines St 11 #04-56",
        "postal": "521123"
    },
    {
        "nric": "S2345678B",
        "full_name": "Siti Nurhaliza",
        "relationship": "Mother",
        "contact": "92345678",
        "email": "siti.nur@example.sg",
        "address": "Blk 456 Bedok North Ave 2 #08-12",
        "postal": "460456"
    }
]

SEED_CHILDREN = [
    {
        "nric": "T0812345C",
        "full_name": "Tan Xiao Ming",
        "dob": "2010-05-15",
        "level": "Secondary 2",
        "class_name": "Sec 2 Express A",
        "school": "Tampines Secondary School",
        "scheme": "MOEFAS"
    },
    {
        "nric": "T0923456D",
        "full_name": "Muhammad Haziq",
        "dob": "2011-09-20",
        "level": "Secondary 1",
        "class_name": "Sec 1 Normal Tech",
        "school": "Tampines Secondary School",
        "scheme": "SBFAS"
    }
]
