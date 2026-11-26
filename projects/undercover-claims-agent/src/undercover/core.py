"""Deterministic business logic: policy, payout, injection screen, evals.

Money and thresholds live here, never in prompts (see guide 03, 05, 10).
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

APPROVAL_THRESHOLD = 1000.0  # payouts above this need human sign-off


@dataclass(frozen=True)
class Cover:
    limit: float
    excess: float
    min_hours: float = 0.0


POLICY: dict[str, Cover] = {
    "baggage_delay": Cover(limit=300.0, excess=0.0, min_hours=12.0),
    "medical": Cover(limit=10000.0, excess=100.0),
}

_INJECTION = [
    r"ignore (all|previous|prior) instructions",
    r"system prompt",
    r"you are now",
    r"approve .* regardless",
]


def is_injection(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in _INJECTION)


def calculate_payout(claim_type: str, claimed: float) -> float:
    cover = POLICY.get(claim_type)
    if cover is None or claimed < 0:
        return 0.0
    return round(max(0.0, min(claimed, cover.limit) - cover.excess), 2)


def rule_decide(claim: dict) -> tuple[str, str]:
    """Baseline decider. Returns (decision, reason). Used offline and as LLM fallback."""
    cover = POLICY.get(claim["type"])
    if cover is None:
        return "REFER", f"type '{claim['type']}' not in auto-decision scope"
    if claim.get("hours", 0) < cover.min_hours:
        return "DECLINE", f"delay {claim.get('hours', 0)}h below {cover.min_hours}h minimum"
    return "APPROVE", "within cover"


# ---------- evals (guide 05) ----------
COST = {("APPROVE", "DECLINE"): 500, ("DECLINE", "APPROVE"): 50,
        ("REFER", "APPROVE"): 20, ("REFER", "DECLINE"): 20,
        ("APPROVE", "REFER"): 10, ("DECLINE", "REFER"): 10}
# key = (truth, predicted). Wrongful decline (truth APPROVE, pred DECLINE) is the costliest.


def cohen_kappa(a: list[str], b: list[str]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("need equal, non-empty label lists")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def expected_cost(truth: list[str], pred: list[str]) -> float:
    return sum(COST.get((t, p), 0) for t, p in zip(truth, pred)) / len(truth)
