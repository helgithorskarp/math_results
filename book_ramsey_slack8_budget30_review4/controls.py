"""Boundary and positive controls for six-reviewer-4's budget30 audit."""
from itertools import combinations, permutations
from pathlib import Path
import json
import audit as a


def rejected(function):
    try:
        function()
    except ValueError:
        return True
    raise ValueError('Invalid or incomplete control was accepted')


def run():
    types = ((8, 2), (8, 2), (10, 2), (10, 2))
    weights = (2, 0, 0, 0, 0, 2)
    pairs = list(combinations(range(4), 2))
    slots = {p: i for i, p in enumerate(pairs)}
    key = a.canonical_core(types, weights)
    for p in permutations(range(4)):
        renamed = tuple(weights[slots[tuple(sorted((p[i], p[j])))]] for i, j in pairs)
        a.require(a.canonical_core(tuple(types[i] for i in p), renamed) == key,
                  'all24 center relabelings give the same complete key')
    a.require(rejected(lambda: a.determinant_crt([[10**30]], [])), 'insufficient CRT is rejected')

    nonsymmetric = [[0, 33], [1, 0]]
    a.require(a.multiply(nonsymmetric, nonsymmetric) == [[33, 0], [0, 33]] and
              nonsymmetric != list(map(list, zip(*nonsymmetric))),
              'rational33 roots exist when symmetry is omitted')
    reducible_Q, L, mixed_root = [[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1, 0], [0, -1]]
    a.require(a.multiply(mixed_root, mixed_root) == reducible_Q and
              sum(mixed_root[i][i] for i in range(2)) not in
              {sum(L[i][i] for i in range(2)), -sum(L[i][i] for i in range(2))},
              'irreducibility is essential to the two-root field argument')

    small_L = [[1, 2], [1, 1]]
    small_Q = a.multiply(small_L, small_L)
    a.require(all((x*x-6*x+1) % 3 for x in range(3)), 'small quotient irreducible modulo3')
    traces = set()
    for sign in (-1, 1):
        for scalar in (-5, 5):
            root = [[scalar, 0, 0], [0, sign, 2*sign], [0, sign, sign]]
            square = [[25, 0, 0], [0, small_Q[0][0], small_Q[0][1]],
                      [0, small_Q[1][0], small_Q[1][1]]]
            a.require(a.multiply(root, root) == square, 'small exact field-root positive control')
            traces.add(sum(root[i][i] for i in range(3)))
    a.require(traces == {-7, -3, 3, 7}, 'all four small predicted trace values realized')

    rows = Path(__file__).with_name('baseline21.rows').read_text().splitlines()
    a.require(len(rows) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in rows),
              'known21 baseline dimensions')
    R = [[int(x) for x in row] for row in rows]
    a.require(all(R[i][i] == 0 and R[i][j] == R[j][i] for i in range(21) for j in range(21)),
              'known21 baseline simple and symmetric')
    B = [[int(i != j)-R[i][j] for j in range(21)] for i in range(21)]
    maxima = [max(sum(M[i][k]*M[j][k] for k in range(21))
                  for i, j in combinations(range(21), 2) if M[i][j]) for M in (R, B)]
    edges = sum(map(sum, R))//2
    a.require(edges == 93 and maxima == [3, 6], 'credited21 baseline pages and edges')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'all_passed': True, 'canonical_relabelings': 24, 'incomplete_CRT_rejected': True,
            'rational33_symmetry_boundary_checked': True, 'reducible_quotient_boundary_checked': True,
            'small_irreducible_field_positive_traces': sorted(traces),
            'credited_baseline21_edges': edges, 'credited_baseline21_max_pages': maxima}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
