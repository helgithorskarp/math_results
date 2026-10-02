"""Bounded necessary singleton/three-balanced-tail cover for disjoint HIGH seeds.

Packed complete 157-state functions. This produces proposals, not exclusions.
The interval is in retained preparation IDs, never a claimed whole-branch cover.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'work'
OUT = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def advance(columns, event):
    a, b = (p - 2 for p in event)
    result = list(columns)
    result[a], result[b] = columns[a] & columns[b], columns[a] | columns[b]
    return tuple(result)


def balanced_tails(ports):
    a, b, c, d = sorted(ports)
    pairings = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
    tails = []
    for p, q in pairings:
        first = sorted((p, q))
        final = sorted((p[1], q[1]))
        tails.append([list(x) for x in first] + [final])
    return tails


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    branch, first, last = map(int, sys.argv[1:4])
    need(0 <= first < last and last - first <= 128, 'Require a bounded interval of at most128 retained IDs')
    p = json.loads((INPUT / f'branch{branch:02}.json').read_text())
    cuts = json.loads((INPUT / f'cuts{branch:02}.json').read_text())
    need(last <= len(cuts['retained_function_ids']), 'Interval outside retained preparation cover')
    ids = cuts['retained_function_ids'][first:last]
    source = ROOT / 'prior'
    fixture = json.loads((source / 'fixture.json').read_text())
    prefix = fixture['B23'] + fixture['LOW_suffixes']['4']
    base = json.loads((source / 'work/low26-partner4-construction-pilot.json').read_text())['core_states']
    domains = json.loads((source / 'work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    cache = json.loads((ROOT / 'work/two-prior-independent-original-cubes.json').read_text())['scalar_cache']
    originals = {core: original for core, original, correct in cache['full_core_witnesses']}
    need(len(base) == 157 and len(domains) == 39, 'Full original-domain interface differs')
    masks = [(r['original_LOW_mask'], r['core_image_index_mask']) for r in domains]
    columns = tuple(sum((x >> j & 1) << i for i, x in enumerate(base)) for j in range(10))
    target = tuple(sum(int(x.bit_count() >= 10-j) << i for i, x in enumerate(base)) for j in range(10))
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    for a, b in p['HIGH_word']:
        need(a < b and live[a] == live[b], 'Nonstandard/unequal HIGH seed')
        del live[a]
        live[b] += 1
        columns = advance(columns, (a, b))
    need(sorted(live.values()) == [6, 7, 7, 7], 'Require a disjoint-pair two-prior route')
    dead = p['dead_preparation_ports']
    need(len(dead) == 6 and 11 in live, 'Six-variable preparation or held largest root differs')
    patterns = [sum((columns[port-2] >> i & 1) << j for j, port in enumerate(dead)) for i in range(157)]
    bins = [sum(1 << i for i, x in enumerate(patterns) if x == k) for k in range(64)]

    def obstruction(values, event=None):
        if event is not None:
            a, b = event
            active = values[a-2] & ~values[b-2]
            lo = next((lo for lo, mask in masks if not active & mask), None)
            if lo is not None:
                return {'kind': 'WHOLE_ORIGINAL_LOW_IDENTITY', 'original_LOW_mask': lo}
        for j in range(10):
            wrong = values[j] ^ target[j]
            if not wrong:
                continue
            invalid = 0
            for q in range(j):
                invalid |= values[q] & ~values[j]
            for q in range(j+1, 10):
                invalid |= values[j] & ~values[q]
            lo = next((lo for lo, mask in masks if not invalid & mask), None)
            if lo is not None:
                bad = (wrong & -wrong).bit_length() - 1
                return {'kind': 'TIGHT_ORIGINAL_LOW_FREE_PIVOT_CUT', 'pivot_port': j+2,
                        'original_LOW_mask': lo, 'full_original_boolean_witness': originals[base[bad]]}
        return None

    counts = Counter()
    survivors, rejections = [], []
    for fid in ids:
        need(time.monotonic() < deadline, 'Incomplete45s guard: no exclusion')
        operations_allow()
        f = p['functions'][fid]
        values = list(columns)
        for port, packed in zip(dead, f['full_six_variable_columns']):
            values[port-2] = sum(bins[k] for k in range(64) if packed >> k & 1)
        values = tuple(values)
        need(obstruction(values) is None, 'Screened preparation cut survived')
        counts['eligible_preparation_functions'] += 1
        high = next(port for port, cost in live.items() if cost == 6)
        for free in dead:
            single = sorted((high, free))
            key = {'function_id': fid, 'singleton': single}
            counts['candidate_singleton_heads'] += 1
            failed = obstruction(values, single)
            head = advance(values, single)
            if failed is None:
                failed = obstruction(head)
            if failed is not None:
                counts['head_' + failed['kind']] += 1
                rejections.append({**key, 'stage': 'HEAD', **failed})
                continue
            counts['active_uncut_singleton_heads'] += 1
            after = dict(live)
            del after[high]
            after[max(single)] = 7
            need(sorted(after.values()) == [7, 7, 7, 7] and sum(1 << d for d in after.values()) == 512,
                 'Singleton failed four equal-root HIGH mass control')
            for tail_id, tail in enumerate(balanced_tails(after)):
                counts['candidate_complete_tail_functions'] += 1
                current = head
                failed = None
                for t, event in enumerate(tail):
                    failed = obstruction(current, event)
                    current = advance(current, event)
                    if failed is None:
                        failed = obstruction(current)
                    if failed is not None:
                        counts['tail_' + failed['kind']] += 1
                        rejections.append({**key, 'tail_id': tail_id, 'stage': 'TAIL',
                                           'tail_event_index': t, 'HIGH_tail': tail, **failed})
                        break
                if failed is not None:
                    continue
                need(current[9] == target[9], 'Whole157-state second-largest statistic fails')
                image = sorted({sum((current[j] >> i & 1) << j for j in range(9)) for i in range(157)})
                literal = prefix + p['HIGH_word'] + f['shortest_word'] + [single] + tail
                need(len(literal) == 32 + len(f['shortest_word']), 'Literal front length differs')
                counts['surviving_complete_fronts'] += 1
                survivors.append({**key, 'tail_id': tail_id, 'HIGH_tail': tail,
                                  'preparation_word': f['shortest_word'], 'prefix': literal,
                                  'prefix_sha256': digest(literal), 'prefix_length': len(literal),
                                  'remaining_gate_budget': 44-len(literal), 'nine_core_states': image,
                                  'nine_core_sha256': digest(image), 'global_port2_correct': current[0] == target[0]})
    finite = {'branch_index': branch, 'retained_interval': [first, last], 'HIGH_word': p['HIGH_word'],
              'retained_function_ids': ids, 'census': dict(counts),
              'survivors_sha256': digest(survivors), 'rejections_sha256': digest(rejections),
              'preparation_functions_sha256': p['full_functions_sha256'],
              'preparation_cut_classification_sha256': cuts['classification_sha256'],
              'front_image_size_range': [min((len(r['nine_core_states']) for r in survivors), default=0),
                                         max((len(r['nine_core_states']) for r in survivors), default=0)],
              'remaining_gate_budgets': dict(sorted(Counter(r['remaining_gate_budget'] for r in survivors).items()))}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_BOUNDED_DISJOINT_TWO_PRIOR_HEAD_THREE_TAIL_PROPOSAL_ONLY',
              **finite, 'survivors': survivors, 'rejections': rejections, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Only the explicit retained-function interval; no full branch, arbitrary-44 or feasibility assertion.'}
    OUT.mkdir(exist_ok=True)
    path = OUT / f'fronts{branch:02}-{first:05}-{last:05}.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('survivors', 'rejections')}, sort_keys=True))


if __name__ == '__main__':
    main()
