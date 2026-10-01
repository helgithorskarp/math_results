#!/usr/bin/env python3
"""Exact finite algebra for the ordinary analytic proof; stdlib CPython3.10+."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mul(p, q):
    out = [F(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out


def power(p, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def ev(p, x):
    out = x*0
    for c in reversed(p):
        out = out*x+c
    return out


def ga(x=0, y=0):
    return F(x), F(y)


def gadd(z, w):
    return z[0]+w[0], z[1]+w[1]


def gscale(z, c):
    return z[0]*c, z[1]*c


def gmul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def gnorm(z):
    return z[0]**2+z[1]**2


def ginv(z):
    n = gnorm(z)
    require(n != 0, 'Gaussian reciprocal pole')
    return z[0]/n, -z[1]/n


def gpower(z, n):
    out = ga(1)
    for _ in range(n):
        out = gmul(out, z)
    return out


def gev(p, z):
    out = ga()
    for c in reversed(p):
        out = gadd(gmul(out, z), ga(c))
    return out


def elementary(xs, n):
    out = [ga(1)]+[ga()]*n
    for x in xs:
        for k in range(n, 0, -1):
            out[k] = gadd(out[k], gmul(out[k-1], x))
    return out


def origin_convolution(a, qs):
    coeff = [ga(1)]
    for q in qs:
        inv = ginv(q)
        nxt = [ga()]*(len(coeff)+1)
        for k, c in enumerate(coeff):
            nxt[k] = gadd(nxt[k], gmul(c, inv))
            nxt[k+1] = gadd(nxt[k+1], gscale(c, -a))
        coeff = nxt
    out = ga()
    for k, c in enumerate(coeff):
        out = gadd(out, gscale(c, F(9,k+1)))
    return out


def weights():
    nodes = tuple(F(i,8) for i in range(9))
    ws = []
    for i, x in enumerate(nodes):
        p, d = [F(1)], F(1)
        for j, y in enumerate(nodes):
            if i != j:
                p = mul(p, [-y, F(1)])
                d *= x-y
        ws.append(sum(c/F(k+1) for k,c in enumerate(p))/d)
    for k in range(9):
        require(sum(w*x**k for w,x in zip(ws,nodes)) == F(1,k+1),
                'interpolation integral weight identity')
    return nodes, ws


def origin_interpolation(a, qs, nodes, ws):
    out = ga()
    for t, w in zip(nodes,ws):
        p = ga(1)
        for q in qs:
            p = gmul(p, gadd(ginv(q),ga(-a*t)))
        out = gadd(out,gscale(p,9*w))
    return out


# Sparse Q-polynomials in seven indeterminates. These identities hold over C.
ZERO = (0,)*7


def pa(p, q, scale=F(1)):
    out = p.copy()
    for k,c in q.items():
        out[k] = out.get(k,F(0))+scale*c
        if out[k] == 0:
            del out[k]
    return out


def pm(p, q):
    out = {}
    for k,c in p.items():
        for l,d in q.items():
            key = tuple(i+j for i,j in zip(k,l))
            out[key] = out.get(key,F(0))+c*d
    return {k:c for k,c in out.items() if c}


def pp(p,n):
    out = {ZERO:F(1)}
    for _ in range(n):
        out = pm(out,p)
    return out


def balanced_newton():
    xs = [{tuple(int(j==i) for j in range(7)):F(1)} for i in range(7)]
    xs.append({k:-c for p in xs for k,c in p.items()})
    es = [{ZERO:F(1)}]+[{} for _ in range(4)]
    for x in xs:
        for k in range(4,0,-1):
            es[k] = pa(es[k],pm(es[k-1],x))
    ps = []
    for k in range(5):
        p = {}
        for x in xs:
            p = pa(p,pp(x,k))
        ps.append(p)
    require(es[1] == {}, 'balance identity')
    require(pa(es[2],ps[2],F(1,2)) == {}, 'full e2 identity')
    require(pa(es[3],ps[3],-F(1,3)) == {}, 'full e3 identity')
    rhs = pa({},pm(ps[2],ps[2]),F(1,8))
    rhs = pa(rhs,ps[4],-F(1,4))
    require(es[4] == rhs, 'full e4 identity')
    return [len(es[k]) for k in range(1,5)]


def derive():
    h,s,a0,c = F(1,32),F(1,16),F(511,512),F(27,56)
    bs = []
    for k in range(9):
        b = [F(0)]*10
        for j in range(9-k):
            b[k+j+1] = F(9*(-1)**(k+j)*comb(8-k,j),k+j+1)
        # Distinct route: multiply z^k by eight-minus-k linear factors,
        # then integrate the full coefficient vector.
        derivative = [F(0)]*k+power([F(1),F(-1)],8-k)
        derivative = [9*(-1)**k*x for x in derivative]
        other = [F(0)]+[x/F(j+1) for j,x in enumerate(derivative)]
        require(b == other, 'two full B coefficient routes')
        require([j*b[j] for j in range(1,10)] == derivative, 'full derivative')
        require(ev(b,F(1)) == F((-1)**k,comb(8,k)), 'B endpoint')
        bs.append(b)
    require(bs[0] == [int(i==0)-x for i,x in enumerate(power([1,-1],9))],
            'B0 exact tail')
    newton_counts = balanced_newton()
    L = h/3+F(5,4)*h*h+sum(F(comb(8,k),8)*h**(k-2) for k in range(5,9))
    t0 = (F(1,2)+L)*8*h*h
    tails = [F(9,9-k)*(1+s)**k*s**(9-k) for k in range(2,9)]
    dbounds = [abs(F((-1)**k,comb(8,k))-1)+tails[k-2]+s**9 for k in range(2,9)]
    require(all(v < F(6,5) for v in dbounds),'all seven D bounds')
    d2 = tails[0]+s**9
    e0 = (d2/2+F(6,5)*L+c*t0)/(1-t0)
    require(e0 < F(1,60),'uniform error: denominator correction must use c*T0')
    radial = F(27,28)-F(1,30)
    angular = 18*a0**18/(16*(1+h))-F(27,28)-F(1,30)
    require(radial > F(7,8) and angular > F(1,32),'coercivity signs')
    require(1-18*(1-a0) > F(1,2),'R18 lower bound')
    require(a0**-2 < 2 and 8*(1-a0)**3 < 1,'tail absorption')
    require(2*(1-a0) == s*s,'uniform complex parameter range')
    nodes,ws = weights()
    controls, records = 0, []
    for scale in (1,2,4,8):
        a = 1-F(1,512*scale)
        for pattern in range(8):
            radii = [1+F((1 if (j+pattern)%2 else -1),128*scale) for j in range(8)]
            qs = []
            for j,r in enumerate(radii):
                t = F((j+pattern)%3-1,128*scale)
                w = ga((1-t*t)/(1+t*t),2*t/(1+t*t))
                require(gnorm(w) == 1, 'unit-phase control')
                qs.append(gscale(w,r))
            m = gscale(tuple(map(sum,zip(*qs))),F(1,8))
            require(sum(radii) == 8 and m[0] >= a,'mean control domain')
            etas = [gadd(gmul(q,ginv(m)),ga(-1)) for q in qs]
            require(all(gnorm(e) <= h*h for e in etas),'tube control domain')
            U = sum(e[0]**2 for e in etas);V = sum(e[1]**2 for e in etas)
            O = origin_convolution(a,qs)
            require(O == origin_interpolation(a,qs,nodes,ws),'full independent origin integral')
            es = elementary(etas,8);z = gscale(m,a)
            num = ga()
            for b,ek in zip(bs,es):
                num = gadd(num,gmul(gev(b,z),ek))
            den = ga()
            for ek in es:
                den = gadd(den,ek)
            K = gscale(gmul(gpower(m,9),O),a)
            require(K == gmul(num,ginv(den)),'full balanced origin identity')
            lower = 1+(1-a)+F(7,8)*U+F(1,32)*V
            require(gnorm(O) >= lower,'quantitative theorem control')
            records.append(str(gnorm(O)-lower))
            controls += 1
    coeff_strings = [[str(x) for x in b] for b in bs]
    return {'schema':1,'author':'six-sendov-1','role':'researcher',
        'status':'finite algebra for an ordinary proof; independent review pending',
        'full_first_power_endpoint_proved':False,'abstract_individual_disks_required':False,
        'a_min':str(a0),'relative_tube':str(h),'radial_cost':'7/8','angular_cost':'1/32',
        'B_full_coefficients':coeff_strings,'B_routes':2,'B_derivative_and_endpoint_identities':18,
        'balanced_Newton_nonzero_coefficients':newton_counts,'balanced_Newton_identities':4,
        'L':str(L),'T0':str(t0),'D_full_bounds':[str(x) for x in dbounds],
        'uniform_error_E0':str(e0),'error_majorant':'1/60',
        'radial_coefficient':str(radial),'angular_coefficient':str(angular),
        'origin_convolution_interpolation_controls':controls,'balanced_origin_controls':controls,
        'coercivity_controls':controls,'controls_sha256':hashlib.sha256('\n'.join(records).encode()).hexdigest()}


def validate(expected, derived):
    require(expected == derived,'complete fixture mismatch')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-fixture',action='store_true')
    args = parser.parse_args()
    derived = derive()
    if args.emit_fixture:
        print(json.dumps(derived,sort_keys=True,indent=2))
        return
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    validate(expected,derived)
    damaged = []
    for key,value in [('relative_tube','1'),('error_majorant','1/64'),
                      ('full_first_power_endpoint_proved',True),('B_routes',1)]:
        bad = copy.deepcopy(expected);bad[key] = value;damaged.append(bad)
    bad = copy.deepcopy(expected);bad['B_full_coefficients'][2][3]='0';damaged.append(bad)
    bad = copy.deepcopy(expected);bad['uniform_error_E0']='0';damaged.append(bad)
    for bad in damaged:
        try:
            validate(bad,derived)
        except ValueError:
            continue
        raise ValueError('damaged fixture accepted')
    print(json.dumps({'result':'PASS','rejected_corruptions':len(damaged),**derived},sort_keys=True))


if __name__ == '__main__':
    main()
