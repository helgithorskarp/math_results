#!/usr/bin/env python3
"""Exact strict-orbit certificate. CPython>=3.11; standard library only.

No code or finite-order data is imported from the preceding packet. Its
all-hinge theorem remains a cited mathematical dependency of PROOF.md.
"""
from fractions import Fraction as F
from itertools import permutations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

A=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))
WA=(12,7,15,44)
WB=(21,11,23,43)
GROUP=tuple(product(permutations(range(3)),product((-1,1),repeat=3)))
KEYS=tuple(product(range(3),range(5),range(7)))
AXES=((1,0,0),(0,1,0),(0,0,1))


def need(ok,why):
    if not ok:raise RuntimeError(why)


def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()


def columns(points):
    out=[]
    for perm,signs in GROUP:
        row=[]
        for point in points:
            e=[0,0,0]
            for i in range(3):e[perm[i]]=signs[i]*point[i]
            powers=(1+e[0],2+e[0]+e[1],3+sum(e))
            need(all(0<=x<=d for x,d in zip(powers,(2,4,6))), 'Uncleared exponent')
            col={k:comb(powers[0],k[0])*comb(powers[1],k[1])*comb(powers[2],k[2])
                 for k in KEYS if all(j<=d for j,d in zip(k,powers))}
            # Entry-level cross-check via repeated polynomial multiplication.
            direct={(0,0,0):1}
            for axis,power in enumerate(powers):
                for _ in range(power):
                    nxt=dict(direct)
                    for k,v in direct.items():
                        new=list(k);new[axis]+=1;new=tuple(new)
                        nxt[new]=nxt.get(new,0)+v
                    direct=nxt
            need(col==direct,'Two coefficient constructions disagree')
            row.append(col)
        out.append(row)
    return out


def check_targets(targets,data):
    need(len(targets)==48,'Wrong assignment size')
    least=None;nonzero=0;linear_witnesses=[]
    for i,j in enumerate(targets):
        need(isinstance(j,int) and 0<=j<48,'Invalid target label')
        positive_axes=set()
        for name,base,source in [('A',WA,i),('B',WB,i^7)]:
            polys=data[name]
            for k in KEYS:
                form=tuple(polys[j][l].get(k,0)-polys[source][l].get(k,0) for l in range(4))
                value=sum(d*w for d,w in zip(form,base))
                if not any(form):continue
                need(value>0,'A claimed robust comparison has a nonpositive coefficient')
                margin=F(value,184*max(map(abs,form)))
                need(margin>=F(1,552),'Insufficient weight margin')
                least=margin if least is None else min(least,margin)
                nonzero+=1
                if k in AXES:
                    positive_axes.add(k)
                    linear_witnesses.append([i,j,name,list(k),list(form),value])
        need(positive_axes==set(AXES),'One chamber variable has no strict linear witness')
    return least,nonzero,linear_witnesses


def audit():
    here=Path(__file__).resolve().parent
    raw=here.joinpath('STRICT_TARGETS.json').read_bytes()
    cert=json.loads(raw)
    need(cert['schema']=='strict-square-cone-orbit-v1','Wrong certificate schema')
    need(len(GROUP)==len(set(GROUP))==48,'Invalid group')
    for i,(p,s) in enumerate(GROUP):
        need(GROUP[i^7]==(p,tuple(-v for v in s)),'Invalid antipodal label')
    data={'A':columns(A),'B':columns(B)}
    least,count,witnesses=check_targets(cert['targets'],data)
    rejected=False
    try:check_targets([0]*48,data)
    except RuntimeError:rejected=True
    need(rejected,'Constant invalid assignment was accepted')
    radius=F(1,4000);kappa=F(1,552)-radius
    need(kappa>0,'Weight class does not lie strictly inside the old cone')
    need(F(7,184)-radius>F(1,32),'The uniform positive mass floor failed')
    need(F(3,184)-radius>0 and F(30,184)-radius>0,'Nonzero source gradient not certified')
    need(F(1,6)-2*F(1,48)>=F(1,8),'Cloud mean-support gap failed')
    # Every base pair contracts; the minimum source separation squared is 2.
    X=((0,0,0),)+A+tuple(tuple(-x for x in b) for b in B)
    Y=((0,0,0),)+A+B
    dx=[];losses={}
    for i in range(9):
        for j in range(i):
            u=sum((a-b)**2 for a,b in zip(X[i],X[j]))
            v=sum((a-b)**2 for a,b in zip(Y[i],Y[j]))
            need(u>=v,'Base map is not a contraction')
            dx.append(u);losses[u-v]=losses.get(u-v,0)+1
    need(min(dx)==2 and losses=={0:28,8:8},'Wrong base geometry')
    return {
      'status':'STRICT_ORBIT_AND_STABILITY_INPUTS_PASS',
      'strict_targets':cert['targets'],
      'assignment_count':48,'strict_chamber_axis_obligations':144,
      'positive_linear_coefficients':len(witnesses),
      'nonzero_coefficient_forms_checked':count,
      'coefficient_margin':str(least),
      'weight_radius':str(radius),'strict_margin_lower_bound':str(kappa),
      'minimum_mass_lower_bound':'1/32','mean_support_gap_lower_bound':'1/6',
      'cloud_radius_for_geometric_gap':'1/48','cloud_geometric_gap_lower_bound':'1/8',
      'minimum_source_distance_squared':2,'pair_loss_counts':losses,
      'two_coefficient_constructions_agree':True,'invalid_assignment_rejected':True,
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),
      'linear_witness_digest':hashlib.sha256(encoded(witnesses)).hexdigest(),
      'trust_boundary':'Exact finite strictness lemma plus the analytic proof and the cited preceding all-hinge theorem; no peer review or formalization.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=encoded(audit())
    if args.check:
        need(result==Path(__file__).with_name('EXPECTED.json').read_bytes(),'Audit differs')
        print('STRICT_ORBIT_AND_STABILITY_INPUTS_PASS',hashlib.sha256(result).hexdigest())
    else:print(result.decode(),end='')

if __name__=='__main__':main()
