"""Exact whole-certificate checks for the actual three-double angular family.

Python 3.10+ standard library only.  This checks algebra and complete signs;
the classification and compression interpretation are ordinary written proof.
Same author: six-sendov-2, researcher.  No independent-review claim.
"""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb
from pathlib import Path

BASE = Path(__file__).resolve().parent
DOMAIN = "QQ[r][z], r>1 and B=1+2r^2-r^4-r^6>0"
KEYS = {
    "domain", "critical_quartic", "inverse_common_denominator",
    "inverse_numerators", "discriminant",
    "discriminant_divided_by_inverse_denominator", "angular_numerator_u",
    "angular_denominator_u", "complete_bernstein_denominator",
    "complete_bernstein_divided_gap",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def load_json(path):
    data = Path(path).read_bytes()
    require(len(data) <= 150_000, "oversized certificate or expected fixture")
    return json.loads(data, object_pairs_hook=unique_object)


def rational(value):
    require(type(value) is str and 0 < len(value) <= 500,
            "rational must be a bounded canonical string")
    try:
        number = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc
    require(str(number) == value, "noncanonical rational")
    return number


def vector(value, length=None):
    require(type(value) is list and 1 <= len(value) <= 128,
            "polynomial must be a bounded coefficient list")
    if length is not None:
        require(len(value) == length, "coefficient-vector dimension")
    result = list(map(rational, value))
    require(len(result) == 1 or result[-1] != 0, "trailing polynomial zero")
    return result


def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a or [Q(0)]


def add(a, b):
    return trim([(a[i] if i < len(a) else Q(0))
                 + (b[i] if i < len(b) else Q(0))
                 for i in range(max(len(a), len(b)))])


def scale(a, t):
    return trim([x * t for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i+j] += x*y
    return trim(c)


def divide(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], "zero polynomial divisor")
    q = [Q(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        j, v = len(a) - len(b), a[-1] / b[-1]
        q[j] += v
        a = sub(a, [Q(0)]*j + scale(b, v))
    return trim(q), trim(a)


def evaluate(a, x):
    out = Q(0)
    for c in reversed(a):
        out = out*x+c
    return out


def ztrim(a):
    a = [trim(x) for x in a]
    while len(a) > 1 and a[-1] == [0]:
        a.pop()
    return a


def zadd(a, b):
    return ztrim([add(a[i] if i < len(a) else [Q(0)],
                     b[i] if i < len(b) else [Q(0)])
                  for i in range(max(len(a), len(b)))])


def zmul(a, b):
    c = [[Q(0)] for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] = add(c[i+j], mul(x, y))
    return ztrim(c)


def zscale(a, t):
    return ztrim([scale(v, t) for v in a])


def zdiv(a, b):
    require(b[-1] == [1], "only monic outer division is used")
    a = ztrim(a)
    q = [[Q(0)] for _ in range(max(1, len(a) - len(b) + 1))]
    while a != [[0]] and len(a) >= len(b):
        j, v = len(a) - len(b), a[-1]
        q[j] = add(q[j], v)
        terms = [[Q(0)] for _ in range(j)] + [mul(v, x) for x in b]
        a = zadd(a, zscale(terms, -1))
    return ztrim(q), ztrim(a)


def zderiv(a):
    return ztrim([scale(a[i], i) for i in range(1, len(a))])


def resultant(a, b):
    # Entire Sylvester determinant by subset DP, with QQ[r] coefficients.
    n, m = len(a)-1, len(b)-1
    size, rows = n+m, []
    for i in range(m):
        rows.append([[Q(0)]]*i + list(reversed(a)) + [[Q(0)]]*(m-i-1))
    for i in range(n):
        rows.append([[Q(0)]]*i + list(reversed(b)) + [[Q(0)]]*(n-i-1))
    dp = {0: [Q(1)]}
    for row in rows:
        new = {}
        for mask, v in dp.items():
            for j, x in enumerate(row):
                if mask & (1 << j) or x == [0]:
                    continue
                term = mul(v, x)
                if (mask >> (j+1)).bit_count() % 2:
                    term = scale(term, -1)
                key = mask | (1 << j)
                new[key] = add(new.get(key, [Q(0)]), term)
        dp = new
    return dp.get((1 << size)-1, [Q(0)])


def expand_u_in_r(a):
    out = [Q(0)] * (2*len(a)-1)
    for i, c in enumerate(a):
        out[2*i] = c
    return trim(out)


def unit_coefficients(a):
    # Complete power map after u=1+v/4, with no sampling.
    out = [Q(0)] * len(a)
    for j, c in enumerate(a):
        for k in range(j+1):
            out[k] += c*comb(j, k)/4**k
    return trim(out)


def bernstein(a):
    n = len(a)-1
    return [sum(a[j]*Q(comb(k, j), comb(n, j)) for j in range(k+1))
            for k in range(n+1)]


def strings(a):
    return [str(x) for x in a]


def zstrings(a):
    return list(map(strings, a))


def original_powers(f, count=5):
    # Monic degree-eight Newton recurrence, in QQ[r].
    out = [[Q(8)]]
    for k in range(1, count+1):
        value = scale(f[8-k], -k)
        for j in range(1, k):
            value = sub(value, mul(f[8-j], out[k-j]))
        out.append(value)
    return out


def zero_matrix():
    return [[Q(0) for _ in range(7)] for _ in range(7)]


def identity(c=Q(1)):
    out = zero_matrix()
    for i in range(7):
        out[i][i] = c
    return out


def matrix_add(a, b):
    return [[a[i][j]+b[i][j] for j in range(7)] for i in range(7)]


def matrix_mul(a, b):
    out = zero_matrix()
    for i in range(7):
        for k in range(7):
            if a[i][k]:
                for j in range(7):
                    if b[k][j]:
                        out[i][j] += a[i][k]*b[k][j]
    return out


def matrix_scale(a, c):
    return [[v*c for v in row] for row in a]


def matrix_inverse(a):
    out = [row[:] + e for row, e in zip(a, identity())]
    for j in range(7):
        pivot = next((i for i in range(j, 7) if out[i][j]), None)
        require(pivot is not None, "singular seven-slot derivative")
        out[j], out[pivot] = out[pivot], out[j]
        t = out[j][j]
        out[j] = [v/t for v in out[j]]
        for i in range(7):
            if i != j and out[i][j]:
                t = out[i][j]
                out[i] = [v-t*w for v, w in zip(out[i], out[j])]
    return [row[7:] for row in out]


def matrix_eval(a, H):
    out = zero_matrix()
    for c in reversed(a):
        out = matrix_add(matrix_mul(out, H), identity(c))
    return out


def matrix_trace(a):
    return sum(a[i][i] for i in range(7))


def seven_slot_cases(f_generic, num, den):
    rows = []
    for r in (Q(101, 100), Q(11, 10), Q(10, 9)):
        B = 1+2*r*r-r**4-r**6
        require(r > 1 and B > 0, "nonphysical literal parameter")
        f = [evaluate(a, r) for a in f_generic]
        h = [(i+1)*f[i+1]/8 for i in range(8)]
        H = zero_matrix()
        for j in range(6):
            H[j+1][j] = Q(1)
        for j in range(7):
            H[j][6] = -h[j]
        derivative = matrix_eval([(i+1)*h[i+1] for i in range(7)], H)
        inverse = matrix_inverse(derivative)
        require(matrix_mul(derivative, inverse) == identity(),
                "whole seven-slot derivative-inverse identity")
        mass = matrix_scale(matrix_mul(matrix_eval(f, H), inverse), -8)
        N, X = -2*f[6], (-2*f[6])**2/2-4*f[4]
        D = X-N*N/8
        require(matrix_trace(mass) == N and D > 0,
                "actual seven-slot mass or norm bridge")
        eta = matrix_trace(matrix_mul(mass, mass))
        C = (N*N-eta)/D
        require(C == evaluate(num, r*r)/evaluate(den, r*r) and C < 16,
                "actual seven-slot angular formula")
        powers = [evaluate(a, r) for a in original_powers(f_generic)]
        require(powers[1] == powers[3] == powers[5] == 0 and powers[2] == N,
                "actual original moment interpretation")
        rows.append({"r": str(r), "B": str(B),
                     "all_original_first_five_powers": strings(powers),
                     "full_f_coefficients": strings(f),
                     "full_h_coefficients": strings(h),
                     "N": str(N), "X": str(X), "D": str(D),
                     "raw_mass_trace": str(matrix_trace(mass)),
                     "raw_eta": str(eta), "angular_C": str(C)})
    return rows


def build_record(cert):
    require(type(cert) is dict and set(cert) == KEYS, "certificate exact key set")
    require(type(cert["domain"]) is str and cert["domain"] == DOMAIN,
            "certificate domain")
    require(type(cert["critical_quartic"]) is list
            and len(cert["critical_quartic"]) == 5, "quartic dimension")
    require(type(cert["inverse_numerators"]) is list
            and len(cert["inverse_numerators"]) == 4, "inverse dimension")
    H4 = [vector(a) for a in cert["critical_quartic"]]
    Delta = vector(cert["inverse_common_denominator"])
    invnum = [vector(a) for a in cert["inverse_numerators"]]
    declared_disc = vector(cert["discriminant"])
    disc_quotient = vector(cert["discriminant_divided_by_inverse_denominator"])
    num, den = (vector(cert[k], 19) for k in
                ("angular_numerator_u", "angular_denominator_u"))
    declared_den_bern = vector(cert["complete_bernstein_denominator"], 19)
    declared_gap_bern = vector(cert["complete_bernstein_divided_gap"], 18)
    require(H4[-1] == [1] and Delta[-1] == 1,
            "monic quartic and common inverse denominator")

    # The direct classification's stationary identity, before p=r+r^3.
    parameter = [Q(0), Q(1)]
    d2_p = [[Q(1)], scale(parameter, -1), [Q(1)]]
    q_p = [add(mul(parameter, parameter), [Q(1)]),
           scale(parameter, -2), [Q(1)]]
    cubic = [scale(mul(mul(parameter, parameter), parameter), -1),
             add(scale(mul(parameter, parameter), 3), [Q(1)]),
             scale(parameter, -3), [Q(1)]]
    derivative_ratio = zadd(zmul(zderiv(zmul(d2_p, d2_p)), q_p),
                            zscale(zmul(zmul(d2_p, d2_p), zderiv(q_p)), -1))
    require(derivative_ratio == zscale(zmul(d2_p, cubic), 2),
            "whole generic square/quadratic stationary identity")

    p = [Q(0), Q(1), Q(0), Q(1)]
    beta = [Q(0), Q(0), Q(0), Q(1)]
    B = [Q(1), Q(0), Q(2), Q(0), Q(-1), Q(0), Q(-1)]
    d2 = [[Q(1)], scale(p, -1), [Q(1)]]
    D3 = zmul(d2, [beta, [Q(1)]])
    Q2 = [B, [Q(0), Q(2)], [Q(1)]]
    f = zmul(zmul(D3, D3), Q2)
    gU = zmul(d2, d2)
    gL = zmul(zmul([scale(beta, -1), [Q(1)]],
                  [scale(beta, -1), [Q(1)]]), [B, [Q(0), Q(-2)], [Q(1)]])
    tau = mul(mul([Q(-1), Q(0), Q(1)], [Q(-1), Q(0), Q(1)]),
              [Q(1), Q(0), Q(1)])
    q = [add(mul(p, p), [Q(1)]), scale(p, -2), [Q(1)]]
    require(zadd(gU, [scale(mul(tau, v), -1) for v in q]) == gL,
            "entire original-quartet factorization")
    powers = original_powers(f)
    require(powers[1] == powers[3] == powers[5] == [0],
            "entire first-third-fifth original moments")
    h = zscale(zderiv(f), Q(1, 8))
    quotient, remainder = zdiv(h, D3)
    require(remainder == [[0]] and quotient == H4,
            "entire actual derivative factorization")
    Hprime = zderiv(H4)
    disc = resultant(H4, Hprime)
    require(disc == declared_disc, "entire Sylvester discriminant")
    require(mul(Delta, disc_quotient) == disc,
            "whole inverse denominator discriminant divisibility")
    inverse_quotient, inverse_remainder = zdiv(zmul(Hprime, invnum), H4)
    require(inverse_remainder == [Delta], "entire derivative inverse identity")
    mass = zdiv(zmul(zscale(zmul(D3, Q2), -8), invnum), H4)[1]
    mass2 = zdiv(zmul(mass, mass), H4)[1]
    a, b, c = H4[3], H4[2], H4[1]
    tracepowers = [[Q(4)], scale(a, -1), sub(mul(a, a), scale(b, 2)),
                   sub(add(scale(mul(mul(a, a), a), -1),
                           scale(mul(a, b), 3)), scale(c, 3))]

    def trace(coefficients):
        out = [Q(0)]
        for i, coefficient in enumerate(coefficients):
            out = add(out, mul(coefficient, tracepowers[i]))
        return out

    N, X = powers[2], powers[4]
    require(N == scale(f[6], -2), "whole norm coefficient bridge")
    D = sub(X, scale(mul(N, N), Q(1, 8)))
    mass_trace, eta_num = trace(mass), trace(mass2)
    require(mass_trace == mul(N, Delta), "entire raw mass normalization")
    numerator = sub(mul(mul(N, N), mul(Delta, Delta)), eta_num)
    lhs = mul(numerator, expand_u_in_r(den))
    rhs = mul(mul(D, mul(Delta, Delta)), expand_u_in_r(num))
    require(lhs == rhs, "entire degree-120 actual angular identity")
    gap = sub(scale(den, 16), num)
    divided_gap, rem = divide(gap, [Q(-1), Q(1)])
    require(rem == [0], "whole uniform-edge gap divisibility")
    den_unit, gap_unit = unit_coefficients(den), unit_coefficients(divided_gap)
    den_bern, gap_bern = bernstein(den_unit), bernstein(gap_unit)
    require(den_bern == declared_den_bern, "whole denominator Bernstein vector")
    require(gap_bern == declared_gap_bern, "whole divided-gap Bernstein vector")
    require(all(x > 0 for x in den_bern+gap_bern), "strict complete positivity")
    require(sum(num) == 16*sum(den) and sum(den) > 0,
            "sharp uniform-edge rational limit")
    physical_B = [Q(1), Q(2), Q(-1), Q(-1)]
    require(evaluate(physical_B, Q(5, 4)) == Q(-1, 64),
            "physical B boundary containment")
    return {
        "status": "whole exact identities and signs passed",
        "actual_agent": "six-sendov-2", "role": "researcher",
        "claim_status": "complete ordinary author proof; unformalized and independently unreviewed",
        "domain": DOMAIN, "coefficient_order": "ascending powers, including interior zeros",
        "generic_stationary_identity_QQ_p_z": zstrings(derivative_ratio),
        "upper_quartic_QQ_r_z": zstrings(gU),
        "lower_quartic_QQ_r_z": zstrings(gL),
        "q_QQ_r_z": zstrings(q), "tau_QQ_r": strings(tau),
        "D3_QQ_r_z": zstrings(D3), "Q2_QQ_r_z": zstrings(Q2),
        "full_original_f_QQ_r_z": zstrings(f),
        "full_critical_h_QQ_r_z": zstrings(h),
        "all_original_first_five_powers_QQ_r": zstrings(powers),
        "critical_quartic_QQ_r_z": zstrings(H4),
        "inverse_common_denominator_QQ_r": strings(Delta),
        "inverse_numerators_QQ_r_z": zstrings(invnum),
        "inverse_identity_quotient_QQ_r_z": zstrings(inverse_quotient),
        "whole_discriminant_QQ_r": strings(disc),
        "discriminant_quotient_QQ_r": strings(disc_quotient),
        "raw_mass_numerator_remainder_QQ_r_z": zstrings(mass),
        "raw_mass_squared_numerator_remainder_QQ_r_z": zstrings(mass2),
        "quartic_trace_powers_QQ_r": zstrings(tracepowers),
        "raw_mass_trace_numerator_QQ_r": strings(mass_trace),
        "raw_eta_numerator_QQ_r": strings(eta_num),
        "N_QQ_r": strings(N), "X_QQ_r": strings(X), "D_QQ_r": strings(D),
        "whole_cleared_angular_identity_both_sides_QQ_r": strings(lhs),
        "identity_degrees_r": {"discriminant": len(disc)-1,
                               "cleared_angular": len(lhs)-1},
        "angular_numerator_u": strings(num), "angular_denominator_u": strings(den),
        "divided_gap_u": strings(divided_gap),
        "denominator_power_after_u_1_plus_v_over_4": strings(den_unit),
        "divided_gap_power_after_u_1_plus_v_over_4": strings(gap_unit),
        "complete_bernstein_denominator": strings(den_bern),
        "complete_bernstein_divided_gap": strings(gap_bern),
        "physical_B_u": strings(physical_B), "B_at_5_over_4": "-1/64",
        "Num_at_1": str(sum(num)), "Den_at_1": str(sum(den)), "sharp_limit": "16",
        "seven_slot_cases": seven_slot_cases(f, num, den),
        "angular_bound": "C<16 for every physical member; supremum16 only as r descends1",
    }


def self_test(cert):
    changes = [
        ("critical_quartic", (0, 0)), ("inverse_numerators", (0, 0)),
        ("inverse_common_denominator", (0,)), ("discriminant", (0,)),
        ("angular_numerator_u", (0,)), ("angular_denominator_u", (0,)),
        ("complete_bernstein_denominator", (0,)),
        ("complete_bernstein_divided_gap", (0,)),
    ]
    for key, indices in changes:
        damaged = deepcopy(cert)
        target = damaged[key]
        for index in indices[:-1]:
            target = target[index]
        index = indices[-1]
        target[index] = str(Q(target[index])+1)
        try:
            build_record(damaged)
        except ValueError:
            continue
        raise ValueError("semantic certificate damage was accepted: " + key)
    return len(changes)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=BASE/"CERTIFICATE.json")
    parser.add_argument("--expected", type=Path, default=BASE/"EXPECTED.json")
    parser.add_argument("--record", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    cert = load_json(args.certificate)
    record = build_record(cert)
    data = canonical(record)
    fixture = load_json(args.expected)
    # Canonical byte equality distinguishes booleans/numbers/strings and every
    # coefficient, rejecting missing/extra keys and altered inner dimensions.
    require(canonical(fixture) == data, "whole typed expected record mismatch")
    controls = self_test(cert) if args.self_test else 0
    if args.record:
        args.record.write_bytes(data)
    print(json.dumps({"status": record["status"], "record_bytes": len(data),
                      "record_sha256": sha256(data).hexdigest(),
                      "semantic_rejections": controls,
                      "angular_bound": record["angular_bound"]}, sort_keys=True))


if __name__ == "__main__":
    main()
