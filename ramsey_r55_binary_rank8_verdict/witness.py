"""Literal physical good43 checker for a selected-vector certificate."""
from itertools import combinations
import json
import sys
from pathlib import Path
from counter import require

def form(u,v):
    return sum(((u>>j)&1)*((v>>(j+4))&1)+((v>>j)&1)*((u>>(j+4))&1) for j in range(4))%2

def verify(vertices):
    require(len(vertices)==43 and len(set(vertices))==43,'43 distinct labels')
    require(all(type(v)is int and 1<=v<=255 for v in vertices),'coordinate range')
    pairs=list(combinations(range(43),2));edges={p:form(vertices[p[0]],vertices[p[1]]) for p in pairs}
    count=0
    for vs in combinations(range(43),5):
        total=sum(edges[e] for e in combinations(vs,2))
        require(total not in (0,10),'physical monochromatic five-set: '+str(vs));count+=1
    value=sum(edges[p]<<i for i,p in enumerate(pairs))
    return {'good43':True,'five_subsets':count,'edgeword':f'{value:0226x}','red_edges':sum(edges.values())}

if __name__=='__main__':
    print(json.dumps(verify(json.loads(Path(sys.argv[1]).read_text())['coordinates']),indent=2))
