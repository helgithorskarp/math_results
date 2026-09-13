#!/usr/bin/env python3
"""Independent exact audit of the unit-edge dominating-triple theorem.

This checker imports neither target executable.  It reconstructs the finite
palette lemma from redundant orbit/phase assignments, checks the exceptional
geometry with rational arithmetic, and audits the exceptional two-centre
boundary used by the full statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_unit_edge_dominating_triples"

PAIR4 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR3 = ((0, 1), (0, 2), (1, 2))
TARGET_DIGESTS = {
    "build.py": "50411e55e64746dc643b09a8098ee68d314b16bcefaed6d4f0b07dc25d03c97b",
    "certificate.json": "21de55d7ad9a122aff7f973ffdfd011c51152dc50e59c45738a9fd1f487e0950",
    "verify.py": "adc758404a6be9455c913ae34e59244c98666c1ef2de0622607ad300d18ae9b2",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_partition(word):
    relabel = {}
    return tuple(relabel.setdefault(value, len(relabel)) for value in word)


def conflict_mask(orbit_ids, phases, pairs):
    mask = 0
    for bit, (left, right) in enumerate(pairs):
        if orbit_ids[left] == orbit_ids[right] and phases[left] != phases[right]:
            mask |= 1 << bit
    return mask


def parity_masks(n, pairs):
    """Generate all conflict graphs through deliberately redundant assignments."""
    masks = set()
    partitions = set()
    for orbit_ids in product(range(n), repeat=n):
        partitions.add(canonical_partition(orbit_ids))
        for phases in product((0, 1), repeat=n):
            masks.add(conflict_mask(orbit_ids, phases, pairs))
    return masks, partitions


def allocations(n, a_mask, c_mask, pairs, forced_a=()):
    answers = []
    for word in product((0, 1), repeat=n):  # 1=A palette; 0=C palette.
        if any(word[index] != 1 for index in forced_a):
            continue
        if any((a_mask >> bit & 1) and word[left] == word[right] == 1
               for bit, (left, right) in enumerate(pairs)):
            continue
        if any((c_mask >> bit & 1) and word[left] == word[right] == 0
               for bit, (left, right) in enumerate(pairs)):
            continue
        answers.append(word)
    return answers


def audit_certificate(certificate):
    need(certificate["schema"] == "unit-edge-dominating-triples-parity-v1", "schema")
    need(certificate["pair_order_4"] == [list(pair) for pair in PAIR4], "four-point pair order")
    need(certificate["pair_order_3"] == [list(pair) for pair in PAIR3], "three-point pair order")

    masks, partitions = parity_masks(4, PAIR4)
    need(len(partitions) == 15, "complete set-partition census")
    need(certificate["partition_label_encodings"] == len(partitions) * 2**4 == 240,
         "partition/phase encoding count")
    need(certificate["distinct_parity_conflict_graphs_4"] == len(masks) == 29,
         "complete parity-conflict graph census")

    histogram = Counter()
    exceptions = []
    admissible = 0
    for a_mask in sorted(masks):
        for c_mask in sorted(masks):
            # Bits 0 and 5 are the two same-owner intersection pairs.
            if bool(a_mask & 1) != bool(c_mask & 1):
                continue
            if bool(a_mask & 32) != bool(c_mask & 32):
                continue
            admissible += 1
            answers = allocations(4, a_mask, c_mask, PAIR4)
            histogram[len(answers)] += 1
            if not answers:
                exceptions.append({"a_mask": a_mask, "c_mask": c_mask})
    encoded_histogram = {str(key): value for key, value in sorted(histogram.items())}
    need(certificate["admissible_no_triple_graph_pairs"] == admissible == 251,
         "four-point admissible pair census")
    need(certificate["allocation_count_histogram"] == encoded_histogram,
         "four-point allocation histogram")
    need(certificate["unsat_no_triple"] == exceptions == [
        {"a_mask": 45, "c_mask": 51},
        {"a_mask": 51, "c_mask": 45},
    ], "four-point abstract exceptions")

    triple_histogram = Counter()
    triple_exceptions = []
    triple_systems = 0
    # Vertex 0 is triple-owned and forced to A.  C-conflicts incident with it
    # are irrelevant; the only possible C edge is bit 2 between vertices 1,2.
    for a_mask in range(8):
        for c_mask in (0, 4):
            triple_systems += 1
            answers = allocations(3, a_mask, c_mask, PAIR3, forced_a=(0,))
            triple_histogram[len(answers)] += 1
            if not answers:
                triple_exceptions.append({"a_mask": a_mask, "c_mask": c_mask})
    encoded_triple = {str(key): value for key, value in sorted(triple_histogram.items())}
    need(certificate["triple_systems"] == triple_systems == 16, "triple system census")
    need(certificate["triple_allocation_count_histogram"] == encoded_triple,
         "triple allocation histogram")
    need(certificate["unsat_one_triple"] == triple_exceptions == [
        {"a_mask": 3, "c_mask": 4},
        {"a_mask": 7, "c_mask": 4},
    ], "triple abstract exceptions")
    return {
        "set_partitions": len(partitions),
        "conflict_graphs": len(masks),
        "admissible_graph_pairs": admissible,
        "allocation_histogram": encoded_histogram,
        "no_triple_exceptions": exceptions,
        "triple_systems": triple_systems,
        "triple_allocation_histogram": encoded_triple,
        "one_triple_exceptions": triple_exceptions,
    }


def surd_is_rational(pair, rational):
    """Decide a+b*sqrt(33)=r, using irrationality of sqrt(33)."""
    a, b = pair
    return b == 0 and a == rational


def bi(value=0, sqrt3=0, sqrt11=0, sqrt33=0):
    """Element of Q(sqrt(3),sqrt(11)) in the displayed product basis."""
    return tuple(Fraction(entry) for entry in (value, sqrt3, sqrt11, sqrt33))


def bi_add(left, right, scale=1):
    return tuple(a + scale * b for a, b in zip(left, right))


def bi_mul(left, right):
    out = [Fraction(0)] * 4
    for left_mask, a in enumerate(left):
        for right_mask, b in enumerate(right):
            common = left_mask & right_mask
            factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
            out[left_mask ^ right_mask] += a * b * factor
    return tuple(out)


def point(x=bi(), y=bi()):
    return x, y


def point_add(left, right, scale=1):
    return bi_add(left[0], right[0], scale), bi_add(left[1], right[1], scale)


def point_norm_squared(value):
    return bi_add(bi_mul(value[0], value[0]), bi_mul(value[1], value[1]))


def rotate_sixth(value):
    half = Fraction(1, 2)
    sqrt3 = bi(0, 1)
    return (
        bi_add(tuple(half * entry for entry in value[0]),
               tuple(half * entry for entry in bi_mul(value[1], sqrt3)), -1),
        bi_add(tuple(half * entry for entry in bi_mul(value[0], sqrt3)),
               tuple(half * entry for entry in value[1])),
    )


def sixth_relation_exponent(first, second):
    current = first
    for exponent in range(6):
        if current == second:
            return exponent
        current = rotate_sixth(current)
    need(current == first, "sixth rotation closes")
    return None


def explicit_double_exception_masks():
    zero, one = point(), point(bi(1), bi())
    centre = point(bi(Fraction(1, 2)), bi(0, 0, Fraction(1, 2)))
    mixed = (
        (0, point(bi(Fraction(1, 4), 0, 0, Fraction(-1, 12)),
                  bi(0, Fraction(1, 12), Fraction(1, 4)))),
        (0, point(bi(Fraction(1, 4), 0, 0, Fraction(1, 12)),
                  bi(0, Fraction(-1, 12), Fraction(1, 4)))),
        (1, point(bi(Fraction(3, 4), 0, 0, Fraction(-1, 12)),
                  bi(0, Fraction(-1, 12), Fraction(1, 4)))),
        (1, point(bi(Fraction(3, 4), 0, 0, Fraction(1, 12)),
                  bi(0, Fraction(1, 12), Fraction(1, 4)))),
    )
    centres = (zero, one)
    for owner, value in mixed:
        need(point_norm_squared(point_add(value, centres[owner], -1)) == bi(1),
             "explicit point misses A-owner circle")
        need(point_norm_squared(point_add(value, centre, -1)) == bi(1),
             "explicit point misses exceptional-centre circle")
        need(point_norm_squared(point_add(value, centres[1 - owner], -1)) != bi(1),
             "unexpected triple-owned exceptional point")

    a_mask = c_mask = 0
    for bit, (left, right) in enumerate(PAIR4):
        i, p = mixed[left]
        j, q = mixed[right]
        exponent = sixth_relation_exponent(
            point_add(p, centres[i], -1), point_add(q, centres[j], -1)
        )
        if exponent is not None and (j - i + exponent) % 2:
            a_mask |= 1 << bit
        exponent = sixth_relation_exponent(
            point_add(p, centre, -1), point_add(q, centre, -1)
        )
        if exponent is not None and (j - i + exponent) % 2:
            c_mask |= 1 << bit
    return a_mask, c_mask


def geometry_audit():
    cosines = (1, Fraction(1, 2), Fraction(-1, 2), -1,
               Fraction(-1, 2), Fraction(1, 2))
    chord_squares = tuple(2 - 2 * value for value in cosines)
    need(chord_squares == (0, 1, 3, 4, 3, 1), "sixth-rotation chord table")
    odd_steps = tuple(step for step in (1, 3, 5) if chord_squares[step] in (1, 4))
    need(odd_steps == (1, 3, 5), "odd phase-conflict rotations")
    # For two distinct unit-circle centres, a three-step chord would make the
    # two intersection points antipodal and hence make the centres coincide.
    distinct_centre_conflict_chord_square = 1
    conflict_centre_distance_square = 4 - distinct_centre_conflict_chord_square
    need(conflict_centre_distance_square == 3, "within-pair conflict locus")

    # Both within-pair conflicts force |c|^2=|c-1|^2=3.
    x = Fraction(1, 2)
    y_squared = Fraction(11, 4)
    need(x * x + y_squared == 3, "first exceptional centre distance")
    need((x - 1) ** 2 + y_squared == 3, "second exceptional centre distance")

    # cos(delta)=5/6 and sin(delta)=sqrt(11)/6.  Rotating either direction by
    # plus/minus pi/3 gives the following values in Q(sqrt(33)).
    cross_cosines = (
        (Fraction(5, 6), Fraction(0)),
        (Fraction(5, 12), Fraction(1, 12)),
        (Fraction(5, 12), Fraction(-1, 12)),
    )
    even_sixth_cosines = (Fraction(1), Fraction(-1, 2))
    need(all(not surd_is_rational(value, target)
             for value in cross_cosines for target in even_sixth_cosines),
         "no cross conflict at the double-exceptional centre")
    actual_double_masks = explicit_double_exception_masks()
    need(actual_double_masks == (33, 33), "exact exceptional conflict masks")
    need(actual_double_masks not in ((45, 51), (51, 45)),
         "abstract four-point exceptions are not physical")

    triple_distance_squares = (
        (Fraction(7, 2), Fraction(1, 2)),
        (Fraction(7, 2), Fraction(-1, 2)),
    )
    need(all(not surd_is_rational(value, 1) for value in triple_distance_squares),
         "no triple-owned point at the exceptional centre")

    # At C_0 intersect C_1, the upper directions have exponents 1 from a0
    # and 2 from a1; the lower directions have exponents 5 and 4.  The owner
    # offset in f_A makes both descriptions agree.
    common_point_parities = ((0 + 1) % 2, (1 + 2) % 2,
                             (0 + 5) % 2, (1 + 4) % 2)
    need(common_point_parities == (1, 1, 1, 1), "two-owner colour consistency")
    return {
        "sixth_rotation_chord_squares": [int(value) for value in chord_squares],
        "within_pair_conflict_centre_distance_squared": int(conflict_centre_distance_square),
        "double_exceptional_centres": "(1+i*sqrt(11))/2 and its conjugate",
        "double_exception_actual_masks": list(actual_double_masks),
        "cross_cosines_Qsqrt33": [[str(a), str(b)] for a, b in cross_cosines],
        "triple_distance_squares_Qsqrt33": [
            [str(a), str(b)] for a, b in triple_distance_squares
        ],
        "common_point_owner_descriptions_agree": True,
    }


def triangular_norm_squared(left, right):
    """Squared norm for [s,t]=(s*sqrt(3)/2,t/2)."""
    ds, dt = left[0] - right[0], left[1] - right[1]
    return Fraction(3 * ds * ds + dt * dt, 4)


def audit_two_centre_patch(colors=None):
    a = (0, 0)
    b = (2, 0)
    rim_a = ((1, 1), (0, 2), (-1, 1), (-1, -1), (0, -2), (1, -1))
    rim_b = tuple((s + 2, t) for s, t in rim_a)
    points = (a, b, (1, 1), (0, 2), (-1, 1), (-1, -1), (0, -2),
              (1, -1), (3, 1), (2, 2), (2, -2), (3, -1))
    need(len(set(points)) == 12 and set(points) == {a, b, *rim_a, *rim_b},
         "complete exceptional two-centre patch")
    if colors is None:
        colors = (2, 0, 1, 0, 1, 0, 1, 3, 1, 2, 1, 2)
    need(len(colors) == len(points), "two-centre colour word length")
    edges = []
    for left, right in combinations(range(len(points)), 2):
        if triangular_norm_squared(points[left], points[right]) == 1:
            need(colors[left] != colors[right], "two-centre patch colouring")
            edges.append((left, right))
    need(len(edges) == 23, "complete exceptional patch edge count")

    witnesses = 0
    directed_cases = 0
    for rim, opposite_centre, opposite_rim in (
        (rim_a, b, set(rim_b)),
        (rim_b, a, set(rim_a)),
    ):
        for point in rim:
            directed_cases += 1
            distance_squared = triangular_norm_squared(point, opposite_centre)
            expected = 2 if distance_squared < 4 else 1 if distance_squared == 4 else 0
            actual = sum(
                other != point and triangular_norm_squared(point, other) == 1
                for other in opposite_rim
            )
            need(actual == expected, "complete cross-circle boundary intersection count")
            witnesses += actual
    need((directed_cases, witnesses) == (12, 12), "two-centre boundary totals")
    return {
        "patch_vertices": len(points),
        "strict_patch_edges": len(edges),
        "directed_boundary_cases": directed_cases,
        "certified_cross_circle_intersections": witnesses,
        "all_patch_edges_proper": True,
    }


def run(certificate_path, target_directory):
    target_directory = Path(target_directory)
    for filename, expected in TARGET_DIGESTS.items():
        need(file_digest(target_directory / filename) == expected,
             f"target source digest: {filename}")
    certificate = json.loads(Path(certificate_path).read_text())
    finite = audit_certificate(certificate)
    geometry = geometry_audit()
    two_centre = audit_two_centre_patch()
    return {
        "verified": True,
        "verdict": "ACCEPT_WITH_MINOR_DOCUMENTATION_CORRECTIONS",
        "scope": "plane unit-distance graphs with a dominating set of at most three vertices containing an edge",
        "record_improvement": False,
        "target_source_commit": "4c6eee8bfd5788dde7aa659fecb83b7da16618ed",
        "finite_allocation": finite,
        "exceptional_geometry": geometry,
        "two_centre_boundary": two_centre,
        "dependency_status": {
            "connected_dominating_triples": "committed and independently accepted at h3359",
            "two_centre_full_support": "committed author theorem; required boundary independently audited here",
        },
        "documentation_corrections": [
            "PROOF.md contains a literal backspace byte where beta_O is intended.",
            "Equations (3) and (4) should explicitly fix one representative in each six-rotation orbit.",
            "The two-centre source is committed and author-checked but has no committed independent VERIFIES edge.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--target-directory", type=Path, default=TARGET)
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run(arguments.certificate, arguments.target_directory)
    if arguments.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "expected independent review output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
