"""Finite exact corroboration of PROOF.md; not the ordinary analytic bridges.

Sparse polynomials use twelve commuting indeterminates and arbitrary-precision
rational coefficients. Each identity compares its entire coefficient map.
All scalar budgets concern the single endpoint e=2**-16.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
import json

E = F(1, 65536)
DIM = 12
ZERO = (0,) * DIM


class CertificateError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise CertificateError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def constant(q):
    return {} if not q else {ZERO: F(q)}


def variable(i):
    exponent = list(ZERO)
    exponent[i] = 1
    return {tuple(exponent): F(1)}


def add(*polys):
    out = {}
    for p in polys:
        for monomial, q in p.items():
            out[monomial] = out.get(monomial, F(0)) + q
    return {m: q for m, q in out.items() if q}


def scale(p, q):
    return {m: a * q for m, a in p.items() if a * q}


def multiply(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            exponent = tuple(x + y for x, y in zip(m, n))
            out[exponent] = out.get(exponent, F(0)) + a * b
    return {m: a for m, a in out.items() if a}


def power(p, n):
    need(type(n) is int and n >= 0, "invalid polynomial exponent")
    out = constant(1)
    for _ in range(n):
        out = multiply(out, p)
    return out


def derivative(p, i):
    out = {}
    for m, q in p.items():
        if m[i]:
            exponent = list(m)
            exponent[i] -= 1
            out[tuple(exponent)] = q * m[i]
    return out


def substitute(p, i, image):
    out = {}
    for m, q in p.items():
        exponent = list(m)
        exponent[i] = 0
        out = add(out, multiply({tuple(exponent): q}, power(image, m[i])))
    return out


def encoded(p):
    # The whole sparse coefficient map, not a sampled evaluation.
    return [[list(m), str(q)] for m, q in sorted(p.items())]


def identity(rows, name, lhs, rhs):
    difference = add(lhs, scale(rhs, -1))
    need(not difference, "identity: " + name)
    rows.append({"name": name, "coefficient_count": len(lhs),
                 "lhs_sha256": sha256(canonical(encoded(lhs))).hexdigest(),
                 "rhs_sha256": sha256(canonical(encoded(rhs))).hexdigest(),
                 "nonzero_residual_coefficients": len(difference)})


def margin(rows, name, lhs, rhs=0, strict=True):
    lhs, rhs = F(lhs), F(rhs)
    need(lhs > rhs if strict else lhs >= rhs, "budget: " + name)
    rows.append({"name": name, "lhs": str(lhs), "rhs": str(rhs),
                 "difference": str(lhs - rhs), "strict": strict})


def field_multiply(x, y):
    # Q[w]/(w**2+w+1).  conjugation sends w to -1-w.
    a, b = x
    c, d = y
    return (a*c - b*d, a*d + b*c - b*d)


def field_power(x, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = field_multiply(out, x)
    return out


def finite_identities(changes):
    rows = []
    roots = [variable(i) for i in range(8)]
    z, a, eta, k = [variable(i) for i in range(8, 12)]
    elementary = [constant(1)] + [{} for _ in range(8)]
    product = constant(1)
    for root in roots:
        product = multiply(product, add(z, scale(root, -1)))
        for m in range(8, 0, -1):
            elementary[m] = add(elementary[m],
                                 multiply(root, elementary[m-1]))
    coefficient = {9-m: scale(elementary[m], F(9, 9-m) * (-1)**m)
                   for m in range(1, 9)}
    primitive = add(power(z, 9), *[
        multiply(coefficient[j], power(z, j)) for j in range(1, 9)])
    identity(rows, "all eight integrated derivative coefficients",
             derivative(primitive, 8),
             scale(product, changes.get("derivative_factor", 9)))
    s1 = add(*roots)
    s2 = add(*[power(root, 2) for root in roots])
    identity(rows, "Newton first power trace", s1,
             scale(coefficient[8], F(-8, 9)))
    identity(rows, "Newton second power trace", s2,
             add(power(s1, 2), scale(coefficient[7],
                 -changes.get("newton_factor", F(14, 9)))))

    # Here roots[i] instead stand for the independent complex c_(i+1).
    polynomial = add(power(z, 9), *[
        multiply(roots[j-1], power(z, j)) for j in range(1, 9)])
    anchored = add(polynomial,
                   scale(substitute(polynomial, 8, a), -1))
    anchored_rhs = add(power(z, 9), scale(power(a, 9), -1), *[
        multiply(roots[j-1], add(power(z, j), scale(power(a, j), -1)))
        for j in range(1, 9)])
    identity(rows, "anchor determines the uncapped constant",
             anchored, anchored_rhs)
    dp = substitute(derivative(polynomial, 8), 8, a)
    ddp = substitute(derivative(derivative(polynomial, 8), 8), 8, a)
    identity(rows, "marked trace numerator after clearing a",
             add(multiply(a, ddp), scale(dp, -8)),
             add(*[scale(multiply(roots[j-1], power(a, j-1)), j*(j-9))
                   for j in range(1, 9)]))

    pair_table = []
    for j in range(1, 9):
        wj = field_power((F(0), F(1)), j)
        cj = field_power((F(-1), F(-1)), j)
        pair = tuple((x+y)/2 for x, y in zip(wj, cj))
        normal_weight = F(0) if j % 3 == 0 else F(-3, 2)
        if j == 6:
            normal_weight = changes.get("c6_pair_weight", normal_weight)
        need(pair == (normal_weight + 1, F(0)),
             "identity: cube-root paired complex coefficient " + str(j))
        pair_table.append({"j": j, "average_in_Qw": [str(q) for q in pair],
                           "linear_normal_weight": str(normal_weight),
                           "imaginary_coefficient_contribution": "0"})
    rows.append({"name": "complete cube-root coefficient table",
                 "rows": pair_table})

    x, y = variable(0), variable(1)
    quadratic = add(power(x, 2), power(y, 2))
    u = add(scale(multiply(x, z), -2), multiply(quadratic, power(z, 2)))
    jet = constant(1)
    binomial = F(1)
    for n in range(1, 4):
        binomial *= (F(-1, 2) - (n-1)) / n
        jet = add(jet, scale(power(u, n), binomial))
    jet = {m: q for m, q in jet.items() if m[8] <= 3}
    expected_jet = add(constant(1), multiply(x, z),
        multiply(add(power(x, 2), scale(power(y, 2), F(-1, 2))), power(z, 2)),
        multiply(add(power(x, 3), scale(multiply(x, power(y, 2)),
                     -changes.get("cubic_coefficient", F(3, 2)))), power(z, 3)))
    identity(rows, "entire reciprocal homogeneous jet through degree three",
             jet, expected_jet)
    identity(rows, "total-energy real-second-trace relation",
             quadratic, add(scale(power(x, 2), 2),
                            scale(add(power(x, 2), scale(power(y, 2), -1)), -1)))
    identity(rows, "Young cubic-loss square after clearing 4a^5",
             power(add(multiply(a, x), scale(y, -3)), 2),
             add(multiply(power(a, 2), power(x, 2)), scale(power(y, 2), 9),
                 scale(multiply(multiply(a, x), y), -6)))
    aa = add(constant(1), scale(eta, -1))
    j_lhs = add(scale(power(aa, 2), 72), scale(power(aa, 3), -72),
                scale(eta, -42), scale(multiply(multiply(k, eta), aa), -8),
                scale(multiply(k, eta), 7))
    j_rhs = multiply(eta, add(constant(30), scale(k, -1),
                  multiply(add(constant(-144), scale(k, 8)), eta),
                  scale(power(eta, 2), 72)))
    identity(rows, "leading lower-bound polynomial cleared by 9a^3", j_lhs, j_rhs)
    # Optional context: exact limiting trace in the credited six-plus-two branch.
    uu, hh, rr = variable(0), variable(1), variable(2)
    xx = scale(add(uu, multiply(rr, hh)), F(1, 8))
    yy = add(xx, scale(multiply(rr, hh), F(-1, 2)))
    identity(rows, "optional credited branch limiting trace", uu,
             add(scale(xx, 6), scale(yy, 2)))
    return rows


def core(changes=None):
    changes = changes or {}
    identities = finite_identities(changes)
    margins = []
    k = 8
    l = F(changes.get("original_radius", 16))
    b0 = F(changes.get("normal_error", 1728))
    trace = F(changes.get("trace_loss", 108))
    q = F(changes.get("second_trace_cap", 13))
    phi = (1 + l*E)**7
    amin = 1-E
    margin(margins, "nine original circles are disjoint", F(4, 9), 2*l*E)
    margin(margins, "original-root Rouche strict difference",
           9*l-9-16*k, (36*l*l+36*k*l)*phi*E)
    normal = (4*l*l+4*k*l)*phi+l*l/2+4+4*k
    margin(margins, "full paired half-normal error", b0, normal)
    margin(margins, "marked root lies within its circle", l, 1)
    margin(margins, "critical Rouche bound at one third", F(1, 729), F(9*k, 4)*E)
    margin(margins, "critical reciprocal denominators positive", amin, F(1, 3))
    s1cap = F(8*k, 9)
    margin(margins, "Re second trace cap", q, s1cap*s1cap*E+F(14*k, 9))
    denominator = 9-(72+36*k)*E
    margin(margins, "marked analytic trace denominator", denominator)
    margin(margins, "marked analytic trace loss", trace, 120*k/(amin*denominator))
    margin(margins, "reciprocal imaginary-energy factor", F(27, 128), F(1, 5))
    coarse = F(1130)
    margin(margins, "initial sublevel energy", coarse, 30+10*trace+q, strict=False)
    margin(margins, "higher-coefficient square-root energy range", F(4, 225), coarse*E)
    # The nonnegative Maclaurin bounds in the text, with sqrt(H)<2/15,
    # and sqrt(8)>2 in the two odd cases.
    rc_components = {
        "c5": F(9, 5)*comb(8, 4)/8**2,
        "c4": F(9, 4)*comb(8, 5)*F(2, 15)/(8**2*2),
        "c2": F(9, 2)*comb(8, 7)*F(2, 15)**3/(8**3*2),
        "c1": F(9)*comb(8, 8)*F(2, 15)**4/8**4,
    }
    need(rc_components == {"c5": F(63, 32), "c4": F(21, 160),
                           "c2": F(1, 12000), "c1": F(1, 1440000)},
         "identity: higher-coefficient factors")
    rc_cap = F(changes.get("higher_coefficient_cap", F(9, 4)))
    margin(margins, "all retained higher coefficients", rc_cap, sum(rc_components.values()))
    n_actual = F(28, 3)*b0+s1cap**2
    margin(margins, "paired second-trace eta squared cap", 16180, n_actual)
    margin(margins, "real-trace objective coefficient positive", amin, F(7, 8))
    objective_n = F(changes.get("objective_eta_squared", 8100))
    margin(margins, "objective eta squared loss", objective_n, F(16180)/(2*amin**3))
    remainder = F(7)/(4*amin**3)+F(9)/(4*amin**5)+1/(amin**5*(1-1/(3*amin)))
    margin(margins, "entire cubic and all-orders objective energy loss", 6, remainder)
    jlower = F(12, 5)
    margin(margins, "uniform leading objective slope", F(30-k, 9)-(16-F(8*k, 9))*E, jlower)
    margin(margins, "original-normal energy eta coefficient", 22, F(28, 3)+F(14*k, 9))
    margin(margins, "original-normal energy eta squared coefficient", 16200, n_actual)
    margin(margins, "original-normal energy squared coefficient", 4, F(7, 2))
    b = F(changes.get("bootstrap_linear_cap", 29))
    boot_linear = 22+8*(3-jlower)
    boot_quadratic = 16200+8*objective_n
    need(boot_linear == F(134, 5) and boot_quadratic == 81000,
         "identity: sublevel bootstrap coefficients")
    need(4+8*6 == 52, "identity: quadratic self-improvement factor")
    margin(margins, "finite-bootstrap linear error absorption", b, boot_linear+boot_quadratic*E)
    previous = coarse
    endpoints = [288, 38, changes.get("final_energy_cap", 30)]
    for step, next_cap in enumerate(endpoints, 1):
        divisor = 1-52*previous*E
        margin(margins, "bootstrap divisor " + str(step), divisor)
        margin(margins, "bootstrap substitution " + str(step), next_cap*divisor, b)
        previous = F(next_cap)
    margin(margins, "strict first-power chamber slope", jlower-(objective_n+6*previous**2)*E, 2)
    # Context only: the old theorem covers a cube of radius 1/1024 about
    # its true algebraic limiting tuple, not an approximately rounded tuple.
    cl, cu, radius = F(15, 16), F(31, 32), F(1, 1024)
    cubic = lambda c: 8*c**3-6*c-1
    margin(margins, "optional branch cubic left sign", -cubic(cl))
    margin(margins, "optional branch cubic right sign", cubic(cu))
    margin(margins, "optional branch embedding monotone", 24*cl**2-6)
    hlow, hhigh = 14/(3*(1+cu)), 14/(3*(1+cl))
    ulow, uhigh = -8*(F(2, 3)-1/(3*(1+cu))), -8*(F(2, 3)-1/(3*(1+cl)))
    rlow, rhigh = (cl-5)/3, (cu-5)/3
    phlow, phhigh = rlow*hhigh, rhigh*hlow
    xlow, xhigh = (ulow+phlow)/8, (uhigh+phhigh)/8
    ylow, yhigh = xlow-phhigh/2, xhigh-phlow/2
    margin(margins, "optional branch c8 upper trace direction", ulow-8*radius, -4)
    margin(margins, "optional branch c8 lower trace direction", F(-32, 9), uhigh+8*radius)
    margin(margins, "optional branch x absolute box", F(9, 8), max(abs(xlow),abs(xhigh))+radius)
    margin(margins, "optional branch y absolute box", F(9, 8), max(abs(ylow),abs(yhigh))+radius)
    margin(margins, "optional branch T absolute box", F(25, 16), hhigh/2+radius)
    branch = {}
    for m in range(2, 9):
        choose = lambda n: comb(6, n) if 0 <= n <= 6 else 0
        majorant = (choose(m)*E**(m-1)*F(9, 8)**m
                    +2*choose(m-1)*E**(m-1)*F(9, 8)**m
                    +choose(m-2)*(F(25, 16)*E**(m-2)*F(9, 8)**(m-2)
                                  +E**(m-1)*F(9, 8)**m))
        bound = F(9, 9-m)*majorant
        branch[str(9-m)] = str(bound)
        margin(margins, "optional credited branch c" + str(9-m) + " over eta", 3, bound)
    margin(margins, "optional branch c8 chamber inclusion", 8, F(9, 2))
    return {"schema": "sendov-effective-K8-chamber-exact-v1", "eta_endpoint": str(E),
            "core_claim": "actual disk-rooted anchored K8: F>8+2eta; F<=8+3eta implies H<30eta",
            "identities": identities, "whole_domain_margins": margins,
            "higher_coefficient_factors": {k: str(v) for k, v in rc_components.items()},
            "optional_branch_coefficient_over_eta_bounds": branch,
            "ordinary_unformalized_bridges": ["Rouche root counting and labels",
                 "Taylor and actual disk half-normals", "complex trace and positivity",
                 "nonnegative Maclaurin", "Legendre full infinite tail",
                 "Cauchy and Young", "positive-divisor finite self-improvement"]}


DAMAGES = (
    ("wrong derivative factor", {"derivative_factor": 8}),
    ("wrong Newton second trace", {"newton_factor": F(13, 9)}),
    ("retain the canceled c6", {"c6_pair_weight": F(-3, 2)}),
    ("wrong reciprocal cubic", {"cubic_coefficient": F(4, 3)}),
    ("too small original circle", {"original_radius": 15}),
    ("too small normal remainder", {"normal_error": 1600}),
    ("too small trace loss", {"trace_loss": 100}),
    ("too small second trace cap", {"second_trace_cap": 12}),
    ("discard higher-coefficient loss", {"higher_coefficient_cap": 2}),
    ("too small objective eta squared loss", {"objective_eta_squared": 8000}),
    ("too small bootstrap linear cap", {"bootstrap_linear_cap": 27}),
    ("invalid final energy substitution", {"final_energy_cap": 28}),
)


def build_record():
    result = core()
    controls = []
    for name, damage in DAMAGES:
        try:
            core(damage)
        except CertificateError as exc:
            controls.append({"damage": name, "rejected_by": str(exc)})
        else:
            raise CertificateError("semantic damage unexpectedly accepted: " + name)
    result["mathematical_damage_controls"] = controls
    return result
