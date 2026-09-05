#!/usr/bin/env python3
"""Reviewer-owned exact audit for the cross-four-cycle gluing theorem.

This checker imports no reviewed module.  It reconstructs the two calibration
components from pinned coordinates, independently repeats the complete
diagonal-length classification, and exhausts the residue states used by both
four-colouring branches.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PINS = {
    159: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    214: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}
CALIBRATION_PIN = "b35e911535a1ef1ec0c8d47c8a4a08bb10053d8e4e5c9557fe24eac20d32b259"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source(order: int) -> list[tuple[int, int, int, int]]:
    path = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / f"points{order}.tsv"
    require(sha256(path) == SOURCE_PINS[order], "source-coordinate hash")
    points = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        require(len(values) == 16, "coordinate width")
        require(all(values[index] == 0 for index in range(16)
                    if index not in (0, 5, 9, 12)), "coordinate subfield")
        points.append(tuple(values[index] for index in (0, 5, 9, 12)))
    require(len(points) == len(set(points)) == order, "source point count")
    return points


def components() -> dict[str, tuple[list[tuple[int, int, int, int]], int]]:
    A = read_source(159)
    V = read_source(214)
    fixed = [tuple(6 * value for value in point) for point in A]
    rotated = []
    for a, b, c, d in A:
        # Multiplication by (5+i*sqrt(11))/6, at common scale 72.
        rotated.append((5 * a - 11 * d, 5 * b - c,
                        5 * c + 11 * b, 5 * d + a))
    B = list(dict.fromkeys(fixed + rotated))
    require(len(B) == 292, "inner-union cardinality")
    return {"B": (B, 72), "V": (V, 12)}


def squared_norm(p: tuple[int, int, int, int],
                 q: tuple[int, int, int, int]) -> tuple[int, int]:
    a, b, c, d = (x - y for x, y in zip(p, q))
    return a * a + 33 * b * b + 3 * c * c + 11 * d * d, 2 * (a * b + c * d)


def pair_data(points: list[tuple[int, int, int, int]], scale: int) -> tuple[Counter, int, bool]:
    counts = Counter()
    adjacency = [[] for _ in points]
    edges = 0
    for i, j in combinations(range(len(points)), 2):
        value = squared_norm(points[i], points[j])
        counts[value] += 1
        if value == (scale * scale, 0):
            adjacency[i].append(j)
            adjacency[j].append(i)
            edges += 1
    seen = {0}
    todo = [0]
    for vertex in todo:
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                todo.append(neighbor)
    return counts, edges, len(seen) == len(points)


def mul_real(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] * y[0] + 33 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def sqrt_fraction(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def square_in_real_field(a: Fraction, b: Fraction) -> bool:
    """Decide whether a+b*sqrt(33) is a square in Q(sqrt(33))."""
    if b == 0:
        return sqrt_fraction(a) is not None or sqrt_fraction(a / 33) is not None
    discriminant_root = sqrt_fraction(a * a - 33 * b * b)
    if discriminant_root is None:
        return False
    for sign in (1, -1):
        p = sqrt_fraction((a + sign * discriminant_root) / 2)
        if p in (None, 0):
            continue
        q = b / (2 * p)
        if p * p + 33 * q * q == a and 2 * p * q == b:
            return True
    return False


def rotation_root_in_field(norm_b: tuple[int, int], norm_v: tuple[int, int]) -> bool:
    product_value = mul_real(norm_b, norm_v)
    denominator = 3 * (72 * 12) ** 2
    return square_in_real_field(Fraction(product_value[0], denominator),
                                Fraction(product_value[1], denominator))


def root33_mod(bits: int) -> int:
    """Return the stable residue of the 2-adic root sqrt(33)=1 (mod 8)."""
    large_modulus = 1 << (bits + 4)
    residues = {value % (1 << bits) for value in range(large_modulus)
                if value % 8 == 1 and value * value % large_modulus == 33 % large_modulus}
    require(len(residues) == 1, "unstable 2-adic square-root residue")
    return residues.pop()


def norm_is_unit(norm_value: tuple[int, int], scale: int) -> bool:
    scale_valuation = 0
    odd_scale = scale
    while odd_scale % 2 == 0:
        scale_valuation += 1
        odd_scale //= 2
    denominator_valuation = 2 * scale_valuation
    modulus = 1 << (denominator_valuation + 1)
    numerator = (norm_value[0] + norm_value[1] * root33_mod(denominator_valuation + 1)) % modulus
    require(numerator % (1 << denominator_valuation) == 0, "nonintegral diagonal norm")
    return bool((numerator >> denominator_valuation) & 1)


def audit_diagonals(parts: dict[str, tuple[list[tuple[int, int, int, int]], int]]) -> None:
    B, scale_b = parts["B"]
    V, scale_v = parts["V"]
    b_counts, b_edges, b_connected = pair_data(B, scale_b)
    v_counts, v_edges, v_connected = pair_data(V, scale_v)
    require((len(b_counts), len(v_counts)) == (1056, 372), "norm-type totals")
    require((b_edges, v_edges) == (1251, 977), "component edge totals")
    require(b_connected and v_connected, "component connectivity")

    census = Counter()
    outside_pairs = set()
    for norm_v, multiplicity_v in v_counts.items():
        norm_b = (4 * scale_b * scale_b - (scale_b // scale_v) ** 2 * norm_v[0],
                  -(scale_b // scale_v) ** 2 * norm_v[1])
        multiplicity_b = b_counts.get(norm_b, 0)
        if not multiplicity_b:
            continue
        branch = "in_E" if rotation_root_in_field(norm_b, norm_v) else "outside_E"
        census[branch + "_norm_pairs"] += 1
        census[branch + "_segment_pairs"] += multiplicity_b * multiplicity_v
        if branch == "outside_E":
            outside_pairs.add((norm_b, norm_v))
    require(census == {
        "in_E_norm_pairs": 26,
        "in_E_segment_pairs": 2551052,
        "outside_E_norm_pairs": 51,
        "outside_E_segment_pairs": 1748914,
    }, "complementary-diagonal census")

    calibration_path = ROOT / "hadwiger_nelson_cross_four_cycle_gluing" / "calibration.json"
    require(sha256(calibration_path) == CALIBRATION_PIN, "calibration hash")
    rows = json.loads(calibration_path.read_text())
    require(len(rows) == 51, "selected calibration rows")
    selected_pairs = set()
    branch_counts = Counter()
    for row in rows:
        i, j, k, l = row["seed"]
        norm_b = squared_norm(B[i], B[j])
        norm_v = squared_norm(V[k], V[l])
        require((norm_b, norm_v) in outside_pairs, "selected seed is not outside-field")
        selected_pairs.add((norm_b, norm_v))
        unit = norm_is_unit(norm_b, scale_b)
        require(unit == norm_is_unit(norm_v, scale_v), "diagonal parities disagree")
        branch = "unit_diagonals" if unit else "even_diagonals"
        require(row["branch"] == branch, "selected branch label")
        require(not any(tuple(B[i][t] + B[j][t] for t in range(4)) == tuple(2 * p[t] for t in range(4))
                        for p in B), "selected B midpoint is internal")
        require(not any(tuple(V[k][t] + V[l][t] for t in range(4)) == tuple(2 * p[t] for t in range(4))
                        for p in V), "selected V midpoint is internal")
        branch_counts[branch] += 1
    require(selected_pairs == outside_pairs, "outside-field length-type coverage")
    require(branch_counts == {"unit_diagonals": 43, "even_diagonals": 8},
            "calibration branch totals")
    print("PASS components: B=292/1251 V=214/977, both unit-distance graphs connected")
    print("PASS diagonals: norm_types=1056+372 complementary=77 in_E=26 outside_E=51 segment_pairs=2551052+1748914")
    print("PASS calibration seeds: all 51 outside-field types represented once, branches=43 unit+8 even, midpoints external")


def ring_mul(x: tuple[int, int], y: tuple[int, int], modulus: int) -> tuple[int, int]:
    a, b = x
    c, d = y
    return (a * c - b * d) % modulus, (a * d + b * c - b * d) % modulus


def ring_norm(x: tuple[int, int], modulus: int) -> int:
    a, b = x
    return (a * a - a * b + b * b) % modulus


def residue(x: tuple[int, int]) -> tuple[int, int]:
    return x[0] % 2, x[1] % 2


def half_residue(x: tuple[int, int]) -> tuple[int, int]:
    require(x[0] % 2 == x[1] % 2 == 0, "attempted division by two")
    return (x[0] // 2) % 2, (x[1] // 2) % 2


def audit_residue_colorings() -> None:
    field4 = list(product(range(2), repeat=2))
    even_states = 0
    for x, y in product(field4, repeat=2):
        if (ring_norm(x, 2) + ring_norm(y, 2)) % 2 != 1:
            continue
        require(x != y, "even-diagonal cross-color collision")
        even_states += 1
    require(even_states == 6, "even-diagonal residue-state total")

    ring4 = list(product(range(4), repeat=2))
    units = [x for x in ring4 if ring_norm(x, 4) % 2]
    rho_lifts = [(1, 0), (0, 1), (3, 3)]
    require(all(ring_norm(rho, 4) == 1 for rho in rho_lifts), "rho norm")
    diagonal_states = radial_states = 0
    for d, e in product(units, repeat=2):
        if (ring_norm(d, 4) + ring_norm(e, 4)) % 4:
            continue
        matching = [rho for rho in rho_lifts if residue(ring_mul(rho, e, 4)) == residue(d)]
        require(len(matching) == 1, "rho residue choice")
        rho = matching[0]
        diagonal_states += 1
        for X, Y in product(units, repeat=2):
            if residue(X) != residue(d) or residue(Y) != residue(e):
                continue
            if (ring_norm(X, 4) + ring_norm(Y, 4)) % 4:
                continue
            color_p = half_residue(((X[0] + d[0]) % 4, (X[1] + d[1]) % 4))
            rho_y = ring_mul(rho, Y, 4)
            color_q = half_residue(((rho_y[0] + d[0]) % 4,
                                    (rho_y[1] + d[1]) % 4))
            require(color_p != color_q, "unit-diagonal cross-color collision")
            radial_states += 1
    require(diagonal_states > 0 and radial_states > 0, "unit-diagonal state coverage")
    print(f"PASS residue colorings: even_cross_states={even_states} unit_diagonal_states={diagonal_states} unit_radial_states={radial_states}")


def main() -> None:
    parts = components()
    print("PASS pinned sources: A=159 V=214 B=292 exact points in E")
    audit_diagonals(parts)
    audit_residue_colorings()
    print("PASS: independent exact audit supports the cross-four-cycle gluing theorem")
    print("SCOPE: the uniform K2,2 geometry and 2-adic coset argument are re-derived mathematics; calibration cases are not an exhaustive placement census")


if __name__ == "__main__":
    main()
