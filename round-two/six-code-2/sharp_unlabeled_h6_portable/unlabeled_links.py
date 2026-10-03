"""Exact full neighbor links of unlabeled cores on declared complete graphs.

Carrier and every-row physical graph audits are explicit dependencies. This
new checker reconstructs labels, the whole unlabeled domain, every candidate
link pair by physical cap/tail sets, and an original-coordinate sharp witness.
It does not repeat the earlier full carrier or clique census.
"""
import argparse
from operations import check_operations
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


def points(word, weight, length=17):
    need(type(word) is int and 0 <= word < 1 << length and word.bit_count() == weight,
         'literal point domain')
    return frozenset(i for i in range(length) if word >> i & 1)


def equal(actual, expected, message):
    need(actual == expected, message)


def packing(words, size):
    need(len(words) == len(set(words)) == size, 'positive distinct word count')
    ps = [points(w, 5, 18) for w in words]
    need(all(len(a & b) <= 2 for a, b in combinations(ps, 2)), 'positive physical collision')
    triples = [t for p in ps for t in combinations(sorted(p), 3)]
    need(len(triples) == len(set(triples)) == 10 * size, 'positive triple ownership')
    return ps


def rejects(name, action, expected):
    try:
        action()
    except ValueError as error:
        need(str(error) == expected, 'unintended semantic rejection')
        return name
    raise ValueError('semantic damage accepted: ' + name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--case-root', type=Path, action='append', required=True)
    parser.add_argument('--labels', type=Path, action='append', required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh full-link output required')
    args.work.mkdir(parents=True)
    begin, states = time.monotonic(), 0

    def step(amount=1):
        nonlocal states
        states += amount
        if states % 1024 < amount:
            check_operations()
            need(states <= 2_000_000 and time.monotonic() - begin < 60,
                 'INCOMPLETE original60s/two-million full-link guard')

    parent_raw = args.parent.read_bytes()
    need(hashlib.sha256(parent_raw).hexdigest() == '32e66195e3252e2a50a2d6c55ed7d9af9a8693e7f7121276aeca1474f80c3758', 'literal D bytes')
    old_words = sorted(json.loads(parent_raw)['words'])
    old = tuple(points(w, 5) for w in old_words)
    triples = [t for p in old for t in combinations(sorted(p), 3)]
    need(len(old) == 68 and len(triples) == len(set(triples)) == 680 and
         set(triples) == set(combinations(range(17), 3)), 'complete Steiner partition')
    previous = {}
    for filename in args.labels:
        for cert in json.loads(filename.read_bytes())['certificates']:
            need(cert['graph_sha256'] not in previous, 'duplicate declared graph certificate')
            previous[cert['graph_sha256']] = cert
    results, packets, seen_graphs = [], [], set()
    for folder in args.case_root:
        raw = (folder / 'carrier/CORES.json').read_bytes()
        gr = (folder / 'graph/GRAPH.json').read_bytes()
        ar = (folder / 'point-audit/EXACT_RESULT.json').read_bytes()
        sr = (folder / 'graph/SUMMARY.json').read_bytes()
        data, graph, audit = json.loads(raw), json.loads(gr), json.loads(ar)
        gh = hashlib.sha256(gr).hexdigest()
        need(gh in previous and gh not in seen_graphs, 'declared full graph certificate domain')
        seen_graphs.add(gh)
        need(audit['status'] == 'COMPLETE_PHYSICAL_FIXED_Q_EXTRA_PAIR_H6_AUDIT' and
             audit['producer_summary_sha256'] == hashlib.sha256(sr).hexdigest() and
             graph['core_carrier_sha256'] == hashlib.sha256(raw).hexdigest() and
             graph['ordered_graph_row_sha256'] == audit['physical_graph_row_sha256'] and
             data['parent_words'] == old_words and graph['hole_words'] == data['hole_words'] == audit['empty_holes'],
             'complete physical carrier and graph dependency')
        cores = data['cores']; n = len(cores)
        rows = tuple(int(r, 16) for r in graph['adjacency_hex'])
        need(n == graph['vertices'] == audit['cores'] == len(rows) and
             all(0 <= r < 1 << n for r in rows), 'complete graph row domain')
        holes = tuple(points(w, 5) for w in data['hole_words'])
        q = points(data['noncontained_q'], 4)
        need(len(holes) == len(set(holes)) == 6 and set(holes) <= set(old), 'six empty parents')
        labels, cache, physical = [], {}, []
        for core in cores:
            word = core['cap']; cap = points(word, 5)
            need(cap not in old, 'new cap outside D')
            if word not in cache:
                owners = [p for p in old if len(p & cap) == 4]
                need(len(owners) <= 1 and (not owners or owners[0] in holes), 'unique empty four-intersection parent')
                cache[word] = holes.index(owners[0]) if owners else None
                step(68)
            labels.append(cache[word])
            tails = tuple(points(t, 4) for t in core['tails'])
            need(len(core['parents']) == len(set(core['parents'])) == len(tails), 'whole core assignment domain')
            need(all(0 <= p < 68 and t <= old[p] for p, t in zip(core['parents'], tails)), 'tail original parent binding')
            physical.append((cap, tails, dict(zip(core['parents'], core['tails']))))
            step()
        equal(labels, previous[gh]['labels'], 'complete physical labels differ')
        unlabeled = [i for i, label in enumerate(labels) if label is None]
        umask = sum(1 << i for i in unlabeled)

        def compatible(i, j):
            a, at, aa = physical[i]; b, bt, ba = physical[j]
            step(1 + len(at) + len(bt) + len(at) * len(bt))
            return (len(a & b) <= 2 and all(len(a & t) <= 2 for t in bt) and
                    all(len(b & t) <= 2 for t in at) and
                    all(t == u or len(t & u) <= 1 for t in at for u in bt) and
                    all(p not in ba or ba[p] == t for p, t in aa.items()))

        link_rows, link_pairs, triangles, first_edge, first_triangle = [], 0, 0, None, None
        control_pair = None
        degrees, label_sets = [], []
        for i in unlabeled:
            need(not rows[i] & umask, 'unlabeled induced graph independence')
            neighbors, remaining = [], rows[i]
            while remaining:
                bit = remaining & -remaining; remaining ^= bit
                neighbors.append(bit.bit_length() - 1)
                step()
            # All set bits are exhausted; missing edges are covered by the pinned every-row audit.
            need(all(rows[j] >> i & 1 and compatible(i, j) for j in neighbors), 'physical complete unlabeled edge')
            distinct = sorted({labels[j] for j in neighbors})
            need(None not in distinct and len(distinct) <= 2, 'at most two complete neighbor parent labels')
            degrees.append([i, len(neighbors)]); label_sets.append([i, distinct])
            links = []
            for j, k in combinations(neighbors, 2):
                actual = compatible(j, k)
                if control_pair is None: control_pair = (j, k, actual)
                equal(bool(rows[j] >> k & 1), actual, 'physical candidate link pair differs')
                equal(bool(rows[k] >> j & 1), actual, 'reverse physical candidate link pair differs')
                link_pairs += 1
                if actual:
                    links.append([j, k]); triangles += 1
                    if first_triangle is None: first_triangle = [i, j, k]
                step()
            if neighbors and first_edge is None: first_edge = [i, neighbors[0]]
            link_rows.append({'core_id': i, 'all_neighbors': neighbors, 'all_link_edges': links})
        equal(degrees, previous[gh]['complete_unlabeled_degrees'], 'complete unlabeled degree domain differs')
        equal(label_sets, previous[gh]['complete_unlabeled_neighbor_labels'], 'complete neighbor label domain differs')
        maximum = 3 if triangles else 2 if first_edge else 1 if unlabeled else 0
        chosen = first_triangle or first_edge or (unlabeled[:1] if unlabeled else [])
        need(chosen, 'positive unlabeled witness present in this declared scope')
        assignment = {}
        for i in chosen:
            for p, t in zip(cores[i]['parents'], cores[i]['tails']):
                need(p not in assignment or assignment[p] == t, 'positive glued parent consistency')
                assignment[p] = t
        removed = set(data['hole_words']) | {old_words[p] for p in assignment}
        words = sorted((set(old_words) - removed) | {cores[i]['cap'] for i in chosen} |
                       {data['noncontained_q'] | (1 << 17)} | {t | (1 << 17) for t in assignment.values()})
        size = 63 + maximum; ps = packing(words, size)
        represented, noncontained = set(), []
        for w in words:
            if not w >> 17 & 1: continue
            tail = points(w ^ (1 << 17), 4)
            owners = [p for p in old if tail <= p]
            if owners:
                need(len(owners) == 1 and owners[0] not in represented, 'positive unique tail ownership')
                represented.add(owners[0])
            else: noncontained.append(tail)
        need(noncontained == [q] and (set(old) - set(ps)) - represented == set(holes), 'positive exact empty-parent boundary')
        step(size * (size - 1) // 2 + 10 * size)
        need(control_pair is not None, 'actual candidate link pair for semantic control')
        pair_j, pair_k, pair_actual = control_pair
        controls = [rejects('omitted-unlabeled-link-vertex', lambda: equal(unlabeled[:-1], unlabeled, 'complete link vertex domain'), 'complete link vertex domain'),
                    rejects('altered-physical-link-pair', lambda: equal(not pair_actual, compatible(pair_j, pair_k), 'physical candidate link pair differs'), 'physical candidate link pair differs'),
                    rejects('duplicated-positive-word', lambda: packing(words[:-1] + [words[0]], size), 'positive distinct word count')]
        packet = {'extra_pair': data['additional_empty_parents'], 'graph_sha256': gh,
                  'all_unlabeled_links': link_rows, 'maximum_clique_with_unlabeled': maximum,
                  'sharp_positive_words': words, 'sharp_positive_core_ids': chosen}
        packets.append(packet)
        results.append({'extra_pair': data['additional_empty_parents'], 'cores': n,
                        'graph_sha256': gh, 'carrier_sha256': hashlib.sha256(raw).hexdigest(),
                        'physical_audit_sha256': hashlib.sha256(ar).hexdigest(), 'unlabeled_cores': len(unlabeled),
                        'complete_unlabeled_degree_sum': sum(d for i, d in degrees),
                        'all_candidate_link_pairs_checked': link_pairs, 'unlabeled_triangles': triangles,
                        'maximum_clique_with_unlabeled': maximum, 'sharp_unlabeled_packing_size': size,
                        'cap_parent_rigidity_from_size': size + 1,
                        'positive': {'core_ids': chosen, 'words': words, 'a': len(assignment), 'R': len(removed),
                                     's': maximum, 't': 1, 'h': 6, 'noncontained_q': data['noncontained_q']},
                        'semantic_controls': controls})
    equal(seen_graphs, set(previous), 'entire declared graph domain')
    need(time.monotonic() - begin < 60 and states <= 2_000_000, 'INCOMPLETE final full-link guard')
    packet = encoded({'agent': 'six-code-2', 'role': 'researcher', 'cases': packets})
    (args.work / 'CERTIFICATES.json').write_bytes(packet)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'EXACT_FULL_UNLABELED_LINKS_AND_SHARP_ORIGINAL_PACKINGS',
              'cases': results, 'certificate_bytes': len(packet), 'certificate_sha256': hashlib.sha256(packet).hexdigest(),
              'state_units': states, 'complete_carrier_and_every_row_graph_audits_are_dependencies': True,
              'ordinary_restriction_gluing_and_transport_bridges_formalized': False,
              'independent_person_review': 'pending', 'all_h6_or_global_endpoint_claim': False}
    rb = encoded(result); (args.work / 'EXACT_RESULT.json').write_bytes(rb)
    execution = {'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'original_math_seconds': 60, 'original_math_states': 2_000_000,
                 'exact_bytes': len(rb), 'exact_sha256': hashlib.sha256(rb).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
