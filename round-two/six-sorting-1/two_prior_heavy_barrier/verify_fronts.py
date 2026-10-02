"""Independent numeric full singleton cover for one heavy-chain HIGH seed.

Separate scalar gates, all legal equal-merge orders, complete 157-state images
and original LOW cubes. No producer imports. Necessary targets, not solutions.
"""
from collections import Counter
import hashlib
from itertools import combinations
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


def gate(x, a, b):
    if x >> a & 1 and not (x >> b & 1):
        x ^= (1 << a) | (1 << b)
    return x


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def table(word, ports):
    index = {p: j for j, p in enumerate(ports)}
    rows = []
    for x in range(1 << len(ports)):
        for a, b in word:
            x = gate(x, index[a], index[b])
        rows.append(x)
    return tuple(rows)


def all_equal_tails(classes):
    histories = []
    controls = 0
    def visit(state, word):
        nonlocal controls
        if len(state) == 1:
            need(state == ((11, 9),) and len(word) == 3, 'Heavy tail root differs')
            histories.append(word)
            return
        for i, j in combinations(range(len(state)), 2):
            controls += 1
            a, da = state[i]
            b, db = state[j]
            if da != db:
                continue
            fresh = tuple(sorted([r for k, r in enumerate(state) if k not in (i, j)] + [(b, da+1)]))
            visit(fresh, word + [[a, b]])
    visit(tuple(sorted(classes)), [])
    need(len(histories) == 1 and controls == 10, 'Complete heavy tail event cover differs')
    return histories, controls


def main():
    operations_allow()
    started = time.monotonic()
    deadline = started + 45
    index = int(sys.argv[1])
    cache_record = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())
    cache = cache_record['scalar_cache']
    need(digest(cache) == cache_record['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01', 'Independent base cache differs')
    p = json.loads((OUT/f'branch{index:02}.json').read_text())
    screen = json.loads((OUT/f'cuts{index:02}.json').read_text())
    front = json.loads((OUT/f'heavy-fronts{index:02}.json').read_text())
    need(digest(front['survivors']) == front['survivors_sha256'] and
         digest(front['rejections']) == front['rejections_sha256'], 'Front list digest differs')
    states = [core for core, original, correct in cache['full_core_witnesses']]
    state_index = {x: i for i, x in enumerate(states)}
    domains = {lo: {state_index[x & 1023] for x in values}
               for lo, values in cache['original_LOW_domains']}
    need(len(states) == 157 and len(domains) == 39, 'Original scalar image cover incomplete')
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    initial = list(states)
    for a, b in p['HIGH_word']:
        need(a < b and live[a] == live[b], 'HIGH seed not standard/equal')
        del live[a]
        live[b] += 1
        initial = [gate(x, a-2, b-2) for x in initial]
    need(sorted(live.values()) == [6, 6, 6, 8], 'Not a heavy-chain seed')
    dead = tuple(port for port in range(2, 12) if port not in live)
    need(list(dead) == p['dead_preparation_ports'], 'Six-port preparation map differs')

    def inactive(values, event):
        a, b = event
        inversions = {i for i, x in enumerate(values) if (x >> (a-2) & 1) > (x >> (b-2) & 1)}
        return next((lo for lo, domain in domains.items() if not inversions & domain), None)

    def verify_reject(record, values, event, literal):
        lo = record['original_LOW_mask']
        need(lo in domains, 'Invalid original LOW witness')
        if record['kind'] == 'WHOLE_ORIGINAL_LOW_IDENTITY':
            a, b = event
            need(all((values[i] >> (a-2) & 1) <= (values[i] >> (b-2) & 1)
                     for i in domains[lo]), 'Claimed whole-cube identity fails')
            return
        need(record['kind'] == 'TIGHT_ORIGINAL_LOW_FREE_PIVOT_CUT', 'Unknown rejection kind')
        port = record['pivot_port']
        need(2 <= port <= 11, 'Invalid free pivot')
        # Apply the prefix on full eleven-free-bit original images, keeping12.
        conditional = set(dict(cache['original_LOW_domains'])[lo])
        for a, b in literal[len(cache['prefix']):]:
            need(any((x >> (a-2) & 1) > (x >> (b-2) & 1) for x in conditional),
                 'Free-cut prefix has an unrecorded original identity')
            conditional = {gate(x, a-2, b-2) for x in conditional}
        pivot = port-2
        need(all(all((x >> q & 1) <= (x >> pivot & 1) for q in range(pivot)) and
                 all((x >> pivot & 1) <= (x >> q & 1) for q in range(pivot+1, 11))
                 for x in conditional), 'Actual original free-pivot inequalities fail')
        original = record['full_original_boolean_witness']
        row = [original >> q & 1 for q in range(13)]
        for a, b in literal:
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        need(row[port] != int(original.bit_count() >= 13-port), 'Wrong-rank witness is correct')

    survived = {}
    rejected = {}
    for r in front['survivors']:
        key = (r['function_id'], tuple(r['singleton']))
        need(key not in survived, 'Surviving front duplicated')
        survived[key] = r
    for r in front['rejections']:
        key = (r['function_id'], tuple(r['singleton']))
        need(key not in rejected and key not in survived, 'Rejected front duplicated')
        rejected[key] = r
    counts = Counter()
    metrics = Counter()
    covered = set()
    sizes = []
    budgets = Counter()
    image_hashes = []
    for fid in screen['retained_function_ids']:
        need(time.monotonic() < deadline, 'Incomplete independent front replay:45s guard')
        if fid % 128 == 0:
            operations_allow()
        f = p['functions'][fid]
        preparation = f['shortest_word']
        values = initial
        for a, b in preparation:
            need(inactive(values, [a, b]) is None, 'Preparation witness inactive on original cube')
            values = [gate(x, a-2, b-2) for x in values]
        counts['eligible_preparation_functions'] += 1
        for high, cost in sorted(live.items()):
            if cost != 6:
                continue
            for free in dead:
                single = sorted([high, free])
                key = (fid, tuple(single))
                counts['candidate_singleton_heads'] += 1
                literal_head = cache['prefix'] + p['HIGH_word'] + preparation + [single]
                if key in rejected and rejected[key]['stage'] == 'HEAD':
                    r = rejected[key]
                    verify_reject(r, values, single, literal_head)
                    counts['head_' + r['kind']] += 1
                    covered.add(key)
                    continue
                need(inactive(values, single) is None, 'Unreported head identity')
                head = [gate(x, single[0]-2, single[1]-2) for x in values]
                after = dict(live)
                del after[high]
                after[max(single)] = 7
                need(sorted(after.values()) == [6, 6, 7, 8] and sum(1 << d for d in after.values()) == 512,
                     'Head fails saturated HIGH costs')
                histories, controls = all_equal_tails(sorted(after.items()))
                counts['active_uncut_singleton_heads'] += 1
                counts['candidate_complete_tails'] += 1
                metrics['tail_orders'] += len(histories)
                metrics['tail_event_controls'] += controls
                need(key in survived or key in rejected, 'Candidate head silently missing')
                r = survived[key] if key in survived else rejected[key]
                tail = r['HIGH_tail']
                leaves = sorted(after)
                need(all(a < b and a in leaves and b in leaves for a, b in tail),
                     'Tail has a nonstandard gate or port outside the live leaves')
                need(table(tail, leaves) == table(histories[0], leaves) and len(tail) == 3,
                     'Tail misses its complete16-row legal equal-merge function')
                current = head
                for t, event in enumerate(tail):
                    if key in rejected and r['tail_event_index'] == t:
                        verify_reject(r, current, event, literal_head + tail[:t+1])
                        counts['tail_' + r['kind']] += 1
                        covered.add(key)
                        break
                    need(inactive(current, event) is None, 'Unreported tail original-cube identity')
                    current = [gate(x, event[0]-2, event[1]-2) for x in current]
                if key in rejected:
                    continue
                need(all((x >> 9 & 1) == int(states[i].bit_count() >= 1) for i, x in enumerate(current)),
                     'Full global second-largest statistic fails')
                image = sorted({x & 511 for x in current})
                need(image == r['nine_core_states'] and digest(image) == r['nine_core_sha256'],
                     'Complete nine-core image differs')
                literal = literal_head + tail
                need(literal == r['prefix'] and digest(literal) == r['prefix_sha256'] and
                     len(literal) == r['prefix_length'] == 32 + len(preparation) and
                     r['remaining_gate_budget'] == 44-len(literal), 'Literal prefix or gate budget differs')
                need(r['global_port2_correct'] == all((x & 1) == int(states[i].bit_count() >= 10)
                     for i, x in enumerate(current)), 'Full third statistic flag differs')
                counts['surviving_complete_fronts'] += 1
                metrics['complete_scalar_core_inputs'] += 157
                sizes.append(len(image))
                budgets[r['remaining_gate_budget']] += 1
                image_hashes.append(r['nine_core_sha256'])
                covered.add(key)
    need(covered == set(survived) | set(rejected) and dict(counts) == front['census'],
         'Complete independently covered candidate census differs')
    finite = {'branch_index': index, 'HIGH_word': p['HIGH_word'], 'census': dict(counts),
              'metrics': dict(metrics), 'producer_front_sha256': front['finite_sha256'],
              'complete_image_hashes_sha256': digest(image_hashes),
              'front_image_size_range': [min(sizes, default=0), max(sizes, default=0)],
              'remaining_gate_budgets': dict(sorted(budgets.items()))}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_HEAVY_TWO_PRIOR_SINGLETON_TAIL_ORIGINAL_CUBE_AND_FULL_IMAGE_COVER_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'One heavy-chain two-prior necessary frontier; retained target feasibility and sorting exclusion remain unresolved.',
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False}
    suffix = '-O' if not __debug__ else ''
    (OUT/f'heavy-checked{index:02}{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True))


if __name__ == '__main__':
    main()
