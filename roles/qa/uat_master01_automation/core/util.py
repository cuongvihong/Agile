"""Small helpers: money parsing, run state shared between cases."""
from __future__ import annotations

import json
import re
from decimal import Decimal, InvalidOperation

from . import config

_MONEY = re.compile(r"(?:SGD|S\$|\$)\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)")


def money(text: str | None) -> Decimal | None:
    """First money amount in a text: 'SGD 1,000.00', 'S$ 50.00', '$19.5' (non breaking spaces allowed)."""
    if not text:
        return None
    m = _MONEY.search(text.replace(" ", " "))
    if not m:
        return None
    try:
        return Decimal(m.group(1).replace(",", ""))
    except InvalidOperation:
        return None


def amount_after(label: str, text: str) -> Decimal | None:
    """Money amount that follows a label in a page text, for example amount_after('EA BALANCE', body)."""
    t = text.replace(" ", " ")
    i = t.lower().find(label.lower())
    if i < 0:
        return None
    return money(t[i + len(label): i + len(label) + 80])


def norm(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").replace(" ", " ")).strip()


# ---- state shared between cases of one run (application codes, scheme names) ----

def state_get(key: str, default=None):
    try:
        return json.loads(config.STATE_JSON.read_text(encoding="utf-8")).get(key, default)
    except Exception:
        return default


def state_set(key: str, value) -> None:
    try:
        st = json.loads(config.STATE_JSON.read_text(encoding="utf-8"))
    except Exception:
        st = {}
    st[key] = value
    config.STATE_JSON.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")


def state_append(key: str, value) -> None:
    items = state_get(key, []) or []
    if value not in items:
        items.append(value)
    state_set(key, items)


def all_money(text: str | None) -> list[Decimal]:
    out = []
    for m in _MONEY.finditer((text or "").replace(" ", " ")):
        try:
            out.append(Decimal(m.group(1).replace(",", "")))
        except InvalidOperation:
            pass
    return out
