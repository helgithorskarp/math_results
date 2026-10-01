"""Exact column-product controls for the written leaf-root reduction.

This controls twelve necessary interfaces, not full host existence.
Only the ordinary proof permits every unknown X--Y edge assignment.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
KEY = 6790396772737


def require(condition, message):
    if not condition:
        raise ValueError(message)


def red_rows(key, n):
    rows = [0] * n
    for bit, (i, j) in enumerate(combinations(range(n), 2)):
        if key & (1 << bit):
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return rows


def blue_pages(rows, i, j):
    universe = (1 << len(rows)) - 1
    first = universe ^ (rows[i] | (1 << i))
    second = universe ^ (rows[j] | (1 << j))
    return (first & second).bit_count()


def main_record():
    J = red_rows(KEY, 10)
    degrees = [word.bit_count() for word in J]
    require(degrees == [3, 1, 2, 2, 3, 3, 3, 3, 3, 3], 'leaf degrees')
    require(J[1] == 1 and sum(degrees) == 26, 'leaf or edge count')
    F = [(J[i + 2] >> 2) for i in range(8)]
    margins = [4 - word.bit_count() for word in F]
    cycle = [(i, j) for i, j in combinations(range(6), 2)
             if F[i] & (1 << j)]
    require(len(cycle) == 6, 'ordinary six-cycle')
    pool = []
    assignments = 0
    choices = [tuple(sum(1 << t for t in S)
                     for S in combinations(range(3), size)) for size in margins]
    for columns in product(*choices):
        assignments += 1
        if any(sum(bool(word & (1 << t)) for word in columns) != 4
               for t in range(3)):
            continue
        if any(columns[i] & columns[j] for i, j in cycle):
            continue
        pool.append(columns)
    pool.sort()
    require(assignments == 6561 and len(pool) == 12, 'complete column cover')
    require(len(set(pool)) == 12, 'duplicate labeled pattern')
    hand = []
    for alpha, beta in product(range(3), repeat=2):
        if alpha == beta:
            continue
        gamma = 3 - alpha - beta
        for x, y in ((alpha, beta), (beta, alpha)):
            hand.append((7 ^ (1 << alpha), 7 ^ (1 << beta),
                         1 << beta, 1 << beta, 1 << alpha, 1 << alpha,
                         (1 << gamma) | (1 << x), (1 << gamma) | (1 << y)))
    require(pool == sorted(hand), 'hand classification differs entrywise')

    def frame(left, right):
        # Roots0,1, mark2, X3..10, Y11..18, T19..21.
        rows = [0] * 22
        def add(i, j):
            rows[i] |= 1 << j
            rows[j] |= 1 << i
        for i, j in ((0, 1), (0, 2), (1, 2)):
            add(i, j)
        for root, start, pattern in ((0, 3, left), (1, 11, right)):
            for i in range(8):
                add(root, start + i)
                if i >= 6:
                    add(2, start + i)
                for j in range(i + 1, 8):
                    if F[i] & (1 << j):
                        add(start + i, start + j)
                for t in range(3):
                    if pattern[i] & (1 << t):
                        add(start + i, 19 + t)
        for t in range(3):
            add(2, 19 + t)
        require([rows[i].bit_count() for i in (0, 1, 2, 19, 20, 21)]
                == [10, 10, 9, 9, 9, 9], 'fixed endpoint degree equations')
        return rows

    bad = Counter()
    unknown = tuple(product(range(3, 11), range(11, 19)))
    individual_controls = complete_controls = 0
    for left, right in product(pool, repeat=2):
        shared = [left[6] & left[7], right[6] & right[7]]
        require(all(word.bit_count() == 1 for word in shared), 'unique centers')
        c, d = (word.bit_length() - 1 for word in shared)
        red = c == d
        i, j = (2, 19 + c) if red else (19 + c, 19 + d)
        target = 4 if red else 7
        rows = frame(left, right)
        def page_count():
            require(bool(rows[i] & (1 << j)) == red, 'spine color')
            return (rows[i] & rows[j]).bit_count() if red else blue_pages(rows, i, j)
        require(page_count() == target, 'literal fixed-spine contradiction')
        for a, b in unknown:
            require(i not in (a, b) and j not in (a, b), 'unknown endpoint edge')
            rows[a] |= 1 << b; rows[b] |= 1 << a
            require(page_count() == target, 'individual cross-edge invariance')
            rows[a] ^= 1 << b; rows[b] ^= 1 << a
            individual_controls += 1
        for a, b in unknown:
            rows[a] |= 1 << b; rows[b] |= 1 << a
        require(page_count() == target, 'complete red cross-block invariance')
        complete_controls += 1
        bad['red_mark_center_four_pages' if red
            else 'blue_distinct_centers_seven_pages'] += 1

    # Root0, mark1, leaves2,3, seven other local points4..10.
    prefix = [0] * 11
    for j in range(1, 11):
        prefix[0] |= 1 << j; prefix[j] |= 1
    for leaf in (2, 3):
        prefix[leaf] |= 1 << 1; prefix[1] |= 1 << leaf
    forced = blue_pages(prefix, 2, 3)
    require(forced == 7, 'injectivity seven-page prefix')

    payload = (HERE / 'primary21.blue').read_bytes()
    blue = payload.decode().splitlines()
    require(len(blue) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'}
                                   for row in blue), 'primary fixture shape')
    require(all(blue[i][i] == '0' for i in range(21)), 'primary diagonal')
    require(all(blue[i][j] == blue[j][i] for i in range(21) for j in range(21)),
            'primary symmetry')
    rows = [sum(1 << j for j in range(21) if j != i and blue[i][j] == '0')
            for i in range(21)]
    rpages = []; bpages = []
    for i, j in combinations(range(21), 2):
        if rows[i] & (1 << j):
            rpages.append((rows[i] & rows[j]).bit_count())
        else:
            bpages.append(blue_pages(rows, i, j))
    require((len(rpages), max(rpages), max(bpages)) == (93, 3, 6), 'primary baseline')
    return {
        'leaf_key': KEY, 'local_degrees': degrees,
        'column_domain_size': 6561, 'row_pair_domain_size': 4900,
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


if __name__ == '__main__':
    actual = main_record()
    expected = json.loads((HERE / 'expected.json').read_text())
    require(json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True),
            'complete expected mathematical record differs')
    print(json.dumps(actual, indent=2, sort_keys=True))
