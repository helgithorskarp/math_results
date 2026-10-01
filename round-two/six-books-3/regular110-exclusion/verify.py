"""Independent standard-library checks: forward stars, all labels, integer DP.

Imports neither census.py nor check.py. No computation here is a premise of
the new analytic four-cycle argument or of Hall's published classification.
"""
from pathlib import Path
from itertools import combinations, permutations
import hashlib
import json

HERE = Path(__file__).parent
PAIRS = list(combinations(range(10), 2))
INDEX = {p: k for k, p in enumerate(PAIRS)}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encode(adj):
    return sum(1 << k for k, (i, j) in enumerate(PAIRS) if adj[i] >> j & 1)


def direct():
    adj = [14, 1, 1, 1] + [0] * 6
    degree = [0, 2, 2, 2] + [3] * 6
    out = set()
    calls = 0

    def go(i):
        nonlocal calls
        calls += 1
        if i == 10:
            need(not any(degree), 'Incomplete forward star')
            out.add(encode(adj))
            return
        available = [j for j in range(i + 1, 10) if degree[j] and not adj[i] & adj[j]]
        for chosen in combinations(available, degree[i]):
            if any(adj[a] >> b & 1 for a, b in combinations(chosen, 2)):
                continue
            old = degree[i]
            degree[i] = 0
            for j in chosen:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
                degree[j] -= 1
            if all(degree[j] <= sum(degree[k] > 0 and not adj[j] & adj[k]
                                   for k in range(i + 1, 10) if k != j)
                   for j in range(i + 1, 10)):
                go(i + 1)
            for j in chosen:
                adj[i] ^= 1 << j
                adj[j] ^= 1 << i
                degree[j] += 1
            degree[i] = old
    go(1)
    return out, calls


def orbit(adj):
    need(len(adj) == 10, 'Wrong core order')
    need(all(m.bit_count() == 3 and not m >> i & 1 for i, m in enumerate(adj)), 'Noncubic core')
    need(all(bool(adj[i] >> j & 1) == bool(adj[j] >> i & 1)
             for i, j in PAIRS), 'Asymmetric core')
    need(not any(adj[i] & adj[j] for i, j in PAIRS if adj[i] >> j & 1), 'Triangle in core')
    edges = [(a, b) for a, b in PAIRS if adj[a] >> b & 1]
    out = set()
    mapping = [0] * 10
    for root in range(10):
        nbr = [i for i in range(10) if adj[root] >> i & 1]
        tail = [i for i in range(10) if i != root and i not in nbr]
        mapping[root] = 0
        for nn in permutations((1, 2, 3)):
            for i, v in zip(nbr, nn):
                mapping[i] = v
            for rr in permutations(range(4, 10)):
                for i, v in zip(tail, rr):
                    mapping[i] = v
                mask = 0
                for a, b in edges:
                    x, y = sorted((mapping[a], mapping[b]))
                    mask |= 1 << INDEX[x, y]
                out.add(mask)
    return out


def primary_words():
    raw = (HERE / 'primary_cubic10_g4.g6').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '01324766dc1dfd3b64a9ab130f4162684e9df86f7fee664e6c904e0471eff285',
         'Primary cubic bytes changed')
    words = []
    for line in raw.decode().splitlines():
        need(len(line) == 9 and line[0] == 'I', 'Wrong primary graph6 order/length')
        value = 0
        for character in line[1:]:
            digit = ord(character) - 63
            need(0 <= digit < 64, 'Invalid graph6 character')
            value = value * 64 + digit
        need(value & 7 == 0, 'Nonzero graph6 padding')
        adj = [0] * 10
        position = 47
        for j in range(1, 10):
            for i in range(j):
                if value >> position & 1:
                    adj[i] += 1 << j
                    adj[j] += 1 << i
                position -= 1
        neighbors = [i for i in range(1, 10) if adj[0] >> i & 1]
        need(len(neighbors) == 3, 'Wrong primary root degree')
        tail = [i for i in range(1, 10) if i not in neighbors]
        order = [0] + neighbors + tail
        word = sum(1 << k for k, (i, j) in enumerate(PAIRS) if adj[order[i]] >> order[j] & 1)
        words.append(word)
    return words


def pack_minimum(row_count, occurrences):
    states = {0: 0}
    for _ in range(row_count):
        new = {}
        for total, cost in states.items():
            for used in range(5):
                t = total + used
                c = cost + used * (used - 1) // 2
                new[t] = min(new.get(t, c), c)
        states = new
    return states[occurrences]


def baseline():
    raw = (HERE / 'primary21.txt').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
         'Primary21 bytes changed')
    matrix = json.loads(raw.decode().split('\n\n', 1)[0])
    need(len(matrix) == 21 and all(len(row) == 21 for row in matrix), 'Wrong primary21 dimensions')
    result = {}
    for name, color in [('red', 0), ('blue', 1)]:
        edge_count = 0
        max_pages = 0
        for i, j in combinations(range(21), 2):
            need(matrix[i][j] in (0, 1) and matrix[i][j] == matrix[j][i], 'Invalid baseline matrix')
            if matrix[i][j] == color:
                edge_count += 1
                pages = sum(matrix[i][k] == color and matrix[j][k] == color
                            for k in range(21) if k not in (i, j))
                max_pages = max(max_pages, pages)
        result[name + '_edges'] = edge_count
        result[name + '_max_pages'] = max_pages
    need(result == {'red_edges': 93, 'blue_edges': 117, 'red_max_pages': 3, 'blue_max_pages': 6},
         'Known21 baseline failed')
    return result


def check_cycles(adj):
    neighbors = [{j for j in range(10) if adj[i] >> j & 1} for i in range(10)]
    cycles = 0
    for points in combinations(range(10), 4):
        chosen = set(points)
        degrees = [len(neighbors[i] & chosen) for i in points]
        if degrees == [2] * 4:
            cycles += 1
            upper = 0
            for i, j in combinations(points, 2):
                common = len(neighbors[i] & neighbors[j])
                if j in neighbors[i]:
                    need(common == 0, 'Four-cycle chord/triangle')
                    upper += 1
                else:
                    need(common >= 2, 'Opposite pair lacks two neighbors')
                    upper += 4 - common
            need(upper <= 8, 'Four-cycle capacity contradiction failed')
    return cycles


def run(expected):
    cores = expected['generator']['cores']
    universe, calls = direct()
    covered = set()
    sizes, orbit_sets, cycle_counts = [], [], []
    for core in cores:
        adj = core['neighbors']
        words = orbit(adj)
        need(not covered & words, 'Duplicate core class')
        need(words <= universe, 'Invalid core orbit')
        covered |= words
        sizes.append(len(words))
        orbit_sets.append(words)
        cycle_counts.append(check_cycles(adj))
    need(covered == universe, 'Core classes do not cover direct enumeration')
    primary_ids = []
    for word in primary_words():
        ids = [i + 1 for i, words in enumerate(orbit_sets) if word in words]
        need(len(ids) == 1, 'Primary core lacks unique class')
        primary_ids.append(ids[0])
    need(sorted(primary_ids) == list(range(1, len(cores) + 1)), 'Missing primary class')
    pairs5 = list(combinations(range(5), 2))
    petersen = [sum(1 << j for j, q in enumerate(pairs5) if not set(p) & set(q)) for p in pairs5]
    explicit = orbit(petersen)
    need(explicit == orbit_sets[-1] and cycle_counts[-1] == 0, 'Explicit Petersen comparison failed')
    minimum = pack_minimum(11, 20)
    need(minimum == 9, 'Wrong packing minimum')
    digest = hashlib.sha256(''.join(str(x) + '\n' for x in sorted(universe)).encode()).hexdigest()
    return {'normalized_graphs': len(universe), 'recursion_calls': calls, 'class_sizes': sizes,
            'normalized_sha256': digest, 'primary_data_core_ids': primary_ids,
            'four_cycle_counts': cycle_counts, 'packing_minimum': minimum,
            'Petersen_confirmed': True, 'known21': baseline()}


if __name__ == '__main__':
    expected = json.loads((HERE / 'expected.json').read_text())
    actual = run(expected)
    need(actual == expected['verifier'], 'Expected independent result differs')
    print(json.dumps({'status': 'PASS', 'agent': 'six-books-3', 'role': 'researcher',
                      **actual}, sort_keys=True))
