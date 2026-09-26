"""Independent primary-variable check of every mixed 8/9-plane lift.

This deliberately does not import the reviewed contribution's model.py and
does not encode its redundant plane-cap constraints.  Exact five-point fiber
cardinalities are expanded directly into subset clauses, leaving only the 125
point variables.  Each UNSAT result is accepted only after DRAT-trim verifies
the solver's proof against the emitted DIMACS file.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import time

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "no_eight_planes72"
POINTS = tuple(product(range(5), repeat=3))
POINT_INDEX = {point: index + 1 for index, point in enumerate(POINTS)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def directions() -> tuple[tuple[int, int, int], ...]:
    result = []
    for vector in POINTS:
        if vector == (0, 0, 0):
            continue
        first = next(coordinate for coordinate in vector if coordinate)
        inverse = pow(first, -1, 5)
        normalized = tuple(inverse * coordinate % 5 for coordinate in vector)
        if normalized not in result:
            result.append(normalized)
    return tuple(result)


def affine_lines() -> tuple[tuple[int, ...], ...]:
    lines = {
        tuple(
            sorted(
                POINT_INDEX[
                    tuple((point[j] + scalar * vector[j]) % 5 for j in range(3))
                ]
                for scalar in range(5)
            )
        )
        for point in POINTS
        for vector in directions()
    }
    if len(lines) != 775:
        raise RuntimeError(f"expected 775 affine lines, found {len(lines)}")
    return tuple(sorted(lines))


LINES = affine_lines()


def exact_five(literals: tuple[int, ...], weight: int) -> list[list[int]]:
    """Prime subset clauses for exactly ``weight`` of five literals."""
    if len(literals) != 5 or not 0 <= weight <= 5:
        raise ValueError("invalid five-variable cardinality")
    clauses = [
        [-literal for literal in subset]
        for subset in combinations(literals, weight + 1)
    ]
    clauses.extend(
        list(subset)
        for subset in combinations(literals, 6 - weight)
    )
    return clauses


def check_cardinality_encoding() -> None:
    literals = (1, 2, 3, 4, 5)
    for weight in range(6):
        clauses = exact_five(literals, weight)
        for bits in product((False, True), repeat=5):
            selected = {index + 1 for index, bit in enumerate(bits) if bit}
            satisfied = all(
                any((literal > 0) == (abs(literal) in selected) for literal in clause)
                for clause in clauses
            )
            if satisfied != (sum(bits) == weight):
                raise RuntimeError("direct cardinality encoding failed its truth table")


def noncollinear(triple: tuple[int, int, int]) -> bool:
    points = tuple((index // 5, index % 5) for index in triple)
    (x0, y0), (x1, y1), (x2, y2) = points
    return ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)) % 5 != 0


def build_formula(
    word: str, *, gauge_fix: bool = True, expected_total: int = 72
) -> tuple[list[list[int]], tuple[int, int, int] | None]:
    if len(word) != 25 or any(character not in "01234" for character in word):
        raise ValueError("invalid quotient word")
    weights = tuple(map(int, word))
    if sum(weights) != expected_total:
        raise ValueError(f"quotient word does not total {expected_total}")
    clauses = [[-variable for variable in line] for line in LINES]
    for index, weight in enumerate(weights):
        fiber = tuple(range(5 * index + 1, 5 * index + 6))
        clauses.extend(exact_five(fiber, weight))
    gauge = None
    if gauge_fix:
        four_fibers = tuple(index for index, weight in enumerate(weights) if weight == 4)
        gauge = next(
            (triple for triple in combinations(four_fibers, 3) if noncollinear(triple)),
            None,
        )
        if gauge is None:
            raise RuntimeError("no noncollinear three-hole gauge")
        clauses.extend([[-(5 * index + 1)] for index in gauge])
    return clauses, gauge


def write_dimacs(path: Path, clauses: list[list[int]]) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write(f"p cnf 125 {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)))
            output.write(" 0\n")


def validate_witness(word: str, model: list[int]) -> None:
    selected = {literal for literal in model if 0 < literal <= 125}
    if any(set(line) <= selected for line in LINES):
        raise RuntimeError("SAT witness contains an affine line")
    for index, weight in enumerate(map(int, word)):
        actual = sum(variable in selected for variable in range(5 * index + 1, 5 * index + 6))
        if actual != weight:
            raise RuntimeError("SAT witness has an incorrect fiber weight")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=1252)
    parser.add_argument("--conflicts", type=int, default=500_000)
    args = parser.parse_args()
    if not 0 <= args.start < args.stop <= 1252 or args.conflicts <= 0:
        parser.error("invalid interval or conflict budget")

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    representatives = json.loads((TARGET / "orbits.json").read_text())
    if len(representatives) != 1252:
        raise RuntimeError("incomplete representative family")

    check_cardinality_encoding()
    known = json.loads((TARGET.parent / "known70.json").read_text())["points"]
    known_word = "".join(str(sum(point // 5 == index for point in known)) for index in range(25))
    control_clauses, _ = build_formula(known_word, gauge_fix=False, expected_total=70)
    with Solver(name="cadical195", bootstrap_with=control_clauses) as control_solver:
        if not control_solver.solve():
            raise RuntimeError("independent encoding rejected the known 70-point set")
        validate_witness(known_word, control_solver.get_model())

    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    records = []
    started = time.monotonic()
    for index in range(args.start, args.stop):
        word = representatives[index]["weights"]
        clauses, gauge = build_formula(word)
        cnf = out / f"case_{index:04d}.cnf"
        proof = out / f"case_{index:04d}.drat"
        log = out / f"case_{index:04d}.log"
        write_dimacs(cnf, clauses)
        case_started = time.monotonic()
        with Solver(name="cadical195", bootstrap_with=clauses, with_proof=True) as solver:
            solver.conf_budget(args.conflicts)
            answer = solver.solve_limited()
            if answer is True:
                validate_witness(word, solver.get_model())
                raise RuntimeError(f"case {index} has a valid line-free lift")
            if answer is None:
                raise RuntimeError(f"case {index} reached the conflict budget")
            if libc.fflush(None) != 0:
                raise RuntimeError("native proof stream flush failed")
            solver.solver.prfile.seek(0)
            proof.write_bytes(solver.solver.prfile.read())
            stats = solver.accum_stats()
        with log.open("w") as output:
            checked = subprocess.run(
                [str(checker), str(cnf), str(proof)],
                stdout=output,
                stderr=subprocess.STDOUT,
                check=False,
                text=True,
            )
        if checked.returncode != 0 or "s VERIFIED" not in log.read_text():
            raise RuntimeError(f"DRAT-trim rejected case {index}")
        record = {
            "index": index,
            "status": "UNSAT_DRAT_VERIFIED",
            "gauge": list(gauge),
            "variables": 125,
            "clauses": len(clauses),
            "cnf_sha256": sha256(cnf),
            "proof_sha256": sha256(proof),
            "proof_bytes": proof.stat().st_size,
            "conflicts": stats["conflicts"],
            "seconds": time.monotonic() - case_started,
        }
        (out / f"case_{index:04d}.json").write_text(json.dumps(record, indent=2) + "\n")
        records.append(record)
        print(json.dumps({"case": index, "status": record["status"]}), flush=True)

    summary = {
        "status": "INDEPENDENT_PRIMARY_ENCODING_VERIFIED",
        "start": args.start,
        "stop": args.stop,
        "verified": len(records),
        "complete_family": args.start == 0 and args.stop == 1252,
        "line_count": len(LINES),
        "variables_per_case": 125,
        "cardinality_truth_table": True,
        "positive_control_size": 70,
        "checker_sha256": sha256(checker),
        "proof_bytes": sum(record["proof_bytes"] for record in records),
        "max_conflicts": max(record["conflicts"] for record in records),
        "elapsed_seconds": time.monotonic() - started,
        "cases": records,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "cases"}, indent=2))


if __name__ == "__main__":
    main()
