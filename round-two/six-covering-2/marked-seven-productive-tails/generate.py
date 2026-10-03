"""Bounded raw-phase BASE pilot; incomplete work is not an exclusion."""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import time

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 10), (28, 4))


def run():
    start = time.monotonic()
    points = [x for x in range(2520) if all(x % m != a for m, a in PREFIX)]
    labels = [m for m in range(8, 2521) if 2520 % m == 0 and m not in dict(PREFIX)]
    actions = {}
    for m in labels:
        phases = [0] * m
        for i, x in enumerate(points):
            phases[x % m] |= 1 << i
        actions[m] = phases
    full = (1 << len(points)) - 1
    cutoff = len(points) - 120
    result = {'agent': 'six-covering-2', 'role': 'researcher',
              'original_BASE_prefix': PREFIX, 'period': 2520,
              'initial_holes': len(points), 'free_original_labels': labels,
              'raw_free_phase_count': sum(labels), 'stable_covered_cutoff': cutoff,
              'soft_seconds': 18, 'retained_cap': 300, 'stages': [],
              'complete': False, 'universal_BASE_121_bound': False,
              'full_cover_excluded': False, 'global_bound_changed': False}
    retained = [((), 0)]
    fixed = []
    for new in ((15, 18), (24,), (36,)):
        rows = []
        next_retained = []
        fixed.extend(new)
        remaining = [m for m in labels if m not in fixed]
        stage = {'fixed_originals': list(fixed), 'remaining_originals': remaining,
                 'expected_rows': len(retained) * __import__('math').prod(new),
                 'rows': rows, 'complete': False}
        result['stages'].append(stage)
        for previous, old_union in retained:
            for phases in product(*(range(m) for m in new)):
                if time.monotonic() - start > 18:
                    result['stop'] = 'Soft time cap; no exclusion'
                    result['seconds'] = time.monotonic() - start
                    return result
                union = old_union
                for m, a in zip(new, phases, strict=True):
                    union |= actions[m][a]
                uncovered = full ^ union
                marginals = [max((mask & uncovered).bit_count() for mask in actions[m])
                             for m in remaining]
                covered = union.bit_count()
                bound = covered + sum(marginals)
                actual = previous + phases
                rows.append([list(actual), covered, marginals, bound])
                if bound >= cutoff:
                    next_retained.append((actual, union))
        if len(rows) != stage['expected_rows']:
            raise ValueError('Incomplete actual raw-phase frontier')
        stage['complete'] = True
        stage['retained_phases'] = [list(phases) for phases, union in next_retained]
        stage['upper_bound_range'] = [min(row[-1] for row in rows),
                                      max(row[-1] for row in rows)] if rows else None
        stage['rows_sha256'] = hashlib.sha256(json.dumps(rows,
            separators=(',', ':')).encode()).hexdigest()
        if not next_retained:
            result['complete'] = True
            result['universal_BASE_121_bound'] = True
            result['stop'] = 'Entire stable-cutoff raw-phase frontier empty'
            break
        if len(next_retained) > 300:
            result['stop'] = 'Retained-frontier cap; no exclusion'
            break
        retained = next_retained
    else:
        result['complete'] = True
        result['stop'] = 'Complete stages retain possibilities; no exclusion'
    result['seconds'] = time.monotonic() - start
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    record = run()
    Path(args.out).write_text(json.dumps(record, indent=2) + '\n')
    summary = {k: v for k, v in record.items() if k != 'stages'}
    summary['stages'] = [{k: v for k, v in stage.items() if k != 'rows'}
                         for stage in record['stages']]
    print(json.dumps(summary, indent=2))
