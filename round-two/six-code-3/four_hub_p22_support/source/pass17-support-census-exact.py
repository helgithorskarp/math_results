"""Exact necessary ordered hub support census, with fixed state/time guards.

At hub a HIGH at saturated s, its 1+3*delta_sa leave neighbors consist
of HH leaves, at most q_s HIGH-SAT leaves, and LOW-SAT leave friends.
Those LOW-SAT friends are distinct positive-deficit centers for a, other
than s. Thus N_a >= 2+3*delta_sa-HH_leave_degree_s(a)-q_s.
For each physical signature only the lower bound is used, not a guessed
actual LOW-friend count. Quota-compatible rows are necessary, not packings.
"""
import collections
import hashlib
import itertools
import json
import time
from pathlib import Path

S=Path('round-two/six-code-3/scratch')
R=Path('round-two/six-code-3/four_hub_p21_endpoint_cut')
PAIR=list(itertools.combinations(range(4),2))
TRIPLE=list(itertools.combinations(range(4),3))
STATE_CAP=500000
TIME_CAP=20

def need(c,m):
    if not c: raise ValueError(m)

def count_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for x in range(total+1):
        for tail in count_compositions(total-x,parts-1):
            yield (x,)+tail

def lambda_vectors(T,triple):
    # Exact small scalar carrier, no light-role symmetry reduction.
    for values in itertools.product(range(6),repeat=6):
        if sum(values)!=21: continue
        leave=tuple(14+int(set(p)<=set(triple))-3*l for p,l in zip(PAIR,values))
        if min(leave)<0 or max(leave)>14: continue
        D=tuple(sum(l for p,l in zip(PAIR,values) if a in p)-(2 if a==0 else 6) for a in range(4))
        if min(D)<0: continue
        yield values,D,leave

def options(catalogue,type_id,triple,leave):
    triple_mask=(1<<TRIPLE.index(triple)) if triple else 0
    grouped={}
    q=types[type_id]['q']
    for index,r in enumerate(catalogue):
        if r['type_id']!=type_id or r['HHH_covered_mask'] not in (0,triple_mask): continue
        # A zero total quota forbids every local leave in that coordinate.
        if any(r['HH_leave_mask']>>i&1 and not leave[i] for i in range(6)): continue
        d=tuple(r['hub_deficits'])
        lb=tuple(2+3*d[a]-sum(r['HH_leave_mask']>>i&1 for i,p in enumerate(PAIR) if a in p)-q
                 if d[a] else 0 for a in range(4))
        key=(d,lb)
        if key not in grouped:grouped[key]=index
    # Only coordinatewise nondominated lower bounds matter to this
    # necessary existence relaxation. A removed pattern is replaced by
    # an ACTUAL retained same-delta pattern with no larger requirement.
    keys=sorted(grouped)
    return [k for k in keys if not any(j[0]==k[0] and j[1]!=k[1] and
            all(a<=b for a,b in zip(j[1],k[1])) for j in keys)]

def census(population,T,catalogue):
    start=time.monotonic(); visited=0; tested_lambdas=0; leaves=[]
    # Extend records one center at a time. State holds (D4,N4,max_required_N4).
    # Same type has a sorted pattern index to remove repeated-row order only.
    for triple in (TRIPLE if T else [()]):
        for lam,target,pairleave in lambda_vectors(T,triple):
            # All six permutations of identical light hub roles are
            # bijections. Retain the lexical minimum of the joint
            # (covered triple,lambda6) orbit, not of either alone.
            orbit=[]
            for lights in itertools.permutations((1,2,3)):
                p=(0,)+lights
                inverse=tuple(p.index(a) for a in range(4))
                tri=tuple(sorted(inverse[a] for a in triple))
                l=tuple(lam[PAIR.index(tuple(sorted((p[a],p[b]))))] for a,b in PAIR)
                orbit.append((tri,l))
            if (tuple(triple),tuple(lam)) != min(orbit): continue
            tested_lambdas+=1
            groups=[]
            for type_id,n in population:
                opts=options(catalogue,type_id,triple,pairleave)
                groups.append((type_id,n,opts))
            groups.sort(key=lambda g:len(g[2]))
            current={(0,)*12}
            for type_id,n,opts in groups:
                nxt=set()
                # Aggregate a repeated type by all weak compositions of its
                # ordered d4/support-lower-bound signatures. Keep only distinct
                # group states; time/state guard never implies absence.
                local={(0,)*12}
                for _ in range(n):
                    new=set()
                    for state in local:
                        for d,lb in opts:
                            dd=tuple(state[a]+d[a] for a in range(4))
                            if any(dd[a]>target[a] for a in range(4)):continue
                            nn=tuple(state[4+a]+int(d[a]>0) for a in range(4))
                            req=tuple(max(state[8+a],lb[a]) for a in range(4))
                            if any(req[a]>target[a] for a in range(4)):continue
                            new.add(dd+nn+req);visited+=1
                            if visited>STATE_CAP or time.monotonic()-start>TIME_CAP:
                                return dict(status='INCOMPLETE_SUPPORT_CENSUS',visited=visited,tested_lambdas=tested_lambdas,
                                            surviving_ordered_states=leaves)
                    local=new
                for x,y in itertools.product(current,local):
                    dd=tuple(x[a]+y[a] for a in range(4))
                    if any(dd[a]>target[a] for a in range(4)):continue
                    nn=tuple(x[4+a]+y[4+a] for a in range(4))
                    req=tuple(max(x[8+a],y[8+a]) for a in range(4))
                    nxt.add(dd+nn+req);visited+=1
                    if visited>STATE_CAP or time.monotonic()-start>TIME_CAP:
                        return dict(status='INCOMPLETE_SUPPORT_CENSUS',visited=visited,tested_lambdas=tested_lambdas,
                                    surviving_ordered_states=leaves)
                current=nxt
            valid=sorted(x for x in current if x[:4]==target and all(x[4+a]>=x[8+a] for a in range(4)))
            if valid:
                leaves.append(dict(triple=list(triple),pair_replications=list(lam),hub_deficit_totals=list(target),states=valid))
    return dict(status='COMPLETE_SUPPORT_CENSUS',visited=visited,tested_lambdas=tested_lambdas,
                surviving_ordered_states=leaves,elapsed_seconds=time.monotonic()-start)

types=json.loads((R/'expected.json').read_text())['types']

def main():
    catalogue=json.loads((S/'pass16-hub-role-catalogue.json').read_text())['records']
    populations=json.loads((S/'pass16-p21-unit-graphs.json').read_text())['survivors']
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_EXACT_PARETO_SUPPORT_CENSUS',records=[],
                state_cap_per_population=STATE_CAP,time_cap_per_population=TIME_CAP,
                q_degree_upper_bound_not_equality=True,global_frequency_caps=False,new_pair_total_claim=None)
    out=S/'pass17-support-census-exact.json';need(not out.exists(),'fresh support output')
    for r in populations:
        c=census(r['population'],r['branch'][1],catalogue)
        c.update(ordinal=r['ordinal'],population=r['population'],branch=r['branch'])
        result['records'].append(c)
        out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps({k:v for k,v in c.items() if k!='surviving_ordered_states'}|dict(surviving_lambda_states=len(c['surviving_ordered_states'])),sort_keys=True),flush=True)

if __name__=='__main__':main()
