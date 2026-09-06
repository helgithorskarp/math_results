#!/usr/bin/env python3
"""Physical complete fixed-word cover for (4,1,2); no profile producer."""
from collections import Counter
from itertools import product
from pathlib import Path
from functools import lru_cache
import copy
import importlib.util

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('physical_attachment_audit',ROOT.parent/'ramsey_r55_order3_eleven_core194_attachments/audit.py')
physical=importlib.util.module_from_spec(spec);spec.loader.exec_module(physical)
need=physical.need


def orbit_map(p,ids):
    physical.check_permutation(p,ids)
    return {x:ids[tuple(sorted((p[u],p[v])))] for (u,v),x in ids.items()}


def transport(units,mapping):
    return {mapping[abs(x)]*(1 if x>0 else -1) for x in units}


def literal_star(word,ids):
    answer=[]
    moving=[0,0,0,0,1,2,2]
    for vertex,t in list(zip(range(12,33,3),moving))+list(zip(range(35,43),word)):
        for endpoint,red in ((33,t!=2),(34,t!=1)):
            answer.append(ids[tuple(sorted((vertex,endpoint)))]*(1 if red else -1))
    return answer


@lru_cache(maxsize=1)
def expected():
    ids=physical.primary();hist=Counter();maps={};raw=0
    for word in product(range(3),repeat=8):
        raw+=1
        red_u=15+sum(t!=2 for t in word)
        red_v=18+sum(t!=1 for t in word)
        if red_u not in range(18,25) or red_v not in range(18,25):continue
        counts=tuple(word.count(t) for t in range(3));hist[counts]+=1
        p=list(range(43));order=sorted(range(8),key=lambda i:word[i])
        for new,old in enumerate(order):p[35+old]=35+new
        key=tuple(p)
        if key not in maps:maps[key]=orbit_map(p,ids)
        need(transport(literal_star(word,ids),maps[key])==set(literal_star(sorted(word),ids)),
             'actual complete star transport under fixed sorting')
        need(p[:35]==list(range(35)),'all moving vertices and ordered pair fixed')
    need(raw==6561 and sum(hist.values())==5253 and len(hist)==27,'complete fixed-word census')
    rows=[]
    for (x,y,z),weight in sorted(hist.items()):
        counts=[4,1,2,x,y,z];units=physical.normalized_units(counts,True)
        need(units==literal_star([0]*x+[1]*y+[2]*z,ids),'thirty physical normalized units')
        rows.append(dict(counts=counts,red_degrees=[15+x+y,18+x+z],
            labeled_assignments=210*weight,units=units))
    need(sum(r['labeled_assignments'] for r in rows)==1103130,'complete labeled star weight')
    return rows,dict(fixed_words=raw,allowed_fixed_words=sum(hist.values()),normalized_profiles=len(rows),
        distinct_sorting_permutations=len(maps),physical_units_checked=810,
        labeled_full_star_weight=1103130,endpoint_swaps_used=0)


def base_symmetries(base):
    ids=physical.primary()
    with base.open() as stream:
        need(stream.readline()=='p cnf 320 366069\n','complete base header')
        clauses={tuple(sorted(map(int,line.split()[:-1]))) for line in stream}
    need(len(clauses)==366069,'complete distinct base clauses')
    moving=physical.normalized_units((4,1,2));checked=[]
    for f in range(35,42):
        p=list(range(43));p[f],p[f+1]=f+1,f;mapping=orbit_map(p,ids)
        for clause in clauses:
            need(tuple(sorted(transport(clause,mapping))) in clauses,'complete base clause symmetry')
        need(transport(moving,mapping)==set(moving),'fixed sorting preserves moving units')
        checked.append('fixed_%d_%d'%(f,f+1))
    return dict(complete_base_clauses=366069,generators=checked,clause_images_checked=366069*7)


def verify(rows,wanted):
    need(rows==wanted,'complete entrywise physical twenty-seven-profile certificate')


def controls(rows,wanted):
    rejected=[]
    for name in ('missing_profile','duplicate_profile','wrong_fixed_count','wrong_moving_count',
                 'wrong_degree','wrong_weight','wrong_fixed_unit','wrong_moving_unit'):
        bad=copy.deepcopy(rows)
        if name=='missing_profile':bad.pop()
        elif name=='duplicate_profile':bad.append(copy.deepcopy(bad[0]))
        elif name=='wrong_fixed_count':bad[0]['counts'][3]+=1
        elif name=='wrong_moving_count':bad[0]['counts'][0]-=1
        elif name=='wrong_degree':bad[0]['red_degrees'][0]-=1
        elif name=='wrong_weight':bad[0]['labeled_assignments']+=1
        elif name=='wrong_fixed_unit':bad[0]['units'][-1]*=-1
        elif name=='wrong_moving_unit':bad[0]['units'][0]*=-1
        try:verify(bad,wanted)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    return rejected
