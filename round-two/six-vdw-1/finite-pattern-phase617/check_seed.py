"""Literal finite coloring decoder/checker; no model generator/auditor import."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(q, N, signed):
    need(q in [7, 617] and type(N) is int and 6 < N <= 3704,
         'chosen actual finite witness domain')
    chars = {x: sum((k*x) % q > q//2 for k in range(1, q//2+1)) % 2 for x in range(1, q)}
    root_positions = [n for n in range(N) if n % q in (0, 1, 4)]
    root_tags = {n: 49+i for i, n in enumerate(root_positions)}
    variables = 48+len(root_positions)
    values = {}
    for literal in signed:
        need(type(literal) is int and 1 <= abs(literal) <= variables,
             'actual independent color literal range')
        need(abs(literal) not in values, 'duplicate or contradictory actual color declaration')
        values[abs(literal)] = int(literal > 0)
    need(set(values) == set(range(1, variables+1)), 'all independent actual color bits assigned exactly once')
    colors = []
    for n in range(N):
        if n in root_tags:
            colors.append(values[root_tags[n]])
        else:
            r = n % q
            key = 4*chars[r]+2*chars[(r-1) % q]+chars[(r-4) % q]
            colors.append(values[key*6+n % 6+1])
    return colors, variables, root_positions


def verify(q, N, signed):
    colors, variables, root_positions = decode(q, N, signed)
    digest = hashlib.sha256()
    APs = points = 0
    for d in range(1, (N-1)//6+1):
        for a in range(N-6*d):
            ns = [a+j*d for j in range(7)]
            actual = [colors[n] for n in ns]
            need(len(set(actual)) == 2, 'actual monochromatic original integer AP:'+str([a, d, ns]))
            digest.update(struct.pack('<HH7B', a, d, *actual))
            APs += 1
            points += 7
    need(APs == sum(N-6*d for d in range(1, (N-1)//6+1)) and points == APs*7,
         'whole actual positive integer progression coverage')
    raw = bytes(colors)
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'EXACT_ORIGINAL_FINITE_COLORING_WITNESS_VERIFIED',
            'q': q, 'N': N, 'zero_interval': [0, N-1], 'variables': variables,
            'all_original_root_positions': root_positions, 'literal_integer_APs': APs,
            'literal_AP_points': points, 'whole_original_AP_color_stream_sha256': digest.hexdigest(),
            'whole_actual_coloring_sha256': hashlib.sha256(raw).hexdigest(),
            'root_occurrences_independently_colored': True, 'valid3704_coloring': N == 3704,
            'external_review_claimed': False}, colors



def seed_assignment(N):
    # The independent literal witness verifier uses Gauss symbols. This
    # control oracle uses an explicit set of squares, not Euler or Gauss.
    q = 617
    squares = {x*x % q for x in range(1, q)}
    free = [n for n in range(N) if n % q in [0, 1, 4]]
    colors = [int(n % q not in squares) if n % q else int(n == 3702) for n in range(N)]
    values = [k//4 for k in range(8) for s in range(6)]+[colors[n] for n in free]
    return [i+1 if b else -i-1 for i, b in enumerate(values)], colors


def verify_seed():
    signed, expected = seed_assignment(3703)
    seed, actual = verify(617, 3703, signed)
    need(actual == expected, 'whole literal historical3703 construction word')
    inverse, opposite = verify(617, 3703, [-x for x in signed])
    need(opposite == [1-c for c in expected], 'genuine historical palette complement')
    need(seed['literal_integer_APs'] == 1140833 and inverse['literal_integer_APs'] == 1140833,
         'complete historical positive AP domain, not a claimed new bound')
    damaged = signed[:]
    need(damaged[-1] == 67, 'actual historical exceptional root0 occurrence is variable67')
    damaged[-1] = -67
    try:
        verify(617, 3703, damaged)
    except ValueError as e:
        need(str(e) == 'actual monochromatic original integer AP:[0, 617, [0, 617, 1234, 1851, 2468, 3085, 3702]]',
             'actual root0 endpoint damage has intended vertical rejection')
        root_damage = str(e)
    else:
        raise ValueError('damaged historical root0 column accepted')
    try:
        verify(617, 3703, signed[:-1])
    except ValueError as e:
        need(str(e) == 'all independent actual color bits assigned exactly once', 'missing actual endpoint bit rejected')
        missing_damage = str(e)
    else:
        raise ValueError('missing actual endpoint bit accepted')
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'KNOWN3703_INDEPENDENT_LITERAL_POSITIVE_CONTROLS_PASS',
            'known_seed_positive_words': [seed, inverse], 'known_seed_is_new_bound': False,
            'historical_semantic_damage_rejections': [{'name': 'zeroed_actual_root0_endpoint', 'rejection': root_damage},
                                                       {'name': 'missing_actual_root0_endpoint', 'rejection': missing_damage}],
            'native_solver_used': False, 'valid3704_coloring': False,
            'external_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(verify_seed(), sort_keys=True))
