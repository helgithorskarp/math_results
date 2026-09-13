"""Exact E arithmetic and complete weighted-contact generation; standard library."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import isqrt, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv'
SOURCE_SHA = 'f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50'
ZERO = (F(0),)*4
ONE = (F(1), F(0), F(0), F(0))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def add(x, y):
    return tuple(a+b for a, b in zip(x, y))

def scale(x, s):
    return tuple(s*a for a in x)

def sub(x, y):
    return add(x, scale(y, -1))

def conj(x):
    return x[0], x[1], -x[2], -x[3]

def mul(x, y):
    a,b,c,d = x
    A,B,C,D = y
    return (a*A+33*b*B-3*c*C-11*d*D,
            a*B+b*A-c*D-d*C,
            a*C+c*A+11*(b*D+d*B),
            a*D+d*A+3*(b*C+c*B))

def norm(x):
    return mul(x, conj(x))

def inverse_real(x):
    a,b,c,d = x
    require(c == d == 0, 'nonreal inverse')
    den = a*a-33*b*b
    require(den != 0, 'zero inverse')
    return a/den, -b/den, F(0), F(0)

def rational_sqrt(q):
    if q < 0:
        return None
    a,b = isqrt(q.numerator), isqrt(q.denominator)
    return F(a,b) if a*a == q.numerator and b*b == q.denominator else None

def sqrt_real(x):
    a,b,c,d = x
    require(c == d == 0, 'nonreal square-root input')
    if not b:
        s = rational_sqrt(a)
        if s is not None:
            return s, F(0), F(0), F(0)
        s = rational_sqrt(a/33)
        return None if s is None else (F(0),s,F(0),F(0))
    h = rational_sqrt(a*a-33*b*b)
    if h is None:
        return None
    for sign in (-1,1):
        q = rational_sqrt((a+sign*h)/2)
        if q:
            z = (q,b/(2*q),F(0),F(0))
            require(mul(z,z) == x, 'square-root identity')
            return z
    return None

def points():
    raw = SOURCE.read_bytes()
    require(sha256(raw).hexdigest() == SOURCE_SHA, 'source hash')
    rows = [tuple(map(int,l.split())) for l in raw.decode().splitlines()
            if l and not l.startswith('#')][:374]
    require(len(rows) == 374, 'source size')
    require(all(len(p) == 16 and all(p[i] == 0 for i in range(16)
                if i not in (0,5,9,12)) for p in rows), 'E coordinate support')
    A = [tuple(F(p[i],96) for i in (0,5,9,12)) for p in rows]
    require(len(set(A)) == 374, 'source collisions')
    return A

def differences(A):
    pairs = {}
    for i,a in enumerate(A):
        for j,b in enumerate(A):
            pairs.setdefault(sub(a,b), []).append((i,j))
    return pairs

def directions(pairs):
    """All (d,r), up to sign, for N((1-u)d+u*r)=1, trace(u)=5/4."""
    T = F(5,4)
    found = set()
    for d in pairs:
        if d == ZERO:
            found.update((d,r) for r in pairs if norm(r) == ONE)
            continue
        disc = add(scale(ONE,T*T-4),scale(inverse_real(norm(d)),4))
        root = sqrt_real(disc)
        if root is None:
            continue
        for sign in (-1,1):
            y = mul(d,scale(add(scale(ONE,T),scale(root,sign)),F(1,2)))
            r = sub(d,y)
            if r in pairs:
                cross = mul(conj(d),y)
                require(cross[2:] == (0,0), 'nonreal cross term')
                require(sub(add(norm(d),norm(y)),scale(cross,T)) == ONE,
                        'unit identity')
                found.add((d,r))
    require(all((scale(d,-1),scale(r,-1)) in found for d,r in found),
            'opposite direction missing')
    return sorted((d,r) for d,r in found if (d,r) < (scale(d,-1),scale(r,-1)))

def root33(bits):
    t = 0
    for j in range(max(0,bits-3)):
        if (4*t*t+t-2) % (1 << (j+1)):
            t += 1 << j
    r = (1+8*t) % (1 << bits)
    require((r*r-33) % (1 << bits) == 0, 'Hensel root')
    return r

def residue(z):
    """Reduction in O/4 = (Z/4)[w]/(w^2+w+1); reject nonintegral input."""
    den = lcm(*(x.denominator for x in z))
    a,b,c,d = [int(x*den) for x in z]
    e = (den & -den).bit_length()-1
    mod = 1 << (e+2)
    r = root33(e+2)
    iv = pow(3*(den >> e),-1,mod)
    A = (3*a+3*b*r+3*c+d*r)*iv % mod
    B = (6*c+2*d*r)*iv % mod
    require(A % (1 << e) == B % (1 << e) == 0, 'point outside O')
    return A >> e, B >> e

def quotient_directions():
    U = [(a,b) for a,b in product(range(4),repeat=2)
         if (a*a-a*b+b*b) % 4 == 1]
    return ({(0,0,a,b) for a,b in U} | {(a,b,a,b) for a,b in U}
            | {(2*a,2*b,0,0) for a,b in ((1,0),(0,1),(1,1))})

def quotient_colour(z):
    a,b,c,d = z
    a0,a1,b0,b1,c0,c1,d0,d1 = a&1,a>>1,b&1,b>>1,c&1,c>>1,d&1,d>>1
    lo = (a1 ^ b1 ^ c1 ^ d1 ^ b0 ^ (a0 & b0)
          ^ ((a0 ^ b0) & (c0 ^ d0)) ^ (c0 & d0))
    hi = a1 ^ c0 ^ d0
    return lo+2*hi
