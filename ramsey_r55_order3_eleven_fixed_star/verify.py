#!/usr/bin/env python3
"""Independent physical K4 reconstruction and direct subset-predicate audit.

Imports no producer, previous search code, SAT encoding or zeta transform.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'
CORE_WORD = '100110110011011101'


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


def color_rows(n, red, color):
    rows = [0] * n
    for u, v in combinations(range(n), 2):
        if int((u, v) in red) == color:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def cliques(rows, size, candidates):
    found = []
    def visit(prefix, available):
        if len(prefix) == size:
            found.append(tuple(prefix))
            return
        if available.bit_count() < size - len(prefix):
            return
        while available:
            bit = available & -available
            available ^= bit
            v = bit.bit_length()-1
            visit(prefix+[v], available & rows[v])
    visit([], candidates)
    return found


def reconstruct(n, red, f, groups):
    """A K5 either avoids f or comes from a monochromatic K4 in G-f."""
    remaining = ((1 << n)-1) ^ (1 << f)
    counts = []
    for color in (0, 1):
        rows = color_rows(n, red, color)
        coeff = Counter()
        constant = len(cliques(rows, 5, remaining))
        if constant:
            coeff[0] = constant
        for q in cliques(rows, 4, remaining):
            # Every contact to a fixed vertex must already have the right color.
            if any(v not in groups and not (rows[f] & (1 << v)) for v in q):
                continue
            mask = 0
            for v in q:
                if v in groups:
                    mask |= 1 << groups[v]
            coeff[mask] += 1
        counts.append(coeff)
    return counts


def direct_scores(coeff, k):
    # Evaluate each monomial separately; no dynamic program or transform.
    return [[sum(m for s, m in coeff[0].items() if (s & a) == 0),
             sum(m for s, m in coeff[1].items() if (s & a) == s)]
            for a in range(1 << k)]


def unpack(raw, k):
    need(type(raw) is list and len(raw) == 2, 'two colors')
    out = []
    for records in raw:
        need(type(records) is list, 'coefficient list')
        for r in records:
            need(type(r) is list and len(r) == 2, 'coefficient record')
            s, m = r
            need(type(s) is int and 0 <= s < (1 << k) and s.bit_count() <= 4, 'support mask')
            need(type(m) is int and m > 0, 'positive physical weight')
        need(records == sorted(records) and len({r[0] for r in records}) == len(records), 'canonical supports')
        out.append(Counter(dict(records)))
    return out


def validate_block(block, coeff, expected_f, expected_base, expected_table):
    need(block['fixed_vertex'] == expected_f, 'fixed vertex')
    need(block['base_mask'] == expected_base, 'base mask')
    need(unpack(block['coefficients_blue_red'], 11) == coeff, 'K4 coefficient reconstruction')
    values = direct_scores(coeff, 11)
    need(values == expected_table, 'all assignment counts')
    totals = [sum(v) for v in values]
    baseline, minimum = totals[expected_base], min(totals)
    expected = {
        'base_counts_blue_red': values[expected_base], 'minimum': minimum,
        'argmin_masks': [a for a, s in enumerate(totals) if s == minimum],
        'minimum_changed': min(s for a, s in enumerate(totals) if a != expected_base),
        'improving_assignments': sum(s < baseline for s in totals),
        'neutral_changed_assignments': sum(s == baseline for a, s in enumerate(totals) if a != expected_base),
        'score_histogram': [[s, m] for s, m in sorted(Counter(totals).items())]}
    for key, value in expected.items():
        need(block[key] == value, key)
    return values


def literal(n, red):
    found = [[], []]
    for q in combinations(range(n), 5):
        color = int((q[0], q[1]) in red)
        if all(int(e in red) == color for e in combinations(q, 2)):
            found[color].append(q)
    return found


def action_audit(red):
    action = [v+1 if v < 33 and v % 3 < 2 else v-2 if v < 33 else v for v in range(43)]
    for u, v in combinations(range(43), 2):
        need(((u, v) in red) == (tuple(sorted((action[u], action[v]))) in red), 'C3 action')
    for t in range(11):
        for e in combinations(range(3*t, 3*t+3), 2):
            need((e in red) == (t < 4), 'internal color')
    word = ''.join(str(int((3*i, 3*j+d) in red)) for i, j in combinations(range(4), 2) for d in range(3))
    need(word == CORE_WORD, 'core word')


def audit(work):
    original = (HERE / 'input.edges').read_bytes()
    need(hashlib.sha256(original).hexdigest() == INPUT_SHA, 'input identity')
    red = read(HERE / 'input.edges')
    action_audit(red)
    certificate = json.loads((work / 'certificate.json').read_text())
    raw = (work / 'tables.json').read_bytes()
    tables = json.loads(raw)
    need(certificate['input_sha256'] == INPUT_SHA, 'certificate input identity')
    need(certificate['tables_sha256'] == hashlib.sha256(raw).hexdigest(), 'tables identity')
    need(certificate['tables_bytes'] == len(raw), 'tables byte length')
    for key, val in [('vertices', 43), ('block_count', 10), ('bits_per_block', 11),
                     ('assignments_per_block', 2048), ('assignment_scores', 20480), ('distinct_colorings', 20471)]:
        need(certificate[key] == val, key)
    need(len(certificate['blocks']) == len(tables) == 10, 'all ten blocks')
    base_bad = literal(43, red)
    recursive_bad = [cliques(color_rows(43, red, c), 5, (1 << 43)-1) for c in (0, 1)]
    need(base_bad == recursive_bad, 'base literal/recursive agreement')
    groups = {v: v//3 for v in range(33)}
    choices = []
    summaries = []
    for index, f in enumerate(range(33, 43)):
        coeff = reconstruct(43, red, f, groups)
        base = sum(1 << t for t in range(11) if (3*t, f) in red)
        block = certificate['blocks'][index]
        values = validate_block(block, coeff, f, base, tables[index])
        need(values[base] == list(map(len, base_bad)), 'unchanged graph counts')
        choices.extend((sum(counts), f, a) for a, counts in enumerate(values))
        summaries.append({k: block[k] for k in ('fixed_vertex', 'base_mask', 'minimum', 'argmin_masks',
                                              'minimum_changed', 'improving_assignments', 'neutral_changed_assignments')})
    score, f, mask = min(choices)
    expected_winner = {'score': score, 'fixed_vertex': f, 'mask': mask,
                       'edges_sha256': hashlib.sha256((work / 'winner.edges').read_bytes()).hexdigest()}
    need(certificate['winner'] == expected_winner, 'winner selection')
    winner = read(work / 'winner.edges')
    for u, v in combinations(range(43), 2):
        expected = bool(mask & (1 << (u//3))) if v == f and u < 33 else (u, v) in red
        need(((u, v) in winner) == expected, 'decoded winner coloring')
    action_audit(winner)
    winner_bad = literal(43, winner)
    need(winner_bad == [cliques(color_rows(43, winner, c), 5, (1 << 43)-1) for c in (0, 1)], 'winner literal/recursive')
    need(sum(map(len, winner_bad)) == score, 'physical winner score')
    return {'verified': True, 'blocks': summaries, 'assignment_scores_checked': 20480,
            'distinct_colorings': 20471, 'base_counts_blue_red': list(map(len, base_bad)),
            'winner': expected_winner, 'winner_counts_blue_red': list(map(len, winner_bad)),
            'winner_red_edges': len(winner), 'changed_physical_pairs': len(winner ^ red),
            'minimum_changed': min(b['minimum_changed'] for b in summaries),
            'coefficient_records': sum(len(c) for b in certificate['blocks'] for c in b['coefficients_blue_red']),
            'target_graph': score == 0}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = audit(a.work)
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('VERIFIED', report['assignment_scores_checked'], 'assignment scores; minimum', report['winner']['score'])
