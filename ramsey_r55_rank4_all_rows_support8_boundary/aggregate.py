#!/usr/bin/env python3
"""One physical CNF for every canonical rank-four row task with |supp(B)| <= 8."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import shutil
import time


N = 43
A_SIZE = 20
B_SIZE = 23
LABELS = 16
EXPECTED_COVER_SHA256 = "bd1161b4261eb1ee3f8bc2cd0104a062c858bf38d596cf725acbfb195b158bac"


def dot(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def rank(values: list[int]) -> int:
    basis: dict[int, int] = {}
    for value in values:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def rows_from_code(code: int) -> list[int]:
    if type(code) is not int or not 0 <= code < 2**30:
        raise ValueError("invalid row code")
    counts = [(code >> (2 * value)) & 3 for value in range(15)]
    zeros = 20 - sum(counts)
    if zeros not in (0, 1):
        raise ValueError("invalid row weight")
    rows = [0] * zeros + [
        value for value in range(1, 16) for _ in range(counts[value - 1])
    ]
    if len(rows) != A_SIZE or rows != sorted(rows) or rank(rows) != 4:
        raise ValueError("invalid canonical row task")
    if max(Counter(rows).values()) > 3:
        raise ValueError("row multiplicity exceeds three")
    return rows


def load_cover(path: Path) -> tuple[list[dict], str]:
    digest = file_sha256(path)
    if digest != EXPECTED_COVER_SHA256:
        raise ValueError(f"unexpected row-cover hash {digest}")
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "code\tzero\torbit_size\tsupport\ttriples":
        raise ValueError("row-cover header")
    tasks = []
    previous = -1
    for line in lines[1:]:
        fields = list(map(int, line.split("\t")))
        if len(fields) != 5:
            raise ValueError("row-cover fields")
        code, zero, orbit_size, support, triples = fields
        rows = rows_from_code(code)
        counts = Counter(rows)
        if not (
            code > previous
            and zero == counts[0]
            and orbit_size > 0
            and 20160 % orbit_size == 0
            and support == sum(counts[x] > 0 for x in range(1, 16))
            and triples == sum(counts[x] == 3 for x in range(1, 16))
        ):
            raise ValueError(f"row-cover metadata at code {code}")
        tasks.append({
            "code": code,
            "zero": zero,
            "orbit_size": orbit_size,
            "support": support,
            "triples": triples,
            "rows": rows,
        })
        previous = code
    if len(tasks) != 10959:
        raise ValueError(f"unexpected task count {len(tasks)}")
    if sum(task["orbit_size"] for task in tasks) != 154847637:
        raise ValueError("unexpected covered row-profile mass")
    return tasks, digest


class StreamCNF:
    def __init__(self, body_path: Path):
        if body_path.exists():
            raise ValueError(f"refusing existing body {body_path}")
        self.body_path = body_path
        self.handle = body_path.open("w", encoding="ascii")
        self.variables = 0
        self.clauses = 0
        self.length_histogram: dict[int, int] = {}

    def new_var(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, literals) -> None:
        unique = []
        seen = set()
        for literal in literals:
            if not literal or type(literal) is not int:
                raise ValueError("invalid literal")
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                unique.append(literal)
        self.handle.write(" ".join(map(str, unique)) + " 0\n")
        self.clauses += 1
        self.length_histogram[len(unique)] = self.length_histogram.get(len(unique), 0) + 1

    def gate_or(self, literals: list[int]) -> int:
        if not literals:
            raise ValueError("empty OR gate")
        output = self.new_var()
        self.add([-output] + literals)
        for literal in literals:
            self.add([output, -literal])
        return output

    def gate_and(self, literals: list[int]) -> int:
        if not literals:
            raise ValueError("empty AND gate")
        output = self.new_var()
        self.add([output] + [-literal for literal in literals])
        for literal in literals:
            self.add([-output, literal])
        return output

    def at_most(self, literals: list[int], bound: int, gate: int | None = None) -> None:
        """Sinz sequential encoding of sum(literals) <= bound."""
        def emit(clause) -> None:
            self.add(([-gate] if gate is not None else []) + list(clause))

        n = len(literals)
        if bound >= n:
            return
        if bound < 0:
            emit([])
            return
        if bound == 0:
            for literal in literals:
                emit([-literal])
            return
        state = [[self.new_var() for _ in range(bound)] for _ in range(n - 1)]
        emit([-literals[0], state[0][0]])
        for column in range(1, bound):
            emit([-state[0][column]])
        for row in range(1, n - 1):
            emit([-literals[row], state[row][0]])
            emit([-state[row - 1][0], state[row][0]])
            for column in range(1, bound):
                emit([-literals[row], -state[row - 1][column - 1], state[row][column]])
                emit([-state[row - 1][column], state[row][column]])
        for row in range(1, n):
            emit([-literals[row], -state[row - 1][bound - 1]])

    def at_least(self, literals: list[int], bound: int, gate: int | None = None) -> None:
        self.at_most([-literal for literal in literals], len(literals) - bound, gate)

    def finish(self, cnf_path: Path) -> None:
        self.handle.close()
        if cnf_path.exists():
            raise ValueError(f"refusing existing CNF {cnf_path}")
        with cnf_path.open("wb") as output:
            output.write(f"p cnf {self.variables} {self.clauses}\n".encode("ascii"))
            with self.body_path.open("rb") as body:
                shutil.copyfileobj(body, output, length=1024 * 1024)
        self.body_path.unlink()


def xor_gate(formula: StreamCNF, first: int, second: int) -> int:
    output = formula.new_var()
    formula.add([first, second, -output])
    formula.add([first, -second, output])
    formula.add([-first, second, output])
    formula.add([-first, -second, -output])
    return output


def build(cover_path: Path, cnf_path: Path, metadata_path: Path) -> dict:
    if metadata_path.exists():
        raise ValueError(f"refusing existing metadata {metadata_path}")
    tasks, cover_hash = load_cover(cover_path)
    started = time.monotonic()
    formula = StreamCNF(cnf_path.with_suffix(cnf_path.suffix + ".body"))
    blocks: dict[str, dict[str, int]] = {}

    def record(name: str, before_variables: int, before_clauses: int) -> None:
        blocks[name] = {
            "variables": formula.variables - before_variables,
            "clauses": formula.clauses - before_clauses,
        }

    def before() -> tuple[int, int]:
        return formula.variables, formula.clauses

    # Exactly one canonical row task.  Each selector implies the corresponding
    # sorted physical row labels; row-label at-most-one then makes the list exact.
    mark = before()
    selectors = [formula.new_var() for _ in tasks]
    formula.add(selectors)
    formula.at_most(selectors, 1)
    row_label = [[formula.new_var() for _ in range(LABELS)] for _ in range(A_SIZE)]
    for row in row_label:
        for first, second in combinations(row, 2):
            formula.add([-first, -second])
    for selector, task in zip(selectors, tasks):
        for position, label in enumerate(task["rows"]):
            formula.add([-selector, row_label[position][label]])
    record("canonical_row_selector", *mark)

    # All 443 internal edges and 460 cross edges are independent physical
    # variables before the factor equations and Ramsey clauses are imposed.
    mark = before()
    physical: dict[tuple[int, int], int] = {}
    internal: dict[tuple[int, int], int] = {}
    cross: dict[tuple[int, int], int] = {}
    for edge in combinations(range(N), 2):
        variable = formula.new_var()
        physical[edge] = variable
        if (edge[0] < A_SIZE) == (edge[1] < A_SIZE):
            internal[edge] = variable
        else:
            cross[edge] = variable
    if len(internal) != 443 or len(cross) != 460 or len(physical) != 903:
        raise RuntimeError("physical edge allocation")
    record("physical_edges", *mark)

    # Sorted B labels, exact caps, support indicators, support <= 8, spanning,
    # and zero-row/zero-column incompatibility.
    mark = before()
    column_label = [[formula.new_var() for _ in range(LABELS)] for _ in range(B_SIZE)]
    for row in column_label:
        formula.add(row)
        for first, second in combinations(row, 2):
            formula.add([-first, -second])
    for position in range(B_SIZE - 1):
        for larger in range(LABELS):
            for smaller in range(larger):
                formula.add([-column_label[position][larger], -column_label[position + 1][smaller]])
    for value in range(LABELS):
        cap = 2 if value == 0 else 5
        for position in range(B_SIZE - cap):
            formula.add([-column_label[position][value], -column_label[position + cap][value]])
    support = [formula.gate_or([column_label[position][value] for position in range(B_SIZE)])
               for value in range(LABELS)]
    formula.at_most(support, 8)
    formula.add([-row_label[0][0], -support[0]])
    for normal in range(1, LABELS):
        formula.add([
            column_label[position][value]
            for position in range(B_SIZE)
            for value in range(LABELS)
            if dot(normal, value)
        ])
    record("column_labels_caps_support_span", *mark)

    # Stars encode every nonzero label's dot products with B.  A physical cross
    # edge selects its star through the canonical but variable row label.
    mark = before()
    stars = [[None] * B_SIZE for _ in range(LABELS)]
    for value in range(1, LABELS):
        for position in range(B_SIZE):
            star = formula.new_var()
            stars[value][position] = star
            for column_value in range(LABELS):
                formula.add([
                    -column_label[position][column_value],
                    star if dot(value, column_value) else -star,
                ])
    for row_position in range(A_SIZE):
        for column_position in range(B_SIZE):
            edge = cross[row_position, A_SIZE + column_position]
            formula.add([-row_label[row_position][0], -edge])
            for value in range(1, LABELS):
                star = stars[value][column_position]
                formula.add([-row_label[row_position][value], -edge, star])
                formula.add([-row_label[row_position][value], edge, -star])
    record("dot_product_cross_edges", *mark)

    # Exact complement-cut rank >= 4.  A rank drop occurs exactly when
    # U p = 1, V q = 1, and p.q = 1.  One long clause forbids each such pair.
    mark = before()
    rank_guard_pairs = 0
    for row_normal in range(1, LABELS):
        for column_normal in range(1, LABELS):
            if not dot(row_normal, column_normal):
                continue
            rank_guard_pairs += 1
            formula.add([
                row_label[position][value]
                for position in range(A_SIZE)
                for value in range(LABELS)
                if not dot(value, row_normal)
            ] + [
                column_label[position][value]
                for position in range(B_SIZE)
                for value in range(LABELS)
                if not dot(value, column_normal)
            ])
    if rank_guard_pairs != 120:
        raise RuntimeError("complement-rank guard count")
    record("complement_rank_four", *mark)

    # Detect every tripled row label from the sorted row list, then gate h3771's
    # 10..13 contact interval.  Table membership guarantees the cap of three.
    mark = before()
    tripled = [None] * LABELS
    triple_windows: dict[int, list[int]] = {}
    for value in range(1, LABELS):
        windows = [
            formula.gate_and([row_label[position][value], row_label[position + 2][value]])
            for position in range(A_SIZE - 2)
        ]
        triple_windows[value] = windows
        tripled[value] = formula.gate_or(windows)
        formula.at_least([stars[value][position] for position in range(B_SIZE)], 10,
                         tripled[value])
        formula.at_most([stars[value][position] for position in range(B_SIZE)], 13,
                        tripled[value])
    record("tripled_row_contacts", *mark)

    # Sorted rows with cap three can agree only at distance one or two; sorted
    # columns with cap five can agree only at distance one through four.
    mark = before()
    row_pairs = [(first, first + distance)
                 for distance in (1, 2)
                 for first in range(A_SIZE - distance)]
    column_pairs = [(first, first + distance)
                    for distance in (1, 2, 3, 4)
                    for first in range(B_SIZE - distance)]
    row_equal_gates = []
    column_equal_gates = []
    for first, second in row_pairs:
        equal = formula.new_var()
        row_equal_gates.append(equal)
        for value in range(LABELS):
            formula.add([-row_label[first][value], -row_label[second][value], equal])
        differences = []
        for other in range(A_SIZE):
            if other in (first, second):
                continue
            differences.append(xor_gate(
                formula,
                internal[tuple(sorted((first, other)))],
                internal[tuple(sorted((second, other)))],
            ))
        formula.at_least(differences, 8, equal)
    for first, second in column_pairs:
        equal = formula.new_var()
        column_equal_gates.append(equal)
        for value in range(LABELS):
            formula.add([-column_label[first][value], -column_label[second][value], equal])
        differences = []
        for other in range(B_SIZE):
            if other in (first, second):
                continue
            differences.append(xor_gate(
                formula,
                internal[tuple(sorted((A_SIZE + first, A_SIZE + other)))],
                internal[tuple(sorted((A_SIZE + second, A_SIZE + other)))],
            ))
        formula.at_least(differences, 8, equal)
    record("equal_label_pair_distances", *mark)

    # R(4,5)=25 gives the exact necessary red-degree interval 18..24.
    mark = before()
    for vertex in range(N):
        incident = [physical[tuple(sorted((vertex, other)))]
                    for other in range(N) if other != vertex]
        if len(incident) != 42 or len(set(incident)) != 42:
            raise RuntimeError("physical degree literals")
        formula.at_least(incident, 18)
        formula.at_most(incident, 24)
    record("degree_18_24", *mark)

    # Literal physical target: both polarities for every five-set.
    mark = before()
    physical_five_sets = 0
    for vertices in combinations(range(N), 5):
        edges = [physical[edge] for edge in combinations(vertices, 2)]
        formula.add(edges)
        formula.add([-edge for edge in edges])
        physical_five_sets += 1
    if physical_five_sets != 962598:
        raise RuntimeError("five-set count")
    record("physical_five_sets", *mark)

    formula.finish(cnf_path)
    metadata = {
        "schema": "rank4-all-canonical-rows-total-support-at-most-eight-v1",
        "scope": {
            "canonical_row_tasks": len(tasks),
            "covered_row_profiles": sum(task["orbit_size"] for task in tasks),
            "column_vertices": B_SIZE,
            "column_total_support_maximum": 8,
            "column_zero_cap": 2,
            "column_nonzero_cap": 5,
            "internal_physical_edges": len(internal),
            "cross_physical_edges": len(cross),
            "physical_five_sets": physical_five_sets,
        },
        "cover": {
            "path_name": cover_path.name,
            "sha256": cover_hash,
            "row_codes": [task["code"] for task in tasks],
            "selector_variables": selectors,
        },
        "maps": {
            "row_label_variables": row_label,
            "column_label_variables": column_label,
            "support_variables": support,
            "tripled_variables": tripled,
            "internal_variables": {f"{a},{b}": variable for (a, b), variable in internal.items()},
            "cross_variables": {f"{a},{b}": variable for (a, b), variable in cross.items()},
        },
        "optimized_pair_windows": {
            "row_pairs": [list(pair) for pair in row_pairs],
            "column_pairs": [list(pair) for pair in column_pairs],
            "row_equal_gates": row_equal_gates,
            "column_equal_gates": column_equal_gates,
        },
        "rank_guard_pairs": rank_guard_pairs,
        "blocks": blocks,
        "formula": {
            "variables": formula.variables,
            "clauses": formula.clauses,
            "bytes": cnf_path.stat().st_size,
            "sha256": file_sha256(cnf_path),
            "clause_length_histogram": {str(k): v for k, v in sorted(formula.length_histogram.items())},
            "generation_seconds": time.monotonic() - started,
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.cover, args.cnf, args.metadata), sort_keys=True))


if __name__ == "__main__":
    main()
