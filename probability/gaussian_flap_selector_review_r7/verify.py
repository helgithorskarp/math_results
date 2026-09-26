#!/usr/bin/env python3
"""Independent R7 audit of the R4 selector motion, without author code/data.

Exact rational coordinates and the quotient ring
Q[u,v]/(u^2-U2,v^2-V2). The positive square roots are interpreted in
REVIEW.md. Universal signs use a factored polynomial certificate, not
finite time samples. Standard-library Python 3.11/3.12 only.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)


# A small polynomial ring Q[Q,A,B], independent of the motion fixture ring.
def add(*ps):
    out = {}
    for p in ps:
        for exponent, value in p.items():
            out[exponent] = out.get(exponent, F(0)) + value
    return {e: c for e, c in out.items() if c}


def scale(p, c):
    return {e: F(c) * a for e, a in p.items() if c * a}


def mul(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            g = tuple(x + y for x, y in zip(e, f))
            out[g] = out.get(g, F(0)) + a * b
    return {e: c for e, c in out.items() if c}


def power(p, n):
    out = {(0, 0, 0): F(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def diff(p, i):
    out = {}
    for e, c in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            out[tuple(f)] = c * e[i]
    return out


class E:
    """Four coefficients in 1,u,v,u*v over exact rational numbers."""
    def __init__(self, values, r2, e2):
        self.c = tuple(map(F, values))
        require(len(self.c) == 4, "algebraic coefficient count")
        self.r2, self.e2 = F(r2), F(e2)

    def cast(self, x):
        if isinstance(x, E):
            require((self.r2, self.e2) == (x.r2, x.e2), "mixed fixture rings")
            return x
        return E((x, 0, 0, 0), self.r2, self.e2)

    def __add__(self, other):
        other = self.cast(other)
        return E([x + y for x, y in zip(self.c, other.c)], self.r2, self.e2)

    __radd__ = __add__

    def __neg__(self):
        return E([-x for x in self.c], self.r2, self.e2)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        other = self.cast(other)
        c = [F(0)] * 4
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                factor = (self.r2 if i & j & 1 else 1)
                factor *= (self.e2 if i & j & 2 else 1)
                c[i ^ j] += x * y * factor
        return E(c, self.r2, self.e2)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / F(scalar))

    def __eq__(self, other):
        return self.c == self.cast(other).c


def polynomial_audit():
    one = {(0, 0, 0): F(1)}
    t, q, e = ({(1, 0, 0): F(1)}, {(0, 1, 0): F(1)},
               {(0, 0, 1): F(1)})
    den = add(one, mul(q, t))
    # F' + 2e, using sqrt(1-q^2)=e(1+q), with the denominator cleared.
    left = mul(e, add(scale(power(den, 2), 2), scale(mul(add(one, q),
        add(mul(q, power(t, 2)), scale(t, 2), q)), -1)))
    right = mul(mul(mul(e, add(one, scale(q, -1))), add(one, scale(t, -1))),
                add(scale(one, 2), mul(q, add(one, t))))
    require(left == right, "factored exceptional derivative certificate")
    # Interpret t,q,e now as A,B,epsilon; h_k=B(A+B).
    margin = add(mul(q, add(t, q)), scale(mul(mul(t, q),
                 power(add(one, scale(e, -1)), 2)), -1))
    positive = add(power(q, 2), mul(mul(mul(t, q), e), add(scale(one, 2), scale(e, -1))))
    require(margin == positive, "strict reserve identity")
    # Delta identity after c=AB-L; variables now stand for Q,AB,L.
    delta_left = add(mul(t, e), mul(add(q, scale(e, -1)), add(t, q)))
    delta_right = mul(q, add(t, q, scale(e, -1)))
    require(delta_left == delta_right, "exceptional Gram amplitude identity")
    # Norm and constant Gram identities for one shifted normal.
    norm_left = add(power(add(t, q), 2),
                    mul(add(one, scale(power(q, 2), -1)),
                        add(one, scale(power(t, 2), -1))))
    require(norm_left == power(add(one, mul(t, q)), 2), "shifted norm identity")
    require(add(mul(t, add(t, q)), one, scale(power(t, 2), -1))
            == add(one, mul(t, q)), "shifted cross identity")
    return 5


EDGES = list(combinations(range(4), 2))


def arcs(mask):
    return [(a, b) if (mask >> j) & 1 else (b, a)
            for j, (a, b) in enumerate(EDGES)]


def incidence_audit():
    counts = Counter()
    selections = 0
    pair_checks = 0
    exceptional = 0
    for mask in range(64):
        es = arcs(mask)
        degrees = [sum(a == i for a, b in es) for i in range(4)]
        kind = "sink" if 0 in degrees else "source_cycle" if 3 in degrees else "strong"
        counts[kind] += 1
        if kind == "sink":
            continue
        require(1 in degrees, "a sinkless tournament needs an outdegree-one tail")
        for i in range(4):
            if degrees[i] != 1:
                continue
            k = next(b for a, b in es if a == i)
            selections += 1
            for (a, b), (r, s) in combinations(es, 2):
                pair_checks += 1
                if {a, r} == {i, k}:
                    slack = Counter()
                    if s == a:
                        slack[a] += 1
                    if b == r:
                        slack[r] += 1
                    require(slack == {k: 1}, "exceptional pair has wrong reserve")
                    exceptional += 1
    require(dict(counts) == {"sink": 32, "source_cycle": 8, "strong": 24},
            "tournament coverage")
    return {"tournaments": dict(sorted(counts.items())),
            "outdegree_one_choices": selections, "flap_pair_checks": pair_checks,
            "exceptional_pair_checks": exceptional}


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def triangular(a, b, d):
    z = -1/a
    x = -(1+1/(a*a))/b
    y = -(1+1/(a*a)+x*x)/d
    return [[F(0), F(0), a], [b, F(0), z], [x, d, z], [x, y, z]]


FIXTURES = {
    "regular": [[F(x) for x in row] for row in
                [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]],
    "asymmetric_beta_center": triangular(F(1), F(2), F(3)),
    "strongly_asymmetric": triangular(F(1,3), F(4), F(2,5)),
}


def direct_motion_audit(vertices, mask, i):
    es = arcs(mask)
    require(sum(a == i for a, b in es) == 1, "invalid selected tail")
    k = next(b for a, b in es if a == i)
    r, l = [j for j in range(4) if j not in (i, k)]
    vi, vk, vr, vl = [vertices[j] for j in (i,k,r,l)]
    dr, dl, cross = dot(vr,vr), dot(vl,vl), dot(vr,vl)
    determinant = dr*dl-cross*cross
    require(determinant > 0, "projection plane rank")
    rhsr, rhsl = dot(vi,vr), dot(vi,vl)
    coefr = (dl*rhsr-cross*rhsl)/determinant
    coefl = (dr*rhsl-cross*rhsr)/determinant
    p = [coefr*x+coefl*y for x,y in zip(vr,vl)]
    ni, nk = sub(vi,p), sub(vk,p)
    require(all(dot(n,v)==0 for n in (ni,nk) for v in (vr,vl)),
            "both normals have the computed projection")
    L, A2, B2 = dot(p,p), dot(ni,ni), dot(nk,nk)
    AB = -dot(ni,nk)
    require(L>0 and A2>0 and B2>0 and AB>0, "projection positivity")
    require(A2*B2 == AB*AB and AB == L+1, "opposite normal components")
    lengths = [dot(v,v) for v in vertices]
    require(lengths[i]+1 == A2+AB and lengths[k]+1 == B2+AB,
            "the two contraction reserves")
    U2, V2 = A2/lengths[i], B2/lengths[k]
    require(0<U2<1 and 0<V2<1, "shift domains")
    zero = E((0,0,0,0),U2,V2)
    u, v = E((0,1,0,0),U2,V2), E((0,0,1,0),U2,V2)
    theta = [zero]*4
    theta[i], theta[k] = u, -v
    theta2 = [F(0)]*4
    theta2[i], theta2[k] = U2,V2
    base = [list(w) for w in vertices]
    base[i],base[k] = p,p
    amplitude = L+1+u*v
    labels = [(None,j) for j in range(4)]+es
    times = [F(-1),F(-2,3),F(0),F(3,5),F(1)]
    gram_checks=derivative_checks=endpoint_checks=0
    for t in times:
        inv = [(1-theta[j]*t)/(1-theta2[j]*t*t) for j in range(4)]
        lam = [(t+theta[j])*inv[j] for j in range(4)]
        prime = [(1-theta2[j])*inv[j]*inv[j] for j in range(4)]
        aux = [[w*inv[j] for w in base[j]] for j in range(4)]
        auxp = [[-w*theta[j]*inv[j]*inv[j] for w in base[j]] for j in range(4)]
        for a in range(4):
            require(dot(aux[a],ni)==0, "auxiliary rank exceeds two")
            for b in range(a,4):
                direct = lam[a]*lam[b]*dot(vertices[a],vertices[b])
                direct += (1-t*t)*dot(aux[a],aux[b])
                want = zero+dot(vertices[a],vertices[b])
                if {a,b}=={i,k}:
                    want += (1-t*t)*inv[i]*inv[k]*amplitude
                require(direct==want,"direct coordinate Gram identity")
                gram_checks+=1
        states=[]
        for a,b in labels:
            original=[zero+x for x in vertices[b]]
            op=[zero]*3
            residual=[zero]*3
            rp=[zero]*3
            if a is not None:
                original=[x+lam[a]*y for x,y in zip(original,vertices[a])]
                op=[prime[a]*y for y in vertices[a]]
                residual,rp=aux[a],auxp[a]
            states.append((original,op,residual,rp))
            if abs(t)==1:
                endpoint=[x+(t*y if a is not None else 0)
                          for x,y in zip(vertices[b], vertices[a] if a is not None else [0]*3)]
                require(original==endpoint,"endpoint coordinates")
                require((1-t*t)*dot(residual,residual)==0,"endpoint residual")
                endpoint_checks+=1
        fprime=-2*t*inv[i]*inv[k]-(1-t*t)*(theta[i]*inv[i]*inv[i]*inv[k]
                                         +theta[k]*inv[i]*inv[k]*inv[k])
        dg=fprime*amplitude
        if t==0:
            common_head_original=[lam[i]*x-lam[k]*y for x,y in zip(vi,vk)]
            common_head_residual=sub(aux[i],aux[k])
            midpoint=dot(common_head_original,common_head_original)+dot(common_head_residual,common_head_residual)
            endpoint=dot(sub(vi,vk),sub(vi,vk))
            require(midpoint==endpoint-2*amplitude,"full-family tight pair has an interior dip")
        for x,y in combinations(range(10),2):
            z,zp,w,wp=[sub(states[x][j],states[y][j]) for j in range(4)]
            direct=2*dot(z,zp)-2*t*dot(w,w)+2*(1-t*t)*dot(w,wp)
            a,b=labels[x]
            e,f=labels[y]
            want=zero
            if a is None and e is not None:
                want=-2*(lengths[e]+1)*prime[e]*int(b==e)
            elif e is None and a is not None:
                want=-2*(lengths[a]+1)*prime[a]*int(f==a)
            elif a is not None and e is not None:
                want=-2*((dg if {a,e}=={i,k} else zero)
                          +(lengths[a]+1)*prime[a]*int(f==a)
                          +(lengths[e]+1)*prime[e]*int(b==e))
            require(direct==want,"direct pair-distance derivative")
            derivative_checks+=1
    # Adding the omitted common-head pair cannot use the same motion:
    # its squared distance at the midpoint is endpoint distance -2*amplitude.
    require(amplitude.c[0]>0 and amplitude.c[3]>0 and amplitude.c[1]==amplitude.c[2]==0,
            "strict positive hump on a full-family tight pair")
    return {"mask":mask,"tail":i,"head":k,"projection_length_squared":str(L),
            "normal_A_squared":str(A2),"normal_B_squared":str(B2),"normal_AB":str(AB),
            "gram_identities":gram_checks,"pair_derivative_identities":derivative_checks,
            "endpoint_checks":endpoint_checks,"full_family_motion_rejected":True}


def coordinate_audit():
    records={}
    for name,vertices in FIXTURES.items():
        require(all(dot(vertices[a],vertices[b])==-1 for a,b in combinations(range(4),2)),
                "orthocentric fixture")
        records[name]=[direct_motion_audit(vertices,2,0),
                       direct_motion_audit(vertices,4,0),
                       direct_motion_audit(vertices,4,1)]
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result={"polynomial_identities":polynomial_audit(),"incidences":incidence_audit(),
            "coordinate_checks":coordinate_audit()}
    expected=Path(__file__).with_name('EXPECTED.json')
    if args.write:
        expected.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        require(json.loads(expected.read_text())==result,"expected record mismatch")
    allrows=[x for rows in result['coordinate_checks'].values() for x in rows]
    print(json.dumps({"status":"R7_SELECTOR_MOTION_REVIEW_EXACT_CHECKS_PASS",
                      "polynomial_identities":result['polynomial_identities'],
                      "incidences":result['incidences'],
                      "pair_derivative_identities":sum(x['pair_derivative_identities'] for x in allrows),
                      "full_family_motion_rejections":len(allrows)},sort_keys=True))


if __name__=='__main__':
    main()
