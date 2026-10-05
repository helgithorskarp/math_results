"""Rational original-row producer for the newly proved small-cube closure.

six-downset-1 / researcher. Credited retained-vector/scalar/mean recipes
from published b7d26214, verbatim arithmetic below; only domain preflight changes.
This implementation uses a NEW separated M/WA/WF physical basis.
No predecessor executable, EXPECTED, factor or cap is imported.
The infinite theorem is an ordinary proof, not finite enumeration.
"""
from source_binding import verify_source as _verify_source
_verify_source()
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
              'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import signal

LIMIT_BYTES = 32*1024*1024

def require(ok,message):
    if not ok:
        raise ValueError(message)

def barrier():
    state = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state)/n).exists() for n in
            ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')

def preflight(n,counts):
    require(type(n) is int and 2<=n<=6,'proved small-cube domain and unchanged n<=6')
    require(type(counts) in (list,tuple) and 2<=len(counts)<=n
            and all(type(k) is int for k in counts),'literal distinct count/mark types')
    h=counts[0]
    require(3<=h<=10 and all(2<=k<h for k in counts[1:]),'unique heavy literal h<=10')
    F=sum(counts)
    require(F>=9,'qualified total F>=9')
    N=2**n+6*F
    require(N<=80,'unchanged original N80 parent guard BEFORE construction')
    return N

def vector(*terms):
    out={}
    for multiplier,v in terms:
        multiplier=Q(multiplier)
        for i,x in v.items():
            out[i]=out.get(i,Q(0))+multiplier*x
    return {i:x for i,x in out.items() if x}

def total(vs):
    return vector(*[(Q(1),v) for v in vs])

def unit(i):
    return {i:Q(1)}

def build(n,counts):
    barrier()
    N=preflight(n,counts)  # No original family/rows allocated above this line.
    counts=tuple(counts)
    r,h,q=len(counts),counts[0],2**(n-1)
    F,L,D0=sum(counts),sum(counts[1:]),3*h
    m,ell,s=3*F,3*F+1,q+3*h
    c0=Q(q*ell+9*sum(k*(h-k) for k in counts[1:])+3*h-6*F-1,ell**2)
    groups=[]
    for k in counts:
        v=Q(-(s-3*k-1),ell)
        R=1+v
        B2=Q(s*(k-1),3*k)
        a,c=R/(2*B2),9*R/(2*s)
        b=-2*a
        etaL=s-1-c0-a*a*B2-Q(2*s,3)*c*c
        etaF=s-1-c0-b*b*B2-Q(2*s,3*(k-1))*c*c
        pair=-1-c0-a*b*B2
        mu=(2*pair+etaF)/3
        alpha=2*(2*etaL-pair-etaF)
        beta=etaF-mu
        require(mu>0 and alpha>0 and beta>0,'positive exact scalar producer')
        groups.append(dict(k=Q(k),v=v,R=R,B2=B2,a=a,b=b,c=c,
            etaL=etaL,etaF=etaF,pair=pair,mu=mu,alpha=alpha,beta=beta))
    S=sum((k*g['mu'] for k,g in zip(counts,groups)),Q(0))
    SL=S-h*groups[0]['mu']
    for k,g in zip(counts,groups):
        g['off']=-k*g['mu']**2/(S*(k-1))
        g['nu']=g['mu']-g['off']
    kappa=1/(h*groups[0]['mu'])+1/SL+4*sum(
        (k*g['mu']**2/(SL*SL*g['beta']) for k,g in zip(counts[1:],groups[1:])),Q(0))
    d=N-3
    Gamma=[{} for _ in range(d)]
    def entry(i,j,x):
        x=Q(x)
        if x:
            Gamma[i][j]=x
    oldsize=2*q-1
    for i in range(oldsize):
        for j in range(oldsize):
            entry(i,j,s*(i==j)+(q-D0)*((i+1)^(j+1)==oldsize)-1)
    old=[unit(i) for i in range(oldsize)]
    H=[vector((-1,total([v for a,v in enumerate(old,1) if a&(1<<g)])))
       for g in range(r)]
    B=[];offset=oldsize
    for g,k in enumerate(counts):
        width=k-1 if g==0 else k
        for i in range(width):
            for j in range(width):
                entry(offset+i,offset+j,Q(s,3)*(Q(i==j)-Q(1,h)))
        bs=[unit(offset+i) for i in range(width)]
        if g==0:
            bs.append(vector((-1,total(bs))))
        B.append(bs)
        offset+=width
    means=[vector((Q(1,k),total(bs))) for k,bs in zip(counts,B)]
    contrasts=[[vector((1,v),(-1,mean)) for v in bs] for bs,mean in zip(B,means)]
    T=[]
    for f in range(F):
        entry(offset,offset,Q(2*s,3));entry(offset+1,offset+1,Q(2*s,3))
        entry(offset,offset+1,Q(-s,3));entry(offset+1,offset,Q(-s,3))
        u,v=unit(offset),unit(offset+1)
        T.append((u,v,vector((-1,u),(-1,v))))
        offset+=2
    retained_dimension=offset
    require(offset==2*q+3*F-2,'entire retained dimension')
    facetgroups=[g for g,k in enumerate(counts) for _ in range(k)]
    marked=[];starts=[];start=0
    for g,k in enumerate(counts):
        starts.append(start)
        for i in range(k):
            marked.extend(vector((Q(1,D0),H[g]),(1,B[g][i]),(1,t)) for t in T[start+i])
        start+=k
    K=total(old+marked)
    z0=vector((Q(-1,ell),K))
    projections=[]
    for g,k in enumerate(counts):
        p=groups[g];start=starts[g]
        for i in range(k):
            f=start+i
            projections.append(vector((1,z0),(p['a'],contrasts[g][i]),(p['c'],T[f][1])))
            projections.append(vector((1,z0),(p['a'],contrasts[g][i]),(p['c'],T[f][0])))
            others=total([T[start+j][2] for j in range(k) if j!=i])
            projections.append(vector((1,z0),(p['b'],contrasts[g][i]),(p['c']/(k-1),others)))
    mean=[]
    for i,gi in enumerate(facetgroups):
        a=groups[gi]
        row=[]
        for j,gj in enumerate(facetgroups):
            row.append(a['mu'] if i==j else a['off'] if gi==gj
                       else -a['mu']*groups[gj]['mu']/S)
        mean.append(row)
    require(all(sum(row,Q(0))==0 for row in mean),'whole facet mean row sums')
    M=[unit(offset+i) for i in range(F-1)]
    M.append(vector((-1,total(M))))
    for i in range(F-1):
        for j in range(F-1):
            entry(offset+i,offset+j,mean[i][j])
    offset+=F-1
    WA=[];WF=[]
    for f,g in enumerate(facetgroups):
        WA.append(unit(offset));entry(offset,offset,groups[g]['alpha']);offset+=1
        WF.append(unit(offset));entry(offset,offset,groups[g]['beta']);offset+=1
    require(offset==d,'entire separated positive physical dimension')
    residual=[]
    for f in range(F):
        residual.extend((vector((1,M[f]),(Q(1,2),WA[f]),(Q(-1,2),WF[f])),
                         vector((1,M[f]),(Q(-1,2),WA[f]),(Q(-1,2),WF[f])),
                         vector((1,M[f]),(1,WF[f]))))
    private=[vector((1,p),(1,w)) for p,w in zip(projections,residual)]
    rows=[z0]+old+marked+private
    require(len(rows)==N and not total(rows),'ACTUAL empty is negative sum of proper rows')
    family=[0]+list(range(1,2**n));marked_masks=[];private_masks=[]
    for f,g in enumerate(facetgroups):
        a,b=1<<(n+2*f),1<<(n+2*f+1)
        private_masks.extend((a,b,a|b))
        marked_masks.extend(((1<<g)|a,(1<<g)|b,(1<<g)|a|b))
    family+=marked_masks+private_masks
    a=[Q(0)]*(N-1);b=[Q(0)]*(N-1)
    private_start=oldsize+m
    for f,g in enumerate(facetgroups):
        for j in range(3):
            if g==0:
                a[private_start+3*f+j]=Q(1,h)
            elif j==2:
                b[private_start+3*f+j]=groups[g]['mu']/SL
    require(sum(a)==3 and sum(b)==1,'weighted proper repair normalization')
    p=[x-3*y for x,y in zip(a,b)]
    c=[(x+3*y)/6 for x,y in zip(a,b)]
    Mx=total(M[:h])
    dual=vector((S/(h*groups[0]['mu']*SL),Mx))
    for f,g in enumerate(facetgroups):
        if g:
            dual=vector((1,dual),(-2*groups[g]['mu']/(SL*groups[g]['beta']),WF[f]))
    def dense(v):
        return [str(v.get(i,Q(0))) for i in range(d)]
    return dict(version=1,agent='six-downset-1',role='researcher',n=n,counts=list(counts),
        N=N,s=s,q=q,F=F,ell=ell,dimension=d,retained_dimension=retained_dimension,
        family=family,metric=[[str(Gamma[i].get(j,Q(0))) for j in range(d)] for i in range(d)],
        rows=[dense(v) for v in rows],group_scalars=[{k:str(v) for k,v in g.items()} for g in groups],
        common_norm=str(c0),meanS=str(S),light_meanS=str(SL),kappa=str(kappa),
        a=[str(x) for x in a],b=[str(x) for x in b],p=[str(x) for x in p],
        c=[str(x) for x in c],dual_vector=dense(dual))

def main():
    def expire(a,b):
        raise TimeoutError('unchanged60s producer guard; incomplete is not nonexistence')
    signal.signal(signal.SIGALRM,expire);signal.alarm(60)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,default=4)
    parser.add_argument('--counts',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    counts=[int(x) for x in args.counts.split(',')]
    require(not args.out.exists(),'unique producer output')
    raw=json.dumps(build(args.n,counts),separators=(',',':')).encode()+b'\n'
    require(len(raw)<=LIMIT_BYTES,'unchanged32MiB generated record guard')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(raw)
    signal.alarm(0)
    print(json.dumps(dict(status='GENERATED UNTRUSTED ORIGINAL GEOMETRY',bytes=len(raw),
        counts=counts,n=args.n,new_source=None,new_graph=None)))

if __name__=='__main__':
    main()
