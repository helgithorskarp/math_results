"""Regenerate the sixteen positive half words via exact direction parity.

The optional discovery stage uses the pinned sibling's cyclotomic arithmetic.
Its output is checked edge by edge by verify.py without importing this code.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
SELECTED=(0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,17)


def need(ok,message):
    if not ok:raise ValueError(message)


def discover():
    plan=json.loads((HERE/'inputs.json').read_text())
    source=HERE.parent/plan['word_discovery_source']
    need(sha256(source.read_bytes()).hexdigest()==plan['word_discovery_source_sha256'],'arithmetic source hash')
    spec=importlib.util.spec_from_file_location('cyclotomic',source);q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    raw=(HERE.parent/plan['graph_file']).read_bytes();need(sha256(raw).hexdigest()==plan['graph_sha256'],'graph hash');graph=json.loads(raw)
    sqrt3,U=q.field_constants();g1=q.build_g1(graph['paths'],sqrt3,U);points=q.build_g2(g1,sqrt3)
    need(q.coordinate_hash(points,False)=='c450c335d446647890189542ad66d1443095772e5aeef2e7c7f41e417d9bad1e','G2 coordinate order')
    need(all(U[i+42]==(q.neg(U[i][0]),q.neg(U[i][1])) for i in range(42)),'antipodal direction labels')
    directions={u:i%42 for i,u in enumerate(U)};edges=[(a,b) for a,b in graph['G3_edges'] if b<1066]
    labelled=[];adj=[[] for _ in points]
    for a,b in edges:
        difference=(q.sub(points[b][0],points[a][0]),q.sub(points[b][1],points[a][1]));k=directions[difference]
        labelled.append((a,b,k));adj[a].append((b,k));adj[b].append((a,k))
    paths=[None]*1066;paths[0]=0;stack=[0]
    while stack:
        a=stack.pop()
        for b,k in adj[a]:
            if paths[b] is None:paths[b]=paths[a]^(1<<k);stack.append(b)
    need(all(v is not None for v in paths),'connected half')
    basis={}
    for a,b,k in labelled:
        relation=paths[a]^paths[b]^(1<<k)
        while relation:
            col=relation.bit_length()-1
            if col not in basis:basis[col]=relation;break
            relation^=basis[col]
    free=[i for i in range(42) if i not in basis];kernel=[]
    for j in free:
        vector=1<<j
        for k in sorted(basis):
            if (basis[k]&vector).bit_count()%2:vector^=1<<k
        kernel.append(vector)
    need(len(kernel)==12,'discovery parity dimension')
    forms=[sum(((v>>i)&1)<<j for j,v in enumerate(kernel)) for i in range(42)]
    vertex_forms=[sum(((v&w).bit_count()%2)<<j for j,v in enumerate(kernel)) for w in paths]
    zeros=[sum(((a&f).bit_count()%2==0)<<j for j,f in enumerate(forms)) for a in range(4096)]
    pairs=[]
    # a,b,a XOR b are the three nonzero members of the same 2D binary space.
    for a in range(1,4096):
        for b in range(a+1,4096):
            if b<(a^b) and not zeros[a]&zeros[b]:pairs.append((a,b))
    need(len(pairs)==42,'discovery affine word count')
    words=[]
    for index in SELECTED:
        a,b=pairs[index];word=[((a&f).bit_count()%2)+2*((b&f).bit_count()%2) for f in vertex_forms]
        need(all(word[u]!=word[v] for u,v in edges),'positive discovery word')
        words.append(''.join(map(str,word)))
    return '\n'.join(words)+'\n'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    start=time.monotonic();raw=discover().encode();args.out.mkdir(parents=True,exist_ok=True);(args.out/'half_colourings.txt').write_bytes(raw)
    print(json.dumps({'half_colourings_sha256':sha256(raw).hexdigest(),'bytes':len(raw),'seconds':time.monotonic()-start},sort_keys=True))

if __name__=='__main__':main()
