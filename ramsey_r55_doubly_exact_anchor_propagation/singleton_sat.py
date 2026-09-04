#!/usr/bin/env python3
"""Generate/check the exact SAT dichotomy for the residual blue singleton.

The Boolean variables x_{ij}, 0 <= i < j < 42, encode a red edge in
F = G-u.  Vertices 0,...,20 form C=N_R(u); vertices 21,...,41 form
O=N_B(u), with vertex 21 the unique red-degree-20 vertex.  The formula is
a relaxation of the residual singleton normal form.  Consequently:

* UNSAT eliminates that normal form; and
* every SAT model extends (by the fixed edges incident with u) to an
  honest order-43 graph with no monochromatic K_5.

Only the sequential-counter auxiliary variables depend on the encoding.
The first 861 variables always have the graph interpretation above.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path
from typing import Sequence


N_F = 42
U = 42
C = tuple(range(21))
O = tuple(range(21, 42))
Z = 21
EDGE_PAIRS = tuple(itertools.combinations(range(N_F), 2))
EDGE_VAR = {edge: i + 1 for i, edge in enumerate(EDGE_PAIRS)}
BASE_VARS = len(EDGE_PAIRS)


def edge_var(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return EDGE_VAR[(i, j)]


class ClauseSink:
    """Base class supplying fresh variables and cardinality encodings."""

    def __init__(self, first_fresh: int = BASE_VARS + 1) -> None:
        self.next_var = first_fresh
        self.nclauses = 0

    def fresh(self) -> int:
        ans = self.next_var
        self.next_var += 1
        return ans

    def add(self, clause: Sequence[int]) -> None:
        raise NotImplementedError

    def at_most(self, literals: Sequence[int], k: int) -> None:
        """Sinz sequential-counter encoding of sum(literals) <= k."""
        n = len(literals)
        if k < 0:
            self.add(())
            return
        if k >= n:
            return
        if k == 0:
            for literal in literals:
                self.add((-literal,))
            return

        # s[i][j] represents: among positions 0,...,i, at least j+1
        # literals are true.  Only rows i=0,...,n-2 are needed.
        s = [[self.fresh() for _ in range(k)] for _ in range(n - 1)]
        self.add((-literals[0], s[0][0]))
        for j in range(1, k):
            self.add((-s[0][j],))

        for i in range(1, n - 1):
            self.add((-literals[i], s[i][0]))
            self.add((-s[i - 1][0], s[i][0]))
            for j in range(1, k):
                self.add((-literals[i], -s[i - 1][j - 1], s[i][j]))
                self.add((-s[i - 1][j], s[i][j]))

        for i in range(1, n):
            self.add((-literals[i], -s[i - 1][k - 1]))

    def exactly(self, literals: Sequence[int], k: int) -> None:
        self.at_most(literals, k)
        self.at_most(tuple(-literal for literal in literals), len(literals) - k)


class DimacsWriter(ClauseSink):
    HEADER = f"p cnf {0:12d} {0:12d}\n"

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.file = path.open("w+", encoding="ascii", newline="\n")
        self.file.write(self.HEADER)

    def add(self, clause: Sequence[int]) -> None:
        self.file.write(" ".join(map(str, clause)))
        self.file.write(" 0\n")
        self.nclauses += 1

    def finish(self) -> tuple[int, int]:
        nvars = self.next_var - 1
        header = f"p cnf {nvars:12d} {self.nclauses:12d}\n"
        if len(header) != len(self.HEADER):
            raise AssertionError("DIMACS header width overflow")
        self.file.seek(0)
        self.file.write(header)
        self.file.close()
        return nvars, self.nclauses


class MemorySink(ClauseSink):
    def __init__(self, first_fresh: int) -> None:
        super().__init__(first_fresh)
        self.clauses: list[tuple[int, ...]] = []

    def add(self, clause: Sequence[int]) -> None:
        self.clauses.append(tuple(clause))
        self.nclauses += 1


def generate_formula(path: Path) -> tuple[int, int]:
    sink = DimacsWriter(path)

    # Both colors are forbidden on every 5-set of F.
    for vertices in itertools.combinations(range(N_F), 5):
        edges = tuple(edge_var(i, j) for i, j in itertools.combinations(vertices, 2))
        sink.add(tuple(-literal for literal in edges))  # no red K_5
        sink.add(edges)  # no blue K_5

    # A monochromatic K_5 through u is exactly a red K_4 in C or a blue
    # K_4 in O, because all u-C edges are red and all u-O edges are blue.
    for vertices in itertools.combinations(C, 4):
        sink.add(tuple(-edge_var(i, j) for i, j in itertools.combinations(vertices, 2)))
    for vertices in itertools.combinations(O, 4):
        sink.add(tuple(edge_var(i, j) for i, j in itertools.combinations(vertices, 2)))

    # In F=G-u, all vertices in C and z have red degree 20; the other
    # twenty vertices in O have red degree 21.
    for vertex in range(N_F):
        incident = tuple(edge_var(vertex, other) for other in range(N_F) if other != vertex)
        target = 20 if vertex in C or vertex == Z else 21
        sink.exactly(incident, target)

    # The two exact order-21 cores have 100 edges in their relevant color:
    # G[C] has 100 red edges and G[O] has 100 blue (=110 red) edges.
    sink.exactly(tuple(edge_var(i, j) for i, j in itertools.combinations(C, 2)), 100)
    sink.exactly(tuple(edge_var(i, j) for i, j in itertools.combinations(O, 2)), 110)

    return sink.finish()


def simplify_clauses(
    clauses: Sequence[tuple[int, ...]], assignment: dict[int, bool]
) -> list[tuple[int, ...]] | None:
    """Unit-propagate a small formula; return None on contradiction."""
    todo = list(clauses)
    while True:
        reduced: list[tuple[int, ...]] = []
        units: list[int] = []
        for clause in todo:
            kept: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    kept.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not kept:
                return None
            if len(kept) == 1:
                units.append(kept[0])
            reduced.append(tuple(kept))
        changed = False
        for literal in units:
            variable, value = abs(literal), literal > 0
            old = assignment.get(variable)
            if old is not None and old != value:
                return None
            if old is None:
                assignment[variable] = value
                changed = True
        todo = reduced
        if not changed:
            return todo


def satisfiable_extension(
    clauses: Sequence[tuple[int, ...]], assignment: dict[int, bool]
) -> bool:
    assignment = dict(assignment)
    reduced = simplify_clauses(clauses, assignment)
    if reduced is None:
        return False
    if not reduced:
        return True
    variable = abs(reduced[0][0])
    for value in (False, True):
        branch = dict(assignment)
        branch[variable] = value
        if satisfiable_extension(reduced, branch):
            return True
    return False


def self_test() -> None:
    # Exhaustively check the existential meaning of the counter auxiliaries
    # on all cardinalities through n=5.
    for n in range(1, 6):
        literals = tuple(range(1, n + 1))
        for k in range(n + 1):
            sink = MemorySink(n + 1)
            sink.exactly(literals, k)
            for mask in range(1 << n):
                fixed = {i + 1: bool(mask & (1 << i)) for i in range(n)}
                actual = satisfiable_extension(sink.clauses, fixed)
                expected = mask.bit_count() == k
                if actual != expected:
                    raise AssertionError((n, k, mask, actual, expected))

    if BASE_VARS != 861:
        raise AssertionError(BASE_VARS)
    print("sequential-counter self-test: PASS (all n<=5 exact cardinalities)")
    print("base graph variables: 861")


def parse_model(path: Path) -> dict[int, bool]:
    status = None
    assignment: dict[int, bool] = {}
    for raw_line in path.read_text(encoding="ascii", errors="strict").splitlines():
        line = raw_line.strip()
        if line.startswith("s "):
            status = line[2:].strip()
        if not line.startswith("v "):
            continue
        for field in line[2:].split():
            literal = int(field)
            if literal:
                assignment[abs(literal)] = literal > 0
    if status != "SATISFIABLE":
        raise ValueError(f"model status is {status!r}, not 'SATISFIABLE'")
    missing = [variable for variable in range(1, BASE_VARS + 1) if variable not in assignment]
    if missing:
        raise ValueError(f"model omits {len(missing)} graph variables; first is {missing[0]}")
    return assignment


def graph6(n: int, red_edges: set[tuple[int, int]]) -> str:
    if not 0 <= n <= 62:
        raise ValueError("this compact graph6 writer supports n<=62")
    bits = [int((i, j) in red_edges) for j in range(1, n) for i in range(j)]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = [63 + n]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(63 + value)
    return "".join(map(chr, payload))


def check_model(path: Path, graph_path: Path | None) -> None:
    assignment = parse_model(path)
    red_edges = {edge for edge, variable in EDGE_VAR.items() if assignment[variable]}
    red_edges.update((vertex, U) for vertex in C)

    def is_red(i: int, j: int) -> bool:
        if i > j:
            i, j = j, i
        return (i, j) in red_edges

    bad: list[tuple[tuple[int, ...], str]] = []
    for vertices in itertools.combinations(range(43), 5):
        count = sum(is_red(i, j) for i, j in itertools.combinations(vertices, 2))
        if count == 10:
            bad.append((vertices, "red"))
        elif count == 0:
            bad.append((vertices, "blue"))
    if bad:
        raise AssertionError(f"model has monochromatic K_5: {bad[0]}")

    degrees = [sum(is_red(v, w) for w in range(43) if w != v) for v in range(43)]
    expected = [21] * 21 + [20] + [21] * 20 + [21]
    if degrees != expected:
        raise AssertionError(f"red degrees {degrees} != {expected}")
    e_c = sum(is_red(i, j) for i, j in itertools.combinations(C, 2))
    e_o = sum(is_red(i, j) for i, j in itertools.combinations(O, 2))
    e_cross = sum(is_red(i, j) for i in C for j in O)
    if (e_c, e_o, e_cross) != (100, 110, 220):
        raise AssertionError((e_c, e_o, e_cross))

    encoded = graph6(43, red_edges)
    if graph_path is not None:
        graph_path.write_text(encoded + "\n", encoding="ascii")
    print("SAT model verification: PASS")
    print("order: 43")
    print("red degree multiset: 20^1 21^42")
    print("homogeneous 5-sets: 0")
    print("partition red edge counts (C,O,C-O): 100 110 220")
    print(f"red graph6: {encoded}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test")
    generate = subparsers.add_parser("generate")
    generate.add_argument("output", type=Path)
    check = subparsers.add_parser("check-model")
    check.add_argument("model", type=Path)
    check.add_argument("--write-graph", type=Path)
    args = parser.parse_args()

    if args.command == "self-test":
        self_test()
    elif args.command == "generate":
        nvars, nclauses = generate_formula(args.output)
        print(f"DIMACS variables: {nvars}")
        print(f"DIMACS clauses: {nclauses}")
        print(f"DIMACS sha256: {sha256(args.output)}")
    else:
        check_model(args.model, args.write_graph)


if __name__ == "__main__":
    main()
