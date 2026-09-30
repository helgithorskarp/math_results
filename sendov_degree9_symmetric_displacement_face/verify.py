#!/usr/bin/env python3
"""Exact spectral formula and Bernstein proof for a displacement face.

Author: six-sendov-2 (researcher). Standard library only. All checks stay
active under python -O. The sparse polynomial kernel is adapted from this
author's prior four-block checker; no campaign module is imported.
"""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json


CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


class Poly:
    """Sparse Q[x,y], with exact scalar division only."""
    def __init__(self, value=0):
        if isinstance(value, Poly):
            value = value.t
        if isinstance(value, (int, Q)):
            value = {(0, 0): Q(value)}
        self.t = {p: Q(c) for p, c in value.items() if c}

    def __add__(self, other):
        t = dict(self.t)
        for p, c in Poly(other).t.items():
            t[p] = t.get(p, Q(0)) + c
        return Poly(t)

    __radd__ = __add__

    def __neg__(self):
        return Poly({p: -c for p, c in self.t.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        t = {}
        for p, c in self.t.items():
            for r, b in Poly(other).t.items():
                s = (p[0]+r[0], p[1]+r[1])
                t[s] = t.get(s, Q(0)) + c*b
        return Poly(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out = Poly(1)
        for _ in range(n):
            out *= self
        return out

    def __truediv__(self, other):
        if not isinstance(other, (int, Q)) or not other:
            raise ValueError('division requires a nonzero rational scalar')
        return Poly({p: c/Q(other) for p, c in self.t.items()})

    def __eq__(self, other):
        return self.t == Poly(other).t

    def value(self, x, y):
        return sum(c*Q(x)**i*Q(y)**j for (i,j),c in self.t.items())

    def dump(self):
        return [[i,j,str(c)] for (i,j),c in sorted(self.t.items())]


x = Poly({(1,0):1})
y = Poly({(0,1):1})


def diff(f, axis):
    return Poly({tuple(v-1 if j == axis else v for j,v in enumerate(p)):
                 p[axis]*c for p,c in f.t.items() if p[axis]})


def sub(f, a, b):
    a, b = Poly(a), Poly(b)
    ap = [a**i for i in range(1+max((i for i,j in f.t), default=0))]
    bp = [b**j for j in range(1+max((j for i,j in f.t), default=0))]
    out = Poly(0)
    for (i,j),c in f.t.items():
        out += c*ap[i]*bp[j]
    return out


def bernstein(f, box):
    x0,x1,y0,y1 = box
    transformed = sub(f, x0+(x1-x0)*x, y0+(y1-y0)*y)
    m = max((i for i,j in transformed.t), default=0)
    n = max((j for i,j in transformed.t), default=0)
    coefficients = {}
    for k in range(m+1):
        for l in range(n+1):
            coefficients[k,l] = sum(
                c*Q(comb(k,i),comb(m,i))*Q(comb(l,j),comb(n,j))
                for (i,j),c in transformed.t.items() if i<=k and j<=l)
    # Reverse reconstruction, rather than trusting a sign inventory alone.
    bx = [comb(m,i)*x**i*(1-x)**(m-i) for i in range(m+1)]
    by = [comb(n,j)*y**j*(1-y)**(n-j) for j in range(n+1)]
    rebuilt = Poly(0)
    for (i,j),c in coefficients.items():
        rebuilt += c*bx[i]*by[j]
    check(rebuilt == transformed, 'complete Bernstein inverse identity')
    return (m,n), coefficients


def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r,v in zip(a,b)]
    for j in range(n):
        candidates = [i for i in range(j,n) if a[i][j]]
        check(bool(candidates), 'nonsingular rational projection Gram matrix')
        i = candidates[0]
        a[j], a[i] = a[i], a[j]
        a[j] = [v/a[j][j] for v in a[j]]
        for i in range(j+1,n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u,v in zip(a[i],a[j])]
    out = [Q(0)]*n
    for j in range(n-1,-1,-1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1,n))
    return out


def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j,b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u,v in zip(r,b)]
        if any(r):
            j = next(j for j,v in enumerate(r) if v)
            pivots[j] = [v/r[j] for v in r]
            selected.append(original)
    return selected


def pinching(theta):
    """Definition-level control: Frobenius projection onto A's commutant."""
    check(len(theta) == 8 and sum(theta) == 0, 'balanced matrix profile')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/8
          for j in range(8)] for i in range(8)]
    pairs = list(combinations_with_replacement(range(8),2))
    metric = [Q(1 if i == j else 2) for i,j in pairs]
    target = [theta[i]*theta[j]/8 for i,j in pairs]
    all_rows = []
    for i in range(8):
        for j in range(i+1,8):
            r = []
            for h,k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                r.append(v)
            all_rows.append(r)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c,v in zip(r,target)) for r in rows]
    gram = [[sum(c*d/g for c,d,g in zip(r,s,metric))
             for s in rows] for r in rows]
    lam = solve(gram,rhs)
    projected = [v-sum(r[k]*b for r,b in zip(rows,lam))/metric[k]
                 for k,v in enumerate(target)]
    # Check every constraint, including those discarded as dependent.
    for r in all_rows:
        check(sum(c*v for c,v in zip(r,projected)) == 0,
              'projected matrix commutes with A')
    residual = [u-v for u,v in zip(target,projected)]
    check(sum(g*u*v for g,u,v in zip(metric,projected,residual)) == 0,
          'orthogonal target decomposition')
    return sum(g*v*v for g,v in zip(metric,projected)),len(rows)


def compute():
    global CHECKS
    CHECKS = 0
    # First ring: x=S=X+u, y=P=Xu. No square roots are used.
    S,P = x,y
    A = 2+3*S
    B = S+2*P
    delta = A*A-16*B
    c0 = S*S+2*S+2*P*S-12*P
    c1 = 8*P-3*S*S+4*S-4
    W = 2*c1*B+c0*A
    psi_n = (1024*P*P+c0*c0)*delta+W*W
    psi_d = 64*B*B*delta
    N = (468*S*S+976*S+1424-448*P)*B*B*delta-45*psi_n
    D = (S+2)*B*B*delta

    # Whole coefficient identities for g'(Y)=(Y-1)(4Y^2-A Y+B).
    gp = [-S-2*P, 2*(P+2*S+1), -3*(S+2), Poly(4)]
    factored = [-B,A+B,-A-4,Poly(4)]
    for a,b in zip(gp,factored):
        check(a == b, 'derivative of the even root polynomial')
    # Remainder of (Y-1)(Y^2-SY+P) modulo 4Y^2-A Y+B.
    reduced0 = (-A*B+4*(S+1)*B-16*P)/16
    reduced1 = (A*A-4*B-4*(S+1)*A+16*(S+P))/16
    check(reduced0 == c0/16, 'spectral residue constant remainder')
    check(reduced1 == c1/16, 'spectral residue linear remainder')
    check(c0+16*P == (S+2)*B, 'sum of spectral weights')
    check(psi_n == (1024*P*P+c0*c0)*delta+W*W,
          'squared weights denominator identity')
    mu2,mu4 = 2*(S+2),2*(S*S-2*P+2)
    check(((224*mu4+122*mu2*mu2)*psi_d-5760*psi_n)*D
          == N*(mu2*psi_d), 'displacement functional from reviewed quartic')

    # Second ring: x=X, y=u.
    NX,DX = sub(N,x+y,x*y),sub(D,x+y,x*y)
    check(sub(delta,x+y,x*y) == 9*(x-y)**2+4*(1-x)*(1-y),
          'physical nonnegative discriminant')
    HX = diff(NX,0)*DX-NX*diff(DX,0)
    G = 780*DX-NX
    low_raw = sub(G,x,x*y)
    check(min(i for i,j in low_raw.t) == 2, 'removable low-chart x^2 factor')
    low = Poly({(i-2,j):c for (i,j),c in low_raw.t.items()})
    check(low_raw == x*x*low, 'complete low-chart quotient identity')
    upper = sub(G,x,Q(1,4)+(x-Q(1,4))*y)
    cases = [
      ('low_1',low,(Q(0),Q(3,4),Q(1,2),Q(1))),
      ('low_2',low,(Q(3,8),Q(3,4),Q(1,4),Q(1,2))),
      ('low_3',low,(Q(3,8),Q(3,4),Q(0),Q(1,4))),
      ('low_4',low,(Q(0),Q(3,8),Q(0),Q(1,2))),
      ('upper',upper,(Q(3,4),Q(1),Q(0),Q(1))),
      ('increasing_X',HX,(Q(3,4),Q(1),Q(0),Q(1,4))),
    ]
    certificate = []
    inventory = {}
    for name,poly,box in cases:
        degree,bs = bernstein(poly,box)
        for c in bs.values():
            check(c >= 0, 'nonnegative Bernstein certificate '+name)
        if name == 'increasing_X':
            check(min(bs.values()) > 5000, 'strict derivative numerator margin')
        elif name != 'upper':
            check(min(bs.values()) > 0, 'strict low-chart margin')
        certificate.append({'name':name,'box':list(map(str,box)),
          'degree':list(degree),'count':len(bs),'minimum':str(min(bs.values())),
          'zero':sum(c == 0 for c in bs.values())})
        inventory[name] = [[i,j,str(c)] for (i,j),c in sorted(bs.items())]
    check(sum(v['count'] for v in certificate) == 380,
          'all Bernstein entries accounted for')
    check(Q(13,4)*Q(7,4)**2*10 == Q(3185,32) < 100,
          'physical displacement denominator bound')

    # Reproduce and credit the already published boundary curve exactly.
    nb = 2058+21912*y-15876*y*y+19224*y**3+3402*y**4
    db = (3+y)*(1+3*y)**2
    check(sub(NX,1,y)*db == nb*sub(DX,1,y), 'boundary rational identity')
    p = (26634-231084*y-907290*y*y+376920*y**3
         +971190*y**4+224532*y**5+30618*y**6)
    check(diff(nb,1)*db-nb*diff(db,1) == p, 'boundary derivative polynomial')
    check(p.value(0,Q(2,25)) > 0, 'left algebraic root bracket')
    check(p.value(0,Q(9,100)) < 0, 'right algebraic root bracket')
    prime_upper = Q(-231084)+sum(Q(k)*p.t[0,k]*Q(1,4)**(k-1)
                                  for k in range(3,7))
    check(prime_upper == Q(-24357717,256) < -90000,
          'one-sided bound for boundary derivative slope')
    check(db.value(0,Q(1,4)) == Q(637,64) < 10,
          'boundary denominator bound')
    check(nb.value(0,Q(1,9))/db.value(0,Q(1,9)) == Q(5472,7) > 780,
          'boundary test exceeds both excluded regions')
    check(Q(5472,7)-780 == Q(12,7), 'explicit global stability cutoff')

    # A failed universal spread principle, at a physical interior point.
    NP = diff(N,1)*D-N*diff(D,1)
    jp = NP.value(1,Q(15,256))/D.value(1,Q(15,256))**2
    check(jp == Q(765897880984,3166916181) > 0,
          'fixed-sum spread monotonicity obstruction')

    controls = []
    for h,k in [(Q(1),Q(1,3)),(Q(1,2),Q(1,3)),(Q(3,4),Q(1,4)),
                (Q(1,2),Q(1,2)),(Q(1),Q(0)),(Q(0),Q(0)),(Q(1),Q(1))]:
        psi,rank = pinching([Q(1),Q(1),h,k,-Q(1),-Q(1),-h,-k])
        X,u = h*h,k*k
        s,pv = X+u,X*u
        den = psi_d.value(s,pv)
        if den:
            check(psi == psi_n.value(s,pv)/den, 'definition-level spectral value')
        else:
            expected = {(Q(0),Q(0)):Q(1,8),(Q(1),Q(1)):Q(1)}
            check(psi == expected[X,u], 'exceptional collision spectral value')
        controls.append({'outer':str(h),'inner':str(k),'Psi':str(psi),'rank':rank})
    for X,u,psi,val in [(Q(0),Q(0),Q(1,8),Q(532)),
                        (Q(1),Q(1),Q(1),Q(480))]:
        m2,m4 = 4+2*(X+u),4+2*(X*X+u*u)
        check((224*m4+122*m2*m2-5760*psi)/m2 == val,
              'continuous exceptional displacement value')

    canonical = {'N':N.dump(),'D':D.dump(),'Psi_n':psi_n.dump(),
                 'Psi_d':psi_d.dump(),'HX':HX.dump(),'bernstein':inventory}
    digest = sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'schema':1,'exact_checks':CHECKS,'coefficient_sha256':digest,
            'bernstein_entries':380,'certificates':certificate,
            'matrix_controls':controls,'boundary_P_prime_upper':str(prime_upper),
            'fixed_sum_obstruction':str(jp),'exceptional_J':['532','480']}


def require_equal(actual,expected):
    if actual != expected:
        raise ValueError('expected manifest differs from exact reconstruction')


def main():
    actual = compute()
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    require_equal(actual,expected)
    mutations = []
    for key in ['schema','exact_checks','coefficient_sha256','bernstein_entries']:
        bad = deepcopy(expected)
        bad[key] = 'corrupted'
        mutations.append(bad)
    bad = deepcopy(expected)
    bad['certificates'][0]['minimum'] = '0'
    mutations.append(bad)
    bad = deepcopy(expected)
    bad['matrix_controls'][0]['Psi'] = '0'
    mutations.append(bad)
    rejected = 0
    for bad in mutations:
        try:
            require_equal(actual,bad)
        except ValueError:
            rejected += 1
    if rejected != 6:
        raise ValueError('corrupt manifest control was accepted')
    print(json.dumps({'exact_checks':actual['exact_checks'],
      'bernstein_entries':actual['bernstein_entries'],'matrix_controls':7,
      'rejected_corrupt_manifests':rejected,
      'coefficient_sha256':actual['coefficient_sha256']},sort_keys=True))


if __name__ == '__main__':
    main()
