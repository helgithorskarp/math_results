"""Finite support for the exact-minimum and full skew bridge.

Actual six-sendov-3 / researcher. Reuses five whole pinned same-author
PUBLIC10314 modules. Reads no generated mathematical record or peer program.
Globality, analytic inversion, stationarity and uniform Taylor bounds are
ordinary written mathematics, outside this finite computation.
"""
from pathlib import Path
import json, sys
from hashlib import sha256

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D / "kernel"))
import calculation as calc

j, s, F, need = calc.j, calc.s, calc.F, calc.need
ar = s.ar
ids = []
eq = lambda name, a, b: s.eq(ids, name, a, b)


def central_zero(poly):
    """Evaluate mu=mu_star,t=0 by the exact injective packed monomials."""
    out = s.N0
    for n, value in poly.items():
        need(type(n) is int and n >= 0, "nonnegative packed index")
        if n % 32 == 0:
            out = s.na(out, s.nm({0: value}, s.np(j.m.MUstar, n // 32)))
    return out


base = tuple(
    {key: tuple(central_zero(side) for side in g) for key, g in p.items()}
    for p in calc.no_ninth()
)
order = 10
base_p = s.actual_polynomial(*base, order, 2)
base_roots = s.roots_and_normals(base_p, order, ids)
for label in (3, 4, 5, 6):
    eq("BASELINE all4 active half-normals below10/" + str(label),
       base_roots[label]["normals"][:10], [s.G0] * 10)

q3, q4 = (base_roots[label]["normals"][10][0] for label in (3, 4))
A3, B3 = calc.AB[3]
A4, B4 = calc.AB[4]
h = s.ns(s.H, F(1, 7))
det = s.nm(h, s.na(s.nm(A4, B3), s.ns(s.nm(A3, B4), -1)))
tau = s.nm(s.nm(h, s.na(s.nm(B3, q4), s.ns(s.nm(B4, q3), -1))),
           s.ni(det))
beta = s.nm(s.na(s.nm(A3, q4), s.ns(s.nm(A4, q3), -1)),
            s.ni(det))
A, B, K = base
parts = (
    s.pa(A, {(10, 0): s.gf(tau)}),
    s.pa(B, {(10, 0): s.gf(tau)}),
    s.pa(K, {(8, 0): (s.N0, beta)}),
)
p = s.actual_polynomial(*parts, order, 2)
pn, powers = s.newton_polynomial(*parts, order, 2)
eq("ENTIRE zero-skew literal primitive versus all8 Newton slots",
   [g for row in p for g in row], [g for row in pn for g in row])
roots = s.roots_and_normals(p, order, ids)
for label in (3, 4, 5, 6):
    eq("ALL4 repaired half-normals through10/" + str(label),
       roots[label]["normals"], [s.G0] * 11)
for e in (1, 3, 5, 7, 9):
    eq("WHOLE zero-skew primitive odd epsilon/" + str(e), p[e], [s.G0] * 10)
    for label, row in enumerate(roots):
        eq("ALL9 zero-skew root odd epsilon/" + str(label) + "/" + str(e),
           [row["root"][e]], [s.G0])
anchor = [s.G1, s.G0, s.gs(s.G1, -1)] + [s.G0] * 8
eq("WHOLE actual ninth marked root", roots[0]["root"], anchor)
for label, row in enumerate(roots):
    eq("ALL9 WHOLE zero-skew root conjugacy/" + str(label),
       row["root"], [s.gc(g) for g in roots[(-label) % 9]["root"]])

for name, factor, expected in (
    ("small", parts[0], s.uz),
    ("large-center", parts[1], s.up),
):
    need(all(g[1] == s.N0 for g in factor.values()), "physical real factor " + name)
    eq("WHOLE normalized initial real critical/" + name,
       [factor[(2, 0)]], [s.gf(expected)])
alpha_star = s.na(s.w2, s.ns(j.m.MUstar, F(-1, 3)))
beta_star = s.na(s.w2, j.m.MUstar)
eq("WHOLE selected small real first jet", [parts[0][(4, 0)]], [s.gf(alpha_star)])
eq("WHOLE selected large real first jet", [parts[1][(4, 0)]], [s.gf(beta_star)])
need(all(g[0] == s.N0 for g in parts[2].values()), "whole pure imaginary split")
eq("WHOLE selected imaginary first jet", [parts[2][(2, 0)]],
   [(s.N0, s.gamma)])
first = calc.direct_first(parts, order)
eq("WHOLE positive FIRST versus separate scalar recursion",
   first, calc.scalar_recursion(parts, order, ids))
J0 = s.const(s.fcf(
    F(-8304485822364161, 181398528),
    F(-6510273073800785, 30233088),
    F(2123849893841477, 7558272),
))
target = [s.G0] * 11
for e, a in ((0, s.ns(s.N1, 8)), (2, s.C["C"]), (4, s.C["Bstar"]),
             (6, s.Tstar), (8, j.m.Gmean), (10, J0)):
    target[e] = s.gf(a)
eq("ENTIRE fresh zero-skew fifth scalar", first, target)
eq("ENTIRE physical zero cubic", calc.cubes(parts, order), [s.G0] * 11)

# Fresh full twelve-variable polynomial support for the credited limiting
# Hessian and the new sharp linear skew reduction. No axis sampling.
fc = lambda a, b=0, d=0: s.fcf(F(a), F(b), F(d))
aT = fc(F(-11564, 405), F(-20482, 81), F(123284, 405))
bT = fc(F(49, 180), F(-105889, 486), F(305123, 1215))
H = s.fH
b2 = ar.ns(H, F(1, 2))
gamma = ar.nm(s.fkappa, ar.ni(H))
field_scale = lambda p, a: ar.pm(ar.pc(a), p)
scalar = lambda q: ar.pc(ar.ns(ar.N1, F(q)))
vars = [ar.pv(ar.variable(i)) for i in range(12)]
hs, us = vars[:6], vars[6:]
sumh, sumu = ar.pa(*hs), ar.pa(*us)
squares = lambda items: ar.pa(*(ar.pm(x, x) for x in items))
sqh, squ = squares(hs), squares(us)
L0 = field_scale(sumh, ar.ns(H, F(-3, 2)))
Q = ar.pa(
    field_scale(sqh, ar.nm(aT, ar.ni(b2))),
    field_scale(ar.pm(sumh, sumh), ar.nm(bT, ar.ni(b2))),
    ar.ps(squ, F(1, 2)), ar.ps(ar.pm(sumu, sumu), F(1, 4)),
)
centered_h = [ar.pa(x, ar.ps(sumh, F(-1, 6))) for x in hs]
residual = ar.pa(
    field_scale(squares(centered_h), ar.nm(aT, ar.ni(b2))),
    ar.ps(squ, F(1, 2)), ar.ps(ar.pm(sumu, sumu), F(1, 4)),
)
rankone = field_scale(ar.pm(L0, L0), gamma)
need(Q == ar.pa(rankone, residual), "WHOLE12 sharp rank-one quadratic identity")

# The cubic follows exactly from h1+h2=-sumh and
# h1^2+h2^2=H-sumhsmall^2 at eta=0. It retains every small slot.
cubic = ar.pa(
    L0, ar.ps(ar.pm(sumh, sqh), F(3, 2)),
    ar.ps(ar.pm(ar.pm(sumh, sumh), sumh), F(1, 2)),
    *(ar.pm(ar.pm(x, x), x) for x in hs),
)
# Pair identity: (h1+h2)^3 - 3 h1*h2*(h1+h2), with
# 2 h1*h2=(h1+h2)^2-(h1^2+h2^2).
pair_sum = ar.ps(sumh, -1)
pair_sumsq = ar.pa(ar.pc(H), ar.ps(sqh, -1))
pair_product = ar.ps(ar.pa(ar.pm(pair_sum, pair_sum), ar.ps(pair_sumsq, -1)),
                     F(1, 2))
cubic_pair = ar.pa(
    ar.pm(ar.pm(pair_sum, pair_sum), pair_sum),
    ar.ps(ar.pm(pair_product, pair_sum), -3),
    *(ar.pm(ar.pm(x, x), x) for x in hs),
)
need(cubic == cubic_pair, "WHOLE12 exact cubic pair elimination")
linear = tuple(
    {m: q for m, q in component.items() if sum(m) == 1}
    for component in cubic
)
need(linear == L0, "WHOLE12 linear physical cubic at the analytic minimizer")
for i in range(12):
    derivative = tuple(ar.derivative(x, i) for x in cubic)
    constant_derivative = tuple(
        {m: q for m, q in x.items() if sum(m) == 0}
        for x in derivative
    )
    wanted = ar.pc(ar.ns(H, F(-3, 2))) if i < 6 else ar.pc(ar.N0)
    need(constant_derivative == wanted, "ALL12 cubic differential coordinate " + str(i))

# Equality direction x_h_i=-1/(9H), x_u_i=0 gives L0=1 and Q=gamma.
def at_equality(poly):
    answer = ar.N0
    value = ar.ns(ar.ni(H), F(-1, 9))
    monomials = set().union(*(set(x) for x in poly))
    for monomial in monomials:
        if any(monomial[i] for i in range(6, 20)):
            continue
        coeff = tuple(poly[k].get(monomial, F(0)) for k in range(6))
        answer = ar.na(answer, ar.nm(coeff, ar.np(value, sum(monomial[:6]))))
    return answer
need(at_equality(L0) == ar.N1, "ENTIRE sharp linear equality direction")
need(at_equality(Q) == gamma, "ENTIRE sharp quadratic equality direction")
need(at_equality(residual) == ar.N0, "ENTIRE centered/real residual vanishes")
need(ar.na(aT, ar.ns(bT, 6)) ==
     ar.ns(ar.nm(ar.np(H, 2), s.fkappa), F(27, 4)),
     "WHOLE field agreement with credited kappa/H")

signs = []
for name, a in (
    ("H", H), ("kappa", s.fkappa), ("gamma", gamma), ("aT", aT),
    ("aT_over_b2", ar.nm(aT, ar.ni(b2))), ("minus_J0", ar.ns(J0[0], -1)),
    ("even_normal_determinant", det[0]),
):
    coefficients = list(map(F, s.field_real_form(s.fc, a)))
    lo, hi, clo, chi = calc.rational_interval(coefficients)
    need(lo > 0, "strict rational field sign " + name)
    signs.append({"name": name, "whole_cubic": list(map(str, coefficients)),
                  "strict_rational_interval": [str(lo), str(hi)]})
for label in (0, 1, 2, 7, 8):
    g = roots[label]["normals"][2]
    need(g[1] == s.N0 and set(g[0]) == {0}, "whole inactive radial constant")
    coefficients = list(map(F, s.field_real_form(s.fc, g[0][0])))
    lo, hi, _, _ = calc.rational_interval(coefficients)
    need(hi < 0, "strict rational inactive radial " + str(label))
    signs.append({"name": "inactive_half_normal_" + str(label),
                  "whole_cubic": list(map(str, coefficients)),
                  "strict_rational_interval": [str(lo), str(hi)]})

record = {
    "agent": "six-sendov-3", "role": "researcher", "independent_review": False,
    "ordinary_analytic_bridges_outside_exact_kernel": True,
    "generated_mathematical_inputs_read": False,
    "same_author_public_kernel_pins": json.loads((D / "kernel-pins.json").read_text()),
    "whole_zero_skew_factors": j.encoded_parts(parts),
    "whole_all8_moments": [
        s.encoded_vector([power.get((e, 0), s.G0) for e in range(11)])
        for power in powers[1:]
    ],
    "whole_primitive": [s.encoded_vector(row) for row in p],
    "whole_all9_originals": s.output_roots(roots),
    "whole_first": s.encoded_vector(first), "J0": s.rpoly(J0),
    "selected_small_first_jet": s.rpoly(alpha_star),
    "selected_large_first_jet": s.rpoly(beta_star),
    "whole_quadratic": [ar.encoded(x) for x in Q],
    "whole_rankone": [ar.encoded(x) for x in rankone],
    "whole_residual": [ar.encoded(x) for x in residual],
    "whole_linear_cubic": [ar.encoded(x) for x in L0],
    "whole_exact_cubic": [ar.encoded(x) for x in cubic],
    "sharp_rankone_whole_coefficient_map_equal": True,
    "whole_cubic_pair_elimination_equal": True,
    "all12_cubic_differential_coordinates_equal": True,
    "equality_direction_L0": list(map(str, at_equality(L0))),
    "equality_direction_Q0": list(map(str, at_equality(Q))),
    "gamma": list(map(str, s.field_real_form(s.fc, gamma))),
    "whole_identities": ids, "whole_identity_count": len(ids),
    "strict_signs": signs,
    "scope": "Finite support only; the actual global fifth coefficient and full uniform sharp skew theorem require the separate ordinary written chart comparison.",
}
data = ar.canonical(record) + b"\n"
(D / "record.json").write_bytes(data)
print(json.dumps({"whole_identities": len(ids), "strict_signs": len(signs),
                  "whole_quadratic": True, "whole_cubic_differential": True,
                  "bytes": len(data), "sha256": sha256(data).hexdigest()}))
