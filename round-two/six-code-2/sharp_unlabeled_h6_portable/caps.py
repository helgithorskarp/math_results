"""Complete partial-cap carrier for one fixed noncontained old four-tail Q.

six-code-2, researcher. New source preserving sealed one/two/pencil work.
For h=6 every leaf is a literal64-word packing and seven compatible
cores give70. Zero/one extra inputs retain the old complete carrier bytes.
Preparation alone gives no clique/absence conclusion.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def points(w):
    return tuple(p for p in range(17) if w >> p & 1)


def mask(ps):
    return sum(1 << p for p in ps)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--q', type=int, required=True)
    parser.add_argument('--extra-empty-parents', type=int, nargs='+', default=[])
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    need(args.resume == args.work.exists(), 'use a new work directory or explicit resume')
    args.work.mkdir(parents=True, exist_ok=args.resume)
    begin, states = time.monotonic(), 0
    raw = args.parent.read_bytes()
    old = tuple(sorted(json.loads(raw)['words']))
    need(len(old) == len(set(old)) == 68 and all(0 <= w < 1 << 17 and w.bit_count() == 5 for w in old),
         'literal Steiner parent word domain')
    occupied = [mask(t) for w in old for t in combinations(points(w), 3)]
    triple_ids = {mask(t): i for i, t in enumerate(combinations(range(17), 3))}
    need(len(occupied) == len(set(occupied)) == 680 and set(occupied) == set(triple_ids),
         'literal complete680-triple parent')
    q = args.q
    need(type(q) is int and 0 <= q < 1 << 17 and q.bit_count() == 4 and
         not any(q & w == q for w in old), 'old four-tail must be noncontained')
    holes = tuple(w for w in old if (q & w).bit_count() >= 3)
    need(len(holes) == 4 and all((q & w).bit_count() == 3 for w in holes),
         'noncontained Q has exactly four triple-blocking empty parents')
    q_blockers = holes
    extras = tuple(args.extra_empty_parents)
    need(len(extras) == len(set(extras)) <= 2 and all(type(w) is int and w in old and w not in holes for w in extras),
         'zero to two distinct extra empty parents outside the reserved four')
    if extras:
        holes = tuple(sorted(holes + extras))
    h = len(holes)
    need(h in (4, 5, 6), 'only four blockers with at most two extra empty parents')
    extra_one = extras[0] if len(extras) == 1 else None
    hole_ids = {old.index(w) for w in holes}
    pair_ids = {mask(p): i for i, p in enumerate(combinations(range(17), 2))}
    tail_pair_cache, tail_triple_cache = {}, {}

    def tail_resources(t):
        if t not in tail_pair_cache:
            tail_pair_cache[t] = sum(1 << pair_ids[mask(p)] for p in combinations(points(t), 2))
            tail_triple_cache[t] = sum(1 << triple_ids[mask(p)] for p in combinations(points(t), 3))
        return tail_pair_cache[t]

    old_set = set(old)
    eligible = []
    for ps in combinations(range(17), 5):
        cap = mask(ps)
        if cap in old_set or (cap & q).bit_count() > 2:
            continue
        sizes = [(cap & w).bit_count() for w in old]
        if not any(n >= 4 and i not in hole_ids for i, n in enumerate(sizes)):
            eligible.append((cap, sizes))
    need(len(eligible) > 0, 'physical prospective-cap domain empty')
    cores, cap_rows = [], []
    if args.resume:
        prior = json.loads((args.work / 'PARTIAL_CORES.json').read_bytes())
        need(tuple(prior['parent_words']) == old and tuple(prior['hole_words']) == holes and prior['noncontained_q'] == q,
             'resumable carrier input mismatch')
        cores, cap_rows = prior['cores'], prior['caps']
        need([c['cap'] for c in cap_rows] == [c for c, _ in eligible[:len(cap_rows)]],
             'resumable completed-cap prefix mismatch')
    start_cap = len(cap_rows)
    core_hist = Counter((tuple(c['hole_intersections']), c['required_parents'], c['core_count'])
                        for c in cap_rows)
    first = len(cores)

    def guard(completed):
        if states > 2_000_000 or time.monotonic() - begin >= 60:
            # Discard only the currently uncompleted cap's leaves; the exact
            # completed prefix is safe to resume without counting it twice.
            saved_cores = cores if completed else cores[:first]
            prefix = {'agent': 'six-code-2', 'role': 'researcher', 'parent_words': old,
                      'noncontained_q': q, 'hole_words': holes, 'caps': cap_rows, 'cores': saved_cores}
            (args.work / 'PARTIAL_CORES.json').write_bytes(encoded(prefix))
            receipt = {'agent': 'six-code-2', 'role': 'researcher',
                       'status': 'INCOMPLETE_NONCONTAINED_Q_CARRIER_NO_ABSENCE_CLAIM',
                       'states_this_pass': states, 'completed_cap_words': len(cap_rows),
                       'prepared_cores': len(saved_cores), 'initial_state_guard': 2_000_000,
                       'initial_whole_guard_seconds': 60, 'next_cap_index': len(cap_rows)}
            (args.work / 'PARTIAL.json').write_bytes(encoded(receipt))
            raise TimeoutError('INCOMPLETE initial60s/two-million-state noncontained-Q preparation guard')

    for cap_index in range(start_cap, len(eligible)):
        cap, sizes = eligible[cap_index]
        hole_sizes = tuple((cap & w).bit_count() for w in holes)
        parents = tuple(i for i, n in enumerate(sizes) if n >= 3 and i not in hole_ids)
        need(all(sizes[i] == 3 for i in parents), 'nonempty blocker has a triple')
        domains = []
        for i in parents:
            choices = []
            for p in points(cap & old[i]):
                tail = old[i] ^ (1 << p)
                need(tail.bit_count() == 4 and (tail & cap).bit_count() == 2, 'partial cap tail choice')
                if (tail & q).bit_count() <= 1:
                    choices.append((tail, tail_resources(tail)))
            need(len(choices) <= 3, 'at most three physical omissions per triple parent')
            domains.append(tuple(choices))
        first = len(cores)

        def visit(row, resources, tails):
            nonlocal states
            states += 1
            if states % 2048 == 0:
                guard(False)
            if row == len(parents):
                need(all((a & b).bit_count() <= 1 for a, b in combinations(tails, 2)),
                     'pair resource versus physical tail compatibility')
                removed = set(holes) | {old[i] for i in parents}
                words = tuple(sorted((old_set - removed) | {cap, q | (1 << 17)} | {t | (1 << 17) for t in tails}))
                need(len(words) == len(set(words)) == 70 - h and
                     all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)),
                     'literal positive66 fixed-Q four-empty-parent partial core')
                cores.append({'cap': cap, 'hole_intersections': hole_sizes, 'parents': parents, 'tails': tails,
                    'parent_mask': sum(1 << i for i in parents), 'pair_mask': resources,
                    'tail_triple_mask': sum(tail_triple_cache[t] for t in tails),
                    'cap_triple_mask': sum(1 << triple_ids[mask(t)] for t in combinations(points(cap), 3))})
                return
            for tail, pairs in domains[row]:
                if not resources & pairs:
                    visit(row + 1, resources | pairs, tails + (tail,))

        visit(0, 0, ())
        count = len(cores) - first
        core_hist[(hole_sizes, len(parents), count)] += 1
        cap_rows.append({'cap': cap, 'hole_intersections': hole_sizes,
                         'required_parents': len(parents), 'first_core': first, 'core_count': count})
        if len(cap_rows) % 64 == 0:
            guard(True)
    guard(True)
    packet = {'agent': 'six-code-2', 'role': 'researcher',
        'status': 'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_FOUR_EMPTY_STEINER_PARENTS',
        'parent_words': old, 'noncontained_q': q, 'hole_words': holes, 'hole_indices': sorted(hole_ids),
        'caps': cap_rows, 'cores': cores,
        'scope': 'One fixed noncontainedQ. All old-point non-design caps meetingQ in at most2 and with every four-intersection confined to its four blocking empty parents; all compatible required contained tails meetingQ in at most1. Includes zero-core caps. No graph/absence or all-Q normalization conclusion.'}
    if h == 5:
        packet.update({'status': 'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_FIVE_EMPTY_STEINER_PARENTS',
                       'reserved_Q_parent_words': q_blockers, 'additional_empty_parent': extra_one, 'h': h,
                       'scope': 'Literal noncontainedQ and exactly five specified empty parents: its four Q-triple blockers plus one extraD parent. Every prospective cap and required contained-tail assignment is included. No graph/absence or all-extra-parent conclusion.'})
    if h == 6:
        packet.update({'status': 'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_SIX_EMPTY_STEINER_PARENTS',
                       'reserved_Q_parent_words': q_blockers, 'additional_empty_parents': sorted(extras), 'h': h,
                       'scope': 'Literal noncontainedQ and exactly six specified empty parents: its four Q-triple blockers plus two extraD parents. Every prospective cap and required contained-tail assignment is included. No graph/absence, all-extra-pair or global endpoint conclusion.'})
    b = encoded(packet)
    (args.work / 'CORES.json').write_bytes(b)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': packet['status'],
        'parent_input_sha256': hashlib.sha256(raw).hexdigest(), 'noncontained_q': q, 'hole_words': holes,
        'hole_pair_intersections': [(a & b).bit_count() for a, b in combinations(holes, 2)], 'complete_cap_words': len(cap_rows),
        'complete_partial_cores': len(cores), 'zero_core_cap_words': sum(r['core_count'] == 0 for r in cap_rows),
        'core_count_histogram_by_hole_intersections': [list(h) + [p, k, n] for (h, p, k), n in sorted(core_hist.items())],
        'preparation_states_this_pass': states, 'resumed_completed_caps': start_cap,
        'carrier_bytes': len(b), 'carrier_sha256': hashlib.sha256(b).hexdigest(),
        'initial_whole_guard_seconds': 60, 'initial_state_guard': 2_000_000,
        'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'independent_carrier_audit': 'pending; literal leaf packing checks are same producer',
        'scope': packet['scope']}
    (args.work / 'SUMMARY.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
