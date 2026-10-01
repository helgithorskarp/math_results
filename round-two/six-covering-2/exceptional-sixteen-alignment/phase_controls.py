"""Literal affine/phase controls; exclusions require separate complete trees."""
from collections import Counter
from itertools import product
from math import gcd
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'five-class-exclusion'))
from normal_forms import MODULI, normalize

N = 10080
E = ((8, 0), (9, 0), (10, 0), (14, 1), (12, 10))
NEW_ROOTS = tuple(E + ((16, a),) for a in (1, 2))
OPEN_ROOT = E + ((16, 4),)


def require(test, message):
    if not test:
        raise ValueError(message)


def crt(values):
    return sum(a * (N // q) * pow(N // q, -1, q)
               for a, q in zip(values, (32, 9, 5, 7))) % N


def controls():
    reps, maps = Counter(), []
    physical_points = 0
    for a in range(16):
        if a in (0, 8):
            require(set(range(a, N, 16)) <= set(range(0, N, 8)),
                    'Aligned sixteen is not contained in eight')
            continue
        representative = 1 if a % 2 else 2 if a % 4 else 4
        u2 = pow(a // representative, -1, 16 // representative)
        u = crt((u2, 1, 1, 1))
        require(gcd(u, N) == 1 and u * a % 16 == representative,
                'Invalid sixteen affine unit')
        require(all(u * b % n == b for n, b in E), 'Known phase not fixed')
        images = set()
        for x in range(N):
            y = u * x % N
            images.add(y)
            require(all((x % n == b) == (y % n == b) for n, b in E),
                    'Literal prescribed cylinder changed')
            require((x % 16 == a) == (y % 16 == representative),
                    'Literal sixteen cylinder changed')
            physical_points += 1
        require(images == set(range(N)), 'Physical affine map not bijective')
        reps[representative] += 1
        maps.append({'phase': a, 'representative': representative, 'unit': u})
    require(reps == {1: 8, 2: 4, 4: 2}, 'Incomplete sixteen partition')
    raw_five = exceptional_five = allowed_six = excluded_six = 0
    for phases in product(*(range(m) for m in MODULI)):
        image, u, v = normalize(phases)
        raw_five += 1
        a8, a9, a10, a14, a12 = phases
        exceptional = ((a10-a8) % 2 == 0 and (a14-a8) % 2 == 1
                       and (a12-a8) % 4 == 2 and (a12-a9) % 3 != 0)
        require((image == E) == exceptional, 'Exceptional physical pattern differs')
        if not exceptional:
            continue
        exceptional_five += 1
        for a16 in range(16):
            b16 = (u*a16+v) % 16
            allowed = (a16-a8) % 8 == 4
            require(allowed == (b16 in (4, 12)), 'Intrinsic sixteen difference differs')
            allowed_six += allowed
            excluded_six += not allowed
    require((raw_five, exceptional_five, allowed_six, excluded_six)
            == (120960, 5040, 10080, 70560), 'Complete phase counts changed')
    return {'agent': 'six-covering-2', 'role': 'researcher', 'period': N,
            'physical_five_phase_tuples': raw_five,
            'exceptional_five_tuples': exceptional_five,
            'exceptional_six_tuples': allowed_six + excluded_six,
            'allowed_six_tuples': allowed_six, 'excluded_six_tuples': excluded_six,
            'redundant_normalized_sixteen_phases': [0, 8],
            'representative_phase_counts': dict(sorted(reps.items())),
            'literal_affine_point_controls': physical_points,
            'positive_sixteen_transports': maps,
            'open_root': OPEN_ROOT,
            'scope': 'Counts/transports only; roots1/2 need literal exclusion; root4 remains open'}


def check_application(data):
    require((data['period'], data['minimum'], tuple(map(tuple, data['anchors'])))
            == (N, 8, OPEN_ROOT), 'Wrong open comparison domain')
    resources = [n for n in range(8, N+1) if N % n == 0 and n not in dict(OPEN_ROOT)]
    require(data['available_moduli'] == resources, 'Incomplete comparison resources')
    points = {x for x in range(N) if all(x % n != a for n, a in OPEN_ROOT)}
    mask = int(data['residual_hex'], 16)
    require(mask >= 0 and mask >> N == 0, 'Comparison support outside domain')
    require({x for x in range(N) if mask >> x & 1} == points
            and data['residual_count'] == len(points) == 5408, 'False comparison support')
    require(data['four_top_resources'] == [288, 1440, 2016, 10080]
            and not data['prescribed_top_phases']
            and all(n in resources for n in data['four_top_resources']), 'False comparison top resources')
    return {'residual': len(points), 'resources': len(resources), 'prescribed_top_phases': 0}


if __name__ == '__main__':
    import json
    print(json.dumps(controls(), sort_keys=True))
