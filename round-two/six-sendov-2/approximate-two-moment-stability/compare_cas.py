"""Whole alternate SymPy checks, same author; no independent review."""
from pathlib import Path
import importlib.util
import hashlib
import json
import resource
import time
import sympy as S

started = time.monotonic()
here = Path(__file__).resolve().parent
fixture = json.loads((here/'expected.json').read_text())
spec = importlib.util.spec_from_file_location('own_raw_chart_transport', here/'verify.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
native = V.build()
variables = S.symbols('B E r s t F G J p0 p1 p2')
B,E,r,s,t,Fc,G,J,p0,p1,p2 = variables
z,theta = S.symbols('z theta')
ring = S.QQ.frac_field(t).poly_ring(*(v for v in variables if v != t))
checks = {}
coefficient_count = 0

def encode(expression):
    numerator, denominator = S.fraction(S.cancel(expression))
    monomial = S.Poly(denominator, t, domain=S.QQ)
    if len(monomial.terms()) != 1:
        raise ValueError('unexpected localization outside t')
    (shift,), scale = monomial.terms()[0]
    rows = []
    for key, coefficient in S.Poly(numerator, *variables, domain=S.QQ).terms():
        if coefficient:
            powers = list(key)
            powers[4] -= shift
            rows.append([powers, str(coefficient/scale)])
    return sorted(rows)

def seq(poly):
    length = 1 if poly.is_zero else poly.degree()+1
    return [poly.nth(i) for i in range(length)]

def compare(name, polynomials, native_polynomials):
    global coefficient_count
    left = [encode(a) for a in polynomials]
    right = [V.P(a).encoded() for a in V.ut(native_polynomials)]
    if left != right:
        raise ValueError('ENTIRE alternate polynomial map '+name)
    coefficient_count += len(left)
    checks[name] = True

def maps(hcoeff, pcoeff):
    h = S.Poly(sum(a*z**i for i,a in enumerate(hcoeff)),z,domain=ring)
    p = S.Poly(sum(a*z**i for i,a in enumerate(pcoeff)),z,domain=ring)
    primitive = S.Poly(sum(8*h.nth(i)*z**(i+1)/S.Integer(i+1) for i in range(8)),z,domain=ring)
    Q, residual = (8*primitive+p*h.diff()).div(h, auto=False)
    O = p*h.diff((z,2))+(p.diff()-Q)*h.diff()+(64-Q.diff())*h
    x = sum(h.nth(7-i)*theta**i for i in range(1,8))
    logseries = S.Poly(-x+x*x/2-x*x*x/3,theta,domain=ring)
    tau = [S.Integer(7)]+[i*logseries.nth(i) for i in range(1,7)]
    def T(poly):
        normal = poly.rem(h, auto=False)
        result = sum(normal.nth(k)*(sum(tau[j]*z**(k-1-j) for j in range(k))-k*z**(k-1))
                     for k in range(1,7))
        return S.Poly(result,z,domain=ring)
    ps = (p*p).rem(h, auto=False)
    W = (p*(Q-p.diff())).rem(h, auto=False)
    K = -16*p-T(T(ps))*S.Rational(1,4)+T(W)*S.Rational(1,4)
    if O.degree() > 5 or K.degree() > 5:
        raise ValueError('entire higher coefficient cancellation')
    return {'Q':seq(Q),'residual':seq(residual),'ODE':seq(O),'K':seq(K),'p2':seq(ps),'W':seq(W)}

def nth(poly, i):
    return poly[i] if i<len(poly) else S.Integer(0)

h = [J,G,Fc,E,B,-S.Rational(3,8),0,1]
coefficient = maps(h,[p0,p1,p2,r,s,t])
raw = maps(h,[p0,p1,p2,r*t,s*t,t])
p2star = 8+t*(5*B/S.Integer(7)-27*s/S.Integer(56)-r*s)
step = maps(h,[p0,p1,p2star,r*t,s*t,t])
x0 = S.cancel(-nth(step['ODE'],5).subs(p0,0)/42)
x1 = S.cancel(-4*nth(step['ODE'],4).subs(p1,0)/15)
compfull = maps(h,[x0,x1,p2star,r*t,s*t,t])
composed = {name:compfull[name] for name in ['ODE','K']}
gF = S.cancel(-nth(composed['K'],4).subs(G,0)/(24*t*t))
k3 = S.cancel(nth(composed['K'],3).subs(G,gF))
Fstar = S.cancel(14*k3.subs(Fc,0)/(15*t*t))
Gstar = S.cancel(gF.subs(Fc,Fstar))
o3 = S.cancel(nth(composed['ODE'],3).subs({Fc:Fstar,G:Gstar},simultaneous=True))
Jstar = S.cancel(o3.subs(J,0)/(28*t))
P0star = S.cancel(x0.subs({Fc:Fstar,G:Gstar},simultaneous=True))
P1star = S.cancel(x1.subs({Fc:Fstar,G:Gstar},simultaneous=True))
hstar = [Jstar,Gstar,Fstar,E,B,-S.Rational(3,8),0,1]
pstar = [P0star,P1star,p2star,r*t,s*t,t]
final = maps(hstar,pstar)
residuals = [t*nth(final['ODE'],i) for i in [2,1,0]]+[nth(final['K'],1),nth(final['K'],0)+4]
data = {'coefficient':coefficient,'raw':raw,'p2stage':step,'composed':composed,'final':final}
for stage, stage_maps in data.items():
    for name, polynomials in stage_maps.items():
        compare(stage+'.'+name, polynomials, native[stage][name])
single = {'p2star':p2star,'p0affine':x0,'p1affine':x1,'gF':gF,
          'Fstar':Fstar,'Gstar':Gstar,'Jstar':Jstar}
for name, polynomial in single.items():
    compare(name,[polynomial],[native[name]])
compare('hstar',hstar,native['hstar'])
compare('pstar',pstar,native['pstar'])
compare('ALL_FIVE_final_residuals',residuals,native['residuals'])
phi = [nth(coefficient['ODE'],i) for i in range(6)]+[
    nth(coefficient['K'],i)+(4 if i==0 else 0) for i in [0,1,3,4,5]]
if [encode(a) for a in phi] != fixture['whole_coefficient_phi']:
    raise ValueError('ENTIRE eleven-row coefficient Phi')
gradient_norms = []
for i,a in enumerate(phi):
    norm = S.Integer(0)
    for j,v in enumerate(variables):
        derivative = S.diff(a,v)
        if encode(derivative) != V.diffvar(native['coefficient_phi'][i],j).encoded():
            raise ValueError('ENTIRE gradient polynomial '+str((i,j)))
        norm += sum(abs(S.Rational(c)) for key,c in encode(derivative))
    gradient_norms.append(str(norm))
if gradient_norms != fixture['whole_gradient_row_norms'] or len(checks) != 36:
    raise ValueError('complete map count or row-gradient norm')

print(json.dumps({'actual_agent':'six-sendov-2','role':'researcher',
    'same_author_only':True,'independent_review':False,'complete':True,
    'SymPy':S.__version__,'entire_maps_compared':len(checks),
    'every_coefficient_polynomial_compared':coefficient_count,
    'whole_gradient_polynomials_compared':121,
    'all_whole_comparisons':checks,
    'whole_fixture_sha256':hashlib.sha256(V.canonical(fixture)).hexdigest(),
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
