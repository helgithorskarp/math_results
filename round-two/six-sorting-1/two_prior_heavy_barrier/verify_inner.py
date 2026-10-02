"""Scalar selected outer and complete original inner cube/heap anchor replay."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
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
    source = ROOT/'prior'
    manifest = json.loads((source/'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((source/'numeric.py').read_bytes()).hexdigest() == pin, 'Credited scalar source changed')
    spec = importlib.util.spec_from_file_location('two_prior_seven_independent_numeric', source/'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    p = json.loads((ROOT/'work/two-prior-seven-inner-producer.json').read_text())
    need(digest(p['cases']) == p['cases_sha256'] and not p['inconclusive_case_ids'],
         'Inner certificate incomplete or still inconclusive')
    expected = []
    for branch in (0, 6, 11, 15, 16, 19, 21, 22, 23, 24):
        constant = json.loads((OUT/f'residual-constant{branch:02}.json').read_text())
        expected.extend([branch, i] for i in constant['inconclusive_front_indices'])
    need(expected == p['complete_seven_case_ids'] ==
         [[r['branch_index'], r['front_index']] for r in p['cases']] and len(expected) == 7,
         'Inner certificates do not cover exactly all seven residuals')
    counts = Counter()
    replay = []
    masses = []
    for case in p['cases']:
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete independent inner45s guard: not an exclusion')
        branch, index = case['branch_index'], case['front_index']
        front = json.loads((OUT/f'heavy-fronts{branch:02}.json').read_text())['survivors'][index]
        need(case['producer_exceeds44'] and case['prefix_sha256'] == front['prefix_sha256'] and
             case['nine_core_sha256'] == front['nine_core_sha256'], 'Wrong residual front binding')
        seen = set()
        mass = 0
        for witness in case['selected_witnesses']:
            lo, hi = witness['original_LOW_mask'], witness['original_HIGH_mask']
            need(lo.bit_count() == hi.bit_count() == 3 and not lo & hi and lo | hi < 8192,
                 'Invalid original3+3 clamping')
            record = numeric.family(13, front['prefix'], lo, hi, 'outer')
            need(record == witness['outer_record'], 'Full original outer record differs')
            pruned = numeric.pruning(13, front['prefix'], record)
            q = tuple(tuple(g) for g in pruned['retained_prefix'])
            need(digest(q) == witness['retained_Q_sha256'], 'Original oriented carrier word differs')
            bound = witness['B7']
            if bound == 16:
                inner_hashes, anchors = {}, {}
            else:
                checked, data, aggregate = numeric.inner_checked(q)
                need(bound == checked, 'Full original inner scalar families/heap bound differs')
                inner_hashes = {k: r['records_sha256'] for k, r in data.items()}
                anchors = {k: r['lower_bound'] for k, r in aggregate.items()}
            need(isinstance(bound, int) and bound >= 16 and witness['label'] == record[4]+record[5]+bound,
                 'Unjustified nested label')
            key = tuple(record[2:4])
            need(key not in seen, 'Selected outer classes overlap')
            seen.add(key)
            mass += 1 << witness['label']
            counts[f'B7_{bound}'] += 1
            counts['selected_outer_occurrences'] += 1
            replay.append([branch, index, record, digest(pruned), bound, inner_hashes, anchors])
        need(mass == case['selected_mass'] and mass > 1 << 44, 'Strict inner selected mass does not exceed44 ceiling')
        masses.append([branch, index, mass])
        counts['independently_inner_excluded_cases'] += 1
    finite = {'census': dict(counts), 'metrics': numeric.METRICS, 'complete_seven_case_ids': expected,
              'replay_sha256': digest(replay), 'root_masses_sha256': digest(masses),
              'minimum_selected_mass': min(r[2] for r in masses), 'size44_ceiling': 1 << 44,
              'distinct_inner_words': numeric.inner_checked.cache_info().currsize,
              'complete_producer_cases_sha256': p['cases_sha256'], 'credited_scalar_source_sha256': pin}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'ALL_SEVEN_HEAVY_RESIDUALS_INDEPENDENTLY_INNER_ANCHOR_EXCLUDED',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Seven residual heavy-chain fronts only; must combine with complete cover and other independently checked exclusions.',
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False}
    suffix = '-O' if not __debug__ else ''
    (ROOT/f'work/two-prior-seven-inner-independent{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True))
    print(json.dumps({'census': dict(counts), 'metrics': numeric.METRICS}, sort_keys=True))


if __name__ == '__main__':
    main()
