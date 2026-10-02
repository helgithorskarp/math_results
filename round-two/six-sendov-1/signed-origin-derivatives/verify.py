#!/usr/bin/env python3
"""Whole exact author record, not a formal kernel or independent review."""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
E = Q(1, 100)
A0 = 1 - E
EXCESS = 4 + 3 * E
M = [Q(9, 16), Q(3, 5), Q(3, 4), Q(1), Q(7, 5), Q(17, 8), Q(7, 2), Q(1)]

def require(ok, why):
    if not ok:
        raise ValueError(why)

def clean(p):
    return {k: v for k, v in p.items() if v}

def mul3(p, q):
    r = {}
    for (i, j, t), x in p.items():
        for (k, l, s), y in q.items():
            key = (i + k, j + l, t + s)
            r[key] = r.get(key, Q(0)) + x * y
    return clean(r)

def face_product(p, k):
    f = {(0, 0, 0): Q(1)}
    for j in range(8 - p):
        term = {(0, 0, 0): Q(1), (1, 0, 1): Q(-1, 2)}
        if j < k:
            term[(1, 1, 1)] = -EXCESS / k
        f = mul3(f, term)
    g = {}
    for (i, j, t), v in f.items():
        key = (i + p, j)
        g[key] = g.get(key, Q(0)) + (-1) ** p * 9 * v / (p + t + 1)
    return clean(g)

def face_binomial(p, k):
    g = {}
    for i in range(9 - p - k):
        for j in range(k + 1):
            for l in range(j + 1):
                c = (Q((-1) ** (p + i + j) * 9 * comb(8 - p - k, i)
                       * comb(k, j) * comb(j, l), p + i + j + 1)
                     * Q(1, 2) ** (i + j - l))
                if l:
                    c *= (EXCESS / k) ** l
                key = (p + i + j, l)
                g[key] = g.get(key, Q(0)) + c
    return clean(g)

def box_power(f):
    g = {}
    for (i, j), v in f.items():
        for h in range(i + 1):
            key = (h, j)
            g[key] = g.get(key, Q(0)) + v * comb(i, h) * A0 ** (i - h) * E ** h
    return clean(g)

def bernstein(f, da, du):
    return [[sum((v * Q(comb(i, k), comb(da, k)) * Q(comb(j, l), comb(du, l))
                  for (k, l), v in f.items() if k <= i and l <= j), Q(0))
             for j in range(du + 1)] for i in range(da + 1)]

def inverse_bernstein(b, da, du):
    f = {}
    for i in range(da + 1):
        for j in range(du + 1):
            for k in range(da - i + 1):
                for l in range(du - j + 1):
                    key = (i + k, j + l)
                    c = (b[i][j] * comb(da, i) * comb(du, j)
                         * comb(da - i, k) * comb(du - j, l) * (-1) ** (k + l))
                    f[key] = f.get(key, Q(0)) + c
    return clean(f)

def sparse(f):
    return [[i, j, str(v)] for (i, j), v in sorted(f.items())]

def cmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

def cadd(z, w):
    return (z[0] + w[0], z[1] + w[1])

def cs(z, v):
    return (z[0] * v, z[1] * v)

def mixed(a, q, omitted):
    coeff = [(Q(1), Q(0))]
    for j, z in enumerate(q):
        if j in omitted:
            continue
        nxt = [(Q(0), Q(0)) for _ in range(len(coeff) + 1)]
        for k, x in enumerate(coeff):
            nxt[k] = cadd(nxt[k], x)
            nxt[k + 1] = cadd(nxt[k + 1], cs(cmul(x, z), -a))
        coeff = nxt
    p = len(omitted)
    value = (Q(0), Q(0))
    for k, z in enumerate(coeff):
        value = cadd(value, cs(z, Q(9) * (-a) ** p / (p + k + 1)))
    return value

def enc(z):
    return [str(z[0]), str(z[1])]

def literal(a, q):
    return {"a": str(a), "q": [enc(z) for z in q],
            "origin": enc(mixed(a, q, set())),
            "gradient": [enc(mixed(a, q, {j})) for j in range(8)],
            "ordered_hessian": [[enc(mixed(a, q, {j, k})) if j != k else ["0", "0"]
                                 for k in range(8)] for j in range(8)],
            "successive_distinct_partials": [enc(mixed(a, q, set(range(p)))) for p in range(1, 9)]}

def build():
    faces = []
    maxima = []
    for p in range(1, 9):
        values = []
        for k in range(9 - p):
            f = face_product(p, k)
            require(f == face_binomial(p, k), "entire differentiated face routes differ")
            g = box_power(f)
            b = bernstein(g, 8, k)
            require(inverse_bernstein(b, 8, k) == g, "entire tensor inverse differs")
            flat = [x for row in b for x in row]
            if p < 8:
                require(all(abs(x) < M[p - 1] for x in flat), "strict signed derivative coefficient fails")
            else:
                require(all(abs(x) <= 1 for x in flat), "eighth-order closed endpoint fails")
            values += flat
            faces.append({"order": p, "free": k, "tensor_degrees": [8, k],
                          "power_a_u": sparse(f), "power_v_u": sparse(g),
                          "bernstein": [[str(x) for x in row] for row in b],
                          "min": str(min(flat)), "max": str(max(flat))})
        maxima.append(max(abs(x) for x in values))
    require(len(faces) == 36 and sum(len(x["bernstein"]) * len(x["bernstein"][0]) for x in faces) == 1080,
            "whole finite family census differs")
    real_margins = [M[i] - maxima[i] for i in range(7)]
    taylor = [[M[p + k - 1] / factorial(k) for k in range(9 - p)] for p in range(1, 9)]
    eps = Q(1, 8)
    complex_values = [sum((x * eps ** k for k, x in enumerate(poly)), Q(0)) for poly in taylor]
    e = Q(1, 16000)
    d0 = Q(104960, 39)
    margins = {
        "complex_gradient": Q(2, 3) - complex_values[0],
        "complex_hessian": Q(3, 4) - complex_values[1],
        "product_gradient": 2 - Q(753, 700) ** 7,
        "seed_parameter_box": Q(1, 100) - e,
        "whole_phase_box": Q(1, 64) - 161 * e,
        "global_cost_rounding": Q(82) - Q(653, 8),
        "initial_E2": 28 * (1 - e) ** 2 - 26 - Q(7, 4),
        "coarse_v1": Q(7, 5) - 8 * d0 * e,
        "coarse_E2_25": 28 * (1 - e) ** 2 - Q(14, 5) - 25,
        "coarse_v2": Q(1, 10) - Q(14, 25) * d0 * e,
        "coarse_E2_27": 28 * (1 - e) ** 2 - Q(1, 5) - 27,
        "coarse_v3": Q(9, 100) - Q(14, 27) * d0 * e,
    }
    require(all(x > 0 for x in margins.values()) and all(x > 0 for x in real_margins), "strict scalar margin fails")
    ones = [(Q(1), Q(0))] * 8
    for p in range(1, 9):
        require(mixed(Q(1), ones, set(range(p))) == (Q((-1) ** p, comb(8, p)), Q(0)), "unit-tuple exact derivative anchor")
    r = [(Q(9, 2), Q(0))] + [(Q(1, 2), Q(0))] * 7
    q = list(r)
    q[1] = (Q(63, 130), Q(8, 65))
    positive = mixed(Q(1), r, {1})[0]
    loss = mixed(Q(1), r, set())[0] - mixed(Q(1), q, set())[0]
    require(positive == Q(1971, 3584) and loss == positive / 65 and loss > 0,
            "positive-gradient/full one-slot phase-loss control")
    controls = [literal(Q(1), ones), literal(A0, [(Q(1, 2), Q(0))] * 8),
                literal(Q(1), r), literal(Q(1), q)]
    rejected = {
        "real_gradient_half": Q(1, 2) - maxima[0],
        "real_hessian_half": Q(1, 2) - maxima[1],
        "seventh_order_three": Q(3) - maxima[6],
        "eighth_order_zero": -maxima[7],
        "complex_gradient_budget_three_fifths": Q(3, 5) - complex_values[0],
        "complex_hessian_budget_two_thirds": Q(2, 3) - complex_values[1],
        "global_nonpositive_gradient": -positive,
        "zero_phase_loss_on_all_envelopes": -loss,
    }
    require(all(x < 0 for x in rejected.values()), "bad budget or envelope control not rejected")
    return {"agent": "six-sendov-1", "role": "researcher", "a_interval": [str(A0), "1"],
            "real_floor": "1/2", "real_total_cap": "803/100", "excess": str(EXCESS),
            "real_bounds": [str(x) for x in M], "whole_faces": faces,
            "real_strict_margins": [str(x) for x in real_margins],
            "closed_order8_maximum": str(maxima[7]),
            "complete_complex_taylor_coefficients": [[str(x) for x in poly] for poly in taylor],
            "complex_eps_cap": "1/8", "complex_endpoint_values": [str(x) for x in complex_values],
            "strict_margins": {k: str(v) for k, v in margins.items()},
            "phase_coefficients": {"deficit": "9/16", "l1_square": "3/8", "normalized_phase": "525/8",
                                   "normalization": "16", "whole_cost": "653/8", "rounded": "82"},
            "coarse_d0": str(d0), "coarse_proportional_v": str(Q(14, 27) * d0),
            "whole_literal_controls": controls, "positive_gradient": str(positive), "phase_loss": str(loss),
            "literal_eps_squared": "1/65", "literal_deficit": "1/65",
            "rejected_mathematical_budgets": {k: str(v) for k, v in rejected.items()}}

def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def pairs(xs):
    d = {}
    for k, v in xs:
        require(k not in d, "duplicate JSON key")
        d[k] = v
    return d

def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON")))

def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def check_manifest():
    m = load(ROOT / "MANIFEST.json")
    require(m["schema"] == 1, "manifest schema")
    for name, digest in m["sha256"].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, "frozen source/fixture pin " + name)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bootstrap", action="store_true", help="author-only write new record, never default checking")
    p.add_argument("--expected", type=Path)
    p.add_argument("--export", type=Path)
    args = p.parse_args()
    if not args.bootstrap:
        check_manifest()
    v = build()
    if args.bootstrap:
        (ROOT / "EXPECTED.json").write_text(json.dumps(v, indent=2) + "\n")
    else:
        require(same(v, load(args.expected or ROOT / "EXPECTED.json")), "entire typed record differs")
    if args.export:
        args.export.write_text(json.dumps(v, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "whole_record_sha256": hashlib.sha256(canonical(v)).hexdigest(),
                      "complete_faces": 36, "tensor_coefficients": 1080, "real_strict_bounds": 7,
                      "strict_scalar_margins": len(v["strict_margins"]), "whole_literal_controls": 4,
                      "rejected_mathematical_budgets": len(v["rejected_mathematical_budgets"])}))

if __name__ == "__main__":
    main()
