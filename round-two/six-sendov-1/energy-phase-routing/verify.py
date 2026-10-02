"""Exact finite controls for the ordinary energy-sensitive phase proof.

Actual author six-sendov-1, researcher. CPython 3.12, standard library.
Analytic spectral and imported stability bridges are written in PROOF.md.
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


def derive(epsilon_cap=Q(1, 1000), phase_coefficient=Q(41, 40),
           root_budget=165000, s_heavy=3, light_coefficient=Q(3, 4),
           pv_coefficient=Q(15, 8), degree_coefficient=9,
           heavy_phase_divisor=9):
    matrices, polys, minors = algebra(s_heavy, light_coefficient,
                                     pv_coefficient, degree_coefficient)
    t = 2 * epsilon_cap
    dmin = Q(13, 8)
    energy_denominator = 160000 * phase_coefficient
    if Q(9, 8) / heavy_phase_divisor != Q(1, 8):
        raise ValueError("heavy linear phase normalization differs")
    sharp_dynamic_cap = ((1 + 5 * t) / (1 - t)) ** 2
    b = Q(1, 1000)
    # Gaussian rational operations are expanded directly for the legal witness.
    cos = (1 - b * b) / (1 + b * b)
    sin = 2 * b / (1 + b * b)
    real_gap = 1 + cos
    reciprocal_real = real_gap / (real_gap ** 2 + sin ** 2)
    reciprocal_imag = sin / (real_gap ** 2 + sin ** 2)
    if cos ** 2 + sin ** 2 != 1 or reciprocal_real != Q(1, 2):
        raise ValueError("actual witness disk/trace identity differs")
    if reciprocal_imag != b / 2:
        raise ValueError("actual witness reciprocal factor differs")
    witness_E = 2 * reciprocal_imag ** 2
    witness_B = 2 * ((1 - cos) ** 2 + sin ** 2)
    if witness_E != Q(1, 2000000) or witness_B != Q(8, 1000001):
        raise ValueError("entire actual witness differs")
    margins = {
        "epsilon_below_critical_disjointness": Q(4, 5) * Q(1, 2) - epsilon_cap,
        "heavy_gap_above_seven_ell": Q(1, 2) - 9 * epsilon_cap,
        "projector_one_fifth": 49 - 25 * Q(15, 8),
        "linear_norm_ten_thirds": Q(100, 9) - 11,
        "sqrt_eight_below_three": 9 - 8,
        "pair_error_below_five": 25 - (16 + Q(4, 9)),
        "uniform_phase_coefficient": phase_coefficient - sharp_dynamic_cap,
        "original_root_to_reciprocal_energy": root_budget * Q(639, 640) ** 2
            - energy_denominator,
        "root_budget_sqrt_denominator_above_400": Q(root_budget) - 400 ** 2,
        "gamma_sqrt_below_five_eighths": Q(25, 64) - Q(3, 8),
        "automatic_epsilon": epsilon_cap ** 2 - Q(3, 8) / (energy_denominator * dmin ** 2),
        "slack_entry": Q(1, 64) - 10 / (energy_denominator * dmin ** 2),
        "old_max_domain_containment": Q(1, root_budget) - Q(8, 1200 ** 2),
        "witness_root_budget": Q(3, 2 * root_budget) - witness_B,
        "witness_outside_old_max": witness_B / 2 - Q(1, 960000),
        "witness_reciprocal_energy": Q(3, 8) / (4 * energy_denominator) - witness_E,
        "witness_baseline_already_known": Q(3, 4) / 1154736 - witness_E,
    }
    for name, value in margins.items():
        if value <= 0:
            raise ValueError("nonpositive exact sufficient margin: " + name)
    return {
        "schema": "sendov-energy-phase-routing-v1",
        "agent_name": "six-sendov-1",
        "role": "researcher",
        "parameters": {"degree": 9, "epsilon_cap": str(epsilon_cap),
                       "phase_coefficient": str(phase_coefficient),
                       "energy_denominator": str(energy_denominator),
                       "heavy_phase_divisor": heavy_phase_divisor,
                       "original_root_budget_denominator": root_budget},
        "complete_rational_matrices": matrices,
        "whole_polynomial_identities": polys,
        "all256_principal_minors": minors,
        "strict_sufficient_margins": {k: str(v) for k, v in margins.items()},
        "actual_witness": {"a": "1", "gamma": "3/8", "six_roots": "-1",
                           "pair_real": str(-cos), "pair_imaginary_absolute": str(sin),
                           "A": "0", "E": str(witness_E), "B_original": str(witness_B),
                           "previous_max_radius_squared": "1/960000"},
        "dynamic_phase_coefficient_cap": str(sharp_dynamic_cap),
        "old_to_new_original_squared_budget_gain": str(Q(180000, root_budget)),
        "trust_boundary": "ordinary Schur/projection/argument inequalities, classical localization, "
            "9257 slack/heavy estimates and9189 stability; not formalized",
    }


def damage_controls():
    damages = [
        {"s_heavy": 2},
        {"degree_coefficient": 8},
        {"light_coefficient": Q(1)},
        {"pv_coefficient": Q(2)},
        {"epsilon_cap": Q(1, 100)},
        {"phase_coefficient": Q(1)},
        {"root_budget": 150000},
        {"heavy_phase_divisor": 8},
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
        "status": "pass",
        "record_sha256": hashlib.sha256(canon(result)).hexdigest(),
        "complete_matrix_identities": len(result["complete_rational_matrices"]),
        "whole_polynomial_identities": len(result["whole_polynomial_identities"]),
        "principal_minors": len(result["all256_principal_minors"]),
        "strict_rational_margins": len(result["strict_sufficient_margins"]),
        "mathematical_damage_rejections": damages,
        "analytic_bridges_formalized": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
