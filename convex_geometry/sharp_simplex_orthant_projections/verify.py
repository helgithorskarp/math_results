"""Exact author checks for the geometric theorem in PROOF.md.

CPython 3.11+, standard library only. No floating-point geometry or solver.
"""
from copy import deepcopy
from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product
from math import comb, factorial, gcd
from pathlib import Path
import hashlib
import json


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


def parameter(c):
    require(len(c) >= 2 and min(c) >= 0 and sum(c) == 1,
            "invalid barycentric parameter")


def envelope_inequalities(c):
    """Expand sum max(|w_i|,c_i)<=2; eliminate w_N=-sum of other w_i."""
    parameter(c)
    n = len(c)-1
    result = {}
    for signs in product((-1, 0, 1), repeat=n+1):
        a = tuple(s-signs[-1] for s in signs[:-1])
        b = F(2)-sum(c[i] for i, s in enumerate(signs) if s == 0)
        if not any(a):
            require(b >= 0, "inconsistent constant inequality")
            continue
        divisor = reduce(gcd, (abs(x) for x in a))
        a = tuple(x//divisor for x in a)
        b /= divisor
        result[a] = min(result.get(a, b), b)
    return sorted(result.items())


def planar_joint_image(c):
    """Independent representation: lambda,mu>=0; sums1; lambda+mu>=c.

Variables are lambda0,lambda1,mu0,mu1. The last coordinate of each
probability vector is eliminated separately, leaving nine inequalities.
"""
    parameter(c)
    require(len(c) == 3, "joint image is planar")
    inequalities = []
    for i in range(4):
        a = [0]*4
        a[i] = -1
        inequalities.append((tuple(a), F(0)))
    inequalities += [((1, 1, 0, 0), F(1)), ((0, 0, 1, 1), F(1)),
                     ((-1, 0, -1, 0), -c[0]),
                     ((0, -1, 0, -1), -c[1]),
                     ((1, 1, 1, 1), 2-c[2])]
    raw = vertices(inequalities)
    return hull((v[0]-v[2], v[1]-v[3]) for v in raw)


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


def section_polygon3(points, z):
    candidates = [p[:2] for p in points if p[2] == z]
    for a, b in combinations(points, 2):
        if a[2] > b[2]:
            a, b = b, a
        if a[2] < b[2] and a[2] <= z <= b[2]:
            t = (z-a[2])/(b[2]-a[2])
            candidates.append(tuple((1-t)*a[i]+t*b[i] for i in range(2)))
    return hull(candidates)


def sliced_volume3(points):
    """All sections from raw generators; Simpson is exact on every vertex slab."""
    levels = sorted({p[2] for p in points})
    volume = F(0)
    for lo, hi in zip(levels, levels[1:]):
        a, b, c = (area(section_polygon3(points, z))
                   for z in (lo, (lo+hi)/2, hi))
        volume += (hi-lo)*(a+4*b+c)/6
    return volume, len(levels)-1


def sliced_area2(points):
    levels = sorted({p[0] for p in points})
    heights = []
    for x in levels:
        ys = [p[1] for p in points if p[0] == x]
        for a, b in combinations(points, 2):
            if a[0] > b[0]:
                a, b = b, a
            if a[0] < b[0] and a[0] <= x <= b[0]:
                ys.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
        require(bool(ys), "empty vertical section")
        heights.append(max(ys)-min(ys))
    return sum((levels[i+1]-levels[i])*(heights[i]+heights[i+1])/2
               for i in range(len(levels)-1))


def certify_polygon(points, polygon, expected):
    require(len(polygon) >= 3 and len(set(polygon)) == len(polygon),
            "invalid polygon list")
    require(all(p in points for p in polygon), "non-generator vertex")
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        slacks = [cross(a, b, p) for p in points]
        require(min(slacks) >= 0 and max(slacks) > 0, "failed supporting edge")
    require(area(polygon) == expected > 0, "incorrect polygon area")
    require(sliced_area2(points) == expected, "vertical area mismatch")


def check_lift(w):
    a = [list(map(F, row)) for row in w["matrix"]]
    require(len(a) == 2 and len(a[0]) == len(a[1]), "bad matrix shape")
    m = len(a[0])
    pairs = w["coordinate_pairs"]
    require(all(len(pair) == 2 and pair[0] != pair[1]
                and all(isinstance(i, int) and 0 <= i < m for i in pair)
                for pair in pairs), "bad coordinate square")
    require({i for pair in pairs for i in pair} == set(range(m)),
            "a coordinate axis is missing")
    gram = [[dot(x, y) for y in a] for x in a]
    det = gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    require(det > 0, "rank below two")
    require(gram == w["gram"] and det == F(w["gram_determinant"]), "wrong Gram data")
    inv = [[gram[1][1]/det, -gram[0][1]/det],
           [-gram[1][0]/det, gram[0][0]/det]]
    columns = list(zip(*a))
    p = [[sum(columns[i][r]*inv[r][s]*columns[j][s]
              for r in range(2) for s in range(2))
          for j in range(m)] for i in range(m)]
    require(all(sum(p[i][k]*p[k][j] for k in range(m)) == p[i][j]
                for i in range(m) for j in range(m)), "projection not idempotent")
    require(sum(p[i][i] for i in range(m)) == 2, "projection trace")
    require(all(p[i][j] == p[j][i] for i in range(m) for j in range(m)),
            "projection not symmetric")
    require(all(sum(a[r][k]*p[k][j] for k in range(m)) == a[r][j]
                for r in range(2) for j in range(m)), "A != A P")
    values = []
    counts = []
    for positive, key in ((False, "full"), (True, "positive")):
        points = {tuple(s*a[r][i]+t*a[r][j] for r in range(2))
                  for i, j in pairs
                  for s, t in product((0, 1) if positive else (-1, 1), repeat=2)}
        polygon = [tuple(map(F, x)) for x in w[key+"_polygon"]]
        expected = F(w[key+"_area"])
        certify_polygon(points, polygon, expected)
        values.append(expected)
        counts.append(dict(generators=len(points),vertices=len(polygon),
                           supporting_tests=len(points)*len(polygon)))
    require(values[0]/values[1] == F(16, 3), "lift does not attain16/3")
    return dict(ambient_dimension=m,gram_determinant=str(det),
                full_area=str(values[0]),positive_area=str(values[1]),
                ratio=str(values[0]/values[1]),images=counts)


def negative_controls(w):
    bad = []
    x = deepcopy(w); x["full_area"] = "71"; bad.append(("wrong full area", x))
    x = deepcopy(w); del x["full_polygon"][0]; bad.append(("missing full vertex", x))
    x = deepcopy(w); x["positive_area"] = "14"; bad.append(("wrong positive area", x))
    x = deepcopy(w); x["coordinate_pairs"] = x["coordinate_pairs"][2:]
    bad.append(("missing coordinate axes", x))
    x = deepcopy(w); x["matrix"][1] = x["matrix"][0][:]
    bad.append(("rank-one map", x))
    for name, x in bad:
        try:
            check_lift(x)
        except ValueError:
            continue
        raise ValueError("accepted malformed lift: "+name)
    for c in ((F(1),F(1),F(0)), (F(-1),F(1),F(1))):
        try:
            envelope_inequalities(c)
        except ValueError:
            continue
        raise ValueError("accepted invalid barycentric vector")
    return [name for name, _ in bad]+["wrong barycentric sum", "negative barycentric coordinate"]


def main():
    w = json.loads((Path(__file__).parent/"WITNESS.json").read_text())
    lift = check_lift(w)
    for c in ((F(0),F(1)), (F(1,2),F(1,2)), (F(1),F(0))):
        interval = vertices(envelope_inequalities(c))
        require(interval[-1][0]-interval[0][0] == 2, "C1 mismatch")
    planar = []
    for i in range(7):
        for j in range(7-i):
            c = (F(i,6), F(j,6), F(6-i-j,6))
            ring = hull(vertices(envelope_inequalities(c)))
            other = planar_joint_image(c)
            require(ring == other, "two planar descriptions disagree")
            ratio = 2*area(ring)
            require(ratio == 6-2*sum(x*x for x in c), "planar formula mismatch")
            planar.append(dict(c=list(map(str,c)),ratio=str(ratio),vertices=len(ring)))
    inequalities = envelope_inequalities((F(1,4),)*4)
    vs = vertices(inequalities)
    volume, faces, triangles = facet_volume3(inequalities, vs)
    sliced, slabs = sliced_volume3(vs)
    require(volume == sliced and 6*volume == F(127,8), "C3 volume mismatch")
    bounds = []
    known = {1:F(2),2:F(16,3),3:F(127,8)}
    for n in range(1,13):
        size = n+1
        whole = 2**size*sum(F(comb(size,j)*size**j,factorial(j))
                           for j in range(size+1))
        lo = F(factorial(n),4*size**size)*whole
        hi = size*lo
        if n in known:
            require(lo <= known[n] <= hi, "finite constant violates section bounds")
        bounds.append(dict(n=n,whole_volume=str(whole),lower=str(lo),upper=str(hi)))
    record = json.dumps(planar,sort_keys=True,separators=(",",":"))
    output = dict(
        status="VERIFIED_SHARP_SIMPLEX_PROJECTION_CERTIFICATES",
        lift=lift,
        planar_grid=dict(denominator=6,cases=len(planar),
                         sha256=hashlib.sha256(record.encode()).hexdigest(),
                         minimum=str(min(F(x["ratio"]) for x in planar)),
                         maximum=str(max(F(x["ratio"]) for x in planar))),
        three_dimensional=dict(C3=str(6*volume),vertices=len(vs),facets=faces,
                               facet_triangles=triangles,vertical_slabs=slabs,
                               two_volume_methods_agree=True),
        rational_section_bounds=bounds,
        rejected_corruptions=negative_controls(w),
        scope="Finite certificates only; realization, strict concavity and asymptotic rate use PROOF.md."
    )
    print(json.dumps(output,sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
