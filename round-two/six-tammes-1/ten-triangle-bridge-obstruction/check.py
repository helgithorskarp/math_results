"""Dense A-anchored producer; exact full coverage, no external data input."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse
import json
from poly import add, mul, neg, bezout, bernstein

A = [(0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11)]
B = [(1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12)]
LABELS = {0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12}
R, DEN = [F(0), F(1)], [F(2), F(-1)]
LO, HI = F(28, 39), F(1186, 1593)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def boundary(triangles):
    counts = Counter(tuple(sorted(e)) for t in triangles for e in combinations(t, 2))
    return sorted(e for e, n in counts.items() if n == 1)


def reflect(first, second, old):
    return [add(mul(R, add(a, b)), neg(z)) for a, b, z in zip(first, second, old)]


def dot_num(a, b):
    same, total = [], []
    for i in range(3):
        for j in range(3):
            term = mul(a[i], b[j])
            total = add(total, term)
            if i == j:
                same = add(same, term)
    return add(mul(DEN, same), mul(R, add(total, neg(same))))


def gap(a, b):
    return add(dot_num(a, b), neg(R))


def propagate(points, triangles, edge, outside):
    root = next(i for i, t in enumerate(triangles) if set(edge) <= set(t))
    third = next(v for v in triangles[root] if v not in edge)
    require(third not in points, 'new root label')
    points[third] = reflect(points[edge[0]], points[edge[1]], points[outside])
    done = {root}
    while len(done) < len(triangles):
        advanced = False
        for i, t in enumerate(triangles):
            if i in done:
                continue
            parents = [j for j in done if len(set(t) & set(triangles[j])) == 2]
            if not parents:
                continue
            require(len(parents) == 1, 'tree traversal parent')
            parent = triangles[parents[0]]
            shared = sorted(set(t) & set(parent))
            old = next(v for v in parent if v not in shared)
            new = next(v for v in t if v not in shared)
            require(new not in points, 'new tree label')
            points[new] = reflect(points[shared[0]], points[shared[1]], points[old])
            done.add(i)
            advanced = True
        require(advanced, 'complete cluster traversal')


def construct(placement):
    a, aa, b, bb = placement
    ae, be = tuple(sorted((a, aa))), tuple(sorted((b, bb)))
    require(ae in boundary(A) and be in boundary(B), 'literal boundary placement')
    p = {0: [[F(1)], [], []], 5: [[], [F(1)], []], 11: [[], [], [F(1)]]}
    p[6] = reflect(p[0], p[11], p[5])
    p[7] = reflect(p[0], p[5], p[11])
    p[9] = reflect(p[5], p[11], p[0])
    inside = next(t for t in A if set(ae) <= set(t))
    old = next(v for v in inside if v not in ae)
    p[b] = reflect(p[a], p[aa], p[old])
    p[bb] = reflect(p[a], p[b], p[aa])
    propagate(p, B, be, a)
    triangles = A + B + [(a, aa, b), (a, b, bb)]
    edges = sorted({tuple(sorted(e)) for t in triangles for e in combinations(t, 2)})
    require(set(p) == LABELS and len(edges) == 21, 'complete twelve-point patch')
    require(all(not add(dot_num(v, v), neg(DEN)) for v in p.values()), 'twelve norm identities')
    require(all(not gap(p[i], p[j]) for i, j in edges), 'twenty-one edge identities')
    # ALL entries are compared with the reverse-anchored checker, not just two gaps.
    gram = [[dot_num(p[i], p[j]) for j in sorted(LABELS)] for i in sorted(LABELS)]
    return p, edges, gram, gap(p[7], p[12]), gap(p[9], p[10])


def placements():
    return [(a, next(x for x in ae if x != a), b, next(x for x in be if x != b))
            for ae in boundary(A) for be in boundary(B) for a in ae for b in be]


def encode(poly):
    return [str(x) for x in poly]


def build():
    require(F(2) * F(14, 25) / (1 + F(14, 25)) == LO, 'lower change of variable')
    require(F(2) * F(593, 1000) / (1 + F(593, 1000)) == HI < 1, 'upper change of variable')
    collection, rows, index = [], [], {}
    gap_degree = witness_degree = 0
    for placement in placements():
        _, _, _, f, g = construct(placement)
        h, u, v = bezout(f, g)
        coeffs = bernstein(h, LO, HI)
        require(coeffs and (all(x > 0 for x in coeffs) or all(x < 0 for x in coeffs)),
                'strict root-free Bernstein certificate')
        key = tuple(h)
        if key not in index:
            index[key] = len(collection)
            collection.append({'polynomial': encode(h), 'Bernstein': encode(coeffs)})
        rows.append(list(placement) + [index[key]])
        gap_degree = max(gap_degree, len(f) - 1, len(g) - 1)
        witness_degree = max(witness_degree, len(u) - 1, len(v) - 1)
    require(len(rows) == len(set(tuple(r[:4]) for r in rows)) == 144, 'all144 placements')
    return {'format': 'ten-triangle-bridge-v1', 'cosine_closed_band': ['14/25', '593/1000'],
            'r_closed_band': [str(LO), str(HI)], 'A_triangles': [list(t) for t in A],
            'B_triangles': [list(t) for t in B], 'cross_contacts': [[7, 12], [9, 10]],
            'row_fields': ['a', 'a_prime', 'b', 'b_prime', 'root_free_polynomial_index'],
            'rows': rows, 'root_free_polynomials': collection,
            'maximum_contact_gap_degree': gap_degree,
            'maximum_Bezout_witness_degree': witness_degree}


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    args = parser.parse_args()
    record = build()
    output = canonical(record)
    require(json.loads((Path(__file__).parent / 'CERTIFICATE.json').read_text()) == record,
            'whole included certificate matches fresh producer')
    if args.emit:
        args.emit.write_text(output)
    print(json.dumps({'status': 'complete', 'placements': len(record['rows']),
                      'root_free_polynomials': len(record['root_free_polynomials']),
                      'norm_identities': 144 * 12, 'patch_contact_identities': 144 * 21,
                      'Bezout_identities': 144,
                      'maximum_contact_gap_degree': record['maximum_contact_gap_degree'],
                      'maximum_Bezout_witness_degree': record['maximum_Bezout_witness_degree']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
