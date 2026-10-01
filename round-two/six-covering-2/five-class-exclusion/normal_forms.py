"""Complete affine five-class reduction for period10080; standard library only."""
from collections import Counter
from itertools import product
from math import gcd

N = 10080
MODULI = (8, 9, 10, 14, 12)
EXCLUDED = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 3))
FORMS = tuple(((8, 0), (9, 0), (10, b), (14, c), (12, d))
              for b, c, d in product((0, 1), (0, 1), (0, 4, 6, 10, 3, 7)))


def crt(values):
    periods = (32, 9, 5, 7)
    return sum(a * (N // q) * pow(N // q, -1, q)
               for a, q in zip(values, periods)) % N


def normalize(phases):
    if len(phases) != len(MODULI) or any(type(a) is not int or not 0 <= a < m
                                        for a, m in zip(phases, MODULI)):
        raise ValueError('Invalid prescribed phase')
    a8, a9, a10, a14, a12 = phases
    delta4, delta3 = (a12 - a8) % 4, (a12 - a9) % 3
    u2 = 1 if delta4 % 2 == 0 else 3 * pow(delta4, -1, 4) % 4
    u3 = 1 if delta3 == 0 else pow(delta3, -1, 3)
    b, c = (a10 - a8) % 2, (a14 - a8) % 2
    u = crt((u2, u3, 1, 1))
    v = crt((-u2 * a8, -u3 * a9, b - a10, c - a14))
    if gcd(u, N) != 1:
        raise ValueError('Affine multiplier is not a unit')
    image = tuple((m, (u * a + v) % m) for a, m in zip(phases, MODULI))
    if image not in FORMS:
        raise ValueError('Affine image lies outside the complete form list')
    return image, u, v


def controls():
    counts = Counter()
    literal = []
    samples = ((0, 0, 1, 1, 3), (7, 8, 8, 12, 2), (3, 1, 4, 2, 9))
    for phases in product(*(range(m) for m in MODULI)):
        image, u, v = normalize(phases)
        counts[image] += 1
        a8, a9, a10, a14, a12 = phases
        forbidden = all((a - a8) % 2 == 1 for a in (a10, a14, a12)) and (a12 - a9) % 3 == 0
        if (image == EXCLUDED) != forbidden:
            raise ValueError('Intrinsic forbidden pattern and normal form differ')
        if phases in samples:
            perm = [(u * x + v) % N for x in range(N)]
            if set(perm) != set(range(N)):
                raise ValueError('Literal affine map is not bijective')
            for a, (m, b) in zip(phases, image):
                if {perm[x] for x in range(a, N, m)} != set(range(b, N, m)):
                    raise ValueError('Literal affine cylinder mismatch')
            literal.append(phases)
    if sum(counts.values()) != 120960 or set(counts) != set(FORMS):
        raise ValueError('Finite form enumeration changed')
    if counts[EXCLUDED] != 5040 or len(literal) != 3:
        raise ValueError('Forbidden-pattern controls changed')
    rejected = 0
    for phases in ((8, 0, 1, 1, 3), (0, 0, 1, 1), (0, 0, True, 1, 3)):
        try:
            normalize(phases)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed phase input accepted')
    return {'raw_phase_tuples': sum(counts.values()), 'normal_forms': len(counts),
            'excluded_raw_tuples': counts[EXCLUDED], 'remaining_forms': 23,
            'literal_period_maps': len(literal), 'rejected_inputs': rejected,
            'form_counts': [[[[m, a] for m, a in form], counts[form]] for form in FORMS]}


def check_application(state):
    """Check the compact literal handoff; this is not an exclusion certificate."""
    root = ((8, 0), (9, 0), (10, 0), (14, 0), (12, 0))
    if (state['period'], state['minimum'], tuple(map(tuple, state['anchors']))) != (N, 8, root):
        raise ValueError('Wrong application root')
    remaining = [m for m in range(8, N + 1) if N % m == 0 and m not in dict(root)]
    if state['available_moduli'] != remaining:
        raise ValueError('Application resource set is incomplete')
    mask = int(state['residual_hex'], 16)
    if mask < 0 or mask >> N:
        raise ValueError('Application residue mask outside period')
    points = [x for x in range(N) if all(x % m != a for m, a in root)]
    if {x for x in range(N) if mask >> x & 1} != set(points):
        raise ValueError('Application literal residual differs')
    if state['residual_count'] != len(points):
        raise ValueError('Application residual count differs')
    if state['four_top_resources'] != [288, 1440, 2016, 10080] or state['prescribed_top_phases']:
        raise ValueError('Application top phases differ')
    if any(m not in remaining for m in state['four_top_resources']):
        raise ValueError('Application top resource is already prescribed')
    return {'residual': len(points), 'resources': len(remaining), 'prescribed_top_phases': 0}


if __name__ == '__main__':
    import json
    print(json.dumps(controls(), sort_keys=True))
