#!/usr/bin/env python3
"""Independent census via real quadratic pairs and middle-coefficient normalization.

Imports neither census.py nor coloring.py. Reconstructs and compares every
pair classification and every edge group through canonical stream hashes.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def scale(a, t):
    return a[0]*t, a[1]*t


def mul(a, b):
    return a[0]*b[0]+33*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def divide(a, b):
    norm = b[0]**2-33*b[1]**2
    if not norm:
        raise ZeroDivisionError
    return scale(mul(a, (b[0], -b[1])), 1/norm)


def norm(z):
    return add(mul(z[0], z[0]), scale(mul(z[1], z[1]), 3))


def nonnegative(t):
    a, b = t
    if b == 0:
        return a >= 0
    if b > 0:
        return a >= 0 or 33*b*b >= a*a
    return a >= 0 and a*a >= 33*b*b


def sqrtq(t):
    if t < 0:
        return None
    n, d = isqrt(t.numerator), isqrt(t.denominator)
    if (n*n, d*d) == (t.numerator, t.denominator):
        return Q(n, d)
    return None


def square_root(t):
    """Return an explicit root in Q(sqrt(33)), or prove none by trace/norm."""
    a, b = t
    candidates = []
    if b == 0:
        p, q = sqrtq(a), sqrtq(a/33)
        if p is not None:
            candidates.append((p, Q(0)))
        if q is not None:
            candidates.append((Q(0), q))
    else:
        r = sqrtq(a*a-33*b*b)
        if r is not None:
            for square in ((a+r)/2, (a-r)/2):
                p = sqrtq(square)
                if p is not None and p != 0:
                    candidates.append((p, b/(2*p)))
    for c in candidates:
        if mul(c, c) != t:
            raise ValueError('false square root')
    return next(iter(candidates), None)


def main():
    controls = 0
    for a in range(-4, 5):
        for b in range(-4, 5):
            z = (Q(a), Q(b))
            if square_root(mul(z, z)) is None:
                raise ValueError('square missed')
            controls += 1
    for z in ((-1, 0), (2, 0), (3, 0), (1, 1)):
        if square_root(tuple(map(Q, z))) is not None:
            raise ValueError('nonsquare accepted')
        controls += 1
    for z, expected in (((0,0),True), ((-6,1),False), ((-5,1),True),
                        ((6,-1),True), ((5,-1),False)):
        if nonnegative(tuple(map(Q, z))) != expected:
            raise ValueError('wrong real ordering')
        controls += 1
    raw = (HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv').read_bytes()
    if sha256(raw).hexdigest() != '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02':
        raise ValueError('coordinate hash mismatch')
    vertices = []
    for line in raw.decode().splitlines():
        if line.startswith('#') or not line:
            continue
        a = list(map(int, line.split()))
        if len(a) != 16 or any(a[i] for i in range(16) if i not in (0,5,9,12)):
            raise ValueError('bad coordinates')
        # z = x + sqrt(-3)*y, with x,y in Q(sqrt(33)).
        vertices.append(((Q(a[0],12),Q(a[5],12)),(Q(a[9],12),Q(a[12],36))))
    if len(vertices) != len(set(vertices)) or len(vertices) != 159 or vertices[0] != (ZERO,ZERO):
        raise ValueError('bad fixed-origin instance')
    edges = []
    for i, (x,y) in enumerate(vertices):
        for j, (X,Y) in enumerate(vertices[:i]):
            if norm((add(x,scale(X,-1)),add(y,scale(Y,-1)))) == ONE:
                edges.append((j,i))
    library = [tuple(map(int, s)) for s in (HERE/'colorings.txt').read_text().splitlines()]
    if len(edges) != 646 or any(len(c)!=159 or c[0]!=0 or any(v not in range(4) for v in c)
                                or any(c[i]==c[j] for i,j in edges) for c in library):
        raise ValueError('bad component certificate')
    classification, partition = sha256(), sha256()
    counts = []
    norms = [norm(z) for z in vertices]
    for reflected in (False, True):
        groups = defaultdict(list)
        stat = Counter()
        for i, (x,y) in enumerate(vertices[1:], 1):
            for j, (X,Y0) in enumerate(vertices[1:], 1):
                Y = scale(Y0, -1) if reflected else Y0
                S = add(add(norms[i],norms[j]),(-Q(1),Q(0)))
                delta = add(scale(mul(norms[i],norms[j]),4),scale(mul(S,S),-1))
                if not nonnegative(delta):
                    case = 'no_unit_roots'
                elif square_root(scale(delta,Q(1,3))) is not None:
                    case = 'roots_in_E'
                else:
                    case = 'outside_E_pairs'
                    # c=conjugate(a)*b = cr + sqrt(-3)*ci.
                    cr = add(mul(x,X),scale(mul(y,Y),3))
                    ci = add(mul(x,Y),scale(mul(y,X),-1))
                    if S != ZERO:
                        key = ('middle',divide(cr,S),divide(ci,S))
                    elif cr != ZERO:
                        key = ('zero',divide(ci,cr))
                    else:
                        key = ('vertical',)
                    groups[key].append((i,j))
                stat[case] += 1
                classification.update(f'{int(reflected)}:{i},{j}:{case}\n'.encode())
        for ee in sorted(tuple(sorted(v)) for v in groups.values()):
            line = f'{int(reflected)}:' + ';'.join(f'{i},{j}' for i,j in ee) + '\n'
            partition.update(line.encode())
        counts.append({'reflected':reflected,'classes':len(groups),'pairs':dict(stat)})
    expected = json.loads((HERE/'expected.json').read_text())
    result = {'arithmetic_controls':controls, 'vertices':159, 'internal_edges':len(edges),
              'families':counts, 'classification_sha256':classification.hexdigest(),
              'edge_partition_sha256':partition.hexdigest()}
    for key in ('classification_sha256','edge_partition_sha256'):
        if result[key] != expected[key]:
            raise ValueError(f'entry-level census mismatch: {key}')
    result['entry_level_match'] = True
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
