#!/usr/bin/env python3
"""Propose the exact F103 thirteen-core cut census. No solver or exclusion."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

Q = 103


def need(condition, message):
    if not condition:
        raise ValueError(message)


def representatives():
    def orbit(x):
        return {x, (1-x) % Q, pow(x, -1, Q), pow((1-x) % Q, -1, Q),
                x * pow((x-1) % Q, -1, Q) % Q,
                (x-1) * pow(x, -1, Q) % Q}
    return sorted({min(orbit(x)) for x in range(2, Q)})


def transcript(rows):
    digest = hashlib.sha256()
    for row in rows:
        digest.update((json.dumps(row, separators=(',', ':'), sort_keys=True) + '\n').encode())
    return digest.hexdigest()


def generate():
    pattern = frozenset(x % Q for x in range(-2, 7)) | frozenset(j * pow(2, -1, Q) % Q for j in (1, 3, 5, 7))
    seed_pattern = range(5)
    need(len(pattern) == 13, 'Collapsed thirteen-point pattern')
    field_sevens = {tuple(sorted((p + j*r) % Q for j in range(7)))
                    for r in range(1, 52) for p in range(Q)}
    template = sorted(s for s in field_sevens if set(s) <= pattern)
    need(len(field_sevens) == 5253 and len(template) == 6, 'Unexpected field-seven template')
    result = {'agent': 'six-vdw-3', 'role': 'researcher', 'q': Q,
              'pattern': sorted(pattern), 'field_sevens_in_pattern': [list(s) for s in template],
              'representatives': representatives(), 'classes': [],
              'full_cyclic_exclusion_claimed': False, 'W_bound_improved': False}
    for lam in result['representatives']:
        holes = {0, 1, lam}
        records = {}
        eligible = 0
        for slope in range(1, 52):
            for start in range(Q):
                seed = tuple(sorted((start + j*slope) % Q for j in seed_pattern))
                if holes.intersection(seed):
                    continue
                eligible += 1
                core = tuple(sorted({(start + j*slope) % Q for j in pattern} - holes))
                available = [tuple(sorted((start + x*slope) % Q for x in support))
                             for support in template
                             if not holes.intersection((start + x*slope) % Q for x in support)]
                witness = min(available) if available else None
                row = {'core': list(core), 'seed': list(seed),
                       'field_seven_witness': list(witness) if witness is not None else None}
                if core in records:
                    need(records[core] == row, 'Core collision between distinct seed supports')
                records[core] = row
        ordered = [records[k] for k in sorted(records)]
        essential = [r for r in ordered if r['field_seven_witness'] is None]
        histogram = Counter(len(r['core']) for r in ordered)
        result['classes'].append({
            'lambda': lam, 'holes': sorted(holes), 'eligible_seed_supports': eligible,
            'distinct_regular_cores': len(ordered), 'locally_covered_cores': len(ordered) - len(essential),
            'cores_without_field_seven': len(essential),
            'core_size_histogram': {str(k): histogram[k] for k in sorted(histogram)},
            'all_core_rows_sha256': transcript(ordered), 'exceptional_cores': essential,
        })
    for key in ('eligible_seed_supports', 'distinct_regular_cores', 'locally_covered_cores', 'cores_without_field_seven'):
        result['total_' + key] = sum(c[key] for c in result['classes'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = generate()
    args.output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({k: v for k, v in data.items() if k not in ('classes','pattern','field_sevens_in_pattern')}))
