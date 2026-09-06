#!/usr/bin/env python3
"""Six one-empty signature patterns and the complementary multiple-empty branch."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_core194_full'
BOUNDARY=ROOT.parent/'ramsey_r55_order3_eleven_guarded_four'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
WORD='100110110110110100'
PAIRS=list(combinations(range(4),2))
BASE=dict(bytes=24968396,sha256='f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf')


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def premise():
    require(info(PREVIOUS/'result.json')['sha256']=='306ef2a839f2fd38e32e0aeb35d33c597ddce05c10dbe1d855624883042f3892','prior guarded result')
    require(info(PREVIOUS/'verification.json')['sha256']=='6a2726aa9d27a7fcc249d496368142c25c409aa17165620b686d1af86e5b1932','prior fresh reconstruction')
    r=json.loads((PREVIOUS/'result.json').read_text());v=json.loads((PREVIOUS/'verification.json').read_text())
    require(r['complete'] and v['verified'] and r['open']==v['open']==[194] and not r['excluded'],'full Core194 still open')
    c=r['cases'][0]
    require(c['formula']==BASE and v['cases'][0]['formula']==BASE,'entire guarded base')
    require(c['bits']==WORD and c['omitted']==[0,1,2,3] and c['labeled']==81,'core and all four anchors')
    return c


def certificate():
    def red(a,b):
        i,s=divmod(a,3);j,t=divmod(b,3)
        if i==j:return True
        return WORD[3*PAIRS.index((i,j))+(t-s)%3]=='1'
    witnesses=[]
    for omitted in range(4):
        vertices=[v for v in range(12) if v//3!=omitted]
        witness=next(c for c in combinations(vertices,4) if all(red(a,b) for a,b in combinations(c,2)))
        witnesses.append(dict(omitted=omitted,red_k4=list(witness)))
    patterns=[]
    for missing in PAIRS:
        masks=[0]+[1<<i for i in range(4)]+[(1<<i)|(1<<j) for i,j in PAIRS if (i,j)!=missing]
        masks.sort(key=lambda m:tuple((m>>i)&1 for i in range(4)))
        patterns.append(dict(missing_pair=list(missing),masks=masks))
    return dict(index=194,bits=WORD,labeled=81,red_k4_witnesses=witnesses,one_empty_patterns=patterns)


def cases():
    premise();rows=[]
    for p in certificate()['one_empty_patterns']:
        i,j=p['missing_pair'];rows.append(dict(id=f'one_{i}{j}',index=194,branch='one',**p))
    rows.append(dict(id='multiple',index=194,branch='multiple'))
    return sorted(rows,key=lambda c:c['id'])


def clauses(case):
    if case['branch']=='multiple':return [(-v,) for v in range(222,226)]
    require(case in cases(),'exact one-empty case')
    return [((1 if (m>>i)&1 else -1)*(211+11*f+i),) for f,m in enumerate(case['masks']) if f for i in range(4)]


def make(base,output,case):
    require(info(base)==BASE,'complete guarded base identity');tail=clauses(case)
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34320 617932\n','guarded base header')
        g.write(f'p cnf 34320 {617932+len(tail)}\n'.encode());shutil.copyfileobj(f,g)
        for row in tail:g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
