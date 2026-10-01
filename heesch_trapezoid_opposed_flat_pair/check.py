#!/usr/bin/env python3
"""Exact affine geometry for an opposed-flat two-copy obstruction.

Generic affine/star/network primitives are adapted from the same author's
heesch_trapezoid_tip_propagation/check.py, graph8468. No prior executable
or native formula is imported. Written bridges are credited in proof.md.

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
import argparse
import copy

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


def flat_mates(p):
    ends=(image((N,Lin(-1)),p),image((N-1,Lin(1)),p))
    if p[0]:ends=ends[::-1]
    a,b=ends;mates=[]
    for key in sorted(MATRICES):
        trial=(image((N,Lin(-1)),(*key,Z,Z)),image((N-1,Lin(1)),(*key,Z,Z)))
        if key[0]:trial=trial[::-1]
        u,v=trial
        if sub(v,u)==sub(a,b):mates.append((*key,*sub(b,u)))
    return tuple(mates),ends


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


def concrete_compose(p,q):
    origin=image((0,0),q)
    columns=tuple(sub(image(image(v,q),p),image(origin,p)) for v in ((1,0),(0,1)))
    key=next(k for k,cols in MATRICES.items() if cols==columns)
    return (*key,*image(q[2:],p))


def positive_fixture(c):
    n=c['n'];assert n==12 and c['offset']==5
    poses=tuple(map(tuple,c['normalized_poses']))
    assert poses==((0,0,0,0),(1,3,17,-2)) and c['boundary_cycles']==1
    assert c['frame']==[0,1,-1,-22]
    assert [list(concrete_compose(tuple(c['frame']),p)) for p in poses]==c['actual_poses']
    polys=[tuple(tuple(v.value(n) for v in z) for z in quad(p)) for p in poses]
    for i,p in enumerate(polys):
        for q in polys[:i]:
            separated=False
            for v,other in ((p,q),(q,p)):
                for a,b in zip(v,v[1:]+v[:1]):
                    if all(det(sub(b,a),sub(z,a))<=0 for z in other):separated=True
            assert separated,'Fixture skeleton interiors overlap'
    owners=defaultdict(list)
    for i,p in enumerate(poses):
        for a,b,s in concrete_chords(n,p):owners[tuple(sorted((a,b)))].append((i,a,b,s))
    outside=[];contacts=0
    for rows in owners.values():
        assert len(rows)<=2
        if len(rows)==2:
            x,y=rows
            assert x[1:3]==y[2:0:-1] and x[-1]+y[-1]==0
            contacts+=1
        else:outside.append(rows[0])
    successor={r[1]:r[2] for r in outside}
    assert len(successor)==len(outside) and set(successor)==set(successor.values())
    remaining=set(successor);cycles=0
    while remaining:
        start=min(remaining);v=start
        while True:
            assert v in remaining
            remaining.remove(v);v=successor[v]
            if v==start:break
        cycles+=1
    assert cycles==c['boundary_cycles']
    edges=list(owners);minimum=None;incident=defaultdict(set)
    for a,b in edges:
        assert norm(sub(b,a)) in (1,3)
        incident[a].add(RAYS.index(primitive(sub(b,a))))
        incident[b].add(RAYS.index(primitive(sub(a,b))))
    for i,(a,b) in enumerate(edges):
        for u,v in edges[:i]:
            if {a,b}&{u,v}:continue
            d=segment_distance2(a,b,u,v)
            assert d>=F(3,4),'Fixture loses the physical transfer margin'
            minimum=d if minimum is None else min(minimum,d)
    assert minimum==F(3,4)
    assert all(min((a-b)%12,(b-a)%12)>=1 for rows in incident.values() for a in rows for b in rows if a!=b)
    return {'copies':len(poses),'whole_contacts':contacts,'exposed_ports':len(outside),
            'boundary_cycles':cycles,'nonincident_distance_squared':'3/4',
            'ray_separation_degrees':30,'scope':'Nonvacuous physical subpacking via credited bounded deformation; no corona is asserted.'}


def lower_interval(x, left, right_offset):
    """Exact affine minimum on n>=8, left<=j<=n+right_offset."""
    x=linear(x)
    assert 8+right_offset>=left
    if x.b>=0:
        base,slope=x.c+left*x.b,x.a
    else:
        base,slope=x.c+right_offset*x.b,x.a+x.b
    assert slope>=0,('Unbounded affine domain',x)
    return base+8*slope


def lower_offset(x):
    return lower_interval(x,1,-2)


def unit_midpoint_margin():
    """Every charged unit midpoint is >=sqrt(3)/4 from other carriers.

    Long bottom/top units use an affine unit index, proved on their entire
    index domains. The two left units are explicit. Euclidean squared
    distance is derived from primitive determinant slacks.
    """
    root=(0,0,0,0)
    cases=[('bottom',(J+F(1,2),Lin(-1)),0,lambda s:lower_interval(s,0,-1)),
           ('top',(J+F(1,2),Lin(1)),2,lambda s:lower_interval(s,0,-2)),
           ('left_lower',(Z,Lin(-F(1,2))),3,lower_n),
           ('left_upper',(Z,Lin(F(1,2))),3,lower_n)]
    records=[]
    for name,point,carrier,domain in cases:
        bounds=[]
        for i,(d,a) in enumerate(planes(quad(root))):
            slack=det(d,sub(point,a))
            if i==carrier:
                assert slack==Z
                continue
            lo=domain(slack)
            dsq=3*lo*lo/(4*norm(d))
            assert lo>0 and dsq>=F(3,16)
            bounds.append(str(dsq))
        records.append({'unit_type':name,'other_carrier_distance_squared_bounds':bounds})
    # Midpoint (1/2,-1), followed vertically down by sqrt(3)/32.
    displacement=(F(1,32),-F(1,16))
    assert norm(displacement)==F(3,1024)
    assert F(3,1024)>F(1,1600)**2
    return {'complete_unit_cases':records,'minimum_other_carrier_distance_squared':'3/16',
            'shared_carrier_distance_squared_at_overlap_point':'3/1024',
            'maximum_arc_displacement':'1/1600',
            'overlap_point_axial':['17/32','-17/16'],
            'scope':'Exact carrier inequalities plus the written homotopy argument put this point inside both the negative mirror mate and any positive mate of the protected negative unit.'}


def verify(c):
    assert c['agent']=='six-heesch-3' and c['role']=='researcher'
    assert c['geometry']=={'width_minimum':8,'amplitude':'1/100',
                          'maximum_displacement':'1/1600',
                          'genuine_angles':[60,90,90,120],
                          'signs':{'bottom':-1,'top':1,'left':1,'flat':0}}
    assert c['domain']=={'offset_minimum':1,'offset_maximum':'n-2'}
    assert c['protected_roles']==['O','B']
    assert c['pair']=={'O':[0,0,0,0],'B_orientation':[1,3],
                       'B_translation':['n+l','-2']}
    O=(0,0,0,0);B=(1,3,N+J,Lin(-2))
    mates,ends=flat_mates(B)
    proper=(0,0,J-N+1,Lin(-2))
    mirrored=(1,0,J-N+1,Lin(-2))
    assert mates==(proper,mirrored)
    assert ends==((J,Lin(-1)),(J+1,Lin(-3)))
    assert c['flat_mates']==[[0,0,'l-n+1',-2],[1,0,'l-n+1',-2]]
    assert c['flat_endpoints']==[['l',-1],['l+1',-3]]
    tip=(Z,Lin(-1))
    assert slots(quad(O),tip,lower_offset)=={0,1}
    assert slots(quad(proper),tip,lower_offset)==set(range(6,12))
    assert lower_offset(-(J-N+1))>=1
    assert lower_offset(J)>=1
    assert c['proper_gap']=={'point':[0,-1],'old_slots':[0,1],
                             'new_slots':[6,7,8,9,10,11],
                             'gap_slots':[2,3,4,5],'bounding_states':[1,1]}
    assert words(120,1,1)==[]
    # The mirrored bottom is a negative carrier running from l to l-n.
    # It contains this entire unit, strictly away from its left endpoint.
    assert lower_offset(N-J)>=2 and lower_offset(J-1)>=0
    start=image((N-J,Lin(-1)),mirrored)
    finish=image((N-J+1,Lin(-1)),mirrored)
    assert start==(Z,Lin(-1)) and finish==(Lin(1),Lin(-1))
    assert c['mirrored_negative_unit']=={'endpoints':[[1,-1],[0,-1]],
                                       'state':-1,'old_state':-1}
    # Reflection reverses CCW traversal, so finish->start is its unit.
    margin=unit_midpoint_margin()
    return {'uniform_pair':{'widths':'every integer n>=8','offsets':'every integer 1<=l<=n-2',
                            'protected_roles':['O','B'],'complete_whole_flat_mates':2,
                            'proper_gap_word_count':0,'mirror_rejection':'overlap with a whole mate of protected O'},
            'unit_overlap_margin':margin,
            'n12_positive_pair':positive_fixture(c['n12_fixture'])}


def controls(c):
    damaged=[]
    d=copy.deepcopy(c);d['geometry']['amplitude']='1/10';damaged.append(d)
    d=copy.deepcopy(c);d['domain']['offset_minimum']=0;damaged.append(d)
    d=copy.deepcopy(c);d['protected_roles']=['B'];damaged.append(d)
    d=copy.deepcopy(c);d['pair']['B_orientation']=[0,3];damaged.append(d)
    d=copy.deepcopy(c);d['flat_mates'][0][2]='l-n';damaged.append(d)
    d=copy.deepcopy(c);d['proper_gap']['bounding_states'][1]=-1;damaged.append(d)
    d=copy.deepcopy(c);d['mirrored_negative_unit']['state']=1;damaged.append(d)
    d=copy.deepcopy(c);d['n12_fixture']['actual_poses'][1][2]+=1;damaged.append(d)
    for d in damaged:
        try:verify(d)
        except AssertionError:continue
        raise AssertionError('Malformed certificate accepted')
    return len(damaged)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected');args=parser.parse_args()
    c=json.loads((HERE/'certificate.json').read_text())
    result={'agent':'six-heesch-3','role':'researcher',
            'status':'AUTHOR_ALL_WIDTH_OPPOSED_FLAT_PAIR_VERIFIED',
            **verify(c),'malformed_controls_rejected':controls(c),
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'arithmetic':'Python3.11+ exact rational affine coefficients, standard library only.',
            'proof_status':'Written all-real author proof and exact identities/inequalities. Unformalized and independently unreviewed.',
            'scope':'A two-copy local obstruction to one strict surround of both named old copies. No global height, new corona lower bound, inventory census or finite-seven solution.'}
    if args.expected:assert result==json.loads(Path(args.expected).read_text())
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
