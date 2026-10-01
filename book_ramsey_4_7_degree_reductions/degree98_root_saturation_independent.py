#!/usr/bin/env python3
"""Separate author check: bit intersections and an integral quotient minor.

Imports no first-implementation module. Input graph controls are validation
fixtures, not an exhaustive graph domain or mathematical premise.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path


def check(ok, message):
    if not ok:
        raise ValueError(message)


def fingerprint(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def bareiss(matrix):
    a = [row[:] for row in matrix]
    sign, previous = 1, 1
    if not a:
        return 1
    for k in range(len(a) - 1):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            sign = -sign
        value = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = value * a[i][j] - a[i][k] * a[k][j]
                check(numerator % previous == 0, "Bareiss division")
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = value
    return sign * a[-1][-1]


def graph_audit(record):
    m, c = record["m"], record["m"] - 2
    rows = record["rows"]
    check(len(rows) == 22 and all(len(row) == 22 and set(row) <= {"0", "1"}
                                for row in rows), "binary graph input")
    masks = [sum((ch == "1") << j for j, ch in enumerate(row)) for row in rows]
    neighbors = [[j for j in range(22) if masks[i] >> j & 1] for i in range(22)]
    check(all(not (masks[i] >> i & 1) and
              (masks[i] >> j & 1) == (masks[j] >> i & 1)
              for i in range(22) for j in range(22)), "simple symmetric graph")
    d = [x.bit_count() for x in masks]
    check(d == [8] * m + [9] * (24 - 2 * m) + [10] * c, "graph histogram")
    universe = (1 << 22) - 1
    complement = [universe ^ masks[i] ^ (1 << i) for i in range(22)]
    f = [[0] * 22 for _ in range(22)]
    for i, j in itertools.combinations(range(22), 2):
        red = bool(masks[i] >> j & 1)
        pages = ((masks[i] & masks[j]) if red else
                 (complement[i] & complement[j])).bit_count()
        f[i][j] = f[j][i] = (3 if red else 6) - pages
        rsq = (masks[i] & masks[j]).bit_count()
        check(rsq == d[i] + d[j] - 14 + (17 - d[i] - d[j]) * red - f[i][j],
              "literal signed codegree identity")
    check(f == record["defects"], "every literal graph-control F entry")
    aroot = [i for i in range(22) if d[i] == 8]
    croot = [i for i in range(22) if d[i] == 10]
    u = [int(i in aroot) for i in range(22)]
    v = [int(i in croot) for i in range(22)]
    h = [len(set(neighbors[i]).intersection(aroot)) for i in range(22)]
    k = [len(set(neighbors[i]).intersection(croot)) for i in range(22)]
    def apply_k(x):
        return [2 * sum(x[j] for j in neighbors[i]) + (2 * d[i] - 17) * x[i]
                for i in range(22)]
    def apply_f(x):
        return [sum(f[i][j] * x[j] for j in range(22)) for i in range(22)]
    for j in range(22):
        unit = [int(i == j) for i in range(22)]
        actual = apply_k(apply_k(unit))
        forced = [((2 * d[i] - 17) ** 2 + 4 * d[i] if i == j else
                   4 * (d[i] + d[j] - 14) - 4 * f[i][j]) for i in range(22)]
        check(actual == forced, "all original square entries")
    incident = [sum(row) for row in f]
    check(incident == [196 - 294 + 38 * d[i] - d[i] ** 2
                        - 2 * sum(d[j] for j in neighbors[i]) for i in range(22)],
          "general incident identity")
    check(incident == [1 - 3 * u[i] + v[i] + 2 * (h[i] - k[i]) for i in range(22)],
          "special incident identity")
    fu, fv = apply_f(u), apply_f(v)
    ra, rc = sum(incident[i] for i in aroot), sum(incident[i] for i in croot)
    kh, kk = apply_k(h), apply_k(k)
    check(kh == [6 * m + (12 - 2 * m) * u[i] + 2 * m * v[i]
                 + h[i] - 2 * fu[i] for i in range(22)], "corrected K h")
    check(kk == [10 * c - 2 * c * u[i] + (8 + 2 * c) * v[i]
                 - 3 * k[i] - 2 * fv[i] for i in range(22)], "corrected K k")
    kfu, kfv = apply_k(fu), apply_k(fv)
    check([2 * x for x in apply_f(h)] == [2 * m - 4 * m * u[i]
          + 2 * (u[i] + v[i]) * h[i] + 2 * (m - 1) * h[i] - 2 * m * k[i]
          - ra + kfu[i] + fu[i] for i in range(22)], "general F h")
    check([2 * x for x in apply_f(k)] == [2 * c - 4 * c * u[i]
          + 2 * (u[i] + v[i]) * k[i] + 2 * c * h[i] - 2 * (c + 1) * k[i]
          - rc + kfv[i] - 3 * fv[i] for i in range(22)], "general F k")
    p = [1 + h[i] - k[i] - 2 * u[i] for i in range(22)]
    fp = apply_f(p)
    error = apply_k([fu[i] - fv[i] for i in range(22)])
    check([2 * (fp[i] - 3 * p[i]) for i in range(22)] ==
          [(u[i] + v[i]) * incident[i] - ra + rc + error[i]
           - 3 * (fu[i] - fv[i]) for i in range(22)], "corrected F p")
    ea = sum(bool(masks[i] >> j & 1) for i, j in itertools.combinations(aroot, 2))
    ec = sum(bool(masks[i] >> j & 1) for i, j in itertools.combinations(croot, 2))
    check(ra + rc == 4 * (ea - ec - 1), "exact root budget")
    leaf_groups = [range(m + t * 3, m + t * 3 + 3) for t in range(3)]
    scaled_trace = 0
    edge_count = 0
    for group in leaf_groups:
        for i in group:
            for j in group:
                if masks[i] >> j & 1:
                    scaled_trace += 3 * (i == j) - 1
                if i < j and masks[i] >> j & 1:
                    edge_count += 1
    check(scaled_trace == -2 * edge_count, "integer projection trace")
    adjacency = [[int(masks[i] >> j & 1) for j in range(22)] for i in range(22)]
    return {"m": m, "sample": record["sample"],
            "graph_sha256": fingerprint(adjacency), "defect_sha256": fingerprint(f),
            "all_defects_nonnegative": all(z >= 0 for row in f for z in row)}


def small_domains(m):
    n = 12 - 2 * m
    pairs = list(itertools.combinations(range(n), 2))
    if not n:
        yield (), []
        return
    for weights in itertools.product(range(4), repeat=len(pairs)):
        edges = [(i, j, z) for (i, j), z in zip(pairs, weights)]
        margins = [sum(z for i, j, z in edges if t in (i, j)) for t in range(n)]
        if margins != [3] * n:
            continue
        triple = tuple(weights[:3]) if m == 4 else ()
        yield triple, edges


def kernel_audit(m, weights, small_edges, artificial=False, exported=None):
    roots = 2 * m - 2
    center = [roots + i for i in range(3)]
    triples = [[roots + 3 + 3 * i + j for j in range(3)] for i in range(3)]
    small = list(range(roots + 12, 22))
    edge_list = [(i, j, 1) for i, j in itertools.combinations(center, 2)]
    edge_list += [(i, j, 1) for i, triple in zip(center, triples) for j in triple]
    if not artificial:
        edge_list += [(small[i], small[j], z) for i, j, z in small_edges]
    f = [[0] * 22 for _ in range(22)]
    for i, j, z in edge_list:
        f[i][j] += z
        f[j][i] += z
    d = [8] * m + [10] * (m - 2) + [9] * (24 - 2 * m)
    h = [[((2 * d[i] - 17) ** 2 + 4 * d[i] if i == j else
           4 * (d[i] + d[j] - 14) - 4 * f[i][j]) for j in range(22)]
         for i in range(22)]
    if exported is not None:
        check(f == exported["F"] and h == exported["H"], "every normal-form F/H entry")
    a = [[h[i][j] - 21 * (i == j) for j in range(22)] for i in range(22)]
    def action(x):
        return [sum(a[i][j] * x[j] for j in range(22)) for i in range(22)]
    leaf_basis = []
    for i, j, k in triples:
        leaf_basis += [[int(t == i) - int(t == j) for t in range(22)],
                       [int(t == j) - int(t == k) for t in range(22)]]
    check(all(action(x) == [0] * 22 for x in leaf_basis), "six leaf directions")
    gram = [[sum(x[i] * y[i] for i in range(22)) for y in leaf_basis]
            for x in leaf_basis]
    check(bareiss(gram) == 27 and all(gram[i][i] == 2 for i in range(6)), "Gram")
    representatives = list(range(roots)) + center + [triple[0] for triple in triples] + small
    columns = [[int(i == t) for i in range(22)] for t in list(range(roots)) + center]
    columns += [[int(i in triple) for i in range(22)] for triple in triples]
    columns += [[int(i == t) for i in range(22)] for t in small]
    check(len(columns) == 16, "sixteen quotient directions")
    images = [action(x) for x in columns]
    for x in images:
        check(all(len({x[i] for i in triple}) == 1 for triple in triples),
              "constant-leaf subspace invariance")
    quotient = [[x[i] for x in images] for i in representatives]
    quotient_det = bareiss(quotient)
    if artificial:
        check(quotient_det == 0, "missing-cubic control did not lose rank")
        return {"artificial_quotient_determinant": 0}
    check(quotient_det != 0, "whole kernel not the six-dimensional leaf lattice")
    # Leaf rows force centers zero; center rows force each leaf sum zero;
    # the small block must be invertible. Check the entire small block exactly.
    small_det = bareiss([[f[i][j] for j in small] for i in small])
    check(small_det != 0, "additional defect kernel")
    w = [Q(0)] * 22
    for i in center:
        w[i] = Q(1)
    for triple in triples:
        for i in triple:
            w[i] = Q(-1, 3)
    for i in small:
        w[i] = Q(1, 3)
    check([sum(f[i][j] * w[j] for j in range(22)) for i in range(22)] ==
          [0] * roots + [1] * (22 - roots), "inverse-image sum control")
    c = m - 2
    root_block = [[1 + 2 * m, 4 * c], [4 * m, 1 + 6 * c]]
    denom = bareiss(root_block)
    alpha, beta = Q(2 * c - 3, denom), Q(2 * c - 1, denom)
    check(root_block[0][0] * alpha + root_block[0][1] * beta == -3 and
          root_block[1][0] * alpha + root_block[1][1] * beta == -5,
          "root elimination coefficients")
    gamma = sum(w)
    nu = 3 * m * alpha + 5 * c * beta + 4
    check(gamma == Q(12 - 2 * m, 3) and nu == Q(2 * (1 - c), denom)
          and 1 - nu * gamma != 0, "entire eigenspace sum equation")
    record = {"m": m, "weights": list(weights), "F_sha256": fingerprint(f),
              "H_sha256": fingerprint(h), "rank_H_minus_21I": 16,
              "nullity_F_B": 6, "root_determinant": denom,
              "gamma": str(gamma), "nu": str(nu),
              "sum_factor": str(1 - nu * gamma), "Gram_determinant": 27}
    return record, quotient_det, small_det


def trace_controls():
    # For the literal mod-two leaf Gram, G=G^{-1}. Symmetric GS has 21
    # elementary generators. Check their corresponding traces separately.
    g = [[int(i // 2 == j // 2 and i != j) for j in range(6)] for i in range(6)]
    count = 0
    for i in range(6):
        for j in range(i, 6):
            symmetric = [[int((a, b) in {(i, j), (j, i)}) for b in range(6)]
                         for a in range(6)]
            trace = sum(sum(g[a][k] * symmetric[k][a] for k in range(6))
                        for a in range(6)) % 2
            check(trace == 0, "mod-two self-adjoint trace generator")
            count += 1
    c = [[0, 5], [1, -1]]
    g0, b = [[2, 0], [0, 10]], [[1, 1], [1, 4]]
    g4 = [[g0[i % 2][j % 2] if i // 2 == j // 2 else b[i % 2][j % 2]
           for j in range(4)] for i in range(4)]
    s4 = [[c[i % 2][j % 2] if i // 2 == j // 2 else 0 for j in range(4)]
          for i in range(4)]
    for i, j in itertools.product(range(4), repeat=2):
        check(sum(g4[i][k] * s4[k][j] for k in range(4)) ==
              sum(s4[k][i] * g4[k][j] for k in range(4)), "rank-four symmetry")
        check(sum(s4[i][k] * s4[k][j] for k in range(4)) + s4[i][j] == 5 * (i == j),
              "rank-four quadratic")
    check(bareiss(g4) == 205 and sum(s4[i][i] for i in range(4)) == -2,
          "rank-four determinant and trace")
    gr, sr = [[2, 1], [1, 2]], [[Q(0), Q(5, 2)], [Q(2), Q(-1)]]
    for i, j in itertools.product(range(2), repeat=2):
        check(sum(gr[i][k] * sr[k][j] for k in range(2)) ==
              sum(sr[k][i] * gr[k][j] for k in range(2)), "rational symmetry")
        check(sum(sr[i][k] * sr[k][j] for k in range(2)) + sr[i][j] == 5 * (i == j),
              "rational quadratic")
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--report", type=Path, help="optional private audit report")
    args = parser.parse_args()
    expected = json.loads(Path(__file__).with_name("degree98_root_saturation_expected.json").read_text())
    control_data = json.loads(args.controls.read_text())
    controls = control_data["graphs"]
    check([(x["m"], x["sample"]) for x in controls] ==
          [(m, s) for m in (4, 5, 6) for s in range(32)], "control domain")
    records = [graph_audit(x) for x in controls]
    check(fingerprint(records) == expected["graph_control_stream_sha256"],
          "all literal graph and defect records differ")
    exported_forms = {(x["m"], tuple(x["weights"])): x for x in control_data["forms"]}
    check(len(exported_forms) == len(control_data["forms"]) == 12, "matrix-export domain")
    entries, quotients = [], []
    for m in (4, 5, 6):
        for weights, small in small_domains(m):
            record, quotient_det, small_det = kernel_audit(
                m, weights, small, exported=exported_forms[(m, weights)])
            entries.append(record)
            quotients.append({"m": m, "weights": list(weights),
                              "quotient_determinant": quotient_det,
                              "small_defect_determinant": small_det})
    check(sorted(entries, key=lambda x: (x["m"], x["weights"])) ==
          expected["forced_form_records"], "all full F/H fingerprints and kernel records")
    kernel_audit(4, (0, 0, 3), [], artificial=True)
    result = {"agent": "six-books-1", "role": "researcher", "complete": True,
              "signed_graph_controls": len(records), "forced_forms": len(entries),
              "literal_graph_F_entries_compared": 96 * 22 * 22,
              "red_edge_projection_trace_controls": 96,
              "full_F_entries_compared": 12 * 22 * 22,
              "full_H_entries_compared": 12 * 22 * 22,
              "whole_kernel_method": "nonzero integral sixteen-dimensional quotient determinant",
              "mod_two_trace_generators": trace_controls(), "quotients": quotients,
              "graph_control_stream_sha256": fingerprint(records),
              "controls_are_validation_only": True}
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "quotients"}, sort_keys=True))


if __name__ == "__main__":
    main()
