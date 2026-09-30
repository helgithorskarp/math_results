#!/usr/bin/env python3
"""Rebuild the frame carrier from zero blocks and replay literal proof trees."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
HIGH = frozenset(range(5))
LOW = tuple(range(5, 17))
SPECIAL = frozenset(range(5, 9))
MATCHED = frozenset(range(9, 17))
ALL_PAIRS = frozenset(combinations(range(17), 2))
LEAVE = frozenset({(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4),
                   (2, 4), (3, 4), (0, 5), (1, 6), (2, 7), (3, 8),
                   (9, 10), (11, 12), (13, 14), (15, 16)})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def pair_set(q):
    return frozenset(combinations(sorted(q), 2))


def move(q, p):
    return tuple(sorted(p[v] for v in q))


def direct_group():
    """Filter all five-high permutations and all 8! matched-point bijections."""
    low_maps = []
    low_leave = {(9, 10), (11, 12), (13, 14), (15, 16)}
    for p in permutations(range(9, 17)):
        if {tuple(sorted((p[i], p[i+1]))) for i in (0, 2, 4, 6)} == low_leave:
            low_maps.append(p)
    require(len(low_maps) == 384, "direct matched-point map count")
    high_maps = [h for h in permutations(range(5))
                 if {tuple(sorted((h[a], h[b]))) for a, b in LEAVE if b < 5}
                 == {e for e in LEAVE if e[1] < 5}]
    require(len(high_maps) == 8 and all(h[4] == 4 for h in high_maps),
            "direct high map count or fixed point")
    result = []
    for h in high_maps:
        for low in low_maps:
            p = h + tuple(h[i] + 5 for i in range(4)) + low
            require(len(p) == len(set(p)) == 17, "direct nonpermutation")
            require({move(e, p) for e in LEAVE} == set(LEAVE), "direct map changes leave")
            result.append(p)
    require(len(set(result)) == 3072, "direct group count")
    return tuple(sorted(result))


def valid_prefix(quads):
    multiplicities = Counter(e for q in quads for e in pair_set(q))
    return (len(quads) == 4 and all(len(q) == len(set(q)) == 4 for q in quads)
            and set(multiplicities.values()) == {1} and not (set(multiplicities) & LEAVE))


def frame_quads(frame):
    a, b, zeros = frame
    return ((0, 1) + a, (2, 3) + b) + zeros


def direct_frames():
    """Start with the two zero-high blocks, then split their four matched points."""
    zero_candidates = [q for q in combinations(LOW, 4)
                       if len(set(q) & SPECIAL) == 2 and not (pair_set(q) & LEAVE)]
    raw = set()
    for z1, z2 in combinations(zero_candidates, 2):
        if set(z1) & set(z2) or (set(z1 + z2) & SPECIAL) != SPECIAL:
            continue
        tail_points = tuple(sorted(set(z1 + z2) & MATCHED))
        require(len(tail_points) == 4, "zero-block tail union")
        for a in combinations(tail_points, 2):
            b = tuple(x for x in tail_points if x not in a)
            frame = (a, b, (z1, z2))
            if valid_prefix(frame_quads(frame)):
                raw.add(frame)
    require(len(raw) == 2448, "direct raw frame count")
    # A second, deliberately less reduced enumeration checks the ordinary
    # incidence bridge: allow all twelve low points in both double tails.
    broad = set()
    for a in combinations(LOW, 2):
        if set(a) & {5, 6} or a in LEAVE:
            continue
        for b in combinations(LOW, 2):
            if set(b) & {7, 8} or b in LEAVE or a == b:
                continue
            multiplicities = Counter(SPECIAL)
            multiplicities.update(a)
            multiplicities.update(b)
            for z1 in combinations(sorted(multiplicities), 4):
                rest = multiplicities - Counter(z1)
                if any(n != 1 for n in rest.values()) or sum(rest.values()) != 4:
                    continue
                z2 = tuple(sorted(rest))
                if z1 < z2:
                    frame = (a, b, (z1, z2))
                    if valid_prefix(frame_quads(frame)):
                        broad.add(frame)
    require(broad == raw, "ordinary tail simplification lost frames")
    return frozenset(raw)


def frame_action(frame, p):
    quads = [move(q, p) for q in frame_quads(frame)]
    a = next(tuple(x for x in q if x >= 5) for q in quads if 0 in q and 1 in q)
    b = next(tuple(x for x in q if x >= 5) for q in quads if 2 in q and 3 in q)
    zeros = tuple(sorted(q for q in quads if not (set(q) & HIGH)))
    return a, b, zeros


def rebuild():
    group, raw = direct_group(), direct_frames()
    remaining = set(raw)
    cases = []
    while remaining:
        root = min(remaining)
        orbit = {frame_action(root, p) for p in group}
        require(orbit <= raw and orbit <= remaining, "direct invalid orbit")
        stabilizer = tuple(p for p in group if frame_action(root, p) == root)
        require(len(orbit)*len(stabilizer) == len(group), "direct orbit-stabilizer failure")
        remaining.difference_update(orbit)
        prefix = frame_quads(root)
        require(valid_prefix(prefix), "direct invalid fixed blocks")
        covered = frozenset(e for q in prefix for e in pair_set(q))
        rows = tuple(sorted(ALL_PAIRS - LEAVE - covered))
        row_set = frozenset(rows)
        # Scan all C(17,4)=2380 quadruples instead of constructing h+triple.
        columns = tuple(q for q in combinations(range(17), 4)
                        if len(set(q) & HIGH) == 1 and pair_set(q) <= row_set)
        require(len(rows) == 96, "direct residual row count")
        cases.append({'index': len(cases), 'tail01': root[0], 'tail23': root[1],
                      'zero_quads': root[2], 'fixed_quads': prefix,
                      'orbit_size': len(orbit), 'stabilizer_order': len(stabilizer),
                      'rows': rows, 'columns': columns,
                      'input_sha256': sha256(encoded([prefix, rows, columns])).hexdigest()})
    require(len(cases) == 7 and sum(c['orbit_size'] for c in cases) == len(raw),
            "direct incomplete carrier")
    frame_counts = Counter(sum(e in LEAVE for e in combinations(sorted(a+b), 2))
                           for a, b, _ in raw)
    tail_counts = Counter(sum(e in LEAVE for e in combinations(sorted(a+b), 2))
                          for a, b in {(a, b) for a, b, _ in raw})
    summary = {'group_order': len(group), 'raw_frames': len(raw),
               'group_sha256': sha256(encoded(group)).hexdigest(),
               'raw_frames_sha256': sha256(encoded(sorted(raw))).hexdigest(),
               'tail_counts': dict(sorted(tail_counts.items())),
               'frame_counts': dict(sorted(frame_counts.items()))}
    return cases, summary, group, raw


def replay_tree(tree, rows, columns):
    edges = tuple(pair_set(q) for q in columns)
    nodes = 0

    def walk(node, left):
        nonlocal nodes
        nodes += 1
        require(bool(left), "rejection tree reached a positive cover")
        require(type(node) is list and len(node) == 2, "malformed node")
        pivot, children = node
        require(type(pivot) is int and 0 <= pivot < len(rows) and rows[pivot] in left,
                "pivot is not an uncovered pair")
        require(type(children) is list, "malformed children")
        available = [j for j, e in enumerate(edges) if rows[pivot] in e and e <= left]
        require(all(type(c) is list and len(c) == 2 and type(c[0]) is int for c in children),
                "malformed branch")
        require([c[0] for c in children] == available, "not every compatible column has a branch")
        for j, child in children:
            walk(child, left - edges[j])

    walk(tree, frozenset(rows))
    return nodes


def verify_certificate(certificate, cases, summary):
    require(certificate.get('schema') == 'all-unit-eight-core-v1', "wrong schema")
    require(encoded(certificate.get('carrier_summary')) == encoded(summary), "carrier summary mismatch")
    records = certificate.get('cases')
    require(type(records) is list and len(records) == len(cases), "missing or extra case")
    counts = []
    for record, case in zip(records, cases):
        for key in ('index', 'tail01', 'tail23', 'zero_quads', 'fixed_quads',
                    'orbit_size', 'stabilizer_order', 'input_sha256'):
            require(encoded(record.get(key)) == encoded(case[key]), "case mismatch: " + key)
        counts.append(replay_tree(record['tree'], case['rows'], case['columns']))
    return counts


def positive_control():
    # Twenty lines in the known order-four affine plane. Four vertical
    # lines are fixed; the remaining sixteen provide a positive residual.
    def times(a, b):
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
    witness = [tuple(sorted(4*x + (times(slope, x) ^ b) for x in range(4)))
               for slope in range(4) for b in range(4)]
    all_edges = Counter(e for q in fixed+witness for e in pair_set(q))
    require(len(all_edges) == 120 and set(all_edges.values()) == {1}, "affine positive fixture")
    rows = tuple(sorted(set(all_edges) - {e for q in fixed for e in pair_set(q)}))
    covered = Counter(e for q in witness for e in pair_set(q))
    require(len(rows) == 96 and set(covered) == set(rows) and set(covered.values()) == {1},
            "positive residual cover rejected")
    # A fake rejection proof for a one-block positive instance must fail
    # both at a missing branch and when the successful branch reaches zero.
    one = (0, 1, 2, 3)
    one_rows = tuple(sorted(pair_set(one)))
    rejected = 0
    for bad in ([0, []], [0, [[0, [0, []]]]]):
        try:
            replay_tree(bad, one_rows, (one,))
        except ValueError:
            rejected += 1
        else:
            raise ValueError("fake no-cover certificate for a positive input accepted")
    return rows, tuple(witness), {'fixture': 'affine_four_vertical_lines_fixed',
                                'residual_quads': len(witness), 'residual_pairs': len(rows),
                                'positive_cover_accepted': True,
                                'false_rejection_proofs_rejected': rejected}


def invalid_controls(certificate, cases, summary):
    mutations = []
    bad = deepcopy(certificate)
    bad['cases'][0]['tree'][1].pop()
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['cases'][0]['tree'][0] = 96
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['cases'][0]['tree'][1][0][0] = 10000
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['cases'][0]['input_sha256'] = '0'*64
    mutations.append(bad)
    bad = deepcopy(certificate)
    bad['cases'].pop()
    mutations.append(bad)
    for bad in mutations:
        try:
            verify_certificate(bad, cases, summary)
        except ValueError:
            continue
        raise ValueError("invalid certificate control accepted")
    return len(mutations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-primary', action='store_true')
    args = parser.parse_args()
    cases, summary, group, raw = rebuild()
    data = (HERE / 'unit_eight_certificate.json').read_bytes()
    expected = json.loads((HERE / 'unit_eight_expected.json').read_text())
    require(sha256(data).hexdigest() == expected['certificate_sha256'], "certificate byte hash mismatch")
    certificate = json.loads(data)
    counts = verify_certificate(certificate, cases, summary)
    require(counts == expected['nodes_per_case'], "node counts differ")
    stream_hash = sha256(encoded([[c['fixed_quads'], c['rows'], c['columns']] for c in cases])).hexdigest()
    require(stream_hash == expected['input_stream_sha256'], "input stream hash mismatch")
    require([len(c['columns']) for c in cases] == expected['columns_per_case'], "column counts differ")
    invalid = invalid_controls(certificate, cases, summary)
    positive_rows, positive_columns, positive = positive_control()
    if args.compare_primary:
        import check_unit_eight as primary
        other, other_summary = primary.generate()
        require(encoded(other) == encoded(cases) and encoded(other_summary) == encoded(summary),
                "primary case stream differs entry by entry")
        require(tuple(sorted(primary.leave_group())) == group, "actual group maps differ entry by entry")
        require(primary.generate_frames()[0] == raw, "raw frames differ entry by entry")
        try:
            primary.rejection_tree(positive_rows, positive_columns)
        except primary.CoverFound:
            pass
        else:
            raise ValueError("primary did not find positive control")
        try:
            primary.rejection_tree(cases[0]['rows'], cases[0]['columns'], node_limit=0)
        except primary.Incomplete:
            pass
        else:
            raise ValueError("zero node limit returned a mathematical verdict")
    report = {'agent': 'six-code-1', 'role': 'researcher',
              'status': 'COMPLETE_LITERAL_REPLAY', 'frames': len(cases),
              'raw_frames': len(raw), 'leave_group_order': len(group), 'nodes': sum(counts),
              'nodes_per_case': counts, 'maximum_nodes_per_case': max(counts),
              'input_stream_sha256': stream_hash, 'certificate_sha256': sha256(data).hexdigest(),
              'invalid_certificate_controls_rejected': invalid, 'positive_control': positive,
              'global_72_word_exclusion': False, 'independent_peer_review': False,
              'ordinary_bridges_formalized': False}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
