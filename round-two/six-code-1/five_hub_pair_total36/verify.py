"""Reconstruct all physical inputs/count vectors; check every P35 obstruction.

Actual author six-code-1, researcher. Python standard library only. All
ordinary hypotheses/completeness bridges and imported statements: PROOF.md.
Same-author distinct engines are validation, not external independent review.
"""
from collections import Counter
import argparse
import copy
import hashlib
import itertools as it
import json
from pathlib import Path

import oracle
import producer

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def baseline(raw):
    words = raw.decode('ascii').splitlines()
    need(len(words) == len(set(words)) == 69 and all(len(w) == 18 and
         set(w) <= {'0', '1'} and w.count('1') == 5 for w in words), 'Primary69 literal domain')
    sets = [{i for i, b in enumerate(w) if b == '1'} for w in words]
    distances = Counter()
    for a, b in it.combinations(sets, 2):
        need(len(a & b) <= 2, 'Primary69 intersections')
        distances[len(a ^ b)] += 1
    triples = [t for w in sets for t in it.combinations(sorted(w), 3)]
    need(len(triples) == len(set(triples)) == 690, 'Primary69 distinct triple ownership')
    return dict(words=69, pair_checks=2346, owned_triples=690,
                distances={str(k): distances[k] for k in sorted(distances)},
                sha256=hashlib.sha256(raw).hexdigest(), status='KNOWN_BASELINE_REPRODUCTION_ONLY')


def positive_colored_path(heavy):
    """Literal U--C--B graph, retaining its actual colors and radius."""
    edges = {(0, 1): 1, (1, 2): 2 if heavy else 1}
    U, A, C, B = {0}, {0}, {1}, {2}
    adjacency = [{1}, {0, 2}, {1}]
    endpoints = lambda side, color: sum((a in side) + (b in side)
        for (a, b), c in edges.items() if c == color)
    D = sum(len(adjacency[p]) for p in U)
    I = sum(min(len(adjacency[p]), len(A) - 1) for p in A)
    C1, C2, B2 = endpoints(C, 1), endpoints(C, 2), endpoints(B, 2)
    roots = {p for p in range(3) if len({p} | adjacency[p] |
             set().union(*(adjacency[q] for q in adjacency[p]))) == 3}
    R = len(U & roots)
    need(D <= I + C1 and C1 + C2 >= R + len(B), 'Positive path obeys capacity cuts')
    need(not (D == I + C1 and (C2 == 0 or B2 == 0)), 'Positive path is not closed')
    return dict(edges=[list(e) + [c] for e, c in sorted(edges.items())],
                D=D, I=I, C1=C1, C2=C2, B2=B2, R=R, nB=len(B),
                literal_C_B_edges=1, radius_two_roots=sorted(roots))


def graph_calibration():
    """All3-point two-color graphs/roles audit the general ordinary cut scope."""
    pair_positions = [(0, 1), (0, 2), (1, 2)]
    tested = admissible = radius_tests = equality_tests = 0
    for colors in it.product(range(3), repeat=3):
        edges = {p: c for p, c in zip(pair_positions, colors) if c}
        adjacent = [set() for _ in range(3)]
        for a, b in edges:
            adjacent[a].add(b)
            adjacent[b].add(a)
        for roles in it.product(range(4), repeat=3):
            #0 unit/ineligible,1 unit/eligible,2 nonunit/ineligible,3 nonunit/eligible.
            tested += 1
            U = {p for p in range(3) if roles[p] < 2}
            A = {p for p in U if roles[p] == 0}
            C = {p for p in range(3) if roles[p] == 2}
            B = {p for p in range(3) if roles[p] == 3}
            eligible = {p for p in range(3) if roles[p] in (1, 3)}
            if any((color != 1 and (a in U or b in U)) or
                   (a in U and b in eligible) or (b in U and a in eligible)
                   for (a, b), color in edges.items()):
                continue
            admissible += 1
            D = sum(len(adjacent[p]) for p in U)
            I = sum(min(len(adjacent[p]), len(A) - 1) for p in A)
            endpoint = lambda side, color: sum(
                ((a in side) + (b in side)) for (a, b), c in edges.items() if c == color)
            C1, C2, B2 = endpoint(C, 1), endpoint(C, 2), endpoint(B, 2)
            UC = [(a, b) for a, b in edges if (a in U and b in C) or (b in U and a in C)]
            CB = [(a, b) for a, b in edges if (a in C and b in B) or (b in C and a in B)]
            roots = {p for p in range(3) if len({p} | adjacent[p] |
                     set().union(*(adjacent[q] for q in adjacent[p]))) == 3}
            R = len(U & roots)
            need(D <= I + C1, 'General unit-capacity lemma on literal positive graph')
            if R and B:
                radius_tests += 1
                need(len(UC) >= R and len(CB) >= len(B) and not set(UC) & set(CB),
                     'Distinct literal crossings, not reuse of a weighted endpoint')
                need(C1 + C2 >= R + len(B), 'General two-radius crossing lemma')
            if D == I + C1 and B and (C2 == 0 or B2 == 0):
                equality_tests += 1
                need(not CB and not ((U | C) & roots), 'Literal closed partition root obstruction')
    return dict(all_three_point_colored_graph_role_pairs=tested,
                admissible=admissible, radius_crossing_tests=radius_tests,
                closed_partition_tests=equality_tests,
                positive_controls=dict(heavy_crossing=positive_colored_path(True),
                                       unit_color_with_slack=positive_colored_path(False)),
                scope='Abstract general-cut calibration; none is an eighteen-point packing.')


def controls(data, rows, selected, types, branches, raw69):
    labels = []

    def rejects(label, call):
        try:
            call()
        except (ValueError, KeyError, TypeError, UnicodeError):
            labels.append(label)
            return
        raise ValueError('Damaged object accepted: ' + label)

    for label, edit in (
        ('missing_star', lambda x: x['stars'].pop()),
        ('missing_block', lambda x: x['stars'][0].pop()),
        ('repeated_block', lambda x: x['stars'][0].__setitem__(1, x['stars'][0][0])),
        ('repeated_point', lambda x: x['stars'][0][0].__setitem__(1, x['stars'][0][0][0])),
        ('point_outside17', lambda x: x['stars'][0][0].__setitem__(0, 17)),
        ('boolean_point', lambda x: x['stars'][0][0].__setitem__(0, True)),
    ):
        bad = copy.deepcopy(data)
        edit(bad)
        rejects('literal_' + label, lambda: producer.rows_and_physical_bridge(bad))
        rejects('physical_bit_' + label, lambda: oracle.physical_rows(bad))

    def compare_bank(candidate):
        need(candidate == types, 'Entire actual conservative carrier differs')

    exceptional = [t for t in types if t[9]]
    need(len(exceptional) == 2 and sum(r['coordinates'][9] for r in rows) == 8 and
         sum(r['coordinates'][9] for r in selected) == 8, 'All eight physical exceptions retained')
    rejects('omit_all_five_hub_exceptions', lambda: compare_bank([t for t in types if not t[9]]))
    heavy_zero = (2, 0, 0, False, 3, 1, -1, 5, 2, 0, 0)
    need(heavy_zero in types, 'Actual heavy zero-charge carrier remains')
    rejects('omit_heavy_zero_charge_type', lambda: compare_bank([t for t in types if t != heavy_zero]))
    other = copy.deepcopy(types)
    changed = list(other[0]); changed[7] += 1; other[0] = tuple(changed)
    rejects('change_corrected_indicator_margin', lambda: compare_bank(other))
    need(any(5 - sum(a in b for b in data['stars'][0]) == 5 for a in range(17)),
         'Unused physical point retained in raw domain')
    rejects('drop_unused_point_deficit5_rows', lambda: need(
        [r for r in rows if r['fixture'] != 0] == rows, 'Missing-point carrier differs'))

    #Complete canonical lists, not merely counts, are the comparison interface.
    first = next(b for b in branches if b['patterns'])
    full = first['patterns']
    rejects('delete_one_necessary_vector', lambda: need(full[:-1] == full, 'Missing complete vector'))
    rejects('repeat_one_necessary_vector', lambda: need(full + full[:1] == full, 'Duplicate complete vector'))
    rejects('drop_N5_one_branch', lambda: need(len([b for b in branches if not b['N5']]) == 27,
                                            'Genuine exceptional branches omitted'))
    local = Counter(tuple(r['coordinates']) for r in selected)
    repeated = [(i, c, local[t]) for b in branches for v in b['patterns']
                for i, (t, c) in enumerate(zip(types, v)) if c > local[t]]
    need(repeated, 'Positive real carrier witnesses unbounded global repetition')
    rejects('use_local_population_as_global_cap', lambda: need(not repeated,
                                                            'Local orbit counts cannot cap global rows'))
    unit_failure = next(c for b in branches for c in b['certificates']
                        if c['reason'] == 'UNIT_NEIGHBOR_CAPACITY')
    crossing = next(c for b in branches for c in b['certificates']
                    if c['reason'] == 'DISTINCT_RADIUS_TWO_CROSSINGS')
    need(unit_failure['D'] > unit_failure['I'] + unit_failure['C1'], 'Actual unit certificate')
    need(crossing['C1'] + crossing['C2'] < crossing['unit_roots_k0'] +
         crossing['eligible_nonunit_rows'], 'Actual distinct-crossing certificate')
    witness = next((v, c) for b in branches for v, c in zip(b['patterns'], b['certificates'])
                   if c['ineligible_unit_rows'] < c['unit_rows'])
    wrong = dict(witness[1])
    wrong['I'] = sum(count * min(t[4] - t[1], wrong['unit_rows'] - 1)
                     for t, count in zip(types, witness[0]) if t[0] == 0)
    rejects('cap_unit_internal_edges_by_all_units', lambda: need(
        wrong == oracle.direct_capacity(types, witness[0]), 'Eligible units cannot supply unit neighbors'))
    positive = positive_colored_path(True)
    rejects('discard_heavy_crossing_positive_control', lambda: need(
        positive['C1'] >= positive['R'] + positive['nB'], 'False omission of actual color2'))
    rejects('close_without_color2_guard', lambda: need(
        not (positive['D'] == positive['I'] + positive['C1'] and positive['literal_C_B_edges']),
        'Equality alone leaves an actual heavy crossing'))
    rejects('damaged_known69', lambda: baseline(raw69.replace(b'1', b'0', 1)))

    transports = 0
    filtered_transports = 0
    for permutation in ([16 - p for p in range(17)], [(3 * p + 2) % 17 for p in range(17)],
                        [p ^ 1 if p < 16 else 16 for p in range(17)]):
        need(sorted(permutation) == list(range(17)), 'Actual point bijection')
        inverse = {b: a for a, b in enumerate(permutation)}
        changed = copy.deepcopy(data)
        changed['stars'] = [[[permutation[p] for p in b] for b in star] for star in data['stars']]
        rr, _ = producer.rows_and_physical_bridge(changed)
        rs = producer.conservative_rows(changed, rr)
        oo, os = oracle.physical_rows(changed)
        need(rr == oo and rs == os, 'Full transported physical engines')
        for collection, reference in [(rr, rows), (rs, selected)]:
            normalized = [dict(r, hub_high=sorted(inverse[p] for p in r['hub_high'])) for r in collection]
            normalized.sort(key=lambda r: (r['fixture'], r['hub_high']))
            need(normalized == reference, 'Every physical point-role transport')
        transports += len(rr)
        filtered_transports += len(rs)
    return dict(rejected=labels, rejected_count=len(labels), actual_point_transports=transports,
                conservative_point_transports=filtered_transports,
                repeated_type_witness=list(repeated[0]))


def run():
    fixture = (ROOT / 'fixtures.json').read_bytes()
    need(hashlib.sha256(fixture).hexdigest() ==
         'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7', 'Credited literal fixture bytes')
    raw69 = (ROOT / 'BASELINE69.txt').read_bytes()
    need(hashlib.sha256(raw69).hexdigest() ==
         'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d', 'Known69 source bytes')
    data = json.loads(fixture)
    rows, _ = producer.rows_and_physical_bridge(data)
    selected = producer.conservative_rows(data, rows)
    other_rows, other_selected = oracle.physical_rows(data)
    need(rows == other_rows and selected == other_selected, 'All literal/physical rows match')
    types = sorted({tuple(r['coordinates']) for r in selected})
    need(len(rows) == 426 and len(selected) == 410 and len(types) == 51, 'Complete conservative carrier')
    need(all(t[5] + t[8] == t[4] - t[1] for t in types), 'Every retained saturated support color')
    cases = producer.arithmetic()
    need(cases == oracle.all_cases(), 'Entire rectangular/inequality scalar domain')
    branches = []
    for case in cases:
        vectors, nodes = producer.produce(types, case)
        second, states = oracle.coefficient_vectors(types, case)
        need(vectors == second, 'Every full specialized/coefficient vector')
        certs = [producer.certificate(types, v) for v in vectors]
        need(certs == [oracle.direct_capacity(types, v) for v in second], 'Every colored-endpoint certificate')
        need(all(c['reason'] != 'OPEN' for c in certs), 'A physical candidate remains; no exclusion')
        branches.append(dict(**case, patterns=[list(v) for v in vectors], certificates=certs,
                             producer_nodes=nodes, coefficient_states=states))
    scope_controls = controls(data, rows, selected, types, branches, raw69)
    return dict(actual_agent='six-code-1', role='researcher',
                status='EXACT_CONDITIONAL_P35_EXCLUSION_ALL27_BRANCHES',
                fields=list(producer.FIELDS), full_row_sha256=digest(rows),
                conservative_row_sha256=digest(selected), types=[list(t) for t in types],
                branches=branches, controls=scope_controls,
                graph_calibration=graph_calibration(), baseline=baseline(raw69),
                scope='Necessary local carrier and full row vectors, not constructed codes. Ordinary point/selector/radius/capacity/coverage bridges in PROOF.md remain unformalized; external review pending.')


def summary(record):
    reasons = Counter(c['reason'] for b in record['branches'] for c in b['certificates'])
    return dict(actual_agent='six-code-1', role='researcher', status=record['status'],
                whole_record_sha256=digest(record), actual_marks=426, conservative_marks=410,
                actual_I5_marks=8, types=len(record['types']), scalar_cases=len(record['branches']),
                necessary_vectors=sum(len(b['patterns']) for b in record['branches']),
                N5_one_vectors=sum(len(b['patterns']) for b in record['branches'] if b['N5']),
                rejection_counts=dict(sorted(reasons.items())),
                rejected_damages=record['controls']['rejected_count'],
                physical_point_transports=record['controls']['actual_point_transports'],
                max_producer_nodes=max(b['producer_nodes'] for b in record['branches']),
                max_coefficient_states=max(b['coefficient_states'] for b in record['branches']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--no-expected', action='store_true', help='Compute the first record before sealing EXPECTED.json')
    args = parser.parse_args()
    record = run()
    compact = summary(record)
    if not args.no_expected:
        need(compact == json.loads((ROOT / 'EXPECTED.json').read_text()), 'Sealed complete mathematical record differs')
    if args.output:
        args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
