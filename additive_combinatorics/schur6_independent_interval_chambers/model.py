"""Exact linear chamber of independent-column interval deformations.

Run colours and their cyclic order stay fixed; all positive integral run
lengths are independent variables. For each modular interval nonintersection,
retain the ordering satisfied by the seed. This is one explicitly defined
convex chamber, not all run-order templates or all independent columns.
"""
import argparse
import hashlib
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

from word import transform_word,verify_word

def columns(word):
    a=(len(word)+1)//5
    return [[word[5*q+b-1] if word[5*q+b-1]>=2 else 0 for q in range(a)] for b in (1,2)]


def runs(row):
    result=[]
    for c in row:
        if result and result[-1][0]==c:result[-1][1]+=1
        else:result.append([c,1])
    return result


def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def scale(k,x):return tuple(k*a for a in x)


def chamber(source,multiplier=1):
    data=json.loads(Path(source).read_text())
    if 'seed_word' in data:data=dict(word=data['seed_word'],axis_factor=data['seed_axis_factor'])
    verify_word(data)
    word=transform_word(data['word'],multiplier);a0=data['axis_factor'];row=[None]+word
    controls=[runs([row[5*u] for u in range(1,a0//2+1)]),*map(runs,columns(word))]
    sizes=list(map(len,controls));dimension=sum(sizes);seed=[length for part in controls for _,length in part]
    zero=(0,)*(dimension+1);one=zero[:-1]+(1,)
    unit=[tuple(int(i==j) for i in range(dimension))+(0,) for j in range(dimension)]
    half=zero
    for v in unit[:sizes[0]]:half=add(half,v)
    modulus=add(scale(2,half),one)
    def ev(x):return sum(v*z for v,z in zip(x[:-1],seed))+x[-1]
    def intervals(part,offset,start):
        result={c:[] for c in range(6)};cursor=start
        for j,(c,length) in enumerate(part):
            end=add(cursor,unit[offset+j]);result[c].append((cursor,sub(end,one)));cursor=end
        return result,cursor
    positive,_=intervals(controls[0],0,one)
    E={c:positive[c]+[(sub(modulus,u),sub(modulus,l)) for l,u in positive[c]] for c in range(6)}
    A,endA=intervals(controls[1],sizes[0],zero)
    B,endB=intervals(controls[2],sum(sizes[:2]),zero)
    equalities=[sub(endA,modulus),sub(endB,modulus)]
    assert all(ev(e)==0 for e in equalities)
    rows={};raw_obligations=0
    def inequality(form,reason):
        assert ev(form)<=0,(reason,ev(form))
        coefficients=form[:-1];rhs=-form[-1]
        common=math.gcd(*coefficients,rhs)
        if common>1:coefficients=tuple(v//common for v in coefficients);rhs//=common
        if not any(coefficients):assert rhs>=0;return
        key=(*coefficients,rhs)
        rows.setdefault(key,reason)
    def separate(first,second,reason):
        nonlocal raw_obligations
        raw_obligations+=1
        l,u=first;L,U=second
        if ev(u)<ev(L):inequality(add(sub(u,L),one),[*reason,'left_before_right'])
        else:
            assert ev(U)<ev(l),(reason,ev(l),ev(u),ev(L),ev(U))
            inequality(add(sub(U,l),one),[*reason,'right_before_left'])
    def isum(X,Y):return add(X[0],Y[0]),add(X[1],Y[1])
    def shift(X,t):return add(X[0],scale(t,modulus)),add(X[1],scale(t,modulus))
    def difference(X,Y):return sub(X[0],Y[1]),sub(X[1],Y[0])
    for c in range(6):
        for i,j in itertools.combinations_with_replacement(range(len(E[c])),2):
            for z,Z in enumerate(E[c]):
                for t in (0,1):separate(isum(E[c][i],E[c][j]),shift(Z,t),['axis_sum',c,i,j,z,t])
    for c in range(2,6):
        for i,j in itertools.combinations_with_replacement(range(len(A[c])),2):
            for z,Z in enumerate(B[c]):
                for t in (0,1):separate(isum(A[c][i],A[c][j]),shift(Z,t),['A_A_B',c,i,j,z,t])
        for i,X in enumerate(A[c]):
            for j,k in itertools.combinations_with_replacement(range(len(B[c])),2):
                total=isum(X,isum(B[c][j],B[c][k]))
                for t in (1,2):
                    point=sub(scale(t,modulus),one)
                    separate(total,(point,point),['A_B_B_minus_one',c,i,j,k,t])
    for name,part,special in (('A',A,0),('B',B,1)):
        for state in (0,2,3,4,5):
            c=special if state==0 else state
            for i,X in enumerate(part[state]):
                for j,Y in enumerate(part[state]):
                    for z,Z in enumerate(E[c]):
                        for t in (-1,0):separate(difference(X,Y),shift(Z,t),['difference_axis',name,state,i,j,z,t])
    for j in range(dimension):inequality(sub(one,unit[j]),['positive_run_length',j])
    keys=sorted(rows)
    return dict(axis_factor=a0,multiplier=multiplier,run_colours=[[c for c,_ in part] for part in controls],
                run_counts=sizes,dimension=dimension,seed_lengths=seed,
                rows=[list(key) for key in keys],reasons=[rows[key] for key in keys],
                equalities=[list(e[:-1])+[-e[-1]] for e in equalities],
                objective=list(modulus[:-1]),objective_constant=modulus[-1],
                raw_interval_obligations=raw_obligations,seed_word=word)


def verify_dual(model,certificate):
    n=model['dimension'];left=[Fraction(0) for _ in range(n)];bound=Fraction(model['objective_constant'])
    for entry in certificate['inequalities']:
        i=entry['row'];weight=Fraction(entry['weight']);assert weight>=0
        row=model['rows'][i]
        for j in range(n):left[j]+=weight*row[j]
        bound+=weight*row[-1]
    for i,weight in enumerate(certificate['equality_weights']):
        weight=Fraction(weight);row=model['equalities'][i]
        for j in range(n):left[j]+=weight*row[j]
        bound+=weight*row[-1]
    assert left==list(map(Fraction,model['objective'])),[(i,str(a),b) for i,(a,b) in enumerate(zip(left,model['objective'])) if a!=b]
    assert bound==Fraction(certificate['upper_bound_axis_factor'])
    return dict(status='EXACT_RATIONAL_DUAL_VERIFIED',upper_bound=str(bound),nonzero_rows=len(certificate['inequalities']))


def run(source,output,multiplier=1):
    import scipy
    import numpy as np
    from scipy.optimize import linprog
    tick=time.monotonic();model=chamber(source,multiplier)
    rows=np.array(model['rows'],dtype=float);eq=np.array(model['equalities'],dtype=float)
    result=linprog(-np.array(model['objective']),A_ub=rows[:,:-1],b_ub=rows[:,-1],
                   A_eq=eq[:,:-1],b_eq=eq[:,-1],bounds=(None,None),method='highs',options={'time_limit':45})
    record=dict(source=source,axis_factor=model['axis_factor'],multiplier=multiplier,
                run_counts=model['run_counts'],dimension=model['dimension'],inequalities=len(model['rows']),
                raw_interval_obligations=model['raw_interval_obligations'],lp_status=int(result.status),lp_message=result.message,
                scipy_version=scipy.__version__,model_sha256=hashlib.sha256(json.dumps(model,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                scope='one interval-separation chamber, all three independent run-length vectors')
    if result.success:
        def exact(value):return Fraction(float(value)).limit_denominator(1000000)
        weights=[exact(-y) for y in result.ineqlin.marginals]
        equal=[exact(-y) for y in result.eqlin.marginals]
        upper=Fraction(model['objective_constant'])+sum(w*row[-1] for w,row in zip(weights,model['rows']))+sum(w*row[-1] for w,row in zip(equal,model['equalities']))
        certificate=dict(inequalities=[dict(row=i,weight=str(w)) for i,w in enumerate(weights) if w],
                         equality_weights=list(map(str,equal)),upper_bound_axis_factor=str(upper))
        record.update(lp_optimum_axis_factor=float(-result.fun+model['objective_constant']),
                      exact_certificate=certificate,check=verify_dual(model,certificate),
                      lp_lengths=[str(exact(x)) for x in result.x])
    record['seconds']=time.monotonic()-tick
    Path(output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('exact_certificate','lp_lengths')}),flush=True)
    return model,record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--multiplier',type=int,default=1);args=p.parse_args();run(args.source,args.output,args.multiplier)
