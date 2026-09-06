"""Rebuild the compact triple-cut certificate from a pinned exploratory graph."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXAMPLE_SHA='a8343f5462d523f2203f0f85e1aa526ab64060713bb1661af4e04ff8d52d1924'


def need(ok,msg):
    if not ok:raise ValueError(msg)


def clique_sets(n,red,k,color):
    rows=[0]*n
    for u,v in itertools.combinations(range(n),2):
        if ((u,v) in red)==color:rows[u]|=1<<v;rows[v]|=1<<u
    def visit(prefix,remaining):
        if len(prefix)==k:
            yield prefix;return
        while remaining.bit_count()+len(prefix)>=k:
            bit=remaining&-remaining;remaining^=bit;v=bit.bit_length()-1
            yield from visit(prefix+[v],remaining&rows[v])
    return list(visit([], (1<<n)-1))


def produce():
    raw=(HERE/'EXAMPLE43.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==EXAMPLE_SHA,'fixture identity')
    full={tuple(e) for e in json.loads(raw)['red_edges']}
    labels=[0,1,2,3,4,7,8,10,12,15,19]
    target=[(8,9),(8,10),(9,10)]
    blue_triangles=[(1,3,7),(1,5,6),(1,4,7)]
    R={(0,2)}|{(u,v) for u in (0,2) for v in (8,9,10)}
    B=set()
    for pair,tri in zip(target,blue_triangles):
        B.update(tuple(sorted(e)) for e in itertools.combinations(tri,2))
        B.update(tuple(sorted((u,v))) for u in pair for v in tri)
    need(not R&B,'consistent partial colors')
    need(all((labels[u],labels[v]) in full for u,v in R),'embedded red premises')
    need(all((labels[u],labels[v]) not in full for u,v in B),'embedded blue premises')
    completions=[]
    for deleted in range(11):
        keep=[v for v in range(11) if v!=deleted];position={v:i for i,v in enumerate(keep)}
        free=[e for e in target if deleted not in e]
        found=None
        for mask in range(1<<len(free)):
            edges={(position[u],position[v]) for u,v in itertools.combinations(keep,2)
                   if (u,v) not in target and (labels[u],labels[v]) in full}
            edges.update((position[u],position[v]) for i,(u,v) in enumerate(free) if mask>>i&1)
            if not clique_sets(10,edges,5,True) and not clique_sets(10,edges,5,False):
                bitmask=sum(1<<i for i,e in enumerate(itertools.combinations(range(10),2)) if e in edges)
                found={'deleted':deleted,'red_mask_hex':format(bitmask,'012x')};break
        need(found is not None,'deletion completion missing');completions.append(found)
    types=[117,421,621];self_witness=[]
    core={e for e in full if e[1]<11}
    for t in types:
        found={}
        for c in (True,False):
            tri=next(s for s in clique_sets(11,core,3,c) if all(bool(t>>v&1)==c for v in s))
            found['red' if c else 'blue']=tri
        self_witness.append(found)
    return {'format':'r55-critical-path-triple-cut-v1',
            'partial':{'n':11,'red_edges':[list(e) for e in sorted(R)],'blue_edges':[list(e) for e in sorted(B)]},
            'forcing_pairs':[list(e) for e in target],'blue_forcing_triangles':[list(t) for t in blue_triangles],
            'red_root_pair':[0,2],'deletion_completions':completions,
            'example_original_labels':labels,'core_red_edges':[list(e) for e in sorted(core)],
            'footprints':types,'self_copy_witnesses':self_witness,
            'guarded_count_cut':{'types':types,'coefficients':[1,1,1],'upper_bound':2},
            'example_sha256':EXAMPLE_SHA}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(not a.output.exists(),'fresh output');a.output.write_text(json.dumps(produce(),indent=2,sort_keys=True)+'\n')
