"""Definition-level geometry and exact finite-cover audit; no third-party code."""
import hashlib
import json
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations, product
from math import gcd
from pathlib import Path

import construct


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def primitive(a):
    g = gcd(*a)
    require(g > 0, "zero direction")
    return tuple(x // g for x in a)


def angle_compare(a, b):
    def half(x):
        return int(x[1] < 0 or (x[1] == 0 and x[0] < 0))
    if half(a) != half(b):
        return half(a) - half(b)
    c = cross(a, b)
    return -((c > 0) - (c < 0))


def polygon_classes(vertices):
    n = len(vertices)
    normals, bounds = [], []
    for i, p in enumerate(vertices):
        q = vertices[(i + 1) % n]
        a = (q[1] - p[1], p[0] - q[0])
        b = dot(a, p)
        require(all(dot(a, x) <= b for x in vertices), "polygon not convex CCW")
        require(sum(dot(a, x) == b for x in vertices) == 2, "degenerate edge")
        normals.append(a)
        bounds.append(b)
    active = [[a for a, b in zip(normals, bounds) if dot(a, p) == b]
              for p in vertices]
    rays = sorted({primitive((s * a[1], -s * a[0]))
                   for a in normals for s in (-1, 1)}, key=cmp_to_key(angle_compare))
    sectors = [tuple(x + y for x, y in zip(a, rays[(i + 1) % len(rays)]))
               for i, a in enumerate(rays)]
    for i, d in enumerate(sectors):
        require(cross(rays[i], d) > 0 and cross(d, rays[(i + 1) % len(rays)]) > 0,
                "invalid sector representative")
    def covered(d):
        return tuple(i for i, aa in enumerate(active) if all(dot(a, d) < 0 for a in aa))
    incidence = [(d, covered(d)) for d in rays + sectors]
    sets = {frozenset(s) for _, s in incidence}
    maximal = {s for s in sets if s and not any(s < t for t in sets)}
    return normals, bounds, active, rays, incidence, maximal


def min_cover(n, masks):
    """Dynamic program over covered ground subsets, independent of the producer."""
    full = (1 << n) - 1
    d = [n + 1] * (1 << n)
    d[0] = 0
    for state in range(1 << n):
        for edge in masks:
            new = state | edge
            if d[new] > d[state] + 1:
                d[new] = d[state] + 1
    require(d[full] <= n, "uncoverable family")
    return d[full]


def solve_square(rows, rhs):
    n = len(rhs)
    a = [[F(x) for x in row] + [F(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return None
        a[pivot], a[col] = a[col], a[pivot]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for i in range(n):
            if i != col:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[col])]
    return tuple(row[-1] for row in a)


def fractional_certificate(n, masks):
    """Enumerate dual vertices, then obtain a matching small primal certificate.

    Only tiny fixed audit families use this routine. The public theorem does
    not rely on enumeration as a replacement for finite LP duality.
    """
    constraints = [(tuple(int(m >> i & 1) for i in range(n)), F(1)) for m in masks]
    constraints += [(tuple(-int(i == j) for i in range(n)), F(0)) for j in range(n)]
    best, dual = F(-1), None
    for active in combinations(constraints, n):
        z = solve_square([a for a, _ in active], [b for _, b in active])
        if z is not None and all(dot(a, z) <= b for a, b in constraints):
            if sum(z) > best:
                best, dual = sum(z), z
    require(dual is not None, "no dual vertex")
    for k in range(1, min(n, len(masks)) + 1):
        for columns in combinations(range(len(masks)), k):
            for equal_rows in combinations(range(n), k):
                w = solve_square([[int(masks[j] >> i & 1) for j in columns]
                                  for i in equal_rows], [1] * k)
                if w is None or any(x < 0 for x in w) or sum(w) != best:
                    continue
                primal = tuple(w[columns.index(j)] if j in columns else F(0)
                               for j in range(len(masks)))
                if all(sum(wj for m, wj in zip(masks, primal) if m >> i & 1) >= 1
                       for i in range(n)):
                    check_certificate(n, masks, primal, dual)
                    return best, primal, dual
    raise ValueError("failed to obtain matching primal certificate")


def check_certificate(n, masks, primal, dual):
    require(len(primal) == len(masks) and len(dual) == n, "certificate lengths")
    require(all(x >= 0 for x in primal + dual), "negative certificate entry")
    for i in range(n):
        require(sum(w for e, w in zip(masks, primal) if e >> i & 1) >= 1,
                "primal uncovered element")
    for e in masks:
        require(sum(z for i, z in enumerate(dual) if e >> i & 1) <= 1,
                "dual overloaded edge")
    require(sum(primal) == sum(dual), "primal/dual objective mismatch")


def independent_product(n, e, m, f):
    return tuple(sum(1 << (i * m + j) for i, j in product(range(n), range(m))
                     if a >> i & 1 and b >> j & 1) for a, b in product(e, f))


def audit_greedy(n, masks, weights, certificate):
    unseen = set(range(n))
    require(certificate["remaining"][0] == n, "wrong initial trace")
    mass = sum(weights)
    for j, index in enumerate(certificate["indices"]):
        require(0 <= index < len(masks) and weights[index] > 0, "invalid chosen class")
        covered = {i for i in unseen if masks[index] >> i & 1}
        gain = len(covered)
        require(gain > 0 and gain * mass >= len(unseen), "greedy decay failure")
        require(gain == max(sum(e >> i & 1 for i in unseen)
                            for e, w in zip(masks, weights) if w > 0), "not a maximum gain")
        unseen -= covered
        require(certificate["remaining"][j + 1] == len(unseen), "wrong trace")
    require(not unseen, "cover incomplete")


def main():
    evidence = []
    p = ((0, 0), (4, 0), (5, 3), (2, 5), (-1, 3))
    normals, bounds, active, rays, incidence, maximal = polygon_classes(p)
    wanted = {frozenset((i, (i + 1) % 5)) for i in range(5)}
    require(maximal == wanted, "pentagon incidence differs from C5")
    step_checks = 0
    for d, cov in incidence:
        for i, v in enumerate(p):
            if i in cov:
                positive = [F(b - dot(a, v), 2 * dot(a, d))
                            for a, b in zip(normals, bounds) if dot(a, d) > 0]
                t = min([F(1, 2)] + positive)
                require(t > 0, "invalid interior step")
                x = tuple(F(a) + t * b for a, b in zip(v, d))
                require(all(dot(a, x) < b for a, b in zip(normals, bounds)),
                        "declared direction does not enter interior")
            else:
                require(any(dot(a, d) >= 0 for a in active[i]), "missing obstruction")
            step_checks += 1
            evidence.append(["geometry", list(d), i, i in cov])
    directions = ((0, 6), (-4, 2), (-4, -5), (4, -5), (4, 2))
    base = tuple((1 << i) | (1 << ((i + 1) % 5)) for i in range(5))
    for e, d in zip(base, directions):
        got = sum(1 << i for i in range(5) if all(dot(a, d) < 0 for a in active[i]))
        require(got == e, "wrong direction representative")
    require(min_cover(5, base) == 3, "pentagon ordinary value")
    check_certificate(5, base, (F(1, 2),) * 5, (F(1, 2),) * 5)
    indices = ((0, 0), (0, 1), (1, 0), (1, 3), (2, 2), (3, 1), (3, 4), (4, 3))
    product_dirs = [directions[i] + directions[j] for i, j in indices]
    coverage = []
    for i, j in product(range(5), repeat=2):
        cov = [h for h, d in enumerate(product_dirs)
               if all(dot(a, d[:2]) < 0 for a in active[i])
               and all(dot(a, d[2:]) < 0 for a in active[j])]
        require(cov, "product vertex not covered")
        coverage.append([i, j, cov])
    # Fiber lower certificate: five fibers each require >=3 directions;
    # each direction is counted in at most two fibers; hence 2M>=15.
    require((5 * 3 + 1) // 2 == 8, "fiber lower bound")
    square = independent_product(5, base, 5, base)
    check_certificate(25, square, (F(1, 4),) * 25, (F(1, 4),) * 25)
    greedy_cases = []
    for r in (1, 2, 3):
        n, masks, weights = construct.tensor(5, base, [F(1, 2)] * 5, r)
        expected_masks = tuple(sum(1 << sum(x * 5 ** (r - j - 1) for j, x in enumerate(v))
                                  for v in product(range(5), repeat=r)
                                  if all(base[c] >> x & 1 for c, x in zip(cs, v)))
                               for cs in product(range(5), repeat=r))
        require(masks == expected_masks, "product masks not definition-level equal")
        trace = construct.greedy(n, masks, weights)
        audit_greedy(n, masks, weights, trace)
        require(len(trace["indices"]) <= construct.power_bound(5, F(5, 2), r),
                "rational power bound failed")
        greedy_cases.append({"r": r, "vertices": n, "classes": len(masks),
                             "selected": len(trace["indices"]),
                             "trace": trace})
    # Every set family on a three-element ground set, with all nonempty
    # subsets eligible. Reducing to maximal members preserves all cover values.
    families = []
    canonical = {}
    for code in range(1, 1 << 7):
        masks = tuple(e for e in range(1, 8) if code >> (e - 1) & 1)
        union = 0
        for e in masks:
            union |= e
        if union != 7:
            continue
        tau, w, z = fractional_certificate(3, masks)
        ordinary = min_cover(3, masks)
        reduced = tuple(e for e in masks if not any(e != f and e & f == e for f in masks))
        old = canonical.setdefault(reduced, fractional_certificate(3, reduced))
        require(old[0] == tau and min_cover(3, reduced) == ordinary, "maximal reduction")
        families.append((masks, tau, ordinary))
        evidence.append(["family", code, str(tau), ordinary])
    pair_checks = 0
    equal_factor_checks = 0
    for e, (tau, w, z) in canonical.items():
        for f, (sigma, ww, zz) in canonical.items():
            edges = independent_product(3, e, 3, f)
            check_certificate(9, edges, tuple(a * b for a, b in product(w, ww)),
                              tuple(a * b for a, b in product(z, zz)))
            ie, iff, ip = min_cover(3, e), min_cover(3, f), min_cover(9, edges)
            require(ip >= tau * iff and ip >= sigma * ie and ip <= ie * iff,
                    "mixed product bound")
            if tau == ie or sigma == iff:
                require(ip == ie * iff, "gap-free multiplier failed")
                equal_factor_checks += 1
            trace = construct.greedy(9, edges, tuple(a * b for a, b in product(w, ww)))
            audit_greedy(9, edges, tuple(a * b for a, b in product(w, ww)), trace)
            pair_checks += 1
            evidence.append(["pair", e, f, str(tau * sigma), ip, len(trace["indices"])])
    rejection_checks = 0
    def reject(fn):
        nonlocal rejection_checks
        try:
            fn()
        except ValueError:
            rejection_checks += 1
        else:
            raise ValueError("malformed input/certificate was accepted")
    reject(lambda: construct.check_family(2, [1]))
    reject(lambda: construct.check_family(2, [0, 3]))
    reject(lambda: construct.check_family(2, [1, 1, 2]))
    reject(lambda: construct.check_weights(2, [1, 2], [1, 0]))
    reject(lambda: construct.check_weights(2, [3], [-1]))
    reject(lambda: construct.tensor(5, base, [F(1, 2)] * 5, 0))
    reject(lambda: construct.strict_exponent(5, 3, 3))
    reject(lambda: construct.power_bound(1, 2, 1))
    reject(lambda: check_certificate(5, base, (F(1, 2),) * 5, (F(1),) * 5))
    bad_trace = {"indices": [0], "remaining": [5, 3]}
    reject(lambda: audit_greedy(5, base, (F(1, 2),) * 5, bad_trace))
    # Each of the eight displayed product directions is essential to this
    # particular certificate; deletion holes do not alone prove optimality.
    deletion_holes = []
    for removed in range(8):
        holes = [[i, j] for i, j, cov in coverage if cov == [removed]]
        require(holes, "unexpected redundant direction")
        deletion_holes.append({"removed": removed, "hole": holes[0]})
    sufficient = construct.strict_exponent(5, F(5, 2), 3)
    evidence += [["coverage", coverage], ["greedy", greedy_cases], ["deletions", deletion_holes]]
    digest = hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {"status": "pass", "pentagon": {"vertices": p, "normals": normals,
               "direction_strata": len(incidence), "vertex_direction_checks": step_checks,
               "ordinary": 3, "fractional": "5/2", "square_ordinary": 8,
               "square_fractional": "25/4", "product_direction_indices": indices,
               "product_vertex_checks": 25, "deletion_holes": deletion_holes},
              "small_families": len(families), "maximal_families": len(canonical),
              "ordered_product_checks": pair_checks, "gap_free_factor_checks": equal_factor_checks,
              "greedy_pentagon_powers": [{k: v for k, v in c.items() if k != "trace"}
                                         for c in greedy_cases],
              "sufficient_exponent_bound_not_minimal": sufficient,
              "rejection_controls": rejection_checks, "entrywise_sha256": digest}
    expected = Path(__file__).with_name("expected.json")
    require(expected.is_file(), "missing frozen expected output")
    require(json.loads(expected.read_text()) == json.loads(json.dumps(result)), "frozen output differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
