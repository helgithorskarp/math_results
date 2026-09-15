#!/usr/bin/env python3
"""Independent exact review of the Parts373 receiver relation.

This checker does not import the submitted Python modules.  In particular it
reconstructs Q(sqrt(3),sqrt(5),sqrt(11)) as a tower of quadratic extensions
and emits a two-bit-per-colour SAT encoding, rather than the submitted one-hot
encoding.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


TARGET = "hadwiger_nelson_parts373_receiver_relation"
SCALE = 96
H = tuple(v for v in range(374) if v != 310)
D = (310,) + tuple(range(374, 509))
S = tuple(range(374, 509))
N = (150, 169, 287, 296)
EXPECTED_BOUNDARY = (
    0, 150, 169, 243, 244, 245, 287, 296, 344, 345, 346, 357,
    358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368,
)
PERMS0 = tuple((0,) + p for p in permutations((1, 2, 3)))
EXPECTED_INPUT_HASHES = {
    "points.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "host_relation.tsv": "35d8b6d85f5231f7024212688a5c4b3e1731cbefc6696250a9a6e2b27e3e9d0c",
    "small_extensions.tsv": "1af27f98130b1721cfdaf8220c59701f022d4f4a8277ebcd016fe407e9878739",
    "parent_five.txt": "c3db502649705108f62099c90a7f94e8c0a7cc9b5babe7fe7563db37b9bfe636",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


# Elements of Q(sqrt(3),sqrt(5),sqrt(11)) are nested pairs.  A pair (a,b)
# represents a + b*sqrt(d) at the indicated level.  This deliberately avoids
# the submitted subset-mask/radical-gcd multiplication implementations.
def add3(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul3(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def add5(x, y):
    return add3(x[0], y[0]), add3(x[1], y[1])


def scale3(k, x):
    return k * x[0], k * x[1]


def mul5(x, y):
    return (
        add3(mul3(x[0], y[0]), scale3(5, mul3(x[1], y[1]))),
        add3(mul3(x[0], y[1]), mul3(x[1], y[0])),
    )


def add11(x, y):
    return add5(x[0], y[0]), add5(x[1], y[1])


def scale5(k, x):
    return scale3(k, x[0]), scale3(k, x[1])


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
    require(lines[0] == "# basis=1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165 scale=96",
            "coordinate header")
    points = [tuple(map(int, line.split())) for line in lines[1:] if line]
    require(len(points) == 509, "509 coordinate rows")
    require(len(set(points)) == 509, "coordinate rows are distinct")
    require(all(len(p) == 16 for p in points), "16 coefficients per point")
    return points


def reconstruct(points):
    edges = []
    nonzero_zero_distances = 0
    for a, b in combinations(range(len(points)), 2):
        d2 = squared_distance(points[a], points[b])
        if d2 == ZERO:
            nonzero_zero_distances += 1
        if d2 == UNIT_SQUARED:
            edges.append((a, b))
    require(nonzero_zero_distances == 0, "no distinct pair has zero algebraic distance")
    require(len(edges) == 2442, "complete strict unit-edge reconstruction")
    hset, dset = set(H), set(D)
    host_edges = tuple(e for e in edges if set(e) <= hset)
    module_edges = tuple(e for e in edges if set(e) <= dset)
    cross_edges = tuple((a, b) if a in hset else (b, a) for a, b in edges
                        if (a in hset) != (b in hset))
    boundary = tuple(sorted({a for a, _ in cross_edges}))
    require(len(host_edges) == 1856, "host unit-edge count")
    require(len(module_edges) == 552, "module unit-edge count")
    require(len(cross_edges) == 34, "cross-edge count")
    require(boundary == EXPECTED_BOUNDARY, "23-pin boundary")
    return tuple(edges), host_edges, module_edges, cross_edges, boundary


def proper(word: str, vertices, edges, colours: int):
    require(len(word) == len(vertices), "colour-word length")
    require(all(c in "0123456789"[:colours] for c in word), "colour-word alphabet")
    assignment = dict(zip(vertices, map(int, word)))
    require(all(assignment[a] != assignment[b] for a, b in edges),
            "proper colouring witness")
    return assignment


def read_table(path: Path, expected_rows: int):
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split("\t")
        require(len(fields) == 2, f"two-column table at line {line_number}")
        rows.append(tuple(fields))
    require(len(rows) == expected_rows, f"expected {expected_rows} table rows")
    require(len(set(rows)) == expected_rows, "table rows are distinct")
    return tuple(rows)


def canonical(pattern):
    return min(tuple(p[c] for c in pattern) for p in PERMS0)


def bit_var(index, bit):
    return 2 * index + bit + 1


def differs_literals(index, colour):
    """Two literals whose disjunction says encoded colour != colour."""
    return tuple(bit_var(index, bit) if ((colour >> bit) & 1) == 0
                 else -bit_var(index, bit) for bit in (0, 1))


def literal_value(literal, true_variables):
    return (literal > 0) == (abs(literal) in true_variables)


def verify_binary_semantics():
    """Exhaustively validate the local truth tables used by the encoding."""
    for assigned in range(4):
        true_variables = {
            bit_var(0, bit) for bit in (0, 1) if (assigned >> bit) & 1
        }
        for forbidden in range(4):
            clause = differs_literals(0, forbidden)
            require(any(literal_value(lit, true_variables) for lit in clause)
                    == (assigned != forbidden), "colour-inequality truth table")
    for colour_a in range(4):
        for colour_b in range(4):
            true_variables = {
                bit_var(index, bit)
                for index, colour in enumerate((colour_a, colour_b))
                for bit in (0, 1) if (colour >> bit) & 1
            }
            edge_clauses = [
                differs_literals(0, colour) + differs_literals(1, colour)
                for colour in range(4)
            ]
            require(all(any(literal_value(lit, true_variables) for lit in clause)
                        for clause in edge_clauses) == (colour_a != colour_b),
                    "four-clause edge truth table")


def binary_cnf(vertices, edges, blocked_boundary_rows=()):
    position = {v: i for i, v in enumerate(vertices)}
    clauses = []
    for a, b in edges:
        ia, ib = position[a], position[b]
        for colour in range(4):
            clauses.append(differs_literals(ia, colour) + differs_literals(ib, colour))
    # Every colouring orbit has a representative with vertex 0 encoded as 00.
    clauses.extend(((-bit_var(position[0], bit),) for bit in (0, 1)))
    for pattern in blocked_boundary_rows:
        for permutation in PERMS0:
            clause = []
            for vertex, colour in zip(EXPECTED_BOUNDARY, pattern):
                if vertex == 0:
                    continue
                clause.extend(differs_literals(position[vertex], permutation[colour]))
            clauses.append(tuple(clause))
    return tuple(clauses)


def write_dimacs(path: Path, variable_count: int, clauses) -> None:
    with path.open("w") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def verify(source: Path, output: Path):
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name, expected_hash in EXPECTED_INPUT_HASHES.items():
        require(digest(source / name) == expected_hash, f"frozen input hash: {name}")
    verify_binary_semantics()

    points = read_points(source / "points.tsv")
    edges, host_edges, module_edges, cross_edges, boundary = reconstruct(points)
    boundary_set = set(boundary)
    nset = set(N)
    interface = tuple(v for v in boundary if v not in nset)
    boundary_edges = tuple(e for e in host_edges if set(e) <= boundary_set)
    require(boundary_edges == ((0, 150), (0, 169), (150, 169)),
            "boundary is one triangle plus 20 isolates")
    require(tuple(sorted(a for a, b in cross_edges if b == 310)) == N,
            "310 has exactly the four stated host neighbours")
    require(all(310 not in edge for edge in module_edges),
            "310 has no neighbours inside the removed module")
    small_cross = tuple(edge for edge in cross_edges if edge[1] != 310)
    require(tuple(sorted({a for a, _ in small_cross})) == interface,
            "small-side interface equals B minus N")

    extension_rows = read_table(source / "small_extensions.tsv", 424)
    extension = dict(extension_rows)
    require(len(extension) == 424, "unique small-side projection keys")
    for pattern, word in extension_rows:
        require(len(pattern) == len(interface) and set(pattern) <= set("0123"),
                "small-side projection format")
        small_colouring = proper(word, S, module_edges, 4)
        interface_colouring = dict(zip(interface, map(int, pattern)))
        require(all(interface_colouring[a] != small_colouring[b]
                    for a, b in small_cross), "small-side extension contacts")

    relation_rows = read_table(source / "host_relation.tsv", 468)
    patterns = tuple(tuple(map(int, pattern)) for pattern, _ in relation_rows)
    require(len(set(patterns)) == 468, "468 unique boundary patterns")
    palettes = Counter()
    old_projections, new_projections = set(), set()
    full_508_words = 0
    l_edges = tuple(e for e in edges if max(e) < 374)
    parent_minus_310 = tuple(e for e in edges if 310 not in e)
    for (pattern_text, word), pattern in zip(relation_rows, patterns):
        require(len(pattern) == len(boundary), "boundary-pattern length")
        host_colouring = proper(word, H, host_edges, 4)
        require(host_colouring[0] == 0, "origin colour normalized to zero")
        require(tuple(host_colouring[v] for v in boundary) == pattern,
                "host word restricts to listed pattern")
        require(len(set(pattern)) == 4, "listed boundary uses all four colours")
        require(pattern == canonical(pattern), "canonical S3 orbit representative")

        palette_size = len({host_colouring[v] for v in N})
        palettes[palette_size] += 1
        normalizer = min(PERMS0,
                         key=lambda p: tuple(p[host_colouring[v]] for v in interface))
        projection = "".join(str(normalizer[host_colouring[v]]) for v in interface)
        if palette_size == 4:
            new_projections.add(projection)
            require(projection in extension, "rainbow projection has S witness")
            inverse = {normalizer[c]: c for c in range(4)}
            combined = dict(host_colouring)
            combined.update({v: inverse[int(c)]
                             for v, c in zip(S, extension[projection])})
            require(all(combined[a] != combined[b] for a, b in parent_minus_310),
                    "composed proper colouring of all 508 points except 310")
            full_508_words += 1
        else:
            old_projections.add(projection)
            combined = dict(host_colouring)
            omitted = set(range(4)) - {host_colouring[v] for v in N}
            require(omitted, "non-rainbow star omits a colour")
            combined[310] = min(omitted)
            require(all(combined[a] != combined[b] for a, b in l_edges),
                    "non-rainbow host colouring extends over 310")

    require(palettes == Counter({4: 424, 3: 30, 2: 14}), "N-palette partition")
    require(len(old_projections) == 20, "20 old-side projections")
    require(len(new_projections) == 424, "424 rainbow projections")
    require(old_projections.isdisjoint(new_projections), "projection sectors disjoint")
    require(new_projections == set(extension), "extension table covers rainbow sector")
    require(full_508_words == 424, "424 proper G minus 310 colourings")

    five = (source / "parent_five.txt").read_text().strip()
    proper(five, tuple(range(509)), edges, 5)
    require(set(five) == set("01234"), "parent witness uses five colours")

    host_binary = binary_cnf(H, host_edges, patterns)
    parent_binary = binary_cnf(tuple(range(509)), edges)
    require(len(host_binary) == 10234, "binary host clause count")
    require(len(parent_binary) == 9770, "binary parent clause count")
    write_dimacs(output / "host_completeness_binary.cnf", 2 * len(H), host_binary)
    write_dimacs(output / "parent_binary.cnf", 2 * 509, parent_binary)

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
        "boundary": list(boundary),
        "boundary_edges": [list(e) for e in boundary_edges],
        "canonical_host_patterns": len(patterns),
        "labelled_host_patterns": 24 * len(patterns),
        "neighbour_palette_sizes": {str(k): palettes[k] for k in sorted(palettes)},
        "old_interface_patterns": len(old_projections),
        "new_interface_patterns": len(new_projections),
        "small_side_extension_witnesses": len(extension),
        "parent_minus_310_four_words_checked": full_508_words,
        "parent_five_word_checked": True,
        "replacement_new_point_allowance": 135,
        "replacement_supplied": False,
        "record_candidate": False,
        "binary_encoding": "two_bits_per_vertex_four_edge_clauses",
        "binary_encoding_truth_tables_checked": True,
        "host_binary_variables": 2 * len(H),
        "host_binary_clauses": len(host_binary),
        "parent_binary_variables": 2 * 509,
        "parent_binary_clauses": len(parent_binary),
        "host_binary_cnf_sha256": digest(output / "host_completeness_binary.cnf"),
        "parent_binary_cnf_sha256": digest(output / "parent_binary.cnf"),
        "input_sha256": {name: digest(source / name) for name in EXPECTED_INPUT_HASHES},
    }
    expected_path = Path(__file__).resolve().parent / "EXPECTED.json"
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()), "frozen review expectations")
    (output / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=here.parent / TARGET)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.source, args.out), indent=2))


if __name__ == "__main__":
    main()
