#!/usr/bin/env python3
"""Independent replay of the triple-closure coverage for one or more vertices.

Different implementation from the generator: free masks from neighbour lists
(pure Python), alive/extendability bitsets as Python ints, complete enumeration
of uncovered triples with numpy boolean matrices, exact list-colouring check
for triples with internal edges.  Every uncovered triple must be declared
(explicitly, or by implication through a swap point / declared pair).

Usage: triple_verify.py RESULTS_DIR [u ...]            (scratch results, default: all present)
       triple_verify.py triple_certificate.json [u ...]  (rows and declared triples taken from the certificate)
Prints per-vertex summary and a global summary; exit code 1 on failure.
"""
from __future__ import annotations
import base64, hashlib, importlib.util, json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
N, K = 509, 4


def load():
    spec = importlib.util.spec_from_file_location('pc', PAIRDIR / 'pair_closure.py')
    pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
    parts = pc.load_parts()
    points, edges, rows, fams, qnb, qq_edges = pc.load_all()
    cert = json.loads((PAIRDIR / 'pair_certificate.json').read_text())
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    pf = [[] for _ in range(N)]
    pos, RB = 0, (N - 1) // 4
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            raw = packed[pos:pos + RB]; pos += RB
            vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(vals)
            row = [-1 if v == u else next(it) for v in range(N)]
            parts.validate_coloring(N, edges, row, K, u)
            pf[u].append(row)
    assert pos == len(packed)
    declared_pairs = [set(tuple(sorted(p)) for p in lst) for lst in cert['declared_pairs']]
    swaps = json.loads((PAIRDIR / 'swaps.json').read_text())
    return parts, edges, rows, fams, pf, declared_pairs, swaps, qnb, qq_edges


def verify_u(u, res, ctx):
    parts, edges, rows, fams, pf, declared_pairs, swaps, qnb, qq_edges = ctx
    nq = len(qnb)
    qadj = [set() for _ in range(nq)]
    for a, b in qq_edges:
        qadj[a].add(b); qadj[b].add(a)
    qqset = set(qq_edges)
    lib = [rows[u]] + list(fams[u]) + list(pf[u])
    for s in res['new_rows']:
        row = [-1 if ch == '-' else int(ch) for ch in s]
        assert len(row) == N and row[u] == -1 and all(c >= 0 for i, c in enumerate(row) if i != u)
        parts.validate_coloring(N, edges, row, K, u)
        lib.append(row)
    m = len(lib)
    # free masks from neighbour lists (pure Python)
    fm = np.zeros((m, nq), dtype=np.int64)
    for j, col in enumerate(lib):
        for q in range(nq):
            used = 0
            for w in qnb[q]:
                if w != u:
                    used |= 1 << col[w]
            fm[j, q] = 15 - used
    alive = fm != 0                                   # (m, nq)
    swap_pts = {q for q, uu in swaps if uu == u}
    dpairs = declared_pairs[u]
    decl = {tuple(t[:3]): t[3] for t in res['declared_triples']}
    assert set(decl) == {tuple(sorted(t)) for t in decl}
    excl = np.zeros(nq, dtype=bool)
    for q in swap_pts:
        excl[q] = True
    # --- zero-edge triples: complete enumeration with boolean matrices
    QA = np.zeros((nq, nq), dtype=bool)
    for a, b in qq_edges:
        QA[a, b] = QA[b, a] = True
    uncovered = []
    Af = alive.astype(np.float32)
    for i in range(nq):
        if excl[i]:
            continue
        both = alive[:, i][:, None] & alive           # (m, nq): colourings where i and j alive
        # for each j, third point k uncovered iff no colouring has i, j, k all alive
        # compute count matrix C[j,k] = sum_c both[c,j] & alive[c,k]
        C = both.T.astype(np.float32) @ Af  # (nq, nq), exact counts < 2^24
        bad = (C == 0)
        js, ks = np.nonzero(np.triu(bad, 1))
        for j, k in zip(js, ks):
            j, k = int(j), int(k)
            if j <= i or k <= j or excl[j] or excl[k]:
                continue
            if QA[i, j] or QA[i, k] or QA[j, k]:
                continue                               # handled below
            uncovered.append((i, j, k))
    # --- triples with >= 1 internal edge: exact list-colouring check per colouring
    aliveint = [0] * nq
    for q in range(nq):
        v = 0
        for j in range(m):
            if alive[j, q]:
                v |= 1 << j
        aliveint[q] = v
    fmcols = fm

    def ext_exact(t):
        internal = [(x, y) for x in range(3) for y in range(x + 1, 3) if (min(t[x], t[y]), max(t[x], t[y])) in qqset]
        for j in range(m):
            f = [fmcols[j, q] for q in t]
            found = False
            for c0 in range(K):
                if not f[0] >> c0 & 1: continue
                for c1 in range(K):
                    if not f[1] >> c1 & 1: continue
                    if (0, 1) in internal and c1 == c0: continue
                    for c2 in range(K):
                        if not f[2] >> c2 & 1: continue
                        if (0, 2) in internal and c2 == c0: continue
                        if (1, 2) in internal and c2 == c1: continue
                        found = True; break
                    if found: break
                if found: break
            if found:
                return True
        return False
    n_edge_triples = 0
    for (a, b) in qq_edges:
        if excl[a] or excl[b]:
            continue
        # edge-extendability bitset over colourings
        E = 0
        for j in range(m):
            fa, fb = fm[j, a], fm[j, b]
            if fa and fb and not (fa == fb and fa in (1, 2, 4, 8)):
                E |= 1 << j
        for k in range(nq):
            if k == a or k == b or excl[k]:
                continue
            n_edge_triples += 1
            if k in qadj[a] or k in qadj[b]:
                t = tuple(sorted((a, b, k)))
                if t[0] == a and t[1] == b or True:
                    pass
                # >=2 internal edges: exact check (dedupe: only when (a,b) is the lexicographically first edge of t)
                edges_in_t = sorted((min(x, y), max(x, y)) for x in t for y in t if x < y and (min(x, y), max(x, y)) in qqset)
                if edges_in_t[0] != (min(a, b), max(a, b)):
                    continue
                if not ext_exact(t):
                    uncovered.append(t)
            else:
                if aliveint[k] & E == 0:
                    uncovered.append(tuple(sorted((a, b, k))))
    # classify uncovered triples
    n_implied = n_explicit = 0
    bad = []
    for t in set(uncovered):
        if any((min(x, y), max(x, y)) in dpairs for x in t for y in t if x < y):
            n_implied += 1
        elif t in decl:
            n_explicit += 1
        else:
            bad.append(t)
    # every explicitly declared triple must indeed be uncovered (sanity, not needed for soundness)
    unc_set = set(uncovered)
    stale = [t for t in decl if t not in unc_set]
    return {'u': u, 'library': m, 'uncovered_total': len(set(uncovered)), 'implied_by_pairs': n_implied,
            'explicit': n_explicit, 'undeclared_uncovered': len(bad), 'stale_declarations': len(stale),
            'ok': len(bad) == 0}


def results_from_certificate(cert_path):
    """Per-vertex result dicts (new_rows as strings, declared triples) from the packed certificate."""
    cert = json.loads(Path(cert_path).read_text())
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    out, pos, RB = {}, 0, (N - 1) // 4
    for u, size in enumerate(cert['family_sizes']):
        rows = []
        for _ in range(size):
            raw = packed[pos:pos + RB]; pos += RB
            vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(vals)
            rows.append(''.join('-' if v == u else str(next(it)) for v in range(N)))
        out[u] = {'u': u, 'new_rows': rows, 'declared_triples': [list(t) + ['declared'] for t in cert['declared_triples'][u]]}
    assert pos == len(packed)
    return out


def main():
    src = Path(sys.argv[1])
    from_cert = src.is_file()
    if from_cert:
        allres = results_from_certificate(src)
        us = [int(x) for x in sys.argv[2:]] or sorted(allres)
    else:
        rdir = src
        us = [int(x) for x in sys.argv[2:]] or sorted(int(p.stem[2:]) for p in rdir.glob('u_*.json'))
    ctx = load()
    t0 = time.time()
    allok = True
    for u in us:
        res = allres[u] if from_cert else json.loads((rdir / f'u_{u:03d}.json').read_text())
        r = verify_u(u, res, ctx)
        allok &= r['ok']
        print(json.dumps(r), f'{time.time()-t0:.0f}s', flush=True)
    print('all_ok', allok)
    sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()
