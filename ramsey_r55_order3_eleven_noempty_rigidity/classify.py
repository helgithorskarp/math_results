#!/usr/bin/env python3
"""Necessary four-bit multiplicities when no fixed signature is empty."""
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_anchor_propagation'
PIN='efb670ac77e1ff9e3d3b8b22040942e64a27164bd83b45db95f388209bcbb801'


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def counts(total,length):
    if length==1:
        yield (total,);return
    for first in range(total+1):
        for rest in counts(total-first,length-1):yield (first,)+rest


def red_edges(bits):
    pairs=list(combinations(range(4),2));edges=set()
    for u,v in combinations(range(12),2):
        i,s=divmod(u,3);j,t=divmod(v,3)
        if i==j or bits[3*pairs.index((i,j))+(t-s)%3]=='1':edges.add((u,v))
    return edges


def classify():
    require(info(PREVIOUS/'result.json')['sha256']==PIN,'inherited result pin')
    old=json.loads((PREVIOUS/'result.json').read_text());require(old['complete'],'inherited completion')
    rows=[];large=[m for m in range(16) if m.bit_count()>=2]
    for core in old['cases']:
        if core['status']!='open':continue
        good=core['omitted'];g=len(good);red=red_edges(core['bits']);witnesses=[]
        for i in good:
            vertices=[v for v in range(12) if v//3!=i]
            witness=next(t for t in combinations(vertices,4) if all(e in red for e in combinations(t,2)))
            witnesses.append(dict(omitted=i,red_k4=list(witness)))
        singles=[1+int(i in good) for i in range(4)];profiles=[];raw=0
        for tail in counts(10-sum(singles),len(large)):
            raw+=1;vector=[0]*16
            for i,x in enumerate(singles):vector[1<<i]=x
            for m,x in zip(large,tail):vector[m]=x
            if any(sum(x for m,x in enumerate(vector) if m&(1<<i))>4 for i in range(4)):continue
            if any(sum(vector[m] for m in range(16) if m&(15^(1<<i))==(15^(1<<i))) for i in good):continue
            if any(vector[1<<i]+vector[(1<<i)|(1<<j)]>3 for i in range(4) for j in range(4) if i!=j):continue
            valid=True
            for i in range(4):
                if i in good:continue
                projection=[0]*8
                for m,x in enumerate(vector):
                    word=sum(((m>>j)&1)<<k for k,j in enumerate(j for j in range(4) if j!=i))
                    projection[word]+=x
                if projection!=[1,2,2,1,2,1,1,0]:valid=False;break
            if valid:profiles.append([m for m,x in enumerate(vector) for _ in range(x)])
        rows.append(dict(index=core['index'],bits=core['bits'],labeled=core['labeled'],good=good,
                         red_k4_witnesses=witnesses,singletons=singles,raw_completions=raw,profiles=sorted(profiles)))
    profiles=next(r for r in rows if r['index']==194)['profiles'];cases=[]
    for number,masks in enumerate(profiles):
        prefix=sorted([[int(bool(m&(1<<i))) for i in range(4)] for m in masks])
        cases.append(dict(index=number,core=194,masks=masks,prefixes=prefix))
    require(len(rows)==26 and len(cases)==15,'expected finite boundary')
    return dict(format='r55-r4-noempty-rigidity-v1',cores=rows,cases=cases,
        raw_completions=sum(r['raw_completions'] for r in rows),
        arithmetically_closed=[r['index'] for r in rows if not r['profiles']])


if __name__=='__main__':print(json.dumps(classify(),indent=2,sort_keys=True))
