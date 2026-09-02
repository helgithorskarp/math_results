#!/usr/bin/env python3
"""Independent checker for interface_L.json (and optionally s_vertex_leaks.json).

Solver-free part (needs only SymPy through ../hadwiger_nelson_parts509_criticality/parts509.py):
  * rebuilds the 509-point graph with exact arithmetic and the L/S decomposition;
  * checks the listed cross edges, interface and radius labels;
  * checks that every witness is a proper 4-colouring of L with the origin
    coloured 0, that its interface restriction canonicalises to the listed class,
    that the 20 classes are distinct, and that every class satisfies the stated
    invariants (one auxiliary triple monochromatic in colour 0, the other rainbow;
    the 12 reference vertices use at most two colours, one at least 8 times);
  * if s_vertex_leaks.json is given, checks every leak witness as a proper
    4-colouring of L ∪ (S - v) whose restriction to L is the class witness.

Solver part (python-sat, CaDiCaL 1.9.5; skipped with --no-solver):
  * completeness: L's 4-colouring CNF with the origin pinned and all 120 permuted
    class blockers is unsatisfiable;
  * blocking: for each class, S has no proper 4-colouring compatible with it;
  * if s_vertex_leaks.json is given, for each v and each class NOT listed, S - v
    has no compatible colouring.
"""
from __future__ import annotations
import argparse, importlib.util, itertools, json, sys
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('interface')
    ap.add_argument('--leaks')
    ap.add_argument('--no-solver', action='store_true')
    args = ap.parse_args()
    data = json.loads(Path(args.interface).read_text())
    parts = load_parts()
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    assert len(points) == 509 and len(edges) == 2442
    assert parts.file_sha256(BASE / 'parts509.vtx') == data['source_vtx_sha256']

    def has5(p):
        return any(p[j][i] != 0 for j in (0, 1) for i in (2, 3, 6, 7))
    L = [i for i in range(509) if not has5(points[i])]
    S = [i for i in range(509) if has5(points[i])]
    assert L == list(range(374)) and S == list(range(374, 509))
    assert points[0] == (parts.ZERO, parts.ZERO)
    Lset = set(L)
    cross = sorted((a, b) if a in Lset else (b, a) for a, b in edges if (a in Lset) != (b in Lset))
    assert cross == [tuple(e) for e in data['cross_edges_L_S']]
    IL = sorted({l for l, s in cross})
    assert IL == data['interface_L'] and len(IL) == 19
    IL_nz = [v for v in IL if v != 0]
    assert IL_nz == data['interface_L_nonorigin']
    assert sorted({s for l, s in cross}) == data['interface_S']
    LE = [(a, b) for a, b in edges if a in Lset and b in Lset]
    SE = [(a, b) for a, b in edges if a not in Lset and b not in Lset]
    assert len(LE) == 1860 and len(SE) == 552
    # radius labels, exact
    from fractions import Fraction
    lab = {}
    for v in IL:
        r2 = parts.f_add(parts.f_sq(points[v][0]), parts.f_sq(points[v][1]))
        coeff = {i: r2[i] for i in range(8) if r2[i] != 0}
        if not coeff:
            lab[v] = 'origin'
        elif coeff == {0: Fraction(4)}:
            lab[v] = 'reference'
        elif coeff == {0: Fraction(17, 6), 5: Fraction(-1, 6)}:
            lab[v] = 'aux_inner'
        elif coeff == {0: Fraction(17, 6), 5: Fraction(1, 6)}:
            lab[v] = 'aux_outer'
        else:
            raise AssertionError(f'unexpected radius for {v}: {coeff}')
    assert lab == {int(k): v for k, v in data['interface_labels'].items()}
    assert [lab[v] for v in IL_nz].count('reference') == 12
    # cross-edge geometry: 12 origin-S, 6 auxiliary (inner-outer), 12 reference-reference
    kinds = {}
    for l, s in cross:
        kinds[lab[l]] = kinds.get(lab[l], 0) + 1
    assert kinds == {'origin': 12, 'aux_inner': 3, 'aux_outer': 3, 'reference': 12}, kinds

    rows = data['classes']
    assert len(rows) == data['class_count'] == 20
    classes = set()
    for row in rows:
        col = [int(ch) for ch in row['witness_colouring_L']]
        assert len(col) == 374 and col[0] == 0
        for a, b in LE:
            assert col[a] != col[b], 'witness is not a proper colouring of L'
        key = tuple(col[v] for v in IL_nz)
        assert ''.join(map(str, key)) == row['witness_interface']
        canon = min(tuple(p[c] for c in key) for p in PERMS)
        assert ''.join(map(str, canon)) == row['class']
        classes.add(row['class'])
        ai = ''.join(str(col[v]) for v in IL_nz if lab[v] == 'aux_inner')
        ao = ''.join(str(col[v]) for v in IL_nz if lab[v] == 'aux_outer')
        assert ai == row['aux_inner'] and ao == row['aux_outer']
        assert (ai == '000') != (ao == '000'), 'exactly one auxiliary triple is monochromatic 0'
        other = ao if ai == '000' else ai
        assert len(set(other)) == 3, 'the other auxiliary triple is rainbow'
        ref = [col[v] for v in IL_nz if lab[v] == 'reference']
        mult = sorted((ref.count(c) for c in set(ref)), reverse=True)
        assert mult == row['reference_multiplicities'] and mult in ([12], [8, 4]), mult
    assert len(classes) == 20
    print('solver-free checks: 20 distinct classes, witnesses proper, invariants hold')

    leaks = None
    if args.leaks:
        leaks = json.loads(Path(args.leaks).read_text())['leaks']
        assert sorted(int(k) for k in leaks) == S
        n_wit = 0
        for v_str, entries in leaks.items():
            v = int(v_str)
            verts = sorted(set(L) | (set(S) - {v}))
            vs = set(verts)
            Sverts = [u for u in verts if u >= 374]
            for e in entries:
                w = e['witness_colouring_S_minus_v']
                assert len(w) == len(Sverts)
                wit = rows[e['class_index']]['witness_colouring_L']
                col = {u: int(wit[u]) for u in L}
                col.update({u: int(ch) for u, ch in zip(Sverts, w)})
                for a, b in edges:
                    if a in vs and b in vs:
                        assert col[a] != col[b]
                n_wit += 1
        print(f'leak witnesses checked: {n_wit} (solver-free)')

    if args.no_solver:
        print('solver checks skipped')
        return
    from pysat.solvers import Solver
    idx = {v: i for i, v in enumerate(L)}
    var = lambda v, c: idx[v] * K + c + 1
    cl = [[var(v, c) for c in range(K)] for v in L]
    for a, b in LE:
        for c in range(K):
            cl.append([-var(a, c), -var(b, c)])
    cl.append([var(0, 0)])
    for row in rows:
        col = [int(ch) for ch in row['witness_colouring_L']]
        for p in PERMS:
            cl.append([-var(v, p[col[v]]) for v in IL_nz])
    with Solver(name='cadical195', bootstrap_with=cl) as s:
        assert not s.solve(), 'completeness failed: an unlisted interface colouring exists'
    print('solver check: the 20 classes are complete (UNSAT)')
    sidx = {v: i for i, v in enumerate(S)}
    svar = lambda v, c: sidx[v] * K + c + 1
    base = [[svar(v, c) for c in range(K)] for v in S]
    for a, b in SE:
        for c in range(K):
            base.append([-svar(a, c), -svar(b, c)])
    for ci, row in enumerate(rows):
        col = row['witness_colouring_L']
        units = [[-svar(s, int(col[l]))] for l, s in cross]
        with Solver(name='cadical195', bootstrap_with=base + units) as s:
            assert not s.solve(), f'S admits a colouring compatible with class {ci}'
    print('solver check: S blocks all 20 classes (UNSAT each)')
    if leaks is not None:
        m = len(S)
        act = lambda v: m * K + sidx[v] + 1
        cl2 = [[-act(v)] + [svar(v, c) for c in range(K)] for v in S]
        for a, b in SE:
            for c in range(K):
                cl2.append([-act(a), -act(b), -svar(a, c), -svar(b, c)])
        n_unsat = 0
        with Solver(name='cadical195', bootstrap_with=cl2) as s:
            for v in S:
                listed = {e['class_index'] for e in leaks[str(v)]}
                for ci, row in enumerate(rows):
                    if ci in listed:
                        continue
                    col = row['witness_colouring_L']
                    assum = [act(u) if u != v else -act(u) for u in S] + [-svar(t, int(col[l])) for l, t in cross if t != v]
                    assert not s.solve(assumptions=assum), f'S - {v} leaks class {ci} but it is not listed'
                    n_unsat += 1
        print(f'solver check: leak lists are complete ({n_unsat} UNSAT calls)')
    print('all_checks=true')


if __name__ == '__main__':
    main()
