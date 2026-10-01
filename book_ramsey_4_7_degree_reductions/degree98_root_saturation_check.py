#!/usr/bin/env python3
"""Exact controls for the analytic root-saturation theorem; Python >=3.11.

The proof is in degree98_root_saturation.md. Signed graph controls validate
identities; they are not admissible hosts or an exhaustive host search.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":"),
                                     sort_keys=True).encode()).hexdigest()


def mv(a, x):
    return [sum(t * z for t, z in zip(row, x)) for row in a]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    p = 0
    for j in range(len(a[0])):
        q = next((i for i in range(p, len(a)) if a[i][j]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        scale = a[p][j]
        a[p] = [x / scale for x in a[p]]
        for i in range(p + 1, len(a)):
            if a[i][j]:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def det(a):
    a = [[Fraction(x) for x in row] for row in a]
    value = Fraction(1)
    for j in range(len(a)):
        q = next((i for i in range(j, len(a)) if a[i][j]), None)
        if q is None:
            return Fraction(0)
        if q != j:
            a[q], a[j] = a[j], a[q]
            value = -value
        scale = a[j][j]
        value *= scale
        for i in range(j + 1, len(a)):
            z = a[i][j] / scale
            a[i] = [x - z * y for x, y in zip(a[i], a[j])]
    return value


def graph_controls():
    """Havel--Hakimi, then deterministic degree-preserving two-edge switches."""
    out = []
    for m in (4, 5, 6):
        b, c = 24 - 2 * m, m - 2
        degrees = [8] * m + [9] * b + [10] * c
        todo = degrees[:]
        adj = [set() for _ in todo]
        while max(todo):
            v = max(range(22), key=lambda i: (todo[i], -i))
            size = todo[v]
            candidates = sorted((i for i in range(22) if i != v and todo[i]),
                                key=lambda i: (-todo[i], i))[:size]
            require(len(candidates) == size, "non-graphical control degrees")
            todo[v] = 0
            for i in candidates:
                require(i not in adj[v], "repeated control edge")
                adj[v].add(i)
                adj[i].add(v)
                todo[i] -= 1
        state = 104729 + m
        for sample in range(32):
            changed = 0
            trials = 0
            while changed < 16:
                edges = [(i, j) for i in range(22) for j in sorted(adj[i]) if i < j]
                state = (1664525 * state + 1013904223) % (1 << 32)
                a, z = edges[state % len(edges)]
                state = (1664525 * state + 1013904223) % (1 << 32)
                x, y = edges[state % len(edges)]
                trials += 1
                require(trials <= 20000, "control construction did not finish")
                if len({a, z, x, y}) != 4 or x in adj[a] or y in adj[z]:
                    continue
                for i, j in ((a, z), (x, y)):
                    adj[i].remove(j)
                    adj[j].remove(i)
                for i, j in ((a, x), (z, y)):
                    adj[i].add(j)
                    adj[j].add(i)
                changed += 1
            out.append({"m": m, "sample": sample,
                        "rows": ["".join(str(int(j in adj[i])) for j in range(22))
                                 for i in range(22)]})
    return out


def audit_graph(record):
    m, c = record["m"], record["m"] - 2
    r = [[int(t) for t in row] for row in record["rows"]]
    require(len(r) == 22 and all(len(row) == 22 for row in r), "graph shape")
    require(all(r[i][i] == 0 and r[i][j] == r[j][i]
                and r[i][j] in (0, 1) for i in range(22) for j in range(22)),
            "not a simple graph")
    d = list(map(sum, r))
    require(d == [8] * m + [9] * (24 - 2 * m) + [10] * c, "degrees")
    red = [{j for j in range(22) if r[i][j]} for i in range(22)]
    blue = [set(range(22)) - red[i] - {i} for i in range(22)]
    fmat = [[0 if i == j else (3 - len(red[i] & red[j]) if r[i][j]
                               else 6 - len(blue[i] & blue[j]))
             for j in range(22)] for i in range(22)]
    u = [int(i < m) for i in range(22)]
    v = [int(i >= 22 - c) for i in range(22)]
    h, k = mv(r, u), mv(r, v)
    f, fu, fv = list(map(sum, fmat)), mv(fmat, u), mv(fmat, v)
    ra, rc = sum(f[:m]), sum(f[22 - c:])
    kmat = [[2 * r[i][j] + ((2 * d[i] - 17) if i == j else 0)
             for j in range(22)] for i in range(22)]
    hmat = [[21 * int(i == j) + 16 - 4 * (u[i] + u[j])
             + 4 * (v[i] + v[j]) + 4 * int(i == j) * (u[i] + v[i])
             - 4 * fmat[i][j] for j in range(22)] for i in range(22)]
    require(mm(kmat, kmat) == hmat, "full K square")
    rsq = mm(r, r)
    for i in range(22):
        for j in range(22):
            if i != j:
                require(rsq[i][j] == d[i] + d[j] - 14
                        + (17 - d[i] - d[j]) * r[i][j] - fmat[i][j],
                        "off-diagonal codegree bridge")
    require(f == [2 - (d[i] - 10) ** 2 + 2 * (h[i] - k[i])
                  for i in range(22)], "incident defect")
    require(mv(kmat, h) == [6 * m + (12 - 2 * m) * u[i] + 2 * m * v[i]
                           + h[i] - 2 * fu[i] for i in range(22)], "K h")
    require(mv(kmat, k) == [10 * c - 2 * c * u[i] + (8 + 2 * c) * v[i]
                           - 3 * k[i] - 2 * fv[i] for i in range(22)], "K k")
    kfu, kfv = mv(kmat, fu), mv(kmat, fv)
    fh, fk = mv(fmat, h), mv(fmat, k)
    require([2 * x for x in fh] == [2 * m - 4 * m * u[i]
            + 2 * (u[i] + v[i]) * h[i] + 2 * (m - 1) * h[i] - 2 * m * k[i]
            - ra + kfu[i] + fu[i] for i in range(22)], "general F h")
    require([2 * x for x in fk] == [2 * c - 4 * c * u[i]
            + 2 * (u[i] + v[i]) * k[i] + 2 * c * h[i] - 2 * (c + 1) * k[i]
            - rc + kfv[i] - 3 * fv[i] for i in range(22)], "general F k")
    p = [1 + h[i] - k[i] - 2 * u[i] for i in range(22)]
    fp = mv(fmat, p)
    corrected = [(u[i] + v[i]) * f[i] - (ra - rc) + kfu[i] - kfv[i]
                 - 3 * (fu[i] - fv[i]) for i in range(22)]
    require([2 * (fp[i] - 3 * p[i]) for i in range(22)] == corrected,
            "corrected positive-vector identity")
    ea = sum(r[i][j] for i in range(m) for j in range(i + 1, m))
    ec = sum(r[i][j] for i in range(22 - c, 22) for j in range(i + 1, 22))
    require(ra + rc == -4 + 4 * (ea - ec), "root defect budget")
    # This projection identity holds for any simple graph; invariance of its
    # leaf space is a separate written premise of the theorem, not these controls.
    triples = [list(range(m + 3 * t, m + 3 * t + 3)) for t in range(3)]
    p3 = [[sum(3 * int(i == j) - 1 for triple in triples
               if i in triple and j in triple) for j in range(22)] for i in range(22)]
    projected_trace3 = sum(sum(r[i][j] * p3[j][i] for j in range(22)) for i in range(22))
    leaf_edges = sum(r[i][j] for triple in triples for i, j in itertools.combinations(triple, 2))
    require(projected_trace3 == -2 * leaf_edges, "literal red-edge projection trace")
    record["defects"] = fmat
    return {"m": m, "sample": record["sample"], "graph_sha256": digest(r),
            "defect_sha256": digest(fmat),
            "all_defects_nonnegative": min(min(row) for row in fmat) >= 0}


def forms():
    for m in (4, 5, 6):
        if m == 4:
            for x in range(4):
                for y in range(4 - x):
                    yield m, (x, y, 3 - x - y)
        else:
            yield m, ()


def normal_form(m, weights, omit_cubic=False):
    c, roots = m - 2, 2 * m - 2
    f = [[0] * 22 for _ in range(22)]
    centers = list(range(roots, roots + 3))
    leaves = [list(range(roots + 3 + 3 * i, roots + 6 + 3 * i)) for i in range(3)]
    small = list(range(roots + 12, 22))
    def edge(i, j, value):
        f[i][j] = f[j][i] = value
    for i, j in itertools.combinations(centers, 2):
        edge(i, j, 1)
    for i, triple in zip(centers, leaves):
        for j in triple:
            edge(i, j, 1)
    if not omit_cubic:
        if m == 4:
            x, y, z = weights
            for i, j, value in ((0, 1, x), (2, 3, x), (0, 2, y), (1, 3, y),
                                (0, 3, z), (1, 2, z)):
                edge(small[i], small[j], value)
        elif m == 5:
            edge(*small, 3)
    u = [int(i < m) for i in range(22)]
    v = [int(m <= i < roots) for i in range(22)]
    h = [[21 * int(i == j) + 16 - 4 * (u[i] + u[j]) + 4 * (v[i] + v[j])
          + 4 * int(i == j) * (u[i] + v[i]) - 4 * f[i][j]
          for j in range(22)] for i in range(22)]
    return f, h, roots, centers, leaves, small


def audit_form(m, weights):
    f, h, roots, centers, leaves, small = normal_form(m, weights)
    a = [[h[i][j] - 21 * int(i == j) for j in range(22)] for i in range(22)]
    require(rank(a) == 16, "entire eigenspace is not dimension six")
    bblock = [row[roots:] for row in f[roots:]]
    require(rank(bblock) == 22 - roots - 6, "entire defect kernel")
    basis = []
    for i, j, k in leaves:
        x, y = [0] * 22, [0] * 22
        x[i], x[j] = 1, -1
        y[j], y[k] = 1, -1
        basis.extend([x, y])
    require(all(mv(a, x) == [0] * 22 for x in basis), "leaf kernel")
    gram = [[sum(x * y for x, y in zip(s, t)) for t in basis] for s in basis]
    require(det(gram) == 27 and all(gram[i][i] % 2 == 0 for i in range(6)),
            "full leaf lattice Gram")
    w = [Fraction(0)] * 22
    for i in centers:
        w[i] = Fraction(1)
    for triple in leaves:
        for i in triple:
            w[i] = Fraction(-1, 3)
    for i in small:
        w[i] = Fraction(1, 3)
    require(mv(f, w) == [0] * roots + [1] * (22 - roots), "F w")
    c = m - 2
    denom = 5 - 4 * c * c
    gamma = Fraction(12 - 2 * m, 3)
    nu = Fraction(2 * (1 - c), denom)
    factor = 1 - nu * gamma
    require(sum(w) == gamma and factor != 0, "root-elimination sum")
    return {"m": m, "weights": list(weights), "F_sha256": digest(f),
            "H_sha256": digest(h), "rank_H_minus_21I": rank(a),
            "nullity_F_B": 22 - roots - rank(bblock),
            "root_determinant": denom, "gamma": str(gamma), "nu": str(nu),
            "sum_factor": str(factor), "Gram_determinant": 27}


def lattice_controls():
    c = [[0, 5], [1, -1]]
    g0, b = [[2, 0], [0, 10]], [[1, 1], [1, 4]]
    g4 = [[g0[i % 2][j % 2] if i // 2 == j // 2 else b[i % 2][j % 2]
           for j in range(4)] for i in range(4)]
    s4 = [[c[i % 2][j % 2] if i // 2 == j // 2 else 0
           for j in range(4)] for i in range(4)]
    gs = mm(g4, s4)
    require(gs == list(map(list, zip(*gs))), "rank-four self-adjointness")
    sq = mm(s4, s4)
    require(all(sq[i][j] + s4[i][j] == 5 * int(i == j)
                for i in range(4) for j in range(4)), "rank-four quadratic")
    require(det(g4) == 205 and sum(s4[i][i] for i in range(4)) == -2,
            "rank-four sharpness")
    require(det([[g0[i][j] + b[i][j] for j in range(2)] for i in range(2)]) == 41
            and det([[g0[i][j] - b[i][j] for j in range(2)] for i in range(2)]) == 5,
            "rank-four positivity")
    g2, s2 = [[2, 1], [1, 2]], [[0, Fraction(5, 2)], [2, -1]]
    gs2 = mm(g2, s2)
    require(gs2 == list(map(list, zip(*gs2))), "rational self-adjointness")
    sq2 = mm(s2, s2)
    require(all(sq2[i][j] + s2[i][j] == 5 * int(i == j)
                for i in range(2) for j in range(2)), "rational quadratic")
    _, h, _, _, _, _ = normal_form(4, (1, 1, 1), omit_cubic=True)
    artificial_rank = rank([[h[i][j] - 21 * int(i == j) for j in range(22)]
                            for i in range(22)])
    require(artificial_rank == 13, "missing-cubic kernel boundary")
    return {"rank_four_Gram_determinant": 205, "rank_four_trace": -2,
            "rank_four_positive_minor_determinants": [41, 5],
            "rational_rank_two_Gram_determinant": 3, "rational_rank_two_trace": -1,
            "artificial_missing_cubic_eigenspace_dimension": 9}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", type=Path, help="optional private graph-control export")
    parser.add_argument("--write-expected", type=Path, help="write compact author-check summary")
    args = parser.parse_args()
    controls = graph_controls()
    graph_records = [audit_graph(x) for x in controls]
    require(len({x["graph_sha256"] for x in graph_records}) == 96, "duplicate graph controls")
    form_records = [audit_form(m, w) for m, w in forms()]
    result = {"agent": "six-books-1", "role": "researcher",
              "proof_role": "validation of an ordinary analytic proof; no host census",
              "signed_graph_controls": 96, "graphs_by_histogram": {str(m): 32 for m in (4, 5, 6)},
              "valid_book_hosts_in_controls": sum(x["all_defects_nonnegative"] for x in graph_records),
              "off_diagonal_entries_checked": 96 * 22 * 21,
              "full_square_entries_checked": 96 * 22 * 22,
              "incident_entries_checked": 96 * 22,
              "K_action_entries_checked": 96 * 22 * 2,
              "general_F_action_entries_checked": 96 * 22 * 2,
              "corrected_positive_vector_entries_checked": 96 * 22,
              "root_budget_controls": 96,
              "red_edge_projection_trace_controls": 96,
              "graph_control_stream_sha256": digest(graph_records),
              "forced_form_records": form_records, "lattice_controls": lattice_controls()}
    if args.controls:
        form_matrices = []
        for m, weights in forms():
            f, h, *_ = normal_form(m, weights)
            form_matrices.append({"m": m, "weights": list(weights), "F": f, "H": h})
        args.controls.write_text(json.dumps({"graphs": controls, "forms": form_matrices},
                                           separators=(",", ":")) + "\n")
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        path = Path(__file__).with_name("degree98_root_saturation_expected.json")
        require(json.loads(path.read_text()) == result, "published summary mismatch")
    print(json.dumps({"agent": "six-books-1", "role": "researcher", "complete": True,
                      "signed_graph_controls": 96, "forced_forms": len(form_records),
                      "all_full_eigenspace_dimensions": [6], "root_defect_lower_bound": 4,
                      "controls_are_validation_only": True}, sort_keys=True))


if __name__ == "__main__":
    main()
