#!/usr/bin/env python3
"""Exact baseline and arithmetic checks for the written two-hub proof.

This checker does not certify the imported local packing theorems. The
finite normalizations and counting bridges are supplied in PROOF.md.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASELINE_SHA256 = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def packing_statistics(raw, expected_size=None):
    rows = raw.decode("ascii").splitlines()
    require(bool(rows), "empty input")
    require(len(set(rows)) == len(rows), "repeated word")
    require(all(len(s) == 18 and set(s) <= {"0", "1"} and s.count("1") == 5
                for s in rows), "invalid length, alphabet or weight")
    if expected_size is not None:
        require(len(rows) == expected_size, "unexpected size")
    blocks = [frozenset(i for i, bit in enumerate(s) if bit == "1") for s in rows]
    distances = Counter(10 - 2 * len(a & b) for a, b in combinations(blocks, 2))
    require(min(distances, default=10) >= 6, "conflicting words")
    point = Counter(x for b in blocks for x in b)
    pair = Counter(t for b in blocks for t in combinations(sorted(b), 2))
    triple = Counter(t for b in blocks for t in combinations(sorted(b), 3))
    require(max(triple.values()) == 1, "repeated triple")
    require(all(point[x] <= 20 for x in range(18)), "point cap fails")
    require(all(pair[xy] <= 5 for xy in combinations(range(18), 2)), "pair cap fails")
    deficit = {xy: 5 - pair[xy] for xy in combinations(range(18), 2)}
    support = {x: {y for y in range(18) if y != x and deficit[tuple(sorted((x, y)))] > 0}
               for x in range(18)}
    saturated = {x for x in range(18) if point[x] == 20}
    unsaturated = set(range(18)) - saturated
    unused = [t for t in combinations(range(18), 3) if not triple[t]]
    bins = Counter(len(set(t) & unsaturated) for t in unused)
    homogeneous = Counter()
    for t in unused:
        for x in t:
            others = set(t) - {x}
            degree = len(others & support[x])
            if x in saturated:
                require(degree > 0, "saturated link has a low-low leave edge")
            if degree in (0, 2):
                homogeneous[x] += 1
    for x in saturated:
        require(homogeneous[x] == len(support[x]) - 1, "local homogeneous count fails")
    excess = sum(max(deficit[tuple(sorted((x, y)))] - 1, 0)
                 for x in saturated for y in range(18) if y != x)
    eta = sum(homogeneous[x] for x in saturated) - bins[0]
    delta = 72 - len(blocks)
    lhs = excess + bins[2] + 2 * bins[3] + eta
    rhs = 12 * len(unsaturated) + 20 * delta - 24
    require(lhs == rhs, "general deficit identity fails")
    for x, y in combinations(range(18), 2):
        count = sum(x in t and y in t for t in unused)
        require(count == 1 + 3 * deficit[(x, y)], "pair leave degree fails")
    return {
        "words": len(blocks),
        "sha256": sha256(raw).hexdigest(),
        "distance_histogram": {str(k): v for k, v in sorted(distances.items())},
        "point_replications": sorted(point[x] for x in range(18)),
        "covered_triples": len(triple),
        "uncovered_triples": len(unused),
        "general_deficit_identity": {"left": lhs, "right": rhs},
    }


def arithmetic():
    # For a quadruple with j points in W, j <= 1 + choose(j,2).
    block_bound = [{"j": j, "incidences": j, "bound": 1 + j * (j - 1) // 2}
                   for j in range(5)]
    require(all(q["incidences"] <= q["bound"] for q in block_bound), "block bound fails")
    survivors = []
    for z in range(3):
        for covered_a in range(7 - z):
            covered_b = 6 - z - covered_a
            for p in range(7):
                if covered_b > p:
                    continue
                pairs = p * (p - 1) // 2
                if covered_a + 2 * z > 2:
                    continue
                if 6 + covered_b > pairs:
                    continue
                if 5 * p + covered_b > 19 + pairs:
                    continue
                survivors.append({"z": z, "covered_a": covered_a,
                                  "covered_b": covered_b, "p": p})
    require(survivors == [
        {"z": 0, "covered_a": 2, "covered_b": 4, "p": 5},
        {"z": 0, "covered_a": 2, "covered_b": 4, "p": 6},
    ], "unexpected boundary inventory")
    independent_a_bounds = []
    for q in survivors:
        size_a = 16 - q["p"]
        lower = 5 * size_a - 18
        require(lower > 28, "independent-cohort contradiction fails")
        independent_a_bounds.append({"p": q["p"], "size_a": size_a,
                                     "degree_sum_lower": lower, "total_graph_edges": 28})
    multiplicity_three = []
    for z in range(4):
        for covered_a in range(10 - z):
            covered_b = 9 - z - covered_a
            for p in range(8):
                pairs = p * (p - 1) // 2
                if covered_b > p or covered_a + 2 * z > 3:
                    continue
                if 6 + covered_b > pairs or 5 * p + covered_b > 20 + pairs:
                    continue
                multiplicity_three.append({"z": z, "covered_a": covered_a,
                                           "covered_b": covered_b, "p": p})
    require(multiplicity_three == [
        {"z": 0, "covered_a": 3, "covered_b": 6, "p": 7}],
        "unexpected multiplicity-three inventory")
    # Independent A has degree sum D>=26. It demands D distinct uncovered
    # triples on pairs of the other seven points; those pairs have total
    # uncovered capacity 21+3*(27-D). Thus 4D<=102, impossible.
    require(4 * 26 > 7 * 6 // 2 + 3 * 27, "pair-capacity contradiction fails")
    return {"block_incidence_checks": block_bound, "budget_survivors": survivors,
            "independent_cohort_contradictions": independent_a_bounds,
            "multiplicity_three_survivors": multiplicity_three,
            "multiplicity_three_capacity": {"degree_sum_lower": 26,
                "four_times_lower": 104, "capacity_bound": 102}}


def affine_nineteen_identity():
    """Check the generic subset identity on all 20 affine line deletions.

    GF(4) is encoded by two-bit polynomials modulo x^2+x+1. Point 4*x+y
    represents (x,y), and point16 is unused. This is a small positive
    control family, not an enumeration of all nineteen-block packings.
    """
    def multiply(a, b):
        value = 0
        for bit in range(2):
            if b & (1 << bit):
                value ^= a << bit
        if value & 4:
            value ^= 7
        return value
    lines = [frozenset(4 * x + y for y in range(4)) for x in range(4)]
    lines += [frozenset(4 * x + (multiply(slope, x) ^ intercept) for x in range(4))
              for slope in range(4) for intercept in range(4)]
    require(len(lines) == len(set(lines)) == 20, "affine fixture differs")
    require(all(len(a & b) <= 1 for a, b in combinations(lines, 2)), "affine pair repeat")
    records = Counter()
    cases = 0
    for deleted in lines:
        blocks = [b for b in lines if b != deleted]
        rho = Counter(x for b in blocks for x in b)
        covered = {xy for b in blocks for xy in combinations(sorted(b), 2)}
        low = {x for x in range(17) if rho[x] == 5}
        mu = sum(xy not in covered for xy in combinations(sorted(low), 2))
        for u in range(17):
            q = rho[u]
            if q >= 5:
                continue
            high_others = {x for x in range(17) if x != u and rho[x] < 5}
            p = len(high_others)
            c = sum(tuple(sorted((u, x))) in covered for x in high_others)
            bins = Counter(len(b & high_others) for b in blocks)
            lhs = bins[0] + bins[3] + 3 * bins[4]
            rhs = p * (p - 1) // 2 - 5 * p + 17 + q - mu - c
            require(lhs == rhs, "generic nineteen-block subset identity fails")
            cases += 1
            records[(q, p, mu, c, lhs)] += 1
    return {"cases": cases, "scope": "20 affine-plane line deletions, all deficient marks",
            "types": [{"q": q, "p": p, "mu": mu, "c": c, "residue": value,
                       "multiplicity": n}
                      for (q, p, mu, c, value), n in sorted(records.items())]}


def rejection_controls(raw):
    rows = raw.decode("ascii").splitlines()
    mutations = {
        "repeated word": ("\n".join(rows + [rows[0]]) + "\n").encode(),
        "wrong weight": ("0" * 18 + "\n" + "\n".join(rows[1:]) + "\n").encode(),
        "wrong alphabet": ("x" + rows[0][1:] + "\n" + "\n".join(rows[1:]) + "\n").encode(),
        "wrong length": (rows[0][:-1] + "\n" + "\n".join(rows[1:]) + "\n").encode(),
    }
    for name, mutation in mutations.items():
        try:
            packing_statistics(mutation)
        except ValueError:
            continue
        raise ValueError("accepted invalid fixture: " + name)
    return sorted(mutations)


def main():
    raw = (HERE / "acl69.txt").read_bytes()
    require(sha256(raw).hexdigest() == BASELINE_SHA256, "baseline source hash differs")
    result = {"baseline": packing_statistics(raw, 69), "arithmetic": arithmetic(),
              "nineteen_block_positive_controls": affine_nineteen_identity(),
              "rejected_controls": rejection_controls(raw),
              "scope": "Exact baseline and integer arithmetic; imported theorems and written proof bridges are separate premises."}
    if "--check" in sys.argv:
        require(json.loads((HERE / "expected.json").read_text()) == result, "expected record differs")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
