#!/usr/bin/env python3
"""Exact finite obligations for the cap theorem and auxiliary obstruction."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def add(*vectors):
    return [sum(x) for x in zip(*vectors)]


def negative(v):
    return [-x for x in v]


def rank(rows):
    a = [[Q(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        scale = a[r][c]
        a[r] = [x/scale for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def check_angles(data):
    one = [1, 0, 0, 0, 0, 0]
    a, b, c, d, e = [[int(i == j) for i in range(6)] for j in range(1, 6)]
    base = [a, b, c, d, e]+[add(one, negative(v)) for v in [a, b, c, d, e]]
    base += [add(one, negative(a), negative(c)), add(one, negative(b), negative(d)),
             add(one, one, negative(a), negative(b), negative(e)),
             add(one, one, negative(c), negative(d), negative(e))]
    need(data['base_nonnegative_forms'] == base, 'incorrect angle premises')
    seen = set()
    count = nonzero = 0
    for entry in data['branches']:
        t, f = entry['total_choice'], entry['first_choice']
        need((t, f) in set(product(range(2), repeat=2)) and (t, f) not in seen,
             'bad or repeated max branch')
        seen.add((t, f))
        totals = [e, add(a, b)]
        total = totals[t]
        firsts = [a, add(total, d, negative(one))]
        first = firsts[f]
        second = add(total, negative(first))
        branches = [add(total, negative(totals[1-t])),
                    add(first, negative(firsts[1-f]))]
        premises = base+branches
        targets = [add(first, negative(a)), add(one, negative(c), negative(first)),
                   add(second, negative(b)), add(one, negative(d), negative(second)),
                   add(total, negative(e)), add(one, one, negative(e), negative(total))]
        need(entry['total'] == total and entry['first'] == first
             and entry['second'] == second and entry['branch_nonnegative_forms'] == branches
             and entry['target_forms'] == targets, 'wrong max-branch reduction')
        need(len(entry['farkas_coefficients']) == 6, 'missing target certificate')
        for target, certificate in zip(targets, entry['farkas_coefficients']):
            result = [Q(0)]*6
            indices = set()
            for index, coefficient in certificate:
                coefficient = Q(coefficient)
                need(0 <= index < len(premises) and index not in indices
                     and coefficient >= 0, 'invalid nonnegative dual multiplier')
                indices.add(index)
                result = add(result, [coefficient*x for x in premises[index]])
                nonzero += 1
            need(result == target, 'Farkas coefficient identity failed')
            count += 1
    need(seen == set(product(range(2), repeat=2)), 'incomplete max-branch coverage')
    return {'max_branches': len(seen), 'farkas_identities': count, 'dual_terms': nonzero}


# Q(sqrt(2)) for the exact four-cap motion control. No floating conversion.
def q2(x=0, y=0):
    return Q(x), Q(y)


def qadd(x, y):
    return x[0]+y[0], x[1]+y[1]


def qneg(x):
    return -x[0], -x[1]


def qmul(x, y):
    return x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def qscale(x, c):
    return x[0]*c, x[1]*c


def qsign(x):
    a, b = x
    if b == 0:
        return (a > 0)-(a < 0)
    if a == 0 or (a > 0) == (b > 0):
        return (b > 0)-(b < 0)
    difference = a*a-2*b*b
    need(difference != 0, 'irrational square root unexpectedly rational')
    return ((a > 0)-(a < 0)) if difference > 0 else ((b > 0)-(b < 0))


def qdot(x, y):
    result = q2()
    for a, b in zip(x, y):
        result = qadd(result, qmul(a, b))
    return result


def check_hemisphere(data):
    normals = data['normal_vectors']
    offsets = list(map(Q, data['raw_offsets']))
    w = data['hemisphere_vector']
    x = [[Q(a) for a in row] for row in data['vertices']]
    expected_y = [[Q(a) for a in row] for row in data['images']]
    need(normals == [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [1, -1, 0]]
         and offsets == [0, 0, 0, Q(11, 2)] and w == [1, 1, -1], 'wrong fixture normals')
    need(x == [[0, 0, 0], [-1, -1, 0], [-1, 0, 1], [0, -1, 1],
               [1, -2, 5], [-2, -5, -1], [-5, 1, 2], [-4, -10, 7]],
         'wrong cap fixture')
    need(dot(w, w) > 0 and all(dot(v, w) >= 0 for v in normals), 'hemisphere witness failed')
    t = [[dot(v, point)-b for v, b in zip(normals, offsets)] for point in x]
    pairs = set()
    for i, j, coefficient in data['separators']:
        coefficient = Q(coefficient)
        need(i != j and 0 <= i < 4 and 0 <= j < 4 and coefficient > 0,
             'invalid cap separator')
        pairs.add(tuple(sorted((i, j))))
        need(all(row[i]+coefficient*row[j] <= 0 for row in t), 'cap separator failed')
    need(pairs == set(combinations(range(4), 2)), 'incomplete cap separation')
    slopes = [[q2(0, Q(z, 6)) for z in row]
              for row in [(1, 1, 2), (1, -2, -1), (-2, 1, -1)]]
    slopes.append([q2(Q(1, 2)), q2(Q(-1, 2)), q2()])
    for v, h in zip(normals, slopes):
        need(qdot(h, list(map(q2, w))) == q2(), 'auxiliary slope leaves common plane')
        need(qdot(h, h) == q2(1/Q(dot(v, v))), 'wrong auxiliary slope norm')
        projected = add(v, [-Q(dot(v, w), dot(w, w))*a for a in w])
        for j, k in combinations(range(3), 2):
            need(qscale(h[j], projected[k]) == qscale(h[k], projected[j]),
                 'slope not parallel to hemisphere projection')
        need(qsign(qdot(h, list(map(q2, projected)))) > 0, 'wrong projection orientation')
    y, physical, auxiliary, labels = [], [], [], []
    for point, row in zip(x, t):
        active = [i for i, val in enumerate(row) if val > 0]
        need(len(active) <= 1, 'overlapping cap at a vertex')
        i = active[0] if active else -1
        labels.append(i)
        if i == -1:
            physical.append([Q(0)]*3)
            auxiliary.append([q2()]*3)
        else:
            physical.append([row[i]*a/Q(dot(normals[i], normals[i])) for a in normals[i]])
            auxiliary.append([qscale(a, row[i]) for a in slopes[i]])
        y.append(add(point, [-2*a for a in physical[-1]]))
    need(y == expected_y and labels == data['cap_labels'], 'incorrect reflected endpoint')
    need(set(labels) == {-1, 0, 1, 2, 3}, 'all four caps and the core must be active')
    records = []
    tight = 0
    for i, j in combinations(range(8), 2):
        displacement = add(x[i], negative(x[j]))
        v = add(physical[i], negative(physical[j]))
        h = [qadd(a, qneg(b)) for a, b in zip(auxiliary[i], auxiliary[j])]
        energy = dot(displacement, v)-dot(v, v)
        delta = qadd(qdot(h, h), q2(-dot(v, v)))
        initial = dot(displacement, displacement)
        linear = qscale(qadd(delta, q2(-energy)), 4)
        quadratic = qscale(delta, -4)
        need(qsign(linear) <= 0 and qsign(qadd(linear, qscale(quadratic, 2))) <= 0,
             'pair derivative positive during motion')
        end = add(y[i], negative(y[j]))
        need(qadd(q2(initial), qadd(linear, quadratic)) == q2(dot(end, end)),
             'full-time polynomial endpoint mismatch')
        tight += (initial == dot(end, end))
        records.append([i, j, str(initial), [str(z) for z in linear],
                        [str(z) for z in quadratic]])
    paired = rank([add(point, negative(x[0]))+add(out, negative(y[0]))
                   for point, out in zip(x[1:], y[1:])])
    need(paired == 6 and rank(normals) == 3, 'rank control failed')
    # Exact pole/boundary control for the projection lemma.
    pole_normals = [[0, 0, 1], [1, 0, 0], [-1, 0, 0], [0, 1, 0]]
    pole_u = [[0, 1], [1, 0], [-1, 0], [0, 1]]
    need(all(dot(pole_u[i], pole_u[j]) <= 1+2*dot(pole_normals[i], pole_normals[j])
             for i, j in combinations(range(4), 2)), 'polar/boundary control failed')
    tetra = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    square = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    need(add(*tetra) == [0, 0, 0] and rank(tetra) == 3, 'tetrahedron hemisphere obstruction failed')
    need(all(dot(square[i], square[j]) <= 1+Q(2*dot(tetra[i], tetra[j]), 3)
             for i, j in combinations(range(4), 2)), 'tetrahedral weak certificate failed')
    gram = [[Q(dot(a, b), 3) for b in tetra] for a in tetra]
    need(rank(gram) == 3, 'stronger four-vector condition requires rank three')
    return {'vertices': 8, 'active_caps': 4, 'separators': len(pairs),
            'pair_polynomials': len(records), 'tight_pairs': tight,
            'paired_rank': paired, 'polynomials_sha256': digest(records),
            'polar_and_tetrahedral_controls': 'PASS'}


# Z[phi], represented by (a,b) for a+b*phi, phi^2=phi+1.
def pmul(x, y):
    a, b = x
    c, d = y
    return a*c+b*d, a*d+b*c+b*d


def pdot(x, y):
    result = (0, 0)
    for a, b in zip(x, y):
        result = tuple(add(result, pmul(a, b)))
    return result


def edge_chain(triples):
    chain = Counter()
    for a, b, c in triples:
        for u, v in [(a, b), (b, c), (c, a)]:
            chain[tuple(sorted((u, v)))] += 1 if u < v else -1
    return {edge: value for edge, value in chain.items() if value}


def check_icosahedron(data):
    vertices = data['vertices_phi_basis']
    expected = []
    for zero in range(3):
        for a, b in product([-1, 1], repeat=2):
            vector = [[0, 0] for _ in range(3)]
            vector[(zero+1) % 3] = [a, 0]
            vector[(zero+2) % 3] = [0, b]
            expected.append(vector)
    need(vertices == expected, 'wrong exact icosahedral coordinates')
    need(all(pdot(v, v) == (2, 1) for v in vertices), 'wrong common norm')
    need(all(pdot(vertices[i], vertices[j]) in {(0, 1), (0, -1), (-2, -1)}
             for i, j in combinations(range(12), 2)), 'unexpected distinct-normal product')
    anti = data['antipodes']
    need(len(anti) == 12 and all(anti[anti[i]] == i and anti[i] != i for i in range(12)),
         'antipodal pairing invalid')
    need(all(all(add(a, b) == [0, 0] for a, b in zip(vertices[i], vertices[anti[i]]))
             for i in range(12)), 'antipodal coordinates fail')
    edges = {ij for ij in combinations(range(12), 2) if pdot(vertices[ij[0]], vertices[ij[1]]) == (0, 1)}
    need(edges == set(map(tuple, data['edges'])) and len(edges) == 30, 'edge completeness failed')
    faces = {t for t in combinations(range(12), 3) if all(e in edges for e in combinations(t, 2))}
    need(faces == set(map(tuple, data['faces'])) and len(faces) == 20, 'triangle completeness failed')
    cycle = data['cycle']
    need(len(cycle) == len(set(cycle)) == 10, 'wrong cycle')
    need(all(anti[cycle[i]] == cycle[(i+5) % 10] for i in range(10)), 'antipodal half-shift failed')
    need(all(tuple(sorted((cycle[i], cycle[(i+1) % 10]))) in edges for i in range(10)),
         'cycle uses a nonedge')
    disk = data['disk_triangles']
    need(len(disk) == 10 and len(set(tuple(sorted(t)) for t in disk)) == 10,
         'incorrect disk size or repeated face')
    need(all(tuple(sorted(t)) in faces for t in disk), 'disk triangle has a wrong dot product')
    boundary = Counter()
    for i, a in enumerate(cycle):
        b = cycle[(i+1) % 10]
        boundary[tuple(sorted((a, b)))] += 1 if a < b else -1
    need(edge_chain(disk) == dict(boundary), 'oriented disk boundary is not the cycle')
    need(5*31**2 > 50**2 and Q(19, 100) < Q(9, 20)**2
         and Q(9, 2)-1 > 1+1, 'shallow-cap positive control failed')
    return {'normal_count': 12, 'antipodal_pairs': 6, 'edges': len(edges),
            'triangles': len(faces), 'disk_triangles': len(disk), 'cycle_length': len(cycle),
            'boundary_identity': 'PASS', 'strict_cosine_bound': 'phi/(phi+2)>1/4 since phi>1',
            'positive_cap_offset': '9/10', 'common_direction_R4_control': 'PASS'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def audit(data):
    need(data['schema'] == 'gaussian-cap-auxiliary-certificates-v1', 'unknown schema')
    return {'schema': 'gaussian-cap-exact-audit-v1', 'angles': check_angles(data['angles']),
            'hemisphere': check_hemisphere(data['hemisphere']),
            'icosahedron': check_icosahedron(data['icosahedron']),
            'certificate_canonical_sha256': digest(data)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=HERE/'CERTIFICATE.json')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    record = audit(json.loads(args.certificate.read_text()))
    if args.write_expected:
        (HERE/'EXPECTED.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    need(record == json.loads((HERE/'EXPECTED.json').read_text()), 'expected audit record mismatch')
    print(json.dumps({'status': 'EXACT_CAP_CERTIFICATES_PASS', 'record_sha256': digest(record),
                      **record}, sort_keys=True))
