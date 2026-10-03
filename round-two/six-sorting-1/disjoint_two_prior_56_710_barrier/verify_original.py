"""Independent scalar check of original two-HIGH seeds and ONE pilot closure.

No producer imports. Whole 64-row functions and actual original eleven-free
LOW cubes, not just marker profiles. Same author; no external review.
"""
from collections import Counter, deque
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def exchange(row, a, b):
    if row[a] > row[b]:
        row[a], row[b] = row[b], row[a]


def gate(x, a, b):
    if x >> a & 1 and not (x >> b & 1):
        x ^= (1 << a) | (1 << b)
    return x


def table(word, ports):
    indices = {p: i for i, p in enumerate(ports)}
    rows = []
    for initial in range(1 << len(ports)):
        x = initial
        for a, b in word:
            x = gate(x, indices[a], indices[b])
        rows.append(x)
    return tuple(rows)


def main():
    start = time.monotonic()
    fixture = json.loads((ROOT/'prior/fixture.json').read_text())
    prefix = fixture['B23'] + fixture['LOW_suffixes']['4']
    need(len(prefix) == 26, 'Literal prefix differs')
    cover = json.loads((ROOT/'work/two-prior-high-complete-cover.json').read_text())
    proposed = cover['canonical_words']
    costs = dict(fixture['initial_HIGH'])
    orders = []
    for a, b in combinations(sorted(costs), 2):
        if costs[a] != costs[b]:
            continue
        next_costs = {p: c for p, c in costs.items() if p != a}
        next_costs[b] = costs[b] + 1
        for c, d in combinations(sorted(next_costs), 2):
            if next_costs[c] == next_costs[d]:
                orders.append(((a, b), (c, d)))
    numeric_functions = {table(w, sorted(costs)) for w in orders}
    need(len(orders) == 40 and len(proposed) == 25 and
         numeric_functions == {table(w, sorted(costs)) for w in proposed} and
         len(numeric_functions) == 25, 'Complete two-event cover differs')
    need(digest(sorted(numeric_functions)) == cover['full_function_set_sha256'],
         'Complete numeric function cover digest differs')

    original_domains = []
    for lo, hi in combinations(range(13), 2):
        reference = [0] * 13
        reference[lo], reference[hi] = -2, -1
        touched = 0
        for t, (a, b) in enumerate(prefix):
            touched |= int(reference[a] < 0 or reference[b] < 0) << t
            exchange(reference, a, b)
        need(touched.bit_count() <= 9, 'LOW ceiling exceeded')
        if touched.bit_count() != 9:
            continue
        free = [p for p in range(13) if p not in (lo, hi)]
        full_states = set()
        active = 0
        for x in range(2048):
            row = [0] * 13
            row[lo], row[hi] = -2, -1
            for j, p in enumerate(free):
                row[p] = x >> j & 1
            actual_touched = 0
            for t, (a, b) in enumerate(prefix):
                marked = row[a] < 0 or row[b] < 0
                actual_touched |= int(marked) << t
                if not marked and row[a] > row[b]:
                    active |= 1 << t
                exchange(row, a, b)
            need(actual_touched == touched and row[:2] == [-2, -1],
                 'Original LOW route or ranks depend on free assignment')
            full_states.add(sum(row[p] << (p - 2) for p in range(2, 13)))
        need(touched | active == (1 << 26) - 1, 'Base has a redundant tight LOW gate')
        original_domains.append(((1 << lo) | (1 << hi), full_states))
    original_domains.sort()
    need(len(original_domains) == 39, 'Complete original D9 family differs')

    seed_checks = []
    for word in proposed:
        states = [(mask, set(domain)) for mask, domain in original_domains]
        steps = []
        for a, b in word:
            inactive = [mask for mask, domain in states if not any(
                (x >> (a - 2) & 1) > (x >> (b - 2) & 1) for x in domain)]
            steps.append({'gate': [a, b], 'inactive_original_LOW_masks': inactive})
            states = [(mask, {gate(x, a - 2, b - 2) for x in domain})
                      for mask, domain in states]
        seed_checks.append({'HIGH_word': word, 'steps': steps,
                            'active_on_all_original_tight_LOW_cubes': all(
                                not step['inactive_original_LOW_masks'] for step in steps)})

    full_core = set()
    full_core_witnesses = {}
    for original in range(8192):
        row = [original >> p & 1 for p in range(13)]
        for a, b in prefix:
            exchange(row, a, b)
        need(row[0] == int(original == 8191) and row[1] == int(original.bit_count() >= 12)
             and row[12] == int(original != 0), 'Global held ranks differ')
        core = sum(row[p] << (p - 2) for p in range(2, 12))
        full_core.add(core)
        need(int(core == 1023) == int(original.bit_count() >= 11),
             'Global third statistic is not determined by complete core state')
        full_core_witnesses.setdefault(core, [original, int(original.bit_count() >= 11)])
    need(len(full_core) == 157 and digest(sorted(full_core)) ==
         '372c4c20ad7e72a8c9a39ae6caf878c7fcdee1628f94f5a5499ca54a39cda8c8',
         'Independent complete global image differs')
    cache = {'original_LOW_domains': [[mask, sorted(domain)] for mask, domain in original_domains],
             'full_core_witnesses': [[core, *full_core_witnesses[core]] for core in sorted(full_core)],
             'prefix': prefix, 'seed_checks': seed_checks}
    need(digest(cache) == '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01',
         'Whole original cache differs from frozen scalar baseline')
    need(proposed[1] == [[5, 6], [7, 9]] and seed_checks[1]['active_on_all_original_tight_LOW_cubes'],
         'Selected disjoint seed is not completely active')
    (ROOT/'work/two-prior-independent-original-cubes.json').write_text(
        json.dumps({'agent':'six-sorting-1','role':'researcher',
                    'scalar_cache':cache,'scalar_cache_sha256':digest(cache)},indent=2)+'\n')
    finite = {'schema':'whole-original-L4-base-scalar-v1','full_Boolean_inputs':8192,
              'original_LOW_cube_assignments':39*2048,'full_core_image_sha256':digest(sorted(full_core)),
              'scalar_cache_sha256':digest(cache),'selected_HIGH_word':proposed[1],
              'selected_seed_active_on_all_original_domains':True}
    need(time.monotonic()-start < 45,'Incomplete45s original reconstruction')
    suffix='-O' if not __debug__ else ''
    result={'agent':'six-sorting-1','role':'researcher','finite':finite,'finite_sha256':digest(finite),
            'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/f'work/original-checked{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
