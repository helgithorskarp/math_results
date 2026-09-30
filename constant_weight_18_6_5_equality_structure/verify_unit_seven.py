#!/usr/bin/env python3
"""Rebuild seven-edge carriers by direct zero-block scans; replay set proofs."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

HERE = Path(__file__).resolve().parent
HIGH = frozenset(range(5))
LOW = tuple(range(5, 17))
ALL_PAIRS = frozenset(combinations(range(17), 2))
ALL_QUADS = tuple(combinations(range(17), 4))
QUAD_PAIRS = {q: frozenset(combinations(q, 2)) for q in ALL_QUADS}
NAMES = ('triangle', 'path', 'wedge_edge')
LEAVES = {
    'triangle': frozenset({(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
                          (0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10),
                          (11, 12), (13, 14), (15, 16)}),
    'path': frozenset({(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 4), (3, 4),
                      (0, 5), (1, 6), (1, 7), (2, 8), (2, 9), (3, 10),
                      (11, 12), (13, 14), (15, 16)}),
    'wedge_edge': frozenset({(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4),
                            (0, 5), (1, 6), (1, 7), (2, 8), (3, 9), (4, 10),
                            (11, 12), (13, 14), (15, 16)})}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode('ascii')


def digest(value):
    return sha256(encoded(value)).hexdigest()


def moved(q, p):
    return tuple(sorted(p[x] for x in q))


def action(prefix, p):
    return tuple(sorted(moved(q, p) for q in prefix))


def valid(leave, prefix):
    multiplicities = Counter(e for q in prefix for e in QUAD_PAIRS[q])
    return set(multiplicities.values()) == {1} and not set(multiplicities) & leave


def direct_group(leave):
    """Filter all 5!, all attached 6!, and all matched 6! permutations."""
    high_edges = {e for e in leave if e[1] < 5}
    neighbors = {x: h for h, x in leave if h < 5 <= x}
    special = tuple(sorted(neighbors))
    matched = tuple(x for x in LOW if x not in neighbors)
    matched_edges = {e for e in leave if e[0] >= 5}
    low_maps = tuple(p for p in permutations(matched)
                     if {tuple(sorted((p[matched.index(a)], p[matched.index(b)])))
                         for a, b in matched_edges} == matched_edges)
    require(len(low_maps) == 48, 'wrong directly filtered matching map count')
    maps = []
    for h in permutations(range(5)):
        if {moved(e, h) for e in high_edges} != high_edges:
            continue
        for a in permutations(special):
            if any(h[neighbors[x]] != neighbors[y] for x, y in zip(special, a)):
                continue
            for b in low_maps:
                p = list(h) + list(LOW)
                for x, y in zip(special, a):
                    p[x] = y
                for x, y in zip(matched, b):
                    p[x] = y
                p = tuple(p)
                require(len(set(p)) == 17 and {moved(e, p) for e in leave} == set(leave),
                        'direct map changes the actual leave')
                maps.append(p)
    expected = 4608 if leave == LEAVES['triangle'] else 384
    require(len(maps) == len(set(maps)) == expected, 'wrong direct group size')
    return tuple(sorted(maps))


def direct_tails(leave):
    covered = tuple(e for e in combinations(range(5), 2) if e not in leave)
    columns = tuple(q for q in ALL_QUADS if len(set(q) & HIGH) == 2 and not QUAD_PAIRS[q] & leave)
    options = [tuple(q for q in columns if tuple(v for v in q if v in HIGH) == e) for e in covered]
    raw = set()
    for a, b, c in product(*options):
        if QUAD_PAIRS[a] & QUAD_PAIRS[b] or QUAD_PAIRS[c] & (QUAD_PAIRS[a] | QUAD_PAIRS[b]):
            continue
        raw.add((a, b, c))
    return frozenset(raw)


def direct_quotient(raw, group):
    remaining, records = set(raw), []
    while remaining:
        root = min(remaining)
        images = {action(root, p) for p in group}
        require(images <= raw and not (images - remaining), 'direct orbit overlap or escape')
        stabilizer = tuple(p for p in group if action(root, p) == root)
        require(len(images) * len(stabilizer) == len(group), 'direct orbit-stabilizer failure')
        remaining -= images
        records.append((root, len(images), stabilizer))
    require(sum(n for _, n, _ in records) == len(raw), 'direct quotient incomplete')
    return records


class Incomplete(Exception):
    """No verdict when a fixed operational guard is reached."""


def direct_zeros(leave, tail, node_limit=200000, seconds=10):
    """Choose the first two sorted zero blocks; derive the third from incidences."""
    special = {x for h, x in leave if h < 5 <= x}
    counts = {x: int(x in special) + sum(len(set(q) & HIGH) - 1 for q in tail if x in q)
              for x in LOW}
    counts = {x: n for x, n in counts.items() if n}
    require(sum(counts.values()) == 12, 'direct zero incidence total')
    forbidden = set(leave) | {e for q in tail for e in QUAD_PAIRS[q]}
    candidates = tuple(q for q in ALL_QUADS if not set(q) & HIGH
                       and all(x in counts for x in q) and not QUAD_PAIRS[q] & forbidden)
    raw, nodes, start = set(), 0, time.monotonic()
    for i, a in enumerate(candidates):
        remaining = {x: n - int(x in a) for x, n in counts.items()}
        for b in candidates[i+1:]:
            nodes += 1
            if nodes > node_limit or (nodes % 128 == 0 and time.monotonic() - start > seconds):
                raise Incomplete('INCOMPLETE: direct zero-frame guard reached')
            if QUAD_PAIRS[a] & QUAD_PAIRS[b] or any(remaining[x] <= 0 for x in b):
                continue
            after = {x: n - int(x in b) for x, n in remaining.items() if n - int(x in b)}
            if len(after) != 4 or set(after.values()) != {1}:
                continue
            c = tuple(sorted(after))
            if c <= b or QUAD_PAIRS[c] & (forbidden | QUAD_PAIRS[a] | QUAD_PAIRS[b]):
                continue
            z = a, b, c
            require(valid(leave, tail + z) and Counter(x for q in z for x in q) == Counter(counts),
                    'direct invalid zero frame')
            raw.add(z)
    return frozenset(raw)


def direct_triples(leave):
    special = {x for h, x in leave if h < 5 <= x}
    multi = tuple(q for q in ALL_QUADS if len(set(q) & HIGH) == 3 and not QUAD_PAIRS[q] & leave)
    raw = set()
    for q in multi:
        counts = Counter({x: int(x in special) + 2*int(x in q) for x in LOW})
        counts = +counts
        for a in ALL_QUADS:
            if set(a) & HIGH or any(x not in counts for x in a):
                continue
            remaining = counts - Counter(a)
            if len(remaining) != 4 or set(remaining.values()) != {1}:
                continue
            b = tuple(sorted(remaining))
            prefix = q, a, b
            if a < b and valid(leave, prefix):
                require(Counter(x for z in (a, b) for x in z) == counts, 'direct triple incidence mismatch')
                raw.add(prefix)
    return frozenset(raw)


def direct_case(name, branch, prefix, orbit, stabilizer, index):
    leave = LEAVES[name]
    require(valid(leave, prefix), 'direct invalid fixed prefix')
    rows = tuple(sorted(ALL_PAIRS - leave - {e for q in prefix for e in QUAD_PAIRS[q]}))
    columns = tuple(q for q in ALL_QUADS if len(set(q) & HIGH) == 1 and QUAD_PAIRS[q] <= set(rows))
    require(len(rows) == (102 if branch == 'triple' else 84), 'direct pair count mismatch')
    return {'index': index, 'model': name, 'branch': branch, 'fixed_quads': prefix,
            'orbit_size': orbit, 'stabilizer_order': stabilizer,
            'rows': rows, 'columns': columns, 'input_sha256': digest([prefix, rows, columns])}


def rebuild():
    cases, summaries, carriers = [], [], {}
    for name in NAMES:
        leave = LEAVES[name]
        group, tails = direct_group(leave), direct_tails(leave)
        records = direct_quotient(tails, group)
        carriers[name] = {'group': group, 'tails': tails, 'zeros': {}}
        if name == 'triangle':
            raw = direct_triples(leave)
            q = direct_quotient(raw, group)
            carriers[name]['triples'] = raw
            for prefix, n, stabilizer in q:
                cases.append(direct_case(name, 'triple', prefix, n, len(stabilizer), len(cases)))
            summaries.append({'model': name, 'branch': 'triple', 'group_order': len(group),
                              'group_sha256': digest(group), 'raw_prefixes': len(raw),
                              'raw_prefixes_sha256': digest(sorted(raw)), 'prefix_orbits': len(q)})
        first, weight, fibers = len(cases), 0, []
        for tail, n, stabilizer in records:
            zero = direct_zeros(leave, tail)
            q = direct_quotient(zero, stabilizer)
            carriers[name]['zeros'][tail] = zero
            weight += n * len(zero)
            fibers.append([tail, n, len(stabilizer), sorted(zero)])
            for z, zn, zstabilizer in q:
                cases.append(direct_case(name, 'double', tail + z, n*zn, len(zstabilizer), len(cases)))
        summaries.append({'model': name, 'branch': 'double', 'group_order': len(group),
                          'group_sha256': digest(group), 'raw_tails': len(tails),
                          'raw_tails_sha256': digest(sorted(tails)), 'tail_orbits': len(records),
                          'raw_prefixes': weight, 'prefix_orbits': len(cases) - first,
                          'zero_fibers_sha256': digest(fibers)})
    return cases, summaries, carriers


def replay_tree(tree, rows, columns):
    edges = tuple(QUAD_PAIRS[q] for q in columns)
    nodes = 0

    def visit(node, left):
        nonlocal nodes
        nodes += 1
        require(bool(left), 'rejection proof reached a positive cover')
        require(type(node) is list and len(node) == 2, 'malformed rejection node')
        pivot, children = node
        require(type(pivot) is int and 0 <= pivot < len(rows) and rows[pivot] in left,
                'pivot is not an uncovered pair')
        require(type(children) is list and all(type(c) is list and len(c) == 2 and type(c[0]) is int
                                              for c in children), 'malformed branches')
        compatible = [j for j, e in enumerate(edges) if rows[pivot] in e and e <= left]
        require([c[0] for c in children] == compatible, 'missing, extra or reordered compatible branch')
        for j, child in children:
            visit(child, left - edges[j])

    visit(tree, frozenset(rows))
    return nodes


def verify_certificate(certificate, cases, summaries):
    require(certificate.get('schema') == 'all-unit-seven-cores-v1', 'wrong certificate schema')
    require(certificate.get('carrier_summary_sha256') == digest(summaries), 'carrier hash mismatch')
    stream = digest([[c['fixed_quads'], c['rows'], c['columns']] for c in cases])
    require(certificate.get('input_stream_sha256') == stream, 'input stream hash mismatch')
    trees = certificate.get('trees')
    require(type(trees) is list and len(trees) == len(cases), 'missing or extra proof tree')
    return [replay_tree(tree, c['rows'], c['columns']) for tree, c in zip(trees, cases)]


def controls(certificate, cases, summaries):
    mutations = []
    bad = deepcopy(certificate)
    bad['trees'][0][1].pop()
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['trees'][0][0] = 102
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['trees'][0][1][0][0] = 10000
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['trees'].pop()
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['input_stream_sha256'] = '0'*64
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['carrier_summary_sha256'] = '0'*64
    mutations.append(bad)
    for bad in mutations:
        try:
            verify_certificate(bad, cases, summaries)
        except ValueError:
            continue
        raise ValueError('corrupted certificate accepted')

    def multiply(a, b):
        result = 0
        for _ in range(2):
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return result

    fixed = [tuple(4*x+y for y in range(4)) for x in range(4)]
    witness = [tuple(sorted(4*x+(multiply(slope, x)^b) for x in range(4)))
               for slope in range(4) for b in range(4)]
    all_edges = Counter(e for q in fixed+witness for e in QUAD_PAIRS[q])
    rows = tuple(sorted(set(all_edges) - {e for q in fixed for e in QUAD_PAIRS[q]}))
    covered = Counter(e for q in witness for e in QUAD_PAIRS[q])
    require(len(all_edges) == 120 and set(all_edges.values()) == {1}, 'invalid affine fixture')
    require(len(rows) == 96 and set(covered) == set(rows) and set(covered.values()) == {1},
            'positive affine residual cover rejected')
    one = (0, 1, 2, 3)
    false_rejections = 0
    for fake in ([0, []], [0, [[0, [0, []]]]]):
        try:
            replay_tree(fake, tuple(sorted(QUAD_PAIRS[one])), (one,))
        except ValueError:
            false_rejections += 1
        else:
            raise ValueError('false rejection proof for a positive input accepted')
    return rows, tuple(witness), {'invalid_certificate_controls_rejected': len(mutations),
                                 'positive_affine_residual_cover_accepted': True,
                                 'false_positive_rejection_proofs_rejected': false_rejections}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-primary', action='store_true')
    args = parser.parse_args()
    cases, summaries, carriers = rebuild()
    data = (HERE / 'unit_seven_certificate.json').read_bytes()
    expected = json.loads((HERE / 'unit_seven_expected.json').read_text())
    require(sha256(data).hexdigest() == expected['certificate_sha256'], 'certificate byte hash mismatch')
    require(len(data) == expected['certificate_bytes'], 'certificate byte count mismatch')
    certificate = json.loads(data)
    nodes = verify_certificate(certificate, cases, summaries)
    require(len(cases) == expected['cases'] and sum(nodes) == expected['nodes'], 'case or node counts differ')
    require(digest(nodes) == expected['nodes_per_case_sha256'], 'casewise node counts differ')
    require(digest(summaries) == expected['carrier_summary_sha256'], 'expected carrier hash differs')
    require(certificate['input_stream_sha256'] == expected['input_stream_sha256'], 'expected input hash differs')
    rows, columns, checks = controls(certificate, cases, summaries)
    if args.compare_primary:
        import check_unit_seven as primary
        other, other_summaries, other_carriers = primary.generate()
        require(encoded(cases) == encoded(other) and encoded(summaries) == encoded(other_summaries),
                'complete case stream differs entry by entry')
        require(carriers == other_carriers, 'actual maps, raw tails or raw zero fibers differ entry by entry')
        for name in NAMES:
            require(primary.model(name)['leave'] == LEAVES[name], 'literal leave definition differs')
        try:
            primary.rejection_tree(rows, columns)
        except primary.CoverFound:
            checks['primary_detects_positive_cover'] = True
        else:
            raise ValueError('primary did not detect the positive residual cover')
        for call in (lambda: primary.rejection_tree(cases[0]['rows'], cases[0]['columns'], node_limit=0),
                     lambda: primary.zero_frames(primary.model('triangle'), min(carriers['triangle']['tails']), node_limit=0)):
            try:
                call()
            except primary.Incomplete:
                continue
            raise ValueError('zero node cap returned a mathematical verdict')
        checks['zero_cover_and_carrier_caps_return_incomplete'] = True
    print(json.dumps({'agent': 'six-code-1', 'role': 'researcher', 'status': 'COMPLETE_LITERAL_REPLAY',
                      'cases': len(cases), 'nodes': sum(nodes), 'maximum_nodes_per_case': max(nodes),
                      'branches': summaries, 'certificate_bytes': len(data),
                      'certificate_sha256': sha256(data).hexdigest(),
                      'input_stream_sha256': certificate['input_stream_sha256'],
                      'ordinary_bridges_formalized': False, 'independent_peer_review': False,
                      'global_72_word_exclusion': False, **checks}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
