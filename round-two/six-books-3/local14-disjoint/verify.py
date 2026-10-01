"""Separate binary-edge census, generator-walk quotient and literal audit.

Imports no census program or published predecessor. All guards work under -O.
"""
import ast
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDGES = tuple((i, j) for i in range(8) for j in range(i + 1, 8))
LOOKUP = {edge: bit for bit, edge in enumerate(EDGES)}


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def binary_census():
    """Include or omit individual edges, with exact remaining degree bounds."""
    variables = [bit for bit, edge in enumerate(EDGES)
                 if edge not in ((0, 1), (2, 3))]
    suffix = []
    for pos in range(len(variables) + 1):
        suffix.append([sum(i in EDGES[bit] for bit in variables[pos:])
                       for i in range(8)])
    degree = [0] * 8
    target = [2] * 4 + [3] * 4
    result = set()

    def visit(pos, mask):
        if any(degree[i] > target[i]
               or degree[i] + suffix[pos][i] < target[i] for i in range(8)):
            return
        if pos == len(variables):
            need(degree == target, 'Incorrect binary leaf')
            need(mask not in result, 'Duplicate binary leaf')
            result.add(mask)
            return
        visit(pos + 1, mask)
        bit = variables[pos]
        i, j = EDGES[bit]
        degree[i] += 1
        degree[j] += 1
        visit(pos + 1, mask | (1 << bit))
        degree[i] -= 1
        degree[j] -= 1

    visit(0, 0)
    return result


def literal_core(mask):
    graph = [[0] * 10 for _ in range(10)]
    for bit, (i, j) in enumerate(EDGES):
        if mask >> bit & 1:
            graph[i + 2][j + 2] = graph[j + 2][i + 2] = 1
    for i, j in ((0, 2), (0, 3), (1, 4), (1, 5)):
        graph[i][j] = graph[j][i] = 1
    need([sum(r) for r in graph] == [2, 2] + [3] * 8, 'Incorrect core degrees')
    # Count local pages and remaining outside capacity directly by color.
    matrix = [[0] * 10 for _ in range(10)]
    for i in range(10):
        matrix[i][i] = 11 - (10 - 1 - sum(graph[i]))
        for j in range(i):
            if graph[i][j]:
                red_local = 1 + sum(graph[i][k] and graph[j][k]
                                    for k in range(10) if k not in (i, j))
                # Outside common red pages = 11-ti-tj+joint misses.
                bound = 3 - red_local - 11 + matrix[i][i] + matrix[j][j]
            else:
                blue_local = sum(not graph[i][k] and not graph[j][k]
                                 for k in range(10) if k not in (i, j))
                bound = 6 - blue_local
            matrix[i][j] = matrix[j][i] = bound
    triangles = sum(graph[i][j] and graph[i][k] and graph[j][k]
                    for i, j, k in itertools.combinations(range(10), 3))
    return graph, matrix, triangles


def image(mask, permutation):
    answer = 0
    for index, (i, j) in enumerate(EDGES):
        if mask >> index & 1:
            a, b = sorted((permutation[i], permutation[j]))
            answer |= 1 << LOOKUP[a, b]
    return answer


def generating_permutations():
    permutations = []
    for i, j in ((0, 1), (2, 3), (4, 5), (5, 6), (6, 7)):
        p = list(range(8))
        p[i], p[j] = p[j], p[i]
        permutations.append(p)
    permutations.append([2, 3, 0, 1, 4, 5, 6, 7])
    return permutations


def orbit_walk(start, moves):
    orbit = {start}
    pending = [start]
    while pending:
        current = pending.pop()
        for p in moves:
            result = image(current, p)
            if result not in orbit:
                orbit.add(result)
                pending.append(result)
    return orbit


def digest(values):
    return hashlib.sha256(''.join(str(v) + '\n' for v in sorted(values))
                          .encode('ascii')).hexdigest()


def check_certificate(certificate, raw, pair_admissible, eligible, triangle_free, records):
    need(certificate['schema'] == 2, 'Bad schema')
    need(certificate['alignment'] == {
        'low_neighbors': [[2, 3], [4, 5]],
        'cubic_labels': list(range(2, 10)),
        'mask_edges': [list(edge) for edge in EDGES]}, 'Incorrect mask convention')
    expected = {'raw_labeled_count': len(raw),
                'pair_admissible_labeled_count': len(pair_admissible),
                'eligible_labeled_count': len(eligible),
                'triangle_free_labeled_count': len(triangle_free),
                'eligible_orbit_count': len(records),
                'triangle_free_orbit_count': sum(r['triangle_free'] for r in records),
                'stabilizer_order': 192,
                'raw_masks_sha256': digest(raw),
                'pair_admissible_masks_sha256': digest(pair_admissible),
                'eligible_masks_sha256': digest(eligible),
                'triangle_free_masks_sha256': digest(triangle_free)}
    for key, value in expected.items():
        need(certificate[key] == value, 'Incorrect certificate field: ' + key)
    need(certificate['records'] == records, 'Incorrect catalogue entry or coverage')


def baseline():
    source = (HERE / 'primary21.txt').read_text()
    matrix = ast.literal_eval(source.split('\n\n', 1)[0])
    need(len(matrix) == 21 and all(len(r) == 21 for r in matrix), 'Bad baseline shape')
    need(all(matrix[i][i] == 0 for i in range(21)), 'Baseline loop')
    need(all(matrix[i][j] in (0, 1) and matrix[i][j] == matrix[j][i]
             for i in range(21) for j in range(21)), 'Bad baseline entries')
    edges = []
    maxima = []
    for color in (0, 1):
        spines = [(i, j) for i in range(21) for j in range(i + 1, 21)
                  if matrix[i][j] == color]
        page_counts = [sum(matrix[i][k] == color and matrix[j][k] == color
                           for k in range(21) if k not in (i, j)) for i, j in spines]
        edges.append(len(spines))
        maxima.append(max(page_counts))
    need(edges == [93, 117] and maxima == [3, 6], 'Primary baseline mismatch')
    need(hashlib.sha256((HERE / 'primary21.txt').read_bytes()).hexdigest()
         == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
         'Primary baseline bytes changed')


def main():
    raw = binary_census()
    pair_admissible, eligible, triangle_free = set(), set(), set()
    for mask in raw:
        graph, matrix, triangles = literal_core(mask)
        if all(x >= 0 for row in matrix for x in row):
            pair_admissible.add(mask)
            if sum(graph[2][k] and graph[3][k] for k in range(10)) != 1:
                continue
            if sum(graph[4][k] and graph[5][k] for k in range(10)) != 1:
                continue
            eligible.add(mask)
            if triangles == 0:
                triangle_free.add(mask)
    moves = generating_permutations()
    unseen = set(eligible)
    records = []
    while unseen:
        representative = min(unseen)
        orbit = orbit_walk(representative, moves)
        need(orbit <= eligible, 'An orbit leaves the binary census')
        unseen.difference_update(orbit)
        graph, _, triangles = literal_core(representative)
        records.append({'mask': representative, 'orbit_size': len(orbit),
                        'local_triangles': triangles, 'triangle_free': triangles == 0,
                        'neighbor_masks': [sum(value << i for i, value in enumerate(r))
                                           for r in graph]})
    certificate = json.loads((HERE / 'cores.json').read_text())
    check_certificate(certificate, raw, pair_admissible, eligible, triangle_free, records)
    # Missing, altered and mis-normalized data must all be rejected.
    for mutation in ('missing', 'altered', 'alignment'):
        bad = json.loads(json.dumps(certificate))
        if mutation == 'missing':
            bad['records'].pop()
        elif mutation == 'altered':
            bad['records'][0]['neighbor_masks'][0] ^= 1
        else:
            bad['alignment']['low_neighbors'][0] = [2, 4]
        rejected = False
        try:
            check_certificate(bad, raw, pair_admissible, eligible, triangle_free, records)
        except RuntimeError:
            rejected = True
        need(rejected, 'A forged catalogue was accepted')
    baseline()
    print(json.dumps({'verified': True, 'raw': len(raw),
                      'pair_admissible': len(pair_admissible), 'eligible': len(eligible),
                      'triangle_free': len(triangle_free), 'classes': len(records),
                      'triangle_free_classes': sum(r['triangle_free'] for r in records),
                      'forgery_rejections': 3, 'baseline_red_edges': 93,
                      'baseline_page_maxima': [3, 6]}, sort_keys=True))


if __name__ == '__main__':
    main()
