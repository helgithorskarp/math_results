#!/usr/bin/env python3
"""Optional secondary calculation using the pinned author's residue route.

This is explicitly an author-kernel cross-check, not the independent
checker. It extends the original formula to t^4 and compares both complete
coefficient polynomials with the independently produced fixture.
"""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import sys

path = (Path(sys.argv[1]) if len(sys.argv) == 2 else
        Path(__file__).resolve().parent.parent/'sendov_degree9_finite_energy_local_minimum'/'verify.py')
if len(sys.argv) > 2:
    raise ValueError('usage: crosscheck_residue.py [pinned-original-verify.py]')
if sha256(path.read_bytes()).hexdigest() != '3c91c8029d2bfb100fa42d1bfc683baa21005d7fc9f6ba677b095a56c1760382':
    raise ValueError('original source does not match reviewed pin')
spec = importlib.util.spec_from_file_location('pinned_author',path)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
m.MAX = 12


def calculate(w):
    A,B,ua,u,qn,qf,gap,energy,rem = m.profile(w)
    cl = m.plus(m.scaled(m.times(B,m.tp(u,2)),-Q(3,7)),
                m.scaled(m.divide(m.times(m.tp(B,2),m.tp(u,2)),m.minus(B,A)),-Q(1,49)),
                m.scaled(m.times(m.tp(B,2),m.tp(u,3)),-Q(34,49)))
    F2 = m.plus(m.divide(m.rr(m.times(cl,m.conj(u))),m.norm(u)),
                 m.scaled(m.times(m.norm(u),m.tp(m.rr(m.times(B,u)),2)),Q(5,14)))
    for q in [qn,qf]:
        z = m.minus(m.ts(m.a),m.invert(q))
        qp = m.minus(m.scaled(z,18),m.plus(m.scaled(m.plus(m.ts(m.a),A),8),m.scaled(B,2)))
        shift = m.scaled(m.divide(m.times(B,m.tp(q,2),m.minus(z,m.ts(m.a)),m.minus(z,A),m.plus(z,B)),
                                 m.times(m.tp(m.minus(z,B),2),qp)),Q(1,2))
        F2 = m.plus(F2,m.divide(m.rr(m.times(shift,m.conj(q))),m.norm(q)))
    up = m.scaled(m.times(B,m.tp(u,2)),m.G(0,1))
    upp = m.plus(m.scaled(m.times(B,m.tp(u,2)),-1),
                 m.scaled(m.times(m.tp(B,2),m.tp(u,3)),-2))
    E2 = m.plus(m.times(up,m.conj(up)),m.rr(m.times(m.minus(u,m.ts(m.V)),m.conj(upp))))
    lagrange = m.divide(m.deriv(gap),m.deriv(energy))
    shape = m.minus(F2,m.times(lagrange,E2))
    return [m.encode(shape[4].re),m.encode(shape[4].im)]


expected = json.loads(Path(__file__).with_name('expected.json').read_text())
beta = (392-1197*m.V+945*m.V**2)/20
for label,w in [('zero_mean',0),('stationary_mean',beta)]:
    actual = calculate(w)
    if actual != expected['transverse_t4_'+label]:
        raise ValueError('order-four residue route mismatch: '+label)
print(json.dumps({'status':'both complete t4 polynomials agree',
                  'original_input_sha256':sha256(path.read_bytes()).hexdigest(),
                  'arithmetic':'author rational Laurent/Gaussian kernel, input order12',
                  'scope':'secondary residue/discriminant comparison; independent checker imports no author code'},sort_keys=True))
