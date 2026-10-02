#!/usr/bin/env python3
"""Exact bit-mask controls for the ordinary one-nine-root parity proof."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIMARY_SHA = '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def validate_masks(rows):
    need(isinstance(rows, list), 'rows must be a list')
    n = len(rows)
    need(n > 0, 'empty graph')
    for i, r in enumerate(rows):
        need(type(r) is int and 0 <= r < (1 << n), 'mask outside graph')
        need(not r & (1 << i), 'red self loop')
        for j in range(i):
            need(((r >> j) & 1) == ((rows[j] >> i) & 1), 'asymmetric graph')
    return rows


def pair_tables(rows):
    validate_masks(rows)
    n = len(rows)
    full = (1 << n) - 1
    blue = [full ^ rows[i] ^ (1 << i) for i in range(n)]
    degrees = [r.bit_count() for r in rows]
    red_common = [[0] * n for _ in range(n)]
    blue_common = [[0] * n for _ in range(n)]
    pages = [0, 0]
    failures = [0, 0]
    for u in range(n):
        for v in range(u + 1, n):
            edge = (rows[u] >> v) & 1
            cr = (rows[u] & rows[v]).bit_count()
            cb = (blue[u] & blue[v]).bit_count()
            need(cb == n - 2 - degrees[u] - degrees[v] + cr + 2 * edge,
                 'endpoint identity')
            red_common[u][v] = red_common[v][u] = cr
            blue_common[u][v] = blue_common[v][u] = cb
            color = 0 if edge else 1
            actual = cr if edge else cb
            pages[color] = max(pages[color], actual)
            failures[color] += int(actual > (3 if edge else 6))
    return degrees, red_common, blue_common, pages, failures


def primary_report(raw):
    need(hashlib.sha256(raw).hexdigest() == PRIMARY_SHA, 'primary raw hash')
    # The authors append search metadata after the leading JSON matrix.
    matrix, end = json.JSONDecoder().raw_decode(raw.decode())
    need(raw.decode()[end:].startswith('\n\nsearch_function_used = '), 'primary trailer')
    need(type(matrix) is list and len(matrix) == 21, 'primary order')
    need(all(type(r) is list and len(r) == 21 for r in matrix), 'primary dimensions')
    need(all(type(v) is int and v in (0, 1) for r in matrix for v in r), 'primary values')
    need(all(matrix[i][i] == 0 for i in range(21)), 'primary diagonal')
    need(all(matrix[i][j] == matrix[j][i] for i in range(21)
             for j in range(i)), 'primary symmetry')
    rows = [sum(1 << j for j in range(21) if i != j and matrix[i][j] == 0)
            for i in range(21)]
    degrees, _, _, pages, failures = pair_tables(rows)
    edges = sum(degrees) // 2
    need(edges == 93 and pages == [3, 6] and failures == [0, 0], 'primary page control')
    return {'raw_sha256': PRIMARY_SHA, 'order': 21, 'red_edges': edges,
            'blue_edges': 210 - edges, 'red_pages': pages[0], 'blue_pages': pages[1],
            'checked_pairs': 210,
            'degree_histogram': {str(k): v for k, v in sorted(Counter(degrees).items())}}


def control_report(item):
    need(type(item) is dict and set(item) == {'name', 'red_masks', 'expected_q', 'expected_n'},
         'control fields')
    need(type(item['name']) is str and item['name'], 'control name')
    rows = item['red_masks']
    need(type(rows) is list and len(rows) == 22, 'control order')
    degrees, cr, cb, pages, failures = pair_tables(rows)
    need(degrees[:4] == [9] * 4 and degrees[4:] == [10] * 18, 'control degrees')
    need(sum(degrees) == 216, 'control edge sum')
    a = [(rows[i] & 15).bit_count() for i in range(4)]
    q = sum(a) // 2
    types = [(rows[x] & 15).bit_count() for x in range(4, 22)]
    counts = [types.count(t) for t in range(5)]
    need(counts[0] == 0, 'control rootlessness')
    need(type(item['expected_q']) is int and item['expected_q'] == q, 'declared q')
    need(type(item['expected_n']) is list and
         all(type(v) is int for v in item['expected_n']) and
         item['expected_n'] == counts[1:], 'declared type profile')
    n1, n2, n3, n4 = counts[1:]
    need(n1 == 2 * q + n3 + 2 * n4, 'type-count identity')
    slack = [[(3 if (rows[i] >> x) & 1 else 5) - cr[i][x]
              for x in range(4, 22)] for i in range(4)]
    total = sum(map(sum, slack))
    weighted = 2 * n3 + 6 * n4 + sum(d * d for d in a)
    need(total == weighted, 'mixed slack identity')
    alpha = []
    for i in range(4):
        neighbors = [x for x in range(22) if (rows[i] >> x) & 1]
        e = sum((rows[u] >> v) & 1 for j, u in enumerate(neighbors)
                for v in neighbors[j + 1:])
        direct = sum(3 - cr[i][x] for x in neighbors)
        need(direct == 27 - 2 * e and direct % 2 == 1, 'odd neighborhood deficit')
        alpha.append(direct)
    blue_slack = sum(5 - cr[i][x] for i in range(4) for x in range(4, 22)
                     if not (rows[i] >> x) & 1)
    low_red_slack_twice = 2 * sum(3 - cr[i][j] for i in range(4)
                                  for j in range(i + 1, 4) if (rows[i] >> j) & 1)
    need(total == sum(alpha) + blue_slack - low_red_slack_twice,
         'low-edge correction to parity')
    need(sum(failures) > 0, 'fixture must be invalid, not a host witness')
    return {'name': item['name'], 'q': q, 'n': counts[1:], 'red_edges': 108,
            'mixed_slack': total, 'low_internal_degrees': a,
            'row_slacks': [sum(slack[i][j] for i in range(4)) for j in range(18)],
            'negative_mixed_slacks': sum(v < 0 for r in slack for v in r),
            'alpha': alpha, 'blue_mixed_slack': blue_slack,
            'twice_low_red_slack': low_red_slack_twice,
            'red_pages': pages[0], 'blue_pages': pages[1],
            'red_failing_pairs': failures[0], 'blue_failing_pairs': failures[1],
            'low_pair_red_codegrees': [cr[i][j] for i in range(4) for j in range(i + 1, 4)]}


def all_controls(data):
    need(type(data) is dict and set(data) == {'schema', 'controls'}, 'fixture fields')
    need(type(data['schema']) is int and data['schema'] == 1, 'fixture schema')
    need(type(data['controls']) is list and len(data['controls']) == 6, 'fixture count')
    result = [control_report(x) for x in data['controls']]
    need(len({x['name'] for x in result}) == len(result), 'duplicate fixture names')
    return result


def small_graphs():
    digest = hashlib.sha256()
    records = []
    for n in range(1, 7):
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        checked = red_pairs = blue_pairs = 0
        for key in range(1 << len(pairs)):
            rows = [0] * n
            for k, (u, v) in enumerate(pairs):
                if (key >> k) & 1:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            d = [r.bit_count() for r in rows]
            b = [((1 << n) - 1) ^ rows[u] ^ (1 << u) for u in range(n)]
            for u, v in pairs:
                edge = (rows[u] >> v) & 1
                cr = (rows[u] & rows[v]).bit_count()
                cb = (b[u] & b[v]).bit_count()
                need(cb == n - 2 - d[u] - d[v] + cr + 2 * edge, 'small endpoint control')
                digest.update(f'{n}:{key}:{u}:{v}:{cr}:{cb}\n'.encode())
                checked += 1
                red_pairs += edge
                blue_pairs += 1 - edge
        records.append({'order': n, 'graphs': 1 << len(pairs), 'pairs': checked,
                        'red_pairs': red_pairs, 'blue_pairs': blue_pairs})
    return {'orders': records, 'graphs': sum(r['graphs'] for r in records),
            'pairs': sum(r['pairs'] for r in records),
            'ordered_pair_sha256': digest.hexdigest()}


def margin_profiles():
    records = []
    for n1 in range(19):
        for n2 in range(19 - n1):
            for n3 in range(19 - n1 - n2):
                n4 = 18 - n1 - n2 - n3
                incidence = n1 + 2 * n2 + 3 * n3 + 4 * n4
                gap = 36 - incidence
                if gap < 0 or gap > 12 or gap % 2:
                    continue
                q = gap // 2
                need(n1 == 2 * q + n3 + 2 * n4, 'profile identity')
                records.append([q, n1, n2, n3, n4])
    records.sort()
    small = [r for r in records if r[1] <= 1]
    need(small == [[0, 0, 18, 0, 0], [0, 1, 16, 1, 0]], 'small singleton coverage')
    allowed = [r for r in records if r[0] != 0 or r[3] + 3 * r[4] >= 2]
    need(min(r[1] for r in allowed) == 2, 'relaxed parity minimum')
    return {'profiles': len(records), 'by_q': [sum(r[0] == q for r in records) for q in range(7)],
            'ordered_profile_sha256': hashlib.sha256(canonical(records).encode()).hexdigest(),
            'zero_one_singleton_profiles': small,
            'parity_relaxed_minimum_n1': 2,
            'nonrootless_boundary': {'q': 0, 'n0_to_n4': [1, 0, 16, 0, 1],
                                    'incidences': 36, 'correct_n1': 0, 'wrong_plus_n0_n1': 4}}


def compare(actual, expected):
    need(type(expected) is dict and canonical(actual) == canonical(expected),
         'full expected record mismatch')


def run():
    fixture = json.loads((HERE / 'controls.json').read_text())
    return {'schema': 1, 'primary21': primary_report((HERE / 'primary21.txt').read_bytes()),
            'small_graphs': small_graphs(), 'profiles': margin_profiles(),
            'controls': all_controls(fixture)}


def self_test():
    base = json.loads((HERE / 'controls.json').read_text())
    original = all_controls(base)
    primary_report((HERE / 'primary21.txt').read_bytes())
    damaged = []
    for tag in ('self-loop', 'asymmetric', 'mask-range', 'wrong-q', 'wrong-profile',
                'wrong-degree', 'missing-control', 'duplicate-name', 'bool-mask',
                'nonrootless-degree-correct'):
        d = copy.deepcopy(base)
        item = d['controls'][0]
        if tag == 'self-loop': item['red_masks'][0] |= 1
        elif tag == 'asymmetric': item['red_masks'][0] ^= 1 << 4
        elif tag == 'mask-range': item['red_masks'][0] |= 1 << 22
        elif tag == 'wrong-q': item['expected_q'] += 1
        elif tag == 'wrong-profile': item['expected_n'][0] += 1
        elif tag == 'wrong-degree':
            x = next(x for x in range(4, 22) if item['red_masks'][0] & (1 << x))
            item['red_masks'][0] ^= 1 << x
            item['red_masks'][x] ^= 1
        elif tag == 'missing-control': d['controls'].pop()
        elif tag == 'duplicate-name': d['controls'][1]['name'] = item['name']
        elif tag == 'bool-mask': item['red_masks'][0] = False
        else:
            # Preserve every degree, but replace a pair and its opposite by
            # an empty type and a quadruple type. This exercises n0=0 itself.
            d['controls'][0] = copy.deepcopy(base['controls'][2])
            item = d['controls'][0]
            item['name'] = base['controls'][0]['name']
            item['expected_n'] = [0, 16, 0, 1]
            def link(i, j, on):
                if on:
                    item['red_masks'][i] |= 1 << j
                    item['red_masks'][j] |= 1 << i
                else:
                    item['red_masks'][i] &= ~(1 << j)
                    item['red_masks'][j] &= ~(1 << i)
            for low in (0, 1):
                link(low, 4, False)
                link(low, 7, True)
            for x in (9, 10):
                link(7, x, False)
                link(4, x, True)
            degrees, _, _, _, _ = pair_tables(item['red_masks'])
            need(degrees == [9] * 4 + [10] * 18, 'nonrootless damage preserves degrees')
            need(sum((r & 15) == 0 for r in item['red_masks'][4:]) == 1,
                 'nonrootless damage has one empty type')
        try:
            all_controls(d)
        except ValueError as error:
            if tag == 'nonrootless-degree-correct':
                need('rootlessness' in str(error), 'wrong nonrootless rejection')
            damaged.append(tag)
        else:
            raise ValueError('damaged fixture accepted: ' + tag)
    forged = copy.deepcopy(original)
    forged[0]['mixed_slack'] += 1
    try:
        compare({'controls': original}, {'controls': forged})
    except ValueError:
        damaged.append('forged-summary')
    else:
        raise ValueError('forged summary accepted')
    return {'schema': 1, 'rejected': damaged, 'reject_count': len(damaged),
            'positive_controls': len(original), 'primary_pages': [3, 6],
            'nonrootless_control_n0_to_n4': [1, 0, 16, 0, 1]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected', type=Path)
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    need(not (args.expected and args.self_test), 'choose replay or self-test')
    answer = self_test() if args.self_test else run()
    if args.expected:
        compare(answer, json.loads(args.expected.read_text()))
    print(json.dumps(answer, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
