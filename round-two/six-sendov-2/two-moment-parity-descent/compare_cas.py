"""Optional same-author SymPy 1.14 whole polynomial comparison."""
import importlib.util
from pathlib import Path
import json
import time
import sympy as s

started = time.monotonic()
path = Path(__file__).with_name('verify.py')
spec = importlib.util.spec_from_file_location('parity_author_checker', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
record, _, _, _ = m.universal()
z, e, g, j, c = s.symbols('z E G J c')
symbols = [e, g, j, c]
f = z**8-z**6/s.Integer(2)+2*e*z**4+4*g*z**2+8*j*z+c
h = s.diff(f, z)/8
# Logarithmic derivative at infinity independently yields the whole traces.
t = s.symbols('t')
trace_series = s.series((z*s.diff(h,z)/h).subs(z,1/t), t, 0, 12).removeO().expand()
traces = [trace_series.coeff(t,k) for k in range(12)]
moment_series = s.series((8*(z*h-f)/h).subs(z,1/t), t, 0, 8).removeO().expand()
moments = [moment_series.coeff(t,k+1) for k in range(7)]
gram = [[traces[i+k] for k in range(6)] for i in range(6)]
def polynomial(r):
    return sum(s.Rational(a)*s.prod(v**k for v,k in zip(symbols,monomial))
               for monomial,a in r)
def equal(a, r):
    if s.Poly(s.expand(a-polynomial(r)), *symbols) != 0:
        raise ValueError('whole CAS coefficient-polynomial mismatch')
for a,r in zip(traces,record['traces']): equal(a,r)
for a,r in zip(moments,record['coupling_moments']): equal(a,r)
for row,records in zip(gram,record['gram']):
    for a,r in zip(row,records): equal(a,r)
for index,var in enumerate(symbols):
    for row,records in zip(gram,record['all_four_gram_derivatives'][index]):
        for a,r in zip(row,records): equal(s.diff(a,var),r)
    for a,r in zip(moments[:6],record['all_four_moment_derivatives'][index]):
        equal(s.diff(a,var),r)
print(json.dumps({'complete':True,'sympy_version':s.__version__,
                  'whole_coefficient_polynomials_compared':12+7+36+144+24,
                  'same_author_not_independent_review':True,
                  'elapsed_seconds':round(time.monotonic()-started,6)}))
