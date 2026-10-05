"""Exact finite corroboration of PROOF.md; no sign decision or CAD.

Python 3.12.14 / SymPy 1.14.0. All symbolic arithmetic is in characteristic
zero over QQ. The six coefficient variables are ordered E,G,J,c,u,v.
The only determinant expansions are at finitely many rational fixtures.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp

E, G, J, c, u, v, z, t, X, Y = sp.symbols("E G J c u v z t X Y")
variables = (E, G, J, c, u, v)
checks = []


def require(condition, label):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)


def equal(a, b, label):
    require(sp.expand(a-b) == 0, label)


def moments(p, limit):
    a = sp.Poly(p, z).all_coeffs()
    n = len(a)-1
    require(a[0] == 1, "monic Newton input")
    out = [sp.Integer(n)]
    for k in range(1, limit+1):
        val = sum(a[j]*out[k-j] for j in range(1, min(n,k-1)+1))
        if k <= n:
            val += k*a[k]
        out.append(sp.expand(-val))
    return out


def bezout(a, b):
    ac = [sp.expand(a).coeff(z, i) for i in range(8)]
    bc = [sp.expand(b).coeff(z, i) for i in range(7)]
    result = sp.zeros(7)
    for i, ai in enumerate(ac):
        for j, bj in enumerate(bc):
            if i > j:
                for k in range(i-j):
                    result[i-1-k,j+k] += ai*bj
            elif i < j:
                for k in range(j-i):
                    result[j-1-k,i+k] -= ai*bj
    result = result.applyfunc(sp.expand)
    require(result == result.T, "whole Bezout symmetry")
    kernel = sum(result[i,j]*X**i*Y**j for i in range(7) for j in range(7))
    equal((X-Y)*kernel,
          a.subs(z,X)*b.subs(z,Y)-a.subs(z,Y)*b.subs(z,X),
          "whole Bezout kernel identity")
    return result


def terms(expr, names):
    p = sp.Poly(expr, *names, domain=sp.QQ)
    return [[list(power), int(coef.p), int(coef.q)] for power,coef in p.terms()]


def rational(expr):
    expr = sp.Rational(expr)
    return [int(expr.p), int(expr.q)]


f = z**8-z**6/2-u*z**5/3+2*E*z**4+(u/6-v/5)*z**3+4*G*z**2+8*J*z+c
h = sp.diff(f,z)/8
r = sp.expand(8*z*h-8*f)
equal(r,z**6+u*z**5-8*E*z**4+(v-5*u/6)*z**3-24*G*z**2-56*J*z-8*c,
      "complete six-coefficient resolvent numerator")
mu = moments(f,14)
for k,value in [(1,0),(2,1),(3,u),(5,v)]:
    equal(mu[k],value,"chart moment "+str(k))
D = sp.Rational(3,8)-8*E
equal(mu[4]-sp.Rational(1,8),D,"variance statistic")
H8 = sp.Matrix(8,8,lambda i,j:mu[i+j])
B0, Br = bezout(h,sp.diff(h,z)), bezout(h,r)

heat = sp.expand(sum((-t)**j/sp.factorial(j)*sp.diff(f,z,2*j) for j in range(5)))
heat_expected = (z**8-(sp.Rational(1,2)+56*t)*z**6-u*z**5/3
 +(2*E+15*t+840*t**2)*z**4+(u/6-v/5+20*u*t/3)*z**3
 +(4*G-24*E*t-90*t**2-3360*t**3)*z**2
 +(8*J-u*t+6*v*t/5-20*u*t**2)*z
 +c-8*G*t+24*E*t**2+60*t**3+1680*t**4)
equal(heat,heat_expected,"complete backward heat coefficient identity")
heat_mu = moments(heat,5)
A = 1+112*t
for k,value in [(1,0),(2,A),(3,u),(5,v+60*t*u)]:
    equal(heat_mu[k],value,"unnormalized heat moment "+str(k))
# Pay the normalized z^3 coefficient, where both odd moments interact.
equal(u*A/6-(v+60*t*u)/5,u/6-v/5+20*u*t/3,
      "normalized third-degree chart coefficient")
w = v+60*t*u
residual = u**2/A**3+w**2/A**5
equal(sp.cancel(sp.diff(residual,t)*A**6),
      -(60*(A*u-w)**2+276*A**2*u**2+500*w**2),
      "complete residual derivative square certificate")

alpha = sp.Rational(1,112)
hermite = sp.expand(sum((-alpha)**j/sp.factorial(j)*sp.diff(z**8,z,2*j) for j in range(5)))
hermite_mu = moments(hermite,5)
equal(hermite_mu[2],1,"Hermite fixed-profile norm")
equal(hermite_mu[4]-sp.Rational(1,8),sp.Rational(3,28),"Hermite fixed-profile variance")
hermite_h = sp.diff(hermite,z)/8
equal(8*z*hermite_h-8*hermite,sp.diff(hermite_h,z)/7,
      "Hermite seven equal angular masses")


def parameters(p):
    a = sp.Poly(p,z)
    pm = moments(p,5)
    result = {E:a.nth(4)/2,G:a.nth(2)/4,J:a.nth(1)/8,c:a.nth(0),u:pm[3],v:pm[5]}
    equal(f.subs(result),p,"entire fixture chart substitution")
    return result


def fixture(label,p,originals=None):
    data = parameters(p)
    moment_values = [sp.Rational(a.subs(data)) for a in mu]
    H = H8.subs(data)
    if originals is not None:
        direct = [sum(a**k for a in originals) for k in range(15)]
        require(moment_values == direct,"all15 direct original fixture moments: "+label)
        require(H == sp.Matrix(8,8,lambda i,j:direct[i+j]),"whole direct Hermite fixture: "+label)
        require(sum(originals)==0 and sum(a*a for a in originals)==1,
                "actual fixture balance/norm: "+label)
    leading = [H[:k,:k].det(method="domain-ge") for k in range(1,9)]
    require(all(a>0 for a in leading),"eight strict Hermite fixture determinants: "+label)
    hq, rq = h.subs(data), r.subs(data)
    b0, br = B0.subs(data), Br.subs(data)
    det_poly = sp.Poly((b0+t*br).det(method="domain-ge"),t,domain=sp.QQ)
    delta = b0.det(method="domain-ge")
    require(delta>0,"positive actual critical discriminant: "+label)
    equal(delta,sp.discriminant(hq,z),"whole discriminant fixture identity: "+label)
    # Definition-level residue interpolant in QQ[z]/h, using exact Bezout inverse.
    inverse = sp.invert(sp.diff(hq,z),hq,z)
    mass = sp.rem(rq*inverse,hq,z)
    multiplication = sp.Matrix(7,7,lambda i,j:sp.Poly(sp.rem(mass*z**j,hq,z),z).nth(i))
    char = multiplication.charpoly().all_coeffs()
    expected = [(-1)**k*char[k] for k in range(8)]
    actual = [det_poly.nth(k)/delta for k in range(8)]
    require(actual == expected,"all8 determinant/residue coefficients: "+label)
    equal(sp.trace(multiplication),1,"actual fixture mass sum: "+label)
    eta = sp.trace(multiplication*multiplication)
    N = det_poly.nth(2)
    equal(2*N/delta,1-eta,"entire angular numerator fixture: "+label)
    d = D.subs(data)
    require(d>0,"positive simple original variance: "+label)
    value = (1-eta)/d
    for threshold in [value-1,value+1]:
        equal(threshold*d*delta-2*N,d*delta*(threshold-value),
              "legal threshold clearing fixture: "+label)
    return {"label":label,"parameters":{str(a):rational(data[a]) for a in variables},
            "leading_Hermite_determinants":[rational(a) for a in leading],
            "delta":rational(delta),"determinant_coefficients":[rational(det_poly.nth(k)) for k in range(8)],
            "residue_multiplication_matrix":[[rational(a) for a in row] for row in multiplication.tolist()],
            "eta":rational(eta),"D":rational(d),"C":rational(value)}


even_roots = [sp.Rational(a,42) for a in [-19,-15,-14,-10,10,14,15,19]]
general_roots = [sp.Rational(a,70) for a in [21,-43,31,-37,0,6,10,12]]
even = sp.expand(sp.prod(z-a for a in even_roots))
general = sp.expand(sp.prod(z-a for a in general_roots))
fixtures = [fixture("even distinct rational originals",even,even_roots),
            fixture("general distinct rational originals",general,general_roots),
            fixture("nonsymmetric exactZ Hermite-licensed originals",even+8*z/sp.Integer(10)**12),
            fixture("Hermite fixed profile",hermite)]
require(fixtures[-1]["C"] == [8,1],"Hermite exact angular value8")

# Original-root licensing is essential even if h stays simple-real.
invalid = even+1
bad_parameters = parameters(invalid)
require(h.subs(bad_parameters)==sp.diff(even,z)/8,"infeasible constant shift keeps critical polynomial")
bad_leading = [H8.subs(bad_parameters)[:k,:k].det(method="domain-ge") for k in range(1,9)]
require(not all(a>0 for a in bad_leading),"Hermite licence rejects infeasible constant shift")
uniform = (z**2-sp.Rational(1,8))**4
uniform_parameters = parameters(uniform)
uniform_leading = [H8.subs(uniform_parameters)[:k,:k].det(method="domain-ge") for k in range(1,9)]
require(not all(a>0 for a in uniform_leading),"strict licence excludes uniform collision")
equal(D.subs(uniform_parameters),0,"uniform zero denominator retained")
ut = sp.expand(heat.subs(uniform_parameters).subs(t,alpha))
uf = sp.Poly(ut,z)
uniform_regularized = sum(uf.nth(k)*2**sp.Rational(k-8,2)*z**k for k in range(9))
fixtures.append(fixture("normalized regularized uniform collision",uniform_regularized))

records = {"polynomial_domain":"QQ[E,G,J,c,u,v]", "variables":[str(a) for a in variables],
           "mu_0_to_14":[terms(a,variables) for a in mu],
           "Hermite8":[[terms(a,variables) for a in row] for row in H8.tolist()],
           "B0":[[terms(a,variables) for a in row] for row in B0.tolist()],
           "Br":[[terms(a,variables) for a in row] for row in Br.tolist()],
           "heat_variables":[str(a) for a in (*variables,t,z)],
           "whole_heat_coefficients":terms(heat,(*variables,t,z)),
           "fixtures":fixtures,
           "negative_controls":{"infeasible_constant_shift_leading_minors":[rational(a) for a in bad_leading],
                                "uniform_leading_minors":[rational(a) for a in uniform_leading]},
           "checks":checks}
payload = (json.dumps(records,sort_keys=True,separators=(",",":"))+"\n").encode()
parser = argparse.ArgumentParser()
parser.add_argument("--records",type=Path,required=True,help="write the complete exact record outside the source tree")
args = parser.parse_args()
args.records.parent.mkdir(parents=True,exist_ok=True)
args.records.write_bytes(payload)
print(json.dumps({"python":platform.python_version(),"sympy":sp.__version__,
                  "record_bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),
                  "complete_checks":len(checks),"fixtures":len(fixtures),
                  "expanded_multivariate_determinants":False,
                  "QE_or_sign_decision":False},sort_keys=True))
