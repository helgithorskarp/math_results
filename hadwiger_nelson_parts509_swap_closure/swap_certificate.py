#!/usr/bin/env python3
"""Build and verify the one-point swap-closure certificate for the Parts-509 graph.

Certificate content: for every vertex u, a short family of proper 4-colourings
of G-u (in addition to the previously certified deletion colouring of G-u)
such that for every completion point q with >= 4 unit neighbours, some
colouring in the family leaves N(q)-u short of a colour.  Verification is
solver-free: it reconstructs the exact graph, re-enumerates all completion
points exactly, decodes every colouring, checks it edge by edge, and replays
the coverage of all (q, u) instances.

  python swap_certificate.py build  swap_results_dir  completion_points.json  swap_certificate.json
  python swap_certificate.py verify completion_points.json swap_certificate.json
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
N, K = 509, 4
FORMAT = 'parts509-swap-closure-v1'
ROW_BYTES = (N - 1) // 4  # 127 bytes: 508 retained colours, 2 bits each


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


def pack_row(coloring, u):
    values = [c for v, c in enumerate(coloring) if v != u]
    assert len(values) == N - 1 and all(0 <= c < K for c in values)
    out = bytearray()
    for start in range(0, len(values), 4):
        out.append(sum(values[start + s] << (2 * s) for s in range(4)))
    return bytes(out)


def unpack_row(raw, u):
    assert len(raw) == ROW_BYTES
    values = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
    it = iter(values)
    return [-1 if v == u else next(it) for v in range(N)]


def rainbow(coloring, nbrs, u):
    seen = 0
    for w in nbrs:
        if w != u:
            seen |= 1 << coloring[w]
    return seen == 15


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


def load_q4(completion_path):
    comp = json.loads(Path(completion_path).read_text())
    return comp, [tuple(r['neighbors']) for r in comp['points'] if len(r['neighbors']) >= 4]


def command_build(results_dir, completion_path, out_path):
    parts = load_parts()
    points, edges, rows = load_base(parts)
    comp, q4 = load_q4(completion_path)
    q4_records = [r for r in comp['points'] if len(r['neighbors']) >= 4]
    families = []
    swaps = []
    packed = bytearray()
    for u in range(N):
        r = json.loads((Path(results_dir) / f'u_{u:03d}.json').read_text())
        assert r['u'] == u
        for qi in r['swaps']:
            swaps.append({'u': u, 'q_neighbors': list(q4[qi]), 'q_x': q4_records[qi]['x'], 'q_y': q4_records[qi]['y']})
        fam = []
        for s in r['colorings']:
            coloring = [-1 if ch == '-' else int(ch) for ch in s]
            parts.validate_coloring(N, edges, coloring, K, u)
            fam.append(coloring)
        # keep only colourings that cover something not covered earlier (greedy order preserved)
        uncovered = [qi for qi, nb in enumerate(q4) if rainbow(rows[u], nb, u)]
        kept = []
        for coloring in fam:
            newly = [qi for qi in uncovered if not rainbow(coloring, q4[qi], u)]
            if newly:
                kept.append(coloring)
                uncovered = [qi for qi in uncovered if rainbow(coloring, q4[qi], u)]
        assert sorted(uncovered) == sorted(r['swaps']), f'vertex {u}: uncovered instances differ from declared swaps'
        families.append(len(kept))
        for coloring in kept:
            packed += pack_row(coloring, u)
    payload = bytes(packed)
    cert = {
        'format': FORMAT,
        'claim': 'For every completion point q with >= 4 unit neighbours and every vertex u, some listed proper 4-colouring of G-u (or the base deletion colouring) leaves N(q)-u short of a colour; hence the strict unit-distance graph on (V-u)+q is 4-colourable.',
        'coordinate_sha256': file_sha256(BASE / 'parts509.vtx'),
        'edge_sha256': parts.edge_sha256(edges),
        'base_certificate_sha256': file_sha256(BASE / 'certificate.json'),
        'completion_points_sha256': file_sha256(completion_path),
        'q3_count': comp['q3_count'], 'q4_count': len(q4),
        'row_packing': 'one 127-byte row per colouring: 508 retained vertices in increasing order (deleted vertex omitted), four 2-bit colours per byte, low bits first',
        'family_sizes': families,
        'swaps': swaps,
        'swap_note': 'declared instances (q, u) for which no witness exists in this certificate; their non-4-colourability is certified separately by DRAT proofs',
        'family_rows_base64': base64.b64encode(payload).decode('ascii'),
        'packed_rows_sha256': hashlib.sha256(payload).hexdigest(),
    }
    Path(out_path).write_text(json.dumps(cert, indent=1, sort_keys=True) + '\n')
    print(json.dumps({'rows': sum(families), 'max_family': max(families), 'payload_bytes': len(payload), 'certificate_sha256': file_sha256(out_path)}, indent=2))


def command_verify(completion_path, cert_path, skip_enumeration=False):
    t0 = time.time()
    parts = load_parts()
    points, edges, rows = load_base(parts)
    cert = json.loads(Path(cert_path).read_text())
    if cert.get('format') != FORMAT:
        raise ValueError('unknown certificate format')
    if cert['coordinate_sha256'] != file_sha256(BASE / 'parts509.vtx'):
        raise ValueError('coordinate hash mismatch')
    if cert['edge_sha256'] != parts.edge_sha256(edges):
        raise ValueError('edge hash mismatch')
    if cert['base_certificate_sha256'] != file_sha256(BASE / 'certificate.json'):
        raise ValueError('base certificate hash mismatch')
    if cert['completion_points_sha256'] != file_sha256(completion_path):
        raise ValueError('completion point file hash mismatch')
    comp, q4 = load_q4(completion_path)
    if not skip_enumeration:
        import udg
        fresh = udg.completion_points(points, edges)
        committed = [(tuple(r['x']), tuple(r['y']), tuple(r['neighbors'])) for r in comp['points']]
        fresh_keys = [(tuple(r['x']), tuple(r['y']), tuple(r['neighbors'])) for r in fresh['points']]
        if sorted(committed) != sorted(fresh_keys):
            raise ValueError('committed completion points differ from fresh exact enumeration')
        print(f'fresh exact enumeration agrees: Q3={fresh["q3_count"]} Q4={fresh["q4_count"]} ({time.time()-t0:.0f}s)', flush=True)
    payload = base64.b64decode(cert['family_rows_base64'], validate=True)
    if hashlib.sha256(payload).hexdigest() != cert['packed_rows_sha256']:
        raise ValueError('packed rows hash mismatch')
    sizes = cert['family_sizes']
    if len(sizes) != N or len(payload) != sum(sizes) * ROW_BYTES:
        raise ValueError('family size table inconsistent with payload')
    offset = 0
    edge_checks = 0
    instances = base_covered = family_covered = 0
    uncovered_found = set()
    for u in range(N):
        fam = []
        for _ in range(sizes[u]):
            coloring = unpack_row(payload[offset:offset + ROW_BYTES], u)
            offset += ROW_BYTES
            parts.validate_coloring(N, edges, coloring, K, u)
            edge_checks += sum(1 for a, b in edges if a != u and b != u)
            fam.append(coloring)
        for nb in q4:
            instances += 1
            if not rainbow(rows[u], nb, u):
                base_covered += 1
            elif any(not rainbow(c, nb, u) for c in fam):
                family_covered += 1
            else:
                uncovered_found.add((tuple(nb), u))
    declared = {(tuple(s['q_neighbors']), s['u']) for s in cert['swaps']}
    if uncovered_found != declared:
        raise ValueError(f'uncovered instances {sorted(uncovered_found - declared)[:5]} differ from declared swaps {sorted(declared - uncovered_found)[:5]}')
    per_point = {}
    for nb, u in declared:
        per_point.setdefault(nb, []).append(u)
    max_swaps_per_point = max((len(v) for v in per_point.values()), default=0)
    if max_swaps_per_point > 1:
        raise ValueError('some completion point has two swap vertices; the delete-two corollary needs explicit pair witnesses')
    print(json.dumps({
        'all_checks': True,
        'q3_points': comp['q3_count'], 'q4_points': len(q4),
        'swap_instances': instances,
        'covered_by_base_deletion_rows': base_covered,
        'covered_by_family_rows': family_covered,
        'family_rows': sum(sizes), 'retained_edge_inequality_checks': edge_checks,
        'declared_swaps': len(declared), 'max_swaps_per_point': max_swaps_per_point,
        'conclusion': 'every instance (q, u) outside the declared swap list has a checked witness colouring; each completion point has at most one swap vertex, so for every point q of the plane and every pair {u, v} some witness restricts to a proper 4-colouring of (V - u - v) + q; no 508-vertex 5-chromatic graph arises from the Parts graph by deleting two vertices and adding one point',
        'seconds': round(time.time() - t0, 1),
    }, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build'); b.add_argument('results_dir'); b.add_argument('completion'); b.add_argument('out')
    v = sub.add_parser('verify'); v.add_argument('completion'); v.add_argument('certificate'); v.add_argument('--skip-enumeration', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'build':
        command_build(a.results_dir, a.completion, a.out)
    else:
        command_verify(a.completion, a.certificate, a.skip_enumeration)


if __name__ == '__main__':
    main()
