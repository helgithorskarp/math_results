#!/usr/bin/env python3
"""Independent physical-premise audit, bit-mask RUP replay, and exact counts.

Does not import build.py or interface.py. RUP uses repeated whole-formula
scans, independently of the generating solver and the earlier occurrence
checker in ramsey_r55_one_sided_induced_path/check_rup.py.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from collections import Counter
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def masks(clause, variables):
    positive = negative = 0
    for x in clause:
        require(type(x) is int and 0 < abs(x) <= variables, "invalid literal")
        bit = 1 << (abs(x) - 1)
        require(not (positive | negative) & bit, "duplicate variable in clause")
        if x > 0:
            positive |= bit
        else:
            negative |= bit
    return positive, negative


def propagation(formula, assumptions):
    true = false = 0
    steps = 0
    for x in assumptions:
        if x > 0:
            true |= 1 << (x - 1)
        else:
            false |= 1 << (-x - 1)
    if true & false:
        return True, steps
    while True:
        changed = False
        for pos, neg in formula:
            if pos & true or neg & false:
                continue
            rest = (pos | neg) & ~(true | false)
            if rest == 0:
                return True, steps
            if rest & (rest - 1) == 0:
                if rest & pos:
                    true |= rest
                else:
                    false |= rest
                steps += 1
                changed = True
        if not changed:
            return False, steps


def replay(premises, proof, variables, final):
    formula = [masks(c, variables) for c in premises]
    steps = 0
    require(bool(proof), "empty proof")
    for index, c in enumerate(proof):
        encoded = masks(c, variables)
        conflict, count = propagation(formula, [-x for x in c])
        require(conflict, f"addition {index} is not RUP")
        formula.append(encoded)
        steps += count
    require(set(proof[-1]) == set(final), "wrong final clause")
    return {"additions": len(proof), "propagations": steps}


def expected_template():
    # Independently reconstruct by assigning each vertex a module index.
    block = dict(zip(range(1, 19), [0]*4 + [1]*4 + [2]*4 + [3]*3 + [4]*3))
    fixed, free = {}, []
    for u, v in it.combinations(range(19), 2):
        if u == 0:
            fixed[u, v] = 1
        elif block[u] == block[v]:
            free.append((u, v))
        else:
            fixed[u, v] = int((block[u] - block[v]) % 5 in (1, 4))
    return fixed, free


def audit_package(package):
    data = json.loads((package / "TEMPLATE.json").read_text())
    fixed, free = expected_template()
    require(data["n"] == 43 and data["root"] == 0, "incorrect size or root")
    require(data["modules"] == [list(range(1, 5)), list(range(5, 9)),
                               list(range(9, 13)), [13, 14, 15], [16, 17, 18]],
            "incorrect module metadata")
    require(data["fixed"] == [[*p, c] for p, c in sorted(fixed.items())],
            "incorrect fixed template")
    require(data["local_pairs"] == [list(p) for p in free], "incorrect local map")
    require(len(fixed) == 147 and sum(fixed.values()) == 83 and len(free) == 24,
            "incorrect template counts")
    ids = {p: i + 1 for i, p in enumerate(free)}
    local = []
    for p in data["premises"]:
        vertices, color = p["vertices"], p["color"]
        require(color in (0, 1) and len(vertices) == len(set(vertices)) == 5
                and vertices == sorted(vertices)
                and all(type(v) is int and 0 <= v < 19 for v in vertices),
                "invalid five-set premise")
        pairs = list(it.combinations(vertices, 2))
        require(all(fixed[e] == color for e in pairs if e in fixed),
                "premise is already satisfied by constants")
        require(all(e in fixed or e in ids for e in pairs), "unbound premise pair")
        clause = [(1 - 2 * color) * ids[e] for e in pairs if e in ids]
        require(p["local_clause"] == clause, "incorrect premise substitution")
        local.append(clause)
    # Independently enumerate every required K4/I5 clause on all 18 vertices.
    expected = set()
    for size, color in ((4, 1), (5, 0)):
        for vertices in it.combinations(range(1, 19), size):
            pairs = list(it.combinations(vertices, 2))
            if all(fixed[e] == color for e in pairs if e in fixed):
                expected.add(tuple((1 - 2 * color) * ids[e] for e in pairs if e in ids))
    require(len(local) == len(expected) and set(map(tuple, local)) == expected,
            "incomplete or duplicated local formula")
    proof = []
    for line in (package / "proof.rup").read_text().splitlines():
        xs = list(map(int, line.split()))
        require(xs and xs[-1] == 0 and 0 not in xs[:-1], "bad proof syntax")
        proof.append(xs[:-1])
    initial = propagation([masks(c, 24) for c in local], [])
    require(initial == (False, 0), "initial local UP is not silent")
    return data, replay(local, proof, 24, [])


def audit_cut(cut):
    fixed, free = expected_template()
    labels, color = cut["vertices"], cut["color"]
    require(type(color) is int and color in (0, 1), "invalid transport color")
    require(len(labels) == len(set(labels)) == 19
            and all(type(v) is int and 0 <= v < 43 for v in labels), "bad relabelling")
    physical_pairs = list(it.combinations(range(43), 2))
    ids = {p: i + 1 for i, p in enumerate(physical_pairs)}
    actual = {tuple(sorted((labels[u], labels[v]))): c if color else 1 - c
              for (u, v), c in fixed.items()}
    wanted_physical = sorted([*p, 1 - c] for p, c in actual.items())
    require(sorted(cut["physical_clause"]) == wanted_physical, "wrong physical guard")
    guard = sorted((1 - 2 * c) * ids[p] for p, c in actual.items())
    require(sorted(cut["canonical_clause"]) == guard, "wrong canonical guard")
    premises = []
    for p in cut["canonical_premises"]:
        v, c = p["vertices"], p["color"]
        require(type(c) is int and c in (0, 1) and len(v) == len(set(v)) == 5
                and all(type(x) is int and 0 <= x < 43 for x in v),
                "invalid Ramsey premise")
        literal = sorted((1 - 2 * c) * ids[e] for e in it.combinations(sorted(v), 2))
        require(sorted(p["clause"]) == literal, "premise is not a literal Ramsey clause")
        premises.append(p["clause"])
    result = replay(premises, cut["canonical_rup"], 903, guard)
    # Full global CNF under this template: inside 19 vertices audited literally;
    # any five-set using outside vertices has at least four unknown edges.
    widths, satisfied = Counter(), 0
    for v in it.combinations(sorted(labels), 5):
        pairs = list(it.combinations(v, 2))
        for c in (0, 1):
            if any(e in actual and actual[e] != c for e in pairs):
                satisfied += 1
            else:
                widths[sum(e not in actual for e in pairs)] += 1
    require(not widths[0] and not widths[1], "global CNF has initial empty/unit clause")
    outside_min = min(t*(5-t) + math.comb(t, 2) for t in range(1, 6))
    require(outside_min >= 2, "outside unit clause possible")
    result.update({"premises": len(premises), "guard_literals": len(guard),
                   "inside_19_satisfied": satisfied,
                   "inside_19_unsatisfied_widths": {str(k): v for k, v in sorted(widths.items()) if v},
                   "outside_clause_count": 2*(math.comb(43, 5)-math.comb(19, 5)),
                   "outside_unknown_width_at_least": outside_min,
                   "initial_global_units": 0, "initial_global_empty_clauses": 0})
    return result


def exact_count():
    single = sum(math.comb(24, t) * sum(math.comb(732, k)
                                     for k in range(307-t, 431-t)) for t in range(7))
    # Independent integer generating-polynomial calculation. Generate the 732
    # unconstrained edges by Pascal additions, then convolve the root polynomial.
    coeff = [1]
    for _ in range(732):
        coeff = [coeff[0]] + [coeff[i-1] + coeff[i] for i in range(1, len(coeff))] + [coeff[-1]]
    root = [1] + [0]*6
    for _ in range(24):
        for t in range(6, 0, -1):
            root[t] += root[t-1]
    dp = sum(root[t] * coeff[k] for t in range(7)
             for k in range(len(coeff)) if 390 <= 83+t+k <= 513)
    require(dp == single, "count implementations disagree")
    require(2*single > 2**750, "declared count gate failed")
    return {"red_family": str(single), "both_disjoint_colors": str(2*single),
            "both_colors_bit_length": (2*single).bit_length(),
            "greater_than_2_to_750": True,
            "root_choices": sum(root), "unconditioned_other_edges": 732,
            "global_edge_window": [390, 513], "root_chosen_color_degree": [18, 24]}


def elementary_controls():
    cycle = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
    tags = []
    for word in range(32):
        active = [i for i in range(5) if word >> i & 1]
        inactive = [i for i in range(5) if not word >> i & 1]
        red_pairs = [p for p in it.combinations(active, 2) if p in cycle]
        blue_pairs = [p for p in it.combinations(inactive, 2) if p not in cycle]
        require(red_pairs or blue_pairs, "uncovered module tag pattern")
        tags.append("root_red_K5" if red_pairs else "blue_K5")
    # P5 has no nontrivial module; this supports the h4015 interpretation only.
    tested = 0
    for size in range(2, 5):
        for subset in it.combinations(range(5), size):
            outside = set(range(5)) - set(subset)
            require(any(0 < sum(abs(u-v) == 1 for u in subset) < size for v in outside),
                    "P5 has a nontrivial module")
            tested += 1
    return {"tag_patterns_covered": len(tags), "P5_nonmodule_subsets": tested}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("cut", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    _, local = audit_package(args.package)
    global_check = audit_cut(json.loads(args.cut.read_text()))
    result = {"status": "VERIFIED_STRUCTURAL_PHYSICAL_CUT", "local_rup": local,
              "global_rup_and_up": global_check, "count": exact_count(),
              "elementary_controls": elementary_controls(),
              "proof_sha256": hashlib.sha256((args.package / "proof.rup").read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
