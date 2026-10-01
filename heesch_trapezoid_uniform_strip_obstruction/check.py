"""Exact affine certificate for every integer width n>=8.

Two complete charged covers force overlapping tiles whenever the root and its
two vertical translates occur. No native solver, enumeration data, old local
cap, candidate pool or geometry helper is imported. The written quartic
atomic-contact and Jordan-boundary arguments remain explicit proof premises.
"""
from fractions import Fraction as F
from math import gcd
import json
import argparse
import hashlib
import sys
from pathlib import Path
import resource
import time

OUT=Path(__file__).resolve().parent
if sys.flags.optimize:
    raise RuntimeError("Ordinary Python with assertions is required")

# An affine scalar is c0+cN*n+cT*t.
def A(c=0,n=0,t=0):return (F(c),F(n),F(t))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def evaluate(a,n,t):return a[0]+a[1]*n+a[2]*t
def det(d,v):return sub(mul(d[0],v[1]),mul(d[1],v[0]))
def norm(d):return d[0]**2+d[0]*d[1]+d[1]**2


def matrix(h,k):
    def image(v):
        q,r=v
        if h:q,r=q+r,-r
        for unused in range(k):q,r=-r,q+r
        return q,r
    return image((1,0)),image((0,1))


def transform(v,key):
    a,b=matrix(*key)
    return add(mul(a[0],v[0]),mul(b[0],v[1])),add(mul(a[1],v[0]),mul(b[1],v[1]))


def quad(pose):
    h,k,q,r=pose
    source=[(A(),A(-1)),(A(n=1),A(-1)),(A(-1,n=1),A(1)),(A(),A(1))]
    result=[]
    for v in source:
        x,y=transform(v,(h,k));result.append((add(x,q),add(y,r)))
    return result[::-1] if h else result


def bounds(slack,lower,upper):
    reports=[]
    for constant,slope in (lower,upper):
        c=slack[0]+slack[2]*constant
        m=slack[1]+slack[2]*slope
        value=c+8*m
        assert m>=0 and value>=F(1,8),('Universal margin failed',slack,lower,upper,c,m,value)
        reports.append({'value_at_n8':str(value),'slope_in_n':str(m)})
    return reports


def certificate(pose,point,lower,upper):
    vertices=quad(pose);out=[]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        edge=(sub(b[0],a[0]),sub(b[1],a[1]))
        sample=tuple(evaluate(x,8,0) for x in edge)
        assert all(x.denominator==1 for x in sample)
        x,y=map(int,sample);scale=gcd(x,y);assert scale>0
        direction=(x//scale,y//scale)
        assert norm(direction) in (1,3)
        assert det(direction,edge)==A(),'Edge direction depends on the parameters'
        component=0 if direction[0] else 1
        factor=mul(F(1,direction[component]),edge[component])
        assert factor[2]==0 and factor[1]>=0 and evaluate(factor,8,0)>0
        relative=(sub(A(point[0]),a[0]),sub(A(point[1]),a[1]))
        slack=det(direction,relative)
        out.append({'primitive_direction':direction,'affine_slack':[str(v) for v in slack],
                    'endpoint_certificates':bounds(slack,lower,upper)})
    return out


def coverage():
    allkeys=[(h,k) for h in range(2) for k in range(6)]
    def directed(vector,key):
        a,b=matrix(*key)
        sign=-1 if key[0] else 1
        return (sign*(vector[0]*a[0]+vector[1]*b[0]),sign*(vector[0]*a[1]+vector[1]*b[1]))
    negative=[key for key in allkeys if directed((1,0),key)==(0,1)]
    positive_top=[key for key in allkeys if directed((-1,0),key)==(-1,0)]
    positive_left=[key for key in allkeys if directed((0,-1),key)==(-1,0)]
    assert negative==[(0,1),(1,4)]
    assert positive_top==[(0,0),(1,3)]
    assert positive_left==[(0,5),(1,4)]
    # Derive every translation as the old reversed-arc start minus the
    # transformed prototype start. t here denotes the prototype unit index.
    templates=[('negative_bottom',(A(t=1),A(-1)),(A(1,t=1),A(-1)),(A(),A()),negative,
                [(A(-1),A(1,t=-1)),(A(-1),A(1,t=1))]),
               ('positive_top',(A(1,t=1),A(1)),(A(t=1),A(1)),(A(1),A(-1)),positive_top,
                [(A(t=-1),A(-2)),(A(2,t=1),A(-2))]),
               ('positive_left',(A(),A(t=1)),(A(),A(-1,t=1)),(A(1),A(-1)),positive_left,
                [(A(1,t=-1),A(-1)),(A(t=1),A(-1))])]
    for name,a,b,target,keys,expected in templates:
        for key,want in zip(keys,expected):
            start=transform(b if key[0] else a,key)
            got=(sub(target[0],start[0]),sub(target[1],start[1]))
            assert got==want,('Provider translation mismatch',name,key,got,want)
    return {'negative_bottom_orientation_codes':negative,'positive_top_orientation_codes':positive_top,
            'positive_left_orientation_codes':positive_left,
            'root_positive_left_unit_raw_forms':['(0,1,-1,b), 2-n<=b<=1','(1,4,-1,b), 1<=b<=n'],
            'root_negative_bottom_unit_raw_forms':['(0,0,a,-2), 2-n<=a<=0','(1,3,a,-2), 2<=a<=n',
                                                 '(0,5,a,-1), a=0,1','(1,4,a,-1), a=0,1'],
            'scope':'Static12-isometry direction completeness and symbolic start/end translations. Unit indices range0..n-1,0..n-2 and0,1 as specified in the written proof.'}


def verify():
    upper=(0,0,A(-1),A(2));lower=(0,0,A(1),A(-2))
    cases=[('upper_positive_proper',(0,1,A(-1),A(t=1)),upper,(F(-1,2),F(9,8)),(2,-1),(1,0)),
           ('upper_positive_reflected_except_forced',(1,4,A(-1),A(t=1)),upper,(F(-1,2),F(3,2)),(2,0),(0,1)),
           ('bottom_negative_top_proper',(0,0,A(t=1),A(-2)),lower,(F(5,4),F(-2)),(2,-1),(0,0)),
           ('bottom_negative_top_reflected',(1,3,A(t=1),A(-2)),lower,(F(5,4),F(-2)),(2,0),(0,1)),
           ('bottom_negative_left_proper',(0,5,A(t=1),A(-1)),lower,(F(3,2),F(-2)),(0,0),(1,0)),
           ('bottom_negative_left_reflected_except_forced',(1,4,A(t=1),A(-1)),lower,(F(3,2),F(-2)),(1,0),(1,0)),
           ('forced_provider_conflict',(1,4,A(-1),A(1)),(1,4,A(),A(-1)),(F(-1,2),F(-2)),(0,0),(0,0))]
    proof=[]
    for name,p,q,point,l,u in cases:
        assert u[1]-l[1]>=0 and u[0]-l[0]+8*(u[1]-l[1])>=0
        proof.append({'case':name,'point':[str(x) for x in point],
                      'parameter_lower':[str(x) for x in l],'parameter_upper':[str(x) for x in u],
                      'provider_planes':certificate(p,point,l,u),'blocker_planes':certificate(q,point,l,u)})
    return {'agent':'six-heesch-3','role':'researcher','status':'UNIFORM_AFFINE_INTERIOR_MARGIN_CERTIFICATE_VERIFIED',
            'parameter_domain':'Every integer n>=8','coverage':coverage(),'cases':proof,
            'linear_halfplane_inequalities':sum(len(x['provider_planes'])+len(x['blocker_planes']) for x in proof),
            'primitive_determinant_margin':'1/8','euclidean_boundary_distance_lower':'1/16',
            'profile_displacement_upper':'1/1600','forced_providers':[[1,4,-1,1],[1,4,0,-1]],
            'fixed_motif':[[0,0,0,0],[0,0,-1,2],[0,0,1,-2]],
            'written_claim':'No finite packing containing the fixed motif can have its normalized root strictly in the interior of the packing union. Arbitrary other real copies and topology are allowed.',
            'trust_boundary':'Exact affine arithmetic and staticD6 direction/translation identities are checked here. Written atomic-quartic mating and Jordan-boundary stability prove the real-motion and physical-overlap bridges. Not a formalization, height record or global upper forTn.'}


def controls():
    failures=0
    trials=[lambda:bounds(A(c=10,n=-1),(0,0),(0,0)),
            lambda:bounds(A(c=1,n=1,t=-1),(0,0),(2,1)),
            lambda:certificate((1,4,A(5),A(-1)),(F(-1,2),F(-2)),(0,0),(0,0)),
            lambda:certificate((0,1,A(-1),A(t=1)),(F(-1,2),F(9,8)),(1,-1),(1,0))]
    for trial in trials:
        try:trial()
        except AssertionError:failures+=1
        else:raise AssertionError('A malformed universal-margin control was accepted')
    return failures


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected')
    parser.add_argument('--certificate')
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args();start=time.monotonic();report=verify()
    canonical=json.dumps(report,sort_keys=True,separators=(',',':')).encode()
    summary={'agent':'six-heesch-3','role':'researcher','status':report['status'],
             'parameter_domain':report['parameter_domain'],
             'linear_halfplane_inequalities':report['linear_halfplane_inequalities'],
             'primitive_determinant_margin':report['primitive_determinant_margin'],
             'euclidean_boundary_distance_lower':report['euclidean_boundary_distance_lower'],
             'profile_displacement_upper':report['profile_displacement_upper'],
             'certificate_canonical_sha256':hashlib.sha256(canonical).hexdigest()}
    if args.controls:summary['malformed_controls_rejected']=controls()
    if args.expected:
        expected=json.loads(Path(args.expected).read_text())
        assert summary==expected,'Exact expected report differs'
    if args.certificate:Path(args.certificate).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(summary,seconds=time.monotonic()-start,
                          rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
