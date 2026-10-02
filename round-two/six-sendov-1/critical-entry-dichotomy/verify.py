"""Finite exact controls for the ordinary analytic routing proof.

Author: six-sendov-1, researcher. Python 3.12, standard library only.
The analytic disk/homotopy/argument/Taylor bridges are in PROOF.md.
No theorem or certificate from another contribution is executed here.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


def constant(n, value=1):
    return {(0,) * n: Q(value)} if value else {}


def variable(n, i):
    exponent = [0] * n
    exponent[i] = 1
    return {tuple(exponent): Q(1)}


def plus(*polys):
    result = {}
    for poly in polys:
        for exponent, value in poly.items():
            result[exponent] = result.get(exponent, Q(0)) + value
    return {e: v for e, v in result.items() if v}


def times(left, right):
    result = {}
    for e, v in left.items():
        for f, w in right.items():
            exponent = tuple(a + b for a, b in zip(e, f, strict=True))
            result[exponent] = result.get(exponent, Q(0)) + v * w
    return {e: v for e, v in result.items() if v}


def scale(poly, value):
    return {e: v * Q(value) for e, v in poly.items() if v * Q(value)}


def power(poly, k):
    n = len(next(iter(poly)))
    result = constant(n)
    for _ in range(k):
        result = times(result, poly)
    return result


def product(polys, n):
    result = constant(n)
    for poly in polys:
        result = times(result, poly)
    return result


def derivative(poly, i):
    result = {}
    for exponent, value in poly.items():
        if exponent[i]:
            new = list(exponent)
            new[i] -= 1
            result[tuple(new)] = value * exponent[i]
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def polynomial_record(poly):
    terms = [[list(e), str(v)] for e, v in sorted(poly.items())]
    return {
        "complete_terms": len(terms),
        "complete_coefficient_sha256": hashlib.sha256(canonical(terms)).hexdigest(),
    }


def identity(records, name, left, right):
    if left != right:
        raise ValueError("polynomial identity failed: " + name)
    records[name] = polynomial_record(left)


def polynomial_controls(degree_coefficient, heavy_coefficient, imaginary_scaling_power):
    records = {}
    n = 10
    z = variable(n, 0)
    ell = variable(n, 1)
    roots = [variable(n, i) for i in range(2, 10)]
    g = product([plus(z, scale(u, -1)) for u in roots], n)
    chi = plus(scale(g, degree_coefficient), scale(times(z, derivative(g, 0)), -1))

    # Different construction: differentiate at the marked root, then invert.
    marked = times(z, product([plus(constant(n), times(z, u)) for u in roots], n))
    local_derivative = derivative(marked, 0)
    inverted = {}
    for exponent, value in local_derivative.items():
        new = list(exponent)
        new[0] = 8 - exponent[0]
        inverted[tuple(new)] = value * (-1) ** exponent[0]
    identity(records, "entire_reciprocal_derivative", chi, inverted)

    # Third construction: all 256 elementary-symmetric subset monomials.
    elementary = {}
    for mask in range(1 << 8):
        k = mask.bit_count()
        exponent = [8 - k, 0] + [(mask >> i) & 1 for i in range(8)]
        elementary[tuple(exponent)] = Q((-1) ** k * (k + 1))
    identity(records, "entire_elementary_characteristic", chi, elementary)

    coefficient7 = {
        (0,) + e[1:]: v for e, v in chi.items() if e[0] == 7
    }
    identity(records, "entire_first_trace_coefficient", coefficient7, scale(plus(*roots), -2))

    common_g = power(plus(z, scale(ell, -1)), 8)
    common_chi = plus(scale(common_g, 9), scale(times(z, derivative(common_g, 0)), -1))
    common_target = times(power(plus(z, scale(ell, -1)), 7), plus(z, scale(ell, -9)))
    identity(records, "collapsed_multiplicity_seven_and_one", common_chi, common_target)

    # Disk image identity, with five independent real indeterminates.
    n = 5
    x, y, s, t, radius = [variable(n, i) for i in range(n)]
    A = plus(power(x, 2), power(y, 2), scale(power(radius, 2), -1))
    dx, dy = plus(x, scale(s, -1)), plus(y, scale(t, -1))
    B = plus(power(dx, 2), power(dy, 2))
    numerator = plus(A, scale(plus(times(x, dx), times(y, dy)), -2), B)
    identity(records, "mobius_image_full_quadratic", numerator,
             plus(power(s, 2), power(t, 2), scale(power(radius, 2), -1)))

    # Completing the square for the convex disk of reciprocal values.
    p, q = s, t
    normv = plus(power(p, 2), power(q, 2))
    realwv = plus(times(x, p), scale(times(y, q), -1))
    completed = plus(times(power(A, 2), normv),
                     scale(times(A, realwv), -2),
                     power(x, 2), power(y, 2), scale(power(radius, 2), -1))
    identity(records, "mobius_disk_completed_square", completed,
             times(A, plus(times(A, normv), scale(realwv, -2), constant(n))))

    n = 4
    q, ell, M, N = [variable(n, i) for i in range(n)]
    shift = plus(q, scale(ell, -9))
    gap = plus(q, scale(ell, -1))
    remainder = plus(shift, scale(M, -heavy_coefficient))
    lhs = plus(scale(times(gap, remainder), 8),
               times(shift, M), scale(times(q, N), -8))
    rhs = scale(plus(times(gap, shift), scale(times(q, M), -1),
                     scale(times(q, N), -1)), 8)
    identity(records, "heavy_first_moment_remainder", lhs, rhs)

    n = 2
    u, gap = variable(n, 0), variable(n, 1)
    identity(records, "secular_moment_expansion",
             times(u, gap), plus(times(u, plus(gap, scale(u, -1))), power(u, 2)))

    n = 3
    a, x, y = [variable(n, i) for i in range(n)]
    d = plus(constant(n), a)
    b = plus(constant(n), scale(power(a, 2), -1))
    real_num = plus(constant(n), times(d, x))
    disk_num = plus(
        times(b, plus(power(real_num, 2), times(power(d, 2), power(y, 2)))),
        scale(times(times(a, d), real_num), 2), scale(power(d, 2), -1))
    target = times(power(d, 2), plus(scale(x, 2), times(b, plus(power(x, 2), power(y, 2)))))
    identity(records, "centered_unit_disk_constraint", disk_num, target)

    # Quoted9225 moment coordinates, checked as complete identities after
    # clearing only the explicit opening denominator Qopen.
    n = 10
    eta, V, H, K, y, T, M, Qopen, Usum, Hsquare = [
        variable(n, i) for i in range(n)]
    mh = scale(plus(times(eta, V), scale(H, -1)), Q(1, 2))
    nh = scale(plus(M, scale(K, -1), scale(times(mh, y), -2)), Q(1, 2))
    hp, hm = plus(mh, Qopen), plus(mh, scale(Qopen, -1))
    up_num, um_num = plus(times(y, Qopen), nh), plus(times(y, Qopen), scale(nh, -1))
    identity(records, "complex_chart_first_h_moment", plus(H, hp, hm), times(eta, V))
    identity(records, "complex_chart_mixed_moment",
             plus(times(Qopen, K), times(hp, up_num), times(hm, um_num)),
             times(Qopen, M))
    identity(records, "complex_chart_first_u_moment",
             plus(times(Qopen, Usum), up_num, um_num),
             times(Qopen, plus(Usum, scale(y, 2))))
    lhs = plus(Hsquare, power(hp, 2), power(hm, 2),
               scale(plus(Hsquare, scale(T, 2)), -1))
    rhs = scale(plus(power(Qopen, 2), power(mh, 2), scale(T, -1)), 2)
    identity(records, "complex_chart_second_h_moment_mod_opening", lhs, rhs)

    n = 3
    t, du, h = [variable(n, i) for i in range(n)]
    physical_norm = plus(power(times(power(t, 2), du), 2),
                         power(times(power(t, imaginary_scaling_power), h), 2))
    identity(records, "literal_normalized_to_physical_free_metric", physical_norm,
             plus(times(power(t, 4), power(du, 2)), times(power(t, 2), power(h, 2))))
    return records


def derive(radius_denominator=1200, heavy_coefficient=Q(9, 8),
           slack_cap=10, eta_endpoint=Q(1, 65536), degree_coefficient=9,
           imaginary_scaling_power=1):
    algebra = polynomial_controls(degree_coefficient, heavy_coefficient, imaginary_scaling_power)
    dmin, ellmin, epsmax = Q(13, 8), Q(1, 2), Q(1, 1000)
    xmax = Q(5, 8) / radius_denominator
    epsilon_cap = xmax / (dmin * (1 - xmax))
    phase_multiplier = Q(500, 499)
    phase_coefficient = Q(8) * phase_multiplier ** 2 / radius_denominator ** 2
    energy_coefficient = Q(8) / (
        radius_denominator ** 2 * dmin ** 2 * Q(999, 1000) ** 2)
    heavy_remainder_cap = Q(27, 28) + Q(8, 21)
    slack_coefficient = 2 + Q(7) / (2 * (ellmin - epsmax))

    e = eta_endpoint
    endpoint_d, endpoint_gamma = 2 - e, Q(3, 8) - e
    original_radius = Q(1, 1000)
    old_energy_cap = endpoint_d * endpoint_gamma / (22 * 8 * 9 ** 4)
    original_energy_bound = Q(8) * original_radius ** 2 / (
        endpoint_d ** 2 * (endpoint_d - original_radius) ** 2)
    # Whole-interval elementary bounds from the credited initial formulas.
    c_lo, c_hi = Q(3, 4), Q(1)
    y0_lo, y0_hi = 1 / (3 * (1 + c_hi)), 1 / (3 * (1 + c_lo))
    H_lo, H_hi = 14 * y0_lo, 14 * y0_hi
    U_lo, U_hi = -8 * (Q(2, 3) - y0_lo), -8 * (Q(2, 3) - y0_hi)
    h_lo, h_hi = (c_lo - 5) / 3, (c_hi - 5) / 3
    B_lo, B_hi = -h_hi * H_lo, -h_lo * H_hi
    x0_lo, x0_hi = (U_lo - B_hi) / 8, (U_hi - B_lo) / 8
    y1_lo, y1_hi = (U_lo + 3 * B_lo) / 8, (U_hi + 3 * B_hi) / 8
    T0_lo, T0_hi = H_lo / 2, H_hi / 2
    mh_cap = Q(31, 1000)
    nh_cap = (1 + Q(12, 100) + 4 * mh_cap) / 2
    opening_floor = Q(99, 100)
    free_h_cap = Q(1, 100)
    sqrt_e_cap = Q(1, 256)
    chart_critical_cap = 3 * e + Q(3, 2) * sqrt_e_cap
    primitive = {
        "uniform_x_cap": xmax,
        "uniform_epsilon_cap": epsilon_cap,
        "heavy_remainder_cap": heavy_remainder_cap,
        "slack_coefficient_bound": slack_coefficient,
        "phase_quadratic_coefficient": phase_coefficient,
        "original_energy_coefficient": energy_coefficient,
        "slack_gamma_coefficient": slack_cap * energy_coefficient,
        "near_boundary_old_energy_cap": old_energy_cap,
        "near_boundary_original_energy_bound": original_energy_bound,
        "whole_parent_seven_critical_radius": Q(3, 128) + Q(1, 320) + Q(9, 2560000),
        "branch_q_distance_from_one": (e + Q(1, 128)) / (1 - e - Q(1, 128)),
        "physical_separation": 1 - Q(1, 32) - Q(1, 128),
        "branch_initial_x_lower": x0_lo,
        "branch_initial_x_upper": x0_hi,
        "branch_initial_y_lower": y1_lo,
        "branch_initial_y_upper": y1_hi,
        "branch_initial_T_lower": T0_lo,
        "branch_initial_T_upper": T0_hi,
        "complex_chart_mean_h_cap": mh_cap,
        "complex_chart_mixed_n_cap": nh_cap,
        "complex_chart_opening_floor": opening_floor,
        "complex_chart_heavy_real_cap": 2 + nh_cap / opening_floor,
        "complex_chart_heavy_imaginary_cap": mh_cap + Q(5, 4),
        "complex_chart_physical_critical_cap": chart_critical_cap,
    }
    margins = {
        "x_below_1_over_1000": epsmax - xmax,
        "epsilon_below_1_over_1000": epsmax - epsilon_cap,
        "reciprocal_cluster_disjointness": 4 * ellmin - 5 * epsmax,
        "nine_epsilon_below_ell": ellmin - 9 * epsmax,
        "heavy_original_reciprocal_gap_above_three": 8 * ellmin - 10 * epsmax - 3,
        "cauchy_schwarz_square_margin": Q(9) - 8,
        "heavy_remainder_below_two": 2 - heavy_remainder_cap,
        "slack_coefficient_below_cap": Q(slack_cap) - slack_coefficient,
        "phase_entry_margin": Q(1, 160000) - phase_coefficient,
        "slack_entry_margin": Q(1, 64) - slack_cap * energy_coefficient,
        "near_boundary_radius_margin": endpoint_d ** 2 * endpoint_gamma
            - (radius_denominator * original_radius) ** 2,
        "near_boundary_old_energy_already_applies": old_energy_cap - original_energy_bound,
        "gain_squared_over_7348_literal_root_radius": Q(1944, radius_denominator) ** 2 * dmin - 4,
        "whole_parent_seven_critical_below_1_over_32": Q(1, 32)
            - primitive["whole_parent_seven_critical_radius"],
        "formal_branch_critical_square_margin": (Q(1, 128) - 2 * e) ** 2 - Q(3, 2) * e,
        "formal_branch_reciprocal_above_zero": 1 - e - Q(1, 128),
        "formal_branch_q_below_1_over_120": Q(1, 120)
            - primitive["branch_q_distance_from_one"],
        "initial_x_cube_below_one": 1 - max(abs(x0_lo), abs(x0_hi)) - Q(1, 1024),
        "initial_y_cube_below_one": 1 - max(abs(y1_lo), abs(y1_hi)) - Q(1, 1024),
        "initial_T_cube_positive": T0_lo - Q(1, 1024),
        "initial_T_cube_below_three_halves": Q(3, 2) - T0_hi - Q(1, 1024),
        "sqrt_eta_endpoint_bound": sqrt_e_cap ** 2 - e,
        "complex_chart_mean_h_margin": mh_cap - (e + 6 * free_h_cap) / 2,
        "complex_chart_opening_square_margin": 1 - mh_cap ** 2 - opening_floor ** 2,
        "sqrt_three_halves_below_five_quarters": Q(5, 4) ** 2 - Q(3, 2),
        "complex_chart_heavy_real_below_three": 1 - nh_cap / opening_floor,
        "complex_chart_heavy_imaginary_below_three_halves": Q(3, 2) - mh_cap - Q(5, 4),
        "complex_chart_critical_below_1_over_128": Q(1, 128) - chart_critical_cap,
    }
    for name, margin in margins.items():
        if margin < 0 or (margin == 0 and name != "sqrt_eta_endpoint_bound"):
            raise ValueError("nonpositive sufficient margin: " + name)
    return {
        "schema": "sendov-critical-entry-dichotomy-v1",
        "author": "six-sendov-1",
        "role": "researcher",
        "parameters": {
            "degree": 9,
            "radius_denominator": radius_denominator,
            "heavy_first_moment_coefficient": str(heavy_coefficient),
            "slack_energy_cap": slack_cap,
            "eta_endpoint": str(eta_endpoint),
            "imaginary_scaling_power_in_sqrt_eta": imaginary_scaling_power,
        },
        "whole_polynomial_identities": algebra,
        "exact_values": {k: str(v) for k, v in primitive.items()},
        "strict_margins": {
            k: str(v) for k, v in margins.items() if k != "sqrt_eta_endpoint_bound"
        },
        "closed_rational_bounds": {
            "sqrt_eta_endpoint_bound": str(margins["sqrt_eta_endpoint_bound"])
        },
        "proof_boundary": "ordinary disk convexity, root-count homotopy, phase and modulus inequalities; imported9189 and labeled9174; no formal kernel",
    }


def damage_controls():
    damages = [
        {"degree_coefficient": 8},
        {"heavy_coefficient": Q(1)},
        {"radius_denominator": 1000},
        {"slack_cap": 8},
        {"eta_endpoint": Q(1, 16384)},
        {"imaginary_scaling_power": 2},
    ]
    for damage in damages:
        try:
            derive(**damage)
        except ValueError:
            continue
        raise ValueError("damaged mathematical control was accepted: " + repr(damage))
    return len(damages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    record = derive()
    damages = damage_controls()
    if args.write_expected:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads(args.expected.read_text())
        if expected != record:
            raise ValueError("complete expected record differs from regeneration")
    print(json.dumps({
        "status": "pass",
        "record_sha256": hashlib.sha256(canonical(record)).hexdigest(),
        "whole_polynomial_identities": len(record["whole_polynomial_identities"]),
        "strict_rational_margins": len(record["strict_margins"]),
        "closed_rational_bounds": len(record["closed_rational_bounds"]),
        "mathematical_damage_rejections": damages,
        "analytic_bridges_formalized": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
