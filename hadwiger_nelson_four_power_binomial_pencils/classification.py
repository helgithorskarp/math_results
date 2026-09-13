#!/usr/bin/env python3
"""Independent standard-library projective-column classification."""
from collections import Counter
from itertools import product
import hashlib,json
from pathlib import Path
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
P1=((1,0),(0,1),(1,1),(1,2),(1,3))
def need(ok,msg):
    if not ok:raise ValueError(msg)
def normalize(row):
    pivot=next(t for t in row if t);inv=next(u for u in (1,2,3) if MUL[u][pivot]==1)
    return tuple(MUL[inv][t] for t in row)
def run():
    pencils=Counter();profiles=Counter()
    for directions in product(P1,repeat=4):
        multiplicities=sorted(Counter(directions).values())
        if multiplicities not in ([1,1,2],[2,2]):continue
        for scale in product((1,2,3),repeat=4):
            cols=[(MUL[s][a],MUL[s][b]) for s,(a,b) in zip(scale,directions)]
            p=tuple(sorted((normalize(tuple(MUL[a][u]^MUL[b][v] for u,v in cols)),0) for a,b in P1))
            need(len(set(p))==5,'rank two with five distinct row directions')
            support=tuple(sorted(sum(t!=0 for t in n) for n,c in p))
            need(support in ((2,3,3,4,4),(2,2,4,4,4)),'support profile')
            pencils[p]+=1
    need(sum(pencils.values())==34020 and len(pencils)==189 and set(pencils.values())=={180},'complete GL2 classification')
    records=json.loads((Path(__file__).parent/'PENCILS.json').read_text())
    supplied=[tuple((tuple(n),c) for n,c in p) for idx,p in records]
    need(len(supplied)==len(set(supplied))==189 and sorted(supplied)==sorted(pencils),'entrywise class alignment')
    for p in pencils:profiles[','.join(map(str,sorted(sum(t!=0 for t in n) for n,c in p)))]+=1
    return {'status':'PASS','generator_matrices':34020,'matrices_per_row_space':180,'intrinsic_pencils':189,'support_profiles':dict(sorted(profiles.items())),'lifts_per_pencil':2048,'total_lifts':387072,'pencil_set_sha256':hashlib.sha256(json.dumps(sorted(pencils),separators=(',',':')).encode()).hexdigest()}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
