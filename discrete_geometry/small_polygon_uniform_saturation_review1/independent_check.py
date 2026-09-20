#!/usr/bin/env python3
"""Independent exact audit for the uniform small-polygon saturation theorem.

This checker imports no target code or expected data.  It tests three
definition-level bridges by methods different from the target checker:

* exhaustive convex hulls of all subsets of a 4-by-4 integer grid;
* exhaustive interior-index subsets for every sign code through n=10;
* an exact parametric family built from primitive Pythagorean triples.

The finite checks corroborate the written proof.  They are not a substitute
for its uniform convex-geometric and analytic arguments.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(u, v):
    return (u[0] + v[0], u[1] + v[1])


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def mul(a, u):
    return (a * u[0], a * u[1])


def neg(u):
    return (-u[0], -u[1])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def turn(a, b, c):
    return cross(sub(b, a), sub(c, b))


def convex_hull(points):
    """Strict counterclockwise hull, deleting boundary subdivisions."""
    pts = sorted(set(points))
    if len(pts) <= 1:
        return tuple(pts)
    lower = []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return tuple(lower[:-1] + upper[:-1])


def translated_canonical(poly):
    require(len(poly) >= 3, "not two-dimensional")
    base = poly[0]
    return tuple(sub(p, base) for p in poly)


def edges(poly):
    return tuple(sub(poly[(i + 1) % len(poly)], poly[i])
                 for i in range(len(poly)))


def primitive_direction(e):
    g = gcd(abs(e[0]), abs(e[1]))
    require(g > 0, "zero edge")
    return (e[0] // g, e[1] // g)


def square_part(n):
    """Return a,s with sqrt(n)=a*sqrt(s), s square-free."""
    require(n > 0, "nonpositive squared length")
    a = 1
    s = n
    p = 2
    while p * p <= s:
        while s % (p * p) == 0:
            s //= p * p
            a *= p
        p += 1
    return a, s


def perimeter_signature(poly):
    """Exact formal sum of square roots, grouped by square-free part."""
    out = Counter()
    for e in edges(poly):
        a, s = square_part(dot(e, e))
        out[s] += a
    return out


def doubled(signature):
    return Counter({s: 2 * a for s, a in signature.items()})


def sign_coefficients(c):
    return (-(c[0] + c[-1]),) + tuple(
        c[j - 1] - c[j] for j in range(1, len(c))
    )


def half_edge_velocities(v):
    return tuple(v[j + 1] - v[j] for j in range(len(v) - 1)) + (
        -v[0] - v[-1],
    )


def lattice_hull_census():
    """Audit Minkowski merging and reconstruction from definitions."""
    grid = tuple((x, y) for x in range(-1, 3) for y in range(-1, 3))
    polygons = set()
    subset_count = 0
    for mask in range(1 << len(grid)):
        if mask.bit_count() < 3:
            continue
        subset_count += 1
        hull = convex_hull(grid[i] for i in range(len(grid)) if mask >> i & 1)
        if len(hull) >= 3:
            polygons.add(translated_canonical(hull))

    cases = Counter()
    strict_reconstructions = 0
    formal_perimeter_checks = 0
    disk_checks = 0
    digest = sha256()
    examples = {}

    for poly in sorted(polygons):
        pe = edges(poly)
        k = len(poly)
        dirs = {primitive_direction(e) for e in pe}
        require(len(dirs) == k, "repeated oriented direction")
        r = sum(neg(d) in dirs for d in dirs) // 2

        differences = tuple(sub(p, q) for p in poly for q in poly)
        z = convex_hull(differences)
        m = len(z)
        require(m == 2 * k - 2 * r, "difference-body edge count")
        require(perimeter_signature(z) == doubled(perimeter_signature(poly)),
                "Cauchy perimeter identity")
        formal_perimeter_checks += 1

        diameter2 = max(dot(sub(p, q), sub(p, q)) for p in poly for q in poly)
        saturated = sum(dot(v, v) == diameter2 for v in z)
        require(all(dot(v, v) <= diameter2 for v in z),
                "difference body outside diameter disk")
        require(saturated >= 2, "diameter not attained antipodally")
        disk_checks += len(z)
        cases[(k, r, m)] += 1

        key = None
        if k == 3 and r == 0:
            key = "triangle_full_2k"
        elif k == 4 and r == 1:
            key = "trapezoid_drop_two"
        elif k == 4 and r == 2:
            key = "parallelogram_drop_four"
        if key is not None and key not in examples:
            examples[key] = {
                "polygon": [list(p) for p in poly],
                "difference_edges": m,
            }

        if r == 0:
            require(m == 2 * k, "strict case did not have 2k edges")
            ze = edges(z)
            require(all(ze[j + k] == neg(ze[j]) for j in range(k)),
                    "antipodal edge indexing")
            selected = []
            code = []
            pe_counter = Counter(pe)
            for e in ze[:k]:
                in_forward = pe_counter[e] == 1
                in_reverse = pe_counter[neg(e)] == 1
                require(in_forward ^ in_reverse, "sign selection not unique")
                c = 1 if in_forward else -1
                code.append(c)
                selected.append(mul(c, e))
            require(Counter(selected) == pe_counter,
                    "selected half-edges do not reconstruct P")
            require(tuple(map(sum, zip(*selected))) == (0, 0),
                    "selected half-edges do not close")
            a = sign_coefficients(tuple(code))
            half_vertices = z[:k]
            require(tuple(sum(a[j] * half_vertices[j][d] for j in range(k))
                          for d in range(2)) == (0, 0),
                    "summation-by-parts closure")
            strict_reconstructions += 1

        digest.update(json.dumps(
            [poly, k, r, m, saturated], separators=(",", ":")
        ).encode())

    require(set(examples) == {
        "triangle_full_2k", "trapezoid_drop_two", "parallelogram_drop_four"
    }, "missing smallest degeneracy control")
    return {
        "grid_subsets_with_at_least_three_points": subset_count,
        "distinct_translated_strict_hulls": len(polygons),
        "formal_perimeter_checks": formal_perimeter_checks,
        "difference_body_vertex_disk_checks": disk_checks,
        "strict_sign_reconstructions": strict_reconstructions,
        "case_histogram": {
            f"k={k},r={r},m={m}": count
            for (k, r, m), count in sorted(cases.items())
        },
        "smallest_controls": examples,
        "record_sha256": digest.hexdigest(),
    }


def deformation_census():
    """Enumerate all interior-index subsets, not just individual motions."""
    totals = Counter()
    digest = sha256()
    for n in range(3, 11):
        for code_mask in range(1 << n):
            c = tuple(1 if code_mask >> j & 1 else -1 for j in range(n))
            a = sign_coefficients(c)
            require(any(a), "closure row vanished")
            totals["codes"] += 1

            for r in range(n):
                totals["singleton_positions"] += 1
                if a[r] == 0:
                    totals["singleton_zero_coefficients"] += 1
                elif sum(x != 0 for x in a) == 1:
                    # Closure would force z_r=0, impossible for a strict
                    # difference-body vertex because the origin is interior.
                    totals["singleton_sole_coefficient_obstructions"] += 1
                else:
                    totals["singleton_curve_candidates"] += 1

            for interior_mask in range(1 << n):
                if interior_mask.bit_count() < 2:
                    continue
                interior = [j for j in range(n) if interior_mask >> j & 1]
                zeros = [j for j in interior if a[j] == 0]
                v = [0] * n
                if zeros:
                    r = zeros[0]
                    s = 255
                    v[r] = 1
                    totals["zero_coefficient_subset_motions"] += 1
                else:
                    r, s = interior[:2]
                    v[r] = a[s]
                    v[s] = -a[r]
                    totals["two_nonzero_subset_motions"] += 1
                    if s == r + 1 or (r == 0 and s == n - 1):
                        totals["chosen_adjacent_pairs"] += 1
                require(any(v), "zero closure motion")
                require(sum(a[j] * v[j] for j in range(n)) == 0,
                        "closure motion incomplete")
                require(any(half_edge_velocities(v)), "all edges stationary")
                if v[0]:
                    totals["motions_using_antipodal_endpoint"] += 1
                totals["interior_subsets_of_size_at_least_two"] += 1
                digest.update(bytes((n, r, s)))
                digest.update(code_mask.to_bytes(2, "little"))
                digest.update(interior_mask.to_bytes(2, "little"))

    totals["record_sha256"] = digest.hexdigest()
    return dict(totals)


def rational_sqrt(q):
    a = isqrt(q.numerator)
    b = isqrt(q.denominator)
    require(a * a == q.numerator and b * b == q.denominator,
            "length is not rational")
    return Q(a, b)


def validate_strict_symmetric_half(z):
    full = tuple(z) + tuple(neg(p) for p in z)
    require(all(dot(p, p) <= 1 for p in full), "outside unit disk")
    for j, p in enumerate(full):
        q = full[(j + 1) % len(full)]
        edge = sub(q, p)
        for k, vertex in enumerate(full):
            if k not in (j, (j + 1) % len(full)):
                require(cross(edge, sub(vertex, p)) > 0,
                        "not a strict supporting edge")


def pythagorean_curve_family():
    triples = set()
    for m in range(2, 30):
        for n in range(1, m):
            if gcd(m, n) != 1 or (m - n) % 2 == 0:
                continue
            x, y, hyp = m * m - n * n, 2 * m * n, m * m + n * n
            for a, b in ((x, y), (y, x)):
                if 2 * a < hyp and hyp <= 500:
                    triples.add((a, b, hyp))

    digest = sha256()
    curve_sides = 0
    derivative_checks = 0
    closest_interior_radius = Q(0)
    smallest_derivative = Q(1)
    for a_int, b_int, hyp_int in sorted(triples):
        a, b, hyp = Q(a_int), Q(b_int), Q(hyp_int)
        z = (
            (2 * a / hyp, Q(0)),
            (a / hyp, b / hyp),
            (-a / hyp, b / hyp),
        )
        c = (1, -1, 1)
        coeff = sign_coefficients(c)
        validate_strict_symmetric_half(z)
        require(dot(z[0], z[0]) < 1, "first vertex not interior")
        require(dot(z[1], z[1]) == dot(z[2], z[2]) == 1,
                "circle vertices not active")
        require(tuple(sum(coeff[j] * z[j][d] for j in range(3))
                      for d in range(2)) == (0, 0), "initial closure")

        e = (sub(z[1], z[0]), sub(z[2], z[1]), sub(neg(z[0]), z[2]))
        units = tuple(mul(1 / rational_sqrt(dot(q, q)), q) for q in e)
        g0 = neg(add(units[-1], units[0]))
        g1 = sub(units[0], units[1])
        tangent1 = (-z[1][1], z[1][0])
        derivative = dot(sub(g1, mul(Q(coeff[1], coeff[0]), g0)), tangent1)
        require(derivative == -b / hyp and derivative != 0,
                "incorrect or zero first variation")
        derivative_checks += 1
        smallest_derivative = min(smallest_derivative, abs(derivative))
        closest_interior_radius = max(closest_interior_radius, 2 * a / hyp)

        for h in (Q(1, 100000), Q(-1, 100000)):
            co = (1 - h * h) / (1 + h * h)
            si = 2 * h / (1 + h * h)
            moved = add(mul(co, z[1]), mul(si, tangent1))
            zz = list(z)
            zz[1] = moved
            zz[0] = sub(z[0], mul(Q(coeff[1], coeff[0]), sub(moved, z[1])))
            validate_strict_symmetric_half(tuple(zz))
            require(dot(zz[0], zz[0]) < 1, "compensated vertex left disk")
            require(dot(zz[1], zz[1]) == 1, "rotation left circle")
            require(tuple(sum(coeff[j] * zz[j][d] for j in range(3))
                          for d in range(2)) == (0, 0), "curve lost closure")
            curve_sides += 1

        digest.update(f"{a_int},{b_int},{hyp_int},{derivative}\n".encode())

    require(len(triples) >= 10, "too few Pythagorean fixtures")
    return {
        "primitive_triples": len(triples),
        "nonzero_first_variation_checks": derivative_checks,
        "two_sided_curve_checks": curve_sides,
        "closest_interior_radius": str(closest_interior_radius),
        "smallest_absolute_derivative": str(smallest_derivative),
        "record_sha256": digest.hexdigest(),
    }


def exact_scalar_margins():
    """Recheck the proof's deliberately coarse constants over 3<pi<22/7."""
    pi_lower = Q(3)
    pi_upper = Q(22, 7)
    margins = {
        "edge_count_gap": pi_lower * pi_lower / 6 - Q(1, 100),
        "normal_width": pi_lower * pi_lower / 16 - Q(3, 50),
        "misalignment": Q(1, 256) - Q(1, 300),
        "gradient_ratio": Q(3) - 5 * pi_upper / 6,
        "curve_angle": Q(5, 16) - 3 * pi_upper / 32,
        "separation": Q(11, 16) - Q(5, 16),
        "bingane_n32": Q(32**3) - 100 * pi_upper**7 / 18,
    }
    require(all(x > 0 for x in margins.values()), "nonpositive scalar margin")
    return {key: str(value) for key, value in margins.items()}


def main():
    result = {
        "schema": 1,
        "trust_boundary": (
            "Finite exact checks corroborate the edge-count, reconstruction, "
            "deformation-case, and feasible-curve bridges. The uniform theorem "
            "still rests on the audited convex-geometric and analytic proof, "
            "plus Bingane's published construction for the corollary."
        ),
        "lattice_hulls": lattice_hull_census(),
        "deformation_completeness": deformation_census(),
        "last_interior_curve": pythagorean_curve_family(),
        "scalar_margins": exact_scalar_margins(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(canonical.encode()).hexdigest()
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    expected = Path(__file__).with_name("EXPECTED.json")
    if expected.exists():
        require(output == expected.read_text(), "expected record mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
