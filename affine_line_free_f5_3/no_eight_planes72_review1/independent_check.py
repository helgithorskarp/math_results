#!/usr/bin/env python3
"""Independent exact check of the no-eight-plane theorem at cardinality 72.

This checker imports none of the reviewed Python or C++ implementation.  It
enumerates quotient deficits as multisets of unit tokens, applies every affine
map of the quotient plane to every published representative, and uses a SAT
encoding with only the 125 primary point variables.  In particular it omits
the submitted plane-cardinality constraints and every sequential-counter
auxiliary variable.  It also directly excludes the 144 multi-eight quotients
rather than importing their earlier SAT exclusions.  Each fresh UNSAT proof
is checked by a separately built DRAT-trim executable.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import subprocess
import sys
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "no_eight_planes72"
PLANE_POINTS = tuple(product(range(5), repeat=2))
SPACE_POINTS = tuple(product(range(5), repeat=3))
NORMALS_2D = (*tuple((1, slope) for slope in range(5)), (0, 1))
ROW_PROFILE = (8, 16, 16, 16, 16)
COLUMN_PROFILE = (9, 15, 16, 16, 16)
CATALOGUE_SHA256 = "765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profiles(word: bytes) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(
                word[5 * x + y]
                for x, y in PLANE_POINTS
                if (normal[0] * x + normal[1] * y) % 5 == offset
            )
            for offset in range(5)
        )
        for normal in NORMALS_2D
    )


def validate_word(word: bytes) -> tuple[tuple[int, ...], ...]:
    require(len(word) == 25 and all(value <= 4 for value in word), "invalid quotient")
    require(sum(word) == 72, "incorrect quotient total")
    line_profiles = profiles(word)
    require(max(max(profile) for profile in line_profiles) <= 16, "quotient line exceeds 16")
    require(line_profiles[0] == ROW_PROFILE, "row profile is not A")
    require(line_profiles[-1] == COLUMN_PROFILE, "column profile is not B")
    require(word[0] <= 1, "low-plane intersection exceeds one point")
    require(max(word[:5]) <= 3, "zero row fiber exceeds three points")
    require(max(word[::5]) <= 3, "zero column fiber exceeds three points")
    return line_profiles


def enumerate_catalogue() -> set[bytes]:
    """Enumerate the 4x4 deficit block as eight or nine unit tokens."""
    answers: set[bytes] = set()
    column_margins = (5, 4, 4, 4)
    for total in (8, 9):
        for units in combinations_with_replacement(range(16), total):
            rows = [0] * 4
            columns = [0] * 4
            block = [0] * 16
            valid = True
            for cell in units:
                row, column = divmod(cell, 4)
                rows[row] += 1
                columns[column] += 1
                block[cell] += 1
                if block[cell] > 4 or rows[row] > 3 or columns[column] > column_margins[column] - 1:
                    valid = False
                    break
            if not valid:
                continue
            deficit = [0] * 25
            for row in range(4):
                for column in range(4):
                    deficit[5 * (row + 1) + column + 1] = block[4 * row + column]
                deficit[5 * (row + 1)] = 4 - rows[row]
            for column in range(4):
                deficit[column + 1] = column_margins[column] - columns[column]
            deficit[0] = total - 5
            if not all(0 <= value <= 4 for value in deficit):
                continue
            word = bytes(4 - value for value in deficit)
            try:
                validate_word(word)
            except RuntimeError:
                continue
            answers.add(word)
    return answers


def catalogue_bytes(catalogue: set[bytes]) -> bytes:
    return b"".join(bytes(value + 48 for value in word) + b"\n" for word in sorted(catalogue))


def eight_count(word: bytes) -> int:
    return sum(profile.count(8) for profile in validate_word(word))


def affine_inverse_permutations() -> tuple[tuple[int, ...], ...]:
    permutations = []
    for a, b, c, d in product(range(5), repeat=4):
        if (a * d - b * c) % 5 == 0:
            continue
        for translate_x, translate_y in PLANE_POINTS:
            inverse = [-1] * 25
            for old_index, (x, y) in enumerate(PLANE_POINTS):
                new_x = (a * x + b * y + translate_x) % 5
                new_y = (c * x + d * y + translate_y) % 5
                inverse[5 * new_x + new_y] = old_index
            require(min(inverse) >= 0 and len(set(inverse)) == 25, "nonpermutation affine map")
            permutations.append(tuple(inverse))
    require(len(permutations) == 12_000, "incorrect affine group order")
    require(len(set(permutations)) == 12_000, "duplicate affine permutation")
    return tuple(permutations)


def check_full_affine_partition(
    remaining: set[bytes], representatives: list[dict]
) -> dict[int, int]:
    permutations = affine_inverse_permutations()
    covered: set[bytes] = set()
    histogram: dict[int, int] = {}
    for index, record in enumerate(representatives):
        word = bytes(map(int, record["weights"]))
        require(word in remaining, f"representative {index} is absent")
        normalized_images = {
            image
            for inverse in permutations
            if (image := bytes(word[position] for position in inverse)) in remaining
        }
        require(
            len(normalized_images) == record["orbit_size"],
            f"full affine orbit-size mismatch at {index}",
        )
        require(min(normalized_images) == word, f"representative {index} is not canonical")
        require(not covered.intersection(normalized_images), f"orbit overlap at {index}")
        covered.update(normalized_images)
        size = len(normalized_images)
        histogram[size] = histogram.get(size, 0) + 1
    require(covered == remaining, "full affine orbits do not partition the catalogue")
    return histogram


def normalized_directions(dimension: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vector
        for vector in product(range(5), repeat=dimension)
        if any(vector) and next(entry for entry in vector if entry) == 1
    )


def affine_lines() -> tuple[tuple[int, ...], ...]:
    index = {point: position + 1 for position, point in enumerate(SPACE_POINTS)}
    directions = normalized_directions(3)
    require(len(directions) == 31, "incorrect projective direction count")
    lines = {
        tuple(
            sorted(
                index[
                    tuple(
                        (coordinate + scalar * direction_coordinate) % 5
                        for coordinate, direction_coordinate in zip(point, direction, strict=True)
                    )
                ]
                for scalar in range(5)
            )
        )
        for point in SPACE_POINTS
        for direction in directions
    }
    pair_lines = set()
    for first, second in combinations(SPACE_POINTS, 2):
        difference = tuple((right - left) % 5 for left, right in zip(first, second, strict=True))
        pair_lines.add(
            tuple(
                sorted(
                    index[
                        tuple(
                            (coordinate + scalar * step) % 5
                            for coordinate, step in zip(first, difference, strict=True)
                        )
                    ]
                    for scalar in range(5)
                )
            )
        )
    require(len(lines) == 775 and lines == pair_lines, "affine-line generation mismatch")
    return tuple(sorted(lines))


def last_gauge(word: bytes) -> tuple[int, int, int]:
    full = [index for index, value in enumerate(word) if value == 4]
    gauges = []
    for triple in combinations(full, 3):
        points = [divmod(index, 5) for index in triple]
        determinant = (
            (points[1][0] - points[0][0]) * (points[2][1] - points[0][1])
            - (points[2][0] - points[0][0]) * (points[1][1] - points[0][1])
        ) % 5
        if determinant:
            gauges.append(triple)
    require(bool(gauges), "no noncollinear triple of four-point fibers")
    return gauges[-1]


def check_gauge_interpolation(gauges: set[tuple[int, int, int]]) -> None:
    affine_functions = tuple(product(range(5), repeat=3))
    for gauge in gauges:
        points = tuple(divmod(index, 5) for index in gauge)
        for heights in product(range(5), repeat=3):
            solutions = 0
            for a, b, c in affine_functions:
                values = tuple((a * x + b * y + c) % 5 for x, y in points)
                solutions += values == heights
            require(solutions == 1, f"nonunique affine interpolation at gauge {gauge}")


def fiber_clauses(literals: tuple[int, ...], cardinality: int) -> list[list[int]]:
    clauses = [
        [-literal for literal in subset] for subset in combinations(literals, cardinality + 1)
    ]
    clauses.extend(
        list(subset) for subset in combinations(literals, len(literals) - cardinality + 1)
    )
    return clauses


def check_fiber_encoding() -> None:
    literals = tuple(range(1, 6))
    for cardinality in range(6):
        clauses = fiber_clauses(literals, cardinality)
        for mask in range(1 << 5):
            selected = {index + 1 for index in range(5) if mask & (1 << index)}
            satisfies = all(
                any((literal > 0) == (abs(literal) in selected) for literal in clause)
                for clause in clauses
            )
            require(satisfies == (len(selected) == cardinality), "fiber encoding is not exact")


def direct_clauses(
    word: bytes, lines: tuple[tuple[int, ...], ...]
) -> tuple[list[list[int]], tuple[int, int, int]]:
    clauses = [[-literal for literal in line] for line in lines]
    for fiber, cardinality in enumerate(word):
        literals = tuple(range(5 * fiber + 1, 5 * fiber + 6))
        clauses.extend(fiber_clauses(literals, cardinality))
    gauge = last_gauge(word)
    clauses.extend([[-(5 * fiber + 1)] for fiber in gauge])
    return clauses, gauge


def write_cnf(path: Path, clauses: list[list[int]]) -> None:
    text = [f"p cnf 125 {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    path.write_text("".join(text), encoding="ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--keep-proofs", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    require(checker.is_file(), "DRAT-trim executable is missing")

    catalogue = enumerate_catalogue()
    catalogue_hash = hashlib.sha256(catalogue_bytes(catalogue)).hexdigest()
    require(len(catalogue) == 5_428, "unexpected mixed quotient count")
    require(catalogue_hash == CATALOGUE_SHA256, "catalogue hash mismatch")
    discarded = {word for word in catalogue if eight_count(word) >= 2}
    remaining = catalogue - discarded
    require(len(discarded) == 144 and len(remaining) == 5_284, "incorrect catalogue split")
    require(all(eight_count(word) == 1 for word in remaining), "remaining quotient split failed")

    representatives = json.loads((TARGET / "orbits.json").read_text())
    require(len(representatives) == 1_252, "unexpected representative count")
    orbit_histogram = check_full_affine_partition(remaining, representatives)

    check_fiber_encoding()
    lines = affine_lines()
    families = [
        *(("multi_eight_labeled", word) for word in sorted(discarded)),
        *(("single_eight_orbit", bytes(map(int, record["weights"]))) for record in representatives),
    ]
    gauges = {last_gauge(word) for _, word in families}
    check_gauge_interpolation(gauges)

    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    records = []
    total_proof_bytes = 0
    for case, (family, word) in enumerate(families):
        clauses, gauge = direct_clauses(word, lines)
        cnf = out / f"case_{case:04d}.cnf"
        proof = out / f"case_{case:04d}.drat"
        write_cnf(cnf, clauses)
        with Solver(name="cadical195", bootstrap_with=clauses, with_proof=True) as solver:
            answer = solver.solve()
            require(answer is False, f"direct encoding case {case} is not UNSAT")
            require(libc.fflush(None) == 0, "native proof stream flush failed")
            solver.solver.prfile.seek(0)
            proof.write_bytes(solver.solver.prfile.read())
            conflicts = solver.accum_stats()["conflicts"]
        checked = subprocess.run(
            [str(checker), str(cnf), str(proof)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            checked.returncode == 0 and b"s VERIFIED" in checked.stdout,
            f"DRAT check failed in case {case}",
        )
        proof_bytes = proof.stat().st_size
        total_proof_bytes += proof_bytes
        records.append(
            {
                "case": case,
                "family": family,
                "clauses": len(clauses),
                "cnf_sha256": digest(cnf),
                "conflicts": conflicts,
                "gauge": list(gauge),
                "proof_bytes": proof_bytes,
                "proof_sha256": digest(proof),
            }
        )
        if not args.keep_proofs:
            cnf.unlink()
            proof.unlink()
        if (case + 1) % 100 == 0 or case + 1 == len(families):
            print(f"verified {case + 1}/{len(families)}", file=sys.stderr, flush=True)

    record_bytes = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "INDEPENDENT_NO_EIGHT_PLANE_CHECK_PASSED",
        "affine_group_order": 12_000,
        "catalogue_sha256": catalogue_hash,
        "direct_clause_range": [
            min(record["clauses"] for record in records),
            max(record["clauses"] for record in records),
        ],
        "direct_encoding": (
            "125 primary variables; line clauses; subset fiber clauses; "
            "no plane-cap clauses or auxiliary variables"
        ),
        "direct_multi_eight_exclusions": len(discarded),
        "drat_checker_sha256": digest(checker),
        "full_affine_orbit_histogram": {
            str(key): orbit_histogram[key] for key in sorted(orbit_histogram)
        },
        "gauge_interpolation_triples": len(gauges),
        "labeled_mixed_quotients": len(catalogue),
        "lines": len(lines),
        "max_conflicts": max(record["conflicts"] for record in records),
        "proof_bytes": total_proof_bytes,
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "single_eight_affine_classes": len(representatives),
        "sum_conflicts": sum(record["conflicts"] for record in records),
        "verified_unsat_proofs": len(records),
    }
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
