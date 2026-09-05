#!/usr/bin/env python3
"""Literal graph, degree-table and exact linear-certificate checks; no producer import."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re

PIN = '8b6b7b1b17d4a8b62cbeff401acad021764bc55986e65cab557ed9500dad48ed'
SIGNATURES = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def core_matrix(bits):
    need(len(bits) == 18 and set(bits) <= {'0', '1'}, 'core bits')
    adj = [[False]*12 for _ in range(12)]
    offset = 0
    for i, j in combinations(range(4), 2):
        for d in range(3):
            for s in range(3):
                a, b = 3*i+s, 3*j+(s+d) % 3
                adj[a][b] = adj[b][a] = bits[offset+d] == '1'
        offset += 3
    for i in range(4):
        for a, b in combinations(range(3*i, 3*i+3), 2):
            adj[a][b] = adj[b][a] = True
    return adj


def classify(cover, result):
    need(result['format'] == 'r55-k11-four-blue-k4-exclusion-v1' and result['cover_sha256'] == PIN, 'classification format/input')
    excluded, retained = [], []
    for case in cover['cases']:
        adj = core_matrix(case['bits'])
        blues = [list(vs) for vs in combinations(range(12), 4)
                 if all(not adj[a][b] for a, b in combinations(vs, 2))]
        row = dict(index=case['index'], bits=case['bits'], labeled=case['labeled'])
        if blues:
            row['blue_k4'] = blues[0]
            excluded.append(row)
        else:
            retained.append(row)
    need(result['excluded'] == excluded and result['retained'] == retained, 'complete core partition')
    need(result['excluded_classes'] == len(excluded) == 118 and result['retained_classes'] == len(retained) == 79, 'class counts')
    for label, rows in [('excluded', excluded), ('retained', retained)]:
        need(result[label+'_labeled'] == sum(r['labeled'] for r in rows), 'labeled count')
    need(result['excluded_labeled']+result['retained_labeled'] == 115543, 'labeled coverage')
    return result['excluded_labeled'], result['retained_labeled']


def fixed_matrix(variant):
    adj = [[False]*10 for _ in range(10)]
    removed = {1: (3, 12), 2: (5, 10), 4: (9, 6)}.get(variant)
    for i, j in combinations(range(10), 2):
        red = SIGNATURES[i] & SIGNATURES[j] == 0
        if removed and {SIGNATURES[i], SIGNATURES[j]} == set(removed):
            red = False
        adj[i][j] = adj[j][i] = red
    return adj


def attachment_graph(fixed, mask):
    adj = [row+[False]*3 for row in fixed]+[[False]*13 for _ in range(3)]
    for f in range(10):
        for u in range(10, 13):
            adj[f][u] = adj[u][f] = not(mask >> f & 1)
    return adj


def k5_free(adj):
    # Independent literal five-set test; only stop after finding an actual bad set.
    for vs in combinations(range(len(adj)), 5):
        first = adj[vs[0]][vs[1]]
        if all(adj[a][b] == first for a, b in combinations(vs, 2)):
            return False
    return True


def attachments(data):
    need(data['format'] == 'r55-blue-triangle-fixed-attachments-v1', 'attachment format')
    need(data['fixed_signatures'] == list(SIGNATURES) and data['complementary_variants'] == [0, 1, 2, 4], 'attachment labels')
    need(data['requires_singleton'] is True and data['max_pair_signatures'] == 1, 'attachment bounds')
    rows = []
    for variant in (0, 1, 2, 4):
        fixed = fixed_matrix(variant)
        allowed = [mask for mask in range(1024) if k5_free(attachment_graph(fixed, mask))]
        need(allowed == data['blue_fixed_masks'] and len(allowed) == 33, 'complete literal attachment set')
        need(all(mask & 15 and (mask >> 4).bit_count() <= 1 for mask in allowed), 'packing row bridge')
        # A pair-signature vertex has six red core neighbors and these fixed neighbors.
        local_degrees = [6+sum(fixed[f]) for f in range(4, 10)]
        need(all(d in (8, 9) for d in local_degrees), 'local pair degrees')
        degree_table = []
        for d in local_degrees:
            full = [d+3*(7-b) for b in range(8)]
            feasible = [b for b, total in enumerate(full) if total <= 24]
            need(feasible == list(range(2, 8)), 'packing column bridge from degree upper bound')
            degree_table.append(full)
        rows.append(dict(variant=variant, allowed=len(allowed), max_pairs=max((m >> 4).bit_count() for m in allowed),
                         local_degrees=local_degrees, degree_table=degree_table))
    return rows


def parse_opb(raw):
    lines = raw.splitlines()
    need(lines and lines[0] == '* #variable= 42 #constraint= 13', 'packing header')
    need(len(lines) == 14, 'packing row count')
    rows = []
    for line in lines[1:]:
        match = re.fullmatch(r'((?:[+-]\d+ x\d+ )+)>= (-?\d+) ;', line)
        need(match is not None, 'packing syntax')
        terms = re.findall(r'([+-]\d+) x(\d+)', match.group(1))
        vector = [0]*42
        seen = set()
        for coefficient, variable in terms:
            i = int(variable)-1
            need(0 <= i < 42 and i not in seen, 'packing variable')
            seen.add(i)
            vector[i] = int(coefficient)
        rows.append((vector, int(match.group(2))))
    return rows


def certificate(raw, cert):
    rows = parse_opb(raw)
    for r, (coeff, rhs) in enumerate(rows):
        expected = [(-1 if i//6 == r else 0) if r < 7 else (1 if i % 6 == r-7 else 0) for i in range(42)]
        need(coeff == expected and rhs == (-1 if r < 7 else 2), 'packing semantic row')
    need(cert['format'] == 'nonnegative-integer-row-sum-v1', 'certificate format')
    weights = cert['multipliers']
    need(len(weights) == 13 and all(type(w) is int and w >= 0 for w in weights), 'nonnegative row multipliers')
    coeff = [sum(weights[r]*rows[r][0][i] for r in range(13)) for i in range(42)]
    rhs = sum(w*row[1] for w, row in zip(weights, rows))
    need(coeff == cert['expected_coefficients'] == [0]*42, 'coefficient cancellation')
    need(rhs == cert['expected_rhs'] == 5, 'positive contradiction')
    return dict(variables=42, inequalities=13, summed_coefficients=coeff, summed_rhs=rhs, contradiction='0 >= 5')


def run(cover_path, source, report):
    raw = cover_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'pinned core cover')
    cover = json.loads(raw)
    counts = classify(cover, json.loads((source/'classification.json').read_text()))
    attachment_rows = attachments(json.loads((source/'attachments.json').read_text()))
    linear = certificate((source/'packing.opb').read_text(), json.loads((source/'packing_certificate.json').read_text()))
    out = dict(verified=True, excluded_classes=118, retained_classes=79, excluded_labeled=counts[0], retained_labeled=counts[1],
               literal_core_four_sets=197*495, literal_attachment_graphs=4096, attachment_rows=attachment_rows,
               packing=linear, external_degree_upper_bound=24,
               files={name: hashlib.sha256((source/name).read_bytes()).hexdigest()
                      for name in ('classification.json', 'attachments.json', 'packing.opb', 'packing_certificate.json')})
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('verified', 'excluded_classes', 'retained_classes', 'excluded_labeled', 'retained_labeled')}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    run(a.cover, a.source, a.report)
