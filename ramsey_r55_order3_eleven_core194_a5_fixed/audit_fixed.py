#!/usr/bin/env python3
"""Physical full-word and coupled-permutation audit; no profile producer."""
from collections import Counter
from itertools import product
from pathlib import Path
from functools import lru_cache
import copy
import importlib.util

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('physical_attachment_audit', ROOT.parent / 'ramsey_r55_order3_eleven_core194_attachments/audit.py')
physical = importlib.util.module_from_spec(spec); spec.loader.exec_module(physical)
need = physical.need
TYPES = ((5,0,2), (5,1,1))


def coupled_swap():
    p = list(range(43)); p[33],p[34] = 34,33
    for s in range(3): p[27+s],p[30+s] = 30+s,27+s
    return p


def orbit_map(p, ids):
    physical.check_permutation(p, ids)
    answer = {}
    for (u,v), x in ids.items():
        y = ids[tuple(sorted((p[u],p[v])))]; answer[x] = y
    return answer


def transport(units, mapping):
    return {mapping[abs(x)] * (1 if x>0 else -1) for x in units}


def literal_star(abc, word, ids):
    types = [0]*abc[0] + [1]*abc[1] + [2]*abc[2]
    answer = []
    for vertex,t in list(zip(range(12,33,3),types)) + list(zip(range(35,43),word)):
        for endpoint, red in ((33,t!=2),(34,t!=1)):
            answer.append(ids[tuple(sorted((vertex,endpoint)))] * (1 if red else -1))
    return answer


@lru_cache(maxsize=1)
def expected():
    ids = physical.primary(); rows=[]; censuses=[]
    for abc in TYPES:
        hist=Counter(); permutations=set(); maps={}; swapped=0; allowed=0
        for word in product(range(3), repeat=8):
            a,b,c = abc
            red_u = 3*(a+b) + sum(t!=2 for t in word)
            red_v = 3*(a+c) + sum(t!=1 for t in word)
            if red_u not in range(18,25) or red_v not in range(18,25): continue
            allowed += 1; p=list(range(43)); oriented=word
            if b==c and word.count(1)>word.count(2):
                p=coupled_swap(); oriented=tuple(0 if t==0 else 3-t for t in word)
                swapped += 1
            order=sorted(range(8), key=lambda i:oriented[i])
            for new,old in enumerate(order): p[35+old]=35+new
            key=tuple(p)
            if key not in maps: maps[key]=orbit_map(p,ids)
            permutations.add(key)
            counts=abc+tuple(oriented.count(t) for t in range(3)); hist[counts]+=1
            wanted=literal_star(abc, sorted(oriented), ids)
            need(transport(literal_star(abc,word,ids),maps[key])==set(wanted),
                 'actual full-star transport under coupled normalization')
            # In particular, the already fixed moving assignment is preserved.
            need(transport(literal_star(abc,word,ids)[:14],maps[key])==set(wanted[:14]),
                 'moving normalization preserved')
        # 21 moving placements times two orientations for (5,0,2).
        # 42 moving placements for (5,1,1); hist already merges endpoint orientations.
        for counts,weight in sorted(hist.items()):
            a,b,c,x,y,z=counts
            units=physical.normalized_units(counts,True)
            need(units==literal_star(abc,[0]*x+[1]*y+[2]*z,ids),'physical normalized unit meanings')
            rows.append(dict(counts=list(counts),red_degrees=[3*(a+b)+x+y,3*(a+c)+x+z],
                             labeled_assignments=42*weight,units=units))
        need(len(hist)==(10 if abc==(5,0,2) else 9),'complete profile number')
        censuses.append(dict(moving_counts=list(abc),fixed_words=6561,allowed_fixed_words=allowed,
            normalized_profiles=len(hist),coupled_swaps=swapped,
            distinct_normalizing_permutations=len(permutations),labeled_full_star_weight=42*allowed))
    # An endpoint-only swap is a bijection of the base but NOT of the moving child.
    bad=list(range(43));bad[33],bad[34]=34,33
    units=physical.normalized_units((5,1,1))
    need(transport(units,orbit_map(bad,ids))!=set(units),'endpoint-only normalization rejected')
    need(len(rows)==19 and sum(r['labeled_assignments'] for r in rows)==195342,'nineteen-profile star weight')
    return rows,dict(types=censuses,physical_units_checked=570,
        normalized_profiles=19,labeled_full_star_weight=195342,endpoint_only_swap_rejected=True)


def base_symmetries(base):
    """Check every complete clause under generators for all normalization maps."""
    ids=physical.primary(); generators=[('coupled_endpoint_triangle_swap',coupled_swap())]
    for f in range(35,42):
        p=list(range(43));p[f],p[f+1]=f+1,f;generators.append(('fixed_%d_%d'%(f,f+1),p))
    with base.open() as stream:
        need(stream.readline()=='p cnf 320 366069\n','complete base header')
        clauses={tuple(sorted(map(int,line.split()[:-1]))) for line in stream}
    need(len(clauses)==366069,'complete distinct base clauses')
    checked=[]
    for name,p in generators:
        mapping=orbit_map(p,ids)
        for clause in clauses:
            need(tuple(sorted(transport(clause,mapping))) in clauses,'complete base clause symmetry '+name)
        moving=(physical.normalized_units((5,1,1)),) if name.startswith('coupled') else tuple(physical.normalized_units(t) for t in TYPES)
        for units in moving: need(transport(units,mapping)==set(units),'generator preserves moving child')
        checked.append(name)
    return dict(complete_base_clauses=366069,generators=checked,clause_images_checked=366069*len(checked))


def verify(rows,wanted):
    need(rows==wanted,'complete entrywise physical nineteen-profile certificate')


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
