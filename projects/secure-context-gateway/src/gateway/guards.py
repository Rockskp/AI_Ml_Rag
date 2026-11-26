"""Guardrails applied to tool inputs/outputs at the gateway (guide 10)."""
from __future__ import annotations

import re

_INJECTION = re.compile(r"ignore (all|previous|prior) instructions|system prompt|you are now", re.I)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_CARD = re.compile(r"\b(?:\d[ -]?){13,16}\b")
EGRESS_ALLOWLIST = {"undercover.example"}


def mask_pii(text: str) -> str:
    return _CARD.sub("[CARD]", _EMAIL.sub("[EMAIL]", text))


def quarantine(text: str) -> str:
    """Tool output is untrusted data. Mask PII and neutralise instruction-like content."""
    text = mask_pii(text)
    if _INJECTION.search(text):
        return "[REDACTED: content looked like instructions to an AI system]"
    return text


def egress_allowed(url: str) -> bool:
    m = re.match(r"https://([^/:]+)", url)
    return bool(m) and m.group(1).lower() in EGRESS_ALLOWLIST
