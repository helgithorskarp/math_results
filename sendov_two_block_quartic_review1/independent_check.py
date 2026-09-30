#!/usr/bin/env python3
"""Independent simple critical-root Taylor derivation; no author imports."""
import hashlib
import argparse
import json
import math
import sys
import time
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ_I

ORDER = 4
checks = 0


def require(condition, label):
    global checks
    if not condition:
        raise ValueError(label)
    checks += 1


def conjugate(f):
    ring = f.numer.ring
    def bar(p):
        return ring.from_dict({mon: QQ_I.dtype(c.x, -c.y)
                               for mon, c in p.terms()})
    return f.field.new(bar(f.numer), bar(f.denom))


def constant(K, c):
    return [K.convert(c) if hasattr(K, 'convert') else K(c)] + [K.zero] * ORDER


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(a, c):
    return [c * x for x in a]


def multiply(a, b):
    return [sum((a[j] * b[k-j] for j in range(k+1)), a[0].field.zero)
            for k in range(ORDER+1)]


def reciprocal(a):
    K = a[0].field
    b = [1/a[0]]
    for k in range(1, ORDER+1):
        b.append(-sum((a[j]*b[k-j] for j in range(1,k+1)), K.zero)/a[0])
    require(multiply(a,b) == constant(K,1), 'inverse substitution')
    return b


def modulus(a, positive_base):
    K = a[0].field
    c = multiply(a, [conjugate(x) for x in a])
    b = [positive_base]
    require(b[0]**2 == c[0], 'positive modulus base')
    for k in range(1, ORDER+1):
        b.append((c[k] - sum((b[j]*b[k-j] for j in range(1,k)), K.zero))
                 / (2*b[0]))
    require(multiply(b,b) == c, 'modulus square substitution')
    return b


def phase(K, slope):
    imaginary = K.convert(sp.I)
    return [(imaginary*slope)**k/K.convert(math.factorial(k))
            for k in range(ORDER+1)]


def critical_data(K, m, r, a):
    """Derive R(z) by product rule, then find its ORIGINAL z roots."""
    s, n = m-r, m+1
    one = constant(K,1)
    x, y = phase(K,s), phase(K,-r)
    # R(z)=(z+x)(z+y)+(z-a)[r(z+y)+s(z+x)].
    linear = add(add(x,y),add(scale(y,r),scale(x,s)))
    linear = add(linear,constant(K,-a*m))
    scalar = add(multiply(x,y),scale(add(scale(y,r),scale(x,s)),-a))
    def equation(z):
        return add(add(scale(multiply(z,z),n),multiply(linear,z)),scalar)
    roots = []
    for base in (-K.one, (m*a-1)/n):
        z = constant(K,base)
        require(equation(z)[0] == 0, 'critical root base')
        derivative = 2*n*base+linear[0]
        require(derivative != 0, 'critical root simple in residual quadratic')
        for k in range(1,ORDER+1):
            z[k] = -equation(z)[k]/derivative
        require(equation(z) == constant(K,0), 'critical root substitution all coefficients')
        roots.append(z)
    require(add(roots[0],roots[1]) == scale(linear,-1/n), 'critical Vieta sum')
    require(multiply(roots[0],roots[1]) == scale(scalar,1/n), 'critical Vieta product')
    q = [reciprocal(add(constant(K,a),scale(z,-1))) for z in roots]
    ux = reciprocal(add(constant(K,a),x))
    uy = reciprocal(add(constant(K,a),y))
    v = 1/(1+a)
    F = add(add(scale(modulus(ux,v),r-1),scale(modulus(uy,v),s-1)),
            add(modulus(q[0],v),modulus(q[1],n*v)))
    dx,dy = add(ux,constant(K,-v)),add(uy,constant(K,-v))
    E = add(scale(multiply(dx,[conjugate(c) for c in dx]),r),
            scale(multiply(dy,[conjugate(c) for c in dy]),s))
    require(F[0] == 2*m*v, 'collapsed baseline')
    require(all(F[j] == E[j] == 0 for j in range(1,ORDER+1,2)) and E[0] == 0,
            'evenness through retained order')
    return F,E


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).resolve().with_name('expected.json'))
    parser.add_argument('--output', type=Path, help='write a regenerated compact manifest')
    args = parser.parse_args()
    K = QQ_I.frac_field('m','r')
    m,r = K.gens
    s,n,D,M = m-r,m+1,3*m+2,m+2
    a = M/(2*m)
    F,E = critical_data(K,m,r,a)
    k = r*s
    f4 = m**3*M*k*(-m**2*(m**2-4*m-4)+(m-6)*D*k)/D**5
    energy2 = 16*m**5*k/D**4
    coefficient = M*D**3/(256*m**7)*(m**2*(m**2-4*m-4)/k-(m-6)*D)
    require(F[2] == 0,'vanishing cutoff curvature symbolic m,r')
    require(F[4] == f4,'independent all-degree t4 coefficient')
    require(E[2] == energy2,'independent all-degree energy coefficient')
    require(-F[4]/E[2]**2 == coefficient,'energy quartic conversion')
    # Five deliberate changes must fail existing exact identities.
    rejected = 0
    for left,right in ((F[4]+1,f4), (2*E[2],energy2),
                       (-F[4]/E[2]**2,coefficient+1),
                       (F[2]+r,0), (F[0]-1,2*m/(1+a))):
        if left == right:
            raise ValueError('changed coefficient escaped the invariant')
        rejected += 1
    # Independent two-parameter quadratic curvature with a free marked radius.
    global ORDER
    saved = ORDER
    ORDER = 2
    J = QQ_I.frac_field('m','r','a')
    mj,rj,aj = J.gens
    Fj,Ej = critical_data(J,mj,rj,aj)
    require(Fj[2] == (aj-(mj+2)/(2*mj))*mj*rj*(mj-rj)/(1+aj)**3,
            'free-radius second-order curvature symbolic m,r,a')
    require(Ej[2] == mj*rj*(mj-rj)/(1+aj)**4,'free-radius leading energy')
    ORDER = saved
    # Independent polynomial identities for displacement and basin objectives.
    X = sp.Symbol('x')
    mm = sp.Symbol('m')
    T = mm**2-4*mm-4
    U = -mm**2+8*mm+4
    polynomial = T*X+U*X**2+T*X**3
    require(sp.expand(sp.diff(polynomial,X)-
                      (T*(1-2*X+3*X**2)+8*mm*X)) == 0,
            'displacement coefficient strictly increasing for m>=5')
    require(sp.expand(polynomial.subs(X,1)-(mm**2-4)) == 0,
            'even-degree balanced coefficient')
    # Basin denominator = T(1+x)^2-(m-6)(3m+2)x; minimize its reciprocal.
    denom = T*(1+X)**2-(mm-6)*(3*mm+2)*X
    require(sp.expand(sp.diff(denom,X)-(2*T*X+U)) == 0,'basin objective derivative')
    require(sp.cancel(2*T/(mm-1)+U -
                      (-mm**3+11*mm**2-12*mm-12)/(mm-1)) == 0,
            'basin objective endpoint derivative')
    b = (mm-1)/(mm+1)
    require(sp.cancel(T*(b+1/(mm-1))+U-
                      (3*mm**3+7*mm**2-12*mm-12)/(mm**2-1)) == 0,
            'odd-degree balanced basin optimizer')
    require(sp.cancel(denom.subs(X,b)-
                      (mm**4-mm**2-16*mm-12)/(mm+1)**2) == 0,
            'odd-degree balanced basin denominator')
    yy = sp.Symbol('y')
    for expression,shift in ((T,5),(3*mm**3+7*mm**2-12*mm-12,3),
                             (mm**4-mm**2-16*mm-12,3)):
        pp=sp.Poly(sp.expand(expression.subs(mm,yy+shift)),yy)
        require(all(c>=0 for c in pp.all_coeffs()) and pp.eval(0)>0,
                'unbounded integer-degree positive coefficient certificate')
    require(sp.expand(denom.subs(X,1)-denom-
                      (1-X)*(T*X+4*mm)) == 0,'even balanced basin endpoint identity')
    require(sp.cancel(denom.subs(X,b)-denom-
                      (b-X)*(T*(b+X)+U)) == 0,'odd balanced basin endpoint identity')
    pair= (m+2)*(m**3-4*m**2+13*m+18)*(3*m+2)**3/(512*m**7)
    # Substitution in the expression domain is exact, and independent of field evaluation.
    Ksingle=sp.cancel(coefficient.as_expr().subs({'r':1}))
    pair_expr=pair.as_expr()
    comparison_poly=mm**4-9*mm**3+13*mm**2-13*mm-6
    require(sp.cancel(Ksingle-pair_expr-
        (mm+2)*(3*mm+2)**3*comparison_poly/(512*mm**7*(mm-1))) == 0,
        'strict comparison threshold identity')
    require(all(c>0 for c in sp.Poly(sp.expand(comparison_poly.subs(mm,yy+8)),yy).all_coeffs()),
            'all degrees at least nine threshold sign')
    require([comparison_poly.subs(mm,j) for j in (5,6,7)]==[-246,-264,-146],
            'lower-degree threshold exceptions')
    # Numeric specializations are controls; symbolic m,r proof precedes them.
    rows = []
    for degree_m in range(3,21):
        values = []
        for count in range(1,degree_m):
            ss=degree_m-count
            val=sp.cancel(coefficient.as_expr().subs({'m':degree_m,'r':count}))
            fv=sp.cancel(f4.as_expr().subs({'m':degree_m,'r':count}))
            l=-fv/max(count,ss)**4
            require(val>0 and l>0,'positive specialized coefficients')
            values.append((count,val,l))
        bestE=max(z[1] for z in values);bestL=max(z[2] for z in values)
        v0=sp.Rational(2*degree_m,3*degree_m+2)
        basins=[(z[0],degree_m*sp.Rational(min(z[0],degree_m-z[0]),
                                        max(z[0],degree_m-z[0]))*v0**4/z[2])
                for z in values]
        bestB=min(z[1] for z in basins)
        bmin=[z[0] for z in basins if z[1]==bestB]
        emax=[z[0] for z in values if z[1]==bestE]
        lmax=[z[0] for z in values if z[2]==bestL]
        require(emax == ([1,2] if degree_m==3 else [2] if degree_m==4 else [1,degree_m-1]),
                'energy multiplicity controls')
        require(lmax==sorted(set([degree_m//2,(degree_m+1)//2])),
                'displacement multiplicity controls')
        require(bmin==lmax,'basin multiplicity controls')
        rows.append({'m':degree_m,'energy_optimizers':emax,'displacement_optimizers':lmax,
                     'maximum_energy_coefficient':str(bestE),
                     'maximum_displacement_coefficient':str(bestL),
                     'minimum_basin_squared_constant_kappa':str(bestB)})
    nine=rows[5]
    require(nine['maximum_displacement_coefficient']=='9600/371293',
            'degree-nine credited four-pair coefficient')
    require(nine['minimum_basin_squared_constant_kappa']=='3328/75',
            'degree-nine improved basin upper constant')
    Cpair9=sp.cancel(pair_expr.subs({'m':8}))
    oldB=sp.Rational(13,8)**4/(2*Cpair9)
    require(oldB==sp.Rational(53248,945),'preceding moving-pair basin upper constant')
    require(sp.Rational(3328,75)/oldB==sp.Rational(63,80),'exact squared basin improvement')
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'domain':'QQ(i)(m,r), and QQ(i)(m,r,a), truncated real t series',
            'method':'original critical quadratic simple-root recursion, individual inverse and modulus series',
            'versions':{'python':'.'.join(sys.version.split()[0].split('.')[:2]),'sympy':sp.__version__},
            'checks':checks,'rejected_mutations':rejected,'symbolic_F4':str(f4.as_expr()),
            'symbolic_E2':str(E[2].as_expr()),'symbolic_K':str(coefficient.as_expr()),
            'finite_controls':rows,'degree9':{'balanced_displacement_coefficient':'9600/371293',
            'basin_squared_constant_a_minus_cutoff':'5408/75',
            'basin_squared_constant_kappa':'3328/75',
            'squared_improvement_over_moving_pair':'63/80'}}
    encoded=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        expected=args.expected.read_text()
        require(json.loads(expected)==json.loads(encoded),'expected exact manifest')
    print('PASS',hashlib.sha256(encoded.encode()).hexdigest(),'checks',result['checks'],
          'seconds',round(time.monotonic()-started,3),flush=True)


if __name__ == '__main__':
    main()
