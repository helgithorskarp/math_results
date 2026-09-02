#!/usr/bin/env python3
"""Pack the all-anchored delete-5-add-4 closure certificate.
usage: pack4.py RESULTS_DIR AGGREGATE_JSON DIRECT_JSON OUT_JSON
Rows: 2-bit packing as in the sibling certificates (508 retained vertices in increasing order, 4 per byte, low bits
first, 127 bytes per row).  Point references: 'q3:I' (completion point I), 'k2:I' (Q2K point I of the triple
certificate's q2k_points list), 'n:I:J:S' (non-K intersection point of vertices I<J, sign S)."""
import base64, hashlib, json, sys, time
from pathlib import Path
from paths import HERE, COMPLETION, SWAP_CERT, PAIR_CERT, AMBIENT, TRIPLE_CERT, N, K


def pack_row(row, u):
    vals = [row[v] for v in range(N) if v != u]
    assert len(vals) == N - 1 and all(0 <= x < 4 for x in vals)
    out = bytearray()
    for i in range(0, len(vals), 4):
        b = 0
        for s, x in enumerate(vals[i:i + 4]):
            b |= x << (2 * s)
        out.append(b)
    return bytes(out)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    resdir, aggf, directf, outf = map(Path, sys.argv[1:5])
    partial = '--partial' in sys.argv
    import build_universe
    U4 = json.loads((HERE / 'universe4.json').read_text()) if (HERE / 'universe4.json').exists() else build_universe.build()
    n3, n2 = U4['n_q3'], U4['n_q2k']; nk = n3 + n2
    labels = U4['nonk_labels']

    def ref(p):
        if p < n3: return f'q3:{p}'
        if p < nk: return f'k2:{p - n3}'
        i, j, s = labels[p - nk]; return f'n:{i}:{j}:{s}'

    sizes, packed, declared, stats = [], bytearray(), [], {'sat_calls': 0, 'passes': 0, 'seconds': 0.0, 'unsat': 0, 'budget': 0, 'rows': 0}
    done = []
    for u in range(N):
        f = resdir / f'u_{u:03d}.json'
        if not f.exists():
            assert partial, f'missing {f}'
            sizes.append(0); declared.append([]); continue
        done.append(u)
        r = json.loads(f.read_text())
        assert r['u'] == u
        rows = [[-1 if ch == '-' else int(ch) for ch in s] for s in r['new_rows']]
        for row in rows:
            assert row[u] == -1
            packed += pack_row(row, u)
        sizes.append(len(rows)); stats['rows'] += len(rows)
        declared.append([[sorted(ref(p) for p in A), st] for A, st in r['declared']])
        stats['sat_calls'] += r['sat_calls']; stats['passes'] += r['passes']; stats['seconds'] += r['seconds']
        stats['unsat'] += sum(1 for _, st in r['declared'] if st == 'unsat'); stats['budget'] += sum(1 for _, st in r['declared'] if st == 'budget')
    agg = json.loads(aggf.read_text()); direct = json.loads(directf.read_text())
    cands = [{'A': [ref(p) for p in c['A']], 'Uhat': c['Uhat'], 'valid': c['valid']} for c in agg['candidates']]
    wit = [{'A': [ref(p) for p in t['A']], 'D': t['D'], 'status': t['status'], 'colouring': t['colouring'], 'point_colours': t['point_colours']} for t in direct['tests']]
    assert all(t['status'] == 'sat' for t in direct['tests'])
    cert = {
        'format': 'parts509-quad-closure-v1',
        'claim': 'For every set A of four distinct points of the plane outside V, each at unit distance from at least two Parts vertices, '
                 'that can be the added point set of a 5-vertex-critical unit-distance graph on (V \\ D) u A (Q2K and non-K points have >= 2 '
                 'unit neighbours in A, completion points with exactly three vertex neighbours have >= 1), and every set D of at least five '
                 'Parts vertices, the strict unit-distance graph on (V \\ D) u A is 4-colourable.',
        'row_packing': 'one 127-byte row per colouring: 508 retained vertices in increasing order (deleted vertex omitted), 2 bits each, 4 per byte, low bits first',
        'family_sizes': sizes, 'family_rows_base64': base64.b64encode(bytes(packed)).decode(), 'packed_rows_sha256': hashlib.sha256(bytes(packed)).hexdigest(),
        'declared_sets': declared,
        'declared_note': 'per vertex u: point sets A (references) for which no listed colouring of G - u extends to A and the solver did not find one '
                         '(status unsat or budget); together with the declared sets of the sibling certificates (swap points, declared pairs, declared triples, '
                         'Q2K clusters) every uncovered set of at most four points contains a declared set',
        'aggregation': {'hist4': agg['hist4'], 'hist_small': agg['hist_small'], 'declared_sets_total': agg['declared_sets'], 'candidates': cands},
        'direct_witnesses': wit,
        'statistics': stats,
        'vertices_done': done if partial else 'all',
        'inputs_sha256': {
            'completion_points.json': sha(COMPLETION), 'swap_certificate.json': sha(SWAP_CERT), 'pair_certificate.json': sha(PAIR_CERT),
            'ambient_w3_edges.json': sha(AMBIENT), 'triple_certificate.json': sha(TRIPLE_CERT),
        },
    }
    outf.write_text(json.dumps(cert))
    print(f'wrote {outf} ({outf.stat().st_size/1e6:.2f} MB): rows {stats["rows"]}, declared unsat {stats["unsat"]} budget {stats["budget"]}, candidates {len(cands)}, witnesses {len(wit)}')


if __name__ == '__main__':
    main()
