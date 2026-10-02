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

    pilot = json.loads((ROOT/'work/two-prior-high-six-port-pilot.json').read_text())
    word = pilot['HIGH_word']
    need(next(s for s in seed_checks if s['HIGH_word'] == word)[
         'active_on_all_original_tight_LOW_cubes'], 'Pilot seed is itself an original-cube identity')
    live = dict(costs)
    for a, b in word:
        need(a < b and live[a] == live[b], 'Pilot has a non-equal or nonstandard seed')
        del live[a]
        live[b] += 1
    dead = tuple(p for p in range(2, 12) if p not in live)
    need(list(dead) == pilot['dead_preparation_ports'] and len(dead) == 6,
         'Six-port preparation map differs')
    need([list(pair) for pair in sorted(live.items())] == pilot['HIGH_live_costs'],
         'Live HIGH cost map differs')

    projected = []
    minimum_tests = []
    for mask, domain in original_domains:
        post = set(domain)
        for a, b in word:
            post = {gate(x, a - 2, b - 2) for x in post}
        tests = {(sum((x >> (p - 2) & 1) << j for j, p in enumerate(dead)),
                  int(x == 2047)) for x in post}
        projected.append({x for x, value in tests})
        minimum_tests.append((mask, tests))

    complete_global = []
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
        for a, b in word:
            exchange(row, a, b)
        local = sum(row[p] << j for j, p in enumerate(dead))
        complete_global.append((original, local, int(original.bit_count() >= 11)))
    need(len(full_core) == 157 and digest(sorted(full_core)) ==
         '372c4c20ad7e72a8c9a39ae6caf878c7fcdee1628f94f5a5499ca54a39cda8c8',
         'Independent complete global image differs')
    wrong_tests = sorted({(local, correct) for original, local, correct in complete_global})

    def lock_for(f):
        wrong = any((f[x] & 1) != correct for x, correct in wrong_tests)
        if not wrong:
            return None
        return next((mask for mask, tests in minimum_tests if all(
            (f[x] & 1) == correct for x, correct in tests)), None)

    identity = tuple(range(64))
    queue = deque([identity])
    words = {identity: ()}
    census = Counter()
    absorbed = {}
    gates = tuple(combinations(range(6), 2))
    deadline = time.monotonic() + 45
    while queue:
        need(time.monotonic() <= deadline, 'Incomplete independent pilot: time guard')
        f = queue.popleft()
        census['expanded_full_functions'] += 1
        lock = lock_for(f)
        if lock is not None:
            absorbed[f] = lock
            census['minimum_lock_absorbed'] += 1
            continue
        for a, b in gates:
            active = all(any((f[x] >> a & 1) > (f[x] >> b & 1) for x in domain)
                         for domain in projected)
            if not active:
                census['inactive_original_domain_edges'] += 1
                continue
            fresh = tuple(gate(x, a, b) for x in f)
            need(fresh != f, 'Admissible comparator is an identity')
            census['admissible_edges'] += 1
            if fresh not in words:
                words[fresh] = words[f] + ((dead[a], dead[b]),)
                queue.append(fresh)
    supplied = {}
    for record in pilot['functions']:
        proposed_word = record['shortest_word']
        f = table(proposed_word, dead)
        need(f not in supplied and f in words and len(proposed_word) == len(words[f]),
             'Supplied function is duplicate, missing or has nonminimal word')
        columns = record['full_six_variable_columns']
        need(f == tuple(sum((c >> x & 1) << j for j, c in enumerate(columns)) for x in range(64)),
             'Supplied whole six-input function differs')
        current = identity
        for a, b in proposed_word:
            need(a < b and a in dead and b in dead and lock_for(current) is None,
                 'Witness is nonstandard or passes an absorbed obstruction')
            i, j = dead.index(a), dead.index(b)
            need(all(any((current[x] >> i & 1) > (current[x] >> j & 1) for x in domain)
                     for domain in projected), 'Witness gate inactive on an original LOW cube')
            current = tuple(gate(x, i, j) for x in current)
        need(current == f, 'Full representative witness replay differs')
        supplied[f] = record
    need(set(words) == set(supplied) and len(words) == pilot['complete_full_functions_seen'],
         'Complete independent function set differs')
    need(dict(census) == pilot['census'], 'Independent full transition census differs')
    supplied_locks = {}
    scalar_witnesses = []
    for proposal in pilot['minimum_lock_proposals']:
        f = table(proposal['word'], dead)
        mask = proposal['original_LOW_mask']
        tests = dict(minimum_tests)[mask]
        need(f not in supplied_locks and f in absorbed and all(
            (f[x] & 1) == correct for x, correct in tests), 'Wrong original conditional-minimum lock')
        original = next(original for original, local, correct in complete_global
                        if (f[local] & 1) != correct)
        row = [original >> p & 1 for p in range(13)]
        for a, b in prefix + word + proposal['word']:
            exchange(row, a, b)
        need(row[2] != int(original.bit_count() >= 11), 'Full original-input witness does not fail')
        scalar_witnesses.append([mask, original])
        supplied_locks[f] = mask
    need(set(supplied_locks) == set(absorbed), 'Absorbed function set differs')
    cache = {'original_LOW_domains': [[mask, sorted(domain)] for mask, domain in original_domains],
             'full_core_witnesses': [[core, *full_core_witnesses[core]] for core in sorted(full_core)],
             'prefix': prefix, 'seed_checks': seed_checks}
    (ROOT/'work/two-prior-independent-original-cubes.json').write_text(
        json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                    'scalar_cache': cache, 'scalar_cache_sha256': digest(cache)}, indent=2) + '\n')
    finite = {'complete_event_orders': len(orders), 'distinct_event_functions': len(numeric_functions),
              'original_LOW_cube_assignments': 39 * 2048,
              'independent_original_cube_cache_sha256': digest(cache),
              'seed_checks': seed_checks, 'pilot_HIGH_word': word,
              'pilot_complete_functions': len(words), 'pilot_census': dict(census),
              'pilot_numeric_function_sha256': digest(sorted(words)),
              'pilot_scalar_original_lock_witnesses_sha256': digest(scalar_witnesses),
              'shortest_lengths': dict(sorted(Counter(map(len, words.values())).items()))}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'INDEPENDENT_COMPLETE_ORIGINAL_CUBE_SEEDS_AND_ONE_MINIMUM_ABSORBING_PILOT_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic() - start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Complete 25 two-event cover and ONE seed six-port preparation closure only; no singleton/tail or sorting exclusion.',
              'same_author_algorithmic_independence': True,
              'external_person_review_claimed': False}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
