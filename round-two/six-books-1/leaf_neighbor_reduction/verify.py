"""Independent row-pair and literal-color check of the leaf interfaces.

No producer module is imported. Completeness comes from two arbitrary
four-subsets and the uniquely determined third row, not a hash alone.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import hashlib
import json

HERE = Path(__file__).resolve().parent
F_EDGES = ((0, 4), (0, 5), (1, 2), (1, 3), (2, 5),
           (2, 7), (3, 4), (3, 6), (4, 7), (5, 6))
MARGINS = (2, 2, 1, 1, 1, 1, 2, 2)
CYCLE = tuple((i, j) for i, j in F_EDGES if i < 6 and j < 6)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pages(matrix, i, j):
    color = matrix[i][j]
    return sum(matrix[i][k] == color and matrix[j][k] == color
               for k in range(len(matrix)) if k not in (i, j))


def independent_record():
    # Reconstruct original literal ten-point graph, separate from key decoding.
    neighbors = ((1, 8, 9), (0,), (6, 7), (4, 5), (3, 7, 9),
                 (3, 6, 8), (2, 5, 9), (2, 4, 8), (0, 5, 7), (0, 4, 6))
    key = sum(2 ** b for b, (i, j) in enumerate(combinations(range(10), 2))
              if j in neighbors[i])
    require(all((j in neighbors[i]) == (i in neighbors[j])
                for i in range(10) for j in range(10)), 'literal leaf symmetry')
    require(tuple((i, j) for i, j in combinations(range(8), 2)
                  if j + 2 in neighbors[i + 2]) == F_EDGES, 'literal induced block')
    degrees = [len(neighbors[i]) for i in range(10)]
    require([4 - sum(i in edge for edge in F_EDGES) for i in range(8)]
            == list(MARGINS), 'column margins from literal degree equations')

    rows = tuple(frozenset(x) for x in combinations(range(8), 4))
    pool = []
    checked = 0
    for first, second in product(rows, repeat=2):
        checked += 1
        remainder = [MARGINS[i] - int(i in first) - int(i in second)
                     for i in range(8)]
        if any(r not in (0, 1) for r in remainder):
            continue
        third = frozenset(i for i, r in enumerate(remainder) if r)
        if len(third) != 4:
            continue
        triplet = (first, second, third)
        if any(any(i in S and j in S for S in triplet) for i, j in CYCLE):
            continue
        pool.append(tuple(sum(2 ** t for t in range(3) if i in triplet[t])
                          for i in range(8)))
    pool.sort()
    require(checked == 4900 and len(pool) == len(set(pool)) == 12,
            'complete row-pair domain or injectivity')
    hand = []
    for alpha in range(3):
        for beta in range(3):
            if alpha == beta:
                continue
            gamma = next(t for t in range(3) if t not in (alpha, beta))
            for q, r in ((alpha, beta), (beta, alpha)):
                hand.append((7 - 2 ** alpha, 7 - 2 ** beta,
                             2 ** beta, 2 ** beta, 2 ** alpha, 2 ** alpha,
                             2 ** gamma + 2 ** q, 2 ** gamma + 2 ** r))
    require(pool == sorted(hand), 'hand patterns differ entrywise')

    def partial_graph(left, right):
        # Mark0, T1..3, roots4,5, X6..13, Y14..21.
        matrix = [[False] * 22 for _ in range(22)]
        def edge(i, j):
            matrix[i][j] = matrix[j][i] = True
        for i, j in ((0, 4), (0, 5), (4, 5)):
            edge(i, j)
        for root, start, pattern in ((4, 6, left), (5, 14, right)):
            for i in range(8):
                edge(root, start + i)
            edge(0, start + 6); edge(0, start + 7)
            for i, j in F_EDGES:
                edge(start + i, start + j)
            for t in range(3):
                edge(0, 1 + t)
                for i, mask in enumerate(pattern):
                    if mask & 2 ** t:
                        edge(1 + t, start + i)
        require([sum(matrix[i]) for i in range(6)] == [9, 9, 9, 9, 10, 10],
                'fixed endpoint degree equations')
        return matrix

    bad = Counter()
    unknown = tuple(product(range(6, 14), range(14, 22)))
    individual_controls = complete_controls = 0
    for left, right in product(pool, repeat=2):
        centers = []
        for pattern in (left, right):
            choices = [t for t in range(3) if pattern[6] & pattern[7] & 2 ** t]
            require(len(choices) == 1, 'center not unique')
            centers.append(choices[0])
        first, second = centers
        red = first == second
        i, j = (0, first + 1) if red else (first + 1, second + 1)
        expected = 4 if red else 7
        matrix = partial_graph(left, right)
        require(matrix[i][j] == red and pages(matrix, i, j) == expected,
                'literal fixed-spine contradiction')
        for a, b in unknown:
            require(i not in (a, b) and j not in (a, b), 'unknown endpoint edge')
            matrix[a][b] = matrix[b][a] = True
            require(pages(matrix, i, j) == expected, 'single cross-edge invariance')
            matrix[a][b] = matrix[b][a] = False
            individual_controls += 1
        for a, b in unknown:
            matrix[a][b] = matrix[b][a] = True
        require(pages(matrix, i, j) == expected, 'complete cross-block invariance')
        complete_controls += 1
        bad['red_mark_center_four_pages' if red
            else 'blue_distinct_centers_seven_pages'] += 1

    prefix = [[False] * 11 for _ in range(11)]
    for j in range(1, 11):
        prefix[0][j] = prefix[j][0] = True
    for leaf in (2, 3):
        prefix[1][leaf] = prefix[leaf][1] = True
    forced = pages(prefix, 2, 3)
    require(forced == 7, 'injectivity forced pages')

    payload = (HERE / 'primary21.blue').read_bytes()
    lines = payload.decode().splitlines()
    require(len(lines) == 21 and all(len(s) == 21 and set(s) <= {'0', '1'}
                                    for s in lines), 'primary fixture shape')
    require(all(lines[i][i] == '0' for i in range(21)), 'primary diagonal')
    matrix = [[i != j and lines[i][j] == '0' for j in range(21)] for i in range(21)]
    require(all(matrix[i][j] == matrix[j][i] for i in range(21) for j in range(21)),
            'primary symmetry')
    rpages = []; bpages = []
    for i, j in combinations(range(21), 2):
        (rpages if matrix[i][j] else bpages).append(pages(matrix, i, j))
    require((len(rpages), max(rpages), max(bpages)) == (93, 3, 6), 'primary baseline')
    return {
        'leaf_key': key, 'local_degrees': degrees,
        'column_domain_size': 3 ** 8, 'row_pair_domain_size': checked,
        'interfaces_per_block': len(pool), 'profiles': pool,
        'interface_sha256': hashlib.sha256(json.dumps(pool, separators=(',', ':')).encode()).hexdigest(),
        'complete_interface_pairs': 144, 'violations': dict(bad),
        'individual_cross_edge_controls': individual_controls,
        'all_cross_edges_red_controls': complete_controls,
        'spine_endpoints_disjoint_from_all_unknown_edges': True,
        'injectivity_forced_blue_pages': forced,
        'prior21': {'vertices': 21, 'red_edges': len(rpages), 'blue_edges': len(bpages),
                    'maximum_red_pages': max(rpages), 'maximum_blue_pages': max(bpages),
                    'fixture_sha256': hashlib.sha256(payload).hexdigest()},
    }


def validate_record(supplied, actual):
    require(json.dumps(supplied, sort_keys=True) == json.dumps(actual, sort_keys=True),
            'complete expected mathematical record differs')


def self_test(expected, actual):
    mutations = []
    def add(name, change):
        damaged = copy.deepcopy(expected)
        change(damaged)
        mutations.append((name, damaged))
    add('omitted interface', lambda d: d['profiles'].pop())
    add('duplicate interface', lambda d: d['profiles'].__setitem__(0, d['profiles'][1]))
    add('changed actual incidence', lambda d: d['profiles'][0].__setitem__(0, 1))
    add('wrong leaf key', lambda d: d.__setitem__('leaf_key', d['leaf_key'] + 1))
    add('erased blue-spine cases', lambda d: d['violations'].__setitem__('blue_distinct_centers_seven_pages', 0))
    add('lost unknown-edge controls', lambda d: d.__setitem__('individual_cross_edge_controls', 9215))
    add('boolean numeric incidence', lambda d: d['profiles'][0].__setitem__(2, True))
    add('wrong injectivity pages', lambda d: d.__setitem__('injectivity_forced_blue_pages', 6))
    rejected = []
    for name, damaged in mutations:
        try:
            validate_record(damaged, actual)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged record accepted: ' + name)
    return {'damages_rejected': len(rejected), 'damage_names': rejected}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    actual = independent_record()
    expected = json.loads((HERE / 'expected.json').read_text())
    validate_record(expected, actual)
    print(json.dumps(self_test(expected, actual) if args.self_test else actual,
                     indent=2, sort_keys=True))
