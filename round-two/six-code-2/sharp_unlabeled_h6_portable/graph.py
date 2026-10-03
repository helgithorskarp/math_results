"""Exact fixed-noncontained-Q physical graph and cap-clique construction.

six-code-2, researcher. New source; sealed two-hole work is unchanged.
No coverage of all hole triples is presumed. Guarded incomplete search
is not absence. Every first positive68/69/70 is saved immediately.
"""
import argparse
from collections import Counter, defaultdict
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


class Positive70Found(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--carrier', type=Path, required=True)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--control69', type=Path)
    args = parser.parse_args()
    need(not args.work.exists(), 'new fixed-triple graph work directory required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    raw = args.carrier.read_bytes()
    data = json.loads(raw)
    need(data['status'] in ('COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_FOUR_EMPTY_STEINER_PARENTS',
                            'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_FIVE_EMPTY_STEINER_PARENTS',
                            'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_SIX_EMPTY_STEINER_PARENTS'),
         'carrier incomplete or wrong scope')
    q = data['noncontained_q']
    h = len(data['hole_words'])
    need(h in (4, 5, 6), 'only the specified h4/h5/h6 model')
    base_size = 69 - h
    cores = data['cores']
    n = len(cores)
    cap_occurrences, tail_occurrences = defaultdict(int), defaultdict(int)
    for i, c in enumerate(cores):
        cap_occurrences[c['cap']] |= 1 << i
        for tail in c['tails']:
            tail_occurrences[tail] |= 1 << i
    cap_forbidden, tail_forbidden = {}, {}

    def guard(stage, cursor, states=0):
        if states > 2_000_000 or time.monotonic() - begin >= 60:
            (args.work / 'PARTIAL.json').write_bytes(encoded({'agent': 'six-code-2', 'role': 'researcher',
                'status': 'INCOMPLETE_NONCONTAINED_Q_GRAPH_OR_CLIQUE_SEARCH_NO_ABSENCE',
                'stage': stage, 'cursor': cursor, 'states': states,
                'carrier_sha256': hashlib.sha256(raw).hexdigest(),
                'initial_whole_guard_seconds': 60, 'initial_clique_state_guard': 2_000_000,
                'positive_sizes_saved': [k for k in range(base_size,71) if (args.work / f'WITNESS{k}.json').exists()]}))
            raise TimeoutError('INCOMPLETE fixed60s/two-million-state three-hole graph guard')

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
        'status': 'COMPLETE_FIXED_NONCONTAINED_Q_PHYSICAL_INVERSE_GRAPH_SINGLE_PRODUCER',
        'edges': sum(row.bit_count() for row in adjacency) // 2,
        'noncontained_q': q, 'hole_words': data['hole_words'], 'core_carrier_sha256': hashlib.sha256(raw).hexdigest(),
        'adjacency_hex': [format(row, 'x') for row in adjacency],
        'ordered_graph_row_sha256': row_digest.hexdigest()}
    if h == 5:
        graph.update({'h': h, 'additional_empty_parent': data['additional_empty_parent'],
                      'status': 'COMPLETE_FIXED_NONCONTAINED_Q_H5_PHYSICAL_INVERSE_GRAPH_SINGLE_PRODUCER'})
    if h == 6:
        graph.update({'h': h, 'additional_empty_parents': data['additional_empty_parents'],
                      'status': 'COMPLETE_FIXED_NONCONTAINED_Q_H6_PHYSICAL_INVERSE_GRAPH_SINGLE_PRODUCER'})
    gb = encoded(graph)
    (args.work / 'GRAPH.json').write_bytes(gb)
    old, holes = set(data['parent_words']), set(data['hole_words'])
    base = set(json.loads(args.parent.read_bytes())['base_words'])
    first = {k: None for k in range(base_size,71)}

    def positive(ids):
        target = base_size + len(ids)
        if first[target] is not None:
            return
        selected = [cores[i] for i in ids]
        removed = holes | {data['parent_words'][p] for c in selected for p in c['parents']}
        caps = {c['cap'] for c in selected}
        tails = {t for c in selected for t in c['tails']}
        words = tuple(sorted((old - removed) | caps | {q | (1 << 17)} | {t | (1 << 17) for t in tails}))
        need(len(words) == target and len(caps) == len(ids) and len(removed) == len(tails) + h,
             'positive physical three-hole normal form')
        need(all(w.bit_count() == 5 for w in words) and
             all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)),
             'positive physical packing pair check')
        triples = [ps for w in words for ps in combinations([p for p in range(18) if w >> p & 1], 3)]
        need(len(triples) == len(set(triples)) == 10 * target, 'positive physical triple check')
        record = {'agent': 'six-code-2', 'role': 'researcher',
            'status': 'LITERAL_POSITIVE_PACKING_FIXED_NONCONTAINED_Q_SINGLE_PRODUCER',
            'size': target, 'words': words, 'core_ids': ids, 'noncontained_q': q, 'hole_words': sorted(holes),
            'caps': sorted(caps), 'tails': sorted(tails), 'removed_parents': sorted(removed),
            's': len(caps), 'a': len(tails), 't': 1, 'R': len(removed),
            'retained_B7': len(base & set(words)), 'omitted_B7': sorted(base - set(words)),
            'carrier_sha256': graph['core_carrier_sha256'],
            'independent_witness_validation': 'pending; producer exact pairs/triples only'}
        if h == 5:
            record.update({'h': h, 'additional_empty_parent': data['additional_empty_parent']})
        if h == 6:
            record.update({'h': h, 'additional_empty_parents': data['additional_empty_parents']})
        (args.work / f'WITNESS{target}.json').write_bytes(encoded(record))
        first[target] = ids
        if h >= 5 and target == 70:
            stop = {'agent': 'six-code-2', 'role': 'researcher',
                    'status': 'POSITIVE70_FOUND_CLIQUE_CENSUS_STOPPED_NO_ABSENCE',
                    'size': 70, 'core_ids': ids, 'h': h, 'noncontained_q': q,
                    'additional_empty_parents': sorted(set(data['hole_words']) - set(data['reserved_Q_parent_words'])),
                    'complete_graph_saved': True, 'clique_census_complete': False,
                    'independent_original_word_check': 'pending'}
            (args.work / 'POSITIVE_STOP.json').write_bytes(encoded(stop))
            print(json.dumps(stop, sort_keys=True), flush=True)
            raise Positive70Found()

    positive([])
    if n:
        positive([0])
    if h == 6:
        need(args.control69 is not None, 'h6 requires the known literal69 boundary control')
        control_raw = args.control69.read_bytes()
        control = json.loads(control_raw)
        words = control['words']
        need(len(words) == len(set(words)) == 69 and all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5 for w in words),
             'known control69 domain')
        need(all((u & v).bit_count() <= 2 for u, v in combinations(words, 2)), 'known control69 collision')
        ctrl_caps = sorted(w for w in words if not w >> 17 & 1 and w not in old)
        assignment, noncontained = {}, []
        for w in words:
            if not w >> 17 & 1: continue
            tail = w ^ (1 << 17)
            owners = [i for i, b in enumerate(data['parent_words']) if tail & b == tail]
            if owners:
                need(len(owners) == 1 and owners[0] not in assignment, 'known control69 tail ownership')
                assignment[owners[0]] = tail
            else:
                noncontained.append(tail)
        control_removed = old - set(words)
        need(noncontained == [q] and control_removed - {data['parent_words'][i] for i in assignment} == holes and len(ctrl_caps) == 6,
             'known control69 exact h6 boundary')
        ctrl_ids = []
        for cap in ctrl_caps:
            ids = [i for i, c in enumerate(cores) if c['cap'] == cap and all(assignment.get(p) == t for p, t in zip(c['parents'], c['tails']))]
            need(len(ids) == 1, 'known control69 complete carrier core')
            ctrl_ids += ids
        need(all(adjacency[i] >> j & 1 for i, j in combinations(ctrl_ids, 2)), 'known control69 physical six-core clique')
        positive(sorted(ctrl_ids))
        (args.work / 'CONTROL69_LINK.json').write_bytes(encoded({'agent': 'six-code-2', 'role': 'researcher',
            'status': 'KNOWN69_INPUT_AND_NORMALIZED_SIX_CORE_CONTROL_CHECKED_NOT_NEW_RESEARCH',
            'input_sha256': hashlib.sha256(control_raw).hexdigest(), 'core_ids': sorted(ctrl_ids),
            'original_s': 6, 'original_a': len(assignment), 'original_R': len(control_removed),
            'normalized_size': 69, 'h': 6, 'noncontained_q': q, 'hole_words': sorted(holes)}))
    states = triangles = four_cliques = five_cliques = six_cliques = seven_cliques = 0
    for i in range(n):
        above_i = adjacency[i] >> (i + 1) << (i + 1)
        js = above_i
        while js:
            bit = js & -js
            js ^= bit
            j = bit.bit_length() - 1
            states += 1
            positive([i, j])
            ks = above_i & adjacency[j]
            ks = ks >> (j + 1) << (j + 1)
            triangles += ks.bit_count()
            while ks:
                bit_k = ks & -ks
                ks ^= bit_k
                k = bit_k.bit_length() - 1
                states += 1
                positive([i, j, k])
                ls = ks & adjacency[k]
                four_cliques += ls.bit_count()
                while ls:
                    bit_l = ls & -ls
                    ls ^= bit_l
                    ell = bit_l.bit_length() - 1
                    states += 1
                    positive([i, j, k, ell])
                    ms = ls & adjacency[ell]
                    five_cliques += ms.bit_count()
                    if ms:
                        m = (ms & -ms).bit_length() - 1
                        positive([i, j, k, ell, m])
                    if h >= 5:
                        remaining_ms = ms
                        while remaining_ms:
                            bit_m = remaining_ms & -remaining_ms
                            remaining_ms ^= bit_m
                            m = bit_m.bit_length() - 1
                            states += 1
                            positive([i, j, k, ell, m])
                            ns = remaining_ms & adjacency[m]
                            six_cliques += ns.bit_count()
                            if ns:
                                last = (ns & -ns).bit_length() - 1
                                positive([i, j, k, ell, m, last])
                            if h == 6:
                                remaining_ns = ns
                                while remaining_ns:
                                    bit_n = remaining_ns & -remaining_ns
                                    remaining_ns ^= bit_n
                                    nu = bit_n.bit_length() - 1
                                    states += 1
                                    positive([i, j, k, ell, m, nu])
                                    os = remaining_ns & adjacency[nu]
                                    seven_cliques += os.bit_count()
                                    if os:
                                        last = (os & -os).bit_length() - 1
                                        positive([i, j, k, ell, m, nu, last])
                                    if states % 1024 == 0:
                                        guard('ordered-seven-cliques', [i, j, k, ell, m, nu], states)
                            if states % 1024 == 0:
                                guard('ordered-six-cliques', [i, j, k, ell, m], states)
                    if states % 1024 == 0:
                        guard('ordered-five-cliques', [i, j, k, ell], states)
                if states % 1024 == 0:
                    guard('ordered-four-cliques', [i, j, k], states)
            if states % 1024 == 0:
                guard('ordered-three-cliques', [i, j], states)
        if i % 256 == 0:
            guard('ordered-cliques', [i], states)
    guard('complete', [n], states)
    summary = {'agent': 'six-code-2', 'role': 'researcher',
        'status': 'COMPLETE_FIXED_NONCONTAINED_Q_GRAPH_THROUGH_FIVE_CLIQUES_SINGLE_PRODUCER_ONLY',
        'noncontained_q': q, 'hole_words': data['hole_words'], 'vertices': n, 'edges': graph['edges'],
        'triangles': triangles, 'four_cliques': four_cliques, 'five_cliques': five_cliques,
        'first_witness_core_ids': first, 'clique_states': states,
        'degree_histogram': sorted(Counter(r.bit_count() for r in adjacency).items()),
        'carrier_sha256': graph['core_carrier_sha256'], 'graph_bytes': len(gb),
        'graph_sha256': hashlib.sha256(gb).hexdigest(), 'ordered_graph_row_sha256': row_digest.hexdigest(),
        'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'initial_whole_guard_seconds': 60, 'initial_clique_state_guard': 2_000_000,
        'independent_complete_audit': 'pending',
        'scope': 'Only this literal noncontainedQ with its four empty parents and arbitrary contained remaining tails. No all-Q normalization or global endpoint; absence requires separate physical carrier/graph audit.'}
    if h == 5:
        summary.update({'h': h, 'six_cliques': six_cliques,
                        'additional_empty_parent': data['additional_empty_parent'],
                        'status': 'COMPLETE_FIXED_NONCONTAINED_Q_H5_GRAPH_THROUGH_SIX_CLIQUES_SINGLE_PRODUCER_ONLY',
                        'scope': 'Only literalQ, its four reserved parents and the specified extra empty parent. Complete source clique census through six only if this SUMMARY exists; any POSITIVE_STOP or PARTIAL is not absence. No all-extra-parent or global endpoint claim.'})
    if h == 6:
        summary.update({'h': h, 'six_cliques': six_cliques, 'seven_cliques': seven_cliques,
                        'additional_empty_parents': data['additional_empty_parents'],
                        'status': 'COMPLETE_FIXED_NONCONTAINED_Q_H6_GRAPH_THROUGH_SEVEN_CLIQUES_SINGLE_PRODUCER_ONLY',
                        'scope': 'Only literalQ, its four reserved parents and the specified two extra empty parents. Complete source clique census through seven only if this SUMMARY exists; any POSITIVE_STOP or PARTIAL is not absence. No all-extra-pair or global endpoint claim.'})
    (args.work / 'SUMMARY.json').write_bytes(encoded(summary))
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == '__main__':
    try:
        main()
    except Positive70Found:
        pass
