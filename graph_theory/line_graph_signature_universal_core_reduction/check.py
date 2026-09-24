"""Exact author audit: definitions, congruences and constructive replay.

Run with Python 3.11, standard library only. Checks survive python -O.
No imports from any predecessor research package.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
import hashlib
import json

import reduction as build


def need(condition, message):
    if not condition:
        raise ValueError(message)


def inertia(matrix):
    """Exact symmetric elimination with scalar and hyperbolic pivots."""
    n = len(matrix)
    need(all(len(row) == n for row in matrix), "square matrix required")
    need(all(matrix[i][j] == matrix[j][i] for i in range(n)
             for j in range(i)), "symmetric matrix required")
    a = [[F(x) for x in row] for row in matrix]
    live = list(range(n))
    positive = negative = 0
    while live:
        v = next((i for i in live if a[i][i]), None)
        if v is not None:
            diagonal = a[v][v]
            positive += diagonal > 0
            negative += diagonal < 0
            live.remove(v)
            touched = [i for i in live if a[i][v]]
            for offset, i in enumerate(touched):
                for j in touched[offset:]:
                    a[i][j] -= a[i][v]*a[v][j]/diagonal
                    a[j][i] = a[i][j]
            continue
        pair = next(((i, j) for i in live for j in live
                     if i < j and a[i][j]), None)
        if pair is None:
            return positive, len(live), negative
        u, v = pair
        edge = a[u][v]
        live.remove(u)
        live.remove(v)
        touched = [i for i in live if a[i][u] or a[i][v]]
        for offset, i in enumerate(touched):
            for j in touched[offset:]:
                a[i][j] -= (a[i][u]*a[v][j]+a[i][v]*a[u][j])/edge
                a[j][i] = a[i][j]
        positive += 1
        negative += 1
    return positive, 0, negative


def characteristic(matrix):
    """Integer Faddeev--LeVerrier, independent of symmetric elimination."""
    n = len(matrix)
    a = matrix
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n+1):
        b = [[sum(a[i][h]*b[h][j] for h in range(n))
              for j in range(n)] for i in range(n)]
        trace = sum(b[i][i] for i in range(n))
        need(trace % k == 0, "characteristic polynomial division")
        c = -trace//k
        coefficients.append(c)
        for i in range(n):
            b[i][i] += c
    return coefficients


def variations(values):
    signs = [1 if x > 0 else -1 for x in values if x]
    return sum(x != y for x, y in zip(signs, signs[1:]))


def polynomial_inertia(matrix):
    coefficients = characteristic(matrix)
    nonzero = list(coefficients)
    zeros = 0
    while len(nonzero) > 1 and nonzero[-1] == 0:
        nonzero.pop()
        zeros += 1
    p = variations(nonzero)
    q = variations([x*(-1)**i for i, x in enumerate(nonzero)])
    # Real-rootedness of a symmetric characteristic polynomial makes both
    # Descartes bounds exact. This also detects a broken polynomial route.
    need(p+q+zeros == len(matrix), "real-root sign accounting")
    return (p, zeros, q), coefficients


def determinant(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    if not n:
        return 1
    previous = 1
    sign = 1
    for k in range(n-1):
        row = next((i for i in range(k, n) if a[i][k]), None)
        if row is None:
            return 0
        if row != k:
            a[k], a[row] = a[row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = a[i][j]*pivot-a[i][k]*a[k][j]
                need(value % previous == 0, "Bareiss division")
                a[i][j] = value//previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def vertex_matrix(graph):
    n = graph.order
    a = [[0]*n for _ in range(n)]
    for i in range(n):
        a[i][i] = -2
    for u, v in graph.edges:
        a[u][u] += 1
        a[v][v] += 1
        a[u][v] = a[v][u] = 1
    return a


def line_matrix(graph):
    # Literal intersection of the defining edge sets, not an incidence Gram.
    es = [set(e) for e in graph.edges]
    return [[int(i != j and bool(es[i] & es[j])) for j in range(len(es))]
            for i in range(len(es))]


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sig(values):
    return values[0]-values[2]


def congruence(matrix, basis):
    n = len(matrix)
    rows = [[(j, x) for j, x in enumerate(row) if x] for row in basis]
    result = [[F(0)]*n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            x = matrix[a][b]
            if not x:
                continue
            for i, u in rows[a]:
                for j, v in rows[b]:
                    result[i][j] += x*u*v
    return result


def split_basis(graph, vertex, left):
    n = graph.order
    right = graph.neighbors()[vertex]-set(left)
    beta = len(right)-1
    t = [[F(0)]*(n+4) for _ in range(n+4)]
    for i in range(n):
        t[i][i] = 1
    # New coordinate order: old coordinates, A, B0, y, t.
    t[n][vertex] = 1
    t[n][n+2] = 1
    t[n+3][n+3] = 1
    t[n+3][vertex] = -beta
    t[n+3][n+2] = -F(beta, 2)
    for j in right:
        t[n+3][j] = -1
    t[n+1] = [-x for x in t[n+3]]
    t[n+1][n] += 1
    t[n+2][n+1] = 1
    t[n+2][vertex] = -1
    return t


def verify_split(graph, vertex, left):
    enlarged = build.split_vertex(graph, vertex, left)
    n = graph.order
    expected = [[F(0)]*(n+4) for _ in range(n+4)]
    old = vertex_matrix(graph)
    for i in range(n):
        expected[i][:n] = old[i]
    expected[n][n+1] = expected[n+1][n] = 1
    expected[n+2][n+3] = expected[n+3][n+2] = 1
    actual = congruence(vertex_matrix(enlarged), split_basis(graph, vertex, left))
    need(actual == expected, "split matrix congruence")
    return enlarged


def replay(graph, trace):
    """Replay edge changes independently of the constructor's move functions."""
    n = graph.order
    es = set(graph.edges)
    splits = caps = 0
    for record in trace:
        x = record['vertex']
        need(0 <= x < n, "trace vertex")
        if record['move'] == 'split':
            left = set(record['left'])
            neighbors = {v if u == x else u for u, v in es if x in (u, v)}
            need(len(neighbors) >= 4 and len(left) == 2 and left < neighbors,
                 "trace split partition")
            move = {tuple(sorted((x, v))) for v in neighbors-left}
            es -= move
            es |= {tuple(sorted((n, v))) for v in neighbors-left}
            path = [x, n+1, n+2, n+3, n]
            es |= {tuple(sorted(e)) for e in zip(path, path[1:])}
            n += 4
            splits += 1
        elif record['move'] == 'cap':
            need(sum(x in e for e in es) == 1, "cap must close a leaf")
            for cycle in ([n, n+1, n+2, n+3], list(range(n+4, n+9))):
                es |= {tuple(sorted((cycle[i], cycle[(i+1) % len(cycle)])))
                       for i in range(len(cycle))}
            es.add((n, n+4))
            es.add(tuple(sorted((x, n+1))))
            n += 9
            caps += 1
        else:
            raise ValueError("unknown trace move")
    return build.Graph(n, tuple(sorted(es))), splits, caps


def null_basis(rows, width):
    a = [[F(x) for x in row] for row in rows]
    pivots = []
    at = 0
    for col in range(width):
        found = next((i for i in range(at, len(a)) if a[i][col]), None)
        if found is None:
            continue
        a[at], a[found] = a[found], a[at]
        pivot = a[at][col]
        a[at] = [x/pivot for x in a[at]]
        for i in range(len(a)):
            if i != at and a[i][col]:
                factor = a[i][col]
                a[i] = [x-factor*y for x, y in zip(a[i], a[at])]
        pivots.append(col)
        at += 1
    free = [j for j in range(width) if j not in pivots]
    basis = [[F(0)]*len(free) for _ in range(width)]
    for j, col in enumerate(free):
        basis[col][j] = 1
        for i, pivot in enumerate(pivots):
            basis[pivot][j] = -a[i][col]
    return basis, len(pivots)


def parity_inertia(branch_count, paths):
    b = branch_count
    p = [[int(i == j) for j in range(b)] for i in range(b)]
    rows = []
    q = 0
    for u, v, length in paths:
        q += (length-1)//2
        if length % 2:
            sign = 1 if length % 4 == 1 else -1
            p[u][v] += sign
            p[v][u] += sign
        else:
            row = [0]*b
            row[u] += 1
            row[v] += 1 if length % 4 == 2 else -1
            rows.append(row)
    z, rank = null_basis(rows, b)
    dim = b-rank
    r = [[sum(z[u][i]*p[u][v]*z[v][j] for u in range(b) for v in range(b))
          for j in range(dim)] for i in range(dim)]
    restricted = inertia(r)
    return plus(restricted, (q+rank, len(rows)-rank, q+rank)), restricted, rank


def audit_module():
    k = line_matrix(build.MODULE)
    values, polynomial = polynomial_inertia(k)
    need(values == inertia(k) == (6, 0, 5), "module inertia")
    need(determinant(k) == -8, "module determinant")
    entries = {(0, 1): F(1, 2), (1, 2): F(1, 2),
               (2, 3): F(-1, 2), (0, 3): F(-1, 2)}
    vector = [entries.get(e, F(0)) for e in build.MODULE.edges]
    root = build.MODULE.edges.index((1, 9))
    rhs = [sum(x*y for x, y in zip(row, vector)) for row in k]
    need(rhs == [int(i == root) for i in range(len(k))], "module response")
    need(vector[root] == 0, "nonzero root response")
    minor = [[x for j, x in enumerate(row) if j != root]
             for i, row in enumerate(k) if i != root]
    need(determinant(minor) == 0, "module root cofactor")
    return {'vertices': 10, 'edges': 11, 'inertia': values,
            'determinant': -8, 'root_cofactor': 0,
            'characteristic_polynomial': polynomial,
            'inverse_root_column': [str(x) for x in vector]}


def connected_graphs(order):
    possible = list(combinations(range(order), 2))
    for mask in range(1 << len(possible)):
        graph = build.Graph(order, tuple(e for i, e in enumerate(possible)
                                         if mask >> i & 1))
        if graph.connected():
            yield graph


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                        separators=(',', ':')).encode()).hexdigest()


def audit_all_small():
    counts = Counter()
    histogram = Counter()
    h = hashlib.sha256()
    totals = Counter()
    largest = 0
    for order in range(2, 6):
        for original in connected_graphs(order):
            index = totals['inputs']
            counts[order] += 1
            totals['inputs'] += 1
            adj = original.neighbors()
            ell = sum(len(row) == 1 for row in adj)
            a = sum(max(len(row)-3, 0) for row in adj)
            c = original.cyclomatic()
            old_m = inertia(vertex_matrix(original))
            old_l = inertia(line_matrix(original))
            poly_m, _ = polynomial_inertia(vertex_matrix(original))
            need(poly_m == old_m, "old polynomial inertia")
            need(old_l == plus(old_m, (0, 0, c-1)), "old incidence inertia")
            core, trace = build.to_core(original)
            rebuilt, splits, caps = replay(original, trace)
            need(rebuilt == core and splits == a and caps == ell, "trace replay")
            need(core.order == order+4*a+9*ell, "vertex count")
            need(len(core.edges) == len(original.edges)+4*a+11*ell, "edge count")
            need(core.cyclomatic() == c+2*ell, "cycle count")
            need(all(2 <= len(row) <= 3 for row in core.neighbors()), "core degree")
            new_m = inertia(vertex_matrix(core))
            need(new_m == plus(old_m, (2*a+6*ell, 0, 2*a+3*ell)), "core inertia")
            new_l = plus(new_m, (0, 0, core.cyclomatic()-1))
            need(new_l == plus(old_l, (2*a+6*ell, 0, 2*a+5*ell)), "line inertia")
            need(2*sig(old_l)-c-1 == 2*sig(new_l)-core.cyclomatic()-1,
                 "conjecture slack")
            if index % 29 == 0 or core.order <= 8:
                need(inertia(line_matrix(core)) == new_l, "literal enlarged line graph")
                totals['direct_output_line_inertias'] += 1
            if core.cyclomatic() >= 2:
                branches, paths = build.branch_paths(core)
                need(len(branches) == 2*core.cyclomatic()-2, "branch count")
                predicted, restricted, rank = parity_inertia(len(branches), paths)
                need(predicted == new_m, "parity form inertia")
                need(4*sig(restricted)-3*len(branches)-4 ==
                     2*(2*sig(old_l)-c-1), "universal matrix slack")
                small, representative_paths = build.residue_representative(core)
                small_m = inertia(vertex_matrix(small))
                predicted_small, rr, _ = parity_inertia(len(branches), representative_paths)
                need(small_m == predicted_small and sig(small_m) == sig(new_m)
                     and small_m[1] == new_m[1], "compact representative")
                need(rr == restricted, "identical restricted inertia")
                need(small.cyclomatic() == c+2*ell, "representative cycles")
                totals['parity_and_representative_cases'] += 1
                largest = max(largest, small.order)
            totals['split_moves'] += splits
            totals['cap_moves'] += caps
            totals['output_vertices'] += core.order
            totals['output_edges'] += len(core.edges)
            histogram[(c, ell, a)] += 1
            h.update(json.dumps([original.edges, core.edges, old_l, new_l,
                                 trace], separators=(',', ':')).encode()+b'\n')
    return {'counts_by_order': dict(sorted(counts.items())),
            'totals': dict(sorted(totals.items())),
            'maximum_compact_order': largest,
            'input_parameter_histogram': [[*k, v] for k, v in sorted(histogram.items())],
            'entrywise_sha256': h.hexdigest()}


def audit_local_splits():
    count = 0
    singular = 0
    h = hashlib.sha256()
    # All host graphs through four vertices, including disconnected hosts:
    # the matrix identity itself does not require connectivity.
    for n in range(3, 5):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            graph = build.Graph(n, tuple(e for i, e in enumerate(pairs) if mask >> i & 1))
            for v, row in enumerate(graph.neighbors()):
                ns = sorted(row)
                for bits in range(1, (1 << len(ns))-1):
                    left = [x for i, x in enumerate(ns) if bits >> i & 1]
                    new = verify_split(graph, v, left)
                    original_inertia = inertia(vertex_matrix(graph))
                    need(inertia(vertex_matrix(new)) == plus(original_inertia, (2, 0, 2)),
                         "local split inertia")
                    singular += original_inertia[1] > 0
                    count += 1
                    h.update(json.dumps([n, graph.edges, v, left],
                                        separators=(',', ':')).encode()+b'\n')
    # Unequal and large neighbor parts, with arbitrary edges among ports.
    for n in (5, 8, 11):
        for complete in (False, True):
            graph = build.make_graph(n, combinations(range(n), 2) if complete else
                                     [(0, v) for v in range(1, n)])
            for cut in range(1, n-1):
                verify_split(graph, 0, list(range(1, cut+1)))
                count += 1
    return {'exact_congruences': count, 'singular_small_inputs': singular,
            'small_input_sha256': h.hexdigest()}


def audit_residues():
    records = []
    kernels = [
        (2, [(0, 0), (0, 1), (1, 1)]),
        (2, [(0, 1)]*3),
        (4, [(0, 0), (0, 1), (1, 2), (1, 2), (2, 3), (3, 3)]),
    ]
    count = 0
    for n, edges in kernels:
        # Complete four-residue assignments on both two-vertex kernels.
        # A fixed modular schedule exercises the six-edge kernel.
        assignments = (product(range(4), repeat=len(edges)) if n == 2 else
                       ((j % 4, j//4 % 4, j//16 % 4, (3*j+1) % 4,
                         (j//4+2) % 4, (j//16+3) % 4) for j in range(64)))
        histogram = Counter()
        h = hashlib.sha256()
        for residues in assignments:
            paths = [(u, v, {0: 4, 1: 5, 2: 6 if u == v else 2, 3: 3}[r])
                     for (u, v), r in zip(edges, residues)]
            graph = build.realize(n, paths)
            predicted, restricted, rank = parity_inertia(n, paths)
            actual = inertia(vertex_matrix(graph))
            need(actual == predicted, "residue realization")
            histogram[(sig(restricted), rank, actual[1])] += 1
            bigger = build.four_subdivide(graph, graph.edges[0])
            need(inertia(vertex_matrix(bigger)) == plus(actual, (2, 0, 2)),
                 "four-subdivision")
            if count % 11 == 0:
                need(inertia(line_matrix(bigger)) ==
                     plus(inertia(line_matrix(graph)), (2, 0, 2)), "line subdivision")
            h.update(json.dumps([paths, actual], separators=(',', ':')).encode()+b'\n')
            count += 1
        records.append({'branch_count': n, 'kernel_edges': edges,
                        'histogram': [[*k, v] for k, v in sorted(histogram.items())],
                        'entrywise_sha256': h.hexdigest()})
    return {'cases': count, 'kernels': records}


def negative_controls():
    triangle = build.make_graph(3, [(0, 1), (0, 2), (1, 2)])
    rejected = []
    calls = [
        ('duplicate_edge', lambda: build.make_graph(2, [(0, 1), (1, 0)])),
        ('loop_in_simple_graph', lambda: build.make_graph(2, [(0, 0)])),
        ('empty_split', lambda: build.split_vertex(triangle, 0, [])),
        ('full_split', lambda: build.split_vertex(triangle, 0, [1, 2])),
        ('nonneighbor_split', lambda: build.split_vertex(triangle, 0, [1, 3])),
        ('invalid_cap_port', lambda: build.attach_module(triangle, 3)),
        ('singleton_input', lambda: build.to_core(build.Graph(1, ()))),
        ('disconnected_input', lambda: build.to_core(build.make_graph(3, [(0, 1)]))),
        ('noncubic_kernel', lambda: build.realize(2, [(0, 1, 3)])),
        ('length_two_loop', lambda: build.realize(2, [(0, 0, 2), (0, 1, 1), (1, 1, 3)])),
        ('parallel_direct_edges', lambda: build.realize(2, [(0, 1, 1)]*3)),
        ('cap_at_nonleaf_trace', lambda: replay(triangle, [{'move': 'cap', 'vertex': 0}])),
    ]
    for name, call in calls:
        try:
            call()
        except (ValueError, RuntimeError):
            rejected.append(name)
        else:
            raise ValueError('negative control accepted: '+name)
    basis = split_basis(triangle, 0, [1])
    basis[0][0] += 1
    good = congruence(vertex_matrix(build.split_vertex(triangle, 0, [1])),
                      split_basis(triangle, 0, [1]))
    bad = congruence(vertex_matrix(build.split_vertex(triangle, 0, [1])), basis)
    need(good != bad, "corrupted congruence was not detected")
    rejected.append('corrupted_split_basis')
    k = line_matrix(build.MODULE)
    rho = build.MODULE.edges.index((1, 9))
    k[rho][0] = k[0][rho] = 0
    need(determinant(k) != -8, "corrupted module was not detected")
    rejected.append('corrupted_module_edge')
    return rejected


def main():
    output = {'module': audit_module(), 'local_splits': audit_local_splits(),
              'all_connected_labelled_through_five': audit_all_small(),
              'residue_boundaries': audit_residues(),
              'negative_controls': negative_controls()}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
