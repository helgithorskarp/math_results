#!/usr/bin/env python3
"""Independent exact review checker for Discovery Net h4005.

This implementation does not import the target package.  It enumerates the
exceptional rotations by direct circle-line intersection (rather than the
target verifier's half-angle parametrization) and represents each physical
point in a two-dimensional quadratic field.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_hexagon_rotational_sums"
CERTIFICATE_SHA256 = "9fd7e3c6883ce823af804b8bbc3dbbf1f4f7a819157e7f3a9925825c7925bac8"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_decomposition(number: int) -> tuple[int, int]:
    """Return f,s with number=f^2*s and s squarefree."""
    require(isinstance(number, int) and number >= 0, "negative radicand")
    if number == 0:
        return 0, 0
    factor = 1
    squarefree = 1
    divisor = 2
    remainder = number
    while divisor * divisor <= remainder:
        exponent = 0
        while remainder % divisor == 0:
            remainder //= divisor
            exponent += 1
        factor *= divisor ** (exponent // 2)
        if exponent % 2:
            squarefree *= divisor
        divisor += 1
    if remainder > 1:
        squarefree *= remainder
    return factor, squarefree


Element = tuple[Q, Q]  # a+b*sqrt(s), with s held by the caller


def add(left: Element, right: Element) -> Element:
    return left[0] + right[0], left[1] + right[1]


def scale(multiplier: Q | int, value: Element) -> Element:
    return multiplier * value[0], multiplier * value[1]


def multiply(left: Element, right: Element, field: int) -> Element:
    return (left[0] * right[0] + field * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def normalized_rotation(field: int, real: Element, imag_over_sqrt3: Element) -> "Rotation":
    if field == 1:
        real = (real[0] + real[1], Q(0))
        imag_over_sqrt3 = (imag_over_sqrt3[0] + imag_over_sqrt3[1], Q(0))
        field = 0
    require(field == 0 or field > 1, "noncanonical quadratic field")
    if field == 0:
        require(real[1] == imag_over_sqrt3[1] == 0, "radical in rational field")
    if real[1] == 0 and imag_over_sqrt3[1] == 0:
        field = 0
    return Rotation(field, Q(real[0]), Q(real[1]),
                    Q(imag_over_sqrt3[0]), Q(imag_over_sqrt3[1]))


@dataclass(frozen=True, order=True)
class Rotation:
    """u=(x0+x1 sqrt(s))+i sqrt(3)(y0+y1 sqrt(s))."""

    field: int
    x0: Q
    x1: Q
    y0: Q
    y1: Q

    @property
    def real(self) -> Element:
        return self.x0, self.x1

    @property
    def imag_over_sqrt3(self) -> Element:
        return self.y0, self.y1

    def conjugate(self) -> "Rotation":
        return Rotation(self.field, self.x0, self.x1, -self.y0, -self.y1)

    def times_omega(self) -> "Rotation":
        return normalized_rotation(
            self.field,
            scale(Q(1, 2), add(self.real, scale(-3, self.imag_over_sqrt3))),
            scale(Q(1, 2), add(self.real, self.imag_over_sqrt3)),
        )


def norm_squared(rotation: Rotation) -> Element:
    return add(multiply(rotation.real, rotation.real, rotation.field),
               scale(3, multiply(rotation.imag_over_sqrt3,
                                 rotation.imag_over_sqrt3, rotation.field)))


def parse_rotation(row: list[int]) -> Rotation:
    require(isinstance(row, list) and len(row) == 6 and
            all(type(value) is int for value in row), "rotation row format")
    field, a, b, c, d, denominator = row
    require(denominator > 0 and math.gcd(a, b, c, d, denominator) == 1,
            "rotation row is not primitive")
    if field == 0:
        require(b == d == 0, "rational rotation has radical coefficients")
    else:
        factor, squarefree = squarefree_decomposition(field)
        require(factor == 1 and squarefree == field and field > 1,
                "rotation field is not squarefree")
    rotation = normalized_rotation(
        field,
        (Q(a, denominator), Q(b, denominator)),
        (Q(c, denominator), Q(d, denominator)),
    )
    require(rotation.field == field, "rotation uses a reducible field")
    require(norm_squared(rotation) == (Q(1), Q(0)), "rotation is not unit")
    return rotation


def hexagon() -> list[tuple[int, int]]:
    return [(a, b) for a in range(-2, 3) for b in range(-2, 3)
            if max(abs(a), abs(b), abs(a + b)) <= 2]


def eisenstein_norm(vector: tuple[int, int]) -> int:
    a, b = vector
    return a * a + a * b + b * b


def product_data(first: tuple[int, int], second: tuple[int, int]) -> tuple[int, int, int, int, int]:
    a, b = first
    c, d = second
    m = eisenstein_norm(first)
    n = eisenstein_norm(second)
    p = 2 * a * c + a * d + b * c + 2 * b * d
    q = b * c - a * d
    constant = 1 - m - n
    require(p * p + 3 * q * q == 4 * m * n, "Eisenstein product identity")
    return m, n, p, q, constant


def direct_event_roots(differences: list[tuple[int, int]]) -> tuple[set[Rotation], dict[str, int]]:
    """Intersect pX+3qY=c directly with X^2+3Y^2=1."""
    roots: set[Rotation] = set()
    feasible_pairs = tangencies = algebraic_occurrences = 0
    for first in differences:
        if first == (0, 0):
            continue
        for second in differences:
            if second == (0, 0):
                continue
            m, n, p, q, constant = product_data(first, second)
            denominator = 4 * m * n
            discriminant = denominator - constant * constant
            if discriminant < 0:
                continue
            feasible_pairs += 1
            tangencies += discriminant == 0
            radical_factor, field = squarefree_decomposition(3 * discriminant)
            for sign in (-1, 1):
                real = (Q(p * constant, denominator),
                        Q(-sign * q * radical_factor, denominator))
                imag = (Q(q * constant, denominator),
                        Q(sign * p * radical_factor, 3 * denominator))
                root = normalized_rotation(field, real, imag)
                require(norm_squared(root) == (Q(1), Q(0)), "event root is not unit")
                roots.add(root)
                algebraic_occurrences += 1
    return roots, {
        "ordered_difference_pairs": 3600,
        "feasible_circle_line_pairs": feasible_pairs,
        "tangent_pairs": tangencies,
        "root_occurrences_with_tangent_multiplicity": algebraic_occurrences,
    }


def collision_roots(differences: list[tuple[int, int]]) -> set[Rotation]:
    roots: set[Rotation] = set()
    for first in differences:
        if first == (0, 0):
            continue
        for second in differences:
            if second == (0, 0):
                continue
            m, n, p, q, _ = product_data(first, second)
            if m == n:
                root = normalized_rotation(
                    0, (Q(-p, 2 * n), Q(0)), (Q(-q, 2 * n), Q(0)))
                require(norm_squared(root) == (Q(1), Q(0)), "collision root is not unit")
                roots.add(root)
    return roots


def orbit(rotation: Rotation) -> set[Rotation]:
    result: set[Rotation] = set()
    current = rotation
    for _ in range(6):
        result.add(current)
        result.add(current.conjugate())
        current = current.times_omega()
    require(current == rotation, "sixfold action does not close")
    return result


def lattice_coordinate(vector: tuple[int, int]) -> tuple[Q, Q]:
    a, b = vector
    return Q(2 * a + b, 2), Q(b, 2)


Point = tuple[Element, Element]  # real coordinate, imaginary coordinate / sqrt(3)


def point(first: tuple[int, int], second: tuple[int, int], rotation: Rotation) -> Point:
    first_real, first_imag = lattice_coordinate(first)
    second_real, second_imag = lattice_coordinate(second)
    real = add((first_real, Q(0)),
               add(scale(second_real, rotation.real),
                   scale(-3 * second_imag, rotation.imag_over_sqrt3)))
    imag = add((first_imag, Q(0)),
               add(scale(second_imag, rotation.real),
                   scale(second_real, rotation.imag_over_sqrt3)))
    return real, imag


def point_difference(left: Point, right: Point) -> Point:
    return (add(left[0], scale(-1, right[0])),
            add(left[1], scale(-1, right[1])))


def point_norm_squared(value: Point, field: int) -> Element:
    return add(multiply(value[0], value[0], field),
               scale(3, multiply(value[1], value[1], field)))


def base_graph(patch: list[tuple[int, int]]) -> tuple[set[tuple[int, int]], list[set[int]]]:
    edges = {
        (i, j)
        for i in range(len(patch))
        for j in range(i)
        if eisenstein_norm((patch[i][0] - patch[j][0],
                            patch[i][1] - patch[j][1])) == 1
    }
    adjacency = [set() for _ in patch]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    return edges, adjacency


def fixed_triangle_colouring_count(adjacency: list[set[int]]) -> int:
    triangle = next((a, b, c)
                    for a in range(len(adjacency))
                    for b in adjacency[a] if a < b
                    for c in adjacency[a] & adjacency[b] if b < c)
    assigned = {triangle[0]: 0, triangle[1]: 1, triangle[2]: 2}

    def search() -> int:
        if len(assigned) == len(adjacency):
            return 1
        choices = []
        for vertex in range(len(adjacency)):
            if vertex in assigned:
                continue
            forbidden = {assigned[n] for n in adjacency[vertex] if n in assigned}
            available = tuple(colour for colour in range(3) if colour not in forbidden)
            if not available:
                return 0
            choices.append((len(available), -len(adjacency[vertex]), vertex, available))
        _, _, vertex, available = min(choices)
        total = 0
        for colour in available:
            assigned[vertex] = colour
            total += search()
            assigned.pop(vertex)
        return total

    return search()


def audit_case(patch: list[tuple[int, int]], row: dict) -> tuple[dict, dict[int, tuple[str, int, int]]]:
    rotation = parse_rotation(row["angle"])
    addresses = [(first, second) for first in patch for second in patch]
    points = [point(first, second, rotation) for first, second in addresses]
    word = row["colours"]
    require(isinstance(word, str) and len(word) == len(addresses) and
            set(word) <= set("0123"), "malformed colour word")
    declared_chi = row["chi"]
    require(type(declared_chi) is int and declared_chi in (3, 4) and
            all(int(colour) < declared_chi for colour in word), "colour palette")

    physical_id: dict[Point, int] = {}
    label_to_physical = []
    for physical_point in points:
        if physical_point not in physical_id:
            physical_id[physical_point] = len(physical_id)
        label_to_physical.append(physical_id[physical_point])

    patterns = {
        sign: [(first[0] - first[1] + sign * (second[0] - second[1])) % 3
               for first, second in addresses]
        for sign in (-1, 1)
    }
    failures: dict[int, tuple[str, int, int]] = {}
    physical_edges: set[tuple[int, int]] = set()
    coincidences = unit_label_pairs = checked_pairs = 0
    for i in range(len(points)):
        for j in range(i):
            checked_pairs += 1
            if points[i] == points[j]:
                coincidences += 1
                require(word[i] == word[j], "colour word does not descend through a coincidence")
                for sign, pattern in patterns.items():
                    if pattern[i] != pattern[j] and sign not in failures:
                        failures[sign] = ("collision", j, i)
                continue
            difference = point_difference(points[i], points[j])
            if point_norm_squared(difference, rotation.field) == (Q(1), Q(0)):
                unit_label_pairs += 1
                require(word[i] != word[j], "colour word is improper on a unit pair")
                physical_edges.add(tuple(sorted((label_to_physical[i], label_to_physical[j]))))
                for sign, pattern in patterns.items():
                    if pattern[i] == pattern[j] and sign not in failures:
                        failures[sign] = ("unit_edge", j, i)

    valid_patterns = sorted(set(patterns) - set(failures))
    require((declared_chi == 3) == bool(valid_patterns), "wrong exact chromatic class")
    require(len(physical_id) == row["vertices"] and len(physical_edges) == row["edges"],
            "wrong physical graph counts")
    return {
        "angle": row["angle"],
        "orbit_size": len(orbit(rotation)),
        "vertices": len(physical_id),
        "edges": len(physical_edges),
        "chi": declared_chi,
        "valid_three_colour_signs": valid_patterns,
        "coincident_label_pairs": coincidences,
        "unit_label_pairs": unit_label_pairs,
        "checked_label_pairs": checked_pairs,
    }, failures


def generic_fixture(patch: list[tuple[int, int]], roots: set[Rotation]) -> dict[str, int]:
    # u=i is represented by Y=sqrt(3)/3 in u=X+i*sqrt(3)Y.
    rotation = normalized_rotation(3, (Q(0), Q(0)), (Q(0), Q(1, 3)))
    require(norm_squared(rotation) == (Q(1), Q(0)) and rotation not in roots,
            "u=i is not a generic unit rotation")
    addresses = [(first, second) for first in patch for second in patch]
    points = [point(first, second, rotation) for first, second in addresses]
    require(len(set(points)) == 361, "generic fixture has a collision")
    colours = [(first[0] - first[1] + second[0] - second[1]) % 3
               for first, second in addresses]
    edges = 0
    for i in range(len(points)):
        for j in range(i):
            if point_norm_squared(point_difference(points[i], points[j]), rotation.field) == (Q(1), Q(0)):
                edges += 1
                require(colours[i] != colours[j], "generic residue word is improper")
    require(edges == 1596, "generic edge count")
    return {"vertices": len(points), "edges": edges, "checked_label_pairs": 64_980}


def validate(certificate: dict) -> dict:
    require(certificate.get("family") == "H2+uH2; |u|=1; all strict unit edges",
            "wrong family")
    rows = certificate.get("cases")
    require(isinstance(rows, list) and len(rows) == 15, "wrong representative count")

    patch = hexagon()
    require(len(patch) == 19, "hexagon order")
    patch_set = set(patch)
    require({(-b, a + b) for a, b in patch} == patch_set, "omega does not preserve H")
    require({(a + b, -b) for a, b in patch} == patch_set, "conjugation does not preserve H")
    base_edges, base_adjacency = base_graph(patch)
    require(len(base_edges) == 42 and all(base_adjacency), "base graph census")
    fixed_count = fixed_triangle_colouring_count(base_adjacency)
    require(fixed_count == 1, "H is not uniquely three-colourable with a fixed triangle")
    residue = [(a - b) % 3 for a, b in patch]
    require(all(residue[i] != residue[j] for i, j in base_edges), "base residue colouring")

    differences = sorted({(a - c, b - d) for a, b in patch for c, d in patch})
    require(len(differences) == 61, "difference-set order")
    roots, root_stats = direct_event_roots(differences)
    require(len(roots) == 174, "exceptional-rotation count")
    collision_set = collision_roots(differences)
    require(collision_set <= roots, "a collision lies outside the edge-event set")

    expanded: set[Rotation] = set()
    case_orbits: list[set[Rotation]] = []
    for row in rows:
        current_orbit = orbit(parse_rotation(row["angle"]))
        require(not expanded.intersection(current_orbit), "representative orbits overlap")
        expanded.update(current_orbit)
        case_orbits.append(current_orbit)
    require(expanded == roots, "certificate orbits do not equal the direct root census")

    case_receipts = []
    witness_receipts = []
    for row in rows:
        case_receipt, failures = audit_case(patch, row)
        case_receipts.append(case_receipt)
        witness_receipts.append(failures)
    four_rotations = sum(receipt["orbit_size"] for receipt in case_receipts
                         if receipt["chi"] == 4)
    require(four_rotations == 48, "four-chromatic rotation count")
    generic = generic_fixture(patch, roots)

    return {
        "status": "INDEPENDENT_H4005_ACCEPT",
        "target_certificate_sha256": CERTIFICATE_SHA256,
        "base": {
            "vertices": len(patch),
            "edges": len(base_edges),
            "fixed_triangle_three_colourings": fixed_count,
        },
        "difference_vectors": len(differences),
        "exceptional_rotations": len(roots),
        "collision_rotations": len(collision_set),
        "rotation_orbits": len(rows),
        "orbit_size_histogram": dict(sorted(Counter(map(len, case_orbits)).items())),
        "chromatic_orbit_histogram": dict(sorted(Counter(row["chi"] for row in rows).items())),
        "three_chromatic_exceptional_rotations": len(roots) - four_rotations,
        "four_chromatic_rotations": four_rotations,
        "all_label_pairs_checked": sum(row["checked_label_pairs"] for row in case_receipts),
        "direct_root_census": root_stats,
        "generic_u_i": generic,
        "physical_order_set": sorted({row["vertices"] for row in case_receipts}),
        "case_receipts": case_receipts,
        "pattern_failure_witnesses": [
            {str(sign): list(witness) for sign, witness in sorted(failures.items())}
            for failures in witness_receipts
        ],
        "record_improvement": False,
    }


def controls(certificate: dict) -> list[str]:
    rejected: list[str] = []

    def reject(name: str, mutate) -> None:
        altered = copy.deepcopy(certificate)
        mutate(altered)
        try:
            validate(altered)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise ValueError(f"negative control accepted: {name}")

    reject("missing_rotation_orbit", lambda data: data["cases"].pop())
    reject("nonunit_rotation", lambda data: data["cases"][0]["angle"].__setitem__(5, 2))
    reject("improper_colour_word", lambda data: data["cases"][0].update(colours="0" * 361))
    reject("false_chromatic_class", lambda data: data["cases"][0].update(chi=4))
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()

    if args.certificate.resolve() == (TARGET / "certificate.json").resolve():
        require(sha256(args.certificate) == CERTIFICATE_SHA256, "target certificate hash")
    certificate = json.loads(args.certificate.read_text())
    receipt = validate(certificate)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        canonical = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
        observed = {
            "receipt_sha256": hashlib.sha256(canonical).hexdigest(),
            "exceptional_rotations": receipt["exceptional_rotations"],
            "rotation_orbits": receipt["rotation_orbits"],
            "chromatic_orbit_histogram": {
                str(key): value
                for key, value in receipt["chromatic_orbit_histogram"].items()
            },
            "four_chromatic_rotations": receipt["four_chromatic_rotations"],
            "physical_order_set": receipt["physical_order_set"],
            "all_label_pairs_checked": receipt["all_label_pairs_checked"],
            "generic_u_i": receipt["generic_u_i"],
        }
        require(observed == expected,
                "independent expected receipt")
    if args.controls:
        receipt["rejected_controls"] = controls(certificate)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
