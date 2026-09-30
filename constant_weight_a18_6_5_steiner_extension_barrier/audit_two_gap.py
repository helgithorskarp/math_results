"""Direct set compatibility and expanded positive two-outsider controls."""
from itertools import combinations
import json

from geometry import classical_design, points, require
from generate_two_gap import enumerate_masks, graph_masks


def direct_pair(left, right):
    b, qs = left
    c, rs = right
    return (len(set(points(b)) & set(points(c))) <= 2 and
            all(q == r or len(set(points(q)) & set(points(r))) <= 1
                for q in qs for r in rs))


def expanded_pair(circles, gaps, chosen):
    outsiders = {b for b, qs in chosen}
    qs = {q for b, old_parts in chosen for q in old_parts}
    removed = set(gaps) | {c for c in circles if any(
        len(set(points(c)) & set(points(b))) >= 3 for b in outsiders)}
    words = (set(circles) - removed) | outsiders | {q | (1 << 17) for q in qs}
    require(len(outsiders) == 2 and len(words) == 68, 'incorrect positive control size')
    require(len(removed) - len(qs) == 2, 'incorrect positive control gap count')
    sets = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(all(len(w) == 5 for w in sets), 'incorrect positive control weight')
    require(all(len(u & v) <= 2 for u, v in combinations(sets, 2)),
            'positive control is not a packing')
    return len(words)


def main():
    circles, gap = classical_design()
    results = []
    for intersection, second in ((0, 1828), (1, 5169), (2, 362)):
        gaps = {gap, second}
        records, _ = enumerate_masks(circles, gaps)
        adjacency, _ = graph_masks(records)
        shared_edge = None
        for i, row in enumerate(adjacency):
            later = row & ~((1 << (i + 1)) - 1)
            while later:
                bit = later & -later
                j = bit.bit_length() - 1
                if set(records[i][1]) & set(records[j][1]):
                    shared_edge = (i, j)
                    break
                later ^= bit
            if shared_edge is not None:
                break
        require(shared_edge is not None, 'missing equal-four-set positive control')
        selected = sorted({i * (len(records) - 1) // 31 for i in range(32)} | set(shared_edge))
        comparisons = 0
        for i, j in combinations(selected, 2):
            require(bool(adjacency[i] >> j & 1) == direct_pair(records[i], records[j]),
                    'direct set compatibility mismatch')
            comparisons += 1
        size = expanded_pair(circles, gaps, [records[i] for i in shared_edge])
        results.append({'gap_intersection': intersection, 'direct_pair_cases': comparisons,
                        'equal_four_sets_allowed': True, 'positive_packing_size': size})
    print(json.dumps({'controls': results}, sort_keys=True))


if __name__ == '__main__':
    main()
