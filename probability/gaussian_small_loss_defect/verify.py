#!/usr/bin/env python3
"""Exact author controls; no numerical integration or analytic formalization."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import subprocess
import sys

from certificate import (need, ceil_log2, floor_log2, annular_schedule,
                         normalized_schedule, relative_schedule, finite_guard)

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def digest(value):
    return hashlib.sha256(json.dumps(encode(value), sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def pow2(n):
    return F(2**n) if n >= 0 else F(1, 2**(-n))


def rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError("negative control was accepted")


def check_pins():
    pins = json.loads((ROOT/"INPUTS.json").read_text())["files"]
    for pin in pins:
        local = REPO/pin["path"]
        data = local.read_bytes() if local.exists() else b""
        if hashlib.sha256(data).hexdigest() != pin["sha256"]:
            data = subprocess.check_output(
                ["git", "-C", str(REPO), "show", pin["commit"]+":"+pin["path"]])
        need(hashlib.sha256(data).hexdigest() == pin["sha256"],
             "versioned dependency mismatch: "+pin["path"])
    return len(pins)


def reference_budgets(R, k, W, A, K0, L, K1, K2):
    c = W*W/16
    delta = c/(4*K1)
    bounds = [
        k*k/(4*R*R*K0), delta**2/(2*K0), k*delta**2/(8*R*R*K0),
        W**4*k*k*delta**2/(144*R**4*K0), 2*k*delta/R,
        c*delta**4/(8*A*L*L*K0*K0),
        c*c*delta**4/(64*K2*K2*K0**3)]
    return c, delta, bounds


def assembly(R, k, W, A, K0, L, K1, K2, d):
    c, delta, bounds = reference_budgets(R, k, W, A, K0, L, K1, K2)
    need(K0 >= 2*R*R/k and L >= 96*R**3/k+6*R, "alignment constants")
    need(K1 >= 16*A*R/k and K2 >= 2*R/W**2, "error coefficients")
    need(0 < d <= min(bounds), "insufficient loss cutoff")
    M, alpha = K0*d, K0*d/delta**2
    need(R*R*M <= k*k/4, "cross-covariance budget")
    need(alpha <= F(1, 2) and alpha <= k/(8*R*R), "conditional covariance")
    need(M <= W**4*k*k*delta**2/(144*R**4), "rare half-space budget")
    need(d <= 2*k*delta/R, "one-label loss budget")
    need(K1*delta == c/4, "core linear term")
    need(A*L*L*alpha*alpha <= c*d/8, "core quadratic term")
    need(K2*K2*alpha*alpha*M <= (c*d/8)**2, "cross square-root term")
    # Check pair multiplicities, rather than suppressing the cross term.
    need(W*W/4 >= c and W*W/8 >= 2*c and W*W/8 >= c,
         "GG/GJ/JJ favorable coefficients")
    return bounds


class Mono:
    """A Laurent monomial with exact coefficient and formal exponents."""
    def __init__(self, coefficient=1, **powers):
        self.coefficient = F(coefficient)
        self.powers = {k: F(v) for k, v in powers.items() if v}

    def __mul__(self, other):
        if not isinstance(other, Mono):
            other = Mono(other)
        powers = self.powers.copy()
        for k, v in other.powers.items():
            powers[k] = powers.get(k, F(0))+v
        return Mono(self.coefficient*other.coefficient, **powers)

    __rmul__ = __mul__

    def __pow__(self, n):
        return Mono(self.coefficient**n,
                    **{k: n*v for k, v in self.powers.items()})

    def __truediv__(self, other):
        if not isinstance(other, Mono):
            other = Mono(other)
        return self*other**-1

    def __rtruediv__(self, other):
        return Mono(other)*self**-1

    def equal(self, other):
        return (self.coefficient == other.coefficient
                and self.powers == other.powers)


def exponential_table():
    # T=exp(-Rm), U=exp(-R^2); all other letters are independent variables.
    R, k, K0, L, J = [Mono(**{n: 1}) for n in ["R", "k", "K0", "L", "J"]]
    W, A = Mono(1, T=2, U=F(5, 2)), Mono(64, T=-3)
    K1, K2 = 16*A*R/k, 2*R/W**2
    c, delta, actual = reference_budgets(R, k, W, A, K0, L, K1, K2)
    # reference_budgets derives J=2^16 R/k; substitute it into target table.
    J = 2**16*R/k
    need(delta.equal(J**-1*Mono(1, T=7, U=5)), "derived delta")
    coefficients = [
        k*k/(4*R*R*K0), 1/(2*K0*J**2),
        k/(8*R*R*K0*J**2), k*k/(144*R**4*K0*J**2),
        2*k/(R*J), 1/(8192*L**2*K0**2*J**4),
        1/(65536*R**2*K0**3*J**4)]
    pairs = [(0, 0), (14, 10), (14, 10), (22, 20),
             (7, 5), (35, 25), (44, 40)]
    for x, a, (t, u) in zip(actual, coefficients, pairs):
        need(x.equal(a*Mono(1, T=t, U=u)), "formal exponential coefficient")
        need(t <= 44 and u <= 40, "uniform exponential envelope")
    return pairs


def integral_identities():
    # Laurent polynomial q^3+4q: d(P exp(-q^2/2))/dq
    # equals -(q^4+q^2-4)exp(-q^2/2), leaving 4 I0.
    P = {3: F(1), 1: F(4)}
    derivative_minus_q = {}
    for degree, coefficient in P.items():
        derivative_minus_q[degree-1] = derivative_minus_q.get(degree-1, F(0))+degree*coefficient
        derivative_minus_q[degree+1] = derivative_minus_q.get(degree+1, F(0))-coefficient
    need(derivative_minus_q == {2: F(-1), 4: F(-1), 0: F(4)},
         "Hessian tail integration-by-parts identity")
    need(F(36)*F(3, 4)*(F(5, 4)**3) == F(3375, 64) < 64,
         "tail integral divided by top-set volume")
    # Expand (v+2R)^2 before integrating against exp(-v^2/4).
    # I0=sqrt(pi), I1=2, I2=2sqrt(pi).
    R = Mono(1, R=1)
    volume = F(8, 3)
    need(volume == F(2**3, 3), "inner ball integral coefficient")
    need((2*(2*R)*2).equal(8*R), "tail linear-radius coefficient")
    need(((2*R)**2).equal(4*R**2), "tail quadratic-radius coefficient")
    return 4


def family(alpha):
    # Previously published R6 geometry, used only as a guard calibration.
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    xs = [tuple(F(a, 80) for a in z) for z in v]
    xs += [tuple(-F(a, 4) for a in z) for z in v]
    ys = xs[:4]+[tuple(F(29*a, 120) for a in z) for z in v]
    core = [F(1, 8), F(1, 4), F(1, 4), F(3, 8)]
    outer = [F(1, 2), F(1, 4), F(1, 8), F(1, 8)]
    p = [(1-alpha)*w for w in core]+[alpha*w for w in outer]
    return xs, ys, p


def run():
    pins = check_pins()
    logarithm_controls = 0
    for p, q in product(range(1, 40), range(1, 31)):
        x = F(p, q)
        lo, hi = floor_log2(x), ceil_log2(x)
        need(pow2(lo) <= x < pow2(lo+1), "floor log2")
        need(pow2(hi-1) < x <= pow2(hi), "ceil log2")
        logarithm_controls += 1
    # Elementary analytic constants: e<3 follows from n!>=2^(n-1),
    # strict for n>=3. log2>2/3 follows from 2 artanh(1/3)'s positive series.
    need(F(1)+F(3, 4)+F(3, 4)**2/2 > 2, "log2<3/4")
    need(6*F(2, 3) > F(25, 8), "upper and annular windows overlap")
    need(F(245, 36) < 7 and F(64, 27) < 3, "modulus exponential budget")
    need(F(25, 9) < 3 and F(44, 7) < F(64, 9), "pi square-root bounds")
    Kcap = F(1, 4)*3*3**7*F(256, 9)*F(196, 9)
    need(Kcap == 1016064 < 2**20, "loss modulus dyadic cap")

    rows = []
    for R, ratio, add in product([F(1, 4), F(1, 2), F(1), F(2)],
                                 [16, 64], [0, 3, 7]):
        k = R*R/ratio
        m = max(5*R, 3*R+1)+add
        s = annular_schedule(R, k, m)
        W, A = pow2(-s["omega"]), pow2(s["A_exponent"])
        K0, L, K1, K2 = [pow2(s[n+"_exponent"]) for n in ("K0", "L", "K1", "K2")]
        need(s["omega"] >= 4*R*m+5*R*R, "posterior exponential floor")
        need(s["A_exponent"] >= 6+6*R*m, "Hessian exponential ceiling")
        bounds = assembly(R, k, W, A, K0, L, K1, K2, pow2(-s["loss_bits"]))
        for N, bound in zip(s["budget_exponents"], bounds):
            need(pow2(-N) <= bound, "compressed/direct budget comparison")
        rows.append([R, k, m, s["loss_bits"]])
    normalized = []
    for m in [4, 5, 8, 13, 16, 22, 29, 56, 100]:
        s = normalized_schedule(m)
        R, k = F(1, 2), F(1, 2**15)
        bounds = assembly(R, k, pow2(-(2*m+2)), pow2(3*m+6), pow2(14),
                          pow2(19), pow2(3*m+24), pow2(4*m+4),
                          pow2(-s["loss_bits"]))
        for n, bound in zip(s["budget_exponents"], bounds):
            need(pow2(-n) <= bound, "normalized dyadic cutoff")
        need(s["loss_bits"] >= 360, "fixed upper-window join")
        normalized.append([m, s["loss_bits"]])
    # A universal linear inequality check, not only the preceding samples.
    for slope, constant in [(0, 44), (14, 83), (14, 98), (22, 124),
                            (7, 47), (35, 219), (44, 208)]:
        need(44-slope >= 0 and (44-slope)*3+208-constant >= 0,
             "last budget dominates for every integer m>=3")
    exponents = exponential_table()
    integrals = integral_identities()

    table, finite = [], []
    for b in [0, 32, 64, 128, 256, 1024]:
        s = relative_schedule(b)
        m, N = s["m"], s["loss_bits"]
        need(m*m >= 3*(b+20) and (m-1)**2 < 3*(b+20),
             "minimal relative-error schedule")
        table.append([b, m, N])
        data = family(pow2(-N-3))
        result = finite_guard(*data, b)
        need(result["status"] == "CONTROLLED_DEFECT", "finite nonzero-loss guard")
        need(result["relative_defect_bits"] == b and result["d"] > 0, "defect output")
        finite.append(result)
    need(table == [[0,8,560],[32,13,780],[64,16,912],[128,22,1176],
                   [256,29,1484],[1024,56,2672]], "published table")
    huge = relative_schedule(10**200)
    need(huge["m"]**2 >= 3*(10**200+20)
         and huge["loss_bits"] == 44*huge["m"]+208, "compressed huge-bit input")

    xs, ys, p = family(pow2(-915))
    expected = finite_guard(xs, ys, p, 64)
    for scale in [1, 2, 3]:
        xx = [tuple(scale*x[(j+1)%3]+[2,-3,1][j] for j in range(3)) for x in xs]
        yy = [tuple(scale*y[(j+1)%3]+[-1,4,2][j] for j in range(3)) for y in ys]
        need(finite_guard(xx, yy, p, 64, F(scale*scale)) == expected,
             "independent translations, rotation, variance scaling")
    # Discard zero-mass outliers before checking support contraction.
    need(finite_guard(xs+[(100,0,0)], ys+[(-1000,0,0)], p+[F(0)], 64)
         == expected, "zero-weight label")
    flat = [(F(-1, 8), F(0), F(0)), (F(1, 8), F(0), F(0))]
    moved = [tuple((1-pow2(-1000))*x for x in z) for z in flat]
    need(finite_guard(flat, moved, [F(1, 2)]*2, 64)["reason"] == "covariance",
         "covariance collapse unresolved")
    need(finite_guard(flat, flat, [F(1, 2)]*2, 64)["status"] == "ZERO_LOSS",
         "singular zero-loss equality")
    need(finite_guard(*family(F(1, 100)), 64)["reason"] == "loss",
         "positive-loss complement unresolved")
    need(finite_guard([tuple(100*z for z in x) for x in xs],
                      [tuple(100*z for z in y) for y in ys], p, 64)["reason"] == "radius",
         "large radius unresolved")
    bad = 0
    for call in [
        lambda: relative_schedule(-1), lambda: relative_schedule(1.0),
        lambda: normalized_schedule(3), lambda: annular_schedule(0, F(1, 8), 4),
        lambda: annular_schedule(F(1, 2), F(1, 8), 2),
        lambda: floor_log2(0), lambda: ceil_log2(-1),
        lambda: finite_guard(xs[:-1], ys, p, 64),
        lambda: finite_guard(xs, ys, [F(-1)]+p[1:], 64),
        lambda: finite_guard(xs, ys, p, 64, F(0)),
        lambda: finite_guard(xs, ys, p, 64, 1.0),
        lambda: finite_guard(xs, [tuple(2*z for z in x) for x in xs], p, 64),
    ]:
        bad += rejected(call)
    return {"status": "SMALL_LOSS_DEFECT_PASS",
            "scope": "Exact author controls only; analytic theorem unformalized and pending independent review.",
            "versioned_input_pins": pins, "logarithm_controls": logarithm_controls,
            "general_schedules": rows, "normalized_schedules": normalized,
            "formal_exponential_table": exponents, "radial_integral_controls": integrals,
            "modulus_upper_bound": Kcap, "relative_error_table": table,
            "finite_geometry_controls": len(finite), "finite_results_sha256": digest(finite),
            "variance_scalings": 3, "zero_weight_control": 1,
            "singular_zero_loss_control": 1, "unresolved_controls": 3,
            "invalid_input_rejections": bad, "compressed_bit_input": "10^200",
            "degree_two_guard_pair_bound": 19}


def main():
    record = (json.dumps(encode(run()), sort_keys=True, indent=2)+"\n").encode()
    expected = ROOT/"EXPECTED.json"
    if sys.argv[1:] == ["--write-expected"]:
        need(not expected.exists(), "refusing to replace expected record")
        expected.write_bytes(record)
    else:
        need(not sys.argv[1:], "usage: verify.py [--write-expected]")
        need(expected.read_bytes() == record, "expected record mismatch")
        for line in (ROOT/"SHA256SUMS").read_text().splitlines():
            sha, name = line.split(maxsplit=1)
            need(Path(name).name == name, "local manifest paths only")
            need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == sha,
                 "packet manifest mismatch: "+name)
    print("SMALL_LOSS_DEFECT_PASS")
    print("record_sha256="+hashlib.sha256(record).hexdigest())


if __name__ == "__main__":
    main()
