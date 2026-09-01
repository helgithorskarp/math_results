#!/usr/bin/env python3
"""Build and verify the two-point augmentation closure certificate of the
Parts-509 graph ("no 508 by deleting three vertices and adding two points").

Certificate content (pair_certificate.json):
  * for every vertex u, additional proper 4-colourings of G - u (packed rows),
  * the list of pairs A = {q1, q2} of completion points and vertices u for which
    no listed colouring extends to both points (declared instances),
  * for every pair A whose declared vertex set U(A) has at least three members
    and every 3-subset D of U(A), an explicit proper 4-colouring of the
    508-vertex graph G - D + A.

Verification is solver-free: exact reconstruction of the graph, exact
recomputation of all unit distances between completion points and vertices and
among completion points, decoding and edge-by-edge checking of every colouring,
and a replay of the coverage argument with free-colour masks.

  python pair_certificate.py build  pair_results_dir pair_layer2_results.json completion_points.json pair_certificate.json
  python pair_certificate.py verify completion_points.json pair_certificate.json [--skip-enumeration]
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, itertools, json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
_SW = [HERE.parent / 'hadwiger_nelson_parts509_swap_closure',
       Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure']
SWAPDIR = next(p for p in _SW if (p / 'swap_certificate.json').exists())
sys.path.insert(0, str(SWAPDIR))   # exact tower-field arithmetic (kfield.py) and unit-distance tooling (udg.py) of the sibling
N, K = 509, 4
FORMAT = 'parts509-pair-closure-v1'
ROW_BYTES = (N - 1) // 4          # 127 bytes: 508 retained colours, 2 bits each
ROW3_BYTES = 127                  # 506 retained colours + 2 point colours = 508 values


def log(msg):
    print(msg, flush=True)


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509_base', BASE / 'parts509.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def file_sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def pack_values(values):
    assert len(values) % 4 == 0 and all(0 <= c < K for c in values)
    out = bytearray()
    for start in range(0, len(values), 4):
        out.append(sum(values[start + s] << (2 * s) for s in range(4)))
    return bytes(out)


def unpack_values(raw):
    return [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]


def pack_row(coloring, u):
    return pack_values([c for v, c in enumerate(coloring) if v != u])


def unpack_row(raw, u):
    assert len(raw) == ROW_BYTES
    it = iter(unpack_values(raw))
    return [-1 if v == u else next(it) for v in range(N)]


def pack_triple(coloring, D, qcolors):
    values = [c for v, c in enumerate(coloring) if v not in D] + list(qcolors)
    assert len(values) == N - 3 + 2
    return pack_values(values)


def unpack_triple(raw, D):
    assert len(raw) == ROW3_BYTES
    vals = unpack_values(raw)
    it = iter(vals[:N - 3])
    coloring = [-1 if v in D else next(it) for v in range(N)]
    return coloring, vals[N - 3:N - 1]


def load_base(parts):
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    cert = json.loads((BASE / 'certificate.json').read_text())
    packed = base64.b64decode(cert['deletion_colorings_base64'], validate=True)
    if hashlib.sha256(packed).hexdigest() != cert['packed_deletion_colorings_sha256']:
        raise ValueError('base deletion certificate hash mismatch')
    rows = parts.unpack_deletion_rows(packed, N)
    for d, row in enumerate(rows):
        parts.validate_coloring(N, edges, row, K, d)
    return points, edges, rows


def load_swap_families(parts, edges):
    sc = json.loads((SWAPDIR / 'swap_certificate.json').read_text())
    payload = base64.b64decode(sc['family_rows_base64'], validate=True)
    if hashlib.sha256(payload).hexdigest() != sc['packed_rows_sha256']:
        raise ValueError('swap certificate hash mismatch')
    fams = [[] for _ in range(N)]
    pos = 0
    for u, size in enumerate(sc['family_sizes']):
        for _ in range(size):
            row = unpack_row(payload[pos:pos + ROW_BYTES], u)
            pos += ROW_BYTES
            parts.validate_coloring(N, edges, row, K, u)
            fams[u].append(row)
    assert pos == len(payload)
    return sc, fams


def exact_incidences(points, qpts, workers=8):
    """Exact unit pairs among V ∪ Q3 (integer arithmetic): returns (q_neighbors, qq_edges, vv_edges)."""
    import udg
    allpts = list(points) + list(qpts)
    edges = udg.unit_edges(allpts, workers=workers)
    nq = len(qpts)
    qnb = [[] for _ in range(nq)]
    qq, vv = [], []
    for a, b in edges:
        if b < N:
            vv.append((a, b))
        elif a < N:
            qnb[b - N].append(a)
        else:
            qq.append((a - N, b - N))
    return [tuple(sorted(nb)) for nb in qnb], sorted(qq), sorted(vv)


class Coverage:
    """Vectorised free-colour masks and pair coverage for one deleted vertex."""

    def __init__(self, qnb, qq_edges):
        self.nq = len(qnb)
        maxd = max(len(nb) for nb in qnb)
        self.nbarr = np.full((self.nq, maxd), -1, dtype=np.int64)
        for i, nb in enumerate(qnb):
            self.nbarr[i, :len(nb)] = nb
        self.qa = np.array([a for a, b in qq_edges], dtype=np.int64)
        self.qb = np.array([b for a, b in qq_edges], dtype=np.int64)
        self.iu = np.triu_indices(self.nq, 1)

    def free_masks(self, coloring, u):
        col = np.array(list(coloring) + [-1], dtype=np.int64)
        c = col[self.nbarr]
        c = np.where(self.nbarr == u, -1, c)
        used = np.zeros(self.nq, dtype=np.int64)
        for k in range(K):
            used |= (c == k).any(axis=1).astype(np.int64) << k
        return 15 - used

    def coverage(self, coloring, u):
        fm = self.free_masks(coloring, u)
        ok = fm != 0
        cov = np.outer(ok, ok)
        conflict = (fm[self.qa] == fm[self.qb]) & np.isin(fm[self.qa], (1, 2, 4, 8))
        cov[self.qa[conflict], self.qb[conflict]] = False
        cov[self.qb[conflict], self.qa[conflict]] = False
        return cov


def validate_triple(edges, qnb, qqset, A, D, coloring, qcolors):
    Dset = set(D)
    for v, c in enumerate(coloring):
        if v in Dset:
            assert c == -1
        else:
            assert 0 <= c < K
    for a, b in edges:
        if a not in Dset and b not in Dset and coloring[a] == coloring[b]:
            raise ValueError(f'monochromatic base edge {(a, b)} in triple witness {A} {D}')
    for q, qc in zip(A, qcolors):
        assert 0 <= qc < K
        for w in qnb[q]:
            if w not in Dset and coloring[w] == qc:
                raise ValueError(f'point {q} clashes with neighbour {w} in triple witness {A} {D}')
    if (A[0], A[1]) in qqset and qcolors[0] == qcolors[1]:
        raise ValueError(f'adjacent points {A} coloured alike in triple witness {D}')


def command_build(results_dir, layer2_path, completion_path, out_path):
    parts = load_parts()
    points, edges, rows = load_base(parts)
    sc, fams = load_swap_families(parts, edges)
    comp = json.loads(Path(completion_path).read_text())
    qnb = [tuple(r['neighbors']) for r in comp['points']]
    amb = json.loads((HERE / 'ambient_w3_edges.json').read_text())
    qq_edges = sorted((a - N, b - N) for a, b in amb['edges'] if a >= N and b >= N)
    qqset = set(qq_edges)
    cov = Coverage(qnb, qq_edges)
    layer2 = json.loads(Path(layer2_path).read_text())
    packed = bytearray()
    sizes, declared = [], []
    stats = {'solver_unsat': 0, 'swap_implied': 0}
    for u in range(N):
        r = json.loads((Path(results_dir) / f'u_{u:03d}.json').read_text())
        assert r['u'] == u
        covered = np.zeros((cov.nq, cov.nq), dtype=bool)
        for row in [rows[u]] + fams[u]:
            covered |= cov.coverage(row, u)
        kept = []
        for s in r['new_rows']:
            row = [-1 if ch == '-' else int(ch) for ch in s]
            parts.validate_coloring(N, edges, row, K, u)
            c = cov.coverage(row, u)
            if (c & ~covered).any():
                kept.append(row)
                covered |= c
        unc = set(zip(*[x.tolist() for x in np.nonzero(~covered & np.triu(np.ones_like(covered), 1))]))
        solver_unsat = {tuple(p) for p in r['unsat_pairs']}
        implied = {(min(q, q2), max(q, q2)) for q in r['swap_points'] for q2 in range(cov.nq) if q2 != q}
        assert unc == (solver_unsat | implied) - set(), f'vertex {u}: uncovered pairs differ from solver/swap declarations'
        stats['solver_unsat'] += len(solver_unsat)
        stats['swap_implied'] += len(implied - solver_unsat)
        sizes.append(len(kept))
        for row in kept:
            packed += pack_row(row, u)
        declared.append(sorted(unc))
    payload = bytes(packed)
    # triple witnesses
    tpacked = bytearray()
    triples = []
    for w in layer2['triple_witnesses']:
        A, D = tuple(w['A']), tuple(w['D'])
        coloring = [-1 if ch == '-' else int(ch) for ch in w['coloring']]
        validate_triple(edges, qnb, qqset, A, D, coloring, w['q_colors'])
        triples.append({'A': list(A), 'D': list(D)})
        tpacked += pack_triple(coloring, set(D), w['q_colors'])
    tpayload = bytes(tpacked)
    cert = {
        'format': FORMAT,
        'claim': ('For every vertex u and every pair {q1, q2} of completion points (all points of the plane with >= 3 unit '
                  'neighbours in V), some listed proper 4-colouring of G - u (base deletion row, swap-closure family row or '
                  'row listed here) extends to both points, except for the declared instances; for every pair whose declared '
                  'vertex set has >= 3 members, every 3-subset D has an explicit proper 4-colouring of G - D + {q1, q2}. '
                  'Hence no 5-chromatic unit-distance graph on 508 vertices arises from the Parts graph by deleting three '
                  'vertices and adding two points of the plane.'),
        'coordinate_sha256': file_sha256(BASE / 'parts509.vtx'),
        'edge_sha256': parts.edge_sha256(edges),
        'base_certificate_sha256': file_sha256(BASE / 'certificate.json'),
        'swap_certificate_sha256': file_sha256(SWAPDIR / 'swap_certificate.json'),
        'completion_points_sha256': file_sha256(completion_path),
        'q3_count': len(qnb), 'q3q3_unit_pairs': len(qq_edges),
        'row_packing': 'one 127-byte row per colouring: 508 retained vertices in increasing order (deleted vertex omitted), four 2-bit colours per byte, low bits first',
        'triple_packing': 'one 127-byte row per triple witness: 506 retained vertices in increasing order, then the colours of q1 and q2, four 2-bit values per byte, low bits first',
        'family_sizes': sizes,
        'family_rows_base64': base64.b64encode(payload).decode('ascii'),
        'packed_rows_sha256': hashlib.sha256(payload).hexdigest(),
        'declared_pairs': declared,
        'declared_note': 'instances (pair, u) with no witness among the listed colourings; the solver reported them unsatisfiable or they contain a certified swap point of u; they are not part of the 4-colourability certificate',
        'U_histogram': layer2['U_histogram'],
        'pairs_with_U_ge3': layer2['pairs_with_U_ge3'],
        'pairs_with_U_eq2': layer2['pairs_with_U_eq2'],
        'triple_witnesses': triples,
        'triple_rows_base64': base64.b64encode(tpayload).decode('ascii'),
        'packed_triple_rows_sha256': hashlib.sha256(tpayload).hexdigest(),
        'candidates_508': layer2['candidates_508'],
    }
    Path(out_path).write_text(json.dumps(cert, sort_keys=True) + '\n')
    log(json.dumps({'rows': sum(sizes), 'max_family': max(sizes), 'payload_bytes': len(payload),
                    'declared_instances': sum(len(d) for d in declared), **stats,
                    'triple_witnesses': len(triples), 'certificate_sha256': file_sha256(out_path)}, indent=2))


def command_verify(completion_path, cert_path, skip_enumeration=False, workers=8):
    t0 = time.time()
    parts = load_parts()
    points, edges, rows = load_base(parts)
    cert = json.loads(Path(cert_path).read_text())
    if cert.get('format') != FORMAT:
        raise ValueError('unexpected certificate format')
    for key, path in (('coordinate_sha256', BASE / 'parts509.vtx'), ('base_certificate_sha256', BASE / 'certificate.json'),
                      ('swap_certificate_sha256', SWAPDIR / 'swap_certificate.json'), ('completion_points_sha256', completion_path)):
        if cert[key] != file_sha256(path):
            raise ValueError(f'{key} mismatch')
    if cert['edge_sha256'] != parts.edge_sha256(edges):
        raise ValueError('edge hash mismatch')
    sc, fams = load_swap_families(parts, edges)
    if sc['completion_points_sha256'] != cert['completion_points_sha256']:
        raise ValueError('completion-point file differs from the one certified by the swap closure')
    import kfield as kf, udg
    comp = json.loads(Path(completion_path).read_text())
    qpts = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in comp['points']]
    listed_nb = [tuple(r['neighbors']) for r in comp['points']]
    if not skip_enumeration:
        fresh = udg.completion_points(points, edges, workers=workers)
        fresh_sets = {tuple(r['neighbors']) for r in fresh['points']}
        if fresh_sets != set(listed_nb) or fresh['q3_count'] != len(listed_nb):
            raise ValueError('fresh exact enumeration disagrees with the committed completion points')
        log(f'fresh exact enumeration agrees: Q3={len(listed_nb)} ({time.time()-t0:.0f}s)')
    qnb, qq_edges, vv = exact_incidences(points, qpts, workers)
    if vv != sorted(edges):
        raise ValueError('integer re-verification of the base edges failed')
    if qnb != listed_nb:
        raise ValueError('exact rescan of completion-point neighbourhoods disagrees with the committed lists')
    if len(qq_edges) != cert['q3q3_unit_pairs']:
        raise ValueError('number of unit pairs among completion points differs from the certificate')
    qqset = set(qq_edges)
    nq = len(qnb)
    log(f'exact incidences: {nq} completion points, {sum(len(nb) for nb in qnb)} point-vertex unit pairs, {len(qq_edges)} point-point unit pairs ({time.time()-t0:.0f}s)')
    payload = base64.b64decode(cert['family_rows_base64'], validate=True)
    if hashlib.sha256(payload).hexdigest() != cert['packed_rows_sha256']:
        raise ValueError('packed row hash mismatch')
    sizes = cert['family_sizes']
    if len(sizes) != N or len(payload) != sum(sizes) * ROW_BYTES:
        raise ValueError('family sizes do not match payload')
    cov = Coverage(qnb, qq_edges)
    U = {}
    offset = 0
    n_rows = 0
    edge_checks = 0
    declared_total = 0
    for u in range(N):
        fam = [rows[u]] + fams[u]
        for _ in range(sizes[u]):
            row = unpack_row(payload[offset:offset + ROW_BYTES], u)
            offset += ROW_BYTES
            parts.validate_coloring(N, edges, row, K, u)
            fam.append(row)
        n_rows += len(fam)
        edge_checks += len(fam) * sum(1 for a, b in edges if a != u and b != u)
        covered = np.zeros((nq, nq), dtype=bool)
        for row in fam:
            covered |= cov.coverage(row, u)
        unc = ~covered
        unc[np.tril_indices(nq)] = False
        pairs = list(zip(*[x.tolist() for x in np.nonzero(unc)]))
        declared = {tuple(p) for p in cert['declared_pairs'][u]}
        if set(pairs) != declared:
            raise ValueError(f'vertex {u}: uncovered pairs differ from the declared instances')
        declared_total += len(pairs)
        for p in pairs:
            U.setdefault(p, []).append(u)
    hist = {}
    for A, s in U.items():
        hist[len(s)] = hist.get(len(s), 0) + 1
    log(f'coverage replayed for all {N} vertices: {n_rows} colourings, {edge_checks} retained-edge checks, {declared_total} declared instances, |U(A)| histogram {dict(sorted(hist.items()))} ({time.time()-t0:.0f}s)')
    # triple witnesses
    tpayload = base64.b64decode(cert['triple_rows_base64'], validate=True)
    if hashlib.sha256(tpayload).hexdigest() != cert['packed_triple_rows_sha256']:
        raise ValueError('packed triple hash mismatch')
    tw = cert['triple_witnesses']
    if len(tpayload) != len(tw) * ROW3_BYTES:
        raise ValueError('triple payload size mismatch')
    have = {}
    for i, w in enumerate(tw):
        A, D = tuple(w['A']), tuple(sorted(w['D']))
        coloring, qcolors = unpack_triple(tpayload[i * ROW3_BYTES:(i + 1) * ROW3_BYTES], set(D))
        validate_triple(edges, qnb, qqset, A, D, coloring, qcolors)
        have[(A, D)] = True
    needed = 0
    for A, s in U.items():
        if len(s) >= 3:
            for D in itertools.combinations(sorted(s), 3):
                needed += 1
                if (A, D) not in have:
                    raise ValueError(f'missing triple witness for pair {A} and deletion {D}')
    big = sum(1 for s in U.values() if len(s) >= 3)
    if cert['candidates_508']:
        raise ValueError('certificate lists 508-vertex candidates; the closure claim does not hold')
    summary = {
        'all_checks': True, 'q3_points': nq, 'q3q3_unit_pairs': len(qq_edges), 'pairs': nq * (nq - 1) // 2,
        'pair_instances': nq * (nq - 1) // 2 * N, 'colourings_checked': n_rows, 'retained_edge_checks': edge_checks,
        'declared_instances': declared_total, 'pairs_with_nonempty_U': len(U), 'U_histogram': {str(k): v for k, v in sorted(hist.items())},
        'pairs_with_U_ge3': big, 'triple_instances_needed': needed, 'triple_witnesses_checked': len(tw),
        'conclusion': 'for every pair of points of the plane and every three vertices, some checked colouring restricts/extends to a proper 4-colouring of (V - D) + {q1, q2}; no 508-vertex 5-chromatic graph arises from the Parts graph by deleting three vertices and adding two points',
        'seconds': round(time.time() - t0, 1),
    }
    log(json.dumps(summary, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build'); b.add_argument('results_dir'); b.add_argument('layer2'); b.add_argument('completion'); b.add_argument('out')
    v = sub.add_parser('verify'); v.add_argument('completion'); v.add_argument('cert'); v.add_argument('--skip-enumeration', action='store_true'); v.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    if a.cmd == 'build':
        command_build(a.results_dir, a.layer2, a.completion, a.out)
    else:
        command_verify(a.completion, a.cert, a.skip_enumeration, a.workers)


if __name__ == '__main__':
    main()
