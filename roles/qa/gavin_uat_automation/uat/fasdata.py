"""Valid test data for the e-Service FAS form. Every NRIC passes the check digit rule of the form. Names are fictional."""
from __future__ import annotations

from datetime import date

from pages.fas_form_page import Applicant, Beneficiary, FamilyMember
from uat.actors import birth_date, make_nric


def academic_year() -> str:
    return str(date.today().year)


def parent(nationality: str = "SC") -> Applicant:
    return Applicant(full_name="Lim Wei Minh", nric=make_nric("S"), dob="1985-03-12", gender="MALE",
                     nationality=nationality, relationship="FATHER")


def child(age: int = 10, name: str | None = None) -> Beneficiary:
    return Beneficiary(full_name=name or f"UAT Child {make_nric('S')[1:6]}", nric=make_nric("S"), dob=birth_date(age), gender="MALE",
                       school="UAT Primary School", level="PRIMARY", grade="P4")


def other_member() -> FamilyMember:
    return FamilyMember(full_name="Tan Mei Ling", nric=make_nric("S"), dob="1987-06-20", gender="FEMALE",
                        relationship="MOTHER", has_income=False)
