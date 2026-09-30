"""Witness checker using distinct ranks; imports no generator or SAT code.

Only the witnessed deletion counts are required by the mathematical bound.
It does not certify that no larger prefix deletion count exists.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]


def shortest(vertices, excluded, start, end, reverse=False):
    arcs = [(b, a) if reverse else (a, b) for a, b in itertools.combinations(vertices, 2)
            if (a, b) not in excluded]
    distance = {start: 0}
    queue = [start]
    for v in queue:
        for a, b in arcs:
            if a == v and b not in distance:
                distance[b] = distance[v] + 1
                queue.append(b)
    return distance.get(end)


def evaluate_witness(gates, row):
    labels = []
    rest = row['witness_base3']
    for i in range(13):
        labels.append(rest % 3)
        rest //= 3
    assert rest == 0 and labels.count(2) >= 2 and labels.count(0) >= 1
    low, middle = labels.count(0), labels.count(1)
    assert middle == row['middle_wires']
    pools = [iter(range(low)), iter(range(low, low + middle)),
             iter(range(low + middle, 13))]
    ranks = [next(pools[label]) for label in labels]
    deleted = 0
    for a, b in gates:
        deleted += (ranks[a] < low or ranks[a] >= low + middle or
                    ranks[b] < low or ranks[b] >= low + middle)
        if ranks[a] > ranks[b]:
            ranks[a], ranks[b] = ranks[b], ranks[a]
    assert ranks[-2:] == [11, 12]
    x = sum((rank >= low + middle) << i for i, rank in enumerate(ranks[:11]))
    y = sum((rank >= low) << i for i, rank in enumerate(ranks[:11]))
    assert (x, y, deleted) == (row['high_mask'], row['nonlow_mask'], row['prefix_deleted'])


def tail_touches(gates, x, y):
    colors = [2 if x >> i & 1 else 1 if y >> i & 1 else 0 for i in range(11)]
    count = 0
    for a, b in gates:
        count += colors[a] != 1 or colors[b] != 1
        if colors[a] > colors[b]:
            colors[a], colors[b] = colors[b], colors[a]
    assert colors == sorted(colors)
    return count


def verify(cert, mixed):
    assert cert['known_lower_bounds'] == LOWER
    assert mixed['schema'] == 1
    assert [c['case'] for c in mixed['cases']] == [1, 2]
    checked = 0
    first = cert['cases'][1]['states']
    second = cert['cases'][2]['states']
    assert all(((x >> 1) & 1) <= ((x >> 10) & 1) for x in first + second)
    # This ordered rectangle persists under all standard comparators:
    # the maximum of a prefix cannot increase, nor a suffix minimum decrease.
    assert all(max((x >> i) & 1 for i in range(4)) <= ((x >> 10) & 1) for x in first)
    # No permutation maps the 145-state case into the 146-state case:
    # the omitted row could change each column sum by only zero or one.
    second_column6 = sum(x >> 6 & 1 for x in second)
    first_columns = [sum(x >> i & 1 for x in first) for i in range(11)]
    assert len(first) == len(second) + 1 == 146
    assert second_column6 == 123 and all(s not in (123, 124) for s in first_columns)
    max_skips = [(6, 8), (6, 9), (7, 9)]
    min_skips = [(0, 3), (0, 4), (0, 5), (2, 5)]
    assert shortest([6, 7, 8, 9], max_skips, 6, 9) == 3
    assert shortest([0, 2, 3, 4, 5], min_skips, 5, 0, reverse=True) == 3
    for entry in mixed['cases']:
        case = cert['cases'][entry['case']]
        gates = cert['prefix'] + case['tournament']
        assert len(gates) == 24
        assert len(entry['strict_middle7_rows']) == (68 if entry['case'] == 1 else 66)
        assert len({(r['high_mask'], r['nonlow_mask'])
                    for r in entry['strict_middle7_rows']}) == len(entry['strict_middle7_rows'])
        assert len(entry['one_high_one_low_rows']) == 9
        assert {(r['high_mask'], r['nonlow_mask']) for r in entry['one_high_one_low_rows']} == {
            (1 << i, 2047 ^ (1 << j)) for i in (6, 9, 10) for j in (0, 1, 5)}
        assert case['maximum_suffix_touch_limits'][case['states'].index(64)] == 3
        assert case['minimum_suffix_touch_limits'][case['states'].index(2015)] == 3
        assert any(tuple(p) in max_skips for p in case['known_21_suffix'])
        assert any(tuple(p) in min_skips for p in case['known_21_suffix'])
        for collection in ('strict_middle7_rows', 'one_high_one_low_rows'):
            for row in entry[collection]:
                evaluate_witness(gates, row)
                x, y = row['high_mask'], row['nonlow_mask']
                assert x & ~y == 0 and x in case['states'] and y in case['states']
                k = y.bit_count() - x.bit_count()
                assert k == row['middle_wires']
                assert row['suffix_union_cap'] == 44 - LOWER[k] - row['prefix_deleted']
                separate = (case['maximum_suffix_touch_limits'][case['states'].index(x)] +
                            case['minimum_suffix_touch_limits'][case['states'].index(y)])
                assert separate == row['separate_sum_cap']
                if collection == 'strict_middle7_rows':
                    assert k >= 7 and row['suffix_union_cap'] < separate
                assert tail_touches(case['known_21_suffix'], x, y) <= row['suffix_union_cap'] + 1
                checked += 1
        central = next(r for r in entry['one_high_one_low_rows']
                       if r['high_mask'] == 1024 and r['nonlow_mask'] == 2045)
        assert central['middle_wires'] == 9 and central['prefix_deleted'] == 16
        assert central['suffix_union_cap'] == 3 and central['separate_sum_cap'] == 4
    return checked


def main():
    cert = json.loads((HERE / 'certificate.json').read_text())
    raw = (HERE / 'mixed_certificate.json').read_bytes()
    mixed = json.loads(raw)
    count = verify(cert, mixed)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'witness_bounds_checked': count, 'distinct_stricter_bounds': 134,
                      'one_high_one_low_bounds': 18,
                      'case1_ordered_rectangle': [[0, 1, 2, 3], [10]],
                      'both_cases_initial_order': [1, 10],
                      'case2_no_permutation_subsumption_column': [6, 123],
                      'maximum_branch_shortcuts': [[6, 8], [6, 9], [7, 9]],
                      'minimum_branch_shortcuts': [[0, 3], [0, 4], [0, 5], [2, 5]],
                      'certificate_sha256': hashlib.sha256(raw).hexdigest(),
                      'status': 'Witnessed necessary bounds checked; global gap remains open.'}))


if __name__ == '__main__':
    main()
