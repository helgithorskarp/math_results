#!/usr/bin/env python3
"""Exact finite controls for the ordinary analytic chamber proof.

Standard library, characteristic zero, whole sparse polynomial comparison.
This does not formally verify complex analysis or imported analytic premises.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def const(value, n):
    value = Q(value)
    return {(0,) * n: value} if value else {}


def var(index, n):
    powers = [0] * n
    powers[index] = 1
    return {tuple(powers): Q(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(poly, value):
    return {key: coefficient * value for key, coefficient in poly.items()
            if coefficient * value}


def mul(left, right):
    out = {}
    for key, value in left.items():
        for other, coefficient in right.items():
            target = tuple(x + y for x, y in zip(key, other))
            out[target] = out.get(target, Q(0)) + value * coefficient
    return {key: value for key, value in out.items() if value}


def power(poly, exponent, n):
    out = const(1, n)
    for unused in range(exponent):
        out = mul(out, poly)
    return out


def coefficient(poly, index, degree):
    out = {}
    for key, value in poly.items():
        if key[index] == degree:
            target = list(key)
            target[index] = 0
            out[tuple(target)] = value
    return out


def derivative(poly, index):
    out = {}
    for key, value in poly.items():
        if key[index]:
            target = list(key)
            target[index] -= 1
            out[tuple(target)] = value * key[index]
    return out


def substitute(poly, index, replacement, n):
    out = {}
    for key, value in poly.items():
        target = list(key)
        degree = target[index]
        target[index] = 0
        out = add(out, mul({tuple(target): value}, power(replacement, degree, n)))
    return out


def encode(poly):
    return [[list(key), [value.numerator, value.denominator]]
            for key, value in sorted(poly.items())]


def rational(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def cyclic(poly):
    out = {}
    for (degree,), value in poly.items():
        target = (degree % 9,)
        out[target] = out.get(target, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def generic_identities():
    record = {}
    n = 9
    z = var(8, n)
    roots = [var(j, n) for j in range(8)]
    full = const(1, n)
    for root in roots:
        full = mul(full, add(z, scale(root, -1)))
    # Independent complete subset expansion, including every constant term.
    subset = {}
    for m in range(9):
        for chosen in combinations(range(8), m):
            key = [0] * n
            key[8] = 8 - m
            for j in chosen:
                key[j] = 1
            subset[tuple(key)] = Q((-1) ** m)
    require(full == subset, "complete generic factorization differs")
    record["generic_factorization"] = encode(full)
    primitive = {}
    for key, value in full.items():
        target = list(key)
        target[8] += 1
        primitive[tuple(target)] = value * Q(9, target[8])
    require(derivative(primitive, 8) == scale(full, 9), "complete monic primitive derivative")
    record["generic_derivative"] = encode(scale(full, 9))
    c8 = scale(coefficient(full, 8, 7), Q(9, 8))
    c7 = scale(coefficient(full, 8, 6), Q(9, 7))
    t1 = add(*roots)
    t2 = add(*(mul(root, root) for root in roots))
    require(t1 == scale(c8, Q(-8, 9)), "whole first Newton/Vieta identity")
    require(t2 == add(power(scale(c8, Q(8, 9)), 2, n),
                     scale(c7, Q(-14, 9))), "whole second Newton/Vieta identity")
    record["generic_T1"] = encode(t1)
    record["generic_T2"] = encode(t2)

    x, y = var(0, 2), var(1, 2)
    lhs = add(power(x, 2, 2), power(y, 2, 2))
    rhs = add(scale(x, 2), const(-1, 2),
              power(add(x, const(-1, 2)), 2, 2), power(y, 2, 2))
    require(lhs == rhs, "whole scalar square identity")
    record["scalar_square"] = encode(lhs)
    r = var(0, 1)
    denominator = mul(add(const(1, 1), r), add(const(4, 1), scale(r, 2)))
    slack = add(const(4, 1), scale(r, 8), scale(denominator, -1))
    require(slack == scale(mul(r, add(const(1, 1), scale(r, -1))), 2),
            "energy denominator domain polynomial")
    record["energy_denominator_slack"] = encode(slack)
    reciprocal_lhs = add(const(1, 1), scale(mul(
        add(const(1, 1), scale(r, -2)), add(const(1, 1), scale(r, 2))), -1))
    require(reciprocal_lhs == scale(power(r, 2, 1), 4), "energy reciprocal clearing")
    record["energy_reciprocal_slack"] = encode(reciprocal_lhs)

    # Binomial and independent differential recurrence controls, not an
    # infinite-series certificate. The all-index tail is an ordinary proof.
    closed = [Q(comb(2 * m, m), 4 ** m) for m in range(33)]
    recurrent = [Q(1)]
    for m in range(32):
        recurrent.append(recurrent[-1] * Q(2 * m + 1, 2 * m + 2))
    require(closed == recurrent, "whole finite binomial recurrence record")
    square = [sum((closed[j] * closed[m-j] for j in range(m+1)), Q(0))
              for m in range(33)]
    require(square == [Q(1)] * 33, "whole reciprocal square-series coefficients")
    record["finite_binomial_coefficients"] = [rational(x) for x in closed]
    record["finite_square_coefficients"] = [rational(x) for x in square]

    eta = var(0, 1)
    a = add(const(1, 1), scale(eta, -1))
    numerator = add(scale(power(a, 2, 1), 8),
                    scale(mul(add(const(8, 1), scale(eta, Q(14, 3))),
                              power(a, 3, 1)), -1),
                    scale(mul(eta, a), Q(-16, 9)),
                    scale(eta, Q(-14, 9)), scale(power(eta, 2, 1), Q(-128, 81)))
    target = mul(power(eta, 2, 1), add(
        const(Q(-146, 81), 1), scale(eta, -6),
        scale(power(eta, 2, 1), Q(14, 3))))
    require(numerator == target, "entire rational baseline numerator")
    record["baseline_numerator"] = encode(numerator)
    return record, (c8, c7, t1, t2)


def family_identities():
    record = {}
    eta, z = var(0, 2), var(1, 2)
    a = add(const(1, 2), scale(eta, -1))
    b = scale(eta, Q(2, 9))
    v = add(scale(eta, Q(7, 18)), scale(power(eta, 2, 2), Q(-28, 81)))
    q = add(power(z, 2, 2), scale(mul(eta, z), Q(4, 9)),
            scale(eta, Q(7, 18)), scale(power(eta, 2, 2), Q(-8, 27)))
    full = power(q, 4, 2)
    independent = {}
    shifted = add(z, b)
    for j in range(5):
        independent = add(independent, scale(mul(
            power(v, j, 2), power(shifted, 8-2*j, 2)), comb(4, j)))
    require(full == independent, "whole family critical polynomial")
    record["family_derivative"] = encode(scale(full, 9))
    primitive = {}
    for key, value in full.items():
        target = list(key)
        target[1] += 1
        primitive[tuple(target)] = value * Q(9, target[1])
    p = add(primitive, scale(substitute(primitive, 1, a, 2), -1))
    require(derivative(p, 1) == scale(full, 9), "whole anchored derivative")
    require(not substitute(p, 1, a, 2), "whole marked anchor")
    require(coefficient(p, 1, 8) == scale(eta, 2), "whole family c8")
    require(coefficient(p, 1, 7) == scale(eta, 2), "whole family c7 cancellation")
    record["family_polynomial"] = encode(p)
    record["family_c8"] = encode(coefficient(p, 1, 8))
    record["family_c7"] = encode(coefficient(p, 1, 7))
    jet = coefficient(p, 0, 1)
    expected_jet = add(scale(power(z, 8, 2), 2), scale(power(z, 7, 2), 2), const(5, 2))
    require(jet == expected_jet, "entire first family polynomial jet")
    record["family_first_jet"] = encode(jet)
    radius = add(power(add(a, b), 2, 2), v)
    target = add(const(1, 2), scale(eta, Q(-7, 6)),
                 scale(power(eta, 2, 2), Q(7, 27)))
    require(radius == target, "whole literal objective squared radius")
    record["objective_squared_radius"] = encode(radius)

    w = var(0, 1)
    psi = add(scale(power(w, 8, 1), 2), scale(power(w, 7, 1), 2), const(5, 1))
    root_jet = scale(cyclic(mul(psi, w)), Q(-1, 9))
    require(not cyclic(add(scale(mul(power(w, 8, 1), root_jet), 9), psi)),
            "entire original root jet modulo w9-1")
    companion = {}
    for (degree,), value in root_jet.items():
        companion[(8*degree % 9,)] = companion.get((8*degree % 9,), Q(0)) + value
    alpha = scale(cyclic(add(mul(power(w, 8, 1), root_jet),
                             mul(w, companion))), Q(1, 2))
    expected_alpha = add(const(Q(-5, 9), 1), scale(w, Q(-1, 9)),
                         scale(power(w, 8, 1), Q(-1, 9)),
                         scale(power(w, 2, 1), Q(-1, 9)),
                         scale(power(w, 7, 1), Q(-1, 9)))
    require(alpha == expected_alpha, "entire companion half-normal jet")
    require(sum(root_jet.values(), Q(0)) == -1, "marked original motion")
    require(sum(alpha.values(), Q(0)) == -1, "marked half-normal motion")
    record["original_root_jet_mod_w9"] = encode(root_jet)
    record["companion_half_normal_jet_mod_w9"] = encode(alpha)
    c = var(0, 1)
    real_normal = add(const(5, 1), scale(c, 2),
                      scale(add(scale(power(c, 2, 1), 2), const(-1, 1)), 2))
    completed = add(scale(power(add(c, const(Q(1, 4), 1)), 2, 1), 4),
                    const(Q(11, 4), 1))
    require(real_normal == completed, "whole normal square completion")
    record["normal_square_completion"] = encode(real_normal)
    objective_first_slope = -4 * sum(coefficient(radius, 0, 1).values(), Q(0))
    require(objective_first_slope == Q(14, 3), "objective first derivative")
    record["objective_first_slope"] = rational(objective_first_slope)
    return record, (p, a, eta, z, alpha, root_jet, w)


def budgets(*, sqrt_eta=Q(1, 256), critical_cutoff=Q(1, 6),
            cutoff_slope=Q(5), total_remainder=Q(147), rho=Q(1, 128),
            energy_base=Q(1, 4)):
    eta_cap = sqrt_eta ** 2
    alo, r, B = Q(255, 256), Q(1, 16), Q(2, 9)
    V = Q(7, 18) + Q(28, 81) * rho
    t, z = var(0, 2), var(1, 2)
    majorant = power(add(power(add(z, scale(t, B)), 2, 2), scale(t, V)), 4, 2)
    tail_bounds = {}
    for k in range(1, 7):
        terms = coefficient(majorant, 1, k-1)
        require(all(key[0] >= 2 for key in terms), "family tail lacks double zero")
        tail_bounds[k] = sum((value * Q(9, k) * rho ** (key[0]-2)
                              for key, value in terms.items()), Q(0))
    P = (9*(1+rho)**8 + 2*((1+r)**8+(1+rho)**8)
         + 2*((1+r)**7+(1+rho)**7)
         + 4*rho*sum(((1+r)**k+(1+rho)**k for k in range(1, 7)), Q(0)))
    margins = {
        "a_lower": 1-eta_cap-alo,
        "sqrt_H_35": 35**2-6*(193+cutoff_slope),
        "scaled_radius_36": 36-35/alo,
        "critical_radius_domain": critical_cutoff-36*sqrt_eta,
        "retained_energy": energy_base-Q(5,4)*critical_cutoff,
        "inverse_cube_33over32": Q(33,32)-alo**-3,
        "second_trace_25over8": Q(25,8)-Q(28,9)-Q(256,81)*eta_cap,
        "higher_trace_146": 146-Q(5,4)*Q(33,32)*Q(25,8)*36,
        "quadratic_base_2": 2-Q(33,32)*(Q(146,81)+6*eta_cap),
        "total_remainder": total_remainder-146-2*sqrt_eta,
        "large_objective_case": cutoff_slope-Q(14,3),
        "whole_chamber_slope_four": Q(14,3)-total_remainder*sqrt_eta-4,
        "family_v_positive": Q(7,18)-Q(28,81)*eta_cap,
        "family_objective_positive": 1-Q(7,6)*eta_cap,
        "family_coefficient_chamber": 2-4*eta_cap,
        "P_less21": 21-P,
        "baseline_circle_quarter": 9*r-36*(1+r)**7*r*r-Q(1,4),
        "perturb_circle_quarter": Q(1,4)-21*rho,
        "baseline_quotient5": 9-36*r*(1+r)**7-5,
        "companion_quotient6": 6-(5+Q(25,2)*rho),
        "original_normal_negative": Q(11,36)-6*(eta_cap/rho)/(1-eta_cap/rho),
        "original_disks_separate": Q(1,2)-2*r,
    }
    margins.update({"family_tail_"+str(k): 4-value for k, value in tail_bounds.items()})
    for name, value in margins.items():
        require(value > 0, "nonpositive strict margin: " + name)
    closed_tail = Q(3,4)*(1-critical_cutoff)-Q(5,8)
    require(closed_tail >= 0, "negative closed whole-tail budget")
    return {
        "sqrt_eta_cap": rational(sqrt_eta), "eta_cap": rational(eta_cap),
        "complex_eta_radius": rational(rho),
        "strict_margins": {k:rational(v) for k,v in sorted(margins.items())},
        "closed_tail_margin": rational(closed_tail),
        "family_tail_bounds": {str(k):rational(v) for k,v in tail_bounds.items()},
        "whole_anchored_majorant_P": rational(P),
    }


def regenerate():
    generic, (c8, c7, t1, t2) = generic_identities()
    family, (p, a, eta, z, alpha, root_jet, w) = family_identities()
    budget = budgets()
    rejected = []
    def reject_identity(name, wrong, correct):
        require(wrong != correct, "damaged identity was not detected: " + name)
        rejected.append(name)
    reject_identity("first_trace_sign", scale(c8, Q(8,9)), t1)
    reject_identity("second_trace_missing_square", scale(c7,Q(-14,9)), t2)
    reject_identity("second_trace_wrong_sign", add(power(scale(c8,Q(8,9)),2,9),
                    scale(c7,Q(14,9))), t2)
    reject_identity("anchor_wrong_marked_root",
                    substitute(p,1,add(const(1,2),scale(eta,-2)),2), {})
    # Actual normal uses the companion section at the reflected unit root.
    wrong_alpha = cyclic(mul(power(w, 8, 1), root_jet))
    reject_identity("companion_normal_omitted", encode(wrong_alpha), encode(alpha))
    configs = [
        ("critical_radius_quarter", {"critical_cutoff":Q(1,4)}),
        ("cutoff_without_energy_bootstrap", {"cutoff_slope":Q(1000)}),
        ("eta_cap_too_large", {"sqrt_eta":Q(1,64)}),
        ("understated_total_remainder", {"total_remainder":Q(100)}),
        ("oversized_complex_root_domain", {"rho":Q(1,16)}),
        ("positive_energy_removed", {"energy_base":Q(0)}),
    ]
    for name, config in configs:
        try:
            budgets(**config)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("damaged mathematical budget accepted: "+name)
    record = {
        "schema": 1, "domain": "Q sparse polynomials; all eight critical variables",
        "generic_identities": generic, "family_identities": family,
        "budgets": budget, "mathematical_damage_rejections": rejected,
        "analytic_bridges_formalized": False,
    }
    return record


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate fixture key: "+key)
        out[key] = value
    return out


def forbidden_number(value):
    raise ValueError("nonintegral or nonfinite fixture number: "+value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path,
                        default=Path(__file__).with_name("EXPECTED.json"))
    parser.add_argument("--emit", type=Path)
    args = parser.parse_args()
    actual = regenerate()
    if args.emit is not None:
        args.emit.write_text(canonical(actual)+"\n")
    else:
        expected = json.loads(args.fixture.read_text(), object_pairs_hook=no_duplicates,
                              parse_float=forbidden_number, parse_constant=forbidden_number)
        require(canonical(actual) == canonical(expected), "entire typed fixture differs")
    encoded = canonical(actual).encode()
    print(json.dumps({
        "status":"PASS",
        "whole_record_sha256":hashlib.sha256(encoded).hexdigest(),
        "complete_identity_records":len(actual["generic_identities"])+len(actual["family_identities"]),
        "strict_margins":len(actual["budgets"]["strict_margins"]),
        "mathematical_damage_rejections":len(actual["mathematical_damage_rejections"]),
        "analytic_bridges_formalized":False,
    },sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        sys.exit(1)
