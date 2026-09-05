"""Alternate tensor-basis census and full geometric colouring-certificate audit.

Imports only the earlier independent audit arithmetic, not field.py or contacts.py.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import argparse, json, math, time
import audit as A


def canonical(a, d):
    assert isinstance(d, int) and d > 0 and len(a) == 24
    assert all(isinstance(v, int) for v in a)
    common = math.gcd(d, *a)
    return tuple(v//common for v in a), d//common


def decode(r):
    a, d = r
    canonical(a, d)  # Also reject malformed coordinate rows.
    return canonical(A.decode(a), d)


def multiply(x, y):
    return canonical(A.mul(x[0], y[0]), x[1]*y[1])


def factors():
    p = A.inverse_sine_numerator(4)
    q = A.scale(A.mul(A.sub(A.O, A.OMEGA), A.inverse_sine_numerator(1)), -1)
    r = A.scale(A.mul(A.OMEGA, A.inverse_sine_numerator(2)), -1)
    h = [A.mul(a, A.zp(j)) for a in (p, q, r) for j in range(7)]
    u, v = A.sub(h[7], h[0]), A.sub(h[14], h[0])
    directions = [u, v, A.add(u, v)]
    H = [A.scale(a, 6) for a in h]
    M = [A.Z]+[A.scale(a, 6) for a in directions]
    M += [A.add(A.scale(a, 4), A.scale(A.mul(A.W, a), 2)) for a in directions]
    return H, M


def unit_edges(points, denominator):
    target = A.scale(A.O, denominator**2)
    return [[i, j] for i, j in combinations(range(len(points)), 2)
            if A.norm(A.sub(points[i], points[j])) == target]


def check_colouring(p, q, fibres, edges, he, me):
    assert A.proper(p, he, 21) and A.proper(q, me, 7)
    row = []
    for fibre in fibres:
        values = {p[a]^q[b] for a, b in fibre}
        assert len(values) == 1
        row.append(values.pop())
    assert A.proper(row, edges, len(fibres))
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'contacts_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    certificate_raw = (here/'contacts_certificate.json').read_bytes()
    assert certificate_raw == (args.work/'certificate.json').read_bytes()
    certificate = json.loads(certificate_raw)
    H, M = factors()
    he, me = unit_edges(H, 42), unit_edges(M, 42)
    assert len(he) == 42 and len(me) == 11
    assert len(set(H)) == 21 and len(set(M)) == 7
    assert {A.mul(A.zp(1), h) for h in H} == set(H)
    # Collect directed differences from complete unordered edge lists.
    differences = []
    for points, edges in ((H, he), (M, me)):
        values = set()
        for a, b in edges:
            v = A.sub(points[a], points[b])
            values.add(v); values.add(A.scale(v, -1))
        differences.append(values)
    assert tuple(map(len, differences)) == (84, 14)
    # The two roots of Re(eta)=-1/2 are omega-1 and -omega.
    roots = (A.sub(A.OMEGA, A.O), A.scale(A.OMEGA, -1))
    angles = Counter()
    for a in differences[0]:
        for b in differences[1]:
            for eta in roots:
                value = A.mul(eta, A.mul(a, A.conjugate(b)))
                angles[canonical(value, 42**2)] += 1
    assert len(angles) == 252 and sum(angles.values()) == 2352
    rotation_raw = (args.work/'rotations.json').read_bytes()
    rotations = json.loads(rotation_raw)
    supplied = {decode(x['r']): x['multiplicity'] for x in rotations}
    assert len(supplied) == len(rotations) and supplied == angles
    assert sha256(rotation_raw).hexdigest() == expected['rotation_stream_sha256']
    assert len(certificate) == len(expected['cases']) == 36
    covered = set()
    for record in certificate:
        r = decode(record['r'])
        assert A.norm(r[0]) == A.scale(A.O, r[1]**2)
        orbit = {multiply((A.zp(j), 1), r) for j in range(7)}
        assert len(orbit) == 7 and not covered.intersection(orbit)
        covered.update(orbit)
    assert covered == set(angles)
    # The 96 q rows fixing only q0=0 are complete, by recursive propagation.
    q = [0]+[-1]*6
    qrows = []
    def extend(i):
        if i == 7:
            qrows.append(q.copy()); return
        for colour in range(4):
            q[i] = colour
            if all(q[a] < 0 or q[b] < 0 or q[a] != q[b] for a, b in me):
                extend(i+1)
        q[i] = -1
    extend(1)
    assert len(qrows) == 96
    assert not any(all(([0, 1, 2]+list(tail))[a] != ([0, 1, 2]+list(tail))[b]
                       for a, b in me) for tail in product(range(3), repeat=4))
    stream = sha256()
    histogram = Counter()
    pair_checks = edge_checks = fibre_checks = 0
    for i, record in enumerate(certificate):
        raw = (args.work/f'{i:02d}.graph.json').read_bytes()
        stream.update(raw)
        g = json.loads(raw)
        case = expected['cases'][i]
        assert sha256(raw).hexdigest() == case['graph_sha256']
        assert g['r'] == record['r'] == case['r']
        rn, rd = record['r']; denominator = 42*rd
        HH = [A.scale(h, rd) for h in H]
        MM = [A.mul(A.decode(rn), m) for m in M]
        gd = g['denominator']
        assert isinstance(gd, int) and gd > 0 and denominator % gd == 0
        factor_scale = denominator//gd
        def points_from(rows):
            for row in rows: canonical(row, gd)
            return [A.scale(A.decode(row), factor_scale) for row in rows]
        assert HH == points_from(g['H']) and MM == points_from(g['M'])
        points = points_from(g['points'])
        assert len(set(points)) == len(points) == case['vertices']
        assert set(points) == {A.add(h, m) for h in HH for m in MM}
        index = {point: j for j, point in enumerate(points)}
        fibres = [[] for _ in points]
        for a in range(21):
            for b in range(7): fibres[index[A.add(HH[a], MM[b])]].append([a, b])
        assert fibres == g['fibres']
        assert dict(sorted(Counter(map(len, fibres)).items())) == {int(k): v for k, v in case['collision_histogram'].items()}
        edges = unit_edges(points, denominator)
        assert edges == g['edges'] and he == g['H_edges'] and me == g['M_edges']
        factor = {tuple(sorted((index[A.add(HH[a], m)], index[A.add(HH[b], m)])))
                  for a, b in he for m in MM}
        factor |= {tuple(sorted((index[A.add(h, MM[a])], index[A.add(h, MM[b])])) )
                   for a, b in me for h in HH}
        edge_set = set(map(tuple, edges))
        assert factor <= edge_set
        assert sorted(factor) == list(map(tuple, g['factor_edges']))
        extra = sorted(edge_set-factor)
        assert extra == list(map(tuple, g['extra_edges']))
        assert (len(edges), len(factor), len(extra)) == (case['edges'], case['factor_edges'], case['extra_edges'])
        row = check_colouring(record['H_colouring'], record['M_colouring'], fibres, edges, he, me)
        embedding = [index[A.add(HH[0], m)] for m in MM]
        assert len(set(embedding)) == 7
        assert all(tuple(sorted((embedding[a], embedding[b]))) in edge_set for a, b in me)
        bad = row.copy(); bad[edges[0][0]] = bad[edges[0][1]]
        assert not A.proper(bad, edges, len(points))
        histogram[len(points), len(edges), len(extra)] += 1
        pair_checks += len(points)*(len(points)-1)//2
        edge_checks += len(edges)
        fibre_checks += sum(map(len, fibres))
        print(json.dumps({'case': i, 'vertices': len(points), 'edges': len(edges), 'status': 'GEOMETRY AND COLOURING VERIFIED'}), flush=True)
    assert stream.hexdigest() == expected['graph_stream_sha256']
    assert sha256(certificate_raw).hexdigest() == expected['certificate_sha256']
    assert pair_checks == expected['representative_sum_pair_checks']
    assert edge_checks == expected['witness_edge_checks']
    out = {'status': 'ALL252 ROTATIONS VERIFIED IN THE ALTERNATE BASIS',
           'rotations_compared_entrywise': len(angles), 'disjoint_C7_orbits': 36,
           'H_and_M_pair_checks': 231, 'sum_pair_checks': pair_checks,
           'formal_sum_representations_compared': fibre_checks, 'colour_edge_checks': edge_checks,
           'spindle_embeddings_checked': 36, 'normalized_spindle_colourings': len(qrows),
           'normalized_spindle_three_colour_cases': 81, 'invalid_colourings_rejected': 36,
           'case_histogram': [list(k)+[v] for k, v in sorted(histogram.items())],
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
