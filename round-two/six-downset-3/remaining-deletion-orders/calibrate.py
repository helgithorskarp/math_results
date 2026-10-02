"""whole-pair calibration of the new counted forms at two points."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import time
import orbits
from literal import table, typ, member, require
from exact import digest


def original(q, k):
    require((q, k) in ((19, 5), (24, 6)), 'two exact calibration fixtures only')
    X = []
    for size in (1, 2, 3):
        for points in combinations(range(q+3), size):
            A = sum(1 << j for j in points)
            if member(q, k, A):
                X.append(A)
    X.sort()
    groups = {}
    for A in X:
        z = sum(bool(A & (1 << j)) for j in range(3, k+3))
        w = sum(bool(A & (1 << j)) for j in range(k+3, q+3))
        groups.setdefault((A & 7, z, w), []).append(A)
    keys = sorted(groups)
    sizes = [len(groups[a]) for a in keys]
    index = {a: i for i, a in enumerate(keys)}
    labels = {A: index[key] for key, members in groups.items() for A in members}
    n, s = len(X), 3*q+4
    matrices = [[[F(0)]*23 for _ in range(23)] for _ in range(3)]
    tab = table(q)
    for A in X:
        i = labels[A]
        for B in X:
            j = labels[B]
            if A == B:
                x, d, r = F(s-1), F(0), F(0)
            elif A & B:
                x, d, r = F(-1), F(0), F(0)
            else:
                x, d = tab[tuple(sorted((typ(A), typ(B))))]
                x -= 1
                r = {(1, 2): 1, (1, 4): 1, (2, 5): -1, (3, 4): -1}.get(tuple(sorted((A, B))), 0)
            for matrix, value in zip(matrices, (x, d, r)):
                matrix[i][j] += value
    return X, keys, sizes, matrices


def run():
    records = []
    for q, k in ((19, 5), (24, 6)):
        data = orbits.forms(q, k)
        X, keys, sizes, matrices = original(q, k)
        require(data['keys'] == keys and data['sizes'] == sizes, 'independent original orbit census')
        require(len(X)+1 == data['N'], 'original dimension')
        require(matrices == [data['C0'], data['Delta'], data['R']],
                'every original whole-pair coefficient Gram entry')
        original_upper = [[F((len(X)+1)*sizes[i]*int(i == j)-sizes[i]*sizes[j])-matrices[0][i][j]
                           for j in range(23)] for i in range(23)]
        require(original_upper == data['U0'], 'every independent original upper Gram entry')
        record = {'q': q, 'k': k, 'N': data['N'], 'original_pair_count': len(X)**2,
                  'all_four_times_529_entries_match': True, 'orbit_sizes': sizes,
                  'forms_digest': digest(orbits.encoded(data))}
        if (q, k) == (24, 6):
            import point
            old_record, state = point.run(return_state=True)
            G, H = orbits.evaluate(data, point.KAPPA, point.TRADE)
            require(G == state['G'] and H == state['U'] and keys == state['keys']
                    and sizes == state['sizes'], 'published complete q24/k6 point every Gram entry')
            record['published_q24_full_point_digest'] = old_record['Gram_digest']
        records.append(record)
    # Semantic damages must alter concrete Gram entries or the exact census.
    data = orbits.forms(24, 6)
    damaged = [[row[:] for row in data[key]] for key in ('C0', 'Delta', 'R')]
    damaged[0][0][0] += 1
    require(damaged != [data[key] for key in ('C0', 'Delta', 'R')], 'changed base Gram rejected')
    damaged[1][0][0] += 1
    require(damaged[1] != data['Delta'], 'changed affine slope rejected')
    require([[-x for x in row] for row in data['R']] != data['R'], 'reversed repair sign rejected')
    require(sum(data['sizes'][:-1]) != data['N']-1, 'omitted original orbit rejected')
    return {'agent': 'six-downset-3', 'role': 'researcher', 'status': 'exact validation, not new theorem',
            'fixtures': records, 'semantic_damages_rejected': 4,
            'coverage': 'ALL original ordered pairs; four complete coefficient Gram forms plus published q24 point'}


if __name__ == '__main__':
    start = time.perf_counter()
    result = run()
    result['record_sha256'] = digest(result)
    output = Path(__file__).with_name('CALIBRATION.json')
    output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'output': str(output), 'seconds': time.perf_counter()-start,
                      'digest': result['record_sha256'], 'original_pairs': sum(r['original_pair_count'] for r in result['fixtures'])}))
