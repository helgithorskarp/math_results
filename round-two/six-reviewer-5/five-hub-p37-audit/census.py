"""Owned9527 counting DAG reused for NEW P36 domain; no target author imports.

The two prior row reconstructors are explicitly reused from reviewer9422.
Target defining mathematics is known; new executable/expected are unread.
"""
import collections,functools,hashlib,itertools as it,json,pathlib,time
import prior_rows,prior_bit_rows

P=pathlib.Path(__file__).resolve().parent
FIELDS=('e','k','q','eligible','h','c1','c2','psi','I5','mu')

def need(ok,message):
    if not ok:raise ValueError(message)
def encode(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(encode(x)).hexdigest()

def raw_and_types(stars):
    raw=prior_rows.marks(stars)
    need(raw==prior_bit_rows.literal_rows(stars),'every426 prior set/bit row field')
    capped=[]
    for r in raw:
        H=set(r['hubs'])
        if any(r['delta'][a]>(3 if a in H else 2) for a in r['high']):continue
        sat=[a for a in r['high'] if a not in H]
        c1=sum(r['delta'][a]==1 for a in sat)
        c2=sum(r['delta'][a]==2 for a in sat)
        need(c1+c2==r['h']-r['k'] and c2==r['sigma'],'complete actual support/color roles')
        capped.append({**r,'c1':c1,'c2':c2,'mu':r['margin']})
    types=sorted({tuple(r[k] for k in FIELDS) for r in capped})
    return raw,capped,types

def scalars():
    out=[]
    # Ordinary inequality plus Q>=4I gives these finite rectangular bounds.
    for I,T,X,tau,Q in it.product(range(4),range(1,6),range(5),range(3),range(15)):
        E=14-T-2*tau-Q;K=17-E+2*X;budget=3*(E+Q+I-K)
        if Q>=4*I and 2*T+2*X+4*tau+Q-I<=11 and E>=0 and K>=0 and budget>=0:
            out.append({'N5':I,'T':T,'X':X,'tau':tau,'Q':Q,'E':E,'K':K,'margin_budget':budget})
    return out

def populations(types,case):
    charges=[(1,c[0],c[1],c[2],c[6],c[8],c[9]) for c in types]
    target=(13,case['E'],case['K'],case['Q'],2*case['X'],case['N5'],case['margin_budget'])
    active=[i for i,a in enumerate(charges) if all(a[j]<=target[j] for j in range(7))]
    active.sort(key=lambda i:(sum(charges[i][j] for j in (1,3,4,5,6)),charges[i]),reverse=True)
    columns=[charges[i] for i in active]
    # Prefix-free counting DAG: each factor chooses its full multiplicity once.
    # Counts alone are computed first; a second walk expands positive paths.
    suffix=[]
    for pos in range(len(columns)+1):
        rest=columns[pos:]
        suffix.append([(min(r[j] for r in rest),max(r[j] for r in rest)) for j in range(1,7)] if rest else [])
    states=0;started=time.monotonic()
    @functools.cache
    def count(pos,state):
        nonlocal states
        states+=1
        need(states<=100000,'INCOMPLETE fixed100000-state guard')
        need(time.monotonic()-started<10,'INCOMPLETE fixed10s branch guard')
        n=state[0]
        if pos==len(columns):return int(all(v==0 for v in state[:6]))
        for j,(lo,hi) in enumerate(suffix[pos],1):
            if state[j]<n*lo or (j<6 and state[j]>n*hi):return 0
        a=columns[pos]
        maximum=min([n]+[state[j]//a[j] for j in range(1,7) if a[j]])
        total=0
        for m in range(maximum+1):
            child=tuple(state[j]-m*a[j] for j in range(7))
            total+=count(pos+1,child)
        return total
    expected=count(0,target);found=[]
    def expand(pos,state,path):
        if pos==len(columns):
            need(all(v==0 for v in state[:6]),'positive terminal exact totals')
            vector=[0]*len(types)
            for index,n in zip(active,path):vector[index]=n
            found.append(tuple(vector));return
        a=columns[pos]
        maximum=min([state[0]]+[state[j]//a[j] for j in range(1,7) if a[j]])
        for m in range(maximum+1):
            child=tuple(state[j]-m*a[j] for j in range(7))
            if count(pos+1,child):expand(pos+1,child,path+[m])
    if expected:expand(0,target,[])
    need(len(found)==len(set(found))==expected,'whole positive path expansion equals count-DAG root')
    for vector in found:
        actual=tuple(sum(n*a[j] for n,a in zip(vector,charges)) for j in range(7))
        need(actual[:6]==target[:6] and actual[6]<=target[6],'every complete population exact totals')
    return sorted(found),states

def metrics(types,vector):
    r={k:0 for k in ('U','A','C','B','D','I','C1','C2','B2','R','closed_root')}
    A=sum(n for n,c in zip(vector,types) if c[0]==0 and not c[3])
    r['A']=A
    for n,c in zip(vector,types):
        if not n:continue
        e,k,q,eligible,h,c1,c2,psi,I5,mu=c
        degree=c1+c2
        if e==0:
            r['U']+=n;r['D']+=n*degree
            if not eligible:r['I']+=n*min(degree,A-1)
            if k==0:r['R']+=n;r['closed_root']+=n
        elif eligible:
            r['B']+=n;r['B2']+=n*c2
        else:
            r['C']+=n;r['C1']+=n*c1;r['C2']+=n*c2
            if k==0:r['closed_root']+=n
    return r

def failures(r):
    out=[]
    if r['D']>r['I']+r['C1']:out.append('unit_endpoint')
    if r['R'] and r['B'] and r['C1']+r['C2']<r['R']+r['B']:out.append('distinct_crossing')
    if r['B'] and r['closed_root'] and r['D']==r['I']+r['C1'] and (r['C2']==0 or r['B2']==0):out.append('all_color_closure')
    return out

def stronger_graph_cut(types,vector,r):
    if not(r['R'] and r['B']):return {'active':False}
    need_edges=max(r['R'],r['D']-r['I'])+r['B']
    paths=0
    for n,c in zip(vector,types):
        if n and c[0]>0 and not c[3]:
            d=c[5]+c[6]
            phi=max(a*min(r['B'],d-a) for a in range(min(r['R'],c[5])+1))
            paths+=n*phi
    return {'active':True,'joint_endpoint_demand':need_edges,'available_C_support':r['C1']+r['C2'],
            'root_B_pair_demand':r['R']*r['B'],'maximum_local_common_neighbor_paths':paths,
            'violates_joint_endpoint':r['C1']+r['C2']<need_edges,
            'violates_root_pair_cover':r['R']*r['B']>paths}

