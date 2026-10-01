"""Independent exact J74 audit; six-reviewer-4, independent reviewer.

No author modules or runtime data are imported. Integer-pair geometry uses
coordinates scaled by 20, exhaustive supporting triples, and lexicographic
infinitesimal chamber perturbations (no tangent-ray sorting). The optional
source comparison parses only literal arithmetic/model assignments.
"""

import argparse
import ast
from collections import Counter
from fractions import Fraction
from functools import total_ordering
import hashlib
from itertools import combinations, product
import json
from math import comb, gcd
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def minus(x, y):
    return (x[0] - y[0], x[1] - y[1])


def times(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sign(x):
    a, b = x
    if not a:
        return (b > 0) - (b < 0)
    if not b or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    norm = a * a - 5 * b * b
    need(norm != 0, "irrationality of sqrt5")
    return ((norm > 0) - (norm < 0)) * ((a > 0) - (a < 0))


@total_ordering
class S:
    """(a+b*sqrt5)/d with common integer denominator, never float arithmetic."""
    __slots__ = ("a", "b", "d")

    def __init__(self, a=0, b=0, d=1):
        if isinstance(a, S):
            self.a, self.b, self.d = a.a, a.b, a.d
            return
        need(isinstance(a, int) and isinstance(b, int) and isinstance(d, int), "integer surd data")
        need(d != 0, "nonzero denominator")
        if d < 0:
            a, b, d = -a, -b, -d
        g = gcd(gcd(abs(a), abs(b)), d)
        self.a, self.b, self.d = a // g, b // g, d // g

    def __add__(self, other):
        o = S(other)
        return S(self.a * o.d + o.a * self.d, self.b * o.d + o.b * self.d, self.d * o.d)
    __radd__ = __add__

    def __neg__(self):
        return S(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + -S(other)

    def __rsub__(self, other):
        return S(other) + -self

    def __mul__(self, other):
        o = S(other)
        a, b = times((self.a, self.b), (o.a, o.b))
        return S(a, b, self.d * o.d)
    __rmul__ = __mul__

    def __truediv__(self, other):
        o = S(other)
        a, b = times((self.a, self.b), (o.a, -o.b))
        return S(a * o.d, b * o.d, self.d * (o.a * o.a - 5 * o.b * o.b))

    def __rtruediv__(self, other):
        return S(other) / self

    def __pow__(self, exponent):
        need(isinstance(exponent, int) and exponent >= 0, "nonnegative integer power")
        out = S(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        o = S(other)
        return (self.a, self.b, self.d) == (o.a, o.b, o.d)

    def __lt__(self, other):
        o = S(other)
        return sign((self.a * o.d - o.a * self.d, self.b * o.d - o.b * self.d)) < 0

    def __hash__(self):
        return hash((self.a, self.b, self.d))

    def __repr__(self):
        return f"({Fraction(self.a, self.d)})+({Fraction(self.b, self.d)})sqrt5"


def vsub(x, y):
    return tuple(minus(a, b) for a, b in zip(x, y))


def vscale(k, x):
    return tuple((k * a, k * b) for a, b in x)


def dot(x, y):
    out = (0, 0)
    for a, b in zip(x, y):
        out = plus(out, times(a, b))
    return out


def cross(x, y):
    return (minus(times(x[1], y[2]), times(x[2], y[1])),
            minus(times(x[2], y[0]), times(x[0], y[2])),
            minus(times(x[0], y[1]), times(x[1], y[0])))


def zero(x):
    return all(t == (0, 0) for t in x)


def axis(x):
    if zero(x):
        return None
    pivot = next(t for t in x if t != (0, 0))
    conjugate = (pivot[0], -pivot[1])
    y = tuple(times(t, conjugate) for t in x)
    g = 0
    for t in y:
        for c in t:
            g = gcd(g, abs(c))
    orient = next(t[0] for t in y if t != (0, 0))
    return tuple(((a if orient > 0 else -a) // g,
                  (b if orient > 0 else -b) // g) for a, b in y)


def as_fields(x, denominator=1):
    return tuple(S(a, b, denominator) for a, b in x)


def fdot(x, y):
    return sum((a * b for a, b in zip(x, y)), S())


def fcross(x, y):
    return (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0])


def construct():
    rid = set()
    for base in (((10, 0), (10, 0), (20, 10)),
                 ((0, 0), (15, 5), (25, 5)),
                 ((15, 5), (5, 5), (10, 10))):
        for signs in product((-1, 1), repeat=3):
            v = tuple((t * a, t * b) for t, (a, b) in zip(signs, base))
            for k in range(3):
                rid.add(v[k:] + v[:k])
    axes = (((0, 0), (1, 1), (2, 0)), ((0, 0), (-1, -1), (2, 0)))
    caps = [{v for v in rid if dot(a, v) == (90, 30)} for a in axes]
    need(len(rid) == 60 and [len(c) for c in caps] == [5, 5], "original and caps")
    need(caps[0].isdisjoint(caps[1]), "disjoint cupolas")
    cosine, sine_over_axis = S(1, 1, 4), S(-1, 1, 8)
    rotated = []
    for a, cap in zip(axes, caps):
        af = as_fields(a)
        base_ring = {v for v in rid if dot(a, v) == (50, 30)}
        need(len(base_ring) == 10 and
             {v for v in rid if sign(minus(dot(a, v), (50, 30))) > 0} == cap,
             "complete cupola above its ten-point base plane")
        need(cosine * cosine + sine_over_axis * sine_over_axis * fdot(af, af) == 1,
             "proper Rodrigues coefficients")
        result, rotated_ring = set(), set()
        for v in cap | base_ring:
            vf = as_fields(v)
            c = fcross(af, vf)
            t = (1 - cosine) * fdot(af, vf) / fdot(af, af)
            w = [cosine * vf[j] + t * af[j] + sine_over_axis * c[j] for j in range(3)]
            need(all(x.d == 1 for x in w), "coordinate scale20 is exact")
            target = tuple((x.a, x.b) for x in w)
            if v in cap:
                result.add(target)
            else:
                rotated_ring.add(target)
        need(rotated_ring == base_ring, "36-degree gyration preserves complete base decagon")
        rotated.append(result)
    vertices = sorted((rid - caps[0] - caps[1]) | rotated[0] | rotated[1])
    need(len(vertices) == 60 and all(dot(v, v) == (1100, 400) for v in vertices), "J74 model and radius")
    need(S(*dot(axes[0], axes[1])) / S(*dot(axes[0], axes[0])) == S(0, -1, 5), "meta axis angle")
    return vertices, rid


def facets(vertices):
    found = set()
    nonsupporting = collinear = 0
    for i, j, k in combinations(range(60), 3):
        normal = cross(vsub(vertices[j], vertices[i]), vsub(vertices[k], vertices[i]))
        if zero(normal):
            collinear += 1
            continue
        offset = dot(normal, vertices[i])
        orientation = 0
        coplanar = []
        for r, v in enumerate(vertices):
            side = sign(minus(dot(normal, v), offset))
            if not side:
                coplanar.append(r)
            elif not orientation:
                orientation = side
            elif side != orientation:
                nonsupporting += 1
                break
        else:
            need(orientation != 0, "full dimension")
            found.add(tuple(coplanar))
    cycles, vectors, edges = [], [], Counter()
    for face in sorted(found):
        adjacency = {i: [j for j in face if j != i and dot(vsub(vertices[j], vertices[i]),
                                                       vsub(vertices[j], vertices[i])) == (400, 0)] for i in face}
        need(all(len(a) == 2 for a in adjacency.values()), "regular facet edge graph")
        cycle = [face[0], adjacency[face[0]][0]]
        while len(cycle) < len(face):
            next_point, = [j for j in adjacency[cycle[-1]] if j != cycle[-2]]
            need(next_point not in cycle, "simple connected boundary cycle")
            cycle.append(next_point)
        need(cycle[0] in adjacency[cycle[-1]], "closed facet boundary")
        raw = ((0, 0),) * 3
        for i, j in zip(cycle, cycle[1:] + cycle[:1]):
            raw = tuple(plus(a, b) for a, b in zip(raw, cross(vertices[i], vertices[j])))
        if sign(dot(raw, vertices[cycle[0]])) < 0:
            cycle.reverse()
            raw = vscale(-1, raw)
        need(sign(dot(raw, vertices[cycle[0]])) > 0, "origin inside all hull facets")
        for i, j in zip(cycle, cycle[1:] + cycle[:1]):
            edge = vsub(vertices[j], vertices[i])
            for k in face:
                if k not in (i, j):
                    need(sign(dot(raw, cross(edge, vsub(vertices[k], vertices[i])))) > 0,
                         "complete convex boundary")
            edges[tuple(sorted((i, j)))] += 1
        cycles.append(cycle)
        vectors.append(raw)  # Physical area vector is raw/800.
    need(len(found) == 62 and Counter(map(len, found)) == {3: 20, 4: 30, 5: 12}, "all62 supporting facets")
    need(len(edges) == 120 and set(edges.values()) == {2}, "all120 edges")
    return found, cycles, vectors, {"triples": comb(60, 3), "collinear_triples": collinear,
                                    "nonsupporting_triples": nonsupporting,
                                    "facets": 62, "edges": 120}


def candidate_value(vectors, d):
    total = (0, 0)
    for b in vectors:
        x = dot(b, d)
        total = plus(total, x if sign(x) >= 0 else (-x[0], -x[1]))
    return S(*times(total, total)) / (1600 * 1600 * S(*dot(d, d)))


def zonotope(vectors):
    candidates = []
    seen = set()
    parallel = 0
    for i, j in combinations(range(len(vectors)), 2):
        d = axis(cross(vectors[i], vectors[j]))
        if d is None:
            parallel += 1
        elif d not in seen:
            seen.add(d)
            candidates.append(d)
    values = {d: candidate_value(vectors, d) for d in candidates}
    minimum = min(values.values())
    minima = sorted(d for d in candidates if values[d] == minimum)
    all_vertices = set()
    local_chambers = 0
    for d in candidates:
        base = [sign(dot(b, d)) for b in vectors]
        zeros = [i for i, s in enumerate(base) if not s]
        local = set()
        for i in zeros:
            tangent = cross(d, vectors[i])
            first = [sign(dot(vectors[j], tangent)) for j in zeros]
            second = [sign(dot(vectors[j], vectors[i])) for j in zeros]
            for tangent_sign, side in product((-1, 1), repeat=2):
                signs = list(base)
                for j, a, b in zip(zeros, first, second):
                    signs[j] = tangent_sign * a if a else side * b
                    need(signs[j] != 0, "lexicographic interior direction")
                local.add(tuple(signs))
        local_chambers += len(local)
        for signs in local:
            g = ((0, 0),) * 3
            for b, s in zip(vectors, signs):
                g = tuple(plus(x, (s * y[0], s * y[1])) for x, y in zip(g, b))
            all_vertices.add(g)  # Physical vertex is g/1600.
            all_vertices.add(vscale(-1, g))
    norms = {g: S(*dot(g, g)) / (1600 * 1600) for g in all_vertices}
    maximum = max(norms.values())
    maxima = sorted(set(axis(g) for g, value in norms.items() if value == maximum))
    need(len(all_vertices) - local_chambers + 2 * len(candidates) == 2, "zonotope incidence consistency")
    return values, minimum, minima, maximum, maxima, {"projective_facets": len(candidates),
                                                      "parallel_pairs": parallel,
                                                      "vertices": len(all_vertices),
                                                      "edges": local_chambers,
                                                      "facets": 2 * len(candidates)}


def projected_hull(vertices, d):
    # Jarvis boundary walk, followed by literal support-halfplane checks.
    unit = (((1, 0), (0, 0), (0, 0)), ((0, 0), (1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0)))
    u = next(cross(d, e) for e in unit if not zero(cross(d, e)))
    w = cross(d, u)
    points = {}
    for i, v in enumerate(vertices):
        points.setdefault((dot(v, u), dot(v, w)), i)
    indices = list(points.values())
    start = min(indices, key=lambda i: (S(*dot(vertices[i], u)), S(*dot(vertices[i], w))))

    def distance(i, j):
        v = vsub(vertices[j], vertices[i])
        return S(*dot(v, v)) - S(*times(dot(v, d), dot(v, d))) / S(*dot(d, d))

    hull = [start]
    while True:
        current = hull[-1]
        candidate = next(i for i in indices if i != current)
        for j in indices:
            if j == current:
                continue
            turn = sign(dot(d, cross(vsub(vertices[candidate], vertices[current]),
                                      vsub(vertices[j], vertices[current]))))
            if turn < 0 or (turn == 0 and distance(current, j) > distance(current, candidate)):
                candidate = j
        if candidate == start:
            break
        need(candidate not in hull, "simple projected boundary")
        hull.append(candidate)
    for i, j in zip(hull, hull[1:] + hull[:1]):
        need(all(sign(dot(d, cross(vsub(vertices[j], vertices[i]), vsub(p, vertices[i])))) >= 0
                 for p in vertices), "literal projected support edges")
    for previous, current, following in zip(hull[-1:] + hull[:-1], hull, hull[1:] + hull[:1]):
        need(sign(dot(d, cross(vsub(vertices[current], vertices[previous]),
                              vsub(vertices[following], vertices[current])))) > 0,
             "every projected corner is strict and irredundant")
    return hull


def project(v, d):
    vf, df = as_fields(v, 20), as_fields(d)
    t = fdot(vf, df) / fdot(df, df)
    return tuple(x - t * y for x, y in zip(vf, df))


def polygon_area_squared(vertices, hull, d):
    points = [project(vertices[i], d) for i in hull]
    b = [S(), S(), S()]
    for p, q in zip(points, points[1:] + points[:1]):
        b = [x + y / 2 for x, y in zip(b, fcross(p, q))]
    return fdot(b, b)


def matrix_product(a, b):
    return [[sum((x * y for x, y in zip(row, column)), S()) for column in zip(*b)] for row in a]


def determinant(a):
    return fdot(a[0], fcross(a[1], a[2]))


def minimum_fits(vertices, minima):
    axes = [((1, 0), (0, 0), (0, 0)), ((0, 0), (1, 0), (0, 0))] + [
        ((2, 0), (t, t), (3 * u, u)) for t in (-1, 1) for u in (-1, 1)]
    need(set(map(axis, axes)) == set(minima), "stated minimum axes")
    normals = [as_fields(a) for a in axes[:2]] + [
        tuple(x / S(2, 2) for x in as_fields(a)) for a in axes[2:]]
    need(all(fdot(a, a) == 1 for a in normals), "unit normals")
    hulls = [projected_hull(vertices, a) for a in axes]
    need(all(len(h) == 12 for h in hulls), "all minimum hulls have12 corners")
    points = [[project(vertices[i], a) for i in h] for h, a in zip(hulls, axes)]
    ds = [[[fdot(tuple(x - y for x, y in zip(p, q)), tuple(x - y for x, y in zip(p, q)))
            for q in ps] for p in ps] for ps in points]
    counts, motions = [], []
    for ia, pa in enumerate(points):
        row = []
        for ib, pb in enumerate(points):
            count = 0
            for direction, shift in product((-1, 1), range(12)):
                perm = [(shift + direction * i) % 12 for i in range(12)]
                if not all(ds[ia][i][j] == ds[ib][perm[i]][perm[j]] for i in range(12) for j in range(12)):
                    continue
                ea = [tuple(x - y for x, y in zip(pa[j], pa[0])) for j in (1, 2)] + [normals[ia]]
                eb = [tuple(x - y for x, y in zip(pb[perm[j]], pb[perm[0]])) for j in (1, 2)] + [
                    tuple(direction * x for x in normals[ib])]
                inverse_rows = [fcross(ea[1], ea[2]), fcross(ea[2], ea[0]), fcross(ea[0], ea[1])]
                det = fdot(ea[0], inverse_rows[0])
                need(det != 0, "independent frame")
                inverse_rows = [[x / det for x in r] for r in inverse_rows]
                q = matrix_product(list(map(list, zip(*eb))), inverse_rows)
                need(matrix_product(q, list(map(list, zip(*q)))) == [[S(int(i == j)) for j in range(3)] for i in range(3)], "proper matrix orthogonality")
                need(determinant(q) == 1, "proper spatial lift")
                t = [x - fdot(r, pa[0]) for x, r in zip(pb[perm[0]], q)]
                need(t == [S()] * 3, "zero physical translation")
                for i in range(12):
                    need([fdot(r, pa[i]) for r in q] == list(pb[perm[i]]), "full corner correspondence")
                motions.append((ia, ib, tuple(x for r in q for x in r)))
                count += 1
            row.append(count)
        counts.append(row)
    need(len(motions) == 22, "complete22 proper configurations")
    return axes, hulls, counts, motions


def cone_gates(vertices, rid):
    common = set(vertices) & rid
    changed = (set(vertices) | rid) - common
    d = ((0, 0), (1, 0), (0, 0))
    hull = [vertices[i] for i in projected_hull(vertices, d)]
    need(len(common) == 50 and len(changed) == 20 and set(hull) <= common, "common model geometry")
    rho = S(-1, 1, 8)
    count = zeros = 0
    for p, q in zip(hull, hull[1:] + hull[:1]):
        for v in set(hull) | changed:
            if v in (p, q):
                continue
            t = cross(vsub(q, p), vsub(v, p))
            tx, ty, tz = map(lambda x: S(*x), t)
            slack = ty - rho * ((tx if tx >= 0 else -tx) + (tz if tz >= 0 else -tz))
            need(ty > 0 and slack >= 0, "closed cone gate")
            if v in hull:
                need(slack > 0, "strict polygon gate")
            zeros += int(slack == 0)
            count += 1
    need(count == 360 and zeros == 2, "all360 gates and two boundary equalities")
    return {"common_vertices": 50, "changed_vertices": 20, "gates": count, "zero_slacks": zeros}


def source_comparison(directory, vertices, found, values, motions):
    # Restricted AST evaluator: arithmetic declarations only, no execution.
    env = {}

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            f = Fraction(str(node.value))
            return S(f.numerator, 0, f.denominator)
        if isinstance(node, ast.Name):
            return env[node.id]
        if isinstance(node, ast.Tuple):
            return tuple(evaluate(x) for x in node.elts)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -evaluate(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add): return a + b
            if isinstance(node.op, ast.Sub): return a - b
            if isinstance(node.op, ast.Mult): return a * b
            if isinstance(node.op, ast.Div): return a / b
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Q":
            args = [evaluate(x) for x in node.args]
            need(len(args) <= 2 and not node.keywords, "literal Q call")
            return sum((x * y for x, y in zip(args, [S(1), S(0, 1)])), S())
        raise ValueError("unsupported model expression")

    original_faces = None
    for node in ast.parse((directory / "model.py").read_text()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == "FACES": original_faces = ast.literal_eval(node.value)
            elif name in ("s", "VERTICES") or name.startswith("C"):
                env[name] = evaluate(node.value)
    author_vertices = env["VERTICES"]
    mapping = []
    for v in author_vertices:
        w = [20 * x for x in v]
        need(all(x.d == 1 for x in w), "source coordinate normalization")
        mapping.append(vertices.index(tuple((x.a, x.b) for x in w)))
    need(len(mapping) == len(set(mapping)) == 60, "all author vertex entries")
    need({tuple(sorted(mapping[i] for i in f)) for f in original_faces} == found, "all author facet sets")
    vectors = []
    for face in original_faces:
        raw = ((0, 0),) * 3
        cycle = [mapping[i] for i in face]
        for i, j in zip(cycle, cycle[1:] + cycle[:1]):
            raw = tuple(plus(a, b) for a, b in zip(raw, cross(vertices[i], vertices[j])))
        if sign(dot(raw, vertices[cycle[0]])) < 0:
            raw = vscale(-1, raw)
        vectors.append(raw)
    seen, stream = set(), []
    for i, j in combinations(range(62), 2):
        d = axis(cross(vectors[i], vectors[j]))
        if d is None or d in seen:
            continue
        seen.add(d)
        pivot = next(a for a, b in d if (a, b) != (0, 0))
        normalized = as_fields(d, pivot)
        stream.append(repr(normalized) + ":" + repr(values[d]) + "\n")
    expected = json.loads((directory / "expected.json").read_text())
    digest = hashlib.sha256("".join(stream).encode()).hexdigest()
    need(digest == expected["candidate_spectrum_sha256"], "all613 source spectrum values/order")

    def parse_field(text):
        a, b = text.removesuffix("sqrt5").split(")+(" )
        fa, fb = Fraction(a[1:]), Fraction(b[:-1])
        return S(fa.numerator * fb.denominator, fb.numerator * fa.denominator, fa.denominator * fb.denominator)

    target_motions = set()
    for m in expected["minimum_receiver_proper_motions"]:
        columns = [[parse_field(t) for t in c] for c in m["proper_matrix_columns"]]
        target_motions.add((m["source_axis"], m["receiver_axis"], tuple(x for row in zip(*columns) for x in row)))
    need(set(motions) == target_motions and len(target_motions) == 22, "all22 author motion matrices")
    return {"vertex_entries": 60, "facet_sets": 62, "spectrum_entries": len(seen),
            "source_spectrum_sha256": digest, "proper_motion_matrices": 22}


def build(author_source=None):
    need(S(0, 1) * S(0, 1) == 5 and S(9, -4) > 0, "field controls")
    unit = [((800, 0), (0, 0), (0, 0)), ((0, 0), (800, 0), (0, 0)),
            ((0, 0), (0, 0), (800, 0))]
    cube = unit + [vscale(-1, b) for b in unit]
    split = [tuple((a // 2, b // 2) for a, b in v) for v in cube for _ in range(2)]
    for control in (cube, split):
        _, lo, _, hi, _, counts = zonotope(control)
        need(lo == 1 and hi == 3 and (counts["vertices"], counts["edges"], counts["facets"]) == (8, 12, 6),
             "cube and parallel-split chamber controls")
    vertices, rid = construct()
    found, cycles, vectors, model = facets(vertices)
    values, minimum, minima, maximum, maxima, inventory = zonotope(vectors)
    need(minimum == S(207, 91, 2) and maximum == S(113, 50), "claimed global extrema")
    need(inventory == {"projective_facets": 613, "parallel_pairs": 14, "vertices": 1568, "edges": 2792, "facets": 1226}, "complete zonotope inventory")
    axes, hulls, counts, motions = minimum_fits(vertices, minima)
    for d, h in zip(axes, hulls):
        need(polygon_area_squared(vertices, h, d) == minimum, "all six literal minimum polygon areas")
    max_hulls = [projected_hull(vertices, d) for d in maxima]
    need(set(maxima) == {axis(((22, 0), (0, 0), (13, 5))),
                         axis(((22, 0), (0, 0), (-13, -5)))}, "both stated maximum axes")
    need([len(h) for h in max_hulls] == [18, 18], "maximum18-corner shadows")
    for d, h in zip(maxima, max_hulls):
        need(polygon_area_squared(vertices, h, d) == maximum, "both literal maximum polygon areas")
    fourth = maximum / minimum
    need(fourth == S(641, 67, 722), "exact fourth-power scale bound")
    need(S(1023021211654, 0, 10**12)**4 < fourth, "lower decimal scale endpoint")
    need(fourth < S(1023021211655, 0, 10**12)**4, "upper decimal scale endpoint")
    record = {"status": "PASS", "actual_author": "six-reviewer-4", "role": "independent reviewer",
              "independent_zonotope_controls": 2,
              "model": model, "zonotope": inventory,
              "minimum_area_squared": repr(minimum), "maximum_area_squared": repr(maximum),
              "minimum_axes": [[repr(x) for x in as_fields(d, next(a for a, b in d if (a, b) != (0, 0)))] for d in minima],
              "maximum_axes": [[repr(x) for x in as_fields(d, next(a for a, b in d if (a, b) != (0, 0)))] for d in maxima],
              "minimum_corner_counts": list(map(len, hulls)), "maximum_corner_counts": list(map(len, max_hulls)),
              "minimum_fit_counts": counts, "proper_fit_configurations": len(motions),
              "cone": cone_gates(vertices, rid), "scale_bound_fourth_power": repr(fourth),
              "scope": "complete exact J74 finite geometry; universal coverage and strict supremum refinement are written proofs"}
    if author_source is not None:
        record["author_comparison"] = source_comparison(author_source, vertices, found, values, motions)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-source", type=Path)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("expected.json"))
    args = parser.parse_args()
    record = build(args.author_source)
    data = json.dumps(record, sort_keys=True, indent=2) + "\n"
    if args.emit:
        print(data, end="")
        return
    expected = json.loads(args.expected.read_text())
    comparison = record.pop("author_comparison", None)
    need(record == expected, "complete expected result mismatch")
    print(json.dumps({"status": "PASS", "facets": 62, "zonotope_vertices": 1568,
                      "proper_minimum_fits": 22, "maximum_corners": [18, 18],
                      "author_comparison": comparison}, sort_keys=True))


if __name__ == "__main__":
    main()
