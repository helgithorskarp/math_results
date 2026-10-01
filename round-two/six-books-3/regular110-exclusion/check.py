"""Exact validation of the analytic four-cycle packing and known cubic census."""
import ast
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import census

HERE = Path(__file__).parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def decode_g6(line):
    need(len(line) == 9 and ord(line[0]) - 63 == 10, 'Invalid ten-point graph6')
    bits = [(ord(c) - 63 >> k) & 1 for c in line[1:] for k in range(5, -1, -1)]
    need(all(0 <= ord(c) - 63 < 64 for c in line[1:]), 'Invalid graph6 character')
    need(not any(bits[45:]), 'Nonzero graph6 padding')
    adj = [0] * 10
    position = 0
    for j in range(1, 10):
        for i in range(j):
            if bits[position]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            position += 1
    return adj


def capacity(adj, i, j):
    common = (adj[i] & adj[j]).bit_count()
    return 1 - common if adj[i] >> j & 1 else 4 - common


def four_cycles(adj):
    for points in combinations(range(10), 4):
        mask = sum(1 << i for i in points)
        if all((adj[i] & mask).bit_count() == 2 for i in points):
            yield points


def validate_cycle(adj, points):
    need(len(points) == 4 and len(set(points)) == 4 and all(0 <= i < 10 for i in points),
         'Invalid four-cycle vertex set')
    mask = sum(1 << i for i in points)
    need(all((adj[i] & mask).bit_count() == 2 for i in points), 'Set is not an induced four-cycle')
    value = sum(capacity(adj, i, j) for i, j in combinations(points, 2))
    need(value <= 8, 'Four-cycle capacity exceeds eight')
    return value


def pack_table():
    need(all((t - 1) * (t - 2) // 2 >= 0 for t in range(5)), 'False integer inequality')
    histogram = Counter()
    for n0, n1, n2, n3 in product(range(12), repeat=4):
        n4 = 11 - n0 - n1 - n2 - n3
        if n4 >= 0 and n1 + 2*n2 + 3*n3 + 4*n4 == 20:
            cost = n2 + 3*n3 + 6*n4
            histogram[cost] += 1
    need(min(histogram) == 9, 'Packing lower bound failed')
    return {str(k): v for k, v in sorted(histogram.items())}


def baseline():
    data = (HERE / 'primary21.txt').read_bytes()
    need(sha256(data).hexdigest() == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
         'Primary21 fixture changed')
    matrix = ast.literal_eval(data.decode().split('\n\n', 1)[0])
    need(len(matrix) == 21 and all(len(r) == 21 for r in matrix), 'Wrong baseline dimensions')
    need(all(matrix[i][j] in (0, 1) and matrix[i][j] == matrix[j][i]
             for i, j in combinations(range(21), 2)), 'Invalid baseline adjacency')
    result = {}
    for label, color in [('red', 0), ('blue', 1)]:
        adj = [sum(1 << j for j in range(21) if j != i and matrix[i][j] == color)
               for i in range(21)]
        edges = [(i, j) for i, j in combinations(range(21), 2) if matrix[i][j] == color]
        result[label] = {'edges': len(edges), 'max_pages': max((adj[i] & adj[j]).bit_count()
                                                             for i, j in edges)}
    need(result == {'red': {'edges': 93, 'max_pages': 3},
                    'blue': {'edges': 117, 'max_pages': 6}}, 'Known21 baseline failed')
    return result


def run():
    result = census.enumerate_cores()
    maps, normal = census.normalizations()
    data = (HERE / 'primary_cubic10_g4.g6').read_bytes()
    need(sha256(data).hexdigest() == '01324766dc1dfd3b64a9ab130f4162684e9df86f7fee664e6c904e0471eff285',
         'Primary cubic fixture changed')
    keys = set()
    for line in data.decode().splitlines():
        adj = decode_g6(line)
        need(all(m.bit_count() == 3 for m in adj), 'Noncubic primary graph')
        need(not any(adj[i] & adj[j] for i, j in combinations(range(10), 2)
                     if adj[i] >> j & 1), 'Primary graph has a triangle')
        keys.add(min(census.rooted_key(adj, r, maps, normal) for r in range(10)))
    need(keys == {(tuple(c['key'][0]), c['key'][1]) for c in result['cores']},
         'Primary six-core comparison failed')
    for core in result['cores']:
        adj = core['neighbors']
        cycles = list(four_cycles(adj))
        core['four_cycle_count'] = len(cycles)
        core['four_cycle_witness'] = list(cycles[0]) if cycles else None
        core['witness_capacity_sum'] = validate_cycle(adj, cycles[0]) if cycles else None
        if cycles:
            need(core['witness_capacity_sum'] <= 8, 'Four-cycle cut failed')
        else:
            need(all((adj[i] & adj[j]).bit_count() == (0 if adj[i] >> j & 1 else 1)
                     for i, j in combinations(range(10), 2)), 'Petersen parameters failed')
    result['packing_cost_distribution'] = pack_table()
    result['known21'] = baseline()
    return result


if __name__ == '__main__':
    expected = json.loads((HERE / 'expected.json').read_text())
    actual = run()
    need(actual == expected['generator'], 'Expected generator result differs')
    print(json.dumps({'status': 'PASS', 'agent': 'six-books-3', 'role': 'researcher',
                      'rooted_classes': actual['rooted_classes'], 'known_cubic_classes': actual['unrooted_classes'],
                      'packing_minimum': min(map(int, actual['packing_cost_distribution'])),
                      'excluded_non_Petersen_types': 5, 'known21': actual['known21']}, sort_keys=True))
