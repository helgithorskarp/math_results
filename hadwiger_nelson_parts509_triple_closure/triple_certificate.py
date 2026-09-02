#!/usr/bin/env python3
"""Certificate builder / solver-free verifier for the delete-4-add-3 closure of
the Parts-509 graph.

Layer (i): triples of Q3 points.  Coverage replay per deleted vertex u
(vectorised bitsets over the witness library): a triple A of Q3 points is
covered by a colouring c of G - u iff c extends to A (list colouring with the
internal unit edges of A).  Every uncovered triple must be declared:
explicitly, or by containing a swap point of u or a declared pair of u
(sibling certificates).  Layer (ii)/(iii): clusters built on the K-rational
two-neighbour points Q2K; layer (iii-b, non-K): rigorous float screen.

Commands:
  check RESULTS_DIR [--workers W] [--vertices a,b,..]        replay scratch results
  build RESULTS_DIR Q2K_EXTRA EXTRA_U DIRECT OUT              pack the certificate
  verify CERT [--workers W] [--skip-nonk]                     full solver-free verification
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, itertools, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np

HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND
               if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND
               if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
BASEDIR = next(p / 'hadwiger_nelson_parts509_criticality' for p in _CAND
               if (p / 'hadwiger_nelson_parts509_criticality' / 'parts509.py').exists())
sys.path.insert(0, str(SWAPDIR))      # kfield.py, udg.py of the sibling
N, K = 509, 4
RB = (N - 1) // 4
POP8 = np.array([bin(i).count('1') for i in range(256)], dtype=np.int64)
TOL = 1e-7
CTX = {}


def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}', flush=True)


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------ row packing

def pack_row(coloring, u):
    vals = [coloring[v] for v in range(N) if v != u]
    assert len(vals) == N - 1 and all(0 <= c < K for c in vals)
    out = bytearray()
    for i in range(0, len(vals), 4):
        b = 0
        for s, c in enumerate(vals[i:i + 4]):
            b |= c << (2 * s)
        out.append(b)
    assert len(out) == RB
    return bytes(out)


def unpack_row(raw, u):
    vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
    it = iter(vals)
    return [-1 if v == u else next(it) for v in range(N)]


def row_to_str(row):
    return ''.join('-' if c < 0 else str(c) for c in row)


def row_from_str(s):
    return [-1 if ch == '-' else int(ch) for ch in s]


# ------------------------------------------------------------ context

def load_context(with_incidences=False):
    spec = importlib.util.spec_from_file_location('pc_mod', PAIRDIR / 'pair_closure.py')
    pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
    parts = pc.load_parts()
    points, edges, rows, fams, qnb, qq_edges = pc.load_all()
    cert = json.loads((PAIRDIR / 'pair_certificate.json').read_text())
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    pf = [[] for _ in range(N)]
    pos = 0
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            row = unpack_row(packed[pos:pos + RB], u); pos += RB
            parts.validate_coloring(N, edges, row, K, u)
            pf[u].append(row)
    assert pos == len(packed)
    declared_pairs = [set(tuple(sorted(p)) for p in lst) for lst in cert['declared_pairs']]
    swaps = json.loads((PAIRDIR / 'swaps.json').read_text())
    nq = len(qnb)
    maxd = max(len(nb) for nb in qnb)
    nbarr = np.full((nq, maxd), -1, dtype=np.int64)
    for i, nb in enumerate(qnb):
        nbarr[i, :len(nb)] = nb
    QA = np.zeros((nq, nq), dtype=bool)
    for a, b in qq_edges:
        QA[a, b] = QA[b, a] = True
    qadj = [set() for _ in range(nq)]
    for a, b in qq_edges:
        qadj[a].add(b); qadj[b].add(a)
    t2 = set()
    for b in range(nq):
        nb = sorted(qadj[b])
        for i in range(len(nb)):
            for j in range(i + 1, len(nb)):
                t2.add(tuple(sorted((nb[i], b, nb[j]))))
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    CTX.update(parts=parts, points=points, edges=edges, adj=adj, rows=rows, fams=fams, pf=pf,
               declared_pairs=declared_pairs, swaps=swaps, qnb=qnb, qq_edges=qq_edges, qqset=set(qq_edges),
               nbarr=nbarr, QA=QA, qadj=qadj, t2=sorted(t2), nq=nq, pair_cert=cert)


def free_masks(coloring, u):
    nbarr = CTX['nbarr']
    col = np.array(list(coloring) + [-1], dtype=np.int64)
    c = col[nbarr]
    c = np.where(nbarr == u, -1, c)
    used = np.zeros(len(nbarr), dtype=np.int64)
    for k in range(K):
        used |= (c == k).any(axis=1).astype(np.int64) << k
    return 15 - used


def list_colourable(fms, internal):
    n = len(fms)
    assigned = []

    def rec(i):
        if i == n:
            return True
        for c in range(K):
            if not (fms[i] >> c & 1):
                continue
            if any(assigned[j] == c for (j, k) in internal if k == i):
                continue
            assigned.append(c)
            if rec(i + 1):
                return True
            assigned.pop()
        return False
    return rec(0)


def extends_nbrs(coloring, deleted, nbrs, internal):
    """Colouring of G - deleted extends to points with the given V-neighbour lists."""
    fms = []
    for nb in nbrs:
        used = 0
        for w in nb:
            if w not in deleted:
                used |= 1 << coloring[w]
        fms.append(15 - used)
    return list_colourable(fms, internal)


# ------------------------------------------------------------ layer (i) replay

def replay_u(u, new_rows, declared_triples):
    parts, edges, qnb, nq = CTX['parts'], CTX['edges'], CTX['qnb'], CTX['nq']
    QA, qq_edges, t2 = CTX['QA'], CTX['qq_edges'], CTX['t2']
    lib = [CTX['rows'][u]] + list(CTX['fams'][u]) + list(CTX['pf'][u])
    for row in new_rows:
        assert len(row) == N and row[u] == -1
        parts.validate_coloring(N, edges, row, K, u)
        lib.append(row)
    m = len(lib)
    W = (m + 63) // 64
    fm = np.array([free_masks(col, u) for col in lib], dtype=np.int64)
    alive_b = fm != 0
    alive = np.zeros((nq, W), dtype=np.uint64)
    for j in range(m):
        w, bit = divmod(j, 64)
        alive[alive_b[j], w] |= np.uint64(1) << np.uint64(bit)
    qa = np.array([a for a, b in qq_edges], dtype=np.int64)
    qb = np.array([b for a, b in qq_edges], dtype=np.int64)
    eok = np.zeros((len(qq_edges), W), dtype=np.uint64)
    for j in range(m):
        fa, fb = fm[j, qa], fm[j, qb]
        ok = (fa != 0) & (fb != 0) & ~((fa == fb) & np.isin(fa, (1, 2, 4, 8)))
        w, bit = divmod(j, 64)
        eok[ok, w] |= np.uint64(1) << np.uint64(bit)
    swap_pts = {q for q, uu in CTX['swaps'] if uu == u}
    excl = np.zeros(nq, dtype=bool)
    for q in swap_pts:
        excl[q] = True
    dpairs = CTX['declared_pairs'][u]
    decl = set(tuple(t) for t in declared_triples)
    uncovered = set()
    dead_cnt = m - POP8[alive.view(np.uint8)].reshape(nq, -1).sum(axis=1)
    dead_cnt[excl] = -1
    maxdead = int(dead_cnt.max())
    for i in range(nq):
        if excl[i]:
            continue
        R = alive & alive[i]
        pc = POP8[R.view(np.uint8)].reshape(nq, -1).sum(axis=1)
        cand = np.nonzero((pc <= maxdead) & ~excl & ~QA[i])[0]
        for j in cand:
            j = int(j)
            if j <= i:
                continue
            if pc[j] == 0:
                assert (i, j) in dpairs, f'uncovered pair {(i, j)} not declared for u={u}'
                continue
            z = ~((alive & R[j]).any(axis=1)) & ~QA[i] & ~QA[j] & ~excl
            z[:j + 1] = False
            for k in np.nonzero(z)[0]:
                uncovered.add((i, j, int(k)))
    for ei, (a, b) in enumerate(qq_edges):
        if excl[a] or excl[b]:
            continue
        E = eok[ei]
        if not E.any():
            assert (a, b) in dpairs, f'uncovered edge pair {(a, b)} not declared for u={u}'
            continue
        z = ~((alive & E).any(axis=1)) & ~QA[a] & ~QA[b] & ~excl
        z[a] = False; z[b] = False
        for k in np.nonzero(z)[0]:
            uncovered.add(tuple(sorted((a, b, int(k)))))
    qqset = CTX['qqset']
    for t in t2:
        if any(excl[q] for q in t):
            continue
        internal = [(x, y) for x in range(3) for y in range(x + 1, 3) if (t[x], t[y]) in qqset]
        if not any(list_colourable([int(fm[j, q]) for q in t], internal) for j in range(m)):
            uncovered.add(t)
    n_impl = n_expl = 0
    bad = []
    for t in uncovered:
        if any((t[x], t[y]) in dpairs for x in range(3) for y in range(x + 1, 3)):
            n_impl += 1
        elif t in decl:
            n_expl += 1
        else:
            bad.append(t)
    stale = [t for t in decl if t not in uncovered]
    return {'u': u, 'library': m, 'uncovered': len(uncovered), 'implied_by_pairs': n_impl,
            'explicit': n_expl, 'undeclared': bad[:20], 'n_undeclared': len(bad), 'stale': len(stale)}


def _check_one(args):
    u, rdir = args
    r = json.loads((Path(rdir) / f'u_{u:03d}.json').read_text())
    return replay_u(u, [row_from_str(s) for s in r['new_rows']], [t[:3] for t in r['declared_triples']])


def _verify_one(args):
    u, new_rows, decl = args
    return replay_u(u, new_rows, decl)


def aggregate_U(explicit_by_u, declared_pairs, swaps, nq):
    """U(A) for all triples with a contribution beyond swap points."""
    from collections import defaultdict
    U = defaultdict(set)
    swap_u = defaultdict(set)
    for q, u in swaps:
        swap_u[q].add(u)
    for u in range(N):
        for t in explicit_by_u[u]:
            U[tuple(t)].add(u)
        sp = {q for q, uu in swaps if uu == u}
        for (a, b) in declared_pairs[u]:
            if a in sp or b in sp:
                continue
            for q in range(nq):
                if q != a and q != b:
                    U[tuple(sorted((a, b, q)))].add(u)
    full = {}
    for A, us in U.items():
        s = set(us)
        for q in A:
            s |= swap_u.get(q, set())
        full[A] = s
    return full


# ------------------------------------------------------------ Q2K layer helpers

def unit_pairs_float(P, Q=None, tol=TOL):
    same = Q is None
    if same:
        Q = P
    h = 0.05
    cellsP = {}
    for idx, (x, y) in enumerate(P):
        cellsP.setdefault((int(np.floor(x / h)), int(np.floor(y / h))), []).append(idx)
    cellsQ = cellsP if same else {}
    if not same:
        for idx, (x, y) in enumerate(Q):
            cellsQ.setdefault((int(np.floor(x / h)), int(np.floor(y / h))), []).append(idx)
    R = int(np.ceil((1 + tol) / h)) + 1
    offsets = []
    for ox in range(-R, R + 1):
        for oy in range(-R, R + 1):
            mnx = max(0, abs(ox) - 1) * h; mny = max(0, abs(oy) - 1) * h
            mxx = (abs(ox) + 1) * h; mxy = (abs(oy) + 1) * h
            if np.hypot(mnx, mny) <= 1 + tol and np.hypot(mxx, mxy) >= 1 - tol:
                offsets.append((ox, oy))
    out = []
    for (cx, cy), ids in cellsP.items():
        A = P[ids]
        for ox, oy in offsets:
            jds = cellsQ.get((cx + ox, cy + oy))
            if not jds:
                continue
            B = Q[jds]
            d = np.hypot(A[:, None, 0] - B[None, :, 0], A[:, None, 1] - B[None, :, 1])
            ii, jj = np.nonzero(np.abs(d - 1) < tol)
            for a, b in zip(ii, jj):
                i, j = ids[a], jds[b]
                if same and i >= j:
                    continue
                out.append((int(i), int(j)))
    return sorted(set(out))


def build_clusters(q2k_nbrs, q2k_q3_adj, q2k_q2k_adj, q3nb, qqset):
    """Deterministic list of clusters (ii), (iii-a), (iii-b-K)."""
    nb3, nb2 = {}, {}
    for i, j in q2k_q3_adj:
        nb3.setdefault(i, []).append(j)
    for i, j in q2k_q2k_adj:
        nb2.setdefault(i, []).append(j); nb2.setdefault(j, []).append(i)
    cls = []
    for p in sorted(nb3):
        lst = sorted(nb3[p])
        for x in range(len(lst)):
            for y in range(x + 1, len(lst)):
                a2, a3 = lst[x], lst[y]
                edges = [(0, 1), (0, 2)] + ([(1, 2)] if (a2, a3) in qqset else [])
                cls.append({'id': f'ii:{p}:{a2}:{a3}', 'nbrs': [q2k_nbrs[p], q3nb[a2], q3nb[a3]], 'edges': edges})
    adj22 = set(q2k_q2k_adj)
    for (p1, p2) in sorted(adj22):
        for a3 in sorted(set(nb3.get(p1, [])) & set(nb3.get(p2, []))):
            cls.append({'id': f'iiia:{p1}:{p2}:{a3}', 'nbrs': [q2k_nbrs[p1], q2k_nbrs[p2], q3nb[a3]],
                        'edges': [(0, 1), (0, 2), (1, 2)]})
    for (p1, p2) in sorted(adj22):
        for p3 in sorted(nb2.get(p1, [])):
            if p3 > p2 and (p2, p3) in adj22:
                cls.append({'id': f'iiib:{p1}:{p2}:{p3}', 'nbrs': [q2k_nbrs[p] for p in (p1, p2, p3)],
                            'edges': [(0, 1), (0, 2), (1, 2)]})
    return cls


def _cluster_check(args):
    ci, cl, Udecl, fresh_rows = args
    parts, edges = CTX['parts'], CTX['edges']
    bad = []
    for u in range(N):
        lib = [CTX['rows'][u]] + list(CTX['fams'][u]) + list(CTX['pf'][u]) + list(CTX['trows'][u])
        extra = fresh_rows.get(u, [])
        for row in extra:
            parts.validate_coloring(N, edges, row, K, u)
        if u in Udecl:
            continue
        if any(extends_nbrs(col, {u}, cl['nbrs'], cl['edges']) for col in itertools.chain(extra, lib)):
            continue
        bad.append(u)
    return ci, bad


def nonk_points(points, workers):
    import kfield as kf, mpmath as mp
    mp.mp.dps = 50
    global _NK
    _NK = {'points': points, 'kf': kf, 'mp': mp, 'SQ': {p: mp.sqrt(p) for p in kf.PRIMES}}
    out = []
    with Pool(workers, initializer=_nk_init, initargs=(points,)) as pool:
        for i, rows in pool.imap_unordered(_nk_row, range(len(points)), chunksize=4):
            out.extend(rows)
    return out


_NK = {}


def _nk_init(points):
    import kfield as kf, mpmath as mp
    mp.mp.dps = 50
    _NK.update(points=points, kf=kf, mp=mp, SQ={p: mp.sqrt(p) for p in kf.PRIMES})


def _to_mp(x):
    kf, mp, SQ = _NK['kf'], _NK['mp'], _NK['SQ']
    total = mp.mpf(0)
    for mask, a in enumerate(x):
        if not a:
            continue
        v = mp.mpf(a.numerator) / a.denominator
        for bit in range(3):
            if (mask >> bit) & 1:
                v *= SQ[kf.PRIMES[bit]]
        total += v
    return total


def _nk_row(i):
    kf, mp = _NK['kf'], _NK['mp']
    pts = _NK['points']
    Kk = 3
    FOUR = kf.const(Kk, 4)
    xi, yi = pts[i]
    out = []
    for j in range(i + 1, len(pts)):
        xj, yj = pts[j]
        dx = kf.sub(xi, xj); dy = kf.sub(yi, yj)
        d2 = kf.add(kf.mul(dx, dx, Kk), kf.mul(dy, dy, Kk))
        num = kf.sub(FOUR, d2)
        if kf.sign(num) <= 0:
            continue
        rho2 = kf.mul(num, kf.inv(kf.scale(d2, 4), Kk), Kk)
        if kf.field_sqrt(rho2, Kk) is not None:
            continue
        r = mp.sqrt(_to_mp(rho2))
        mx = (_to_mp(xi) + _to_mp(xj)) / 2; my = (_to_mp(yi) + _to_mp(yj)) / 2
        wx = -_to_mp(dy) * r; wy = _to_mp(dx) * r
        for s in (1, -1):
            out.append((i, j, s, float(mx + s * wx), float(my + s * wy)))
    return i, out


# ------------------------------------------------------------ build

def canonical_nonk_clusters(raw_clusters):
    """Non-K triangle clusters in canonical order: labels (i, j, s) sorted inside each
    triangle, triangles sorted lexicographically."""
    out = []
    for cl in raw_clusters:
        labs = sorted(tuple(l) for l in cl['labels'])
        out.append({'id': cl['id'], 'labels': labs, 'nbrs': [[l[0], l[1]] for l in labs],
                    'edges': [(0, 1), (0, 2), (1, 2)]})
    out.sort(key=lambda c: c['labels'])
    return out


def command_build(results_dir, q2k_extra_path, extra_u_path, direct_path, out_path, nonk_exact_path=None, nonk_u_path=None):
    load_context()
    parts, edges = CTX['parts'], CTX['edges']
    rdir = Path(results_dir)
    fam_sizes, blob, declared = [], bytearray(), []
    stats = {'witnesses': 0, 'unsat': 0, 'budget': 0, 'calls': 0}
    for u in range(N):
        r = json.loads((rdir / f'u_{u:03d}.json').read_text())
        assert r['u'] == u
        rows = [row_from_str(s) for s in r['new_rows']]
        for row in rows:
            parts.validate_coloring(N, edges, row, K, u)
            blob += pack_row(row, u)
        fam_sizes.append(len(rows))
        declared.append(sorted(t[:3] for t in r['declared_triples']))
        for k in ('witnesses', 'unsat', 'budget'):
            stats[k] += r[k]
        stats['calls'] += r['sat_calls']
    ex = json.loads(Path(q2k_extra_path).read_text())
    eu = json.loads(Path(extra_u_path).read_text())
    res_by_id = {r['id']: r for r in eu['results']}
    # cluster ids in build order of build_clusters (verify recomputes them)
    q2k_nbrs = [p['neighbors'] for p in ex['q2k']]
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    q3nb = [list(r['neighbors']) for r in comp['points']]
    cls = build_clusters(q2k_nbrs, [tuple(e) for e in ex['adj_q2k_q3']], [tuple(e) for e in ex['adj_q2k_q2k']], q3nb, CTX['qqset'])
    assert len(cls) == len(eu['results']), (len(cls), len(eu['results']))
    cl_U, fresh_idx, fresh_blob = [], [], bytearray()
    for ci, cl in enumerate(cls):
        r = res_by_id[cl['id']]
        cl_U.append(sorted(r['U']))
        for fr in r['new_rows']:
            row = row_from_str(fr['row'])
            parts.validate_coloring(N, edges, row, K, fr['u'])
            fresh_idx.append([ci, fr['u']])
            fresh_blob += pack_row(row, fr['u'])
    nk_U, nk_fresh_idx, nk_fresh_blob, nk_info = [], [], bytearray(), {}
    if nonk_exact_path:
        nke = json.loads(Path(nonk_exact_path).read_text())
        nku = json.loads(Path(nonk_u_path).read_text())
        nk_res = {r['id']: r for r in nku['results']}
        nk_cls = canonical_nonk_clusters(nke['clusters'])
        assert len(nk_cls) == len(nku['results']) == nke['triangles']
        for ci, cl in enumerate(nk_cls):
            r = nk_res[cl['id']]
            nk_U.append(sorted(r['U']))
            for fr in r['new_rows']:
                row = row_from_str(fr['row'])
                parts.validate_coloring(N, edges, row, K, fr['u'])
                nk_fresh_idx.append([ci, fr['u']])
                nk_fresh_blob += pack_row(row, fr['u'])
        nk_info = {'exact_unit_pairs': len(nke['unit_pairs']), 'cases': nke['cases'], 'triangles': nke['triangles'],
                   'k_point_candidates_unit': nke['k_point_candidates_unit']}
    direct = []
    if direct_path and Path(direct_path).exists():
        for rec in json.loads(Path(direct_path).read_text()):
            assert rec['status'] == 'sat', rec
            direct.append({'id': rec['id'], 'D': rec['D'], 'row': rec['row'], 'point_colours': rec['point_colours']})
    cert = {
        'format': 'parts509-triple-closure-v1',
        'claim': 'For every 4-set D of Parts vertices and every 3 distinct points A of the plane, the strict '
                 'unit-distance graph on (V \\ D) u A is 4-colourable.',
        'layer1_stats': stats,
        'row_packing': 'one 127-byte row per colouring: 508 retained vertices in increasing order (deleted vertex omitted), 2 bits each, 4 per byte, low bits first',
        'family_sizes': fam_sizes,
        'family_rows_base64': base64.b64encode(bytes(blob)).decode(),
        'packed_rows_sha256': hashlib.sha256(bytes(blob)).hexdigest(),
        'declared_triples': declared,
        'q2k_points': [{'x': p['x'], 'y': p['y'], 'neighbors': p['neighbors']} for p in ex['q2k']],
        'q2k_q3_unit_pairs': ex['adj_q2k_q3'],
        'q2k_q2k_unit_pairs': ex['adj_q2k_q2k'],
        'cluster_count': len(cls),
        'cluster_U': cl_U,
        'cluster_fresh_index': fresh_idx,
        'cluster_fresh_rows_base64': base64.b64encode(bytes(fresh_blob)).decode(),
        'cluster_fresh_sha256': hashlib.sha256(bytes(fresh_blob)).hexdigest(),
        'nonk': dict({'points': ex['nonk_points'], 'unit_pair_candidates': len(ex['nonk_unit_pair_candidates']),
                      'candidate_triangles': len(ex['nonk_candidate_triangles']), 'tolerance': ex['tolerance'],
                      'k_point_candidates': len(ex['nonk_vs_q2k_candidates']) + len(ex['nonk_vs_q3_candidates'])}, **nk_info),
        'nonk_cluster_U': nk_U,
        'nonk_cluster_fresh_index': nk_fresh_idx,
        'nonk_cluster_fresh_rows_base64': base64.b64encode(bytes(nk_fresh_blob)).decode(),
        'nonk_cluster_fresh_sha256': hashlib.sha256(bytes(nk_fresh_blob)).hexdigest(),
        'direct_witnesses': direct,
        'base_certificate_sha256': file_sha256(BASEDIR / 'certificate.json'),
        'swap_certificate_sha256': file_sha256(SWAPDIR / 'swap_certificate.json'),
        'pair_certificate_sha256': file_sha256(PAIRDIR / 'pair_certificate.json'),
        'completion_points_sha256': file_sha256(SWAPDIR / 'completion_points.json'),
    }
    Path(out_path).write_text(json.dumps(cert))
    log(f'wrote {out_path}: {sum(fam_sizes)} rows, {sum(len(d) for d in declared)} explicit triples, '
        f'{len(cls)} Q2K clusters ({len(fresh_idx)} fresh rows), {len(nk_U)} non-K clusters ({len(nk_fresh_idx)} fresh rows), '
        f'{len(direct)} direct witnesses')


# ------------------------------------------------------------ verify

def command_verify(cert_path, workers=8, skip_nonk=False):
    t0 = time.time()
    cert = json.loads(Path(cert_path).read_text())
    assert cert['format'] == 'parts509-triple-closure-v1'
    checks = {}
    for key, path in (('base_certificate_sha256', BASEDIR / 'certificate.json'),
                      ('swap_certificate_sha256', SWAPDIR / 'swap_certificate.json'),
                      ('pair_certificate_sha256', PAIRDIR / 'pair_certificate.json'),
                      ('completion_points_sha256', SWAPDIR / 'completion_points.json')):
        checks[key] = file_sha256(path) == cert[key]
    load_context()
    parts, points, edges, qnb, qq_edges, nq = CTX['parts'], CTX['points'], CTX['edges'], CTX['qnb'], CTX['qq_edges'], CTX['nq']
    log(f'context loaded: {len(edges)} edges, {nq} Q3 points, {len(qq_edges)} Q3-Q3 unit pairs')
    # exact incidences of V u Q3 recomputed with integer arithmetic (sibling udg)
    import udg, kfield as kf
    qpts = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in json.loads((SWAPDIR / 'completion_points.json').read_text())['points']]
    allpts = list(points) + qpts
    ex_edges = udg.unit_edges(allpts, workers=workers)
    vv = sorted((a, b) for a, b in ex_edges if b < N)
    q3v = {}
    qq = []
    for a, b in ex_edges:
        if b >= N > a:
            q3v.setdefault(b - N, []).append(a)
        elif a >= N:
            qq.append((a - N, b - N))
    checks['exact_incidences'] = (vv == sorted(edges) and sorted(qq) == sorted(qq_edges)
                                  and all(tuple(sorted(q3v.get(i, []))) == tuple(qnb[i]) for i in range(nq)))
    log(f'exact incidences V u Q3 recomputed: {checks["exact_incidences"]}  ({time.time()-t0:.0f}s)')
    # unpack triple rows
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    checks['packed_rows_sha256'] = hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    trows = [[] for _ in range(N)]
    pos = 0
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            row = unpack_row(packed[pos:pos + RB], u); pos += RB
            parts.validate_coloring(N, edges, row, K, u)
            trows[u].append(row)
    checks['rows_consumed'] = pos == len(packed)
    CTX['trows'] = trows
    log(f'{sum(len(r) for r in trows)} triple rows decoded and validated')
    # layer (i) replay
    decl = [[tuple(t) for t in lst] for lst in cert['declared_triples']]
    tot = {'uncovered': 0, 'implied_by_pairs': 0, 'explicit': 0, 'n_undeclared': 0, 'stale': 0}
    ok_replay = True
    with Pool(workers, initializer=load_context) as pool:
        for r in pool.imap_unordered(_verify_one, [(u, trows[u], decl[u]) for u in range(N)], chunksize=1):
            for k in tot:
                tot[k] += r[k]
            ok_replay &= r['n_undeclared'] == 0
    checks['layer1_coverage'] = ok_replay
    log(f'layer (i) replay: {tot}  ok={ok_replay}  ({time.time()-t0:.0f}s)')
    # U(A) and direct witnesses for Q3 triples
    full = aggregate_U(decl, CTX['declared_pairs'], CTX['swaps'], nq)
    hist = {}
    for A, s in full.items():
        hist[len(s)] = hist.get(len(s), 0) + 1
    cands = {A: sorted(s) for A, s in full.items() if len(s) >= 4}
    direct = {}
    for rec in cert['direct_witnesses']:
        direct[(rec['id'], tuple(rec['D']))] = rec
    qqset = CTX['qqset']
    ok_direct = True
    n_direct = 0
    for A, U in cands.items():
        nbrs = [qnb[q] for q in A]
        internal = [(i, j) for i in range(3) for j in range(i + 1, 3) if (A[i], A[j]) in qqset]
        for D in itertools.combinations(U, 4):
            rec = direct.get(('q3:' + ':'.join(map(str, A)), D))
            ok_direct &= rec is not None and _check_direct(rec, D, nbrs, internal)
            n_direct += 1
    checks['q3_direct_witnesses'] = ok_direct
    log(f'|U(A)| histogram {dict(sorted(hist.items()))}; candidates {len(cands)}; direct tests {n_direct} ok={ok_direct}')
    # Q2K layer
    fresh = json.loads((SWAPDIR / 'completion_points.json').read_text())
    cp = udg.completion_points(points, edges, workers=workers, min_neighbors=2)
    enum2 = sorted(((tuple(r['x']), tuple(r['y'])), tuple(r['neighbors'])) for r in cp['points'] if len(r['neighbors']) == 2)
    cert2 = sorted(((tuple(p['x']), tuple(p['y'])), tuple(p['neighbors'])) for p in cert['q2k_points'])
    checks['q2k_enumeration'] = enum2 == cert2 and cp['q3_count'] == nq
    log(f'Q2K re-enumerated: {len(enum2)} points, matches certificate: {checks["q2k_enumeration"]}  ({time.time()-t0:.0f}s)')
    q2k = [(kf.from_strings(p['x']), kf.from_strings(p['y'])) for p in cert['q2k_points']]
    q2k_nbrs = [list(p['neighbors']) for p in cert['q2k_points']]
    P2 = np.array([[kf.to_float(q[0]), kf.to_float(q[1])] for q in q2k])
    P3 = np.array([[kf.to_float(q[0]), kf.to_float(q[1])] for q in qpts])
    ONE = kf.one(3)

    def d2(p, q):
        dx = kf.sub(p[0], q[0]); dy = kf.sub(p[1], q[1])
        return kf.add(kf.mul(dx, dx, 3), kf.mul(dy, dy, 3))
    adj23 = sorted((i, j) for i, j in unit_pairs_float(P2, P3) if d2(q2k[i], qpts[j]) == ONE)
    adj22 = sorted((i, j) for i, j in unit_pairs_float(P2) if d2(q2k[i], q2k[j]) == ONE)
    checks['q2k_incidences'] = adj23 == [tuple(e) for e in cert['q2k_q3_unit_pairs']] and adj22 == [tuple(e) for e in cert['q2k_q2k_unit_pairs']]
    log(f'Q2K incidences: Q3 {len(adj23)}, Q2K {len(adj22)}; match {checks["q2k_incidences"]}')
    q3nb = [list(nb) for nb in qnb]
    cls = build_clusters(q2k_nbrs, adj23, adj22, q3nb, qqset)
    checks['cluster_count'] = len(cls) == cert['cluster_count'] == len(cert['cluster_U'])
    fblob = base64.b64decode(cert['cluster_fresh_rows_base64'], validate=True)
    checks['cluster_fresh_sha256'] = hashlib.sha256(fblob).hexdigest() == cert['cluster_fresh_sha256']
    fresh_rows = [dict() for _ in cls]
    pos = 0
    for ci, u in cert['cluster_fresh_index']:
        row = unpack_row(fblob[pos:pos + RB], u); pos += RB
        fresh_rows[ci].setdefault(u, []).append(row)
    checks['fresh_consumed'] = pos == len(fblob)
    ok_cl = True
    ehist = {}
    with Pool(workers, initializer=_cl_init, initargs=(trows,)) as pool:
        jobs = [(ci, cl, set(cert['cluster_U'][ci]), fresh_rows[ci]) for ci, cl in enumerate(cls)]
        for ci, bad in pool.imap_unordered(_cluster_check, jobs, chunksize=8):
            ok_cl &= not bad
            k = len(cert['cluster_U'][ci]); ehist[k] = ehist.get(k, 0) + 1
    checks['cluster_coverage'] = ok_cl
    log(f'clusters {len(cls)}: coverage ok={ok_cl}; |U| histogram {dict(sorted(ehist.items()))}  ({time.time()-t0:.0f}s)')
    ok_cd = True
    n_cd = 0
    for ci, cl in enumerate(cls):
        U = cert['cluster_U'][ci]
        if len(U) >= 4:
            for D in itertools.combinations(U, 4):
                rec = direct.get((cl['id'], tuple(D)))
                ok_cd &= rec is not None and _check_direct(rec, D, cl['nbrs'], cl['edges'])
                n_cd += 1
    checks['cluster_direct_witnesses'] = ok_cd
    log(f'cluster direct tests {n_cd} ok={ok_cd}')
    # non-K layer: enumerate, screen, confirm exactly, triangles, clusters
    ehist_nk, n_nkd = {}, 0
    if not skip_nonk:
        import nonk_exact as nx
        nk = nonk_points(points, workers)
        labels = [(i, j, s) for i, j, s, _, _ in nk]
        PN = np.array([[x, y] for _, _, _, x, y in nk])
        cNN = unit_pairs_float(PN)
        cN2 = unit_pairs_float(PN, P2); cN3 = unit_pairs_float(PN, P3)
        geoms = {}

        def gm(i):
            if i not in geoms:
                geoms[i] = nx.geom(points, *labels[i])
            return geoms[i]
        confirmed = [(i, j) for i, j in cNN if nx.unit_nonk_pair(gm(i), gm(j))[0]]
        bad_k = sum(1 for i, j in cN2 if nx.unit_nonk_kpoint(gm(i), q2k[j])) + \
                sum(1 for i, j in cN3 if nx.unit_nonk_kpoint(gm(i), qpts[j]))
        nbN = {}
        for i, j in confirmed:
            nbN.setdefault(i, set()).add(j); nbN.setdefault(j, set()).add(i)
        tri = [(i, j, k) for i, j in confirmed for k in nbN[i] & nbN[j] if k > j]
        nk_cls = canonical_nonk_clusters([{'id': None, 'labels': [labels[i], labels[j], labels[k]]} for i, j, k in tri])
        for ci, cl in enumerate(nk_cls):
            cl['id'] = 'nonk:' + ':'.join(':'.join(map(str, l)) for l in cl['labels'])
        c = cert['nonk']
        checks['nonk_counts'] = (len(nk) == c['points'] and len(cNN) == c['unit_pair_candidates']
                                 and len(confirmed) == c['exact_unit_pairs'] and len(tri) == c['triangles']
                                 and len(cN2) + len(cN3) == c['k_point_candidates'])
        checks['nonk_no_k_neighbours'] = bad_k == 0
        checks['nonk_cluster_count'] = len(nk_cls) == len(cert['nonk_cluster_U'])
        log(f'non-K points {len(nk)}, candidate pairs {len(cNN)}, exact unit pairs {len(confirmed)}, triangles {len(tri)}, '
            f'K-point candidates {len(cN2)+len(cN3)} (unit: {bad_k})  ({time.time()-t0:.0f}s)')
        fblob = base64.b64decode(cert['nonk_cluster_fresh_rows_base64'], validate=True)
        checks['nonk_fresh_sha256'] = hashlib.sha256(fblob).hexdigest() == cert['nonk_cluster_fresh_sha256']
        nk_fresh = [dict() for _ in nk_cls]
        pos = 0
        for ci, u in cert['nonk_cluster_fresh_index']:
            row = unpack_row(fblob[pos:pos + RB], u); pos += RB
            nk_fresh[ci].setdefault(u, []).append(row)
        checks['nonk_fresh_consumed'] = pos == len(fblob)
        ok_nk = True
        if checks['nonk_cluster_count']:
            with Pool(workers, initializer=_cl_init, initargs=(trows,)) as pool:
                jobs = [(ci, cl, set(cert['nonk_cluster_U'][ci]), nk_fresh[ci]) for ci, cl in enumerate(nk_cls)]
                for ci, bad in pool.imap_unordered(_cluster_check, jobs, chunksize=32):
                    ok_nk &= not bad
                    k = len(cert['nonk_cluster_U'][ci]); ehist_nk[k] = ehist_nk.get(k, 0) + 1
            for ci, cl in enumerate(nk_cls):
                U = cert['nonk_cluster_U'][ci]
                if len(U) >= 4:
                    for D in itertools.combinations(U, 4):
                        rec = direct.get((cl['id'], tuple(D)))
                        ok_nk &= rec is not None and _check_direct(rec, D, cl['nbrs'], cl['edges'])
                        n_nkd += 1
        checks['nonk_cluster_coverage'] = ok_nk
        log(f'non-K clusters {len(nk_cls)}: coverage ok={ok_nk}; |U| histogram {dict(sorted(ehist_nk.items()))}; direct tests {n_nkd}  ({time.time()-t0:.0f}s)')
    allok = all(checks.values())
    print(json.dumps({'all_checks': allok, 'checks': checks, 'layer1': tot, 'U_histogram': dict(sorted(hist.items())),
                      'q3_candidates': len(cands), 'q3_direct_tests': n_direct, 'clusters': len(cls),
                      'cluster_U_histogram': dict(sorted(ehist.items())), 'cluster_direct_tests': n_cd,
                      'nonk_cluster_U_histogram': dict(sorted(ehist_nk.items())), 'nonk_direct_tests': n_nkd,
                      'seconds': round(time.time() - t0)}, indent=1))
    return allok


def _cl_init(trows):
    load_context()
    CTX['trows'] = trows


def _check_direct(rec, D, nbrs, internal):
    edges = CTX['edges']
    row = row_from_str(rec['row'])
    pc = rec['point_colours']
    Dset = set(D)
    if len(row) != N or any((row[v] == -1) != (v in Dset) for v in range(N)):
        return False
    if any(not (0 <= c < K) for v, c in enumerate(row) if v not in Dset):
        return False
    for a, b in edges:
        if a not in Dset and b not in Dset and row[a] == row[b]:
            return False
    if len(pc) != len(nbrs) or any(not (0 <= c < K) for c in pc):
        return False
    for i, nb in enumerate(nbrs):
        if any(row[w] == pc[i] for w in nb if w not in Dset):
            return False
    for (i, j) in internal:
        if pc[i] == pc[j]:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    c = sub.add_parser('check'); c.add_argument('results_dir'); c.add_argument('--workers', type=int, default=4)
    c.add_argument('--vertices', default=None)
    b = sub.add_parser('build'); b.add_argument('results_dir'); b.add_argument('q2k_extra'); b.add_argument('extra_u')
    b.add_argument('direct'); b.add_argument('out'); b.add_argument('--nonk-exact', default=None); b.add_argument('--nonk-u', default=None)
    v = sub.add_parser('verify'); v.add_argument('cert'); v.add_argument('--workers', type=int, default=8)
    v.add_argument('--skip-nonk', action='store_true')
    args = ap.parse_args()
    if args.cmd == 'check':
        rdir = Path(args.results_dir)
        us = [int(x) for x in args.vertices.split(',')] if args.vertices else \
            sorted(int(p.stem[2:]) for p in rdir.glob('u_*.json'))
        t0 = time.time()
        ok = True
        tot = {'uncovered': 0, 'implied_by_pairs': 0, 'explicit': 0, 'n_undeclared': 0, 'stale': 0}
        with Pool(args.workers, initializer=load_context) as pool:
            for r in pool.imap_unordered(_check_one, [(u, rdir) for u in us], chunksize=1):
                for k in tot:
                    tot[k] += r[k]
                ok &= r['n_undeclared'] == 0
                print(json.dumps(r), f'{time.time()-t0:.0f}s', flush=True)
        print('totals', tot, 'all_ok', ok, flush=True)
        sys.exit(0 if ok else 1)
    if args.cmd == 'build':
        command_build(args.results_dir, args.q2k_extra, args.extra_u, args.direct, args.out, args.nonk_exact, args.nonk_u)
    if args.cmd == 'verify':
        sys.exit(0 if command_verify(args.cert, args.workers, args.skip_nonk) else 1)


if __name__ == '__main__':
    main()
