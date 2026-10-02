"""PRIVATE conservative P21 cuts; passing does not assert realization.

Credit Code1 chat1864 for R+|B| crossing. Retain all actual colours.
The max(R,D-I)+|B| strengthening also retains the unit-demand lower
bound on U--C edges. No published finite unit-adjacency guard is enlarged.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import sys
import time

ROOT=Path('round-two/six-code-3')
sys.path.insert(0,str(ROOT/'four_hub_p21_endpoint_cut'))
import cuts

def distinct_neighbor_max(vertices, root):
    row=vertices[root]
    demand=tuple(row['ss_hist'])
    dp={(0,0,0,0,0):0}
    start=time.monotonic();states=0
    for i,other in enumerate(vertices):
        if i==root:continue
        if row['e']==0 and other['eligible']:continue
        if other['e']==0 and row['eligible']:continue
        new=dict(dp)
        for count,value in dp.items():
            for colour in range(5):
                if count[colour]>=demand[colour] or not other['ss_hist'][colour]:continue
                updated=list(count);updated[colour]+=1;updated=tuple(updated)
                new[updated]=max(new.get(updated,-1),value+other['h']-other['k'])
                states+=1
                if states>500000 or time.monotonic()-start>20:
                    raise RuntimeError('INCOMPLETE fixed distinct-neighbor guard')
        dp=new
    return dp.get(demand,-1)

def inspect(vertices):
    for i,row in enumerate(vertices):
        bound=distinct_neighbor_max(vertices,i)
        if bound<0:
            return dict(kind='distinct_weighted_partners',root=i,neighbor_degree_upper=bound)
        if row['k']==0 and bound<13:
            return dict(kind='distinct_radius_bound',root=i,neighbor_degree_upper=bound)
    old=cuts.one_cut(vertices)
    if old['kind']!='UNRESOLVED':return old
    U,A,C,D,I,C1=cuts.endpoints(vertices)
    B={i for i,r in enumerate(vertices) if r['e']>0 and r['eligible']}
    R=sum(vertices[i]['k']==0 for i in U)
    Ctotal=sum(sum(vertices[i]['ss_hist']) for i in C)
    if R and B and Ctotal<max(R,D-I)+len(B):
        return dict(kind='radius_crossing_capacity',R=R,B=len(B),unit_demand=D,
                    internal_upper=I,C1=C1,Ctotal=Ctotal,crossing_lower=max(R,D-I)+len(B))
    return dict(kind='UNRESOLVED',R=R,B=len(B),unit_demand=D,internal_upper=I,C1=C1,Ctotal=Ctotal)

def main():
    data=json.loads((ROOT/'scratch/pass16-p21-producer.json').read_text())
    inventory=data['inventory'];records=[];survivors=[]
    stats=Counter();branchstats={}
    start=time.monotonic()
    for branch in inventory['branches']:
        bkey=tuple(branch[k] for k in ('Q','T','X','tau'))
        counts=Counter()
        for template in branch['templates']:
            if template['failures']:continue
            vertices=cuts.expand(inventory['types'],template['population'])
            if len(vertices)!=14:raise ValueError('actual saturated population size')
            result=inspect(vertices)
            record=dict(branch=list(bkey),population=template['population'],**result)
            records.append(record);stats[result['kind']]+=1;counts[result['kind']]+=1
            if result['kind']=='UNRESOLVED':survivors.append(record)
        if counts:branchstats[str(bkey)]=dict(counts)
    output=dict(agent='six-code-3',role='researcher',status='PRIVATE_P21_NECESSARY_CUTS_ONLY',
                statistics=dict(stats),branch_statistics=branchstats,records=records,survivors=survivors,
                new_pair_total_claim=None,ordinary_bridges_formalized=False,independent_cut_check_pending=True,
                credit_chat1864='Code1 radius crossing R+|B|; own strengthening uses max(R,D-I)+|B|')
    p=ROOT/'scratch/pass16-p21-cuts.json'
    if p.exists():raise ValueError('fresh output')
    p.write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(statistics=dict(stats),branch_statistics=branchstats,elapsed_seconds=time.monotonic()-start),sort_keys=True))

if __name__=='__main__':main()
