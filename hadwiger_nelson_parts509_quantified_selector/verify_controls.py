#!/usr/bin/env python3
"""Independently exhaust the generated matrix using a small DPLL evaluator."""
from hashlib import sha256
import json
from pathlib import Path
import time
import controls
import encode


def require(value,message):
    if not value:
        raise RuntimeError(message)


def parse(raw):
    lines=raw.decode('ascii').splitlines()
    head=lines.pop(0).split()
    require(head[:2]==['p','cnf'],'header')
    nv,nc=map(int,head[2:])
    prefix=[]
    while lines and lines[0][0] in 'ea':
        line=lines.pop(0).split()
        require(line[-1]=='0','prefix terminator')
        prefix.append((line[0],list(map(int,line[1:-1]))))
    require([q for q,_ in prefix] in [['e','a','e'],['a','e']],'prefix order')
    require(sorted(v for _,vs in prefix for v in vs)==list(range(1,nv+1)),'prefix partition')
    rows=[]
    for line in lines:
        values=list(map(int,line.split()))
        require(values[-1]==0 and all(1<=abs(v)<=nv for v in values[:-1]),'literal syntax')
        rows.append(tuple(values[:-1]))
    require(len(rows)==nc,'clause count')
    require({abs(v) for row in rows for v in row}==set(range(1,nv+1)),'quantified atom absent from matrix')
    return prefix,rows


def sat(rows,truth):
    truth=set(truth)
    while True:
        if any(-v in truth for v in truth):
            return False
        rest=[]
        for row in rows:
            if any(v in truth for v in row):
                continue
            r=tuple(v for v in row if -v not in truth)
            if not r:
                return False
            rest.append(r)
        if not rest:
            return True
        units={r[0] for r in rest if len(r)==1}
        rows=rest
        if not units:
            v=min(rows,key=len)[0]
            return sat(rows,{v}) or sat(rows,{-v})
        truth=units


def inspect(case):
    args={k:case[k] for k in ['n','edges','cross','patterns','budget']}
    raw,meta=encode.encode(**args)
    prefix,rows=parse(raw)
    n=case['n']
    outer=prefix[0][1] if prefix[0][0]=='e' else []
    universal=next(vs for q,vs in prefix if q=='a')
    bits=max(1,(len(case['patterns'])-1).bit_length())
    require(len(universal)==bits+2*n,'universal dimension')
    auxiliary=set(outer)-set(range(1,n+1))
    # Outer auxiliaries factor into constraints involving only outer variables.
    # Their existence can therefore be checked independently of universals.
    require(all(set(map(abs,row))<=set(outer) for row in rows
                if any(abs(v) in auxiliary for v in row)),'outer auxiliary dependency')
    winning=[]
    checked=0
    for selection in range(1<<n):
        X={v for v in range(n) if (selection>>v)&1}
        chosen=[i+1 if i in X else -i-1 for i in range(n)]
        good=True
        for values in range(1<<len(universal)):
            p=values & ((1<<bits)-1)
            colors=[(values>>(bits+2*v))&3 for v in range(n)]
            bad=(p>=len(case['patterns']) or
                 any(a in X and b in X and colors[a]==colors[b] for a,b in case['edges']) or
                 any(v in X and colors[v]==case['patterns'][p][a] for a,v in case['cross']))
            expected=len(X)<=case['budget'] and bad
            assumptions=chosen+[v if (values>>j)&1 else -v for j,v in enumerate(universal)]
            actual=sat(rows,assumptions)
            require(actual==expected,('matrix mismatch',case['name'],selection,values))
            good &= actual
            checked+=1
        if good:
            winning.append(selection)
    require(bool(winning)==case['expected'],('QBF truth',case['name']))
    return dict(name=case['name'],truth=bool(winning),winning_selection_masks=winning,
                matrix_assignments_checked=checked,variables=meta['variables'],clauses=meta['clauses'],
                qdimacs_sha256=sha256(raw).hexdigest())


def main():
    rows=[inspect(case) for case in controls.controls()]
    result=dict(status='ALL PARSED-CNF QUANTIFIER CONTROLS VERIFIED',cases=len(rows),
                matrix_assignments_checked=sum(r['matrix_assignments_checked'] for r in rows),facts=rows)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
