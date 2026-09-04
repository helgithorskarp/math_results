#!/usr/bin/env python3
"""Centralizer-normalized formulas for the two residual order-nine types."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / (
    "ramsey_r55_order9_partial_automorphism_obstruction/generate_formula.py"
)
SOURCE_SHA256 = "ff4e41859de3189a7ab87b34a0de4b841d38d59c304a17c90cba0e243a846a87"
SPEC = importlib.util.spec_from_file_location("order9_base", SOURCE)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
CASES = ((3, 5, 1), (4, 2, 1))


def block(variables, values):
    return tuple(-variable if value else variable
                 for variable, value in zip(variables, values, strict=True))


def symmetry_clauses(case):
    """Keep one representative by sorting profiles, then normalizing phases."""
    mapping, _ = BASE.edge_mapping(case)
    cycles = BASE.vertex_cycles(case)
    nines = [cycle for cycle in cycles if len(cycle) == 9]
    threes = [cycle for cycle in cycles if len(cycle) == 3]
    result = set()
    for group, width in ((nines, 4), (threes, 1)):
        profiles = [[mapping[tuple(sorted((cycle[0], cycle[d])))]
                     for d in range(1, width + 1)] for cycle in group]
        words = list(itertools.product((0, 1), repeat=width))
        for left, right in zip(profiles, profiles[1:]):
            for a in words:
                for b in words:
                    if a > b:
                        result.add(block(left + right, a + b))
    anchor = nines[0][0]
    for cycle in nines[1:] + threes:
        cross = [mapping[tuple(sorted((anchor, vertex)))] for vertex in cycle]
        if len(set(cross)) != len(cycle):
            raise AssertionError("cross word does not have distinct variables")
        for word in itertools.product((0, 1), repeat=len(cycle)):
            if any(word[shift:] + word[:shift] < word for shift in range(len(cycle))):
                result.add(block(cross, word))
    return result


def build(case):
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("base generator hash mismatch")
    if case not in CASES:
        raise ValueError("not one of the two residual types")
    variables, base, distribution, _ = BASE.build(case, False)
    clauses = sorted(set(base) | symmetry_clauses(case), key=lambda c: (len(c), c))
    return variables, clauses, distribution, len(base)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=(0, 1), required=True)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    case = CASES[args.case]
    variables, clauses, distribution, base_count = build(case)
    with args.output.open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    print(f"case={case} variables={variables} clauses={len(clauses)} "
          f"symmetry_clauses={len(clauses)-base_count} orbit_sizes={distribution} "
          f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
