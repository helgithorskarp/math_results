"""Exact source-first P36 exclusion producer; six-code-1 researcher."""
from collections import Counter
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'five_hub_pair_total36'

def need(ok,message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def frozen_engine(name):
    manifest=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for filename,sha in manifest['frozen_source_sha256'].items():
        need(hashlib.sha256((PARENT/filename).read_bytes()).hexdigest()==sha,
             'changed published mathematical prerequisite')
    spec=importlib.util.spec_from_file_location('p37_frozen_'+name,PARENT/(name+'.py'))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def scalar_cases():
    out=[]
    for N in range(4):
        for T in range(1,(11-3*N)//2+1):
            for X in range((11-3*N-2*T)//2+1):
                for tau in range((11-3*N-2*T-2*X)//4+1):
                    for Q in range(4*N,12+N-2*T-2*X-4*tau):
                        E=14-T-2*tau-Q;K=17-E+2*X
                        out.append(dict(N5=N,T=T,X=X,tau=tau,Q=Q,E=E,K=K,
                                        margin_budget=3*(E+Q+N-K)))
    return sorted(out,key=lambda c:(c['N5'],c['T'],c['X'],c['tau'],c['Q']))

def certificate(types,case,vector):
    if case['N5']:
        return dict(reason='9538_EXCEPTIONAL_SURCHARGE',N5=case['N5'])
    if vector[20]>3:
        return dict(reason='COMPLEMENT_TRIANGLE_TYPE20_CAP',population=vector[20],bound=3)
    if case['T']!=1:
        return dict(reason='OPEN')
    bad=[i for i,(t,n) in enumerate(zip(types,vector)) if n and t[10]>2*t[1]]
    if bad:
        return dict(reason='T1_HUB_DELTA_CAP',types=bad)
    if vector[20]>1:
        return dict(reason='T1_ELIGIBLE_SINGLE_HUB_CAP',population=vector[20],bound=1)
    if vector[22]>4:
        return dict(reason='T1_DEGREE_ONE_SINGLE_HUB_CAP',population=vector[22],bound=4)
    rows=[t for t,n in zip(types,vector) for _ in range(n)]
    A=[t for t in rows if t[0]==0 and not t[3]]
    V=[t for t in rows if t[0]==0 and t[3]]
    C=[t for t in rows if t[0]>0 and not t[3]]
    B=[t for t in rows if t[0]>0 and t[3]]
    R=sum(t[0]==0 and t[1]==0 for t in rows)
    DA=sum(t[4]-t[1] for t in A)
    DV=sum(t[4]-t[1] for t in V)
    even=2*(sum(min(t[4]-t[1],len(A)-1) for t in A)//2)
    C1=sum(t[5] for t in C)
    if R and B and C1<DV+max(R,DA-even):
        return dict(reason='9538_ELIGIBLE_UNIT_ROOT_CAPACITY',R=R,D_A=DA,D_V=DV,
                    I_even=even,C1=C1,required=DV+max(R,DA-even))
    return dict(reason='OPEN')

def deficit_calibration():
    start=time.monotonic();records=[]
    # Four bars in21 positions encode all five nonnegative totals summing17.
    for bars in it.combinations(range(21),4):
        D=(bars[0],bars[1]-bars[0]-1,bars[2]-bars[1]-1,
           bars[3]-bars[2]-1,20-bars[3])
        ok=all(D[a]+D[b]<=10 for a,b in it.combinations(range(5),2))
        counts=[]
        if ok:
            need(max(D)<=7,'complementary pair totals imply single-hub cap7')
            for n in it.product(*(range(1+max(0,min(d//2,d-4))) for d in D)):
                need(sum(n)<=3,'eligible isolated deficit-two support cap3')
                counts.append(n)
        records.append(dict(D=D,pair_cap_valid=ok,eligible_counts=counts))
        need(len(records)<=100000 and time.monotonic()-start<=10,
             'INCOMPLETE fixed100000-record/10s calibration guard')
    return sorted(records,key=lambda r:r['D'])

def build():
    old=frozen_engine('producer')
    literal=json.loads((PARENT/'fixtures.json').read_text())
    raw,_=old.rows_and_physical_bridge(literal)
    selected=old.conservative_rows(literal,raw)
    types=sorted({tuple(r['coordinates']) for r in selected})
    need(types[20]==(1,1,0,True,4,3,0,0,0,0,2) and
         types[22]==(1,1,1,False,4,3,-3,0,0,0,2),'exact new type scopes')
    cases=scalar_cases();branches=[];maximum=0
    for case in cases:
        vectors,states=old.produce(types,case)
        maximum=max(maximum,states)
        rows=[]
        for vector in vectors:
            prior=old.certificate(types,vector)
            if prior['reason']!='OPEN':
                cut=dict(reason='OLD_FROZEN_CUT',cut=prior)
            else:
                cut=certificate(types,case,vector)
            rows.append(dict(vector=vector,certificate=cut))
        branches.append(dict(case=case,rows=rows))
    record=dict(actual_marks=raw,conservative_marks=selected,types=types,
                scalar_cases=cases,branches=branches,deficit_calibration=deficit_calibration())
    return record,dict(max_states=maximum)
