#!/usr/bin/env python3
"""Definition-level checker for two disjoint protected-exterior support cuts.

No phase rectangles, incidence lists, or propagation engine are imported.
Euler's criterion gives the two partial words. APs and disjoint support sets
are checked directly. --allow-incomplete explicitly weakens output status.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import time

P, K, N, C, H = 617, 7, 3704, 1852, 565
LO, HI = C-H, C+H
HEADER, RECORD = struct.Struct('<8s6HI'), struct.Struct('<3H')


def require(test, message):
    if not test:
        raise ValueError(message)


def qr():
    require(all(P % d for d in range(2, 25)), 'primality617')
    q = [-1]
    for r in range(1, P):
        x = pow(r, (P-1)//2, P)
        require(x in (1, P-1), 'Euler criterion')
        q.append(int(x == P-1))
    return q


def color(x, key, q):
    require(type(x) is int and 0 <= x < N, 'position bounds')
    if LO <= x < HI:
        return None
    s, t, g = key
    r = (x-C+(s if x < LO else t)) % P
    return None if r == 0 else q[r] ^ (0 if x < LO else g)


def ap_points(a, d):
    require(type(a) is int and type(d) is int and a >= 0 and d > 0 and a+6*d < N,
            'AP shape, bounds or constant difference')
    return [a+j*d for j in range(7)]


def opposed(record, key, q):
    v, d0, d1 = record
    require(LO <= v < HI, f'free center outside bridge: {key}')
    support = set()
    for b, d in enumerate((d0, d1)):
        points = ap_points(v-3*d, d)
        require(points[3] == v, 'symmetric AP center')
        for x in points:
            if x == v:
                continue
            require(color(x, key, q) == b, f'unprotected/pole/wrong-color premise: {key}')
            support.add(x)
    require(len(support) == 12, f'two APs must have distinct protected premises: {key}')
    return support


def implications(record, key, q, erased=()):
    require(record['key'] == list(key), 'implication phase key')
    word = [color(x, key, q) for x in range(N)]
    for x in erased:
        require(type(x) is int and 0 <= x < N and word[x] is not None, 'nonprotected erasure')
        word[x] = None
    initial = word[:]
    support = set()
    require(isinstance(record['steps'], list), 'implication step list')
    for step in record['steps']:
        require(isinstance(step, list) and len(step) == 4 and all(type(x) is int for x in step),
                'integer implication step')
        x, value, a, d = step
        require(0 <= x < N and value in (0, 1) and word[x] is None, 'forced value/free point')
        points = ap_points(a, d)
        require(x in points and all(word[y] == 1-value for y in points if y != x),
                f'six fixed opposite-color premises: {key}')
        support.update(y for y in points if initial[y] is not None)
        word[x] = value
    final = record['final_ap']
    require(isinstance(final, list) and len(final) == 2, 'final AP shape')
    points = ap_points(*final)
    require(word[points[0]] in (0, 1) and all(word[y] == word[points[0]] for y in points),
            f'final AP is not completely fixed and monochromatic: {key}')
    support.update(y for y in points if initial[y] is not None)
    require(support and not support.intersection(erased), 'empty or erased support')
    return support


def load_binary(path, magic):
    data = path.read_bytes()
    require(len(data) >= HEADER.size, 'truncated header')
    fields = HEADER.unpack_from(data)
    target = P*(2*P-1)
    require(fields == (magic, P, K, N, H, 0, P, target), 'magic/dimensions/full key coverage')
    require(len(data) == HEADER.size+target*RECORD.size, 'truncated/trailing records')
    return data, struct.iter_unpack('<3H', data[HEADER.size:])


def load_supplement(path, expected_format):
    if path is None:
        return {}
    data = json.loads(path.read_text())
    require(data['format'] == expected_format and data['length'] == N and data['half_width'] == H,
            'supplement format/geometry')
    result = {}
    for r in data['records']:
        require(isinstance(r['key'], list) and len(r['key']) == 3 and all(type(x) is int for x in r['key']),
                'integer phase key')
        key = tuple(r['key'])
        s, t, g = key
        require(0 <= s < P and 0 <= t < P and g in (0, 1) and (s != t or g), 'incompatible key')
        require(key not in result, 'duplicate supplement key')
        result[key] = r
    return result


def verify(first_path, second_path, first_stars, second_supplement=None, allow_incomplete=False):
    start = time.monotonic()
    first_data, first = load_binary(first_path, b'QRD617P1')
    second_data, second = load_binary(second_path, b'QRD617P2')
    stars = load_supplement(first_stars, 'QR617_AP_IMPLICATIONS_V1')
    extras = load_supplement(second_supplement, 'QR617_SECOND_SUPPORT_IMPLICATIONS_V1')
    q = qr()
    first_holes, second_holes, missing = set(), set(), []
    size_pairs, step_histogram = Counter(), Counter()
    total = pairs = 0
    for s in range(P):
        for t in range(P):
            for g in (0, 1):
                if s == t and g == 0:
                    continue
                key = (s, t, g)
                a, b = next(first), next(second)
                if a == (0, 0, 0):
                    first_holes.add(key)
                    require(key in stars, f'missing first star {key}')
                    support_a = implications(stars[key], key, q)
                else:
                    support_a = opposed(a, key, q)
                total += 1
                if b == (0, 0, 0):
                    second_holes.add(key)
                    if key not in extras:
                        require(allow_incomplete, f'missing second proof {key}')
                        missing.append(list(key))
                        continue
                    support_b = implications(extras[key], key, q, erased=support_a)
                    step_histogram[len(extras[key]['steps'])] += 1
                else:
                    support_b = opposed(b, key, q)
                    pairs += 1
                require(not support_a.intersection(support_b), f'protected supports overlap {key}')
                size_pairs[(len(support_a), len(support_b))] += 1
    require(next(first, None) is None and next(second, None) is None, 'incomplete key traversal')
    require(first_holes == set(stars), 'unused/missing first stars')
    require(set(extras).issubset(second_holes), 'unused second implication supplement')
    if not allow_incomplete:
        require(second_holes == set(extras), 'unused/missing second supplements')
    return {'agent': 'six-vdw-3', 'role': 'researcher',
            'status': 'VERIFIED_PARTIAL_TWO_SUPPORT_CUT' if missing else 'VERIFIED_COMPLETE_TWO_SUPPORT_CUT',
            'length': N, 'half_width': H, 'bridge': [LO, HI],
            'incompatible_phase_domain': total,
            'two_disjoint_supports_checked': sum(size_pairs.values()),
            'second_opposed_pairs_checked': pairs,
            'first_implication_proofs_checked': len(first_holes),
            'second_implication_proofs_checked': len(extras),
            'second_implication_steps_histogram': dict(sorted(step_histogram.items())),
            'support_size_pairs': [[a, b, c] for (a, b), c in sorted(size_pairs.items())],
            'uncovered_phase_keys': missing,
            'first_sha256': hashlib.sha256(first_data).hexdigest(),
            'second_sha256': hashlib.sha256(second_data).hexdigest(),
            'seconds': time.monotonic()-start,
            'scope': 'Conditional protected QR617 exteriors, all bridge/poles arbitrary. No unrestricted exclusion or improved W(2,7) bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('first', type=Path)
    parser.add_argument('second', type=Path)
    parser.add_argument('--first-stars', type=Path, required=True)
    parser.add_argument('--second-supplement', type=Path)
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.first, args.second, args.first_stars, args.second_supplement, args.allow_incomplete)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'uncovered_phase_keys'}, indent=2))
