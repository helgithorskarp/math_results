#!/usr/bin/env python3
"""Independent exact audit of the Parts136 reverse receiver.

This checker imports no target module.  It reconstructs the coordinate field
as a tower of quadratic extensions and emits two-bit colour CNFs rather than
the target's one-hot encoding.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from math import factorial
import json
from pathlib import Path


TARGET = "hadwiger_nelson_parts136_reverse_receiver"
SCALE = 96
H = (0,) + tuple(range(374, 509))
D = tuple(range(1, 374))
EXPECTED_BOUNDARY = (
    0, 430, 432, 434, 476, 478, 480, 481, 482, 483,
    484, 485, 486, 487, 488, 489, 490, 491, 492,
)
PERMS0 = tuple((0,) + p for p in permutations((1, 2, 3)))
EXPECTED_INPUT_HASHES = {
    "points.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "fixtures.json": "783a0a4477626b4ab6bd29020bb5bc397a7a3eeef1c10c06b890f13ef066b077",
}
EXPECTED_PATTERN_HASH = "f67f18e35fcd20c46c405c2b7458712091afd12f5fdeaee6443555735fb56649"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def pair_stream_digest(pairs) -> str:
    stream = "".join(f"{a} {b}\n" for a, b in pairs).encode()
    return sha256(stream).hexdigest()


# A field element is nested as Q -> Q(sqrt(3)) -> Q(sqrt(5)) ->
# Q(sqrt(3),sqrt(5),sqrt(11)).  This is deliberately different from the
# target's subset-mask and squarefree-radical multiplication routines.
def add3(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul3(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def scale3(k, x):
    return k * x[0], k * x[1]


def add5(x, y):
    return add3(x[0], y[0]), add3(x[1], y[1])


def mul5(x, y):
    return (
        add3(mul3(x[0], y[0]), scale3(5, mul3(x[1], y[1]))),
        add3(mul3(x[0], y[1]), mul3(x[1], y[0])),
    )


def scale5(k, x):
    return scale3(k, x[0]), scale3(k, x[1])


def add11(x, y):
    return add5(x[0], y[0]), add5(x[1], y[1])


def mul11(x, y):
    return (
        add5(mul5(x[0], y[0]), scale5(11, mul5(x[1], y[1]))),
        add5(mul5(x[0], y[1]), mul5(x[1], y[0])),
    )


def tower(coefficients):
    require(len(coefficients) == 8, "eight coefficients per coordinate")
    a = tuple(coefficients)
    return (((a[0], a[1]), (a[2], a[3])),
            ((a[4], a[5]), (a[6], a[7])))


ZERO = tower((0,) * 8)
UNIT_SQUARED = tower((SCALE * SCALE,) + (0,) * 7)


def squared_distance(p, q):
    dx = tower(tuple(a - b for a, b in zip(p[:8], q[:8])))
    dy = tower(tuple(a - b for a, b in zip(p[8:], q[8:])))
    return add11(mul11(dx, dx), mul11(dy, dy))


def read_points(path: Path):
    lines = path.read_text().splitlines()
    require(lines[0] ==
            "# basis=1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165 scale=96",
            "coordinate header")
    points = [tuple(map(int, line.split())) for line in lines[1:] if line]
    require(len(points) == len(set(points)) == 509, "509 distinct coordinate rows")
    require(all(len(point) == 16 for point in points), "16 coefficients per point")
    return points


def reconstruct(points):
    edges = []
    zero_distances = 0
    for a, b in combinations(range(509), 2):
        d2 = squared_distance(points[a], points[b])
        zero_distances += d2 == ZERO
        if d2 == UNIT_SQUARED:
            edges.append((a, b))
    require(zero_distances == 0, "no distinct pair has zero algebraic distance")
    require(len(edges) == 2442, "complete strict parent unit graph")
    hset, dset = set(H), set(D)
    host_edges = tuple(edge for edge in edges if set(edge) <= hset)
    module_edges = tuple(edge for edge in edges if set(edge) <= dset)
    cross_edges = tuple((a, b) if a in hset else (b, a) for a, b in edges
                        if (a in hset) != (b in hset))
    boundary = tuple(sorted({a for a, _ in cross_edges}))
    require(len(host_edges) == 564, "host edge count")
    require(len(module_edges) == 1836, "removed-module edge count")
    require(len(cross_edges) == 42, "cross-edge count")
    require(boundary == EXPECTED_BOUNDARY, "19-pin physical boundary")
    require(not any(set(edge) <= set(boundary) for edge in host_edges),
            "physical boundary is independent")
    return tuple(edges), host_edges, module_edges, cross_edges, boundary


def proper(word: str, vertices, edges, colours: int):
    require(len(word) == len(vertices), "colour-word length")
    require(all(symbol in "0123456789"[:colours] for symbol in word),
            "colour-word alphabet")
    assignment = dict(zip(vertices, map(int, word)))
    require(all(assignment[a] != assignment[b] for a, b in edges),
            "proper literal colouring")
    return assignment


def canonical(pattern):
    return min(tuple(permutation[colour] for colour in pattern)
               for permutation in PERMS0)


def bit_var(index, bit):
    return 2 * index + bit + 1


def differs_literals(index, colour):
    """Two literals whose disjunction says encoded colour differs from colour."""
    return tuple(bit_var(index, bit) if ((colour >> bit) & 1) == 0
                 else -bit_var(index, bit) for bit in (0, 1))


def literal_value(literal, true_variables):
    return (literal > 0) == (abs(literal) in true_variables)


def verify_binary_semantics():
    for assigned in range(4):
        true_variables = {bit_var(0, bit) for bit in (0, 1)
                          if (assigned >> bit) & 1}
        for forbidden in range(4):
            clause = differs_literals(0, forbidden)
            require(any(literal_value(lit, true_variables) for lit in clause)
                    == (assigned != forbidden), "colour inequality truth table")
    for colour_a in range(4):
        for colour_b in range(4):
            true_variables = {
                bit_var(index, bit)
                for index, colour in enumerate((colour_a, colour_b))
                for bit in (0, 1) if (colour >> bit) & 1
            }
            clauses = [differs_literals(0, colour) + differs_literals(1, colour)
                       for colour in range(4)]
            require(all(any(literal_value(lit, true_variables) for lit in clause)
                        for clause in clauses) == (colour_a != colour_b),
                    "edge encoding truth table")


def binary_cnf(vertices, edges, blocked_boundary_rows=()):
    position = {vertex: index for index, vertex in enumerate(vertices)}
    clauses = []
    for a, b in edges:
        for colour in range(4):
            clauses.append(differs_literals(position[a], colour)
                           + differs_literals(position[b], colour))
    # Global colour symmetry permits vertex 0 to be fixed to binary 00.
    clauses.extend(((-bit_var(position[0], bit),) for bit in (0, 1)))
    for pattern in blocked_boundary_rows:
        for permutation in PERMS0:
            clause = []
            for vertex, colour in zip(EXPECTED_BOUNDARY, pattern):
                if vertex == 0:
                    continue
                clause.extend(differs_literals(position[vertex],
                                               permutation[colour]))
            clauses.append(tuple(clause))
    return tuple(clauses)


def write_dimacs(path: Path, variable_count: int, clauses):
    with path.open("w") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def read_relation(path: Path):
    rows = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split("\t")
        require(len(fields) == 2, f"two-column relation row {number}")
        rows.append(tuple(fields))
    require(len(rows) == len(set(rows)) == 41025, "41025 distinct relation rows")
    return tuple(rows)


def verify(source: Path, output: Path, relation: Path | None = None):
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name, expected in EXPECTED_INPUT_HASHES.items():
        require(digest(source / name) == expected, f"frozen source hash: {name}")
    verify_binary_semantics()
    points = read_points(source / "points.tsv")
    edges, host_edges, module_edges, cross_edges, boundary = reconstruct(points)

    fixtures = json.loads((source / "fixtures.json").read_text())
    five = proper(fixtures["parent_five"], tuple(range(509)), edges, 5)
    require(set(five.values()) == set(range(5)), "parent five-word uses five colours")
    for row in fixtures["host_rows"]:
        pattern = tuple(map(int, row["pattern"]))
        colouring = proper(row["witness"], H, host_edges, 4)
        require(tuple(colouring[v] for v in boundary) == pattern,
                "fixture restriction")
        require(pattern == canonical(pattern), "fixture canonical representative")

    result = {
        "verdict": "accept_with_scope_limitations",
        "exact_field_implementation": "quadratic_tower_Q_sqrt3_sqrt5_sqrt11",
        "exact_pairs_checked": 129286,
        "parent_points": 509,
        "parent_complete_unit_edges": len(edges),
        "host_points": len(H),
        "host_complete_unit_edges": len(host_edges),
        "removed_points": len(D),
        "removed_internal_edges": len(module_edges),
        "cross_edges": len(cross_edges),
        "parent_edge_sha256": pair_stream_digest(edges),
        "host_edge_sha256": pair_stream_digest(host_edges),
        "removed_edge_sha256": pair_stream_digest(module_edges),
        "cross_edge_sha256": pair_stream_digest(cross_edges),
        "boundary": list(boundary),
        "boundary_edges": 0,
        "fixture_rows_checked": len(fixtures["host_rows"]),
        "parent_five_word_checked": True,
        "replacement_new_point_allowance": 372,
        "replacement_supplied": False,
        "record_candidate": False,
        "complete_relation_checked": relation is not None,
        "input_sha256": {name: digest(source / name)
                         for name in EXPECTED_INPUT_HASHES},
    }

    if relation is not None:
        rows = read_relation(relation)
        patterns = []
        for pattern_text, word in rows:
            require(len(pattern_text) == len(boundary), "19-symbol pattern")
            pattern = tuple(map(int, pattern_text))
            require(pattern[0] == 0 and pattern == canonical(pattern),
                    "normalized canonical pattern")
            colouring = proper(word, H, host_edges, 4)
            require(tuple(colouring[v] for v in boundary) == pattern,
                    "full host witness restricts correctly")
            patterns.append(pattern)
        require(len(set(patterns)) == 41025, "41025 unique canonical patterns")
        patterns = tuple(sorted(patterns))
        stream = "".join("".join(map(str, pattern)) + "\n"
                         for pattern in patterns).encode()
        pattern_hash = sha256(stream).hexdigest()
        require(pattern_hash == EXPECTED_PATTERN_HASH, "frozen target pattern set")
        palette = Counter(len(set(pattern)) for pattern in patterns)
        require(palette == Counter({2: 7, 3: 1500, 4: 39518}),
                "boundary palette histogram")
        require((0,) * len(boundary) not in patterns, "monochromatic boundary absent")
        labelled = sum(24 // factorial(4 - len(set(pattern))) for pattern in patterns)
        require(labelled == 984516, "fully labelled pattern count")

        host_binary = binary_cnf(H, host_edges, patterns)
        parent_binary = binary_cnf(tuple(range(509)), edges)
        require(len(host_binary) == 248408, "binary completeness clause count")
        require(len(parent_binary) == 9770, "binary parent clause count")
        write_dimacs(output / "host_completeness_binary.cnf", 2 * len(H), host_binary)
        write_dimacs(output / "parent_binary.cnf", 2 * 509, parent_binary)
        (output / "canonical_patterns.txt").write_bytes(stream)
        result.update({
            "host_words_checked": len(rows),
            "canonical_patterns": len(patterns),
            "labelled_patterns": labelled,
            "boundary_palette_histogram": {str(k): palette[k]
                                           for k in sorted(palette)},
            "canonical_patterns_sha256": pattern_hash,
            "binary_encoding": "two_bits_per_vertex_four_edge_clauses",
            "binary_encoding_truth_tables_checked": True,
            "host_binary_variables": 2 * len(H),
            "host_binary_clauses": len(host_binary),
            "host_binary_cnf_sha256": digest(output / "host_completeness_binary.cnf"),
            "parent_binary_variables": 2 * 509,
            "parent_binary_clauses": len(parent_binary),
            "parent_binary_cnf_sha256": digest(output / "parent_binary.cnf"),
            "negative_proof_checks_still_required": True,
        })

    expected_path = Path(__file__).resolve().parent / "EXPECTED.json"
    if expected_path.exists() and relation is not None:
        require(result == json.loads(expected_path.read_text()),
                "frozen review expectations")
    (output / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=here.parent / TARGET)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--relation", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.source, args.out, args.relation), indent=2))


if __name__ == "__main__":
    main()
