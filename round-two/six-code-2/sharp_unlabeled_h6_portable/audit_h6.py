"""Literal MRV/physical-graph/incidence audit of the specified Q+h6 model.

six-code-2, researcher. No producer imports. Known69 is validation only;
same-author algorithm independence is separate from independent-person review.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from point_helpers import encoded, literal, point_set, require


def core_family(cap, old, holes, q, guard):
    domains = {i: tuple(old[i] - {p} for p in sorted(old[i] & cap)
                       if len((old[i] - {p}) & q) <= 1)
               for i in range(len(old)) if i not in holes and len(old[i] & cap) >= 3}
    require(all(len(t) == 4 and len(t & cap) <= 2 for ts in domains.values() for t in ts),
            'physical tail domain')
    keys, nodes = set(), 0
    def visit(assignment):
        nonlocal nodes
        nodes += 1
        if nodes % 2048 == 0:
            guard('adaptive-literal-MRV')
        if len(assignment) == len(domains):
            keys.add(tuple((i, literal(t)) for i, t in sorted(assignment.items())))
            return
        available = {i: tuple(t for t in ts if all(len(t & u) <= 1 for u in assignment.values()))
                     for i, ts in domains.items() if i not in assignment}
        chosen = min(available, key=lambda i: (len(available[i]), i))
        for tail in available[chosen]:
            visit(assignment | {chosen: tail})
    visit({})
    return keys, nodes, len(domains)


def check_keys(actual, expected):
    require(actual == expected, 'physical complete core keys differ')


def check_holes(actual, blockers, extras):
    require(len(extras) == 2 and len(set(extras)) == 2 and not set(extras) & blockers and
            actual == blockers | set(extras) and len(actual) == 6,
            'exact physical six empty parents differ')


def check_row(actual, expected):
    require(actual == expected, 'complete physical row differs')


def check_color(colors, i, j):
    require(colors[i] != colors[j], 'same-color physical edge')


def packing(words, size):
    require(len(words) == len(set(words)) == size, 'positive distinct word count')
    require(all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5 for w in words),
            'positive weight-five domain')
    physical = tuple(frozenset(v for v in range(18) if w >> v & 1) for w in words)
    require(all(len(a & b) <= 2 for a, b in combinations(physical, 2)), 'positive physical collision')
    triples = [t for w in physical for t in combinations(sorted(w), 3)]
    require(len(triples) == len(set(triples)) == 10 * size, 'positive triple ownership')
    return physical


def boundary(words, old, q, holes, size):
    ps = packing(words, size)
    removed = set(old) - set(ps)
    caps = tuple(w for w in ps if 17 not in w and w not in old)
    contained, noncontained, represented = [], [], set()
    for word in ps:
        if 17 not in word:
            continue
        tail = word - {17}
        owners = [b for b in old if tail <= b]
        if owners:
            require(len(owners) == 1 and owners[0] in removed and owners[0] not in represented,
                    'physical represented-parent decoding')
            represented.add(owners[0]); contained.append(tail)
        else:
            noncontained.append(tail)
    require(noncontained == [q], 'exact physical noncontained tail differs')
    require(removed - represented == holes, 'positive empty-parent boundary differs')
    require(len(removed) == len(contained) + 6 and len(caps) == size - 63,
            'positive h6 counting identity differs')
    return {'size': size, 's': len(caps), 'a': len(contained), 't': 1,
            'R': len(removed), 'h': 6, 'empty_parents': sorted(literal(b) for b in holes),
            'word_pair_checks': size * (size - 1) // 2, 'owned_triples': 10 * size}


def rejection(label, callback, expected):
    try:
        callback()
    except ValueError as error:
        require(str(error) == expected, 'control rejected for unintended reason: ' + label)
        return label
    raise ValueError('semantic damage accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    for name in ['parent', 'carrier', 'graph', 'colors', 'producer-summary', 'witness-dir', 'baseline69', 'control69', 'work']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--control-a', type=int, required=True)
    parser.add_argument('--control-R', type=int, required=True)
    args = parser.parse_args()
    require(args.control_a >= 0 and args.control_R == args.control_a + 6, 'expected h6 control identity')
    require(not args.work.exists(), 'fresh physical h6 audit required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    def guard(stage):
        require(time.monotonic() - begin < 60, 'INCOMPLETE original60s h6 audit: ' + stage)
    raw = args.carrier.read_bytes(); d = json.loads(raw)
    fixture = json.loads(args.parent.read_bytes())
    old = tuple(point_set(w, 5) for w in sorted(fixture['words']))
    require(d['parent_words'] == sorted(fixture['words']) and len(old) == len(set(old)) == 68,
            'literal specified68D')
    triples = [t for b in old for t in combinations(sorted(b), 3)]
    require(len(triples) == len(set(triples)) == 680 and set(triples) == set(combinations(range(17), 3)),
            'literal complete680-tripleD')
    q = point_set(d['noncontained_q'], 4)
    require(not any(q <= b for b in old), 'Q must be noncontained')
    blockers = {b for b in old if len(b & q) >= 3}
    require(len(blockers) == 4 and all(len(b & q) == 3 for b in blockers), 'four literal Q-triple blockers')
    extras = tuple(point_set(w, 5) for w in d['additional_empty_parents'])
    require(len(extras) == 2 and all(b in old for b in extras), 'extra parents outside literalD')
    holes = {point_set(w, 5) for w in d['hole_words']}
    check_holes(holes, blockers, extras)
    hole_ids = {i for i, b in enumerate(old) if b in holes}
    require(d['status'] == 'COMPLETE_SINGLE_NONCONTAINED_Q_CAP_CARRIER_SIX_EMPTY_STEINER_PARENTS' and d['h'] == 6 and d['hole_indices'] == sorted(hole_ids), 'physical h6 hole indices differ')
    caps = tuple(frozenset(ps) for ps in combinations(range(17), 5)
                 if frozenset(ps) not in old and len(frozenset(ps) & q) <= 2 and
                 all(len(frozenset(ps) & b) <= 3 for i, b in enumerate(old) if i not in hole_ids))
    require([entry['cap'] for entry in d['caps']] == [literal(c) for c in caps], 'complete cap carrier/order')
    actual, core_caps, core_tails = defaultdict(set), [], []
    cap_domain = set(caps)
    for core in d['cores']:
        c = point_set(core['cap'], 5); ids, tails = core['parents'], core['tails']
        require(c in cap_domain and len(ids) == len(set(ids)) == len(tails) and
                set(ids) == {i for i, b in enumerate(old) if i not in hole_ids and len(c & b) >= 3},
                'physical core required-parent domain')
        ts = tuple(point_set(t, 4) for t in tails)
        require(all(t <= old[i] and len(t & q) <= 1 and len(t & c) <= 2 for i, t in zip(ids, ts)) and
                all(len(t & u) <= 1 for t, u in combinations(ts, 2)), 'physical required-tail compatibility')
        key = tuple(sorted(zip(ids, tails)))
        require(key not in actual[c], 'duplicate physical core')
        actual[c].add(key); core_caps.append(c); core_tails.append(ts)
    offset, mr_nodes, key_digest, histogram = 0, 0, hashlib.sha256(), Counter()
    for c, entry in zip(caps, d['caps']):
        expected, nodes, parents = core_family(c, old, hole_ids, q, guard)
        mr_nodes += nodes
        require(mr_nodes <= 2_000_000, 'INCOMPLETE original two-million physical MRV states')
        check_keys(actual[c], expected)
        require(entry['first_core'] == offset and entry['core_count'] == len(expected) and
                all(row['cap'] == literal(c) for row in d['cores'][offset:offset + len(expected)]),
                'zero/positive cap-prefix coverage')
        offset += len(expected)
        key_digest.update(encoded([literal(c), sorted(expected)]))
        histogram[tuple(len(c & point_set(w, 5)) for w in d['hole_words']) + (parents, len(expected))] += 1
        guard('complete-literal-cap-keys')
    require(offset == len(d['cores']), 'complete core prefix differs')
    cap_occ, tail_occ = defaultdict(int), defaultdict(int)
    for i, (c, ts) in enumerate(zip(core_caps, core_tails)):
        cap_occ[c] |= 1 << i
        for tail in ts:
            tail_occ[tail] |= 1 << i
    cap3, tail3, tail2 = defaultdict(int), defaultdict(int), defaultdict(int)
    for c, bits in cap_occ.items():
        for t in combinations(sorted(c), 3): cap3[t] |= bits
    for tail, bits in tail_occ.items():
        for t in combinations(sorted(tail), 3): tail3[t] |= bits
        for t in combinations(sorted(tail), 2): tail2[t] |= bits
    cap_bad, tail_bad = {}, {}
    for c in cap_occ:
        bad = 0
        for t in combinations(sorted(c), 3): bad |= cap3[t] | tail3[t]
        cap_bad[c] = bad
    for tail in tail_occ:
        cb, pb = 0, 0
        for t in combinations(sorted(tail), 3): cb |= cap3[t]
        for t in combinations(sorted(tail), 2): pb |= tail2[t]
        tail_bad[tail] = cb | (pb & ~tail_occ[tail])
    gr = args.graph.read_bytes(); g = json.loads(gr)
    color_raw = args.colors.read_bytes(); cd = json.loads(color_raw); colors = cd['colors']
    n = len(core_caps); all_bits = (1 << n) - 1
    require(g['vertices'] == n and len(g['adjacency_hex']) == n and
            g['core_carrier_sha256'] == hashlib.sha256(raw).hexdigest(), 'physical graph scope')
    require(g['hole_words'] == d['hole_words'] and g['noncontained_q'] == literal(q) and g['h'] == 6 and
            g['additional_empty_parents'] == d['additional_empty_parents'], 'physical graph parameters')
    require(len(colors) == n and all(type(c) is int and 0 <= c < cd['color_count'] for c in colors) and
            cd['graph_sha256'] == hashlib.sha256(gr).hexdigest(), 'positive color domain/scope')
    neighbors, row_digest, degrees, expected_rows = [], hashlib.sha256(), Counter(), []
    for i, (c, ts) in enumerate(zip(core_caps, core_tails)):
        bad = cap_bad[c]
        for tail in ts: bad |= tail_bad[tail]
        row = all_bits & ~bad
        check_row(int(g['adjacency_hex'][i], 16), row)
        require(not row >> i & 1, 'physical self edge')
        expected_rows.append(row); row_digest.update(encoded([i, format(row, 'x')])); degrees[row.bit_count()] += 1
        nb = set()
        while row:
            bit = row & -row; row ^= bit; j = bit.bit_length() - 1
            check_color(colors, i, j); nb.add(j)
        neighbors.append(nb)
        if i % 256 == 0: guard('complete-literal-graph-and-colors')
    require(sum(k * v for k, v in degrees.items()) == 2 * g['edges'] and
            all(i in neighbors[j] for i, row in enumerate(neighbors) for j in row), 'physical edges/symmetry')
    edge_tests = triple_tests = pair_tests = six_tests = seven_tests = tri_inc = four_inc = five_inc = six_inc = seven_inc = 0
    for i, row in enumerate(neighbors):
        for j in sorted(v for v in row if v > i):
            edge_tests += 1; common = row & neighbors[j]; tri_inc += len(common)
            for k in sorted(common):
                triple_tests += 1; ck = sorted(common & neighbors[k]); four_inc += len(ck)
                for ell, m in combinations(ck, 2):
                    pair_tests += 1
                    if m not in neighbors[ell]: continue
                    five_inc += 1
                    remaining = [v for v in ck if v > m]
                    for last in remaining:
                        six_tests += 1
                        if last in neighbors[ell] and last in neighbors[m]: six_inc += 1
                    for nu, omega in combinations(remaining, 2):
                        seven_tests += 1
                        if (nu in neighbors[ell] and nu in neighbors[m] and omega in neighbors[ell] and
                            omega in neighbors[m] and omega in neighbors[nu]):
                            seven_inc += 1
            require(edge_tests + triple_tests + pair_tests + six_tests + seven_tests <= 2_000_000,
                    'INCOMPLETE original two-million physical clique states')
        if i % 128 == 0: guard('physical-edge-clique-incidences')
    require(tri_inc % 3 == four_inc % 12 == five_inc % 30 == six_inc % 60 == seven_inc % 105 == 0,
            'physical clique incidence divisibility')
    counts = {'triangles': tri_inc // 3, 'four_cliques': four_inc // 12,
              'five_cliques': five_inc // 30, 'six_cliques': six_inc // 60, 'seven_cliques': seven_inc // 105}
    summary_raw = args.producer_summary.read_bytes(); summary = json.loads(summary_raw)
    require(summary['graph_sha256'] == hashlib.sha256(gr).hexdigest() and
            summary['carrier_sha256'] == hashlib.sha256(raw).hexdigest() and
            all(summary[key] == value for key, value in counts.items()) and
            summary['edges'] == edge_tests == g['edges'], 'whole producer census differs')
    positives = []
    positive_words = None
    for size in range(63, 71):
        path = args.witness_dir / ('WITNESS%d.json' % size)
        if path.exists():
            words = json.loads(path.read_bytes())['words']
            positives.append(boundary(words, old, q, holes, size)); positive_words = words
    require(positive_words is not None, 'literal positive packing missing')
    baseline_raw = args.baseline69.read_bytes(); lines = baseline_raw.decode().splitlines()
    require(len(lines) == 69 and all(len(s) == 18 and set(s) <= {'0', '1'} for s in lines), 'literal known69 input')
    packing([int(s, 2) for s in lines], 69)
    control_raw = args.control69.read_bytes(); control = json.loads(control_raw)
    require(control['noncontained_q'] == literal(q) and control['hole_words'] == d['hole_words'] and control['h'] == 6,
            'known control69 scope differs')
    control_boundary = boundary(control['words'], old, q, holes, 69)
    require(control_boundary['s'] == 6 and control_boundary['a'] == args.control_a and control_boundary['R'] == args.control_R,
            'known control69 expected physical parameters')
    target = next(c for c in caps if actual[c]); expected = actual[target]
    damaged = set(expected); damaged.pop()
    controls = [rejection('omitted-valid-core', lambda: check_keys(damaged, expected), 'physical complete core keys differ')]
    controls.append(rejection('omitted-extra-empty-parent', lambda: check_holes(blockers, blockers, extras), 'exact physical six empty parents differ'))
    controls.append(rejection('extra-is-reserved-Q-parent', lambda: check_holes(holes, blockers, (next(iter(blockers)), extras[1])), 'exact physical six empty parents differ'))
    i = next(i for i, row in enumerate(neighbors) if row); j = min(neighbors[i])
    controls.append(rejection('omitted-valid-physical-edge', lambda: check_row(expected_rows[i] ^ (1 << j), expected_rows[i]), 'complete physical row differs'))
    damaged_colors = list(colors); damaged_colors[j] = colors[i]
    controls.append(rejection('same-color-physical-edge', lambda: check_color(damaged_colors, i, j), 'same-color physical edge'))
    size = len(positive_words); duplicated = list(positive_words[:-1]) + [positive_words[0]]
    controls.append(rejection('duplicate-positive-word', lambda: packing(duplicated, size), 'positive distinct word count'))
    first = sorted(packing(positive_words, size)[0])[:4]
    collision = next(literal(first) | (1 << p) for p in range(18)
                     if p not in first and (literal(first) | (1 << p)) not in positive_words)
    collided = list(positive_words[:-1]) + [collision]
    controls.append(rejection('distinct-weight-five-collision', lambda: packing(collided, size), 'positive physical collision'))
    other = next(b for b in old if b not in holes)
    controls.append(rejection('wrong-physical-empty-parent-boundary', lambda: boundary(positive_words, old, q, blockers | {other,extras[0]}, size), 'positive empty-parent boundary differs'))
    record = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_PHYSICAL_FIXED_Q_EXTRA_PAIR_H6_AUDIT',
              'noncontained_q': literal(q), 'additional_empty_parents': sorted(literal(b) for b in extras),
              'empty_holes': sorted(literal(b) for b in holes), 'h': 6,
              'prospective_caps': len(caps), 'zero_core_caps': sum(not actual[c] for c in caps),
              'cores': n, 'adaptive_MRV_nodes': mr_nodes,
              'physical_core_key_sha256': key_digest.hexdigest(),
              'physical_graph_row_sha256': row_digest.hexdigest(), 'complete_physical_rows': n,
              'edges': edge_tests, **counts, 'edge_tests': edge_tests,
              'triangle_neighborhood_tests': triple_tests, 'five_pair_tests': pair_tests,
              'six_extension_tests': six_tests, 'seven_extension_pair_tests': seven_tests,
              'physical_clique_states': edge_tests + triple_tests + pair_tests + six_tests + seven_tests,
              'proper_color_count': cd['color_count'], 'color_classes': sorted(Counter(colors).items()),
              'degree_histogram': sorted(degrees.items()),
              'cap_core_histogram': [list(k) + [v] for k, v in sorted(histogram.items())],
              'positive_witnesses': positives, 'maximum_positive_size': max(p['size'] for p in positives),
              'producer_summary_sha256': hashlib.sha256(summary_raw).hexdigest(),
              'known_baseline69_sha256': hashlib.sha256(baseline_raw).hexdigest(),
              'known_control69_sha256': hashlib.sha256(control_raw).hexdigest(), 'known_control69_boundary': control_boundary,
              'known69_is_new_research': False, 'semantic_damage_rejections': controls,
              'ordinary_bridges_formalized': False, 'independent_person_review': 'pending',
              'all_Q_or_all_extra_parents_or_global_claim': False,
              'scope': 'Only the specified literalD/y, fixed noncontainedQ and its four reserved parents plus two stated extra empty parents. Ordinary complete-core restriction, optional-tail restoration, gluing and incidence bridges are unformalized.'}
    guard('complete-physical-h6-audit')
    rb = encoded(record); (args.work / 'EXACT_RESULT.json').write_bytes(rb)
    execution = {'agent': 'six-code-2', 'role': 'researcher', 'seconds': time.monotonic() - begin,
                 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'original_math_seconds': 60, 'original_math_states': 2000000,
                 'exact_bytes': len(rb), 'exact_sha256': hashlib.sha256(rb).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
