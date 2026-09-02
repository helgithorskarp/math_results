#!/usr/bin/env python3
"""Generate the 35 CNFs for the sharp point-degree bound in C(12,5,2).

All generated instances and solver proofs belong in a caller-supplied scratch
directory.  The repository contains only this deterministic generator and the
compact expected manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


POINTS = tuple(range(11))
A_BLOCKS = tuple(itertools.combinations(POINTS, 4))
ROW_PERMUTATIONS = tuple(itertools.permutations(range(3)))
MASK_MAPS = {
    permutation: tuple(
        sum(((mask >> row) & 1) << permutation[row] for row in range(3))
        for mask in range(8)
    )
    for permutation in ROW_PERMUTATIONS
}


def weak_compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    """Yield all ordered weak compositions of total into the given parts."""
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from weak_compositions(total - first, parts - 1, prefix + (first,))


def rows_are_distinct(counts: tuple[int, ...]) -> bool:
    for first, second in itertools.combinations(range(3), 2):
        if all(
            counts[mask] == 0
            or ((mask >> first) & 1) == ((mask >> second) & 1)
            for mask in range(8)
        ):
            return False
    return True


def canonical_signature(counts: tuple[int, ...]) -> tuple[int, ...]:
    images = []
    for permutation in ROW_PERMUTATIONS:
        image = [0] * 8
        for mask, count in enumerate(counts):
            image[MASK_MAPS[permutation][mask]] = count
        images.append(tuple(image))
    return min(images)


def degree_six_representatives() -> list[dict[str, object]]:
    """Return the 35 S_11 x S_3 orbits of three distinct 5-subsets."""
    signatures = set()
    for counts in weak_compositions(11, 8):
        row_sizes = tuple(
            sum(counts[mask] for mask in range(8) if (mask >> row) & 1)
            for row in range(3)
        )
        if row_sizes != (5, 5, 5) or not rows_are_distinct(counts):
            continue
        signatures.add(canonical_signature(counts))

    representatives = []
    for signature in sorted(signatures):
        cells: list[tuple[int, ...]] = []
        next_point = 0
        for count in signature:
            cells.append(tuple(range(next_point, next_point + count)))
            next_point += count
        assert next_point == 11
        blocks = tuple(
            tuple(
                point
                for mask in range(8)
                if (mask >> row) & 1
                for point in cells[mask]
            )
            for row in range(3)
        )
        assert len(set(blocks)) == 3 and all(len(block) == 5 for block in blocks)
        representatives.append({"signature": signature, "B_blocks": blocks})
    assert len(representatives) == 35
    return representatives


def degree_seven_representatives() -> list[dict[str, object]]:
    """Return the five orbits of two distinct 5-subsets, by intersection size."""
    first = tuple(range(5))
    representatives = []
    for intersection in range(5):
        second = tuple(range(intersection)) + tuple(range(5, 10 - intersection))
        assert len(second) == 5
        assert len(set(first) & set(second)) == intersection
        representatives.append({"intersection": intersection, "B_blocks": (first, second)})
    return representatives


def at_most(variables: list[int], bound: int, next_variable: int):
    """Sinz sequential-counter CNF for sum(variables) <= bound.

    Returns (clauses, largest_variable).  Auxiliary s[i,j] means that at least
    j+1 of variables[0:i+1] are true.  Only equisatisfiability is required.
    """
    assert 0 < bound < len(variables)
    n = len(variables)
    s: dict[tuple[int, int], int] = {}
    for i in range(n - 1):
        for j in range(bound):
            next_variable += 1
            s[i, j] = next_variable

    clauses: list[list[int]] = []
    clauses.append([-variables[0], s[0, 0]])
    clauses.extend([[-s[0, j]] for j in range(1, bound)])
    for i in range(1, n - 1):
        clauses.append([-variables[i], s[i, 0]])
        clauses.append([-s[i - 1, 0], s[i, 0]])
        for j in range(1, bound):
            clauses.append([-variables[i], -s[i - 1, j - 1], s[i, j]])
            clauses.append([-s[i - 1, j], s[i, j]])
        clauses.append([-variables[i], -s[i - 1, bound - 1]])
    clauses.append([-variables[-1], -s[n - 2, bound - 1]])
    return clauses, next_variable


def build_cnf(degree: int, b_blocks: tuple[tuple[int, ...], ...]):
    """Encode extension by at most degree many 4-subsets containing x."""
    assert len(b_blocks) == 9 - degree
    assert len(set(b_blocks)) == len(b_blocks)
    assert all(len(block) == 5 and set(block) <= set(POINTS) for block in b_blocks)
    b_sets = tuple(map(set, b_blocks))
    a_sets = tuple(map(set, A_BLOCKS))
    clauses: list[list[int]] = []

    # Cover each pair {x,p}; only an A-block contains x.
    for point in POINTS:
        clauses.append([index + 1 for index, block in enumerate(A_BLOCKS) if point in block])

    # Pairs among the other eleven points already covered by a B-block need no clause.
    for pair in itertools.combinations(POINTS, 2):
        pair_set = set(pair)
        if not any(pair_set <= block for block in b_sets):
            clauses.append(
                [index + 1 for index, block in enumerate(a_sets) if pair_set <= block]
            )

    cardinality_clauses, largest_variable = at_most(
        list(range(1, len(A_BLOCKS) + 1)), degree, len(A_BLOCKS)
    )
    clauses.extend(cardinality_clauses)
    return largest_variable, clauses


def cnf_bytes(variables: int, clauses: list[list[int]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    instances = []
    orbit_payload: dict[str, object] = {"degree_6": []}
    families = ((6, degree_six_representatives()),)
    for degree, representatives in families:
        for orbit, representative in enumerate(representatives):
            b_blocks = tuple(tuple(block) for block in representative["B_blocks"])
            variables, clauses = build_cnf(degree, b_blocks)
            data = cnf_bytes(variables, clauses)
            filename = f"degree_{degree}_orbit_{orbit:02d}.cnf"
            (output / filename).write_bytes(data)
            instances.append(
                {
                    "file": filename,
                    "degree": degree,
                    "orbit": orbit,
                    "variables": variables,
                    "clauses": len(clauses),
                    "sha256": sha256(data),
                }
            )
            orbit_payload[f"degree_{degree}"].append(representative)

    orbits_data = (json.dumps(orbit_payload, indent=2, sort_keys=True) + "\n").encode()
    (output / "orbit_representatives.json").write_bytes(orbits_data)
    manifest = {
        "format": "C(12,5,2) distinguished-point extension CNFs v1",
        "mathematical_variables_per_instance": len(A_BLOCKS),
        "degree_7_orbits_handled_symbolically": 5,
        "degree_6_labeled_signatures": 110,
        "degree_6_burnside_fixed_counts": [110, 28, 8],
        "degree_6_orbits": 35,
        "orbit_representatives_sha256": sha256(orbits_data),
        "instances": instances,
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (output / "manifest.json").write_bytes(manifest_data)
    print(json.dumps({"instances": len(instances), "manifest_sha256": sha256(manifest_data)},
                     sort_keys=True))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="scratch output directory")
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
