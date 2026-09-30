"""Exact degree11 scalar reduction and normalized cubic10 candidate census.

Author: six-books-3, researcher. Python 3.11+, standard library only.
This produces necessary local candidates, not order22 Ramsey witnesses.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
PAIRS = list(combinations(range(10), 2))
INDEX = {edge: i for i, edge in enumerate(PAIRS)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalized_cubics(n):
    """All simple cubic H on n labels with N_H(0)={1,2,3}."""
    require(4 <= n <= 10 and n % 2 == 0, 'unsupported control order')
    pairs = list(combinations(range(n), 2))
    index = {edge: i for i, edge in enumerate(pairs)}
    degrees = [3] * n
    mask = 0
    for j in (1, 2, 3):
        mask |= 1 << index[(0, j)]
        degrees[0] -= 1
        degrees[j] -= 1

    def visit(i, current):
        if i == n:
            require(not any(degrees), 'nonzero terminal degrees')
            yield current
            return
        choices = [j for j in range(i + 1, n) if degrees[j]]
        need = degrees[i]
        if len(choices) < need:
            return
        for selected in combinations(choices, need):
            degrees[i] = 0
            next_mask = current
            for j in selected:
                degrees[j] -= 1
                next_mask |= 1 << index[(i, j)]
            positive = sum(x > 0 for x in degrees[i + 1:])
            # Every positive remaining degree needs that many other
            # positive vertices. This necessary condition is only pruning.
            if all(x <= positive - 1 for x in degrees[i + 1:] if x):
                yield from visit(i + 1, next_mask)
            for j in selected:
                degrees[j] += 1
            degrees[i] = need

    yield from visit(1, mask)


def edge_orbits(domain):
    """Exact actions fixing 0,1 and the set {2,3}; no graph catalogue."""
    actions = []
    for low in ((2, 3), (3, 2)):
        for high in permutations(range(4, 10)):
            point_map = (0, 1) + low + high
            require(sorted(point_map) == list(range(10)), 'not a point permutation')
            actions.append([1 << INDEX[tuple(sorted((point_map[a], point_map[b])))]
                            for a, b in PAIRS])
    require(len(actions) == 1440, 'wrong group size')
    remaining = set(domain)
    records = []
    while remaining:
        representative = min(remaining)
        edges = [i for i in range(45) if representative >> i & 1]
        orbit = {sum(action[i] for i in edges) for action in actions}
        require(orbit <= remaining, 'orbits overlap or leave normalized domain')
        remaining.difference_update(orbit)
        records.append({'mask': representative, 'orbit_size': len(orbit)})
    return records


def histogram_reduction():
    records = []
    for n1 in (0, 1):
        for n2 in (1, 3, 5, 7):
            n3 = 11 - n1 - n2
            old_d = (21 - 8 * n1 - n2) // 2
            minimum = 2 * (n1 + n2)
            residual = old_d - minimum
            records.append({'n1': n1, 'n2': n2, 'n3': n3,
                            'old_budget_D': old_d,
                            'mandatory_column_cost': minimum,
                            'residual_E': residual, 'allowed': residual >= 0})
    require([(x['n1'], x['n2']) for x in records if x['allowed']]
            == [(0, 1), (0, 3), (1, 1)], 'incorrect scalar reduction')
    return records


def baseline():
    rows = (HERE / 'baseline21.rows').read_text().splitlines()
    require(len(rows) == 21 and all(len(row) == 21 for row in rows), 'bad baseline shape')
    red = [{j for j, value in enumerate(row) if value == '1'} for row in rows]
    require(all(set(row) <= {'0', '1'} for row in rows), 'bad baseline character')
    require(all(i not in red[i] and all((j in red[i]) == (i in red[j])
                for j in range(21)) for i in range(21)), 'bad baseline graph')
    full = set(range(21))
    caps = [0, 0]
    for i, j in combinations(range(21), 2):
        if j in red[i]:
            caps[0] = max(caps[0], len(red[i] & red[j]))
        else:
            caps[1] = max(caps[1], len((full - red[i] - {i}) & (full - red[j] - {j})))
    result = {'red_edges': sum(map(len, red)) // 2,
              'red_degree_histogram': {str(d): count for d, count in
                                      sorted(Counter(map(len, red)).items())},
              'red_spine_max': caps[0], 'blue_spine_max': caps[1]}
    require(result['red_edges'] == 93 and caps == [3, 6], 'baseline did not reproduce')
    return result


def generate():
    raw = list(normalized_cubics(10))
    require(len(set(raw)) == len(raw), 'repeated labeled cubic graph')
    for mask in raw:
        for i in range(10):
            require(sum(bool(mask >> INDEX[tuple(sorted((i, j)))] & 1)
                        for j in range(10) if j != i) == 3, 'bad cubic degree')
    domain = sorted(raw)
    records = edge_orbits(domain)
    controls = {n: len(list(normalized_cubics(n))) for n in (4, 6, 8)}
    require(controls == {4: 1, 6: 7, 8: 553}, 'small census controls failed')
    return {'schema': 'degree11-leaf-candidates-v1',
            'scope': 'necessary local candidates; no full-host existence or exclusion',
            'histograms': histogram_reduction(), 'baseline': baseline(),
            'small_normalized_cubic_counts': {str(n): count for n, count in controls.items()},
            'normalized_labeled_count': len(domain), 'group_size': 1440,
            'oriented_edge_orbits': len(records),
            'domain_sha256': hashlib.sha256(
                ''.join(str(x) + '\n' for x in domain).encode()).hexdigest(),
            'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = generate()
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.write_expected:
        (HERE / 'expected.json').write_text(serialized)
    else:
        require(result == json.loads((HERE / 'expected.json').read_text()),
                'expected output mismatch')
    print(serialized, end='')


if __name__ == '__main__':
    main()
