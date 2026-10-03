"""A-anchored dense producer, with complete two/three-bridge case coverage."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse, json
from poly import add, mul, neg, bezout, bernstein

A = [(0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11)]
B = [(1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12)]
CORE = {0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12}
TYPES = ('S', 'UV', 'VW', 'UVW')
R, DEN = [F(0), F(1)], [F(2), F(-1)]
LO, HI = F(28, 39), F(1186, 1593)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def boundary(tris):
    count = Counter(tuple(sorted(e)) for t in tris for e in combinations(t, 2))
    return sorted(e for e, n in count.items() if n == 1)


def flip(x, y, z):
    return [add(mul(R, add(a, b)), neg(c)) for a, b, c in zip(x, y, z)]


def inner_num(x, y):
    total, same = [], []
    for i in range(3):
        for j in range(3):
            term = mul(x[i], y[j])
            total = add(total, term)
            if i == j:
                same = add(same, term)
    return add(mul(DEN, same), mul(R, add(total, neg(same))))


def gap(x, y):
    return add(inner_num(x, y), neg(R))


def core_points(which):
    if which == 'A':
        p = {0: [[F(1)], [], []], 5: [[], [F(1)], []], 11: [[], [], [F(1)]]}
        p[6] = flip(p[0], p[11], p[5])
        p[7] = flip(p[0], p[5], p[11])
        p[9] = flip(p[5], p[11], p[0])
    elif which == 'B':
        p = {1: [[F(1)], [], []], 2: [[], [F(1)], []], 4: [[], [], [F(1)]]}
        p[8] = flip(p[2], p[4], p[1])
        p[10] = flip(p[1], p[2], p[4])
        p[12] = flip(p[1], p[10], p[2])
    else:
        raise ValueError('core selector')
    return p


def path(case):
    kind, a, aa, b, bb = case
    need(kind in TYPES, 'path type')
    if kind == 'S':
        return [(a, aa, b), (a, b, bb)]
    if kind == 'UV':
        return [(a, aa, 13), (a, b, 13), (a, b, bb)]
    if kind == 'VW':
        return [(a, aa, b), (a, b, 13), (b, bb, 13)]
    return [(a, aa, 13), (a, b, 13), (b, bb, 13)]


def finish_cluster(p, triangles, edge, outside):
    root = next(i for i, t in enumerate(triangles) if set(edge) <= set(t))
    new = next(v for v in triangles[root] if v not in edge)
    need(new not in p, 'fresh cluster root corner')
    p[new] = flip(p[edge[0]], p[edge[1]], p[outside])
    done = {root}
    while len(done) < 4:
        advanced = False
        for i, t in enumerate(triangles):
            if i in done:
                continue
            parents = [j for j in done if len(set(t) & set(triangles[j])) == 2]
            if not parents:
                continue
            need(len(parents) == 1, 'single tree parent')
            parent = triangles[parents[0]]
            shared = sorted(set(t) & set(parent))
            old = next(v for v in parent if v not in shared)
            new = next(v for v in t if v not in shared)
            need(new not in p, 'fresh cluster child corner')
            p[new] = flip(p[shared[0]], p[shared[1]], p[old])
            done.add(i)
            advanced = True
        need(advanced, 'complete cluster propagation')


def construct(case, full_gram=False):
    kind, a, aa, b, bb = case
    ae, be = tuple(sorted((a, aa))), tuple(sorted((b, bb)))
    need(ae in boundary(A) and be in boundary(B), 'literal boundary case')
    p = core_points('A')
    previous = next(t for t in A if set(ae) <= set(t))
    bridge = path(case)
    for triangle in bridge:
        shared = sorted(set(previous) & set(triangle))
        need(len(shared) == 2, 'bridge edge')
        old = next(v for v in previous if v not in shared)
        new = next(v for v in triangle if v not in shared)
        need(new not in p, 'fresh bridge corner')
        p[new] = flip(p[shared[0]], p[shared[1]], p[old])
        previous = triangle
    outside = next(v for v in bridge[-1] if v not in be)
    finish_cluster(p, B, be, outside)
    labels = CORE if kind == 'S' else CORE | {13}
    edges = sorted({tuple(sorted(e)) for t in A + B + bridge for e in combinations(t, 2)})
    need(set(p) == labels and len(edges) == (21 if kind == 'S' else 23), 'entire patch label/edge set')
    need(all(not add(inner_num(v, v), neg(DEN)) for v in p.values()), 'unit identities')
    need(all(not gap(p[i], p[j]) for i, j in edges), 'patch contact identities')
    gram = [[inner_num(p[i], p[j]) for j in sorted(labels)] for i in sorted(labels)] if full_gram else None
    return gram, gap(p[7], p[12]), gap(p[9], p[10])


def cases():
    return [(kind, a, next(x for x in ae if x != a), b, next(x for x in be if x != b))
            for kind in TYPES for ae in boundary(A) for be in boundary(B) for a in ae for b in be]


def encode(p):
    return [str(x) for x in p]


def core_certificates():
    answer = []
    for name, triangles in [('A', A), ('B', B)]:
        p = core_points(name)
        prescribed = {tuple(sorted(e)) for t in triangles for e in combinations(t, 2)}
        for i, j in combinations(sorted(p), 2):
            value = gap(p[i], p[j])
            if (i, j) in prescribed:
                need(not value, 'known internal contact')
            else:
                coefficients = bernstein(value, LO, HI)
                need(all(x < 0 for x in coefficients), 'strict internal noncontact')
                answer.append({'cluster': name, 'pair': [i, j], 'gap': encode(value),
                               'Bernstein': encode(coefficients)})
    need(len(answer) == 12, 'twelve internal noncontacts')
    return answer


def build():
    need(F(2) * F(14, 25) / (1 + F(14, 25)) == LO, 'lower parameter transform')
    need(F(2) * F(593, 1000) / (1 + F(593, 1000)) == HI < 1, 'upper transform/positive denominator')
    collection, rows, lookup = [], [], {}
    gap_degree = witness_degree = 0
    for case in cases():
        _, f, g = construct(case)
        h, u, v = bezout(f, g)
        coefficients = bernstein(h, LO, HI)
        need(all(x > 0 for x in coefficients) or all(x < 0 for x in coefficients), 'root-free common-root witness')
        key = tuple(h)
        if key not in lookup:
            lookup[key] = len(collection)
            collection.append({'polynomial': encode(h), 'Bernstein': encode(coefficients)})
        rows.append(list(case) + [lookup[key]])
        gap_degree = max(gap_degree, len(f) - 1, len(g) - 1)
        witness_degree = max(witness_degree, len(u) - 1, len(v) - 1)
    need(len(rows) == 576 and len({tuple(r[:5]) for r in rows}) == 576, 'full unique576 rows')
    return {'format': 'eleven-triangle-bridge-v1', 'cosine_closed_band': ['14/25', '593/1000'],
            'r_closed_band': [str(LO), str(HI)], 'A_triangles': [list(t) for t in A],
            'B_triangles': [list(t) for t in B], 'cross_contacts': [[7, 12], [9, 10]],
            'fresh_corner_label': 13, 'types': list(TYPES),
            'row_fields': ['type', 'a', 'a_prime', 'b', 'b_prime', 'root_free_polynomial_index'],
            'rows': rows, 'root_free_polynomials': collection, 'core_noncontacts': core_certificates(),
            'maximum_gap_degree': gap_degree, 'maximum_Bezout_witness_degree': witness_degree}


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    args = parser.parse_args()
    record = build()
    need(json.loads((Path(__file__).parent / 'CERTIFICATE.json').read_text()) == record, 'whole fresh/included certificate binding')
    if args.emit:
        args.emit.write_text(canonical(record))
    print(json.dumps({'status': 'complete', 'cases': 576, 'case_types': dict(Counter(r[0] for r in record['rows'])),
                      'root_free_polynomials': len(record['root_free_polynomials']), 'Bezout_identities': 576,
                      'norm_identities': 144 * 12 + 432 * 13, 'patch_contact_identities': 144 * 21 + 432 * 23,
                      'strict_internal_noncontacts': 12, 'maximum_gap_degree': record['maximum_gap_degree'],
                      'maximum_Bezout_witness_degree': record['maximum_Bezout_witness_degree']}, sort_keys=True))


if __name__ == '__main__':
    main()
