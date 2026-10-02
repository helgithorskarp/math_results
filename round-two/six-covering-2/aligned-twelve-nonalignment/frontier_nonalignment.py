"""Complete phase controls; nonextendibility requires the separate tree proof."""
from collections import Counter
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import json
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'aligned-twelve-fourteen-presence'))
from frontier_fourteen import REMOVED as PREVIOUS_REMOVED
from normal_forms import N, MODULI, FORMS, normalize

ROOT = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 4))
REMOVED = tuple(form for form in FORMS if form in PREVIOUS_REMOVED or form == ROOT)
REMAINING = tuple(form for form in FORMS if form not in REMOVED)
THEOREM_FORMS = tuple(((8, 0), (9, 0), (10, b), (14, c), (12, d))
                      for b in (0, 1) for c in (0, 1) for d in (0, 4))


def crt(coordinates):
    return sum(a * (N // q) * pow(N // q, -1, q)
               for q, a in zip((32, 9, 5, 7), coordinates)) % N


def explicit_new_map(phases):
    """Independent affine map for the new intrinsic physical phase pattern."""
    a8, a9, a10, a14, a12 = phases
    if not ((a10 - a8) % 2 == 1 and (a14 - a8) % 2 == 1
            and (a12 - a8) % 4 == 0 and (a12 - a9) % 3 != 0):
        raise ValueError('Outside the new phase pattern')
    u3 = pow((a12 - a9) % 3, -1, 3)
    u = crt((1, u3, 1, 1))
    v = crt((-a8, -u3 * a9, 1 - a10, 1 - a14))
    if gcd(u, N) != 1 or tuple((m, (u * a + v) % m)
                               for m, a in zip(MODULI, phases)) != ROOT:
        raise ValueError('Explicit unit map fails')
    return u, v


def controls():
    counts = Counter()
    new_count = previous_count = combined_count = theorem_count = 0
    digest = sha256()
    for phases in product(*(range(m) for m in MODULI)):
        image, u, v = normalize(phases)
        counts[image] += 1
        a8, a9, a10, a14, a12 = phases
        new_pattern = ((a10 - a8) % 2 == 1 and (a14 - a8) % 2 == 1
                       and (a12 - a8) % 4 == 0 and (a12 - a9) % 3 != 0)
        theorem_pattern = (a12 - a8) % 4 == 0
        if (image == ROOT) != new_pattern:
            raise ValueError('New form and intrinsic pattern differ')
        if (image in THEOREM_FORMS) != theorem_pattern:
            raise ValueError('Eight theorem forms and physical pattern differ')
        if theorem_pattern and image not in REMOVED:
            raise ValueError('Original12 nonalignment theorem has an unexcluded phase form')
        if new_pattern:
            uu, vv = explicit_new_map(phases)
            digest.update(json.dumps([phases, uu, vv], separators=(',', ':')).encode())
        new_count += new_pattern
        theorem_count += theorem_pattern
        previous_count += image in PREVIOUS_REMOVED
        combined_count += image in REMOVED
    if (sum(counts.values()), set(counts), new_count, previous_count,
            combined_count, theorem_count, len(REMOVED), len(REMAINING)) != (
            120960, set(FORMS), 5040, 45360, 50400, 30240, 13, 11):
        raise ValueError('Complete affine frontier changed')
    if ROOT in PREVIOUS_REMOVED or not set(THEOREM_FORMS) <= set(REMOVED):
        raise ValueError('Wrong credited or newly removed forms')
    return {'period': N, 'physical_phase_tuples': sum(counts.values()),
            'new_removed_forms': 1, 'new_removed_tuples': new_count,
            'credited_removed_tuples': previous_count,
            'combined_removed_forms': len(REMOVED), 'combined_removed_tuples': combined_count,
            'remaining_forms': len(REMAINING), 'theorem_pattern_forms': len(THEOREM_FORMS),
            'theorem_pattern_tuples': theorem_count,
            'explicit_new_map_sha256': digest.hexdigest(),
            'form_counts': [[[[m, a] for m, a in form], counts[form]] for form in FORMS],
            'remaining_prefixes': [[list(pair) for pair in form] for form in REMAINING]}


if __name__ == '__main__':
    print(json.dumps({'status': 'Phase controls only; new exclusion needs complete tree replay',
                      'controls': controls()}, sort_keys=True))
