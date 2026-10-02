"""PRIVATE exact necessary unit graphs; guard stays <=15 edges/10s.

At tau=0 a center needs h-1-q nonedges among its saturated high
neighbors. An internal unit graph already gives some neighbor-pair
edges. Cross-unit endpoint demands are checked against all Hall subsets,
including forced external edges. Passing remains a necessary relaxation.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import sys
import time

ROOT=Path('round-two/six-code-3')
sys.path.insert(0,str(ROOT/'four_hub_p21_endpoint_cut'))
sys.path.insert(0,str(ROOT/'scratch'))
import cuts
import importlib.util
spec=importlib.util.spec_from_file_location('forced',ROOT/'scratch/pass16-p21-forced.py')
forced_engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(forced_engine)

def audit(vertices,branch):
    domains,forced,failure=forced_engine.propagate(vertices)
    if failure:raise ValueError('input is not surviving propagation')
    U,A,C,D,I,C1=cuts.endpoints(vertices)
    unitlist=sorted(U);clist=sorted(C)
    edges=[(i,j) for i,j in itertools.combinations(unitlist,2) if 0 in domains[(i,j)]]
    if len(edges)>15:raise RuntimeError('INCOMPLETE published finite unit-edge scope; no absence')
    mandatory={pair for pair,col in forced.items() if col==0 and set(pair)<=U}
    mandatory_mask=sum(1<<i for i,p in enumerate(edges) if p in mandatory)
    demands=[sum(vertices[i]['ss_hist']) for i in unitlist]
    cross_forced={(u,c) for u in unitlist for c in clist if forced.get(tuple(sorted((u,c))))==0}
    cross_pool={(u,c) for u in unitlist for c in clist
                if (u,c) not in cross_forced and tuple(sorted((u,c))) not in forced
                and 0 in domains[tuple(sorted((u,c)))]}
    caps=[vertices[c]['ss_hist'][0]-sum(c in pair for pair,col in forced.items()
             if col==0 and not (set(pair)&U)) - sum(y==c for x,y in cross_forced) for c in clist]
    if min(caps,default=0)<0:raise ValueError('negative C residual capacity')
    started=time.monotonic();checks=Counter();accepted=[]
    for mask in range(1<<len(edges)):
        if time.monotonic()-started>10:raise RuntimeError('INCOMPLETE fixed unit graph10sec guard')
        checks['whole_masks']+=1
        if mask&mandatory_mask!=mandatory_mask:
            checks['missing_forced_edge']+=1;continue
        neighbors={u:set() for u in unitlist}
        for i,(u,v) in enumerate(edges):
            if mask>>i&1:neighbors[u].add(v);neighbors[v].add(u)
        debt=[demands[j]-len(neighbors[u])-sum(x==u for x,y in cross_forced) for j,u in enumerate(unitlist)]
        if any(d<0 or d>sum(x==u for x,y in cross_pool) for u,d in zip(unitlist,debt)):
            checks['unit_degree_capacity']+=1;continue
        if sum(debt)>sum(caps):checks['aggregate_C_capacity']+=1;continue
        if branch[3]==0 and any(sum(v in neighbors[w] for v,w in itertools.combinations(neighbors[u],2))
                               > demands[j]*(demands[j]-1)//2-(4-vertices[u]['q'])
                               for j,u in enumerate(unitlist)):
            checks['unit_uncovered_triangle']+=1;continue
        bad=False
        for subset in range(1<<len(unitlist)):
            J={u for j,u in enumerate(unitlist) if subset>>j&1}
            needed=sum(debt[j] for j,u in enumerate(unitlist) if u in J)
            upper=sum(min(caps[j],sum((u,c) in cross_pool for u in J)) for j,c in enumerate(clist))
            if needed>upper:bad=True;break
        if bad:checks['cross_Hall_capacity']+=1;continue
        checks['necessary_unit_graphs']+=1;accepted.append(mask)
    return dict(kind='unit_graph_INCOMPATIBLE' if not accepted else 'UNRESOLVED',
                units=unitlist,potential_internal_edges=[list(e) for e in edges],
                checks=dict(checks),accepted_internal_masks=accepted,elapsed_seconds=time.monotonic()-started)

def main():
    inv=json.loads((ROOT/'scratch/pass16-p21-producer.json').read_text())['inventory']
    previous=json.loads((ROOT/'scratch/pass16-p21-forced.json').read_text())['survivors']
    records=[];stats=Counter()
    for record in previous:
        result=audit(cuts.expand(inv['types'],record['population']),record['branch'])
        stats[result['kind']]+=1
        records.append(dict(ordinal=record['ordinal'],branch=record['branch'],population=record['population'],**result))
    output=dict(agent='six-code-3',role='researcher',status='PRIVATE_P21_COMPLETE_UNIT_RELAXATION',statistics=dict(stats),records=records,
                survivors=[r for r in records if r['kind']=='UNRESOLVED'],independent_check_pending=True,new_pair_total_claim=None)
    out=ROOT/'scratch/pass16-p21-unit-graphs.json'
    if out.exists():raise ValueError('fresh output')
    out.write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(statistics=dict(stats),branches=[dict(ordinal=r['ordinal'],kind=r['kind'],checks=r['checks'],elapsed_seconds=r['elapsed_seconds']) for r in records]),sort_keys=True))

if __name__=='__main__':main()
