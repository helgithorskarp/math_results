"""Exact transport and containment controls, without a covering exclusion.

The missing mathematical premise is a complete literal replay of root
[(8,0),(9,0),(10,0),(14,1),(12,10),(16,4),(20,1)].
"""
import hashlib
import json

N = 10080
R = ((8, 0), (9, 0), (10, 0), (14, 1), (12, 10), (16, 4))
AXES = (32, 9, 5, 7)


def need(test, message):
    if not test:
        raise ValueError(message)


def crt(values):
    return sum(a * (N // q) * pow(N // q, -1, q)
               for a, q in zip(values, AXES)) % N


def positive_transport(a):
    need(type(a) is int and 0 <= a < 20 and a not in (0, 10),
         'Phase is outside the positive twenty family')
    r = (1 if a % 5 else 5) if a % 2 else (2 if a % 4 else 4)
    maps = [list(range(q)) for q in AXES]
    if a % 2 and a % 4 == 3:
        maps[0] = [x ^ 2 if x % 2 else x for x in range(32)]
    b, c = a % 5, r % 5
    maps[2][c], maps[2][b] = maps[2][b], maps[2][c]
    return r, maps


def check():
    divisors = [n for n in range(1, N + 1) if N % n == 0]
    excluded_phases = [a for a in range(20) if a % 2 and a % 5]
    digest = hashlib.sha256()
    points = families = 0
    transports = []
    counts = {}
    for a in range(20):
        if a in (0, 10):
            continue
        representative, maps = positive_transport(a)
        counts[representative] = counts.get(representative, 0) + 1
        for q, mapping in zip(AXES, maps):
            need(set(mapping) == set(range(q)), 'Coordinate is not bijective')
        perm = [crt([mapping[x % q] for q, mapping in zip(AXES, maps)])
                for x in range(N)]
        need(set(perm) == set(range(N)), 'Physical map is not bijective')
        for n in divisors:
            phase_map = [perm[b] % n for b in range(n)]
            need(len(set(phase_map)) == n, 'Divisor phase map is not bijective')
            need(all(perm[x] % n == phase_map[x % n] for x in range(N)),
                 'A divisor cylinder family is not preserved')
            families += 1
        for x, y in enumerate(perm):
            need(all((x % n == b) == (y % n == b) for n, b in R),
                 'Known prescribed class moved')
            need((x % 20 == a) == (y % 20 == representative),
                 'Twenty class did not map to its representative')
            points += 1
        digest.update(json.dumps([a, representative, perm], separators=(',', ':')).encode())
        transports.append({'phase': a, 'representative': representative,
                           'binary_odd_second_digit_toggle': a % 4 == 3,
                           'five_coordinate_swap': [a % 5, representative % 5]})
    need(counts == {1: 8, 2: 4, 4: 4, 5: 2}, 'Incomplete phase partition')
    redundant = [a for a in range(20)
                 if set(range(a, N, 20)) <= set(range(0, N, 10))]
    need(redundant == [0, 10], 'Incorrect redundant twenty phases')
    allowed = [a for a in range(20) if a not in redundant + excluded_phases]
    need(allowed == [2, 4, 5, 6, 8, 12, 14, 15, 16, 18],
         'Incorrect conditional allowed family')
    need(all((bool(a % 2)) == (a % 5 == 0) for a in allowed),
         'Conditional phase relation fails')
    containment_controls = 0
    for a in range(20):
        need(set(range(a, N, 20)) <= set(range(a % 10, N, 10)),
             'Twenty class not contained in its ten projection')
        containment_controls += 1
    return {
        'agent': 'six-covering-2', 'role': 'researcher', 'period': N,
        'fixed_root': R, 'literal_divisors': len(divisors),
        'positive_twenty_transports': transports,
        'representative_phase_counts': counts,
        'physical_point_controls': points, 'divisor_family_controls': families,
        'ordered_permutations_sha256': digest.hexdigest(),
        'twenty_to_ten_containment_controls': containment_controls,
        'twenty_phases_redundant_in_ten_zero': redundant,
        'conditional_allowed_twenty_phases': allowed,
        'remaining_canonical_twenty_phases': [2, 4, 5],
        'scope': 'Transport and containment only. Nonextendibility requires the separate complete root certificate.',
    }


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
