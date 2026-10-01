"""Exact phase controls for the parity restriction at period 10080."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'five-class-exclusion'))
from normal_forms import N, MODULI, FORMS, EXCLUDED, normalize

PHASES = (0, 4, 6, 10)
EVEN_FORMS = tuple(((8, 0), (9, 0), (10, 0), (14, 0), (12, d))
                   for d in PHASES)
REMOVED = EVEN_FORMS + (EXCLUDED,)
REMAINING = tuple(form for form in FORMS if form not in REMOVED)
NEXT_FORM = ((8, 0), (9, 0), (10, 0), (14, 1), (12, 0))


def controls():
    """Check every physical phase tuple and the exact remaining form list."""
    counts = Counter()
    parity_tuples = combined_tuples = literal_maps = 0
    samples = ((7, 8, 1, 3, 5), (3, 1, 1, 9, 7), (0, 0, 0, 0, 10))
    for phases in product(*(range(m) for m in MODULI)):
        image, u, v = normalize(phases)
        counts[image] += 1
        a8, a9, a10, a14, a12 = phases
        same_parity = all((a - a8) % 2 == 0 for a in (a10, a14, a12))
        old_pattern = (all((a - a8) % 2 == 1 for a in (a10, a14, a12))
                       and (a12 - a9) % 3 == 0)
        if (image in EVEN_FORMS) != same_parity:
            raise ValueError('Parity pattern differs from the four normal forms')
        if (image == EXCLUDED) != old_pattern:
            raise ValueError('Previously excluded pattern changed')
        if (image in REMOVED) != (same_parity or old_pattern):
            raise ValueError('Combined forbidden patterns changed')
        parity_tuples += same_parity
        combined_tuples += same_parity or old_pattern
        if phases in samples:
            permutation = [(u * x + v) % N for x in range(N)]
            if set(permutation) != set(range(N)):
                raise ValueError('Whole-period affine map is not bijective')
            for a, (m, b) in zip(phases, image):
                if {permutation[x] for x in range(a, N, m)} != set(range(b, N, m)):
                    raise ValueError('Whole-period class image differs')
            literal_maps += 1
    if (sum(counts.values()), set(counts), parity_tuples, combined_tuples,
            len(REMAINING), literal_maps) != (120960, set(FORMS), 15120, 20160, 19, 3):
        raise ValueError('Complete phase frontier changed')
    return {'period': N, 'physical_phase_tuples': sum(counts.values()),
            'normal_forms': len(FORMS), 'new_removed_forms': len(EVEN_FORMS),
            'new_removed_physical_tuples': parity_tuples,
            'combined_removed_forms': len(REMOVED),
            'combined_removed_physical_tuples': combined_tuples,
            'remaining_forms': len(REMAINING), 'literal_period_maps': literal_maps,
            'form_counts': [[[[m, a] for m, a in form], counts[form]] for form in FORMS],
            'remaining_prefixes': [[list(pair) for pair in form] for form in REMAINING]}


def check_application(state):
    """Verify the next literal handoff; this is neither a cover nor an exclusion."""
    if (state['period'], state['minimum'], tuple(map(tuple, state['anchors']))) != (N, 8, NEXT_FORM):
        raise ValueError('Wrong next application root')
    if NEXT_FORM not in REMAINING:
        raise ValueError('Application root is already excluded')
    available = [m for m in range(8, N + 1) if N % m == 0 and m not in dict(NEXT_FORM)]
    if state['available_moduli'] != available:
        raise ValueError('Incomplete next application resource list')
    mask = int(state['residual_hex'], 16)
    if mask < 0 or mask >> N:
        raise ValueError('Application mask outside period')
    points = {x for x in range(N) if all(x % m != a for m, a in NEXT_FORM)}
    if {x for x in range(N) if mask >> x & 1} != points or state['residual_count'] != len(points):
        raise ValueError('Application literal residual differs')
    if state['four_top_resources'] != [288, 1440, 2016, 10080] or state['prescribed_top_phases']:
        raise ValueError('Application top phases differ')
    if any(m not in available for m in state['four_top_resources']):
        raise ValueError('Application top resource is already used')
    return {'residual': len(points), 'resources': len(available), 'prescribed_top_phases': 0}


if __name__ == '__main__':
    import json
    print(json.dumps(controls(), sort_keys=True))
