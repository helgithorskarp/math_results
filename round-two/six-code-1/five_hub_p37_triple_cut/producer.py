"""Exact P37/T>=3 producer; six-code-1, researcher."""
from collections import Counter
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'five_hub_pair_total36'
BTYPE=(1,1,0,True,4,3,0,0,0,0,2)

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def frozen():
    manifest=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for name,sha in manifest['frozen_source_sha256'].items():
        need(hashlib.sha256((PARENT/name).read_bytes()).hexdigest()==sha,'changed frozen mathematical source')
    spec=importlib.util.spec_from_file_location('p37_triple_parent_producer',PARENT/'producer.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def cases():
    out=[]
    for T in range(3,8):
        for X in range((15-2*T)//2+1):
            for tau in range((15-2*T-2*X)//4+1):
                for Q in range(16-2*T-2*X-4*tau):
                    E=17-T-2*tau-Q;K=19-E+2*X
                    out.append(dict(T=T,X=X,tau=tau,N5=0,Q=Q,E=E,K=K,
                                    margin_budget=3*(E+Q-K)))
    return sorted(out,key=lambda c:(c['T'],c['X'],c['tau'],c['Q']))

def columns(K):
    """All ordered positive supports with distinguished, DISTINCT B hubs0/1.

    Each hub deficit is1/2. Any heavy row has HIGH-leave degree at most1.
    No code automorphism is imposed; naming the two hubs is a role transport.
    """
    start=time.monotonic();out=[];nodes=0
    for N in it.product(range(1,K-3),repeat=5):
        nodes+=1
        need(nodes<=100000 and time.monotonic()-start<=10,'INCOMPLETE column100000-state/10s guard')
        if sum(N)!=K or min(N[0],N[1])<4:continue
        for n in it.product(*(range(v+1) for v in N)):
            if sum(n)!=19-K or min(n[0],n[1])<1:continue
            if any(x and s<3 for x,s in zip(n,N)):continue
            D=tuple(s+x for s,x in zip(N,n))
            if max(D)>8 or any(D[a]+D[b]>11 for a,b in it.combinations(range(5),2)):continue
            out.append(dict(N=N,n=n,D=D))
    return sorted(out,key=lambda r:(r['N'],r['n'],r['D']))

def check_vector(types,case,v):
    need(len(v)==len(types) and all(type(n) is int and n>=0 for n in v),'full nonnegative integer vector')
    totals=(sum(v),)+tuple(sum(n*t[i] for n,t in zip(v,types)) for i in (0,1,2,8,9,10))
    need(totals==(13,case['E'],case['K'],case['Q'],2*case['X'],0,19),'all scalar and actual hub-weight totals')
    need(sum(n*t[7] for n,t in zip(v,types))<=case['margin_budget'],'corrected-margin budget')

def certificate(types,case,v,old,column_records):
    check_vector(types,case,v)
    prior=old.certificate(types,v)
    if prior['reason']!='OPEN':return dict(reason='FROZEN_ENDPOINT_RADIUS_OR_CLOSURE',cut=prior)
    rows=[t for t,n in zip(types,v) for _ in range(n)]
    A=[t for t in rows if not t[0] and not t[3]]
    V=[t for t in rows if not t[0] and t[3]]
    C=[t for t in rows if t[0] and not t[3]]
    B=[t for t in rows if t[0] and t[3]]
    R=sum(not t[0] and not t[1] for t in rows)
    DA=sum(t[4]-t[1] for t in A);DV=sum(t[4]-t[1] for t in V)
    even=2*(sum(min(t[4]-t[1],len(A)-1) for t in A)//2)
    C1=sum(t[5] for t in C);required=DV+max(R,DA-even)
    if R and (V or B) and C1<required:
        return dict(reason='9538_ROOT_ENDPOINT_C1',R=R,D_A=DA,D_V=DV,I_even=even,C1=C1,required=required)
    bcount=sum(t==BTYPE for t in rows)
    if bcount>2:return dict(reason='ACTUAL_HH_B2_CAP',B_count=bcount,bound=2)
    scope=(case['T']==3 and case['K'] in (12,13) and bcount==2 and
           all(t[1]<=1 and t[10]<=2*t[1] and (t[10]<2 or t[2]<=1) for t in rows))
    if scope:
        need(not column_records[case['K']],'joint column feasibility remains open')
        return dict(reason='DISJOINT_SINGLE_HUB_COLUMNS',K=case['K'],hub_weight=19,
                    heavy_entries=19-case['K'],distinct_B_hubs=True,
                    all_five_columns_positive=True,accepted_ordered_allocations=0)
    return dict(reason='OPEN')

def build():
    old=frozen();literal=json.loads((PARENT/'fixtures.json').read_text())
    raw,_=old.rows_and_physical_bridge(literal);selected=old.conservative_rows(literal,raw)
    types=sorted({tuple(r['coordinates']) for r in selected})
    need(len(raw)==426 and len(selected)==410 and len(types)==51 and BTYPE in types,'complete conservative physical carrier')
    calibration={K:columns(K) for K in (12,13,14)}
    need(not calibration[12] and not calibration[13] and calibration[14],'two target residues absent, relaxed support control positive')
    branches=[];maximum=0
    for case in cases():
        vectors,states=old.produce(types,case);maximum=max(maximum,states)
        rows=[dict(vector=v,certificate=certificate(types,case,v,old,calibration)) for v in vectors]
        branches.append(dict(case=case,rows=rows))
    return dict(actual_marks=raw,conservative_marks=selected,types=types,scalar_cases=cases(),
                branches=branches,ordered_column_calibration=calibration),dict(max_coefficient_states=maximum)
