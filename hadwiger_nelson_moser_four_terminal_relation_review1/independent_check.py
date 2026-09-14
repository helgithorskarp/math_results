#!/usr/bin/env python3
"""Independent exact audit of the eleven-point Moser terminal relation.

This program deliberately imports no code from the reviewed package.  Geometry is
constructed from radicals in SymPy's exact algebraic number field, while colourings
are enumerated as restricted-growth strings (set partitions), not as labelled
interior assignments or supplied witnesses.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path

import sympy as sp


LABELS = ("0", "1", "2", "3", "4", "5", "6", "A", "B", "C", "D")
TERMINALS = (7, 8, 9, 10)
ROWS = (
    (0, 0, 0, 0),
    (12, 0, 0, 0),
    (6, 0, 6, 0),
    (18, 0, 6, 0),
    (10, 0, 0, 2),
    (5, -1, 5, 1),
    (15, -1, 5, 3),
    (6, 0, -6, 0),
    (12, 0, 12, 0),
    (20, 0, 0, 4),
    (-5, -1, 5, -1),
)
EXPECTED_EDGES = (
    (0, 1), (0, 2), (0, 4), (0, 5), (0, 7), (0, 10),
    (1, 2), (1, 3), (1, 7), (2, 3), (2, 8), (3, 6), (3, 8),
    (4, 5), (4, 6), (4, 9), (5, 6), (5, 10), (6, 9),
)
FORBIDDEN = {(0, 0, 0, 0), (0, 0, 1, 1)}


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    raw = json.dumps(value, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def restricted_growth_strings(length, max_colours):
    """Generate canonical set partitions using at most max_colours blocks."""
    need(length >= 1 and max_colours >= 1, "positive RGS dimensions")
    word = [0] * length

    def visit(position, largest):
        if position == length:
            yield tuple(word)
            return
        upper = min(largest + 1, max_colours - 1)
        for colour in range(upper + 1):
            word[position] = colour
            yield from visit(position + 1, max(largest, colour))

    yield from visit(1, 0)


def canonical(word):
    names = {}
    return tuple(names.setdefault(colour, len(names)) for colour in word)


def proper_partitions(vertices, edges, max_colours):
    positions = {vertex: position for position, vertex in enumerate(vertices)}
    local_edges = [
        (positions[a], positions[b])
        for a, b in edges
        if a in positions and b in positions
    ]
    for word in restricted_growth_strings(len(vertices), max_colours):
        if all(word[a] != word[b] for a, b in local_edges):
            yield word


def check_named_word(word, edges, removed=None):
    if isinstance(word, str):
        need(len(word) == 11 and set(word) <= set("0123"), "named word syntax")
        word = tuple(map(int, word))
    else:
        word = tuple(word)
    need(len(word) == 11, "named word length")
    for vertex, colour in enumerate(word):
        if vertex == removed:
            need(colour == -1, "deleted vertex marker")
        else:
            need(type(colour) is int and 0 <= colour < 4, "named colour range")
    need(
        all(
            word[a] != word[b]
            for a, b in edges
            if a != removed and b != removed
        ),
        "improper supplied word",
    )
    return tuple(word[v] for v in TERMINALS)


def exact_geometry():
    # AlgebraicField provides exact arithmetic in Q(sqrt(3),sqrt(11)).
    field = sp.QQ.algebraic_field(sp.sqrt(3), sp.sqrt(11))
    q = lambda value: field.from_sympy(sp.sympify(value))
    zero, one = q(0), q(1)
    sqrt3, sqrt11, sqrt33 = map(q, (sp.sqrt(3), sp.sqrt(11), sp.sqrt(33)))

    def add(z, w):
        return z[0] + w[0], z[1] + w[1]

    def sub(z, w):
        return z[0] - w[0], z[1] - w[1]

    def mul(z, w):
        return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]

    def scale(z, amount):
        amount = q(amount)
        return z[0] * amount, z[1] * amount

    def conjugate(z):
        return z[0], -z[1]

    def squared_distance(z, w):
        difference = sub(z, w)
        return difference[0] ** 2 + difference[1] ** 2

    z0, z1 = (zero, zero), (one, zero)
    rho = (q(sp.Rational(1, 2)), sqrt3 / q(2))
    t = (q(sp.Rational(5, 6)), sqrt11 / q(6))
    points = (
        z0,
        z1,
        rho,
        add(z1, rho),
        t,
        mul(t, rho),
        mul(t, add(z1, rho)),
        conjugate(rho),
        scale(rho, 2),
        scale(t, 2),
        mul(t, sub(rho, z1)),
    )

    row_points = tuple(
        (
            (q(a) + q(b) * sqrt33) / q(12),
            (q(c) * sqrt3 + q(d) * sqrt11) / q(12),
        )
        for a, b, c, d in ROWS
    )
    need(points == row_points, "radical formulas do not equal displayed coordinate rows")
    need(len(set(points)) == 11, "physical point collision")

    edges = []
    exact_distances = []
    compatibility_distances = []
    for a, b in combinations(range(11), 2):
        d2 = squared_distance(points[a], points[b])
        exact_distances.append(d2)
        if d2 == one:
            edges.append((a, b))
        da, db, dc, dd = (ROWS[a][j] - ROWS[b][j] for j in range(4))
        rational_part = da * da + 33 * db * db + 3 * dc * dc + 11 * dd * dd
        radical_part = 2 * (da * db + dc * dd)
        compatibility_distances.append((a, b, rational_part, radical_part))
        reconstructed = (q(rational_part) + q(radical_part) * sqrt33) / q(144)
        need(d2 == reconstructed, "row norm and direct radical norm disagree")

    need(tuple(edges) == EXPECTED_EDGES, "complete unit-edge census")
    left_diamond = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)}
    right_diamond = {(0, 4), (0, 5), (4, 5), (4, 6), (5, 6)}
    interior = {(a, b) for a, b in edges if b < 7}
    caps = {(a, b) for a, b in edges if b >= 7}
    need(interior == left_diamond | right_diamond | {(3, 6)},
         "two-diamond interior structure")
    need(caps == {(0, 7), (1, 7), (2, 8), (3, 8),
                  (4, 9), (6, 9), (0, 10), (5, 10)},
         "terminal cap structure")
    need(not any(a in TERMINALS and b in TERMINALS for a, b in edges),
         "terminals are not independent")
    need(squared_distance(points[7], points[8]) == q(7), "AB squared length")
    need(squared_distance(points[9], points[10]) == q(7), "CD squared length")

    failed_points = list(points)
    failed_points[9] = mul(t, add(scale(z1, 2), rho))
    failed_edges = tuple(
        (a, b)
        for a, b in combinations(range(11), 2)
        if squared_distance(failed_points[a], failed_points[b]) == one
    )
    need(len(set(failed_points)) == 11, "failed-formula point collision")
    need(len(failed_edges) == 18 and (4, 9) not in failed_edges,
         "failed-formula edge census")

    return {
        "edges": tuple(edges),
        "failed_edges": failed_edges,
        "compatibility_distances": compatibility_distances,
        "point_sha256": digest(ROWS),
        "distance_sha256": digest(compatibility_distances),
        "edge_sha256": digest(edges),
    }


def audit_colourings(edges, failed_edges):
    all_terminal_patterns = set(restricted_growth_strings(4, 4))
    need(len(all_terminal_patterns) == 15, "Bell number B4")

    three_colour_count = sum(
        1 for _ in proper_partitions(tuple(range(11)), edges, 3)
    )
    need(three_colour_count == 0, "unexpected three-colouring")

    canonical_full = list(proper_partitions(tuple(range(11)), edges, 4))
    need(canonical_full and all(max(word) == 3 for word in canonical_full),
         "four-colour existence and exact chromatic number")

    relation_counter = Counter()
    canonical_relation = set()
    same, different = set(), set()
    for word in canonical_full:
        canonical_relation.add(canonical(tuple(word[v] for v in TERMINALS)))
        for a, b in combinations(range(11), 2):
            (same if word[a] == word[b] else different).add((a, b))
        for colour_permutation in permutations(range(4)):
            pins = tuple(colour_permutation[word[v]] for v in TERMINALS)
            relation_counter[pins] += 1

    expected_relation = all_terminal_patterns - FORBIDDEN
    need(canonical_relation == expected_relation, "canonical terminal relation")
    named_relation = set(relation_counter)
    formula_relation = {
        pins
        for pins in product(range(4), repeat=4)
        if pins[0] != pins[1] or pins[2] != pins[3]
    }
    need(named_relation == formula_relation, "named Boolean terminal relation")
    need(sum(relation_counter.values()) == 24 * len(canonical_full),
         "named/canonical colouring orbit count")

    all_pairs = set(combinations(range(11), 2))
    need(same == all_pairs - set(edges), "equality occurs on every nonedge only")
    need(different == all_pairs, "inequality occurs on every pair")

    projection_sizes = []
    for omitted in range(4):
        projection = {
            canonical(tuple(pattern[j] for j in range(4) if j != omitted))
            for pattern in canonical_relation
        }
        projection_sizes.append(len(projection))
        need(len(projection) == 5, "non-neutral three-terminal projection")

    deletion_data = {}
    vertices = tuple(range(11))
    for deleted in range(7):
        active = tuple(v for v in vertices if v != deleted)
        terminal_patterns = set()
        count = 0
        position = {vertex: i for i, vertex in enumerate(active)}
        for word in proper_partitions(active, edges, 4):
            count += 1
            terminal_patterns.add(
                canonical(tuple(word[position[v]] for v in TERMINALS))
            )
        need(terminal_patterns == all_terminal_patterns,
             f"deletion {deleted} is not terminal-neutral")
        deletion_data[str(deleted)] = {
            "canonical_proper_colourings": count,
            "canonical_terminal_patterns": len(terminal_patterns),
        }

    failed_words = list(proper_partitions(tuple(range(11)), failed_edges, 4))
    failed_relation = {
        canonical(tuple(word[v] for v in TERMINALS)) for word in failed_words
    }
    need(failed_relation == all_terminal_patterns, "failed formula is not neutral")

    return {
        "canonical_proper_four_colourings": len(canonical_full),
        "canonical_proper_at_most_three": three_colour_count,
        "named_proper_four_colourings": sum(relation_counter.values()),
        "canonical_terminal_patterns": len(canonical_relation),
        "canonical_forbidden": ["0000", "0011"],
        "named_terminal_patterns": len(named_relation),
        "labelled_relation_sha256": digest(sorted(named_relation)),
        "extension_multiplicity_sha256": digest(sorted(relation_counter.items())),
        "same_colour_nonunit_pairs": len(same),
        "different_colour_pairs": len(different),
        "three_terminal_projection_sizes": projection_sizes,
        "interior_deletions": deletion_data,
        "failed_formula_canonical_proper_four_colourings": len(failed_words),
        "failed_formula_terminal_patterns": len(failed_relation),
    }


def audit_certificate(certificate_path, edges, failed_edges):
    certificate = json.loads(certificate_path.read_text())
    need(certificate.get("schema") == "moser-four-terminal-relation-v1", "schema")
    all_patterns = set(restricted_growth_strings(4, 4))

    positive = certificate.get("positive_words")
    need(type(positive) is list and len(positive) == 13, "positive word count")
    positive_patterns = {
        canonical(check_named_word(word, edges)) for word in positive
    }
    need(len(positive_patterns) == 13 and positive_patterns == all_patterns - FORBIDDEN,
         "positive certificate coverage")

    deletion_rows = certificate.get("vertex_deletions")
    need(type(deletion_rows) is list and len(deletion_rows) == 7,
         "deletion row count")
    seen = set()
    for row in deletion_rows:
        deleted = row.get("deleted")
        need(type(deleted) is int and 0 <= deleted < 7 and deleted not in seen,
             "deletion index coverage")
        seen.add(deleted)
        words = row.get("words")
        need(type(words) is list and len(words) == 2, "deletion witness count")
        patterns = {
            canonical(check_named_word(word, edges, removed=deleted)) for word in words
        }
        need(patterns == FORBIDDEN, "deletion witnesses do not release exclusions")

    failed = certificate.get("failed_formula_words")
    need(type(failed) is list and len(failed) == 15, "failed witness count")
    failed_patterns = {
        canonical(check_named_word(word, failed_edges)) for word in failed
    }
    need(failed_patterns == all_patterns, "failed-formula witness coverage")
    return {
        "schema": certificate["schema"],
        "positive_words_checked": len(positive),
        "deletion_words_checked": 2 * len(deletion_rows),
        "failed_formula_words_checked": len(failed),
        "certificate_used_as_proof_premise": False,
    }


def run(source_directory):
    geometry = exact_geometry()
    colour = audit_colourings(geometry["edges"], geometry["failed_edges"])
    certificate = audit_certificate(
        source_directory / "certificate.json",
        geometry["edges"],
        geometry["failed_edges"],
    )
    return {
        "status": "INDEPENDENT EXACT REVIEW PASS",
        "sympy_version": sp.__version__,
        "geometry_backend": "QQ.algebraic_field(sqrt(3),sqrt(11))",
        "points": 11,
        "all_pairs": 55,
        "strict_unit_edges": len(geometry["edges"]),
        "failed_formula_strict_unit_edges": len(geometry["failed_edges"]),
        "point_sha256": geometry["point_sha256"],
        "distance_sha256": geometry["distance_sha256"],
        "edge_sha256": geometry["edge_sha256"],
        "colouring": colour,
        "supplied_certificate_audit": certificate,
        "record_improvement": False,
    }


def main():
    default_source = Path(__file__).resolve().parent.parent / (
        "hadwiger_nelson_moser_four_terminal_relation"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=default_source)
    args = parser.parse_args()
    print(json.dumps(run(args.source.resolve()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
