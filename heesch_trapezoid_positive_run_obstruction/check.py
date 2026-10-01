#!/usr/bin/env python3
"""Exact affine geometry and a compact four-copy obstruction certificate.

Python standard library only; no constructor, inventory, SAT solver, proof
trace or previous executable is imported. The all-real completeness bridges
are written in proof.md and credited there. This is not a formal proof.
"""
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json
import sys

if sys.flags.optimize:
    raise RuntimeError('Ordinary Python is required; optimized Python is unsupported')
HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Lin:
    """c + a*n + b*j, with exact rational coefficients."""
    c: F = F(0)
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        for k in ('c', 'a', 'b'):
            object.__setattr__(self, k, F(getattr(self, k)))

    def __add__(self, other):
        o = linear(other)
        return Lin(self.c+o.c, self.a+o.a, self.b+o.b)

    __radd__ = __add__

    def __neg__(self):
        return Lin(-self.c, -self.a, -self.b)

    def __sub__(self, other):
        return self + -linear(other)

    def __rsub__(self, other):
        return linear(other) + -self

    def __mul__(self, scalar):
        assert not isinstance(scalar, Lin), 'Only affine-by-scalar products are needed'
        s = F(scalar)
        return Lin(self.c*s, self.a*s, self.b*s)

    __rmul__ = __mul__

    def value(self, n, j=0):
        return self.c+self.a*n+self.b*j


def linear(x):
    return x if isinstance(x, Lin) else Lin(x)


Z, N, J = Lin(), Lin(a=1), Lin(b=1)
ZERO = (Z, Z)
RAYS = ((1,0),(1,1),(0,1),(-1,2),(-1,1),(-2,1),
        (-1,0),(-1,-1),(0,-1),(1,-2),(1,-1),(2,-1))


def add(x,y): return x[0]+y[0], x[1]+y[1]
def sub(x,y): return x[0]-y[0], x[1]-y[1]
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def norm(x): return x[0]*x[0]+x[0]*x[1]+x[1]*x[1]
def primitive(x):
    assert all(F(z).denominator == 1 for z in x)
    d = gcd(int(x[0]), int(x[1]))
    assert d > 0
    return int(x[0])//d, int(x[1])//d


def rotate(x): return -x[1], x[0]+x[1]
def reflect(x): return x[0]+x[1], -x[1]
MATRICES = {}
for h,k in product(range(2), range(6)):
    columns = []
    for v in ((1,0),(0,1)):
        u = reflect(v) if h else v
        for _ in range(k):
            u = rotate(u)
        columns.append(u)
    MATRICES[h,k] = tuple(columns)
assert len(set(MATRICES.values())) == 12


def image(x,p):
    u,v = MATRICES[p[:2]]
    return x[0]*u[0]+x[1]*v[0]+p[2], x[0]*u[1]+x[1]*v[1]+p[3]


def quad(p):
    vertices = ((Z,Lin(-1)),(N,Lin(-1)),(N-1,Lin(1)),(Z,Lin(1)))
    if p[0]: vertices = vertices[::-1]
    return tuple(image(v,p) for v in vertices)


def lower_n(x):
    x = linear(x)
    assert x.b == 0 and x.a >= 0, ('Not bounded below on n>=8', x)
    return x.value(8)


def lower_cut(x):
    """Exact minimum on n>=8, 3<=j<=n, if bounded below."""
    x = linear(x)
    if x.b >= 0:
        base, slope = x.c+3*x.b, x.a
    else:
        base, slope = x.c, x.a+x.b
    assert slope >= 0, ('Not bounded below on the cut domain', x)
    return base+8*slope


def planes(poly):
    result = []
    for a,b in zip(poly, poly[1:]+poly[:1]):
        edge = sub(b,a)
        d = primitive(tuple(z.value(8,3) for z in edge))
        assert det(d,edge) == Z
        idx = 0 if d[0] else 1
        factor = edge[idx]*F(1,d[idx])
        assert lower_n(factor) >= 1
        result.append((d,a))
    return result


def buffered_point(p,q,x,cut_domain=False):
    bounds = []
    for d,a in planes(quad(p))+planes(quad(q)):
        s = det(d,sub(x,a))
        lo = (lower_cut if cut_domain else lower_n)(s)
        assert lo > 0, ('Point not strictly inside both skeletons', lo)
        # In axial coordinates: distance^2 = 3*det(d,x-a)^2/(4*norm(d)).
        dsq = 3*lo*lo/(4*norm(d))
        assert dsq > F(1,1600)**2
        bounds.append((lo,dsq))
    return min(s for s,_ in bounds), min(d for _,d in bounds)


def slots(poly,x,domain=lower_n):
    active = []
    for d,a in planes(poly):
        s = det(d,sub(x,a))
        if s == Z:
            active.append(d)
        else:
            assert domain(s) > 0, 'Point must be on the indicated boundary for every width'
    assert active
    result = set()
    for k in range(12):
        test = add(RAYS[k], RAYS[(k+1)%12])
        if all(det(d,test) > 0 for d in active): result.add(k)
    return result


def words(angle,left,right):
    types = {60:((-1,1),(1,-1)),90:((-1,0),(0,-1),(1,0),(0,1)),120:((1,1),)}
    answers = []
    def visit(remaining,previous,sofar):
        if remaining == 0:
            if previous == -right: answers.append(sofar)
            return
        for a,pairs in types.items():
            if a > remaining: continue
            for x,y in pairs:
                if x == -previous: visit(remaining-a,y,sofar+[(a,x,y)])
    visit(angle,left,[])
    return answers


def bottom_pairs():
    pair = []
    for side in (-1,1):
        options = []
        for key in sorted(MATRICES):
            z = image((N,Lin(-1)),(*key,Z,Z))
            p = (*key,*sub((J,Z),z))
            delta = sub(image((Z,Lin(-1)),p),(J,Z))
            if delta != (side*N,Z): continue
            if all(lower_n(-v[1]) >= 0 for v in quad(p)): options.append(p)
        assert len(options) == 1
        pair.append(options[0])
    expected = ((1,0,J-N+1,Lin(-1)),(0,3,J+N,Lin(-1)))
    assert tuple(pair) == expected
    flat = []
    for p in pair:
        ends = (image((N,Lin(-1)),p),image((N-1,Lin(1)),p))
        flat.append(ends[::-1] if p[0] else ends)
    assert flat[0] == flat[1][::-1]
    assert set(flat[0]) == {(J,Z),(J+1,Lin(-2))}
    return expected


def flat_mates(p):
    ends = (image((N,Lin(-1)),p),image((N-1,Lin(1)),p))
    if p[0]: ends = ends[::-1]
    a,b = ends
    mates = []
    for key in sorted(MATRICES):
        ends2 = (image((N,Lin(-1)),(*key,Z,Z)),image((N-1,Lin(1)),(*key,Z,Z)))
        if key[0]: ends2 = ends2[::-1]
        u,v = ends2
        if sub(v,u) == sub(a,b): mates.append((*key,*sub(b,u)))
    return tuple(mates),ends


def verify_affine(certificate):
    encoded = certificate['uniform_old_poses']
    old = tuple((h,k,Lin(*q),Lin(*r)) for h,k,q,r in encoded)
    A,B,C,D = old
    assert old == ((0,2,Lin(1),Z),(1,0,Lin(1),Lin(1)),
                   (0,3,2*N,Lin(1)),(0,3,2*N+2,Lin(-1)))
    # Positive left of A, positive top of B and the first positive top of C.
    assert [image(v,A) for v in ((Z,Lin(1)),ZERO,(Z,Lin(-1)))] == [(Z,Z),(Lin(1),Z),(Lin(2),Z)]
    assert [image(v,B) for v in ((Z,Lin(1)),(N-1,Lin(1)))] == [(Lin(2),Z),(N+1,Z)]
    assert [image(v,C) for v in ((N-1,Lin(1)),(N-2,Lin(1)))] == [(N+1,Z),(N+2,Z)]
    assert slots(quad(A),(Lin(1),Z)) == set(range(6))
    s1,s2 = slots(quad(A),(Lin(2),Z)),slots(quad(B),(Lin(2),Z))
    assert not s1&s2 and s1|s2 == set(range(6)) and sorted((len(s1),len(s2))) == [2,4]
    assert slots(quad(B),(J,Z),lower_cut) == set(range(6))
    s1,s2 = slots(quad(B),(N+1,Z)),slots(quad(C),(N+1,Z))
    assert not s1&s2 and s1|s2 == set(range(6)) and len(s1) == len(s2) == 3
    # Every possible change between two bottom mates: 60/60, 60/90, 90/90.
    assert words(60,1,1) == [] and words(30,1,0) == [] and words(30,0,1) == []
    pair = bottom_pairs()
    # L=n+2, so the complete range is 2<=j<=n. For all 3<=j<=n,
    # the right mate collides with the SAME fourth old copy D.
    cut_slack,cut_distance = buffered_point(pair[1],D,(N+F(11,4),Lin(-1)),True)
    G = (0,3,N+2,Lin(-1))
    assert pair[1] == (0,3,N+J,Lin(-1))
    mates,ends = flat_mates(D)
    Q,forced = (0,0,Lin(3),Lin(-1)),(1,0,Lin(3),Lin(-1))
    assert set(mates) == {Q,forced} and ends == ((N+2,Z),(N+3,Lin(-2)))
    # Q's last top unit and B's corresponding top unit have reverse directions
    # and BOTH intrinsic states +1; the two outward quartics overlap.
    assert image((Lin(1),Lin(1)),Q) == (Lin(4),Z)
    assert image((Z,Lin(1)),Q) == (Lin(3),Z)
    assert image((Lin(1),Lin(1)),B) == (Lin(3),Z)
    assert image((Lin(2),Lin(1)),B) == (Lin(4),Z)
    mid = (Lin(F(7,2)),Z)
    for p in (Q,B):
        slacks = [det(d,sub(mid,a)) for d,a in planes(quad(p))]
        assert slacks.count(Z) == 1
        assert all(s == Z or lower_n(s) >= F(1,2) for s in slacks)
    assert F(1,100)*F(1,2)**2*F(1,2)**2 == F(1,1600)
    final_slack,final_distance = buffered_point(forced,G,(Lin(5),Lin(-1)))
    return {'width_domain':'every integer n>=8; affine coefficients, not a sampled interval',
            'run_length':'n+2','complete_cut_range':'2<=j<=n',
            'rejected_cut_range':'3<=j<=n','forced_cut':2,
            'cut_overlap_minimum_primitive_slack':str(cut_slack),
            'cut_overlap_distance_squared_lower':str(cut_distance),
            'forced_overlap_minimum_primitive_slack':str(final_slack),
            'forced_overlap_distance_squared_lower':str(final_distance),
            'whole_flat_mates':2,'excluded_mate':'reverse positive/positive unit overlap'}


def concrete_chords(n,p):
    ports = [((0,1),(0,0),1),((0,0),(0,-1),1)]
    ports += [((i,-1),(i+1,-1),-1) for i in range(n)]
    ports += [((n,-1),(n-1,1),0)]
    ports += [((i,1),(i-1,1),1) for i in range(n-1,0,-1)]
    rows = [(image(a,p),image(b,p),s) for a,b,s in ports]
    return [(b,a,s) for a,b,s in rows] if p[0] else rows


def segment_distance2(a,b,c,d):
    # For disjoint nonincident segments the nearest pair has an endpoint.
    def point_segment(p,u,v):
        z,w = sub(v,u),sub(p,u)
        dot2 = 2*z[0]*w[0]+z[0]*w[1]+z[1]*w[0]+2*z[1]*w[1]
        t = min(F(1),max(F(0),F(dot2,2*norm(z))))
        return norm(sub(p,add(u,(t*z[0],t*z[1]))))
    cross = det(sub(b,a),sub(d,c))
    if cross:
        t,u = F(det(sub(c,a),sub(d,c)),cross),F(det(sub(c,a),sub(b,a)),cross)
        assert not (0<=t<=1 and 0<=u<=1), 'Nonincident segments intersect'
    return min(point_segment(a,c,d),point_segment(b,c,d),point_segment(c,a,b),point_segment(d,a,b))


def verify_positive_instance(certificate):
    n = 12
    old = tuple(tuple(p) for p in certificate['normalized_n12_old_poses'])
    assert old == ((0,2,1,0),(1,0,1,1),(0,3,24,1),(0,3,26,-1))
    polys = [tuple(tuple(v.value(n) for v in z) for z in quad(p)) for p in old]
    for i,p in enumerate(polys):
        for q in polys[:i]:
            found = False
            for v in (p,q):
                other = q if v is p else p
                for a,b in zip(v,v[1:]+v[:1]):
                    if all(det(sub(b,a),sub(z,a)) <= 0 for z in other): found = True
            assert found, 'Skeleton interiors overlap'
    owners = defaultdict(list)
    for i,p in enumerate(old):
        for a,b,s in concrete_chords(n,p): owners[tuple(sorted((a,b)))].append((i,a,b,s))
    outside = []
    contacts = 0
    for edge,rows in owners.items():
        assert len(rows) <= 2
        if len(rows) == 2:
            x,y = rows
            assert x[1:3] == y[2:0:-1] and x[-1]+y[-1] == 0
            contacts += 1
        else: outside.append(rows[0])
    nxt = {row[1]:row[2] for row in outside}
    assert len(nxt) == len(outside) and set(nxt) == set(nxt.values())
    start = min(nxt); x = start; seen = []
    while not seen or x != start:
        assert len(seen) < len(nxt)
        seen.append(x); x = nxt[x]
    assert len(seen) == len(nxt)
    edges = list(owners)
    distances = []
    rays = defaultdict(set)
    for a,b in edges:
        rays[a].add(primitive(sub(b,a))); rays[b].add(primitive(sub(a,b)))
    for i,(a,b) in enumerate(edges):
        for c,d in edges[:i]:
            if {a,b}&{c,d}: continue
            distances.append(segment_distance2(a,b,c,d))
    minimum = min(distances)
    assert minimum == F(3,4) and minimum > (2*F(1,1600))**2
    assert all(s <= set(RAYS) for s in rays.values())
    # Different incident rays are >=30 degrees apart. The quartic's lateral
    # deviation / endpoint distance is <=1/100 < 1/4 < tan(15 degrees).
    assert F(1,100) < F(1,4) and F(7,4)**2 > 3
    assert contacts == 13 and len(outside) == 78
    frame = (0,2,48,-19)
    global_poses = []
    for p in old:
        cols = tuple(sub(image(image(v,p),frame),image(image((0,0),p),frame)) for v in ((1,0),(0,1)))
        key = next(k for k,m in MATRICES.items() if m == cols)
        global_poses.append([*key,*image(p[2:],frame)])
    assert global_poses == certificate['application_global_poses']
    return {'n':n,'physical_disc_copies':4,'whole_contacts':contacts,'exposed_ports':len(outside),
            'minimum_nonincident_distance_squared':str(minimum),'minimum_incident_ray_degrees':30,
            'physical_transfer':'written bounded quartic deformation; matched curves move together'}


def verify(certificate):
    assert certificate['agent'] == 'six-heesch-3' and certificate['role'] == 'researcher'
    assert certificate['claim_scope'] == 'uniform necessary obstruction; no global Heesch upper bound'
    return {'affine':verify_affine(certificate),'positive_instance':verify_positive_instance(certificate)}


def main():
    raw = (HERE/'certificate.json').read_bytes()
    cert = json.loads(raw)
    result = verify(cert)
    controls = 0
    import copy
    for field,mutation in [
        ('uniform_old_poses',lambda x:x[0][2].__setitem__(0,2)),
        ('uniform_old_poses',lambda x:x[3][2].__setitem__(0,3)),
        ('normalized_n12_old_poses',lambda x:x[2].__setitem__(2,25)),
        ('application_global_poses',lambda x:x[0].__setitem__(3,-19)),
        ('claim_scope',lambda x:'global Heesch upper bound'),
    ]:
        bad = copy.deepcopy(cert)
        v = mutation(bad[field])
        if v is not None: bad[field] = v
        try: verify(bad)
        except (AssertionError, ValueError, TypeError): controls += 1
        else: raise RuntimeError('Malformed control accepted')
    assert controls == 5
    report = {'agent':'six-heesch-3','role':'researcher','status':'AUTHOR_EXACT_READER_PASSED',
              **result,'malformed_controls_rejected':controls,
              'canonical_certificate_sha256':hashlib.sha256(json.dumps(cert,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
              'trust_boundary':'written all-real whole-mate and finite-star lemmas; unformalized and independently unreviewed',
              'target_status':'finite-seven target remains open; no new corona count or global height claimed'}
    expected = json.loads((HERE/'expected.json').read_text())
    assert report == expected
    print(json.dumps(report,indent=2))


if __name__ == '__main__': main()
