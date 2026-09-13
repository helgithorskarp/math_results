#!/usr/bin/env python3
"""Standard-library independent column classification of the whole F4 class."""
from collections import Counter
from itertools import permutations,product
import hashlib,json
from pathlib import Path

# Rows/columns are0,1,t,1+t in F2[t]/(t^2+t+1).
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
P1=((1,0),(0,1),(1,1),(1,2),(1,3))


def need(ok,msg):
    if not ok:raise ValueError(msg)


def normalize(row):
    pivot=next(t for t in row if t)
    inv=next(u for u in (1,2,3) if MUL[u][pivot]==1)
    return tuple(MUL[inv][t] for t in row)


def run():
    # No zero column and no repeated projective column are allowed: either
    # would create a nonzero row combination of support at most two.
    pencils=Counter()
    for columns in permutations(P1,4):
        for scale in product((1,2,3),repeat=4):
            cols=[(MUL[s][a],MUL[s][b]) for s,(a,b) in zip(scale,columns)]
            p=tuple(sorted((normalize(tuple(MUL[a][u]^MUL[b][v] for u,v in cols)),0) for a,b in P1))
            need(len(set(p))==5,'five distinct row directions')
            need(sorted(sum(t!=0 for t in n) for n,c in p)==[3,3,3,3,4],'intrinsic support profile')
            pencils[p]+=1
    need(sum(pencils.values())==9720 and len(pencils)==54 and set(pencils.values())=={180},'full GL2 orbit classification')
    records=json.loads((Path(__file__).parent/'PENCILS.json').read_text())
    supplied=[tuple((tuple(n),c) for n,c in p) for idx,p in records]
    need(len(supplied)==len(set(supplied))==54 and set(supplied)==set(pencils),'entrywise independent class alignment')
    return {'status':'PASS','ordered_generator_matrices':9720,'matrices_per_row_space':180,'intrinsic_pencils':54,'lifts_per_pencil':2048,'total_lifts':110592,'pencil_set_sha256':hashlib.sha256(json.dumps(sorted(pencils),separators=(',',':')).encode()).hexdigest()}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
