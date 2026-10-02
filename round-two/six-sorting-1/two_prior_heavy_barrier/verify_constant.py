"""Independent scalar whole128-cube selected-outer constant16 replay.

Bounded disjoint case slices. Imports only the credited published numeric
checker, never packed pruning/profile or the new producer. No inner bounds.
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
OUT = ROOT/'work'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    branch, first, last = map(int, sys.argv[1:4])
    source = ROOT/'prior'
    manifest = json.loads((source/'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((source/'numeric.py').read_bytes()).hexdigest() == pin, 'Credited scalar source changed')
    spec = importlib.util.spec_from_file_location('two_prior_independent_scalar_outer', source/'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    front = json.loads((OUT/f'heavy-fronts{branch:02}.json').read_text())
    n = json.loads((OUT/f'heavy-checked{branch:02}.json').read_text())
    o = json.loads((OUT/f'heavy-checked{branch:02}-O.json').read_text())
    need(n['finite'] == o['finite'] and n['finite']['producer_front_sha256'] == front['finite_sha256'],
         'Whole necessary front cover not independently checked in both modes')
    proposal = json.loads((OUT/f'residual-constant{branch:02}.json').read_text())
    cases = proposal['cases']
    need(digest(cases) == proposal['cases_sha256'], 'Selected certificate cases digest differs')
    inheritance = json.loads((ROOT/'work/two-prior-heavy-inherited-obstructions.json').read_text())
    expected = [r['front_index'] for r in inheritance['classifications']
                if r['branch_index'] == branch and r['status'].startswith('NO_PUBLISHED')]
    need([r['front_index'] for r in cases] == expected and 0 <= first < last <= len(cases),
         'Residual cover or bounded disjoint case slice incomplete')
    replay = []
    masses = []
    counts = Counter()
    for offset in range(first, last):
        need(time.monotonic() < deadline, 'Incomplete independent constant replay:45s guard')
        if offset % 128 == 0:
            operations_allow()
        case = cases[offset]
        index = case['front_index']
        r = front['survivors'][index]
        need(case['branch_index'] == branch and case['prefix_sha256'] == r['prefix_sha256'] and
             case['nine_core_sha256'] == r['nine_core_sha256'], 'Certificate references wrong whole front')
        if not case['constant16_exceeds44']:
            counts['inconclusive_cases_preserved_open'] += 1
            continue
        seen = set()
        mass = 0
        for w in case['selected_witnesses']:
            low, high = w['original_LOW_mask'], w['original_HIGH_mask']
            need(low.bit_count() == high.bit_count() == 3 and not low & high and low | high < 8192,
                 'Invalid original3+3 domain')
            record = numeric.family(13, r['prefix'], low, high, 'outer')
            need(record == w['outer_record'], 'Whole original scalar D/R/identity record differs')
            pruned = numeric.pruning(13, r['prefix'], record)
            q = pruned['retained_prefix']
            need(digest(q) == w['retained_Q_sha256'], 'Retained oriented carrier word differs')
            need(w['B7'] == 16 and w['label'] == record[4]+record[5]+16,
                 'Unjustified constant seven-input bound or nested label')
            current = tuple(record[2:4])
            need(current not in seen, 'Selected current outer classes overlap')
            seen.add(current)
            mass += 1 << w['label']
            replay.append([index, record, digest(pruned), w['label']])
            counts['selected_outer_occurrences'] += 1
        need(mass == case['selected_mass'] and mass > 1 << 44, 'Strict selected nested inequality fails')
        masses.append([index, mass])
        counts['independently_constant16_excluded_cases'] += 1
    finite = {'branch_index': branch, 'case_slice': [first, last], 'census': dict(counts),
              'metrics': numeric.METRICS, 'replay_sha256': digest(replay), 'root_masses_sha256': digest(masses),
              'minimum_selected_mass': min((r[1] for r in masses), default=None),
              'complete_case_certificate_sha256': proposal['cases_sha256'],
              'complete_front_cover_sha256': front['finite_sha256'], 'credited_scalar_source_sha256': pin}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_DISJOINT_HEAVY_RESIDUAL_CONSTANT16_SELECTED_ORIGINAL_CUBES_INDEPENDENTLY_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'One bounded necessary-front slice; inconclusive cases remain open; no full branch claim from partial slices.',
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False}
    suffix = '-O' if not __debug__ else ''
    (OUT/f'constant-checked{branch:02}-{first:05}-{last:05}{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
