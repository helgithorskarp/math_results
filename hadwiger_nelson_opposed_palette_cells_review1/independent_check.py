#!/usr/bin/env python3
"""Clean-room audit of the opposed-palette-cell unit-distance gadget.

The checker imports no code from the target contribution.  It derives the
coordinates from the displayed geometric formulas in a multiquadratic field,
reconstructs the complete strict unit graph, and uses a generic domain-based
graph-colouring search on every named four-colour terminal assignment.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_TARGET = HERE.parent / "hadwiger_nelson_opposed_palette_cells"
PRIMES = (3, 5, 7)
RADICAL_ORDER = (0, 1, 2, 4, 3, 5, 6, 7)
TERMINALS = (5, 6, 7, 8, 12, 13, 14, 15)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# An element of Q(sqrt(3),sqrt(5),sqrt(7)) is an eight-entry tuple indexed by
# the squarefree-prime mask.  This quotient-polynomial implementation is
# independent of the target's integer prime-mask and sparse-radicand routines.
def atom(mask=0, coefficient=0):
    row = [Q(0)] * 8
    row[mask] = Q(coefficient)
    return tuple(row)


ZERO = atom()
ONE = atom(0, 1)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-x for x in value)


def scale(value, scalar):
    scalar = Q(scalar)
    return tuple(scalar * x for x in value)


def multiply(left, right):
    answer = [Q(0)] * 8
    for a, x in enumerate(left):
        if not x:
            continue
        for b, y in enumerate(right):
            if not y:
                continue
            shared = a & b
            factor = 1
            for bit, prime in enumerate(PRIMES):
                if shared & (1 << bit):
                    factor *= prime
            answer[a ^ b] += factor * x * y
    return tuple(answer)


def point_add(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def point_neg(value):
    return neg(value[0]), neg(value[1])


def point_sub(left, right):
    return point_add(left, point_neg(right))


def point_scale(value, scalar):
    return scale(value[0], scalar), scale(value[1], scalar)


def rotate_i_sqrt3(value):
    root3 = atom(1, 1)
    return neg(multiply(root3, value[1])), multiply(root3, value[0])


def squared_norm(value):
    return add(multiply(value[0], value[0]), multiply(value[1], value[1]))


def apex(first, second, sign):
    rotated = point_scale(rotate_i_sqrt3(point_sub(second, first)), sign)
    return point_scale(point_add(point_add(first, second), rotated), Q(1, 2))


def construct_points():
    a = (atom(0, Q(-1, 2)), ZERO)
    b = (atom(0, Q(1, 2)), ZERO)
    d = (atom(0, Q(3, 4)), atom(3, Q(1, 4)))
    c = (ZERO, add(atom(3, Q(1, 4)), atom(4, Q(1, 4))))
    e = (atom(0, Q(-3, 4)), atom(3, Q(1, 4)))
    cell = [a, b, d, c, e]
    cell.extend((apex(d, c, 1), apex(d, c, -1),
                 apex(e, a, 1), apex(e, a, -1)))
    points = list(cell)
    for point in cell:
        opposite = point_neg(point)
        if opposite not in points:
            points.append(opposite)
    return points


def exact_graph(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if squared_norm(point_sub(points[a], points[b])) == ONE]


def normalize(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def canonical_patterns(length):
    return sorted({normalize(word) for word in product(range(4), repeat=length)})


def make_solver(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def solve(pins=(), colour_count=4):
        full = (1 << colour_count) - 1
        domains = [full] * vertex_count
        queue = []
        for vertex, colour in pins:
            require(0 <= colour < colour_count, "pin colour outside domain")
            wanted = 1 << colour
            domains[vertex] &= wanted
            if not domains[vertex]:
                return None
            queue.append(vertex)

        def propagate(state, initial):
            state = list(state)
            pending = list(initial)
            seen = set()
            while pending:
                vertex = pending.pop()
                domain = state[vertex]
                if domain == 0:
                    return None
                if domain & (domain - 1):
                    continue
                marker = (vertex, domain)
                if marker in seen:
                    continue
                seen.add(marker)
                for neighbour in adjacency[vertex]:
                    reduced = state[neighbour] & ~domain
                    if reduced != state[neighbour]:
                        if reduced == 0:
                            return None
                        state[neighbour] = reduced
                        if not reduced & (reduced - 1):
                            pending.append(neighbour)
            return tuple(state)

        def search(state):
            state = propagate(state, range(vertex_count))
            if state is None:
                return None
            undecided = [v for v, domain in enumerate(state)
                         if domain & (domain - 1)]
            if not undecided:
                return tuple(domain.bit_length() - 1 for domain in state)
            vertex = min(
                undecided,
                key=lambda v: (state[v].bit_count(), -len(adjacency[v]), v),
            )
            choices = state[vertex]
            for colour in range(colour_count):
                bit = 1 << colour
                if choices & bit:
                    child = list(state)
                    child[vertex] = bit
                    answer = search(tuple(child))
                    if answer is not None:
                        return answer
            return None

        state = propagate(tuple(domains), queue)
        return None if state is None else search(state)

    return solve


def compact_hash(value):
    payload = json.dumps(value, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def fixture_rows(points):
    rows = []
    for x, y in points:
        row = []
        for coordinate in (x, y):
            for mask in RADICAL_ORDER:
                value = 8 * coordinate[mask]
                require(value.denominator == 1, "coordinate denominator exceeds 8")
                row.append(value.numerator)
        rows.append(row)
    return rows


def parse_target_points(path):
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        entries = [int(x) for x in line.split()]
        require(entries[0] == len(rows), "noncanonical target point labels")
        rows.append(entries[1:])
    return rows


def check_certificate(certificate, edges, feasibility):
    positive = certificate["positive"]
    negative = certificate["negative"]
    target_yes = {tuple(int(c) for c in pattern): word
                  for pattern, word in positive}
    target_no = {tuple(int(c) for c in pattern) for pattern in negative}
    require(len(target_yes) == len(positive), "duplicate target positives")
    require(len(target_no) == len(negative), "duplicate target negatives")
    require(set(feasibility) == target_yes.keys() | target_no,
            "target certificate omits a canonical pattern")
    require({word for word, feasible in feasibility.items() if feasible}
            == target_yes.keys(), "target positive relation differs")
    for pattern, word in target_yes.items():
        require(len(word) == 16 and set(word) <= set("0123"),
                "malformed target witness")
        colouring = tuple(int(c) for c in word)
        require(all(colouring[a] != colouring[b] for a, b in edges),
                "improper target positive witness")
        require(tuple(colouring[v] for v in TERMINALS) == pattern,
                "target witness does not realize its pins")
    return compact_hash(sorted("".join(map(str, word)) for word in target_no))


def audit(target_dir):
    points = construct_points()
    require(len(points) == 16 and len(set(points)) == 16,
            "the construction does not have 16 distinct points")
    rows = fixture_rows(points)
    target_rows = parse_target_points(target_dir / "points.tsv")
    require(rows == target_rows, "independent formulas disagree with points.tsv")

    edges = exact_graph(points)
    require(len(edges) == 25, "strict physical graph does not have 25 edges")
    edge_set = set(edges)
    require(not any(a in TERMINALS and b in TERMINALS for a, b in edges),
            "the eight terminals are not independent")
    for a, b in zip(TERMINALS[::2], TERMINALS[1::2]):
        require(squared_norm(point_sub(points[a], points[b])) == atom(0, 3),
                "designated terminal pair is not at distance sqrt(3)")

    solve = make_solver(16, edges)
    two_colouring = solve(colour_count=2)
    three_colouring = solve(colour_count=3)
    require(two_colouring is None and three_colouring is not None,
            "chromatic number is not exactly three")

    # This deliberately solves all named assignments, not only one word from
    # each colour-permutation orbit.
    named_yes = set()
    named_witness = {}
    for word in product(range(4), repeat=8):
        witness = solve(zip(TERMINALS, word))
        if witness is not None:
            named_yes.add(word)
            named_witness[word] = witness

    canonical = canonical_patterns(8)
    feasibility = {
        word: (word in named_yes)
        for word in canonical
    }
    require(all((word in named_yes) == (normalize(word) in named_yes)
                for word in product(range(4), repeat=8)),
            "named feasibility is not invariant under normalization")
    allowed = sum(feasibility.values())
    forbidden = len(feasibility) - allowed

    projection_summary = {}
    seven_projection = {}
    for size in range(1, 8):
        all_patterns = set(canonical_patterns(size))
        nonneutral = 0
        for subset in combinations(range(8), size):
            seen = {normalize(word[i] for i in subset) for word in named_yes}
            missing = all_patterns - seen
            if missing:
                nonneutral += 1
            if size == 7:
                seven_projection[subset] = missing
        projection_summary[str(size)] = {
            "subsets": len(list(combinations(range(8), size))),
            "nonneutral": nonneutral,
        }

    essential = []
    for word, feasible in feasibility.items():
        if feasible:
            continue
        if all(normalize(word[i] for i in subset) not in missing
               for subset, missing in seven_projection.items()):
            essential.append(word)

    # Stronger than the target's 36 canonical checks: test both orientations
    # of every one of the four terminal pairs for each ordered palette pair.
    palette_checks = 0
    palettes = list(combinations(range(4), 2))
    for p, q in product(palettes, repeat=2):
        for flips in product(range(2), repeat=4):
            pairs = [p, q, p, q]
            word = tuple(
                colour
                for pair, flip in zip(pairs, flips)
                for colour in (pair if not flip else pair[::-1])
            )
            require((word in named_yes) == set(p).isdisjoint(q),
                    "complementary-palette criterion fails")
            palette_checks += 1

    # Restrict the independently reconstructed graph to the first cell and
    # check its complete four-terminal orbit domain with the same generic
    # solver, without using the target's path relation.
    first_vertices = tuple(range(9))
    first_edges = [(a, b) for a, b in edges
                   if a in first_vertices and b in first_vertices]
    require(len(first_edges) == 13, "first cell does not have 13 edges")
    solve_cell = make_solver(9, first_edges)
    cell_patterns = canonical_patterns(4)
    require(all(solve_cell(zip(range(5, 9), word)) is not None
                for word in cell_patterns), "a single-cell pattern is missing")

    certificate = json.loads((target_dir / "certificate.json").read_text())
    negative_hash = check_certificate(certificate, edges, feasibility)

    example = tuple(map(int, certificate["irreducible_example"]))
    require(example in essential, "stated irreducible example is not essential")
    for dropped in range(8):
        pins = [(TERMINALS[i], example[i]) for i in range(8) if i != dropped]
        require(solve(pins) is not None, "stated example has a bad seven-pin restriction")

    degree_sequence = sorted(Counter(v for edge in edges for v in edge).values())
    result = {
        "status": "INDEPENDENT_AUDIT_PASSED",
        "points": len(points),
        "strict_unit_edges": len(edges),
        "all_physical_pair_checks": len(points) * (len(points) - 1) // 2,
        "degree_sequence": degree_sequence,
        "terminals_independent": True,
        "sqrt3_terminal_pairs": 4,
        "chromatic_number": 3,
        "named_terminal_assignments_solved": 4 ** 8,
        "named_allowed_assignments": len(named_yes),
        "canonical_terminal_patterns": len(canonical),
        "canonical_allowed": allowed,
        "canonical_forbidden": forbidden,
        "essential_eight_terminal_forbidden": len(essential),
        "projection_summary": projection_summary,
        "single_cell_patterns_checked": len(cell_patterns),
        "all_oriented_palette_checks": palette_checks,
        "point_sha256": compact_hash(rows),
        "edge_sha256": compact_hash(edges),
        "negative_sha256": negative_hash,
        "essential_sha256": compact_hash(
            sorted("".join(map(str, word)) for word in essential)
        ),
        "three_colouring": "".join(map(str, three_colouring)),
        "target_positive_witnesses_checked": len(certificate["positive"]),
        "target_positive_edge_checks": len(certificate["positive"]) * len(edges),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.target_dir.resolve())
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
