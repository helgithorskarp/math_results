#!/usr/bin/env python3
"""Independent Boolean/wedge and bounded-recurrence identity controls."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
PRIMARY_HASH = '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55'


def require(value, message):
    if not value:
        raise ValueError(message)


def encode(data):
    return json.dumps(data, separators=(',', ':'), sort_keys=True)


def from_masks(masks):
    require(type(masks) is list and len(masks) > 0, 'row list')
    n = len(masks)
    require(all(type(m) is int and 0 <= m < 2 ** n for m in masks), 'row mask domain')
    matrix = [[bool((masks[i] // (2 ** j)) % 2) for j in range(n)] for i in range(n)]
    for i in range(n):
        require(not matrix[i][i], 'loop in graph')
        for j in range(i):
            require(matrix[i][j] == matrix[j][i], 'nonsymmetric graph')
    return matrix


def literal(matrix):
    """Count two-edge walks by centers, without neighborhood intersections."""
    n = len(matrix)
    degrees = [sum(row) for row in matrix]
    red = [[0] * n for _ in range(n)]
    blue = [[0] * n for _ in range(n)]
    for w in range(n):
        for u in range(n):
            if w == u:
                continue
            for v in range(u + 1, n):
                if w == v:
                    continue
                if matrix[w][u] and matrix[w][v]:
                    red[u][v] += 1
                elif not matrix[w][u] and not matrix[w][v]:
                    blue[u][v] += 1
    maximum = [0, 0]
    failures = [0, 0]
    for u in range(n):
        for v in range(u + 1, n):
            red[v][u], blue[v][u] = red[u][v], blue[u][v]
            endpoint_correction = 2 if matrix[u][v] else 0
            require(blue[u][v] == n - 2 - degrees[u] - degrees[v] +
                    red[u][v] + endpoint_correction, 'literal endpoint identity')
            index = 0 if matrix[u][v] else 1
            pages = red[u][v] if matrix[u][v] else blue[u][v]
            maximum[index] = max(maximum[index], pages)
            failures[index] += int(pages > (3 if index == 0 else 6))
    return degrees, red, blue, maximum, failures


def primary(raw):
    require(hashlib.sha256(raw).hexdigest() == PRIMARY_HASH, 'baseline byte hash')
    # Parse only the matrix block; retain and authenticate the complete raw file.
    values = json.loads(raw.decode().split('\n\n', 1)[0])
    require(type(values) is list and len(values) == 21, 'baseline order')
    require(all(type(row) is list and len(row) == 21 for row in values), 'baseline rows')
    require(all(type(x) is int and x in [0, 1] for row in values for x in row), 'baseline values')
    require(all(values[i][i] == 0 for i in range(21)), 'baseline diagonal')
    require(all(values[i][j] == values[j][i] for i in range(21) for j in range(i)),
            'baseline symmetry')
    matrix = [[i != j and values[i][j] == 0 for j in range(21)] for i in range(21)]
    d, _, _, pages, failures = literal(matrix)
    edges = sum(int(matrix[i][j]) for i in range(21) for j in range(i))
    require(edges == 93 and pages == [3, 6] and failures == [0, 0], 'baseline Ramsey control')
    return {'raw_sha256': PRIMARY_HASH, 'order': 21, 'red_edges': edges,
            'blue_edges': 210 - edges, 'red_pages': pages[0], 'blue_pages': pages[1],
            'checked_pairs': 210,
            'degree_histogram': {str(k): v for k, v in sorted(Counter(d).items())}}


def signed_control(item):
    require(type(item) is dict and sorted(item) ==
            ['expected_n', 'expected_q', 'name', 'red_masks'], 'physical control fields')
    require(type(item['name']) is str and len(item['name']) > 0, 'physical control label')
    matrix = from_masks(item['red_masks'])
    require(len(matrix) == 22, 'physical order')
    d, red, blue, maximum, failures = literal(matrix)
    require(d == [9] * 4 + [10] * 18, 'physical degree profile')
    lows = [sum(matrix[i][j] for j in range(4)) for i in range(4)]
    q = sum(int(matrix[i][j]) for i in range(4) for j in range(i))
    high_type_sizes = [sum(matrix[x][i] for i in range(4)) for x in range(4, 22)]
    histogram = Counter(high_type_sizes)
    require(histogram[0] == 0, 'physical rootless condition')
    counts = [histogram[t] for t in [1, 2, 3, 4]]
    require(type(item['expected_q']) is int and item['expected_q'] == q,
            'physical low edge declaration')
    require(type(item['expected_n']) is list and all(type(x) is int for x in item['expected_n'])
            and item['expected_n'] == counts, 'physical type declaration')
    require(2 * q + counts[2] + 2 * counts[3] == counts[0], 'physical degree sum count')
    row_slacks, negative = [], 0
    for x in range(4, 22):
        total = 0
        for i in range(4):
            bound = 3 if matrix[x][i] else 5
            s = bound - red[i][x]
            total += s
            negative += int(s < 0)
        row_slacks.append(total)
    total_slack = sum(row_slacks)
    # Count cross-endpoint walks directly by their centers as a separate bridge.
    walk_count = 0
    for w in range(22):
        left = sum(matrix[w][i] for i in range(4))
        right = sum(matrix[w][x] for x in range(4, 22))
        walk_count += left * right
    require(walk_count == sum(red[i][x] for i in range(4) for x in range(4, 22)),
            'cross-center walk count')
    require(total_slack == 288 + 4 * q - walk_count, 'literal cap total')
    require(total_slack == 2 * counts[2] + 6 * counts[3] + sum(x * x for x in lows),
            'literal weighted slack')
    alpha = []
    for i in range(4):
        triangles = sum(int(matrix[i][u] and matrix[i][v] and matrix[u][v])
                        for u in range(22) for v in range(u + 1, 22))
        value = 27 - 2 * triangles
        require(value % 2 == 1, 'literal neighborhood parity')
        require(value == sum(3 - red[i][x] for x in range(22) if matrix[i][x]),
                'literal red deficit')
        alpha.append(value)
    blue_slack = sum(6 - blue[i][x] for i in range(4) for x in range(4, 22)
                     if not matrix[i][x])
    twice_low = sum(2 * (3 - red[i][j]) for i in range(4)
                    for j in range(i + 1, 4) if matrix[i][j])
    require(total_slack + twice_low == sum(alpha) + blue_slack, 'literal low correction')
    require(sum(failures) > 0, 'physical control is not a valid host')
    return {'name': item['name'], 'q': q, 'n': counts, 'red_edges': sum(d) // 2,
            'mixed_slack': total_slack, 'low_internal_degrees': lows,
            'row_slacks': row_slacks, 'negative_mixed_slacks': negative,
            'alpha': alpha, 'blue_mixed_slack': blue_slack,
            'twice_low_red_slack': twice_low,
            'red_pages': maximum[0], 'blue_pages': maximum[1],
            'red_failing_pairs': failures[0], 'blue_failing_pairs': failures[1],
            'low_pair_red_codegrees': [red[i][j] for i in range(4) for j in range(i + 1, 4)]}


def controls(data):
    require(type(data) is dict and sorted(data) == ['controls', 'schema'], 'control envelope')
    require(type(data['schema']) is int and data['schema'] == 1, 'control schema')
    require(type(data['controls']) is list and len(data['controls']) == 6, 'control coverage')
    answer = [signed_control(item) for item in data['controls']]
    require(len(set(item['name'] for item in answer)) == len(answer), 'control labels')
    return answer


def exhaustive_small():
    checksum = hashlib.sha256()
    totals = []
    for n in range(1, 7):
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        m = [[False] * n for _ in range(n)]
        seen = checked = red_pairs = blue_pairs = 0

        def leaf(key):
            nonlocal seen, checked, red_pairs, blue_pairs
            require(key == seen, 'noncontiguous exhaustive small graph coverage')
            seen += 1
            _, red, blue, _, _ = literal(m)
            for u, v in pairs:
                checksum.update(f'{n}:{key}:{u}:{v}:{red[u][v]}:{blue[u][v]}\n'.encode())
                checked += 1
                if m[u][v]: red_pairs += 1
                else: blue_pairs += 1

        def visit(k, key):
            if k < 0:
                leaf(key)
                return
            u, v = pairs[k]
            m[u][v] = m[v][u] = False
            visit(k - 1, key)
            m[u][v] = m[v][u] = True
            visit(k - 1, key + 2 ** k)
            m[u][v] = m[v][u] = False

        visit(len(pairs) - 1, 0)
        require(seen == 2 ** len(pairs), 'small graph completion')
        totals.append({'order': n, 'graphs': seen, 'pairs': checked,
                       'red_pairs': red_pairs, 'blue_pairs': blue_pairs})
    return {'orders': totals, 'graphs': sum(r['graphs'] for r in totals),
            'pairs': sum(r['pairs'] for r in totals),
            'ordered_pair_sha256': checksum.hexdigest()}


def bounded_profiles():
    records = []
    for q in range(7):
        desired = 36 - 2 * q

        def extend(t, vertices_left, incidences_left, counts):
            if t == 1:
                if vertices_left == incidences_left:
                    completed = [vertices_left] + list(reversed(counts))
                    require(completed[0] == 2 * q + completed[2] + 2 * completed[3],
                            'bounded recurrence identity')
                    records.append([q] + completed)
                return
            for number in range(vertices_left + 1):
                rest = incidences_left - t * number
                left = vertices_left - number
                if left <= rest <= (t - 1) * left:
                    extend(t - 1, left, rest, counts + [number])

        extend(4, 18, desired, [])
    records.sort()
    require(len(set(tuple(r) for r in records)) == len(records), 'profile duplicates')
    exceptional = [r for r in records if r[1] in [0, 1]]
    require(exceptional == [[0, 0, 18, 0, 0], [0, 1, 16, 1, 0]], 'exceptional coverage')
    surviving = [r[1] for r in records if r[0] > 0 or r[3] + 3 * r[4] >= 2]
    require(min(surviving) == 2, 'bounded relaxed minimum')
    # This is a degree-count relaxation, not a graph construction.
    boundary = [1, 0, 16, 0, 1]
    incidences = sum(t * boundary[t] for t in range(5))
    require(sum(boundary) == 18 and incidences == 36, 'nonrootless boundary margin')
    require(boundary[1] == -2 * boundary[0] + boundary[3] + 2 * boundary[4],
            'nonrootless sign')
    return {'profiles': len(records), 'by_q': [sum(r[0] == q for r in records) for q in range(7)],
            'ordered_profile_sha256': hashlib.sha256(encode(records).encode()).hexdigest(),
            'zero_one_singleton_profiles': exceptional, 'parity_relaxed_minimum_n1': 2,
            'nonrootless_boundary': {'q': 0, 'n0_to_n4': boundary, 'incidences': incidences,
                                    'correct_n1': 0, 'wrong_plus_n0_n1': 4}}


def match(actual, wanted):
    require(type(wanted) is dict and encode(actual) == encode(wanted), 'complete expected mismatch')


def compute():
    return {'schema': 1, 'primary21': primary((DIRECTORY / 'primary21.txt').read_bytes()),
            'small_graphs': exhaustive_small(), 'profiles': bounded_profiles(),
            'controls': controls(json.loads((DIRECTORY / 'controls.json').read_text()))}


def damaged_controls():
    data = json.loads((DIRECTORY / 'controls.json').read_text())
    good = controls(data)
    primary((DIRECTORY / 'primary21.txt').read_bytes())
    rejected = []
    for name in ['self-loop', 'asymmetric', 'mask-range', 'wrong-q', 'wrong-profile',
                 'wrong-degree', 'missing-control', 'duplicate-name', 'bool-mask',
                 'nonrootless-degree-correct']:
        d = copy.deepcopy(data)
        first = d['controls'][0]
        if name == 'self-loop': first['red_masks'][0] += 1
        elif name == 'asymmetric': first['red_masks'][0] ^= 16
        elif name == 'mask-range': first['red_masks'][0] += 2 ** 22
        elif name == 'wrong-q': first['expected_q'] += 1
        elif name == 'wrong-profile': first['expected_n'][0] += 1
        elif name == 'wrong-degree':
            matrix = from_masks(first['red_masks'])
            x = next(x for x in range(4, 22) if matrix[0][x])
            first['red_masks'][0] -= 2 ** x
            first['red_masks'][x] -= 1
        elif name == 'missing-control': d['controls'] = d['controls'][:-1]
        elif name == 'duplicate-name': d['controls'][1]['name'] = first['name']
        elif name == 'bool-mask': first['red_masks'][0] = False
        else:
            d['controls'][0] = copy.deepcopy(data['controls'][2])
            first = d['controls'][0]
            first['name'] = data['controls'][0]['name']
            first['expected_n'] = [0, 16, 0, 1]
            matrix = from_masks(first['red_masks'])
            for low in [0, 1]:
                matrix[low][4] = matrix[4][low] = False
                matrix[low][7] = matrix[7][low] = True
            for x in [9, 10]:
                matrix[7][x] = matrix[x][7] = False
                matrix[4][x] = matrix[x][4] = True
            require([sum(row) for row in matrix] == [9] * 4 + [10] * 18,
                    'nonrootless control must preserve degrees')
            require(sum(not any(matrix[x][:4]) for x in range(4, 22)) == 1,
                    'nonrootless control must have one empty type')
            first['red_masks'] = [sum(2 ** j for j in range(22) if row[j]) for row in matrix]
        try:
            controls(d)
        except ValueError as error:
            if name == 'nonrootless-degree-correct':
                require('rootless' in str(error), 'wrong reason for nonrootless rejection')
            rejected.append(name)
        else:
            raise ValueError('damage accepted: ' + name)
    forged = copy.deepcopy(good)
    forged[0]['mixed_slack'] += 1
    try:
        match({'controls': good}, {'controls': forged})
    except ValueError:
        rejected.append('forged-summary')
    else:
        raise ValueError('forged summary accepted')
    return {'schema': 1, 'rejected': rejected, 'reject_count': len(rejected),
            'positive_controls': len(good), 'primary_pages': [3, 6],
            'nonrootless_control_n0_to_n4': [1, 0, 16, 0, 1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    require(not (args.expected and args.self_test), 'one execution mode')
    result = damaged_controls() if args.self_test else compute()
    if args.expected:
        match(result, json.loads(args.expected.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
