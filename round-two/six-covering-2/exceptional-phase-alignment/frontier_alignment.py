"""Complete finite phase controls; tree exclusions are checked separately."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'twelve-class-exclusion'))
from frontier_twelve import REMOVED as PREVIOUS_REMOVED
from normal_forms import N, MODULI, FORMS, normalize

NEW_FORMS = tuple(((8, 0), (9, 0), (10, 0), (14, 1), (12, d))
                  for d in (4, 6))
EXCEPTION = ((8, 0), (9, 0), (10, 0), (14, 1), (12, 10))
REMOVED = tuple(form for form in FORMS
                if form in PREVIOUS_REMOVED or form in NEW_FORMS)
REMAINING = tuple(form for form in FORMS if form not in REMOVED)


def controls():
    counts = Counter()
    new_tuples = combined_tuples = parity_domain_tuples = exception_tuples = 0
    for phases in product(*(range(m) for m in MODULI)):
        image, multiplier, offset = normalize(phases)
        counts[image] += 1
        a8, a9, a10, a14, a12 = phases
        same_ten_twelve = (a10-a8) % 2 == 0 and (a12-a8) % 2 == 0
        delta4, delta3 = (a12-a8) % 4, (a12-a9) % 3
        twelve_pattern = delta4 == 0 and delta3 == 0
        parity_pattern = all((a-a8) % 2 == 0 for a in (a10, a14, a12))
        old_pattern = (all((a-a8) % 2 == 1 for a in (a10, a14, a12))
                       and delta3 == 0)
        previous = twelve_pattern or parity_pattern or old_pattern
        new = (same_ten_twelve and (a14-a8) % 2 == 1 and
               ((delta4 == 0 and delta3 != 0) or (delta4 == 2 and delta3 == 0)))
        exceptional = (same_ten_twelve and (a14-a8) % 2 == 1
                       and delta4 == 2 and delta3 != 0)
        if (image in NEW_FORMS) != new:
            raise ValueError('New cells differ from their intrinsic phase patterns')
        if (image in REMOVED) != (previous or new):
            raise ValueError('Combined removed cells differ')
        if (same_ten_twelve and image not in REMOVED) != exceptional:
            raise ValueError('Unexcluded parity-domain phases differ from exception')
        if (image == EXCEPTION) != exceptional:
            raise ValueError('Exceptional alignment is not exactly the stated root')
        new_tuples += new
        combined_tuples += image in REMOVED
        parity_domain_tuples += same_ten_twelve
        exception_tuples += exceptional
    actual = (sum(counts.values()), set(counts), new_tuples, combined_tuples,
              parity_domain_tuples, exception_tuples, len(REMOVED), len(REMAINING))
    expected = (120960, set(FORMS), 7560, 35280, 30240, 5040, 10, 14)
    if actual != expected:
        raise ValueError('Complete affine frontier changed')
    return {'period': N, 'physical_phase_tuples': sum(counts.values()),
            'new_removed_forms': len(NEW_FORMS), 'new_removed_tuples': new_tuples,
            'combined_removed_forms': len(REMOVED),
            'combined_removed_tuples': combined_tuples,
            'remaining_forms': len(REMAINING),
            'common_ten_twelve_parity_tuples': parity_domain_tuples,
            'exceptional_tuples': exception_tuples,
            'exceptional_prefix': [list(pair) for pair in EXCEPTION],
            'form_counts': [[[[m, a] for m, a in form], counts[form]] for form in FORMS],
            'remaining_prefixes': [[list(pair) for pair in form] for form in REMAINING]}


if __name__ == '__main__':
    import json
    print(json.dumps(controls(), sort_keys=True))
