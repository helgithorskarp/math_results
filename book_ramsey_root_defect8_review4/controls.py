#!/usr/bin/env python3
"""Signed graph bridge samples and a known positive book fixture.

The Havel--Hakimi/switch generator adapts this reviewer's earlier source
25f496ce12ac7b323c1fd3561135f77a56bf7935. These samples are not host coverage.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

from incidence import digest, need
from reference import replay_rounds


def havel_hakimi():
    remaining = [8]*4+[10]*2+[9]*16
    rows = [set() for _ in remaining]
    while any(remaining):
        order = sorted(range(22), key=lambda i: (-remaining[i], i))
        i = order[0]
        amount = remaining[i]
        need(amount <= len(order)-1, 'graphical degree sequence')
        remaining[i] = 0
        for j in order[1:amount+1]:
            need(remaining[j] > 0 and j not in rows[i], 'Havel--Hakimi step')
            rows[i].add(j)
            rows[j].add(i)
            remaining[j] -= 1
    return rows


def graph_bridge(rows):
    d = list(map(len, rows))
    need(d == [8]*4+[10]*2+[9]*16, 'signed sample histogram')
    need(all(i not in rows[i] and (j in rows[i]) == (i in rows[j])
             for i in range(22) for j in range(22)), 'simple signed sample')
    universe = set(range(22))
    blue = [universe-rows[i]-{i} for i in range(22)]
    F = [[0]*22 for _ in range(22)]
    for i, j in combinations(range(22), 2):
        red_pages = len(rows[i] & rows[j])
        defect = 3-red_pages if j in rows[i] else 6-len(blue[i] & blue[j])
        F[i][j] = F[j][i] = defect
        formula = d[i]+d[j]-14+(17-d[i]-d[j])*int(j in rows[i])-defect
        need(formula == red_pages, 'signed ordinary pair formula')
    f = list(map(sum, F))
    for i in range(22):
        h = len(rows[i] & set(range(4)))
        k = len(rows[i] & {4, 5})
        wanted = 2*(h-k-1) if i < 4 else 2*(h-k+1) if i < 6 else 1+2*(h-k)
        need(f[i] == wanted, 'signed incident class identity')
        red_triangles = sum(int(b in rows[a]) for a, b in combinations(rows[i], 2))
        blue_triangles = sum(int(b in blue[a]) for a, b in combinations(blue[i], 2))
        need(f[i] == 3*d[i]+6*(21-d[i])-2*(red_triangles+blue_triangles), 'literal incident triangles')
    eA = sum(int(j in rows[i]) for i, j in combinations(range(4), 2))
    eC = int(5 in rows[4])
    q = sum(f[:6])
    need(q == -4+4*(eA-eC) and sum(f) == 36, 'signed total/root budget')
    need(sum(x-1 for x in f[6:]) == 20-q, 'signed B surplus')
    M = [[int(j in rows[6+i]) for j in range(6)] for i in range(16)]
    G = [[sum(M[v][i]*M[v][j] for v in range(16)) for j in range(6)] for i in range(6)]
    s = [d[i]-len(rows[i] & set(range(6))) for i in range(6)]
    for i in range(6):
        need(G[i][i] == s[i], 'signed Gram diagonal')
        for j in range(i+1, 6):
            common = d[i]+d[j]-14+(17-d[i]-d[j])*int(j in rows[i])-F[i][j]
            need(G[i][j] == common-len(rows[i] & rows[j] & set(range(6))), 'signed root Gram pair')
    for v in range(16):
        for j in range(6):
            PM = sum(M[x][j] for x in range(16) if 6+x in rows[6+v])
            MR = sum(M[v][k] for k in range(6) if k in rows[j])
            rhs = (3 if j < 4 else 5)-2*M[v][j]*int(j >= 4)-MR-F[6+v][j]
            need(PM == rhs, 'signed root--B equation')
    # The original correlation identity is audited, then omitted from the proof filter.
    K = [[sum(M[v][i]*M[x][j] for v in range(16) for x in range(16)
              if 6+x in rows[6+v]) for j in range(6)] for i in range(6)]
    Z = [[s[i]*(3 if j < 4 else 5)-sum(G[i][k] for k in rows[j] if k < 6)
          -2*G[i][j]*int(j >= 4) for j in range(6)] for i in range(6)]
    for i in range(6):
        for j in range(6):
            MTW = sum(M[v][i]*F[6+v][j] for v in range(16))
            need(K[i][j] == K[j][i] and K[i][j] == Z[i][j]-MTW, 'signed MTPM identity')
    return digest([sorted(row) for row in rows]), all(F[i][j] >= 0 for i, j in combinations(range(22), 2))


def run():
    rows = havel_hakimi()
    records = []
    valid = 0
    edges = list(combinations(range(22), 2))
    for sample in range(16):
        sha, is_valid = graph_bridge(rows)
        records.append([sample, sha])
        valid += is_valid
        if sample == 15:
            break
        chosen = None
        for offset in range(len(edges)):
            i, j = edges[(offset+17*sample) % len(edges)]
            if j not in rows[i]:
                continue
            for x, y in edges:
                if len({i, j, x, y}) == 4 and y in rows[x] and x not in rows[i] and y not in rows[j]:
                    chosen = i, j, x, y
                    break
            if chosen:
                break
        need(chosen is not None, 'degree-preserving switch exists')
        i, j, x, y = chosen
        for a, b in [(i, j), (x, y)]:
            rows[a].remove(b)
            rows[b].remove(a)
        for a, b in [(i, x), (j, y)]:
            rows[a].add(b)
            rows[b].add(a)
    need(valid == 0, 'signed samples are not valid book hosts')
    fixture = Path(__file__).with_name('baseline21.rows').read_text().splitlines()
    need(len(fixture) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in fixture), 'fixture encoding')
    red = [{j for j, v in enumerate(row) if v == '1'} for row in fixture]
    need(all(i not in red[i] and (j in red[i]) == (i in red[j]) for i in range(21) for j in range(21)), 'simple fixture')
    blue = [set(range(21))-red[i]-{i} for i in range(21)]
    rp = [len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]]
    bp = [len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j not in red[i]]
    need((len(rp), max(rp), max(bp)) == (93, 3, 6), 'known positive ordinary book fixture')
    rejected = False
    try:
        replay_rounds([[2], [1]], {'excluded': True,
                      'rounds': [{'before': [1, 1], 'after': [0, 1]}]})
    except ValueError:
        rejected = True
    need(rejected, 'fabricated supported deletion must be rejected')
    return {'signed_graphs': 16, 'distinct_signed_graphs': len({r[1] for r in records}),
            'signed_graph_stream_sha256': digest(records), 'valid_book_hosts': valid,
            'off_diagonal_pairs': 16*231, 'incident_rows': 16*22,
            'root_Gram_entries': 16*36, 'root_B_equations': 16*96,
            'MTPM_equations': 16*36, 'root_budget_checks': 16,
            'fabricated_supported_deletion_rejected': True,
            'known_positive_fixture': {'vertices': 21, 'red_edges': len(rp),
                                       'red_page_maximum': max(rp), 'blue_page_maximum': max(bp)},
            'complete': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = run()
    if args.expected:
        need(result == json.loads(args.expected.read_text()), 'controls expected mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
