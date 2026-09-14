#!/usr/bin/env python3
"""Independent exact review of the three-diamond palette-chain source.

No target Python module is imported. Geometry uses SymPy's exact algebraic
number field. Colourings are generated as restricted-growth strings, so the
search works with canonical set partitions instead of the target's named
assignment/backtracking loop.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from math import factorial
from pathlib import Path

import sympy as sp


LABELS = ("P0", "P1", "P2", "P3", "X0", "Y0", "X1", "Y1", "X2", "Y2")
TERMINALS = (4, 5, 6, 7, 8, 9)
FULL_VERTICES = tuple(range(10))
REDUCED_VERTICES = (1, 2, 4, 5, 6, 7, 8, 9)
EXPECTED_EDGES = (
    (0, 3),
    (0, 4), (0, 5),
    (1, 4), (1, 5), (1, 6), (1, 7),
    (2, 6), (2, 7), (2, 8), (2, 9),
    (3, 8), (3, 9),
    (4, 5), (6, 7), (8, 9),
)
TERMINAL_EDGES = {(4, 5), (6, 7), (8, 9)}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def rgs(length, max_colours):
    """All restricted-growth strings of length n with at most k blocks."""
    need(length >= 1 and max_colours >= 1, "positive RGS dimensions")
    word = [0] * length

    def visit(position, largest):
        if position == length:
            yield tuple(word)
            return
        for colour in range(min(largest + 1, max_colours - 1) + 1):
            word[position] = colour
            yield from visit(position + 1, max(largest, colour))

    yield from visit(1, 0)


def canonical(word):
    names = {}
    return tuple(names.setdefault(colour, len(names)) for colour in word)


def pattern_text(word):
    return "".join(map(str, canonical(word)))


def induced_edges(vertices, edges):
    present = set(vertices)
    return tuple((a, b) for a, b in edges if a in present and b in present)


def proper_partitions(vertices, edges, max_colours):
    positions = {vertex: position for position, vertex in enumerate(vertices)}
    local_edges = tuple(
        (positions[a], positions[b])
        for a, b in edges
        if a in positions and b in positions
    )
    for word in rgs(len(vertices), max_colours):
        if all(word[a] != word[b] for a, b in local_edges):
            yield word


def named_orbit(word):
    used = max(word) + 1
    for injection in permutations(range(4), used):
        yield tuple(injection[colour] for colour in word)


def terminal_relation(vertices, edges):
    positions = {vertex: position for position, vertex in enumerate(vertices)}
    canonical_words = list(proper_partitions(vertices, edges, 4))
    canonical_relation = {
        pattern_text(tuple(word[positions[v]] for v in TERMINALS))
        for word in canonical_words
    }
    named_relation = set()
    named_multiplicity = Counter()
    for word in canonical_words:
        for named_word in named_orbit(word):
            pins = tuple(named_word[positions[v]] for v in TERMINALS)
            named_relation.add(pins)
            named_multiplicity[pins] += 1
    return canonical_words, canonical_relation, named_relation, named_multiplicity


def direct_formula(assignment):
    palettes = [set(assignment[2 * i:2 * i + 2]) for i in range(3)]
    return bool(palettes[0] & palettes[1]) and bool(palettes[1] & palettes[2])


def exact_geometry(certificate):
    s_expr = sp.sqrt(3)
    y_expr = sp.sqrt((4 - s_expr) / 2)
    field = sp.QQ.algebraic_field(s_expr, y_expr)
    q = lambda expression: field.from_sympy(sp.sympify(expression))
    zero, one = q(0), q(1)
    s, y = q(s_expr), q(y_expr)
    need(field.mod.degree() == 4, "unexpected algebraic field degree")
    need(s * s == q(3) and y * y == q(2) - s / q(2), "field relations")

    def add(p, qpoint):
        return p[0] + qpoint[0], p[1] + qpoint[1]

    def sub(p, qpoint):
        return p[0] - qpoint[0], p[1] - qpoint[1]

    def scale(p, amount):
        amount = q(amount)
        return p[0] * amount, p[1] * amount

    def dist2(p, qpoint):
        dx, dy = sub(p, qpoint)
        return dx * dx + dy * dy

    caps = (
        (zero, zero),
        ((one + s) / q(2), y),
        ((one - s) / q(2), y),
        (one, zero),
    )
    points = list(caps)
    for left, right in zip(caps, caps[1:]):
        dx, dy = sub(right, left)
        midpoint = scale(add(left, right), sp.Rational(1, 2))
        offset = (-dy / (q(2) * s), dx / (q(2) * s))
        points.extend((add(midpoint, offset), sub(midpoint, offset)))
    points = tuple(points)
    need(len(points) == 10 and len(set(points)) == 10, "point census/collision")

    for i in range(3):
        need(dist2(caps[i], caps[i + 1]) == q(3), "cap distance sqrt(3)")
    need(dist2(caps[0], caps[3]) == one, "closing cap edge")

    distance_rows = []
    exact_edges = []
    for a, b in combinations(range(10), 2):
        squared = dist2(points[a], points[b])
        coefficients = [str(value) for value in squared.to_list()]
        distance_rows.append([a, b, coefficients])
        if squared == one:
            exact_edges.append((a, b))
    need(tuple(exact_edges) == EXPECTED_EDGES, "complete exact unit-edge census")

    rows = certificate.get("points")
    need(type(rows) is list and len(rows) == 10, "certificate point rows")
    parsed = []
    for expected_label, row in zip(LABELS, rows):
        need(type(row) is dict and row.get("label") == expected_label, "point label")

        def parse_element(values):
            need(type(values) is list and len(values) == 4 and
                 all(type(value) is str for value in values), "coordinate row")
            a, b, c, d = map(sp.Rational, values)
            return q(a + b * s_expr + c * y_expr + d * s_expr * y_expr)

        parsed.append((parse_element(row.get("x")), parse_element(row.get("y"))))
    need(tuple(parsed) == points, "certificate rows differ from radical construction")
    need(certificate.get("point_rows_sha256") == digest(rows), "point-row hash")

    edge_rows = certificate.get("edges")
    need(type(edge_rows) is list and all(type(row) is list and len(row) == 2 for row in edge_rows),
         "certificate edge rows")
    need(tuple(map(tuple, edge_rows)) == EXPECTED_EDGES, "certificate edge list")
    need(certificate.get("edge_rows_sha256") == digest(edge_rows), "edge-row hash")

    return {
        "edges": tuple(exact_edges),
        "distance_signature_sha256": digest(distance_rows),
        "point_rows_sha256": digest(rows),
        "edge_rows_sha256": digest(edge_rows),
    }


def audit_colouring(edges):
    proper_two = list(proper_partitions(FULL_VERTICES, edges, 2))
    proper_three = list(proper_partitions(FULL_VERTICES, edges, 3))
    full_words, allowed_canonical, allowed_named, named_multiplicity = terminal_relation(
        FULL_VERTICES, edges
    )
    need(not proper_two and not proper_three, "full graph lower chromatic bound")
    need(len(full_words) == 208 and all(max(word) == 3 for word in full_words),
         "full graph canonical four-colouring census")

    bare_named = {
        assignment
        for assignment in product(range(4), repeat=6)
        if all(assignment[2 * i] != assignment[2 * i + 1] for i in range(3))
    }
    bare_canonical = {pattern_text(assignment) for assignment in bare_named}
    formula_named = {assignment for assignment in bare_named if direct_formula(assignment)}
    need(len(bare_named) == 1728 and len(bare_canonical) == 74, "bare relation census")
    need(allowed_named == formula_named, "full named relation/formula disagreement")
    need(allowed_canonical == {pattern_text(a) for a in formula_named},
         "full canonical relation/formula disagreement")

    # Check the claimed structural proof at graph level.
    diamonds = (
        (0, 1, 4, 5),
        (1, 2, 6, 7),
        (2, 3, 8, 9),
    )
    edge_set = set(edges)
    for left, right, x, y in diamonds:
        required = {(left, x), (left, y), (right, x), (right, y), (x, y)}
        need(required <= edge_set and (left, right) not in edge_set, "diamond structure")
    need((0, 3) in edge_set, "closing edge structure")

    return {
        "chromatic_number": 4,
        "canonical_proper_at_most_two": len(proper_two),
        "canonical_proper_at_most_three": len(proper_three),
        "canonical_proper_at_most_four": len(full_words),
        "named_proper_four_colourings": sum(
            factorial(4) // factorial(4 - (max(word) + 1)) for word in full_words
        ),
        "canonical_bare_patterns": len(bare_canonical),
        "canonical_extendible_patterns": len(allowed_canonical),
        "canonical_forbidden_patterns": len(bare_canonical - allowed_canonical),
        "named_bare_assignments": len(bare_named),
        "named_extendible_assignments": len(allowed_named),
        "named_forbidden_assignments": len(bare_named - allowed_named),
        "canonical_relation_sha256": digest(sorted(allowed_canonical)),
        "named_relation_sha256": digest(sorted(allowed_named)),
        "named_extension_multiplicity_sha256": digest(sorted(named_multiplicity.items())),
    }


def audit_reduction(edges):
    reduced_edges = induced_edges(REDUCED_VERTICES, edges)
    need(len(reduced_edges) == 11, "reduced edge count")
    reduced_two = list(proper_partitions(REDUCED_VERTICES, reduced_edges, 2))
    reduced_three = list(proper_partitions(REDUCED_VERTICES, reduced_edges, 3))
    reduced_words, reduced_canonical, reduced_named, reduced_multiplicity = terminal_relation(
        REDUCED_VERTICES, reduced_edges
    )
    need(not reduced_two and len(reduced_three) == 4, "reduced chromatic number")

    full_words, full_canonical, full_named, _ = terminal_relation(FULL_VERTICES, edges)
    need(reduced_canonical == full_canonical and reduced_named == full_named,
         "outer caps change the complete terminal relation")

    deletion_relations = {}
    for deleted in range(4):
        active = tuple(v for v in FULL_VERTICES if v != deleted)
        words, canonical_relation, named_relation, _ = terminal_relation(active, edges)
        deletion_relations[str(deleted)] = {
            "canonical_proper_colourings": len(words),
            "canonical_terminal_patterns": len(canonical_relation),
            "named_terminal_assignments": len(named_relation),
        }
    need(deletion_relations["0"]["canonical_terminal_patterns"] == 52 and
         deletion_relations["3"]["canonical_terminal_patterns"] == 52,
         "outer cap redundancy")
    need(deletion_relations["1"]["canonical_terminal_patterns"] == 62 and
         deletion_relations["2"]["canonical_terminal_patterns"] == 62,
         "essential shared-cap deletion boundary")

    core_deletions = {}
    bare_assignments = {
        assignment
        for assignment in product(range(4), repeat=6)
        if all(assignment[2 * i] != assignment[2 * i + 1] for i in range(3))
    }
    for deleted in (1, 2):
        active = tuple(v for v in REDUCED_VERTICES if v != deleted)
        words, canonical_relation, named_relation, _ = terminal_relation(active, edges)
        if deleted == 1:
            expected_named = {
                assignment for assignment in bare_assignments
                if set(assignment[2:4]) & set(assignment[4:6])
            }
            remaining_formula = "palette(E1) intersects palette(E2)"
        else:
            expected_named = {
                assignment for assignment in bare_assignments
                if set(assignment[0:2]) & set(assignment[2:4])
            }
            remaining_formula = "palette(E0) intersects palette(E1)"
        need(named_relation == expected_named, "core deletion formula")
        core_deletions[str(deleted)] = {
            "canonical_proper_colourings": len(words),
            "canonical_terminal_patterns": len(canonical_relation),
            "named_terminal_assignments": len(named_relation),
            "remaining_formula": remaining_formula,
        }
    need(all(row["canonical_terminal_patterns"] == 62 and
             row["named_terminal_assignments"] == 1440
             for row in core_deletions.values()),
         "eight-point core deletion boundary")

    no_shared_caps = tuple(v for v in FULL_VERTICES if v not in (0, 1, 2, 3))
    _, bare_canonical, bare_named, _ = terminal_relation(no_shared_caps, edges)
    need(len(bare_canonical) == 74 and len(bare_named) == 1728,
         "terminal-only bare relation")

    return {
        "removed_vertices": [0, 3],
        "retained_labels": [LABELS[v] for v in REDUCED_VERTICES],
        "points": len(REDUCED_VERTICES),
        "all_pairs": len(REDUCED_VERTICES) * (len(REDUCED_VERTICES) - 1) // 2,
        "strict_unit_edges": len(reduced_edges),
        "chromatic_number": 3,
        "canonical_proper_at_most_two": len(reduced_two),
        "canonical_proper_at_most_three": len(reduced_three),
        "canonical_proper_at_most_four": len(reduced_words),
        "canonical_extendible_patterns": len(reduced_canonical),
        "named_extendible_assignments": len(reduced_named),
        "canonical_relation_sha256": digest(sorted(reduced_canonical)),
        "named_relation_sha256": digest(sorted(reduced_named)),
        "named_extension_multiplicity_sha256": digest(sorted(reduced_multiplicity.items())),
        "single_cap_deletions_from_full": deletion_relations,
        "interior_deletions_from_eight_point_core": core_deletions,
        "fixed_support_relation_core_minimal": True,
        "global_minimality_claimed": False,
    }


def audit_certificate(certificate, edges, full_audit):
    need(certificate.get("format") == "hn-three-diamond-palette-chain-v1", "schema")
    chromatic = certificate.get("chromatic")
    need(type(chromatic) is dict and chromatic.get("number") == 4, "chromatic block")
    four_word = chromatic.get("four_colouring")
    need(type(four_word) is str and len(four_word) == 10 and set(four_word) <= set("0123"),
         "four-colour word syntax")
    word = tuple(map(int, four_word))
    need(all(word[a] != word[b] for a, b in edges), "improper four-colour word")

    relation = certificate.get("relation")
    need(type(relation) is dict and relation.get("terminals") == list(TERMINALS),
         "relation terminal block")
    need(relation.get("bare_terminal_edges") == [list(edge) for edge in sorted(TERMINAL_EDGES)],
         "bare terminal edges")
    expected_bare = {
        pattern_text(assignment)
        for assignment in product(range(4), repeat=6)
        if all(assignment[2 * i] != assignment[2 * i + 1] for i in range(3))
    }
    full_words, allowed_canonical, _, _ = terminal_relation(FULL_VERTICES, edges)
    need(relation.get("canonical_bare_patterns") == sorted(expected_bare),
         "certificate bare patterns")
    need(relation.get("canonical_extendible_patterns") == sorted(allowed_canonical),
         "certificate extendible patterns")

    witnesses = relation.get("canonical_witnesses")
    need(type(witnesses) is dict and set(witnesses) == allowed_canonical,
         "certificate witness coverage")
    for pattern, text in witnesses.items():
        need(type(text) is str and len(text) == 10 and set(text) <= set("0123"),
             "witness syntax")
        witness = tuple(map(int, text))
        need(all(witness[a] != witness[b] for a, b in edges), "improper witness")
        need(pattern_text(tuple(witness[v] for v in TERMINALS)) == pattern,
             "witness terminal pattern")

    need((relation.get("named_bare_assignments"),
          relation.get("named_extendible_assignments"),
          relation.get("named_forbidden_assignments")) ==
         (full_audit["named_bare_assignments"],
          full_audit["named_extendible_assignments"],
          full_audit["named_forbidden_assignments"]), "certificate named counts")
    return {
        "four_colouring_checked": True,
        "canonical_witnesses_checked": len(witnesses),
        "certificate_used_as_relation_proof_premise": False,
    }


def run(source_directory):
    certificate = json.loads((source_directory / "certificate.json").read_text())
    geometry = exact_geometry(certificate)
    full_audit = audit_colouring(geometry["edges"])
    reduction = audit_reduction(geometry["edges"])
    certificate_audit = audit_certificate(certificate, geometry["edges"], full_audit)
    return {
        "status": "INDEPENDENT EXACT REVIEW PASS WITH EIGHT-POINT REFINEMENT",
        "sympy_version": sp.__version__,
        "geometry_backend": "QQ.algebraic_field(sqrt(3),sqrt((4-sqrt(3))/2))",
        "full_source": {
            "points": 10,
            "all_pairs": 45,
            "strict_unit_edges": len(geometry["edges"]),
            "distance_signature_sha256": geometry["distance_signature_sha256"],
            "point_rows_sha256": geometry["point_rows_sha256"],
            "edge_rows_sha256": geometry["edge_rows_sha256"],
            **full_audit,
        },
        "eight_point_relation_core": reduction,
        "supplied_certificate_audit": certificate_audit,
        "five_chromatic_construction": False,
        "record_improvement": False,
    }


def main():
    default_source = Path(__file__).resolve().parent.parent / (
        "hadwiger_nelson_three_diamond_palette_chain"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=default_source)
    args = parser.parse_args()
    print(json.dumps(run(args.source.resolve()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
