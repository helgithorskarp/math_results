#!/usr/bin/env python3
"""Independent exact check of the two-eight-plane exclusion.

This checker does not import the reviewed Python or C++ implementation.  It
uses a multiset enumeration of deficit units, the full 12,000-element affine
group rather than the submitted low-line normalization, and a primary-variable
SAT encoding with no sequential counters or plane-cap clauses.  Each UNSAT
answer is checked by a separately built DRAT-trim executable.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import subprocess
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "two_eight_planes72"
PLANE_POINTS = tuple(product(range(5), repeat=2))
SPACE_POINTS = tuple(product(range(5), repeat=3))
NORMALS_2D = (*tuple((1, slope) for slope in range(5)), (0, 1))
CATALOGUE_SHA256 = "ea95e0794a925fd8b3842b3ad4e90b9ab69828340a1ea065bc61fe8b9e8286cf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_directions(dimension: int) -> tuple[tuple[int, ...], ...]:
    vectors = []
    for vector in product(range(5), repeat=dimension):
        if any(vector) and next(entry for entry in vector if entry) == 1:
            vectors.append(vector)
    return tuple(vectors)


def validate_word(word: bytes) -> None:
    require(len(word) == 25 and all(value <= 4 for value in word), "invalid quotient word")
    require(sum(word) == 72, "incorrect quotient total")
    profiles = []
    for normal in NORMALS_2D:
        profile = tuple(
            sum(
                word[5 * x + y]
                for x, y in PLANE_POINTS
                if (normal[0] * x + normal[1] * y) % 5 == offset
            )
            for offset in range(5)
        )
        profiles.append(profile)
    require(max(max(profile) for profile in profiles) <= 16, "quotient line exceeds 16")
    require(profiles[0] == (8, 16, 16, 16, 16), "row profile is not A")
    require(profiles[-1] == (8, 16, 16, 16, 16), "column profile is not A")
    require(word[0] <= 1, "axis intersection exceeds one point")
    require(max(word[:5]) <= 3, "zero row fiber exceeds three points")
    require(max(word[::5]) <= 3, "zero column fiber exceeds three points")


def enumerate_catalogue() -> set[bytes]:
    """Enumerate 4x4 deficits as multisets of seven or eight unit tokens."""
    answers: set[bytes] = set()
    for total in (7, 8):
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
                if rows[row] > 3 or columns[column] > 3:
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
                deficit[column + 1] = 4 - columns[column]
            deficit[0] = total - 4
            word = bytes(4 - value for value in deficit)
            try:
                validate_word(word)
            except RuntimeError:
                continue
            answers.add(word)
    return answers


def catalogue_bytes(catalogue: set[bytes]) -> bytes:
    return b"".join(bytes(value + 48 for value in word) + b"\n" for word in sorted(catalogue))


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
    return tuple(permutations)


def check_full_affine_partition(
    catalogue: set[bytes], representatives: list[dict]
) -> dict[int, int]:
    permutations = affine_inverse_permutations()
    covered: set[bytes] = set()
    histogram: dict[int, int] = {}
    for index, record in enumerate(representatives):
        word = bytes(map(int, record["weights"]))
        require(word in catalogue, f"representative {index} is absent")
        normalized_images = set()
        for inverse in permutations:
            if sum(word[inverse[position]] for position in range(5)) != 8:
                continue
            if sum(word[inverse[5 * position]] for position in range(5)) != 8:
                continue
            image = bytes(word[position] for position in inverse)
            require(image in catalogue, f"affine image of representative {index} is absent")
            normalized_images.add(image)
        expected_size = record["orbit_size"]
        require(len(normalized_images) == expected_size, f"orbit-size mismatch at {index}")
        require(not covered.intersection(normalized_images), f"orbit overlap at {index}")
        covered.update(normalized_images)
        histogram[expected_size] = histogram.get(expected_size, 0) + 1
    require(covered == catalogue, "full affine orbits do not partition the catalogue")
    return histogram


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


def gauge_for(word: str) -> tuple[int, int, int]:
    full = [index for index, value in enumerate(word) if value == "4"]
    for triple in combinations(full, 3):
        points = [divmod(index, 5) for index in triple]
        determinant = (
            (points[1][0] - points[0][0]) * (points[2][1] - points[0][1])
            - (points[2][0] - points[0][0]) * (points[1][1] - points[0][1])
        ) % 5
        if determinant:
            return triple
    raise RuntimeError("no noncollinear triple of four-point fibers")


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
    word: str, lines: tuple[tuple[int, ...], ...]
) -> tuple[list[list[int]], tuple[int, int, int]]:
    clauses = [[-literal for literal in line] for line in lines]
    for fiber, value in enumerate(word):
        literals = tuple(range(5 * fiber + 1, 5 * fiber + 6))
        clauses.extend(fiber_clauses(literals, int(value)))
    gauge = gauge_for(word)
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
    serialized_catalogue = catalogue_bytes(catalogue)
    catalogue_hash = hashlib.sha256(serialized_catalogue).hexdigest()
    require(len(catalogue) == 4_442, "unexpected quotient count")
    require(catalogue_hash == CATALOGUE_SHA256, "catalogue hash mismatch")

    representatives = json.loads((TARGET / "orbits.json").read_text())
    require(len(representatives) == 164, "unexpected representative count")
    orbit_histogram = check_full_affine_partition(catalogue, representatives)

    check_fiber_encoding()
    lines = affine_lines()
    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    records = []
    total_proof_bytes = 0
    for case, representative in enumerate(representatives):
        clauses, gauge = direct_clauses(representative["weights"], lines)
        cnf = out / f"case_{case:03d}.cnf"
        proof = out / f"case_{case:03d}.drat"
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

    record_bytes = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "INDEPENDENT_TWO_EIGHT_PLANE_CHECK_PASSED",
        "affine_group_order": 12_000,
        "catalogue_sha256": catalogue_hash,
        "direct_clause_range": [
            min(record["clauses"] for record in records),
            max(record["clauses"] for record in records),
        ],
        "direct_encoding": (
            "primary variables; line clauses; subset fiber clauses; no plane-cap clauses"
        ),
        "drat_checker_sha256": digest(checker),
        "full_affine_orbit_histogram": {
            str(key): orbit_histogram[key] for key in sorted(orbit_histogram)
        },
        "labeled_quotients": len(catalogue),
        "lines": len(lines),
        "max_conflicts": max(record["conflicts"] for record in records),
        "proof_bytes": total_proof_bytes,
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "representatives": len(representatives),
        "sum_conflicts": sum(record["conflicts"] for record in records),
        "verified_unsat_proofs": len(records),
    }
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
