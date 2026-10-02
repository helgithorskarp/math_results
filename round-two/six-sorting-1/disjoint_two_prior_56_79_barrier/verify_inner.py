"""Separate scalar outer/carrier and complete inner-family/heap replay.

Uses credited pinned numeric.py, never packed producer/anchors/profile code.
Inconclusive cases are retained; an incomplete32-case stage proves nothing.
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
    first, last = map(int, sys.argv[1:3])
    source = ROOT / 'prior'
    manifest = json.loads((source / 'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((source / 'numeric.py').read_bytes()).hexdigest() == pin, 'Credited scalar source changed')
    spec = importlib.util.spec_from_file_location('disjoint_selected_original_inner_numeric', source / 'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    proposal = json.loads((OUT / f'inner01-{first:05}-{last:05}.json').read_text())
    need(digest(proposal['cases']) == proposal['finite']['cases_sha256'], 'Inner case arrays differ')
    summary = json.loads((OUT / 'branch01-constant-summary.json').read_text())
    residual = summary['inconclusive_catalogue_indices']
    expected = residual[first:last]
    need(0 <= first < last <= len(residual) and last-first <= 32 and
         expected == proposal['finite']['complete_residual_indices'] ==
         [c['catalogue_index'] for c in proposal['cases']], 'Explicit residual interval is incomplete')
    catalogue = json.loads((OUT / 'branch01-catalogue.json').read_text())
    need(catalogue['finite_sha256'] == proposal['finite']['catalogue_finite_sha256'] ==
         summary['catalogue_finite_sha256'], 'Wrong representative catalogue binding')
    counts, replay, masses, open_indices = Counter(), [], [], []
    for case in proposal['cases']:
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s original inner replay: no exclusion')
        index = case['catalogue_index']
        front = catalogue['representatives'][index]
        need(case['prefix_sha256'] == front['prefix_sha256'] and case['nine_core_sha256'] == front['nine_core_sha256'],
             'Wrong representative literal front')
        if not case['producer_exceeds44']:
            counts['inner_inconclusive_preserved_open'] += 1
            open_indices.append(index)
            continue
        seen, mass = set(), 0
        for witness in case['selected_witnesses']:
            low, high = witness['original_LOW_mask'], witness['original_HIGH_mask']
            need(low.bit_count() == high.bit_count() == 3 and not low & high and low | high < 8192,
                 'Invalid original3+3 restriction')
            record = numeric.family(13, front['prefix'], low, high, 'outer')
            need(record == witness['outer_record'], 'Whole scalar original outer record differs')
            pruned = numeric.pruning(13, front['prefix'], record)
            word = tuple(tuple(gate) for gate in pruned['retained_prefix'])
            need(digest(word) == witness['retained_Q_sha256'], 'Whole oriented carrier word differs')
            bound = witness['B7']
            if bound == 16:
                hashes, anchors = {}, {}
            else:
                checked, data, aggregate = numeric.inner_checked(word)
                need(bound == checked, 'Complete scalar original inner families or heap bound differs')
                hashes = {name: r['records_sha256'] for name, r in data.items()}
                anchors = {name: r['lower_bound'] for name, r in aggregate.items()}
            need(isinstance(bound, int) and bound >= 16 and witness['label'] == record[4]+record[5]+bound,
                 'Unjustified inner label')
            key = tuple(record[2:4])
            need(key not in seen, 'Selected original outer classes overlap')
            seen.add(key)
            mass += 1 << witness['label']
            counts[f'B7_{bound}'] += 1
            counts['selected_outer_occurrences'] += 1
            replay.append([index, record, digest(pruned), bound, hashes, anchors])
        need(mass == case['selected_mass'] and mass > 1 << 44, 'Strict selected inner root mass fails')
        masses.append([index, mass])
        counts['independently_inner_excluded_cases'] += 1
    need(open_indices == proposal['finite']['inconclusive_catalogue_indices'], 'Open residual identities differ')
    finite = {'residual_slice': [first, last], 'complete_residual_indices': expected, 'census': dict(counts),
              'metrics': numeric.METRICS, 'replay_sha256': digest(replay), 'root_masses_sha256': digest(masses),
              'minimum_selected_mass': min((r[1] for r in masses), default=None),
              'distinct_inner_words': numeric.inner_checked.cache_info().currsize,
              'complete_producer_cases_sha256': proposal['finite']['cases_sha256'],
              'credited_scalar_source_sha256': pin, 'inconclusive_catalogue_indices': open_indices}
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'BOUNDED_ORIGINAL_INNER_ANCHOR_SCALAR_PREMISES_CHECKED',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False,
              'scope': 'Only explicit strict positive residual certificates; listed inconclusive cases remain open.'}
    suffix = '-O' if not __debug__ else ''
    (OUT / f'inner-checked01-{first:05}-{last:05}{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
