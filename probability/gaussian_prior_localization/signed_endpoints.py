#!/usr/bin/env python3
"""Exact signed endpoint certificates; no Gaussian quadrature or middle sign."""

import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    need(type(value) in (int, str), "rationals must be integers or strings")
    return F(value)


def ceilq(q):
    return -((-q.numerator) // q.denominator)


def ceil_log2(q):
    need(q >= 1, "logarithm input must be at least one")
    p = max(0, q.numerator.bit_length() - q.denominator.bit_length())
    if F(1 << p) < q:
        p += 1
    need(F(1 << p) >= q and (not p or F(1 << (p-1)) < q),
         "logarithm bracket")
    return p


def norm2(v):
    return sum(t*t for t in v)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def exact_rank(rows):
    rows = [list(map(F, row)) for row in rows]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][col]
        rows[rank] = [v/divisor for v in rows[rank]]
        for i in range(rank+1, len(rows)):
            scale = rows[i][col]
            rows[i] = [v-scale*w for v, w in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def family_budget(k):
    need(type(k) is int and k >= 1, "positive integer k required")
    ell = (k-1).bit_length()
    h = isqrt(ell+1)
    n = (k+h-1)//h
    atoms = min(k**3*(2*comb(2*ell+6, 3)-1),
                n**3*(2*comb(4*ell+11, 3)-1))
    W = 4*k*atoms
    log_bound = (W-1).bit_length()
    delta = F(1, 12288*k**5)
    B = 54*k*k+2*log_bound
    Q = 49152*k**5*B
    E = Q*Q
    peak = 1-F(1, W*W*(1024*k**4+1))
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "scope": "every member of R^c_k with at least two positive weights",
        "k": k, "atoms": atoms, "coordinate_denominator": 256*k**3,
        "weight_denominator": W, "support_radius": 3*k,
        "minimum_squared_pair_loss": str(F(1, 256*k**4)),
        "minimum_positive_weight": str(F(1, W)),
        "log_inverse_weight_upper": log_bound,
        "mean_support_gap_lower": str(delta), "tail_B_upper": B,
        "tail_radius_upper": str(Q),
        "low_endpoint": {"base": 2, "negative_exponent": E},
        "relative_log_radius_upper": 2*Q,
        "low_adverse_relative_upper": str(-6*delta*(E+2)),
        "source_peak_upper": str(peak),
        "point_branch": "all thresholds have equal hinges",
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def parse_instance(obj):
    need(isinstance(obj, dict), "instance must be an object")
    need(set(obj) <= {"source", "target", "weights", "variance"},
         "unknown instance field")
    need(all(k in obj for k in ("source", "target", "weights")),
         "missing instance field")
    need(rational(obj.get("variance", 1)) == 1, "variance one required")
    need(all(isinstance(obj[k], list) for k in ("source", "target", "weights")),
         "input lists required")
    xs = [tuple(rational(a) for a in v) for v in obj["source"]]
    ys = [tuple(rational(a) for a in v) for v in obj["target"]]
    ws = [rational(w) for w in obj["weights"]]
    need(len(xs) == len(ys) == len(ws) > 0, "label counts")
    need(all(len(v) == 3 for v in xs+ys), "dimension three required")
    need(all(w >= 0 for w in ws) and sum(ws) == 1, "probability weights")
    # Validate the supplied finite map, including any zero-weight labels.
    for i, j in combinations(range(len(ws)), 2):
        need(norm2(sub(xs[i], xs[j])) >= norm2(sub(ys[i], ys[j])),
             "expansion or inconsistent source collision")
    groups = {}
    for x, y, w in zip(xs, ys, ws):
        if w:
            groups[x, y] = groups.get((x, y), F(0))+w
    rows = sorted(groups.items())
    xs = [xy[0] for xy, w in rows]
    ys = [xy[1] for xy, w in rows]
    ws = [w for xy, w in rows]
    return xs, ys, ws


def certify_instance(obj):
    xs, ys, ws = parse_instance(obj)
    if len(ws) == 1:
        return {"status": "POINT_EQUALITY_ALL_THRESHOLDS", "positive_source_sites": 1}
    pairs = list(combinations(range(len(ws)), 2))
    losses = [norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j])) for i, j in pairs]
    ell = min(losses)
    need(ell > 0, "strict pair loss required for this endpoint certificate")
    # Separate centering at the exact weighted means preserves all hinges.
    cx = tuple(sum(w*x[t] for w, x in zip(ws, xs)) for t in range(3))
    cy = tuple(sum(w*y[t] for w, y in zip(ws, ys)) for t in range(3))
    xs = [sub(x, cx) for x in xs]
    ys = [sub(y, cy) for y in ys]
    R = max(sum(abs(a) for a in v) for v in xs+ys)
    dbar = max(sum(abs(a) for a in sub(xs[i], xs[j])) for i, j in pairs)
    m = min(ws)
    delta = ell/(8*dbar)
    log_bound = ceil_log2(1/m)
    B = 6*R*R+2*log_bound
    Q = 4*B/delta
    E = ceilq(Q*Q)
    peak = 1-m*m*ell/(4+ell)
    need(0 < peak < 1 and delta <= 2*R, "endpoint range")
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "positive_source_sites": len(ws), "support_radius": str(R),
        "source_diameter_upper": str(dbar),
        "minimum_squared_pair_loss": str(ell),
        "minimum_positive_weight": str(m),
        "log_inverse_weight_upper": log_bound,
        "mean_support_gap_lower": str(delta), "tail_B_upper": str(B),
        "tail_radius_upper": str(Q),
        "low_endpoint": {"base": 2, "negative_exponent": E},
        "relative_log_radius_upper": 2*ceilq(Q),
        "low_adverse_relative_upper": str(-6*delta*(E+2)),
        "source_peak_upper": str(peak),
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def pinned_inputs():
    obj = json.loads((HERE/"SIGNED_ENDPOINT_INPUTS.json").read_text())
    need(obj.get("schema") == 1 and obj.get("files"), "dependency manifest")
    for name, digest in obj["files"].items():
        need(sha256((HERE/name).read_bytes()).hexdigest() == digest,
             "changed dependency: "+name)
    return len(obj["files"])


def reject(fn):
    try:
        fn()
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return
    raise ValueError("ineligible control was accepted")


def controls():
    from paired_cubature import budget, check_grid
    dep_count = pinned_inputs()
    # Pair-loss implies an eligible uniform homothety. This verifies the
    # polynomial inequality, including maximal loss and a collapsed target.
    homothety = 0
    for D in range(1, 18):
        for numerator in range(1, 17):
            ell = F(D*numerator, 16)
            lam = 1-ell/(2*D)
            for denom in range(1, 8):
                a = ell+(D-ell)*F(denom, 7)
                need(a-ell <= (1-ell/D)*a <= lam*lam*a,
                     "homothety reduction")
                homothety += 1
    # Exact actual mean supports for collinear two-point contractions:
    # gap=(source length-target length)/4, independent of their weights.
    collinear = 0
    for source in range(1, 13):
        for j in range(16):
            target = F(source*j, 16)
            loss = source*source-target*target
            need(loss/(8*source) <= (source-target)/4, "mean-support normalization")
            collinear += 1
    peak_controls = 0
    for n in range(1, 25):
        for d in range(2, 13):
            m, ell = F(1, d), F(n, 7)
            v = m*m*ell/(4+ell)
            need(0 < 2*v < 1 and (1-v)**2 >= 1-2*v, "peak square-root bound")
            peak_controls += 1
    # Budget compatibility is checked against the existing public producer.
    ks = list(range(1, 129))+[1000, 1000000]
    for k in ks:
        c, b = family_budget(k), budget(k)
        need(c['atoms'] == b['atoms'] and
             c['coordinate_denominator'] == b['coordinate_denominator'] and
             c['weight_denominator'] == b['weight_denominator'], "producer budget")
        W, L = c['weight_denominator'], c['coordinate_denominator']
        ell = F(c['minimum_squared_pair_loss'])
        delta = F(c['mean_support_gap_lower'])
        R, Q = F(c['support_radius']), F(c['tail_radius_upper'])
        E = c['low_endpoint']['negative_exponent']
        log_bound = c['log_inverse_weight_upper']
        K = R*R+2*log_bound
        need(ell == F(256*k*k, L*L) and delta == ell/(48*k), "loss normalization")
        need(F(c['source_peak_upper']) == 1-ell/(W*W*(4+ell)), "peak composition")
        need(Q >= 4*R and Q*Q >= 2*K and Q >= K/R, "low-tail side conditions")
        need(E == Q*Q and c['relative_log_radius_upper']**2 >= 2*E,
             "symbolic dyadic cutoff")
        need(F(c['low_adverse_relative_upper']) == -6*delta*(E+2), "relative sign")
    # A genuine rank-six, strictly contracting datum from the hinge controls.
    xs = [(0,0,0)]
    ys = [(0,0,0)]
    for j in range(3):
        for sign in (-1,1):
            x, y = [0,0,0], [0,0,0]
            x[j], y[j] = sign*128, 64
            xs.append(tuple(x)); ys.append(tuple(y))
    masses = [24]+[22]*6
    grid_check = check_grid(1, xs, ys, masses)
    paired_rank = exact_rank([x+y for x, y in zip(xs[1:], ys[1:])])
    need(paired_rank == 6, "paired affine rank")
    grid_check['paired_affine_rank'] = paired_rank
    obj = {"source": [[str(F(a,256)) for a in v] for v in xs],
           "target": [[str(F(a,256)) for a in v] for v in ys],
           "weights": [str(F(m,156)) for m in masses], "variance": 1}
    instance = certify_instance(obj)
    # Exact translations and signed permutations preserve all chosen bounds.
    moved = deepcopy(obj)
    for field, shift in [('source', (3,-7,2)), ('target', (-9,1,4))]:
        moved[field] = [[str(F(row[2])+shift[0]), str(-F(row[0])+shift[1]),
                         str(F(row[1])+shift[2])] for row in obj[field]]
    need(certify_instance(moved) == instance, "translation/signed permutation")
    split = deepcopy(obj)
    split['source'].append(split['source'][0][:]); split['target'].append(split['target'][0][:])
    split['weights'][0] = '1/13'; split['weights'].append('1/13')
    need(certify_instance(split) == instance, "merged source collision")
    zero = deepcopy(obj)
    zero['source'].append(zero['source'][0][:]); zero['target'].append(zero['target'][0][:])
    zero['weights'].append(0)
    need(certify_instance(zero) == instance, "zero mass")
    collapse = {"source": [[-1,0,0],[1,0,0]],
                "target": [[0,0,0],[0,0,0]], "weights": ['1/2','1/2']}
    collapse_cert = certify_instance(collapse)
    point = {"source": [[2,3,4],[2,3,4]],
             "target": [[-1,5,0],[-1,5,0]], "weights": ['1/3','2/3']}
    point_cert = certify_instance(point)
    need(point_cert['status'] == 'POINT_EQUALITY_ALL_THRESHOLDS', "point branch")
    bad = []
    for weights in ([1,1], [-1,2], [0.5,0.5], [True,False]):
        x = deepcopy(collapse); x['weights'] = weights; bad.append(x)
    x = deepcopy(collapse); x['target'] = [[-1,0,0],[1,0,0]]; bad.append(x)
    x = deepcopy(collapse); x['target'] = [[-2,0,0],[2,0,0]]; bad.append(x)
    x = deepcopy(point); x['target'][1][0] += 1; bad.append(x)
    x = deepcopy(collapse); x['variance'] = 2; bad.append(x)
    x = deepcopy(collapse); x['source'][0] = [1,2]; bad.append(x)
    x = deepcopy(collapse); x['weights'] = ['1/2']; bad.append(x)
    for x in bad:
        reject(lambda x=x: certify_instance(x))
    for k in [0,-1,True,1.0]:
        reject(lambda k=k: family_budget(k))
    return {"status": "SIGNED_FRONTIER_ENDPOINTS_PASS", "pinned_dependencies": dep_count,
            "homothety_controls": homothety, "collinear_controls": collinear,
            "peak_controls": peak_controls, "family_budget_controls": len(ks),
            "symmetry_collision_zero_controls": 3,
            "rejected_controls": len(bad)+4, "rank_six_grid_check": grid_check,
            "rank_six_instance": instance, "collapsed_target": collapse_cert,
            "point": point_cert,
            "family_certificates": [family_budget(k) for k in (1,4,64,1000)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--check', action='store_true')
    group.add_argument('--budget', type=int)
    group.add_argument('--instance', type=Path)
    parser.add_argument('--expected', type=Path, default=HERE/'SIGNED_ENDPOINT_EXPECTED.json')
    args = parser.parse_args()
    if args.budget is not None:
        result = family_budget(args.budget)
    elif args.instance:
        result = certify_instance(json.loads(args.instance.read_text()))
    else:
        result = controls()
        if args.check:
            expected = json.loads(args.expected.read_text())
            need(result == expected, "complete endpoint record differs")
            print(result['status'])
            return
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
