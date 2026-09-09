#!/usr/bin/env python3
"""Optional factor-certificate regeneration using SymPy, independent of verifier."""
from pathlib import Path
from itertools import product
from functools import reduce
from math import gcd
import argparse
import hashlib
import json
import platform
import time
import sympy as S

x, y = S.symbols('x y')
DX, DY = 1+3*x*x, 1+3*y*y
CX, CY, SX, SY = 1-3*x*x, 1-3*y*y, 2*x, 2*y
W = [(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
D = sorted({(a-c, b-d) for (a, b), (c, d) in product(W, repeat=2)})


def rotation(q):
    a, b = q
    return -b, a+b


def canonical(ds):
    out = []
    for _ in range(6):
        out.append(ds); ds = tuple(map(rotation, ds))
    return min(out)


def norm(q):
    a, b = q
    return a*a+a*b+b*b


def dot_cross(d, e):
    a, b = 2*d[0]+d[1], d[1]
    c, f = 2*e[0]+e[1], e[1]
    return (a*c+3*b*f)//2, 3*(a*f-b*c)//2


def key(poly):
    cs = tuple(int(poly.coeff_monomial(x**i*y**j)) for i in range(3) for j in range(3))
    g = reduce(gcd, cs)
    if not g:
        return cs
    if next(c for c in reversed(cs) if c) < 0:
        g = -g
    return tuple(c//g for c in cs)


def polynomial(ds):
    d, e, f = ds
    p, q = dot_cross(d, e); r, s = dot_cross(d, f); t, z = dot_cross(e, f)
    return S.Poly((norm(d)+norm(e)+norm(f)-1)*DX*DY
                  +(p*CX-q*SX)*DY+(r*CY-s*SY)*DX
                  +t*(CX*CY+3*SX*SY)-z*(CX*SY-SX*CY), x, y, domain=S.ZZ)


def run(out):
    start = time.monotonic(); out.mkdir(parents=True, exist_ok=False)
    polynomials = sorted({key(polynomial(ds)) for ds in {canonical(ds) for ds in product(D, repeat=3)}})
    factorization = {}; all_factors = set()
    for p in polynomials:
        if p == (0,)*9:
            factorization[p] = []
            continue
        poly = S.Poly(sum(c*x**i*y**j for c, (i, j) in zip(p, product(range(3), repeat=2))), x, y, domain=S.ZZ)
        fs = []
        for f, exponent in S.factor_list(poly)[1]:
            fk = key(f); all_factors.add(fk); fs.extend([fk]*exponent)
        factorization[p] = fs
    factors = sorted(all_factors); index = {f: i for i, f in enumerate(factors)}
    cert = {'coefficient_order': 'x exponent outer, y exponent inner, each 0,1,2',
            'factors': factors, 'factorization': [[index[f] for f in factorization[p]] for p in polynomials]}
    encoded = (json.dumps(cert, separators=(',', ':'))+'\n').encode()
    (out/'certificate.json').write_bytes(encoded)
    receipt = {'python': platform.python_version(), 'sympy': S.__version__, 'domain': 'ZZ[x,y], characteristic zero',
               'normalized_polynomials': len(polynomials), 'factors_including_two_positive_denominators': len(factors),
               'certificate_bytes': len(encoded), 'certificate_sha256': hashlib.sha256(encoded).hexdigest(),
               'elapsed_seconds': time.monotonic()-start, 'solver_calls': 0}
    (out/'GENERATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
