#!/usr/bin/env python3
"""Exact corroboration of the written theorem; Python 3.11+, no dependencies.

All HNF lattices <(a,0),(b,c)> of index at most 60 are tested, without
identifying isomorphic triangulations. The proof has no finite-size cutoff.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

AXES = ((1, 0), (0, 1), (1, -1))
STEPS = AXES + tuple((-x, -y) for x, y in AXES)


def rank_f2(columns):
    basis = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot in basis:
                column ^= basis[pivot]
            else:
                basis[pivot] = column
                break
    return len(basis)


def unit_reduce(matrix):
    """Integer unimodular pivots only; return unit rank and residual matrix.

    A nonzero residual is NOT declared torsion-free or diagonal. This modest
    certificate suffices for the chosen fixtures; no general Smith claim.
    """
    matrix = [row[:] for row in matrix]
    rank = 0
    while matrix and matrix[0]:
        pivot = next(((i, j) for i, row in enumerate(matrix)
                      for j, value in enumerate(row) if abs(value) == 1), None)
        if pivot is None:
            break
        i, j = pivot
        matrix[0], matrix[i] = matrix[i], matrix[0]
        for row in matrix:
            row[0], row[j] = row[j], row[0]
        if matrix[0][0] == -1:
            matrix[0] = [-x for x in matrix[0]]
        head = matrix[0]
        matrix = [[x - row[0] * y for x, y in zip(row[1:], head[1:])]
                  for row in matrix[1:]]
        # Column operations clear the pivot row without changing this block.
        rank += 1
    return rank, matrix


def construct(a, b, c):
    assert a > 0 and c > 0 and 0 <= b < a
    def reduce(x, y):
        q, r = divmod(y, c)
        return ((x - b*q) % a)*c + r
    vertices = [(x, y) for x in range(a) for y in range(c)]
    n = len(vertices)
    adj = [{reduce(x+dx, y+dy) for dx, dy in STEPS} for x, y in vertices]
    if any(len(row) != 6 or i in row for i, row in enumerate(adj)):
        return None
    assert all(i in adj[j] for i in range(n) for j in adj[i])
    faces = set()
    oriented = []
    for x, y in vertices:
        oriented.extend(((reduce(x, y), reduce(x+1, y), reduce(x, y+1)),
                         (reduce(x+1, y+1), reduce(x, y+1), reduce(x+1, y))))
    for face in oriented:
        assert len(set(face)) == 3
        faces.add(tuple(sorted(face)))
    edges = sorted((i, j) for i in range(n) for j in adj[i] if i < j)
    assert len(edges) == 3*n and len(faces) == 2*n
    incidence = Counter(e for f in faces for e in combinations(f, 2))
    assert set(incidence) == set(edges) and set(incidence.values()) == {2}
    # Integral cancellation certifies the orientation, independently of F2.
    oriented_boundary = Counter()
    for i, j, k in oriented:
        for s, t in ((i, j), (j, k), (k, i)):
            oriented_boundary[tuple(sorted((s, t)))] += 1 if s < t else -1
    assert not any(oriented_boundary.values())
    for i in range(n):
        link = [tuple(v for v in face if v != i) for face in faces if i in face]
        assert len(link) == 6
        assert set(Counter(v for e in link for v in e).values()) == {2}
        reached = {min(adj[i])}
        while True:
            new = reached | {v for e in link if set(e) & reached for v in e}
            if new == reached:
                break
            reached = new
        assert reached == adj[i]
    reached = {0}
    while True:
        new = reached | {j for i in reached for j in adj[i]}
        if new == reached:
            break
        reached = new
    assert len(reached) == n
    # Connected, closed, oriented simplicial surface with chi=0: a torus.
    triangles = sorted((i, j, k) for i in range(n) for j in adj[i] if i < j
                       for k in adj[i] & adj[j] if j < k)
    assert faces <= set(triangles)
    k4 = next(((i, j, k, min(adj[i] & adj[j] & adj[k]))
               for i, j, k in triangles if adj[i] & adj[j] & adj[k]), None)
    return n, vertices, reduce, adj, faces, edges, triangles, k4


def check(a, b, c):
    data = construct(a, b, c)
    row = {'hnf': [a, b, c], 'n': a*c}
    if data is None:
        return dict(row, case='invalid')
    n, vertices, reduce, adj, faces, edges, triangles, k4 = data
    if k4:
        return dict(row, case='K4_excluded')
    missing = set(triangles) - faces
    axes = [s for s in AXES if reduce(3*s[0], 3*s[1]) == 0]
    predicted = {tuple(sorted(reduce(x+t*dx, y+t*dy) for t in range(3)))
                 for dx, dy in axes for x, y in vertices}
    assert missing == predicted, (a, b, c, missing, predicted)
    assert len(axes) in (0, 1, 3)
    if not axes:
        assert not missing
        case, target = 'torus', [1, 2, 1]
    elif len(axes) == 1:
        assert len(missing)*3 == n
        assert set(Counter(v for face in missing for v in face).values()) == {1}
        case, target = 'one_axis', [1, 1, n//3]
    else:
        assert n == 9
        parts = {frozenset(set(range(n)) - adj[i]) for i in range(n)}
        assert len(parts) == 3 and set(map(len, parts)) == {3}
        assert set.union(*(set(p) for p in parts)) == set(range(n))
        assert all((j in adj[i]) == (next(p for p in parts if i in p) !=
                                    next(p for p in parts if j in p))
                   for i in range(n) for j in range(n))
        case, target = 'three_axes', [1, 0, 8]
    index = {edge: i for i, edge in enumerate(edges)}
    columns = [sum(1 << index[e] for e in combinations(t, 2)) for t in triangles]
    rank = rank_f2(columns)
    betti = [1, len(edges) - n + 1 - rank, len(triangles) - rank]
    assert betti == target, (a, b, c, betti, target)
    return dict(row, case=case, missing=len(missing), betti_f2=betti)


def integral_fixture(a, b, c):
    data = construct(a, b, c)
    assert data is not None
    n, _, _, adj, _, edges, triangles, k4 = data
    assert k4 is None
    # Collapse a spanning tree: the remaining edge coordinates present H1.
    reached, tree, queue = {0}, set(), [0]
    for i in queue:
        for j in sorted(adj[i]):
            if j not in reached:
                reached.add(j)
                queue.append(j)
                tree.add(tuple(sorted((i, j))))
    assert len(tree) == n - 1
    remaining = [e for e in edges if e not in tree]
    index = {e: i for i, e in enumerate(remaining)}
    matrix = [[0]*len(triangles) for _ in remaining]
    for column, (i, j, k) in enumerate(triangles):
        for edge, sign in (((i, j), 1), ((j, k), 1), ((i, k), -1)):
            if edge in index:
                matrix[index[edge]][column] = sign
    rank, residual = unit_reduce(matrix)
    assert not any(value for row in residual for value in row)
    betti = [1, len(remaining)-rank, len(triangles)-rank]
    assert betti == check(a, b, c)['betti_f2']
    return {'hnf': [a, b, c], 'betti_Z': betti, 'H1_torsion': [],
            'unit_pivots': rank, 'nonzero_residual_entries': 0}


def run():
    bound = 60
    rows = [check(a, b, c) for a in range(1, bound+1)
            for c in range(1, bound//a+1) for b in range(a)]
    assert len(rows) == sum(sum(d for d in range(1, n+1) if n % d == 0)
                            for n in range(1, bound+1))
    fixtures = [integral_fixture(*p) for p in
                ((4, 0, 4), (3, 0, 4), (3, 1, 4), (3, 2, 5), (3, 0, 3))]
    # Hypothesis controls: these really are simplicial degree-six tori,
    # but the graph has K4, so the full flag complex is higher-dimensional.
    controls = []
    for p, clique_number in (((7, 2, 1), 7), ((4, 1, 2), 4)):
        data = construct(*p)
        assert data is not None and data[-1] is not None
        n, _, _, adj, *_ = data
        omega = max(k for k in range(n+1) if any(
            all(j in adj[i] for i, j in combinations(s, 2))
            for s in combinations(range(n), k)))
        assert omega == clique_number
        controls.append({'hnf': list(p), 'n': n, 'clique_number': omega})
    rank, residual = unit_reduce([[2]])
    assert rank == 0 and residual == [[2]]  # Do not silently discard torsion.
    serial = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    return {'hnf_index_bound': bound, 'parameter_tuples': len(rows),
            'counts': dict(sorted(Counter(r['case'] for r in rows).items())),
            'row_sha256': sha256(serial).hexdigest(),
            'integral_fixtures': fixtures, 'K4_controls': controls,
            'torsion_guard': 'nonunit residual retained'}


if __name__ == '__main__':
    result = run()
    if '--emit' not in sys.argv[1:]:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result == expected, (result, expected)
        print('PASS: exact checks match expected.json')
    print(json.dumps(result, sort_keys=True, indent=2))
