"""Complete private singleton/tail intake for TEN heavy-chain HIGH routes.

Exactly two prior equal HIGH events, the second joining their cost7 root
to the original cost7 port11. Fifteen disjoint-pair routes are not processed.
"""
from collections import Counter
import hashlib
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


def advance(columns, event):
    a, b = event
    a -= 2
    b -= 2
    fresh = list(columns)
    fresh[a], fresh[b] = columns[a] & columns[b], columns[a] | columns[b]
    return tuple(fresh)


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    started = time.monotonic()
    deadline = started + 45
    index = int(sys.argv[1])
    producer = json.loads((OUT/f'branch{index:02}.json').read_text())
    cuts = json.loads((OUT/f'cuts{index:02}.json').read_text())
    source = ROOT/'prior'
    fixture = json.loads((source/'fixture.json').read_text())
    prefix = fixture['B23'] + fixture['LOW_suffixes']['4']
    base = json.loads((source/'work/low26-partner4-construction-pilot.json').read_text())['core_states']
    domains = json.loads((source/'work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    cache = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())['scalar_cache']
    originals = {x: original for x, original, correct in cache['full_core_witnesses']}
    original_masks = [(r['original_LOW_mask'], r['core_image_index_mask']) for r in domains]
    full = tuple(sum((x >> j & 1) << i for i, x in enumerate(base)) for j in range(10))
    target = tuple(sum(int(x.bit_count() >= 10-j) << i for i, x in enumerate(base)) for j in range(10))
    word = producer['HIGH_word']
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    for a, b in word:
        need(a < b and live[a] == live[b], 'Nonstandard or unequal HIGH seed')
        del live[a]
        live[b] += 1
        full = advance(full, [a, b])
    need(sorted(live.values()) == [6, 6, 6, 8] and live[11] == 8,
         'This intake is for the heavy-chain subfamily only')
    dead = producer['dead_preparation_ports']
    patterns = [sum((full[p-2] >> i & 1) << j for j, p in enumerate(dead)) for i in range(157)]
    bins = [sum(1 << i for i, x in enumerate(patterns) if x == k) for k in range(64)]

    def obstruction(columns, event=None):
        if event is not None:
            a, b = event
            active = columns[a-2] & ~columns[b-2]
            lo = next((lo for lo, mask in original_masks if not active & mask), None)
            if lo is not None:
                return {'kind': 'WHOLE_ORIGINAL_LOW_IDENTITY', 'original_LOW_mask': lo}
        for j in range(10):
            wrong = columns[j] ^ target[j]
            if not wrong:
                continue
            invalid = 0
            for q in range(j):
                invalid |= columns[q] & ~columns[j]
            for q in range(j+1, 10):
                invalid |= columns[j] & ~columns[q]
            lo = next((lo for lo, mask in original_masks if not invalid & mask), None)
            if lo is not None:
                bad = (wrong & -wrong).bit_length()-1
                return {'kind': 'TIGHT_ORIGINAL_LOW_FREE_PIVOT_CUT', 'pivot_port': j+2,
                        'original_LOW_mask': lo, 'full_original_boolean_witness': originals[base[bad]]}
        return None

    counts = Counter()
    survivors = []
    rejections = []
    for fid in cuts['retained_function_ids']:
        need(time.monotonic() < deadline, 'Incomplete intake: operational45s guard')
        if fid % 128 == 0:
            operations_allow()
        f = producer['functions'][fid]
        columns = list(full)
        for p, c in zip(dead, f['full_six_variable_columns']):
            columns[p-2] = sum(bins[k] for k in range(64) if c >> k & 1)
        columns = tuple(columns)
        need(obstruction(columns) is None, 'A previously screened preparation cut survived')
        counts['eligible_preparation_functions'] += 1
        for high, cost in sorted(live.items()):
            if cost != 6:
                continue
            for free in dead:
                singleton = sorted([high, free])
                counts['candidate_singleton_heads'] += 1
                failed = obstruction(columns, singleton)
                head = advance(columns, singleton)
                if failed is None:
                    failed = obstruction(head)
                key = {'function_id': fid, 'singleton': singleton}
                if failed is not None:
                    counts['head_' + failed['kind']] += 1
                    rejections.append({**key, 'stage': 'HEAD', **failed})
                    continue
                counts['active_uncut_singleton_heads'] += 1
                after = dict(live)
                del after[high]
                after[max(singleton)] = 7
                need(sorted(after.values()) == [6, 6, 7, 8] and sum(1 << d for d in after.values()) == 512,
                     'Singleton failed saturated HIGH cost control')
                tail = []
                while len(after) > 1:
                    groups = {}
                    for p, d in sorted(after.items()):
                        groups.setdefault(d, []).append(p)
                    matching = [ports for ports in groups.values() if len(ports) >= 2]
                    need(len(matching) == 1 and len(matching[0]) == 2, 'Heavy saturated tail is not forced')
                    a, b = matching[0]
                    old = after[b]
                    del after[a]
                    after[b] = old + 1
                    tail.append([a, b])
                need(after == {11: 9} and len(tail) == 3, 'Forced heavy tail differs')
                counts['candidate_complete_tails'] += 1
                current = head
                failed = None
                for t, event in enumerate(tail):
                    failed = obstruction(current, event)
                    current = advance(current, event)
                    if failed is None:
                        failed = obstruction(current)
                    if failed is not None:
                        counts['tail_' + failed['kind']] += 1
                        rejections.append({**key, 'stage': 'TAIL', 'tail_event_index': t,
                                           'HIGH_tail': tail, **failed})
                        break
                if failed is not None:
                    continue
                need(current[9] == target[9], 'Full HIGH tail failed whole157-state second-largest statistic')
                image = sorted({sum((current[j] >> i & 1) << j for j in range(9)) for i in range(157)})
                literal = prefix + word + f['shortest_word'] + [singleton] + tail
                need(len(literal) == 32 + len(f['shortest_word']), 'Literal front length differs')
                counts['surviving_complete_fronts'] += 1
                survivors.append({**key, 'HIGH_tail': tail, 'preparation_word': f['shortest_word'],
                                  'prefix': literal, 'prefix_sha256': digest(literal),
                                  'prefix_length': len(literal), 'remaining_gate_budget': 44-len(literal),
                                  'nine_core_states': image, 'nine_core_sha256': digest(image),
                                  'global_port2_correct': current[0] == target[0]})
    finite = {'branch_index': index, 'HIGH_word': word, 'census': dict(counts),
              'survivors_sha256': digest(survivors), 'rejections_sha256': digest(rejections),
              'retained_preparation_ids_sha256': digest(cuts['retained_function_ids']),
              'front_image_size_range': [min((len(r['nine_core_states']) for r in survivors), default=0),
                                         max((len(r['nine_core_states']) for r in survivors), default=0)],
              'remaining_gate_budgets': dict(sorted(Counter(r['remaining_gate_budget'] for r in survivors).items()))}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_PRIVATE_ONE_HEAVY_TWO_PRIOR_SINGLETON_FRONT_INTAKE_NEEDS_INDEPENDENT_REPLAY',
              **finite, 'survivors': survivors, 'rejections': rejections,
              'finite_sha256': digest(finite), 'seconds': time.monotonic()-started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'One heavy-chain HIGH route, complete singleton/forced-three-tail intake only. Disjoint two-prior routes and sorting exclusions remain open.'}
    (OUT/f'heavy-fronts{index:02}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('survivors', 'rejections')}, sort_keys=True))


if __name__ == '__main__':
    main()
