"""Bounded original-set/closed-form comparisons; infinite proof is in PROOF.md."""
from pathlib import Path
from fractions import Fraction as F
import sys, json, signal, time, resource, importlib.util
from hashlib import sha256
from builder import build, record
from sectors import check_reduced
from exact import require, matvec, vecadd, scale, unit, gram, dot, psd_rank, fingerprint, lift, nullspace

def forms(C,vs):
    images=[matvec(C,v) for v in vs]
    G=[[dot(v,x) for x in images] for v in vs]
    S=[[dot(u,v)+sum(u)*sum(v) for v in images] for u in images]
    return G,S

def baseline():
    path=Path(__file__).with_name('baseline9408.py')
    spec=importlib.util.spec_from_file_location('credited9408_mixed',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    oldfamily,olds,oldC,oldW,_=mod.build(3)
    family,C,W,p,*_=build(3,1,1)
    require((family,p['s'],C,W)==(oldfamily,olds,oldC,oldW),'all prior9408 original Gram/residual positions')
    return {'source':'f8255e1d617237421c32b3d1e13dd865bffd50c4',
            'n':3,'N':16,'Gram_positions':225,'residual_positions':16,
            'core_sha256':fingerprint(C),'status':'exact baseline validation only'}

def compare(n,r,l,mean_recipe='legacy'):
    family,C,W,p,B,P,V,K=build(n,r,l,mean_recipe=mean_recipe);N=p['N'];q=p['q'];oldN=2*q-1;dim=oldN+p['m']
    small,pars=check_reduced(q,r,l,mean_recipe)
    for key in ('d','g','A','D','Fp','a','c','etaL','etaF','etaP','R','mu','alpha','beta','cross','a_mean','b_mean'):
        require(p[key]==pars[key],'independent projection/residual scalar '+key)
    def embed(v):
        out=[F(0)]*(N-1);out[:oldN]=v[:oldN]
        for i in range(p['m']):out[oldN+2*i+1]=v[oldN+i]
        return out
    V=[embed(v) for v in V]
    H=[[-F(i<oldN and bool((i+1)&(1<<j))) for i in range(N-1)] for j in range(r+l)]
    oldG=[F(i<oldN) for i in range(N-1)];f=unit(N-1,oldN-1)
    gp=scale(F(1,2),vecadd(oldG,scale(-1,f)));h0=scale(F(-1,2),vecadd(oldG,f))
    As=[vecadd(h,scale(-1,h0)) for h in H]
    hs=[scale(F(1,3),vecadd(*V[3*j:3*j+3])) for j in range(r)]
    T=[vecadd(V[3*j+a],scale(-1,hs[j])) for j in range(r) for a in range(3)]
    Ta=[vecadd(T[3*j],scale(-1,T[3*j+1])) for j in range(r)]
    Ts=[vecadd(T[3*j],T[3*j+1],scale(-2,T[3*j+2])) for j in range(r)]
    Z=[vecadd(V[3*r+j],scale(F(-1,3),H[r+j])) for j in range(l)]
    private=[oldN+2*i for i in range(p['m'])]
    Ws=[vecadd(unit(N-1,private[i]),scale(-1,embed(P[i]))) for i in range(p['m'])]
    means=[scale(F(1,3),vecadd(*Ws[3*j:3*j+3])) for j in range(r)]
    light=Ws[3*r:]
    Wa=[vecadd(Ws[3*j],scale(-1,Ws[3*j+1])) for j in range(r)]
    Wf=[vecadd(Ws[3*j+2],scale(-1,means[j])) for j in range(r)]
    features={'anti':[Ta[0],Wa[0]],
              'fixed':[gp,h0,vecadd(*As[:r]),vecadd(*As[r:]),vecadd(*Ts),vecadd(*Z),vecadd(*Wf),vecadd(*means)]}
    if r>1:
        features['triangle_standard']=[vecadd(v[0],scale(-1,v[1])) for v in (As,Ts,means,Wf)]
    if l>1:
        features['pendant_standard']=[vecadd(v[0],scale(-1,v[1])) for v in (As[r:],Z,light)]
    positions=0
    for label,vs in features.items():
        G,S=forms(C,vs)
        require((G,S)==small[label],'EVERY literal/closed Gram and actual-empty frame position '+label)
        positions+=len(vs)**2
    changed=[gp,h0]+As+Ta+Ts+Z+Wa+Wf+means+light[:-1]
    dimension=6*r+3*l+1
    require(len(changed)==dimension,'complete changed dimension count')
    G,S=forms(C,changed)
    require(psd_rank(G)==dimension,'independent literal changed Gram')
    cap=[[(N-1)*G[i][j]-S[i][j] for j in range(dimension)] for i in range(dimension)]
    require(psd_rank(cap)==dimension,'complete literal changed cap')
    M=lift(C,p['s']);Q=[[(N-p['s'])*M[i][j]+p['s']*int(i==j)-1 for j in range(N)] for i in range(N)]
    pairs=[(a,(2*q-1)^a) for a in range(1,2*q-1) if a<((2*q-1)^a)]
    high=[]
    for a,b in pairs[1:]:
        v=[F(0)]*N
        for z in (a,b):v[z]+=1
        for z in pairs[0]:v[z]-=1
        high.append(v)
    kernel=nullspace([[F(bool(a&(1<<j)))-F(bool(b&(1<<j))) for a,b in pairs] for j in range(r+l)],len(pairs))
    low=[]
    for z in kernel:
        v=[F(0)]*N
        for value,(a,b) in zip(z,pairs):v[a]+=value;v[b]-=value
        low.append(v)
    require(len(high)==q-2 and len(low)==q-r-l-1,'actual untouched multiplicities')
    for vs,eigenvalue in ((high,2*q),(low,6)):
        for v in vs:require(matvec(Q,v)==scale(eigenvalue,v),'actual eigenaction includes empty/private/marked rows')
    report=record(n,r,l,mean_recipe)
    require(report['status']=='literal repaired cap at greatest rank; no uniform theorem','full seed/repair completed')
    return {'n':n,'r':r,'l':l,'q':q,'N':N,'Gram_positions':positions,'frame_positions':positions,
            'changed_dimension':dimension,'changed_Gram_positions':dimension**2,'changed_frame_positions':dimension**2,
            'untouched_high':len(high),'untouched_low':len(low),'whole':report}
