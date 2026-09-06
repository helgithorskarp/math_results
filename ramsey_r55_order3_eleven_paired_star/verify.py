#!/usr/bin/env python3
"""Independent clique decomposition, followed by exhaustive Gray-code checks.

No producer, subset transform, SAT or previous optimizer is imported.
"""
from array import array
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
INPUT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    lines = Path(path).read_text().splitlines()
    need(lines and lines[0] == '43', 'order header')
    pairs = [tuple(map(int, s.split())) for s in lines[1:]]
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < 43 for e in pairs), 'physical pairs')
    need(pairs == sorted(set(pairs)), 'unique sorted pairs')
    return set(pairs)


def rows(n, red, color):
    result = [0]*n
    for a, b in combinations(range(n), 2):
        if int((a, b) in red) == color:
            result[a] |= 1 << b
            result[b] |= 1 << a
    return result


def cliques(adjacency, size, candidates):
    found = []
    def visit(prefix, available):
        if len(prefix) == size:
            found.append(tuple(prefix))
            return
        if available.bit_count() < size-len(prefix):
            return
        while available:
            bit = available & -available
            available ^= bit
            v = bit.bit_length()-1
            visit(prefix+[v], available & adjacency[v])
    visit([], candidates)
    return found


def reconstruct(n, red, roots, contact_bits):
    """Partition a K5 by its subset of roots; enumerate a K5, K4, or K3.

    contact_bits maps root -> {other endpoint: Boolean index}.
    The mutual root edge is fixed and is checked before accepting a K3.
    """
    available = ((1 << n)-1) ^ sum(1 << f for f in roots)
    result = [Counter(), Counter()]
    strata = [[0, 0, 0], [0, 0, 0]]
    for color in (0, 1):
        adjacency = rows(n, red, color)
        for count in range(3):
            for chosen in combinations(roots, count):
                if any(not adjacency[a] & (1 << b) for a, b in combinations(chosen, 2)):
                    continue
                for q in cliques(adjacency, 5-count, available):
                    support = 0
                    compatible = True
                    for f in chosen:
                        for v in q:
                            if v in contact_bits[f]:
                                support |= 1 << contact_bits[f][v]
                            elif not adjacency[f] & (1 << v):
                                compatible = False
                    if compatible:
                        result[color][support] += 1
                        strata[color][count] += 1
    return result, strata


def direct(coeff, a):
    return [sum(m for s, m in coeff[0].items() if (s & a) == 0),
            sum(m for s, m in coeff[1].items() if (s & a) == s)]


def gray_check(coeff, k, tables, limit=None):
    """Only terms touching the flipped bit can change; compare every visited row.

    No clause state or transform is reused. Each affected monomial is evaluated
    directly at both adjacent masks. Gray(k) = k xor floor(k/2) is a bijection.
    """
    count = (1 << k) if limit is None else limit
    need(1 <= count <= (1 << k), 'prefix range')
    incidence = [[[], []] for _ in range(k)]
    for color, terms in enumerate(coeff):
        for support, weight in terms.items():
            for bit in range(k):
                if support & (1 << bit):
                    incidence[bit][color].append((support, weight))
    # Keep the Gray order conventional; no heuristic reordering of variable bits.
    current = direct(coeff, 0)
    need(current == [tables[0][0], tables[1][0]], 'Gray base counts')
    old = 0
    for index in range(1, count):
        a = index ^ (index >> 1)
        bit = (index & -index).bit_length()-1
        need((a ^ old) == (1 << bit), 'Gray transition')
        delta = 0
        for s, w in incidence[bit][0]:
            delta += w * (((s & a) == 0) - ((s & old) == 0))
        current[0] += delta
        delta = 0
        for s, w in incidence[bit][1]:
            delta += w * (((s & a) == s) - ((s & old) == s))
        current[1] += delta
        need(current[0] == tables[0][a] and current[1] == tables[1][a], 'Gray assignment count')
        if index % 262144 == 0:
            need(current == direct(coeff, a), 'direct Gray checkpoint')
            print('Checked Gray assignments', index+1, flush=True)
        old = a
    need(current == direct(coeff, old), 'direct final Gray counts')
    return {'checked_assignments': count, 'complete': count == (1 << k),
            'incidence_lengths_blue_red': [list(map(len, x)) for x in incidence]}


def literal(n, red):
    result = [[], []]
    for q in combinations(range(n), 5):
        color = int((q[0], q[1]) in red)
        if all(int(e in red) == color for e in combinations(q, 2)):
            result[color].append(q)
    return result


def action_audit(red):
    action = [v+1 if v < 33 and v % 3 < 2 else v-2 if v < 33 else v for v in range(43)]
    for a, b in combinations(range(43), 2):
        need(((a, b) in red) == (tuple(sorted((action[a], action[b]))) in red), 'C3 action')
    for t in range(11):
        for e in combinations(range(3*t, 3*t+3), 2):
            need((e in red) == (t < 4), 'internal color')
    word = ''.join(str(int((3*i, 3*j+d) in red)) for i, j in combinations(range(4), 2) for d in range(3))
    need(word == '100110110011011101', 'core word')


def read_table(path):
    need(path.stat().st_size == (1 << 22)*4, 'table length')
    data = array('I')
    need(data.itemsize == 4, '32-bit array requirement')
    with path.open('rb') as f:
        data.fromfile(f, 1 << 22)
    if sys.byteorder != 'little':
        data.byteswap()
    return data


def audit(work, limit):
    need(hashlib.sha256((HERE/'input.edges').read_bytes()).hexdigest() == INPUT_SHA, 'input identity')
    red = read(HERE/'input.edges')
    action_audit(red)
    roots = (33, 35)
    contacts = {33: {v: v//3 for v in range(33)}, 35: {v: 11+v//3 for v in range(33)}}
    coeff, strata = reconstruct(43, red, roots, contacts)
    raw_coeff = json.loads((work/'coefficients.json').read_text())
    expected_coeff = [[[s, m] for s, m in sorted(c.items())] for c in coeff]
    need(raw_coeff == expected_coeff, 'independent K5/K4/K3 coefficients')
    result = json.loads((work/'result.json').read_text())
    for key, value in [('vertices', 43), ('roots', [33, 35]), ('bits', 22),
                       ('assignments', 1 << 22), ('input_sha256', INPUT_SHA)]:
        need(result[key] == value, key)
    need(result['coefficients_sha256'] == hashlib.sha256((work/'coefficients.json').read_bytes()).hexdigest(), 'coefficient identity')
    tables = []
    for name in ('blue.bin', 'red.bin'):
        p = work/name
        need(result['tables'][name] == {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}, 'table identity')
        tables.append(read_table(p))
    gray = gray_check(coeff, 22, tables, limit)
    report = {'gray': gray, 'coefficient_records': sum(map(len, coeff)), 'physical_coefficient_weights_by_root_count_blue_red': strata}
    if not gray['complete']:
        report['status'] = 'INCOMPLETE_PREFIX_ONLY'
        return report
    # Separate full scan of the now-checked physical-count tables.
    base = sum(1 << i for f in roots for v, i in contacts[f].items() if v % 3 == 0 and (v, f) in red)
    histogram = Counter(map(sum, zip(*tables)))
    baseline = sum(t[base] for t in tables)
    minimum = min(histogram)
    argmins = [a for a in range(1 << 22) if tables[0][a]+tables[1][a] == minimum]
    changed_min = min(tables[0][a]+tables[1][a] for a in range(1 << 22) if a != base)
    both_indices = (a for a in range(1 << 22) if a % 2048 != base % 2048 and a//2048 != base//2048)
    both_min = 10**9
    both_argmins = []
    for a in both_indices:
        total = tables[0][a]+tables[1][a]
        if total < both_min:
            both_min, both_argmins = total, []
        if total == both_min:
            both_argmins.append(a)
    summary = {'base_mask': base, 'base_counts_blue_red': [t[base] for t in tables],
               'minimum': minimum, 'argmin_masks': argmins, 'minimum_changed': changed_min,
               'minimum_both_changed': both_min, 'both_changed_argmin_masks': both_argmins,
               'improving_assignments': sum(c for s, c in histogram.items() if s < baseline),
               'neutral_changed_assignments': histogram[baseline]-1,
               'histogram': [[s, c] for s, c in sorted(histogram.items())]}
    need(result['summary'] == summary, 'complete summary')
    best = argmins[0]
    need(result['winner_mask'] == best, 'winner mask')
    winner = read(work/'winner.edges')
    need(result['winner_sha256'] == hashlib.sha256((work/'winner.edges').read_bytes()).hexdigest(), 'winner identity')
    for a, b in combinations(range(43), 2):
        if b in contacts and a in contacts[b]:
            expected = bool(best & (1 << contacts[b][a]))
        else:
            expected = (a, b) in red
        need(((a, b) in winner) == expected, 'winner physical decoding')
    action_audit(winner)
    graphs = []
    for graph in (red, winner):
        bad = literal(43, graph)
        need(bad == [cliques(rows(43, graph, c), 5, (1 << 43)-1) for c in (0, 1)], 'literal/recursive graph agreement')
        degrees = [sum(tuple(sorted((a, b))) in graph for b in range(43) if b != a) for a in range(43)]
        graphs.append({'red_edges': len(graph), 'counts_blue_red': list(map(len, bad)),
                       'degrees': degrees, 'degree_histogram': [[d, m] for d, m in sorted(Counter(degrees).items())],
                       'bad_sets_blue_red': bad})
    need(graphs[0]['counts_blue_red'] == summary['base_counts_blue_red'], 'physical base score')
    need(sum(graphs[1]['counts_blue_red']) == minimum, 'physical winner score')
    report.update({'status': 'COMPLETE', 'summary': summary, 'graphs': graphs,
                   'changed_physical_pairs': sorted(red ^ winner), 'target_graph': minimum == 0})
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--prefix', type=int)
    a = p.parse_args()
    result = audit(a.work, a.prefix)
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(result['status'], 'assignments checked', result['gray']['checked_assignments'], flush=True)
