#!/usr/bin/env python3
"""Independent exact audit of the radius-67 triangular-overlay census.

This checker deliberately does not import the submitted producer or verifier.  It
works in Cartesian coordinates X+i*sqrt(3)Y, represents rational rotations by
primitive integer triples, and constructs every rational union graph directly.
For irrational events it groups contacts by their primitive line on the unit
ellipse; distinct irrational lines cannot share a root (the proof is in README).
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt, lcm
import json


RADIUS = 67
EXPECTED_CENSUS = [
    [253, 702, 3, 6],
    [469, 1404, 3, 12],
    [487, 1404, 3, 12],
    [493, 1404, 3, 12],
    [499, 1404, 3, 60],
    [499, 1434, 3, 12],
    [505, 1410, 3, 252],
    [505, 1410, 4, 168],
    [505, 1416, 3, 900],
    [505, 1416, 4, 228],
    [505, 1422, 3, 12],
    [505, 1428, 3, 48],
    [505, 1440, 3, 24],
]


def en_norm(z):
    a, b = z
    return a * a + a * b + b * b


def en_conj(z):
    a, b = z
    return a + b, -b


def en_mul(z, w):
    a, b = z
    c, d = w
    return a * c - b * d, a * d + b * c + b * d


def cart(z):
    """Twice the Cartesian coordinates in the basis (1, i*sqrt(3))."""
    a, b = z
    return 2 * a + b, b


def rho(z):
    return (z[0] - z[1]) % 3


def primitive_line(u, v, k):
    g = gcd(gcd(abs(u), abs(v)), abs(k))
    u, v, k = u // g, v // g, k // g
    for q in (u, v, k):
        if q:
            if q < 0:
                u, v, k = -u, -v, -k
            break
    return u, v, k


def rational_key(x, y):
    """Primitive (R,T,N) for alpha=(R+i*sqrt(3)T)/N."""
    n = lcm(x.denominator, y.denominator)
    r = x.numerator * (n // x.denominator)
    t = y.numerator * (n // y.denominator)
    g = gcd(gcd(abs(r), abs(t)), n)
    r, t, n = r // g, t // g, n // g
    if n < 0:
        r, t, n = -r, -t, -n
    assert r * r + 3 * t * t == n * n
    return r, t, n


def line_rational_roots(line):
    """Return the rational intersections of ux+vy=k and x^2+3y^2=1."""
    u, v, k = line
    h = 3 * u * u + v * v
    disc = h - 3 * k * k
    if disc < 0:
        return []
    s = isqrt(disc)
    if s * s != disc:
        return []
    roots = set()
    signs = (1,) if s == 0 else (1, -1)
    for sign in signs:
        x = Fraction(3 * u * k + sign * v * s, h)
        y = Fraction(v * k - sign * u * s, h)
        assert u * x + v * y == k
        assert x * x + 3 * y * y == 1
        roots.add(rational_key(x, y))
    return roots


def forced_three_coloring(points, edges):
    """Find a triangle whose fixed palette forces every other patch vertex."""
    adj = [set() for _ in points]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    triangles = []
    for i, j in edges:
        for k in adj[i] & adj[j]:
            if j < k:
                triangles.append((i, j, k))
    for triangle in triangles:
        colors = dict(zip(triangle, (0, 1, 2)))
        changed = True
        while changed:
            changed = False
            for vertex in range(len(points)):
                if vertex in colors:
                    continue
                seen = {colors[nbr] for nbr in adj[vertex] if nbr in colors}
                if len(seen) >= 2:
                    if len(seen) != 2:
                        break
                    colors[vertex] = ({0, 1, 2} - seen).pop()
                    changed = True
            else:
                continue
            break
        if len(colors) == len(points) and all(colors[i] != colors[j] for i, j in edges):
            return len(points) - 3
    raise AssertionError("no triangle-forced 3-colouring found")


def rational_graph(angle, points, xy, seed_edges):
    """Construct P union alpha*P over one integer denominator."""
    r, t, n = angle
    first = [(n * x, n * y) for x, y in xy]
    second = [(r * x - 3 * t * y, t * x + r * y) for x, y in xy]

    ids = {}
    for p in first + second:
        ids.setdefault(p, len(ids))
    first_ids = [ids[p] for p in first]
    second_ids = [ids[p] for p in second]

    edges = set()
    for i, j in seed_edges:
        edges.add(tuple(sorted((first_ids[i], first_ids[j]))))
        edges.add(tuple(sorted((second_ids[i], second_ids[j]))))

    threshold = 4 * n * n
    contacts = 0
    for i, (ax, ay) in enumerate(first):
        ii = first_ids[i]
        for j, (bx, by) in enumerate(second):
            dx, dy = ax - bx, ay - by
            if dx * dx + 3 * dy * dy == threshold:
                contacts += 1
                jj = second_ids[j]
                assert ii != jj
                edges.add((ii, jj) if ii < jj else (jj, ii))

    # Independently instantiate the localized Eisenstein-residue colouring.
    assert n % 3
    factor = (r * pow(n, -1, 3)) % 3
    colors = {}
    for i, p in enumerate(first):
        colors[ids[p]] = rho(points[i])
    for i, p in enumerate(second):
        c = factor * rho(points[i]) % 3
        old = colors.setdefault(ids[p], c)
        assert old == c
    assert all(colors[i] != colors[j] for i, j in edges)

    coincidences = sum(p == q for p in first for q in second)
    return len(ids), len(edges), 3, contacts, coincidences


def main():
    points = sorted(
        (a, b)
        for a in range(-RADIUS, RADIUS + 1)
        for b in range(-RADIUS, RADIUS + 1)
        if en_norm((a, b)) <= RADIUS
    )
    xy = [cart(z) for z in points]
    assert len(points) == 253

    seed_edges = []
    for i, j in combinations(range(len(points)), 2):
        da = points[i][0] - points[j][0]
        db = points[i][1] - points[j][1]
        if en_norm((da, db)) == 1:
            seed_edges.append((i, j))
    assert len(seed_edges) == 702
    forced_steps = forced_three_coloring(points, seed_edges)
    assert forced_steps == 250

    nonzero = [i for i, z in enumerate(points) if z != (0, 0)]
    contacts = defaultdict(list)
    for i in nonzero:
        z = points[i]
        nz = en_norm(z)
        zbar = en_conj(z)
        for j in nonzero:
            w = points[j]
            nw = en_norm(w)
            a, b = en_mul(w, zbar)
            line = primitive_line(2 * a + b, -3 * b, nz + nw - 1)
            u, v, k = line
            if 3 * u * u + v * v - 3 * k * k >= 0:
                contacts[line].append((i, j))
    assert len(contacts) == 1542

    irrational = {}
    rational_angles = set()
    for line, pairs in contacts.items():
        u, v, k = line
        disc = 3 * u * u + v * v - 3 * k * k
        s = isqrt(disc)
        if disc > 0 and s * s != disc:
            irrational[line] = pairs
        else:
            rational_angles.update(line_rational_roots(line))
    assert len(irrational) == 624

    coincidence_angles = set()
    for i in nonzero:
        zx, zy = xy[i]
        nz = en_norm(points[i])
        for j in nonzero:
            if en_norm(points[j]) != nz:
                continue
            wx, wy = xy[j]
            x = Fraction(zx * wx + 3 * zy * wy, 4 * nz)
            y = Fraction(zy * wx - zx * wy, 4 * nz)
            coincidence_angles.add(rational_key(x, y))
    assert len(coincidence_angles) == 114
    rational_angles.update(coincidence_angles)
    assert len(rational_angles) == 498

    census = Counter()
    contact_checks = 0
    rational_coincidences = 0
    for angle in sorted(rational_angles):
        vertices, edges, chi, contacts_here, coincidences = rational_graph(
            angle, points, xy, seed_edges
        )
        census[(vertices, edges, chi)] += 1
        contact_checks += contacts_here
        rational_coincidences += coincidences
    assert rational_coincidences == 3234

    for line, pairs in irrational.items():
        # Each nonsquare-discriminant line has two roots, and exactly these
        # ordered nonzero pairs are contacts at either root.
        # There are also twelve universal origin contacts for each root.
        contact_checks += 2 * (len(pairs) + 12)
        nonzero_products = {
            rho(points[i]) * rho(points[j]) % 3
            for i, j in pairs
            if rho(points[i]) and rho(points[j])
        }
        assert len(nonzero_products) <= 1
        has_zero_zero = any(rho(points[i]) == rho(points[j]) == 0 for i, j in pairs)
        chi = 4 if has_zero_zero else 3
        census[(505, 1404 + len(pairs), chi)] += 2
    assert contact_checks == 61488

    observed_census = [list(key) + [count] for key, count in sorted(census.items())]
    assert observed_census == EXPECTED_CENSUS
    four = sum(count for (v, e, chi), count in census.items() if chi == 4)
    three = sum(count for (v, e, chi), count in census.items() if chi == 3)
    assert (three, four) == (1350, 396)

    # Moser's angle alpha=(5+i*sqrt(11))/6 is irrational over Q(sqrt(-3)).
    # For z=1+omega, N(z)=3 and |1-alpha|^2=1/3, so the zero-residue
    # cross contact has unit length and rules out three colours.
    assert en_norm((1, 1)) == 3 and rho((1, 1)) == 0
    assert Fraction(3) * (Fraction(2) - 2 * Fraction(5, 6)) == 1

    summary = {
        "contact_lines": len(contacts),
        "exceptional_rotations": len(rational_angles) + 2 * len(irrational),
        "forced_triangle_steps": forced_steps,
        "four_chromatic_exceptional_rotations": four,
        "generic_graph": [505, 1404, 3],
        "irrational_lines": len(irrational),
        "nonzero_coincidence_rotations": len(coincidence_angles),
        "patch_edges": len(seed_edges),
        "patch_vertices": len(points),
        "rational_coincidences_including_origins": rational_coincidences,
        "rational_rotations": len(rational_angles),
        "three_chromatic_exceptional_rotations": three,
        "unit_contacts_including_both_irrational_roots": contact_checks,
        "verified": True,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
