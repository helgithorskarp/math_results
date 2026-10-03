"""Bounded sufficient original3+3 constant-S7 selector, not an exact suffix solver.

An inconclusive selected-domain mass is unresolved. Imports published9007's
nested mechanism and knownS7>=16, using credited packed9590 primitives.
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
PUBLIC = ROOT
OUT = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start+45
    catalogue_mode = sys.argv[1] == 'catalogue'
    if catalogue_mode:
        branch = 1
        first, last = map(int, sys.argv[2:4])
        need(0 <= first < last and last-first <= 1000, 'Require at most1000 representative targets')
    else:
        branch, first, last = map(int, sys.argv[1:4])
    source = PUBLIC / 'prior'
    manifest = json.loads((source / 'source-manifest.json').read_text())
    pins = {r['path']: r['sha256'] for r in manifest['files']}
    for name in ('pruning.py', 'profile.py', 'fixture.json'):
        need(hashlib.sha256((source / name).read_bytes()).hexdigest() == pins[name], 'Credited packed source changed')
    pruning = load('disjoint_published_packed_pruning', source / 'pruning.py')
    profile = load('disjoint_published_packed_profile', source / 'profile.py')
    fixture = json.loads((source / 'fixture.json').read_text())
    pool = fixture['selected_original_pool']
    need(len(pool) == len({tuple(p) for p in pool}) == 99, 'Selected original proposal pool differs')
    if catalogue_mode:
        catalogue = json.loads((OUT / 'branch01-catalogue.json').read_text())
        normal = json.loads((OUT / 'branch01-catalogue-checked.json').read_text())
        optimized = json.loads((OUT / 'branch01-catalogue-checked-O.json').read_text())
        need(normal['finite'] == optimized['finite'] and normal['finite']['producer_quotient_sha256'] ==
             catalogue['finite_sha256'] and digest(catalogue['representatives']) ==
             catalogue['finite']['representatives_sha256'] and last <= len(catalogue['representatives']),
             'Whole physical catalogue not verified normal/O')
        front = {'survivors': catalogue['representatives'], 'finite_sha256': catalogue['finite_sha256']}
        selected = [{'front_index': i, 'prefix_sha256': front['survivors'][i]['prefix_sha256']}
                    for i in range(first, last)]
    else:
        front = json.loads((OUT / f'fronts{branch:02}-{first:05}-{last:05}.json').read_text())
        kernels = json.loads((OUT / f'kernels{branch:02}-{first:05}-{last:05}.json').read_text())
        need(kernels['finite']['producer_front_sha256'] == front['finite_sha256'], 'Kernel classification front binding differs')
        selected = [r for r in kernels['classifications'] if r['status'].startswith('NO_IMPORTED')]
    cases, counts = [], Counter()
    for row in selected:
        need(time.monotonic() < deadline, 'Incomplete45s sufficient bound selector: no exclusion')
        if len(cases) % 32 == 0:
            operations_allow()
        record = front['survivors'][row['front_index']]
        need(record['prefix_sha256'] == row['prefix_sha256'], 'Residual front binding differs')
        classes = {}
        for low, high in pool:
            p = pruning.pruning(record['prefix'], low, high, profile)
            original = p['outer_record']
            label = original[4]+original[5]+16
            key = tuple(original[2:4])
            candidate = {'original_LOW_mask': low, 'original_HIGH_mask': high, 'outer_record': original,
                         'retained_Q_sha256': digest(p['retained_prefix']), 'B7': 16, 'label': label}
            if key not in classes or label > classes[key]['label']:
                classes[key] = candidate
        witnesses, mass = [], 0
        for witness in sorted(classes.values(), key=lambda x: (-x['label'], x['outer_record'][2:4])):
            witnesses.append(witness)
            mass += 1 << witness['label']
            if mass > 1 << 44:
                break
        closed = mass > 1 << 44
        counts['fronts_tested'] += 1
        counts['constant16_exclusion_proposals' if closed else 'constant16_inconclusive'] += 1
        counts['selected_original_outer_occurrences'] += len(witnesses)
        cases.append({'branch_index': branch, 'front_index': row['front_index'],
                      'prefix_sha256': record['prefix_sha256'], 'nine_core_sha256': record['nine_core_sha256'],
                      'whole99_class_mass': sum(1 << w['label'] for w in classes.values()),
                      'constant16_exceeds44': closed, 'selected_mass': mass, 'selected_witnesses': witnesses})
    finite = {'branch_index': branch, 'retained_interval': [first, last], 'census': dict(counts),
              'cases_sha256': digest(cases), 'producer_front_sha256': front['finite_sha256'],
              'kernel_classifications_sha256': None if catalogue_mode else kernels['finite']['classifications_sha256'],
              'inconclusive_front_indices': [r['front_index'] for r in cases if not r['constant16_exceeds44']]}
    if catalogue_mode:
        del finite['retained_interval']
        finite['catalogue_slice'] = [first, last]
        finite['target_kind'] = 'COMPLETE_PHYSICAL_IMAGE_MAXIMUM_BUDGET_REPRESENTATIVES'
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'BOUNDED_CONSTANT16_PROPOSALS_NEED_SCALAR_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'cases': cases, 'cases_sha256': finite['cases_sha256'],
              'seconds': time.monotonic()-start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Only listed sufficient nested inequalities; inconclusive front indices remain open.'}
    prefix = 'constant-catalogue' if catalogue_mode else 'constant'
    (OUT / f'{prefix}{branch:02}-{first:05}-{last:05}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
