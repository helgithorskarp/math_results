"""Literal coefficient geometry transcribed from the written LEMMA9912 proof.

The independent implementation uses a two-component radical module and
an expression DAG, rather than the author's sparse three-variable ring.
"""
from digit import T, Z, expr

LABELS = (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12)
CONTACTS = ((0, 5), (0, 6), (0, 7), (0, 11), (1, 2), (1, 4),
            (1, 10), (1, 12), (2, 4), (2, 8), (2, 10), (4, 8),
            (5, 7), (5, 9), (5, 11), (6, 11), (7, 12), (9, 10),
            (9, 11), (10, 12))


class Radical:
    def __init__(self, constant, linear, relation):
        self.p, self.q = expr(constant), expr(linear)
        self.relation = relation

    def coerce(self, other):
        if isinstance(other, Radical):
            if other.relation is not self.relation:
                raise ValueError('different radical relations')
            return other
        return Radical(other, 0, self.relation)

    def __add__(self, other):
        other = self.coerce(other)
        return Radical(self.p + other.p, self.q + other.q, self.relation)

    __radd__ = __add__

    def __neg__(self):
        return Radical(-self.p, -self.q, self.relation)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        return Radical(self.p * other.p + self.q * other.q * self.relation,
                       self.p * other.q + self.q * other.p, self.relation)

    __rmul__ = __mul__


def cross(u, v):
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2],
            u[0]*v[1]-u[1]*v[0]]


def dot(u, v):
    return sum(x*y for x,y in zip(u,v))*(1-T) + sum(u)*sum(v)*T


def model():
    t, z = T, Z
    a, b, c = 1+t, 1-t, 1+2*t
    D = b*b*c
    C = 1+D*z*z
    K = t*(9*t*t-2*t-3)
    J = a*a+K
    h = 9*t*t-1
    S = D*(t*z*z-2*z)+t*(2*t-1)
    E = C*C-S*S
    G = a**4*((1-t*t)*C*C-S*S)-K*K*C*C+2*S*K*t*a*a*C
    R = D*G
    def lift(x, y=0):
        return Radical(x, y, R)
    def L(v):
        total = sum(v)
        return [x*c-total*t for x in v]
    def scale(k, v):
        return [x*k for x in v]
    def add(*vs):
        return [sum(v[j] for v in vs) for j in range(3)]
    e0 = [lift(1),lift(0),lift(0)]
    N = {1:scale(a*a,e0), 2:[lift(0),lift(a*a),lift(0)],
         4:[lift(0),lift(0),lift(a*a)],
         8:[lift(-a*a),lift(2*t*a),lift(2*t*a)],
         10:[lift(2*t*a),lift(2*t*a),lift(-a*a)],
         12:[lift(2*t*(1+3*t)),lift(3*t*t-2*t-1),lift(-2*t*a)]}
    Wn = add(scale((D*z*z-1)*a*a,e0),scale(2*t,N[12]),
             scale(2*b*z,L(cross(N[12],e0))))
    Wd = a*a*C
    Vd = b*c*a**6*E
    Vn = add(scale(b*c*a*a,add(scale(K*C-S*t*a*a,Wn),
             scale(C*(t*a*a*C-S*K),N[10]))),
             scale(lift(0,-1),L(cross(Wn,N[10]))))
    Un = add(scale(K,add(scale(Vd,Wn),scale(Wd,Vn))),
             scale(-a*(3*t-1),L(cross(Wn,Vn))))
    Wl, Vl = scale(J*Vd,Wn), scale(J*Wd,Vn)
    Omega = h*J*Wd*Vd
    Y = {i:scale(h*J*C*Vd,N[i]) for i in N}
    Y.update({6:scale(h,Un),7:scale(h,Wl),9:scale(h,Vl),
              0:scale(a,add(scale(2*t,Un),scale(2*t,Wl),scale(b,Vl))),
              5:scale(a,add(scale(b,Un),scale(2*t,Wl),scale(2*t,Vl))),
              11:scale(a,add(scale(2*t,Un),scale(b,Wl),scale(2*t,Vl)))})
    return {'a':a,'b':b,'c':c,'D':D,'C':C,'K':K,'J':J,'h':h,
            'S':S,'E':E,'G':G,'R':R,'Omega':Omega,'N':N,'Y':Y}
