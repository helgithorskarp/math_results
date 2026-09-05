#!/usr/bin/env python3
"""Exact colored-five-set inequalities and edge-capacity certificate checker."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'ramsey_r55_visible_obstruction_cover/verify.py'
PARENT_SHA='f2bc76860be8b2d1c1086e070a6800dc8fdd25d0367ea03b94830eac688b1b3f'

def require(ok,message):
    if not ok:raise ValueError(message)

def integer(x):return type(x) is int

def digest(x):
    return hashlib.sha256((json.dumps(x,separators=(',',':'))+'\n').encode()).hexdigest()

def parent():
    require(hashlib.sha256(PARENT.read_bytes()).hexdigest()==PARENT_SHA,'parent checker changed')
    spec=importlib.util.spec_from_file_location('literal_cover_checker',PARENT)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def color_row(seed,red,five):
    """At least one opposite-colored edge: sum c_e x_e >= b.

    Literal x_e is satisfied on a flip when the old edge matches the forbidden
    color; literal 1-x_e is satisfied otherwise. Fixed edges must all match.
    """
    row={};b=1
    for u,v in combinations(five,2):
        old=(v in seed[u])
        if u<3:
            require(old==bool(red),'fixed edge already blocks forbidden color')
        elif old==bool(red):
            row[u,v]=1
        else:
            row[u,v]=-1;b-=1
    return row,b

def decode_five(entry,mixed):
    require(type(entry) is list and len(entry)==3,'weighted five-set row')
    red,five,weight=entry
    require(integer(red) and red in (0,1),'five-set color')
    require(type(five) is list and len(five)==5 and all(integer(v) for v in five)
            and five==sorted(set(five)) and 0<=five[0]<five[-1]<43,'five-set vertices')
    require((five[0]<3)==mixed,'old/mixed five-set category')
    require(integer(weight) and weight>0,'five-set weight')
    return red,tuple(five),weight

def verify_certificate(seed,certificate,base):
    require(type(certificate) is dict and set(certificate)=={'format','seed_sha256','denominator','old_cliques',
            'mixed_cliques','degrees','profiles','upper_penalties'},'certificate schema')
    require(certificate['format']=='r55-creation-sensitive-cover-dual-v1'
            and certificate['seed_sha256']==base.SEED_SHA,'certificate provenance')
    D=certificate['denominator'];require(integer(D) and D>0,'denominator')
    load={e:0 for e in base.EDGES};old_sum=0;mixed_sum=0
    seen=set();holes=Counter();weighted_holes=Counter();origins=[]
    for mixed,name in ((False,'old_cliques'),(True,'mixed_cliques')):
        for entry in certificate[name]:
            red,five,w=decode_five(entry,mixed)
            require((red,five) not in seen,'duplicate five-set');seen.add((red,five))
            row,b=color_row(seed,red,five)
            if not mixed:
                require(b==1,'old row is not an original colored K5');old_sum+=w*b
            else:
                require(b<=0,'seed has mixed K5')
                mixed_sum+=w*b;holes[1-b]+=1;weighted_holes[1-b]+=w
            for e,c in row.items():load[e]+=w*c
            origins.append([red,list(five),w,b])
    degrees={}
    for entry in certificate['degrees']:
        require(type(entry) is list and len(entry)==2,'degree row')
        u,b=entry
        require(integer(u) and 3<=u<43 and integer(b) and b!=0 and u not in degrees,'degree multiplier')
        degrees[u]=b
    profiles={}
    for entry in certificate['profiles']:
        require(type(entry) is list and len(entry)==3,'profile row')
        u,red,b=entry
        require(integer(u) and 0<=u<3 and integer(red) and red in (0,1) and integer(b) and b!=0
                and (u,red) not in profiles,'profile multiplier')
        profiles[u,red]=b
    for u,v in base.EDGES:
        sign=1 if v not in seed[u] else -1
        charge=degrees.get(u,0)+degrees.get(v,0)
        for (root,red),w in profiles.items():
            if (u in seed[root])==bool(red) and (v in seed[root])==bool(red):charge+=w
        load[u,v]+=sign*charge
    penalties={}
    for entry in certificate['upper_penalties']:
        require(type(entry) is list and len(entry)==3,'box row')
        u,v,p=entry
        require(integer(u) and integer(v) and (u,v) in load and integer(p) and p>0 and (u,v) not in penalties,'box penalty')
        penalties[u,v]=p
    visible=base.visible_edges(seed)
    residual=[D*int(e in visible)-load[e]+penalties.get(e,0) for e in base.EDGES]
    require(min(residual)>=0,'overloaded edge')
    numerator=old_sum+mixed_sum-sum(penalties.values())
    require(numerator>38*D,'certificate does not exclude budget 38')
    bound=Fraction(numerator,D)
    return {'exact_bound':[bound.numerator,bound.denominator],'integer_lower_bound':-(-numerator//D),
            'scale':D,'old_clique_weight_sum':old_sum,'mixed_weighted_rhs':mixed_sum,
            'box_penalty_sum':sum(penalties.values()),'corrected_numerator':numerator,
            'old_clique_rows':len(certificate['old_cliques']),'mixed_clique_rows':len(certificate['mixed_cliques']),
            'degree_rows':len(degrees),'profile_rows':len(profiles),'box_rows':len(penalties),
            'selected_mixed_hole_histogram':dict(sorted(holes.items())),
            'selected_mixed_weight_by_holes':dict(sorted(weighted_holes.items())),
            'minimum_edge_residual':min(residual),'maximum_edge_residual':max(residual),
            'edge_residual_sha256':digest(residual),'weighted_row_origins_sha256':digest(origins)}

def encoding_audit(seed,old_fives,discovery,base):
    # Every mixed five-set is visited literally, independently of producer's
    # exceptional-root / color-neighborhood enumeration and duplicate removal.
    edges=base.EDGES;ix={e:i for i,e in enumerate(edges)}
    mixed=[];examined=0
    for five in combinations(range(43),5):
        if five[0]>=3:continue
        examined+=1
        fixed=[(u,v) for u,v in combinations(five,2) if u<3]
        for red in (0,1):
            if any((v in seed[u])!=bool(red) for u,v in fixed):continue
            row,b=color_row(seed,red,five)
            mixed.append([red,list(five),[[ix[e],-c] for e,c in sorted(row.items())],-b])
    mixed.sort(key=lambda x:(x[0],x[1]))
    old=[]
    for red,fives in zip((1,0),old_fives):
        for five in fives:old.append([[[ix[e],-1] for e in combinations(five,2)],-1])
    rows=old+[[entry[2],entry[3]] for entry in mixed]
    equalities=[]
    for u in range(3,43):
        equalities.append([[i,1 if v not in seed[w] else -1] for i,(w,v) in enumerate(edges) if u in (w,v)])
    for root in range(3):
        for red in (1,0):
            equalities.append([[i,1 if v not in seed[u] else -1] for i,(u,v) in enumerate(edges)
                               if (u in seed[root])==bool(red) and (v in seed[root])==bool(red)])
    calculated={'mixed_rows_sha256':digest(mixed),'inequality_rows_sha256':digest(rows),
                'equality_rows_sha256':digest(equalities)}
    for key,value in calculated.items():require(discovery[key]==value,'encoding mismatch: '+key)
    require(discovery['pointwise_rows']==0,'unadvertised pointwise rows')
    require(discovery['old_cover_rows']==len(old) and discovery['mixed_rows']==len(mixed)
            and discovery['equality_rows']==len(equalities) and discovery['primary_variables']==780,'encoding counts')
    return {**calculated,'literal_mixed_five_sets_visited':examined,'old_rows':len(old),'mixed_rows':len(mixed),
            'mixed_width_histogram':dict(sorted(Counter(len(row[2]) for row in mixed).items())),
            'equalities':len(equalities),'pointwise_rows':0}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    ap.add_argument('--discovery',type=Path,default=HERE/'discovery.json')
    ap.add_argument('--report',type=Path,required=True);args=ap.parse_args()
    base=parent();require(hashlib.sha256(base.SEED.read_bytes()).hexdigest()==base.SEED_SHA,'seed hash')
    seed=base.decode(json.loads(base.SEED.read_text()));old=base.check_seed(seed)
    certificate=json.loads(args.certificate.read_text());discovery=json.loads(args.discovery.read_text())
    result={'status':'VERIFIED_CREATION_SENSITIVE_LOWER_BOUND','seed_sha256':base.SEED_SHA,
            'certificate':verify_certificate(seed,certificate,base),'encoding':encoding_audit(seed,old,discovery,base),
            'scope':'Fixed E incidences, individual degrees and E profiles; all old K5s destroyed and all mixed K5s forbidden. No pointwise rows or central caps used; no feasibility above the bound claimed.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
