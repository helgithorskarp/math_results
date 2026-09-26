#!/usr/bin/env python3
"""Definition-level rational checks; universal proof is in PROOF.md.

No input files, network access, floating-point operations, or assertions.
Gaussian replica integrals are normalized by integral(phi_0**k), so no pi
or irrational Gaussian normalization enters any finite calculation.
"""
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial

from rational_bounds import Interval, compact, exp_bounds, log_bounds, sqrt_bounds


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mean(points, weights):
    return tuple(sum(w * x[j] for x, w in zip(points, weights))
                 for j in range(len(points[0])))


def geometry(points, images, weights, radius2):
    require(len(points) == len(images) == len(weights) and len(points) > 0,
            "incompatible lengths")
    n = len(points[0])
    require(n >= 1 and all(len(x) == n for x in points + images), "bad dimension")
    require(all(w > 0 for w in weights) and sum(weights) == 1, "invalid weights")
    require(radius2 > 0 and all(dot(x, x) <= radius2 for x in points), "bad radius")
    m = len(points)
    delta = [[dot(sub(points[i], points[j]), sub(points[i], points[j]))
              - dot(sub(images[i], images[j]), sub(images[i], images[j]))
              for j in range(m)] for i in range(m)]
    require(all(d >= 0 for row in delta for d in row), "map is not contractive")
    rowmeans = [sum(weights[j] * delta[i][j] for j in range(m)) for i in range(m)]
    loss = dot(weights, rowmeans)
    mx, my = mean(points, weights), mean(images, weights)
    cx, cy = [sub(x, mx) for x in points], [sub(y, my) for y in images]
    vx = sum(w * dot(x, x) for x, w in zip(cx, weights))
    vy = sum(w * dot(y, y) for y, w in zip(cy, weights))
    cross = [[sum(w * x[i] * y[j] for x, y, w in zip(cx, cy, weights))
              for j in range(n)] for i in range(n)]
    hs2 = F(0)
    for i, j in itertools.product(range(m), repeat=2):
        h = dot(cx[i], cx[j]) - dot(cy[i], cy[j])
        require(2 * h == -delta[i][j] + rowmeans[i] + rowmeans[j] - loss,
                "double-centering identity")
        hs2 += weights[i] * weights[j] * h * h
    require(loss == 2 * (vx - vy), "variance-drop identity")
    require(hs2 <= radius2 * loss, "Gram HS estimate")
    return {"D": loss, "vx": vx, "vy": vy, "cross": cross, "hs2": hs2}


def procrustes_error(g):
    c = g["cross"]
    if all(v == 0 for row in c for v in row):
        fidelity = Interval.of(0)
    elif len(c) == 1:
        fidelity = Interval.of(abs(c[0][0]))
    elif len(c) == 2:
        # (sigma_1+sigma_2)^2 = sum C_ij^2 + 2|det C|.
        det = c[0][0] * c[1][1] - c[0][1] * c[1][0]
        fidelity = sqrt_bounds(sum(x*x for row in c for x in row) + 2 * abs(det))
    else:
        raise ValueError("checker only handles general cross-covariance through dimension two")
    answer = Interval.of(g["vx"] + g["vy"]) - 2 * fidelity
    return Interval(max(F(0), answer.lo), max(F(0), answer.hi))


def sparse(n, epsilon, a=F(1)):
    require(isinstance(n, int) and n >= 1 and 0 < epsilon < 1 and a > 0,
            "invalid sparse parameters")
    points = [(F(0),) * n]
    for j in range(n):
        for sign in (-1, 1):
            x = [F(0)] * n
            x[j] = sign * a
            points.append(tuple(x))
    images = [tuple(abs(t) for t in x) for x in points]
    weights = [1 - epsilon] + [epsilon / (2 * n)] * (2 * n)
    return points, images, weights


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


def replica_exponent(points, counts, k, s=F(1)):
    vector_sum = tuple(sum(c * x[j] for x, c in zip(points, counts))
                       for j in range(len(points[0])))
    scatter = sum(c * dot(x, x) for x, c in zip(points, counts)) - dot(vector_sum, vector_sum) / k
    require(scatter >= 0, "negative Gaussian scatter")
    return -scatter / (2 * s)


def multinomial(counts):
    result = factorial(sum(counts))
    for c in counts:
        result //= factorial(c)
    return result


def replica(points, weights, k):
    """Finite sum coeff*exp(exponent), computed directly from center tuples."""
    require(isinstance(k, int) and k >= 2, "integer Renyi order required")
    terms = defaultdict(F)
    for counts in compositions(k, len(points)):
        coefficient = F(multinomial(counts))
        for w, count in zip(weights, counts):
            coefficient *= w ** count
        terms[replica_exponent(points, counts, k)] += coefficient
    return {x: c for x, c in terms.items() if c}


def evaluate(terms):
    result = Interval.of(0)
    for exponent, coefficient in sorted(terms.items()):
        result += coefficient * exp_bounds(exponent)
    return result


def replica_taylor(points, n, k):
    """Formal coefficients through epsilon^2, independent of the claimed formula."""
    result = [defaultdict(F) for _ in range(3)]
    for counts in compositions(k, len(points)):
        rare = k - counts[0]
        if rare > 2:
            continue
        exponent = replica_exponent(points, counts, k)
        coefficient = F(multinomial(counts), (2 * n) ** rare)
        for j in range(3 - rare):
            if j <= counts[0]:
                result[rare + j][exponent] += coefficient * (-1)**j * comb(counts[0], j)
    return [{x: c for x, c in terms.items() if c} for terms in result]


def difference(a, b):
    answer = defaultdict(F, a)
    for x, c in b.items():
        answer[x] -= c
    return {x: c for x, c in answer.items() if c}


def rotate(v):
    return (F(3, 5)*v[0]-F(4, 5)*v[1], F(4, 5)*v[0]+F(3, 5)*v[1])


def finite_geometries():
    x = [(F(-1),), (F(-1, 3),), (F(1, 2),), (F(1),)]
    weights = [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]
    grid = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    count = 0
    for values in itertools.product(grid, repeat=4):
        y = [(v,) for v in values]
        if any(abs(values[i]-values[j]) > abs(x[i][0]-x[j][0])
               for i, j in itertools.product(range(4), repeat=2)):
            continue
        g = geometry(x, y, weights, F(1))
        err = procrustes_error(g)
        require(err.lo == err.hi, "one dimensional error must be exact")
        require(err.hi ** 2 <= 2 * g["D"], "one dimensional geometric bound")
        count += 1
    x2 = [(F(0), F(0)), (F(1), F(0)), (F(-1), F(0)),
          (F(0), F(1)), (F(0), F(-1)), (F(3, 5), F(4, 5)),
          (F(-4, 5), F(3, 5))]
    w2 = [F(j, 28) for j in range(1, 8)]
    fixtures = []
    for scale in [F(0), F(1, 2), F(1)]:
        for fold in [False, True]:
            y = [rotate((abs(v[0]) if fold else v[0], scale * v[1])) for v in x2]
            g = geometry(x2, y, w2, F(1))
            if g["D"] == 0:
                require(g["hs2"] == 0, "isometry Gram check")
            else:
                err = procrustes_error(g)
                require(err.hi ** 2 <= 4 * g["D"], "two dimensional geometric bound")
            fixtures.append((x2, y, w2))
    return count, fixtures


def matrix_checks():
    cases = 0
    # Square roots P^(1/2), Q^(1/2) are built from U +/- S, with S diagonal.
    for a, off in itertools.product([F(1, 2), F(1), F(2)], [F(-1), F(1, 3), F(1)]):
        s = [F(1), -a]
        u = [[F(3), off], [off, F(3)]]
        ap = [[(u[i][j] + (s[i] if i == j else 0))/2 for j in range(2)] for i in range(2)]
        bp = [[(u[i][j] - (s[i] if i == j else 0))/2 for j in range(2)] for i in range(2)]
        for v in [ap, bp]:
            require(v[0][0] >= 0 and v[1][1] >= 0
                    and v[0][0]*v[1][1] >= v[0][1]**2, "square root not PSD")
        h = [[sum(ap[i][k]*ap[k][j]-bp[i][k]*bp[k][j] for k in range(2))
              for j in range(2)] for i in range(2)]
        for i, j in itertools.product(range(2), repeat=2):
            require(h[i][j] == (s[i]+s[j])*u[i][j]/2, "anticommutator identity")
        lhs = sum(t*t for t in s)
        det = h[0][0]*h[1][1]-h[0][1]*h[1][0]
        norm2 = (h[0][0]+h[1][1])**2 - 4*min(F(0), det)
        require(lhs*lhs <= norm2, "Powers–Stormer bound")
        require(ap[0][1] != 0 and s[0] != s[1], "noncommuting control")
        cases += 1
    # Orthogonal rank-one ranges attain the square-root inequality exactly.
    ap, bp = [[F(1), F(0)], [F(0), F(0)]], [[F(0), F(0)], [F(0), F(1)]]
    root_distance = sum((ap[i][j]-bp[i][j])**2 for i, j in itertools.product(range(2), repeat=2))
    h = [[sum(ap[i][k]*ap[k][j]-bp[i][k]*bp[k][j] for k in range(2))
          for j in range(2)] for i in range(2)]
    require(root_distance == abs(h[0][0]) + abs(h[1][1]) and h[0][1] == 0,
            "singular equality control")
    return cases + 1


def must_reject(action):
    try:
        action()
    except (ValueError, ZeroDivisionError):
        return 1
    raise ValueError("malformed fixture was accepted")


def main():
    sparse_rows = []
    sparse_count = 0
    for n, epsilon, a in itertools.product(range(1, 7), [F(1, 2), F(1, 5), F(1, 100)], [F(1), F(3, 2)]):
        x, y, w = sparse(n, epsilon, a)
        g = geometry(x, y, w, a*a)
        err = procrustes_error(g)
        require(g["D"] == 2*a*a*epsilon*epsilon/n, "sparse pair loss")
        require(err.lo == err.hi == a*a*epsilon*(2-epsilon/n), "sparse Procrustes error")
        require(err.hi**2 <= 2*n*a*a*g["D"], "sharp geometric inequality")
        require(err.hi**2/(a*a*g["D"]) == 2*n*(1-epsilon/(2*n))**2,
                "sharp coefficient ratio")
        sparse_count += 1
        if a == 1 and epsilon == F(1, 100):
            sparse_rows.append({"dimension": n, "epsilon": str(epsilon), "D": str(g["D"]),
                                "rho_squared": str(err.lo),
                                "constant_ratio_squared": str(err.lo**2/g["D"])})

    one_dimensional, fixtures = finite_geometries()
    symbolic_rows = []
    for n, k in itertools.product(range(1, 4), [2, 3, 4, 8, 9]):
        x, y, _ = sparse(n, F(1, 5))
        f, g = replica_taylor(x, n, k), replica_taylor(y, n, k)
        require(f[0] == g[0] == {F(0): F(1)}, "constant replica coefficient")
        require(f[1] == g[1], "first derivative does not cancel")
        predicted = {F(2, k)-1: -F(k*(k-1), 4*n), F(-1): F(k*(k-1), 4*n)}
        actual = difference(f[2], g[2])
        require(actual == predicted, "replica second derivative coefficient")
        symbolic_rows.append({"dimension": n, "order": k,
                              "difference_epsilon2": [[str(z), str(c)] for z, c in sorted(actual.items())]})

    entropy_cases = []
    for n, epsilon in itertools.product([1, 2], [F(1, 2), F(1, 10), F(1, 100)]):
        x, y, w = sparse(n, epsilon)
        for k in [2, 3, 4, 8, 9]:
            entropy_cases.append((f"sparse_n{n}_e{epsilon}_k{k}", x, y, w, k))
    for i, (x, y, w) in enumerate(fixtures):
        for k in [2, 3]:
            entropy_cases.append((f"nonlinear_2d_{i}_k{k}", x, y, w, k))
    margins = []
    for label, x, y, w, k in entropy_cases:
        g = geometry(x, y, w, F(1))
        pf, pg = replica(x, w, k), replica(y, w, k)
        if g["D"] == 0:
            require(pf == pg, "isometry replica identity")
            continue
        gap = log_bounds(evaluate(pg) / evaluate(pf)) / (k-1)
        exponent = F(1) if k <= 2 else min(F(k, 2), F(4))
        lower_bound = (g["D"] / 4) * exp_bounds(-exponent)
        require(gap.lo >= lower_bound.hi, "finite dimension-free entropy lower bound: " + label)
        margins.append({"case": label, "gap": compact(gap),
                        "claimed_lower_bound": compact(lower_bound),
                        "certified_margin": compact(gap-lower_bound)})

    # Exact algebraic exponent audit of the one-center overlap formula;
    # this includes fractional orders without numerical quadrature.
    overlap_checks = 0
    centers = [(F(-1), F(0)), (F(0), F(1)), (F(0), F(0)),
               (F(3, 5), F(4, 5)), (F(-4, 5), F(-3, 5))]
    for alpha in [F(1, 4), F(1, 2), F(3, 4), F(1), F(3, 2), F(2), F(5, 2), F(9, 2), F(10)]:
        b = 1/alpha if alpha < 1 else F(1) if alpha <= 2 else min(alpha/2, F(4))
        for a, c, d in itertools.product(centers, repeat=3):
            v = tuple(a[j]+c[j]+(alpha-2)*d[j] for j in range(2))
            negative_log_k = (dot(a, a)+dot(c, c)+(alpha-2)*dot(d, d)-dot(v, v)/alpha)/2
            require(negative_log_k <= b, "one-center overlap exponent")
            overlap_checks += 1

    x, y, w = sparse(1, F(1, 2))
    rejected = sum([
        must_reject(lambda: sparse(0, F(1, 2))),
        must_reject(lambda: sparse(1, F(0))),
        must_reject(lambda: geometry(x, y, [F(1)]*3, F(1))),
        must_reject(lambda: geometry(x, y, w, F(1, 2))),
        must_reject(lambda: geometry(x, [(2*t[0],) for t in x], w, F(1))),
        must_reject(lambda: log_bounds(0)),
        must_reject(lambda: sqrt_bounds(-1)),
        must_reject(lambda: exp_bounds(130)),
        must_reject(lambda: Interval(2, 1)),
    ])
    require(exp_bounds(0) == Interval.of(1), "exp zero")
    require(log_bounds(1) == Interval.of(0), "log one")
    require(sqrt_bounds(F(4, 9)) == Interval.of(F(2, 3)), "rational square root")
    print(json.dumps({
        "status": "COVARIANCE_FREE_GAUSSIAN_CHECKS_PASS",
        "arithmetic": "integer and Fraction; outward rational Taylor enclosures",
        "sparse_geometries": sparse_count,
        "one_dimensional_contractions": one_dimensional,
        "two_dimensional_geometries": len(fixtures),
        "matrix_cases": matrix_checks(),
        "fractional_overlap_controls": overlap_checks,
        "symbolic_replica_cases": len(symbolic_rows),
        "finite_entropy_cases": len(entropy_cases),
        "strict_entropy_cases": len(margins),
        "rejected_invalid_inputs": rejected,
        "sharp_constant_controls": sparse_rows,
        "replica_coefficients": symbolic_rows,
        "selected_entropy_certificates": [margins[0], margins[4], margins[10], margins[-1]],
        "coverage": "finite corroboration only; continuum and asymptotic claims require PROOF.md",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
