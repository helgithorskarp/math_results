#!/usr/bin/env python3
"""Exact named-solid alignment and polar-edge audit in Q(phi)[x].

x^3=2x+phi. CAS suggested the three short polynomial expressions;
all identities below are checked by standard-library quotient arithmetic.
"""
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import hashlib
import json
from verify import Q, Z, ONE, PHI, I, qi, require, group, vertices, named_parameters


@dataclass(frozen=True)
class K:
    c: tuple = (Z, Z, Z)

    def __post_init__(self):
        require(len(self.c) == 3, 'bad cubic coefficient length')
        object.__setattr__(self, 'c', tuple(Q.coerce(x) for x in self.c))

    @staticmethod
    def coerce(v):
        return v if isinstance(v, K) else K((Q.coerce(v), Z, Z))

    def __add__(self, other):
        o = K.coerce(other)
        return K(tuple(x+y for x, y in zip(self.c, o.c)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self+-K.coerce(other)

    def __rsub__(self, other):
        return K.coerce(other)+-self

    def __mul__(self, other):
        o = K.coerce(other)
        c = [Z]*5
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                c[i+j] += a*b
        # x^4=2x^2+phi*x, x^3=2x+phi.
        c[2] += 2*c[4]
        c[1] += PHI*c[4]+2*c[3]
        c[0] += PHI*c[3]
        return K(tuple(c[:3]))

    __rmul__ = __mul__

    def inv(self):
        columns = [(self*K(tuple(ONE if i == j else Z for i in range(3)))).c
                   for j in range(3)]
        rows = [[columns[j][i] for j in range(3)]+[ONE if i == 0 else Z]
                for i in range(3)]
        for i in range(3):
            pivot = next((j for j in range(i, 3) if rows[j][i] != Z), None)
            require(pivot is not None, 'singular cubic inversion')
            rows[i], rows[pivot] = rows[pivot], rows[i]
            a = rows[i][i]
            rows[i] = [x/a for x in rows[i]]
            for j in range(3):
                if j != i:
                    a = rows[j][i]
                    rows[j] = [x-a*y for x, y in zip(rows[j], rows[i])]
        inverse = K(tuple(rows[i][3] for i in range(3)))
        require(self*inverse == K.coerce(1), 'wrong cubic inverse')
        return inverse

    def __truediv__(self, other):
        return self*K.coerce(other).inv()

    def __rtruediv__(self, other):
        return K.coerce(other)*self.inv()

    def square(self):
        return self*self

    def interval(self, x):
        return qi(self.c[0])+qi(self.c[1])*x+qi(self.c[2])*x.square()


X = K((Z, ONE, Z))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), K())


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def main():
    x, enclosed, scale = named_parameters()
    phi = K.coerce(PHI)
    q = X*(X+phi)+1
    invx = (X.square()-2)/phi
    require(X*invx == K.coerce(1), 'reciprocal root identity')
    u = phi*(3-X.square())
    r = 5-phi+2*phi*X-3*X.square()
    a = ((14*phi-27)*X.square()+(10*phi-6)*X+32-12*phi)/31
    params = (K.coerce(1), u, r, a, invx)
    for z, p in zip(params, enclosed):
        v = z.interval(x)
        require(v.lo > 0 and v.lo <= p.hi and p.lo <= v.hi,
                'positive algebraic branch mismatch')
    # Sorted normalized McCooey constants C0,...,C19 are compared by
    # EXACT squared identities, then their positive branches are audited.
    c2 = [
        (3-X.square())/q,
        phi*(X-1-invx)*invx.square()/q,
        phi*(X-1-invx)/q,
        X.square().square()*(3-X.square())/q,
        (1-X+(1+phi)*invx)/q,
        invx.square()/phi.square(),
        ((X+2)*phi+2)*invx.square()/(phi.square()*q),
        (-X.square()*(2+phi)+X*(1+3*phi)+4)/(phi.square()*q),
        (1+phi).square()*(1+invx)*invx.square()/(phi.square()*q),
        (2+3*phi-2*X+3*invx)/(phi.square()*q),
        (X.square()*(392+225*phi)+X*(249+670*phi)+470+157*phi)
            /(961*phi.square()*q),
        invx.square(),
        (X.square()+X+1+phi)*invx.square()/q,
        (X.square()+2*X*phi+2)*invx.square()/q,
        (X.square()*(1+2*phi)-phi)/(phi.square()*q),
        (X.square()+X)/q,
        phi.square().square()*invx.square().square(),
        (X.square()*(617+842*phi)+X*(919+1589*phi)+627+784*phi)
            /(961*phi.square()*q),
        phi.square()*invx.square(),
        K.coerce(1),
    ]
    formal = vertices(group())
    evaluated = [tuple(sum((K.coerce(c)*p for c, p in zip(l, params)), K())
                       for l in v) for v in formal]
    positive = set()
    for v in evaluated:
        for z in v:
            if z == K():
                continue
            b = z.interval(x)
            require(b.lo > 0 or b.hi < 0, 'coordinate sign ambiguous')
            positive.add(z if b.lo > 0 else -z)
    require(len(positive) == 20, 'coordinate constant count')
    cs = sorted(positive, key=lambda z: z.interval(x).lo)
    for i, z in enumerate(cs):
        require(z.square() == c2[i], f'C{i} squared identity fails')
        require(z.interval(x).lo > 0, 'constant positive branch')
        if i:
            require(cs[i-1].interval(x).hi < z.interval(x).lo,
                    'constant sorting intervals overlap')
    path = Path(__file__).with_name('model.json')
    literal = json.loads(path.read_text())
    require(set(literal) == {'source', 'vertices', 'faces'}, 'model fields')
    require(literal['source'] == 'https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.txt',
            'unexpected coordinate source')
    V = []
    for row in literal['vertices']:
        require(isinstance(row, list) and len(row) == 3
                and all(type(c) is int and -20 <= c <= 20 for c in row),
                'literal vertex')
        V.append(tuple(K() if c == 0 else cs[abs(c)-1]*(1 if c > 0 else -1)
                       for c in row))
    require(len(V) == len(set(V)) == 92 and set(V) == set(evaluated),
            'literal model and exact orbit differ')
    faces = literal['faces']
    require(len(faces) == 60 and len({tuple(f) for f in faces}) == 60,
            'face count')
    edges = {}
    incidence = [0]*92
    polar = []
    checks = 0
    for fno, f in enumerate(faces):
        require(isinstance(f, list) and len(set(f)) == len(f) == 5
                and all(type(i) is int and 0 <= i < 92 for i in f), 'pentagon grammar')
        normal = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]]))
        height = dot(normal, V[f[0]])
        require(height != K(), 'degenerate face')
        normal = tuple(z/height for z in normal)
        orientation = None
        for pos, first in enumerate(f):
            second = f[(pos+1) % 5]
            for third in f:
                if third in (first, second):
                    continue
                turn = dot(normal, cross(sub(V[second], V[first]),
                                         sub(V[third], V[first]))).interval(x)
                require(turn.lo > 0 or turn.hi < 0, 'degenerate face edge')
                sign = 1 if turn.lo > 0 else -1
                if orientation is None:
                    orientation = sign
                require(sign == orientation, 'face cycle is not strictly convex')
        for j, v in enumerate(V):
            delta = 1-dot(normal, v)
            if j in f:
                require(delta == K(), 'exact face coplanarity')
            else:
                require(delta.interval(x).lo > 0, 'facet support inequality')
            checks += 1
        polar.append(normal)
        for i, j in zip(f, f[1:]+f[:1]):
            incidence[i] += 1
            edge = tuple(sorted((i, j)))
            edges.setdefault(edge, []).append(fno)
    require(len(edges) == 150 and all(len(f) == 2 for f in edges.values()),
            'closed edge incidence')
    require(incidence.count(3) == 80 and incidence.count(5) == 12,
            'original vertex valencies')
    # Every dual vertex lies in one proper icosahedral orbit. Verify the
    # defining regular-face metric directly on all 150 dual edges.
    norms = {dot(v, v) for v in polar}
    require(len(norms) == 1, 'dual vertices are not cospherical')
    lengths = set()
    for fs in edges.values():
        d = sub(polar[fs[0]], polar[fs[1]])
        lengths.add(dot(d, d))
    require(len(lengths) == 1, 'dual edge lengths differ')
    edge2 = next(iter(lengths))
    require(edge2.interval(x).lo > 0, 'zero dual edge')
    # All body vertices occur on support facets; the supplied closed
    # convex boundary has V-E+F=2 and connected facet adjacency.
    reachable, todo = {0}, [0]
    while todo:
        f = todo.pop()
        for fs in edges.values():
            if f in fs:
                g = fs[0] if fs[1] == f else fs[1]
                if g not in reachable:
                    reachable.add(g)
                    todo.append(g)
    require(len(reachable) == 60 and 92-150+60 == 2, 'boundary topology')
    output = {
        'agent': 'six-rupert-1', 'role': 'researcher',
        'coefficient_domain': 'Q(phi)[x]/(phi^2-phi-1, x^3-2*x-phi)',
        'positive_radical_identities': 20, 'literal_vertices_matched': 92,
        'exact_support_facets': 60, 'support_comparisons': checks,
        'convex_face_edge_tests': 900,
        'original_edges': 150, 'dual_equal_edge_checks': 150,
        'dual_regular_triangles': 80, 'dual_regular_pentagons': 12,
        'model_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'floating_point_proof_decisions': 0,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
