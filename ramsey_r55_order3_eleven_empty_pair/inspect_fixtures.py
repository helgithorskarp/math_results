#!/usr/bin/env python3
"""Definition-level checks of sharp blue-pair examples and a red-pair counterexample."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(path, core, pair_red):
    raw = path.read_bytes()
    lines = raw.decode().splitlines()
    n, m = map(int, lines[0].split())
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(n == (14 if pair_red else 13) and len(edges) == m and len(set(edges)) == m, 'dimensions')
    require(all(0 <= a < b < n for a, b in edges), 'edge domain')
    adj = [[False]*n for _ in range(n)]
    for a, b in edges:
        adj[a][b] = adj[b][a] = True
    five_count = 0
    for five in combinations(range(n), 5):
        colors = [adj[a][b] for a, b in combinations(five, 2)]
        require(any(colors) and not all(colors), 'monochromatic five-set')
        five_count += 1
    masks = []
    for v in range(9, n):
        bits = []
        for t in (0, 3, 6):
            require(adj[v][t:t+3] == [adj[v][t]]*3, 'uniformity')
            bits.append(adj[v][t])
        masks.append(sum(2**i for i in range(3) if bits[i]))
    require(masks == ([0, 0, 3, 5, 6] if pair_red else [0, 0, 3, 5]), 'signatures')
    require(adj[9][10] == pair_red, 'pair color')
    common = [v for v in range(n) if v not in (9, 10) and not adj[9][v] and not adj[10][v]]
    fixed_common = [v for v in common if v >= 9]
    require(fixed_common == list(range(11, n)), 'common blue fixed set')
    require(all(adj[a][b] for t in (0, 3, 6) for a, b in combinations(range(t, t+3), 2)), 'minority triangles')
    words = ''.join('1' if adj[3*i][3*j+t] else '0' for i, j in ((0, 1), (0, 2), (1, 2)) for t in range(3))
    require(words == {11: '100110110', 13: '110110101'}[core], 'core words')
    action = [1, 2, 0, 4, 5, 3, 7, 8, 6]+list(range(9, n))
    require(all(adj[a][b] == adj[action[a]][action[b]] for a, b in combinations(range(n), 2)), 'action')
    return dict(file=path.name, sha256=hashlib.sha256(raw).hexdigest(), vertices=n, red_edges=m,
                pair_color='red' if pair_red else 'blue', common_blue_fixed=len(fixed_common),
                signatures=masks, five_sets_checked=five_count, action_pairs_checked=n*(n-1)//2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fixtures', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = dict(verified=True, fixtures=[check(a.fixtures / 'core11.edges', 11, False),
                                         check(a.fixtures / 'core13.edges', 13, False),
                                         check(a.fixtures / 'red_pair14.edges', 11, True)])
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
