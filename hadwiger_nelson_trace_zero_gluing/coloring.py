"""Local-coset radial gluing. Four-tuples represent a+b*sqrt(33)+c*alpha+d*beta."""
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
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


K = load('source_field', 'hadwiger_nelson_nonmono_field_obstruction/coloring.py',
         'a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e')
e, add, mul, bar = K.element, K.add, K.multiply, K.conjugate
ZERO, ONE = K.ZERO, K.ONE


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y, strict=True))


def scale(x, c):
    return tuple(c*a for a in x)


def norm(x):
    return mul(x, bar(x))


def residue(x):
    den = lcm(*(a.denominator for a in x))
    v = (den & -den).bit_length()-1
    modulus = 1 << (v+1)
    r = K.root33_mod_power2(v+1)
    a, b, c, d = (int(t*den) for t in x)
    inv = pow(3*(den >> v), -1, modulus)
    A = (3*a+3*b*r+3*c+d*r)*inv % modulus
    B = (6*c+2*d*r)*inv % modulus
    require(A % (1 << v) == B % (1 << v) == 0, 'nonintegral residue request')
    return (A >> v)+2*(B >> v)


def depth(x):
    """max(0,-v(x)); no upper bound is imposed on the input denominator."""
    den = lcm(*(a.denominator for a in x))
    limit = (den & -den).bit_length()-1
    for k in range(limit+1):
        try:
            residue(scale(x, 1 << k))
            return k
        except ValueError:
            pass
    raise ValueError('integrality bound failed')


def fm(x, y):
    a, b, c, d = x & 1, x >> 1, y & 1, y >> 1
    return ((a*c+b*d) & 1)+2*((a*d+b*c+b*d) & 1)


def fb(x):
    return fm(x, x)


def ft(x):
    t = x ^ fb(x)
    require(t in (0, 1), 'trace not binary')
    return t


def glue(P, Qs, cross):
    require(P and Qs, 'empty source')
    for source in (P, Qs):
        for x in source:
            residue(sub(x, source[0]))  # Check the stated coset hypothesis.
    if not cross:
        colours = []
        for source in (P, Qs):
            c = [residue(sub(x, source[0])) for x in source]
            if ZERO in source:
                shift = c[source.index(ZERO)]
                c = [x ^ shift for x in c]
            colours.append(c)
        return *colours, {'branch': 'no_cross_edges'}
    i, j = cross[0]
    x0, y0 = P[i], Qs[j]
    require(norm(x0) != ZERO or norm(y0) != ZERO, 'bad radial anchor')
    for a, b in cross:
        require(add(norm(P[a]), norm(Qs[b])) == ONE, 'radial identity violated')
    kx, ky = depth(x0), depth(y0)
    require(kx == ky, 'unequal radial depths')
    if kx == 0:
        return [residue(x) for x in P], [residue(y) for y in Qs], {'branch': 'integral', 'depth': 0}
    a, b = residue(scale(x0, 1 << kx)), residue(scale(y0, 1 << kx))
    require(a and b, 'scaled anchors are not units')
    lam = fm(fb(b), a)  # conjugate(a)^{-1}=a in F4^*.
    t = next(t for t in range(4) if ft(fm(fb(a), t)) == 1)
    cp = [residue(sub(x, x0)) for x in P]
    cq = [fm(lam, residue(sub(y, y0))) ^ t for y in Qs]
    require(all(cp[i] != cq[j] for i, j in cross), 'radial colouring collision')
    return cp, cq, {'branch': 'nonintegral', 'depth': kx, 'anchor': [i, j],
                    'scaled_residues': [a, b], 'lambda': lam, 'shift': t}
