"""Literal prefix comparison with the published old budget, using identical weights.

Author six-covering-3, researcher. Controls may already be excluded by peer trees;
none is presented as a new root exclusion or construction.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

from transport import (MASS, actual_value, known_data, old_encode, require, run)
from application import capacity, prepare
from budget import actual_value as old_actual_value, divisors

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mixed-outside-groups"))
from groups import PairBudgets, fractional_pairs


def fixture(anchors, N=10080):
    anchors = [list(pair) for pair in anchors]
    B = N // 35
    residual = [int(not any(x % n == a for n, a in anchors)) for x in range(N)]
    tops = [B * d for d in (1, 5, 7, 35)]
    return {"period": N, "minimum": 8, "anchors": anchors,
            "residual_count": sum(residual),
            "residual_hex": hex(sum(bit << x for x, bit in enumerate(residual))),
            "available_moduli": [n for n in divisors(N) if n >= 8 and n not in dict(anchors)],
            "four_top_resources": tops,
            "prescribed_top_phases": {str(n): a for n, a in anchors if n in tops}}


def evaluate(data, exe, old_exe, b=48, vectors=None, edges=()):
    B, C, anchors, available, tops, fixed, ux, eta, u, v = prepare(data, b, vectors)
    T, N, Q = B // 6, B * C, b * C
    masks, multiplicities = known_data(B, C, anchors)
    periodic = sum(MASS[masks[q][z]] * v[q % b][z] for q in range(T) for z in range(C))
    old_periodic = sum((6 - multiplicities[q][z]) * v[q % b][z]
                       for q in range(T) for z in range(C))
    known_cost = sum(sum(eta[x % Q] for x in range(a, N, n))
                     for n, a in anchors if n not in tops)
    require(old_periodic == 6 * sum(v[q % b][z] for q in range(T) for z in range(C)) - known_cost,
            "literal known costs disagree with primitive multiplicities")
    baseline = old_periodic - periodic
    require(baseline <= 0, "known baseline unexpectedly positive")
    new_top = run(exe, B, b, u, v, masks, fixed)
    p = subprocess.run([str(old_exe), "--orbits"], input=old_encode(B, b, u, v, fixed),
                       text=True, capture_output=True, check=True, timeout=50)
    old_top = json.loads(p.stdout)
    require(old_actual_value(B, C, b, u, v, [(t, r) for _, t, r in old_top["phases"]])
            == old_top["value"], "old witness score mismatch")
    require(baseline + new_top["value"] <= old_top["value"], "new maximum violates old-bound refinement")
    mixed = [ux[x] + eta[x % Q] for x in range(N)]
    outside = [n for n in available if n not in tops]
    caps = {str(n): capacity(mixed, n) for n in outside}
    cut = fractional_pairs(PairBudgets(ux, [eta[x % Q] for x in range(N)], B), outside, edges)
    require(cut["singleton_numerator"] == cut["scale"] * sum(caps.values()), "capacity mismatch")
    new_demand, old_demand = sum(ux) + periodic, sum(ux) + old_periodic
    new_gap = new_demand - sum(caps.values()) - new_top["value"]
    old_gap = old_demand - sum(caps.values()) - old_top["value"]
    require(new_gap >= old_gap, "new necessary gap became weaker")
    return {"period": N, "minimum": 8, "b": b, "anchors": data["anchors"],
            "residual_count": data["residual_count"], "outside_resources": len(outside),
            "known_mask_histogram": {str(k): v for k, v in sorted(Counter(x for row in masks for x in row).items())},
            "ordinary_demand": sum(ux), "new_periodic_demand": periodic,
            "old_periodic_demand": old_periodic, "baseline": baseline,
            "new_demand": new_demand, "old_demand": old_demand,
            "outside_capacity_total": sum(caps.values()),
            "new_top": new_top, "old_top": old_top,
            "new_strict_gap": new_gap, "old_strict_gap": old_gap,
            "gap_improvement": new_gap - old_gap,
            "outside_group_saving_numerator": cut["saving_numerator"],
            "group_scale": cut["scale"],
            "new_group_gap_numerator": cut["scale"] * (new_demand - new_top["value"]) - cut["outside_numerator"],
            "old_group_gap_numerator": cut["scale"] * (old_demand - old_top["value"]) - cut["outside_numerator"],
            "scope": "same-vector necessary-bound comparison; no exclusion if the gap is nonpositive"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path, required=True)
    parser.add_argument("--old-optimizer", type=Path, required=True)
    args = parser.parse_args()
    prefixes = {
        "01d4": ((8, 0), (9, 0), (10, 0), (14, 1), (12, 4)),
        "former01d0": ((8, 0), (9, 0), (10, 0), (14, 1), (12, 0)),
        "former_known32_node": ((8, 0), (9, 0), (10, 0), (14, 0), (12, 10),
                                (16, 1), (15, 2), (32, 9), (18, 6))}
    edges = ((18, 28, 2), (15, 16, 2), (20, 21, 2), (30, 32, 2), (24, 70, 2),
             (35, 36, 2), (56, 90, 2), (40, 63, 2), (45, 112, 2))
    result = {}
    for name, anchors in prefixes.items():
        result[name] = evaluate(fixture(anchors), args.optimizer.resolve(), args.old_optimizer.resolve(),
                                edges=edges if name != "former_known32_node" else ())
    expected = Path(__file__).with_name("expected-application.json")
    if expected.exists():
        require(result == json.loads(expected.read_text()), "published application mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
