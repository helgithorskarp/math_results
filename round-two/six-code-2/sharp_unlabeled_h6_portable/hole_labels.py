"""Physical empty-parent labels and missing-neighbor-label color extension certificate.

six-code-2, researcher. The complete physical core/graph audits are explicit
dependencies; this checker does not claim to reconstruct their tail domains.
No producer imports. The previous stronger active-core hypothesis is false.
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


def physical(word, weight, length=17):
    need(type(word) is int and 0 <= word < 1 << length and word.bit_count() == weight,
         'literal word domain')
    return frozenset(v for v in range(length) if word >> v & 1)


def check_label(actual, expected):
    need(actual == expected, 'physical whole-D four-intersection label')


def check_degree_domain(actual, expected):
    need(actual == expected, 'complete unlabeled degree domain')


def check_degree(actual, expected):
    need(actual == expected, 'physical complete-row unlabeled degree')


def check_edge_color(colors, i, j):
    need(colors[i] != colors[j], 'same-color declared physical edge')


def packing(words, size):
    need(len(words) == len(set(words)) == size, 'positive distinct word count')
    ps = [physical(w, 5, 18) for w in words]
    need(all(len(a & b) <= 2 for a, b in combinations(ps, 2)), 'positive physical collision')
    triples = [t for word in ps for t in combinations(sorted(word), 3)]
    need(len(triples) == len(set(triples)) == 10 * size, 'positive triple ownership')
    return ps


def rejects(label, callback, expected):
    try:
        callback()
    except ValueError as error:
        need(str(error) == expected, 'unintended semantic rejection')
        return label
    raise ValueError('semantic damage accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--case-root', type=Path, action='append', required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh hole-degree audit required')
    args.work.mkdir(parents=True)
    begin, states = time.monotonic(), 0

    def step(amount=1):
        nonlocal states
        states += amount
        if states % 1024 < amount:
            check_operations()
            need(time.monotonic() - begin < 60 and states <= 2_000_000,
                 'INCOMPLETE original60s/two-million hole-degree guard')

    parent_raw = args.parent.read_bytes()
    need(hashlib.sha256(parent_raw).hexdigest() ==
         '32e66195e3252e2a50a2d6c55ed7d9af9a8693e7f7121276aeca1474f80c3758', 'literal D bytes')
    old_words = sorted(json.loads(parent_raw)['words'])
    old = tuple(physical(w, 5) for w in old_words)
    triples = [t for b in old for t in combinations(sorted(b), 3)]
    need(len(old) == len(set(old)) == 68 and len(triples) == len(set(triples)) == 680 and
         set(triples) == set(combinations(range(17), 3)), 'physical complete Steiner partition')
    results, certificates = [], []
    for case_root in args.case_root:
        raw = (case_root / 'carrier/CORES.json').read_bytes()
        graph_raw = (case_root / 'graph/GRAPH.json').read_bytes()
        audit_raw = (case_root / 'point-audit/EXACT_RESULT.json').read_bytes()
        summary_raw = (case_root / 'graph/SUMMARY.json').read_bytes()
        data, graph, audit = json.loads(raw), json.loads(graph_raw), json.loads(audit_raw)
        need(audit['status'] == 'COMPLETE_PHYSICAL_FIXED_Q_EXTRA_PAIR_H6_AUDIT' and
             audit['producer_summary_sha256'] == hashlib.sha256(summary_raw).hexdigest() and
             graph['core_carrier_sha256'] == hashlib.sha256(raw).hexdigest() and
             graph['ordered_graph_row_sha256'] == audit['physical_graph_row_sha256'] and
             graph['vertices'] == audit['cores'] == len(data['cores']) and
             data['parent_words'] == old_words and graph['hole_words'] == data['hole_words'] == audit['empty_holes'],
             'complete physical audit dependency scope')
        q = physical(data['noncontained_q'], 4)
        holes = [physical(w, 5) for w in data['hole_words']]
        need(len(holes) == len(set(holes)) == 6 and set(holes) <= set(old), 'literal six-hole domain')
        rows = tuple(int(row, 16) for row in graph['adjacency_hex'])
        n = len(rows)
        need(n == len(data['cores']) and all(0 <= row < 1 << n for row in rows), 'whole graph row domain')
        labels, label_cache = [], {}
        for core in data['cores']:
            word = core['cap']
            if word not in label_cache:
                cap = physical(word, 5)
                owners = []
                for parent in old:
                    if len(cap & parent) == 4:
                        owners.append(parent)
                    step()
                need(len(owners) <= 1, 'whole-D four-intersection uniqueness')
                need(not owners or owners[0] in holes, 'four-intersection owner must be empty')
                label_cache[word] = holes.index(owners[0]) if owners else None
            labels.append(label_cache[word])
            step()
        unlabeled = [i for i, label in enumerate(labels) if label is None]
        degree_rows = [[i, rows[i].bit_count()] for i in unlabeled]
        maximum = max((degree for i, degree in degree_rows), default=-1)
        degree_histogram = sorted(Counter(degree for i, degree in degree_rows).items())
        # The following is the stated finite certificate condition, not a
        # general assertion about every possible h6 boundary.
        neighbor_labels = []
        degree_exception = None
        for i in unlabeled:
            row, seen_labels, adjacent_ids = rows[i], set(), []
            while row:
                bit = row & -row; row ^= bit; j = bit.bit_length() - 1
                need(labels[j] is not None, 'UNLABELED_INDEPENDENCE_GATE_NOT_ESTABLISHED; no general absence')
                seen_labels.add(labels[j]); adjacent_ids.append(j); step()
            need(len(seen_labels) <= 5, 'MISSING_NEIGHBOR_LABEL_GATE_NOT_ESTABLISHED; no general absence')
            neighbor_labels.append([i, sorted(seen_labels)])
            if len(adjacent_ids) >= 6 and degree_exception is None:
                degree_exception = {'core_id': i, 'cap': data['cores'][i]['cap'],
                                    'degree': len(adjacent_ids), 'all_neighbor_core_ids': adjacent_ids,
                                    'all_neighbor_hole_labels': sorted(seen_labels),
                                    'neighbors_are_not_claimed_mutually_compatible': True}

        colors = list(labels)
        for i in unlabeled:
            forbidden, row = set(), rows[i]
            while row:
                bit = row & -row
                row ^= bit
                j = bit.bit_length() - 1
                need(j != i, 'physical self edge')
                if colors[j] is not None:
                    forbidden.add(colors[j])
                step()
            choices = set(range(6)) - forbidden
            need(choices, 'missing-label color extension empty')
            colors[i] = min(choices)
        edge_count, unlabeled_edges = 0, 0
        for i, row in enumerate(rows):
            above = row >> (i + 1) << (i + 1)
            while above:
                bit = above & -above
                above ^= bit
                j = bit.bit_length() - 1
                need(rows[j] >> i & 1, 'physical edge symmetry')
                if labels[i] is not None and labels[j] is not None:
                    need(labels[i] != labels[j], 'two same-parent four-caps meet in at least3')
                else:
                    unlabeled_edges += 1
                check_edge_color(colors, i, j)
                edge_count += 1
                step()
        need(edge_count == graph['edges'] == audit['edges'], 'complete edge count')
        # Retain a physical counterexample to the stronger rejected guess:
        # an unlabeled core can participate in a compatibility edge.
        i = next(i for i in unlabeled if rows[i])
        j = (rows[i] & -rows[i]).bit_length() - 1
        selected = [data['cores'][i], data['cores'][j]]
        assigned = {}
        for core in selected:
            for parent, tail in zip(core['parents'], core['tails']):
                need(parent not in assigned or assigned[parent] == tail, 'glued parent consistency')
                assigned[parent] = tail
        removed = set(data['hole_words']) | {old_words[p] for p in assigned}
        words = sorted((set(old_words) - removed) | {core['cap'] for core in selected} |
                       {data['noncontained_q'] | (1 << 17)} | {tail | (1 << 17) for tail in assigned.values()})
        ps = packing(words, 65)
        step(65 * 64 // 2 + 650)
        need(labels[i] is None and all(len(physical(selected[0]['cap'], 5) & b) <= 3 for b in old),
             'literal unlabeled cap counterexample')
        represented, noncontained = set(), []
        for word in words:
            if not word >> 17 & 1:
                continue
            tail = physical(word ^ (1 << 17), 4)
            owners = [b for b in old if tail <= b]
            if owners:
                need(len(owners) == 1 and owners[0] not in represented, 'counterexample tail ownership')
                represented.add(owners[0])
            else:
                noncontained.append(tail)
        need(noncontained == [q] and (set(old) - set(ps)) - represented == set(holes),
             'counterexample exact fixed boundary')
        marked = next(k for k, value in enumerate(labels) if value is not None)
        controls = [rejects('wrong-four-intersection-label',
                    lambda: check_label((labels[marked] + 1) % 6, labels[marked]),
                    'physical whole-D four-intersection label')]
        controls.append(rejects('omitted-unlabeled-degree-entry',
                        lambda: check_degree_domain(degree_rows[:-1], degree_rows),
                        'complete unlabeled degree domain'))
        controls.append(rejects('altered-unlabeled-degree',
                        lambda: check_degree(degree_rows[0][1] + 1, rows[degree_rows[0][0]].bit_count()),
                        'physical complete-row unlabeled degree'))
        damaged = list(colors)
        damaged[j] = damaged[i]
        controls.append(rejects('same-color-edge', lambda: check_edge_color(damaged, i, j),
                        'same-color declared physical edge'))
        controls.append(rejects('duplicated-counterexample-word',
                        lambda: packing(words[:-1] + [words[0]], 65), 'positive distinct word count'))
        certificate = {'extra_pair': data['additional_empty_parents'], 'hole_words': data['hole_words'],
                       'graph_sha256': hashlib.sha256(graph_raw).hexdigest(), 'labels': labels,
                       'complete_unlabeled_degrees': degree_rows, 'complete_unlabeled_neighbor_labels': neighbor_labels,
                       'degree_above5_exception': degree_exception, 'extended_colors': colors,
                       'positive65_counterexample': {'core_ids': [i, j], 'unlabeled_cap': selected[0]['cap'],
                                                     'words': words, 'noncontained_q': data['noncontained_q'],
                                                     's': 2, 'a': len(assigned), 'R': len(removed), 't': 1, 'h': 6}}
        certificates.append(certificate)
        results.append({'extra_pair': data['additional_empty_parents'], 'cores': n,
                        'graph_sha256': hashlib.sha256(graph_raw).hexdigest(),
                        'carrier_sha256': hashlib.sha256(raw).hexdigest(),
                        'complete_physical_audit_sha256': hashlib.sha256(audit_raw).hexdigest(),
                        'unique_caps_labeled_physically': len(label_cache),
                        'labeled_cores': n - len(unlabeled), 'unlabeled_cores': len(unlabeled),
                        'unlabeled_degree_histogram': degree_histogram, 'maximum_unlabeled_degree': maximum,
                        'unlabeled_cores_independent': True,
                        'maximum_unlabeled_neighbor_label_count': max(len(row[1]) for row in neighbor_labels),
                        'degree_above5_exception': degree_exception,
                        'all_edges_checked': edge_count, 'edges_with_unlabeled_endpoint': unlabeled_edges,
                        'positive_extended_color_count': max(colors) + 1,
                        'positive65_counterexample': certificate['positive65_counterexample'],
                        'semantic_damage_rejections': controls})
    need(time.monotonic() - begin < 60 and states <= 2_000_000,
         'INCOMPLETE original60s/two-million final hole-degree guard')
    packet = encoded({'agent': 'six-code-2', 'role': 'researcher', 'certificates': certificates})
    (args.work / 'CERTIFICATES.json').write_bytes(packet)
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'EXACT_DECLARED_H6_HOLE_LABEL_MISSING_NEIGHBOR_LABEL_SIX_COLOR_CERTIFICATES',
              'parent_sha256': hashlib.sha256(parent_raw).hexdigest(), 'cases': results,
              'certificate_sha256': hashlib.sha256(packet).hexdigest(), 'certificate_bytes': len(packet),
              'state_units': states, 'state_definition': 'cached literal parent intersections, core labels, graph neighbor/edge checks and one positive65 pair/triple check per case',
              'complete_physical_carrier_graph_audits_are_dependencies': True,
              'ordinary_bridges_formalized': False, 'independent_person_review': 'pending',
              'all_h6_or_global_endpoint_claim': False,
              'stronger_all_active_cores_labeled_hypothesis': 'FALSE; literal65 counterexamples supplied',
              'previous_degree_le5_gate_failed': 'Preserved separately; complete positive high-degree star records show why that sufficient condition cannot be used here.'}
    rb = encoded(result)
    (args.work / 'EXACT_RESULT.json').write_bytes(rb)
    execution = {'seconds': time.monotonic() - begin,
                 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'original_math_seconds': 60, 'original_math_states': 2000000,
                 'exact_bytes': len(rb), 'exact_sha256': hashlib.sha256(rb).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
