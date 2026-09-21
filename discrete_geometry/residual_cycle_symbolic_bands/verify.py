#!/usr/bin/env python3
"""Exact fixture audit for PROOF.md; Python 3.11+, standard library only.

Full Hasse-jet matrices are built from the point definition, without using
the divisibility recursion. A finite-field rank gives a rational rank lower
bound. Rational, linearly independent kernel vectors give the reverse bound.
Thus each reported dimension is certified over Q, not inferred from a prime.
The universal theorem remains the written proof.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, gcd, isqrt, lcm
from pathlib import Path

PRIME = 1000003


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def monomials(degree):
    return [(a, b, degree-a-b) for a in range(degree+1)
            for b in range(degree-a+1)] if degree >= 0 else []


def primitive(values):
    values = [Fraction(x) for x in values]
    denominator = lcm(*(x.denominator for x in values))
    integers = [int(x*denominator) for x in values]
    common = gcd(*integers)
    require(common != 0, "zero primitive vector")
    integers = [x//common for x in integers]
    if next(x for x in integers if x) < 0:
        integers = [-x for x in integers]
    return tuple(integers)


def cross(a, b):
    return primitive((a[1]*b[2]-a[2]*b[1],
                      a[2]*b[0]-a[0]*b[2],
                      a[0]*b[1]-a[1]*b[0]))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def fixture(n, sizes, style):
    require(sum(sizes) == n and all(s >= 3 for s in sizes),
            "cycle sizes must partition all labels into cycles of length >=3")
    lines = []
    for t in range(1, n+1):
        power = 3 if style == "cubic" else 2
        a, b, c = -t, 1, -t**power
        if style == "projective":
            a, b = 9*a-c, 9*b-c  # scaled inverse transpose: z' = x+y+9z
        lines.append(primitive((a, b, c)))
    return validate_arrangement(lines, sizes)


def validate_arrangement(lines, sizes):
    n = len(lines)
    require(sum(sizes) == n and all(s >= 3 for s in sizes), "bad cycles")
    require(len(set(lines)) == n, "repeated line")
    for i, j, k in combinations(range(n), 3):
        require(dot(lines[k], cross(lines[i], lines[j])) != 0,
                "triple concurrence")
    cycles, missing, offset = [], set(), 0
    for size in sizes:
        cycle = tuple(range(offset, offset+size))
        cycles.append(cycle)
        missing.update(tuple(sorted((cycle[j], cycle[(j+1) % size])))
                       for j in range(size))
        offset += size
    pairs = [ij for ij in combinations(range(n), 2) if ij not in missing]
    points = [cross(lines[i], lines[j]) for i, j in pairs]
    require(len(set(points)) == n*(n-3)//2, "point count")
    for i, line in enumerate(lines):
        require(sum(dot(line, p) == 0 for p in points) == n-3,
                "wrong number of selected points on line")
    return lines, cycles, missing, pairs, points


def jet_matrix(points, degree, multiplicity):
    """Integer Hasse-derivative equations in a nonvanishing projective chart."""
    mons = monomials(degree)
    matrix = []
    for p in points:
        chart = next(i for i in (2, 1, 0) if p[i])
        free = [i for i in range(3) if i != chart]
        i, j = free
        powers = [[coord**e for e in range(degree+1)] for coord in p]
        for total in range(multiplicity):
            for u in range(total+1):
                v = total-u
                row = []
                for ex in mons:
                    if ex[i] < u or ex[j] < v:
                        row.append(0)
                    else:
                        row.append(comb(ex[i], u)*comb(ex[j], v)
                                   * powers[i][ex[i]-u]*powers[j][ex[j]-v]
                                   * powers[chart][ex[chart]])
                matrix.append(row)
    return matrix


def rank_mod(matrix, width):
    pivots = {}
    for raw in matrix:
        require(len(raw) == width, "ragged matrix")
        row = [x % PRIME for x in raw]
        for col in range(width):
            a = row[col]
            if not a:
                continue
            if col in pivots:
                pivot = pivots[col]
                row[col:] = [(x-a*y) % PRIME
                             for x, y in zip(row[col:], pivot[col:])]
            else:
                inv = pow(a, -1, PRIME)
                row[col:] = [x*inv % PRIME for x in row[col:]]
                pivots[col] = row
                break
    return len(pivots)


def nullspace_q(matrix, width):
    """Exact rational Gauss-Jordan, used only for the small base spaces."""
    rows = [[Fraction(x) for x in row] for row in matrix]
    pivot_cols, used = [], 0
    for col in range(width):
        found = next((i for i in range(used, len(rows)) if rows[i][col]), None)
        if found is None:
            continue
        rows[used], rows[found] = rows[found], rows[used]
        scale = rows[used][col]
        rows[used] = [x/scale for x in rows[used]]
        for i in range(len(rows)):
            if i == used or not rows[i][col]:
                continue
            a = rows[i][col]
            rows[i] = [x-a*y for x, y in zip(rows[i], rows[used])]
        pivot_cols.append(col)
        used += 1
        if used == len(rows):
            break
    basis = []
    for free in range(width):
        if free in pivot_cols:
            continue
        vector = [Fraction(0)]*width
        vector[free] = 1
        for i, col in enumerate(pivot_cols):
            vector[col] = -rows[i][free]
        basis.append(primitive(vector))
    return basis


def poly_from_vector(vector, degree):
    return {ex: x for ex, x in zip(monomials(degree), vector) if x}


def poly_vector(poly, degree):
    require(all(sum(ex) == degree for ex in poly), "inhomogeneous polynomial")
    return [poly.get(ex, 0) for ex in monomials(degree)]


def multiply(a, b):
    result = {}
    for e, x in a.items():
        for f, y in b.items():
            ex = tuple(u+v for u, v in zip(e, f))
            result[ex] = result.get(ex, 0)+x*y
    return {ex: x for ex, x in result.items() if x}


def power(a, k):
    result = {(0, 0, 0): 1}
    for _ in range(k):
        result = multiply(result, a)
    return result


def line_product(lines):
    result = {(0, 0, 0): 1}
    for line in lines:
        result = multiply(result, {(1, 0, 0): line[0],
                                   (0, 1, 0): line[1],
                                   (0, 0, 1): line[2]})
    return result


def value(poly, point):
    return sum(c*point[0]**e[0]*point[1]**e[1]*point[2]**e[2]
               for e, c in poly.items())


def membership(matrix, vector):
    return all(sum(x*y for x, y in zip(row, vector)) == 0 for row in matrix)


def adjoint_basis(lines, cycles, missing):
    n, result = len(lines), []
    for cycle in cycles:
        s = len(cycle)
        points = [cross(lines[i], lines[j]) for i, j in combinations(cycle, 2)
                  if (i, j) not in missing]
        basis = nullspace_q(jet_matrix(points, s-3, 1), len(monomials(s-3)))
        require(len(basis) == 1, "cycle adjoint is not unique")
        local = poly_from_vector(basis[0], s-3)
        outside = line_product([lines[i] for i in range(n) if i not in cycle])
        result.append(multiply(local, outside))
    return result


def certify_space(points, degree, m, polynomials, audit):
    """Kernel inclusion over Q plus modular independence and maximal rank."""
    width = len(monomials(degree))
    matrix = jet_matrix(points, degree, m)
    vectors = [poly_vector(poly, degree) for poly in polynomials]
    for vector in vectors:
        require(membership(matrix, vector), f"jet failure m={m}, D={degree}")
    require(rank_mod(vectors, width) == len(vectors), "dependent proposed basis")
    rank = rank_mod(matrix, width)
    require(rank == width-len(vectors),
            f"wrong kernel dimension m={m}, D={degree}: {width-rank}")
    audit.append([m, degree, len(points), width, len(matrix), len(vectors)])


def run():
    require(PRIME > 2 and all(PRIME % d for d in range(2, isqrt(PRIME)+1)),
            "rank modulus is not prime")
    fixtures = [
        (7, (7,), "parabola"), (7, (3, 4), "cubic"),
        (8, (8,), "projective"), (8, (3, 5), "parabola"),
        (8, (4, 4), "cubic"), (9, (9,), "cubic"),
        (9, (3, 3, 3), "projective"), (10, (10,), "parabola"),
    ]
    summaries, audit, certificates = [], [], []
    first_failure_forms = 0
    for n, sizes, style in fixtures:
        lines, cycles, missing, pairs, points = fixture(n, sizes, style)
        if style == "projective":
            require(any(p[2] == 0 for p in points), "missing infinity-chart fixture")
        d, h = n-3, n-6
        f = line_product(lines)
        bases = {0: adjoint_basis(lines, cycles, missing)}
        require(len(bases[0]) == len(cycles), "base component count")
        certify_space(points, d, 1, bases[0], audit)
        certify_space(points, d-1, 1, [], audit)
        for r in range(1, h):
            degree = d+r
            base = nullspace_q(jet_matrix(points, degree, 1), len(monomials(degree)))
            require(len(base) == comb(degree+2, 2)-len(points), "base Hilbert value")
            bases[r] = [poly_from_vector(v, degree) for v in base]
            certify_space(points, degree, 1, bases[r], audit)
        for m in (2, 3, 4):
            k, parity = divmod(m, 2)
            alpha = k*n+parity*d
            fk = power(f, k)
            offsets = range(h) if m in (2, 3) else (0,)
            for r in offsets:
                base = (bases[r] if parity else
                        [{ex: 1} for ex in monomials(r)])
                candidates = [multiply(fk, b) for b in base]
                certify_space(points, alpha+r, m, candidates, audit)
            certify_space(points, alpha-1, m, [], audit)
        # A has no arrangement line as a factor: use each omitted intersection
        # as an explicit nonzero-value witness on its two incident lines.
        a = {}
        for b in bases[0]:
            for ex, coefficient in b.items():
                a[ex] = a.get(ex, 0)+coefficient
        a = {ex: coefficient for ex, coefficient in a.items() if coefficient}
        require(all(value(a, cross(lines[i], lines[j])) != 0 for i, j in missing),
                "summed adjoint has a line component")
        for exponent in (2, 3):
            candidate = power(a, exponent)
            matrix = jet_matrix(points, exponent*d, exponent)
            require(membership(matrix, poly_vector(candidate, exponent*d)),
                    "first-failure form has insufficient multiplicity")
            require(exponent*d == n+(exponent-2)*d+h, "endpoint degree")
            first_failure_forms += 1
        # Degree-zero/one forms alone do not certify the theorem: preserve a
        # digest of every rational component-adjoint certificate too.
        certificates.append([n, list(sizes), style,
                             [poly_vector(b, d) for b in bases[0]]])
        summaries.append({"n": n, "cycles": list(sizes), "coordinates": style,
                          "points": len(points), "band_width": h,
                          "points_at_infinity": sum(p[2] == 0 for p in points),
                          "initial_degrees_m1_to_m4": [d, n, n+d, 2*n],
                          "bottom_dimensions_m1_to_m4": [len(cycles), 1,
                                                          len(cycles), 1]})
    # Boundary counterexamples: independence is certified directly, so no
    # extrapolated all-multiplicity assertion at n=6 or n=5 is being tested.
    boundary = []
    for n in (5, 6):
        lines, cycles, missing, _, points = fixture(n, (n,), "cubic")
        a = adjoint_basis(lines, cycles, missing)[0]
        a2 = power(a, 2)
        degree = 2*(n-3)
        require(membership(jet_matrix(points, degree, 2), poly_vector(a2, degree)),
                "small-n boundary witness")
        if n == 6:
            require(rank_mod([poly_vector(a2, 6), poly_vector(line_product(lines), 6)],
                             len(monomials(6))) == 2, "hexagon independence")
        else:
            require(degree < n, "pentagon initial-degree failure")
        boundary.append({"n": n, "m": 2, "adjoint_square_degree": degree})
    rejected = []
    for name, action in [
        ("triple concurrence", lambda: validate_arrangement(
            [(1, 0, 0), (0, 1, 0), (1, 1, 0)], (3,))),
        ("two-cycle", lambda: fixture(7, (2, 5), "parabola")),
        ("incomplete labels", lambda: fixture(7, (3, 3), "cubic")),
    ]:
        try:
            action()
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError("invalid input accepted: "+name)
    points = fixture(7, (7,), "parabola")[-1]
    width = len(monomials(4))
    require(width-rank_mod(jet_matrix(points[:-1], 4, 1), width) >= 2,
            "removed point condition was not detected")
    # Projective Hasse equations must distinguish simple from double vanishing.
    line = {(1, 0, 0): 1}
    p = [(0, 1, 1)]
    require(membership(jet_matrix(p, 1, 1), poly_vector(line, 1)), "simple zero")
    require(not membership(jet_matrix(p, 1, 2), poly_vector(line, 1)), "double zero")
    compact = lambda x: json.dumps(x, separators=(",", ":"), sort_keys=True).encode()
    return {"status": "VERIFIED", "prime": PRIME, "fixtures": summaries,
            "certified_spaces_over_Q": len(audit),
            "jet_matrix_entries": sum(row[3]*row[4] for row in audit),
            "space_audit_sha256": sha256(compact(audit)).hexdigest(),
            "component_adjoint_sha256": sha256(compact(certificates)).hexdigest(),
            "first_failure_forms": first_failure_forms,
            "boundary_controls": boundary, "invalid_inputs_rejected": rejected,
            "additional_controls": ["omitted point condition", "simple vs double zero"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="emit deterministic evidence without comparing expected.json")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True)+"\n"
    if not args.emit:
        expected = Path(__file__).with_name("expected.json").read_text()
        require(encoded == expected, "evidence differs from expected.json")
    print(encoded, end="")


if __name__ == "__main__":
    main()
