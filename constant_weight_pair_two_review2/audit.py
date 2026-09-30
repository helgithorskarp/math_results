#!/usr/bin/env python3
"""Independent full anchor coverage and bit-row rejection-tree validation.

No target-author module is imported. All carrier data are rebuilt from
the written degree/leave reduction; only the public compact trees are read.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import time
import resource
from math import factorial, prod

from exact import insist, encoded, mask, bits, pairs, plane, packing

POINTS = tuple(range(17))
A, B, V = 14, 15, 16
ORDINARY = tuple(range(8))
ALL_PAIRS = frozenset(combinations(POINTS, 2))


def triple_partitions(points):
    """Every unordered triple partition: fix the block containing the least point."""
    points = tuple(sorted(points))
    if not points:
        yield ()
        return
    for rest in combinations(points[1:], 2):
        tail = (points[0],) + rest
        remainder = tuple(x for x in points if x not in tail)
        for part in triple_partitions(remainder):
            yield tuple(sorted((tail,) + part))


def relabel_family(family, p):
    return tuple(sorted(tuple(sorted(p[x] for x in block)) for block in family))


def make_case(index):
    # Derived from the only possible high cores, not from certificate entries.
    if index in (0, 1):
        edges = {(A, V), (B, V)} | {(x, V) for x in ORDINARY}
        edges |= {(x, A) for x in (8, 9, 10)} | {(x, B) for x in (11, 12, 13)}
        tails = ((8, 9, 10), (11, 12, 13)) if index == 0 else ((8, 9, 11), (10, 12, 13))
    elif index == 2:
        edges = {(A, V), (A, B)} | {(x, V) for x in range(9)}
        edges |= {(x, A) for x in (9, 10)} | {(x, B) for x in (11, 12, 13)}
        tails = ((9, 10, 15), (11, 12, 13))
    else:
        edges = {(A, V), (B, V), (A, B), (12, 13)} | {(x, V) for x in ORDINARY}
        edges |= {(x, A) for x in (8, 9)} | {(x, B) for x in (10, 11)}
        tails = ((8, 9, 12), (10, 11, 13)) if index == 3 else ((8, 10, 12), (9, 11, 13))
    leave = frozenset(tuple(sorted(e)) for e in edges)
    insist(len(leave) == 16 and Counter(x for e in leave for x in e) ==
           Counter({A: 4, B: 4, V: 10, **{x: 1 for x in range(14)}}), 'wrong first-star leave')
    fixed = tuple(sorted(tuple(sorted((V,) + t)) for t in tails))
    used = frozenset(e for q in fixed for e in pairs(mask(q)))
    insist(len(used) == 12 and not leave & used, 'shared words use leave pairs')
    return {'index': index, 'leave': leave, 'tails': tails, 'fixed': fixed,
            'available': ALL_PAIRS - leave - used}


def small_maps(case):
    # Exhaust all 6! special-point permutations; ordinary labels and anchors fixed.
    answer = []
    for image in permutations(range(8, 14)):
        p = tuple(range(8)) + image + (A, B, V)
        if frozenset(relabel_family(case['leave'], p)) == case['leave'] and \
           relabel_family(case['fixed'], p) == case['fixed']:
            answer.append(p)
    return tuple(answer)


def tail_coverage():
    """Literal ten-partition census and actual six-point leave permutations."""
    result = []
    for index, expected in ((0, [1, 9]), (2, [1]), (3, [2, 4])):
        case = make_case(index)
        neighbors = tuple(x for x in POINTS if x != V and tuple(sorted((x, V))) not in case['leave'])
        insist(len(neighbors) == 6, 'shared-tail neighbor universe')
        universe = tuple(triple_partitions(neighbors))
        insist(len(universe) == 10, 'unordered six-point partitions')
        legal = {t for t in universe if all(not pairs(mask(q)) & case['leave'] for q in t)}
        group = []
        for images in permutations(neighbors):
            p = list(POINTS)
            for x, y in zip(neighbors, images):
                p[x] = y
            if frozenset(relabel_family(case['leave'], p)) == case['leave']:
                group.append(p)
        pending, records = set(legal), []
        while pending:
            rep = min(pending)
            orbit = {relabel_family(rep, p) for p in group}
            insist(orbit <= pending, 'tail orbits fail exact cover')
            pending -= orbit
            leave = frozenset(e for e in case['leave'] if V not in e) | frozenset(e for t in rep for e in pairs(mask(t)))
            insist(len(leave) == 12, 'eighteen-quad leave size')
            cliques = [q for q in combinations(range(16), 4) if pairs(mask(q)) <= leave]
            completions = [(q, r) for q, r in combinations(cliques, 2)
                           if not pairs(mask(q)) & pairs(mask(r)) and pairs(mask(q)) | pairs(mask(r)) == leave]
            records.append({'orbit_size': len(orbit), 'two_clique_completions': len(completions)})
        insist(sorted(r['orbit_size'] for r in records) == expected, 'tail coverage counts differ')
        insist(sorted((r['orbit_size'], r['two_clique_completions']) for r in records) ==
               ([(1, 1), (9, 0)] if index == 0 else [(1, 1)] if index == 2 else [(2, 0), (4, 0)]),
               'direct completion boundary differs')
        result.append({'high_core_representative': index, 'partitions_checked': 10,
                       'legal_partitions': len(legal), 'actual_six_point_leave_maps': len(group),
                       'tail_orbits': sorted(records, key=lambda r: r['orbit_size'])})
    return result


def first_anchor(case):
    neighbors = tuple(x for x in POINTS if x != A and tuple(sorted((x, A))) not in case['leave'])
    special = frozenset(neighbors) - frozenset(ORDINARY)
    insist(len(neighbors) == 12 and len(special) == 4, 'first-anchor neighbors')
    histogram = Counter()
    examined = 0
    # Complete literal partitions, then quotient their special signatures.
    for part in triple_partitions(neighbors):
        examined += 1
        if all(pairs(mask((A,) + t)) <= case['available'] for t in part):
            signature = tuple(sorted(tuple(x for x in t if x in special) for t in part))
            histogram[signature] += 1
    insist(examined == 15400, 'first-anchor partition domain incomplete')
    insist(all(count == factorial(8) // (factorial(sum(not part for part in signature)) *
               prod(factorial(3-len(part)) for part in signature)) for signature, count in histogram.items()),
           'literal ordinary filling fibers disagree with multinomial formula')
    small = small_maps(case)
    pending = set(histogram)
    records = []
    while pending:
        rep = min(pending)
        orbit = {relabel_family(rep, p) for p in small}
        insist(orbit <= pending, 'special signature cover overlaps or leaves domain')
        pending -= orbit
        next_point = 0
        quads = []
        for s in rep:
            ordinary = tuple(range(next_point, next_point + 3 - len(s)))
            next_point += len(ordinary)
            quads.append(tuple(sorted((A,) + ordinary + s)))
        insist(next_point == 8 and all(pairs(mask(q)) <= case['available'] for q in quads), 'bad consecutive filling')
        records.append({'signature': rep, 'quads': tuple(sorted(quads)), 'small': small,
                        'signature_orbit': tuple(sorted(orbit)),
                        'filling_counts': tuple((s, histogram[s]) for s in sorted(orbit))})
    return records, {'all_partitions': examined, 'legal_quartets': sum(histogram.values()),
                     'special_signatures': len(histogram), 'small_group': len(small), 'orbits': len(records)}


def stabilizer(case, anchor):
    # Different group algorithm: test every ordinary permutation and special map.
    target = frozenset(anchor['quads'])
    group = []
    checked = 0
    started = time.monotonic()
    for ordinary in permutations(ORDINARY):
        for special in anchor['small']:
            checked += 1
            if checked > 200000 or (checked % 1024 == 0 and time.monotonic() - started > 10):
                raise RuntimeError('INCOMPLETE: ordinary permutation guard')
            p = ordinary + special[8:]
            if all(tuple(sorted(p[x] for x in q)) in target for q in anchor['quads']):
                group.append(p)
    insist(all(len(set(p)) == 17 and all(p[x] == x for x in (A, B, V)) and
               frozenset(relabel_family(case['leave'], p)) == case['leave'] and
               relabel_family(case['fixed'], p) == case['fixed'] and
               relabel_family(anchor['quads'], p) == anchor['quads'] for p in group), 'false stabilizer map')
    # Literal closure and inverses: tiny groups, at most144 members.
    reached = set(group)
    insist(tuple(range(17)) in reached and len(reached) == len(group), 'stabilizer identity/duplicates')
    insist(all(tuple(p[q[x]] for x in POINTS) in reached for p in group for q in group), 'stabilizer not closed')
    return tuple(group), checked


def second_anchor(case, anchor, group):
    fixed = tuple(sorted(case['fixed'] + anchor['quads']))
    used = frozenset(e for q in fixed for e in pairs(mask(q)))
    insist(len(used) == 6 * len(fixed), 'prefix repeats pairs')
    available = case['available'] - used
    neighbors = tuple(x for x in POINTS if x != B and tuple(sorted((x, B))) in available)
    existing = sum(B in q for q in fixed)
    insist((existing, len(neighbors)) == ((1, 9) if case['index'] == 1 else (0, 12)), 'second-anchor neighbor count')
    legal = set()
    examined = 0
    for part in triple_partitions(neighbors):
        examined += 1
        quads = tuple(sorted(tuple(sorted((B,) + t)) for t in part))
        if all(pairs(mask(q)) <= available for q in quads):
            legal.add(quads)
    insist(examined == (280 if existing else 15400), 'second-anchor partitions incomplete')
    pending = set(legal)
    records = []
    while pending:
        rep = min(pending)
        orbit = {relabel_family(rep, p) for p in group}
        insist(orbit <= pending, 'second-anchor orbit cover overlaps or leaves domain')
        pending -= orbit
        prefix = tuple(sorted(fixed + rep))
        used = Counter(e for q in prefix for e in pairs(mask(q)))
        insist(set(used.values()) == {1} and sum(A in q for q in prefix) == sum(B in q for q in prefix) == 4 and
               sum(V in q for q in prefix) == 2, 'invalid anchor prefix')
        rows = tuple(sorted(ALL_PAIRS - case['leave'] - set(used)))
        # Inspect all2380 quadruples, including anchors; no preset residual pool.
        columns = tuple(q for q in combinations(POINTS, 4) if pairs(mask(q)) <= set(rows))
        insist(len(rows) == (66 if existing else 60) and not any(x in (A, B, V) for e in rows for x in e), 'residual row domain')
        records.append({'prefix': prefix, 'orbit_size': len(orbit), 'rows': rows, 'columns': columns,
                        'input_sha256': sha256(encoded([rows, columns])).hexdigest()})
    return records, {'all_partitions': examined, 'legal_groups': len(legal), 'orbits': len(records)}


def tree_check(rows, columns, tree, limit=200000):
    """Check each cofactor by exact integer row masks and all surviving columns."""
    positions = {e: j for j, e in enumerate(rows)}
    column_masks = tuple(sum(1 << positions[e] for e in pairs(mask(q))) for q in columns)
    insist(all(m.bit_count() == 6 for m in column_masks), 'invalid column row mask')
    nodes = 0

    def visit(remaining, node):
        nonlocal nodes
        nodes += 1
        if nodes > limit:
            raise RuntimeError('INCOMPLETE: tree verifier node guard')
        insist(remaining and isinstance(node, list) and len(node) == 2, 'accepting leaf or malformed tree')
        pivot, children = node
        insist(type(pivot) is int and 0 <= pivot < len(rows) and remaining >> pivot & 1 and isinstance(children, list), 'invalid uncovered pivot')
        available = [j for j, m in enumerate(column_masks) if m & remaining == m and m >> pivot & 1]
        insist(all(isinstance(child, list) and len(child) == 2 and type(child[0]) is int for child in children), 'malformed child')
        insist([child[0] for child in children] == available, 'branch list is not complete or is duplicated')
        for j, child in children:
            visit(remaining ^ column_masks[j], child)

    visit((1 << len(rows)) - 1, tree)
    return nodes


def rebuild(certificate):
    insist(certificate.get('schema') == 'pair-two-completion-v1' and len(certificate['cases']) == 198, 'certificate header')
    summaries, records = [], []
    for ci in (1, 3, 4):
        case = make_case(ci)
        anchors, acheck = first_anchor(case)
        for ai, anchor in enumerate(anchors):
            group, permutation_checks = stabilizer(case, anchor)
            second, bcheck = second_anchor(case, anchor, group)
            summaries.append({'first_case': ci, 'a_case': ai, 'a_pattern': anchor['signature'], 'a_quads': anchor['quads'],
                              'A_coverage': {'partitions_checked': acheck['all_partitions'], 'compatible_labeled_quartets': acheck['legal_quartets'],
                                             'special_patterns': acheck['special_signatures'], 'A_quartet_orbits': acheck['orbits']},
                              'B_coverage': {'partitions_checked': bcheck['all_partitions'], 'compatible_labeled_B_groups': bcheck['legal_groups'],
                                             'checked_A_stabilizer_size': len(group), 'B_group_orbits': bcheck['orbits']}})
            insist(encoded(summaries[-1]) == encoded(certificate['carrier_summary'][len(summaries)-1]), 'entrywise anchor summary mismatch')
            for bi, record in enumerate(second):
                index = len(records)
                published = certificate['cases'][index]
                wanted = {'index': index, 'first_case': ci, 'a_case': ai, 'b_case': bi, 'orbit_size': record['orbit_size'],
                          'fixed_quads': record['prefix'], 'input_sha256': record['input_sha256']}
                insist(encoded(wanted) == encoded({k: published[k] for k in wanted}), 'entrywise certificate carrier mismatch')
                count = tree_check(record['rows'], record['columns'], published['tree'])
                records.append({'index': index, 'first_case': ci, 'a_case': ai, 'b_case': bi, 'rows': record['rows'],
                                'columns': record['columns'], 'prefix': record['prefix'], 'tree_nodes': count})
            print(json.dumps({'first_case': ci, 'a_case': ai, 'stabilizer': len(group), 'ordinary_permutations_checked': permutation_checks,
                              'second_groups': bcheck['legal_groups'], 'residual_cases': len(second)}), flush=True)
    insist(len(summaries) == 8 and len(records) == 198 and sum(r['tree_nodes'] for r in records) == 351, 'complete certificate census differs')
    return summaries, records


def main(args):
    started = time.monotonic()
    raw = (args.target / 'pair_two_certificate.json').read_bytes()
    insist(sha256(raw).hexdigest() == '2342bc655261f8e0a8a56a87035e09bc652513c42946e379c61b6a990e2c8cb8', 'external certificate bytes changed')
    certificate = json.loads(raw)
    summaries, records = rebuild(certificate)
    stream = sha256(encoded([[r['first_case'], r['a_case'], r['b_case'], r['prefix'], r['rows'], r['columns']]
                            for r in records])).hexdigest()
    insist(stream == '41915997fc45ff79ff155b3f27d13d456a0d53425baa792e194c273a730f1b19',
           'complete entrywise reconstructed stream differs')
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'COMPLETE independent carrier/tree reproduction',
              'anchor_cases': len(summaries), 'residual_cases': len(records), 'tree_nodes': sum(r['tree_nodes'] for r in records),
              'max_tree_nodes': max(r['tree_nodes'] for r in records), 'candidate_columns_range': [min(len(r['columns']) for r in records), max(len(r['columns']) for r in records)],
              'input_stream_sha256': stream, 'certificate_sha256': sha256(raw).hexdigest(),
              'seconds': time.monotonic() - started, 'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.work.mkdir(parents=True, exist_ok=True)
    (args.work / 'carrier.json').write_bytes(encoded({'summaries': summaries, 'records': records}))
    (args.work / 'summary.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--target', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    main(p.parse_args())
