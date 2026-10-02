"""Exact packed inner-anchor refinement of seven heavy residual fronts.

Uses credited published generic pruning and both semantic anchors. Producer
only until all original inner cubes/carrier/heap premises independently replay.
"""
from collections import Counter
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'work'
BRANCHES = (0, 6, 11, 15, 16, 19, 21, 22, 23, 24)


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
    source = ROOT/'prior'
    pruning = load('two_prior_inner_packed_pruning', source/'pruning.py')
    anchors = load('two_prior_inner_packed_anchors', source/'anchors.py')
    pool = json.loads((source/'fixture.json').read_text())['selected_original_pool']
    expected = []
    for branch in BRANCHES:
        baseline = json.loads((OUT/f'residual-constant{branch:02}.json').read_text())
        expected.extend((branch, index) for index in baseline['inconclusive_front_indices'])
    need(len(expected) == 7, 'Observed seven-case frontier changed')
    @lru_cache(None)
    def inner(word):
        data = anchors.semantic.analyze(7, [list(g) for g in word])
        result = anchors.both(7, data)
        return max(16, *(r['lower_bound'] for r in result.values()))
    cases = []
    counts = Counter()
    for branch, index in expected:
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s inner guard: not an exclusion')
        front = json.loads((OUT/f'heavy-fronts{branch:02}.json').read_text())['survivors'][index]
        candidates = []
        for lo, hi in pool:
            p = pruning.pruning(front['prefix'], lo, hi, anchors.semantic)
            candidates.append((sum(p['outer_record'][4:6]), lo, hi, p))
        classes = {}
        tested = 0
        for credit, lo, hi, p in sorted(candidates, key=lambda r: (-r[0], r[1], r[2])):
            need(time.monotonic() < deadline, 'Incomplete45s inner selector: not an exclusion')
            q = tuple(tuple(g) for g in p['retained_prefix'])
            bound = inner(q)
            record = p['outer_record']
            key = tuple(record[2:4])
            label = credit + bound
            if key not in classes or label > classes[key]['label']:
                classes[key] = {'original_LOW_mask': lo, 'original_HIGH_mask': hi,
                    'outer_record': record, 'retained_Q_sha256': digest(q), 'B7': bound, 'label': label}
            tested += 1
            if sum(1 << r['label'] for r in classes.values()) > 1 << 44:
                break
        selected = []
        mass = 0
        for r in sorted(classes.values(), key=lambda r: (-r['label'], r['outer_record'][2:4])):
            selected.append(r)
            mass += 1 << r['label']
            if mass > 1 << 44:
                break
        closed = mass > 1 << 44
        counts['inner_sufficient_exclusion_proposals' if closed else 'inner_inconclusive'] += 1
        counts['selected_outer_occurrences'] += len(selected)
        cases.append({'branch_index': branch, 'front_index': index,
                      'prefix_sha256': front['prefix_sha256'], 'nine_core_sha256': front['nine_core_sha256'],
                      'producer_exceeds44': closed, 'selected_mass': mass,
                      'selected_witnesses': selected, 'proposals_tested': tested})
    finite = {'census': dict(counts), 'cases_sha256': digest(cases),
              'complete_seven_case_ids': expected, 'distinct_inner_words': inner.cache_info().currsize,
              'selected_B7_counts': dict(Counter(w['B7'] for c in cases for w in c['selected_witnesses'])),
              'inconclusive_case_ids': [[r['branch_index'], r['front_index']] for r in cases if not r['producer_exceeds44']]}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_PRIVATE_SEVEN_CASE_INNER_ANCHOR_REFINEMENT_NEEDS_INDEPENDENT_REPLAY',
              **finite, 'cases': cases, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Only seven residual heavy-front certificates; whole outer/inner numeric and carrier replay still required.'}
    (ROOT/'work/two-prior-seven-inner-producer.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
