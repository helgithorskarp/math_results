"""Exact model for the Exoo--Ismailescu half-scale placement family.

The number field basis is (1, sqrt(3), sqrt(11), sqrt(33)).  A field
element is a tuple of four Fractions in that basis; a point is a pair of
field elements.  No floating-point arithmetic is used.
"""

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations


RADICANDS = (1, 3, 11, 33)
ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(0))
FOUR = (Q(4), Q(0), Q(0), Q(0))

# Rows [a,b,c,d] denote ((a sqrt(3)+b sqrt(11))/12,
#                        (c+d sqrt(33))/12).
ROWS = (
    (-2, 0, 0, 2), (2, 0, 0, 2), (0, 0, 0, 0), (0, 0, 0, 4),
    (0, 0, -6, 2), (0, 0, 6, 2), (-1, -3, 3, 3), (1, 3, 3, 3),
    (-3, -3, 3, 1), (3, 3, 3, 1), (-1, -3, -3, 1), (1, 3, -3, 1),
    (-4, 0, 0, 0), (4, 0, 0, 0), (3, -3, -3, 1), (-3, 3, -3, 1),
    (1, -3, -3, 3), (-1, 3, -3, 3), (1, -3, 3, 1), (-1, 3, 3, 1),
    (-2, 0, 6, 0), (2, 0, 6, 0), (-2, 0, -6, 0), (2, 0, -6, 0),
    (0, -6, 0, 2), (0, 6, 0, 2),
)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-a for a in value)


def sub(left, right):
    return add(left, neg(right))


def scale(value, factor):
    return tuple(factor * a for a in value)


def mul(left, right):
    result = [Q(0)] * 4
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i ^ j] += a * b * RADICANDS[i & j]
    return tuple(result)


def point_add(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def point_sub(left, right):
    return sub(left[0], right[0]), sub(left[1], right[1])


def point_scale(value, factor):
    return scale(value[0], factor), scale(value[1], factor)


def squared_norm(value):
    return add(mul(value[0], value[0]), mul(value[1], value[1]))


def inverse_norm(value):
    """Invert an element known to lie in Q(sqrt(33))."""
    if value[1] or value[2]:
        raise ValueError("squared norm lies outside Q(sqrt(33))")
    denominator = value[0] * value[0] - 33 * value[3] * value[3]
    if not denominator:
        raise ValueError("zero squared norm")
    return (value[0] / denominator, Q(0), Q(0), -value[3] / denominator)


def divide_by_norm(value, norm):
    return mul(value, inverse_norm(norm))


def reflect(point):
    return point[0], neg(point[1])


@lru_cache(maxsize=1)
def source_points():
    return tuple(
        ((Q(0), Q(a, 12), Q(b, 12), Q(0)),
         (Q(c, 12), Q(0), Q(0), Q(d, 12)))
        for a, b, c, d in ROWS
    )


def rotate(point, real, imaginary):
    return (
        sub(mul(real, point[0]), mul(imaginary, point[1])),
        add(mul(imaginary, point[0]), mul(real, point[1])),
    )


def make_placement(base, source_pair, target_pair, reflected):
    """Return (1/2) R(base)+t with the two requested coincidences."""
    prepared = tuple(map(reflect, base)) if reflected else base
    source_anchor = prepared[source_pair[0]]
    source_vector = point_scale(
        point_sub(prepared[source_pair[1]], source_anchor), Q(1, 2)
    )
    target_anchor = base[target_pair[0]]
    target_vector = point_sub(base[target_pair[1]], target_anchor)
    norm = squared_norm(source_vector)
    if norm != squared_norm(target_vector):
        raise ValueError("source and target segments have unequal lengths")

    # target_vector/source_vector in complex notation.
    real = divide_by_norm(
        add(mul(target_vector[0], source_vector[0]),
            mul(target_vector[1], source_vector[1])),
        norm,
    )
    imaginary = divide_by_norm(
        sub(mul(target_vector[1], source_vector[0]),
            mul(target_vector[0], source_vector[1])),
        norm,
    )
    if add(mul(real, real), mul(imaginary, imaginary)) != ONE:
        raise AssertionError("computed multiplier is not an exact rotation")
    moved = tuple(
        point_add(
            target_anchor,
            rotate(point_scale(point_sub(point, source_anchor), Q(1, 2)),
                   real, imaginary),
        )
        for point in prepared
    )
    if (moved[source_pair[0]] != base[target_pair[0]] or
            moved[source_pair[1]] != base[target_pair[1]]):
        raise AssertionError("placement failed its anchor coincidences")
    if len(set(moved)) != len(base):
        raise AssertionError("half-scale isometry identified two source points")
    return moved


def enumerate_placements():
    """Enumerate labeled specifications and quotient by moved point set."""
    base = source_points()
    if len(set(base)) != len(base):
        raise AssertionError("source coordinate rows are not distinct")
    pairs = tuple(combinations(range(len(base)), 2))
    norms = {
        pair: squared_norm(point_sub(base[pair[0]], base[pair[1]]))
        for pair in pairs
    }
    representatives = {}
    raw_count = 0
    for source_pair in pairs:
        for unordered_target in pairs:
            if norms[source_pair] != scale(norms[unordered_target], 4):
                continue
            for target_pair in (unordered_target, unordered_target[::-1]):
                for reflected in (False, True):
                    raw_count += 1
                    moved = make_placement(
                        base, source_pair, target_pair, reflected
                    )
                    key = tuple(sorted(moved))
                    representatives.setdefault(
                        key, (source_pair, target_pair, reflected, moved)
                    )
    placements = tuple(representatives[key] for key in sorted(representatives))
    return base, raw_count, placements


@lru_cache(maxsize=None)
def source_distance_edges(base=None):
    """Return the source's unit edges and length-two edges."""
    base = source_points() if base is None else base
    unit = []
    long = []
    for left, right in combinations(range(len(base)), 2):
        norm = squared_norm(point_sub(base[left], base[right]))
        if norm == ONE:
            unit.append((left, right))
        elif norm == FOUR:
            long.append((left, right))
    return tuple(unit), tuple(long)


def union_points(base, moved):
    points = list(base)
    index = {point: i for i, point in enumerate(points)}
    moved_indices = []
    for point in moved:
        if point not in index:
            index[point] = len(points)
            points.append(point)
        moved_indices.append(index[point])
    return tuple(points), tuple(moved_indices)


def unit_graph(base, moved):
    """Construct the complete strict unit-distance graph on base union moved.

    Base--base pairs and moved--moved pairs are classified once in the source.
    Every base--moved pair is tested directly in the number field.  These three
    origin cases cover every pair in the union, including intersection points.
    """
    points, moved_indices = union_points(base, moved)
    unit, long = source_distance_edges(base)
    edges = set(unit)
    for left, right in long:
        a, b = moved_indices[left], moved_indices[right]
        if a != b:
            edges.add(tuple(sorted((a, b))))
    for base_index, base_point in enumerate(base):
        for moved_index, moved_point in zip(moved_indices, moved):
            if base_index != moved_index and squared_norm(
                    point_sub(base_point, moved_point)) == ONE:
                edges.add(tuple(sorted((base_index, moved_index))))
    return points, tuple(sorted(edges))


def direct_unit_edges(points):
    """Definition-level edge construction, used by the controls."""
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if squared_norm(point_sub(points[left], points[right])) == ONE
    )


def descriptor_digest(placements):
    digest = sha256()
    for source, target, reflected, _moved in placements:
        digest.update(
            f"{source[0]},{source[1]}:{target[0]},{target[1]}:{int(reflected)}\n".encode()
        )
    return digest.hexdigest()


def point_set_digest(placements):
    """Hash all canonical exact moved point sets without serializing a dump."""
    digest = sha256()
    for _source, _target, _reflected, moved in placements:
        for point in sorted(moved):
            for coordinate in point:
                for coefficient in coordinate:
                    digest.update(
                        f"{coefficient.numerator}/{coefficient.denominator},".encode()
                    )
                digest.update(b";")
            digest.update(b"|")
        digest.update(b"\n")
    return digest.hexdigest()
