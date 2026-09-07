#!/usr/bin/env python3
"""Independent exact checker for the VND M2 radial-prefix closure certificate.

This deliberately does not import the submitted exact_model.py.  In particular,
signs in Q(sqrt(2),sqrt(3)) are decided algebraically by two nested quadratic
comparisons, rather than by the submitter's rational interval enclosures.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations
from pathlib import Path


Q = Fraction


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def rational_sign(value: Q) -> int:
    return (value > 0) - (value < 0)


def sign_qsqrt2(a: Q, b: Q) -> int:
    """Return sign(a+b*sqrt(2)) using only rational arithmetic."""
    sa, sb = rational_sign(a), rational_sign(b)
    if sb == 0:
        return sa
    if sa == 0 or sa == sb:
        return sb
    comparison = rational_sign(a * a - 2 * b * b)
    require(comparison != 0, "unexpected rational equality with sqrt(2)")
    return comparison if sa > 0 else -comparison


@dataclass(frozen=True)
class K4:
    """a+b*sqrt(2)+c*sqrt(3)+d*sqrt(6), with rational coefficients."""

    a: Q
    b: Q
    c: Q
    d: Q

    def __add__(self, other: K4) -> K4:
        return K4(self.a + other.a, self.b + other.b,
                  self.c + other.c, self.d + other.d)

    def __neg__(self) -> K4:
        return K4(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, other: K4) -> K4:
        return self + (-other)

    def __mul__(self, other: K4) -> K4:
        # View the field as Q(sqrt(2))[sqrt(3)].
        u0 = self.a * other.a + 2 * self.b * other.b
        u1 = self.a * other.b + self.b * other.a
        v0 = self.c * other.c + 2 * self.d * other.d
        v1 = self.c * other.d + self.d * other.c
        w0 = self.a * other.c + 2 * self.b * other.d
        w0 += self.c * other.a + 2 * self.d * other.b
        w1 = self.a * other.d + self.b * other.c
        w1 += self.c * other.b + self.d * other.a
        return K4(u0 + 3 * v0, u1 + 3 * v1, w0, w1)

    def scale(self, scalar: int | Q) -> K4:
        scalar = Q(scalar)
        return K4(scalar * self.a, scalar * self.b,
                  scalar * self.c, scalar * self.d)

    def sign(self) -> int:
        """Exact nested-quadratic sign, independent of interval precision."""
        su = sign_qsqrt2(self.a, self.b)
        sv = sign_qsqrt2(self.c, self.d)
        if sv == 0:
            return su
        if su == 0 or su == sv:
            return sv

        # Compare |a+b sqrt(2)| with sqrt(3)|c+d sqrt(2)|.
        delta_a = self.a * self.a + 2 * self.b * self.b
        delta_a -= 3 * (self.c * self.c + 2 * self.d * self.d)
        delta_b = 2 * self.a * self.b - 6 * self.c * self.d
        magnitude_comparison = sign_qsqrt2(delta_a, delta_b)
        require(magnitude_comparison != 0,
                "unexpected equality between independent quadratic fields")
        return su if magnitude_comparison > 0 else sv

    def certificate_form(self) -> list[list[int]]:
        return [[x.numerator, x.denominator]
                for x in (self.a, self.b, self.c, self.d)]


ZERO = K4(Q(0), Q(0), Q(0), Q(0))
ONE = K4(Q(1), Q(0), Q(0), Q(0))


@dataclass(frozen=True)
class Point:
    x: K4
    y: K4

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point) -> Point:
        return Point(self.x * other.x - self.y * other.y,
                     self.x * other.y + self.y * other.x)

    def conjugate(self) -> Point:
        return Point(self.x, -self.y)

    def norm_squared(self) -> K4:
        return self.x * self.x + self.y * self.y

    def power(self, exponent: int) -> Point:
        if exponent < 0:
            return self.conjugate().power(-exponent)
        result = Point(ONE, ZERO)
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result


ORIGIN = Point(ZERO, ZERO)
PHI0 = Point(K4(Q(0), Q(1, 4), Q(0), Q(1, 4)),
             K4(Q(0), Q(-1, 4), Q(0), Q(1, 4)))
PHI1 = Point(K4(Q(0), Q(0), Q(0), Q(1, 3)),
             K4(Q(0), Q(0), Q(1, 3), Q(0)))


def point_key(point: Point) -> tuple[int, ...]:
    coefficients = (
        point.x.a, point.x.b, point.x.c, point.x.d,
        point.y.a, point.y.b, point.y.c, point.y.d,
    )
    return tuple(item for value in coefficients
                 for item in (value.numerator, value.denominator))


def reconstruct_sets() -> tuple[tuple[Point, ...], tuple[Point, ...]]:
    require(PHI0.norm_squared() == ONE, "phi0 is not a unit")
    require(PHI1.norm_squared() == ONE, "phi1 is not a unit")
    require(PHI0.power(24) == Point(ONE, ZERO), "phi0^24 != 1")
    m1 = {ORIGIN}
    for exponent0 in range(24):
        for exponent1 in (-1, 0, 1):
            m1.add(PHI0.power(exponent0) * PHI1.power(exponent1))
    require(len(m1) == 73, f"M1 has {len(m1)} rather than 73 points")

    m2 = set()
    for left in m1:
        for right in m1:
            point = left + right
            if (point.norm_squared() - ONE).sign() <= 0:
                m2.add(point)
    require(len(m2) == 865, f"M2 has {len(m2)} rather than 865 points")
    return (tuple(sorted(m1, key=point_key)),
            tuple(sorted(m2, key=point_key)))


def shell_prefixes(m2: tuple[Point, ...]) -> list[tuple[K4, tuple[Point, ...]]]:
    shells: dict[K4, list[Point]] = {}
    for point in m2:
        shells.setdefault(point.norm_squared(), []).append(point)
    radii = sorted(shells, key=cmp_to_key(lambda x, y: (x - y).sign()))
    accumulated: list[Point] = []
    prefixes = []
    for radius in radii:
        accumulated.extend(shells[radius])
        prefixes.append((radius, tuple(sorted(accumulated, key=point_key))))
    return prefixes


def maximal_budget_pairs(prefixes):
    usable = [prefix for prefix in prefixes if len(prefix[1]) <= 508]
    valid = []
    for left in usable:
        for right in usable:
            nl, nr = len(left[1]), len(right[1])
            if nl >= nr and nl + nr - 1 <= 508:
                valid.append((left, right))
    maximal = []
    for candidate in valid:
        nl, nr = len(candidate[0][1]), len(candidate[1][1])
        if not any(
            len(other[0][1]) >= nl and len(other[1][1]) >= nr
            and (len(other[0][1]) > nl or len(other[1][1]) > nr)
            for other in valid
        ):
            maximal.append(candidate)
    for pair in valid:
        nl, nr = len(pair[0][1]), len(pair[1][1])
        require(any(len(top[0][1]) >= nl and len(top[1][1]) >= nr
                    for top in maximal),
                f"valid pair {(nl, nr)} is not dominated by a maximal pair")
    return maximal, valid


class ParityDSU:
    def __init__(self, order: int):
        self.parent = list(range(order))
        self.rank = [0] * order
        self.parity = [0] * order

    def find(self, vertex: int) -> tuple[int, int]:
        if self.parent[vertex] == vertex:
            return vertex, 0
        root, parent_parity = self.find(self.parent[vertex])
        self.parity[vertex] ^= parent_parity
        self.parent[vertex] = root
        return root, self.parity[vertex]

    def add_opposite_constraint(self, left: int, right: int) -> None:
        root_l, parity_l = self.find(left)
        root_r, parity_r = self.find(right)
        if root_l == root_r:
            require((parity_l ^ parity_r) == 1,
                    f"odd-cycle contradiction on edge {(left, right)}")
            return
        if self.rank[root_l] < self.rank[root_r]:
            root_l, root_r = root_r, root_l
            parity_l, parity_r = parity_r, parity_l
        self.parent[root_r] = root_l
        self.parity[root_r] = parity_l ^ parity_r ^ 1
        if self.rank[root_l] == self.rank[root_r]:
            self.rank[root_l] += 1


def verify(certificate_path: Path) -> dict[str, object]:
    raw = certificate_path.read_bytes()
    certificate = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == "443047ca455bfd1bf8ebf2cc6c7632e1b06fb455d4e4ea66c96f7e4360225b4f",
            f"unexpected certificate SHA-256 {digest}")
    require(certificate["schema"] == "hn-vnd-radial-prefix-closure-v1",
            "unexpected certificate schema")

    m1, m2 = reconstruct_sets()
    require(certificate["m1_vertices"] == len(m1), "M1 count mismatch")
    require(certificate["m2_vertices"] == len(m2), "M2 count mismatch")
    prefixes = shell_prefixes(m2)
    expected_shells = [
        {"radius_squared": radius.certificate_form(),
         "cumulative_vertices": len(points)}
        for radius, points in prefixes
    ]
    require(certificate["shells"] == expected_shells,
            "published shell table does not match reconstruction")
    shell_sizes = [len(points) for _, points in prefixes]
    require(shell_sizes == [1, 25, 73, 121, 145, 217, 241, 289, 337,
                            361, 433, 457, 505, 553, 577, 649, 673, 721,
                            769, 793, 865],
            f"unexpected radial prefix sizes {shell_sizes}")

    maximal, valid = maximal_budget_pairs(prefixes)
    maximal_sizes = sorted((len(left[1]), len(right[1]))
                           for left, right in maximal)
    require(maximal_sizes == [(241, 241), (289, 217), (361, 145),
                              (433, 73), (457, 25), (505, 1)],
            f"unexpected maximal budget pairs {maximal_sizes}")
    pair_rows = []
    for (left2, left), (right2, right) in sorted(
        maximal, key=lambda pair: (len(pair[0][1]), len(pair[1][1]))
    ):
        linear = ONE - left2 - right2
        squared = linear * linear - (left2 * right2).scale(4)
        require(linear.sign() > 0,
                f"nonpositive linear margin for {(len(left), len(right))}")
        require(squared.sign() > 0,
                f"nonpositive squared margin for {(len(left), len(right))}")
        pair_rows.append({
            "left_vertices": len(left),
            "right_vertices": len(right),
            "nominal_union_vertices": len(left) + len(right) - 1,
            "left_radius_squared": left2.certificate_form(),
            "right_radius_squared": right2.certificate_form(),
            "one_minus_radius_squares": linear.certificate_form(),
            "squared_radius_sum_margin": squared.certificate_form(),
        })
    require(certificate["maximal_budget_pairs"] == pair_rows,
            "published maximal-pair rows or exact margins do not match")

    k505 = next(points for _, points in prefixes if len(points) == 505)
    edges = [(left, right) for left, right in combinations(range(505), 2)
             if (k505[left] - k505[right]).norm_squared() == ONE]
    require(len(edges) == 216, f"K505 has {len(edges)} rather than 216 edges")
    require(certificate["largest_relevant_prefix_vertices"] == 505,
            "published largest-prefix order mismatch")
    require(certificate["largest_relevant_prefix_unit_edges"] ==
            [list(edge) for edge in edges],
            "published K505 edge list does not match exact reconstruction")

    colour_word = certificate["largest_relevant_prefix_bipartition"]
    require(len(colour_word) == 505 and set(colour_word) <= {"0", "1"},
            "published bipartition is not a 505-bit word")
    colours = [int(bit) for bit in colour_word]
    require(all(colours[left] != colours[right] for left, right in edges),
            "published bipartition has a monochromatic edge")
    dsu = ParityDSU(505)
    for left, right in edges:
        dsu.add_opposite_constraint(left, right)
    components = len({dsu.find(vertex)[0] for vertex in range(505)})

    expected_conclusion = (
        "Every union K_r union rho(K_s) with |K_r|+|K_s|-1 <= 508 "
        "is four-colourable for every origin-centred rotation rho."
    )
    require(certificate["conclusion"] == expected_conclusion,
            "certificate conclusion changed")
    return {
        "status": "VERIFIED_INDEPENDENT_VND_RADIAL_PREFIX_CLOSURE",
        "certificate_sha256": digest,
        "m1_vertices": len(m1),
        "m2_vertices": len(m2),
        "shells": len(prefixes),
        "valid_oriented_budget_pairs": len(valid),
        "maximal_budget_pairs": [list(pair) for pair in maximal_sizes],
        "k505_unit_edges": len(edges),
        "k505_bipartite_components": components,
        "sign_method": "nested exact quadratic comparisons",
    }


def main() -> None:
    require(len(sys.argv) == 2,
            "usage: independent_verify.py PATH/TO/certificate.json")
    report = verify(Path(sys.argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
