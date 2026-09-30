"""Separate binary-edge traversal, literal core checks and capacity audits.

Author: six-books-3, researcher. Imports no research generator or predecessor
checker. Explicit checks remain enabled under Python optimization.
"""
from itertools import combinations, permutations
from pathlib import Path
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def binary_census(n):
    require(n in (4, 6, 8, 10), 'unsupported order')
    pairs = list(combinations(range(n), 2))
    free = [(i, a, b) for i, (a, b) in enumerate(pairs) if a]
    used = [3, 1, 1, 1] + [0] * (n - 4)
    left = [0] + [n - 2] * (n - 1)
    initial = sum(1 << i for i, edge in enumerate(pairs)
                  if edge in ((0, 1), (0, 2), (0, 3)))
    answers = []
    nodes = 0

    def dfs(k, mask):
        nonlocal nodes
        nodes += 1
        if k == len(free):
            require(used == [3] * n, 'bad terminal degrees')
            answers.append(mask)
            return
        bit, a, b = free[k]
        left[a] -= 1
        left[b] -= 1
        # Visit the absent edge and then the present edge. The degree
        # bounds are literal availability bounds, not graphical heuristics.
        if used[a] + left[a] >= 3 and used[b] + left[b] >= 3:
            dfs(k + 1, mask)
        if used[a] < 3 and used[b] < 3:
            used[a] += 1
            used[b] += 1
            if used[a] + left[a] >= 3 and used[b] + left[b] >= 3:
                dfs(k + 1, mask | (1 << bit))
            used[a] -= 1
            used[b] -= 1
        left[a] += 1
        left[b] += 1

    dfs(0, initial)
    require(len(set(answers)) == len(answers), 'repeated binary terminal')
    return sorted(answers), nodes


def local_graph(mask):
    require(isinstance(mask, int) and 0 <= mask < (1 << 45), 'bad graph mask')
    adjacency = [set() for _ in range(12)]
    for i, (a, b) in enumerate(combinations(range(10), 2)):
        if mask >> i & 1:
            adjacency[a].add(b)
            adjacency[b].add(a)
    require(all(len(adjacency[i]) == 3 for i in range(10)), 'representative not cubic')
    require(adjacency[0] == {1, 2, 3}, 'bad normalization')
    adjacency[0].remove(1)
    adjacency[1].remove(0)
    adjacency[0].add(10)
    adjacency[10].add(0)
    for i in range(11):
        adjacency[i].add(11)
        adjacency[11].add(i)
    require([len(adjacency[i] - {11}) for i in range(11)]
            == [3, 2] + [3] * 8 + [1], 'bad leaf reconstruction')
    full = set(range(12))
    for i, j in combinations(range(12), 2):
        if j in adjacency[i]:
            require(len(adjacency[i] & adjacency[j]) <= 3, 'red book in local core')
        else:
            require(len((full - adjacency[i] - {i}) &
                        (full - adjacency[j] - {j})) <= 6, 'blue book in local core')
    return adjacency


def audit_literal_identity(core, seed):
    """Audit E by literal pages in arbitrary full graphs, including invalid ones.

    These deterministic algebra controls are not witness searches. U and
    global-degree deficits may be negative on these invalid controls.
    """
    red = [set(row) for row in core] + [set() for _ in range(10)]
    state = seed

    def draw():
        nonlocal state
        state = (1103515245 * state + 12345) % (1 << 31)
        return state

    for b in range(12, 22):
        z_mask = draw() % 2048
        for a in range(11):
            if not (z_mask >> a & 1):
                red[b].add(a)
                red[a].add(b)
    for b, c in combinations(range(12, 22), 2):
        if draw() % 2:
            red[b].add(c)
            red[c].add(b)
    full = set(range(22))
    unused = 0
    spine_slack = [[0] * 11 for _ in range(11)]
    for a, b in combinations(range(11), 2):
        if b in red[a]:
            slack = 3 - len(red[a] & red[b])
        else:
            slack = 6 - len((full - red[a] - {a}) & (full - red[b] - {b}))
        unused += slack
        spine_slack[a][b] = spine_slack[b][a] = slack
    local_degree = [len(core[a] - {11}) for a in range(11)]
    z_sets = [set(range(11)) - red[b] for b in range(12, 22)]
    t = [sum(a in z for z in z_sets) for a in range(11)]
    for a, b in combinations(range(11), 2):
        joint = sum(a in z and b in z for z in z_sets)
        local_common = len((core[a] & core[b]) - {11})
        base = (t[a] + t[b] - 8 if b in core[a]
                else local_degree[a] + local_degree[b] - 3)
        require(joint == base - local_common - spine_slack[a][b],
                'literal mixed-spine identity failed')
    for a in range(11):
        h = local_degree[a]
        pt = sum(t[b] for b in core[a] if b != 11)
        ph = sum(local_degree[b] for b in core[a] if b != 11)
        correction = sum(len(z) - 4 for z in z_sets if a in z)
        require((3 - h) * t[a] - pt ==
                5 * h - h * h - 2 * ph - sum(spine_slack[a]) - correction,
                'literal row-sum identity failed')
    phi = 0
    for b in range(12, 22):
        z = 11 - len(red[b] & set(range(11)))
        phi += (z - 3) * (z - 4) // 2
    degree_deficit = sum((3 - local_degree[a]) * (11 - len(red[a]))
                         for a in range(11))
    require(unused + phi + degree_deficit == 2, 'literal residual identity failed')
    for a in range(11):
        misses = sum(a not in red[b] for b in range(12, 22))
        require(misses - local_degree[a] == 11 - len(red[a]), 'column-degree bridge failed')


def audit_scalars(document):
    records = []
    for n1 in (0, 1):
        for n2 in (1, 3, 5, 7):
            h = [1] * n1 + [2] * n2 + [3] * (11 - n1 - n2)
            # Independently use the degree11 scalar formula, rather than
            # the simplified histogram coefficients in the generator.
            twice_d = 21 - sum(3 * (3 - x) ** 2 - 2 * (3 - x) for x in h)
            require(twice_d % 2 == 0, 'bad scalar parity')
            d = twice_d // 2
            mandatory = sum((3 - x) * x for x in h)
            records.append({'n1': n1, 'n2': n2, 'n3': 11 - n1 - n2,
                            'old_budget_D': d, 'mandatory_column_cost': mandatory,
                            'residual_E': d - mandatory, 'allowed': mandatory <= d})
    require(records == document['histograms'], 'histogram records differ')
    # All possible integer sizes; phi zero exactly at sizes3 and4.
    require([z for z in range(12) if (z - 3) * (z - 4) // 2 == 0] == [3, 4],
            'phi zero sizes differ')
    require(all((z - 3) * (z - 4) // 2 > 2 for z in range(6, 12)),
            'large-size budget bound failed')


def audit_baseline(document):
    rows = (HERE / 'baseline21.rows').read_text().splitlines()
    require(len(rows) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'}
                                  for row in rows), 'malformed baseline')
    red = [sum((value == '1') << j for j, value in enumerate(row)) for row in rows]
    all_bits = (1 << 21) - 1
    blue = [all_bits ^ mask ^ (1 << i) for i, mask in enumerate(red)]
    require(all(not (red[i] >> i & 1) and all((red[i] >> j & 1) == (red[j] >> i & 1)
                for j in range(21)) for i in range(21)), 'bad baseline adjacency')
    caps = [0, 0]
    for i, j in combinations(range(21), 2):
        color = 0 if red[i] >> j & 1 else 1
        masks = red if color == 0 else blue
        caps[color] = max(caps[color], (masks[i] & masks[j]).bit_count())
    degrees = Counter(mask.bit_count() for mask in red)
    result = {'red_edges': sum(mask.bit_count() for mask in red) // 2,
              'red_degree_histogram': {str(d): count for d, count in sorted(degrees.items())},
              'red_spine_max': caps[0], 'blue_spine_max': caps[1]}
    require(result == document['baseline'], 'baseline reproduction differs')


def verify(document):
    require(document['schema'] == 'degree11-leaf-candidates-v1', 'unknown schema')
    audit_scalars(document)
    audit_baseline(document)
    controls = {str(n): len(binary_census(n)[0]) for n in (4, 6, 8)}
    require(controls == document['small_normalized_cubic_counts'], 'small controls differ')
    census, nodes = binary_census(10)
    digest = hashlib.sha256(''.join(str(x) + '\n' for x in census).encode()).hexdigest()
    require(len(census) == document['normalized_labeled_count'] and
            digest == document['domain_sha256'], 'binary census mismatch')
    pairs = list(combinations(range(10), 2))
    position = {pair: i for i, pair in enumerate(pairs)}
    covered = set()
    require(len(document['records']) == document['oriented_edge_orbits'], 'wrong record count')
    require(document['group_size'] == 1440, 'wrong group-size field')
    previous_mask = -1
    for record in document['records']:
        require(set(record) == {'mask', 'orbit_size'}, 'unexpected orbit record fields')
        require(record['mask'] > previous_mask, 'unordered or repeated representatives')
        previous_mask = record['mask']
        core = local_graph(record['mask'])
        for seed in (1, 19, 2047):
            audit_literal_identity(core, seed)
        original = [edge for i, edge in enumerate(pairs) if record['mask'] >> i & 1]
        images = set()
        for swap in (False, True):
            for tail in permutations(range(4, 10)):
                mapping = (0, 1) + ((3, 2) if swap else (2, 3)) + tail
                require(sorted(mapping) == list(range(10)), 'invalid point action')
                image = 0
                for a, b in original:
                    x, y = mapping[a], mapping[b]
                    if y < x:
                        x, y = y, x
                    image |= 1 << position[(x, y)]
                images.add(image)
        require(len(images) == record['orbit_size'] and min(images) == record['mask'],
                'incorrect orbit record')
        require(not covered & images, 'overlapping representative orbits')
        covered.update(images)
    # Compare complete entries, not just the census hash or counts.
    require(covered == set(census), 'orbit union differs from independent labeled sweep')
    return {'complete': True, 'normalized_labeled_count': len(census),
            'oriented_edge_orbits': len(document['records']), 'domain_sha256': digest,
            'binary_nodes': nodes, 'literal_local_cores_checked': len(document['records']),
            'literal_residual_identity_controls': 3 * len(document['records']),
            'literal_mixed_spine_identity_controls': 165 * len(document['records']),
            'literal_row_sum_identity_controls': 33 * len(document['records']),
            'retained_histograms': [[x['n1'], x['n2'], x['n3']]
                                    for x in document['histograms'] if x['allowed']]}


if __name__ == '__main__':
    print(json.dumps(verify(json.loads((HERE / 'expected.json').read_text())),
                     indent=2, sort_keys=True))
