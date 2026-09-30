"""Packed Boolean generation of the endpoint and nullary-minimum frontiers."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(gates, x):
    high = low = 0
    for a, b in gates:
        A, B = x >> a & 1, x >> b & 1
        high += bool(A or B)
        low += not (A and B)
        if A > B:
            x ^= (1 << a) | (1 << b)
    return x, high, low


def certificate():
    raw = (HERE / 'fixture.json').read_bytes()
    f = json.loads(raw)
    p24 = f['prefix21'] + f['tournament']
    p25 = p24 + [[0, 10]]
    y = sorted({run(p24, x)[0] & 2047 for x in range(8192)})
    z = sorted({run(p25, x)[0] & 2047 for x in range(8192)})
    maxima, minima = {}, {}
    for x in range(8192):
        if x.bit_count() < 2:
            continue
        out, h, l = run(p25, x)
        out &= 2047
        if h > maxima.get(out, (-1, -1))[0]:
            maxima[out] = h, x
        if l > minima.get(out, (-1, -1))[0]:
            minima[out] = l, x
    bounds = []
    for x in z:
        dh, wh = maxima[x]
        dl, wl = minima[x]
        bounds.append({'state': x,
                       'high_deleted': dh, 'high_witness': wh,
                       'high_cap': 44 - f['known_lower_bounds'][11 - x.bit_count()] - dh,
                       'low_deleted': dl, 'low_witness': wl,
                       'low_cap': 44 - f['known_lower_bounds'][x.bit_count() + 2] - dl})
    kernels = [[[0, 5], [0, 1]]]
    for partner in (2, 3, 4, 6, 7, 8, 9):
        first = [min(partner, 5), max(partner, 5)]
        position = min(partner, 5)
        kernels.append([first, [0, position], [0, 1]])
    kernels.sort()
    minimum = [[0, 5], [0, 1]]
    w = sorted({run(minimum, x)[0] >> 1 for x in z})
    known19 = [[a - 1, b - 1] for i, (a, b) in enumerate(f['known21'])
               if i not in (0, 3)]
    # The ternary witness fixes inputs10 low, 2/3/5 high, the other nine middle.
    labels = [0 if i == 10 else 2 if i in (2, 3, 5) else 1 for i in range(13)]
    code = sum(v * 3 ** i for i, v in enumerate(labels))
    deleted = 0
    for a, b in p25:
        deleted += labels[a] != 1 or labels[b] != 1
        labels[a], labels[b] = min(labels[a], labels[b]), max(labels[a], labels[b])
    mixed = {'witness_base3': code, 'prefix_deleted': deleted,
             'high_mask': sum((v == 2) << i for i, v in enumerate(labels[:11])),
             'nonlow_mask': sum((v != 0) << i for i, v in enumerate(labels[:11])),
             'middle_wires': 9, 'union_cap': 44 - 25 - deleted}
    return {'schema': 1, 'agent': 'six-sorting-1', 'role': 'researcher',
            'fixture_sha256': hashlib.sha256(raw).hexdigest(),
            'prefix25': p25, 'Y2_states': y, 'Z_states': z,
            'unique_initial_inversion': 65, 'replacement_state': 1088,
            'target_budget': 19, 'known_upper': 21,
            'single_threshold_bounds': bounds, 'central_mixed_bound': mixed,
            'minimum_caps': [2, 1, 3], 'minimum_candidates': [0, 1, 5],
            'minimum_kernels': kernels,
            'nullary_minimum_kernel': minimum, 'W_states': w,
            'W_target_budget': 17, 'W_known19': known19,
            'status': 'Structural reductions; Z19 excluded by the separate checked RUP certificate.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--out', type=Path, default=HERE / 'certificate.json')
    args = p.parse_args()
    data = (json.dumps(certificate(), indent=2) + '\n').encode()
    if args.check:
        assert args.out.read_bytes() == data
    else:
        args.out.write_bytes(data)
    print(json.dumps({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
