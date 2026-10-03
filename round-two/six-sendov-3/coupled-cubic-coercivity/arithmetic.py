"""Exact sparse rational/Gaussian/ninth-root arithmetic, same-author reuse.
Copied unchanged from six-sendov-3 effective-profile-stability/checks.py,
source48241d95ef16ffb51e183c89101762a321152dc0; its original sources9620
(cd6be6d4272505f394bbea6e13ff69a9f73ee5bf) and38e2 are credited there.
This kernel and the new corroboration are NOT independent review.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
import json

E = F(1, 65536)
DIM = 20
ZERO = (0,) * DIM


class CertificateError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise CertificateError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def constant(q):
    return {} if not q else {ZERO: F(q)}


def variable(i):
    exponent = list(ZERO)
    exponent[i] = 1
    return {tuple(exponent): F(1)}


def add(*polys):
    out = {}
    for p in polys:
        for monomial, q in p.items():
            out[monomial] = out.get(monomial, F(0)) + q
    return {m: q for m, q in out.items() if q}


def scale(p, q):
    return {m: a * q for m, a in p.items() if a * q}


def multiply(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            exponent = tuple(x + y for x, y in zip(m, n))
            out[exponent] = out.get(exponent, F(0)) + a * b
    return {m: a for m, a in out.items() if a}


def power(p, n):
    need(type(n) is int and n >= 0, "invalid polynomial exponent")
    out = constant(1)
    for _ in range(n):
        out = multiply(out, p)
    return out


def derivative(p, i):
    out = {}
    for m, q in p.items():
        if m[i]:
            exponent = list(m)
            exponent[i] -= 1
            out[tuple(exponent)] = q * m[i]
    return out


def substitute(p, i, image):
    out = {}
    for m, q in p.items():
        exponent = list(m)
        exponent[i] = 0
        out = add(out, multiply({tuple(exponent): q}, power(image, m[i])))
    return out


def encoded(p):
    # The whole sparse coefficient map, not a sampled evaluation.
    return [[list(m), str(q)] for m, q in sorted(p.items())]


def identity(rows, name, lhs, rhs):
    difference = add(lhs, scale(rhs, -1))
    need(not difference, "identity: " + name)
    rows.append({"name": name, "coefficient_count": len(lhs),
                 "lhs_sha256": sha256(canonical(encoded(lhs))).hexdigest(),
                 "rhs_sha256": sha256(canonical(encoded(rhs))).hexdigest(),
                 "nonzero_residual_coefficients": len(difference)})


def margin(rows, name, lhs, rhs=0, strict=True):
    lhs, rhs = F(lhs), F(rhs)
    need(lhs > rhs if strict else lhs >= rhs, "budget: " + name)
    rows.append({"name": name, "lhs": str(lhs), "rhs": str(rhs),
                 "difference": str(lhs - rhs), "strict": strict})


def field_multiply(x, y):
    # Q[w]/(w**2+w+1).  conjugation sends w to -1-w.
    a, b = x
    c, d = y
    return (a*c - b*d, a*d + b*c - b*d)


def field_power(x, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = field_multiply(out, x)
    return out


def gp(x, y):
    return (x, y)


def gadd(*items):
    return (add(*(x[0] for x in items)), add(*(x[1] for x in items)))


def gscale(x, q):
    return (scale(x[0], q), scale(x[1], q))


def gmul(x, y):
    return (add(multiply(x[0], y[0]), scale(multiply(x[1], y[1]), -1)),
            add(multiply(x[0], y[1]), multiply(x[1], y[0])))


def norm(x):
    return add(power(x[0], 2), power(x[1], 2))


def gid(rows, name, x, y):
    identity(rows, name+' real', x[0], y[0])
    identity(rows, name+' imaginary', x[1], y[1])


# Fresh exact ninth-cyclotomic field Q[w]/(w^6+w^3+1).
N0=(F(0),)*6
N1=(F(1),)+(F(0),)*5
NW=(F(0),F(1),F(0),F(0),F(0),F(0))
def na(*xs):return tuple(sum(x[j] for x in xs) for j in range(6))
def ns(x,q):return tuple(q*t for t in x)
def nm(x,y):
    z=[F(0)]*11
    for j in range(6):
        for k in range(6):z[j+k]+=x[j]*y[k]
    for k in range(10,5,-1):z[k-3]-=z[k];z[k-6]-=z[k]
    return tuple(z[:6])
def np(x,n):
    z=N1
    for _ in range(n):z=nm(z,x)
    return z
def ni(x):
    columns=[nm(x,tuple(F(j==k) for j in range(6))) for k in range(6)]
    a=[[columns[k][j] for k in range(6)]+[F(j==0)] for j in range(6)]
    for k in range(6):
        pivot=next((j for j in range(k,6) if a[j][k]),None)
        need(pivot is not None,'ninth-field inverse is a unit')
        a[k],a[pivot]=a[pivot],a[k];q=a[k][k];a[k]=[t/q for t in a[k]]
        for j in range(6):
            if j!=k:
                q=a[j][k];a[j]=[u-q*v for u,v in zip(a[j],a[k])]
    z=tuple(row[-1] for row in a)
    need(nm(x,z)==N1,'whole field inverse coefficient map')
    return z
def nc(x):return na(*(ns(np(NW,(-j)%9),x[j]) for j in range(6)))
def pc(x):return tuple(constant(t) for t in x)
def pv(x):return (x,)+({},)*5
def pa(*xs):return tuple(add(*(x[j] for x in xs)) for j in range(6))
def ps(x,q):return tuple(scale(t,q) for t in x)
def pm(x,y):
    z=[{} for _ in range(11)]
    for j in range(6):
        for k in range(6):z[j+k]=add(z[j+k],multiply(x[j],y[k]))
    for k in range(10,5,-1):
        z[k-3]=add(z[k-3],scale(z[k],-1));z[k-6]=add(z[k-6],scale(z[k],-1))
    return tuple(z[:6])
def pconj(x):
    out=[{} for _ in range(6)]
    for j in range(6):
        c=nc(tuple(F(k==j) for k in range(6)))
        for k in range(6):out[k]=add(out[k],scale(x[j],c[k]))
    return tuple(out)
def za(*xs):return pa(*(x[0] for x in xs)),pa(*(x[1] for x in xs))
def zs(x,q):return ps(x[0],q),ps(x[1],q)
def zm(x,y):
    return pa(pm(x[0],y[0]),ps(pm(x[1],y[1]),-1)),pa(pm(x[0],y[1]),pm(x[1],y[0]))
def zc(x):return pconj(x[0]),ps(pconj(x[1]),-1)
def zn(x):return zm(x,zc(x))
def zreal(x):return zs(za(x,zc(x)),F(1,2))
def zf(x):return pc(x),pc(N0)
def zv(x,y=None):return pv(x),pv({} if y is None else y)
def zid(rows,name,x,y):
    need(x==y,'whole phase identity '+name)
    serial=[[encoded(p) for p in side] for side in x]
    rows.append({'name':name,'all_twelve_field_polynomial_maps_sha256':sha256(canonical(serial)).hexdigest(),
                 'all_twelve_coefficient_counts':[len(p) for p in x[0]+x[1]],'whole_maps_compared':True})
