"""Seed-selected sum-separation chambers of symmetric Schur axis words.

Only axis run lengths occur. No columns, column-order constraints, or total
column equalities enter this model or its duals.
"""
import argparse
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import time

from audit import check_word


def runs(row):return [(c,len(list(g))) for c,g in itertools.groupby(row)]
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(k,x):return tuple(k*a for a in x)


def model(word,multiplier):
    check_word(word);assert (len(word)+1)%5==0
    a0=(len(word)+1)//5;inv=pow(multiplier,-1,a0)
    axis=[word[5*((inv*q)%a0)-1] for q in range(1,a0)]
    assert axis==axis[::-1]
    parsed=runs(axis[:a0//2]);d=len(parsed);seed=[v for c,v in parsed]
    zero=(0,)*(d+1);one=zero[:-1]+(1,)
    basis=[tuple(int(i==j) for i in range(d))+(0,) for j in range(d)]
    modulus=(2,)*d+(1,);positive={c:[] for c in range(6)};cursor=one
    for j,(c,v) in enumerate(parsed):
        after=add(cursor,basis[j]);positive[c].append((cursor,sub(after,one)));cursor=after
    E={c:positive[c]+[(sub(modulus,U),sub(modulus,L)) for L,U in positive[c]] for c in range(6)}
    def ev(f):return sum(x*y for x,y in zip(f[:-1],seed))+f[-1]
    rows={};raw=0
    def retain(f,reason):
        assert ev(f)<=0
        divisor=math.gcd(*f);f=tuple(x//divisor for x in f) if divisor>1 else f
        if any(f[:-1]):rows.setdefault((*f[:-1],-f[-1]),reason)
        else:assert f[-1]<=0
    for c in range(6):
        for i,j in itertools.combinations_with_replacement(range(len(E[c])),2):
            lo=add(E[c][i][0],E[c][j][0]);hi=add(E[c][i][1],E[c][j][1])
            for z,(L,U) in enumerate(E[c]):
                for t in (0,1):
                    raw+=1;l=add(L,scale(t,modulus));u=add(U,scale(t,modulus))
                    if ev(hi)<ev(l):f=add(sub(hi,l),one);side='left_before_right'
                    else:assert ev(u)<ev(lo);f=add(sub(u,lo),one);side='right_before_left'
                    retain(f,['axis_sum',c,i,j,z,t,side])
    for j in range(d):retain(sub(one,basis[j]),['positive_run_length',j])
    keys=sorted(rows)
    return dict(multiplier=multiplier,axis_factor=a0,axis_word=axis,run_colours=[c for c,v in parsed],
        seed_lengths=seed,dimension=d,rows=[list(k) for k in keys],reasons=[rows[k] for k in keys],
        objective=[2]*d,objective_constant=1,raw_obligations=raw)


def bound(m,rows,reasons,objective,constant):
    import numpy as np
    from scipy.optimize import linprog
    arr=np.array(rows,float)
    r=linprog(-np.array(objective),A_ub=arr[:,:-1],b_ub=arr[:,-1],bounds=(None,None),
        method='highs',options={'time_limit':30})
    assert r.success,r.message
    weights=[Fraction(float(-v)).limit_denominator(1000000) for v in r.ineqlin.marginals]
    assert all(v>=0 for v in weights)
    active=[(v,row) for v,row in zip(weights,rows) if v]
    assert [sum(v*row[j] for v,row in active) for j in range(m['dimension'])]==list(objective)
    upper=constant+sum(v*row[-1] for v,row in active)
    return upper,dict(terms=[dict(weight=str(v),reason=reasons[j]) for j,v in enumerate(weights) if v]),r.x


def run(word,multiplier,output,target=72,max_tests=20):
    start=time.monotonic();m=model(word,multiplier);rows=m['rows'][:];reasons=m['reasons'][:]
    cuts=[];attempted=set();tests=0
    while True:
        upper,proof,point=bound(m,rows,reasons,m['objective'],1)
        if upper<=target or tests>=max_tests:break
        candidates=[j for j,x in enumerate(point) if abs(x-round(x))>1e-6 and j not in attempted]
        candidates.sort(key=lambda j:(math.floor(point[j]),j));changed=False
        for j in candidates:
            if tests>=max_tests:break
            attempted.add(j);tests+=1;obj=[int(k==j) for k in range(m['dimension'])]
            cap,certificate,_=bound(m,rows,reasons,obj,0)
            if math.floor(cap)<point[j]-1e-7:
                certificate.update(coordinate=j,upper=str(cap));cuts.append(certificate)
                rows.append(obj+[math.floor(cap)]);reasons.append(['integer_rounding',len(cuts)-1]);changed=True;break
        if not changed:break
    record=dict(multiplier=multiplier,dimension=m['dimension'],run_colours=m['run_colours'],
        upper_bound_axis_factor=str(upper),rounding_cuts=cuts,tests=tests,**proof)
    Path(output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(multiplier=multiplier,dimension=m['dimension'],upper=str(upper),
        cuts=len(cuts),tests=tests,seconds=round(time.monotonic()-start,3))),flush=True)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--multiplier',type=int,required=True);p.add_argument('--target',type=int,default=72)
    args=p.parse_args();run(json.loads(Path(args.source).read_text())['word'],args.multiplier,args.output,args.target)
