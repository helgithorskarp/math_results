#!/usr/bin/env python3
"""Independent exact audit of the complete 72-point exclusion.

This checker imports none of the reviewed implementation.  It enumerates all
three typed quotient catalogues as multisets of deficit units; invokes a C++
audit using every element of AGL(2,5); independently rebuilds the low-plane
dual inequality; and proves all 4,332 lifting instances with complemented
(hole) variables, a different gauge choice, and fresh DRAT certificates.
"""

from __future__ import annotations

import argparse
import ctypes
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import subprocess
import sys

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "upper_bound71"
LOW = ROOT / "low_planes72"
PLANE_POINTS = tuple(product(range(5), repeat=2))
SPACE_POINTS = tuple(product(range(5), repeat=3))
NORMALS_2D = (*tuple((1, slope) for slope in range(5)), (0, 1))
PROFILE_A = (8, 16, 16, 16, 16)
PROFILE_B = (9, 15, 16, 16, 16)
DEFICIT_A = (12, 4, 4, 4, 4)
DEFICIT_B = (11, 5, 4, 4, 4)
PROFILES = ((PROFILE_A, PROFILE_A), (PROFILE_A, PROFILE_B), (PROFILE_B, PROFILE_B))
CATALOGUE_SHA256 = "7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f"


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
                if (normal[0] * x + normal[1] * y) % 5 == label
            )
            for label in range(5)
        )
        for normal in NORMALS_2D
    )


def validate_word(kind: int, word: bytes) -> None:
    require(kind in range(3), "invalid quotient type")
    require(len(word) == 25 and all(value <= 4 for value in word), "invalid quotient word")
    require(sum(word) == 72, "incorrect quotient total")
    line_profiles = profiles(word)
    require(all(8 <= value <= 16 for profile in line_profiles for value in profile),
            "quotient line violates plane bounds")
    require((line_profiles[0], line_profiles[-1]) == PROFILES[kind],
            "distinguished profiles disagree with quotient type")
    require(word[0] <= (2 if kind == 2 else 1), "intersection pencil bound fails")
    require(max(word[:5]) <= 3 and max(word[::5]) <= 3, "axis pencil bound fails")


def enumerate_type(kind: int) -> set[bytes]:
    """Enumerate the interior deficit block as a multiset of unit tokens."""
    row_margin = DEFICIT_A if kind < 2 else DEFICIT_B
    column_margin = DEFICIT_A if kind == 0 else DEFICIT_B
    totals = ((7, 8), (8, 9), (8, 9, 10))[kind]
    answers: set[bytes] = set()
    for total in totals:
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
                if (block[cell] > 4
                        or rows[row] > row_margin[row + 1] - 1
                        or columns[column] > column_margin[column + 1] - 1):
                    valid = False
                    break
            if not valid:
                continue
            deficit = [0] * 25
            for row in range(4):
                for column in range(4):
                    deficit[5 * (row + 1) + column + 1] = block[4 * row + column]
                deficit[5 * (row + 1)] = row_margin[row + 1] - rows[row]
            for column in range(4):
                deficit[column + 1] = column_margin[column + 1] - columns[column]
            deficit[0] = row_margin[0] + column_margin[0] - 28 + total
            if not all(0 <= value <= 4 for value in deficit):
                continue
            word = bytes(4 - value for value in deficit)
            try:
                validate_word(kind, word)
            except RuntimeError:
                continue
            answers.add(word)
    return answers


def serialize_catalogue(catalogue: set[tuple[int, bytes]]) -> bytes:
    return b"".join(
        str(kind).encode("ascii") + b" " + bytes(value + 48 for value in word) + b"\n"
        for kind, word in sorted(catalogue)
    )


def independent_low_plane_certificate() -> dict[str, object]:
    """Rebuild the 61-by-463 incidence dual needed for a_8+a_9 >= 5."""
    spectra = [tuple(map(int, line.split()))
               for line in (LOW / "spectra_expected.txt").read_text().splitlines()]
    require(len(spectra) == 70, "incorrect planar spectrum catalogue")
    for spectrum in spectra:
        size, *tail = spectrum
        counts, multiplicity = tail[:5], tail[5]
        require(sum(counts) == 30 and multiplicity > 0, "invalid planar spectrum")
        require(sum(k * counts[k] for k in range(5)) == 6 * size,
                "planar point-line incidence mismatch")
        require(sum(k * (k - 1) // 2 * counts[k] for k in range(5))
                == size * (size - 1) // 2, "planar pair-line incidence mismatch")

    parallel = [entry for entry in combinations_with_replacement(range(8, 17), 5)
                if sum(entry) == 72]
    pencils = [(k, entry) for k in range(5)
               for entry in combinations_with_replacement(range(max(8, 5 * k - 8), 17), 6)
               if sum(entry) == 72 + 5 * k]
    columns: list[tuple[str, tuple[int, ...] | tuple[int, tuple[int, ...]]]] = []
    columns.extend(("s", spectrum) for spectrum in spectra)
    columns.extend(("p", entry) for entry in parallel)
    columns.extend(("l", entry) for entry in pencils)
    rows: list[list[int]] = []
    rhs: list[int] = []

    def add_row(coefficient, value: int) -> None:
        rows.append([coefficient(tag, entry) for tag, entry in columns])
        rhs.append(value)

    add_row(lambda tag, entry: int(tag == "s"), 155)
    add_row(lambda tag, entry: entry[0] if tag == "s" else 0, 2232)
    add_row(lambda tag, entry: entry[0] * (entry[0] - 1) // 2 if tag == "s" else 0, 15336)
    add_row(lambda tag, entry: int(tag == "p"), 31)
    for size in range(8, 17):
        add_row(lambda tag, entry, size=size:
                int(entry[0] == size) if tag == "s"
                else (-entry.count(size) if tag == "p" else 0), 0)
    for line_size in range(5):
        for plane_size in range(8, 17):
            add_row(lambda tag, entry, k=line_size, m=plane_size:
                    (entry[1 + k] if tag == "s" and entry[0] == m else
                     (-entry[1].count(m) if tag == "l" and entry[0] == k else 0)), 0)
    add_row(lambda tag, entry: int(tag == "l"), 775)
    add_row(lambda tag, entry: entry[0] if tag == "l" else 0, 2232)
    add_row(lambda tag, entry: entry[0] * (entry[0] - 1) // 2 if tag == "l" else 0, 2556)
    require(len(columns) == 463 and len(rows) == 61, "incorrect incidence-system dimensions")

    certificate = json.loads((LOW / "incidence_certificates.json").read_text())[0]
    require(certificate["cutoff"] == 9, "first dual certificate is not the required cutoff")
    denominator = certificate["denominator"]
    multipliers = certificate["multipliers"]
    require(denominator > 0 and len(multipliers) == 61
            and all(type(value) is int for value in multipliers), "invalid dual multipliers")
    objective = [int(tag == "s" and entry[0] <= 9) for tag, entry in columns]
    slacks = [
        denominator * objective[column]
        - sum(multipliers[row] * rows[row][column] for row in range(61))
        for column in range(463)
    ]
    numerator = sum(multiplier * value for multiplier, value in zip(multipliers, rhs, strict=True))
    require(min(slacks) >= 0 and min(slacks) == certificate["minimum_slack"],
            "dual inequality fails")
    require(numerator == certificate["bound_numerator"], "dual objective mismatch")
    bound = Fraction(numerator, denominator)
    require(bound > 4, "dual certificate does not force five low planes")
    return {
        "columns": len(columns),
        "equations": len(rows),
        "integer_lower_bound": (numerator + denominator - 1) // denominator,
        "minimum_slack": min(slacks),
        "rational_lower_bound": str(bound),
    }


def normalized_directions(dimension: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vector for vector in product(range(5), repeat=dimension)
        if any(vector) and next(value for value in vector if value) == 1
    )


def affine_lines() -> tuple[tuple[int, ...], ...]:
    index = {point: position + 1 for position, point in enumerate(SPACE_POINTS)}
    directional = {
        tuple(sorted(index[tuple((coordinate + scalar * step) % 5
                                 for coordinate, step in zip(point, direction, strict=True))]
                     for scalar in range(5)))
        for point in SPACE_POINTS for direction in normalized_directions(3)
    }
    pair_generated = {
        tuple(sorted(index[tuple((coordinate + scalar * ((other - coordinate) % 5)) % 5
                                 for coordinate, other in zip(first, second, strict=True))]
                     for scalar in range(5)))
        for first, second in combinations(SPACE_POINTS, 2)
    }
    require(len(directional) == 775 and directional == pair_generated,
            "independent affine-line constructions disagree")
    return tuple(sorted(directional, reverse=True))


def exact_cardinality_clauses(variables: tuple[int, ...], cardinality: int) -> list[list[int]]:
    require(0 <= cardinality <= len(variables), "invalid exact cardinality")
    clauses = [[-variable for variable in subset]
               for subset in combinations(variables, cardinality + 1)]
    clauses.extend(list(subset)
                   for subset in combinations(variables, len(variables) - cardinality + 1))
    return clauses


def check_cardinality_encoding() -> None:
    variables = tuple(range(1, 6))
    for cardinality in range(6):
        clauses = exact_cardinality_clauses(variables, cardinality)
        for mask in range(32):
            true_variables = {index + 1 for index in range(5) if mask & (1 << index)}
            satisfies = all(any((literal > 0) == (abs(literal) in true_variables)
                                for literal in clause) for clause in clauses)
            require(satisfies == (len(true_variables) == cardinality),
                    "hole-cardinality truth table failed")


def last_gauge(word: str) -> tuple[int, int, int]:
    full = [index for index, value in enumerate(word) if value == "4"]
    for triple in reversed(tuple(combinations(full, 3))):
        points = [divmod(index, 5) for index in triple]
        determinant = (
            (points[1][0] - points[0][0]) * (points[2][1] - points[0][1])
            - (points[2][0] - points[0][0]) * (points[1][1] - points[0][1])
        ) % 5
        if determinant:
            return triple
    raise RuntimeError("no noncollinear full-fiber triple")


def hole_formula(word: str, lines: tuple[tuple[int, ...], ...]) -> tuple[list[list[int]], tuple[int, int, int]]:
    # A positive variable means that the corresponding point is absent.
    clauses = [list(line) for line in lines]
    for fiber, selected_count in reversed(tuple(enumerate(map(int, word)))):
        variables = tuple(range(5 * fiber + 1, 5 * fiber + 6))
        clauses.extend(exact_cardinality_clauses(variables, 5 - selected_count))
    gauge = last_gauge(word)
    clauses.extend([[5 * fiber + 1] for fiber in gauge])
    return clauses, gauge


def write_cnf(path: Path, clauses: list[list[int]]) -> None:
    contents = [f"p cnf 125 {len(clauses)}\n"]
    contents.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    path.write_text("".join(contents), encoding="ascii")


def replay_hole_proofs(
    out: Path,
    checker: Path,
    representatives: list[dict[str, object]],
    lines: tuple[tuple[int, ...], ...],
    keep_proofs: bool,
) -> dict[str, object]:
    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    total_bytes = 0
    sum_conflicts = 0
    max_conflicts = -1
    max_conflict_case = -1
    clause_counts: list[int] = []
    record_hash = hashlib.sha256()
    for case, representative in enumerate(representatives):
        word = str(representative["weights"])
        clauses, gauge = hole_formula(word, lines)
        cnf = out / f"case_{case:04d}.cnf"
        proof = out / f"case_{case:04d}.drat"
        write_cnf(cnf, clauses)
        with Solver(name="cadical195", bootstrap_with=clauses, with_proof=True) as solver:
            answer = solver.solve()
            if answer is True:
                positive = {literal for literal in solver.get_model() if literal > 0}
                selected = {variable for variable in range(1, 126) if variable not in positive}
                require(len(selected) != 72 or any(set(line) <= selected for line in lines),
                        f"case {case} produced a genuine 72-point counterexample")
                raise RuntimeError(f"hole formula case {case} is SAT")
            require(answer is False, f"hole formula case {case} returned UNKNOWN")
            require(libc.fflush(None) == 0, "native proof stream flush failed")
            solver.solver.prfile.seek(0)
            proof.write_bytes(solver.solver.prfile.read())
            conflicts = solver.accum_stats()["conflicts"]
        checked = subprocess.run([str(checker), str(cnf), str(proof)],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        require(checked.returncode == 0 and b"s VERIFIED" in checked.stdout,
                f"DRAT check failed in case {case}")
        proof_bytes = proof.stat().st_size
        record = {
            "case": case,
            "clauses": len(clauses),
            "cnf_sha256": digest(cnf),
            "conflicts": conflicts,
            "gauge": list(gauge),
            "proof_bytes": proof_bytes,
            "proof_sha256": digest(proof),
        }
        encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
        record_hash.update(len(encoded).to_bytes(4, "big"))
        record_hash.update(encoded)
        total_bytes += proof_bytes
        sum_conflicts += conflicts
        clause_counts.append(len(clauses))
        if conflicts > max_conflicts:
            max_conflicts, max_conflict_case = conflicts, case
        if not keep_proofs:
            cnf.unlink()
            proof.unlink()
        if (case + 1) % 100 == 0 or case + 1 == len(representatives):
            print(json.dumps({"checked_hole_proofs": case + 1,
                              "total": len(representatives)}), file=sys.stderr, flush=True)
    return {
        "clause_count_range": [min(clause_counts), max(clause_counts)],
        "max_conflict_case": max_conflict_case,
        "max_conflicts": max_conflicts,
        "proof_bytes": total_bytes,
        "record_sha256": record_hash.hexdigest(),
        "sum_conflicts": sum_conflicts,
        "verified_unsat_proofs": len(representatives),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--structure-only", action="store_true")
    parser.add_argument("--keep-proofs", action="store_true")
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    require(checker.is_file(), "DRAT-trim executable is missing")

    low_plane = independent_low_plane_certificate()
    typed_catalogues = [enumerate_type(kind) for kind in range(3)]
    catalogue = {(kind, word) for kind, words in enumerate(typed_catalogues) for word in words}
    catalogue_bytes = serialize_catalogue(catalogue)
    catalogue_hash = hashlib.sha256(catalogue_bytes).hexdigest()
    require([len(words) for words in typed_catalogues] == [4442, 5428, 6322],
            "independent typed catalogue counts disagree")
    require(catalogue_hash == CATALOGUE_SHA256, "independent catalogue hash disagrees")
    catalogue_path = out / "catalogue.txt"
    catalogue_path.write_bytes(catalogue_bytes)

    representatives = json.loads((TARGET / "orbits.json").read_text())
    require(len(representatives) == 4332, "incorrect representative count")
    representative_path = out / "representatives.tsv"
    representative_path.write_text("".join(
        f"{record['type']} {record['weights']} {record['orbit_size']}\n"
        for record in representatives
    ), encoding="ascii")
    executable = out / "full_affine_check"
    flags = (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
             if args.sanitize else ["-O3"])
    subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Wconversion", *flags,
                    str(HERE / "full_affine_check.cpp"), "-o", str(executable)], check=True)
    affine = json.loads(subprocess.check_output(
        [str(executable), str(catalogue_path), str(representative_path)], text=True))
    require(affine["covered_typed_quotients"] == 16192
            and affine["representatives"] == 4332, "full affine partition check failed")

    check_cardinality_encoding()
    lines = affine_lines()
    proof_result = None
    if not args.structure_only:
        proof_result = replay_hole_proofs(out, checker, representatives, lines, args.keep_proofs)
    result = {
        "status": ("INDEPENDENT_UPPER_BOUND71_CHECK_PASSED"
                   if proof_result is not None else "INDEPENDENT_UPPER_BOUND71_STRUCTURE_PASSED"),
        "affine_partition": affine,
        "catalogue_sha256": catalogue_hash,
        "direct_encoding": (
            "125 complemented hole variables; positive line clauses; exact subset cardinalities; "
            "last noncollinear full-fiber gauge; no plane clauses or auxiliary variables"
        ),
        "drat_checker_sha256": digest(checker),
        "independent_typed_counts_AA_AB_BB": [len(words) for words in typed_catalogues],
        "lines": len(lines),
        "low_plane_certificate": low_plane,
        "proof_replay": proof_result,
    }
    (out / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
