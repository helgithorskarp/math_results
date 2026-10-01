#!/usr/bin/env python3
"""Independent exact auxiliary audit. The continuous geometry is proved in REVIEW.md."""

from fractions import Fraction as F
from itertools import combinations
import json
from quadratic import Q, equal, psd_rank, require


def add(a, b):
    result = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        result[i] += x
    for i, x in enumerate(b):
        result[i] += x
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def scale(a, s):
    return [x * s for x in a]


def mul(a, b):
    result = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def arithmetic():
    chebyshev = [[F(1)], [F(0), F(1)]]
    for _ in range(2):
        chebyshev.append(add(mul([0, 2], chebyshev[-1]), scale(chebyshev[-2], -1)))
    rows = {}
    for m in range(3, 7):
        row = [F(1)]
        for distance in range(1, m // 2 + 1):
            multiplicity = 1 if 2 * distance == m else 2
            row = add(row, scale(chebyshev[distance], multiplicity))
        rows[str(m)] = [str(x) for x in row]
    require(rows == {"3": ["1", "2"], "4": ["0", "2", "2"],
                     "5": ["-1", "2", "4"], "6": ["-1", "-1", "4", "4"]},
            "independent graph-distance hemisphere rows")
    require(add([1], scale([0, 1], 2)) == [1, 2], "triangle factor")
    require(mul([0, 2], [1, 1]) == [0, 2, 2], "quadrilateral factor")
    require(mul([1, 1], [-1, 0, 4]) == [-1, -1, 4, 4], "hexagon factor")
    a = Q(F(-1, 4), F(1, 4))
    require(equal(4 * a * a + 2 * a - 1, Q()), "pentagon root identity")
    upper = F(3091, 10000)
    require((upper - a).sign() > 0 and (a - F(1, 4)).sign() > 0, "cosine brackets")
    require((4 * upper + 1) ** 2 - 5 == F(9281, 6250000), "rational sqrt upper witness")
    bands = []
    for lo, hi, error, margin in [(F(1, 2), F(3, 5), F(1, 60), F(1, 500)),
                                   (F(14, 25), F(3, 5), F(1, 32), F(1, 400))]:
        values = [c - error - upper - (1 - upper) * (c + margin) ** 2 for c in (lo, hi)]
        require(min(values) > 0 and lo - error > upper and hi + margin < 1,
                "uniform band positivity/domain")
        require(-(1 - upper) < 0, "uniform band concavity")
        bands.append({"interval": [str(lo), str(hi)], "error": str(error),
                      "margin": str(margin), "endpoint_bounds": list(map(str, values))})
    require(bands[0]["endpoint_bounds"] == ["928273/7500000000", "178863073/7500000000"],
            "first band endpoints")
    require(bands[1]["endpoint_bounds"] == ["107/102400", "14158371/1600000000"],
            "second band endpoints")
    e0 = Q(F(7, 16), F(-3, 16))
    require(equal(e0, F(1, 2) - a - (1 - a) / 4), "sharp uniform threshold")
    require((1 - 2 * (1 - a) * F(3, 5)).sign() > 0, "threshold increasing")
    require(equal(a / (1 - a), Q(0, F(1, 5))), "critical packing parameter")
    return {"hemisphere_rows": rows, "bands": bands, "sharp_uniform_tolerance": e0.record(),
            "packing_critical_c": (a / (1 - a)).record()}


def role_paths():
    """Enumerate disjoint active/nonpositive subsets; find runs as graph components."""
    result = {}
    for m in (4, 5, 6):
        vertices = set(range(m))
        exceptional = 0
        words = 0
        lengths = {}
        closed_budgets = set()
        for size in range(3, m + 1):
            for active_tuple in combinations(range(m), size):
                active = set(active_tuple)
                remaining = sorted(vertices - active)
                for nsize in range(len(remaining) + 1):
                    for ntuple in combinations(remaining, nsize):
                        words += 1
                        nonpositive = set(ntuple)
                        if not any((i + 1) % m in nonpositive for i in nonpositive):
                            continue
                        pending = set(nonpositive)
                        components = []
                        while pending:
                            component = {pending.pop()}
                            queue = list(component)
                            while queue:
                                i = queue.pop()
                                for j in ((i - 1) % m, (i + 1) % m):
                                    if j in pending:
                                        pending.remove(j)
                                        component.add(j)
                                        queue.append(j)
                            components.append(component)
                        exceptional_runs = [c for c in components if len(c) >= 2]
                        require(len(exceptional_runs) == 1, "unique exceptional run")
                        removed = exceptional_runs[0]
                        rest = vertices - removed
                        edges = [(i, (i + 1) % m) for i in range(m)
                                 if i in rest and (i + 1) % m in rest]
                        require(active <= rest and len(edges) == len(rest) - 1, "active path coverage")
                        require(all(not ({i, j} <= nonpositive) for i, j in edges), "ordinary path edges")
                        # The cycle minus one nonempty proper connected run is a path.
                        budget = F(2 * len(edges), m)
                        require(budget <= 1, "closed-semicircle budget for equality")
                        if m == 5:
                            require(budget < 1, "pentagon strict path budget")
                        closed_budgets.add(str(budget))
                        exceptional += 1
                        key = str(len(removed))
                        lengths[key] = lengths.get(key, 0) + 1
        result[str(m)] = {"role_words": words, "exceptional_words": exceptional,
                          "run_lengths": lengths, "equality_path_pi_units": sorted(closed_budgets)}
    require([result[str(m)]["exceptional_words"] for m in (4, 5, 6)] == [0, 5, 48],
            "exceptional complete census")
    require(result["6"]["run_lengths"] == {"2": 42, "3": 6}, "hexagon run census")
    return result


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def difference(a, b):
    return tuple(x - y for x, y in zip(a, b))


def orientation(a, b, q):
    return cross(difference(b, a), difference(q, a))


def intersects(a, b, c, d):
    u, v, delta = difference(b, a), difference(d, c), difference(c, a)
    denominator = cross(u, v)
    if not denominator.zero():
        t, s = cross(delta, v) / denominator, cross(delta, u) / denominator
        return t.sign() >= 0 and (1 - t).sign() >= 0 and s.sign() >= 0 and (1 - s).sign() >= 0
    if not cross(delta, u).zero():
        return False
    axis = 0 if not u[0].zero() else 1
    def ordered(x, y):
        return (x, y) if (y - x).sign() >= 0 else (y, x)
    lo1, hi1 = ordered(a[axis], b[axis])
    lo2, hi2 = ordered(c[axis], d[axis])
    return (hi1 - lo2).sign() >= 0 and (hi2 - lo1).sign() >= 0


def winding(vertices, q):
    """Intersect a rightward horizontal ray explicitly; divide to locate each hit."""
    total = 0
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        ay, by = (a[1] - q[1]).sign(), (b[1] - q[1]).sign()
        up, down = ay <= 0 < by, by <= 0 < ay
        if not (up or down):
            continue
        hit = a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
        require(not equal(hit, q[0]), "query on an edge")
        if (hit - q[0]).sign() > 0:
            total += 1 if up else -1
    return total


def concave_fixture():
    D, c = 3835, F(7, 12)
    root = Q(0, 1, D)
    u, v = F(7, 18) - root / 117, F(7, 18) + root / 45
    points = [(0, 0, 1), (u, -v, c), (1, -1, F(1, 2)),
              (1, 1, F(1, 2)), (u, v, c)]
    points = [tuple(Q(0, 0, D).coerce(x) for x in p) for p in points]
    metric = [F(13, 24), F(5, 24), F(1)]
    def dot(p, r):
        return sum((h * x * y for h, x, y in zip(metric, p, r)), Q(0, 0, D))
    require(all(equal(dot(p, p), Q(1, 0, D)) for p in points), "fixture unit vectors")
    contacts = []
    labels = "VAPQB"
    for i, j in combinations(range(5), 2):
        value = dot(points[i], points[j])
        require((c - value).sign() >= 0 and (1 - value).sign() > 0, "fixture packing")
        if equal(value, Q(c, 0, D)):
            contacts.append("".join(sorted(labels[i] + labels[j])))
    planar = [tuple(x / p[2] for x in p[:2]) for p in points]
    for i, j in combinations(range(5), 2):
        if (i - j) % 5 not in (1, 4):
            require(not intersects(planar[i], planar[(i + 1) % 5],
                                   planar[j], planar[(j + 1) % 5]), "fixture self intersection")
    query = tuple(points[0][i] + 8 * points[1][i] + points[2][i] for i in range(3))
    q = tuple(x / query[2] for x in query[:2])
    turns = [orientation(planar[i], planar[(i + 1) % 5], q) for i in range(5)]
    require([x.sign() for x in turns] == [1, 1, 1, 1, -1], "signed angular increments")
    require(orientation(planar[-1], planar[0], planar[1]).sign() < 0, "concavity")
    require(winding(planar, q) == 1, "positive winding")
    for offset in range(5):
        require(winding(planar[offset:] + planar[:offset], q) == 1, "rotated cycle winding")
    require(winding(list(reversed(planar)), q) == -1, "reversed winding")
    require(winding(planar, (Q(100, 0, D), Q(100, 0, D))) == 0, "exterior winding")
    return {"c": str(c), "contacts": sorted(contacts), "increment_signs": [x.sign() for x in turns],
            "projected_determinants": [x.record() for x in turns], "winding": 1,
            "rotations_checked": 5, "reverse_winding": -1, "exterior_winding": 0}


def regular_gram(m, height, include_axis=False):
    height = Q().coerce(height)
    square = height ** 2
    require(height.sign() > 0 and (1 - height).sign() > 0, "regular height domain")
    cosines = {3: [Q(1), Q(F(-1, 2)), Q(F(-1, 2))],
               4: [Q(1), Q(), Q(-1), Q()],
               5: [Q(1), Q(F(-1, 4), F(1, 4)), Q(F(-1, 4), F(-1, 4)),
                   Q(F(-1, 4), F(-1, 4)), Q(F(-1, 4), F(1, 4))],
               6: [Q(1), Q(F(1, 2)), Q(F(-1, 2)), Q(-1), Q(F(-1, 2)), Q(F(1, 2))]}[m]
    require(sum(cosines, Q()).zero(), "regular tangent sum")
    require(equal(sum((x * x for x in cosines), Q()), Q(F(m, 2))), "regular tangent norm")
    gram = [[square + (1 - square) * cosines[(i - j) % m] for j in range(m)]
            for i in range(m)]
    if include_axis:
        gram = [[Q(1)] + [height] * m] + [[height] + row for row in gram]
    return gram


def packing_gram(gram, c):
    require(all(equal(row[i], Q(1)) for i, row in enumerate(gram)), "Gram unit diagonal")
    for i, j in combinations(range(len(gram)), 2):
        require((c - gram[i][j]).sign() >= 0 and (1 - gram[i][j]).sign() > 0,
                "Gram packing pair")
    rank, pivots, zero = psd_rank(gram)
    require(rank == 3, "spherical rank three")
    return {"rank": rank, "positive_pivots": pivots, "zero_block_size": zero,
            "pairs": len(gram) * (len(gram) - 1) // 2}


def sharp_fixtures():
    regular = []
    for m in range(3, 7):
        for height in [F(1, 4), F(1, 2), F(3, 4), F(9, 10)]:
            gram = regular_gram(m, height)
            rank, _, zero = psd_rank(gram)
            require(rank == 3 and zero == m - 3, "regular equality Gram rank")
            regular.append({"m": m, "height": str(height), "rank": rank})
    critical = []
    for c in [Q(0, F(1, 5)), Q(F(1, 2)), Q(F(3, 5)), Q(F(3, 4)), Q(F(9, 10))]:
        gram = regular_gram(5, c, True)
        receipt = packing_gram(gram, c)
        a = Q(F(-1, 4), F(1, 4))
        require(equal(gram[1][2], a + (1 - a) * c * c), "critical pentagon edge")
        critical.append({"c": c.record(), "edge": gram[1][2].record(), **receipt})
    base = regular_gram(5, F(1, 2), True)
    bad_pair = [row[:] for row in base]
    bad_pair[0][1] = bad_pair[1][0] = Q(F(51, 100))
    bad_psd = [row[:] for row in base]
    bad_psd[1][3] -= F(1, 100)
    bad_psd[3][1] -= F(1, 100)
    too_large_rank = [[Q(int(i == j)) for j in range(7)] for i in range(7)]
    rejected = []
    for name, matrix in [("overlarge_pair", bad_pair), ("nonrealizable_gram", bad_psd),
                         ("dimension_four_or_more", too_large_rank)]:
        try:
            packing_gram(matrix, Q(F(1, 2)))
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("actual corrupted matrix accepted: " + name)
    return {"regular_equality_examples": regular, "critical_pentagon_insertions": critical,
            "rejected_matrix_controls": rejected}


def main():
    result = {"agent": "six-reviewer-5", "role": "independent mathematical reviewer",
              "status": "INDEPENDENT_NONCONVEX_CYCLE_AUXILIARY_CHECKS_PASS",
              "arithmetic": arithmetic(), "role_paths": role_paths(),
              "concave_fixture": concave_fixture(), "sharp_fixtures": sharp_fixtures(),
              "trust_boundary": "Continuous minimum, Jordan winding, arc geometry and equality proofs are written in REVIEW.md."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
