#!/usr/bin/env python3
"""Exact local path/triple proposal, not a global exclusion by itself."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

Q=103
SEED=(0,1,2,3,4)
A=(101,102,5,6)
B=(52,53,54,55)
SATELLITES=A+B
EDGES=((101,102),(102,5),(5,6))
TRIPLES=((52,53,54),(53,54,55))

def need(condition,message):
    if not condition:raise ValueError(message)

def reflected(values):return tuple(sorted((4-x)%Q for x in values))

def valid(values,holes):
    for edge in EDGES:
        if not holes.intersection(edge) and not any(values[x] for x in edge):return False
    for triple in TRIPLES:
        if not holes.intersection(triple) and len({values[x] for x in triple})==1:return False
    return True

def polynomial(points,holes,predicate):
    regular=[x for x in points if x not in holes];counts=[0]*(len(regular)+1)
    for bits in itertools.product((0,1),repeat=len(regular)):
        if predicate(dict(zip(regular,bits))):counts[sum(bits)]+=1
    return counts

def profile(holes):
    holes=set(holes)
    pa=polynomial(A,holes,lambda v:all(holes.intersection(e) or any(v[x] for x in e) for e in EDGES))
    pb=polynomial(B,holes,lambda v:all(holes.intersection(t) or len({v[x] for x in t})==2 for t in TRIPLES))
    total=[0]*(len(pa)+len(pb)-1)
    for i,a in enumerate(pa):
        for j,b in enumerate(pb):total[i+j]+=a*b
    return {'holes':sorted(holes),'path_polynomial':pa,'triple_polynomial':pb,'other_color_polynomial':total,
            'accepted':sum(total),'minimum_other_color':next(i for i,v in enumerate(total) if v),
            'minimum_seed_color_on_B':next(i for i,v in enumerate(pb) if v),
            'outside_hole_completions':math.comb(90,3-len(holes))}

def generate():
    profiles=[];zero=[];raw_histogram={i:0 for i in range(4)};inputs=accepted=0;owner={}
    for h in range(4):
        for holes in itertools.combinations(sorted(SATELLITES),h):
            p=profile(holes);profiles.append(p)
            inputs+=2**(8-h);accepted+=p['accepted']
            raw_histogram[p['minimum_other_color']]+=p['outside_hole_completions']
            if p['minimum_other_color']==0:
                need(h==3,'Unexpected local zero-color geography')
                zero.append(holes)
            key=min(holes,reflected(holes));owner[holes]=key
    classes=sorted(set(owner.values()))
    zero_classes=sorted({min(h,reflected(h)) for h in zero})
    need(len(profiles)==93 and len(classes)==49,'Unexpected local hole quotient')
    need(sum(raw_histogram.values())==math.comb(98,3),'Raw seed-disjoint hole cover mismatch')
    return {'agent':'six-vdw-3','role':'researcher','q':Q,'seed':list(SEED),'satellite_order':list(SATELLITES),
            'profiles':profiles,'profile_classes':list(map(list,classes)),
            'raw_seed_disjoint_hole_triples':math.comb(98,3),'raw_minimum_other_color_histogram':raw_histogram,
            'zero_other_color_hole_triples':list(map(list,zero)),'zero_other_color_reflection_classes':list(map(list,zero_classes)),
            'local_inputs':inputs,'local_accepted':accepted,
            'zero_hole_polynomial':profile(())['other_color_polynomial'],
            'local_five_constraints_only':True,'global_satellite_growth_proved':False,
            'W_bound_improved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=generate();a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('profiles','profile_classes')}))
