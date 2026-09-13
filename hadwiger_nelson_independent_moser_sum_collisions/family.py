from pathlib import Path
import sys, json, time
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
from functools import lru_cache
import arithmetic as K
from arithmetic import require
ZERO = K.ZERO
ONE = K.ONE
ALPHA = (F(0), F(0), F(1), F(0))
BETA = (F(0), F(0), F(0), F(1))
add, sub, mul, scale, norm = (K.add, K.sub, K.mul, K.scale, K.norm)

def inv(a):
    return mul(K.conj(a), K.inverse_real(norm(a)))

def sign(x):
    a, b, c, d = x
    require(c == d == 0, 'c == d == 0')
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    r = a * a - 33 * b * b
    return ((a > 0) - (a < 0)) * ((r > 0) - (r < 0))

@lru_cache(maxsize=1)
def spindle():
    rho = scale(add(ONE, ALPHA), F(1, 2))
    eta = scale(add(scale(ONE, 5), BETA), F(1, 6))
    M = [ZERO, ONE, rho, add(ONE, rho), eta, mul(eta, rho), mul(eta, add(ONE, rho))]
    require(len(set(M)) == 7, 'len(set(M)) == 7')
    require(sum((norm(sub(a, b)) == ONE for a, b in combinations(M, 2))) == 11, 'sum((norm(sub(a, b)) == ONE for a, b in combinations(M, 2))) == 11')
    return M

def emul(z, w, s):
    return (add(mul(z[0], w[0]), mul(s, mul(z[1], w[1]))), add(mul(z[0], w[1]), mul(z[1], w[0])))

def econj(z):
    return (K.conj(z[0]), K.conj(z[1]))

def ecscale(z, f):
    return (mul(z[0], f), mul(z[1], f))

def eadd(z, w):
    return (add(z[0], w[0]), add(z[1], w[1]))

def esub(z, w):
    return (sub(z[0], w[0]), sub(z[1], w[1]))

def enumerate_roots():
    M = spindle()
    D = sorted({sub(a, b) for a in M for b in M if a != b})
    Ns = sorted({norm(d) for d in D})
    shapes = {}
    counts = Counter()
    radicands = set()
    for A, B, C in product(Ns, repeat=3):
        H = sub(add(A, B), C)
        delta = sub(scale(mul(A, B), 4), mul(H, H))
        sg = sign(delta)
        counts['shape_' + str(sg)] += 1
        if sg < 0:
            shapes[A, B, C] = None
            continue
        ss = scale(delta, F(1, 3))
        root = K.sqrt_real(ss)
        shapes[A, B, C] = (H, ss, root)
        if sg > 0 and root is None:
            radicands.add(ss)
    reps = []
    classes = {}
    for ss in sorted(radicands):
        for k, rep in enumerate(reps):
            z = K.sqrt_real(mul(ss, K.inverse_real(rep)))
            if z is not None:
                classes[ss] = (k, z)
                break
        else:
            classes[ss] = (len(reps), ONE)
            reps.append(ss)
    roots = set()
    infield = set()
    sample = {}
    st = time.time()
    ni = {d: norm(d) for d in D}
    ii = {d: inv(d) for d in D}
    for a, b, c in product(D, repeat=3):
        sh = shapes[ni[a], ni[b], ni[c]]
        if sh is None:
            counts['nonphysical_triples'] += 1
            continue
        H, ss, root = sh
        A = ni[a]
        den = scale(K.inverse_real(A), F(1, 2))
        base = mul(H, den)
        if root is not None:
            for signum in (1,) if root == ZERO else (-1, 1):
                x = add(base, scale(mul(mul(ALPHA, root), den), signum))
                u = scale(mul(mul(a, x), ii[b]), -1)
                v = scale(mul(mul(a, sub(ONE, x)), ii[c]), -1)
                require(norm(u) == norm(v) == ONE, 'norm(u) == norm(v) == ONE')
                require(add(add(a, mul(u, b)), mul(v, c)) == ZERO, 'add(add(a, mul(u, b)), mul(v, c)) == ZERO')
                infield.add((u, v))
                counts['E_labelled_roots'] += 1
        else:
            field, z = classes[ss]
            tail = mul(mul(ALPHA, z), den)
            for signum in (-1, 1):
                x = (base, scale(tail, signum))
                u = ecscale(x, scale(mul(a, ii[b]), -1))
                v = ecscale(esub((ONE, ZERO), x), scale(mul(a, ii[c]), -1))
                key = (field, u, v)
                require(emul(u, econj(u), reps[field]) == (ONE, ZERO), 'emul(u, econj(u), reps[field]) == (ONE, ZERO)')
                require(emul(v, econj(v), reps[field]) == (ONE, ZERO), 'emul(v, econj(v), reps[field]) == (ONE, ZERO)')
                require(eadd(eadd((a, ZERO), ecscale(u, b)), ecscale(v, c)) == (ZERO, ZERO), 'eadd(eadd((a, ZERO), ecscale(u, b)), ecscale(v, c)) == (ZERO, ZERO)')
                roots.add(key)
                sample.setdefault(key, (D.index(a), D.index(b), D.index(c)))
                counts['outside_labelled_roots'] += 1
    out = {'D': [[str(x) for x in a] for a in D], 'fields': [[str(x) for x in s] for s in reps], 'roots': [{'field': f, 'u': [[str(x) for x in p] for p in u], 'v': [[str(x) for x in p] for p in v], 'witness': sample[f, u, v]} for f, u, v in sorted(roots)], 'infield': [[[str(x) for x in u], [str(x) for x in v]] for u, v in sorted(infield)], 'summary': dict(counts, source_differences=len(D), norms=len(Ns), radicands=len(radicands), quadratic_extensions=len(reps), outside_pairs=len(roots), infield_pairs=len(infield), seconds=time.time() - st)}
    out['summary'].pop('seconds')
    return out
