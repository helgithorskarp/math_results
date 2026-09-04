#!/usr/bin/env python3
"""Exact finite reduction of all orthogonal placements fixing the origin.

An outside-E cross edge determines an irreducible monic quadratic over E.
Its complete cross-edge set consists of all pairs giving that polynomial.
See PROOF.md. No root approximation or solver is used by this verifier.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json
from math import isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FIELD = HERE.parent / 'hadwiger_nelson_nonmono_field_obstruction'
POINTS = HERE.parent / 'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
POINTS_HASH = '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'
FIELD_HASH = 'a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e'
if sha256((FIELD / 'coloring.py').read_bytes()).hexdigest() != FIELD_HASH:
    raise ValueError('field arithmetic hash mismatch')
sys.path.insert(0, str(FIELD))
import coloring as K


def require(test, message):
    if not test:
        raise ValueError(message)


def real_sign(x):
    """Sign of a+b sqrt(33) in the specified real embedding."""
    a, b = x
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    d = a*a - 33*b*b
    return ((a > 0) - (a < 0)) * ((d > 0) - (d < 0))


def rational_sqrt(x):
    if x < 0:
        return None
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    return F(a, b) if a*a == x.numerator and b*b == x.denominator else None


def real_square(x):
    """Whether x is a square in Q(sqrt(33)); an exact iff criterion."""
    a, b = x
    if not b:
        return rational_sqrt(a) is not None or rational_sqrt(a/33) is not None
    n = rational_sqrt(a*a - 33*b*b)
    if n is None:
        return False
    for e in (-1, 1):
        q = rational_sqrt((a+e*n)/2)
        if q is not None and q != 0:
            require(q*q + 33*(b/(2*q))**2 == a, 'bad square criterion')
            return True
    return False


def points():
    raw = POINTS.read_bytes()
    require(sha256(raw).hexdigest() == POINTS_HASH, 'coordinate hash mismatch')
    lines = raw.decode().splitlines()
    require(lines[0] == '# scale 12', 'unexpected scale')
    out = []
    for s in lines:
        if not s or s.startswith('#'):
            continue
        v = tuple(map(int, s.split()))
        require(len(v) == 16, 'bad point row')
        require(all(v[i] == 0 for i in range(16) if i not in (0, 5, 9, 12)),
                'point outside E')
        out.append(K.element(*(F(v[i], 12) for i in (0, 5, 9, 12))))
    require(len(out) == len(set(out)) == 159 and out[0] == K.ZERO, 'bad gadget')
    return out


def internal_edges(A):
    out = []
    for i in range(len(A)):
        for j in range(i):
            a, b, c, d = (A[i][k]-A[j][k] for k in range(4))
            if a*b+c*d == 0 and a*a+33*b*b+3*c*c+11*d*d == 1:
                out.append((j, i))
    return out


def partition_text(reflected, groups):
    """Canonical edge-level partition, independent of polynomial encoding."""
    for ee in sorted(tuple(sorted(v)) for v in groups.values()):
        yield f'{int(reflected)}:' + ';'.join(f'{i},{j}' for i, j in ee) + '\n'


def enumerate_pencils(A, reflected, classification):
    B = [K.conjugate(a) for a in A] if reflected else A
    norms = [K.multiply(a, K.conjugate(a)) for a in A]
    invA = [None] + [K.inverse(K.conjugate(a)) for a in A[1:]]
    invB = [None] + [K.inverse(b) for b in B[1:]]
    counts = Counter()
    groups = defaultdict(list)
    for i in range(1, 159):
        for j in range(1, 159):
            counts['nonzero_pairs'] += 1
            S = K.add(K.add(norms[i], norms[j]), K.negate(K.ONE))
            delta = K.add(tuple(4*x for x in K.multiply(norms[i], norms[j])),
                          K.negate(K.multiply(S, S)))
            require(delta[2:] == (0, 0), 'nonreal discriminant')
            sign = real_sign(delta[:2])
            if sign < 0:
                case = 'no_unit_roots'
            elif real_square(tuple(x/3 for x in delta[:2])):
                case = 'roots_in_E'
            else:
                require(sign > 0, 'unhandled double root')
                case = 'outside_E_pairs'
                invc = K.multiply(invA[i], invB[j])
                T = K.multiply(S, invc)
                V = K.multiply(K.multiply(A[i], K.conjugate(B[j])), invc)
                groups[T, V].append((i, j))
            counts[case] += 1
            classification.update(f'{int(reflected)}:{i},{j}:{case}\n'.encode())
    return dict(counts), groups


def main():
    A = points()
    edges = internal_edges(A)
    require(len(edges) == 646, 'wrong strict component graph')
    raw = (HERE / 'colorings.txt').read_bytes()
    library = [tuple(map(int, line)) for line in raw.decode().splitlines()]
    require(len(library) == 4, 'wrong witness library')
    for c in library:
        require(len(c) == 159 and c[0] == 0 and all(0 <= v < 4 for v in c), 'bad colors')
        require(all(c[i] != c[j] for i, j in edges), 'invalid component coloring')
    perms = [(0,)+p for p in permutations((1, 2, 3))]
    classification, partition, polynomial, coverage = (sha256() for _ in range(4))
    results = {}
    distinct_edges = set()
    total = 0
    for reflected in (False, True):
        counts, groups = enumerate_pencils(A, reflected, classification)
        for s in partition_text(reflected, groups):
            partition.update(s.encode())
        for (T, V), ee in sorted(groups.items()):
            key = [[str(x) for x in T], [str(x) for x in V]]
            polynomial.update((json.dumps([int(reflected), key, ee], separators=(',', ':'))+'\n').encode())
            witness = next(((i, j, k) for i, ca in enumerate(library)
                            for j, cb in enumerate(library) for k, p in enumerate(perms)
                            if all(ca[a] != p[cb[b]] for a, b in ee)), None)
            require(witness is not None, 'uncovered quadratic class')
            # This is a direct positive witness check, not a solver verdict.
            i, j, k = witness
            colors = library[i] + tuple(perms[k][v] for v in library[j][1:])
            require(all(colors[a] != colors[158+b] for a, b in ee), 'bad glued coloring')
            coverage.update((json.dumps([int(reflected), key, witness], separators=(',', ':'))+'\n').encode())
            distinct_edges.add(tuple(ee))
        results['reflection' if reflected else 'rotation'] = {
            **counts, 'quadratic_classes': len(groups), 'unit_isometries': 2*len(groups),
            'cross_edge_histogram': dict(sorted(Counter(map(len, groups.values())).items()))}
        total += len(groups)
    result = {'vertices': 159, 'internal_edges': len(edges), 'library_size': len(library),
              'families': results, 'quadratic_classes_total': total,
              'outside_field_isometries_total': 2*total,
              'distinct_cross_edge_sets': len(distinct_edges), 'uncovered_classes': 0,
              'classification_sha256': classification.hexdigest(),
              'edge_partition_sha256': partition.hexdigest(),
              'polynomial_census_sha256': polynomial.hexdigest(),
              'coverage_sha256': coverage.hexdigest(), 'library_sha256': sha256(raw).hexdigest()}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
