"""Exact contact rotations of the archived Parts159 support.

E elements are a+b sqrt(33)+i(c sqrt(3)+d sqrt(11)).  A quadratic
extension is represented by (a,b), meaning a+b sqrt(D), with D real.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
from math import lcm
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DEPENDENCIES = {
    'hadwiger_nelson_nonmono159_origin_pencil/census.py':
    '31d1cf2e93b7b0cd6903425acbe6d30dcc0c089226bd7e588720327121bd1b43',
    'hadwiger_nelson_nonmono159_origin_pencil/colorings.txt':
    '1c2fab00fd9d8ceff169336f7015012dc9c6e9487d8e5b628419a3e2d98660dd',
    'hadwiger_nelson_nonmono_field_obstruction/coloring.py':
    'a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e',
    'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv':
    '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',
}

def require(test, message):
    if not test:
        raise ValueError(message)

for name, digest in DEPENDENCIES.items():
    require(sha256((REPO/name).read_bytes()).hexdigest() == digest,
            'dependency hash: '+name)
_import_path = sys.path[:]
sys.path.insert(0, str(REPO/'hadwiger_nelson_nonmono159_origin_pencil'))
import census as C
sys.path[:] = _import_path
K = C.K
add, neg, mul = K.add, K.negate, K.multiply

def sub(a, b):
    return add(a, neg(b))

def scale(a, s):
    return tuple(x*s for x in a)

def sqrt_f(x):
    """Return a square root in Q(sqrt(33)), or None iff none exists."""
    a, b = x
    if not b:
        s = C.rational_sqrt(a)
        if s is not None:
            return s, F(0)
        s = C.rational_sqrt(a/33)
        return None if s is None else (F(0), s)
    n = C.rational_sqrt(a*a-33*b*b)
    if n is None:
        return None
    for sign in (-1, 1):
        q = C.rational_sqrt((a+sign*n)/2)
        if q:
            z = q, b/(2*q)
            require(z[0]**2+33*z[1]**2 == a and 2*z[0]*z[1] == b,
                    'square-root identity')
            return z
    return None

def ext_mul(a, b, d):
    return (add(mul(a[0], b[0]), mul(mul(a[1], b[1]), d)),
            add(mul(a[0], b[1]), mul(a[1], b[0])))

def ext_conj(a):
    return K.conjugate(a[0]), K.conjugate(a[1])

def e_contacts(A, u):
    """Every non-origin cross edge and coincidence, with integer arithmetic.

    This uses no modular filter and no polynomial-class lookup.
    """
    B = [mul(u, a) for a in A]
    den = lcm(*(v.denominator for p in A+B for v in p))
    aa = [tuple(int(v*den) for v in p) for p in A]
    bb = [tuple(int(v*den) for v in p) for p in B]
    edges, same = [], []
    for i in range(1, len(A)):
        for j in range(1, len(A)):
            a, b, c, d = (x-y for x, y in zip(aa[i], bb[j]))
            if a == b == c == d == 0:
                same.append((i, j))
            if a*b+c*d == 0 and a*a+33*b*b+3*c*c+11*d*d == den*den:
                edges.append((i, j))
    return edges, same

def library():
    path = REPO/'hadwiger_nelson_nonmono159_origin_pencil/colorings.txt'
    lib = [tuple(map(int, s)) for s in path.read_text().splitlines()]
    words = [tuple(p[c] for c in w) for w in lib
             for p in [(0,)+p for p in permutations((1, 2, 3))]]
    return lib, words

def build():
    A = C.points()
    internal = C.internal_edges(A)
    degree = Counter(v for e in internal for v in e)
    require(len(internal) == 646 and len(degree) == 159 and min(degree.values()) >= 2,
            'internal graph / non-origin coincidence lemma')
    _, groups = C.enumerate_pencils(A, False, sha256())
    items = sorted(groups.items())
    norms = [mul(a, K.conjugate(a)) for a in A]
    inverse = [None]+[K.inverse(a) for a in A[1:]]
    e_roots = set()
    # This separate loop includes all double roots and all roots in E.
    for i in range(1, 159):
        for j in range(1, 159):
            s = sub(add(norms[i], norms[j]), K.ONE)
            delta = sub(scale(mul(norms[i], norms[j]), 4), mul(s, s))
            q = sqrt_f(scale(delta, F(1, 3))[:2])
            if q is None:
                continue
            ic = mul(K.conjugate(inverse[i]), inverse[j])
            imaginary = mul((F(0), F(0), F(1), F(0)), q+(F(0), F(0)))
            for sign in (-1, 1):
                z = scale(mul(add(s, scale(imaginary, sign)), ic), F(1, 2))
                require(mul(z, K.conjugate(z)) == K.ONE, 'E rotation norm')
                e_roots.add(z)
    e_roots = sorted(e_roots)
    e_data = {u: e_contacts(A, u) for u in e_roots}
    require(all(es for es, same in e_data.values()), 'spurious E event')
    ds = []
    for (T, V), es in items:
        i, j = es[0]
        s = sub(add(norms[i], norms[j]), K.ONE)
        delta = sub(scale(mul(norms[i], norms[j]), 4), mul(s, s))
        d = scale(delta, F(1, 3))
        require(d[2:] == (0, 0) and C.real_sign(d[:2]) > 0,
                'nonpositive event radicand')
        require(sqrt_f(d[:2]) is None and any(T),
                'reducible or trace-zero outside-E event')
        ds.append(d)
    representatives, classification = [], {}
    for d in sorted(set(ds)):
        for k, dd in enumerate(representatives):
            ratio = mul(d, K.inverse(dd))
            require(ratio[2:] == (0, 0), 'nonreal ratio')
            s = sqrt_f(ratio[:2])
            if s is not None:
                classification[d] = k, s+(F(0), F(0))
                break
        else:
            classification[d] = len(representatives), K.ONE
            representatives.append(d)
    roots = []
    for index, (((T, V), es), di) in enumerate(zip(items, ds)):
        k, s = classification[di]
        d = representatives[k]
        i, j = es[0]
        ic = mul(K.conjugate(inverse[i]), inverse[j])
        a = scale(T, F(1, 2))
        b = scale(mul(mul((F(0), F(0), F(1), F(0)), s), ic), F(1, 2))
        require(sub(mul(a, a), mul(mul(b, b), d)) == V, 'root polynomial')
        for sign in (-1, 1):
            z = a, scale(b, sign)
            require(ext_mul(z, ext_conj(z), d) == (K.ONE, K.ZERO),
                    'physical unit rotation')
            roots.append((index, k, z))
    return {'A': A, 'internal': internal, 'groups': items, 'roots': roots,
            'fields': representatives, 'e_roots': e_roots, 'e_data': e_data,
            'radicands': len(set(ds))}

def relative_contacts(data, u, v, d):
    r = ext_mul(ext_conj(u), v, d)
    if r[1] == K.ZERO:
        es, same = data['e_data'].get(r[0], ([], []))
        return es, same, 'E'
    key = (scale(r[0], 2), sub(mul(r[0], r[0]), mul(mul(r[1], r[1]), d)))
    es = data['group_map'].get(key, [])
    return es, [], 'outside_E'
