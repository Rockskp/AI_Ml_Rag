"""LangGraph claims workflow: screen -> assess -> calculate -> (human gate) -> pay -> record.

Durable via a checkpointer keyed by thread_id = claim_id (guide 07).
"""
from __future__ import annotations

import operator
from typing import Annotated, Callable, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, RetryPolicy, interrupt

from .core import APPROVAL_THRESHOLD, calculate_payout, is_injection, rule_decide

Decider = Callable[[dict], tuple[str, str]]


class ClaimState(TypedDict, total=False):
    claim: dict
    decision: str
    reason: str
    payout: float
    approver: str
    audit: Annotated[list[str], operator.add]


class PaymentLedger:
    """Stand-in for a payments API that dedups on idempotency key."""

    def __init__(self) -> None:
        self.paid: dict[str, float] = {}

    def pay(self, idempotency_key: str, amount: float) -> None:
        self.paid.setdefault(idempotency_key, amount)


def build_graph(decider: Decider = rule_decide, ledger: PaymentLedger | None = None, checkpointer=None):
    ledger = ledger or PaymentLedger()

    def screen(s: ClaimState):
        if is_injection(s["claim"].get("text", "")):
            return {"decision": "REFER", "reason": "possible prompt injection", "audit": ["screen:flagged"]}
        return {"audit": ["screen:ok"]}

    def assess(s: ClaimState):
        decision, reason = decider(s["claim"])
        return {"decision": decision, "reason": reason, "audit": [f"assess:{decision}"]}

    def calculate(s: ClaimState):
        p = calculate_payout(s["claim"]["type"], float(s["claim"]["claimed"]))
        return {"payout": p, "audit": [f"payout:{p}"]}

    def human_gate(s: ClaimState) -> Command[Literal["pay", "record"]]:
        answer = interrupt({"claim_id": s["claim"]["claim_id"], "payout": s["payout"], "reason": s["reason"]})
        if answer.get("approved") is True:
            return Command(goto="pay", update={"approver": answer.get("by", "?"), "audit": ["human:approved"]})
        return Command(goto="record", update={"decision": "REFER", "reason": "human rejected",
                                              "audit": ["human:rejected"]})

    def pay(s: ClaimState):
        ledger.pay(s["claim"]["claim_id"], s["payout"])
        return {"audit": ["paid"]}

    def record(s: ClaimState):
        return {"audit": [f"record:{s['decision']}"]}

    def after_screen(s: ClaimState) -> str:
        return "record" if s.get("decision") == "REFER" else "assess"

    def after_assess(s: ClaimState) -> str:
        return "calculate" if s["decision"] == "APPROVE" else "record"

    def after_calc(s: ClaimState) -> str:
        return "human_gate" if s["payout"] > APPROVAL_THRESHOLD else "pay"

    g = StateGraph(ClaimState)
    g.add_node("screen", screen)
    g.add_node("assess", assess, retry_policy=RetryPolicy(max_attempts=3))
    g.add_node("calculate", calculate)
    g.add_node("human_gate", human_gate)
    g.add_node("pay", pay, retry_policy=RetryPolicy(max_attempts=3))
    g.add_node("record", record)
    g.add_edge(START, "screen")
    g.add_conditional_edges("screen", after_screen, ["assess", "record"])
    g.add_conditional_edges("assess", after_assess, ["calculate", "record"])
    g.add_conditional_edges("calculate", after_calc, ["human_gate", "pay"])
    g.add_edge("pay", "record")
    g.add_edge("record", END)
    return g.compile(checkpointer=checkpointer or InMemorySaver()), ledger


def run_claim(app, claim: dict) -> dict:
    cfg = {"configurable": {"thread_id": claim["claim_id"]}}
    out = app.invoke({"claim": claim, "audit": []}, cfg)
    pending = bool(app.get_state(cfg).interrupts)
    return {**out, "status": "PENDING_APPROVAL" if pending else "DONE"}


def resume_claim(app, claim_id: str, approved: bool, by: str) -> dict:
    cfg = {"configurable": {"thread_id": claim_id}}
    return app.invoke(Command(resume={"approved": approved, "by": by}), cfg)
