#!/usr/bin/env python3
"""Exact SAT verifier for the three lex-S13 radius-three FC certificates.

The mathematical reduction is explained in README.md.  Subsets of [9] are
9-bit integers.  The solver is asked whether a union-closed family stable
under a candidate configuration can violate its displayed Poonen weight.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from pysat.formula import CNF
from pysat.pb import EncType, PBEnc
from pysat.solvers import Solver


N = 9
SUBSETS = tuple(range(1 << N))
POINTS = tuple(range(1, N + 1))
SWAPS = ((1, 2), (3, 4), (6, 7), (8, 9))


def mask(items: tuple[int, ...]) -> int:
    return sum(1 << (item - 1) for item in items)


def lex_blocks() -> tuple[int, ...]:
    return tuple(mask(block) for block in itertools.combinations(POINTS, 4))


L13 = lex_blocks()[:13]
L13_SET = frozenset(L13)


def union_closure(generators: tuple[int, ...]) -> frozenset[int]:
    closure = {0}
    for generator in generators:
        closure |= {member | generator for member in tuple(closure)}
    return frozenset(closure)


def subgroup() -> tuple[tuple[int, ...], ...]:
    permutations = []
    for choices in itertools.product((False, True), repeat=len(SWAPS)):
        permutation = list(POINTS)
        for chosen, (left, right) in zip(choices, SWAPS):
            if chosen:
                permutation[left - 1], permutation[right - 1] = (
                    permutation[right - 1], permutation[left - 1]
                )
        permutations.append(tuple(permutation))
    return tuple(permutations)


GROUP = subgroup()


def permute_mask(member: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << (permutation[index] - 1)
        for index in range(N)
        if member & (1 << index)
    )


def permute_family(
    family: tuple[int, ...] | frozenset[int], permutation: tuple[int, ...]
) -> frozenset[int]:
    return frozenset(permute_mask(member, permutation) for member in family)


def permute_weights(
    weights: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    result = [0] * N
    for old_index, image in enumerate(permutation):
        result[image - 1] = weights[old_index]
    return tuple(result)


def added_block(edge: tuple[int, int]) -> int:
    return mask((edge[0], edge[1], 8, 9))


REPRESENTATIVES = {
    "16-57-67": (
        tuple(sorted(added_block(edge) for edge in ((1, 6), (5, 7), (6, 7)))),
        (2, 2, 1, 1, 2, 2, 2, 2, 2),
    ),
    "36-57-67": (
        tuple(sorted(added_block(edge) for edge in ((3, 6), (5, 7), (6, 7)))),
        (1, 1, 1, 0, 1, 1, 1, 1, 1),
    ),
    "56-57-67": (
        tuple(sorted(added_block(edge) for edge in ((5, 6), (5, 7), (6, 7)))),
        (2, 2, 1, 1, 2, 2, 2, 2, 2),
    ),
}


def avoidance_count(family: tuple[int, ...], point: int) -> int:
    bit = 1 << (point - 1)
    return sum(not member & bit for member in family)


def radius_three_candidates() -> tuple[tuple[int, ...], ...]:
    base_avoidance = tuple(avoidance_count(L13, point) for point in POINTS)
    capacity = tuple(11 - count for count in base_avoidance)
    hard = tuple(added_block(edge) for edge in itertools.combinations(range(1, 8), 2))
    candidates = []
    for added in itertools.combinations(hard, 3):
        if all(
            avoidance_count(added, point) <= capacity[point - 1]
            for point in POINTS
        ):
            candidates.append(tuple(sorted(added)))
    return tuple(candidates)


def verify_structure() -> dict[str, object]:
    assert len(L13) == len(L13_SET) == 13
    assert tuple(avoidance_count(L13, point) for point in POINTS) == (
        0, 0, 7, 7, 9, 10, 10, 11, 11
    )
    assert len(GROUP) == 16
    assert all(permute_family(L13, permutation) == L13_SET for permutation in GROUP)

    candidates = radius_three_candidates()
    assert len(candidates) == 9
    representatives = {family for family, _weights in REPRESENTATIVES.values()}
    orbit_map: dict[tuple[int, ...], tuple[str, tuple[int, ...]]] = {}
    for name, (representative, weights) in REPRESENTATIVES.items():
        assert min(weights) >= 0 and sum(weights) > 0
        for permutation in GROUP:
            image = tuple(sorted(permute_family(representative, permutation)))
            if image in candidates:
                transported = permute_weights(weights, permutation)
                previous = orbit_map.get(image)
                if previous is not None:
                    # Different automorphisms of one representative must give
                    # the same certificate, so there is no hidden choice.
                    assert previous[1] == transported
                else:
                    orbit_map[image] = (name, transported)
    assert set(orbit_map) == set(candidates)
    assert {source for source, _weights in orbit_map.values()} == set(REPRESENTATIVES)
    assert len(representatives) == 3

    return {
        "candidate_count": len(candidates),
        "orbit_count": len(representatives),
        "orbit_sizes": sorted(
            [sum(source == name for source, _weights in orbit_map.values()) for name in REPRESENTATIVES],
            reverse=True,
        ),
        "subgroup_order": len(GROUP),
    }


def variable(subset: int) -> int:
    return subset + 1


def poonen_coefficients(weights: tuple[int, ...]) -> tuple[int, ...]:
    total = sum(weights)
    return tuple(
        2 * sum(weights[index] for index in range(N) if subset & (1 << index))
        - total
        for subset in SUBSETS
    )


def build_cnf(
    added: tuple[int, ...], weights: tuple[int, ...]
) -> tuple[CNF, dict[str, int]]:
    cnf = CNF()
    generators = L13 + added

    stability = 0
    for subset in SUBSETS:
        for generator in generators:
            target = subset | generator
            if target != subset:
                cnf.append([-variable(subset), variable(target)])
                stability += 1

    unions = 0
    for left in SUBSETS:
        for right in range(left + 1, 1 << N):
            union = left | right
            if union != right:
                cnf.append([-variable(left), -variable(right), variable(union)])
                unions += 1

    coefficients = poonen_coefficients(weights)
    literals: list[int] = []
    magnitudes: list[int] = []
    negative_sum = 0
    for subset, coefficient in enumerate(coefficients):
        if coefficient > 0:
            literals.append(variable(subset))
            magnitudes.append(coefficient)
        elif coefficient < 0:
            literals.append(-variable(subset))
            magnitudes.append(-coefficient)
            negative_sum += -coefficient

    # sum(coefficients[s] * x_s) <= -1 is equivalent to this weighted
    # at-most constraint after complementing all negative terms.
    encoded = PBEnc.atmost(
        lits=literals,
        weights=magnitudes,
        bound=negative_sum - 1,
        top_id=1 << N,
        encoding=EncType.best,
    )
    cnf.extend(encoded.clauses)
    return cnf, {
        "stability_clauses": stability,
        "union_clauses": unions,
        "pb_clauses": len(encoded.clauses),
    }


def cnf_digest(cnf: CNF) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {cnf.nv} {len(cnf.clauses)}\n".encode())
    for clause in cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


def check_case(name: str, solver_name: str) -> dict[str, object]:
    added, weights = REPRESENTATIVES[name]
    assert set(L13).isdisjoint(added)
    assert all(member.bit_count() == 4 for member in added)
    assert union_closure(L13 + added)
    cnf, counts = build_cnf(added, weights)
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
        if satisfiable:
            model = set(literal for literal in solver.get_model() if literal > 0)
            family = frozenset(subset for subset in SUBSETS if variable(subset) in model)
            coefficients = poonen_coefficients(weights)
            assert all(s | generator in family for s in family for generator in L13 + added)
            assert all(s | t in family for s in family for t in family)
            assert sum(coefficients[s] for s in family) <= -1
            raise AssertionError(f"{name}: solver found a checked violating family")
    return {
        "case": name,
        "added_masks": list(added),
        "weights": list(weights),
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "cnf_sha256": cnf_digest(cnf),
        **counts,
        "status": "UNSAT",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--case", choices=tuple(REPRESENTATIVES))
    parser.add_argument("--skip-expected", action="store_true")
    args = parser.parse_args()

    structure = verify_structure()
    names = (args.case,) if args.case else tuple(REPRESENTATIVES)
    cases = [check_case(name, args.solver) for name in names]
    result = {"structure": structure, "cases": cases, "status": "VERIFIED"}

    if not args.skip_expected and args.case is None and args.solver == "cadical195":
        expected_path = Path(__file__).with_name("EXPECTED_RESULTS.json")
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert result == expected
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
