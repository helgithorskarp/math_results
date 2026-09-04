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

    def define_gate(self, inputs: Sequence[int], predicate) -> int:
        """Return a fresh variable equivalent to predicate(inputs)."""
        output = self.fresh()
        for values in itertools.product((False, True), repeat=len(inputs)):
            correct = bool(predicate(values))
            # Forbid precisely the input assignment together with the wrong
            # output value.  Inputs may themselves be signed literals.
            clause = [
                -literal if value else literal
                for literal, value in zip(inputs, values, strict=True)
            ]
            wrong = not correct
            clause.append(-output if wrong else output)
            self.add(clause)
        return output

    def add_binary_vectors(
        self, left: Sequence[int], right: Sequence[int]
    ) -> tuple[int, ...]:
        """CNF circuit for two little-endian unsigned binary vectors."""
        answer: list[int] = []
        carry: int | None = None
        for position in range(max(len(left), len(right))):
            terms = []
            if position < len(left):
                terms.append(left[position])
            if position < len(right):
                terms.append(right[position])
            if carry is not None:
                terms.append(carry)
            if len(terms) == 1:
                answer.append(terms[0])
                carry = None
            elif len(terms) == 2:
                answer.append(
                    self.define_gate(terms, lambda values: sum(values) % 2 == 1)
                )
                carry = self.define_gate(terms, lambda values: sum(values) >= 2)
            elif len(terms) == 3:
                answer.append(
                    self.define_gate(terms, lambda values: sum(values) % 2 == 1)
                )
                carry = self.define_gate(terms, lambda values: sum(values) >= 2)
            else:
                raise AssertionError(terms)
        if carry is not None:
            answer.append(carry)
        return tuple(answer)

    def binary_sum(self, literals: Sequence[int]) -> tuple[int, ...]:
        """Build an exact balanced-adder circuit for a population count."""
        if not literals:
            return ()
        level = [(literal,) for literal in literals]
        while len(level) > 1:
            following = []
            for start in range(0, len(level) - 1, 2):
                following.append(
                    self.add_binary_vectors(level[start], level[start + 1])
                )
            if len(level) % 2:
                following.append(level[-1])
            level = following
        return level[0]

    def exactly_binary(self, literals: Sequence[int], k: int) -> None:
        """Exact cardinality via a balanced binary population-count circuit."""
        if not 0 <= k <= len(literals):
            self.add(())
            return
        bits = self.binary_sum(literals)
        for position, bit in enumerate(bits):
            self.add((bit if (k >> position) & 1 else -bit,))

    def conditional_binary_values(
        self,
        literals: Sequence[int],
        selector: int,
        when_true: int,
        when_false: int,
    ) -> None:
        """Fix a population count to one of two values selected by a literal."""
        if not (0 <= when_true <= len(literals) and 0 <= when_false <= len(literals)):
            self.add(())
            return
        bits = self.binary_sum(literals)
        for position, bit in enumerate(bits):
            true_literal = bit if (when_true >> position) & 1 else -bit
            false_literal = bit if (when_false >> position) & 1 else -bit
            self.add((-selector, true_literal))
            self.add((selector, false_literal))


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


def add_local_profile_constraints(
    sink: ClauseSink, red_exceptional_count: int | None = None
) -> None:
    """Encode every forced singleton local count except the 20 color choices."""
    triangle_variables: dict[tuple[int, int, int], tuple[int, int]] = {}
    for vertices in itertools.combinations(range(N_F), 3):
        edges = tuple(
            edge_var(i, j) for i, j in itertools.combinations(vertices, 2)
        )
        red = sink.fresh()
        for edge in edges:
            sink.add((-red, edge))
        sink.add((red, *(-edge for edge in edges)))
        blue = sink.fresh()
        for edge in edges:
            sink.add((-blue, -edge))
        sink.add((blue, *edges))
        triangle_variables[vertices] = (red, blue)

    def incident(vertex: int, color: int) -> list[int]:
        others = tuple(v for v in range(N_F) if v != vertex)
        return [
            triangle_variables[tuple(sorted((vertex, first, second)))][color]
            for first, second in itertools.combinations(others, 2)
        ]

    # Every c in C is doubly exact.  Red triangles through u correspond to
    # red H-edges incident with c; no blue triangle through u contains c.
    for vertex in C:
        red_local = incident(vertex, 0)
        red_local.extend(
            edge_var(vertex, other) for other in C if other != vertex
        )
        sink.exactly_binary(red_local, 100)
        sink.exactly_binary(incident(vertex, 1), 100)

    # The exceptional degree-20 vertex z remains at the deficiency-seven
    # baseline.  Its blue triangles through u correspond to blue O-edges.
    sink.exactly_binary(incident(Z, 0), 93)
    blue_z = incident(Z, 1)
    blue_z.extend(-edge_var(Z, other) for other in O if other != Z)
    sink.exactly_binary(blue_z, 107)

    # Each other O vertex spends exactly one of the twenty excess units.  In
    # the untyped formula we impose only that its two counts sum to 199.  A
    # typed branch instead selects (99,100) or (100,99) and fixes the number
    # of vertices of the first type.  Blue triangles through u are precisely
    # the blue incident O-edges.
    type_selectors = []
    for vertex in O:
        if vertex == Z:
            continue
        red_local = incident(vertex, 0)
        blue_local = incident(vertex, 1)
        blue_local.extend(
            -edge_var(vertex, other) for other in O if other != vertex
        )
        if red_exceptional_count is None:
            sink.exactly_binary(red_local + blue_local, 199)
        else:
            selector = sink.fresh()
            type_selectors.append(selector)
            sink.conditional_binary_values(red_local, selector, 99, 100)
            sink.conditional_binary_values(blue_local, selector, 100, 99)
    if red_exceptional_count is not None:
        sink.exactly_binary(type_selectors, red_exceptional_count)


def add_stabilizer_symmetry_break(sink: ClauseSink) -> None:
    """Choose canonical prefixes in the C and O-minus-z stabilizer chain."""
    # In the blue core K on O, every degree lies in [3,13]: the lower bound
    # follows from R(4,4)=18 on a vertex's nonneighbors, and the upper bound
    # from R(3,5)=14 on its neighbors.  Since z's red cross degree equals its
    # blue degree in K, relabel C so those red neighbors form a prefix.
    z_cross = tuple(edge_var(vertex, Z) for vertex in C)
    for first, second in zip(z_cross, z_cross[1:]):
        sink.add((first, -second))
    for literal in z_cross[:3]:
        sink.add((literal,))
    for literal in z_cross[13:]:
        sink.add((-literal,))

    # The chosen vertex c0 is therefore red-adjacent to z.  Its H-degree is
    # also in [3,13], so it has 6,...,16 red neighbors among the twenty
    # nondistinguished O vertices.  Relabel those vertices to form a prefix.
    normal_o = tuple(vertex for vertex in O if vertex != Z)
    c0_cross = tuple(edge_var(C[0], vertex) for vertex in normal_o)
    for first, second in zip(c0_cross, c0_cross[1:]):
        sink.add((first, -second))
    for literal in c0_cross[:6]:
        sink.add((literal,))
    for literal in c0_cross[16:]:
        sink.add((-literal,))


def generate_formula(
    path: Path,
    local_profile: bool = False,
    red_exceptional_count: int | None = None,
    stabilizer_break: bool = False,
) -> tuple[int, int]:
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

    if local_profile:
        add_local_profile_constraints(sink, red_exceptional_count)
    if stabilizer_break:
        add_stabilizer_symmetry_break(sink)

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

    # Independently exercise the balanced-adder exact-cardinality circuit.
    for n in range(1, 7):
        literal_sets = [
            tuple(range(1, n + 1)),
            tuple(
                variable if variable % 2 else -variable
                for variable in range(1, n + 1)
            ),
        ]
        for literals in literal_sets:
            for k in range(n + 1):
                sink = MemorySink(n + 1)
                sink.exactly_binary(literals, k)
                for mask in range(1 << n):
                    fixed = {i + 1: bool(mask & (1 << i)) for i in range(n)}
                    actual = satisfiable_extension(sink.clauses, fixed)
                    truth_count = sum(
                        fixed[abs(literal)] == (literal > 0) for literal in literals
                    )
                    expected = truth_count == k
                    if actual != expected:
                        raise AssertionError(
                            ("binary", n, k, literals, mask, actual, expected)
                        )

        # Also check both implications of the selector-controlled variant,
        # including signed inputs.
        literals = literal_sets[1]
        selector = n + 1
        when_true, when_false = n // 3, (2 * n) // 3
        sink = MemorySink(n + 2)
        sink.conditional_binary_values(
            literals, selector, when_true, when_false
        )
        for selector_value in (False, True):
            target = when_true if selector_value else when_false
            for mask in range(1 << n):
                fixed = {i + 1: bool(mask & (1 << i)) for i in range(n)}
                fixed[selector] = selector_value
                actual = satisfiable_extension(sink.clauses, fixed)
                truth_count = sum(
                    fixed[abs(literal)] == (literal > 0) for literal in literals
                )
                expected = truth_count == target
                if actual != expected:
                    raise AssertionError(
                        ("conditional", n, mask, selector_value, actual, expected)
                    )

    # Check the symmetry-breaking clauses directly on every pair of prefix
    # lengths.  Also reject a same-weight nonprefix assignment in each block,
    # which detects a reversed or omitted monotonic implication.
    sink = MemorySink(BASE_VARS + 1)
    add_stabilizer_symmetry_break(sink)
    z_cross = tuple(edge_var(vertex, Z) for vertex in C)
    c0_cross = tuple(edge_var(C[0], vertex) for vertex in O if vertex != Z)

    def prefix_assignment(length_z: int, length_c0: int) -> dict[int, bool]:
        assignment = {
            variable: index < length_z
            for index, variable in enumerate(z_cross)
        }
        assignment.update(
            {
                variable: index < length_c0
                for index, variable in enumerate(c0_cross)
            }
        )
        return assignment

    def clauses_hold(assignment: dict[int, bool]) -> bool:
        return all(
            any(assignment[abs(literal)] == (literal > 0) for literal in clause)
            for clause in sink.clauses
        )

    if sink.nclauses != 60:
        raise AssertionError(("stabilizer clauses", sink.nclauses))
    for length_z in range(len(z_cross) + 1):
        for length_c0 in range(len(c0_cross) + 1):
            actual = clauses_hold(prefix_assignment(length_z, length_c0))
            expected = 3 <= length_z <= 13 and 6 <= length_c0 <= 16
            if actual != expected:
                raise AssertionError(
                    ("stabilizer prefixes", length_z, length_c0, actual, expected)
                )

    for block, swap_at in ((z_cross, 4), (c0_cross, 7)):
        assignment = prefix_assignment(5, 8)
        assignment[block[swap_at]] = False
        assignment[block[swap_at + 1]] = True
        if clauses_hold(assignment):
            raise AssertionError(("stabilizer nonprefix", block, swap_at))

    if BASE_VARS != 861:
        raise AssertionError(BASE_VARS)
    print("sequential-counter self-test: PASS (all n<=5 exact cardinalities)")
    print("binary-adder self-test: PASS (all n<=6 exact cardinalities)")
    print("stabilizer self-test: PASS (all prefix-length pairs)")
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


def check_model(
    path: Path, graph_path: Path | None, require_local_profile: bool = False
) -> None:
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

    local_pairs = []
    for vertex in range(43):
        red_local = blue_local = 0
        others = tuple(v for v in range(43) if v != vertex)
        for first, second in itertools.combinations(others, 2):
            colors = (
                is_red(vertex, first),
                is_red(vertex, second),
                is_red(first, second),
            )
            if all(colors):
                red_local += 1
            elif not any(colors):
                blue_local += 1
        local_pairs.append((red_local, blue_local))
    exact_side = all(local_pairs[vertex] == (100, 100) for vertex in (*C, U))
    z_exact = local_pairs[Z] == (93, 107)
    o_profiles = [local_pairs[vertex] for vertex in O if vertex != Z]
    outside_exact = all(pair in {(99, 100), (100, 99)} for pair in o_profiles)
    has_local_profile = exact_side and z_exact and outside_exact
    if require_local_profile and not has_local_profile:
        raise AssertionError(
            f"model violates forced singleton local profile: {local_pairs}"
        )

    red_exceptional = o_profiles.count((99, 100))
    red_triangles = sum(pair[0] for pair in local_pairs) // 3
    blue_triangles = sum(pair[1] for pair in local_pairs) // 3

    encoded = graph6(43, red_edges)
    if graph_path is not None:
        graph_path.write_text(encoded + "\n", encoding="ascii")
    print("SAT model verification: PASS")
    print("order: 43")
    print("red degree multiset: 20^1 21^42")
    print("homogeneous 5-sets: 0")
    print("partition red edge counts (C,O,C-O): 100 110 220")
    if has_local_profile:
        print(
            "singleton local profile: PASS "
            f"(x={red_exceptional}, triangles={red_triangles},{blue_triangles})"
        )
    else:
        print("singleton local profile: outside the local-profile strengthening")
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
    generate.add_argument(
        "--local-profile",
        action="store_true",
        help="also encode all forced blue-singleton local triangle counts",
    )
    generate.add_argument(
        "--red-exceptional",
        type=int,
        choices=tuple(range(0, 19, 3)),
        help="typed local branch: number of O vertices with (t_R,t_B)=(99,100)",
    )
    generate.add_argument(
        "--stabilizer-break",
        action="store_true",
        help="canonically order two cross-neighborhoods using core degree bounds",
    )
    check = subparsers.add_parser("check-model")
    check.add_argument("model", type=Path)
    check.add_argument("--write-graph", type=Path)
    check.add_argument("--require-local-profile", action="store_true")
    args = parser.parse_args()

    if args.command == "self-test":
        self_test()
    elif args.command == "generate":
        if args.red_exceptional is not None and not args.local_profile:
            parser.error("--red-exceptional requires --local-profile")
        nvars, nclauses = generate_formula(
            args.output,
            args.local_profile,
            args.red_exceptional,
            args.stabilizer_break,
        )
        print(f"DIMACS variables: {nvars}")
        print(f"DIMACS clauses: {nclauses}")
        print(f"DIMACS sha256: {sha256(args.output)}")
    else:
        check_model(args.model, args.write_graph, args.require_local_profile)


if __name__ == "__main__":
    main()
