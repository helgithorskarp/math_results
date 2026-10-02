"""Fresh exact referee corroboration; Python standard library only.

Sparse commutative Q polynomials use sorted token multisets. Complex
coefficients and their conjugates are separate formal tokens. Pointwise
physical controls use Gaussian rationals. Ordinary inequalities remain
the written proof's responsibility, not consequences of finite controls.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib
import json


def need(value, message):
    if not value:
        raise ValueError(message)


def add(*ps):
    out = {}
    for p in ps:
        for m, v in p.items():
            out[m] = out.get(m, F(0)) + v
    return {m: v for m, v in out.items() if v}


def scale(p, q):
    return {m: v * q for m, v in p.items() if v * q}


def mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            m = tuple(sorted(a + b))
            out[m] = out.get(m, F(0)) + x * y
    return {m: v for m, v in out.items() if v}


def const(q):
    return {(): F(q)} if q else {}


def var(k):
    return {(k,): F(1)}


def power(p, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def conj(p):
    out = {}
    for m, q in p.items():
        need(all(0 <= k < 18 for k in m), 'conjugate token domain')
        out[tuple(sorted((k + 9) % 18 for k in m))] = q
    return out


def substitute(p, assignments):
    out = {}
    for m, v in p.items():
        term = const(v)
        for k in m:
            term = mul(term, assignments.get(k, var(k)))
        out = add(out, term)
    return out


def pack(p):
    return [[list(m), str(v)] for m, v in sorted(p.items())]


def digest(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ga_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def ga_mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def ga_conj(a):
    return a[0], -a[1]


def norm(a):
    return a[0] ** 2 + a[1] ** 2


def ga_product(items):
    out = F(1), F(0)
    for x in items:
        out = ga_mul(out, x)
    return out


def weights():
    roots = [
        [(F(1), F(0))] * 9,
        [(F(0), F(0))] * 9,
        [(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1)),
         (F(0), F(0)), (F(0), F(0)), (F(1, 2), F(1, 2)),
         (F(3, 5), F(-4, 5)), (F(2, 3), F(0))],
        [(F(1), F(0)), (F(1, 3), F(2, 3)), (F(2, 3), F(-1, 3)),
         (F(0), F(0)), (F(1, 2), F(1, 3)), (F(-1, 4), F(1, 2)),
         (F(1, 5), F(1, 5)), (F(-1, 3), F(1, 4)), (F(1, 7), F(-1, 5))],
    ]
    points = [(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1)),
              (F(3, 5), F(4, 5)), (F(5, 13), F(-12, 13))]
    records = []
    for number, rs in enumerate(roots):
        need(all(norm(r) <= 1 for r in rs), 'literal disk roots')
        for w in points:
            need(norm(w) == 1, 'literal unit point')
            factors = [ga_add(w, (-r[0], -r[1])) for r in rs]
            p = ga_product(factors)
            derivative = (F(0), F(0))
            omitted = []
            for k in range(9):
                v = ga_product(factors[:k] + factors[k + 1:])
                derivative = ga_add(derivative, v)
                omitted.append((1 - norm(rs[k])) * norm(v))
            direct = 2 * ga_mul(ga_mul(w, derivative), ga_conj(p))[0] - 9 * norm(p)
            need(direct == sum(omitted) and direct >= 0, 'division-free physical weight')
            records.append({'roots': number, 'unit_point': [str(x) for x in w],
                            'weight': str(direct), 'summands': [str(x) for x in omitted],
                            'sampled_original_collision': p == (0, 0)})
    need(sum(r[1] for r in roots[3]) != 0, 'nonreal physical polynomial control')
    return records


def identities():
    d = [var(k) for k in range(9)]
    # Unreduced original polynomial c0=d0-1, degree-nine coefficient 1.
    p = [add(d[0], const(-1))] + d[1:] + [const(1)]
    folded = [{} for _ in range(9)]
    for i in range(10):
        for j in range(10):
            folded[(i - j) % 9] = add(folded[(i - j) % 9],
                                      scale(mul(p[i], conj(p[j])), i + j - 9))
    # Separately multiply p and wp' AFTER evaluation on the cyclic grid.
    evaluated_derivative = [const(9)] + [scale(d[k], k) for k in range(1, 9)]
    cyclic = [{} for _ in range(9)]
    for i in range(9):
        for j in range(9):
            term = add(mul(evaluated_derivative[i], conj(d[j])),
                       mul(d[i], conj(evaluated_derivative[j])),
                       scale(mul(d[i], conj(d[j])), -9))
            cyclic[(i - j) % 9] = add(cyclic[(i - j) % 9], term)
    need(folded == cyclic, 'all nine complete Fourier coefficients')
    D = add(scale(add(d[0], conj(d[0])), 9),
            *[scale(mul(d[k], conj(d[k])), 2 * k - 9) for k in range(9)])
    row1 = add(scale(add(d[1], conj(d[8])), 9),
               *[scale(mul(d[j + 1], conj(d[j])), 2 * j - 8) for j in range(8)],
               scale(mul(d[0], conj(d[8])), -1))
    row2 = add(scale(add(d[2], conj(d[7])), 9),
               *[scale(mul(d[j + 2], conj(d[j])), 2 * j - 7) for j in range(7)],
               scale(mul(d[0], conj(d[7])), -2))
    need([D, row1, row2] == folded[:3], 'zero/first/second rows and wraps')
    need((1, 17) not in row2, 'zero second extra wrap')
    need(all(conj(folded[k]) == folded[(-k) % 9] for k in range(9)), 'full conjugate symmetry')
    # Full elementary symmetric sums in EIGHT independent critical tokens.
    zs = [var(24 + k) for k in range(8)]
    es = [const(1)]
    for m in range(1, 9):
        es.append(add(*[mul_all(zs[k] for k in ids) for ids in combinations(range(8), m)]))
    T = [add(*[power(z, m) for z in zs]) for m in range(1, 4)]
    c8, c7, c6 = scale(es[1], F(-9, 8)), scale(es[2], F(9, 7)), scale(es[3], F(-3, 2))
    need(T[0] == scale(c8, F(-8, 9)), 'first Newton identity')
    need(T[1] == add(power(T[0], 2), scale(c7, F(-14, 9))), 'second Newton identity')
    third = add(scale(power(T[0], 3), F(-1, 4)),
                scale(mul(T[0], T[1]), F(3, 4)), scale(T[2], F(-1, 2)))
    need(c6 == third, 'whole third Newton identity')
    # Build the complete monic critical polynomial directly and compare all
    # elementary coefficients with the integrated derivative's coefficients.
    direct = [const(1)]
    for z in zs:
        nxt = [{} for _ in range(len(direct) + 1)]
        for j, q in enumerate(direct):
            nxt[j] = add(nxt[j], scale(mul(q, z), -1))
            nxt[j + 1] = add(nxt[j + 1], q)
        direct = nxt
    need(direct == [scale(es[8 - k], (-1) ** (8 - k)) for k in range(9)], 'whole critical polynomial')
    # Negative controls exercise nonzero first wrap, absent second wrap,
    # conjugation, and the third-moment sign.
    need(row1 != add(row1, mul(d[0], conj(d[8]))), 'missing first wrap rejected')
    need(row2 != add(row2, mul(d[1], conj(d[8]))), 'extra second wrap rejected')
    need(row1 != substitute(row1, {17: d[8]}), 'unconjugated top term rejected')
    need(c6 != add(third, T[2]), 'wrong third-moment sign rejected')
    return {'cyclic_rows': [pack(q) for q in folded], 'critical_polynomial': [pack(q) for q in direct],
            'third_identity': pack(third), 'mathematical_damages_rejected': 4}


def mul_all(items):
    out = const(1)
    for q in items:
        out = mul(out, q)
    return out


def norm_polynomials():
    eta, x, y, L, b1, b2 = [var(k) for k in range(18, 24)]
    D0 = add(scale(eta, 9), x, y, L)
    alpha = F(151, 1024)
    D9 = add(scale(eta, F(27, 4)), scale(y, -alpha), scale(power(eta, 2), 18),
             scale(mul(eta, x), 18), scale(mul(eta, y), 14), scale(L, 2),
             scale(power(x, 2), F(23, 9)), scale(power(y, 2), F(5, 9)), scale(power(L, 2), F(1, 3)))
    Q1 = add(mul(D0, x), scale(mul(x, y), 6), scale(mul(D0, b1), 8),
             scale(power(L, 2), 8), scale(mul(y, L), 4))
    Q2 = add(scale(mul(D0, y), 2), scale(mul(D0, b2), 7), scale(power(L, 2), 7),
             scale(mul(y, L), 3), scale(mul(x, L), 5))
    r1, r2 = add(D9, scale(Q1, F(1, 9)), b1), add(D9, scale(Q2, F(1, 9)), b2)
    # Explicit written row16, independently compared coefficient by coefficient.
    written1 = add(scale(eta, F(27, 4)), scale(y, -alpha), scale(power(eta, 2), 18),
        scale(mul(eta, x), 19), scale(mul(eta, y), 14), scale(L, 2),
        scale(power(x, 2), F(8, 3)), scale(power(y, 2), F(5, 9)),
        scale(mul(x, y), F(7, 9)), scale(mul(L, x), F(1, 9)),
        scale(power(L, 2), F(11, 9)), scale(mul(y, L), F(4, 9)), b1, scale(mul(D0, b1), F(8, 9)))
    need(r1 == written1, 'entire first norm polynomial')
    # Written row17 retains D0, unlike row16's collected expression.
    written2 = add(D9, scale(mul(D0, y), F(2, 9)), scale(mul(D0, b2), F(7, 9)),
                   scale(power(L, 2), F(7, 9)), scale(mul(y, L), F(1, 3)),
                   scale(mul(x, L), F(5, 9)), b2)
    need(r2 == written2, 'entire second norm polynomial')
    return r1, r2


def budgets(H, Y, C, t3):
    e, E, d, alpha = F(1, 65536), F(1, 256), F(1, 1000), F(151, 1024)
    margins = {}
    def margin(name, value):
        need(value > 0, name)
        margins[name] = str(value)
    margin('critical_radius_squared', F(23, 4) ** 2 - H)
    margin('critical_radius_ratio', 6 - F(23, 4) * F(256, 255))
    if H < 32:
        margin('initial_c8_squared', 18 ** 2 - F(81, 8) * H)
    # At H32 the first bound is non-strict; no artificial strict margin.
    need(F(81, 8) * H <= 18 ** 2, 'initial non-strict c8 envelope')
    lower = [F(9, k) * comb(8, 9 - k) * 2 ** (9 - k) * E ** (7 - k) for k in range(1, 7)]
    margin('initial_lower_sum', 3 - sum(lower))
    margin('c1_small', d - lower[0]); margin('c2_small', d - lower[1])
    r1, r2 = norm_polynomials()
    positive = [add(r, scale(var(20), alpha)) for r in [r1, r2]]
    need(all(v >= 0 for r in positive for v in r.values()), 'monotone positive coefficients')
    eta = var(18)
    coarse = substitute(positive[0], {20: scale(eta, F(9, 2) * H), 21: scale(eta, 3),
                                      22: scale(eta, d)})
    allowed = {(18,), (19,), (18, 18), (18, 19), (19, 19)}
    need(set(coarse) <= allowed, 'coarse mean monomial coverage')
    initial_const = coarse.get((18,), 0) + e * coarse.get((18, 18), 0)
    lam = coarse.get((19,), 0) + e * coarse.get((18, 19), 0) + 18 * E * coarse.get((19, 19), 0)
    margin('mean_constant_below13', 13 - initial_const)
    margin('mean_feedback_below1_5', F(1, 5) - lam)
    margin('mean_bound_below17', 17 - F(65, 4))
    margin('second_coefficient_below_Y', Y - F(9, 14) * (H + F(64, 81) * 17 ** 2 * e))
    margin('first_moment_below16', 16 - F(8, 9) * 17)
    margin('third_moment_squared', t3 ** 2 - H ** 3)
    lower_sum = sum(lower[:5]) + 1024 * e ** 2 + 12 * H * e + F(t3, 2) * E
    margin('improved_lower_sum', C - lower_sum)
    final = [substitute(r, {19: scale(eta, 17), 20: scale(eta, Y), 21: scale(eta, C),
                           22: scale(eta, d), 23: scale(eta, d)}) for r in positive]
    need(all(set(r) <= {(18,), (18, 18)} for r in final), 'final whole polynomial coverage')
    need(final[0].get((18,), 0) == final[1].get((18,), 0), 'shared final linear constant')
    base = final[0][(18,)]
    Ks = [r[(18, 18)] for r in final]
    for j, K in enumerate(Ks):margin('final_quadratic_below2000_'+str(j), 2000 - K)
    mu = base + 2000 * e
    margin('all_top_below31_4', F(31, 4) - mu)
    if H == 32:
        margin('c8_below61_8', F(61, 8) - mu)
        margin('c7_below27_4', F(27, 4) - mu / (1 + alpha))
    return {'H': H, 'Y': Y, 'C': str(C), 'third_moment_majorant': t3,
            'lower_initial': [str(q) for q in lower], 'coarse_constant': str(initial_const),
            'coarse_feedback': str(lam), 'lower_improved': str(lower_sum),
            'final_linear': str(base), 'final_quadratics': [str(q) for q in Ks],
            'top_upper_mu': str(mu), 'c7_upper_mu': str(mu / (1 + alpha)),
            'strict_margins': margins, 'initial_c8_can_be_equal': H == 32}


def build():
    symbolic = identities()
    norms = norm_polynomials()
    return {'schema': 'six-reviewer-1-low-energy-audit-v1', 'symbolic': symbolic,
            'norm_bound_polynomials': [pack(p) for p in norms], 'physical_weight_controls': weights(),
            'original30': budgets(30, 20, F(3, 8), 165), 'refined32': budgets(32, 21, F(2, 5), 182),
            'ordinary_trust_boundary': 'all-index analytic tails, disk-root identity proof, triangle/Maclaurin/monotonicity and actual-root quantifiers; finite controls are corroboration, not infinite proof'}


def same_typed(actual, expected):
    need(type(actual) is type(expected), 'typed fixture mismatch')
    if isinstance(actual, dict):
        need(actual.keys() == expected.keys(), 'fixture key set')
        for k in actual:same_typed(actual[k], expected[k])
    elif isinstance(actual, list):
        need(len(actual) == len(expected), 'fixture list length')
        for a, b in zip(actual, expected):same_typed(a, b)
    else:
        need(actual == expected, 'entire fixture value')
