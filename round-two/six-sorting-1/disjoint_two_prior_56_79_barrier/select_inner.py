"""Bounded original3+3 inner-anchor refinement of genuine constant-bound misses.

Sufficient selector only. Uses the generic published two semantic anchors;
each positive proposal still needs the separate scalar original-cube checker.
"""
from collections import Counter
from functools import lru_cache
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start+45
    first, last = map(int, sys.argv[1:3])
    summary = json.loads((OUT / 'branch01-constant-summary.json').read_text())
    residual = summary['inconclusive_catalogue_indices']
    need(0 <= first < last <= len(residual) and last-first <= 32, 'Require an explicit residual slice of at most32')
    catalogue = json.loads((OUT / 'branch01-catalogue.json').read_text())
    need(summary['catalogue_finite_sha256'] == catalogue['finite_sha256'], 'Residual target catalogue changed')
    source = ROOT / 'prior'
    manifest = json.loads((source / 'source-manifest.json').read_text())
    pins = {r['path']: r['sha256'] for r in manifest['files']}
    for name in ('pruning.py', 'anchors.py', 'profile.py', 'fixture.json'):
        need(hashlib.sha256((source / name).read_bytes()).hexdigest() == pins[name], 'Credited anchor source changed')
    pruning = load('disjoint_inner_packed_pruning', source / 'pruning.py')
    anchors = load('disjoint_inner_packed_anchors', source / 'anchors.py')
    pool = json.loads((source / 'fixture.json').read_text())['selected_original_pool']

    @lru_cache(None)
    def inner(word):
        data = anchors.semantic.analyze(7, [list(gate) for gate in word])
        result = anchors.both(7, data)
        return max(16, *(record['lower_bound'] for record in result.values()))

    cases, counts = [], Counter()
    for index in residual[first:last]:
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s inner selector: no exclusion')
        front = catalogue['representatives'][index]
        candidates = []
        for low, high in pool:
            p = pruning.pruning(front['prefix'], low, high, anchors.semantic)
            candidates.append((sum(p['outer_record'][4:6]), low, high, p))
        classes, tested = {}, 0
        for credit, low, high, p in sorted(candidates, key=lambda x: (-x[0], x[1], x[2])):
            need(time.monotonic() < deadline, 'Incomplete45s selected inner stage: no exclusion')
            word = tuple(tuple(gate) for gate in p['retained_prefix'])
            bound = inner(word)
            record = p['outer_record']
            key = tuple(record[2:4])
            label = credit+bound
            if key not in classes or label > classes[key]['label']:
                classes[key] = {'original_LOW_mask': low, 'original_HIGH_mask': high,
                                'outer_record': record, 'retained_Q_sha256': digest(word), 'B7': bound, 'label': label}
            tested += 1
            if sum(1 << record['label'] for record in classes.values()) > 1 << 44:
                break
        selected, mass = [], 0
        for record in sorted(classes.values(), key=lambda x: (-x['label'], x['outer_record'][2:4])):
            selected.append(record)
            mass += 1 << record['label']
            if mass > 1 << 44:
                break
        closed = mass > 1 << 44
        counts['inner_exclusion_proposals' if closed else 'inner_inconclusive'] += 1
        counts['selected_outer_occurrences'] += len(selected)
        cases.append({'catalogue_index': index, 'prefix_sha256': front['prefix_sha256'],
                      'nine_core_sha256': front['nine_core_sha256'], 'producer_exceeds44': closed,
                      'selected_mass': mass, 'selected_witnesses': selected, 'proposals_tested': tested})
    finite = {'residual_slice': [first, last], 'complete_residual_indices': residual[first:last],
              'census': dict(counts), 'cases_sha256': digest(cases),
              'selected_B7_counts': dict(Counter(w['B7'] for c in cases for w in c['selected_witnesses'])),
              'distinct_inner_words': inner.cache_info().currsize,
              'catalogue_finite_sha256': catalogue['finite_sha256'],
              'inconclusive_catalogue_indices': [c['catalogue_index'] for c in cases if not c['producer_exceeds44']]}
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'BOUNDED_INNER_ANCHOR_PROPOSALS_NEED_SCALAR_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'cases': cases,
              'seconds': time.monotonic()-start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Explicit residual slice only; inconclusive representatives stay open; no suffix construction tested.'}
    (OUT / f'inner01-{first:05}-{last:05}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
