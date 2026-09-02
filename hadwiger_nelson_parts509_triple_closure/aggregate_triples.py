#!/usr/bin/env python3
"""Aggregate the per-vertex triple-closure results into U(A) for every triple
A of Q3 points with at least one declared vertex outside the swap-implied part,
and list the triples with |U(A)| >= 4 (candidates for a 508-vertex graph
G - D + A, D a 4-subset of U(A)).  Optionally run the direct tests.
"""
from __future__ import annotations
import json, sys, time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / 'triple_results'
_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
N = 509


def main():
    swaps = json.loads((PAIRDIR / 'swaps.json').read_text())
    swap_u_of_point = defaultdict(set)
    for q, u in swaps:
        swap_u_of_point[q].add(u)
    files = sorted(RES.glob('u_*.json'))
    print(f'{len(files)} vertex files', flush=True)
    U = defaultdict(set)              # triple -> set of u (explicit + new-pair-implied)
    stats = defaultdict(int)
    nq = 1158
    for f in files:
        r = json.loads(f.read_text())
        u = r['u']
        stats['witnesses'] += r['witnesses']; stats['unsat'] += r['unsat']; stats['budget'] += r['budget']
        stats['calls'] += r['sat_calls']
        sp = set(r['swap_points'])
        for t in r['declared_triples']:
            A = tuple(t[:3])
            U[A].add(u)
            stats['explicit_' + t[3]] += 1
        for (a, b) in r['declared_pairs']:
            if a in sp or b in sp:
                continue                      # swap-implied pair: same u as the swap point
            stats['new_pairs'] += 1
            for q in range(nq):
                if q != a and q != b:
                    U[tuple(sorted((a, b, q)))].add(u)
    # add swap-implied u's
    hist = defaultdict(int)
    cands = []
    for A, us in U.items():
        full = set(us)
        for q in A:
            full |= swap_u_of_point.get(q, set())
        hist[len(full)] += 1
        if len(full) >= 4:
            cands.append({'A': list(A), 'U': sorted(full)})
    # triples made of three swap points only: |U| = 3 from swaps alone (no other contribution) -> not candidates
    print('stats', dict(stats))
    print('|U(A)| histogram over triples with a non-swap contribution:', dict(sorted(hist.items())))
    print('candidates |U|>=4:', len(cands))
    (HERE / 'candidates_508.json').write_text(json.dumps({'stats': dict(stats), 'histogram': dict(hist), 'candidates': cands}))


if __name__ == '__main__':
    main()
