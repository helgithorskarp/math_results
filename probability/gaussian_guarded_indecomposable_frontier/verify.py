#!/usr/bin/env python3
"""Direct exact geometry checks. Does not import the transplant producer."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
from fractions import Fraction as F

HERE = Path(__file__).resolve().parent
ROOT = [(F(1, 9), F(1, 9), F(1, 9)),
        (F(1, 9), F(-1, 9), F(-1, 9)),
        (F(-1, 9), F(1, 9), F(-1, 9)),
        (F(-1, 9), F(-1, 9), F(1, 9))]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def number(x):
    need(type(x) in (int, str), "nonexact scalar")
    return F(x)


def pts(x):
    need(isinstance(x, list) and x, "empty points")
    need(all(isinstance(a, list) and len(a) == 3 for a in x), "wrong dimension")
    return [tuple(number(t) for t in a) for a in x]


def square(x):
    return sum(t*t for t in x)


def distance(x, y):
    return sum((x[j]-y[j])**2 for j in range(3))


def determinant(a):
    n = len(a)
    result = F(0)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = F((-1)**inversions)
        for i in range(n):
            term *= a[i][perm[i]]
        result += term
    return result


def covariance_report(x, w):
    mean = [sum(t*a[j] for a, t in zip(x, w)) for j in range(3)]
    cov = [[sum(t*(a[i]-mean[i])*(a[j]-mean[j]) for a, t in zip(x, w))
            for j in range(3)] for i in range(3)]
    residual = [[cov[i][j] - (F(1, 162) if i == j else 0)
                 for j in range(3)] for i in range(3)]
    # Definition-level decomposition of the claimed positive semidefinite residual.
    direct = [[F(1, 2)*mean[i]*mean[j] +
               sum(t*(a[i]-mean[i])*(a[j]-mean[j]) for a, t in zip(x[4:], w[4:]))
               for j in range(3)] for i in range(3)]
    need(residual == direct, "root covariance identity failed")
    minors = []
    for size in (1, 2, 3):
        for ix in itertools.combinations(range(3), size):
            minors.append(determinant([[residual[i][j] for j in ix] for i in ix]))
    need(all(v >= 0 for v in minors), "covariance floor failed")
    return {"covariance": [[str(v) for v in row] for row in cov],
            "residual_principal_minors": [str(v) for v in minors]}


def pair_loss(p, q, w):
    return sum(w[i]*w[j]*(distance(p[i], p[j])-distance(q[i], q[j]))
               for i in range(len(p)) for j in range(len(p)))


def short(p, q):
    need(len(p) == len(q), "wrong point count")
    losses = [distance(p[i], p[j])-distance(q[i], q[j])
              for i in range(len(p)) for j in range(i)]
    need(all(v >= 0 for v in losses), "pair expansion")
    return len(losses)


def check(data, packet):
    need(set(data) == {"source", "target", "weights", "radius", "budget_bits"}, "input fields")
    p, q = pts(data["source"]), pts(data["target"])
    need(len(p) == len(q) and len(set(p)) == len(p), "input sites")
    w = [number(x) for x in data["weights"]]
    need(len(w) == len(p) and sum(w) == 1 and min(w) > 0, "input weights")
    r, k = data["radius"], data["budget_bits"]
    need(type(r) is int and r >= 1 and type(k) is int and k >= 1, "input guards")
    need(all(square(x) <= r*r for x in p+q), "input radius")
    short(p, q)
    ell = packet["L"]
    need(type(ell) is int and ell == max(4*r, k), "L guard")
    pp, qq = pts(packet["source"]), pts(packet["target"])
    ww = [number(x) for x in packet["weights"]]
    need(len(pp) == len(qq) == len(ww) == len(p)+4, "transplant count")
    need(pp[:4] == qq[:4] == ROOT and ww[:4] == [F(1, 8)]*4, "fixed roots")
    need(ww[4:] == [v/2 for v in w] and sum(ww) == 1, "transplanted weights")
    for i in range(len(p)):
        recovered_p = tuple(9*ell*pp[i+4][j]-(8*ell if j == 0 else 0) for j in range(3))
        recovered_q = tuple(9*ell*qq[i+4][j]-(6*ell if j == 0 else 0) for j in range(3))
        need(recovered_p == p[i] and recovered_q == q[i], "old cloud not preserved")
    need(packet["status"] == "GEOMETRY_ONLY_TRANSPLANT", "status")
    need(packet["adverse_input_verified"] is False and packet["indecomposability_verified"] is False,
         "unsupported proof claim")
    need(number(packet["variance"]) == F(1, 81*ell*ell), "variance scale")
    need(number(packet["threshold_multiplier"]) == F((9*ell)**3, 2), "threshold scale")
    need(number(packet["support_radius_bound"]) == 1 and
         number(packet["covariance_floor"]) == F(1, 162) and
         number(packet["cross_squared_loss_floor"]) == F(14, 81), "advertised guard")
    need(packet["hinge_error_bound"] == {"base": 2, "exponent": -k} and 2*ell*ell >= k,
         "symbolic tail schedule")
    need(packet["localization_guards"] == {"R": 18*ell, "kappa": str(F(ell*ell, 2)),
                                          "alignment_factor": 2593}, "localization guard")
    need(all(square(x) <= F(121, 144) for x in pp+qq), "support radius")
    pairs = short(pp, qq)
    cross = [distance(pp[i], pp[j])-distance(qq[i], qq[j])
             for i in range(4) for j in range(4, len(pp))]
    need(min(cross) > F(14, 81), "cross-pair margin")
    # The separating plane in normalized coordinates is x_1=1/3.
    need(max(x[0] for x in pp[:4]) <= F(1, 9), "background separation")
    need(min(x[0] for x in pp[4:]+qq[4:]) >= F(5, 9), "moving separation")
    # A direct nontrivial intermediate control, unrelated to the SCC implementation.
    zz = ROOT + [tuple((p[i][d]+(7*ell if d == 0 else 0))/(9*ell)
                       for d in range(3)) for i in range(len(p))]
    short(pp, zz)
    short(zz, qq)
    for x, y in zip(pp, zz):
        need(sum(distance(x,a)-distance(y,a) for a in ROOT) == 4*(square(x)-square(y)),
             "interval radial identity")
        need(square(y) <= square(x), "intermediate escaped radius")
    loss = pair_loss(pp, qq, ww)
    need(loss == pair_loss(pp, zz, ww)+pair_loss(zz, qq, ww) and 0 < loss <= 2,
         "ordered loss telescope")
    need(1+4*F((18*ell)**2, 1)/F(ell*ell, 2) == 2593, "uniform alignment factor")
    return {"labels": len(pp), "checked_pairs": pairs, "L": ell,
            "variance": packet["variance"], "minimum_cross_squared_loss": str(min(cross)),
            "ordered_loss": str(loss), "source": covariance_report(pp, ww),
            "intermediate": covariance_report(zz, ww), "target": covariance_report(qq, ww)}


def small_indecomposable():
    p = ROOT + [(F(-1, 9),)*3]
    q = ROOT + [(F(1, 27),)*3]
    w = [F(1, 8)]*4+[F(1, 2)]
    short(p, q)
    need(all(distance(p[4], a) == distance(q[4], a) == F(4, 81) for a in ROOT[1:]),
         "three tight sphere constraints")
    # The two independent differences of those sphere equations impose x=y=z=t.
    normals = [tuple(ROOT[i][j]-ROOT[3][j] for j in range(3)) for i in (1, 2)]
    need(determinant([[n[0], n[1]] for n in normals]) != 0 and
         all(sum(n) == 0 for n in normals), "sphere-difference rank")
    # On that line the equation is 243t^2+18t-1=0, with exactly these two roots.
    roots = [F(-1, 9), F(1, 27)]
    need(all(243*t*t+18*t-1 == 0 for t in roots), "quadratic roots")
    need(roots[0]+roots[1] == F(-18, 243) and roots[0]*roots[1] == F(-1, 243),
         "quadratic factorization")
    need(distance(p[4], ROOT[0]) > distance(q[4], ROOT[0]), "nontrivial cover")
    covariance_report(p, w)
    covariance_report(q, w)
    return {"labels": 5, "full_interval_states": 2,
            "last_coordinate_roots": [str(x) for x in roots],
            "ordered_loss": str(pair_loss(p, q, w)),
            "sign": "Known positive single hyperplane fold; no adverse value claimed."}


def expect_rejection(fn):
    try:
        fn()
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return
    raise ValueError("damaged input was accepted")


def run():
    data = json.loads((HERE/"INPUT.json").read_text())
    packet = json.loads((HERE/"TRANSPLANT.json").read_text())
    supplied = check(data, packet)
    # Production entry point is called only for byte-for-byte reproducibility.
    raw = subprocess.check_output([sys.executable, "-B", str(HERE/"transplant.py"), str(HERE/"INPUT.json")])
    need(raw == (HERE/"TRANSPLANT.json").read_bytes(), "producer bytes differ")
    rejected = 0
    mutations = [
        ("variance", "1"), ("threshold_multiplier", "1"), ("L", packet["L"]+1),
        ("support_radius_bound", "2"), ("covariance_floor", "1/81"),
        ("adverse_input_verified", True), ("indecomposability_verified", True),
    ]
    for key, val in mutations:
        altered = copy.deepcopy(packet); altered[key] = val
        expect_rejection(lambda: check(data, altered)); rejected += 1
    for field, index, val in [("source", 0, ["0", "0", "0"]),
                               ("target", 0, ["0", "0", "0"]),
                               ("weights", 0, "1/16")]:
        altered = copy.deepcopy(packet); altered[field][index] = val
        expect_rejection(lambda: check(data, altered)); rejected += 1
    for key, val in [("radius", 0), ("budget_bits", True), ("radius", 1.5)]:
        altered = copy.deepcopy(data); altered[key] = val
        expect_rejection(lambda: check(altered, packet)); rejected += 1
    altered = copy.deepcopy(data); altered["source"][1] = altered["source"][0]
    expect_rejection(lambda: check(altered, packet)); rejected += 1
    grid = [F(0), F(1, 5), F(1, 2), F(1), F(2)]
    interactions = 0
    for b, m, h in itertools.product(grid, repeat=3):
        j = max(b+m-h, 0)-max(b-h, 0)-max(m-h, 0)
        need(0 <= j <= min(b, m), "hinge interaction")
        interactions += 1
    # Root identities are checked independently of any geometric input.
    need(all(sum(a[j] for a in ROOT) == 0 for j in range(3)), "root mean")
    need(all(sum(a[i]*a[j] for a in ROOT)/4 == (F(1,81) if i == j else 0)
             for i in range(3) for j in range(3)), "root second moment")
    # Endpoint-norm constants and Gaussian-tail exponent schedule use rational arithmetic.
    need(24-F(36,4)-F(1,16) == F(239,16) > 14, "cross constant")
    need(F(33,36)**2 == F(121,144) < 1, "radius constant")
    need(F(1,8) == F(1,4)-F(1,8), "auxiliary gap budget")
    return {"status": "GUARDED_INDECOMPOSABLE_FRONTIER_CONTROLS_PASS",
            "supplied_transplant": supplied, "small_indecomposable_control": small_indecomposable(),
            "hinge_interaction_cases": interactions, "rejections": rejected,
            "transplant_sha256": hashlib.sha256(raw).hexdigest(),
            "gaussian_integrals_evaluated": False, "adverse_input_verified": False,
            "mesh_constructed": False, "old_checkers_replayed": False}


def main():
    if len(sys.argv) == 3:
        a = json.loads(Path(sys.argv[1]).read_text())
        b = json.loads(Path(sys.argv[2]).read_text())
        print(json.dumps({"status": "SUPPLIED_TRANSPLANT_GEOMETRY_VERIFIED", "record": check(a,b)},
                         indent=2, sort_keys=True))
    else:
        need(len(sys.argv) == 1, "usage: verify.py [INPUT.json TRANSPLANT.json]")
        print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
