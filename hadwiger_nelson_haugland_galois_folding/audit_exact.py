#!/usr/bin/env python3
"""Separate characteristic-zero geometry audit using FLINT rational polynomials."""
from pathlib import Path
import hashlib
import json
from math import gcd
from flint import fmpq, fmpq_poly

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'hadwiger_nelson_haugland2131_exact_reproduction/graph.json'
SOURCE_SHA = '201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d'
MOD = fmpq_poly([1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1])
ONE, ZERO, T = fmpq_poly([1]), fmpq_poly([]), fmpq_poly([0, 1])


def require(test, msg):
    if not test:
        raise ValueError(msg)


def mul(a, b):
    return a*b % MOD


def inverse(a):
    g, s, _ = a.xgcd(MOD)
    require(g == ONE and mul(a, s) == ONE, 'inverse')
    return s


POWERS = [T**k % MOD for k in range(42)]


def conjugate(a):
    return sum((a[k]*POWERS[(-k) % 42] for k in range(len(a))), ZERO)


def key(q):
    return tuple(tuple(str(a[k]) for k in range(12)) for a in q)


def unique(points):
    seen, answer = set(), []
    for q in points:
        k = key(q)
        if k not in seen:
            seen.add(k)
            answer.append(q)
    return answer


def evaluate(a, root, p):
    result = 0
    for k in range(len(a)-1, -1, -1):
        c = a[k]
        result = (result*root+int(c.p)*pow(int(c.q), -1, p)) % p
    return result


def main():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'input hash')
    source = json.loads(raw)
    cert = json.loads((HERE/'certificate.json').read_text())
    require(T**42 % MOD == ONE and all(T**(42//q) % MOD != ONE for q in (2, 3, 7)),
            'cyclotomic root')
    w = POWERS[7]
    b = mul(w-ONE, inverse(POWERS[6]-POWERS[36])) + mul(w, inverse(POWERS[12]-POWERS[30]))
    vectors = [x for j in range(42) for x in (POWERS[j], mul(b, POWERS[j]))]
    require(all(mul(v, conjugate(v)) == ONE for v in vectors), 'unit directions')
    points = [(ZERO, ZERO)]
    for path in source['paths']:
        q = ZERO
        for k in path:
            q += vectors[k]
            points.append((q, ZERO))
        require(q == 2*w-ONE, 'exact path endpoint')
    g1 = unique(points)
    g2 = unique([(mul(q, POWERS[35])-ONE, ZERO) for q, _ in g1] +
                [(mul(q, w)+ONE, ZERO) for q, _ in g1])
    g3 = unique(g2 + [(fmpq(7, 8)*(q+ONE)-ONE, fmpq(1, 8)*mul(2*w-ONE, q+ONE))
                      for q, _ in g2])
    require([len(g1), len(g2), len(g3)] == [740, 1066, 2131], 'exact point counts')
    for u, v in source['G3_edges']:
        a, b = g3[u][0]-g3[v][0], g3[u][1]-g3[v][1]
        A, B = conjugate(a), conjugate(b)
        require(mul(a, A)+5*mul(b, B) == ONE and mul(a, B)+mul(b, A) == ZERO,
                'exact unit edge')
    actions = [(a, e) for a in range(42) if gcd(a, 42) == 1 for e in (1, -1)]
    p, root, s = cert['prime'], cert['root42'], cert['sqrt5']
    rows = [[(evaluate(a, pow(root, k, p), p)+sign*s*evaluate(b, pow(root, k, p), p)) % p
             for k, sign in actions] for a, b in g3]
    expected = json.loads((HERE/'expected.json').read_text())
    sha = hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()
    require(sha == expected['source_complex_shadow_sha256'], 'Cartesian/modular source alignment')
    result = {'verified': True, 'exact_point_counts': [len(g1), len(g2), len(g3)],
              'exact_unit_vectors': len(vectors), 'exact_unit_edges_checked': len(source['G3_edges']),
              'all_24_action_shadows_match': True, 'source_complex_shadow_sha256': sha,
              'exact_coordinate_serialization_sha256': hashlib.sha256(
                  json.dumps([key(q) for q in g3], separators=(',', ':')).encode()).hexdigest(),
              'nonedges_rechecked': False, 'chromatic_lower_bound_reproved': False}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
