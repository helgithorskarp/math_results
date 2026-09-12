"""Same-graph transfer to an existing q8 physical base; no core canonicalizer."""
from itertools import combinations
from pathlib import Path
import argparse,json
from common import need,word,mono,source_catalog,route_class,core_guards,assumptions,dependencies

def transport(source,data,queue):
    dependencies();a,q,r,c,blocks,C=source_catalog(source,data)
    need(route_class(q,r)=='Q8_PHYSICAL','source belongs to the 1010 retained original parents')
    red=[B[:] for B in blocks[:r]];blue=[B[:] for B in blocks[r:]];augmentation=None
    if q==7:
        V=blue[0]+C;fours=[list(S) for S in combinations(sorted(V),4) if all(a[u][v]==0 for u,v in combinations(S,2))]
        pair=next(((S,T) for S,T in combinations(fours,2) if set(S).isdisjoint(T)),None)
        if pair is None:
            five=mono(a,V,5,0);need(five is not None,'19-vertex certificate premise failed')
            return {'status':'MONOCHROMATIC_FIVE','source_task':source['task'],'color':0,'vertices':five,'original_task_unsat':False}
        augmentation={'old_block':blue[0],'nineteen':sorted(V),'pair':list(pair)}
        blue=blue[1:]+list(pair)
    need(len(blue)>=8-r,'enough blue blocks')
    kept=blue[:8-r];root=red[0]
    def sig(v):return sum(a[u][v]<<i for i,u in enumerate(root))
    def order(B):return sorted(B,key=lambda v:(-sig(v),v))
    def score(B):return sum(a[u][v]<<(4*i+j) for i,u in enumerate(root) for j,v in enumerate(B))
    ordered=[root]+sorted(map(order,red[1:]),key=score,reverse=True)+sorted(map(order,kept),key=score,reverse=True)
    p=sum(ordered,[]);p+=sorted(set(range(43))-set(p));need(len(p)==43,'transport permutation')
    coreword=sum(a[p[32+i]][p[32+j]]<<k for k,(i,j) in enumerate(combinations(range(11),2)))
    guards=core_guards(queue);matches=[i for i,(m,v) in enumerate(guards) if coreword&m==v];need(len(matches)==1,'unique physical guard')
    leaf=matches[0]
    return {'status':'Q8_PHYSICAL_TRANSPORT_NO_RAMSEY_VERDICT','source_task':source['task'],
            'r':r,'cohort':leaf,'core_word':f'{coreword:014x}','core_assumptions':assumptions(guards[leaf]),
            'new_to_old':p,'graph':word(a,p),'augmentation':augmentation,
            'physical_edge_cube':([119 if a[p[3]][p[4]] else -119] if r==8 else []),
            'original_task_unsat':False,'destination_core_catalog_membership_required':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('queue');p.add_argument('source');p.add_argument('output');s=p.parse_args()
    result=transport(json.loads(Path(s.source).read_text()),s.catalog,s.queue)
    with Path(s.output).open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
