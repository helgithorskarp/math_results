"""Exact finite checks and an interpolation identity certificate.

CPython 3.11+, standard library only. No floating-point geometry or solver.
The continuum optimality proof is in PROOF.md.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def determinant(a, b):
    return a[0]*b[1]-a[1]*b[0]


def cross(a, b, c):
    return determinant((b[0]-a[0], b[1]-a[1]),
                       (c[0]-a[0], c[1]-a[1]))


def hull(points):
    points = sorted(set(points))
    if len(points) < 2:
        return points
    chains = []
    for sequence in (points, points[::-1]):
        chain = []
        for p in sequence:
            while len(chain) > 1 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        chains.append(chain[:-1])
    return chains[0]+chains[1]


def area(polygon):
    return sum((determinant(p, q) for p, q in
                zip(polygon, polygon[1:]+polygon[:1])), F(0))/2


def halfplanes(polygon):
    return [(b[1]-a[1], a[0]-b[0], determinant(a, b))
            for a, b in zip(polygon, polygon[1:]+polygon[:1])]


def inside(point, constraints):
    return all(a*point[0]+b*point[1] <= c for a, b, c in constraints)


def solve(matrix, rhs):
    n = len(rhs)
    rows = [list(map(F, row))+[F(b)] for row, b in zip(matrix, rhs)]
    for i in range(n):
        k = next((k for k in range(i, n) if rows[k][i]), None)
        if k is None:
            return None
        rows[i], rows[k] = rows[k], rows[i]
        value = rows[i][i]
        rows[i] = [x/value for x in rows[i]]
        for j in range(n):
            if j != i:
                value = rows[j][i]
                rows[j] = [x-value*y for x, y in zip(rows[j], rows[i])]
    return tuple(row[-1] for row in rows)


def original_joint_envelope(polygon, origin):
    """Enumerate all vertices of the bounded four-dimensional (x,y) body."""
    constraints = halfplanes(polygon)
    require(area(polygon) > 0 and inside(origin, constraints), "invalid Q or origin")
    rows = []
    for a, b, c in constraints:
        rows.extend([((a, b, 0, 0), c), ((0, 0, a, b), c),
                     ((a, b, a, b), c+a*origin[0]+b*origin[1])])
    points = set()
    for active in combinations(rows, 4):
        x = solve([a for a, _ in active], [b for _, b in active])
        if x is not None and all(sum(a[i]*x[i] for i in range(4)) <= b
                                 for a, b in rows):
            points.add(x)
    require(bool(points), "no joint vertices")
    image = hull((x[0]-x[2], x[1]-x[3]) for x in points)
    return image, len(points)


def sliced_area(points):
    """Independent vertical-section integration from the point generators."""
    levels = sorted({p[0] for p in points})
    heights = []
    for u in levels:
        candidates = [p[1] for p in points if p[0] == u]
        for p, q in combinations(points, 2):
            if p[0] > q[0]:
                p, q = q, p
            if p[0] < q[0] and p[0] <= u <= q[0]:
                candidates.append(p[1]+(q[1]-p[1])*(u-p[0])/(q[0]-p[0]))
        heights.append(max(candidates)-min(candidates))
    return sum(((levels[i+1]-levels[i])*(heights[i]+heights[i+1])/2
                for i in range(len(levels)-1)), F(0))


def kite(b):
    return hull([(-F(1), F(0)), (F(1), F(0)), (F(0), F(1)), (F(0), -b)])


def maximizing_height(b):
    return (1+3*b*b)/(3+b*b)


def kite_ratio(b):
    return 4+4*(1-b)/(3+b*b)


def boundary_arc(b, a, c):
    def right(a):
        return [((2-b-c-b*a)/(1-b), (c-b+b*a)/(1-b)),
                ((3-c+a)/2, (1+c-a)/2),
                ((b+c-a)/(1+b), (1+2*b-b*c+b*a)/(1+b))]
    first = [(2+b-c, -a)]+right(a)+[(F(0), 1+b)]
    reflected = [(-u, v) for u, v in right(-a)[::-1]]
    return first+reflected


def local_polygon(b, a, c):
    arc = boundary_arc(b, a, c)
    return arc+[(-u, -v) for u, v in arc]


def area_polynomial(b, a, c):
    return (5+4*b-9*b*b-4*b**3+2*(1+3*b*b)*c
            -(1+3*b*b)*a*a-(3+b*b)*c*c)/(1-b*b)


def upper_constraints(b, a, c):
    positive = [(1, 1, F(2)), (1, -1, F(2)),
                (b, 1, 1+b), (b, -1, 1+b),
                (1, b, 2+b-c-b*a), (1, -b, 2+b-c+b*a),
                (1+3*b, 3+b, 3+5*b+(1-b)*c-(1-b)*a),
                (1+3*b, -3-b, 3+5*b+(1-b)*c+(1-b)*a)]
    return positive+[(-u, -v, d) for u, v, d in positive]


def dual_identities():
    """Positive normal cancellations and their resulting right-hand sides."""
    for b in (F(1, 7), F(1, 3), F(1, 2), F(6, 7)):
        circuits = [
            ([(1, 1), (-1, 1), (-b, -1)],
             [(1+b)/2, (1-b)/2, F(1)], [F(1), F(1), b],
             (1, b), 2+b, (-b, -F(1))),
            ([(1, 1), (-b, -1), (-1, 1)],
             [1+b, F(2), 1-b], [F(1), b, F(1)],
             (1+3*b, 3+b), 3+5*b, (b-1, 1-b))]
        for normals, weights, bounds, normal, bound, center in circuits:
            require(min(weights) > 0, "nonpositive dual weight")
            require(all(sum(w*n[i] for w, n in zip(weights, normals)) == 0
                        for i in (0, 1)), "failed normal cancellation")
            require(tuple(weights[0]*normals[0][i]-weights[1]*normals[1][i]
                          for i in (0, 1)) == normal, "wrong dual normal")
            require(2*weights[0]*bounds[0]+2*weights[1]*bounds[1]
                    + weights[2]*bounds[2] == bound, "wrong dual bound")
            require(tuple(weights[2]*x for x in normals[2]) == center,
                    "wrong origin coefficients")
    return 8


def interpolation_certificate():
    # After clearing 1-b^2, degrees are <=(3,2,2) in (b,a,c);
    # PROOF.md derives the degree bound directly from adjacent vertices.
    count = 0
    for b, a, c in product([F(i, 5) for i in range(1, 5)],
                           [F(-1), F(0), F(1)], [F(0), F(1), F(2)]):
        require(area(local_polygon(b, a, c)) == area_polynomial(b, a, c),
                "local polynomial identity failed")
        count += 1
    return dict(grid=[4, 3, 3], exact_evaluations=count, cleared_degrees=[3, 2, 2])


def preimages(b, c):
    require(0 < b < c < 1, "outside axis chamber")
    arc = boundary_arc(b, F(0), c)[:5]
    u, _ = arc[0]
    x0, y0 = (u/2, (c-b)/2), (-u/2, (c-b)/2)
    u, v = arc[1]; x1, y1 = (1-v, v), (-F(1), F(0))
    u, v = arc[2]; x2, y2 = (u-1, v), (-F(1), F(0))
    u, v = arc[3]; x3, y3 = (F(0), F(1)), (-u, 1-v)
    x4, y4 = (F(0), F(1)), (F(0), -b)
    q = kite(b); constraints = halfplanes(q)
    for p, (x, y) in zip(arc, [(x0,y0),(x1,y1),(x2,y2),(x3,y3),(x4,y4)]):
        require((x[0]-y[0], x[1]-y[1]) == p, "wrong vertex preimage")
        require(inside(x, constraints) and inside(y, constraints)
                and inside((x[0]+y[0], x[1]+y[1]-c), constraints),
                "infeasible vertex preimage")
    polygon = local_polygon(b, F(0), c)
    require(hull(polygon) == hull(arc+[(-u,v) for u,v in arc]
                                  +[(u,-v) for u,v in arc]
                                  +[(-u,-v) for u,v in arc]), "reflection mismatch")
    require(all(inside(p, upper_constraints(b, 0, c)) for p in polygon),
            "claimed vertex violates upper bound")
    require(area(polygon) == sliced_area(polygon), "independent area mismatch")
    return polygon


def check_fixture(fixture):
    q = hull([tuple(map(F, p)) for p in fixture["polygon"]])
    origin = tuple(map(F, fixture["origin"]))
    envelope, joint_vertices = original_joint_envelope(q, origin)
    value = area(envelope)/area(q)
    require(value == F(fixture["ratio"]), "wrong fixture ratio")
    require(sliced_area(envelope) == area(envelope), "fixture area mismatch")
    if "shadow_parameter" in fixture:
        s = F(fixture["shadow_parameter"])
        require(0 <= s <= 2, "invalid shadow parameter")
        expected_q = hull([(-F(1), F(0)), (F(1), F(0)), (s, F(1)), (F(0), -F(1))])
        require(q == expected_q and area(q) == 2, "wrong chord-movement body")
        require(value == 6-8/(s*s+2*s+4), "wrong optimized shadow formula")
        if s:
            expected_origin = ((s*s+2*s-4)/(s*s+2*s+4), F(0))
            require(origin == expected_origin, "wrong optimizing origin")
            b = (2-s)/(2+s)
            transform = lambda p: (p[1], (s-2*p[0]+s*p[1])/(2+s))
            require(hull(map(transform, q)) == kite(b), "wrong affine identification")
            require(transform(origin) == (0, maximizing_height(b)), "origin map failed")
    return dict(name=fixture["name"], ratio=str(value),
                envelope_vertices=len(envelope), joint_vertices=joint_vertices)


def main():
    fixtures = json.loads((Path(__file__).parent/"WITNESS.json").read_text())
    rows = [check_fixture(fixture) for fixture in fixtures]
    grid_digest = hashlib.sha256()
    count = 0
    for b in (F(1, 10), F(1, 3), F(1, 2), F(2, 3), F(4, 5)):
        for c in (b+(1-b)/4, maximizing_height(b), b+3*(1-b)/4):
            claimed = preimages(b, c)
            actual, _ = original_joint_envelope(kite(b), (F(0), c))
            require(hull(claimed) == actual, "original-definition envelope mismatch")
            require(area(actual) == area_polynomial(b, 0, c), "axis area mismatch")
            if c == maximizing_height(b):
                require(area(actual)/area(kite(b)) == kite_ratio(b), "kite maximum mismatch")
            grid_digest.update((str(b)+";"+str(c)+";"+str(area(actual))+"\n").encode())
            count += 1
    midpoint_gap = F(94,21)-(F(4)+F(34,7))/2
    require(midpoint_gap == F(1,21) > 0, "no convexity obstruction")
    require(F(34,7)-F(1031,216) == F(127,1512) > 0, "no centroid obstruction")
    rejected = []
    for name, field, value in [("wrong ratio","ratio","5"),
                               ("wrong maximizing origin","origin",["0","0"]),
                               ("outside origin","origin",["10","10"])]:
        bad = deepcopy(fixtures[1]); bad[field] = value
        try:
            check_fixture(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: "+name)
    print(json.dumps(dict(status="VERIFIED_SHADOW_CONVEXITY_OBSTRUCTION",
                          fixtures=rows, axis_cases=count, axis_sha256=grid_digest.hexdigest(),
                          dual_circuits=dual_identities(),
                          identity=interpolation_certificate(),
                          midpoint_excess=str(midpoint_gap),
                          centroid_deficit="127/1512",
                          rejected_corruptions=rejected,
                          scope="Global planar optimum unresolved; continuum kite optimization uses PROOF.md."),
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
