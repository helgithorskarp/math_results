"""Independent exact checks using Boolean lists and thirteen distinct ranks.

Does not import the generator or SAT encoder.  The known smaller sorting
network lower bounds are literature dependencies, not established by this code.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]


def values(gates, data):
    result = list(data)
    for a, b in gates:
        if result[a] > result[b]:
            result[a], result[b] = result[b], result[a]
    return result


def marked_ranks(gates, selected):
    """Use distinct integers; selected inputs carry the largest ranks."""
    threshold = 13 - len(selected)
    remaining = iter(range(threshold))
    high = iter(range(threshold, 13))
    data = [next(high) if i in selected else next(remaining) for i in range(13)]
    max_deleted = min_deleted = 0
    for a, b in gates:
        max_deleted += data[a] >= threshold or data[b] >= threshold
        min_deleted += data[a] < threshold or data[b] < threshold
        data[a], data[b] = min(data[a], data[b]), max(data[a], data[b])
    return data, threshold, max_deleted, min_deleted


def main():
    raw = (HERE / 'incumbent.txt').read_bytes()
    nums = [int(t) for t in raw.split()]
    assert nums[:2] == [13, 45] and len(nums) == 92
    incumbent = [list(p) for p in zip(nums[2::2], nums[3::2])]
    assert all(0 <= a < b < 13 for a, b in incumbent)
    cert_bytes = (HERE / 'certificate.json').read_bytes()
    cert = json.loads(cert_bytes)
    assert cert['schema'] == 1 and cert['known_lower_bounds'] == EXPECTED_LOWER
    assert cert['fixture_sha256'] == hashlib.sha256(raw).hexdigest()
    prefix = incumbent[:21]
    assert cert['prefix'] == prefix
    residual12 = set()
    residual11 = [set(), set(), set()]
    for x in range(8192):
        data = [(x >> i) & 1 for i in range(13)]
        assert values(incumbent, data) == sorted(data)
        p21 = values(prefix, data)
        assert p21[12] == max(data)
        residual12.add(sum(b << i for i, b in enumerate(p21[:12])))
        for index, case in enumerate(cert['cases']):
            assert case['case'] == index and len(case['tournament']) == 3
            p24 = values(case['tournament'], p21)
            assert p24[-2:] == sorted(data)[-2:]
            residual11[index].add(sum(b << i for i, b in enumerate(p24[:11])))
            assert values(case['known_21_suffix'], p24[:11]) == sorted(data)[:11]
    assert sorted(residual12) == cert['residual_12_states'] and len(residual12) == 157
    assert {x.bit_length() - 1 for x in residual12 if x.bit_count() == 1} == {6, 9, 10, 11}
    assert len(cert['seven_gate_cuts']) == 4
    for cut in cert['seven_gate_cuts']:
        data, threshold, count, _ = marked_ranks(prefix, set(cut['input_pair']))
        assert threshold == 11 and count == cut['deleted_count'] == 7
        assert data[12] == 12 and data[cut['residual_wire']] == 11
    assert {c['residual_wire'] for c in cert['seven_gate_cuts']} == {6, 9, 10, 11}
    expected_tournaments = [
        [[6, 9], [10, 11], [9, 11]],
        [[6, 10], [9, 11], [10, 11]],
        [[6, 11], [9, 10], [10, 11]],
    ]
    assert [c['tournament'] for c in cert['cases']] == expected_tournaments
    for index, case in enumerate(cert['cases']):
        states = case['states']
        assert sorted(residual11[index]) == states
        assert len(states) == (146 if index < 2 else 145)
        for weight in range(12):
            sorted_mask = sum(1 << i for i in range(11 - weight, 11))
            assert sorted_mask in residual11[index]
        p24 = prefix + case['tournament']
        max_counts, min_counts = {}, {}
        max_witness_counts, min_witness_counts = {}, {}
        for mask in range(8192):
            selected = {i for i in range(13) if mask >> i & 1}
            if len(selected) < 2:
                continue
            ranks, threshold, high, low = marked_ranks(p24, selected)
            assert ranks[-2:] == [11, 12]
            result = sum((ranks[i] >= threshold) << i for i in range(11))
            max_counts[result] = max(high, max_counts.get(result, -1))
            min_counts[result] = max(low, min_counts.get(result, -1))
            max_witness_counts[mask] = (result, high)
            min_witness_counts[mask] = (result, low)
        assert set(max_counts) == residual11[index] == set(min_counts)
        assert [max_counts[x] for x in states] == case['maximum_prefix_deletions']
        assert [min_counts[x] for x in states] == case['minimum_prefix_deletions']
        for j, x in enumerate(states):
            assert max_witness_counts[case['maximum_witness_masks'][j]] == (x, max_counts[x])
            assert min_witness_counts[case['minimum_witness_masks'][j]] == (x, min_counts[x])
            upper = 44 - EXPECTED_LOWER[11 - x.bit_count()] - max_counts[x]
            lower = 44 - EXPECTED_LOWER[x.bit_count() + 2] - min_counts[x]
            assert upper == case['maximum_suffix_touch_limits'][j] >= 0
            assert lower == case['minimum_suffix_touch_limits'][j] >= 0
        assert len(case['known_21_suffix']) == 21
        assert all(0 <= a < b < 11 for a, b in case['known_21_suffix'])
    permutation = cert['case_0_to_1_permutation']
    assert sorted(permutation) == list(range(11))
    renamed = {sum(((x >> i) & 1) << j for i, j in enumerate(permutation))
               for x in residual11[0]}
    assert renamed == residual11[1]
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'certificate_sha256': hashlib.sha256(cert_bytes).hexdigest(),
                      'boolean_inputs': 8192, 'case_state_counts': [146, 146, 145],
                      'seven_gate_cuts': 4, 'rank_input_subsets_per_case': 8178,
                      'known_45_networks_checked': 3,
                      'status': 'Exact prefix reduction checked; no 20-gate exclusion or construction.'}))


if __name__ == '__main__':
    main()
