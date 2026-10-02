"""Whole single-route target quotient by identical physical image and budget.

Construction uses complete image tuples and maximizes the representative budget.
The independent check uses all original interval records and direct image sets;
every original target must equal its representative and have a weaker budget.
Neither mode asserts a representative has been excluded.
"""
from collections import Counter
import hashlib
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


def build():
    start = time.monotonic()
    deadline = start+45
    summary = json.loads((OUT / 'branch01-front-cover-summary.json').read_text())
    ids = json.loads((ROOT / 'work/cuts01.json').read_text())['retained_function_ids']
    need(len(ids) == 3875 and summary['retained_functions'] == 3875, 'Single-route preparation cover differs')
    expected = [[i, min(i+128, len(ids))] for i in range(0, len(ids), 128)]
    need([r['retained_interval'] for r in summary['intervals']] == expected, 'Full interval partition incomplete')
    unique, occurrences, counts, metrics, bindings = {}, [], Counter(), Counter(), []
    for first, last in expected:
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s whole-image quotient')
        p = json.loads((OUT / f'fronts01-{first:05}-{last:05}.json').read_text())
        n = json.loads((OUT / f'check01-{first:05}-{last:05}.json').read_text())
        o = json.loads((OUT / f'check01-{first:05}-{last:05}-O.json').read_text())
        need(n['finite'] == o['finite'] and digest(n['finite']) == n['finite_sha256'] == o['finite_sha256'] and
             n['finite']['producer_front_sha256'] == p['finite_sha256'] and
             digest(p['survivors']) == p['survivors_sha256'] and digest(p['rejections']) == p['rejections_sha256'] and
             p['retained_function_ids'] == ids[first:last], 'Whole target cover binding differs')
        counts.update(p['census'])
        metrics.update(n['finite']['metrics'])
        bindings.append([first, last, p['finite_sha256'], n['finite_sha256']])
        for i, record in enumerate(p['survivors']):
            image = tuple(record['nine_core_states'])
            origin = [first, last, i]
            occurrences.append((origin, image))
            if image not in unique or record['remaining_gate_budget'] > unique[image]['remaining_gate_budget']:
                unique[image] = {**record, 'source_retained_interval': [first, last], 'source_front_index': i}
    representatives = [record for image, record in sorted(unique.items())]
    index = {tuple(record['nine_core_states']): i for i, record in enumerate(representatives)}
    aliases = [origin+[index[image]] for origin, image in occurrences]
    finite = {'branch_index': 1, 'HIGH_word': [[5, 6], [7, 9]], 'retained_functions': len(ids),
              'front_census': dict(counts), 'front_metrics': dict(metrics), 'original_target_count': len(aliases),
              'representative_targets': len(representatives), 'physical_core_ports': list(range(2, 11)),
              'complete_interval_bindings_sha256': digest(bindings),
              'representatives_sha256': digest(representatives), 'aliases_sha256': digest(aliases),
              'remaining_gate_budgets': dict(sorted(Counter(r['remaining_gate_budget'] for r in representatives).items())),
              'image_size_range': [min(map(lambda r: len(r['nine_core_states']), representatives)),
                                   max(map(lambda r: len(r['nine_core_states']), representatives))]}
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'ONE_ROUTE_EXACT_IMAGE_BUDGET_QUOTIENT_PROPOSAL',
              'finite': finite, 'finite_sha256': digest(finite), 'representatives': representatives,
              'aliases': aliases, 'complete_interval_bindings': bindings,
              'seconds': time.monotonic()-start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Every original target is covered only if all listed representatives are independently excluded.'}
    (OUT / 'branch01-catalogue.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('representatives', 'aliases', 'complete_interval_bindings')}, sort_keys=True))


def check():
    start = time.monotonic()
    deadline = start+45
    proposal = json.loads((OUT / 'branch01-catalogue.json').read_text())
    representatives = proposal['representatives']
    need(digest(representatives) == proposal['finite']['representatives_sha256'] and
         digest(proposal['aliases']) == proposal['finite']['aliases_sha256'], 'Quotient arrays differ')
    ids = json.loads((ROOT / 'work/cuts01.json').read_text())['retained_function_ids']
    aliases = {}
    for first, last, i, target in proposal['aliases']:
        key = (first, last, i)
        need(key not in aliases and 0 <= target < len(representatives), 'Repeated/invalid alias')
        aliases[key] = target
    vector_sets = [set(r['nine_core_states']) for r in representatives]
    need(len({tuple(sorted(s)) for s in vector_sets}) == len(vector_sets), 'Representatives not distinct images')
    coverage, replay, bindings, counts, metrics = set(), [], [], Counter(), Counter()
    representative_origins = {(tuple(r['source_retained_interval']), r['source_front_index']): i
                              for i, r in enumerate(representatives)}
    need(len(representative_origins) == len(representatives), 'Repeated chosen physical source front')
    seen_representatives = set()
    for first in range(0, len(ids), 128):
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s independent alias replay')
        last = min(first+128, len(ids))
        p = json.loads((OUT / f'fronts01-{first:05}-{last:05}.json').read_text())
        n = json.loads((OUT / f'check01-{first:05}-{last:05}.json').read_text())
        o = json.loads((OUT / f'check01-{first:05}-{last:05}-O.json').read_text())
        need(p['retained_function_ids'] == ids[first:last] and n['finite'] == o['finite'] and
             n['finite']['producer_front_sha256'] == p['finite_sha256'], 'Original interval not covered normal/O')
        bindings.append([first, last, p['finite_sha256'], n['finite_sha256']])
        counts.update(p['census'])
        metrics.update(n['finite']['metrics'])
        for i, record in enumerate(p['survivors']):
            key = (first, last, i)
            need(key in aliases, 'Original target missing from quotient')
            target = aliases[key]
            representative = representatives[target]
            need(set(record['nine_core_states']) == vector_sets[target] and
                 record['remaining_gate_budget'] <= representative['remaining_gate_budget'],
                 'Wrong image equality or budget direction')
            need(digest(record['nine_core_states']) == record['nine_core_sha256'] == representative['nine_core_sha256'],
                 'Actual whole-image digest differs')
            coverage.add(key)
            replay.append([first, last, i, target, record['remaining_gate_budget'], representative['remaining_gate_budget']])
            origin = ((first, last), i)
            if origin in representative_origins:
                r = representative_origins[origin]
                need(r == target and {k: v for k, v in representatives[r].items()
                                      if k not in ('source_retained_interval', 'source_front_index')} == record,
                     'Representative is not the original scalar-checked literal front')
                seen_representatives.add(r)
    need(coverage == set(aliases) and seen_representatives == set(range(len(representatives))) and
         bindings == proposal['complete_interval_bindings'] and digest(bindings) ==
         proposal['finite']['complete_interval_bindings_sha256'] and
         dict(counts) == proposal['finite']['front_census'] and dict(metrics) == proposal['finite']['front_metrics'],
         'Complete single-route alias/source cover differs')
    finite = {'branch_index': 1, 'source_targets_replayed': len(coverage),
              'representative_targets': len(seen_representatives), 'alias_replay_sha256': digest(replay),
              'producer_quotient_sha256': proposal['finite_sha256'],
              'complete_interval_bindings_sha256': digest(bindings), 'front_census': dict(counts), 'front_metrics': dict(metrics)}
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'WHOLE_ONE_ROUTE_IMAGE_BUDGET_ALIASES_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Verified exact transfer of negative representative results only; representatives need separate exclusions.'}
    suffix = '-O' if not __debug__ else ''
    (OUT / f'branch01-catalogue-checked{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    operations_allow()
    build() if sys.argv[1] == 'build' else check()
