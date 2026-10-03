"""Packed full six-variable producer with original LOW-cube activity.

Run serial bounded branch ranges. Completion is mathematical function closure;
operational guards mean incomplete, never an exclusion. Generated arrays private.
"""
from collections import Counter, deque
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


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def produce(index, word, base, domains):
    start = time.monotonic()
    columns = [sum((x >> j & 1) << i for i, x in enumerate(base)) for j in range(10)]
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    for a, b in word:
        need(a < b and live[a] == live[b], 'Two-event route is not standard/equal')
        active = columns[a-2] & ~columns[b-2]
        need(all(active & r['core_image_index_mask'] for r in domains),
             'Initial HIGH gate identity on original tight LOW cube')
        del live[a]
        live[b] += 1
        columns[a-2], columns[b-2] = columns[a-2] & columns[b-2], columns[a-2] | columns[b-2]
    dead = tuple(p for p in range(2, 12) if p not in live)
    need(len(dead) == 6 and dead[0] == 2, 'Six-port preparation map differs')
    patterns = [sum((columns[p-2] >> i & 1) << j for j, p in enumerate(dead)) for i in range(157)]
    bins = [sum(1 << i for i, x in enumerate(patterns) if x == k) for k in range(64)]
    minimum = sum(1 << i for i, x in enumerate(base) if x == 1023)
    initial = tuple(sum((x >> j & 1) << x for x in range(64)) for j in range(6))
    queue = deque([initial])
    words = {initial: ()}
    locks = []
    census = Counter()
    next_pause_check = start
    deadline = start + 5
    complete = True
    reason = None
    while queue:
        now = time.monotonic()
        if now > deadline or len(words) >= 20000:
            complete = False
            reason = 'INCOMPLETE_OPERATIONAL_TIME_OR_STATE_GUARD'
            break
        if now >= next_pause_check:
            operations_allow()
            next_pause_check = now + .5
        f = queue.popleft()
        census['expanded_full_functions'] += 1
        images = [sum(bins[k] for k in range(64) if c >> k & 1) for c in f]
        wrong = images[0] ^ minimum
        lock = next((r['original_LOW_mask'] for r in domains
                     if not wrong & r['core_image_index_mask']), None)
        if lock is not None and wrong:
            locks.append({'full_function_sha256': digest(f), 'word': words[f],
                          'original_LOW_mask': lock})
            census['minimum_lock_absorbed'] += 1
            continue
        census['correct_global_third_with_conditional_minimum' if lock is not None else
               'no_original_conditional_minimum'] += 1
        for i, j in combinations(range(6), 2):
            active = images[i] & ~images[j]
            if not all(active & r['core_image_index_mask'] for r in domains):
                census['inactive_original_domain_edges'] += 1
                continue
            fresh = list(f)
            fresh[i], fresh[j] = f[i] & f[j], f[i] | f[j]
            fresh = tuple(fresh)
            need(fresh != f, 'Admissible six-port comparator is an identity')
            census['admissible_edges'] += 1
            if fresh not in words:
                words[fresh] = words[f] + ((dead[i], dead[j]),)
                queue.append(fresh)
    functions = [{'full_six_variable_columns': f, 'shortest_word': w} for f, w in sorted(words.items())]
    finite = {'branch_index': index, 'HIGH_word': word, 'HIGH_live_costs': sorted(live.items()),
              'dead_preparation_ports': dead, 'complete': complete, 'incomplete_reason': reason,
              'full_functions_seen': len(words), 'queue_unexpanded': len(queue),
              'census': dict(census), 'shortest_lengths': dict(sorted(Counter(map(len, words.values())).items())),
              'full_functions_sha256': digest(functions), 'minimum_lock_proposals_sha256': digest(locks)}
    record = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_PRIVATE_MINIMUM_ABSORBING_SIX_VARIABLE_PREPARATION_CLOSURE' if complete else reason,
              **finite, 'functions': functions, 'minimum_lock_proposals': locks,
              'seconds': time.monotonic() - start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'finite_sha256': digest(finite), 'source_dependency': 'f47e57677011488966488f68228562643bed2b3c',
              'scope': 'Only preparation functions before first strict singleton, exactly two earlier equal HIGH merges after literal P4; not yet independently checked or a sorting exclusion.'}
    (OUT/f'branch{index:02}.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k not in ('functions', 'minimum_lock_proposals')}, sort_keys=True), flush=True)
    return complete


def main():
    operations_allow()
    OUT.mkdir(exist_ok=True)
    first, last = map(int, sys.argv[1:3])
    need(0 <= first < last <= 25, 'Bounded branch range required')
    cover = json.loads((ROOT/'work/two-prior-high-complete-cover.json').read_text())
    base = json.loads((ROOT/'prior/work/low26-partner4-construction-pilot.json').read_text())['core_states']
    domains = json.loads((ROOT/'prior/work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    need(len(base) == 157 and len(domains) == 39, 'Published base inputs differ')
    for i in range(first, last):
        if not produce(i, cover['canonical_words'][i], base, domains):
            raise ValueError(f'Branch {i} incomplete: preserve arrays; no exclusion')


if __name__ == '__main__':
    main()
