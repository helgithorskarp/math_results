#!/usr/bin/env python3
"""Independent exact review of the complete Parts373 boundary-lens support.

No target module is imported.  Base-field arithmetic uses the quadratic tower
Q(sqrt(3))(sqrt(11)); rational intervals exclude noncontacts, while SymPy
checks the comparatively few surviving mixed-radical equalities.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import isqrt
import json
from pathlib import Path

import sympy as sp


TARGET = "hadwiger_nelson_parts373_boundary_lens_stop"
POINTS_SHA = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
CERTIFICATE_SHA = "8edec4d854e010106643619b561aee30f2e62bbb5e0b4b74037cb0db4f641d09"
H = tuple(v for v in range(374) if v != 310)
B = (
    0, 150, 169, 243, 244, 245, 287, 296, 344, 345, 346, 357,
    358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368,
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest_file(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def digest_json(value):
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return sha256(raw).hexdigest()


# Q3 pairs represent a+b*sqrt(3).  K pairs represent a+b*sqrt(11), a,b in Q3.
Q3_ZERO = (F(0), F(0))
Q3_ONE = (F(1), F(0))
K_ZERO = (Q3_ZERO, Q3_ZERO)
K_ONE = (Q3_ONE, Q3_ZERO)


def q3_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def q3_neg(x):
    return -x[0], -x[1]


def q3_sub(x, y):
    return q3_add(x, q3_neg(y))


def q3_scale(x, scalar):
    return scalar * x[0], scalar * x[1]


def q3_mul(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def q3_inverse(x):
    denominator = x[0] * x[0] - 3 * x[1] * x[1]
    require(denominator != 0, "nonzero Q(sqrt(3)) denominator")
    return x[0] / denominator, -x[1] / denominator


def k_add(x, y):
    return q3_add(x[0], y[0]), q3_add(x[1], y[1])


def k_neg(x):
    return q3_neg(x[0]), q3_neg(x[1])


def k_sub(x, y):
    return k_add(x, k_neg(y))


def k_scale(x, scalar):
    return q3_scale(x[0], scalar), q3_scale(x[1], scalar)


def k_mul(x, y):
    return (
        q3_add(q3_mul(x[0], y[0]), q3_scale(q3_mul(x[1], y[1]), 11)),
        q3_add(q3_mul(x[0], y[1]), q3_mul(x[1], y[0])),
    )


def k_inverse(x):
    denominator = q3_sub(q3_mul(x[0], x[0]), q3_scale(q3_mul(x[1], x[1]), 11))
    inverse_denominator = q3_inverse(denominator)
    result = (
        q3_mul(x[0], inverse_denominator),
        q3_neg(q3_mul(x[1], inverse_denominator)),
    )
    require(k_mul(x, result) == K_ONE, "exact K inverse")
    return result


def k_div(x, y):
    return k_mul(x, k_inverse(y))


def k_from_flat(values):
    require(len(values) == 4, "four K coefficients")
    return ((F(values[0]), F(values[1])), (F(values[2]), F(values[3])))


def k_flat(x):
    return x[0][0], x[0][1], x[1][0], x[1][1]


def vec_add(x, y):
    return k_add(x[0], y[0]), k_add(x[1], y[1])


def vec_sub(x, y):
    return k_sub(x[0], y[0]), k_sub(x[1], y[1])


def vec_scale(x, scalar):
    return k_scale(x[0], scalar), k_scale(x[1], scalar)


def dot(x, y):
    return k_add(k_mul(x[0], y[0]), k_mul(x[1], y[1]))


def interval_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def interval_mul(x, y):
    values = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(values), max(values)


def interval_scale(x, scalar):
    values = scalar * x[0], scalar * x[1]
    return min(values), max(values)


def interval_sub(x, y):
    return x[0] - y[1], x[1] - y[0]


def interval_square(x):
    if x[0] <= 0 <= x[1]:
        return F(0), max(x[0] * x[0], x[1] * x[1])
    values = x[0] * x[0], x[1] * x[1]
    return min(values), max(values)


@lru_cache(None)
def rational_sqrt_bounds(value, bits):
    require(value >= 0, "nonnegative rational square root")
    denominator = 1 << bits
    integer = isqrt((value.numerator << (2 * bits)) // value.denominator)
    lower = F(integer, denominator)
    upper = lower if lower * lower == value else F(integer + 1, denominator)
    require(lower * lower <= value <= upper * upper, "outward square-root bounds")
    return lower, upper


@lru_cache(None)
def q3_interval(x, bits):
    radical = rational_sqrt_bounds(F(3), bits)
    return interval_add((x[0], x[0]), interval_scale(radical, x[1]))


@lru_cache(None)
def k_interval(x, bits):
    # This nested evaluation preserves the tower structure rather than bounding
    # sqrt(33) as an unrelated radical.
    radical = rational_sqrt_bounds(F(11), bits)
    return interval_add(q3_interval(x[0], bits),
                        interval_mul(q3_interval(x[1], bits), radical))


def k_sign(x):
    if x == K_ZERO:
        return 0
    for bits in (80, 160, 320, 640):
        lower, upper = k_interval(x, bits)
        if lower > 0:
            return 1
        if upper < 0:
            return -1
    raise AssertionError("base-field sign was not isolated")


@lru_cache(None)
def positive_k_sqrt_interval(x, bits):
    if x == K_ZERO:
        return F(0), F(0)
    lower, upper = k_interval(x, bits + 16)
    require(lower > 0, "positive lens radicand")
    return rational_sqrt_bounds(lower, bits)[0], rational_sqrt_bounds(upper, bits)[1]


# A point is (A,U,r), denoting A + U*sqrt(r), with A,U in K^2.
def point_box(point, bits):
    base, coefficient, radicand = point
    radical = positive_k_sqrt_interval(radicand, bits + 16)
    axes = []
    for a, u in zip(base, coefficient):
        axes.append(interval_add(k_interval(a, bits + 16),
                                 interval_mul(k_interval(u, bits + 16), radical)))
    return tuple(axes)


def boxes_overlap(p, q):
    return all(not (x[1] < y[0] or y[1] < x[0]) for x, y in zip(p, q))


def distance_interval(p, q):
    total = (F(0), F(0))
    for x, y in zip(p, q):
        total = interval_add(total, interval_square(interval_sub(x, y)))
    return total


SQRT3 = sp.sqrt(3)
SQRT11 = sp.sqrt(11)


@lru_cache(None)
def k_sympy(x):
    values = [sp.Rational(v.numerator, v.denominator) for v in k_flat(x)]
    return values[0] + values[1] * SQRT3 + values[2] * SQRT11 + values[3] * SQRT3 * SQRT11


@lru_cache(None)
def point_sympy(point):
    base, coefficient, radicand = point
    radical = sp.sqrt(k_sympy(radicand))
    return tuple(k_sympy(a) + k_sympy(u) * radical
                 for a, u in zip(base, coefficient))


def sympy_zero(expression):
    reduced = sp.radsimp(sp.expand(expression))
    if reduced == 0:
        return True
    return sp.simplify(reduced) == 0


def exact_point_equal(p, q):
    x, y = point_sympy(p), point_sympy(q)
    return sympy_zero(x[0] - y[0]) and sympy_zero(x[1] - y[1])


def exact_unit(p, q):
    if p[1] == (K_ZERO, K_ZERO) and q[1] == (K_ZERO, K_ZERO):
        return dot(vec_sub(p[0], q[0]), vec_sub(p[0], q[0])) == K_ONE
    x, y = point_sympy(p), point_sympy(q)
    expression = (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 - 1
    return sympy_zero(expression)


def arithmetic_controls():
    basis = (
        K_ONE,
        ((F(0), F(1)), Q3_ZERO),
        (Q3_ZERO, Q3_ONE),
        (Q3_ZERO, (F(0), F(1))),
    )
    for left, right in product(basis, repeat=2):
        difference = sp.expand(k_sympy(k_mul(left, right))
                               - k_sympy(left) * k_sympy(right))
        require(difference == 0, "tower multiplication agrees with definition")
    test = ((F(7, 5), F(-2, 3)), (F(4, 7), F(1, 11)))
    require(k_mul(test, k_inverse(test)) == K_ONE, "tower inversion control")
    for value in (F(0), F(1), F(2), F(999999, 1000000), F(10**40 + 1, 10**40)):
        lower, upper = rational_sqrt_bounds(value, 96)
        require(lower * lower <= value <= upper * upper,
                "directed rational-square-root control")

    # The equality checker must recognize dependent positive radicals rather
    # than treating sqrt(2) and sqrt(6) as independent formal generators.
    sqrt3 = ((F(0), F(1)), Q3_ZERO)
    zero_vector = (K_ZERO, K_ZERO)
    left = (zero_vector, (K_ONE, sqrt3), k_scale(K_ONE, 2))
    right = (zero_vector, (k_scale(sqrt3, F(1, 3)), K_ONE), k_scale(K_ONE, 6))
    require(exact_point_equal(left, right), "dependent-radical equality control")
    shifted = ((k_scale(K_ONE, -2), K_ZERO), zero_vector, K_ZERO)
    positive_root = (zero_vector, (K_ONE, K_ZERO), k_scale(K_ONE, 4))
    require(not exact_point_equal(shifted, positive_root),
            "positive square-root branch control")


def refine_separation(p, q, target):
    for bits in (192, 384, 768):
        interval = distance_interval(point_box(p, bits), point_box(q, bits))
        if target < interval[0] or target > interval[1]:
            return bits
    raise AssertionError("non-equality was not independently separated")


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left != right:
            if left > right:
                left, right = right, left
            self.parent[right] = left


def point_key(point):
    base, coefficient, radicand = point
    return [
        [[str(v) for v in k_flat(axis)] for axis in base],
        [[str(v) for v in k_flat(axis)] for axis in coefficient],
        [str(v) for v in k_flat(radicand)],
    ]


def read_host(points_path):
    require(digest_file(points_path) == POINTS_SHA, "frozen coordinate source hash")
    rows = [
        tuple(map(int, line.split()))
        for line in points_path.read_text().splitlines()
        if line and not line.startswith("#")
    ]
    require(len(rows) == 509 and all(len(row) == 16 for row in rows),
            "509 rows with sixteen coefficients")
    host = {}
    forbidden = (2, 3, 6, 7, 10, 11, 14, 15)
    for label in H:
        row = rows[label]
        require(all(row[index] == 0 for index in forbidden), "host lies in K^2")
        x = k_from_flat(tuple(F(row[index], 96) for index in (0, 1, 4, 5)))
        y = k_from_flat(tuple(F(row[index], 96) for index in (8, 9, 12, 13)))
        host[label] = (x, y)
    require(len(set(host.values())) == 373, "distinct exact host coordinates")
    return host


def generate_occurrences(host):
    zero_vector = (K_ZERO, K_ZERO)
    occurrences = [(host[label], zero_vector, K_ZERO) for label in H]
    origins = [["host", label] for label in H]
    route_occurrences = []
    pair_classes = {"secant": 0, "tangent": 0, "none": 0}
    for a, b in combinations(B, 2):
        delta = vec_sub(host[b], host[a])
        squared = dot(delta, delta)
        require(k_sign(squared) > 0, "distinct boundary pins")
        comparison = k_sign(k_sub(squared, k_scale(K_ONE, 4)))
        if comparison > 0:
            pair_classes["none"] += 1
            continue
        midpoint = vec_scale(vec_add(host[a], host[b]), F(1, 2))
        if comparison == 0:
            pair_classes["tangent"] += 1
            signs = (0,)
            radicand = K_ZERO
        else:
            pair_classes["secant"] += 1
            signs = (-1, 1)
            radicand = k_sub(k_div(k_scale(K_ONE, 4), squared), K_ONE)
            require(k_sign(radicand) > 0, "secant lens radicand")
        for sign in signs:
            coefficient = (
                k_scale(delta[1], F(-sign, 2)),
                k_scale(delta[0], F(sign, 2)),
            )
            occurrence = (midpoint, coefficient, radicand)
            index = len(occurrences)
            occurrences.append(occurrence)
            origins.append(["lens", a, b, sign])
            route_occurrences.append((a, b, sign, index))
    require(pair_classes == {"secant": 81, "tangent": 24, "none": 148},
            "complete boundary-pair classification")
    require(len(route_occurrences) == 186, "all circle-intersection occurrences")
    return occurrences, origins, route_occurrences, pair_classes


def merge_occurrences(occurrences, origins, route_occurrences, initial_bits):
    boxes = [point_box(point, initial_bits) for point in occurrences]
    union_find = UnionFind(len(occurrences))
    overlap_pairs = exact_equal_pairs = separated_overlap_pairs = 0
    for left, right in combinations(range(len(occurrences)), 2):
        if not boxes_overlap(boxes[left], boxes[right]):
            continue
        overlap_pairs += 1
        if exact_point_equal(occurrences[left], occurrences[right]):
            union_find.union(left, right)
            exact_equal_pairs += 1
        else:
            # Coordinate-box overlap does not itself prove inequality.  A
            # positive squared-distance lower bound at higher precision does.
            refine_separation(occurrences[left], occurrences[right], F(0))
            separated_overlap_pairs += 1

    classes = {}
    for index in range(len(occurrences)):
        classes.setdefault(union_find.find(index), []).append(index)
    representatives = sorted(min(items) for items in classes.values())
    class_sizes = Counter(len(items) for items in classes.values())
    occurrence_to_merged = {}
    for merged_index, representative in enumerate(representatives):
        root = union_find.find(representative)
        for occurrence_index in classes[root]:
            occurrence_to_merged[occurrence_index] = merged_index
    points = [occurrences[index] for index in representatives]
    merged_origins = [origins[index] for index in representatives]
    routes = [
        [a, b, sign, occurrence_to_merged[index]]
        for a, b, sign, index in route_occurrences
    ]
    require(len(points) == 488, "exact collision merging gives 488 points")
    require(len(occurrences) - len(points) == 71, "71 redundant occurrences")
    require(len(points) - len(H) == 115, "115 new physical points")
    return {
        "points": points,
        "origins": merged_origins,
        "routes": routes,
        "overlap_pairs": overlap_pairs,
        "exact_equal_pairs": exact_equal_pairs,
        "separated_overlap_pairs": separated_overlap_pairs,
        "collision_class_size_distribution": {
            str(size): count for size, count in sorted(class_sizes.items())
        },
    }


def reconstruct_edges(points, bits):
    boxes = [point_box(point, bits) for point in points]
    edges = []
    interval_rejections = symbolic_checks = refined_candidates = 0
    possible_collisions = 0
    for left, right in combinations(range(len(points)), 2):
        distance = distance_interval(boxes[left], boxes[right])
        if distance[0] <= 0 <= distance[1]:
            possible_collisions += 1
            require(not exact_point_equal(points[left], points[right]),
                    "missed merged collision")
            refine_separation(points[left], points[right], F(0))
        if not (distance[0] <= 1 <= distance[1]):
            interval_rejections += 1
            continue
        if left >= len(H) or right >= len(H):
            symbolic_checks += 1
        if exact_unit(points[left], points[right]):
            edges.append([left, right])
        else:
            refine_separation(points[left], points[right], F(1))
            refined_candidates += 1
    require(possible_collisions == 0, "merged point boxes are pairwise disjoint")
    require(len(edges) == 2200, "complete strict unit-edge count")
    require(interval_rejections + len(edges) + refined_candidates == 118828,
            "all merged pairs decided")
    return edges, {
        "interval_nonunit_rejections": interval_rejections,
        "mixed_radical_symbolic_unit_checks": symbolic_checks,
        "refined_nonunit_candidates": refined_candidates,
        "possible_collision_intervals_after_merge": possible_collisions,
    }


def verify(source, output, bits):
    source = source.resolve()
    arithmetic_controls()
    require(digest_file(source / "certificate.json") == CERTIFICATE_SHA,
            "frozen certificate hash")
    host = read_host(source / "points.tsv")
    occurrences, origins, route_occurrences, pair_classes = generate_occurrences(host)
    merged = merge_occurrences(occurrences, origins, route_occurrences, bits)
    points, routes = merged["points"], merged["routes"]
    edges, edge_stats = reconstruct_edges(points, bits)
    edge_set = {tuple(edge) for edge in edges}
    host_position = {label: index for index, label in enumerate(H)}
    for a, b, _, point_index in routes:
        require(tuple(sorted((host_position[a], point_index))) in edge_set,
                "first defining circle contact")
        require(tuple(sorted((host_position[b], point_index))) in edge_set,
                "second defining circle contact")

    host_edges = [edge for edge in edges if edge[1] < len(H)]
    host_new = [edge for edge in edges if edge[0] < len(H) <= edge[1]]
    new_new = [edge for edge in edges if edge[0] >= len(H)]
    actual_boundary = sorted({H[left] for left, _ in host_new})
    extra_boundary = sorted(set(actual_boundary) - set(B))
    missing_marked = sorted(set(B) - set(actual_boundary))
    require(len(host_edges) == 1856, "host edge count")
    require(len(host_new) == 308 and len(new_new) == 36, "new-edge split")
    require(len(actual_boundary) == 80 and len(extra_boundary) == 58,
            "complete actual host interface")
    require(missing_marked == [0], "origin is the sole unused marked pin")

    require(digest_json(edges) ==
            "800eaa425b8ba5371a93b7370a18c632ef562d0c967481be7acdd49e6d22441f",
            "entry-level edge identity")
    require(digest_json(routes) ==
            "e01a98146d5f70aba9595648e9523e237d5f59e90d28de193e6b1fac9c29a1e6",
            "entry-level route identity")
    require(digest_json([point_key(point) for point in points]) ==
            "10e010eeb24478d67b17a2b2fc5e860ca26e962aa24593e0d59b7db800e994e4",
            "entry-level point-formula identity")
    require(digest_json(merged["origins"]) ==
            "b040ddca9799f6ea2f4274ae91b707cc3efdf830cea69aab25959ee118600e1f",
            "entry-level representative-origin identity")

    certificate = json.loads((source / "certificate.json").read_text())
    word = certificate["colour4"]
    require(len(word) == len(points) and set(word) <= set("0123"),
            "four-colour word domain")
    require(all(word[a] != word[b] for a, b in edges),
            "four-colour word is proper on every physical unit edge")
    require(word[:len(H)] == certificate["host_word"], "full host word retained")
    require("".join(word[host_position[v]] for v in B) == certificate["boundary_word"],
            "listed receiving word retained")

    labels = certificate["three_colour_obstruction_labels"]
    obstruction_vertices = [host_position[label] for label in labels]
    induced = [
        [obstruction_vertices.index(a), obstruction_vertices.index(b)]
        for a, b in edges if a in obstruction_vertices and b in obstruction_vertices
    ]
    require(len(induced) == 11, "seven-point induced obstruction has eleven edges")
    three_words = 0
    for assignment in product(range(3), repeat=7):
        three_words += 1
        require(not all(assignment[a] != assignment[b] for a, b in induced),
                "no proper three-colouring of the obstruction")
    require(three_words == 2187, "all named three-colourings exhausted")

    result = {
        "verdict": "accept_at_restricted_family_scope",
        "base_field_representation": "Q(sqrt(3))(sqrt(11)) quadratic tower",
        "mixed_radical_checker": "SymPy 1.14.0 exact simplification",
        "interval_bits": bits,
        "boundary_pairs": 253,
        "pair_classes": pair_classes,
        "formal_lens_occurrences": len(route_occurrences),
        "unmerged_occurrences_including_host": len(occurrences),
        "collision_overlap_pairs": merged["overlap_pairs"],
        "symbolic_collision_equalities": merged["exact_equal_pairs"],
        "separated_collision_box_overlaps": merged["separated_overlap_pairs"],
        "collision_class_size_distribution": merged["collision_class_size_distribution"],
        "physical_points": len(points),
        "new_physical_points": len(points) - len(H),
        "all_merged_pairs": len(points) * (len(points) - 1) // 2,
        "unit_edges": len(edges),
        "host_unit_edges": len(host_edges),
        "host_new_edges": len(host_new),
        "new_new_edges": len(new_new),
        "actual_host_boundary": actual_boundary,
        "actual_host_boundary_count": len(actual_boundary),
        "extra_host_boundary_outside_marked_B": extra_boundary,
        "extra_host_boundary_count": len(extra_boundary),
        "marked_boundary_without_new_contact": missing_marked,
        "edge_sha256": digest_json(edges),
        "route_sha256": digest_json(routes),
        "point_formula_sha256": digest_json([point_key(point) for point in points]),
        "origins_sha256": digest_json(merged["origins"]),
        **edge_stats,
        "defining_contacts_checked": 2 * len(routes),
        "proper_four_word_checked": True,
        "proper_boundary_word": certificate["boundary_word"],
        "three_colour_assignments_exhausted": three_words,
        "chromatic_number": 4,
        "complete_two_pin_lens_family_four_colourable": True,
        "arithmetic_and_dependent_radical_controls_checked": True,
        "replacement_or_record_candidate": False,
        "points_source_sha256": digest_file(source / "points.tsv"),
        "certificate_sha256": digest_file(source / "certificate.json"),
    }
    expected = Path(__file__).resolve().parent / "EXPECTED.json"
    if expected.exists():
        for key, value in json.loads(expected.read_text()).items():
            require(result.get(key) == value, f"frozen review expectation: {key}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=here.parent / TARGET)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bits", type=int, choices=(96, 128, 192), default=128)
    args = parser.parse_args()
    print(json.dumps(verify(args.source, args.output, args.bits), indent=2))


if __name__ == "__main__":
    main()
