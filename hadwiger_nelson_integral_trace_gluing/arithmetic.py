"""Exact local arithmetic for even-trace gluing and unit-trace field embeddings."""
from pathlib import Path
from fractions import Fraction as Q
from math import lcm
from hashlib import sha256
import importlib.util


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, relative, pin):
    path = Path(__file__).resolve().parent.parent/relative
    require(sha256(path.read_bytes()).hexdigest() == pin, 'dependency pin mismatch')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


C = load('trace_zero_arithmetic', 'hadwiger_nelson_trace_zero_gluing/coloring.py',
         '89ea15f3958154ac514dd36cd391d197e3c04ac1499f520fb0df870ffb13d1cc')
K = C.K
e, add, sub, scale, mul, bar, norm = C.e, C.add, C.sub, C.scale, C.mul, C.bar, C.norm
ZERO, ONE = C.ZERO, C.ONE


def local(x, bits):
    require(bits >= 1, 'positive precision required')
    den = lcm(*(a.denominator for a in x)); v = (den & -den).bit_length()-1
    modulus = 1 << (bits+v); r = K.root33_mod_power2(bits+v)
    a, b, c, d = (int(t*den) for t in x); inv = pow(3*(den >> v), -1, modulus)
    A = (3*a+3*b*r+3*c+d*r)*inv % modulus; B = (6*c+2*d*r)*inv % modulus
    require(A % (1 << v) == B % (1 << v) == 0, 'nonintegral local input')
    return A >> v, B >> v


def rm(x, y, m):
    a, b = x; c, d = y
    return (a*c-b*d) % m, (a*d+b*c-b*d) % m


def rb(x, m):
    return (x[0]-x[1]) % m, -x[1] % m


def rn(x, m):
    return (x[0]*x[0]-x[0]*x[1]+x[1]*x[1]) % m


def ri(x, m):
    inv = pow(rn(x, m), -1, m)
    return tuple(inv*a % m for a in rb(x, m))


def lift_w(constant, bits, branch=0):
    """Root of w^2-w+constant with residue omega or omega^2."""
    require(bits >= 1 and constant % 2 == 1 and branch in (0, 1), 'invalid Hensel data')
    w = (branch, 1)
    for j in range(1, bits):
        m = 1 << (j+1); square = rm(w, w, m)
        f = ((square[0]-w[0]+constant) % m, (square[1]-w[1]) % m)
        require(all(a % (1 << j) == 0 for a in f), 'Hensel divisibility failure')
        w = tuple((a+b) % m for a, b in zip(w, f))  # correction = 2^j*(f/2^j mod 2)
    return w


def unit_root(T, bits, branch=0):
    t = local(T, bits); m = 1 << bits
    require(rn(t, 2) == 1, 'trace is not a local unit')
    w = lift_w(pow(rn(t, m), -1, m), bits, branch)
    u = rm(t, w, m)
    require(rn(u, m) == 1, 'root norm failure')
    J = rm(t, ri(rb(t, m), m), m)
    sq, tu = rm(u, u, m), rm(t, u, m)
    require(tuple((sq[i]-tu[i]+J[i]) % m for i in range(2)) == (0, 0), 'root polynomial failure')
    return u


def field_colour(A, B, T):
    """Zero-th local digits of A+B*u in the compatible unit-trace embedding."""
    den = lcm(*(x.denominator for x in A+B)); k = (den & -den).bit_length()-1
    m = 1 << (k+1)
    x, y = local(scale(A, 1 << k), k+1), local(scale(B, 1 << k), k+1)
    yu = rm(y, unit_root(T, k+1), m)
    z = tuple((a+b) % m for a, b in zip(x, yu))
    return (z[0] >> k)+2*(z[1] >> k)


def qvalue(x, y, T):
    return sub(add(norm(x), norm(y)), mul(T, mul(bar(x), y)))


def glue_even(P, Qs, T, cross):
    require(local(T, 1) == (0, 0), 'trace is not in 2O')
    require(P and Qs, 'empty source')
    for source in (P, Qs):
        for x in source:
            C.residue(sub(x, source[0]))
    if not cross:
        out = []
        for source in (P, Qs):
            colours = [C.residue(sub(x, source[0])) for x in source]
            shift = colours[source.index(ZERO)] if ZERO in source else 0
            out.append([c ^ shift for c in colours])
        return *out, {'branch': 'no_cross'}
    require(all(qvalue(P[i], Qs[j], T) == ONE for i, j in cross), 'cross quadratic identity failed')
    i, j = cross[0]; x0, y0 = P[i], Qs[j]
    k = C.depth(x0); require(C.depth(y0) == k, 'cross anchor depths differ')
    if k == 0:
        return [C.residue(x) for x in P], [C.residue(y) for y in Qs], {'branch': 'integral', 'depth': 0}
    a, b = C.residue(scale(x0, 1 << k)), C.residue(scale(y0, 1 << k))
    require(a and b, 'scaled anchors not units')
    lam = C.fm(C.fb(b), a)
    t = next(t for t in range(4) if C.ft(C.fm(C.fb(a), t)) == 1)
    cp = [C.residue(sub(x, x0)) for x in P]
    cq = [C.fm(lam, C.residue(sub(y, y0))) ^ t for y in Qs]
    require(all(cp[i] != cq[j] for i, j in cross), 'colour collision')
    return cp, cq, {'branch': 'nonintegral', 'depth': k, 'anchor': [i, j],
                    'scaled_residues': [a, b], 'lambda': lam, 'shift': t}
