"""Exact finite controls for the mean-sensitive and signed-trace entry proof.

Actual author six-sendov-1, researcher. CPython 3.12, standard library.
Analytic spectral and imported stability bridges are written in PROOF.md.
Sparse-polynomial/matrix helpers adapt this author's published9307 checker;
this standalone program recomputes its inputs and is author validation.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def const(n, value=1):
    return {(0,) * n: Q(value)} if value else {}


def var(n, k):
    e = [0] * n
    e[k] = 1
    return {tuple(e): Q(1)}


def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, Q(0)) + c
    return {e: c for e, c in out.items() if c}


def mul(p, q):
    out = {}
    for e, c in p.items():
        for f, d in q.items():
            g = tuple(a + b for a, b in zip(e, f, strict=True))
            out[g] = out.get(g, Q(0)) + c * d
    return {e: c for e, c in out.items() if c}


def scale(p, c):
    return {e: d * Q(c) for e, d in p.items() if d * Q(c)}


def prod(items, n):
    out = const(n)
    for p in items:
        out = mul(out, p)
    return out


def diff(p, k):
    out = {}
    for e, c in p.items():
        if e[k]:
            f = list(e)
            f[k] -= 1
            out[tuple(f)] = c * e[k]
    return out


def poly_record(p):
    entries = [[list(e), str(c)] for e, c in sorted(p.items())]
    return {"complete_terms": len(entries),
            "coefficient_sha256": hashlib.sha256(canon(entries)).hexdigest()}


def identity(records, name, left, right):
    if left != right:
        raise ValueError("whole polynomial differs: " + name)
    records[name] = poly_record(left)


def matrix_product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(8))
             for j in range(8)] for i in range(8)]


def matrix_control(records, name, left, right):
    if left != right:
        raise ValueError("complete matrix differs: " + name)
    records[name] = [[str(v) for v in row] for row in left]


def determinant(a):
    # Fraction Gaussian elimination with exact pivoting, no polynomial shortcut.
    a = [[Q(v) for v in row] for row in a]
    n = len(a)
    value = Q(1)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            value = -value
        d = a[k][k]
        value *= d
        for i in range(k + 1, n):
            f = a[i][k] / d
            for j in range(k + 1, n):
                a[i][j] -= f * a[k][j]
            a[i][k] = Q(0)
    return value


def linear_matrix(a, b):
    y = [var(8, k) for k in range(8)]
    return [[add(*(scale(y[k], a[i][k] * b[k][j]) for k in range(8)))
             for j in range(8)] for i in range(8)]


def norm_polynomial(a):
    return add(*(mul(p, p) for row in a for p in row))


def matrix_poly_control(records, name, left, right):
    if left != right:
        raise ValueError("whole polynomial matrix differs: " + name)
    entries = [[poly_record(p) for p in row] for row in left]
    records[name] = {"rows": 8, "columns": 8,
                     "complete_entry_sha256": hashlib.sha256(canon(entries)).hexdigest(),
                     "total_complete_terms": sum(r["complete_terms"]
                                                for row in entries for r in row)}


def algebra(s_heavy=3, light_coefficient=Q(3, 4),
            pv_coefficient=Q(15, 8), degree_coefficient=9):
    matrices, polys = {}, {}
    I = [[Q(i == j) for j in range(8)] for i in range(8)]
    H = [[Q(1, 8) for _ in range(8)] for _ in range(8)]
    P = [[I[i][j] - H[i][j] for j in range(8)] for i in range(8)]
    S = [[P[i][j] + s_heavy * H[i][j] for j in range(8)] for i in range(8)]
    big = [[I[i][j] + 1 for j in range(8)] for i in range(8)]
    matrix_control(matrices, "P_squared", matrix_product(P, P), P)
    matrix_control(matrices, "S_squared", matrix_product(S, S), big)
    matrix_control(matrices, "SP", matrix_product(S, P), P)
    matrix_control(matrices, "PS", matrix_product(P, S), P)
    if any(sum(row) for row in P):
        raise ValueError("P does not annihilate ones")
    matrices["P_ones"] = ["0"] * 8

    # Entire characteristic: complete principal minors versus 9g-qg'.
    n = 9
    q = var(n, 0)
    u = [var(n, k + 1) for k in range(8)]
    g = prod([add(q, scale(v, -1)) for v in u], n)
    chi = add(scale(g, degree_coefficient), scale(mul(q, diff(g, 0)), -1))
    from_minors, minors = {}, []
    for mask in range(1 << 8):
        indices = [i for i in range(8) if mask >> i & 1]
        d = determinant([[big[i][j] for j in indices] for i in indices])
        if d != len(indices) + 1:
            raise ValueError("principal minor differs: " + str(mask))
        minors.append(str(d))
        exponent = [8 - len(indices)] + [(mask >> i) & 1 for i in range(8)]
        from_minors[tuple(exponent)] = (-1) ** len(indices) * d
    identity(polys, "full_characteristic_minors_vs_derivative", from_minors, chi)
    lead = {e: c for e, c in chi.items() if e[0] == 8}
    identity(polys, "monic_characteristic", lead, prod([q] * 8, n))
    first = {(0,) + e[1:]: c for e, c in chi.items() if e[0] == 7}
    identity(polys, "complete_first_trace", first, scale(add(*u), -2))
    common = {}
    for e, c in chi.items():
        f = (e[0], sum(e[1:]))
        common[f] = common.get(f, Q(0)) + c
    common = {e: c for e, c in common.items() if c}
    q2, u2 = var(2, 0), var(2, 1)
    identity(polys, "entire_common_family_factorization", common,
             mul(prod([add(q2, scale(u2, -1))] * 7, 2),
                 add(q2, scale(u2, -9))))

    K = linear_matrix(S, S)
    compressed = [[add(*(scale(K[k][l], P[i][k] * P[l][j])
                         for k in range(8) for l in range(8)))
                   for j in range(8)] for i in range(8)]
    pdy = linear_matrix(P, P)
    matrix_poly_control(matrices, "PKP", compressed, pdy)
    y = [var(8, k) for k in range(8)]
    Ey = add(*(mul(p, p) for p in y))
    b = add(*y)
    b2 = mul(b, b)
    identity(polys, "full_imaginary_norm", norm_polynomial(K),
             add(scale(Ey, 3), b2))
    identity(polys, "full_light_imaginary_norm", norm_polynomial(pdy),
             add(scale(Ey, light_coefficient), scale(b2, Q(1, 64))))
    identity(polys, "whole_combined_leading_phase_budget",
             add(norm_polynomial(pdy), scale(b2, Q(1, 64))),
             add(scale(Ey, Q(3, 4)), scale(b2, Q(1, 32))))
    identity(polys, "full_PV_norm", norm_polynomial(linear_matrix(P, S)),
             add(scale(Ey, pv_coefficient), scale(b2, Q(-1, 8))))
    return matrices, polys, minors


def extra_algebra(polys, pair_coefficient=3, trace_coefficient=Q(7, 8)):
    # Quotient imaginary numerators: all components, no point samples.
    ar, ai, br, bi = [var(4, k) for k in range(4)]
    nr = add(mul(ar, br), mul(ai, bi))
    ni = add(mul(ai, br), scale(mul(ar, bi), -1))
    den = add(mul(br, br), mul(bi, bi))
    identity(polys, "whole_quotient_cancellation_real",
             add(mul(nr, br), scale(mul(ni, bi), -1)), mul(ar, den))
    identity(polys, "whole_quotient_cancellation_imaginary",
             add(mul(nr, bi), mul(ni, br)), mul(ai, den))
    qx, qy, ell = [var(3, k) for k in range(3)]
    dx = add(qx, scale(ell, -1))
    wx = add(qx, scale(ell, -9))
    identity(polys, "full_w_over_D_imaginary_numerator",
             add(mul(qy, dx), scale(mul(wx, qy), -1)),
             scale(mul(ell, qy), 8))
    identity(polys, "full_q_over_D_imaginary_numerator",
             add(mul(qy, dx), scale(mul(qx, qy), -1)),
             scale(mul(ell, qy), -1))
    D, v = [var(2, k) for k in range(2)]
    identity(polys, "entire_geometric_quotient_remainder",
             mul(D, D),
             add(mul(add(D, v), add(D, scale(v, -1))), mul(v, v)))
    q, ell = [var(2, k) for k in range(2)]
    identity(polys, "entire_heavy_linear_remainder_normalization",
             add(scale(q, 8), scale(add(q, scale(ell, -1)), -9)),
             scale(add(q, scale(ell, -9)), -1))
    ell, M, R = [var(3, k) for k in range(3)]
    light_trace = add(scale(ell, 16), scale(M, 2),
                      scale(add(scale(ell, 9), scale(M, Q(9, 8)), R), -1),
                      scale(ell, -7))
    identity(polys, "full_signed_light_trace",
             light_trace, add(scale(M, trace_coefficient), scale(R, -1)))

    y = [var(8, k) for k in range(8)]
    b = add(*y)
    Ey = add(*(mul(p, p) for p in y))
    centered = [add(p, scale(b, Q(-1, 8))) for p in y]
    identity(polys, "whole_mean_variance_budget",
             add(scale(Ey, Q(3, 4)), scale(mul(b, b), Q(1, 32))),
             add(Ey, scale(add(*(mul(p, p) for p in centered)), Q(-1, 4))))

    q, ell, tau = [var(3, k) for k in range(3)]
    gap = add(q, scale(ell, -1))
    gap2 = mul(gap, gap)
    tau2 = mul(tau, tau)
    g = mul(prod([gap] * 6, 3), add(gap2, tau2))
    chi = add(scale(g, 9), scale(mul(q, diff(g, 0)), -1))
    bracket = add(mul(gap2, add(q, scale(ell, -9))),
                  scale(mul(tau2, add(q, scale(ell, -3))), pair_coefficient))
    identity(polys, "entire_centered_pair_characteristic",
             chi, mul(prod([gap] * 5, 3), bracket))
    tau, s, ell = [var(3, k) for k in range(3)]
    q = add(ell, mul(tau, s))
    shifted = mul(tau, s)
    rescaled_bracket = add(mul(mul(shifted, shifted), add(q, scale(ell, -9))),
                           scale(mul(mul(tau, tau), add(q, scale(ell, -3))), 3))
    cubic = add(mul(tau, prod([s] * 3, 3)),
                scale(mul(ell, mul(s, s)), -8),
                scale(mul(tau, s), 3), scale(ell, -6))
    identity(polys, "entire_centered_pair_rescaling",
             rescaled_bracket, mul(mul(tau, tau), cubic))
    limit_poly = {e: c for e, c in cubic.items() if e[0] == 0}
    identity(polys, "entire_centered_pair_limit_polynomial", limit_poly,
             scale(mul(ell, add(mul(s, s), const(3, Q(3, 4)))), -8))
    a, tau = [var(2, k) for k in range(2)]
    d = add(const(2), a)
    one_minus_a2 = add(const(2), scale(mul(a, a), -1))
    excess_scaled = add(mul(one_minus_a2,
                            add(const(2), mul(mul(tau, tau), mul(d, d)))),
                        scale(mul(a, d), 2), scale(mul(d, d), -1))
    identity(polys, "entire_physical_pair_disk_excess",
             excess_scaled, mul(one_minus_a2, mul(mul(tau, tau), mul(d, d))))
    d, v = [var(2, k) for k in range(2)]
    identity(polys, "entire_inverse_original_displacement",
             add(mul(d, add(const(2), mul(d, v))), scale(d, -1)),
             mul(mul(d, d), v))
    eta = var(1, 0)
    two_minus_eta = add(const(1, 2), scale(eta, -1))
    identity(polys, "entire_boundary_value_gap_numerator",
             add(const(1, 16), scale(mul(add(const(1, 8), scale(eta, 4)),
                                           two_minus_eta), -1)),
             scale(mul(eta, eta), 4))
    z, eta = [var(2, k) for k in range(2)]
    powers = [const(2)]
    for _ in range(9):
        powers.append(mul(powers[-1], z))
    cyclotomic = add(*powers[:9])
    identity(polys, "entire_uncovered_legal_family",
             mul(add(z, const(2, -1), eta), cyclotomic),
             add(powers[9], const(2, -1), mul(eta, cyclotomic)))


def derive(epsilon_cap=Q(1, 1000), phase_coefficient=Q(41, 40),
           centered_coefficient=Q(4, 5), heavy_imaginary_coefficient=Q(3),
           slack_coefficient=Q(10), phase_denominator=164000,
           centered_denominator=128000, s_heavy=3, degree_coefficient=9,
           pair_coefficient=3, trace_coefficient=Q(7, 8),
           heavy_phase_divisor=9, witness_tau_denominator=1800,
           anisotropic_radial_coefficient=Q(9, 10), radial_energy_denominator=180):
    matrices, polys, minors = algebra(s_heavy=s_heavy,
                                     degree_coefficient=degree_coefficient)
    extra_algebra(polys, pair_coefficient, trace_coefficient)
    if Q(9, 8) / heavy_phase_divisor != Q(1, 8):
        raise ValueError("heavy phase mean normalization differs")
    if heavy_imaginary_coefficient > 3:
        raise ValueError("fixed heavy phase error would be exceeded")
    t = 2 * epsilon_cap
    C = 2 * (Q(27, 56) + Q(10, 49)) + Q(16, 21)
    C += (Q(104, 189) + Q(20, 441)) * 3 * epsilon_cap
    uniform_cap = ((1 + 5 * t) / (1 - t)) ** 2
    centered_cap = ((Q(7, 8) + 5 * t) / (1 - t)) ** 2
    radial_cap = 2 + Q(7) / (2 * (Q(1, 2) - epsilon_cap))
    light_radial_cap = (Q(15, 16) + 4 * t) ** 2 / (2 * (Q(1, 2) - epsilon_cap))
    equalities = {
        "closed_mixed_radial_budget": Q(7, 8) / 112 + slack_coefficient / 1280,
        "general_phase_entry": phase_coefficient / phase_denominator,
        "centered_phase_entry": centered_coefficient / centered_denominator,
    }
    if equalities != {"closed_mixed_radial_budget": Q(1, 64),
                      "general_phase_entry": Q(1, 160000),
                      "centered_phase_entry": Q(1, 160000)}:
        raise ValueError("closed entry budgets differ")

    # Exact Gaussian-rational inverses of the actual, complex witness roots.
    tau = Q(1, witness_tau_denominator)
    ur = Q(1, 2)
    u_norm2 = ur ** 2 + tau ** 2
    zr, zi = 1 - ur / u_norm2, tau / u_norm2
    if zr ** 2 + zi ** 2 != 1:
        raise ValueError("entire pair witness is outside its exact circle")
    gapr = 1 - zr
    gap2 = gapr ** 2 + zi ** 2
    if gapr / gap2 != ur or zi / gap2 != tau:
        raise ValueError("entire pair witness reciprocal differs")
    witness_E = 2 * tau ** 2
    witness_B = 2 * ((zr + 1) ** 2 + zi ** 2)
    real_z = Q(-499, 501)
    real_u = 1 / (1 - real_z)
    real_v = real_u - ur
    real_E, real_B = real_v ** 2, (real_z + 1) ** 2
    if real_u != Q(501, 1000) or real_E != Q(1, 1000000):
        raise ValueError("entire real witness reciprocal differs")
    gamma = Q(3, 8)
    old_E = gamma / (164000 * 4)
    old_B = 4 * gamma / 165000
    margins = {
        "two_disks_strictly_separated": Q(4, 5) * Q(1, 2) - epsilon_cap,
        "heavy_gap_above_seven_ell": Q(1, 2) - 9 * epsilon_cap,
        "heavy_denominator_above_three": 4 - 10 * epsilon_cap - 3,
        "projector_one_fifth": 49 - 25 * Q(15, 8),
        "sqrt_eight_below_three": Q(9) - 8,
        "sqrt_eleven_below_ten_thirds": Q(100, 9) - 11,
        "sqrt_eighty_eight_below_ten": Q(100) - 88,
        "heavy_imaginary_remainder": heavy_imaginary_coefficient - C,
        "collective_error_below_five": Q(25) - 17,
        "centered_sqrt_majorant": Q(49, 64) - Q(3, 4),
        "uniform_phase_coefficient": phase_coefficient - uniform_cap,
        "centered_phase_coefficient": centered_coefficient - centered_cap,
        "signed_slack_coefficient": slack_coefficient - radial_cap,
        "old_negative_trace_epsilon_is_automatic": epsilon_cap ** 2
            - Q(3, 8) / (164000 * Q(13, 8) ** 2),
        "old_negative_trace_radial_energy_is_contained": Q(1, 1280)
            - 1 / (164000 * Q(13, 8) ** 2),
        "complex_witness_max_energy": gamma / radial_energy_denominator - witness_E,
        "complex_witness_epsilon": epsilon_cap - tau,
        "complex_witness_centered_entry": gamma / (centered_denominator * 4) - witness_E,
        "complex_witness_outside_old_energy": witness_E - old_E,
        "complex_witness_outside_old_original_budget": witness_B - old_B,
        "complex_witness_baseline_already_known": Q(3, 4) / 1154736 - witness_E,
        "real_witness_max_energy": gamma / radial_energy_denominator - real_E,
        "real_witness_trace": gamma / 112 - real_v,
        "real_witness_outside_old_energy": real_E - old_E,
        "real_witness_outside_old_original_budget": real_B - old_B,
        "branch_initial_x_cube_inside_one": 1 - Q(35, 36) - Q(1, 1024),
        "branch_initial_y_cube_inside_two": 2 - Q(17, 9) - Q(1, 1024),
        "branch_initial_y_cube_positive": Q(14, 9) - Q(35, 36) - Q(1, 1024),
        "two_coefficient_neighborhoods_separated_by_six": 7 - Q(18, 65536)
            - Q(16, 499) - 6,
        "light_radial_square_root_majorant": Q(225, 256) - Q(7, 8),
        "anisotropic_radial_coefficient": anisotropic_radial_coefficient - light_radial_cap,
        "new_mixed_radial_entry": Q(1, 64) - Q(7, 8) / 112
            - Q(113, 84) / radial_energy_denominator
            - anisotropic_radial_coefficient / (centered_denominator * Q(13, 8) ** 2),
        "complex_witness_outside9339_energy": witness_E - gamma / (163200 * 4),
        "complex_witness_outside9339_original": witness_B - 4 * gamma / 164000,
        "real_witness_outside9339_energy": real_E - gamma / (163200 * 4),
        "real_witness_outside9339_original": real_B - 4 * gamma / 164000,
        "branch_z8_slope_above_four": Q(30, 7) - Q(9, 1024) - 4,
        "uncovered_family_fails_antipodal_coefficient": Q(7) - Q(16, 499),
    }
    for name, value in margins.items():
        if value <= 0:
            raise ValueError("nonpositive exact sufficient margin: " + name)
    if abs(real_v) != epsilon_cap:
        raise ValueError("real witness does not meet the closed epsilon endpoint")
    return {
        "schema": "sendov-anisotropic-entry-v1",
        "agent_name": "six-sendov-1", "role": "researcher",
        "parameters": {"degree": 9, "epsilon_cap": str(epsilon_cap),
                       "uniform_phase_coefficient": str(phase_coefficient),
                       "centered_phase_coefficient": str(centered_coefficient),
                       "heavy_imaginary_coefficient": str(heavy_imaginary_coefficient),
                       "signed_trace_coefficient": str(trace_coefficient),
                       "slack_energy_coefficient": str(slack_coefficient),
                       "heavy_phase_divisor": heavy_phase_divisor,
                       "general_phase_denominator": phase_denominator,
                       "centered_phase_denominator": centered_denominator},
        "new_radial_parameters": {"real_remainder_energy_coefficient": "113/84",
                                  "imaginary_radial_coefficient": str(anisotropic_radial_coefficient),
                                  "separable_total_energy_denominator": radial_energy_denominator,
                                  "light_radial_coefficient_majorant": str(light_radial_cap)},
        "complete_rational_matrices": matrices,
        "whole_polynomial_identities": polys,
        "all256_principal_minors": minors,
        "strict_sufficient_margins": {k: str(v) for k, v in margins.items()},
        "exact_closed_budgets": {k: str(v) for k, v in equalities.items()},
        "heavy_imaginary_coefficient_majorant": str(C),
        "dynamic_phase_coefficient_cap": str(uniform_cap),
        "centered_dynamic_majorant_cap": str(centered_cap),
        "radial_coefficient_majorant": str(radial_cap),
        "complex_witness": {"a": "1", "gamma": "3/8", "six_roots": "-1",
                            "pair_real": str(zr), "pair_imaginary_absolute": str(zi),
                            "reciprocal_real": str(ur), "reciprocal_imaginary_absolute": str(tau),
                            "A": "0", "b": "0", "E": str(witness_E),
                            "E_y": str(witness_E), "B_original": str(witness_B)},
        "real_witness": {"a": "1", "seven_roots": "-1", "eighth_root": str(real_z),
                         "eighth_reciprocal": str(real_u), "A": str(real_v), "b": "0",
                         "E": str(real_E), "E_y": "0", "B_original": str(real_B),
                         "epsilon": str(abs(real_v)), "known_F": str(8 + 2 * real_v)},
        "old9307_thresholds_at_a_one": {"E": str(old_E), "B_original": str(old_B)},
        "review9339_thresholds_at_a_one": {"E": str(gamma / (163200 * 4)),
                                           "B_original": str(4 * gamma / 164000)},
        "coefficient_interface": {"original_max_motion_cap": str(Q(2, 499)),
                                  "original_z8_coefficient_motion_cap": str(Q(16, 499)),
                                  "branch_eta_cap": "1/65536",
                                  "original_z8_to_branch_gap_lower": str(7 - Q(18, 65536)
                                                                           - Q(16, 499))},
        "trust_boundary": "ordinary quotient/projection/Schur/argument inequalities, classical "
            "localization and Gauss--Lucas, limiting roots,9257 heavy/trace and9189 stability; "
            "not formalized; kernel credit9307, matrix7348, pair benchmark8276/8305; "
            "9113 covering cube/legal family upper bound for coefficient interface and exclusion; "
            "9339 collective radial calculation credited,not a verdict on this new bound",
    }


def damage_controls():
    damages = [
        {"s_heavy": 2}, {"degree_coefficient": 8},
        {"pair_coefficient": 2}, {"trace_coefficient": Q(1)},
        {"heavy_phase_divisor": 8}, {"epsilon_cap": Q(1, 100)},
        {"phase_coefficient": Q(1)}, {"centered_coefficient": Q(3, 4)},
        {"heavy_imaginary_coefficient": Q(2)}, {"slack_coefficient": Q(9)},
        {"phase_denominator": 160000}, {"centered_denominator": 120000},
        {"witness_tau_denominator": 2000},
        {"anisotropic_radial_coefficient": Q(4, 5)},
        {"radial_energy_denominator": 160},
    ]
    for damage in damages:
        try:
            derive(**damage)
        except ValueError:
            continue
        raise ValueError("damaged mathematics accepted: " + repr(damage))
    return len(damages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    result = derive()
    damages = damage_controls()
    if args.write_expected:
        args.expected.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads(args.expected.read_text())
        if expected != result:
            raise ValueError("entire fixture differs from regeneration")
    print(json.dumps({
        "status": "pass", "record_sha256": hashlib.sha256(canon(result)).hexdigest(),
        "complete_matrix_identities": len(result["complete_rational_matrices"]),
        "whole_polynomial_identities": len(result["whole_polynomial_identities"]),
        "principal_minors": len(result["all256_principal_minors"]),
        "strict_rational_margins": len(result["strict_sufficient_margins"]),
        "closed_budget_identities": len(result["exact_closed_budgets"]),
        "mathematical_damage_rejections": damages, "analytic_bridges_formalized": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
