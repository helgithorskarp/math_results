"""Independent full 64-row closure and original-cube lock checker.

Base cache was produced by all original scalar input/cube replays, checked
normally and with -O. No packed producer imports or image-profile assumptions.
"""
from collections import Counter, deque
from itertools import combinations
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


def gate(x, a, b):
    if x >> a & 1 and not (x >> b & 1):
        x ^= (1 << a) | (1 << b)
    return x


def table(word, dead):
    indices = {p: i for i, p in enumerate(dead)}
    rows = []
    for x in range(64):
        for a, b in word:
            x = gate(x, indices[a], indices[b])
        rows.append(x)
    return tuple(rows)


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def check(index, cache):
    started = time.monotonic()
    deadline = started + 45
    proposal = json.loads((OUT/f'branch{index:02}.json').read_text())
    word = proposal['HIGH_word']
    need(proposal['complete'] and not proposal['queue_unexpanded'], 'Producer closure incomplete')
    seed = cache['seed_checks'][index]
    need(seed['HIGH_word'] == word and seed['active_on_all_original_tight_LOW_cubes'],
         'Original-cube seed was not independently checked')
    live = {5: 6, 6: 6, 7: 6, 9: 6, 10: 6, 11: 7}
    for a, b in word:
        need(a < b and live[a] == live[b], 'Nonstandard or unequal initial HIGH event')
        del live[a]
        live[b] += 1
    dead = tuple(p for p in range(2, 12) if p not in live)
    need(list(dead) == proposal['dead_preparation_ports'] and
         [list(p) for p in sorted(live.items())] == proposal['HIGH_live_costs'], 'Physical port map differs')
    minimum_tests = []
    projected = []
    for mask, domain in cache['original_LOW_domains']:
        post = set(domain)
        for a, b in word:
            need(any((x >> (a-2) & 1) > (x >> (b-2) & 1) for x in post),
                 'Initial HIGH gate inactive on one original LOW cube')
            post = {gate(x, a-2, b-2) for x in post}
        tests = tuple(sorted({(sum((x >> (p-2) & 1) << j for j, p in enumerate(dead)),
                               int(x == 2047)) for x in post}))
        minimum_tests.append((mask, tests))
        projected.append(tuple(sorted({x for x, value in tests})))
    unique_projected = tuple(sorted(set(projected)))
    global_tests = []
    global_original = []
    for x, original, correct in cache['full_core_witnesses']:
        for a, b in word:
            x = gate(x, a-2, b-2)
        local = sum((x >> (p-2) & 1) << j for j, p in enumerate(dead))
        global_tests.append((local, correct))
        global_original.append((local, original, correct))
    global_tests = sorted(set(global_tests))
    minimum_cache = {}

    def minimum(f):
        column = tuple(x & 1 for x in f)
        if column not in minimum_cache:
            lock = next((mask for mask, tests in minimum_tests
                         if all(column[x] == correct for x, correct in tests)), None)
            wrong = any(column[x] != correct for x, correct in global_tests)
            minimum_cache[column] = (lock, wrong)
        return minimum_cache[column]

    def activity(f, a, b):
        return all(any((f[x] >> a & 1) > (f[x] >> b & 1) for x in domain)
                   for domain in unique_projected)

    initial = tuple(range(64))
    queue = deque([initial])
    words = {initial: ()}
    absorbed = {}
    census = Counter()
    pairs = tuple(combinations(range(6), 2))
    next_pause_check = started
    while queue:
        now = time.monotonic()
        need(now < deadline, 'Incomplete independent branch: time guard')
        if now >= next_pause_check:
            operations_allow()
            next_pause_check = now + .5
        f = queue.popleft()
        census['expanded_full_functions'] += 1
        lock, wrong = minimum(f)
        if lock is not None and wrong:
            absorbed[f] = lock
            census['minimum_lock_absorbed'] += 1
            continue
        census['correct_global_third_with_conditional_minimum' if lock is not None else
               'no_original_conditional_minimum'] += 1
        for a, b in pairs:
            if not activity(f, a, b):
                census['inactive_original_domain_edges'] += 1
                continue
            fresh = tuple(gate(x, a, b) for x in f)
            need(fresh != f, 'Admissible full-function transition is identity')
            census['admissible_edges'] += 1
            if fresh not in words:
                words[fresh] = words[f] + ((dead[a], dead[b]),)
                queue.append(fresh)
    need(dict(census) == proposal['census'], 'Complete independent transition census differs')
    supplied = {}
    for record in proposal['functions']:
        representative = record['shortest_word']
        f = table(representative, dead)
        need(f in words and f not in supplied and len(representative) == len(words[f]),
             'Function missing, duplicated or representative nonminimal')
        need(f == tuple(sum((c >> x & 1) << j for j, c in enumerate(record['full_six_variable_columns']))
                        for x in range(64)), 'Whole six-input columns differ from scalar function')
        current = initial
        for a, b in representative:
            lock, wrong = minimum(current)
            need(not (lock is not None and wrong), 'Witness passes an absorbed obstruction')
            need(a < b and a in dead and b in dead, 'Nonstandard witness or wrong preparation port')
            i, j = dead.index(a), dead.index(b)
            need(activity(current, i, j), 'Representative gate inactive on an original LOW cube')
            current = tuple(gate(x, i, j) for x in current)
        need(current == f, 'Representative whole-function replay differs')
        supplied[f] = record
    need(set(supplied) == set(words) and len(words) == proposal['full_functions_seen'],
         'Complete independent function set differs')
    need(digest(proposal['functions']) == proposal['full_functions_sha256'], 'Producer list digest differs')
    supplied_locks = {}
    witness_rows = []
    tests_by_mask = dict(minimum_tests)
    for record in proposal['minimum_lock_proposals']:
        f = table(record['word'], dead)
        mask = record['original_LOW_mask']
        need(f in absorbed and f not in supplied_locks and all(
            (f[x] & 1) == correct for x, correct in tests_by_mask[mask]), 'Wrong original minimum lock')
        original = next(original for local, original, correct in global_original
                        if (f[local] & 1) != correct)
        row = [original >> p & 1 for p in range(13)]
        for a, b in cache['prefix'] + word + record['word']:
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        need(row[2] != int(original.bit_count() >= 11), 'Scalar whole-original witness fails to reject')
        columns = [sum((f[x] >> j & 1) << x for x in range(64)) for j in range(6)]
        need(digest(columns) == record['full_function_sha256'], 'Absorbed full-function digest differs')
        supplied_locks[f] = mask
        witness_rows.append([mask, original])
    need(set(absorbed) == set(supplied_locks), 'Complete lock-function lists differ')
    lengths = dict(sorted(Counter(map(len, words.values())).items()))
    need({str(k): v for k, v in lengths.items()} == proposal['shortest_lengths'],
         'Complete shortest-word distribution differs')
    finite = {'branch_index': index, 'HIGH_word': word, 'dead_preparation_ports': dead,
              'full_functions': len(words), 'census': dict(census), 'shortest_lengths': lengths,
              'scalar_numeric_function_sha256': digest(sorted(words)),
              'scalar_original_lock_witnesses_sha256': digest(witness_rows),
              'producer_function_list_sha256': proposal['full_functions_sha256'],
              'projected_original_cube_images': len(unique_projected)}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'INDEPENDENT_COMPLETE_MINIMUM_ABSORBING_SIX_VARIABLE_CLOSURE_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic() - started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False,
              'scope': 'One complete original-cube preparation closure; no singleton/tail or branch/global sorting exclusion.'}
    suffix = '-O' if not __debug__ else ''
    (OUT/f'checked{index:02}{suffix}.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True), flush=True)


def main():
    operations_allow()
    first, last = map(int, sys.argv[1:3])
    need(0 <= first < last <= 25, 'Bounded branch range required')
    record = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())
    cache = record['scalar_cache']
    need(digest(cache) == record['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01',
         'Original scalar cache differs from normal/O checked reconstruction')
    need(len(cache['original_LOW_domains']) == 39 and len(cache['full_core_witnesses']) == 157,
         'Independent scalar base cache incomplete')
    for index in range(first, last):
        check(index, cache)


if __name__ == '__main__':
    main()
