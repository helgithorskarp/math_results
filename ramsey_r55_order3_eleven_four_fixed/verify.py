#!/usr/bin/env python3
"""Independent literal graph checks; imports no construction or core-cover code."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

PIN = '8b6b7b1b17d4a8b62cbeff401acad021764bc55986e65cab557ed9500dad48ed'
SIG = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12)
CHOICES = (0, 1, 2, 4)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def matrix(bits):
    """Generate core edges by literal simultaneous-rotation orbits."""
    adj = [0]*12
    pos = 0
    for i, j in combinations(range(4), 2):
        for offset in range(3):
            if bits[pos] == '1':
                a, b = 3*i, 3*j+offset
                for _ in range(3):
                    adj[a] |= 1 << b
                    adj[b] |= 1 << a
                    a = 3*i+(a+1) % 3
                    b = 3*j+(b+1) % 3
            pos += 1
    for i in range(4):
        for a, b in combinations(range(3*i, 3*i+3), 2):
            adj[a] |= 1 << b
            adj[b] |= 1 << a
    return adj


def clique_count(adj, color, size=5):
    n = len(adj)
    neighbors = adj if color else [((1 << n)-1) ^ row ^ (1 << i) for i, row in enumerate(adj)]

    def visit(candidates, left):
        if left == 0:
            return 1
        total = 0
        while candidates.bit_count() >= left:
            bit = candidates & -candidates
            candidates ^= bit
            total += visit(candidates & neighbors[bit.bit_length()-1], left-1)
        return total
    return visit((1 << n)-1, size)


def attach(core, masks, variant=0):
    adj = core.copy()+[0]*len(masks)
    for u, s in enumerate(masks, 12):
        for v in range(12):
            if (s >> (v//3)) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    opposite = [(3, 12), (5, 10), (9, 6)]
    for a, b in combinations(range(len(masks)), 2):
        sa, sb = masks[a], masks[b]
        red = sa & sb == 0
        for i, (x, y) in enumerate(opposite):
            if {sa, sb} == {x, y} and variant & (1 << i):
                red = False
        if red:
            adj[12+a] |= 1 << (12+b)
            adj[12+b] |= 1 << (12+a)
    return adj


def serialize(adj):
    pairs = [(a, b) for a, b in combinations(range(len(adj)), 2) if adj[a] >> b & 1]
    return (f'{len(adj)} {len(pairs)}\n'+''.join(f'{a} {b}\n' for a, b in pairs)).encode()


def parse(raw):
    lines = raw.decode().splitlines()
    need(bool(lines), 'empty edge list')
    n, m = map(int, lines[0].split())
    need(n == 22 and len(lines) == m+1, 'edge header')
    es = [tuple(map(int, line.split())) for line in lines[1:]]
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < n for e in es), 'edge endpoints')
    need(es == sorted(set(es)), 'edge ordering or duplicate')
    adj = [0]*n
    for a, b in es:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    need(serialize(adj) == raw, 'noncanonical edge encoding')
    return adj


def audit_row(row, bits, graphs):
    need(row['bits'] == bits, 'core bit string')
    core = matrix(bits)
    need(clique_count(core, 0) == clique_count(core, 1) == 0, 'invalid core')
    allowed = []
    for mask in range(16):
        adj = attach(core, [mask])
        if clique_count(adj, 0) == clique_count(adj, 1) == 0:
            allowed.append(mask)
    need(row['allowed'] == allowed, 'one-fixed signature census')
    red_supports, blue = set(), []
    for vs in combinations(range(12), 4):
        vals = [core[a] >> b & 1 for a, b in combinations(vs, 2)]
        if all(vals):
            red_supports.add(sum(1 << i for i in {v//3 for v in vs}))
        elif not any(vals):
            blue.append(list(vs))
    need(row['red_k4_supports'] == sorted(red_supports), 'red K4 supports')
    need(row['blue_k4'] == (blue[0] if blue else None), 'blue K4 witness')
    bad_counts = []
    for variant in range(8):
        adj = attach(core, SIG, variant)
        counts = [clique_count(adj, c) for c in (1, 0)]
        expected = [0, 0 if variant.bit_count() <= 1 else 2 if variant.bit_count() == 2 else 6]
        need(counts == expected, 'template clique census')
        bad_counts.append(counts)
        if variant not in CHOICES:
            continue
        raw = (graphs/f"core{row['index']:03d}_v{variant}.edges").read_bytes()
        decoded = parse(raw)
        need(decoded == adj, 'literal template edge mismatch')
        j = CHOICES.index(variant)
        need(hashlib.sha256(raw).hexdigest() == row['edge_sha256'][j], 'edge hash')
        need(sum(x.bit_count() for x in adj)//2 == row['red_edges'][j], 'red edge count')
        perm = [3*(v//3)+(v+1) % 3 if v < 12 else v for v in range(22)]
        need(all((adj[a] >> b & 1) == (adj[perm[a]] >> perm[b] & 1)
                 for a, b in combinations(range(22), 2)), 'order-three action')
    return dict(index=row['index'], allowed=len(allowed), blue_k4=bool(blue),
                bad_counts=bad_counts, edges=row['red_edges'])


def preflight(result, cover):
    need(result['format'] == 'r55-four-core-fixed-template-v1', 'result format')
    need(result['cover_sha256'] == PIN, 'result input hash')
    need(result['signatures'] == list(SIG) and result['variants'] == list(CHOICES), 'template convention')
    need(result['cores'] == len(result['cases']) == len(cover['cases']) == 197, 'class count')
    need([r['index'] for r in result['cases']] == list(range(197)), 'class indices')


def run(cover_path, source, report):
    raw = cover_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'inherited cover hash')
    cover = json.loads(raw)
    result = json.loads((source/'result.json').read_text())
    preflight(result, cover)
    summaries = [audit_row(row, case['bits'], source/'graphs')
                 for row, case in zip(result['cases'], cover['cases'])]
    count = sum(r['blue_k4'] for r in summaries)
    need(result['blue_k4_cores'] == count == 118, 'rigid-core count')
    out = dict(verified=True, cores=197, one_fixed_graphs=197*16,
               template_graphs=197*8, valid_template_graphs=197*4,
               serialized_edges_checked=197*4, action_pair_checks=197*4*231,
               blue_k4_cores=count, other_cores=197-count,
               allowed_histogram=sorted(Counter(r['allowed'] for r in summaries).items()),
               template_red_k5_counts=[0]*8,
               template_blue_k5_counts=[0, 0, 0, 2, 0, 2, 2, 6],
               result_sha256=hashlib.sha256((source/'result.json').read_bytes()).hexdigest())
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    run(a.cover, a.source, a.report)
