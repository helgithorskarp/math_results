"""Literal bridge controls and forged-certificate rejection, not a host census.

Actual author: six-books-3, researcher. Only Python 3.11 standard library.
Controls may violate the book caps and have negative unused capacity.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import verify

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def baseline():
    data = (HERE / 'baseline21.rows').read_bytes()
    need(sha256(data).hexdigest() == '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec', 'baseline hash')
    rows = data.decode().splitlines()
    need(len(rows) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in rows), 'baseline shape')
    red = [{j for j, bit in enumerate(row) if bit == '1'} for row in rows]
    need(all(i not in red[i] and all(i in red[j] for j in red[i]) for i in range(21)), 'baseline graph')
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    need(sum(map(len, red)) == 186 and sorted(map(len, red)) == [8] * 4 + [9] * 16 + [10], 'baseline degrees')
    need(max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]) == 3, 'baseline red cap')
    need(max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]) == 6, 'baseline blue cap')


def inspect(red, counts, paired=False):
    need(len(red) == 22 and all(len(row) == 10 for row in red), 'control regularity')
    need(all(i not in red[i] and all(i in red[j] for j in red[i]) for i in range(22)), 'control simplicity')
    blue = [set(range(22)) - red[i] - {i} for i in range(22)]
    a, b = sorted(red[0]), sorted(blue[0])
    local = [red[i] & set(a) for i in a]
    h = list(map(len, local))
    misses = [set(a) - red[v] for v in b]
    z = list(map(len, misses))
    gram = [[sum(i in row and j in row for row in misses) for j in a] for i in a]
    need([gram[i][i] for i in range(10)] == [x + 2 for x in h], 'miss column sums')
    need([len(red[v] & set(b)) for v in b] == z, 'outside degrees')
    slack = [[0] * 10 for _ in range(10)]
    for i, j in combinations(range(10), 2):
        x, y = a[i], a[j]
        eps = 3 - len(red[x] & red[y]) if y in red[x] else 6 - len(blue[x] & blue[y])
        slack[i][j] = slack[j][i] = eps
        forced = h[i] + h[j] - (5 if y in red[x] else 2) - len(local[i] & local[j]) - eps
        need(forced == gram[i][j], 'literal full pair bridge')
        counts['pair_identities'] += 1
    for i, x in enumerate(a):
        excess = sum(z[k] - 4 for k, row in enumerate(misses) if x in row)
        neighbor_degree = sum(h[j] for j, y in enumerate(a) if y in local[i])
        need(sum(slack[i]) == 3 * h[i] + sum(h) - 24 - neighbor_degree - excess, 'incident slack bridge')
        counts['incident_identities'] += 1
    if paired:
        isolated = [a[i] for i, degree in enumerate(h) if degree == 0]
        need(len(isolated) == 1 and sum(h) == 26, 'paired control local pattern')
        x = isolated[0]
        indices = [k for k, row in enumerate(misses) if x in row]
        need(len(indices) == 2, 'isolated column sum')
        p, q = (b[k] for k in indices)
        c = set(b) - {p, q}
        k = z[indices[0]] + z[indices[1]] - 2
        outside_edges = sum(len(red[y] & set(b)) for y in b) // 2
        c_edges = sum(len(red[y] & c) for y in c) // 2
        r = int(q in red[p])
        need(outside_edges == sum(h) // 2 + 10, 'outside edge budget')
        need(c_edges == sum(h) // 2 + 8 - k + r, 'paired-root identity')
        need(red[x] == {0} | c and not (red[0] & c), 'paired-root neighborhood decoding')
        counts['paired_root_identities'] += 1
        counts['paired_edge_' + str(r)] += 1
        remaining = [row for index, row in enumerate(misses) if index not in indices]
        for i in range(10):
            for j in range(10):
                if a[i] == x or a[j] == x:
                    continue
                predicted = gram[i][j] - sum(a[i] in misses[index] and a[j] in misses[index] for index in indices)
                actual = sum(a[i] in row and a[j] in row for row in remaining)
                need(predicted == actual, 'literal residual deletion')
                counts['residual_entries'] += 1
    counts['controls'] += 1


def controls(expected):
    counts = {'controls': 0, 'pair_identities': 0, 'incident_identities': 0,
              'paired_root_identities': 0, 'paired_edge_0': 0, 'paired_edge_1': 0, 'residual_entries': 0}
    for steps in combinations(range(1, 11), 5):
        red = [{(i + sign * step) % 22 for step in steps for sign in [-1, 1]} for i in range(22)]
        inspect(red, counts)
    for record in expected['core_records']:
        f = verify.adjacency(record['F_mask'])
        local = [set(), {2, 3}] + [{2 + j for j in row} for row in f]
        local[2].add(1)
        local[3].add(1)
        for kind in ['five_five', 'six_four']:
            parts = [group for group in combinations(range(8), 4 if kind == 'five_five' else 5)
                     if kind != 'five_five' or 0 in group]
            for r in [0, 1]:
                outside = [{(i + step) % 11 for step in [-2, -1, 1, 2]} for i in range(11)]

                def remove(i, j):
                    outside[i].remove(j)
                    outside[j].remove(i)

                def add(i, j):
                    need(j not in outside[i] and i != j, 'duplicate outside edge')
                    outside[i].add(j)
                    outside[j].add(i)

                p = 0
                if kind == 'six_four':
                    q = 1 if r else 3
                    remove(4, 5)
                    add(0, 4)
                    add(0, 5)
                elif r:
                    q = 3
                    add(0, 3)
                else:
                    q = 7
                    remove(3, 4)
                    add(0, 3)
                    add(4, 7)
                need(int(q in outside[p]) == r, 'paired-edge control')
                for group in parts:
                    for last in range(3, 9):
                        steps = {0, 1, 2, last}
                        prime = [{i for i in range(9) if (i - row) % 9 in steps} for row in range(9)]
                        misses = {p: {0} | {2 + i for i in group},
                                  q: {0} | {2 + i for i in range(8) if i not in group}}
                        for v, row in zip([v for v in range(11) if v not in {p, q}], prime):
                            misses[v] = {1 + i for i in row}
                        red = [set() for _ in range(22)]
                        red[0] = set(range(1, 11))
                        for i in range(10):
                            red[1 + i] = {0} | {1 + j for j in local[i]}
                        for v in range(11):
                            red[11 + v] = {11 + w for w in outside[v]}
                            for i in range(10):
                                if i not in misses[v]:
                                    red[1 + i].add(11 + v)
                                    red[11 + v].add(1 + i)
                        inspect(red, counts, paired=True)
    return counts


def forged_inputs(expected, certificates):
    mutations = []
    e = deepcopy(expected)
    e['core_records'].pop()
    mutations.append((e, certificates))
    e = deepcopy(expected)
    e['core_records'][0]['orbit_size'] += 1
    mutations.append((e, certificates))
    e = deepcopy(expected)
    e['cases'].pop()
    mutations.append((e, certificates))
    e = deepcopy(expected)
    e['cases'][0]['states'] += 1
    mutations.append((e, certificates))
    for kind in ['missing_pool', 'bad_coordinate', 'unit_pool']:
        e, c = deepcopy(expected), deepcopy(certificates)
        if kind == 'missing_pool':
            c.pop()
        elif kind == 'bad_coordinate':
            c[0]['vectors'][0][0] = 1.5
        else:
            for pool in c:
                pool['vectors'] = [[1] + [0] * 8]
        # Refresh the hash, ensuring the mathematical guards must reject the forgery.
        e['negative_vectors_sha256'] = sha256(verify.encode(c)).hexdigest()
        mutations.append((e, c))
    for e, c in mutations:
        try:
            verify.certificate_check(e, c)
        except RuntimeError:
            continue
        raise RuntimeError('forged certificate accepted')
    return len(mutations)


if __name__ == '__main__':
    expected = json.loads((HERE / 'expected.json').read_bytes())
    certificates = json.loads((HERE / 'negative_vectors.json').read_bytes())
    baseline()
    print(json.dumps({'agent': 'six-books-3', 'role': 'researcher', 'baseline21': 'verified',
                      'literal_controls': controls(expected),
                      'forged_certificate_rejections': forged_inputs(expected, certificates)}, sort_keys=True))
