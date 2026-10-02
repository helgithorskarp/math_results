#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; ordinary analysis is not formalized."""
import argparse
import hashlib
import json
import math
import os
from fractions import Fraction as Q
from pathlib import Path

for _thread_name in (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "BLIS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
):
    os.environ[_thread_name] = "1"


class Invalid(ValueError):
    pass


def need(predicate, message):
    if not predicate:
        raise Invalid(message)


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def atom(n, i=None, coefficient=1):
    m = [0] * n
    if i is not None:
        m[i] = 1
    return {tuple(m): Q(coefficient)} if coefficient else {}


def add(*polys):
    out = {}
    for p in polys:
        for m, v in p.items():
            out[m] = out.get(m, Q(0)) + v
    return {m: v for m, v in out.items() if v}


def scale(p, c):
    return {m: v * c for m, v in p.items() if v * c}


def mul(p, q):
    out = {}
    for m, v in p.items():
        for n, w in q.items():
            mn = tuple(a + b for a, b in zip(m, n))
            out[mn] = out.get(mn, Q(0)) + v * w
    return {m: v for m, v in out.items() if v}


def power(p, k, dimension):
    out = atom(dimension)
    for _ in range(k):
        out = mul(out, p)
    return out


def derivative(p, index):
    out = {}
    for m, v in p.items():
        if m[index]:
            n = list(m)
            n[index] -= 1
            out[tuple(n)] = v * m[index]
    return out


def encode_poly(p):
    return [[list(m), str(v)] for m, v in sorted(p.items())]


def identity(name, lhs, rhs, retain=False):
    need(lhs == rhs, "complete polynomial mismatch: " + name)
    r = {"name": name, "terms": len(lhs), "matched": True,
         "complete_polynomial_sha256": hashlib.sha256(canonical(encode_poly(lhs))).hexdigest()}
    if retain:
        r["polynomial"] = encode_poly(lhs)
    return r


def identities():
    result = []
    # An independent differentiated general coefficient polynomial.
    n = 10
    z = atom(n, 9)
    p = power(z, 9, n)
    for k in range(9):
        p = add(p, mul(atom(n, k), power(z, k, n)))
    direct = scale(power(z, 8, n), 9)
    for k in range(1, 9):
        direct = add(direct, scale(mul(atom(n, k), power(z, k - 1, n)), k))
    result.append(identity("whole_general_derivative", derivative(p, 9), direct, True))

    # Full critical product and its anchored primitive, at free criticals.
    n = 10
    z, a = atom(n, 8), atom(n, 9)
    h = atom(n)
    for j in range(8):
        h = mul(h, add(z, scale(atom(n, j), -1)))
    primitive = {}
    for m, v in h.items():
        k = m[8] + 1
        upper = list(m)
        upper[8] = k
        anchor = list(m)
        anchor[8] = 0
        anchor[9] += k
        primitive = add(primitive, {tuple(upper): 9 * v / k}, {tuple(anchor): -9 * v / k})
    result.append(identity("whole_anchored_critical_derivative", derivative(primitive, 8), scale(h, 9)))
    at_anchor = {}
    for m, v in primitive.items():
        t = list(m)
        t[9] += t[8]
        t[8] = 0
        at_anchor = add(at_anchor, {tuple(t): v})
    result.append(identity("whole_anchor_vanishes", at_anchor, {}, True))
    prod = atom(n)
    for j in range(8):
        prod = mul(prod, atom(n, j))
    constant_h = {m: v for m, v in h.items() if m[8] == 0}
    result.append(identity("critical_product_constant_sign", constant_h, prod, True))
    for k in range(1, 9):
        ck = {}
        hk = {}
        for m, v in primitive.items():
            if m[8] == k:
                t = list(m); t[8] = 0
                ck[tuple(t)] = v
        for m, v in h.items():
            if m[8] == k - 1:
                t = list(m); t[8] = 0
                hk[tuple(t)] = v
        result.append(identity("whole_Vieta_c" + str(k), scale(ck, Q(k, 9)), hk))

    # Cyclotomic marked motion and radial motion, with free variables.
    n = 4
    z, a, r, eta = [atom(n, j) for j in range(4)]
    one = atom(n)
    geom = add(*[power(z, k, n) for k in range(9)])
    pa = mul(add(z, scale(add(one, scale(eta, -1)), -1)), geom)
    expected = add(power(z, 9, n), scale(one, -1), mul(eta, geom))
    result.append(identity("whole_cyclotomic_marked_motion", pa, expected, True))
    radial = add(*[mul(power(r, 8 - k, n), power(z, k, n)) for k in range(9)])
    result.append(identity("whole_radial_geometric_product", mul(add(z, scale(r, -1)), radial),
                           add(power(z, 9, n), scale(power(r, 9, n), -1))))
    radial_p = mul(add(z, scale(a, -1)), radial)
    radial_coefficients = scale(mul(a, power(r, 8, n)), -1)
    for k in range(1, 9):
        radial_coefficients = add(radial_coefficients,
            mul(mul(power(r, 8 - k, n), add(r, scale(a, -1))), power(z, k, n)))
    radial_coefficients = add(radial_coefficients, power(z, 9, n))
    result.append(identity("whole_radial_coefficients", radial_p, radial_coefficients))
    # Finite geometric derivative and its exact remainder.
    n = 1
    t, one = atom(n, 0), atom(n)
    finite = add(*[scale(power(t, k - 1, n), k) for k in range(1, 9)])
    result.append(identity("finite_geometric_derivative_remainder",
        mul(power(add(one, scale(t, -1)), 2, n), finite),
        add(one, scale(power(t, 8, n), -9), scale(power(t, 9, n), 8)), True))

    # Generic Newton power sums versus independently formed log coefficients.
    # a_j is the coefficient of z^(8-j) in p'/9, c-variable order c1,...,c8.
    n = 8
    ac = {j: scale(atom(n, 8 - j), Q(9 - j, 9)) for j in range(1, 9)}
    newton = {}
    for m in range(1, 13):
        pieces = [mul(ac[j], newton[m-j]) for j in range(1, min(m, 9))]
        if m <= 8:
            pieces.append(scale(ac[m], m))
        newton[m] = scale(add(*pieces), -1)
    base = ac
    current = {0: atom(n)}
    logarithm = {m: {} for m in range(1, 13)}
    for k in range(1, 13):
        next_power = {}
        for i, pp in current.items():
            for j, qq in base.items():
                if i + j <= 12:
                    next_power[i+j] = add(next_power.get(i+j, {}), mul(pp, qq))
        current = next_power
        for m, pp in current.items():
            logarithm[m] = add(logarithm[m], scale(pp, Q((-1)**(k+1), k)))
    for m in range(1, 13):
        result.append(identity("complete_Newton_log_trace_" + str(m), newton[m],
                               scale(logarithm[m], -m), True))
    return result


DEFAULT = {
    "eta_max": Q(1, 65536), "coefficient_factor": Q(2),
    "inner": Q(1, 4), "outer": Q(5, 8), "a_floor": Q(255, 256),
    "sqrt_cap": Q(9, 8), "derivative_cap": Q(9, 4),
    "beta_cap": Q(1, 900), "trace_cap": Q(96),
    "coercivity": Q(1, 6), "penalty": Q(193), "branch_slope": Q(3),
    "ball_ratio": Q(7, 8), "gap_factor": Q(1),
    "radial_tau_factor": Q(1, 16),
    "branch_c8_floor": Q(4), "entry_c8_cap": Q(16, 499),
}


def budget_record(overrides=None):
    b = dict(DEFAULT)
    b.update(overrides or {})
    need(all(isinstance(v, Q) for v in b.values()), "non-rational budget")
    e, cf, r, R, af = [b[k] for k in ("eta_max", "coefficient_factor", "inner", "outer", "a_floor")]
    need(0 < e < 1 and 0 < r < R < af < 1, "invalid contour/eta ordering")
    need(0 < b["beta_cap"] < 1 and 0 <= b["ball_ratio"] < 1, "invalid logarithm/ball domain")
    need(b["coercivity"] > 0 and b["gap_factor"] > 0, "invalid positivity budget")
    B = cf / (9 * R**8 * (1-R)**2)
    D = (R/af) * b["derivative_cap"] * B / (1-b["beta_cap"])
    gain = 8 * b["coercivity"]
    available = gain - b["gap_factor"]
    need(available > 0, "no absorption gain")
    comparator_penalty = b["penalty"] + b["branch_slope"]
    threshold = comparator_penalty / available
    Hcap = comparator_penalty / b["coercivity"]
    per_critical = Hcap / 8
    margins = {
        "root_Rouche": 9*r**8 - cf*e/(1-r)**2,
        "a_floor": 1-e-af,
        "root_square_modulus": b["sqrt_cap"]**2 - (1+r/af),
        "square_energy": 1/(b["sqrt_cap"]**2*(1+b["sqrt_cap"])**2) - b["coercivity"],
        "outer_derivative": 4*b["derivative_cap"]**2*(1-R/af)**3-1,
        "logarithm_disk": b["beta_cap"]-B*e,
        "trace_uniform": b["trace_cap"]-D,
        "objective_uniform": b["penalty"]-2*b["trace_cap"]/af,
        "ball_coefficient_chamber": cf-(1+b["ball_ratio"]),
        "ball_positive_c1": 1-b["ball_ratio"],
        "quarter_power_absorption": 1-threshold**4*9*e**3/(1-b["ball_ratio"]),
        "marked_family_absorption": 1-threshold**4*9*e**3,
        "radial_constant_entry": b["ball_ratio"]-8*b["radial_tau_factor"],
        "radial_other_entry": b["ball_ratio"]-(1+7*e)*b["radial_tau_factor"],
        "radial_positive_r": 1-e*b["radial_tau_factor"],
        "antipodal_c8_separation": 7-b["ball_ratio"]*e-b["entry_c8_cap"],
        "branch_c8_separation": b["branch_c8_floor"]-(1+b["ball_ratio"])-1,
        "branch_initial_c8": Q(30,7)-Q(9,1024)-b["branch_c8_floor"],
        "branch_radius_div_eta": 1-Q(1,2)**2005*e**12,
        "radial_nonconstant_bound_eta8": Q(1,8)-(1+7*e)*b["radial_tau_factor"],
    }
    for name, value in margins.items():
        need(value > 0, "nonpositive mathematical margin: " + name)
    hierarchy = []
    for k in range(1, 9):
        m = 9-k
        hierarchy.append({"coefficient": k, "critical_symmetric_degree": m,
                          "factor": str(Q(9,k)*math.comb(8,m)),
                          "eta_energy_factor": str(per_critical),
                          "power": str(Q(m,2))})
    return {"parameters": {k:str(v) for k,v in sorted(b.items())},
            "margins": {k:str(v) for k,v in sorted(margins.items())},
            "derived": {"log_argument_per_eta":str(B), "trace_per_eta":str(D),
                        "critical_energy_cap_per_eta":str(Hcap),
                        "per_critical_energy_cap":str(per_critical),
                        "c1_eta4_factor":str(9*per_critical**4),
                        "absorption_threshold":str(threshold),
                        "ball_quarter_power_denominator":str(9/(1-b["ball_ratio"]))},
            "coefficient_hierarchy": hierarchy}


def damaged_controls():
    damaged = {
        "larger_eta_breaks_Rouche": {"eta_max": Q(1,4096)},
        "large_coefficient_chamber_breaks_Rouche": {"coefficient_factor": Q(10)},
        "insufficient_critical_radius": {"inner": Q(1,8)},
        "outer_contour_trace_loss": {"outer": Q(1,2)},
        "invalid_small_log_disk": {"beta_cap": Q(1,2000)},
        "underestimated_square_root": {"sqrt_cap": Q(1)},
        "invalid_quarter_energy": {"coercivity": Q(1,4)},
        "underestimated_outer_derivative": {"derivative_cap": Q(2)},
        "underestimated_trace": {"trace_cap": Q(95)},
        "underestimated_objective_loss": {"penalty": Q(192)},
        "ball_allows_zero_c1": {"ball_ratio": Q(1)},
        "overclaimed_quarter_power_gap": {"gap_factor": Q(33,25)},
        "radial_motion_misses_ball": {"radial_tau_factor": Q(1,8)},
        "false_antipodal_radius": {"entry_c8_cap": Q(7)},
        "false_branch_coefficient_floor": {"branch_c8_floor": Q(5)},
    }
    result = []
    for name, changes in damaged.items():
        try:
            budget_record(changes)
        except Invalid as exc:
            result.append({"name":name, "changes":{k:str(v) for k,v in changes.items()},
                           "rejected":True, "mathematical_reason":str(exc)})
        else:
            raise Invalid("damaged mathematical budget accepted: " + name)
    return result


def build_record():
    return {"schema":1, "agent":"six-sendov-1", "role":"researcher",
            "proof_status":"ordinary analytic author proof; unformalized and independently unreviewed",
            "identities":identities(), "whole_domain_budgets":budget_record(),
            "mathematical_damages":damaged_controls(),
            "analytic_trust_boundary":["Rouche with multiplicity", "analytic square root",
                 "argument principle", "annular convergent logarithm", "contour integration by parts",
                 "Cauchy-Schwarz and Maclaurin", "AM-GM", "imported legal comparison9113",
                 "simple-root openness"]}


def strict_object(pairs):
    out = {}
    for k,v in pairs:
        need(k not in out, "duplicate fixture key: " + k)
        out[k] = v
    return out


def forbidden_number(s):
    raise Invalid("nonintegral/nonfinite fixture number: " + s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", type=Path, default=Path(__file__).with_name("EXPECTED.json"))
    ap.add_argument("--record", type=Path)
    args = ap.parse_args()
    actual = build_record()
    expected = json.loads(args.fixture.read_text(), object_pairs_hook=strict_object,
                          parse_float=forbidden_number, parse_constant=forbidden_number)
    need(canonical(expected)==canonical(actual), "whole regenerated record differs from fixture")
    if args.record:
        args.record.write_text(json.dumps(actual,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":"PASS", "identities":len(actual["identities"]),
                      "whole_domain_margins":len(actual["whole_domain_budgets"]["margins"]),
                      "mathematical_damage_rejections":len(actual["mathematical_damages"]),
                      "whole_record_sha256":hashlib.sha256(canonical(actual)).hexdigest()},sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit("FAIL: " + str(exc))
