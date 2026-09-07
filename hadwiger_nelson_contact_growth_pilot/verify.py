#!/usr/bin/env python3
"""Independent stdlib audit in Q[t,r,s]/(t^2-5,r^2+3,s^2+11).

Uses no producer imports, norm formula, enumeration loop, or SAT solver.
The physical embedding is t=sqrt5, r=i sqrt3, s=i sqrt11.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

SQUARES=(5,-3,-11)
ZERO=(0,)*8
ONE=(1,0,0,0,0,0,0,0)
TABLE=[]
for i in range(8):
    row=[]
    for j in range(8):
        c=1
        for k,v in enumerate(SQUARES):
            if (i&j)&(1<<k):c*=v
        row.append((i^j,c))
    TABLE.append(row)

def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,c):return tuple(c*a for a in x)
def conjugate(x):return tuple(-a if bool(i&2)^bool(i&4) else a for i,a in enumerate(x))

def multiply(x,y):
    z=[0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:
                    k,c=TABLE[i][j];z[k]+=a*b*c
    return tuple(z)

def power(x,n):
    if n<0:return power(conjugate(x),-n) # Used only for a verified norm-one x.
    z=ONE
    for _ in range(n):z=multiply(z,x)
    return z

def cartesian_key(x):
    a,b,e,f,g,h,mc,md=x
    return a,b,-mc,-md,e,f,g,h

def numerator(x):
    z=scale(x,96)
    if any(F(a).denominator!=1 for a in z):raise ValueError('nonintegral label')
    return tuple(map(int,z))

def geometry():
    # omega=(1+r)/2, v=(r-rs)/6; native directions omega^j v^k.
    omega=(F(1,2),0,F(1,2),0,0,0,0,0)
    v=(0,0,F(1,6),0,0,0,F(-1,6),0)
    rho=(F(7,8),0,0,F(1,8),0,0,0,0)
    if multiply(v,conjugate(v))!=ONE or multiply(rho,conjugate(rho))!=ONE:
        raise ValueError('bad unit rotation')
    if power(omega,6)!=ONE:raise ValueError('bad sixth root')
    directions=set()
    for j,k in product(range(6),range(-2,3)):
        z=multiply(power(omega,j),power(v,k))
        directions.add(numerator(z));directions.add(numerator(multiply(rho,z)))
    steps=sorted(directions,key=cartesian_key)
    u=power(v,2)
    spindle=[ZERO,ONE,omega,plus(ONE,omega),u,multiply(u,omega),multiply(u,plus(ONE,omega))]
    seed=[numerator(z) for z in spindle+[multiply(rho,z) for z in spindle[1:]]]
    if len(steps)!=60 or len(set(seed))!=13:raise ValueError('bad seed/directions')
    target=scale(ONE,96**2)
    for z in steps:
        if multiply(z,conjugate(z))!=target:raise ValueError('nonunit step')
    return steps,seed

def reconstruct(tape,steps,seed):
    pts=list(seed);seen=set(pts)
    for row in tape:
        if not isinstance(row,list) or len(row)!=2:raise ValueError('bad parent-step record')
        parent,step=row
        if type(parent)!=int or type(step)!=int or not(0<=parent<len(pts) and 0<=step<60):
            raise ValueError('out-of-range parent/step')
        z=plus(pts[parent],steps[step])
        if z in seen:raise ValueError('coincident vertices')
        pts.append(z);seen.add(z)
    return pts

def proper(word,n,edges):
    if type(word)!=str or len(word)!=n or set(word)-set('0123'):raise ValueError('bad colour word')
    if any(word[a]==word[b] for a,b in edges):raise ValueError('monochromatic unit edge')

def expect_reject(fn):
    try:fn()
    except ValueError:return 1
    raise ValueError('corruption was accepted')

def check(cert,work=None):
    required={'format':1,'denominator':96,'step_count':60,'seed_vertices':13,
              'vertex_cap':508,'trajectory_cap':4,'query_conflict_cap':100000,
              'trajectory_conflict_cap':500000,'bank_cap':4}
    if any(cert.get(k)!=v for k,v in required.items()) or len(cert['runs'])!=4:
        raise ValueError('wrong pilot parameters')
    steps,seed=geometry();target=scale(ONE,96**2);counts=[];checks=0;controls=0;native_extra=[]
    hashes=[];edge_hashes=[];word_stream='';nonstrict_tests=0
    for ri,row in enumerate(cert['runs']):
        if row['run']!=ri or row['status']!='SAT' or row['vertices']!=508 or len(row['tape'])!=495:
            raise ValueError('wrong candidate record')
        pts=reconstruct(row['tape'],steps,seed)
        if work is not None:
            producer=json.loads((work/f'run{ri}_points.json').read_text())
            if producer!=[list(cartesian_key(x)) for x in pts]:raise ValueError('coordinate decoder disagreement')
        edges=[];extra=0;step_set=set(steps)
        for j in range(508):
            earlier_dictionary_contacts=0
            for i in range(j):
                d=minus(pts[j],pts[i]);norm=multiply(d,conjugate(d));checks+=1
                if any(norm[k] for k in (2,3,4,5)):raise ValueError('norm not physically real')
                if norm==target:
                    edges.append((i,j));extra+=d not in step_set
                    earlier_dictionary_contacts+=d in step_set
                elif norm[0]==96**2:nonstrict_tests+=1
            if j>=13 and earlier_dictionary_contacts<2:
                raise ValueError('growth point has fewer than two dictionary contacts')
        if len(edges)!=row['edges'] or extra!=row['extra_strict_edges']:raise ValueError('strict edge disagreement')
        proper(row['colouring'],508,edges);counts.append(len(edges));native_extra.append(extra)
        # Every ancestor is an induced prefix, so the final word certifies all496 queries.
        if row['queries']!=496:raise ValueError('wrong query count')
        word_stream+=row['colouring']
        hashes.append(hashlib.sha256(json.dumps([list(cartesian_key(x)) for x in pts],separators=(',',':')).encode()).hexdigest())
        edge_hashes.append(hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest())
        corrupted=list(row['colouring']);a,b=edges[0];corrupted[b]=corrupted[a]
        controls+=expect_reject(lambda:proper(''.join(corrupted),508,edges))
        controls+=expect_reject(lambda:reconstruct([[13,0]]+row['tape'][1:],steps,seed))
        controls+=expect_reject(lambda:reconstruct([[0,60]]+row['tape'][1:],steps,seed))
        if ri==0:
            spindle_edges=[(i,j) for i,j in edges if j<7]
            if len(spindle_edges)!=11:raise ValueError('wrong spindle edges')
            good3=sum(all(w[i]!=w[j] for i,j in spindle_edges) for w in product(range(3),repeat=7))
            if good3:raise ValueError('seed is three-colourable')
    # (64+32sqrt5)/96 has norm1+(4/9)sqrt5, so checking only the rational coefficient fails.
    control=(64,32,0,0,0,0,0,0)
    if multiply(control,conjugate(control))!=(9216,4096,0,0,0,0,0,0):
        raise ValueError('irrational norm control failed')
    return {'verified':True,'candidate_count':4,'vertices_each':508,'edge_counts':counts,
            'chromatic_numbers':[4]*4,'all_pair_norm_checks':checks,'unit_edges_checked':sum(counts),
            'unit_edges_outside_step_dictionary':native_extra,'verified_four_colourings':4,
            'certified_induced_prefix_queries':1984,'seed_three_colour_assignments':3**7,
            'seed_proper_three_colourings':0,'rejected_certificate_corruptions':controls,
            'rational_coefficient_only_false_positives':nonstrict_tests,
            'coordinate_sha256':hashes,'edge_sha256':edge_hashes,
            'colour_stream_sha256':hashlib.sha256(word_stream.encode()).hexdigest(),
            'non_four_colourable_signals':0,'whole_family_classified':False,'record_improvement':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,required=True);p.add_argument('--work',type=Path)
    args=p.parse_args();raw=args.certificate.read_bytes()
    result=check(json.loads(raw),args.work)
    result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
