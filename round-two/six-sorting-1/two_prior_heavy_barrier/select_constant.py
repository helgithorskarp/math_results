"""Bounded exact constant-S7 selected-outer pilot on one heavy route.

Reuse credited published pruning/profile primitives; no inner anchors here.
An inconclusive bound or partial stage remains unresolved. Source arrays private.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    branch = int(sys.argv[1])
    source = ROOT/'prior'
    pruning = load('two_prior_published_packed_pruning', source/'pruning.py')
    profile = load('two_prior_published_profile', source/'profile.py')
    fixture = json.loads((source/'fixture.json').read_text())
    pool = fixture['selected_original_pool']
    need(len(pool) == 99 and len({tuple(p) for p in pool}) == 99, 'Original proposal pool differs')
    inheritance = json.loads((ROOT/'work/two-prior-heavy-inherited-obstructions.json').read_text())
    intake = json.loads((ROOT/f'work/heavy-fronts{branch:02}.json').read_text())
    selected = [r for r in inheritance['classifications']
                if r['branch_index'] == branch and r['status'].startswith('NO_PUBLISHED')]
    cases = []
    counts = Counter()
    for r in selected:
        need(time.monotonic() < deadline, 'Incomplete45s constant pilot; not an exclusion')
        if len(cases) % 32 == 0:
            operations_allow()
        front = intake['survivors'][r['front_index']]
        need(front['prefix_sha256'] == r['prefix_sha256'], 'Residual target binding differs')
        classes = {}
        for lo, hi in pool:
            p = pruning.pruning(front['prefix'], lo, hi, profile)
            record = p['outer_record']
            label = record[4] + record[5] + 16
            key = tuple(record[2:4])
            candidate = {'original_LOW_mask': lo, 'original_HIGH_mask': hi,
                         'outer_record': record, 'retained_Q_sha256': digest(p['retained_prefix']),
                         'B7': 16, 'label': label}
            if key not in classes or label > classes[key]['label']:
                classes[key] = candidate
        witnesses = []
        mass = 0
        for row in sorted(classes.values(), key=lambda t: (-t['label'], t['outer_record'][2:4])):
            witnesses.append(row)
            mass += 1 << row['label']
            if mass > 1 << 44:
                break
        closed = mass > 1 << 44
        counts['fronts_tested'] += 1
        counts['constant16_sufficient_exclusion_proposals' if closed else 'constant16_inconclusive'] += 1
        counts['selected_original_outer_occurrences'] += len(witnesses)
        cases.append({'branch_index': branch, 'front_index': r['front_index'],
                      'prefix_sha256': front['prefix_sha256'], 'nine_core_sha256': front['nine_core_sha256'],
                      'whole99_class_mass': sum(1 << t['label'] for t in classes.values()),
                      'constant16_exceeds44': closed, 'selected_mass': mass,
                      'selected_witnesses': witnesses})
    finite = {'branch_index': branch, 'residual_intake_cases': len(selected), 'census': dict(counts),
              'cases_sha256': digest(cases),
              'inconclusive_front_indices': [r['front_index'] for r in cases if not r['constant16_exceeds44']]}
    out = {'agent': 'six-sorting-1', 'role': 'researcher',
           'status': 'COMPLETE_PRIVATE_CONSTANT16_PILOT_NEEDS_INDEPENDENT_ORIGINAL_CUBE_REPLAY',
           **finite, 'cases': cases, 'finite_sha256': digest(finite),
           'seconds': time.monotonic()-start,
           'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'scope': 'One heavy-route residual exact sufficient bound selector only; no inner anchors or complete branch exclusion asserted.'}
    (ROOT/f'work/residual-constant{branch:02}.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
