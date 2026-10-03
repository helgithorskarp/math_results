"""Exact four-empty-parent contained-tail graph and cap cliques through six.

six-code-2, researcher. Credited inverse-graph/increasing-clique kernels from
sealed q_extra_graph.py. Q and its tail restrictions are absent; the physical
union has64+k words. Original60s/two-million guards unchanged.
A first literal70 is saved immediately and stops with no absence claim.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from physical_helpers import operations_guard


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--carrier', type=Path, required=True)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'new fixed-triple graph work directory required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    raw = args.carrier.read_bytes()
    data = json.loads(raw)
    need(data['status'] == 'COMPLETE_SINGLE_CAP_CARRIER_FOUR_FIXED_EMPTY_STEINER_PARENTS',
         'carrier incomplete or wrong scope')
    need(len(data['hole_words']) == len(set(data['hole_words'])) == 4, 'exact four-hole scope')
    cores = data['cores']
    n = len(cores)
    cap_occurrences, tail_occurrences = defaultdict(int), defaultdict(int)
    for i, c in enumerate(cores):
        cap_occurrences[c['cap']] |= 1 << i
        for tail in c['tails']:
            tail_occurrences[tail] |= 1 << i
    cap_forbidden, tail_forbidden = {}, {}

    def guard(stage, cursor, states=0):
        operations_guard()
        if states > 2_000_000 or time.monotonic() - begin >= 60:
            (args.work / 'PARTIAL.json').write_bytes(encoded({'agent': 'six-code-2', 'role': 'researcher',
                'status': 'INCOMPLETE_FIXED_FOUR_HOLE_GRAPH_OR_CLIQUE_SEARCH_NO_ABSENCE',
                'stage': stage, 'cursor': cursor, 'states': states,
                'carrier_sha256': hashlib.sha256(raw).hexdigest(),
                'initial_whole_guard_seconds': 60, 'initial_clique_state_guard': 2_000_000,
                'positive_sizes_saved': [k for k in range(64,71) if (args.work / f'WITNESS{k}.json').exists()]}))
            raise TimeoutError('INCOMPLETE fixed60s/two-million-state four-hole graph guard')

    for cap in cap_occurrences:
        bad = 0
        for other, bits in cap_occurrences.items():
            if (cap & other).bit_count() >= 3:
                bad |= bits
        for tail, bits in tail_occurrences.items():
            if (cap & tail).bit_count() >= 3:
                bad |= bits
        cap_forbidden[cap] = bad
        guard('cap-conflicts', cap)
    for tail in tail_occurrences:
        bad = 0
        for cap, bits in cap_occurrences.items():
            if (tail & cap).bit_count() >= 3:
                bad |= bits
        for other, bits in tail_occurrences.items():
            if tail != other and (tail & other).bit_count() >= 2:
                bad |= bits
        tail_forbidden[tail] = bad
        guard('tail-conflicts', tail)
    all_bits = (1 << n) - 1
    adjacency, row_digest = [], hashlib.sha256()
    for i, c in enumerate(cores):
        bad = cap_forbidden[c['cap']]
        for tail in c['tails']:
            bad |= tail_forbidden[tail]
        row = all_bits & ~bad
        need(not row >> i & 1, 'graph has self edge')
        adjacency.append(row)
        row_digest.update(encoded([i, format(row, 'x')]))
        if i % 512 == 0:
            guard('complete-adjacency', i)
    graph = {'agent': 'six-code-2', 'role': 'researcher', 'vertices': n,
        'status': 'COMPLETE_FIXED_FOUR_HOLE_PHYSICAL_INVERSE_GRAPH_SINGLE_PRODUCER',
        'edges': sum(row.bit_count() for row in adjacency) // 2,
        'hole_words': data['hole_words'], 'core_carrier_sha256': hashlib.sha256(raw).hexdigest(),
        'adjacency_hex': [format(row, 'x') for row in adjacency],
        'ordered_graph_row_sha256': row_digest.hexdigest()}
    gb = encoded(graph)
    (args.work / 'GRAPH.json').write_bytes(gb)
    old, holes = set(data['parent_words']), set(data['hole_words'])
    base = set(json.loads(args.parent.read_bytes())['base_words'])
    first = {k: None for k in range(64,71)}

    def positive(ids):
        target = 64 + len(ids)
        if first[target] is not None:
            return
        selected = [cores[i] for i in ids]
        removed = holes | {data['parent_words'][p] for c in selected for p in c['parents']}
        caps = {c['cap'] for c in selected}
        tails = {t for c in selected for t in c['tails']}
        words = tuple(sorted((old - removed) | caps | {t | (1 << 17) for t in tails}))
        need(len(words) == target and len(caps) == len(ids) and len(removed) == len(tails) + 4,
             'positive physical four-empty-parent normal form')
        need(all(w.bit_count() == 5 for w in words) and
             all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)),
             'positive physical packing pair check')
        triples = [ps for w in words for ps in combinations([p for p in range(18) if w >> p & 1], 3)]
        need(len(triples) == len(set(triples)) == 10 * target, 'positive physical triple check')
        record = {'agent': 'six-code-2', 'role': 'researcher',
            'status': 'LITERAL_POSITIVE_PACKING_FIXED_FOUR_HOLE_SINGLE_PRODUCER',
            'size': target, 'words': words, 'core_ids': ids, 'hole_words': sorted(holes),
            'caps': sorted(caps), 'tails': sorted(tails), 'removed_parents': sorted(removed),
            's': len(caps), 'a': len(tails), 't': 0, 'R': len(removed),
            'retained_B7': len(base & set(words)), 'omitted_B7': sorted(base - set(words)),
            'carrier_sha256': graph['core_carrier_sha256'],
            'independent_witness_validation': 'pending; producer exact pairs/triples only'}
        (args.work / f'WITNESS{target}.json').write_bytes(encoded(record))
        first[target] = ids

    class FoundSeventy(Exception):
        pass

    counts = {k: 0 for k in range(1,7)}
    states = 0

    def visit(ids, candidates):
        nonlocal states
        states += 1
        if states % 512 == 0:
            guard('ordered-through-six-cliques', ids, states)
        k = len(ids)
        if k:
            counts[k] += 1
        positive(ids)
        if k == 6:
            raise FoundSeventy('literal70 saved; no complete larger census requested')
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            i = bit.bit_length()-1
            visit(ids+[i], candidates & adjacency[i])

    found70 = False
    try:
        visit([], all_bits)
    except FoundSeventy:
        found70 = True
    guard('positive70-stop' if found70 else 'complete-through-six', [n], states)
    if not found70:
        need(counts[2] == graph['edges'], 'ordered edge census differs')
    triangles, four_cliques, five_cliques, six_cliques = (counts[k] for k in range(3,7))
    summary = {'agent': 'six-code-2', 'role': 'researcher',
        'status': ('LITERAL70_SAVED_CLIQUE_CENSUS_STOPPED_NO_ABSENCE' if found70 else
                   'COMPLETE_FIXED_FOUR_HOLE_GRAPH_THROUGH_SIX_CLIQUES_SINGLE_PRODUCER_ONLY'),
        'hole_words': data['hole_words'], 'vertices': n, 'edges': graph['edges'],
        'triangles': triangles, 'four_cliques': four_cliques, 'five_cliques': five_cliques,
        'six_cliques': six_cliques, 'all_counts_complete': not found70, 'counts_through_six': counts,
        'first_witness_core_ids': first, 'clique_states': states,
        'degree_histogram': sorted(Counter(r.bit_count() for r in adjacency).items()),
        'carrier_sha256': graph['core_carrier_sha256'], 'graph_bytes': len(gb),
        'graph_sha256': hashlib.sha256(gb).hexdigest(), 'ordered_graph_row_sha256': row_digest.hexdigest(),
        'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'initial_whole_guard_seconds': 60, 'initial_clique_state_guard': 2_000_000,
        'independent_complete_audit': 'pending',
        'scope': 'Only these four literal emptyD parents, arbitrary outsider caps and contained remaining tails, with NO Q-y word or Q restrictions. No all-four-subset normalization or global endpoint; absence requires separate physical carrier/graph audit.'}
    (args.work / 'SUMMARY.json').write_bytes(encoded(summary))
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
