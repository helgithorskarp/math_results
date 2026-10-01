#!/usr/bin/env python3
"""Exact affine geometry for negative-edge parity and flat-forced tip lemmas.

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


def lower_start(v):
 v=linear(v)
 if v.b>=0:base,slope=v.c+2*v.b,v.a
 else:base,slope=v.c,v.a+v.b
 assert slope>=0
 return base+8*slope


def verify_parity(c):
 assert c['agent']=='six-heesch-3' and c['role']=='researcher'
 assert c['root']==[0,0,0,0] and c['neighbor_orientation']==[1,4]
 assert c['neighbor_row']==-1 and c['forced_translation']==[-2,0]
 assert c['base_offset']==0 and c['forbidden_parity']=='even'
 assert c['width_domain']=='n>=8' and c['step_domain']=='2<=a<=n'
 O=(0,0,Z,Z);P=(1,4,J,Lin(-1));Q=(1,4,J-2,Lin(-1))
 x=(J-1,Lin(-1));z=(Z,Lin(-1))
 so,sp=slots(quad(O),x,lower_start),slots(quad(P),x,lower_start)
 assert so==set(range(6)) and sp=={8,9,10,11} and not so&sp
 missing=set(range(12))-so-sp;assert missing=={6,7}
 assert image((Z,Lin(1)),P)==x
 # P's top germ from D is southwest and positive; O's remaining old germ
 # at x is west and negative. Every filler has the unique prototype60 corner.
 assert image((1,0),(1,4,0,0))==(0,-1)
 options=[]
 for key in sorted(MATRICES):
  at=image((Z,Lin(-1)),(*key,Z,Z));p=(*key,*sub(x,at))
  if slots(quad(p),x,lower_start)!=missing:continue
  neg,pos=image((1,0),(*key,0,0)),image((0,1),(*key,0,0))
  if neg==(0,-1) and pos==(-1,0):options.append(p)
 assert options==[Q] and image((Z,Lin(-1)),Q)==x
 P0=(1,4,Z,Lin(-1))
 so,sp=slots(quad(O),z),slots(quad(P0),z)
 assert so=={0,1} and sp==set(range(6,12)) and not so&sp
 assert set(range(12))-so-sp=={2,3,4,5}
 assert image((Z,Z),P0)==z
 assert image((Z,Lin(1)),O)==(Z,Lin(1))
 assert image((Z,Lin(1)),P0)==(Lin(-1),Lin(-1))
 assert words(120,1,1)==[]
 return {'width_domain':'every integer n>=8','step_domain':'every integer 2<=a<=n',
         'complete_corner_motions':12,'unique_filler':'P_(a-2)',
         'first_gap_degrees':60,'base_gap_degrees':120,'base_gap_states':[1,1],
         'base_necessary_gap_words':0,'consequence':'offsets 0<=a<=n in orientation (1,4) must be odd when only O is strictly interior',
         'odd_offsets':'necessary condition only; no existence claim'}


def verify_flat(c):
 assert c['agent']=='six-heesch-3' and c['role']=='researcher'
 assert c['root']==[0,0,0,0] and c['flat_owner_orientation']==[0,1]
 assert c['flat_owner_q']==-1 and c['blocker_q']==1
 assert c['owner_row_coefficients']==[0,-2] and c['offsets']==[0,1]
 assert c['protected_roles']==['O','C']
 cases=[]
 for t in c['offsets']:
  O=(0,0,Z,Z)
  C=(0,1,Lin(-1),-2*N+t);D=(0,1,Lin(1),-2*N+t)
  Q=(0,4,Lin(-1),Lin(t-1));forced=(1,4,Lin(-1),Lin(t-1))
  mates,ends=flat_mates(C)
  assert set(mates)=={Q,forced} and ends==((Z,-N+t-1),(Lin(-2),-N+t))
  a,b=(Z,-N+t-1),(Z,-N+t)
  assert image((N-1,Lin(1)),Q)==a
  assert image((N-2,Lin(1)),Q)==b
  assert image((N-1,Lin(1)),D)==b
  assert image((N-2,Lin(1)),D)==a
  midpoint=(Z,-N+t-F(1,2))
  for p in (Q,D):
   slacks=[det(d,sub(midpoint,v)) for d,v in planes(quad(p))]
   assert slacks.count(Z)==1
   assert all(s==Z or lower_n(s)>=F(1,2) for s in slacks)
  z=(Z,Lin(t-1));so=slots(quad(O),z);sf=slots(quad(forced),z)
  assert so==({0,1} if t==0 else {8,9,10,11,0,1})
  assert sf=={6,7} and not so&sf
  # The clockwise gap from the old positive north ray to F's positive
  # west ray is 120 degrees, at either a genuine or a regular OLD label.
  assert not (so|sf)&{2,3,4,5}
  assert image((Z,Lin(-1)),forced)==z
  assert image((Z,Z),forced)==(Lin(-1),Lin(t-1))
  assert words(120,1,1)==[]
  cases.append({'offset':t,'complete_whole_flat_mates':2,
                'excluded_mate':'opposed positive/positive top unit',
                'old_sector_degrees':len(so)*30,'forced_sector_degrees':60,
                'protected_gap_degrees':120,'protected_gap_states':[1,1],
                'gap_word_count':0,'midpoint_other_primitive_slack_lower':'1/2'})
 return {'width_domain':'every integer n>=8; exact affine identities and inequalities','cases':cases,'only_O_and_C_require_interiority':True}


def concrete_compose(p,q):
    origin=image((0,0),q)
    columns=tuple(sub(image(image(v,q),p),image(origin,p)) for v in ((1,0),(0,1)))
    key=next(k for k,cols in MATRICES.items() if cols==columns)
    return (*key,*image(q[2:],p))


def positive_fixture(c,kind):
    n=c['n'];assert n==12
    poses=tuple(map(tuple,c['normalized_poses']))
    if kind=='parity':
        assert poses==((0,0,0,0),(1,4,2,-1)) and c['boundary_cycles']==1
    else:
        assert poses==((0,0,0,0),(0,1,-1,-24),(0,1,1,-24)) and c['boundary_cycles']==2
        assert c['frame']==[0,4,47,-16]
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


def verify(c):
    assert c['agent']=='six-heesch-3' and c['role']=='researcher'
    assert c['geometry']=={'width_minimum':8,'amplitude':'1/100','maximum_displacement':'1/1600',
                          'genuine_angles':[60,90,90,120],
                          'signs':{'bottom':-1,'top':1,'left':1,'flat':0}}
    return {'parity':verify_parity(c['parity']),'flat_tip':verify_flat(c['flat_tip']),
            'parity_n12_fixture':positive_fixture(c['parity_n12_fixture'],'parity'),
            'flat_n12_fixture':positive_fixture(c['flat_n12_fixture'],'flat')}


def controls(c):
    damaged=[]
    d=copy.deepcopy(c);d['geometry']['amplitude']='1/10';damaged.append(d)
    d=copy.deepcopy(c);d['parity']['forced_translation'][0]=-1;damaged.append(d)
    d=copy.deepcopy(c);d['parity']['forbidden_parity']='odd';damaged.append(d)
    d=copy.deepcopy(c);d['flat_tip']['blocker_q']=2;damaged.append(d)
    d=copy.deepcopy(c);d['flat_tip']['offsets']=[0,2];damaged.append(d)
    d=copy.deepcopy(c);d['flat_n12_fixture']['actual_poses'][2][3]+=1;damaged.append(d)
    for d in damaged:
        try:verify(d)
        except AssertionError:pass
        else:raise AssertionError('Malformed certificate accepted')
    return len(damaged)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected');args=parser.parse_args()
    c=json.loads((HERE/'certificate.json').read_text())
    r={'agent':'six-heesch-3','role':'researcher','status':'AUTHOR_ALL_WIDTH_TIP_OBSTRUCTIONS_VERIFIED',
       **verify(c),'malformed_controls_rejected':controls(c),
       'canonical_certificate_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
       'arithmetic':'Python3.11+ integers and exact rational affine coefficients; standard library only.',
       'proof_status':'Written all-real author proofs plus separate exact readers. Unformalized and independently unreviewed.',
       'scope':'Two local necessary conditions, no arbitrary-real corona census, new corona lower bound, exact Heesch height or finite-seven solution.'}
    if args.expected:assert r==json.loads(Path(args.expected).read_text()),'Expected output mismatch'
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
