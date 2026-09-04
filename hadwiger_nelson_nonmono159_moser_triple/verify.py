#!/usr/bin/env python3
"""Complete origin-fixing placement census of A against B=A union ((5+i sqrt(11))/6)A.

Uses exact arithmetic and explicit coloring libraries; no solver or angle grid.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'hadwiger_nelson_nonmono159_origin_pencil'
if sha256((PREVIOUS/'census.py').read_bytes()).hexdigest() != '31d1cf2e93b7b0cd6903425acbe6d30dcc0c089226bd7e588720327121bd1b43':
    raise ValueError('arithmetic dependency mismatch')
sys.path.insert(0, str(PREVIOUS))
import census as C
K = C.K
require = C.require


def construction():
    A = C.points()
    t = K.element(F(5,6), 0, 0, F(1,6))
    require(K.is_unit(t), 'inner multiplier is not a unit')
    image = [K.multiply(t,a) for a in A]
    B = list(dict.fromkeys(A+image))
    require(len(B) == 292 and B[0] == K.ZERO, 'incorrect inner union')
    index = {a:i for i,a in enumerate(B)}
    EA, EB = C.internal_edges(A), C.internal_edges(B)
    inherited = set(EA) | {tuple(sorted((index[image[i]],index[image[j]]))) for i,j in EA}
    require(len(EA) == 646 and len(EB) == 1251, 'incorrect component graph')
    require(len(set(A)&set(image)) == 26 and len(set(EB)-inherited) == 18, 'incorrect inner contacts')
    return A, B, EA, EB


def enumerate_classes(B, A, reflected, classification):
    image = [K.conjugate(a) for a in A] if reflected else A
    normsB = [K.multiply(b,K.conjugate(b)) for b in B]
    normsA = [K.multiply(a,K.conjugate(a)) for a in A]
    inverseB = [None]+[K.inverse(K.conjugate(b)) for b in B[1:]]
    inverseA = [None]+[K.inverse(a) for a in image[1:]]
    groups = defaultdict(list)
    counts = Counter()
    for i in range(1,len(B)):
        for j in range(1,len(A)):
            counts['nonzero_pairs'] += 1
            S = K.add(K.add(normsB[i],normsA[j]),K.negate(K.ONE))
            delta = K.add(tuple(4*x for x in K.multiply(normsB[i],normsA[j])),
                          K.negate(K.multiply(S,S)))
            require(delta[2:] == (0,0), 'nonreal discriminant')
            sign = C.real_sign(delta[:2])
            if sign < 0:
                case = 'no_unit_roots'
            elif C.real_square(tuple(x/3 for x in delta[:2])):
                case = 'roots_in_E'
            else:
                require(sign > 0, 'unexpected double root')
                case = 'outside_E_pairs'
                invc = K.multiply(inverseB[i],inverseA[j])
                T = K.multiply(S,invc)
                V = K.multiply(K.multiply(B[i],K.conjugate(image[j])),invc)
                groups[T,V].append((i,j))
            counts[case] += 1
            classification.update(f'{int(reflected)}:{i},{j}:{case}\n'.encode())
    return dict(counts),groups


def read_library(name, vertices, edges):
    raw = (HERE/name).read_bytes()
    library = [tuple(map(int,line)) for line in raw.decode().splitlines()]
    require(bool(library), 'empty coloring library')
    for c in library:
        require(len(c)==len(vertices) and c[0]==0 and all(v in range(4) for v in c), 'bad coloring domain')
        require(all(c[i]!=c[j] for i,j in edges), 'monochromatic internal edge')
    return library,sha256(raw).hexdigest()


def main():
    A,B,EA,EB = construction()
    libA,hashA = read_library('colors_A.txt',A,EA)
    libB,hashB = read_library('colors_B.txt',B,EB)
    require((len(libA),len(libB)) == (5,3), 'wrong library sizes')
    perms = [(0,)+p for p in permutations((1,2,3))]
    classification,partition,polynomial,coverage = (sha256() for _ in range(4))
    summaries = {}
    distinct = set()
    total = 0
    for reflected in (False,True):
        counts,groups = enumerate_classes(B,A,reflected,classification)
        for s in C.partition_text(reflected,groups):
            partition.update(s.encode())
        for (T,V),ee in sorted(groups.items()):
            key = [[str(v) for v in T],[str(v) for v in V]]
            polynomial.update((json.dumps([int(reflected),key,ee],separators=(',',':'))+'\n').encode())
            witness = next(((i,j,k) for i,cb in enumerate(libB) for j,ca in enumerate(libA)
                            for k,p in enumerate(perms)
                            if all(cb[b]!=p[ca[a]] for b,a in ee)),None)
            require(witness is not None, 'uncovered quadratic class')
            i,j,k = witness
            colors = libB[i]+tuple(perms[k][v] for v in libA[j][1:])
            require(len(colors)==450, 'incorrect union size')
            require(all(colors[b]!=colors[len(B)-1+a] for b,a in ee), 'bad union coloring')
            coverage.update((json.dumps([int(reflected),key,witness],separators=(',',':'))+'\n').encode())
            distinct.add(tuple(ee))
        summaries['reflection' if reflected else 'rotation'] = {
            **counts,'quadratic_classes':len(groups),'unit_isometries':2*len(groups),
            'cross_edge_histogram':dict(sorted(Counter(map(len,groups.values())).items()))}
        total += len(groups)
    result = {'A_vertices':len(A),'A_edges':len(EA),'B_vertices':len(B),'B_edges':len(EB),
              'inner_overlap':26,'inner_new_edges':18,'union_vertices_outside_E':450,
              'internal_edges_outside_E':len(EA)+len(EB),'A_library_size':len(libA),
              'B_library_size':len(libB),'families':summaries,'quadratic_classes_total':total,
              'outside_field_isometries_total':2*total,'distinct_cross_edge_sets':len(distinct),
              'uncovered_classes':0,'classification_sha256':classification.hexdigest(),
              'edge_partition_sha256':partition.hexdigest(),'polynomial_census_sha256':polynomial.hexdigest(),
              'coverage_sha256':coverage.hexdigest(),'A_library_sha256':hashA,'B_library_sha256':hashB}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
