"""Generate the two53-state and common41-state completion targets.

Author: six-sorting-1 (researcher). Packed Boolean generation; verification
uses distinct-rank and Boolean-list code in verify.py independently.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def counted(x, word):
    high = low = 0
    for a, b in word:
        A, B = x >> a & 1, x >> b & 1
        high += bool(A or B)
        low += not (A and B)
        if A > B:
            x ^= (1 << a) | (1 << b)
    return x, high, low


def prefix(f, case, length=32, minimum=None):
    p = f['prefix21'] + f['tournaments'][str(case)] + f['minimum_front']
    p += [[a + 1, b + 1] for a, b in (minimum or f['minimum7_on_V'])]
    assert len(p) == 32
    if length == 34:
        p += [[a + 2, b + 2] for a, b in f['maximum3_on_U']]
    return p


def data():
    raw = (HERE / 'fixture.json').read_bytes()
    f = json.loads(raw)
    cases = []
    for case in (1, 2):
        p32, p34 = prefix(f, case), prefix(f, case, 34)
        U = sorted({counted(x, p32)[0] >> 2 & 511 for x in range(8192)})
        F = sorted({counted(x, p34)[0] >> 2 & 255 for x in range(8192)})
        cases.append({'case': case, 'prefix32': p32, 'prefix34': p34,
                      'U_states': U, 'F_states': F})
    assert cases[0]['F_states'] == cases[1]['F_states']
    limits = {}
    p34 = cases[1]['prefix34']
    for x in range(8192):
        if x.bit_count() < 2:
            continue
        z, h, l = counted(x, p34)
        z = z >> 2 & 255
        values = (44 - f['known_lower_bounds'][13 - x.bit_count()] - h,
                  44 - f['known_lower_bounds'][x.bit_count()] - l)
        for direction, cap, used in zip(('high', 'low'), values, (h, l)):
            key = (z, direction)
            if key not in limits or cap < limits[key]['cap']:
                limits[key] = {'cap': cap, 'witness': x, 'deleted': used}
    bounds = []
    for x in cases[1]['F_states']:
        r = {'state': x}
        for direction in ('high', 'low'):
            r.update({direction + '_' + k: v for k, v in limits[x, direction].items()})
        bounds.append(r)
    others = []
    for r in f['subsumed_Y2_kernels']:
        p32 = prefix(f, 2, minimum=r['minimum7_on_V'])
        others.append({**r, 'prefix32': p32,
                       'states': sorted({counted(x, p32)[0] >> 2 & 511 for x in range(8192)})})
    kernels = [[[1, 2], [0, 1]]]
    kernels += [[[2, p], [1, 2], [0, 1]] for p in (3, 4, 5, 6)]
    return {'schema': 1, 'agent': 'six-sorting-1', 'role': 'researcher',
            'fixture_sha256': hashlib.sha256(raw).hexdigest(), 'cases': cases,
            'F_bound_provenance_case': 2, 'F_target_budget': 10,
            'F_single_threshold_bounds': bounds, 'F_minimum_kernels': kernels,
            'F_conditional_routes': {'minimum0': 1, 'minimum1': 2, 'maximum7': 1},
            'subsumed_Y2_cases': others,
            'conclusion': 'The two U sets have sorting size13; their common F has sorting size11. Three further Y2 tree cases have sorting size at least13.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    raw = (json.dumps(data(), indent=2) + '\n').encode()
    if args.check:
        assert (HERE / 'certificate.json').read_bytes() == raw
    else:
        (HERE / 'certificate.json').write_bytes(raw)
    print(json.dumps({'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    main()
