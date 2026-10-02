"""Exact corrected twenty-star rows and five-hub boundary verification.

Actual author six-code-1, researcher. Standard library; no peer executable.
Ordinary classification/incidence/extension/girth bridges are in PROOF.md.
"""
from collections import Counter
import argparse
import copy
import hashlib
import itertools as it
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
FIELDS = ('e', 'k', 'q', 'eligible', 'h', 'g1_S', 'psi', 'corrected_margin', 'ss_excess')


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def literal_rows(data):
    """Pair ownership from intersections of block-index incidence columns."""
    need(isinstance(data, dict) and len(data['stars']) == 23, 'complete23-star input')
    rows = []
    for fi, blocks in enumerate(data['stars']):
        need(len(blocks) == 20, 'twenty blocks')
        need(all(len(b) == 4 and len(set(b)) == 4 and
                 all(type(p) is int and 0 <= p < 17 for p in b) for b in blocks), 'literal four-set')
        need(len({tuple(sorted(b)) for b in blocks}) == 20, 'distinct blocks')
        incident = [{j for j, b in enumerate(blocks) if p in b} for p in range(17)]
        delta = [5 - len(c) for c in incident]
        need(min(delta) >= 0 and sum(delta) == 5, 'deficit domain')
        leave = []
        for a, b in it.combinations(range(17), 2):
            owners = incident[a] & incident[b]
            need(len(owners) <= 1, 'pair repeated')
            if not owners:
                leave.append((a, b))
        high = tuple(p for p, d in enumerate(delta) if d)
        HH = [edge for edge in leave if all(delta[p] > 0 for p in edge)]
        need(len(leave) == 16 and len(HH) == len(high) - 1, 'leave counts')
        for p in range(17):
            need(sum(p in edge for edge in leave) == 1 + 3 * delta[p], 'exact leave degree')
        need(all(any(delta[p] for p in edge) for edge in leave), 'low-low leave')
        isolated = {p for p in high if not any(p in edge for edge in HH)}
        for k in range(len(high) + 1):
            for marks in it.combinations(high, k):
                e = 5 - len(high)
                eligible = bool(isolated.intersection(marks))
                g1 = sum(delta[p] == 1 for p in high if p not in marks)
                sigma = sum(delta[p] - 1 for p in high if p not in marks)
                w = sum(delta[p] for p in marks)
                q = sum(any(p in marks for p in edge) for edge in HH)
                psi = g1 if e == 0 and eligible else -g1 if e and not eligible else 0
                indicator = int(e == 0 and k == 5)
                margin = psi - 3 * (k - e - q)
                need(e == w - k + sigma, 'weighted-support row identity')
                rows.append(dict(fixture=fi, hub_high=list(marks), h=len(high), e=e,
                                 k=k, q=q, eligible=eligible, g1_S=g1, ss_excess=sigma,
                                 hub_weight=w, psi=psi, margin=margin, I5=indicator,
                                 corrected_margin=margin + 3 * indicator))
    return sorted(rows, key=lambda r: (r['fixture'], r['hub_high']))


def boundary(rows):
    branches = []
    slack = 4 * 34 - 133
    for N5 in range(slack // 3 + 1):
        for T, X, tau in it.product(range(1, slack // 2 + 1), range(slack // 2 + 1), range(slack // 4 + 1)):
            for Q in range(4 * N5, slack + N5 + 1):
                if 2 * T + 2 * X + 4 * tau + Q - N5 > slack:
                    continue
                E = -94 + 3 * 34 - T - 2 * tau - Q
                W = -55 + 2 * 34
                K = W - E + 2 * X
                budget = 3 * (E + Q + N5 - K)
                need(N5 == X == tau == 0 and T == 1 and Q in (0, 1), 'boundary arithmetic')
                need(budget >= 0, 'nonnegative margin budget')
                categories = sorted({tuple(r[f] for f in FIELDS) for r in rows
                                     if r['q'] <= Q and r['ss_excess'] == 0 and
                                     r['I5'] == 0 and r['corrected_margin'] <= budget})
                patterns = []
                nodes = 0
                started = time.monotonic()

                def visit(j, counts, totals):
                    nonlocal nodes
                    nodes += 1
                    need(nodes <= 100000 and time.monotonic() - started <= 10,
                         'INCOMPLETE category guard')
                    used, se, sk, sq, sm = totals
                    if any(a > b for a, b in zip(totals, (13, E, K, Q, budget))):
                        return
                    if j == len(categories):
                        if (used, se, sk, sq) == (13, E, K, Q):
                            patterns.append(counts)
                        return
                    r = dict(zip(FIELDS, categories[j]))
                    for c in range(14 - used):
                        visit(j + 1, counts + [c],
                              (used + c, se + c * r['e'], sk + c * r['k'],
                               sq + c * r['q'], sm + c * r['corrected_margin']))

                visit(0, [], (0, 0, 0, 0, 0))
                # Separate sparse generating-function coefficient calculation.
                coefficients = {(0, 0, 0, 0, 0): [()]}
                for category in categories:
                    r = dict(zip(FIELDS, category))
                    updated = {}
                    for totals, vectors in coefficients.items():
                        for c in range(14 - totals[0]):
                            t = (totals[0] + c, totals[1] + c * r['e'],
                                 totals[2] + c * r['k'], totals[3] + c * r['q'],
                                 totals[4] + c * r['corrected_margin'])
                            if any(a > b for a, b in zip(t, (13, E, K, Q, budget))):
                                continue
                            updated.setdefault(t, []).extend(v + (c,) for v in vectors)
                    need(len(updated) <= 100000 and time.monotonic() - started <= 10,
                         'INCOMPLETE coefficient guard')
                    coefficients = updated
                second = sorted(list(v) for t, vs in coefficients.items()
                                if t[:4] == (13, E, K, Q) for v in vs)
                need(sorted(patterns) == second, 'whole category coefficient patterns differ')
                branches.append(dict(T=T, X=X, tau=tau, N5=N5, Q=Q, E=E, W=W, K=K,
                                     margin_budget=budget, fields=list(FIELDS),
                                     categories=[list(c) for c in categories], patterns=patterns))
    need(len(branches) == 2, 'both Q boundary branches')
    return branches


def baseline(raw):
    lines = raw.decode('ascii').splitlines()
    need(len(lines) == 69 and len(set(lines)) == 69, '69 distinct primary words')
    need(all(len(w) == 18 and set(w) <= {'0', '1'} and w.count('1') == 5
             for w in lines), 'binary length18 weight5')
    words = [{p for p, bit in enumerate(w) if bit == '1'} for w in lines]
    distances = Counter()
    for a, b in it.combinations(words, 2):
        need(len(a & b) <= 2, 'primary intersection greater than two')
        distances[len(a ^ b)] += 1
    triples = [t for w in words for t in it.combinations(sorted(w), 3)]
    need(len(triples) == len(set(triples)) == 690, 'primary triple ownership')
    return dict(words=69, weight=5, length=18, pair_checks=2346,
                triple_owners=690, distance_histogram={str(k): distances[k] for k in sorted(distances)},
                sha256=hashlib.sha256(raw).hexdigest(), status='PRIOR69_REPRODUCTION_ONLY')


def graph_neighbors(n, edges):
    need(type(n) is int and n >= 0, 'graph size')
    neighbors = [set() for _ in range(n)]
    seen = set()
    for a, b in edges:
        need(type(a) is int and type(b) is int and 0 <= a < b < n, 'literal simple graph edge')
        need((a, b) not in seen, 'repeated graph edge')
        seen.add((a, b))
        neighbors[a].add(b)
        neighbors[b].add(a)
    return neighbors


def has_triangle(neighbors):
    return any(neighbors[a] & neighbors[b]
               for a in range(len(neighbors)) for b in neighbors[a] if a < b)


def has_four_cycle(neighbors):
    return any(len(neighbors[a] & neighbors[b]) >= 2
               for a, b in it.combinations(range(len(neighbors)), 2))


def moore_layers(n, edges):
    neighbors = graph_neighbors(n, edges)
    need(n > 0 and all(len(ns) == 3 for ns in neighbors), 'nonempty cubic graph')
    need(not has_triangle(neighbors) and not has_four_cycle(neighbors), 'girth at least five')
    layers = []
    for p in range(n):
        first = neighbors[p]
        children = [(q, r) for q in sorted(first) for r in sorted(neighbors[q] - {p})]
        second = [r for q, r in children]
        need(len(first) == 3 and len(second) == len(set(second)) == 6,
             'six distinct grandchildren')
        need(p not in second and not first.intersection(second), 'disjoint neighbor layers')
        need(n >= 1 + 3 + 6, 'Moore lower bound')
        layers.append(dict(root=p, first=sorted(first), second=sorted(second)))
    return layers


def small_graph_validation():
    pairs = list(it.combinations(range(6), 2))
    cubic = triangle_free = girth_five = 0
    for edges in it.combinations(pairs, 9):
        ns = graph_neighbors(6, edges)
        if not all(len(s) == 3 for s in ns):
            continue
        cubic += 1
        if not has_triangle(ns):
            triangle_free += 1
            if not has_four_cycle(ns):
                girth_five += 1
    petersen = sorted({tuple(sorted(e)) for j in range(5) for e in
                       [(j, (j + 1) % 5), (j, j + 5), (j + 5, (j + 2) % 5 + 5)]})
    layers = moore_layers(10, petersen)
    need((cubic, triangle_free, girth_five) == (70, 10, 0), 'literal six-vertex graph census')
    return dict(literal_nine_edge_sets=5005, labeled_cubic_six_graphs=cubic,
                triangle_free_cubic_six_graphs=triangle_free,
                girth_five_cubic_six_graphs=girth_five,
                petersen= dict(vertices=10, edges=[list(e) for e in petersen],
                               all_root_layers=layers, status='POSITIVE_ABSTRACT_GRAPH_ONLY'))


def algebra():
    from math import comb
    need(all(comb(5 - j, 3) == 10 - 6*j + 3*comb(j, 2) - comb(j, 3)
             for j in range(6)), 'homogeneous word polynomial')
    values = []
    for m in range(1, 6):
        n = 18 - m
        B = 4*n - comb(n, 3) - 120*m + 740
        w0 = 20 + 10*m - 5*m*m
        values.append(dict(m=m, n=n, B=B, w0=w0, C=w0 - 2*B))
    need([v['C'] for v in values] == [9, 12, 35, 76, 133], 'all corrected coefficients')
    return values


def controls(data, rows, raw69, branches):
    labels = []

    def rejects(label, call):
        try:
            call()
        except (ValueError, KeyError, TypeError, UnicodeError):
            labels.append(label)
            return
        raise ValueError('Damaged object accepted: ' + label)

    for label, edit in (
        ('missing_fixture', lambda d: d['stars'].pop()),
        ('missing_quadruple', lambda d: d['stars'][0].pop()),
        ('duplicate_quadruple', lambda d: d['stars'][0].__setitem__(1, d['stars'][0][0])),
        ('duplicate_point', lambda d: d['stars'][0][0].__setitem__(1, d['stars'][0][0][0])),
        ('out_of_range_point', lambda d: d['stars'][0][0].__setitem__(0, 17)),
        ('boolean_point', lambda d: d['stars'][0][0].__setitem__(0, True))):
        damaged = copy.deepcopy(data)
        edit(damaged)
        rejects(label, lambda: literal_rows(damaged))

    def compare_rows(candidate):
        need(candidate == rows, 'whole literal marked row universe differs')

    for label, edit in (
        ('missing_last_mark', lambda r: r.pop()),
        ('delete_all_five_hub_exceptions', lambda r: r.__setitem__(slice(None), [v for v in r if not v['I5']])),
        ('wrong_actual_hub_label', lambda r: r[0].__setitem__('hub_high', [0])),
        ('wrong_q_charge', lambda r: r[0].__setitem__('q', 1)),
        ('wrong_eligibility', lambda r: r[0].__setitem__('eligible', True)),
        ('wrong_exception_indicator', lambda r: next(v for v in r if v['I5']).__setitem__('I5', 0)),
        ('consistent_wrong_psi_and_margin', lambda r: (r[0].__setitem__('psi', 1), r[0].__setitem__('corrected_margin', r[0]['corrected_margin'] + 1)))):
        damaged = copy.deepcopy(rows)
        edit(damaged)
        rejects(label, lambda: compare_rows(damaged))
    rejects('uncorrected_five_hub_widening', lambda: need(all(r['margin'] >= 0 for r in rows), 'eight actual failures'))
    damaged = copy.deepcopy(branches)
    damaged[1]['patterns'] = []
    rejects('deleted_unique_boundary_pattern', lambda: need(damaged == branches, 'whole boundary record'))
    rejects('empty_closed_block', lambda: moore_layers(0, []))
    rejects('cubic_triangle', lambda: moore_layers(4, list(it.combinations(range(4), 2))))
    rejects('cubic_four_cycle', lambda: moore_layers(6, [(a, b) for a in range(3) for b in range(3, 6)]))
    lines = raw69.decode().splitlines()
    rejects('primary_word_deleted', lambda: baseline(('\n'.join(lines[:-1])+'\n').encode()))
    bad = list(lines); bad[1] = bad[0]
    rejects('primary_duplicate_word', lambda: baseline(('\n'.join(bad)+'\n').encode()))
    bad = list(lines); bad[0] = bad[0].replace('1', '0', 1)
    rejects('primary_wrong_weight', lambda: baseline(('\n'.join(bad)+'\n').encode()))
    bad = list(lines); bad[0] = '2' + bad[0][1:]
    rejects('primary_nonbinary', lambda: baseline(('\n'.join(bad)+'\n').encode()))
    transports = []
    for point_map in ([16 - p for p in range(17)], [(p + 1) % 17 for p in range(17)],
                      [(3*p + 2) % 17 for p in range(17)]):
        inverse = [point_map.index(p) for p in range(17)]
        transported = copy.deepcopy(data)
        transported['stars'] = [[[point_map[p] for p in b] for b in blocks]
                                for blocks in data['stars']]
        reconstructed = literal_rows(transported)
        for row in reconstructed:
            row['hub_high'] = sorted(inverse[p] for p in row['hub_high'])
        reconstructed.sort(key=lambda r: (r['fixture'], r['hub_high']))
        need(reconstructed == rows, 'whole physical transported row universe')
        need(boundary(reconstructed) == branches, 'whole transported category patterns')
        transports.append(dict(point_map=point_map, stars=23, marked_rows=426))
    return dict(rejected_count=len(labels), rejected_labels=labels,
                actual_point_transports=transports, transported_marked_rows=1278,
                status='PASS_DAMAGES_EXCEPTION_SCOPE_AND_NONEMPTY_CONTROLS')


def compute(data, raw69):
    rows = literal_rows(data)
    need(len(rows) == 426 and sum(r['I5'] for r in rows) == 8, 'complete426/eight exceptions')
    need(all(r['corrected_margin'] >= 0 for r in rows), 'corrected row inequality')
    exceptional = [r for r in rows if r['I5']]
    need(all((r['e'], r['k'], r['q'], r['g1_S'], r['psi'], r['margin'], r['corrected_margin'])
             == (0, 5, 4, 0, 0, -3, 0) for r in exceptional), 'actual exception coordinates')
    original = [{k: v for k, v in r.items() if k not in ('I5', 'corrected_margin')} for r in rows]
    need(digest(original) == '19205841cee4584466bac048f114d0d5f0db096b6861e45f34c94b9180087b16',
         'full original426-row published readout')
    branches = boundary(rows)
    need(branches[0]['patterns'] == [] and branches[1]['patterns'] == [[6, 1, 6, 0]],
         'all actual necessary boundary patterns')
    return dict(status='PASS_CORRECTED426_ROWS_M5_P34_EXCLUSION_CHECKS',
                corrected_rows_sha256=digest(rows), original_rows_sha256=digest(original),
                catalog=dict(actual_rows=426, exception_rows=8, minimum_corrected_margin=0,
                             fixture_populations=[sum(r['fixture'] == fi for r in rows) for fi in range(23)],
                             all_exception_marks=[dict(fixture=r['fixture'], hub_high=r['hub_high'],
                                                      q=r['q'], original_margin=r['margin'],
                                                      corrected_margin=r['corrected_margin']) for r in exceptional]),
                coefficients=algebra(), boundary_branches=branches,
                abstract_girth_validation=small_graph_validation(),
                primary69=baseline(raw69), controls=controls(data, rows, raw69, branches))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = (ROOT / 'fixtures.json').read_bytes()
    raw69 = (ROOT / 'BASELINE69.txt').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7', 'credited fixture bytes')
    need(hashlib.sha256(raw69).hexdigest() == 'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d', 'primary69 bytes')
    expected = json.loads((ROOT / 'EXPECTED.json').read_text())
    need(expected['frozen_before_cold_replays'] is True, 'frozen expected result required')
    result = compute(json.loads(raw), raw69)
    need(result == expected['mathematical_result'], 'whole frozen mathematical result differs')
    output = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
