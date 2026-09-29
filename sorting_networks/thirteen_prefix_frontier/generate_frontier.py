"""Generate the compact exact prefix certificate using packed Boolean masks."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]
TOURNAMENTS = [
    [[6, 9], [10, 11], [9, 11]],
    [[6, 10], [9, 11], [10, 11]],
    [[6, 11], [9, 10], [10, 11]],
]
PERMUTATION = [0, 1, 2, 7, 8, 5, 9, 3, 4, 10, 6]


def fixture():
    raw = (HERE / 'incumbent.txt').read_bytes()
    nums = list(map(int, raw.split()))
    assert nums[:2] == [13, 45] and len(nums) == 92
    gates = [list(p) for p in zip(nums[2::2], nums[3::2])]
    assert all(0 <= a < b < 13 for a, b in gates)
    return raw, gates


def path(gates, x):
    high = low = 0
    for a, b in gates:
        A, B = (x >> a) & 1, (x >> b) & 1
        high += bool(A or B)
        low += not (A and B)
        if A and not B:
            x ^= (1 << a) | (1 << b)
    return x, high, low


def standardize(permutation, gates):
    """Move a leading permutation through comparators, orienting each gate."""
    pending = list(permutation)
    result = []
    for a, b in gates:
        u, v = pending.index(a), pending.index(b)
        result.append([min(u, v), max(u, v)])
        if u > v:
            pending[u], pending[v] = pending[v], pending[u]
    assert pending == list(range(len(pending)))
    return result


def generate():
    raw, gates = fixture()
    prefix = gates[:21]
    residual12 = sorted({path(prefix, x)[0] & 4095 for x in range(8192)})
    assert len(residual12) == 157
    cuts = {}
    for a, b in itertools.combinations(range(13), 2):
        y, count, _ = path(prefix, (1 << a) | (1 << b))
        assert y >> 12 == 1
        residual = y & 4095
        assert residual.bit_count() == 1
        r = residual.bit_length() - 1
        if count == 7 and r not in cuts:
            cuts[r] = {'residual_wire': r, 'input_pair': [a, b], 'deleted_count': count}
    assert set(cuts) == {6, 9, 10, 11}
    suffix = [p for i, p in enumerate(gates[21:]) if i not in (3, 4, 9)]
    cases = []
    for index, tournament in enumerate(TOURNAMENTS):
        p24 = prefix + tournament
        states = sorted({path(p24, x)[0] & 2047 for x in range(8192)})
        maximum, minimum, max_witness, min_witness = {}, {}, {}, {}
        for x in range(8192):
            if x.bit_count() < 2:
                continue
            y, high, low = path(p24, x)
            assert y >> 11 == 3
            y &= 2047
            if high > maximum.get(y, -1):
                maximum[y], max_witness[y] = high, x
            if low > minimum.get(y, -1):
                minimum[y], min_witness[y] = low, x
        assert sorted(maximum) == states and sorted(minimum) == states
        case_suffix = standardize(PERMUTATION, suffix) if index == 0 else suffix
        cases.append({
            'case': index, 'tournament': tournament, 'states': states,
            'maximum_prefix_deletions': [maximum[x] for x in states],
            'maximum_witness_masks': [max_witness[x] for x in states],
            'minimum_prefix_deletions': [minimum[x] for x in states],
            'minimum_witness_masks': [min_witness[x] for x in states],
            'maximum_suffix_touch_limits': [44 - LOWER[11 - x.bit_count()] - maximum[x] for x in states],
            'minimum_suffix_touch_limits': [44 - LOWER[x.bit_count() + 2] - minimum[x] for x in states],
            'known_21_suffix': case_suffix,
        })
    return {
        'schema': 1, 'agent': 'six-sorting-1', 'role': 'researcher',
        'fixture_sha256': hashlib.sha256(raw).hexdigest(),
        'prefix': prefix, 'residual_12_states': residual12,
        'seven_gate_cuts': [cuts[r] for r in sorted(cuts)],
        'case_0_to_1_permutation': PERMUTATION,
        'known_lower_bounds': LOWER, 'cases': cases,
        'target': 'A <=23-gate suffix for prefix21 exists iff a <=20-gate suffix exists for case1 or case2.',
        'status': 'Exact reduction and necessary bounds; both 20-gate frontiers remain unresolved.',
    }


def main():
    p = argparse.ArgumentParser()
    destination = p.add_mutually_exclusive_group(required=True)
    destination.add_argument('--out', type=Path)
    destination.add_argument('--check', type=Path)
    args = p.parse_args()
    certificate = generate()
    data = (json.dumps(certificate, indent=2, sort_keys=True) + '\n').encode()
    if args.check:
        assert args.check.read_bytes() == data
    else:
        args.out.write_bytes(data)
    print(json.dumps({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                      'state_counts': [len(c['states']) for c in certificate['cases']]}))


if __name__ == '__main__':
    main()
