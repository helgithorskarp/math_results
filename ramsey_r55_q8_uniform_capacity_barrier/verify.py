#!/usr/bin/env python3
"""Exact finite checks for PROOF.md; no solver or graph catalog is used.

This checks the bound-table arithmetic and literal small-core controls, not
the imported Ramsey theorems or all 11-vertex graphs. The general argument
and its explicitly limited scope are in PROOF.md.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def capacity(s, t):
    s, t = sorted((s, t))
    if s == 1:
        return 1
    if s == 2:
        return t
    return {(3, 3): 6, (3, 4): 9, (3, 5): 14,
            (4, 4): 18, (4, 5): 25}[s, t]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def arithmetic_certificate():
    weight = Fraction(1, 64)
    require(sum((weight for _ in range(2048)), Fraction()) == 32,
            "total mass")
    rows = []
    for a, b in product(range(4), repeat=2):
        if a + b == 0:
            continue
        red = (1 << a) - 1
        blue = ((1 << b) - 1) << a
        count = sum(s & red == red and s & blue == 0 for s in range(2048))
        require(count == 2 ** (11 - a - b), "literal cylinder count")
        core_bound = capacity(4-a, 4-b)-1
        bound = capacity(5-a, 5-b)-1
        mass = count * weight
        slack = bound-core_bound-mass
        require(slack >= 0, "capacity violation")
        # Independent integer form of the same table check.
        require((bound-core_bound) * 2 ** (a+b) >= 32,
                "integer capacity violation")
        rows.append(dict(a=a, b=b, signatures=count, core_upper=core_bound,
                         total_capacity=bound, external_mass=str(mass),
                         worst_case_slack=str(slack)))
    multiplicities = [capacity(5-p, 5-q)-1
                      for p, q in product(range(4), repeat=2) if p+q]
    require(min(multiplicities) == 1 and weight <= min(multiplicities),
            "individual signature capacity")
    return dict(signatures=2048, each_weight=str(weight), total_mass="32",
                size_classes=len(rows), rows=rows,
                minimum_individual_signature_capacity=min(multiplicities))


def small_core_controls(n):
    """Literal labeled graph enumeration, with A and B excluded from U.

    The 32/2^(a+b) mass calculation is used only to test the generic
    occupant-bound inequality; these small graphs are not q8 tasks.
    """
    pairs = list(combinations(range(n), 2))
    full = (1 << n)-1
    masks = list(range(1 << n))
    four_sets = [m for m in masks if m.bit_count() == 4]
    valid = tested = tight = 0
    for edge_bits in range(1 << len(pairs)):
        adj = [0]*n
        for k, (u, v) in enumerate(pairs):
            if edge_bits >> k & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u

        def clique(mask, color):
            vertices = [v for v in range(n) if mask >> v & 1]
            return all(bool(adj[u] >> v & 1) == color
                       for u, v in combinations(vertices, 2))

        if any(clique(m, True) or clique(m, False) for m in four_sets):
            continue
        valid += 1
        reds = [m for m in masks if m.bit_count() <= 3 and clique(m, True)]
        blues = [m for m in masks if m.bit_count() <= 3 and clique(m, False)]
        for a_mask, b_mask in product(reds, blues):
            if a_mask & b_mask or not (a_mask | b_mask):
                continue
            a, b = a_mask.bit_count(), b_mask.bit_count()
            eligible = full ^ (a_mask | b_mask)
            occupants = sum(bool(eligible >> v & 1)
                            and adj[v] & a_mask == a_mask
                            and adj[v] & b_mask == 0 for v in range(n))
            core_bound = capacity(4-a, 4-b)-1
            require(occupants <= core_bound, "small-core occupant bound")
            residual = capacity(5-a, 5-b)-1-occupants
            require(residual * 2 ** (a+b) >= 32,
                    "small-core uniform-cylinder violation")
            tested += 1
            tight += residual * 2 ** (a+b) == 32
    if n == 4:
        require(valid == 62, "four-vertex control count")
    return dict(order=n, labeled_graphs=1 << len(pairs), valid_cores=valid,
                mixed_pairs_checked=tested, tight_cylinders=tight)


def verify():
    return dict(status="VERIFIED_UNIFORM_FRACTIONAL_CAPACITY_BARRIER",
                arithmetic=arithmetic_certificate(),
                controls=[small_core_controls(n) for n in (4, 5)],
                original_q8_tasks=546356*4,
                new_original_task_exclusions=0, new_good43=0,
                target_solver_calls=0, catalog_records_read=0,
                physical_task_feasibility="UNDECIDED",
                trust="Imported Ramsey bounds and the general proof are not formalized.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.expected:
        require(result == json.loads(args.expected.read_text()),
                "saved result differs from recomputation")
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
