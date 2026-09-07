#!/usr/bin/env python3
"""Independent exact verifier using a nested quadratic representation."""

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# A quadratic pair is a+b*w, w^2=5.  A point is R+i*h*I, where R and I are
# quadratic pairs and h^2=10+2*w.  This is deliberately different from the
# producer's cyclotomic power-basis arithmetic.
QZERO = (F(0), F(0))
QONE = (F(1), F(0))
H2 = (F(10), F(2))


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qneg(a):
    return (-a[0], -a[1])


def qsub(a, b):
    return qadd(a, qneg(b))


def qmul(a, b):
    return (a[0] * b[0] + 5 * a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qinverse(a):
    denominator = a[0] * a[0] - 5 * a[1] * a[1]
    if not denominator:
        raise ZeroDivisionError
    return (a[0] / denominator, -a[1] / denominator)


def qscale(value, a):
    return (value * a[0], value * a[1])


def cadd(a, b):
    return (qadd(a[0], b[0]), qadd(a[1], b[1]))


def cneg(a):
    return (qneg(a[0]), qneg(a[1]))


def csub(a, b):
    return cadd(a, cneg(b))


def cmul(a, b):
    return (
        qsub(qmul(a[0], b[0]), qmul(H2, qmul(a[1], b[1]))),
        qadd(qmul(a[0], b[1]), qmul(a[1], b[0])),
    )


def cconjugate(a):
    return (a[0], qneg(a[1]))


def cnorm(a):
    product = cmul(a, cconjugate(a))
    if product[1] != QZERO:
        raise ArithmeticError("nonreal squared norm")
    return product[0]


def cinverse(a):
    reciprocal_norm = qinverse(cnorm(a))
    conjugate = cconjugate(a)
    return (qmul(reciprocal_norm, conjugate[0]),
            qmul(reciprocal_norm, conjugate[1]))


def cpow(a, exponent):
    result = (QONE, QZERO)
    while exponent:
        if exponent & 1:
            result = cmul(result, a)
        a = cmul(a, a)
        exponent //= 2
    return result


ZETA = (((F(-1, 4)), F(1, 4)), ((F(1, 4)), F(0)))
POWERS = tuple(cpow(ZETA, exponent) for exponent in range(5))
SCALE_SQUARED = {
    "down": (F(3, 2), F(-1, 2)),
    "up": (F(3, 2), F(1, 2)),
}
UNIT_NORM = (F(5, 2), F(-1, 2))
GOLDEN_NORM = (F(5, 2), F(1, 2))

SOURCE_ROWS = (
    (0, 0, 0, 0, 5), (1, 0, 0, 0, 4),
    (0, 0, 0, 1, 4), (1, 0, 0, 1, 3),
    (0, 1, 0, 0, 4), (0, 0, 1, 0, 4),
    (1, 0, 1, 0, 3), (0, 1, 0, 1, 3),
    (1, 1, 0, 0, 3), (0, 0, 1, 1, 3),
    (1, 1, 0, 1, 2), (1, 0, 1, 1, 2),
    (0, 1, 1, 0, 3), (1, 1, 1, 0, 2),
    (0, 1, 1, 1, 2), (1, 1, 1, 1, 1),
)


def cscale(value, point):
    return (qscale(value, point[0]), qscale(value, point[1]))


def source_point(row):
    result = (QZERO, QZERO)
    for exponent, coefficient in enumerate(row):
        result = cadd(result, cscale(F(coefficient), POWERS[exponent]))
    return result


SOURCE = tuple(source_point(row) for row in SOURCE_ROWS)


def point_key(point):
    values = (*point[0], *point[1])
    integers = tuple(int(88 * value) for value in values)
    if any(F(integer, 88) != value
           for integer, value in zip(integers, values)):
        raise ArithmeticError("coordinate is not on the denominator-88 grid")
    return integers


def digest_rows(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(str(value) for value in row) + "\n").encode())
    return digest.hexdigest()


def enumerate_copies(name):
    scale_squared = SCALE_SQUARED[name]
    pairs = tuple(combinations(range(len(SOURCE)), 2))
    differences = {pair: csub(SOURCE[pair[1]], SOURCE[pair[0]])
                   for pair in pairs}
    inverses = {pair: cinverse(value) for pair, value in differences.items()}
    conjugate_inverses = {
        pair: cinverse(cconjugate(value)) for pair, value in differences.items()
    }
    point_sets = {}
    raw = 0
    for source_left, source_right in pairs:
        source_difference = differences[source_left, source_right]
        for target_left, target_right in pairs:
            target_difference = differences[target_left, target_right]
            if cnorm(target_difference) != qmul(
                    scale_squared, cnorm(source_difference)):
                continue
            for swap in (False, True):
                image_left, image_right = (
                    (target_right, target_left) if swap
                    else (target_left, target_right)
                )
                image_difference = csub(SOURCE[image_right], SOURCE[image_left])
                for reflected in (False, True):
                    raw += 1
                    multiplier = cmul(
                        image_difference,
                        conjugate_inverses[source_left, source_right]
                        if reflected else inverses[source_left, source_right],
                    )
                    moved = []
                    for point in SOURCE:
                        difference = csub(point, SOURCE[source_left])
                        if reflected:
                            difference = cconjugate(difference)
                        moved.append(cadd(
                            SOURCE[image_left], cmul(multiplier, difference)
                        ))
                    key = tuple(sorted(point_key(point) for point in moved))
                    point_sets.setdefault(key, tuple(moved))
    return raw, tuple((key, point_sets[key]) for key in sorted(point_sets))


def squared_norm_numerator(key):
    a, b, c, d = key
    real_squared = (a * a + 5 * b * b, 2 * a * b)
    imag_squared = (c * c + 5 * d * d, 2 * c * d)
    scaled_imag_squared = (
        10 * imag_squared[0] + 10 * imag_squared[1],
        2 * imag_squared[0] + 10 * imag_squared[1],
    )
    return (real_squared[0] + scaled_imag_squared[0],
            real_squared[1] + scaled_imag_squared[1])


INTEGER_UNIT_NORM = (19360, -3872)
INTEGER_GOLDEN_NORM = (19360, 3872)


def distance_edges(keys, target=INTEGER_UNIT_NORM):
    edges = []
    for left, right in combinations(range(len(keys)), 2):
        difference = tuple(y - x for x, y in zip(keys[left], keys[right]))
        if squared_norm_numerator(difference) == target:
            edges.append((left, right))
    return tuple(edges)


SOURCE_UNIT_EDGES = (
    (1,2),(1,3),(2,4),(2,5),(3,4),(3,6),(4,7),(4,8),
    (5,6),(5,8),(5,9),(6,7),(6,10),(7,9),(7,12),(7,13),
    (8,10),(8,11),(8,13),(9,11),(10,12),(11,12),(11,14),
    (12,15),(13,14),(13,15),(14,16),(15,16),
)
SOURCE_GOLDEN_EDGES = (
    (1,5),(1,6),(2,3),(2,6),(2,7),(2,9),(3,5),(3,8),
    (3,10),(4,9),(4,10),(4,11),(4,12),(5,13),(6,13),(7,10),
    (7,14),(8,9),(8,15),(9,13),(9,14),(10,13),(10,15),(11,15),
    (11,16),(12,14),(12,16),(14,15),
)


def copy_digest(groups):
    rows = []
    for scale_index, name in enumerate(("down", "up")):
        for index, (point_set, _points) in enumerate(groups[name][1]):
            rows.append((scale_index, index,
                         *(value for point in point_set for value in point)))
    return digest_rows(rows)


def valid_colouring(vertices, edges, row, colours):
    return (len(row) == vertices
            and all(isinstance(value, int) and 0 <= value < colours for value in row)
            and all(row[left] != row[right] for left, right in edges))


def verify(certificate, expected):
    if certificate.get("schema") != "hn-golden-reciprocal-closure-v1":
        raise AssertionError("unknown certificate schema")
    source_keys = tuple(point_key(point) for point in SOURCE)
    source_unit = distance_edges(source_keys, INTEGER_UNIT_NORM)
    source_golden = distance_edges(source_keys, INTEGER_GOLDEN_NORM)
    stated_unit = tuple(sorted((left - 1, right - 1)
                               for left, right in SOURCE_UNIT_EDGES))
    stated_golden = tuple(sorted((left - 1, right - 1)
                                 for left, right in SOURCE_GOLDEN_EDGES))
    if source_unit != stated_unit or source_golden != stated_golden:
        raise AssertionError("reconstructed source edges disagree with Parts")
    source_graph = tuple(sorted(source_unit + source_golden))
    clique = tuple(value - 1 for value in
                   certificate["source"]["clique_labels_one_based"])
    if len(clique) != 5 or any(
            tuple(sorted((left, right))) not in source_graph
            for left, right in combinations(clique, 2)):
        raise AssertionError("source K5 check failed")
    if not valid_colouring(
            len(SOURCE), source_graph, certificate["source"]["five_colouring"], 5):
        raise AssertionError("invalid source five-colouring")

    groups = {name: enumerate_copies(name) for name in ("down", "up")}
    one_scale = {}
    source_key_set = set(source_keys)
    scale_actual = []
    all_copy_keys = {}
    for name in ("down", "up"):
        raw, copies = groups[name]
        overlap_histogram = Counter(
            len(set(point_set) & source_key_set) for point_set, _points in copies
        )
        point_map = {point_key(point): point for point in SOURCE}
        for _point_set, points in copies:
            for point in points:
                point_map.setdefault(point_key(point), point)
        keys = tuple(sorted(point_map))
        edges = distance_edges(keys)
        all_copy_keys[name] = {
            point for point_set, _points in copies for point in point_set
        }
        scale_actual.append({
            "name": name,
            "scale": "1/phi" if name == "down" else "phi",
            "raw_labeled_specifications": raw,
            "distinct_copy_point_sets": len(copies),
            "copy_base_overlap_histogram": [
                {"coincident_points": overlap, "copies": count}
                for overlap, count in sorted(overlap_histogram.items())
            ],
            "closure_vertices": len(keys),
            "closure_edges": len(edges),
            "closure_point_sha256": digest_rows(keys),
            "closure_edge_sha256": digest_rows(edges),
        })
        one_scale[name] = (keys, edges)

    point_map = {point_key(point): point for point in SOURCE}
    for _raw, copies in groups.values():
        for _point_set, points in copies:
            for point in points:
                point_map.setdefault(point_key(point), point)
    keys = tuple(sorted(point_map))
    edges = distance_edges(keys)
    colour_word = certificate["full_closure"]["four_colouring"]
    if not isinstance(colour_word, str) or any(c not in "0123" for c in colour_word):
        raise AssertionError("malformed closure colour word")
    colours = tuple(int(c) for c in colour_word)
    if not valid_colouring(len(keys), edges, colours, 4):
        raise AssertionError("invalid closure four-colouring")

    actual = {
        "source_vertices": len(SOURCE),
        "source_unit_edges": len(source_unit),
        "source_golden_edges": len(source_golden),
        "source_clique_labels_one_based": [value + 1 for value in clique],
        "scales": scale_actual,
        "distinct_copies_total": sum(len(group[1]) for group in groups.values()),
        "copy_point_sets_sha256": copy_digest(groups),
        "scale_closure_intersection_vertices": len(
            all_copy_keys["down"] & all_copy_keys["up"]
        ),
        "closure_vertices": len(keys),
        "closure_edges": len(edges),
        "closure_point_sha256": digest_rows(keys),
        "closure_edge_sha256": digest_rows(edges),
        "four_colouring_sha256": sha256(colour_word.encode()).hexdigest(),
        "record_target_met": False,
    }
    if actual != expected:
        raise AssertionError("verified result disagrees with EXPECTED.json")

    source_section = certificate["source"]
    if (source_section["vertices"], source_section["unit_edges"],
            source_section["golden_edges"], source_section["chromatic_number"]) != (
                len(SOURCE), len(source_unit), len(source_golden), 5):
        raise AssertionError("source metadata mismatch")
    family = certificate["family"]
    if family["scales"] != scale_actual:
        raise AssertionError("scale metadata mismatch")
    if any(family[key] != actual[key] for key in (
            "distinct_copies_total", "copy_point_sets_sha256",
            "scale_closure_intersection_vertices")):
        raise AssertionError("family metadata mismatch")
    closure = certificate["full_closure"]
    for certificate_key, actual_key in (
            ("vertices", "closure_vertices"), ("edges", "closure_edges"),
            ("point_sha256", "closure_point_sha256"),
            ("edge_sha256", "closure_edge_sha256"),
            ("four_colouring_sha256", "four_colouring_sha256")):
        if closure[certificate_key] != actual[actual_key]:
            raise AssertionError(f"closure {certificate_key} mismatch")
    if certificate.get("record_target_met") is not False:
        raise AssertionError("incorrect record claim")
    return actual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE / "EXPECTED.json")
    parser.add_argument("--write-validation", type=Path)
    args = parser.parse_args()
    result = verify(json.loads(args.certificate.read_text()),
                    json.loads(args.expected.read_text()))
    output = {"status": "verified", **result}
    if args.write_validation:
        args.write_validation.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
