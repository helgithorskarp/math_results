"""PRIVATE deterministic coloured-edge propagation and physical walk cuts.

No graph search and no support realization claim. Triangle/collision losses
credit exact radius identity of independent REVIEW9451. A physical SS-high
leave pair at s belongs to an uncovered saturated triple; if tau=0 its
endpoints cannot be adjacent in the saturated deficit graph.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import sys

ROOT=Path('round-two/six-code-3')
sys.path.insert(0,str(ROOT/'four_hub_p21_endpoint_cut'))
import cuts

def propagate(vertices):
    n=len(vertices)
    U,A,C,D,I,C1=cuts.endpoints(vertices)
    domains={(i,j):set(cuts.potential_colours(vertices,i,j,U,C,D==I+C1))
             for i,j in itertools.combinations(range(n),2)}
    required=[[int(c) for c in r['ss_hist']] for r in vertices]
    forced={};trace=[]
    while True:
        changed=False
        for i in range(n):
            for colour in range(5):
                used=sum(c==colour for pair,c in forced.items() if i in pair)
                debt=required[i][colour]-used
                pairs=[pair for pair,values in domains.items() if pair not in forced and i in pair and colour in values]
                if debt<0 or len(pairs)<debt:
                    return domains,forced,dict(kind='forced_color_degree_failure',point=i,colour=colour,debt=debt,available=len(pairs),trace=trace)
                if debt==0:
                    for pair in pairs:
                        domains[pair].remove(colour);changed=True
                        trace.append(['remove',list(pair),colour,i])
                elif len(pairs)==debt:
                    for pair in pairs:
                        forced[pair]=colour;domains[pair]={colour};changed=True
                        trace.append(['force',list(pair),colour,i])
        if not changed:break
    return domains,forced,None

def potential_neighbors(domains,root):
    return {j if i==root else i for (i,j),values in domains.items() if values and root in (i,j)}

def max_neighbor_degrees(vertices,root,domains,forced):
    demand=list(vertices[root]['ss_hist']);base=0
    for (i,j),colour in forced.items():
        if root not in (i,j):continue
        other=j if i==root else i
        demand[colour]-=1;base+=vertices[other]['h']-vertices[other]['k']
    dp={tuple(0 for _ in range(5)):base}
    for other in range(len(vertices)):
        if other==root:continue
        pair=tuple(sorted((root,other)))
        if pair in forced:continue
        values=domains[pair]
        new=dict(dp)
        for counts,total in dp.items():
            for colour in values:
                if counts[colour]>=demand[colour]:continue
                updated=list(counts);updated[colour]+=1;updated=tuple(updated)
                new[updated]=max(new.get(updated,-1),total+vertices[other]['h']-vertices[other]['k'])
        dp=new
    return dp.get(tuple(demand),-1)

def inspect(vertices,branch):
    domains,forced,failure=propagate(vertices)
    if failure:return failure
    n=len(vertices)
    for colour in range(5):
        unused=set(i for i,r in enumerate(vertices) if r['ss_hist'][colour])
        while unused:
            component={min(unused)};todo=list(component)
            while todo:
                i=todo.pop()
                for j in list(unused-component):
                    if colour in domains[tuple(sorted((i,j)))]:
                        component.add(j);todo.append(j)
            unused-=component
            degree=sum(vertices[i]['ss_hist'][colour] for i in component)
            if degree%2:
                return dict(kind='closed_color_parity',colour=colour,component=sorted(component),degree=degree)
    for root,row in enumerate(vertices):
        neighbors={j if i==root else i for (i,j) in forced if root in (i,j)}
        triangles=sum(tuple(sorted((i,j))) in forced for i,j in itertools.combinations(neighbors,2))
        if branch[3]==0:
            demanded=row['h']-1-row['q']
            degree=row['h']-row['k']
            if triangles > degree*(degree-1)//2-demanded:
                return dict(kind='forced_uncovered_triangle',root=root,forced_triangles=triangles,
                            SS_high_leave=demanded,saturated_degree=degree)
        if row['k']:continue
        possible=potential_neighbors(domains,root)
        collision=sum(max(0,sum(tuple(sorted((w,v))) in forced for v in neighbors)-1)
                      for w in set(range(n))-{root}-possible)
        upper=max_neighbor_degrees(vertices,root,domains,forced)
        if upper<13+2*triangles+collision:
            return dict(kind='forced_radius_losses',root=root,neighbor_degree_upper=upper,
                        forced_triangles=triangles,forced_collision=collision)
    return dict(kind='UNRESOLVED',forced_edges=[[list(pair),c] for pair,c in sorted(forced.items())])

def main():
    inv=json.loads((ROOT/'scratch/pass16-p21-producer.json').read_text())['inventory']
    previous=json.loads((ROOT/'scratch/pass16-p21-cuts.json').read_text())['survivors']
    records=[];counts=Counter()
    for ordinal,record in enumerate(previous):
        vertices=cuts.expand(inv['types'],record['population'])
        result=inspect(vertices,record['branch'])
        counts[result['kind']]+=1
        records.append(dict(ordinal=ordinal,branch=record['branch'],population=record['population'],**result))
    output=dict(agent='six-code-3',role='researcher',status='PRIVATE_P21_FORCED_STRUCTURE_ONLY',statistics=dict(counts),records=records,
                survivors=[r for r in records if r['kind']=='UNRESOLVED'],independent_check_pending=True,new_pair_total_claim=None)
    out=ROOT/'scratch/pass16-p21-forced.json'
    if out.exists():raise ValueError('fresh output')
    out.write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(statistics=dict(counts),records=records),sort_keys=True))

if __name__=='__main__':main()
