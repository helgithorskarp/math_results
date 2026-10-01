"""Exact input construction and serialization. six-code-2, researcher."""
from hashlib import sha256
from itertools import combinations, product
import json
import time

STATE_LIMIT = 40000
SECONDS_LIMIT = 45


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def guard(start, states=0):
    require(states <= STATE_LIMIT and time.monotonic() - start < SECONDS_LIMIT,
            'INCOMPLETE: state/time guard; verdict UNKNOWN')


def mul(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 19
    return value


def power(a, exponent):
    value = 1
    while exponent:
        if exponent & 1:
            value = mul(value, a)
        a = mul(a, a)
        exponent >>= 1
    return value


def divide(a, b):
    require(b != 0, 'division by zero')
    return mul(a, power(b, 14))


def mask(points):
    return sum(1 << p for p in points)


def move(word, permutation):
    return mask(permutation[p] for p in range(17) if word >> p & 1)


def projective_image(a, b, c, d, point):
    if point == 16:
        return divide(a, c) if c else 16
    numerator, denominator = mul(a, point) ^ b, mul(c, point) ^ d
    return divide(numerator, denominator) if denominator else 16


def construct_input():
    start = time.monotonic()
    require(all(mul(a, power(a, 14)) == 1 for a in range(1, 16)), 'invalid field')
    line = [a for a in range(16) if power(a, 4) == a] + [16]
    require(len(line) == 5, 'wrong subfield')
    circles, matrices = set(), 0
    for a, b, c, d in product(range(16), repeat=4):
        if not mul(a, d) ^ mul(b, c):
            continue
        if next(t for t in (a, b, c, d) if t) != 1:
            continue
        matrices += 1
        circles.add(mask(projective_image(a, b, c, d, p) for p in line))
    require(matrices == 4080 and len(circles) == 68, 'wrong classical design')
    generators = [[p ^ 1 for p in range(16)] + [16],
                  [mul(2, p) for p in range(16)] + [16],
                  [16] + [divide(1, p) for p in range(1, 16)] + [0],
                  [mul(p, p) for p in range(16)] + [16]]
    require(all(sorted(p) == list(range(17))
                and {move(c, p) for c in circles} == circles for p in generators),
            'generator does not preserve design')
    guard(start)
    return {'design_circles': sorted(circles), 'root_word': 15,
            'actual_transport_generators': generators,
            'sharp_four_parts': [15, 240, 6161, 9249, 16914, 98561]}


def compact_manifest(data):
    return {'input_sha256': digest(data['input']),
            'noncontained_words': len(data['noncontained']),
            'noncontained_sha256': digest(data['noncontained']),
            'root_transport_orbit': len(data['orbit']),
            'root_transport_sha256': digest(data['orbit']),
            'root_partners': len(data['partners']), 'root_partners_sha256': digest(data['partners']),
            'root_partner_edges': len(data['edges']), 'root_edges_sha256': digest(data['edges']),
            'root_degree_four_frames': len(data['frames']), 'root_frames_sha256': digest(data['frames']),
            'frame_gap_histogram': data['frame_gap_histogram'],
            'frame_degree_histogram': data['frame_degree_histogram'],
            'gap_at_most13_families': len(data['negative_carrier']),
            'negative_carrier_sha256': digest(data['negative_carrier']),
            'sharp_gap_cost': data['sharp_gap_cost'], 'sharp_gaps': data['sharp_gaps'],
            'sharp_code_size': len(data['sharp_code']), 'sharp_code_sha256': digest(data['sharp_code'])}
