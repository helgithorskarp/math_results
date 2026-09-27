#!/usr/bin/env python3
"""Exact controls for a conditional Gaussian defect reduction, not a sign oracle."""
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import isqrt, lcm
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def rat(x):
    require(type(x) in (int, str), "rational input must be integer or string")
    return F(x)


def point(x):
    require(isinstance(x, list) and len(x) == 3, "point dimension")
    return tuple(rat(a) for a in x)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def d2(a, b):
    v = sub(a, b)
    return dot(v, v)


def group():
    return tuple(sorted(tuple(s[i]*(p[i]+1) for i in range(3))
                        for p in itertools.permutations(range(3))
                        for s in itertools.product((-1, 1), repeat=3)))


def act(g, x):
    return tuple((1 if j > 0 else -1)*x[abs(j)-1] for j in g)


def compose(g, h):
    return tuple((1 if j > 0 else -1)*h[abs(j)-1] for j in g)


def ceil_sqrt(q):
    require(q >= 0, "negative square-root budget")
    n = isqrt(q.numerator // q.denominator)
    return n if n*n == q else n+1


def validate(data):
    p = tuple(point(x) for x in data["source"])
    q = tuple(point(x) for x in data["target"])
    weights = tuple(rat(x) for x in data["weights"])
    require(len(p) == len(q) == len(weights) and len(p) > 0, "list lengths")
    require(len(set(p)) == len(p), "merge repeated source centres first")
    require(all(w > 0 for w in weights) and sum(weights) == 1, "probability weights")
    radius, variance = rat(data["radius"]), rat(data["variance"])
    k, length = data["bits"], data["length"]
    eta = rat(data["requested_error"])
    require(radius >= 1 and variance > 0 and eta > 0, "positive parameters")
    require(type(k) is int and k >= 1, "positive integer bits")
    require(type(length) is int, "integer separation")
    require(all(dot(x, x) <= radius*radius for x in p+q), "radius guard")
    for i in range(len(p)):
        for j in range(i):
            require(d2(p[i], p[j]) >= d2(q[i], q[j]), "input does not contract")
    require(length >= 16*radius, "cross-block guard")
    require((length-4*radius)**2 >= 32*variance*k, "tail exponent guard")
    require(F(47, 2**k) <= eta, "requested error guard")
    return p, q, weights, radius, variance, k, length, eta


def construct(data):
    p, q, weights, radius, variance, k, length, eta = validate(data)
    gs = group()
    v = (1, 2, 3)
    pp, qq, ww, blocks = [], [], [], []
    for b, g in enumerate(gs):
        for x, y, weight in zip(p, q, weights):
            pp.append(act(g, tuple(length*v[i]+x[i] for i in range(3))))
            qq.append(act(g, tuple(F(length, 2)*v[i]+y[i] for i in range(3))))
            ww.append(weight/48)
            blocks.append(b)
    require(len(set(pp)) == len(pp), "source block collision")
    return tuple(pp), tuple(qq), tuple(ww), tuple(blocks)


def direct_pairs(p, q, blocks):
    """Definition-level integer check, independent of the triangle bound."""
    den = lcm(*(a.denominator for x in p+q for a in x))
    ip = [tuple(int(den*a) for a in x) for x in p]
    iq = [tuple(int(den*a) for a in x) for x in q]
    counts = {"pairs": 0, "within_tight": 0, "within_strict": 0,
              "cross_strict": 0}
    min_cross = None
    for i in range(len(p)):
        for j in range(i):
            loss = d2(ip[i], ip[j])-d2(iq[i], iq[j])
            require(loss >= 0, "constructed expanding pair")
            counts["pairs"] += 1
            if blocks[i] != blocks[j]:
                require(loss > 0, "non-strict cross pair")
                counts["cross_strict"] += 1
                min_cross = loss if min_cross is None else min(min_cross, loss)
            else:
                counts["within_tight" if loss == 0 else "within_strict"] += 1
    counts["minimum_cross_squared_loss"] = str(F(min_cross, den*den))
    return counts


def moments(points, weights):
    mean = tuple(sum(w*x[j] for x, w in zip(points, weights)) for j in range(3))
    cov = tuple(tuple(sum(w*x[i]*x[j] for x, w in zip(points, weights))
                      -mean[i]*mean[j] for j in range(3)) for i in range(3))
    require(mean == (0, 0, 0), "nonzero symmetric mean")
    a = cov[0][0]
    require(a > 0, "degenerate covariance")
    require(cov == tuple(tuple(a if i == j else 0 for j in range(3))
                        for i in range(3)), "nonscalar covariance")
    return a


def hinge(u, h):
    return max(u-h, 0)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][col]
        a[r] = [x/scale for x in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][col]
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def finite_controls():
    interactions = 0
    vals = (F(0), F(1, 4), F(1, 2), F(1), F(2))
    for u in itertools.product(vals, repeat=4):
        bounds = sum(min(u[i], u[j]) for i in range(4) for j in range(i))
        knots = sorted(set((F(0), sum(u), sum(u)+1)+u))
        levels = knots + [(a+b)/2 for a, b in zip(knots, knots[1:])]
        for h in levels:
            value = hinge(sum(u), h)-sum(hinge(x, h) for x in u)
            require(0 <= value <= bounds, "interaction inequality")
            interactions += 1
    # Finite-cell identities only; these cells are not Gaussian data.
    cell_checks = 0
    for a in (F(1, 4), F(1, 2), F(3, 4)):
        for b in (F(1, 4), F(1, 2), F(3, 4)):
            for h in (F(0), F(1, 8), F(3, 8), F(5, 8), F(1)):
                old = sum(hinge(x, h) for x in (a, 1-a))-sum(hinge(x, h) for x in (b, 1-b))
                new = 48*(sum(hinge(x/48, h/48) for x in (a, 1-a))
                          -sum(hinge(x/48, h/48) for x in (b, 1-b)))
                require(new == old, "defect scaling lost copy mass")
                cell_checks += 1
    schedules = []
    for radius in (1, 4, 9):
        for variance in (F(1, 4), F(1), F(7, 2)):
            for k in (1, 8, 64):
                length = max(16*radius, 4*radius+ceil_sqrt(32*variance*k))
                require((length-4*radius)**2 >= 32*variance*k, "square-root schedule")
                require(length >= 16*radius, "schedule cross guard")
                schedules.append([radius, str(variance), k, length])
    return {"scalar_interaction_checks": interactions,
            "disjoint_cell_normalization_checks": cell_checks,
            "exact_schedules": schedules}


def rejection_controls(data):
    bads = []
    def altered(field, value):
        x = copy.deepcopy(data)
        x[field] = value
        bads.append(x)
    altered("variance", "0")
    altered("variance", "-1")
    altered("radius", "1/2")
    altered("bits", 0)
    altered("bits", True)
    altered("length", 0)
    altered("bits", 100000)
    altered("requested_error", "0")
    altered("requested_error", "1/1000000000000000000000000000000")
    x = copy.deepcopy(data); x["weights"][0] = "0"; bads.append(x)
    x = copy.deepcopy(data); x["weights"][0] = "1"; bads.append(x)
    x = copy.deepcopy(data); x["source"][0] = ["999", "0", "0"]; bads.append(x)
    x = copy.deepcopy(data); x["target"][0] = ["0", "0", "-4"]; bads.append(x)
    x = copy.deepcopy(data); x["source"][0] = x["source"][1]; bads.append(x)
    x = copy.deepcopy(data); x["target"].pop(); bads.append(x)
    x = copy.deepcopy(data); x["source"][0] = [0, 1]; bads.append(x)
    for item in bads:
        try:
            validate(item)
        except (ValueError, KeyError, TypeError):
            continue
        raise ValueError("invalid control accepted")
    # The direct checker also rejects an expanding constructed target.
    p, q, w, blocks = construct(data)
    bad_q = list(q)
    bad_q[0] = (F(10**6), F(0), F(0))
    try:
        direct_pairs(p, tuple(bad_q), blocks)
    except ValueError:
        return len(bads)+1
    raise ValueError("damaged constructed geometry accepted")


def audit(data):
    base_p, base_q, weights, radius, variance, k, length, eta = validate(data)
    gs = group(); gset = set(gs); v = (1, 2, 3)
    require(len(gs) == 48 and (1, 2, 3) in gset, "group cardinality")
    require(all(compose(g, h) in gset for g in gs for h in gs), "group closure")
    orbit = tuple(act(g, v) for g in gs)
    require(len(set(orbit)) == 48, "nonregular orbit")
    minimum = min(d2(orbit[i], orbit[j]) for i in range(48) for j in range(i))
    require(minimum == 2, "orbit separation")
    p, q, w, blocks = construct(data)
    pairs = direct_pairs(p, q, blocks)
    table = {x: (y, a) for x, y, a in zip(p, q, w)}
    actions = 0
    for x, y, a in zip(p, q, w):
        for g in gs:
            require(table[act(g, x)] == (act(g, y), a), "equivariance or weight error")
            actions += 1
    cp, cq = moments(p, w), moments(q, w)
    ep = sum(a*dot(tuple(length*v[j]+x[j] for j in range(3)),
                   tuple(length*v[j]+x[j] for j in range(3)))
             for a, x in zip(weights, base_p))/3
    eq = sum(a*dot(tuple(F(length, 2)*v[j]+x[j] for j in range(3)),
                   tuple(F(length, 2)*v[j]+x[j] for j in range(3)))
             for a, x in zip(weights, base_q))/3
    require(cp == ep and cq == eq and cp > cq, "covariance formula")
    require(F(2883, 832) < 4, "universal radius-covariance constant")
    rp2, rq2 = max(dot(x, x) for x in p), max(dot(x, x) for x in q)
    require(rp2 <= 4*cp and rq2 <= 4*cq, "compact isotropic guard")
    pins = []
    for item in data.get("source_pins", []):
        pth = (HERE/item["path"]).resolve()
        digest = hashlib.sha256(pth.read_bytes()).hexdigest()
        require(digest == item["sha256"], "source pin changed")
        pins.append({"path": item["path"], "sha256": digest})
    result = {"status": "FINITE_SYMMETRY_DEFECT_CONTROLS_PASS",
              "gaussian_adverse_input_supplied": False,
              "gaussian_counterexample_certified": False,
              "gaussian_integrals_evaluated": 0,
              "group_order": 48, "group_products": 2304,
              "minimum_orbit_squared_separation": minimum,
              "constructed_labels": len(p), "group_action_checks": actions,
              "base_paired_affine_rank": rank([sub(x, base_p[0])+sub(y, base_q[0])
                                                for x, y in zip(base_p[1:], base_q[1:])]),
              "pair_checks": pairs,
              "source_covariance_scalar": str(cp),
              "target_covariance_scalar": str(cq),
              "source_radius_squared_over_covariance": str(rp2/cp),
              "target_radius_squared_over_covariance": str(rq2/cq),
              "universal_radius_squared_over_covariance_bound": "2883/832",
              "compact_normalized_source_covariance": "I_3",
              "compact_normalized_source_radius_bound": "2",
              "variance": str(variance), "separation": length,
              "radius": str(radius), "tail_bits": k,
              "certified_uniform_error_upper_bound": str(F(47, 2**k)),
              "requested_error": str(eta),
              "source_pins": pins}
    result.update(finite_controls())
    result["invalid_controls_rejected"] = rejection_controls(data)
    return result


def main():
    require(len(sys.argv) <= 2, "usage: verify.py [INPUT.json]")
    input_path = Path(sys.argv[1]) if len(sys.argv) == 2 else HERE/"INPUT.json"
    data = json.loads(input_path.read_text())
    result = audit(data)
    expected = HERE/"EXPECTED.json"
    if input_path.resolve() == (HERE/"INPUT.json").resolve() and expected.exists():
        require(result == json.loads(expected.read_text()), "expected record mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
