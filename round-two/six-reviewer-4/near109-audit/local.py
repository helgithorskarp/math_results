#!/usr/bin/env python3
"""Definition-level checks of an ordinary five-column identity, not a host census."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(adj, a, b):
    adj[a].add(b)
    adj[b].add(a)


def page(adj, a, b):
    if b in adj[a]:
        return len(adj[a] & adj[b])
    return len(set(range(len(adj))) - {a, b} - adj[a] - adj[b])


def identity(adj, root=0, centers=(1, 2), leaves=(3, 4, 5)):
    n = len(adj)
    need(all(i not in xs and all(i in adj[j] for j in xs) for i, xs in enumerate(adj)),
         'simple undirected graph')
    a, b = centers
    chosen = tuple(centers) + tuple(leaves)
    jset = adj[root]
    r = len(jset)
    outside = set(range(n)) - jset - {root}
    need(len(set(chosen)) == 5 and set(chosen) <= jset, 'five actual root neighbors')
    need(b not in adj[a] and all(y not in adj[x] for x, y in combinations(leaves, 2)),
         'induced K2,3 blue spines')
    need(all(y in adj[x] for x in centers for y in leaves), 'six K2,3 red spines')
    h = {x: len(adj[x] & jset) for x in chosen}
    need(h[a] == h[b] == 3 and all(2 <= h[x] <= 3 for x in leaves),
         'root red-page local degree hypotheses')
    t = sum(h[x] for x in leaves)
    cols = {x: outside - adj[x] for x in chosen}
    row_gap = sum((q := sum(y in cols[x] for x in chosen)) * (q - 1) // 2 - 2 * q + 3
                  for y in outside)
    extra_local = sum(len(adj[x] & adj[y] & jset) - 2 for x, y in combinations(leaves, 2))
    common_outside_centers = len(adj[a] & adj[b] & outside)
    red_slack = sum(3 - page(adj, x, y) for x in centers for y in leaves)
    center_slack = 6 - page(adj, a, b)
    leaf_slack = sum(6 - page(adj, x, y) for x, y in combinations(leaves, 2))
    lhs = (red_slack + 2 * center_slack + leaf_slack + row_gap + extra_local
           + common_outside_centers + 2 * (9 - t))
    rhs = 72 - 2 * n - 3 * r
    need(row_gap >= 0 and extra_local >= 0 and common_outside_centers >= 0 and t <= 9,
         'every non-page remainder is nonnegative')
    need(lhs == rhs, 'literal weighted page/cell identity')
    return (n, r, red_slack, center_slack, leaf_slack, row_gap,
            extra_local, common_outside_centers, t, rhs)


def sample(n, r, seed):
    adj = [set() for _ in range(n)]
    for i in range(1, r + 1):
        add(adj, 0, i)
    for a in (1, 2):
        for b in (3, 4, 5):
            add(adj, a, b)
    state = seed + 1

    def bit():
        nonlocal state
        state = (1664525 * state + 1013904223) % (1 << 32)
        return state >> 16

    extras = list(range(6, r + 1))
    if extras:
        for leaf in (3, 4, 5):
            pick = bit() % (len(extras) + 1)
            if pick < len(extras):
                add(adj, leaf, extras[pick])
        for x, y in combinations(extras, 2):
            if bit() % 2 and len(adj[x] - {0}) < 3 and len(adj[y] - {0}) < 3:
                add(adj, x, y)
    for x in range(1, r + 1):
        for y in range(r + 1, n):
            if bit() % 3 == 0:
                add(adj, x, y)
    for x, y in combinations(range(r + 1, n), 2):
        if bit() % 5 < 2:
            add(adj, x, y)
    return adj


def run():
    records = []
    for n, r in ((6, 5), (16, 9), (21, 10), (22, 9), (22, 10)):
        for seed in range(64):
            records.append(identity(sample(n, r, seed)))
    pos = sample(6, 5, 0)
    need(all(page(pos, a, b) <= (3 if b in pos[a] else 6)
             for a, b in combinations(range(6), 2)), 'genuine positive small valid graph')
    n22 = [x for x in records if x[:2] == (22, 10)]
    need(all(x[2] < 0 or x[3] < 0 or x[4] < 0 for x in n22),
         'a selected physical spine violates its cap in every degree-ten22 control')
    negative = 0
    for kind in ('center-extra', 'leaf-edge', 'nonsymmetric'):
        damaged = sample(22, 10, 0)
        if kind == 'center-extra':
            add(damaged, 1, 6)
        elif kind == 'leaf-edge':
            add(damaged, 3, 4)
        else:
            damaged[1].discard(3)
        try:
            identity(damaged)
        except ValueError:
            negative += 1
        else:
            raise ValueError('bad local geometry accepted: ' + kind)
    primary = json.loads((HERE / 'primary21.json').read_text())
    need(len(primary) == 21 and all(len(row) == 21 for row in primary), 'complete primary matrix')
    need(all(primary[i][j] in (0, 1) and primary[i][j] == primary[j][i]
             for i in range(21) for j in range(21)), 'primary binary symmetric entries')
    # The primary file uses the opposite color. Red is its off-diagonal complement.
    red = [{j for j in range(21) if i != j and primary[i][j] == 0} for i in range(21)]
    red_max = max(page(red, a, b) for a, b in combinations(range(21), 2) if b in red[a])
    blue_max = max(page(red, a, b) for a, b in combinations(range(21), 2) if b not in red[a])
    need((sum(map(len, red)) // 2, red_max, blue_max) == (93, 3, 6), 'known primary21 valid fixture')
    return {'actual_reviewer': 'six-reviewer-4', 'synthetic_identity_controls': len(records),
            'physical_selected_pair_counts': 10 * len(records),
            'degree_ten22_falsification_controls': len(n22),
            'positive_valid_six_point_control': 1, 'negative_geometry_controls': negative,
            'identity_trace_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
            'primary21': {'edges': 93, 'red_page_max': red_max, 'blue_page_max': blue_max},
            'infinite_claim_proof': 'ordinary double counting in REVIEW.md; controls are not an enumeration'}


if __name__ == '__main__':
    result = run()
    if sys.argv[1:] != ['--emit']:
        need(not sys.argv[1:], 'usage: local.py [--emit]')
        need(result == json.loads((HERE / 'local-expected.json').read_text()), 'complete local expected record')
    print(json.dumps(result, indent=2, sort_keys=True))
