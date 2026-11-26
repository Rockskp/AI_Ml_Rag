"""Run the eval: python -m undercover [--llm]"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .core import cohen_kappa, expected_cost, rule_decide
from .graph import build_graph, run_claim


def main() -> None:
    decider = rule_decide
    if "--llm" in sys.argv:
        from .llm import llm_decider
        decider = llm_decider()
    claims = json.loads((Path(__file__).resolve().parents[2] / "data" / "claims.json").read_text())
    app, ledger = build_graph(decider)
    truth, pred = [], []
    for c in claims:
        out = run_claim(app, c)
        p = out["decision"]
        truth.append(c["label"]); pred.append(p)
        print(f"{c['claim_id']:6} truth={c['label']:8} pred={p:8} status={out['status']:17} payout={out.get('payout', 0)}")
    acc = sum(t == p for t, p in zip(truth, pred)) / len(truth)
    print(f"\naccuracy={acc:.2f} kappa={cohen_kappa(truth, pred):.2f} expected_cost=${expected_cost(truth, pred):.2f}")
    print(f"paid={ledger.paid}")


if __name__ == "__main__":
    main()
