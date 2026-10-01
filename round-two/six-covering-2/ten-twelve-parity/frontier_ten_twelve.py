"""Complete affine phase counts; nonextendibility is supplied separately."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT / 'exceptional-phase-alignment'))
from frontier_alignment import REMOVED as PREVIOUS_REMOVED
from normal_forms import N, MODULI, FORMS, normalize

PHASES = (10,)
NEW_FORMS = tuple(((8, 0), (9, 0), (10, 0), (14, 1), (12, d))
                  for d in PHASES)
THEOREM_FORMS = tuple(((8, 0), (9, 0), (10, 0), (14, c), (12, d))
                      for c in (0, 1) for d in (0, 4, 6, 10))
REMOVED = tuple(form for form in FORMS
                if form in PREVIOUS_REMOVED or form in NEW_FORMS)
REMAINING = tuple(form for form in FORMS if form not in REMOVED)


def controls():
    counts = Counter()
    new_tuples = theorem_tuples = combined_tuples = 0
    for phases in product(*(range(m) for m in MODULI)):
        image, u, v = normalize(phases)
        counts[image] += 1
        a8, a9, a10, a14, a12 = phases
        same_ten_twelve = (a10-a8) % 2 == 0 and (a12-a8) % 2 == 0
        twelve_pattern = (a12-a8) % 4 == 0 and (a12-a9) % 3 == 0
        parity_pattern = all((a-a8) % 2 == 0 for a in (a10, a14, a12))
        old_pattern = (all((a-a8) % 2 == 1 for a in (a10, a14, a12))
                       and (a12-a9) % 3 == 0)
        alignment_pattern = (same_ten_twelve and (a14-a8) % 2 == 1
                             and (((a12-a8) % 4 == 0 and (a12-a9) % 3 != 0)
                                  or ((a12-a8) % 4 == 2 and (a12-a9) % 3 == 0)))
        previous_pattern = twelve_pattern or parity_pattern or old_pattern or alignment_pattern
        if (image in THEOREM_FORMS) != same_ten_twelve:
            raise ValueError('Ten/twelve parity pattern and its eight forms differ')
        if (image in NEW_FORMS) != (same_ten_twelve and not previous_pattern):
            raise ValueError('The additional exceptional cell differs from its pattern')
        if (image in REMOVED) != (same_ten_twelve or previous_pattern):
            raise ValueError('Combined forbidden phase patterns differ')
        theorem_tuples += same_ten_twelve
        new_tuples += image in NEW_FORMS
        combined_tuples += image in REMOVED
    if (sum(counts.values()), set(counts), theorem_tuples, new_tuples,
            combined_tuples, len(REMOVED), len(REMAINING)) != (
            120960, set(FORMS), 30240, 5040, 40320, 11, 13):
        raise ValueError('Conditional affine frontier changed')
    return {'period': N, 'physical_phase_tuples': sum(counts.values()),
            'theorem_pattern_forms': len(THEOREM_FORMS),
            'theorem_pattern_tuples': theorem_tuples,
            'new_removed_forms': len(NEW_FORMS), 'new_removed_tuples': new_tuples,
            'combined_removed_forms': len(REMOVED),
            'combined_removed_tuples': combined_tuples,
            'remaining_forms': len(REMAINING),
            'form_counts': [[[[m, a] for m, a in form], counts[form]] for form in FORMS],
            'remaining_prefixes': [[list(pair) for pair in form] for form in REMAINING]}


if __name__ == '__main__':
    import json
    print(json.dumps({'status': 'Phase counts only;13 forms require complete new root replays plus credited8837/8963',
                      'phase_controls': controls()}, sort_keys=True))
