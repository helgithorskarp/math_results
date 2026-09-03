#!/usr/bin/env python3
"""Find and definition-check two-summand stabilization witnesses for n=8."""

from __future__ import annotations

import itertools
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
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}

    # Each of X1,X2,Y1,Y2,Y3 is a transitive tournament.  A tournament is
    # transitive exactly when it has no directed triangle.
    for layer in range(5):
        for i, j, k in itertools.combinations(range(N), 3):
            ij = variable(layer, pair_index[i, j])
            ik = variable(layer, pair_index[i, k])
            jk = variable(layer, pair_index[j, k])
            clauses.append([-ij, -jk, ik])
            clauses.append([ij, jk, -ik])

    # Layer order is X1,X2,Y1,Y2,Y3.  Forbid exactly the local truth-table
    # rows that violate T+X1+X2=Y1+Y2+Y3.
    for edge in range(EDGE_COUNT):
        t = (tournament >> edge) & 1
        variables = [variable(layer, edge) for layer in range(5)]
        for bits in itertools.product((0, 1), repeat=5):
            if t + bits[0] + bits[1] == bits[2] + bits[3] + bits[4]:
                continue
            clauses.append([-var if bit else var for var, bit in zip(variables, bits)])
    return clauses


def write_cnf(path: Path, clauses: list[list[int]]) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write(f"p cnf {5 * EDGE_COUNT} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def read_solution(path: Path) -> set[int]:
    true_variables: set[int] = set()
    saw_sat = False
    for line in path.read_text(encoding="ascii").splitlines():
        if line == "s SATISFIABLE":
            saw_sat = True
        elif line.startswith("v "):
            for literal in map(int, line[2:].split()):
                if literal > 0:
                    true_variables.add(literal)
    if not saw_sat:
        raise ValueError(f"solver did not report SAT in {path}")
    return true_variables


def mask_from_solution(true_variables: set[int], layer: int) -> int:
    result = 0
    for edge in range(EDGE_COUNT):
        if variable(layer, edge) in true_variables:
            result |= 1 << edge
    return result


def tournament_matrix(mask: int) -> list[list[int]]:
    matrix = [[0] * N for _ in range(N)]
    for edge, (i, j) in enumerate(PAIRS):
        matrix[i][j] = (mask >> edge) & 1
        matrix[j][i] = 1 - matrix[i][j]
    return matrix


def order_from_mask(mask: int) -> tuple[int, ...]:
    matrix = tournament_matrix(mask)
    scores = [sum(row) for row in matrix]
    if sorted(scores) != list(range(N)):
        raise ValueError(f"nontransitive solver layer: mask={mask}")
    return tuple(sorted(range(N), key=scores.__getitem__))


def check_witness(tournament: int, masks: list[int]) -> None:
    if len(masks) != 5:
        raise ValueError("expected five order masks")
    matrices = [tournament_matrix(mask) for mask in masks]
    tournament_matrix_value = tournament_matrix(tournament)
    for mask in masks:
        order_from_mask(mask)
    for i in range(N):
        for j in range(N):
            lhs = tournament_matrix_value[i][j] + matrices[0][i][j] + matrices[1][i][j]
            rhs = matrices[2][i][j] + matrices[3][i][j] + matrices[4][i][j]
            if lhs != rhs:
                raise ValueError(f"bad equation at ({i},{j}): {lhs} != {rhs}")


def format_order(order: tuple[int, ...]) -> str:
    return ",".join(map(str, order))


def main() -> int:
    if len(sys.argv) != 5:
        print("usage: solve_m2.py SEARCH_OUTPUT CADICAL WORK_DIRECTORY CERTIFICATE", file=sys.stderr)
        return 2
    search_output = Path(sys.argv[1])
    cadical = Path(sys.argv[2])
    work_directory = Path(sys.argv[3])
    certificate_path = Path(sys.argv[4])
    work_directory.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[int, int]] = []
    for line in search_output.read_text(encoding="ascii").splitlines():
        match = FAIL_RE.fullmatch(line)
        if match:
            failures.append((int(match["class_index"]), int(match["mask"])))
    if len(failures) != 96:
        raise ValueError(f"expected 96 one-summand failures, got {len(failures)}")

    certificate_lines = [f"CERTIFICATE stable_tournaments_n8_m2_v1 classes={len(failures)}"]
    for offset, (class_index, tournament) in enumerate(failures, start=1):
        clauses = build_cnf(tournament)
        cnf_path = work_directory / f"class_{class_index}.cnf"
        solution_path = work_directory / f"class_{class_index}.sol"
        write_cnf(cnf_path, clauses)
        completed = subprocess.run(
            [str(cadical), "-q", "--sat", "-w", str(solution_path), str(cnf_path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 10:
            raise RuntimeError(
                f"CaDiCaL failed on class {class_index}: return={completed.returncode} "
                f"stderr={completed.stderr}"
            )
        true_variables = read_solution(solution_path)
        masks = [mask_from_solution(true_variables, layer) for layer in range(5)]
        check_witness(tournament, masks)
        orders = [order_from_mask(mask) for mask in masks]
        certificate_lines.append(
            f"CLASS {class_index} tournament={tournament} "
            + " ".join(
                f"{name}={format_order(order)}"
                for name, order in zip(("x1", "x2", "y1", "y2", "y3"), orders)
            )
        )
        print(f"solved {offset}/{len(failures)} class={class_index}", file=sys.stderr)

    certificate_lines.append(f"SUMMARY classes={len(failures)} m2_witnesses={len(failures)}")
    certificate_path.write_text("\n".join(certificate_lines) + "\n", encoding="ascii")
    print(f"wrote {certificate_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
