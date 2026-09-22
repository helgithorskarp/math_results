"""Definition-level rational checks; geometry helpers adapted from the preceding
sharp_simplex_orthant_projections/verify.py (same author, different volume method).
This is not an independent peer review.
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import reduce
from math import gcd


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def solve(a, b):
    n = len(b)
    m = [list(map(F, row))+[F(x)] for row, x in zip(a, b)]
    for i in range(n):
        k = next((k for k in range(i, n) if m[k][i]), None)
        if k is None:
            return None
        m[i], m[k] = m[k], m[i]
        q = m[i][i]
        m[i] = [x/q for x in m[i]]
        for j in range(n):
            if j != i:
                q = m[j][i]
                m[j] = [x-q*y for x, y in zip(m[j], m[i])]
    return tuple(row[-1] for row in m)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    chains = []
    for seq in (points, points[::-1]):
        chain = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        chains.append(chain[:-1])
    return chains[0]+chains[1]


def area(polygon):
    return F(sum(a[0]*b[1]-a[1]*b[0]
                 for a, b in zip(polygon, polygon[1:]+polygon[:1])), 2)


def vertices(inequalities):
    """Complete active-constraint enumeration of a bounded full-dimensional set."""
    n = len(inequalities[0][0])
    result = set()
    for indices in combinations(range(len(inequalities)), n):
        x = solve([inequalities[i][0] for i in indices],
                  [inequalities[i][1] for i in indices])
        if x is not None and x not in result:
            if all(dot(a, x) <= b for a, b in inequalities):
                result.add(x)
    require(bool(result), "empty vertex enumeration")
    return sorted(result)


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def facet_volume3(inequalities, points):
    """Cone from0 to each polygonal facet, then sum tetrahedron volumes."""
    determinants = []
    facets = 0
    for normal, b in inequalities:
        face = [x for x in points if dot(normal, x) == b]
        if len(face) < 3:
            continue
        k = next(k for k, a in enumerate(normal) if a)
        other = [i for i in range(3) if i != k]
        decode = {tuple(x[i] for i in other): x for x in face}
        ring = hull(decode)
        if len(ring) < 3:
            continue
        facets += 1
        ring = [decode[x] for x in ring]
        require(b > 0, "origin is not strictly inside")
        determinants.extend(abs(det3(ring[0], ring[i], ring[i+1]))
                            for i in range(1, len(ring)-1))
    return sum(determinants)/6, facets, len(determinants)


def inequalities(N, radius):
    result = {}
    for signs in product((-1, 0, 1), repeat=N):
        a = tuple(s - signs[-1] for s in signs[:-1])
        b = F(radius) + sum(bool(s) for s in signs)
        if not any(a):
            continue
        divisor = reduce(gcd, (abs(x) for x in a))
        a = tuple(x // divisor for x in a)
        b /= divisor
        result[a] = min(result.get(a, b), b)
    return sorted(result.items())


def direct_section(N, radius):
    """Eliminate the last coordinate; volume equals intrinsic volume/sqrt(N)."""
    require(N in (2, 3, 4), "direct check supports N=2,3,4")
    constraints = inequalities(N, radius)
    points = vertices(constraints)
    if N == 2:
        return max(p[0] for p in points) - min(p[0] for p in points)
    if N == 3:
        return area(hull(points))
    return facet_volume3(constraints, points)[0]
