#!/usr/bin/env python3
"""Known positive primary fixture and actual degree-preserving negative controls."""
from itertools import combinations
from pathlib import Path
import json
import audit

HERE = Path(__file__).resolve().parent


def run():
    raw = json.loads((HERE / 'primary21.json').read_text())
    red = [{j for j in range(21) if i != j and raw[i][j] == 0} for i in range(21)]
    a = sorted(red[0])
    b = sorted(set(range(21)) - red[0] - {0})
    audit.need(len(a) == len(b) == 10, 'primary rooted ten/ten partition')
    local_red = [sum(1 << j for j, y in enumerate(a) if y in red[x]) for x in a]
    words = [sum(1 << i for i, x in enumerate(a) if x not in red[y]) for y in b]
    actual = [sum(1 << j for j, y in enumerate(b) if y in red[x]) for x in b]
    targets = [x.bit_count() for x in actual]
    domains = [audit.literal_stars(words, [0] * 10, i, local_red, targets) for i in range(10)]
    audit.need(all(actual[i] in domains[i] for i in range(10)), 'all ten genuine positive outside stars')
    answer, nodes = audit.edge_completion(words, [[s] for s in actual])
    audit.need(answer == 1, 'actual known21 completion accepted by all pair tests')
    graph = {(i, j) for i, j in combinations(range(10), 2) if actual[i] >> j & 1}
    damages = set()
    for first, second in combinations(sorted(graph), 2):
        i, j = first
        k, l = second
        if len({i, j, k, l}) != 4:
            continue
        for new in (((i, k), (j, l)), ((i, l), (j, k))):
            fresh = {tuple(sorted(x)) for x in new}
            if not fresh & graph:
                damages.add(tuple(sorted((graph - {first, second}) | fresh)))
    rejected = 0
    for edge_set in sorted(damages):
        star = [sum(1 << (y if x == i else x) for x, y in edge_set if i in (x, y)) for i in range(10)]
        audit.need([x.bit_count() for x in star] == targets, 'actual two-switch preserves all outside degrees')
        if any(star[i] not in domains[i] for i in range(10)) or any(
                not audit.pair_stars(words, i, star[i], j, star[j]) for i, j in combinations(range(10), 2)):
            rejected += 1
    audit.need(rejected == len(damages) > 0, 'all actual asymmetric two-switch damages rejected')
    # Exercise the fallback on a four-variable problem with three completions.
    triples = [(0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5)]
    four_words = [1023 ^ sum(1 << i for i in row) for row in triples]
    four_domains = [[1 << j for j in range(4) if j != i] for i in range(4)]
    count, branch_nodes = audit.edge_completion(four_words, four_domains)
    brute = 0
    pairs = list(combinations(range(4), 2))
    for word in range(64):
        outside = [set() for _ in range(4)]
        for bit, (i, j) in enumerate(pairs):
            if word >> bit & 1:
                outside[i].add(j)
                outside[j].add(i)
        if not all(len(xs) == 1 for xs in outside):
            continue
        red_a = [set(row) for row in triples]
        blue_a = [set(range(10)) - xs for xs in red_a]
        for i, j in pairs:
            if j in outside[i]:
                pages = len(red_a[i] & red_a[j]) + len(outside[i] & outside[j])
                cap = 3
            else:
                blue_i = set(range(4)) - {i} - outside[i]
                blue_j = set(range(4)) - {j} - outside[j]
                pages = 1 + len(blue_a[i] & blue_a[j]) + len(blue_i & blue_j)
                cap = 6
            if pages > cap:
                break
        else:
            brute += 1
    audit.need(count == brute == 3 and branch_nodes > 1,
               'complete edge-branch fallback matches all64 literal four-point words')
    return {'actual_reviewer': 'six-reviewer-4', 'positive21_star_domains': 10,
            'positive21_completion': 1, 'positive21_arc_nodes': nodes,
            'distinct_degree_preserving_B_switches': len(damages), 'damaged_completions_rejected': rejected,
            'edge_branch_literal_words': 64, 'edge_branch_completions': count,
            'edge_branch_search_nodes': branch_nodes}


if __name__ == '__main__':
    result = run()
    import sys
    if sys.argv[1:] != ['--emit']:
        audit.need(not sys.argv[1:], 'usage: controls.py [--emit]')
        audit.need(result == json.loads((HERE / 'controls-expected.json').read_text()), 'full control expected record')
    print(json.dumps(result, sort_keys=True, indent=2))
