"""Complete phase reduction for the modulus-twelve necessity target."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'parity-class-exclusion'))
from frontier import REMOVED as PREVIOUS_REMOVED
from normal_forms import N, MODULI, FORMS, normalize

TWELVE_FORMS = tuple(((8,0),(9,0),(10,b),(14,c),(12,0))
                     for b,c in product((0,1),repeat=2))
NEW_FORMS = tuple(form for form in TWELVE_FORMS if form not in PREVIOUS_REMOVED)
REMOVED = tuple(form for form in FORMS if form in PREVIOUS_REMOVED or form in TWELVE_FORMS)
REMAINING = tuple(form for form in FORMS if form not in REMOVED)


def controls():
    counts = Counter()
    twelve_tuples = combined_tuples = 0
    for phases in product(*(range(m) for m in MODULI)):
        image,u,v = normalize(phases)
        counts[image] += 1
        a8,a9,a10,a14,a12 = phases
        twelve_pattern = (a12-a8)%4==0 and (a12-a9)%3==0
        parity_pattern = all((a-a8)%2==0 for a in (a10,a14,a12))
        old_pattern = (all((a-a8)%2==1 for a in (a10,a14,a12))
                       and (a12-a9)%3==0)
        if (image in TWELVE_FORMS) != twelve_pattern:
            raise ValueError('Twelve pattern and normal forms differ')
        if (image in REMOVED) != (twelve_pattern or parity_pattern or old_pattern):
            raise ValueError('Combined forbidden patterns differ')
        twelve_tuples += twelve_pattern
        combined_tuples += twelve_pattern or parity_pattern or old_pattern
    if (sum(counts.values()),set(counts),twelve_tuples,combined_tuples,
            len(NEW_FORMS),len(REMOVED),len(REMAINING)) != (120960,set(FORMS),10080,27720,3,8,16):
        raise ValueError('Complete modulus-twelve frontier changed')
    return {'period':N,'physical_phase_tuples':sum(counts.values()),
            'twelve_pattern_forms':len(TWELVE_FORMS),'twelve_pattern_tuples':twelve_tuples,
            'new_removed_forms':len(NEW_FORMS),'new_removed_tuples':7560,
            'combined_removed_forms':len(REMOVED),'combined_removed_tuples':combined_tuples,
            'remaining_forms':len(REMAINING),
            'form_counts':[[[[m,a] for m,a in form],counts[form]] for form in FORMS],
            'remaining_prefixes':[[list(pair) for pair in form] for form in REMAINING]}


if __name__=='__main__':
    import json
    print(json.dumps(controls(),sort_keys=True))
