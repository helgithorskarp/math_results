"""Separate scalar original128-input and oriented-carrier pruning replay.

Uses only the pinned credited scalar numeric checker, never the packed selector.
Case slices are complete explicit intervals at most1000; inconclusive stays open.
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


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start+45
    catalogue_mode = sys.argv[1] == 'catalogue'
    if catalogue_mode:
        branch = 1
        first, last, case_first, case_last = map(int, sys.argv[2:6])
    else:
        branch, first, last, case_first, case_last = map(int, sys.argv[1:6])
    source = PUBLIC / 'prior'
    manifest = json.loads((source / 'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((source / 'numeric.py').read_bytes()).hexdigest() == pin, 'Credited scalar checker changed')
    spec = importlib.util.spec_from_file_location('disjoint_independent_scalar_outer', source / 'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    if catalogue_mode:
        catalogue = json.loads((OUT / 'branch01-catalogue.json').read_text())
        normal = json.loads((OUT / 'branch01-catalogue-checked.json').read_text())
        optimized = json.loads((OUT / 'branch01-catalogue-checked-O.json').read_text())
        need(normal['finite'] == optimized['finite'] and normal['finite']['producer_quotient_sha256'] ==
             catalogue['finite_sha256'] and digest(catalogue['representatives']) ==
             catalogue['finite']['representatives_sha256'], 'Whole catalogue has not passed both scalar checks')
        front = {'survivors': catalogue['representatives'], 'finite_sha256': catalogue['finite_sha256']}
    else:
        front = json.loads((OUT / f'fronts{branch:02}-{first:05}-{last:05}.json').read_text())
        normal = json.loads((OUT / f'check{branch:02}-{first:05}-{last:05}.json').read_text())
        optimized = json.loads((OUT / f'check{branch:02}-{first:05}-{last:05}-O.json').read_text())
        need(normal['finite'] == optimized['finite'] and normal['finite']['producer_front_sha256'] == front['finite_sha256'],
             'Bounded front interface has not passed scalar checks in both modes')
    prefix = 'constant-catalogue' if catalogue_mode else 'constant'
    proposal = json.loads((OUT / f'{prefix}{branch:02}-{first:05}-{last:05}.json').read_text())
    cases = proposal['cases']
    need(digest(cases) == proposal['cases_sha256'], 'Case arrays differ')
    if catalogue_mode:
        expected = list(range(first, last))
    else:
        kernels = json.loads((OUT / f'kernels{branch:02}-{first:05}-{last:05}.json').read_text())
        expected = [r['front_index'] for r in kernels['classifications'] if r['status'].startswith('NO_IMPORTED')]
    need([r['front_index'] for r in cases] == expected and 0 <= case_first < case_last <= len(cases) and
         case_last-case_first <= 1000, 'Explicit complete case interval differs')
    replay, masses, counts = [], [], Counter()
    for offset in range(case_first, case_last):
        need(time.monotonic() < deadline, 'Incomplete45s scalar bound replay: no exclusion')
        if offset % 128 == 0:
            operations_allow()
        case = cases[offset]
        index = case['front_index']
        record = front['survivors'][index]
        need(case['branch_index'] == branch and case['prefix_sha256'] == record['prefix_sha256'] and
             case['nine_core_sha256'] == record['nine_core_sha256'], 'Wrong whole-front binding')
        if not case['constant16_exceeds44']:
            counts['inconclusive_preserved_open'] += 1
            continue
        seen, mass = set(), 0
        for witness in case['selected_witnesses']:
            low, high = witness['original_LOW_mask'], witness['original_HIGH_mask']
            need(low.bit_count() == high.bit_count() == 3 and not low & high and low | high < 8192,
                 'Invalid original3+3 cube')
            original = numeric.family(13, record['prefix'], low, high, 'outer')
            need(original == witness['outer_record'], 'Original scalar deletion/identity record differs')
            pruned = numeric.pruning(13, record['prefix'], original)
            need(digest(pruned['retained_prefix']) == witness['retained_Q_sha256'], 'Full oriented carrier word differs')
            need(witness['B7'] == 16 and witness['label'] == original[4]+original[5]+16,
                 'Unjustified S7 constant or nested label')
            current = tuple(original[2:4])
            need(current not in seen, 'Selected current outer classes overlap')
            seen.add(current)
            mass += 1 << witness['label']
            replay.append([index, original, digest(pruned), witness['label']])
            counts['selected_outer_occurrences'] += 1
        need(mass == case['selected_mass'] and mass > 1 << 44, 'Strict nested inequality fails')
        masses.append([index, mass])
        counts['independently_constant16_excluded_cases'] += 1
    finite = {'branch_index': branch, 'retained_interval': [first, last], 'case_slice': [case_first, case_last],
              'census': dict(counts), 'metrics': numeric.METRICS, 'replay_sha256': digest(replay),
              'root_masses_sha256': digest(masses), 'minimum_selected_mass': min((x[1] for x in masses), default=None),
              'complete_case_certificate_sha256': proposal['cases_sha256'],
              'complete_front_cover_sha256': front['finite_sha256'], 'credited_scalar_source_sha256': pin}
    if catalogue_mode:
        del finite['retained_interval']
        finite['catalogue_slice'] = [first, last]
        finite['target_kind'] = 'COMPLETE_PHYSICAL_IMAGE_MAXIMUM_BUDGET_REPRESENTATIVES'
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_BOUNDED_DISJOINT_CONSTANT16_ORIGINAL_CUBE_AND_CARRIER_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False,
              'scope': 'Only explicit positive cases in this complete slice; all inconclusive cases stay open.'}
    suffix = '-O' if not __debug__ else ''
    prefix = 'constant-catalogue-check' if catalogue_mode else 'constant-check'
    path = OUT / f'{prefix}{branch:02}-{first:05}-{last:05}-{case_first:05}-{case_last:05}{suffix}.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
