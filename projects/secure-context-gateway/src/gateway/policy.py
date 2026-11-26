"""Tiny Cedar-style policy engine: default deny, any matching forbid wins over permit (guide 10, 11).

Production: use real Cedar (cedarpy / AgentCore Policy) or OPA. This mirrors the semantics for learning and tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Principal:
    id: str
    roles: frozenset[str]
    customer_id: str | None = None   # set for customers; None for staff


@dataclass(frozen=True)
class Rule:
    effect: str                                   # "permit" | "forbid"
    action: str                                   # tool name or "*"
    when: Callable[[Principal, dict], bool] = field(default=lambda p, c: True)
    name: str = ""


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def evaluate(rules: list[Rule], principal: Principal, action: str, context: dict) -> Decision:
    matching = [r for r in rules if r.action in (action, "*") and r.when(principal, context)]
    forbids = [r for r in matching if r.effect == "forbid"]
    if forbids:
        return Decision(False, f"forbid:{forbids[0].name}")
    permits = [r for r in matching if r.effect == "permit"]
    if permits:
        return Decision(True, f"permit:{permits[0].name}")
    return Decision(False, "default-deny")


def _own(p: Principal, c: dict) -> bool:
    return p.customer_id is not None and c.get("customer_id") == p.customer_id


POLICIES: list[Rule] = [
    Rule("permit", "get_definition", name="glossary-public"),
    Rule("permit", "get_claim_history", lambda p, c: "handler" in p.roles, "handler-reads-all"),
    Rule("permit", "get_claim_history", _own, "customer-reads-own"),
    Rule("permit", "approve_payout", lambda p, c: "agent" in p.roles and c.get("amount", 0) <= 1000,
         "agent-small-payout"),
    Rule("permit", "approve_payout", lambda p, c: "handler" in p.roles and c.get("human_approved") is True,
         "handler-signed-off"),
    Rule("forbid", "approve_payout", lambda p, c: c.get("amount", 0) > 10000, "hard-cap"),
    Rule("forbid", "*", lambda p, c: "suspended" in p.roles, "suspended"),
]
