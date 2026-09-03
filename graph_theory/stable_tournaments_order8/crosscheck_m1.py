#!/usr/bin/env python3
"""Generate m=1 CNFs and cross-check the 96 negative classes with two solvers."""

from __future__ import annotations

import hashlib
import itertools
import os
import re
import subprocess
import sys
from pathlib import Path

N = 8
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
EDGE_COUNT = len(PAIRS)
FAIL_RE = re.compile(r"^FAIL (?P<class_index>\d+) tournament=(?P<mask>\d+)$")


def variable(layer: int, edge: int) -> int:
    return layer * EDGE_COUNT + edge + 1


def build_cnf(tournament: int) -> list[list[int]]:
    clauses: list[list[int]] = []
    pair_index = {pair: edge for edge, pair in enumerate(PAIRS)}
    for layer in range(3):
        for i, j, k in itertools.combinations(range(N), 3):
            ij = variable(layer, pair_index[i, j])
            ik = variable(layer, pair_index[i, k])
            jk = variable(layer, pair_index[j, k])
            clauses.append([-ij, -jk, ik])
            clauses.append([ij, jk, -ik])
    for edge in range(EDGE_COUNT):
        t = (tournament >> edge) & 1
        variables = [variable(layer, edge) for layer in range(3)]
        for bits in itertools.product((0, 1), repeat=3):
            if t + bits[0] == bits[1] + bits[2]:
                continue
            clauses.append([-var if bit else var for var, bit in zip(variables, bits)])
    return clauses


def write_cnf(path: Path, clauses: list[list[int]]) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write(f"p cnf {3 * EDGE_COUNT} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def main() -> int:
    if len(sys.argv) != 6:
        print(
            "usage: crosscheck_m1.py CLASSIFIER_OUTPUT CADICAL MINISAT WORK_DIRECTORY SUMMARY",
            file=sys.stderr,
        )
        return 2
    classifier_output, cadical, minisat, work_directory, summary_path = map(Path, sys.argv[1:])
    work_directory.mkdir(parents=True, exist_ok=True)
    failures: list[tuple[int, int]] = []
    for line in classifier_output.read_text(encoding="ascii").splitlines():
        match = FAIL_RE.fullmatch(line)
        if match:
            failures.append((int(match["class_index"]), int(match["mask"])))
    if len(failures) != 96:
        raise ValueError(f"expected 96 negative classes, got {len(failures)}")

    minisat_environment = dict(os.environ)
    minisat_environment["LD_LIBRARY_PATH"] = str(minisat.parent.parent / "lib")
    summary = ["class\ttournament\tvariables\tclauses\tcnf_sha256\tcadical\tminisat"]
    for offset, (class_index, tournament) in enumerate(failures, start=1):
        clauses = build_cnf(tournament)
        cnf_path = work_directory / f"class_{class_index}.cnf"
        cadical_result = work_directory / f"class_{class_index}.cadical.result"
        cadical_log = work_directory / f"class_{class_index}.cadical.log"
        minisat_result = work_directory / f"class_{class_index}.minisat.result"
        minisat_log = work_directory / f"class_{class_index}.minisat.log"
        write_cnf(cnf_path, clauses)

        completed = subprocess.run(
            [str(cadical), "-q", "--unsat", "-w", str(cadical_result), str(cnf_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        cadical_log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
        if completed.returncode != 20 or "s UNSATISFIABLE" not in cadical_result.read_text(
            encoding="ascii"
        ):
            raise RuntimeError(f"CaDiCaL did not prove UNSAT for class {class_index}")

        completed = subprocess.run(
            [str(minisat), str(cnf_path), str(minisat_result)],
            check=False,
            capture_output=True,
            text=True,
            env=minisat_environment,
        )
        minisat_log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
        if completed.returncode != 20 or minisat_result.read_text(encoding="ascii").strip() != "UNSAT":
            raise RuntimeError(f"MiniSat did not prove UNSAT for class {class_index}")

        digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
        summary.append(
            f"{class_index}\t{tournament}\t{3 * EDGE_COUNT}\t{len(clauses)}\t{digest}"
            "\tUNSAT\tUNSAT"
        )
        print(f"checked {offset}/{len(failures)} class={class_index}", file=sys.stderr)
    summary_path.write_text("\n".join(summary) + "\n", encoding="ascii")
    print(f"verified {len(failures)} negative classes with CaDiCaL and MiniSat")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
