#!/usr/bin/env python3
"""Independent finite checks for the triangle-cactus transfer interfaces.

No target module is imported.  The checks use direct exhaustive search and
exact Fraction arithmetic rather than the target's floating-variable engine
or assembly implementation.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "triangle_cactus_packing_transfer"
TARGET_HASHES = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "AUDIT.json": "b7ca4ff56c74e2bcd1a27818f2e8637e7092c8f69793342ef8a3a9f9de56d62a",
    "PROOF.md": "9b413ba8ffb33606e453fa60515ff286f427d5f7ce1e6c0da64de7e61d26cc27",
    "README.md": "9a33079118ff3a3ca370c111a7adb879ba655876c8e13d7ca1ab5c3299e895bd",
    "RUN.json": "b136350b908f022edb9ac6892940c1d742cfaeb35c41a7e70a2c7a7becfee273",
    "SOURCES.md": "728dbf11afa171ab73b19ac9500b9bddc16358c376c278aa202d8d53e9274a00",
    "assembly.py": "f794bfa7ddcf078c1fbc5887b3c9e6f3fb74b75226dff877c05530cce89370b9",
    "check.py": "b66c9bb8acd0ae10ca9ee2d8d5f2e94a6ba77b911e1d25036253f328468c0789",
    "fixtures.py": "44c43da66f3803b57f691c253c514fb87814ea3e0dea0cc7754c2e6e14f4ae9d",
    "rounding.py": "f89037bfa52655841c76756e5df9f3fab3961b6f6a2090ad101a83bd3667dcfe",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def bind_target() -> str:
    records = []
    for name, expected in sorted(TARGET_HASHES.items()):
        actual = sha256((TARGET / name).read_bytes()).hexdigest()
        need(actual == expected, f"target hash mismatch: {name}")
        records.append((name, actual))
    return sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()


def row_sums(groups: tuple[tuple[int, int], ...], probabilities: tuple[Fraction, ...],
             choices: tuple[int, ...], rows: int = 4) -> list[Fraction]:
    sums = [Fraction(0) for _ in range(rows)]
    for (option0, option1), probability, choice in zip(groups, probabilities, choices):
        mask = (option0, option1)[choice]
        for row in range(rows):
            sums[row] += bool((mask >> row) & 1)
    return sums


def fractional_row_sums(groups: tuple[tuple[int, int], ...],
                        probabilities: tuple[Fraction, ...], rows: int = 4) -> list[Fraction]:
    sums = [Fraction(0) for _ in range(rows)]
    for (option0, option1), probability in zip(groups, probabilities):
        for row in range(rows):
            sums[row] += probability * bool((option0 >> row) & 1)
            sums[row] += (1 - probability) * bool((option1 >> row) & 1)
    return sums


def best_error(groups: tuple[tuple[int, int], ...],
               probabilities: tuple[Fraction, ...]) -> Fraction:
    target = fractional_row_sums(groups, probabilities)
    best = None
    for choices in product((0, 1), repeat=len(groups)):
        actual = row_sums(groups, probabilities, choices)
        error = max((abs(x-y) for x, y in zip(actual, target)), default=Fraction(0))
        best = error if best is None else min(best, error)
    need(best is not None, "no integral partition choice")
    return best


def check_partition_rounding() -> dict:
    """Brute-force integral choices; do not replay the target algorithm."""
    masks = (0, 1, 2, 4, 8)  # column sparsity at most one
    types = tuple(combinations_with_replacement(masks, 2))
    half_cases = 0
    maximum = Fraction(0)
    digest = sha256()
    for groups in combinations_with_replacement(types, 5):
        probabilities = (Fraction(1, 2),) * 5
        error = best_error(groups, probabilities)
        need(error <= 2, "2s discrepancy bound failed for equal weights")
        maximum = max(maximum, error)
        digest.update(f"{groups}:{error};".encode())
        half_cases += 1

    ordered_types = tuple(product(masks, repeat=2))
    unequal_cases = 0
    probabilities = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3))
    for groups in product(ordered_types, repeat=3):
        error = best_error(groups, probabilities)
        need(error <= 2, "2s discrepancy bound failed for unequal weights")
        maximum = max(maximum, error)
        digest.update(f"{groups}:{error};".encode())
        unequal_cases += 1
    return {
        "equal_weight_multiset_cases": half_cases,
        "unequal_weight_ordered_cases": unequal_cases,
        "maximum_optimal_error": str(maximum),
        "case_sha256": digest.hexdigest(),
    }


def check_orientations() -> dict:
    """Count every class-respecting labeled K2/K3 orientation for three classes."""
    cases = 0
    role_vertex_checks = 0
    digest = sha256()
    for size in (2, 3):
        for kind in combinations_with_replacement(range(3), size):
            expected_maps = 1
            for cls in set(kind):
                count = kind.count(cls)
                for factor in range(2, count + 1):
                    expected_maps *= factor
            for role_classes in sorted(set(permutations(kind))):
                maps = [mapping for mapping in permutations(range(size))
                        if tuple(kind[v] for v in mapping) == role_classes]
                need(len(maps) == expected_maps, "class-respecting bijection count failed")
                for role, cls in enumerate(role_classes):
                    vertices = [v for v, vertex_cls in enumerate(kind) if vertex_cls == cls]
                    counts = [sum(mapping[role] == v for mapping in maps) for v in vertices]
                    need(len(set(counts)) == 1 and counts[0] * len(vertices) == len(maps),
                         "role probability is not uniform within its class")
                    role_vertex_checks += len(vertices)
                digest.update(f"{kind}:{role_classes}:{maps};".encode())
                cases += 1
    return {"typed_orientation_cases": cases, "role_vertex_checks": role_vertex_checks,
            "case_sha256": digest.hexdigest()}


def greedy_failures(forbidden: tuple[int, ...], candidate_count: int) -> int:
    available = (1 << candidate_count) - 1
    failed = 0
    for mask in forbidden:
        compatible = available & ~mask
        if not compatible:
            failed += 1
            continue
        selected = compatible & -compatible
        available ^= selected
    return failed


def check_greedy_collision_bound() -> dict:
    """Exhaust every small ordered incompatibility matrix behind (9)."""
    cases = 0
    maximum_slack = 0
    digest = sha256()
    for candidates in range(5):
        all_masks = tuple(range(1 << candidates))
        for q in range(3):
            allowed = tuple(mask for mask in all_masks if mask.bit_count() <= q)
            for requests in range(6):
                bound = max(0, requests-candidates) + q
                for forbidden in product(allowed, repeat=requests):
                    failed = greedy_failures(forbidden, candidates)
                    need(failed <= bound, "rooted greedy collision bound failed")
                    maximum_slack = max(maximum_slack, bound-failed)
                    digest.update(f"{candidates}:{q}:{forbidden}:{failed};".encode())
                    cases += 1
    return {"ordered_incompatibility_matrices": cases,
            "maximum_bound_slack": maximum_slack,
            "case_sha256": digest.hexdigest()}


def check_role_surplus_bound() -> dict:
    """Enumerate scalar endpoint data used in sum max(0,a_v-b_v)."""
    cases = 0
    tight = 0
    for class_size in range(1, 7):
        for target in range(11):
            for deficit in range(target + 1):
                for discrepancy in range(4):
                    upper = Fraction(target, class_size) + discrepancy
                    lower = Fraction(target-deficit, class_size) - discrepancy
                    local_bound = Fraction(deficit, class_size) + 2*discrepancy
                    for demand in range(13):
                        if demand > upper:
                            continue
                        for supply in range(13):
                            if supply < lower:
                                continue
                            surplus = max(0, demand-supply)
                            need(surplus <= local_bound, "local role-surplus bound failed")
                            tight += surplus == local_bound
                            cases += 1
    return {"admissible_scalar_cases": cases, "tight_cases": tight}


def check_coefficients() -> dict:
    cases = 0
    for r in range(2, 7):
        a = 2*(r+1)
        for discrepancy in range(11):
            lifted = discrepancy + 4*a
            for q in range(2, 11):
                need(2*a + 2*lifted + q == 2*discrepancy + 20*(r+1) + q,
                     "transfer coefficient identity failed")
                for blocks in range(1, 9):
                    for components in range(1, blocks + 1):
                        exact = ((blocks-components)*(2*lifted+q)
                                 + (components-1)*q)
                        relaxed = (blocks-1)*(2*lifted+q)
                        need(exact <= relaxed, "component coefficient relaxation failed")
                        cases += 1
    return {"coefficient_cases": cases, "triangle_additive_term": 80}


def main() -> None:
    result = {
        "status": "REVIEW CHECK PASSED",
        "target_files_bound": len(TARGET_HASHES),
        "target_binding_sha256": bind_target(),
        "partition_rounding": check_partition_rounding(),
        "labeled_orientations": check_orientations(),
        "greedy_collision": check_greedy_collision_bound(),
        "role_surplus": check_role_surplus_bound(),
        "coefficient_accounting": check_coefficients(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
