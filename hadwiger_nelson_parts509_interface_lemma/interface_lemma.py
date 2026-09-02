#!/usr/bin/env python3
"""Interface classification of the L ∪ S decomposition of the Parts 509 graph.

The 509 points of Jaan Parts's 5-chromatic unit-distance graph split into the
374 points whose coordinates are free of sqrt5 (the large subgraph L, indices
0..373 in ``parts509.vtx``) and the 135 points involving sqrt5 (the small
subgraph S, indices 374..508); the origin (index 0) belongs to L and is the
centre of the rotation relating the two parts.  Exactly 30 unit-distance edges
join L to S.  Their 19 L-endpoints (origin, 3 inner auxiliary, 3 outer
auxiliary, 12 reference vertices) form the interface I_L.

Commands (all exact geometry comes from ../hadwiger_nelson_parts509_criticality):

  python3 interface_lemma.py enumerate interface_L.json --cnf-dir DIR [--cadical BIN --drat-trim BIN]
      Enumerate every proper 4-colouring of L restricted to I_L, with the origin
      coloured 0 and modulo permutations of the colours 1,2,3 (each class is
      blocked in all six permuted forms after it is found).  Writes the classes
      with one full witness colouring of L per class.  Also writes, in DIR, the
      completeness CNF (L plus all blocking clauses) and, for each class, the
      CNF asserting that S has a proper 4-colouring compatible with the class
      across the cross edges; with solver paths given, every CNF is solved with
      CaDiCaL and its DRAT proof is checked with drat-trim, and the outcomes and
      CNF hashes are recorded in DIR/block_report.json and in the JSON output.

  python3 interface_lemma.py leaks interface_L.json s_vertex_leaks.json
      For every vertex v of S, list the classes p such that S - v has a proper
      4-colouring compatible with p (with a witness colouring of L ∪ (S - v)).

Requires python-sat (CaDiCaL 1.9.5 backend) and SymPy (coordinate parsing).
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, subprocess, time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'hadwiger_nelson_parts509_criticality'
K = 4
PERMS = [(0,) + p for p in itertools.permutations((1, 2, 3))]


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509', BASE / 'parts509.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def has_sqrt5(point):
    # basis index bit 1 is sqrt5: coefficients 2,3,6,7 multiply sqrt5, sqrt15, sqrt55, sqrt165
    return any(point[j][i] != 0 for j in (0, 1) for i in (2, 3, 6, 7))


def radius_class(parts, point):
    """'origin', 'reference' (r = 2), 'aux_inner' (r = sqrt11/2 - sqrt3/6), 'aux_outer' (+), else None."""
    r2 = parts.f_add(parts.f_sq(point[0]), parts.f_sq(point[1]))
    zero = parts.ZERO
    four = tuple(Fraction(4) if i == 0 else Fraction(0) for i in range(8))
    # (sqrt11/2 ∓ sqrt3/6)^2 = 17/6 ∓ sqrt33/6 ; sqrt33 = sqrt3*sqrt11 has basis index 0b101 = 5
    inner = tuple(Fraction(17, 6) if i == 0 else (Fraction(-1, 6) if i == 5 else Fraction(0)) for i in range(8))
    outer = tuple(Fraction(17, 6) if i == 0 else (Fraction(1, 6) if i == 5 else Fraction(0)) for i in range(8))
    if r2 == zero:
        return 'origin'
    if r2 == four:
        return 'reference'
    if r2 == inner:
        return 'aux_inner'
    if r2 == outer:
        return 'aux_outer'
    return None


def decomposition():
    parts = load_parts()
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    assert len(points) == 509 and len(edges) == 2442
    assert points[0] == (parts.ZERO, parts.ZERO), 'vertex 0 must be the origin'
    L = [i for i, p in enumerate(points) if not has_sqrt5(p)]
    S = [i for i, p in enumerate(points) if has_sqrt5(p)]
    assert L == list(range(374)) and S == list(range(374, 509))
    Lset = set(L)
    cross = sorted((a, b) if a in Lset else (b, a) for a, b in edges if (a in Lset) != (b in Lset))
    assert len(cross) == 30
    IL = sorted({l for l, s in cross})
    IS = sorted({s for l, s in cross})
    labels = {v: radius_class(parts, points[v]) for v in IL}
    assert all(labels.values()), labels
    counts = {k: sum(1 for v in IL if labels[v] == k) for k in ('origin', 'aux_inner', 'aux_outer', 'reference')}
    assert counts == {'origin': 1, 'aux_inner': 3, 'aux_outer': 3, 'reference': 12}, counts
    LE = [(a, b) for a, b in edges if a in Lset and b in Lset]
    SE = [(a, b) for a, b in edges if a not in Lset and b not in Lset]
    assert len(LE) == 1860 and len(SE) == 552
    return parts, points, edges, L, S, cross, IL, IS, labels, LE, SE


def colouring_cnf(vertices, edges, origin_pin=True):
    idx = {v: i for i, v in enumerate(vertices)}
    var = lambda v, c: idx[v] * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in vertices]
    for a, b in edges:
        for c in range(K):
            clauses.append([-var(a, c), -var(b, c)])
    if origin_pin:
        clauses.append([var(0, 0)])
    return clauses, var, idx


def write_dimacs(path, nvars, clauses):
    with path.open('w') as f:
        f.write(f'p cnf {nvars} {len(clauses)}\n')
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certify(cnf, cadical, drat_trim):
    if not cadical or not drat_trim:
        return None
    proof = cnf.with_suffix('.drat')
    r = subprocess.run([cadical, '-q', str(cnf), str(proof)], capture_output=True, text=True)
    d = subprocess.run([drat_trim, str(cnf), str(proof)], capture_output=True, text=True)
    return {'cadical_exit': r.returncode, 'drat_trim_verified': 's VERIFIED' in d.stdout}


def canonical(key):
    return min(tuple(p[c] for c in key) for p in PERMS)


def cmd_enumerate(args):
    from pysat.solvers import Solver
    parts, points, edges, L, S, cross, IL, IS, labels, LE, SE = decomposition()
    IL_nz = [v for v in IL if v != 0]
    clauses, var, idx = colouring_cnf(L, LE)
    base = list(clauses)
    solver = Solver(name='cadical195', bootstrap_with=clauses)
    found = {}
    blocking = []
    t0 = time.time()
    while solver.solve():
        model = solver.get_model()
        col = [next(c for c in range(K) if model[var(v, c) - 1] > 0) for v in L]
        assert col[0] == 0
        key = tuple(col[v] for v in IL_nz)
        canon = canonical(key)
        assert canon not in found
        found[canon] = col
        for p in PERMS:
            cl = [-var(v, p[col[v]]) for v in IL_nz]
            solver.add_clause(cl)
            blocking.append(cl)
    solver.delete()
    classes = sorted(found)
    print(f'{len(classes)} interface classes in {time.time()-t0:.1f}s', flush=True)
    cnf_dir = Path(args.cnf_dir)
    cnf_dir.mkdir(parents=True, exist_ok=True)
    report = {'completeness': {}, 'blocking': []}
    h = write_dimacs(cnf_dir / 'complete_L.cnf', len(L) * K, base + blocking)
    report['completeness'] = {'cnf': 'complete_L.cnf', 'sha256': h, 'clauses': len(base) + len(blocking),
                              'result': certify(cnf_dir / 'complete_L.cnf', args.cadical, args.drat_trim)}
    print('completeness', report['completeness'], flush=True)
    # blocking instances on S: S135 (no origin) with the unit clauses induced by the class witness on I_L
    S_cl, S_var, S_idx = colouring_cnf(S, SE, origin_pin=False)
    rows = []
    for ci, canon in enumerate(classes):
        col = found[canon]
        # the witness realises `key`; store the witness and its own interface colouring
        pat = {l: col[l] for l in IL}
        cl = list(S_cl) + [[-S_var(s, pat[l])] for l, s in cross]
        h = write_dimacs(cnf_dir / f'block_{ci}.cnf', len(S) * K, cl)
        res = certify(cnf_dir / f'block_{ci}.cnf', args.cadical, args.drat_trim)
        report['blocking'].append({'class_index': ci, 'cnf': f'block_{ci}.cnf', 'sha256': h, 'clauses': len(cl), 'result': res})
        print('block', ci, res, flush=True)
        key = tuple(col[v] for v in IL_nz)
        aux_in = ''.join(str(col[v]) for v in IL_nz if labels[v] == 'aux_inner')
        aux_out = ''.join(str(col[v]) for v in IL_nz if labels[v] == 'aux_outer')
        ref = [col[v] for v in IL_nz if labels[v] == 'reference']
        mult = sorted((ref.count(c) for c in set(ref)), reverse=True)
        rows.append({'class': ''.join(map(str, canon)), 'witness_interface': ''.join(map(str, key)),
                     'witness_colouring_L': ''.join(map(str, col)),
                     'aux_inner': aux_in, 'aux_outer': aux_out, 'reference_multiplicities': mult})
    (cnf_dir / 'block_report.json').write_text(json.dumps(report, indent=1))
    out = {
        'description': 'Proper 4-colourings of L (Parts-509 vertices 0..373) restricted to the interface I_L, origin coloured 0, modulo permutations of colours 1,2,3',
        'source_vtx_sha256': parts.file_sha256(BASE / 'parts509.vtx'),
        'L_vertices': [0, 373], 'S_vertices': [374, 508], 'L_edges': len(LE), 'S_edges': len(SE),
        'cross_edges_L_S': cross, 'interface_L': IL, 'interface_L_nonorigin': IL_nz, 'interface_S': IS,
        'interface_labels': {str(v): labels[v] for v in IL},
        'class_count': len(classes), 'classes': rows, 'report': report,
    }
    Path(args.output).write_text(json.dumps(out, indent=1))
    print('wrote', args.output)


def cmd_leaks(args):
    from pysat.solvers import Solver
    parts, points, edges, L, S, cross, IL, IS, labels, LE, SE = decomposition()
    data = json.loads(Path(args.interface).read_text())
    S_cl, S_var, S_idx = colouring_cnf(S, SE, origin_pin=False)
    m = len(S)
    act = lambda v: m * K + S_idx[v] + 1
    z = lambda p: m * K + m + p + 1
    clauses = []
    for v in S:
        clauses.append([-act(v)] + [S_var(v, c) for c in range(K)])
    for a, b in SE:
        for c in range(K):
            clauses.append([-act(a), -act(b), -S_var(a, c), -S_var(b, c)])
    pats = []
    for row in data['classes']:
        col = row['witness_colouring_L']
        pats.append({l: int(col[l]) for l in IL})
    for p, pat in enumerate(pats):
        for l, s in cross:
            clauses.append([-z(p), -act(s), -S_var(s, pat[l])])
    solver = Solver(name='cadical195', bootstrap_with=clauses)
    leaks = {}
    for v in S:
        X = [s for s in S if s != v]
        entry = []
        for p in range(len(pats)):
            assum = [act(s) if s != v else -act(s) for s in S] + [z(q) if q == p else -z(q) for q in range(len(pats))]
            if solver.solve(assumptions=assum):
                model = solver.get_model()
                colS = {s: next(c for c in range(K) if model[S_var(s, c) - 1] > 0) for s in X}
                full = {l: int(data['classes'][p]['witness_colouring_L'][l]) for l in L}
                full.update(colS)
                verts = sorted(full)
                # exact check on all edges of L ∪ (S - v)
                vs = set(verts)
                for a, b in edges:
                    if a in vs and b in vs:
                        assert full[a] != full[b]
                entry.append({'class_index': p, 'witness_colouring_S_minus_v': ''.join(str(full[u]) for u in verts if u >= 374)})
        leaks[str(v)] = entry
        print(v, [e['class_index'] for e in entry], flush=True)
    solver.delete()
    Path(args.output).write_text(json.dumps({'description': 'for each S-vertex v (key), the interface classes p of L such that S - v has a proper 4-colouring compatible with class p; the witness string colours the sorted vertex list of S - v, and together with the class witness colouring of L it is a proper 4-colouring of L ∪ (S - v)', 'leaks': leaks}, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('enumerate'); e.add_argument('output'); e.add_argument('--cnf-dir', required=True)
    e.add_argument('--cadical'); e.add_argument('--drat-trim'); e.set_defaults(func=cmd_enumerate)
    l = sub.add_parser('leaks'); l.add_argument('interface'); l.add_argument('output'); l.set_defaults(func=cmd_leaks)
    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
