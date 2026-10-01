#!/usr/bin/env python3
"""Exact three-cube construction, small LMI, and uniform sign certificates.

Python standard library only. Local verify.py supplies the separately published
definition-level checker, cube baseline, lift and ordinary shifted union.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import argparse
import json
import verify as base


class Polynomial:
    """Sparse exact Q[x,y,z], canonical exponent triples."""
    def __init__(self, data):
        if isinstance(data, (int, F)):
            data = {(0, 0, 0): data}
        base.require(all(len(e) == 3 and all(isinstance(k, int) and k >= 0 for k in e)
                         for e in data), "invalid polynomial exponent")
        self.terms = {e: F(c) for e, c in data.items() if c}

    def __add__(self, other):
        other = other if isinstance(other, Polynomial) else Polynomial(other)
        out = defaultdict(F, self.terms)
        for exponent, coefficient in other.terms.items():
            out[exponent] += coefficient
        return Polynomial(out)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Polynomial) else Polynomial(other)
        out = defaultdict(F)
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                out[tuple(a + b for a, b in zip(e, f))] += c * d
        return Polynomial(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        base.require(isinstance(exponent, int) and exponent >= 0, "bad polynomial power")
        out = Polynomial(1)
        for _ in range(exponent):
            out = out * self
        return out

    def evaluate(self, values):
        return sum(c * values[0]**e[0] * values[1]**e[1] * values[2]**e[2]
                   for e, c in self.terms.items())

    def certificate(self):
        return [[list(e), str(c)] for e, c in sorted(self.terms.items())]


def scalar_invariants(t, u, v):
    """Denominator-free frame formulas; also accepts Polynomial parameters."""
    a0 = t - 1
    a = t - 2 * u + 1
    b = t - 2 * v + 1
    n = 2 * (t + u + v) - 2
    du = a0*a0 + 2*u - 2
    dv = a0*a0 + 2*v - 2
    heron = 4*a*a*b*b - (a0*a0 - a*a - b*b)**2
    second_num = heron * ((a0 + 2) * (du*b*b + dv*a*a) + a0*du*dv)
    quad_num = 4*a*a*b*b*a0*a0 * (a0*n*n - n*(3*a0*a0 + n - 4)) + second_num
    trace_num = 2*n*a0 - 3*a0*a0 - n + 4
    return heron, quad_num, trace_num, second_num


def sign_certificates():
    x = Polynomial({(1, 0, 0): 1})
    y = Polynomial({(0, 1, 0): 1})
    z = Polynomial({(0, 0, 1): 1})
    v = 1 + x
    u = v + y
    t = 4*u + z
    polys = scalar_invariants(t, u, v)[:3]
    names = ("heron_numerator", "cap_quadratic_numerator", "twice_N_minus_trace_numerator")
    expected_terms = (34, 219, 10)
    expected_constants = (243, 168399, 27)
    certificates = {}
    summaries = {}
    for name, poly, count, constant in zip(names, polys, expected_terms, expected_constants):
        base.require(len(poly.terms) == count, "unexpected polynomial term count")
        base.require(poly.terms[(0, 0, 0)] == constant, "wrong polynomial constant")
        base.require(all(c > 0 and c.denominator == 1 for c in poly.terms.values()),
                     "nonpositive or nonintegral margin coefficient")
        certificate = poly.certificate()
        certificates[name] = certificate
        encoding = json.dumps(certificate, separators=(",", ":")).encode()
        summaries[name] = {"terms": count, "constant": constant,
                           "minimum_coefficient": str(min(poly.terms.values())),
                           "maximum_total_degree": max(sum(e) for e in poly.terms),
                           "sha256": sha256(encoding).hexdigest()}
    # Evaluate the expanded coefficient lists against direct scalar arithmetic.
    fixtures = [(0, 0, 0), (1, 2, 3), (F(1, 3), F(2, 5), F(7, 11)),
                (4, 0, 13), (0, 8, 0), (2, 3, 17)]
    for values in fixtures:
        vx = 1 + values[0]
        ux = vx + values[1]
        tx = 4*ux + values[2]
        direct = scalar_invariants(tx, ux, vx)[:3]
        base.require(tuple(p.evaluate(values) for p in polys) == direct,
                     "expanded/direct polynomial mismatch")
    return certificates, {"polynomials": summaries, "scalar_evaluation_fixtures": len(fixtures)}


def balanced_gram(t, u, v):
    a = F(t - 2*u + 1, t - 1)
    b = F(t - 2*v + 1, t - 1)
    base.require(a > 0 and b > 0 and a+b > 1 and abs(a-b) < 1,
                 "nondegenerate triangle required")
    p = (1 + a*a - b*b) / (2*a)
    q = (1 + b*b - a*a) / (2*b)
    r = (1 - a*a - b*b) / (2*a*b)
    g = [[F(1), p, q], [p, F(1), r], [q, r, F(1)]]
    return [[(t-1)*e for e in row] for row in g]


def small_parameters(stars):
    t, u, v = stars
    n = 2*(t+u+v)-2
    base.require(all(isinstance(w, int) and w >= 1 and w & (w-1) == 0 for w in stars),
                 "cube stars must be positive powers of two")
    base.require(t >= u >= v >= 1 and t >= 2, "wrong stars")
    if t == u == v:
        g = [[F((t-1)*int(i == j)) for j in range(3)] for i in range(3)]
        beta, regime = F(2*t), "equal_star_prior_closure"
    elif t == u:
        g = [[F(t-1), F(1-t), F(0)], [F(1-t), F(t-1), F(0)],
             [F(0), F(0), F(t-1)]]
        beta, regime = F(n - 2*(t+1)), "two_largest_opposite"
    elif u == v == 1:
        g = balanced_gram(t, u, v)
        beta, regime = F(2), "two_singletons"
    elif t == 2*u and v == 1:
        g = balanced_gram(t, u, v)
        beta, regime = F(1, t-1), "adjacent_singleton_trace"
    elif t == 2*u:
        g = [[F(t-1) for _ in range(3)] for _ in range(3)]
        beta = F(2*(v-1)*(t-2*v+2), t-1)
        regime = "adjacent_aligned"
    else:
        base.require(t >= 4*u, "missing power-of-two regime")
        g = balanced_gram(t, u, v)
        a0, a, b = t-1, t-2*u+1, t-2*v+1
        h, qn, trace_numerator, second_num = scalar_invariants(F(t), F(u), F(v))
        base.require(h > 0 and qn > 0 and trace_numerator > 0, "balanced margin signs")
        denominator = 4*a*a*b*b*a0**3
        cap_quadratic = qn / denominator
        beta = min(F(n-2*t), cap_quadratic/n)
        regime = "widely_unequal_balanced"
        # Independent trace / 2nd elementary-symmetric calculation from G,D.
        d = [1 + F(2*w-2, a0*a0) for w in stars]
        trace = sum(d[i]*g[i][i] for i in range(3))
        second = sum(d[i]*d[j]*(g[i][i]*g[j][j] - g[i][j]**2)
                     for i in range(3) for j in range(i+1, 3))
        base.require(trace == 3*a0 + F(n-4, a0), "balanced trace formula")
        base.require(second == second_num/denominator, "balanced second coefficient")
        base.require(cap_quadratic == n*n-n*trace+second, "balanced quadratic formula")
    base.require(beta > 0, "nonpositive cap margin")
    return g, beta, regime


def check_small_lmi(stars, g, beta):
    """Sherman--Morrison inverse of D+alpha alpha^T, exact 3-by-3 PSD."""
    t = stars[0]
    n = 2*sum(stars)-2
    base.require(all(g[i][i] == t-1 for i in range(3)), "bad Gram diagonal")
    gram_rank = base.psd_rank(g)
    alpha = [F(t-2*u+1, t-1) for u in stars]
    d_inverse = [1/(1+F(2*u-2, (t-1)**2)) for u in stars]
    denominator = 1 + sum(alpha[i]**2*d_inverse[i] for i in range(3))
    inverse = [[d_inverse[i]*int(i == j)
                - d_inverse[i]*alpha[i]*alpha[j]*d_inverse[j]/denominator
                for j in range(3)] for i in range(3)]
    r = [[F(int(i == j))/d_inverse[i] + alpha[i]*alpha[j]
          for j in range(3)] for i in range(3)]
    base.require(all(sum(r[i][k]*inverse[k][j] for k in range(3)) == int(i == j)
                     for i in range(3) for j in range(3)), "incorrect R inverse")
    margin = [[(n-beta)*inverse[i][j] - g[i][j] for j in range(3)] for i in range(3)]
    rank_margin = base.psd_rank(margin)
    base.require(base.psd_rank([[n*inverse[i][j]-g[i][j] for j in range(3)]
                               for i in range(3)]) == 3, "nonstrict upper small LMI")
    return {"Gram_rank": gram_rank, "margin_LMI_rank": rank_margin,
            "Gram_sha256": base.fingerprint(g)}


def three_cubes(orders):
    base.require(len(orders) == 3 and all(isinstance(a, int) and 1 <= a <= 12 for a in orders),
                 "three positive cube orders required")
    base.require(list(orders) == sorted(orders, reverse=True), "orders must be decreasing")
    base.require(sum(2**a for a in orders)-2 <= 80, "literal matrix order exceeds fixed 80 limit")
    parts = [base.cube(a) for a in orders]
    stars = [part[2] for part in parts]
    t = stars[0]
    family, shifted, _, _ = base.union_parts(parts, equal=False)
    n = len(family)
    if t == 1:
        meta = {"orders": list(orders), "regime": "rank_one_prior_baseline", "beta": "4",
                "epsilon": "0", "forced_nullity": 3}
        return (family, shifted, t, "three_cubes(1,1,1)"), shifted, meta
    g, beta, regime = small_parameters(stars)
    small_check = check_small_lmi(stars, g, beta)
    branch_vertices = [(branch, mask, len(part[0])-1)
                       for branch, part in enumerate(parts) for mask in part[0][1:]]
    c = []
    for i, a, full_i in branch_vertices:
        row = []
        for j, b, full_j in branch_vertices:
            if i == j:
                if a == b:
                    value = F(t-1)
                elif a == full_i or b == full_j:
                    value = F(-1)
                elif a ^ b == full_i:
                    value = F(1+t*(2*stars[i]-t-2), t-1)
                else:
                    value = F(-1)
            else:
                ci = F(1) if a == full_i else F(-1, t-1)
                cj = F(1) if b == full_j else F(-1, t-1)
                value = ci*cj*g[i][j]
            row.append(value)
        c.append(row)
    capped = base.lift(c, t)
    shifted_core = base.core(shifted, t)
    q = (n-1)*(t-1) + sum(w-1 + (t-w)*(2*w-1) for w in stars)
    actual_q = sum(shifted_core[i][i] for i in range(n-1)) + sum(map(sum, shifted_core))
    base.require(actual_q == q and q > 0, "shifted trace formula")
    epsilon = beta/(2*(beta+q))
    mixed = [[(1-epsilon)*capped[i][j]+epsilon*shifted[i][j]
              for j in range(n)] for i in range(n)]
    mixed_core = [[(1-epsilon)*c[i][j]+epsilon*shifted_core[i][j]
                   for j in range(n-1)] for i in range(n-1)]
    base.require(base.lift(mixed_core, t) == mixed, "full/core mixtures disagree")
    meta = {"orders": list(orders), "stars": stars, "regime": regime,
            "beta": str(beta), "shifted_Q_trace": q, "epsilon": str(epsilon),
            "upper_gap_bound": str(beta/(2*(n-t))),
            "forced_nullity": stars.count(t)*t, **small_check}
    return (family, mixed, t, "three_cubes("+",".join(map(str, orders))+")"), capped, meta


def full_margin(matrix, s, gamma):
    n = len(matrix)
    slack = [[(n-s)*(int(i == j)-matrix[i][j])
              -gamma*(int(i == j)-F(1, n)) for j in range(n)] for i in range(n)]
    return base.psd_rank(slack)


def many_cubes(orders):
    """Three-branch packets + credited equal-star union; r<=3k only."""
    base.require(len(orders) >= 2 and all(isinstance(a, int) and 1 <= a <= 12 for a in orders),
                 "positive cube orders required")
    base.require(list(orders) == sorted(orders, reverse=True), "orders must be decreasing")
    base.require(sum(2**a for a in orders)-(len(orders)-1) <= 80, "literal order exceeds 80")
    k = orders.count(orders[0])
    base.require(len(orders) <= 3*k, "assembly requires r<=3k")
    packets = [[orders[0]] for _ in range(k)]
    for i, a in enumerate(orders[k:]):
        packets[i % k].append(a)
    factors = []
    for packet in packets:
        if len(packet) == 1:
            factors.append(base.cube(packet[0]))
        elif len(packet) == 2:
            factors.append(base.unequal_cubes(*packet)[0])
        else:
            factors.append(three_cubes(tuple(packet))[0])
    part = factors[0] if k == 1 else base.union_parts(factors)
    gamma = None if k == 1 else base.quantitative_gap(factors, part[1], part[2])
    return part, {"orders": list(orders), "r": len(orders), "k": k,
                  "packet_orders": packets, "scaled_upper_gap": gamma,
                  "forced_nullity": k*part[2]}


def run():
    coefficients, polynomial_summary = sign_certificates()
    triples = [tuple(reversed(a)) for a in combinations_with_replacement(range(1, 5), 3)]
    triples += [(5, 4, 3), (5, 4, 4), (6, 2, 1), (6, 3, 2)]
    entries = []
    regimes = defaultdict(int)
    built = {}
    for orders in triples:
        part, seed, meta = three_cubes(orders)
        family, matrix, s, label = part
        checked = base.check(family, matrix, s)
        base.require(checked["lower_rank"] == len(family)-meta["forced_nullity"], "wrong maximal rank")
        base.require(checked["upper_rank"] == len(family)-1, "unit endpoint not simple")
        seed_check = base.check(family, seed, s)
        full_margin(seed, s, F(meta["beta"]))
        full_margin(matrix, s, F(meta["beta"])/2)
        checked.update(label=label, **meta, seed_matrix_sha256=seed_check["matrix_sha256"],
                       seed_lower_rank=seed_check["lower_rank"])
        entries.append(checked)
        regimes[meta["regime"]] += 1
        built[orders] = part
    assemblies = []
    for orders in [(3, 3, 2, 1), (3, 3, 2, 1, 1), (3, 3, 2, 2, 1, 1),
                   (2, 2, 2, 1, 1, 1), (3, 3, 3, 2, 2, 1, 1)]:
        part, meta = many_cubes(orders)
        family, matrix, s, label = part
        checked = base.check(family, matrix, s)
        base.require(checked["lower_rank"] == len(family)-meta["forced_nullity"], "packet maximal rank")
        base.require(checked["upper_rank"] == len(family)-1, "packet unit simplicity")
        checked.update(label=label, **meta)
        assemblies.append(checked)
    products = []
    fixtures = [[built[(2, 1, 1)], built[(2, 1, 1)]],
                [built[(2, 1, 1)], built[(1, 1, 1)]],
                [built[(2, 2, 1)], built[(1, 1, 1)]]]
    old_unequal = base.unequal_cubes(2, 1)[0]
    fixtures.append([built[(2, 1, 1)], old_unequal])
    for factors in fixtures:
        family, matrix, s, label = base.tensor_parts(factors)
        density = max(F(p[2], len(p[0])) for p in factors)
        eligible = [i for i, p in enumerate(factors) if F(p[2], len(p[0])) == density]
        forced = sum(len(factors[i][0])-base.check(*factors[i][:3])["lower_rank"] for i in eligible)
        checked = base.check(family, matrix, s)
        base.require(checked["lower_rank"] == len(family)-forced, "product forced kernel")
        base.require(checked["upper_rank"] == len(family)-1, "product upper simplicity")
        checked.update(label=label, eligible_factors=eligible, forced_nullity=forced)
        products.append(checked)
    sunflower = []
    for c, orders in [(1, (3, 2, 1)), (2, (3, 2, 1)), (1, (2, 2, 1)), (1, (1, 1, 1))]:
        family, matrix, s, label = base.tensor_parts([base.cube(c), built[orders]])
        checked = base.check(family, matrix, s)
        base.require(2*s == len(family), "sunflower largest star")
        base.require(checked["lower_rank"] == len(family)-2**(c-1), "sunflower lower rank")
        base.require(checked["upper_rank"] == len(family)-2**(c-1), "sunflower upper rank")
        checked.update(label=label, common_core_order=c, petal_orders=list(orders))
        sunflower.append(checked)
    controls = []
    def reject(label, fn):
        base.expect_error(fn)
        controls.append(label)
    reject("bad_order_count", lambda: three_cubes((3, 2)))
    reject("unsorted_orders", lambda: three_cubes((1, 3, 2)))
    reject("zero_order", lambda: three_cubes((3, 2, 0)))
    reject("noninteger_order", lambda: three_cubes((3, 2, F(3, 2))))
    reject("constructor_size_bound", lambda: three_cubes((13, 1, 1)))
    reject("literal_matrix_size_bound", lambda: three_cubes((6, 6, 1)))
    reject("invalid_triangle", lambda: balanced_gram(8, 4, 2))
    reject("non_power_two_gap", lambda: small_parameters((7, 3, 2)))
    reject("insufficient_largest_packets", lambda: many_cubes((4, 2, 1, 1)))
    reject("unsorted_packet_orders", lambda: many_cubes((2, 3, 3, 1)))
    g, beta, _ = small_parameters((8, 2, 1))
    wrong = [row[:] for row in g]
    wrong[0][0] += 1
    reject("Gram_diagonal", lambda: check_small_lmi((8, 2, 1), wrong, beta))
    reject("false_margin", lambda: check_small_lmi((8, 2, 1), g, F(17)))
    f, matrix, s, _ = built[(2, 1, 1)]
    bad = [row[:] for row in matrix]
    bad[1][1] = 1
    reject("support_corruption", lambda: base.check(f, bad, s))
    reject("wrong_star", lambda: base.check(f, matrix, s+1))
    bad_poly = Polynomial({(0, 0, 0): -1, (1, 0, 0): 2})
    reject("nonpositive_polynomial", lambda: base.require(all(c > 0 for c in bad_poly.terms.values()), "bad sign"))
    reject("malformed_polynomial_exponent", lambda: Polynomial({(-1, 0, 0): 2}))
    result = {"claim_status": "author-checked unformalized proof with exact finite polynomial sign certificate",
              "polynomial_signs": polynomial_summary, "three_cubes": entries,
              "many_cube_assemblies": assemblies,
              "products": products, "common_core_sunflowers": sunflower,
              "coverage": {"complete_sorted_order_1_to_4_triples": 20,
                           "additional_triples": 4, "regimes": dict(sorted(regimes.items())),
                           "largest_literal_matrix_order": max(r["N"] for r in entries+products+sunflower)},
              "rejection_controls": controls}
    return result, coefficients


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--coefficients", type=Path, required=True)
    args = parser.parse_args()
    result, coefficients = run()
    if args.write:
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        args.coefficients.write_text(json.dumps(coefficients, indent=2, sort_keys=True)+"\n")
    if args.check:
        base.require(json.loads(args.check.read_text()) == result, "result fixture mismatch")
        base.require(json.loads(args.coefficients.read_text()) == coefficients, "coefficient fixture mismatch")
    print(json.dumps({"ok": True, "coverage": result["coverage"],
                      "rejection_controls": len(result["rejection_controls"]),
                      "results_sha256": sha256((json.dumps(result, indent=2, sort_keys=True)+"\n").encode()).hexdigest(),
                      "coefficients_sha256": sha256((json.dumps(coefficients, indent=2, sort_keys=True)+"\n").encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
