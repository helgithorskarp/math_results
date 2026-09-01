#!/usr/bin/env python3
"""One-point swap search on the Parts-509 graph.

For every completion point q with >= 4 unit neighbours and every vertex u,
decide whether the strict unit-distance graph on (V - u) + q is 4-colourable.
A proper 4-colouring of G-u in which N(q)-u misses a colour is a witness.
Witnesses are shared greedily: every colouring found for G-u is tested
against all still-uncovered points for that u.  Instances with no witness
(solver reports UNSAT under assumptions) are recorded as swaps; they are
certified separately with DRAT proofs.  Results are written per vertex so
the run can be resumed.
"""
from __future__ import annotations
import argparse, importlib.util, json, sys, time, base64, hashlib
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
OUT = HERE / 'swap_results'
N, K = 509, 4
X = N  # index of the added vertex

DATA = {}


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509', BASE / 'parts509.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def init(solver_name):
    parts = load_parts()
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    cert = json.loads((BASE / 'certificate.json').read_text())
    packed = base64.b64decode(cert['deletion_colorings_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_deletion_colorings_sha256']
    rows = parts.unpack_deletion_rows(packed, N)
    for d, row in enumerate(rows):
        parts.validate_coloring(N, edges, row, K, d)
    comp = json.loads((HERE / 'completion_points.json').read_text())
    q4 = [tuple(r['neighbors']) for r in comp['points'] if len(r['neighbors']) >= 4]
    DATA.update(parts=parts, edges=edges, rows=rows, q4=q4, solver=solver_name)


def rainbow(coloring, nbrs, u):
    seen = 0
    for w in nbrs:
        if w != u:
            seen |= 1 << coloring[w]
    return seen == 15


def color_var(v, c):
    return v * K + c + 1


def run_u(u):
    from pysat.solvers import Solver
    parts, edges, rows, q4 = DATA['parts'], DATA['edges'], DATA['rows'], DATA['q4']
    t0 = time.time()
    uncovered = [qi for qi, nb in enumerate(q4) if rainbow(rows[u], nb, u)]
    initial = len(uncovered)
    sel_base = (N + 1) * K
    clauses = []
    for v in range(N):
        if v != u:
            clauses.append([color_var(v, c) for c in range(K)])
    clauses.append([color_var(X, c) for c in range(K)])
    for a, b in edges:
        if a != u and b != u:
            for c in range(K):
                clauses.append([-color_var(a, c), -color_var(b, c)])
    for c, v in enumerate(parts.triangle_avoiding(N, edges, u)):
        clauses.append([color_var(v, c)])
    for qi in uncovered:
        s = sel_base + qi + 1
        for w in q4[qi]:
            if w != u:
                for c in range(K):
                    clauses.append([-s, -color_var(X, c), -color_var(w, c)])
    colorings = []
    swaps = []
    sat_calls = 0
    with Solver(name=DATA['solver'], bootstrap_with=clauses) as solver:
        while uncovered:
            qi = uncovered[0]
            sat_calls += 1
            ok = solver.solve(assumptions=[sel_base + qi + 1])
            if not ok:
                swaps.append(qi)
                uncovered.pop(0)
                continue
            model = solver.get_model()
            pos = {lit for lit in model if lit > 0}
            coloring = []
            for v in range(N):
                if v == u:
                    coloring.append(-1)
                    continue
                sel = [c for c in range(K) if color_var(v, c) in pos]
                assert sel, f"vertex {v} uncoloured"
                coloring.append(sel[0])
            parts.validate_coloring(N, edges, coloring, K, u)
            newly = [qj for qj in uncovered if not rainbow(coloring, q4[qj], u)]
            assert qi in newly, "target instance not covered by its own model"
            remaining = [qj for qj in uncovered if rainbow(coloring, q4[qj], u)]
            uncovered = remaining
            colorings.append(''.join('-' if c < 0 else str(c) for c in coloring))
    result = {
        'u': u,
        'initial_uncovered': initial,
        'sat_calls': sat_calls,
        'colorings': colorings,
        'swaps': swaps,
        'seconds': round(time.time() - t0, 2),
    }
    (OUT / f'u_{u:03d}.json').write_text(json.dumps(result))
    return u, initial, sat_calls, len(colorings), len(swaps), result['seconds']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    todo = [u for u in range(N) if not (OUT / f'u_{u:03d}.json').exists()]
    print(f"{len(todo)} vertices to process", flush=True)
    t0 = time.time()
    with Pool(args.workers, initializer=init, initargs=(args.solver,)) as pool:
        for u, initial, calls, ncol, nsw, sec in pool.imap_unordered(run_u, todo, chunksize=1):
            print(f"u={u:3d} uncovered0={initial:4d} calls={calls:4d} colorings={ncol:4d} swaps={nsw:3d} {sec:7.1f}s  elapsed={time.time()-t0:7.0f}s", flush=True)


if __name__ == '__main__':
    main()
