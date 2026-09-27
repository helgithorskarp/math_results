#!/usr/bin/env python3
"""Exact author controls for NORMAL_BUNDLES.md; CPython 3.11.2 standard library.

Quadratic surds are compared by rational squaring, never floating point.
No finite control replaces the universal written argument. The original
angular proof/checker/output are content-pinned and are not imported.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sign(x):
    return (x > 0) - (x < 0)


def surd_sign(a, b, d):
    """Sign of a+b*sqrt(d), with all arguments rational and d>=0."""
    a, b, d = Q(a), Q(b), Q(d)
    need(d >= 0, "negative surd radicand")
    if not b or not d:
        return sign(a)
    if not a:
        return sign(b)
    if sign(a) == sign(b):
        return sign(a)
    return sign(a) * sign(a*a-b*b*d)


def surd_leq(x, y, d):
    return surd_sign(x[0]-y[0], x[1]-y[1], d) <= 0


def vec(values):
    return tuple(Q(v) for v in values)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def scale(a, x):
    return tuple(a*b for b in x)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def dist2(x, y):
    z = add(x, scale(-1, y))
    return dot(z, z)


def poly_add(*polys):
    out = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, 0) + coefficient
    return {m: c for m, c in out.items() if c}


def poly_mul(x, y):
    out = {}
    for m, c in x.items():
        for n, e in y.items():
            k = tuple(sorted(m+n))
            out[k] = out.get(k, 0) + c*e
    return {m: c for m, c in out.items() if c}


def poly_scale(c, p):
    return {m: c*x for m, x in p.items() if c*x}


def normal_identity():
    var = lambda name: {(name,): Q(1)}
    d = [var('d'+str(i)) for i in range(3)]
    u = [var('u'+str(i)) for i in range(3)]
    v = [var('v'+str(i)) for i in range(3)]
    a, b, h, j = [var(name) for name in ['A', 'B', 'H', 'J']]
    square = lambda p: poly_mul(p, p)
    z = [poly_add(poly_mul(a, ui), poly_scale(-1, poly_mul(b, vi))) for ui, vi in zip(u, v)]
    actual = poly_add(*[square(poly_add(di, zi)) for di, zi in zip(d, z)],
                      square(poly_add(h, poly_scale(-1, j))))
    cross = poly_add(*[poly_scale(2, poly_mul(di, zi)) for di, zi in zip(d, z)])
    expected = poly_add(*[square(di) for di in d], cross,
                        *[square(zi) for zi in z], square(poly_add(h, poly_scale(-1, j))))
    need(not poly_add(actual, poly_scale(-1, expected)), "normal-bundle expansion")
    wrong = poly_add(expected, poly_scale(-2, cross))
    need(bool(poly_add(actual, poly_scale(-1, wrong))), "reversed projection terms accepted")
    return "PASS (generic expansion; reversed cross terms rejected)"


def in_core(core, p):
    if core == 'cube':
        return max(abs(x) for x in p) <= 1
    if core == 'ball':
        return dot(p, p) <= 1
    if core == 'halfspace':
        return p[0] <= 0
    if core == 'line':
        return p[1:] == (0, 0)
    if core == 'segment':
        return p[1:] == (0, 0) and abs(p[0]) <= 1
    if core == 'point':
        return p == (0, 0, 0)
    if core == 'whole_space':
        return True
    raise RuntimeError('unknown core')


def valid_normal(core, p, u, r):
    if not in_core(core, p) or r < 0:
        return False
    if not r:
        return u == (0, 0, 0)
    if dot(u, u) != 1:
        return False
    if core == 'cube':
        return all(not ui or pi == sign(ui) for pi, ui in zip(p, u))
    if core == 'ball':
        return p == u
    if core == 'halfspace':
        return p[0] == 0 and u == (1, 0, 0)
    if core == 'line':
        return u[0] == 0
    if core == 'segment':
        return not u[0] or p[0] == sign(u[0])
    if core == 'point':
        return True
    return False


def fixtures():
    e1, e2 = vec([1, 0, 0]), vec([0, 1, 0])
    u = vec([Q(1, 3), Q(2, 3), Q(2, 3)])
    v = vec([Q(2, 3), Q(1, 3), Q(2, 3)])
    w = vec([Q(-2, 3), Q(2, 3), Q(-1, 3)])
    edge = vec([Q(3, 5), Q(4, 5), 0])
    zero = vec([0, 0, 0])
    inside = (zero, zero, Q(0))
    row = lambda p, n, r: (vec(p), n, Q(r))
    return {
        'cube': [inside, row([1,1,1],u,1), row([1,1,1],v,2), row([-1,1,-1],w,Q(3,2)),
                 row([1,0,0],e1,3), row([0,1,0],e2,1), row([1,1,0],edge,2),
                 row([-1,-1,-1],scale(-1,u),1), row([1,1,1],u,4)],
        'ball': [inside]+[(n,n,Q(i+1,2)) for i,n in enumerate([u,v,w,e1,e2,edge,scale(-1,u)])],
        'halfspace': [inside, row([0,2,3],e1,2), row([0,-1,1],e1,3),
                      row([-1,2,0],zero,0)],
        'line': [inside, row([2,0,0],e2,1), row([-1,0,0],vec([0,Q(3,5),Q(4,5)]),2),
                 row([3,0,0],scale(-1,e2),3)],
        'segment': [inside, row([1,0,0],u,1), row([1,0,0],v,2), row([-1,0,0],w,3),
                    row([0,0,0],e2,4), row([-1,0,0],scale(-1,u),1)],
        'point': [inside]+[(zero,n,Q(i+1,2)) for i,n in enumerate([u,v,w,e1,e2,edge,scale(-1,u)])],
        'whole_space': [inside, row([1,2,3],zero,0), row([-1,0,3],zero,0)],
    }


ANGLES = [(Q(1),Q(0)), (Q(12,13),Q(5,13)), (Q(4,5),Q(3,5)),
          (Q(3,5),Q(4,5)), (Q(5,13),Q(12,13)), (Q(0),Q(1))]


def lifted_pair(x, y, a, b, cosine, sine):
    p, u, r = x
    q, v, s = y
    A, B = (a+cosine)/(1+a*cosine), (b+cosine)/(1+b*cosine)
    h, j = r*sine/(1+a*cosine), s*sine/(1+b*cosine)
    horizontal = dist2(add(p,scale(r*A,u)), add(q,scale(s*B,v)))
    return horizontal+h*h*(1-a*a)+j*j*(1-b*b), -2*h*j


def audit_motions():
    counts = {}
    profiles = {'angular': lambda u: abs(u[0]*u[1]*u[2]),
                'zero': lambda u: Q(0), 'identity': lambda u: Q(1)}
    for core, rows in fixtures().items():
        for p,u,r in rows:
            need(valid_normal(core,p,u,r), 'invalid normal fixture: '+core)
        core_count = 0
        for profile, function in profiles.items():
            factors = [function(row[1]) for row in rows]
            for i,j in combinations(range(len(rows)),2):
                x,y = rows[i],rows[j]
                p,u,r = x
                q,v,s = y
                a,b = factors[i],factors[j]
                delta = add(p,scale(-1,q))
                need(dot(delta,u) >= 0 and dot(delta,v) <= 0, 'projection sign')
                c = dot(u,v)
                radicand = (1-a*a)*(1-b*b)
                if r and s:
                    need(c <= 0 or c*c*(1-a*b)**2 <= radicand, 'angular hypothesis')
                values = [lifted_pair(x,y,a,b,ct,st) for ct,st in ANGLES]
                for ct,st in ANGLES:
                    need(ct*ct+st*st == 1,'angle normalization')
                for previous,following in zip(values,values[1:]):
                    need(surd_leq(following,previous,radicand),'lift distance increased')
                source = dist2(add(p,scale(r,u)),add(q,scale(s,v)))
                target = dist2(add(p,scale(r*a,u)),add(q,scale(s*b,v)))
                need(surd_sign(values[0][0]-source,values[0][1],radicand)==0,'start point')
                lowered = [(target+(1-t)**2*(r*r*(1-a*a)+s*s*(1-b*b)),
                            -2*(1-t)**2*r*s) for t in [Q(0),Q(1,2),Q(1)]]
                need(surd_sign(values[-1][0]-lowered[0][0],
                               values[-1][1]-lowered[0][1],radicand)==0,'stage join')
                for previous,following in zip(lowered,lowered[1:]):
                    need(surd_leq(following,previous,radicand),'lowering increased distance')
                need(lowered[-1] == (target,0),'target endpoint')
                need(target <= source,'endpoint contraction')
                core_count += 1
        counts[core] = {'labels':len(rows),'profiles':len(profiles),'pair_controls':core_count}
    return counts


def rejected_controls():
    need(not valid_normal('cube',vec([1,0,0]),vec([-1,0,0]),Q(1)), 'inward cube normal accepted')
    need(not valid_normal('ball',vec([1,0,0]),vec([0,1,0]),Q(1)), 'tangential ball normal accepted')
    need(not valid_normal('halfspace',vec([1,0,0]),vec([1,0,0]),Q(1)), 'non-core base point accepted')
    # Unit ball offsets mask an inadmissible cone factor pair at small scale.
    a,b,c = Q(0),Q(4,5),Q(13,20)
    need(c*c*(1-a*b)**2 > (1-a*a)*(1-b*b), 'bad full-ray hypothesis accepted')
    def loss(L):
        r,s = Q(13,20)*L,L
        return ((1+r)**2+(1+s)**2-2*c*(1+r)*(1+s)
                -(1+a*r)**2-(1+b*s)**2+2*c*(1+a*r)*(1+b*s))
    need(loss(1)==Q(213,400) and loss(16)==Q(-162,25), 'finite-sample masking control')
    # Parallel rays from different points of a segment cannot have differing factors.
    source = dist2(vec([-1,2,0]),vec([1,2,0]))
    target = dist2(vec([-1,0,0]),vec([1,1,0]))
    need(source==4 and target==5,'parallel-factor control')
    # Surd comparator boundaries and both mixed-sign cases.
    expected = [(1,-1,1,0),(1,-1,2,-1),(2,-1,2,1),(-1,1,2,1),(-2,1,2,-1),(0,-1,2,-1)]
    for aa,bb,dd,wanted in expected:
        need(surd_sign(aa,bb,dd)==wanted,'quadratic surd comparison')
    return {'invalid_normal_inputs_rejected':3,'finite_sample_squared_loss':str(loss(1)),
            'same_rays_large_scale_squared_loss':str(loss(16)),
            'unequal_parallel_factors_source_squared_distance':str(source),
            'unequal_parallel_factors_target_squared_distance':str(target),
            'exact_surd_boundary_controls':len(expected)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    pins=json.loads((base/'NORMAL_INPUTS.json').read_text())
    for name,digest in pins['files'].items():
        need(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original angular input changed: '+name)
    result={'schema':'normal-bundle-author-controls-v1','original_angular_pins':'PASS',
            'normal_identity':normal_identity(),'motions':audit_motions(),
            'rejected_controls':rejected_controls(),
            'raise_samples':len(ANGLES),'lower_samples':3,
            'status':'NORMAL_BUNDLE_AUTHOR_CHECKS_PASS_NOT_INDEPENDENT_REVIEW'}
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        need(output==(base/'NORMAL_EXPECTED.json').read_text(),'NORMAL_EXPECTED.json mismatch')
        print('NORMAL_BUNDLE_AUTHOR_CHECKS_PASS')
    else:
        print(output,end='')


if __name__=='__main__':
    main()
