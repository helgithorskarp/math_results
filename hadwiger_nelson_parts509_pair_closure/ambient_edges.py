#!/usr/bin/env python3
"""Exact unit-distance edges of the ambient point set W3 = V ∪ Q3.

All coordinates are scaled to a common integer denominator so that every
squared-distance test is an exact integer computation in the basis of
K = Q(sqrt3, sqrt5, sqrt11).  V×V edges are taken from the exact 2442-edge
reconstruction and re-verified; Q3×V and Q3×Q3 pairs are tested exhaustively.
"""
from __future__ import annotations
import importlib.util, json, sys, time
from fractions import Fraction
from math import lcm
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kfield as kf
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
_SW = [HERE.parent / 'hadwiger_nelson_parts509_swap_closure',
       Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure']
SWAPDIR = next(p for p in _SW if (p / 'swap_certificate.json').exists())
sys.path.insert(0, str(SWAPDIR))
PRIMES = (3, 5, 11)
K = 3
PTS = None
L2ONE = None


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509', BASE / 'parts509.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def imul(x, y):
    out = [0] * 8
    for sx, a in enumerate(x):
        if not a:
            continue
        for sy, b in enumerate(y):
            if not b:
                continue
            c = a * b
            common = sx & sy
            if common & 1:
                c *= 3
            if common & 2:
                c *= 5
            if common & 4:
                c *= 11
            out[sx ^ sy] += c
    return out


def load_points():
    parts = load_parts()
    vpts = parts.parse_points(BASE / 'parts509.vtx')
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    qpts = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in comp['points']]
    allpts = list(vpts) + qpts
    den = 1
    for x, y in allpts:
        for c in x + y:
            den = lcm(den, c.denominator)
    scaled = [([int(c * den) for c in x], [int(c * den) for c in y]) for x, y in allpts]
    return parts, vpts, qpts, scaled, den


def init():
    global PTS, L2ONE
    _, _, _, scaled, den = load_points()
    PTS = scaled
    L2ONE = [den * den, 0, 0, 0, 0, 0, 0, 0]


def is_unit(i, j):
    xi, yi = PTS[i]
    xj, yj = PTS[j]
    dx = [a - b for a, b in zip(xi, xj)]
    dy = [a - b for a, b in zip(yi, yj)]
    s = imul(dx, dx)
    t = imul(dy, dy)
    return [a + b for a, b in zip(s, t)] == L2ONE


def row(args):
    i, start = args
    return i, [j for j in range(start, len(PTS)) if j != i and is_unit(i, j)]


def main():
    t0 = time.time()
    parts, vpts, qpts, scaled, den = load_points()
    nv, nq = len(vpts), len(qpts)
    print(f"V={nv} Q3={nq} common denominator={den}", flush=True)
    vedges = parts.build_edges(vpts)
    edges = set(vedges)
    with Pool(8, initializer=init) as pool:
        # Q3 rows: test against all V and all later Q3 points
        tasks = [(nv + a, 0) for a in range(nq)]
        for i, js in pool.imap_unordered(row, tasks, chunksize=8):
            for j in js:
                if j < nv or j > i:
                    edges.add((min(i, j), max(i, j)))
        # re-verify V×V exactly with the integer arithmetic (independent of parts509 f_mul)
        vtasks = [(i, i + 1) for i in range(nv)]
        vv = set()
        for i, js in pool.imap_unordered(row, vtasks, chunksize=8):
            for j in js:
                if j < nv:
                    vv.add((i, j))
    assert vv == set(vedges), "integer re-verification of the 2442 V×V edges failed"
    edges = sorted(edges)
    deg = [0] * (nv + nq)
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    qv = sum(1 for a, b in edges if a < nv <= b)
    qq = sum(1 for a, b in edges if a >= nv)
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    # consistency: Q3×V edges must reproduce the neighbour lists
    for a, r in enumerate(comp['points']):
        nb = sorted(e[0] for e in edges if e[1] == nv + a and e[0] < nv)
        assert nb == sorted(r['neighbors']), f"neighbour mismatch for Q3 point {a}"
    out = {
        'vertices': nv + nq, 'parts_vertices': nv, 'q3_points': nq, 'common_denominator': den,
        'edges_total': len(edges), 'edges_VV': len(vedges), 'edges_Q3V': qv, 'edges_Q3Q3': qq,
        'q3_degree_histogram': {},
        'edges': edges,
    }
    from collections import Counter
    out['q3_degree_histogram'] = {str(k): v for k, v in sorted(Counter(deg[nv:]).items())}
    (HERE / 'ambient_w3_edges.json').write_text(json.dumps(out))
    print(f"edges: total {len(edges)}, VV {len(vedges)}, Q3-V {qv}, Q3-Q3 {qq}; Q3 degree hist {out['q3_degree_histogram']}; {time.time()-t0:.1f}s", flush=True)


if __name__ == '__main__':
    main()
