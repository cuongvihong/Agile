"""Create the precondition data through the API the Admin portal uses. Cookies come from the browser window of the MOE HQ actor.

Additive and idempotent: names are checked on the host, and artifacts/seed_state.json remembers what was created and what the references are.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import time

from data import seed_plan as plan
from uat import env

TOPUP = "api/education-account/v1/top-ups"
SCHOOLS = "api/academic-resources/v1/schools"
SCHOOL_USERS = "api/users/v1/school-users"
FEES = "api/v1/fees"  # the way the Admin portal calls it (the gateway also serves /api/billing/v1/fees)
# FAS routes: the way the portals call them first, then the way the gateway also serves them
FAS_PARENT = ["api/v1/fas/parent/applications", "api/fas/v1/fas/parent/applications"]
FAS_SCHEMES = ["api/v1/fas/moe-schemes", "api/fas/v1/fas/moe-schemes"]
FAS_HQ = ["api/v1/fas/moehq/schemes/{id}", "api/fas/v1/fas/moehq/schemes/{id}"]
STATE_FILE = env.ARTIFACTS / "seed_state.json"
LOG_FILE = env.ARTIFACTS / "seed_log.jsonl"
MODE = os.environ.get("UAT_SEED", "1").lower()  # 1 = create, plan = read only, 0 = skip
RUN_CAMPAIGN = os.environ.get("UAT_SEED_RUN_CAMPAIGN") == "1"
TODAY = dt.date.today().isoformat()


class SeedError(AssertionError):
    pass


def state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def remember(key: str, value) -> None:
    s = state()
    s[key] = value
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def unwrap(body):
    return body.get("data") if isinstance(body, dict) and "data" in body else body


def items_of(body) -> list:
    data = unwrap(body)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("items", "data", "results", "records"):
            if isinstance(data.get(k), list):
                return data[k]
    return []


def find_value(obj, *keys):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and obj[k] not in (None, ""):
                return obj[k]
        for v in obj.values():
            r = find_value(v, *keys)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_value(v, *keys)
            if r is not None:
                return r
    return None


def _redact(text: str) -> str:
    """A response of the portal can carry a first password or a token. The log must never hold one."""
    return re.sub(r'("[^"]*(?:pass|secret|token|credential)[^"]*"\s*:\s*)"[^"]*"', r'\1"***"', text, flags=re.I)


class Seeder:
    def __init__(self, req, base: str | None = None):
        self.req = req
        self.base = (base or env.ADMIN_URL).rstrip("/") + "/"

    # ---------------------------------------------------------------- http
    def _go(self, method: str, path: str, **kw):
        url = self.base + path.lstrip("/")
        for attempt in range(6):
            resp = getattr(self.req, method)(url, **kw)
            if resp.status != 429:
                break
            time.sleep(8 + 4 * attempt)
        try:
            body = resp.json()
        except Exception:  # noqa: BLE001
            body = {"raw": (resp.text() or "")[:400]}
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "method": method.upper(), "path": path, "status": resp.status,
                                "request": kw.get("data") or kw.get("params"), "response": _redact(json.dumps(body, ensure_ascii=False))[:600]}, ensure_ascii=False) + "\n")
        time.sleep(0.3)
        return resp.status, body

    def get(self, path, **params):
        return self._go("get", path, params=params or None)

    def post(self, path, data=None):
        return self._go("post", path, data=data if data is not None else {})

    def pages(self, path: str, **params) -> list:
        out, n = [], 1
        while n <= 20:
            status, body = self.get(path, PageNumber=n, PageSize=100, **params)
            if status != 200:
                break
            out += items_of(body)
            d = unwrap(body)
            if not ((d.get("metadata") or {}).get("hasNextPage") if isinstance(d, dict) else False):
                break
            n += 1
        return out

    @staticmethod
    def fail(what: str, status: int, body) -> None:
        raise SeedError(f"{what} returned HTTP {status}: {json.dumps(body, ensure_ascii=False)[:300]}. See artifacts/seed_log.jsonl.")

    # ---------------------------------------------------------------- accounts and top-ups
    def account(self, key: str) -> dict:
        s = plan.STUDENTS[key]
        status, body = self.get(f"{TOPUP}/accounts/search", Identifier=s["nric"])
        d = unwrap(body) if status == 200 else None
        wallet = find_value(d, "walletId")
        if not wallet:
            self.fail(f"Top-up search for {s['name']} ({s['nric']})", status, body)
        return {"key": key, "name": s["name"], "walletId": wallet, "walletCode": find_value(d, "walletCode"),
                "balance": find_value(d, "currentBalance"), "studentId": find_value(d, "studentId")}

    def ensure_topup(self, acc: dict, amount: float) -> dict:
        key = f"{acc['key']}:{amount}"
        done = state().get("topups", {})
        if key in done:
            return {**done[key], "created": False, "after": acc["balance"]}
        ref = f"TUP-IND-UATSEED-{plan.STUDENTS[acc['key']]['code']}-{amount}-v1"  # Top-Up History only lists reference ids that contain TUP-IND-
        status, body = self.post(f"{TOPUP}/individual", {"walletId": acc["walletId"], "amount": amount, "referenceId": ref,
                                                         "reason": f"{plan.PREFIX} test data for UAT cases", "fundingSource": "MOE General Funding"})
        if status not in (200, 201):
            self.fail(f"Top-up of {acc['name']}", status, body)
        after = self.account(acc["key"])["balance"]
        rec = {"ref": ref, "transaction": find_value(unwrap(body), "transactionCode"), "before": acc["balance"]}
        done[key] = rec
        remember("topups", done)
        return {**rec, "created": True, "after": after}

    def restore_ea(self, key: str, target: float) -> dict | None:
        """From round 2: top the EA of the child up to the target (in parts of at most 100) when earlier payments used it up. Round 1 does nothing."""
        if plan.ROUND == "1":
            return None
        acc = self.account(key)
        before = float(acc["balance"] or 0)
        done = state().get("restores", {})
        mark = f"{key}:{plan.ROUND}"
        if mark in done:
            return {**done[mark], "created": False, "before": before, "after": before}
        left, n = round(target - before, 2), 0
        while left > 0.004:
            chunk = min(100.0, left)
            n += 1
            ref = f"TUP-IND-UATSEED-{plan.STUDENTS[key]['code']}-RESTORE-R{plan.ROUND}-{n}"
            status, body = self.post(f"{TOPUP}/individual", {"walletId": acc["walletId"], "amount": chunk, "referenceId": ref,
                                                             "reason": f"{plan.PREFIX} restore EA for round {plan.ROUND}", "fundingSource": "MOE General Funding"})
            if status not in (200, 201):
                self.fail(f"Restore the EA of {acc['name']}", status, body)
            left = round(left - chunk, 2)
        after = float(self.account(key)["balance"] or 0)
        rec = {"parts": n, "before": before, "after": after}
        done[mark] = rec
        remember("restores", done)
        return {**rec, "created": n > 0}

    def ensure_campaign(self, c: dict) -> dict:
        status, body = self.get(f"{TOPUP}/campaigns", PageNumber=1, PageSize=100)
        existing = {x.get("name"): x for x in items_of(body)} if status == 200 else {}
        if c["name"] in existing:
            rec, created = {"id": existing[c["name"]].get("id")}, False
        else:
            status, body = self.post(f"{TOPUP}/campaigns", {"name": c["name"], "description": c["description"], "amountPerStudent": c["amount"],
                                                           "minAge": c["min_age"], "maxAge": c["max_age"], "createdBy": "MOEHQ_User"})
            if status not in (200, 201):
                self.fail(f"Create campaign {c['name']}", status, body)
            rec, created = {"id": find_value(unwrap(body), "id"), "code": find_value(unwrap(body), "code")}, True
        if RUN_CAMPAIGN and not state().get("campaigns", {}).get(c["name"], {}).get("executed"):
            s2, b2 = self.post(f"{TOPUP}/campaigns/execute", {"campaignId": rec["id"], "executedBy": "MOEHQ_User", "executionNotes": plan.PREFIX, "runSynchronously": True})
            if s2 not in (200, 201, 202):
                self.fail(f"Run campaign {c['name']}", s2, b2)
            rec["executed"] = True
        done = state().get("campaigns", {})
        done[c["name"]] = {**done.get(c["name"], {}), **rec}
        remember("campaigns", done)
        return {**rec, "created": created}

    # ---------------------------------------------------------------- School B and its school user
    def find_school(self, code: str) -> dict | None:
        status, body = self.get(f"{SCHOOLS}/table", pageNumber=1, pageSize=50, search=code)
        if status != 200:
            self.fail(f"Search school {code}", status, body)
        for x in items_of(body):
            if str(find_value(x, "moeSchoolCode", "code") or "").upper() == code.upper():
                return {"id": find_value(x, "id"), "name": find_value(x, "name"), "code": code}
        return None

    def ensure_school(self, sc: dict) -> dict:
        """School B: same call as Create school in the Admin portal. Idempotent by the MOE school code."""
        hit = self.find_school(sc["moe_code"])
        if hit:
            return {**hit, "created": False}
        status, body = self.post(SCHOOLS, {"moeSchoolCode": sc["moe_code"], "name": sc["name"], "schoolType": sc["type"]})
        if status not in (200, 201):
            self.fail(f"Create school {sc['moe_code']}", status, body)
        hit = self.find_school(sc["moe_code"]) or {"id": find_value(unwrap(body), "id"), "name": sc["name"], "code": sc["moe_code"]}
        remember("school_b", hit)
        return {**hit, "created": True}

    def find_school_user(self, nric: str, email: str) -> dict | None:
        for term in (nric, email):
            status, body = self.get(f"{SCHOOL_USERS}/table", pageNumber=1, pageSize=50, search=term, includeInactive="true")
            if status != 200:
                self.fail(f"Search school user {term}", status, body)
            for x in items_of(body):
                blob = json.dumps(x, ensure_ascii=False).lower()
                if nric.lower() in blob or email.lower() in blob:
                    return {"id": find_value(x, "id", "userId"), "email": email, "school": find_value(x, "schoolName", "moeSchoolCode", "schoolCode")}
        return None

    def ensure_school_user(self, u: dict) -> dict:
        """The school user of School B: same call as Create school user, tab Single. The response is not kept because it can hold a first password."""
        hit = self.find_school_user(u["nric"], u["email"])
        if hit:
            return {**hit, "created": False}
        status, body = self.post(f"{SCHOOL_USERS}/single", {"nric": u["nric"], "firstName": u["first"], "lastName": u["last"], "email": u["email"], "moeSchoolCode": u["moe_code"]})
        if status not in (200, 201):
            self.fail(f"Create school user {u['nric']}", status, body)
        hit = self.find_school_user(u["nric"], u["email"]) or {"id": find_value(unwrap(body), "id", "userId"), "email": u["email"], "school": u["moe_code"]}
        remember("school_b_user", {"id": hit.get("id"), "email": u["email"]})
        return {**hit, "created": True}

    # ---------------------------------------------------------------- fees
    def fee_type_id(self) -> str:
        types = self.pages(f"{FEES}/fee-types/table", IsActive="true")
        t = next((x for x in types if str(x.get("code", "")).upper() == plan.FEE_TYPE_CODE), None)
        if not t:
            raise SeedError(f"Fee type {plan.FEE_TYPE_CODE} not found. Codes seen: {[x.get('code') for x in types]}")
        return t["id"]

    def ensure_component(self, c: dict) -> dict:
        comps = {x.get("name"): x for x in self.pages(f"{FEES}/fee-components/table")}
        if c["name"] in comps:
            cid, created = comps[c["name"]].get("id"), False
        else:
            status, body = self.post(f"{FEES}/fee-components", {"feeTypeId": self.fee_type_id(), "name": c["name"], "schoolId": None, "isTaxApply": c["tax"],
                                                                 "feeComponentStudentCategories": ["SC"], "feeComponentEducationStages": ["PRIMARY"]})
            if status not in (200, 201):
                self.fail(f"Create fee component {c['name']}", status, body)
            cid = find_value(unwrap(body), "id")
            if not cid:
                self.fail(f"Create fee component {c['name']} (no id)", status, body)
            status, body = self.post(f"{FEES}/fee-components/fee-rate-rules", {"feeComponentId": cid, "feeRateRules": [
                {"educationStage": "PRIMARY", "studentCategory": "SC", "priceAmount": c["price"], "currencyCode": "SGD", "effectiveFrom": plan.RATE_FROM}]})
            if status not in (200, 201):
                self.fail(f"Rate rule of {c['name']}", status, body)
            created = True
        done = state().get("components", {})
        done[c["name"]] = {"id": cid, "price": c["price"]}
        remember("components", done)
        return {"id": cid, "created": created}

    def ensure_publication(self, c: dict, component_id: str) -> dict:
        title = f"{c['name']} {plan.PERIOD_START}"
        pubs = state().get("publications", {})
        if str(pubs.get(title, {}).get("status", "")).upper() == "COMPLETED":
            return {**pubs[title], "title": title, "created": False}
        ids, missing = [], []
        for k in c["students"]:
            s = plan.STUDENTS[k]
            status, body = self.get(f"{FEES}/fee-components/{component_id}/eligible-students", searchTerm=s["name"], pageSize=50)
            if status != 200:
                self.fail(f"Eligible students of {c['name']}", status, body)
            pool = items_of(body)
            hit = next((p for p in pool if str(p.get("code", "")).upper() == s["code"] or str(p.get("displayName", "")).lower() == s["name"].lower()), None)
            (ids if hit and hit.get("id") else missing).append(hit["id"] if hit and hit.get("id") else s["name"])
        if missing:
            raise SeedError(f"{missing} are not in the eligible students of {c['name']} (MISC, PRIMARY, SC, active enrolment). See artifacts/seed_log.jsonl.")
        batch = pubs.get(title, {}).get("id")
        if not batch:
            # the same body the Admin portal sends for 'Create draft' with selected students
            status, body = self.post(f"{FEES}/publication-batches", {"feeComponentId": component_id, "title": title, "schoolScope": "COMPONENT_SCOPE",
                                                                      "studentScope": "SELECTED_TARGETS", "periodStart": plan.PERIOD_START,
                                                                      "periodEndExclusive": plan.PERIOD_END_EXCLUSIVE, "dueDate": plan.DUE_DATE,
                                                                      "schoolIds": [], "studentIds": ids})
            if status not in (200, 201):
                self.fail(f"Create fee batch {title}", status, body)
            batch = find_value(unwrap(body), "id")
            pubs[title] = {"id": batch, "students": ids}
            remember("publications", pubs)
        status, body = self.get(f"{FEES}/publication-batches/{batch}")
        stt = str(((unwrap(body) or {}).get("batch") or {}).get("status") or "")
        if stt.upper() == "DRAFT":
            status, body = self.post(f"{FEES}/publication-batches/{batch}/publish")
            if status not in (200, 202, 409):
                self.fail(f"Publish fee batch {title}", status, body)
        detail = None
        for _ in range(30):
            time.sleep(4)
            _, detail = self.get(f"{FEES}/publication-batches/{batch}")
            d = unwrap(detail) or {}
            stt = str((d.get("batch") or {}).get("status") or "")
            if stt.upper() in ("COMPLETED", "PARTIALLY_FAILED", "FAILED"):
                break
        d = unwrap(detail) or {}
        summ = d.get("summary") or {}
        cc = summ.get("chargeCreation") or {}
        pubs[title].update({"status": stt, "charges": cc.get("created"), "failed": cc.get("failed"), "skipped": summ.get("skippedCount")})
        remember("publications", pubs)
        if stt.upper() != "COMPLETED":
            raise SeedError(f"Fee batch {title} ended as {stt!r}, created={cc.get('created')}, failed={cc.get('failed')}, skipped={summ.get('skippedCount')}")
        if cc.get("created") != len(ids):
            raise SeedError(f"Fee batch {title} created {cc.get('created')} charge(s) for {len(ids)} student(s).")
        return {**pubs[title], "title": title, "created": True}

    # ---------------------------------------------------------------- FAS: R10 parent applies, R6 scheme and budget, HQ approval
    def _try(self, method: str, paths: list[str], **kw):
        """Call the first route that exists (404 and 405 mean the route is not served under that name)."""
        status, body, used = 404, {}, paths[-1]
        for p in paths:
            status, body = self._go(method, p, **kw)
            used = p
            if status not in (404, 405):
                break
        return status, body, used

    def fas_prefill(self, nric: str) -> dict:
        status, body, _ = self._try("get", [p + "/prefill" for p in FAS_PARENT], params={"nric": nric})
        if status != 200:
            self.fail(f"FAS prefill of {nric}", status, body)
        return unwrap(body) or {}

    def fas_applications(self) -> list:
        out, n = [], 1
        while n <= 10:
            status, body, _ = self._try("get", FAS_PARENT, params={"PageNumber": n, "PageSize": 50})
            if status != 200:
                break
            out += items_of(body)
            d = unwrap(body)
            meta = (d.get("metadata") or {}) if isinstance(d, dict) else {}
            if not meta.get("hasNextPage"):
                break
            n += 1
        return out

    def ensure_fas_application(self) -> dict:
        """The parent of the seeded students applies for FAS (the call the e-Service form makes). Idempotent: state first, then the parent's list."""
        f = plan.FAS
        names = [plan.STUDENTS[k]["name"] for k in f["children"]]
        saved = state().get("fas", {}).get("application")
        listed = self.fas_applications()
        by_code = {str(find_value(i, "code") or ""): i for i in listed}
        if saved and saved.get("code") in by_code:
            item = by_code[saved["code"]]
            return {**saved, "status": find_value(item, "status") or saved.get("status"), "created": False}
        for item in listed:  # adopt an application of an earlier run whose state file was lost
            blob = json.dumps(item, ensure_ascii=False).lower()
            if all(n.split()[0].lower() in blob for n in names) and "withdraw" not in str(find_value(item, "status") or "").lower():
                rec = {"code": find_value(item, "code"), "id": find_value(item, "id"), "status": find_value(item, "status"), "adopted": True}
                remember_fas("application", rec)
                return {**rec, "created": False}
        pre = self.fas_prefill(f["parent"])
        ap, ben_pool = pre.get("applicant") or {}, pre.get("eligibleBeneficiaries") or []
        chosen, missing = [], []
        for k in f["children"]:
            s = plan.STUDENTS[k]
            hit = next((b for b in ben_pool if str(b.get("nric", "")).upper() == s["nric"].upper()), None)
            (chosen if hit else missing).append(hit or s["name"])
        if missing:
            raise SeedError(f"The prefill of parent {f['parent']} does not list {missing} as children. Listed: {[b.get('fullName') for b in ben_pool]}")
        body = {
            "academicYear": dt.date.today().year,
            "applicant": {"fullName": ap.get("fullName"), "nric": f["parent"], "dateOfBirth": ap.get("dateOfBirth"), "gender": ap.get("gender"),
                          "nationality": ap.get("nationality") or "SC", "race": "OTHER", "relationshipToBeneficiary": f["relationship"],
                          "phoneNumber": f["phone"], "email": f["email"], "address": ap.get("address"), "employmentStatus": "EMPLOYED",
                          "commitmentAgreed": True, "forwardToSchoolAgreed": True},
            "beneficiaries": [{"fullName": b.get("fullName"), "nric": b.get("nric"), "dateOfBirth": b.get("dateOfBirth"), "gender": b.get("gender"),
                               "schoolName": b.get("schoolName") or "Registered MOE School", "classLevel": b.get("classLevel") or "PRIMARY",
                               "grade": b.get("grade") or "1", "academicLevelId": b.get("academicLevelId")} for b in chosen],
            "familyMembers": [{"fullName": m.get("fullName"), "nric": m.get("nric"), "dateOfBirth": m.get("dateOfBirth"), "gender": m.get("gender"),
                               "relationship": m.get("relationship") or "OTHER", "hasIncome": bool(m.get("hasIncome")), "isIncludedInPci": True}
                              for m in (pre.get("otherFamilyMembers") or [])],
        }
        status, resp, _ = self._try("post", FAS_PARENT, data=body, headers={"Idempotency-Key": f"UATSEED-FAS-{f['parent']}-{body['academicYear']}-v1"})
        d = unwrap(resp) if isinstance(resp, dict) else {}
        if status not in (200, 201) or not find_value(d, "code"):
            msg = " ".join(str(x) for x in [(resp or {}).get("message"), *((resp or {}).get("errors") or [])] if x) if isinstance(resp, dict) else ""
            return {"error": True, "http": status, "message": msg[:400] or json.dumps(resp, ensure_ascii=False)[:400], "created": False}
        rec = {"code": find_value(d, "code"), "id": find_value(d, "id"), "status": find_value(d, "status"), "matched": find_value(d, "matchedSchemeType"),
               "ghi": find_value(d, "grossHouseholdIncome"), "pci": find_value(d, "perCapitaIncome"),
               "allocations": [{"scheme": a.get("schemeName"), "child": a.get("beneficiaryName"), "amount": a.get("estimatedAmount"), "from": a.get("effectiveFrom")}
                               for a in (d.get("allocations") or [])]}
        remember_fas("application", rec)
        return {**rec, "created": True}

    def moe_scheme(self) -> dict | None:
        """The real MOEFAS scheme: not an automation scheme, form open today, earliest effective date first."""
        status, body, _ = self._try("get", FAS_SCHEMES, params={"PageNumber": 1, "PageSize": 100})
        if status != 200:
            self.fail("List MOEFAS schemes", status, body)
        now = dt.datetime.now(dt.timezone.utc).date()
        def day(v):
            try:
                return dt.date.fromisoformat(str(v)[:10])
            except Exception:  # noqa: BLE001
                return None
        rows = []
        for x in items_of(body):
            name = str(x.get("name") or "")
            if any(name.upper().startswith(p.upper()) for p in plan.FAS["scheme_exclude_prefixes"]):
                continue
            o_from, o_to, e_from = day(x.get("openFrom")), day(x.get("openTo")), day(x.get("effectiveFrom"))
            rows.append({"id": x.get("id"), "name": name, "status": str(x.get("status") or ""), "open_from": o_from, "open_to": o_to, "effective_from": e_from,
                         "effective_to": day(x.get("effectiveTo")), "total": x.get("totalBudgetAmount"), "used": x.get("usedBudgetAmount"),
                         "remaining": x.get("remainingBudgetAmount"), "form_open": bool(o_from and o_to and o_from <= now <= o_to)})
        rows.sort(key=lambda r: (not r["form_open"], r["effective_from"] or dt.date.max))
        return rows[0] if rows else None

    def moe_pending(self, scheme_id: str) -> dict:
        paths = [p.format(id=scheme_id) + "/pending-allocations" for p in FAS_HQ]
        status, body, _ = self._try("get", paths, params={"PageNumber": 1, "PageSize": 100})
        if status != 200:
            self.fail("Pending allocations of the scheme", status, body)
        d = unwrap(body) or {}
        inner = d.get("items")
        items = inner.get("items") if isinstance(inner, dict) else inner
        return {"summary": d.get("summary") or {}, "items": items or []}

    def moe_confirm(self, scheme_id: str, allocation_ids: list[str], preview_only: bool = False) -> dict:
        tail = "/allocations/preview" if preview_only else "/allocations/confirm"
        payload = {"allocationIds": allocation_ids} if preview_only else {"allocationIds": allocation_ids, "remarks": plan.FAS["remarks"]}
        status, body, _ = self._try("post", [p.format(id=scheme_id) + tail for p in FAS_HQ], data=payload)
        return {"http": status, "data": unwrap(body) if isinstance(body, dict) else {}, "body": body}


def remember_fas(key: str, value) -> None:
    cur = state().get("fas", {})
    cur[key] = value
    remember("fas", cur)


def seeded_students() -> dict:
    """For the UAT cases: the students and parents that carry seeded data (name, nric, e-Service code, parent persona)."""
    return plan.STUDENTS
