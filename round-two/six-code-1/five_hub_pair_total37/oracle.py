"""Separate exact P36 coefficient/cut oracle; six-code-1 researcher.
Imports no new producer or private census."""
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
    for N,T,X,tau,Q in it.product(range(5),range(1,7),range(7),range(4),range(18)):
        if Q<4*N or 2*T+2*X+4*tau+Q-N>11:
            continue
        E=14-T-2*tau-Q;K=17-E+2*X
        out.append(dict(N5=N,T=T,X=X,tau=tau,Q=Q,E=E,K=K,
                        margin_budget=3*(E+Q+N-K)))
    return sorted(out,key=lambda c:(c['N5'],c['T'],c['X'],c['tau'],c['Q']))

def certificate(types,case,vector):
    fields=('e','k','q','eligible','h','c1','psi','mu','sigma','I5','hub_weight')
    vertices=[]
    for i in range(len(types)):
        for _ in range(vector[i]):
            vertices.append(dict(zip(fields,types[i]),type_index=i))
    if case['N5']>=1:
        return dict(reason='9538_EXCEPTIONAL_SURCHARGE',N5=case['N5'])
    total=sum(v['eligible'] and v['k']==1 and v['hub_weight']==2 for v in vertices)
    if total>3:
        return dict(reason='COMPLEMENT_TRIANGLE_TYPE20_CAP',population=total,bound=3)
    if case['T']!=1:
        return dict(reason='OPEN')
    bad=sorted({v['type_index'] for v in vertices if v['hub_weight']>v['k']+v['k']})
    if bad:
        return dict(reason='T1_HUB_DELTA_CAP',types=bad)
    n0=sum(v['eligible'] and v['k']==1 and v['hub_weight']==2 for v in vertices)
    if n0>=2:
        return dict(reason='T1_ELIGIBLE_SINGLE_HUB_CAP',population=n0,bound=1)
    n1=sum(v['e']==1 and v['k']==1 and v['q']==1 and v['hub_weight']==2
           for v in vertices)
    if n1>=5:
        return dict(reason='T1_DEGREE_ONE_SINGLE_HUB_CAP',population=n1,bound=4)
    eligible=[j for j,v in enumerate(vertices) if v['eligible']]
    units=[j for j,v in enumerate(vertices) if v['e']==0]
    A=set(units)-set(eligible)
    V=set(units)&set(eligible)
    C=set(range(13))-set(units)-set(eligible)
    B=set(eligible)-set(units)
    R=sum(vertices[j]['k']==0 for j in units)
    d=lambda j:vertices[j]['h']-vertices[j]['k']
    DA=sum(d(j) for j in A);DV=sum(d(j) for j in V)
    I=sum(min(d(j),len(A)-1) for j in A);even=I-I%2
    C1=sum(vertices[j]['c1'] for j in C)
    if R>0 and len(B)>0 and DV+max(R,DA-even)>C1:
        return dict(reason='9538_ELIGIBLE_UNIT_ROOT_CAPACITY',R=R,D_A=DA,D_V=DV,
                    I_even=even,C1=C1,required=DV+max(R,DA-even))
    return dict(reason='OPEN')

def deficit_calibration():
    start=time.monotonic();records=[];nodes=0
    def visit(prefix,left):
        nonlocal nodes
        nodes+=1
        need(nodes<=100000 and time.monotonic()-start<=10,
             'INCOMPLETE fixed100000-node/10s calibration guard')
        if len(prefix)<4:
            for value in range(left+1):
                visit(prefix+(value,),left-value)
            return
        D=prefix+(left,)
        descending=sorted(D,reverse=True)
        ok=descending[0]+descending[1]<=10
        counts=[]
        if ok:
            need(all(d<=7 for d in D),'ordered deficit capacity')
            local=[]
            for d in D:
                permitted=[0]
                for n in range(1,5):
                    if any(N>=4 and N>=n and d>=N+n for N in range(d+1)):
                        permitted.append(n)
                local.append(permitted)
            for n in it.product(*local):
                need(sum(n)<4,'four eligible row quota contradiction')
                counts.append(n)
        records.append(dict(D=D,pair_cap_valid=ok,eligible_counts=counts))
    visit((),17)
    return sorted(records,key=lambda r:r['D'])

def build():
    old=frozen_engine('oracle')
    literal=json.loads((PARENT/'fixtures.json').read_text())
    raw,selected=old.physical_rows(literal)
    types=sorted({tuple(r['coordinates']) for r in selected})
    need(types[20]==(1,1,0,True,4,3,0,0,0,0,2) and
         types[22]==(1,1,1,False,4,3,-3,0,0,0,2),'exact new type scopes')
    cases=scalar_cases();branches=[];maximum=0
    for case in cases:
        vectors,states=old.coefficient_vectors(types,case)
        maximum=max(maximum,states)
        rows=[]
        for vector in vectors:
            prior=old.direct_capacity(types,vector)
            if prior['reason']!='OPEN':
                cut=dict(reason='OLD_FROZEN_CUT',cut=prior)
            else:
                cut=certificate(types,case,vector)
            rows.append(dict(vector=vector,certificate=cut))
        branches.append(dict(case=case,rows=rows))
    record=dict(actual_marks=raw,conservative_marks=selected,types=types,
                scalar_cases=cases,branches=branches,deficit_calibration=deficit_calibration())
    return record,dict(max_states=maximum)
