"""Literal controls and a complete actual-prefix pair-budget replay.

Author six-covering-3, researcher. Explicit exceptions remain active under -O.
No floating solver, orbit assumption, or search status is a proof input.
"""

import argparse
import hashlib
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import random
import sys

from groups import PairBudgets, fractional_pairs, require


def literal_score(N, u, v, m, n, a, b, union_v):
    # Intentionally scan physical residues, with no histogram/CRT helper.
    return sum(u[x] * int(x % m == a or x % n == b)
               + v[x] * (int(x % m == a or x % n == b) if union_v else
                         int(x % m == a) + int(x % n == b)) for x in range(N))


def additive(values):
    def at(e, col):
        return values[next(j for j in range(6) if j % 2 == e and j % 3 == col)]
    return all(at(0, c) - at(1, c) == at(0, 0) - at(1, 0) for c in range(3))


def pair_controls():
    rng = random.Random(2026100103)
    pairs = phase_pairs = proper_union_blocks = 0
    for N, B in ((6, 6), (12, 12), (18, 18), (24, 24), (30, 6),
                 (36, 36), (60, 12), (72, 72)):
        C, T = N // B, B // 6
        u = [rng.randrange(7) for _ in range(N)]
        base = [rng.randrange(5) for _ in range(T * C)]
        v = [base[x % (T * C)] for x in range(N)]
        outside = [n for n in range(1, N + 1) if N % n == 0 and gcd(n, B) < B]
        for mode in (None, B):
            oracle = PairBudgets(u, v, mode)
            for m, n in combinations(outside, 2):
                result = oracle.pair(m, n)
                union_v = result["v_mode"] == "union"
                values = [(literal_score(N, u, v, m, n, a, b, union_v), a, b)
                          for a in range(m) for b in range(n)]
                wanted = max(value for value, _, _ in values)
                phases = min((a, b) for value, a, b in values if value == wanted)
                require(result["value"] == wanted and tuple(result["phases"]) == phases,
                        "pair oracle disagrees with literal phase exhaustion")
                pairs += 1
                phase_pairs += m * n
                if union_v:
                    # All union phases, all actual labels and cofactor residues.
                    for a in range(m):
                        for bb in range(n):
                            for q in range(T):
                                for z in range(C):
                                    xs = [next(x for x in range(N)
                                               if x % B == q + T * j and x % C == z)
                                          for j in range(6)]
                                    f = [int(x % m == a or x % n == bb) for x in xs]
                                    require(additive(f), "permitted group union is not additive")
                                    proper_union_blocks += 1
    return {"pair_controls": pairs, "literal_phase_pairs": phase_pairs,
            "proper_union_blocks": proper_union_blocks}


def cover_controls():
    base_cover = ((2, 0), (3, 0), (4, 1), (6, 5), (12, 7))
    rng = random.Random(120241003)
    count = positive_known = negative_lhs = fractional_cases = 0
    safe_groups = general_groups = 0
    for N in (12, 24):
        B, T = N, N // 6
        require(all(any(x % n == a for n, a in base_cover) for x in range(N)),
                "invalid genuine covering control")
        for mask in range(32):
            known = tuple(pair for i, pair in enumerate(base_cover) if mask & (1 << i))
            outside = [n for n in range(2, N) if N % n == 0 and n not in {m for m, _ in known}]
            actual = dict(base_cover)
            for n in (*outside, N):
                actual.setdefault(n, rng.randrange(n))
            for repetition in range(4):
                u = [rng.randrange(8) if not any(x % n == a for n, a in known) else 0
                     for x in range(N)]
                vv = [rng.randrange(7) + 1 for _ in range(T)]
                v = [vv[x % T] for x in range(N)]
                edges = []
                if len(outside) >= 3:
                    for i in range(len(outside)):
                        edge = tuple(sorted((outside[i], outside[(i + 1) % len(outside)])))
                        edges.append((*edge, 1))
                elif len(outside) == 2:
                    edges = [(outside[0], outside[1], 1 + repetition % 2)]
                oracle = PairBudgets(u, v, B if repetition % 2 else None)
                cut = fractional_pairs(oracle, outside, edges)
                known_cost = sum(sum(v[x] for x in range(a, N, n))
                                 for n, a in known if n != N)
                lhs = sum(u) + sum(v) - known_cost
                # One C=1 top always has kappa=0. Its prescribed u cost is0.
                top = 0 if N in dict(known) else max(u)
                require(2 * lhs <= cut["outside_numerator"] + 2 * top,
                        "necessary budget rejects a genuine cover")
                actual_rhs = 2 * sum(u[x] for x in range(actual[N], N, N))
                for n in outside:
                    actual_rhs += cut["singleton_remainders"][str(n)] * sum(
                        u[x] + v[x] for x in range(actual[n], N, n))
                for p in cut["pairs"]:
                    m, n = p["resources"]
                    actual_rhs += p["numerator"] * literal_score(
                        N, u, v, m, n, actual[m], actual[n], p["v_mode"] == "union")
                    safe_groups += p["v_mode"] == "union"
                    general_groups += p["v_mode"] != "union"
                require(2 * lhs <= actual_rhs, "actual group counting fails on a cover")
                count += 1
                positive_known += bool(known)
                negative_lhs += lhs < 0
                fractional_cases += any(p["numerator"] == 1 for p in cut["pairs"])
    return {"genuine_cover_cases": count, "positive_known_v_cases": positive_known,
            "negative_effective_demands": negative_lhs, "fractional_cases": fractional_cases,
            "safe_group_controls": safe_groups, "general_group_controls": general_groups,
            "ambient24_cover_actual_lcm": 12}


def incorrect_union_control():
    N, ns = 12, (2, 3, 4, 6)
    cover = ((2, 0), (3, 0), (4, 1), (6, 5), (12, 7))
    require(all(any(x % n == a for n, a in cover) for x in range(N)), "bad counterexample cover")
    values = [sum(int(any(x % n == a for n, a in zip(ns, phases))) for x in range(N))
              for phases in product(*(range(n) for n in ns))]
    require(len(values) == 144 and max(values) == 11, "wrong incorrect-union control")
    return {"incorrect_union_cover_period": N, "incorrect_union_phase_tuples": len(values),
            "incorrect_union_capacity": max(values), "valid_individual_v_capacity": 15}


def rejection_controls():
    calc = PairBudgets([1] * 12, [1] * 12, 12)
    cases = [lambda: PairBudgets([1], [1, 2]),
             lambda: PairBudgets([-1], [1]),
             lambda: PairBudgets([True], [1]),
             lambda: PairBudgets([1] * 12, [1] * 12, 6),
             lambda: calc.pair(12, 3),
             lambda: calc.pair(3, 3),
             lambda: calc.pair(3, 5),
             lambda: fractional_pairs(calc, [2, 3], [(2, 3, 0)]),
             lambda: fractional_pairs(calc, [2, 3], [(2, 3, 3)]),
             lambda: fractional_pairs(calc, [2, 3], [(2, 3, 0.5)]),
             lambda: fractional_pairs(calc, [2, 3], [(2, 4, 1)]),
             lambda: fractional_pairs(calc, [2, 3], [(2, 3, 1), (3, 2, 1)]),
             lambda: fractional_pairs(calc, [2, 3, 4], [(2, 3, 2), (2, 4, 1)]),
             lambda: fractional_pairs(calc, [2, 2], []),
             lambda: fractional_pairs(calc, [2, 3], [], 0)]
    for case in cases:
        try:
            case()
        except ValueError:
            continue
        raise RuntimeError("invalid group input accepted")
    return {"rejected_inputs": len(cases)}


def target_check(optimizer):
    source = Path(__file__).with_name("input.json")
    data = source.read_bytes()
    fixture = json.loads(data)
    prior = Path(__file__).resolve().parent.parent / "four-top-block-dp"
    sys.path.insert(0, str(prior))
    from application import prepare, evaluate
    B, C, anchors, available, tops, fixed, u, eta, _, _ = prepare(fixture, fixture["b"])
    N, Q = B * C, fixture["b"] * C
    v = [eta[x % Q] for x in range(N)]
    outside = [n for n in available if n not in tops]
    calc = PairBudgets(u, v, B)
    groups = fractional_pairs(calc, outside, fixture["edges"], fixture["scale"])
    # Independent phase exhaustion with literal progression sets.
    phase_pairs = 0
    values_digest = hashlib.sha256()
    for pair in groups["pairs"]:
        m, n = pair["resources"]
        sets_m = [set(range(a, N, m)) for a in range(m)]
        sets_n = [set(range(bb, N, n)) for bb in range(n)]
        um = [sum(u[x] for x in aa) for aa in sets_m]
        un = [sum(u[x] for x in bb) for bb in sets_n]
        vm = [sum(v[x] for x in aa) for aa in sets_m]
        vn = [sum(v[x] for x in bb) for bb in sets_n]
        union_v = pair["v_mode"] == "union"
        best, phases = None, None
        for a, aa in enumerate(sets_m):
            for bb, ss in enumerate(sets_n):
                # Set intersection establishes the literal overlap independently
                # of any compatible-CRT residue or gcd-coset reduction.
                overlap = aa & ss
                score = um[a] + un[bb] + vm[a] + vn[bb] - sum(
                    u[x] + (v[x] if union_v else 0) for x in overlap)
                values_digest.update(f"{score}\n".encode())
                if best is None or score > best:
                    best, phases = score, [a, bb]
                phase_pairs += 1
        require(best == pair["value"] and phases == pair["phases"],
                "target pair differs from literal progression exhaustion")
    result = evaluate(fixture, optimizer, fixture["b"])
    require(groups["singleton_numerator"] == groups["scale"] * result["outside_capacity_total"],
            "outside singleton total mismatch")
    scale = groups["scale"]
    rhs = groups["outside_numerator"] + scale * result["top"]["value"]
    return {"fixture_sha256": hashlib.sha256(data).hexdigest(),
            "period": N, "minimum": 8, "anchors": fixture["anchors"],
            "residual_count": fixture["residual_count"],
            "effective_demand": result["effective_demand"],
            "singleton_total": result["total_capacity"], "top_budget": result["top"],
            "groups": groups, "group_total_numerator": rhs,
            "group_strict_gap_numerator": scale * result["effective_demand"] - rhs,
            "literal_target_phase_pairs": phase_pairs,
            "literal_target_scores_sha256": values_digest.hexdigest(),
            "scope": "same-vector necessary-budget improvement; not an exclusion"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path)
    args = parser.parse_args()
    result = {**pair_controls(), **cover_controls(), **incorrect_union_control(),
              **rejection_controls()}
    if args.optimizer:
        result["target"] = target_check(args.optimizer.resolve())
    expected = Path(__file__).with_name("expected.json" if args.optimizer else "expected-small.json")
    if expected.exists():
        require(result == json.loads(expected.read_text()), "published check output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
