#!/usr/bin/env python3
"""Exact arithmetic for the feasible constant-term / six-moment angular fiber.

CPython 3.11 standard library. Universal statements are ordinary proofs in
PROOF.md, not formalized by these finite certificates. Basic rational polynomial,
Sturm and interval helpers are adapted from the author's preceding full-sphere
checker. This file is standalone; it imports no predecessor or external data.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import resource
import time


def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    out = [Q(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        out[i] += x
    for i, x in enumerate(q):
        out[i] += x
    return trim(out)


def scale(p, c):
    return trim([x * c for x in p])


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def power(p, n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def derivative(p):
    return trim([i * x for i, x in enumerate(p)][1:] or [Q(0)])


def evaluate(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out * x + c
    return out


def divide(p, q):
    p, q = trim(p), trim(q)
    require(q != [0], "zero polynomial divisor")
    out = [Q(0)] * max(1, len(p) - len(q) + 1)
    while p != [0] and len(p) >= len(q):
        i, c = len(p) - len(q), p[-1] / q[-1]
        out[i] += c
        p = add(p, scale([Q(0)] * i + q, -c))
    return trim(out), p


def sturm(p):
    out = [p, derivative(p)]
    while out[-1] != [0]:
        nxt = scale(divide(out[-2], out[-1])[1], -1)
        if nxt == [0]:
            break
        out.append(nxt)
    return out


def variations(chain, x):
    signs = [1 if y > 0 else -1 for p in chain if (y := evaluate(p, x))]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def interval_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def interval_mul(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)


def interval_scale(a, c):
    return (a[0] * c, a[1] * c) if c >= 0 else (a[1] * c, a[0] * c)


def interval_div(a, b):
    require(b[0] > 0 or b[1] < 0, "interval division through zero")
    return interval_mul(a, (1 / b[1], 1 / b[0]))


def interval_poly(p, x):
    out = (Q(0), Q(0))
    for c in reversed(p):
        out = interval_add(interval_mul(out, x), (c, c))
    return out


def interval_square(a):
    if a[0] <= 0 <= a[1]:
        return Q(0), max(a[0] ** 2, a[1] ** 2)
    return min(x * x for x in a), max(x * x for x in a)


def outward_dyadic(a, bits=160):
    """Exact directed rounding, keeping portable witness fixtures compact."""
    denominator = 1 << bits
    lower = (a[0].numerator * denominator) // a[0].denominator
    upper = -((-a[1].numerator * denominator) // a[1].denominator)
    result = Q(lower, denominator), Q(upper, denominator)
    require(result[0] <= a[0] <= a[1] <= result[1],
            "directed dyadic enclosure")
    return result


def sqrt_interval(a):
    require(a[0] > 0, "nonpositive square-root input")
    out = []
    for x in a:
        lo, hi = Q(0), max(Q(1), x)
        for _ in range(150):
            mid = (lo + hi) / 2
            if mid * mid < x:
                lo = mid
            else:
                hi = mid
        out.append((lo, hi))
    return out[0][0], out[1][1]


def encoded(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encoded(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encoded(v) for v in x]
    return x


def monic(p):
    return scale(p, 1 / p[-1])


def gcd(p, q):
    while q != [0]:
        p, q = q, divide(p, q)[1]
    return monic(p)


def rem(p, h):
    return divide(p, h)[1]


def qm(p, q, h):
    return rem(mul(p, q), h)


def inverse(p, h):
    first, second = h, rem(p, h)
    u, v = [Q(0)], [Q(1)]
    while second != [0]:
        quotient, nxt = divide(first, second)
        first, second = second, nxt
        u, v = v, add(u, scale(mul(quotient, v), -1))
    require(len(first) == 1 and first[0] != 0, "polynomial is not invertible")
    out = rem(scale(u, 1 / first[0]), h)
    require(qm(out, p, h) == [Q(1)], "entire quotient inverse")
    return out


def trace_powers(h, n):
    d = len(h) - 1
    out, c = [Q(d)], list(reversed(h))
    for k in range(1, n + 1):
        if k <= d:
            value = -sum(c[j] * out[k-j] for j in range(1, k)) - k*c[k]
        else:
            value = -sum(c[j] * out[k-j] for j in range(1, d+1))
        out.append(value)
    return out


def trace(p, h):
    p = rem(p, h)
    return sum(x*y for x, y in zip(p, trace_powers(h, len(p)-1)))


def solve_positive(mat, rhs):
    require(len(mat) == len(rhs) and
            mat == [list(r) for r in zip(*mat)], "symmetric Gram input")
    aug = [list(row) + [x] for row, x in zip(mat, rhs)]
    n, pivots = len(rhs), []
    for j in range(n):
        pivot = aug[j][j]
        require(pivot > 0, "positive Gram elimination pivot")
        pivots.append(pivot)
        aug[j] = [x / pivot for x in aug[j]]
        for i in range(j+1, n):
            c = aug[i][j]
            aug[i] = [x-c*y for x, y in zip(aug[i], aug[j])]
    out = [Q(0)]*n
    for j in reversed(range(n)):
        out[j] = aug[j][-1] - sum(aug[j][k]*out[k] for k in range(j+1, n))
    require([sum(x*y for x, y in zip(row, out)) for row in mat] == rhs,
            "entire exact Gram solve")
    return out, pivots


def matrix_product(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def matvec(a, b):
    return [sum(x*y for x, y in zip(row, b)) for row in a]


def compression(u, f):
    # B=(e_i-e_8), K=B^T B=I+J, A=K^{-1} B^T diag(u) B.
    k = [[Q(int(i == j)+1) for j in range(7)] for i in range(7)]
    ki = [[Q(int(i == j))-Q(1, 8) for j in range(7)] for i in range(7)]
    d = [[u[i]*int(i == j)+u[7] for j in range(7)] for i in range(7)]
    a = matrix_product(ki, d)
    require(matrix_product(k, a) == d, "Gram selfadjoint compression")
    ap = [[Q(int(i == j)) for j in range(7)] for i in range(7)]
    ts = [Q(7)]
    for _ in range(12):
        ap = matrix_product(ap, a)
        ts.append(sum(ap[i][i] for i in range(7)))
    descending = [Q(1)]
    for j in range(1, 8):
        descending.append(-sum(descending[j-i]*ts[i]
                               for i in range(1, j+1))/j)
    h = scale(derivative(f), Q(1, 8))
    require(list(reversed(descending)) == h,
            "entire degree-seven matrix characteristic equals f'/8")
    v, mu = list(u[:7]), []
    for _ in range(7):
        mu.append(sum(x*y for x, y in zip(u[:7], matvec(k, v))))
        v = matvec(a, v)
    return h, ts, mu


def original_polynomial(u):
    require(len(u) == 8 and sum(u) == 0, "balanced eight original roots")
    f = [Q(1)]
    for x in u:
        f = mul(f, [-x, Q(1)])
    return f


def real_count(p):
    require(gcd(p, derivative(p)) == [Q(1)], "simple-root count input")
    chain = sturm(p)
    bound = 1 + max(abs(x) for x in p[:-1])
    require(evaluate(p, -bound) and evaluate(p, bound), "Sturm endpoints")
    return variations(chain, -bound) - variations(chain, bound)


def critical_nodes(u, h):
    # Each distinct original gap has one critical; each double original root
    # supplies one additional, inactive critical at the root itself.
    levels = sorted(set(u))
    require(all(u.count(x) <= 2 for x in levels), "simple critical spectrum")
    roots = [(x, x) for x in levels if u.count(x) == 2]
    for lo, hi in zip(levels, levels[1:]):
        for _ in range(155):
            mid = (lo+hi)/2
            value = sum(1/(x-mid) for x in u)
            if value < 0:
                lo = mid
            elif value > 0:
                hi = mid
            else:
                lo = hi = mid
                break
        require(all(not lo <= x <= hi for x in u), "secular enclosure pole")
        if lo != hi:
            require(sum(1/(x-lo) for x in u) < 0 <
                    sum(1/(x-hi) for x in u), "secular enclosure signs")
        else:
            require(evaluate(h, lo) == 0, "exact critical root")
        roots.append((lo, hi))
    roots.sort()
    require(len(roots) == 7 and all(roots[i][1] < roots[i+1][0]
            for i in range(6)), "seven disjoint critical enclosures")
    chain = sturm(h)
    for lo, hi in roots:
        require((lo == hi and evaluate(h, lo) == 0) or
                (lo < hi and variations(chain, lo)-variations(chain, hi) == 1),
                "independent Sturm critical isolation")
    return roots


def direct_mass(u, node):
    if node[0] == node[1] and u.count(node[0]) == 2:
        return Q(0), Q(0)
    total = (Q(0), Q(0))
    for x in u:
        inv = interval_div((Q(1), Q(1)), (x-node[1], x-node[0]))
        total = interval_add(total, interval_square(inv))
    return interval_div((Q(64), Q(64)), total)


def overlaps(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def nonnegative_mass(boxes):
    require(all(x[0] >= 0 for x in boxes), "nonnegative-mass feasibility")


def rejected(action, text):
    try:
        action()
    except ValueError as error:
        require(text in str(error), "unexpected negative-control failure")
        return str(error)
    raise ValueError("damaged mathematical control accepted")


class Dual:
    """Exact first-order algebra Q[epsilon]/(epsilon^2), no finite differences."""
    def __init__(self, value, slope=0):
        self.value, self.slope = Q(value), Q(slope)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, other):
        x = self.coerce(other)
        return Dual(self.value+x.value, self.slope+x.slope)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.slope)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        x = self.coerce(other)
        return Dual(self.value*x.value,
                    self.slope*x.value+self.value*x.slope)

    __rmul__ = __mul__

    def __truediv__(self, other):
        x = self.coerce(other)
        require(x.value != 0, "dual unit divisor")
        return Dual(self.value/x.value,
                    (self.slope*x.value-self.value*x.slope)/x.value**2)

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def __eq__(self, other):
        x = self.coerce(other)
        return self.value == x.value and self.slope == x.slope


def dual_polynomial(p, q):
    return [Dual(p[i] if i < len(p) else 0, q[i] if i < len(q) else 0)
            for i in range(max(len(p),len(q)))]


def first_variations(f, h, ih, m, eta, n, d):
    # Independent dual quotient trace versus explicit critical-root motion.
    hp = derivative(h)
    t, remainder = divide(mul(ih,hp),h)
    require(remainder == [Q(1)], "fixed inverse Bezout quotient")
    require(d == Q(3,8)*n*n-4*f[4], "Newton denominator coefficient")
    eta_slopes, c_slopes = [], []
    for k in range(6):
        q = [Q(0)]*k+[Q(1)]
        h1 = scale(derivative(q),Q(1,8))
        correction = scale(qm(ih, add(qm(ih,derivative(h1),h),
                              scale(qm(h1,t,h),-1)),h),-1)
        hd = dual_polynomial(h,h1)
        invd = dual_polynomial(ih,correction)
        require(qm(invd,derivative(hd),hd) == [Dual(1)],
                "whole moving-quotient dual inverse")
        md = scale(qm(dual_polynomial(f,q),invd,hd),-8)
        exact = Dual.coerce(trace(qm(md,md,hd),hd))
        require(exact.value == eta, "dual base entire mass square")
        # lambda_dot=-q'/(8h'); m_dot=-8q/h'-m q''/(8h')
        #                                  +m h''q'/(8h'^2).
        first = -16*trace(qm(qm(m,q,h),ih,h),h)
        second = -Q(1,4)*trace(qm(qm(qm(m,m,h),derivative(derivative(q)),h),ih,h),h)
        third = Q(1,4)*trace(qm(qm(qm(qm(m,m,h),derivative(hp),h),
                                   derivative(q),h),qm(ih,ih,h),h),h)
        require(exact.slope == first+second+third,
                "all six dual / root-motion first variations")
        d_slope = Q(-4) if k == 4 else Q(0)
        eta_slopes.append(exact.slope)
        c_slopes.append(-(exact.slope+(n*n-eta)/d*d_slope)/d)
    return eta_slopes, c_slopes


def study(name, values, expected_class):
    u = list(map(Q, values))
    f = original_polynomial(u)
    h, ts, mu = compression(u, f)
    require(gcd(h, derivative(h)) == [Q(1)], "squarefree derivative")
    require(ts == trace_powers(h, 12), "all thirteen matrix/Newton traces")
    n = sum(x*x for x in u)
    d = sum(x**4 for x in u)-n*n/8
    require(n > 0 and d > 0, "nonuniform angular domain")
    require(mu[:3] == [n, sum(x**3 for x in u), d],
            "raw angular mass moment normalization")
    ih = inverse(derivative(h), h)
    m, kap = scale(qm(f, ih, h), -8), scale(ih, -8)
    require([trace(qm(m, [Q(0)]*j+[Q(1)], h), h)
             for j in range(7)] == mu, "all seven scalar/matrix coupling moments")
    require([trace(qm(kap, [Q(0)]*j+[Q(1)], h), h)
             for j in range(7)] == [Q(0)]*6+[Q(-8)],
            "six invariant moments and seventh slope")
    eta = trace(qm(m, m, h), h)
    a = trace(qm(kap, kap, h), h)
    b = 2*trace(qm(m, kap, h), h)
    require(a > 0, "strict quadratic convexity")
    delta = -b/(2*a)
    r6 = eta-b*b/(4*a)
    star = add(m, scale(kap, delta))
    # Two independently computed Gram systems from full matrix traces/moments.
    g7 = [[ts[i+j] for j in range(7)] for i in range(7)]
    c7, piv7 = solve_positive(g7, mu)
    g6 = [[ts[i+j] for j in range(6)] for i in range(6)]
    c6, piv6 = solve_positive(g6, mu[:6])
    require(trim(c7) == m and sum(x*y for x,y in zip(c7,mu)) == eta,
            "whole seven-moment interpolation equals residue mass polynomial")
    require(trim(c6) == star and len(star) <= 6 and
            sum(x*y for x,y in zip(c6,mu[:6])) == r6,
            "whole six-moment projection equals centered mass polynomial")
    require(eta-r6 == a*delta**2 and
            [r6+a*delta**2, -2*a*delta, a] == [eta, b, a],
            "entire quadratic completion identity")
    # The scalar resolvent coefficients: 8(z h-f)/h, expanding at infinity.
    numerator = scale(add(mul([Q(0), Q(1)], h), scale(f, -1)), 8)
    require(len(numerator) <= 7, "balanced resolvent polynomial part")
    resolvent_moments = []
    for j in range(7):
        coeff = numerator[6-j] if 6-j < len(numerator) else Q(0)
        resolvent_moments.append(coeff-sum(
            h[7-k]*resolvent_moments[j-k] for k in range(1,j+1)))
    require(resolvent_moments == mu, "whole resolvent series through sixth moment")
    nodes = critical_nodes(u, h)
    fboxes, original, centered, squares = [], [], [], (Q(0), Q(0))
    for j, node in enumerate(nodes):
        fbox = interval_poly(f, node)
        hpbox = interval_poly(derivative(h), node)
        residue = interval_scale(interval_div(fbox, hpbox), -8)
        direct = direct_mass(u, node)
        polynomial = interval_poly(m, node)
        require(overlaps(direct, residue) and overlaps(direct, polynomial),
                "independent secular/residue mass agreement")
        hp_sign = 1 if j % 2 == 0 else -1
        require(hpbox[0] > 0 if hp_sign == 1 else hpbox[1] < 0,
                "ordered derivative signs")
        if node[0] == node[1] and node[0] in u:
            require(fbox == (0,0) and residue == direct == polynomial == (0,0),
                    "shared double original critical mass zero")
        else:
            require(fbox[1] < 0 if j % 2 == 0 else fbox[0] > 0,
                    "original hyperbolicity critical signs")
        fboxes.append(fbox)
        original.append(outward_dyadic(direct))
        centered.append(outward_dyadic(interval_poly(star, node)))
        squares = interval_add(squares, interval_square(direct))
    require(squares[0] <= eta <= squares[1], "independent all-mass-square sum")
    even = [fboxes[j] for j in [1,3,5]]
    odd = [fboxes[j] for j in [0,2,4,6]]
    lower = (-min(x[1] for x in even), -min(x[0] for x in even))
    upper = (-max(x[1] for x in odd), -max(x[0] for x in odd))
    if expected_class == "interior":
        require(lower[1] < delta < upper[0], "centered optimum strictly feasible")
        require(all(x[0] > 0 for x in centered), "strict centered masses")
        require(real_count(add(f, [delta])) == 8, "eight-real centered optimum")
        optimum, penalty, count = delta, Q(0), 8
    elif expected_class == "outside_lower":
        require(delta < lower[0], "centered optimum below feasible interval")
        require(any(x[1] < 0 for x in centered), "negative centered mass")
        require(real_count(add(f, [delta])) == 6, "six-real infeasible optimum")
        optimum, penalty, count = None, None, 6
    elif expected_class in ["clipped_zero", "singleton_zero"]:
        require(lower == (0,0) and delta < 0, "exact lower zero / clipped optimum")
        if expected_class == "clipped_zero":
            require(upper[0] > 0, "positive feasible interval length")
            legal_step = upper[0]/2
            require(real_count(add(f,[legal_step])) == 8,
                    "one-double fiber has a genuine feasible interior")
        else:
            require(upper == (0,0), "exact singleton feasible interval")
        require(any(x[1] < 0 for x in centered), "clipped negative centered mass")
        require(real_count(add(f,[delta])) == 6, "infeasible centered primitive")
        optimum, penalty, count = Q(0), a*delta**2, 6
    else:
        raise ValueError("unknown witness class")
    c0, cr6 = (n*n-eta)/d, (n*n-r6)/d
    eta_slopes, c_slopes = first_variations(f,h,ih,m,eta,n,d)
    require(eta_slopes[0] == b, "constant first variation equals quadratic b")
    if optimum is not None:
        feasible_eta = r6+penalty
        require(feasible_eta == eta+b*optimum+a*optimum**2,
                "whole clipped quadratic optimum")
        feasible_c = (n*n-feasible_eta)/d
    else:
        feasible_c = None  # The exact algebraic endpoint is bracketed, not rounded.
    return {
        "name": name, "original_roots": u, "original_levels": len(set(u)),
        "f": f, "h": h, "N": n, "D": d,
        "matrix_trace_powers_0_to_12": ts, "matrix_coupling_moments_0_to_6": mu,
        "residue_mass_polynomial": m, "mass_slope_polynomial": kap,
        "eta": eta, "quadratic_linear": b, "quadratic_leading": a,
        "delta_star": delta, "R6": r6,
        "centered_mass_polynomial": star,
        "gram7_positive_pivots": piv7, "gram6_positive_pivots": piv6,
        "critical_root_enclosures": [outward_dyadic(x) for x in nodes],
        "raw_original_mass_enclosures": original,
        "centered_mass_enclosures": centered,
        "feasible_lower_endpoint_enclosure": outward_dyadic(lower),
        "feasible_upper_endpoint_enclosure": outward_dyadic(upper),
        "classification": expected_class, "simple_real_roots_at_delta_star": count,
        "delta_hat_exact_when_rational": optimum,
        "feasibility_penalty_exact_when_rational": penalty,
        "C_original": c0, "C_R6": cr6,
        "formal_eta_slopes_constant_through_z5": eta_slopes,
        "formal_C_slopes_constant_through_z5": c_slopes,
        "C_fiber_optimum_exact_when_rational": feasible_c
    }


def verify():
    records = {}
    inputs = [
        ("symmetric_interior", [-7,-5,-3,-1,1,3,5,7], "interior"),
        ("high_eight_level_infeasible", [-86,-85,-84,-83,40,98,99,101], "outside_lower"),
        ("near_c3_eight_level_infeasible",
         [-856,-854,-852,-850,412,998,1000,1002], "outside_lower"),
        ("high_seven_level_clipped", [-86,-85,-85,-83,40,98,99,102], "clipped_zero"),
        ("six_level_singleton", [-86,-85,-85,-83,40,40,128,131], "singleton_zero")
    ]
    for name, u, kind in inputs:
        records[name] = study(name, u, kind)
    sym = records["symmetric_interior"]
    require(sym["delta_star"] == Q(-1294848,280993) and
            sym["C_original"] == Q(2901071152,323219671) and
            sym["C_R6"] == Q(2522064,280993), "compact interior rational benchmark")
    near = records["near_c3_eight_level_infeasible"]
    require(Q(2453,100) < near["C_original"] < near["C_R6"] < Q(6133,250),
            "strict high-value infeasible rational benchmark")
    scaled = study("scaled_signed_interior",
                   [-3*x for x in inputs[0][1]], "interior")
    for field, factor in [("delta_star", Q(3)**8), ("N",Q(9)), ("D",Q(81)),
                          ("eta",Q(81)),("R6",Q(81)),
                          ("quadratic_leading",Q(1,3**12)),
                          ("C_original",Q(1)), ("C_R6",Q(1))]:
        require(scaled[field] == factor*sym[field], "raw scaling / sign covariance")
    records["scaled_signed_interior"] = scaled
    # Degenerate derivative: no seven-node inversion, and every nonzero
    # primitive shift is forbidden by the repeated critical root.
    u = list(map(Q, [-5,-5,-5,1,2,3,4,5]))
    f = original_polynomial(u)
    h, ts, mu = compression(u, f)
    g = gcd(h, derivative(h))
    require(g == [Q(5),Q(1)] and evaluate(h,Q(-5)) == 0 and
            evaluate(derivative(h),Q(-5)) == 0 and
            evaluate(f,Q(-5)) == 0, "exact repeated-derivative obstruction")
    degenerate = {"u":u,"f":f,"h":h,"derivative_gcd":g,
                  "feasible_interval":[Q(0),Q(0)]}
    for step in [Q(-1,1000),Q(1,1000)]:
        require(evaluate(add(f,[step]),Q(-5)) == step,
                "repeated critical is not an original shifted root")
        count = real_count(add(f,[step]))
        require(count < 8, "nonzero repeated-critical primitive not hyperbolic")
        degenerate["shift_"+str(step)+"_simple_real_roots"] = count
    records["triple_original_singleton"] = degenerate
    clipped = records["high_seven_level_clipped"]
    records["negative_controls"] = {
        "wrong_residue_factor": rejected(lambda: require(
            trace(scale(sym["residue_mass_polynomial"],8),sym["h"]) == sym["N"],
            "residue normalization"), "residue normalization"),
        "ignore_feasibility": rejected(lambda: nonnegative_mass(
            records["high_eight_level_infeasible"]["centered_mass_enclosures"]),
            "nonnegative-mass feasibility"),
        "ignore_clipping": rejected(lambda: require(
            clipped["C_R6"] == clipped["C_fiber_optimum_exact_when_rational"],
            "nonzero clipping penalty"), "nonzero clipping penalty"),
        "all_double_fibers_singleton": rejected(lambda: require(
            clipped["feasible_upper_endpoint_enclosure"] == (0,0),
            "one-double positive fiber"), "one-double positive fiber"),
        "invert_repeated_derivative": rejected(lambda: inverse(derivative(h),h),
                                               "polynomial is not invertible"),
        "omit_critical_motion": rejected(lambda: require(
            sym["formal_eta_slopes_constant_through_z5"][2] ==
            -16*trace(qm(qm(sym["residue_mass_polynomial"],
                            [Q(0),Q(0),Q(1)],sym["h"]),
                          inverse(derivative(sym["h"]),sym["h"]),sym["h"]),
                      sym["h"]), "critical-motion contribution"),
            "critical-motion contribution")
    }
    return encoded(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    records = verify()
    if args.expected:
        require(json.loads(args.expected.read_text()) == records,
                "entire external fixture differs")
    if args.write_fixture:
        args.write_fixture.write_text(json.dumps(records,indent=2,sort_keys=True)+"\n")
    digest = hashlib.sha256(json.dumps(records,sort_keys=True,
                            separators=(",",":")).encode()).hexdigest()
    print(json.dumps({"status":"checked","records":len(records),
        "simple_critical_profiles":6, "mathematical_negative_controls":6,
        "record_sha256":digest, "elapsed_seconds":time.monotonic()-start,
        "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
