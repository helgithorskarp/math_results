"""Separate tensor-basis reconstruction of every full coupled graph and witness.

Does not import build.py, field.py, contacts.py or their graph/filter functions.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
from math import isqrt
import argparse, copy, json, sys, time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'hadwiger_nelson_heptagon_moser_sum'
sys.path.insert(0, str(PARENT))
import audit as A
import contacts_audit as V

MODULI = ((2017, 54, 822), (2143, 325, 207))


def modular_map(parameters):
    prime, t, s = parameters
    assert prime > 42 and all(prime % k for k in range(2, isqrt(prime)+1))
    z, omega, w = pow(t, 6, prime), pow(t, 7, prime), (1+s)*pow(2, -1, prime) % prime
    assert z != 1 and sum(pow(z, j, prime) for j in range(7)) % prime == 0
    assert (omega*omega-omega+1) % prime == (w*w-w+3) % prime == 0
    weights = [pow(z, i % 6, prime)*pow(omega, i//6 % 2, prime)*pow(w, i//12, prime) % prime
               for i in range(24)]
    return lambda row: sum(x*y for x, y in zip(row, weights)) % prime


def exact_edges(points, d, maps):
    # Integral homomorphisms can only reject nonzero norm-minus-d^2 elements.
    conj = list(map(A.conjugate, points))
    images = [[(f(p), f(c)) for p, c in zip(points, conj)] for f in maps]
    out = []; survivors = 0; target = A.scale(A.O, d*d)
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            keep = True
            for (prime, _, _), values in zip(MODULI, images):
                a, b = values[i]; c, e = values[j]
                if ((a-c)*(b-e)-d*d) % prime:
                    keep = False; break
            if keep:
                survivors += 1
                if A.norm(A.sub(points[i], points[j])) == target: out.append([i, j])
    return out, survivors


def validate_certificate(cert, size, he, me):
    assert A.proper(cert['H_colouring'], he, 21)
    assert A.proper(cert['baseline_M_colouring'], me, 7)
    qs = cert['rotated_M_colourings']
    assert qs and all(A.proper(q, me, 7) for q in qs)
    assert len({tuple(q) for q in qs}) == len(qs)
    indices = cert['case_M_indices']
    assert len(indices) == size
    assert all(type(i) is int and 0 <= i < len(qs) for i in indices)


def descend(cert, case, labels, n, edges):
    p = cert['H_colouring']; qs = [cert['baseline_M_colouring'],
                                  cert['rotated_M_colourings'][cert['case_M_indices'][case]]]
    fibres = [[] for _ in range(n)]
    assert len(labels) == 2 and all(len(block) == 147 for block in labels)
    for k in range(2):
        for h in range(21):
            for m in range(7):
                v = labels[k][7*h+m]
                assert type(v) is int and 0 <= v < n
                fibres[v].append(p[h] ^ qs[k][m])
    assert all(fibre and len(set(fibre)) == 1 for fibre in fibres)
    row = [fibre[0] for fibre in fibres]
    assert A.proper(row, edges, n)
    return row


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args(); start = time.perf_counter()
    expected = json.loads((HERE/'expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (HERE/'certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert len(raw) == expected['certificate_bytes'] and sha256(raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(raw); H, M = V.factors()
    assert len(set(H)) == 21 and len(set(M)) == 7 and M[0] == A.Z
    he, me = V.unit_edges(H, 42), V.unit_edges(M, 42)
    assert len(he) == 42 and len(me) == 11
    # Independently construct all unit-difference ratios, without importing the C7 certificate.
    diffs = []
    for points, edges in ((H, he), (M, me)):
        diff = {A.sub(points[i], points[j]) for i, j in edges}
        diffs.append(diff | {A.scale(x, -1) for x in diff})
    assert tuple(map(len, diffs)) == (84, 14)
    angles = {V.canonical(A.mul(a, A.conjugate(b)), 42**2) for a in diffs[0] for b in diffs[1]}
    assert len(angles) == 252
    rotation_raw = (args.work/'rotations.json').read_bytes()
    assert sha256(rotation_raw).hexdigest() == expected['rotation_stream_sha256']
    rotation_rows = json.loads(rotation_raw); decoded = list(map(V.decode, rotation_rows))
    assert len(decoded) == len(set(decoded)) == 252 and set(decoded) == angles
    assert all(A.norm(a) == A.scale(A.O, d*d) for a, d in decoded)
    validate_certificate(cert, 252, he, me)
    # Fixing the triangle 0,1,2 to distinct named colours is without loss in a 3-colouring.
    assert [0,1] in me and [0,2] in me and [1,2] in me
    assert not any(A.proper([0,1,2]+list(tail), me, 7) for tail in product(range(3), repeat=4))
    maps = [modular_map(par) for par in MODULI]
    hist = Counter(); stream = sha256(); supports = set()
    pairs = colour_checks = cross_checks = survivors = 0
    for case, (rn, rd) in enumerate(rotation_rows):
        graph_raw = (args.work/f'{case:03}.graph.json').read_bytes(); stream.update(graph_raw)
        g = json.loads(graph_raw); assert g['r'] == [rn, rd]
        d = 42*rd; gd = g['denominator']; assert type(gd) is int and gd > 0 and d % gd == 0
        points = []
        for point in g['points']:
            V.canonical(point, gd)
            points.append(A.scale(A.decode(point), d//gd))
        hh = [A.scale(h, rd) for h in H]
        blocks = [[A.scale(m, rd) for m in M], [A.mul(A.decode(rn), m) for m in M]]
        formal = [[A.add(h, m) for h in hh for m in block] for block in blocks]
        assert set(points) == set(formal[0]) | set(formal[1]) and len(set(points)) == len(points)
        index = {point: i for i, point in enumerate(points)}
        labels = [[index[point] for point in block] for block in formal]
        assert labels == g['labels']
        sets = list(map(set, labels)); overlap = sorted(sets[0] & sets[1])
        assert overlap == g['overlap'] and all(index[h] in overlap for h in hh)
        edges, count = exact_edges(points, d, maps)
        assert edges == g['edges']
        component = [[e for e in edges if set(e) <= ss] for ss in sets]
        assert component == g['component_edges']
        cross = [e for e in edges if not any(set(e) <= ss for ss in sets)]
        assert cross == g['new_cross_edges']
        row = descend(cert, case, labels, len(points), edges)
        assert len(set(labels[0][:7])) == 7
        es = set(map(tuple, edges))
        assert all(tuple(sorted((labels[0][i], labels[0][j]))) in es for i, j in me)
        if case == 0:
            control = (labels, len(points), edges, row)
        hist[len(points), len(edges), len(cross), len(overlap)] += 1
        supports.add(frozenset(V.canonical(p, d) for p in points))
        pairs += len(points)*(len(points)-1)//2
        colour_checks += len(edges); cross_checks += len(cross); survivors += count
        print(json.dumps({'case': case, 'status': 'FULL GEOMETRY AND FIXED BASELINE EXTENSION VERIFIED'}), flush=True)
    assert stream.hexdigest() == expected['graph_stream_sha256']
    assert [list(k)+[v] for k, v in sorted(hist.items())] == expected['case_histogram']
    assert len(supports) == expected['distinct_supports']
    assert pairs == expected['full_pair_tests'] and colour_checks == expected['colour_edge_checks']
    assert cross_checks == expected['new_cross_edge_occurrences']
    assert len(cert['rotated_M_colourings']) == expected['rotated_M_colourings_used']
    assert expected['fixed_baseline_colourings'] == 1
    # Controls reject incomplete, malformed and invalid colour witnesses.
    rejected = 0; mutations = []
    bad = copy.deepcopy(cert); bad['case_M_indices'].pop(); mutations.append(bad)
    bad = copy.deepcopy(cert); bad['case_M_indices'][0] = -1; mutations.append(bad)
    bad = copy.deepcopy(cert); bad['H_colouring'] = [0]*21; mutations.append(bad)
    bad = copy.deepcopy(cert); bad['baseline_M_colouring'][0] = 4; mutations.append(bad)
    for bad in mutations:
        try: validate_certificate(bad, 252, he, me)
        except AssertionError: rejected += 1
    labels, n, edges, row = control
    bad = copy.deepcopy(labels); bad[0][0] = n
    try: descend(cert, 0, bad, n, edges)
    except AssertionError: rejected += 1
    bad_row = row.copy(); bad_row[edges[0][0]] = bad_row[edges[0][1]]
    assert not A.proper(bad_row, edges, n); rejected += 1
    assert rejected == 6
    out = {'status': expected['status'], 'rotations_independently_reenumerated': 252,
           'complete_supports_and_edge_lists_compared': 252, 'formal_labels_compared': 252*294,
           'full_pair_tests': pairs, 'colour_edge_checks': colour_checks,
           'new_cross_edge_inequalities_checked': cross_checks,
           'modular_survivors_rechecked_exactly': survivors,
           'modular_false_positives': survivors-colour_checks, 'distinct_supports': len(supports),
           'same_baseline_colouring_extended_in_every_case': True,
           'spindle_embeddings_checked': 252, 'normalized_three_colour_assignments_rejected': 81,
           'invalid_inputs_or_witnesses_rejected': rejected, 'moduli': MODULI,
           'native_solver_calls': 0, 'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
