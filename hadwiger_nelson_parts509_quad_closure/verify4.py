#!/usr/bin/env python3
"""Solver-free verifier of the all-anchored delete-5-add-4 closure certificate (certificate.json or .json.gz).

Checks, from the committed sibling data only (no SAT solver):
  1. input hashes; the universe of points and unit incidences rebuilt from the sibling files agrees with the
     triple certificate (Q2K points, their neighbours, the exact Q2K unit incidences, the non-K counts);
  2. every certificate row is a proper 4-colouring of G - u (exact edge list);
  3. for every vertex u, with the witness libraries (base, swap, pair, triple rows) plus the certificate rows and
     the declared sets (sibling certificates plus this certificate), the exhaustive branching enumeration of
     uncovered point sets of size <= 4 returns nothing: every set of <= 4 universe points that no listed colouring of
     G - u extends to contains a declared set;  every certificate-declared set is re-checked to be uncovered;
  4. the union-closure aggregation: |Û(B)| <= 4 for all declared B of size <= 3, the |Û(A)| histogram, the candidate
     list (valid 4-sets with |Û(A)| >= 5) equals the certificate's, and every (candidate, 5-subset D of Û(A)) has a
     stored proper 4-colouring of (V \\ D) ∪ A (checked exactly: vertex edges, vertex-point incidences, point-point edges).
usage: verify4.py CERT [--workers W] [--vertices u1 u2 ...]
"""
import argparse, base64, gzip, hashlib, itertools, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from paths import COMPLETION, SWAP_CERT, PAIR_CERT, AMBIENT, TRIPLE_CERT, Q2K_EXTRA, NONK_EXACT, N, K
import uncovered_sets as us
import aggregate4
from known_declared import load_known_declared
G = {}


def load_cert(path):
    p = Path(path)
    raw = gzip.open(p, 'rb').read() if p.suffix == '.gz' else p.read_bytes()
    return json.loads(raw)


def unpack_row(raw, u):
    vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
    it = iter(vals)
    return [-1 if v == u else next(it) for v in range(N)]


def decode_ref(uni, ref):
    f = ref.split(':')
    if f[0] == 'q3':
        return int(f[1])
    if f[0] == 'k2':
        return uni.n3 + int(f[1])
    if f[0] == 'n':
        return uni.nk + G['lab_index'][(int(f[1]), int(f[2]), int(f[3]))]
    raise ValueError(ref)


def init(cert_path):
    cert = load_cert(cert_path)
    uni = us.Universe()
    G['uni'] = uni
    G['lab_index'] = {tuple(l): i for i, l in enumerate(uni.nonk_labels)}
    parts, edges, lib, qnb, qq_edges, counts = us.load_libraries()
    RB = (N - 1) // 4
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    pos = 0
    crow = [[] for _ in range(N)]
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            row = unpack_row(packed[pos:pos + RB], u); pos += RB
            parts.validate_coloring(N, edges, row, K, u)
            crow[u].append(row)
    assert pos == len(packed)
    known, src = load_known_declared()
    G['rows'] = [lib[u] + crow[u] for u in range(N)]
    G['known'] = known
    G['cert_declared'] = [[(tuple(sorted(decode_ref(uni, r) for r in A)), st) for A, st in lst] for lst in cert['declared_sets']]
    G['edges'] = edges


def check_u(u):
    t0 = time.time()
    uni = G['uni']
    declared = list(G['known'][u]) + [list(A) for A, st in G['cert_declared'][u]]
    st = us.VertexState(uni, u, G['rows'][u], declared)
    leaves, stats = st.enumerate_uncovered()
    stale = [A for A, s in G['cert_declared'][u] if not st.fails(A).all()]
    return u, len(leaves), stats['nodes'], len(stale), round(time.time() - t0, 1), [list(l) for l in leaves[:5]]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cert'); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--vertices', type=int, nargs='*', default=None)
    ap.add_argument('--checkpoint', default=None, help='directory for per-vertex checkpoints (finished vertices are skipped on rerun)')
    args = ap.parse_args(); t0 = time.time()
    cert = load_cert(args.cert)
    checks = {}
    log = lambda s: print(f'[{time.time()-t0:6.0f}s] {s}', flush=True)
    # 1. hashes and universe cross-checks
    files = {'completion_points.json': COMPLETION, 'swap_certificate.json': SWAP_CERT, 'pair_certificate.json': PAIR_CERT,
             'ambient_w3_edges.json': AMBIENT, 'triple_certificate.json': TRIPLE_CERT}
    for name, p in files.items():
        checks[f'sha256:{name}'] = hashlib.sha256(p.read_bytes()).hexdigest() == cert['inputs_sha256'][name]
    log(f"input hashes: {all(v for k, v in checks.items() if k.startswith('sha256'))}")
    init(args.cert)
    uni = G['uni']
    tc = json.loads(TRIPLE_CERT.read_text())
    ex = json.loads(Q2K_EXTRA.read_text())
    checks['q2k_points'] = [r['neighbors'] for r in tc['q2k_points']] == [r['neighbors'] for r in ex['q2k']] and \
                           [(r['x'], r['y']) for r in tc['q2k_points']] == [(r['x'], r['y']) for r in ex['q2k']]
    checks['q2k_incidences'] = sorted(map(tuple, tc['q2k_q3_unit_pairs'])) == sorted(map(tuple, ex['adj_q2k_q3'])) and \
                               sorted(map(tuple, tc['q2k_q2k_unit_pairs'])) == sorted(map(tuple, ex['adj_q2k_q2k']))
    nk_stats = dict(tc['nonk'])
    checks['nonk_counts'] = (uni.nn == nk_stats.get('points') and len(uni.nonk_edges) == nk_stats.get('exact_unit_pairs') and len(uni.ntri) == nk_stats.get('triangles'))
    log(f'universe: Q3 {uni.n3}, Q2K {uni.n2}, K-edges {len(uni.kedges)}, conn3 {len(uni.conn3)}, conn4 {len(uni.conn4)}, non-K {uni.nn} pts / {len(uni.nonk_edges)} edges / {len(uni.ntri)} triangles / {len(uni.ndia)} diamonds; '
        f"q2k match {checks['q2k_points']}, incidences match {checks['q2k_incidences']}, nonk counts match {checks['nonk_counts']} {nk_stats}")
    log(f"certificate rows {sum(cert['family_sizes'])} (validated), declared sets {sum(len(l) for l in cert['declared_sets'])}")
    # 3. per-vertex enumeration
    us_list = args.vertices if args.vertices is not None else list(range(N))
    tot_leaves = tot_nodes = tot_stale = 0
    ck = Path(args.checkpoint) if args.checkpoint else None
    done = {}
    if ck:
        ck.mkdir(exist_ok=True)
        for u in us_list:
            f = ck / f'u_{u:03d}.json'
            if f.exists():
                done[u] = json.loads(f.read_text())
    for u, (u2, nl, nn, ns, secs, sample) in done.items():
        assert u == u2
        tot_leaves += nl; tot_nodes += nn; tot_stale += ns
        if nl:
            log(f'vertex {u} (checkpoint): undeclared uncovered sets {nl} {sample}')
    todo = [u for u in us_list if u not in done]
    log(f'per-vertex enumeration: {len(done)} vertices from checkpoints, {len(todo)} to do')
    with Pool(args.workers, initializer=init, initargs=(args.cert,)) as pool:
        for i, res in enumerate(pool.imap_unordered(check_u, todo, chunksize=1)):
            u, nl, nn, ns, secs, sample = res
            if ck:
                (ck / f'u_{u:03d}.json').write_text(json.dumps(res))
            tot_leaves += nl; tot_nodes += nn; tot_stale += ns
            if nl or (i + 1) % 50 == 0 or i + 1 == len(todo):
                log(f'vertex {u}: undeclared uncovered sets {nl} {sample if nl else ""} (nodes {nn}, stale declared {ns}, {secs}s); done {i+1}/{len(todo)}')
    checks['no_undeclared_uncovered_set'] = tot_leaves == 0
    log(f'enumeration: undeclared uncovered sets {tot_leaves}, nodes {tot_nodes}, stale certificate declarations {tot_stale}')
    # 4. aggregation and direct witnesses
    labels = {}
    for u in range(N):
        for B in G['known'][u]:
            labels.setdefault(frozenset(B), set()).add(u)
        for A, st in G['cert_declared'][u]:
            labels.setdefault(frozenset(A), set()).add(u)
    agg = aggregate4.aggregate(uni, labels)
    cands = [c for c in agg['candidates'] if c['valid']]
    cert_c = cert['aggregation']['candidates']
    cert_map = {tuple(sorted(decode_ref(uni, r) for r in c['A'])): c for c in cert_c}
    checks['candidates_match'] = set(cert_map) == set(tuple(c['A']) for c in agg['candidates']) and \
        all(cert_map[tuple(c['A'])]['Uhat'] == c['Uhat'] and cert_map[tuple(c['A'])]['valid'] == c['valid'] for c in agg['candidates'])
    checks['hist4_match'] = {int(k): v for k, v in cert['aggregation']['hist4'].items()} == agg['hist4']
    log(f"aggregation: declared sets {len(labels)}, unions {agg['n_unions']}, hist_small {agg['hist_small']}, hist4 {dict(sorted(agg['hist4'].items()))}, "
        f"candidates {len(agg['candidates'])} (valid {len(cands)}); matches certificate: {checks['candidates_match']}, hist {checks['hist4_match']}")
    wit = {}
    for w in cert['direct_witnesses']:
        A = tuple(sorted(decode_ref(uni, r) for r in w['A']))
        wit[(A, tuple(sorted(w['D'])))] = w
    edges = G['edges']
    ok_w = True; n_tests = 0
    for c in cands:
        A = tuple(c['A'])
        for D in itertools.combinations(sorted(c['Uhat']), 5):
            n_tests += 1
            w = wit.get((A, D))
            if w is None or w['status'] != 'sat':
                ok_w = False; log(f'MISSING witness for A={A} D={D}'); continue
            col = [-1 if ch == '-' else int(ch) for ch in w['colouring']]; pc = w['point_colours']
            dele = set(D)
            good = len(col) == N and all(col[v] == -1 for v in D) and all(0 <= col[v] < K for v in range(N) if v not in dele)
            good &= all(col[a] != col[b] for a, b in edges if a not in dele and b not in dele)
            for i, p in enumerate(A):
                good &= 0 <= pc[i] < K and all(col[v] != pc[i] for v in uni.point_nbrs(p) if v not in dele)
            good &= all(pc[i] != pc[j] for i, j in itertools.combinations(range(4), 2) if uni.adjacent(A[i], A[j]))
            if not good:
                ok_w = False; log(f'BAD witness for A={A} D={D}')
    checks['direct_witnesses'] = ok_w
    log(f'direct witnesses: {n_tests} (candidate, D) tests, all valid: {ok_w}')
    checks['all_checks'] = all(checks.values())
    print(json.dumps({'checks': checks, 'undeclared_uncovered': tot_leaves, 'nodes': tot_nodes, 'stale': tot_stale, 'candidates': len(agg['candidates']),
                      'valid_candidates': len(cands), 'direct_tests': n_tests, 'hist4': agg['hist4'], 'hist_small': agg['hist_small'], 'seconds': round(time.time() - t0)}))
    print(f"all_checks={'true' if checks['all_checks'] else 'false'}")


if __name__ == '__main__':
    main()
