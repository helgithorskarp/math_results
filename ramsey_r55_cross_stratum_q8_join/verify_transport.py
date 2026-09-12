"""Literal endpoint verifier. Does not import the routing producer."""
from itertools import combinations
from pathlib import Path
import argparse,json
from common import need,matrix,source_catalog,route_class,core_guards,assumptions,mono,dependencies

def check(source,packet,data,queue):
    dependencies();a,q,r,c,blocks,C=source_catalog(source,data)
    need(route_class(q,r)=='Q8_PHYSICAL','eligible original source family')
    need(packet['source_task']==source['task'] and packet['original_task_unsat'] is False,'source/scope binding')
    if packet['status']=='MONOCHROMATIC_FIVE':
        S=packet['vertices'];color=packet['color']
        need(color in (0,1) and len(S)==5 and len(set(S))==5 and all(type(x) is int and 0<=x<43 for x in S),'five syntax')
        need(all(a[u][v]==color for u,v in combinations(S,2)),'literal five')
        return {'status':'PHYSICAL_FIVE_VERIFIED','original_task_unsat':False}
    need(packet['status']=='Q8_PHYSICAL_TRANSPORT_NO_RAMSEY_VERDICT' and packet['r']==r,'destination scope')
    p=packet['new_to_old'];need(all(type(x) is int for x in p) and sorted(p)==list(range(43)),'permutation')
    aa=matrix(packet['graph']);need(all(aa[u][v]==a[p[u]][p[v]] for u,v in combinations(range(43),2)),'all 903 physical edges')
    need({frozenset(p[4*b:4*b+4]) for b in range(r)}=={frozenset(B) for B in blocks[:r]},'all original red blocks retained')
    for b in range(8):need(all(aa[u][v]==int(b<r) for u,v in combinations(range(4*b,4*b+4),2)),'destination block colors')
    need(mono(aa,list(range(4*r,43)),4,1) is None,'destination red maximality')
    scores=[]
    for b in range(1,8):
        ss=[sum(aa[u][4*b+j]<<u for u in range(4)) for j in range(4)]
        need(all(x>=y for x,y in zip(ss,ss[1:])),'root-column order')
        scores.append(sum(aa[u][4*b+j]<<(4*u+j) for u in range(4) for j in range(4)))
    for values in [scores[:r-1],scores[r-1:]]:need(all(x>=y for x,y in zip(values,values[1:])),'whole-block order')
    w=sum(aa[32+i][32+j]<<k for k,(i,j) in enumerate(combinations(range(11),2)))
    need(packet['core_word']==f'{w:014x}','unclassified core word');guards=core_guards(queue);leaf=packet['cohort']
    need(type(leaf) is int and 0<=leaf<239,'cohort');m,v=guards[leaf]
    need(w&m==v and packet['core_assumptions']==assumptions(guards[leaf]),'physical guard')
    need(packet['physical_edge_cube']==([119 if aa[3][4] else -119] if r==8 else []),'actual physical edge branch')
    need(packet['destination_core_catalog_membership_required'] is False,'broader physical scope')
    # Every K5 prohibition is preserved by the checked full permutation.
    # We intentionally do not claim that this control/input has no K5.
    return {'status':'COMPLETE_Q8_PHYSICAL_TRANSPORT_VERIFIED','source_task':source['task'],'r':r,'cohort':leaf,
            'physical_edge_equalities':903,'original_task_unsat':False,'ramsey_graph_claimed':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('queue');p.add_argument('source');p.add_argument('packet');s=p.parse_args()
    print(json.dumps(check(json.loads(Path(s.source).read_text()),json.loads(Path(s.packet).read_text()),s.catalog,s.queue),sort_keys=True))
