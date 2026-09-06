"""Exact elimination supergraphs for the126 remaining unit-M contact equations."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
from math import isqrt
import argparse, json, time
import field as F

MODULI = ((1093, 275, 128), (1303, 272, 125))  # prime, image of t, image of s


def modular_map(parameters):
    p, t, s = parameters
    assert p > 42 and all(p % k for k in range(2, isqrt(p)+1))
    assert pow(t, 42, p) == 1 and all(pow(t, 42//ell, p) != 1 for ell in (2, 3, 7))
    assert sum(v*pow(t, i, p) for i, v in enumerate(F.K.PHI)) % p == 0
    assert (s*s+11) % p == 0
    weights = [pow(t, i % 12, p)*(s if i >= 12 else 1) % p for i in range(24)]
    return lambda a: sum(x*y for x, y in zip(a, weights)) % p


def determinant_residual(U, n, V, q):
    S = F.add(F.mul(q, U), F.mul(n, V))
    D = F.sub(F.mul(U, F.conjugate(V)), F.mul(F.conjugate(U), V))
    return F.sub(F.norm(S), F.norm(D))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    H, M, d = F.construction()
    unit = F.scale(F.ONE, d*d)
    here = Path(__file__).resolve().parent
    inherited = json.loads((here/'dual_neighbour_certificate.json').read_text())
    hpairs = [inherited['nonunit_H_pair_C7_orbits'][k][0]
              for k in inherited['uncovered_nonunit_orbit_indices']]
    bpairs = inherited['unit_M_difference_labels']
    assert len(hpairs) == 9 and len(bpairs) == 14
    maps = [modular_map(parameters) for parameters in MODULI]
    hd = {(i, j): F.sub(H[i], H[j]) for i, j in combinations(range(21), 2)}
    md = {(i, j): F.sub(M[i], M[j]) for i in range(7) for j in range(7) if i != j}
    hn, mn = ({pair: F.norm(x) for pair, x in points.items()} for points in (hd, md))
    he = [pair for pair in hd if hn[pair] == unit]
    me = [pair for pair in md if pair[0] < pair[1] and mn[pair] == unit]
    factor = sorted({(7*i+m, 7*j+m) for i, j in he for m in range(7)} |
                    {(7*h+i, 7*h+j) for h in range(21) for i, j in me})
    assert len(factor) == 525
    pcolour = json.loads((F.PARENT/'potentials.json').read_text())[0]
    assert len(pcolour) == 21 and all(pcolour[i] != pcolour[j] for i, j in he)
    qrows = [(0,)+tail for tail in product(range(4), repeat=6)
             if all(((0,)+tail)[i] != ((0,)+tail)[j] for i, j in me)]
    assert len(qrows) == 96
    mapped_h = {ij: [(f(x), f(F.conjugate(x))) for f in maps] for ij, x in hd.items()}
    mapped_m = {ij: [(f(x), f(F.conjugate(x))) for f in maps] for ij, x in md.items()}
    mixed = []
    for (i, j), x in hd.items():
        for (p, q), y in md.items():
            Q = F.sub(unit, F.add(hn[i, j], mn[p, q]))
            values = []
            for parameters, f, (xx, xb), (yy, yb) in zip(MODULI, maps, mapped_h[i, j], mapped_m[p, q]):
                mod = parameters[0]
                values.append((xb*yy % mod, xx*yb % mod, f(Q)))
            mixed.append(((7*i+p, 7*j+q), x, y, Q, values))
    assert len(mixed) == 8820
    qpool, cases, graphs = [], [], []
    extra_total = survivors = 0
    vcache = {}
    for hi, hj in hpairs:
        a = F.sub(H[hj], H[hi])
        n = F.norm(a)
        assert a != F.ZERO and n != unit
        for bi, bj in bpairs:
            b = F.sub(M[bi], M[bj])
            assert F.norm(b) == unit
            U = F.mul(F.conjugate(a), b)
            ub = F.conjugate(U)
            mapped = [(f(U), f(ub), f(n)) for f in maps]
            extra = []
            for pair, x, y, Q, values in mixed:
                possible = True
                for parameters, (u, uu, nn), (v, vv, qq) in zip(MODULI, mapped, values):
                    mod = parameters[0]
                    ss, sb = (qq*u+nn*v) % mod, (qq*uu+nn*vv) % mod
                    delta = (u*vv-uu*v) % mod
                    if (ss*sb+delta*delta) % mod:
                        possible = False
                        break
                if not possible: continue
                survivors += 1
                if (x, y) not in vcache: vcache[x, y] = F.mul(F.conjugate(x), y)
                if determinant_residual(U, n, vcache[x, y], Q) == F.ZERO:
                    extra.append(pair)
            extra.sort()
            extra_total += len(extra)
            qcolour = next((q for q in qrows if all(
                (pcolour[i//7] ^ q[i % 7]) != (pcolour[j//7] ^ q[j % 7])
                for i, j in extra)), None)
            assert qcolour is not None, ('No supplied XOR certificate', hi, hj, bi, bj, extra)
            if qcolour not in qpool: qpool.append(qcolour)
            edges = sorted(factor+extra)
            row = [pcolour[i] ^ qcolour[j] for i in range(21) for j in range(7)]
            assert all(row[i] != row[j] for i, j in edges)
            cases.append([hi, hj, bi, bj, qpool.index(qcolour), extra])
            graphs.append({'event': [hi, hj, bi, bj], 'vertices': 147, 'edges': edges})
    assert len(cases) == 126
    certificate = {'case_row_format': ['hi', 'hj', 'mi', 'mj', 'M_colouring_index', 'extra_edges'],
                   'H_colouring': pcolour, 'M_colourings': qpool, 'cases': cases}
    raw = (json.dumps(certificate, separators=(',', ':'))+'\n').encode()
    graph_raw = (json.dumps(graphs, separators=(',', ':'))+'\n').encode()
    (args.out/'certificate.json').write_bytes(raw)
    (args.out/'graphs.json').write_bytes(graph_raw)
    result = {'status': 'ALL MIXED CONTACTS WITH A UNIT M DIFFERENCE ARE FOUR-CHROMATIC',
              'cohort_equations': len(cases), 'formal_vertices_per_envelope': 147,
              'factor_edges_per_envelope': len(factor), 'mixed_pair_tests': len(mixed)*len(cases),
              'all_pair_tests_including_unmixed': 147*146//2*len(cases),
              'modular_survivors_rechecked_exactly': survivors, 'extra_envelope_edges_total': extra_total,
              'modular_false_positives': survivors-extra_total,
              'envelope_edge_histogram': dict(sorted(Counter(len(g['edges']) for g in graphs).items())),
              'colour_edge_checks': sum(len(g['edges']) for g in graphs),
              'H_colourings_used': 1, 'M_colourings_used': len(qpool),
              'remaining_possible_exception_bound': 6720, 'C7_possible_exception_orbit_bound': 960,
              'remaining_event_equations': 168*20, 'remaining_C7_representative_equations': 24*20,
              'certificate_sha256': sha256(raw).hexdigest(),
              'envelope_graph_stream_sha256': sha256(graph_raw).hexdigest(),
              'contact_roots_extracted': False, 'actual_root_graphs_constructed': 0,
              'remaining_both_nonunit_events_enumerated': False, 'native_solver_calls': 0}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
