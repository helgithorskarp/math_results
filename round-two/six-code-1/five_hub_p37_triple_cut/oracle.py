"""Separate exact P37/T>=3 oracle; six-code-1, researcher.

Imports no new producer or expected record. Ordered column D-compositions
and bounded supports differ from the producer's support-first product.
"""
from collections import Counter
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'five_hub_pair_total36'
FIELDS=('e','k','q','eligible','h','c1','psi','mu','sigma','I5','hub_weight')

def need(ok,message):
    if not ok:raise ValueError(message)

def frozen():
    manifest=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for name,sha in manifest['frozen_source_sha256'].items():
        need(hashlib.sha256((PARENT/name).read_bytes()).hexdigest()==sha,'changed frozen mathematical source')
    spec=importlib.util.spec_from_file_location('p37_triple_parent_oracle',PARENT/'oracle.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def cases():
    out=[]
    for T,X,tau,Q in it.product(range(3,9),range(8),range(4),range(16)):
        if 2*T+2*X+4*tau+Q>15:continue
        out.append(dict(T=T,X=X,tau=tau,N5=0,Q=Q,E=17-T-2*tau-Q,
                        K=2+T+2*tau+Q+2*X,margin_budget=3*(15-2*T-2*X-4*tau-Q)))
    return sorted(out,key=lambda c:(c['T'],c['X'],c['tau'],c['Q']))

def columns(K):
    start=time.monotonic();out=[];nodes=0
    # Four bars among18 positions encode all positive five-compositions of19.
    for bars in it.combinations(range(18),4):
        D=(bars[0]+1,bars[1]-bars[0],bars[2]-bars[1],bars[3]-bars[2],18-bars[3])
        need(sum(D)==19 and min(D)>0,'complete actual positive deficit composition')
        if max(D)>8 or sum(sorted(D,reverse=True)[:2])>11:continue
        choices=[]
        for a,d in enumerate(D):
            choices.append([N for N in range(1,d+1) if d-N<=N and
                            (d==N or N>=3) and (a>=2 or N>=4 and d>N)])
        for N in it.product(*choices):
            nodes+=1
            need(nodes<=100000 and time.monotonic()-start<=10,'INCOMPLETE column100000-state/10s guard')
            if sum(N)!=K:continue
            n=tuple(d-s for d,s in zip(D,N));out.append(dict(N=N,n=n,D=D))
    return sorted(out,key=lambda r:(r['N'],r['n'],r['D']))

def check_vector(types,case,v):
    need(len(v)==len(types) and all(type(n) is int and n>=0 for n in v),'complete integer count vector')
    totals=[sum(v)]+[sum(types[j][i]*v[j] for j in range(len(types))) for i in [0,1,2,8,9,10]]
    need(totals==[13,case['E'],case['K'],case['Q'],2*case['X'],0,19],'every literal weighted/support total')
    need(sum(types[j][7]*v[j] for j in range(len(types)))<=case['margin_budget'],'margin upper budget')

def certificate(types,case,v,old,column_records):
    check_vector(types,case,v);prior=old.direct_capacity(types,v)
    if prior['reason']!='OPEN':return dict(reason='FROZEN_ENDPOINT_RADIUS_OR_CLOSURE',cut=prior)
    vertices=[]
    for i in range(len(types)):
        for _ in range(v[i]):vertices.append(dict(zip(FIELDS,types[i])))
    units={j for j,t in enumerate(vertices) if t['e']==0}
    eligible={j for j,t in enumerate(vertices) if t['eligible']}
    A=units-eligible;V=units&eligible;C=set(range(13))-units-eligible;B=eligible-units
    degree=lambda j:vertices[j]['h']-vertices[j]['k']
    R=sum(vertices[j]['k']==0 for j in units);DA=sum(degree(j) for j in A);DV=sum(degree(j) for j in V)
    rawI=sum(min(degree(j),len(A)-1) for j in A);even=rawI-rawI%2
    C1=sum(vertices[j]['c1'] for j in C);required=DV+(R if R>DA-even else DA-even)
    if R>0 and len(V|B)>0 and required>C1:
        return dict(reason='9538_ROOT_ENDPOINT_C1',R=R,D_A=DA,D_V=DV,I_even=even,C1=C1,required=required)
    bcount=sum(t['e']==1 and t['k']==1 and t['q']==0 and t['eligible'] and t['hub_weight']==2 for t in vertices)
    if bcount>=3:return dict(reason='ACTUAL_HH_B2_CAP',B_count=bcount,bound=2)
    singleton=all(t['k']<=1 and t['hub_weight']<=t['k']+t['k'] and
                  (t['hub_weight']!=2 or t['q']<=1) for t in vertices)
    if case['T']==3 and case['K'] in [12,13] and bcount==2 and singleton:
        need(len(column_records[case['K']])==0,'actual single-hub columns not excluded')
        return dict(reason='DISJOINT_SINGLE_HUB_COLUMNS',K=case['K'],hub_weight=19,
                    heavy_entries=19-case['K'],distinct_B_hubs=True,
                    all_five_columns_positive=True,accepted_ordered_allocations=0)
    return dict(reason='OPEN')

def build():
    old=frozen();literal=json.loads((PARENT/'fixtures.json').read_text())
    raw,selected=old.physical_rows(literal);types=sorted({tuple(r['coordinates']) for r in selected})
    need(len(raw)==426 and len(selected)==410 and len(types)==51,'full physical mark carrier')
    calibration={K:columns(K) for K in [12,13,14]}
    need(len(calibration[12])==len(calibration[13])==0 and len(calibration[14])>0,'negative targets and positive relaxed control')
    branches=[];maximum=0
    for case in cases():
        vectors,states=old.coefficient_vectors(types,case);maximum=max(maximum,states)
        rows=[dict(vector=v,certificate=certificate(types,case,v,old,calibration)) for v in vectors]
        branches.append(dict(case=case,rows=rows))
    return dict(actual_marks=raw,conservative_marks=selected,types=types,scalar_cases=cases(),
                branches=branches,ordered_column_calibration=calibration),dict(max_coefficient_states=maximum)
