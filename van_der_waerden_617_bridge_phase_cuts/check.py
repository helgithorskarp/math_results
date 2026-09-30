#!/usr/bin/env python3
"""Direct exact verifier; imports no generator or propagation engine.

The full normalized phase domain is traversed here, independently of all
generator phase rectangles. Each nonzero binary record is checked as two
seven-APs. Each zero record must have a complete AP-implication refutation.
Euler's criterion, rather than a generated list of squares, gives colors.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import time

P, K, N, C = 617, 7, 3704, 1852
HEADER = struct.Struct('<8s6HI')
RECORD = struct.Struct('<3H')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def colors():
    require(all(P % d for d in range(2, 25)), 'primality617')
    q = [-1]
    for r in range(1, P):
        value = pow(r, (P-1)//2, P)
        require(value in (1, P-1), 'Euler criterion')
        q.append(int(value == P-1))
    return q


def ap_points(ap):
    require(isinstance(ap, list) and len(ap) == 2, 'AP shape')
    a, d = ap
    require(type(a) is int and type(d) is int, 'integer AP')
    require(a >= 0 and d > 0 and a+6*d < N, 'AP bounds or constant AP')
    return [a+j*d for j in range(K)]


def load_supplement(path, h):
    if path is None:
        return {}
    data = json.loads(path.read_text())
    require(data['format'] == 'QR617_AP_IMPLICATIONS_V1', 'supplement format')
    require(type(data['length']) is int and data['length'] == N, 'supplement length')
    require(type(data['half_width']) is int and data['half_width'] == h, 'supplement half width')
    require(isinstance(data['records'], list), 'supplement records')
    result = {}
    for record in data['records']:
        key = record['key']
        require(isinstance(key, list) and len(key) == 3, 'supplement key')
        require(all(type(x) is int for x in key), 'integer phase key')
        s, t, g = key
        require(0 <= s < P and 0 <= t < P and g in (0, 1), 'phase key bounds')
        require(s != t or g != 0, 'compatible key outside scope')
        require(tuple(key) not in result, 'duplicate supplement key')
        result[tuple(key)] = record
    return result


def check_implications(record, key, h, q):
    require(record['key'] == list(key), 'implication key mismatch')
    s, t, g = key
    lo, hi = C-h, C+h
    word = [None]*N
    for x in range(N):
        if lo <= x < hi:
            continue
        phase = s if x < lo else t
        value = q[(x-C+phase) % P]
        if value >= 0:
            word[x] = value ^ (0 if x < lo else g)
    steps = record['steps']
    require(isinstance(steps, list) and len(steps) == 3, 'three-petal star steps')
    initial = word[:]
    vertices = set()
    forced_colors = set()
    for step in steps:
        require(isinstance(step, list) and len(step) == 4, 'implication step shape')
        require(all(type(x) is int for x in step), 'integer implication step')
        x, value, a, d = step
        require(lo <= x < hi and value in (0, 1), 'star point or color bounds')
        points = ap_points([a, d])
        require(x in points and word[x] is None, 'implication must assign an unknown AP point')
        require(all(initial[y] == 1-value for y in points if y != x),
                'star petal lacks six initially protected opposite-color premises')
        vertices.add(x)
        forced_colors.add(value)
        word[x] = value
    final_points = ap_points(record['final_ap'])
    require(len(vertices) == 3 and len(forced_colors) == 1, 'three distinct equally forced star points')
    require({x for x in final_points if initial[x] is None} == vertices,
            'final star AP must have exactly these three initially free points')
    values = [word[x] for x in final_points]
    require(values[0] in (0, 1) and all(x == values[0] for x in values),
            'final AP is not completely fixed and monochromatic')
    return len(steps)


def verify(path, supplement_path=None, expected_h=565):
    start = time.monotonic()
    require(type(expected_h) is int and 1 <= expected_h < C, 'expected half width')
    data = path.read_bytes()
    require(len(data) >= HEADER.size, 'truncated header')
    magic, p, k, n, h, begin, end, count = HEADER.unpack_from(data)
    require(magic == b'QRD617P1', 'certificate magic')
    require((p, k, n) == (P, K, N), 'certificate dimensions')
    require(h == expected_h, 'certificate half width differs from required claim')
    require(begin == 0 and end == P, 'full phase-domain coverage is required')
    target = P*(2*P-1)
    require(count == target, 'full-domain record count')
    require(len(data) == HEADER.size+RECORD.size*target, 'truncated or trailing certificate')
    q = colors()
    supplements = load_supplement(supplement_path, h)
    lo, hi = C-h, C+h
    iterator = struct.iter_unpack('<3H', data[HEADER.size:])
    holes, opposed, total = set(), 0, 0
    histogram = Counter()
    minimum_center, maximum_center = N, -1
    maximum_difference = 0
    for s in range(P):
        for t in range(P):
            for g in (0, 1):
                if s == t and g == 0:
                    continue
                key = (s, t, g)
                v, d0, d1 = next(iterator)
                total += 1
                if (v, d0, d1) == (0, 0, 0):
                    holes.add(key)
                    require(key in supplements, f'missing implication supplement for {key}')
                    histogram[check_implications(supplements[key], key, h, q)] += 1
                    continue
                require(lo <= v < hi, f'free center outside bridge for {key}')
                minimum_center = min(minimum_center, v)
                maximum_center = max(maximum_center, v)
                for b, d in enumerate((d0, d1)):
                    require(d > 0 and 0 <= v-3*d and v+3*d < N,
                            f'symmetric AP bounds or constant AP for {key}')
                    maximum_difference = max(maximum_difference, d)
                    for j in (-3, -2, -1, 1, 2, 3):
                        x = v+j*d
                        require(x < lo or x >= hi, f'AP premise inside free bridge for {key}')
                        phase = s if x < lo else t
                        r = (x-C+phase) % P
                        require(r != 0, f'AP premise is a free template pole for {key}')
                        value = q[r] ^ (0 if x < lo else g)
                        require(value == b, f'AP premise has wrong color for {key}')
                opposed += 1
    require(next(iterator, None) is None and total == target, 'incomplete key traversal')
    require(holes == set(supplements), 'unused or missing implication supplement')
    return {'agent':'six-vdw-3','role':'researcher',
            'status':'VERIFIED_COMPLETE_PROTECTED_EXTERIOR_CUT',
            'length':N,'half_width':h,'bridge':[lo,hi],
            'normalized_incompatible_cases_checked':total,
            'opposed_symmetric_AP_pairs_checked':opposed,
            'AP_premises_checked':12*opposed,
            'implication_refutations_checked':len(holes),
            'implication_steps_histogram':dict(sorted(histogram.items())),
            'implication_steps_checked':sum(k*v for k,v in histogram.items()),
            'opposed_AP_center_range':[minimum_center,maximum_center],
            'maximum_opposed_AP_difference':maximum_difference,
            'certificate_bytes':len(data),
            'certificate_sha256':hashlib.sha256(data).hexdigest(),
            'supplement_sha256':hashlib.sha256(supplement_path.read_bytes()).hexdigest()
                if supplement_path is not None else None,
            'seconds':time.monotonic()-start,
            'scope':'Only incompatible QR617 protected exteriors at length3704; all bridge points and all poles free. No unrestricted nonexistence or improved W(2,7) bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--supplement', type=Path)
    parser.add_argument('--half-width', type=int, default=565)
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.supplement, args.half_width), indent=2))
