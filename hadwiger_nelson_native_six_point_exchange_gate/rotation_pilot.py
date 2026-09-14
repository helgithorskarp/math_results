#!/usr/bin/env python3
"""Solver-free check of one alternative quadratic-field rotation host."""
from pathlib import Path
import hashlib
import itertools
import json
import time
from verify import require, parent_module
HERE=Path(__file__).resolve().parent
RAD=(1,3,17,51,11,33,187,561)


def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,b):
    c=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i^j]+=x*y*RAD[i&j]
    return tuple(c)
def norm(p):return add(mul(p[:8],p[:8]),mul(p[8:],p[8:]))
def digest(a):return hashlib.sha256(json.dumps(a,separators=(',',':')).encode()).hexdigest()


def verify():
    start=time.monotonic()
    parent_module() # validate all durable input pins
    source=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
    A=[tuple(map(int,line.split())) for line in source.read_text().splitlines()
       if line and not line.startswith('#')]
    require(len(A)==len(set(A))==159 and all(len(p)==16 for p in A),'source size')
    require(all(all(p[i]==0 for i in range(16) if i not in (0,5,9,12)) for p in A),
            'source is in Q(i sqrt3,i sqrt11)')
    D=set()
    for a,b in itertools.combinations(A,2):
        d=sub(a,b)
        if norm(d)==(144,0,0,0,0,0,0,0):D.update((d,tuple(-x for x in d)))
    require(len(D)==30,'unit directions')
    L=sorted(set(A)|{add(a,d) for a in A for d in D},
             key=lambda p:(p[0],p[5],p[9],p[12]))
    q=(0,0,0,1,0,0,0,0) # sqrt51
    native=[tuple(10*x for x in p) for p in L]
    rotated=[sub(tuple(7*x for x in p[:8]),mul(q,p[8:]))
             +add(mul(q,p[:8]),tuple(7*x for x in p[8:])) for p in L]
    full=list(dict.fromkeys(native+rotated))
    require(len(L)==1960 and len(full)==3919,'new host distinct points')
    positions=(0,2,5,7,9,11,12,14)
    require(all(all(p[i]==0 for i in range(16) if i not in positions) for p in full),
            'compact coordinate subspace')
    points=[tuple(p[i] for i in positions) for p in full]
    terms=[[] for _ in range(8)]
    for offset,pos in ((0,(0,2,5,7)),(4,(1,3,4,6))):
        for i,si in enumerate(pos):
            for j in range(i+1):
                sj=pos[j]
                terms[si^sj].append((offset+i,offset+j,RAD[si&sj]*(1 if i==j else 2)))
    edges=[]
    for i,p in enumerate(points):
        for j in range(i):
            d=sub(p,points[j])
            if sum(c*d[a]*d[b] for a,b,c in terms[0])!=14400:continue
            if all(sum(c*d[a]*d[b] for a,b,c in terms[k])==0 for k in range(1,8)):
                edges.append((j,i))
    word=(HERE/'rotation_four_word.txt').read_text().strip()
    require(len(word)==3919 and set(word)<=set('0123'),'new host colour domain')
    require(len(edges)==29096 and all(word[a]!=word[b] for a,b in edges),
            'new host complete-edge colouring')
    out={'status':'ALTERNATIVE HOST IS FOUR-COLOURABLE','geometry':'L union ((7+i sqrt51)/10)L',
         'vertices':len(points),'edges':len(edges),'denominator':120,
         'point_sha256':digest(points),'edge_sha256':digest(edges),
         'word_sha256':hashlib.sha256(word.encode()).hexdigest(),'seconds':time.monotonic()-start}
    return out


if __name__=='__main__':print(json.dumps(verify(),indent=2))
