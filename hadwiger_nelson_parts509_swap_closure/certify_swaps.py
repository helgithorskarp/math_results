#!/usr/bin/env python3
"""DRAT certification of swap instances (q, u): G - u + q is not 4-colourable.

For each instance a standalone DIMACS file is written with the plain encoding
(one at-least-one clause per vertex, four binary exclusions per edge, three
distinct-colour pins on a triangle of G-u).  CaDiCaL writes a DRAT proof, and
drat-trim replays it.  Only hashes, sizes and checker summaries are kept in the
JSON report; CNFs and proofs stay under /scratch.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess, sys, time
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
N, K, X = 509, 4, 509
CFG = {}


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509', BASE / 'parts509.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def color_var(v, c):
    return v * K + c + 1


def swap_cnf_clauses(edges, triangle_avoiding, nbrs, u):
    """Plain 4-colouring CNF of the strict graph on (V - u) + q, q = vertex X."""
    clauses = []
    for v in range(N + 1):
        if v != u:
            clauses.append([color_var(v, c) for c in range(K)])
    graph_edges = [(a, b) for a, b in edges if a != u and b != u]
    graph_edges += [(w, X) for w in nbrs if w != u]
    for a, b in graph_edges:
        for c in range(K):
            clauses.append([-color_var(a, c), -color_var(b, c)])
    for c, v in enumerate(triangle_avoiding(N, edges, u)):
        clauses.append([color_var(v, c)])
    return clauses, graph_edges


def write_dimacs(path, clauses):
    with path.open('w') as f:
        f.write(f"p cnf {(N + 1) * K} {len(clauses)}\n")
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def init(cadical, drat_trim, outdir):
    parts = load_parts()
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    comp = json.loads((HERE / 'completion_points.json').read_text())
    q4 = [tuple(r['neighbors']) for r in comp['points'] if len(r['neighbors']) >= 4]
    CFG.update(parts=parts, edges=edges, q4=q4, cadical=cadical, drat_trim=drat_trim, outdir=Path(outdir))


def certify(inst):
    qi, u = inst
    parts, edges, q4 = CFG['parts'], CFG['edges'], CFG['q4']
    out = CFG['outdir']
    stem = out / f"swap_q{qi:04d}_u{u:03d}"
    cnf, proof, report = stem.with_suffix('.cnf'), stem.with_suffix('.drat'), stem.with_suffix('.json')
    if report.exists():
        return json.loads(report.read_text())
    t0 = time.time()
    clauses, graph_edges = swap_cnf_clauses(edges, parts.triangle_avoiding, q4[qi], u)
    write_dimacs(cnf, clauses)
    sat = subprocess.run([CFG['cadical'], '-q', str(cnf), str(proof)], capture_output=True, text=True)
    t_solve = time.time() - t0
    if sat.returncode != 20:
        result = {'q': qi, 'u': u, 'status': 'NOT_UNSAT', 'cadical_exit': sat.returncode, 'seconds_solve': round(t_solve, 1)}
        report.write_text(json.dumps(result))
        return result
    t1 = time.time()
    chk = subprocess.run([CFG['drat_trim'], str(cnf), str(proof)], capture_output=True, text=True)
    verified = 's VERIFIED' in chk.stdout
    summary = [line for line in chk.stdout.splitlines() if line.startswith('c ') and ('lemmas' in line or 'clauses' in line or 'resolution' in line)]
    result = {
        'q': qi, 'u': u,
        'status': 'VERIFIED' if verified else 'CHECK_FAILED',
        'cnf_variables': (N + 1) * K, 'cnf_clauses': len(clauses), 'graph_edges': len(graph_edges),
        'cnf_sha256': sha256(cnf), 'proof_bytes': proof.stat().st_size, 'proof_sha256': sha256(proof),
        'drat_trim_summary': summary, 'seconds_solve': round(t_solve, 1), 'seconds_check': round(time.time() - t1, 1),
    }
    report.write_text(json.dumps(result))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--swaps', type=Path, required=True, help='JSON list of [q_index, u] pairs')
    ap.add_argument('--outdir', type=Path, required=True)
    ap.add_argument('--cadical', default='/scratch/cadical-package/usr/bin/cadical')
    ap.add_argument('--drat-trim', default='/scratch/researcher-3-drat-trim/drat-trim')
    ap.add_argument('--workers', type=int, default=4)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    insts = [tuple(x) for x in json.loads(args.swaps.read_text())]
    print(f"{len(insts)} swap instances", flush=True)
    t0 = time.time()
    counts = {}
    with Pool(args.workers, initializer=init, initargs=(args.cadical, args.drat_trim, str(args.outdir))) as pool:
        for r in pool.imap_unordered(certify, insts, chunksize=1):
            counts[r['status']] = counts.get(r['status'], 0) + 1
            print(f"q={r['q']} u={r['u']} {r['status']} solve={r.get('seconds_solve')}s check={r.get('seconds_check')}s proof={r.get('proof_bytes')}  elapsed={time.time()-t0:.0f}s", flush=True)
    print('summary:', counts, flush=True)


if __name__ == '__main__':
    main()
