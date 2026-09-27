#!/usr/bin/env python3
"""Exact convex-normal identities and rational projection examples.

Python >=3.10, standard library. Does not import the earlier radial checker.
Finite controls support, but do not replace, the proof in CONVEX_CORES.md.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Poly:
    """Q[r,s,R,S,c,alpha,beta,d,t], used for universal identities."""
    zero = (0,)*9

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.a = value.a.copy()
        elif isinstance(value, dict):
            self.a = {k: Q(v) for k, v in value.items() if v}
        else:
            self.a = {self.zero: Q(value)} if value else {}

    def __add__(self, other):
        a = self.a.copy()
        for k, v in Poly(other).a.items():
            a[k] = a.get(k, Q(0))+v
        return Poly(a)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.a.items()})

    def __sub__(self, other):
        return self+-Poly(other)

    def __rsub__(self, other):
        return Poly(other)+-self

    def __mul__(self, other):
        a = {}
        for k, v in self.a.items():
            for l, w in Poly(other).a.items():
                m = tuple(i+j for i, j in zip(k, l))
                a[m] = a.get(m, Q(0))+v*w
        return Poly(a)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "invalid exponent")
        a = Poly(1)
        for _ in range(n):
            a = a*self
        return a

    def dt(self):
        return Poly({k[:-1]+(k[-1]-1,): v*k[-1]
                     for k, v in self.a.items() if k[-1]})


def same(a, b):
    require(not (a-b).a, "polynomial mismatch")


def rejected(call):
    try:
        call()
    except ValueError:
        return 1
    raise ValueError("deliberately damaged input was accepted")


def symbolic():
    r,s,R,S,c,alpha,beta,d,t = [
        Poly({tuple(int(i == j) for j in range(9)): 1}) for i in range(9)]
    A,B = (1-t)*r+t*R, (1-t)*s+t*S
    direct = d+2*A*alpha+2*B*beta+A*A+B*B-2*c*A*B
    direct += t*(1-t)*((r-R)-(s-S))**2
    split = d+2*A*alpha+2*B*beta+(1-t)*(r-s)**2+t*(R-S)**2+2*A*B*(1-c)
    derivative = -2*(r-R)*alpha-2*(s-S)*beta+(R-S)**2-(r-s)**2
    derivative -= 2*(1-c)*((r-R)*B+(s-S)*A)
    same(direct, split)
    same(direct.dt(), derivative)
    return 2, rejected(lambda: same(direct, split+2*t*(r-R)*alpha))


def vec(*a):
    return tuple(Q(x) for x in a)


ZERO = vec(0,0,0)


def add(a, b):
    return tuple(x+y for x,y in zip(a,b))


def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))


def scale(q, a):
    return tuple(q*x for x in a)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def square(a):
    return dot(a,a)


def exact_sqrt(x):
    require(x >= 0, "negative norm square")
    a,b = isqrt(x.numerator), isqrt(x.denominator)
    require(a*a == x.numerator and b*b == x.denominator, "nonrational fixture norm")
    return Q(a,b)


def descriptor(x, project):
    p = project(x)
    r = exact_sqrt(square(sub(x,p)))
    u = scale(1/r,sub(x,p)) if r else ZERO
    return x,p,r,u


def normal_data(a, b):
    _,p,r,u = a
    _,q,s,v = b
    alpha,beta,c = dot(sub(p,q),u), -dot(sub(p,q),v), dot(u,v)
    require(alpha >= 0 and beta >= 0 and -1 <= c <= 1, "invalid convex-normal signs")
    return alpha,beta,c


def clip(x):
    return min(Q(1),max(Q(-1),x))


def make_cases():
    radii = [Q(0),Q(1,2),Q(1),Q(3,2),Q(2),Q(3)]
    cube_rays = [(vec(1,0,0),vec(1,0,0)),(vec(-1,0,0),vec(-1,0,0)),
        (vec(0,1,0),vec(0,1,0)),(vec(0,0,-1),vec(0,0,-1)),
        (vec(1,1,0),vec(Q(3,5),Q(4,5),0)),
        (vec(1,1,1),vec(Q(1,3),Q(2,3),Q(2,3))),
        (vec(-1,1,-1),vec(Q(-2,3),Q(2,3),Q(-1,3))),
        (vec(0,-1,1),vec(0,Q(-3,5),Q(4,5)))]
    segment_rays = [(ZERO,vec(0,Q(3,5),Q(4,5))),
        (vec(Q(1,2),0,0),vec(0,1,0)),(vec(Q(-1,2),0,0),vec(0,0,-1)),
        (vec(1,0,0),vec(Q(3,5),Q(4,5),0)),
        (vec(-1,0,0),vec(Q(-2,3),Q(2,3),Q(1,3)))]
    specs = [
        ('cube',lambda x: tuple(clip(v) for v in x),cube_rays,[ZERO,vec(Q(1,2),Q(1,4),Q(-1,4))]),
        ('segment',lambda x: vec(clip(x[0]),0,0),segment_rays,[ZERO]),
        ('singleton',lambda x: ZERO,[(ZERO,u) for _,u in cube_rays],[ZERO]),
        ('halfspace',lambda x: vec(x[0],x[1],min(Q(0),x[2])),
            [(p,vec(0,0,1)) for p in (ZERO,vec(1,0,0),vec(0,1,0))],[vec(0,0,-1)]),
        ('whole_space',lambda x: x,[],[ZERO,vec(1,0,0),vec(0,1,0),vec(0,0,1)])]
    out = []
    for name,project,rays,core in specs:
        points = set(core)
        for p,u in rays:
            require(square(u) == 1 and project(p) == p, "bad ray fixture")
            for r in radii:
                x = add(p,scale(r,u))
                require(project(x) == p, "ray does not project to its base")
                points.add(x)
        out.append((name,project,[descriptor(x,project) for x in sorted(points)]))
    return out


def mirror(r):
    return r if r <= 1 else max(Q(0),2-r)


def inversion(r):
    return r if r <= 1 else 1/r


def repeated(r):
    z = r % 2
    return min(z,2-z)


def endpoint(a, rho):
    _,p,r,u = a
    return add(p,scale(rho(r),u))


def geometry_checks():
    times = [(Q(0),Q(0)),(Q(9,25),Q(12,25)),(Q(1,2),Q(1,2)),
             (Q(16,25),Q(12,25)),(Q(1),Q(0))]
    profiles = [lambda r: r,lambda r: Q(0),mirror,inversion,repeated]
    records = []
    for name,project,points in make_cases():
        pairs = list(combinations(points,2))
        coordinate_checks = 0
        collar_checks = 0
        for a in points:
            x,p,r,u = a
            target = endpoint(a,mirror)
            require(project(target) == p, "normal fibre not preserved")
            if r <= 2:
                pk = x if r <= 1 else add(p,u)
                require(target == sub(scale(2,pk),x), "collar reflection formula failed")
                collar_checks += 1
            else:
                require(target == p, "outer projection branch failed")
        for a,b in pairs:
            x,p,r,u = a; y,q,s,v = b
            alpha,beta,c = normal_data(a,b)
            for rho in profiles:
                R,S = rho(r),rho(s)
                require(0 <= R <= r and 0 <= S <= s and abs(R-S) <= abs(r-s), "bad scalar profile")
                last = None
                for t,h in times:
                    require(h*h == t*(1-t), "bad rational time")
                    A,B = (1-t)*r+t*R,(1-t)*s+t*S
                    fx = add(p,scale(A,u))+(h*(r-R),)
                    fy = add(q,scale(B,v))+(h*(s-S),)
                    direct = square(sub(fx,fy))
                    split = square(sub(p,q))+2*A*alpha+2*B*beta
                    split += (1-t)*(r-s)**2+t*(R-S)**2+2*A*B*(1-c)
                    derivative = -2*(r-R)*alpha-2*(s-S)*beta+(R-S)**2-(r-s)**2
                    derivative -= 2*(1-c)*((r-R)*B+(s-S)*A)
                    require(direct == split and derivative <= 0, "lift identity or sign failed")
                    require(last is None or direct <= last, "time monotonicity failed")
                    last = direct
                    coordinate_checks += 1
        records.append({'core':name,'sites':len(points),'pairs':len(pairs),
                        'lift_coordinate_checks':coordinate_checks,'collar_checks':collar_checks})
    # Invalid normal signs are rejected even under optimized Python.
    invalid_a = (vec(1,0,0),ZERO,Q(1),vec(1,0,0))
    invalid_b = (vec(1,0,0),vec(1,0,0),Q(0),ZERO)
    failures = rejected(lambda: normal_data(invalid_a,invalid_b))
    failures += rejected(lambda: normal_data(invalid_b,invalid_a))
    failures += rejected(lambda: exact_sqrt(Q(2)))
    return records,failures


def main():
    identities,failures = symbolic()
    cases,more = geometry_checks()
    print(json.dumps({'status':'CONVEX_CORE_PASS','polynomial_identities':identities,
                      'cases':cases,'intentional_rejections':failures+more},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
