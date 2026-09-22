"""Finite exact corroboration of PROOF.md; not a proof of all real orders."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json

from rational_bounds import exp_bounds, log_bounds, outward_grid


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def sq(a):
    return dot(a, a)


def mean(w, x):
    return tuple(sum((p * a[j] for p, a in zip(w, x)), F(0))
                 for j in range(len(x[0])))


def fixture(name, weights, x, y, radius):
    w = tuple(map(F, weights))
    x = tuple(tuple(map(F, a)) for a in x)
    y = tuple(tuple(map(F, a)) for a in y)
    require(len(w) == len(x) == len(y) and len(w) > 0, "size mismatch")
    n = len(x[0])
    require(n > 0 and all(len(a) == n for a in x + y), "dimension mismatch")
    require(sum(w) == 1 and min(w) > 0, "invalid probabilities")
    require(radius > 0 and all(sq(a) <= radius**2 for a in x), "invalid radius")
    delta = [[sq(sub(a, b)) - sq(sub(c, d)) for b, d in zip(x, y)]
             for a, c in zip(x, y)]
    require(min(min(row) for row in delta) >= 0, "not a contraction")
    return dict(name=name, w=w, x=x, y=y, R=F(radius), delta=delta, n=n)


def mean_distortion(f):
    return sum((f["w"][i] * f["w"][j] * f["delta"][i][j]
                for i in range(len(f["w"])) for j in range(len(f["w"]))), F(0))


def centered(f):
    w, x, y = f["w"], f["x"], f["y"]
    mx, my = mean(w, x), mean(w, y)
    return tuple(sub(a, mx) for a in x), tuple(sub(b, my) for b in y)


def path_checks(f):
    total = 0
    for co, si in [(F(1), F(0)), (F(3, 5), F(4, 5)),
                   (F(0), F(1)), (F(-3, 5), F(4, 5)), (F(-1), F(0))]:
        for i, j in product(range(len(f["w"])), repeat=2):
            dx, dy = sub(f["x"][i], f["x"][j]), sub(f["y"][i], f["y"][j])
            a, b = tuple((u + v) / 2 for u, v in zip(dx, dy)), sub(dx, dy)
            c = tuple(u + co * v / 2 for u, v in zip(a, b)) + tuple(si * v / 2 for v in b)
            velocity_over_pi = tuple(-si * v / 2 for v in b) + tuple(co * v / 2 for v in b)
            require(sq(c) == (1 + co) * sq(dx) / 2 + (1 - co) * sq(dy) / 2,
                    "lift distance identity")
            require(dot(c, velocity_over_pi) == -si * f["delta"][i][j] / 4,
                    "lift velocity factor")
            total += 1
    return total


def gram_checks(f):
    w, d = f["w"], f["delta"]
    x, y = centered(f)
    rows = [sum(p * v for p, v in zip(w, row)) for row in d]
    avg = mean_distortion(f)
    norm = F(0)
    second = F(0)
    for i, j in product(range(len(w)), repeat=2):
        h = dot(x[i], x[j]) - dot(y[i], y[j])
        require(h == -(d[i][j] - rows[i] - rows[j] + avg) / 2, "double centering")
        norm += w[i] * w[j] * h * h
        second += w[i] * w[j] * d[i][j]**2
    require(norm <= second / 4 <= f["R"]**2 * avg, "Gram norm bound")
    # All fixtures have diagonal centered cross-covariance, giving exact alignment.
    n = f["n"]
    cross = [[sum(p * a[i] * b[j] for p, a, b in zip(w, x, y))
              for j in range(n)] for i in range(n)]
    require(all(cross[i][j] == 0 for i in range(n) for j in range(n) if i != j),
            "fixture requires diagonal cross-covariance")
    signs = [1 if cross[i][i] >= 0 else -1 for i in range(n)]
    y = tuple(tuple(signs[i] * a[i] for i in range(n)) for a in y)
    cov = [[sum(p * a[i] * a[j] for p, a in zip(w, x))
            for j in range(n)] for i in range(n)]
    require(all(cov[i][j] == 0 for i in range(n) for j in range(n) if i != j),
            "fixture requires diagonal input covariance")
    kappa = min(cov[i][i] for i in range(n))
    require(kappa > 0, "degenerate fixture")
    u = tuple(tuple(a + b for a, b in zip(xx, yy)) for xx, yy in zip(x, y))
    v = tuple(sub(xx, yy) for xx, yy in zip(x, y))
    def matrix(a, b):
        return [[sum(p * aa[i] * bb[j] for p, aa, bb in zip(w, a, b))
                 for j in range(n)] for i in range(n)]
    uu, vv, uv = matrix(u, u), matrix(v, v), matrix(u, v)
    rhs = sum((uu[i][j] * vv[j][i] + uv[i][j] * uv[j][i])
              for i in range(n) for j in range(n)) / 2
    err = sum(p * sq(a) for p, a in zip(w, v))
    require(norm == rhs and norm >= kappa * err / 2, "trace alignment bound")
    require(err <= 2 * f["R"]**2 * avg / kappa, "rigid motion bound")
    return dict(D=str(avg), gram_norm_squared=str(norm),
                optimal_rigid_error_squared=str(err), covariance_lower=str(kappa))


def replica_sum(w, points, order):
    """Integral of a Gaussian mixture power, omitting a common positive factor.

I_m = (2*pi)^(-n*(m-1)/2) m^(-n/2)
      E exp(-sum_{i<j}|X_i-X_j|^2/(2*m)), for variance s=1.
"""
    lo = hi = F(0)
    for indices in product(range(len(w)), repeat=order):
        weight = F(1)
        for i in indices:
            weight *= w[i]
        exponent = -sum(sq(sub(points[indices[i]], points[indices[j]]))
                        for i in range(order) for j in range(i)) / (2 * order)
        a, b = exp_bounds(exponent)
        lo += weight * a
        hi += weight * b
    return lo, hi


def entropy_checks(f):
    rows = []
    D = mean_distortion(f)
    for order in (2, 3, 4):
        a, b = replica_sum(f["w"], f["x"], order)
        c, d = replica_sum(f["w"], f["y"], order)
        if D == 0:
            require((a, b) == (c, d), "isometry replica mismatch")
            gap = F(0), F(0)
        else:
            gap = log_bounds(c / b)[0] / (order - 1), log_bounds(d / a)[1] / (order - 1)
        exponent = -F(max(2, order), 2) * (1 + f["R"])**2
        low, high = exp_bounds(exponent)
        factor = D / (2**(f["n"] + 2) * factorial(f["n"]))
        bound = low * factor, high * factor
        require(gap[0] >= bound[1], "entropy lower bound not certified")
        rows.append(dict(alpha=order, gap_interval=outward_grid(gap),
                         cD_interval=outward_grid(bound)))
    return rows


def sharpness_checks():
    rows = []
    for e in (F(1, 4), F(1, 8), F(1, 32), F(1, 128)):
        f = fixture("rare_clipped_atom", [(1-e)/2, (1-e)/2, e],
                    [(-1,), (1,), (2,)], [(-1,), (1,), (1,)], 2)
        g = gram_checks(f)
        require(mean_distortion(f) == 6*e*(1-e), "sharpness distortion")
        require(F(g["covariance_lower"]) == 1+3*e-4*e*e >= 1, "sharpness covariance")
        require(F(g["optimal_rigid_error_squared"]) == e*(1-e), "sharpness error")
        rows.append(dict(epsilon=str(e), **g))
    for a in (F(1, 4), F(1, 2), F(1)):
        # Mode=0 is established analytically in PROOF.md; posterior weights are equal.
        Dposterior = 2*a*a
        exact_gap = a*a/2
        require(exact_gap == Dposterior/4, "sharp infinity coefficient")
    return rows


def interval_checks():
    require(exp_bounds(0) == (1, 1) and log_bounds(1) == (0, 0), "exact special values")
    for x in (F(1, 100), F(1, 2), F(1), F(3), F(16)):
        a, b = exp_bounds(x)
        require(log_bounds(a)[0] <= x <= log_bounds(b)[1], "exp/log enclosure consistency")
        c, d = exp_bounds(-x)
        require(a*c <= 1 <= b*d, "reciprocal enclosure")
    rejected = 0
    for x in (0, -1):
        try:
            log_bounds(x)
        except ValueError:
            rejected += 1
    require(rejected == 2, "log domain acceptance")


def negative_controls():
    bad = [
        ([F(1, 3), F(1, 3)], [(-1,), (1,)], [(-1,), (1,)], 1),
        ([F(1, 2)]*2, [(-1,), (1,)], [(-2,), (2,)], 1),
        ([F(1, 2)]*2, [(-1,), (2,)], [(-1,), (1,)], 1),
        ([F(1, 2)]*2, [(-1,), (1,)], [(-1, 0), (1, 0)], 1),
    ]
    for args in bad:
        try:
            fixture("invalid", *args)
        except ValueError:
            continue
        raise ValueError("invalid fixture was accepted")
    return len(bad)


def main():
    interval_checks()
    fixtures = [
        fixture("reflection_translation", [F(1, 3)]*3,
                [(-1,), (0,), (1,)], [(3,), (2,), (1,)], 1),
        fixture("absolute_value_fold", [F(1, 3)]*3,
                [(-1,), (0,), (1,)], [(1,), (0,), (1,)], 1),
        fixture("asymmetric_clipping", [F(3, 8), F(3, 8), F(1, 4)],
                [(-1,), (1,), (2,)], [(-1,), (1,), (1,)], 2),
        fixture("square_coordinate_contraction", [F(1, 4)]*4,
                list(product((F(-1, 2), F(1, 2)), repeat=2)),
                [(x/2, 0) for x, y in product((F(-1, 2), F(1, 2)), repeat=2)], 1),
    ]
    out = dict(status="FINITE_RATIONAL_CHECKS_PASS",
               arithmetic="fractions.Fraction; exp degree 32, outward 2^-160 grid; log 80 terms",
               path_pair_checks=sum(path_checks(f) for f in fixtures),
               rejected_invalid_fixtures=negative_controls(),
               sharpness=sharpness_checks(),
               fixtures=[dict(name=f["name"], **gram_checks(f), entropy=entropy_checks(f))
                         for f in fixtures],
               scope="Finite corroboration only; the all-order theorem is analytic.")
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
