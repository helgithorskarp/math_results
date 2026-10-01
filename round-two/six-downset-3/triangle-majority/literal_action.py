"""Build literal basis vectors and compare actual action with expected sector forms."""
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
from model import formula, model
from poly import R


def require(ok, message):
    if not ok:
        raise ValueError(message)


def nullspace(matrix):
    """Ordinary rational RREF, not a polynomial/Schur algorithm."""
    a = [list(map(F, row)) for row in matrix]
    require(a and len({len(row) for row in a}) == 1, 'bad RREF input')
    width, pivots, row = len(a[0]), [], 0
    for col in range(width):
        p = next((i for i in range(row, len(a)) if a[i][col]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        scale = a[row][col]
        a[row] = [v/scale for v in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [x-scale*y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    result = []
    for col in range(width):
        if col not in pivots:
            v = [F(int(j == col)) for j in range(width)]
            for i, p in enumerate(pivots):
                v[p] = -a[i][col]
            result.append(v)
    require(all(not sum(x*y for x, y in zip(r, v)) for r in matrix for v in result),
            'RREF nullspace residual')
    return len(pivots), result


def literal(q, c_override=None):
    require(type(q) is int and q == 4, 'literal action check covers q=4')
    points = range(q+3)
    members = sorted(sum(1 << i for i in t)
                     for size in [1, 2, 3] for t in combinations(points, size)
                     if size < 3 or sum(i < 3 for i in t) >= 2)
    typ = lambda mask: ((mask & 7).bit_count(), (mask >> 3).bit_count())
    weights = formula(F(q))
    s = 3*q+4
    c = [[F(s*int(a == b)-1)+(weights[tuple(sorted((typ(a), typ(b))))] if not a & b else 0)
          for b in members] for a in members]
    if c_override is not None:
        c = c_override
    edges = list(combinations(range(q), 2))
    incidence = [[int(i in edge) for edge in edges] for i in range(q)]
    incidence_rank, harmonic = nullspace(incidence)
    require(incidence_rank == q and len(harmonic) == q*(q-3)//2, 'edge harmonic dimensions differ')
    point_basis = lambda count: [[int(i == k)-int(i == count-1) for i in range(count)]
                                 for k in range(count-1)]
    core = {0: [None], 1: point_basis(3)}
    outside = {0: [None], 1: point_basis(q), 2: harmonic}
    def vector(degree, cb, ob, level):
        j, ell = degree
        result = []
        for mask in members:
            if typ(mask) != level:
                result.append(F(0)); continue
            core_value = 1 if j == 0 else sum(cb[i] for i in range(3) if mask >> i & 1)
            if ell == 0:
                out_value = 1
            elif ell == 1:
                out_value = sum(ob[i] for i in range(q) if mask >> (i+3) & 1)
            else:
                selected = tuple(i for i in range(q) if mask >> (i+3) & 1)
                out_value = ob[edges.index(selected)]
            result.append(F(core_value*out_value))
        return result
    data = model(R(q), weights)
    columns, records, trials = [], [], []
    for sector in data:
        degree, levels = sector['degree'], sector['levels']
        j, ell = degree
        count = 0
        for cb, ob in product(core[j], outside[ell]):
            basis = [vector(degree, cb, ob, level) for level in levels]
            columns.extend(basis)
            for k, v in enumerate(basis):
                actual = [sum(row[h]*v[h] for h in range(len(members))) for row in c]
                expected = [sum((sector['lower'][i][k]/sector['norms'][i]).at(0)*basis[i][h]
                                for i in range(len(levels))) for h in range(len(members))]
                require(actual == expected, 'literal matrix sector action differs')
                trials.append((actual, expected))
                count += 1
        records.append({'sector': list(degree), 'level_count': len(levels),
                        'copies': len(core[j])*len(outside[ell]), 'action_vectors': count})
    check_columns(columns, len(members))
    require(sum(r['action_vectors'] for r in records) == len(members) == 41,
            'literal total dimensions differ')
    return {'q': q, 'dimension': len(members), 'literal_basis_rank': len(members),
            'point_edge_incidence_rank': incidence_rank, 'harmonic_edge_dimension': len(harmonic),
            'sectors': records}, columns, trials


def check_columns(columns, dimension):
    require(len(columns) == dimension and all(len(v) == dimension for v in columns),
            'literal basis coverage differs')
    rank, _ = nullspace([[v[i] for v in columns] for i in range(dimension)])
    require(rank == dimension, 'literal basis is dependent')


if __name__ == '__main__':
    result, _, _ = literal(4)
    print(json.dumps(result))
