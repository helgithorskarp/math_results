#!/usr/bin/env python3
"""Certificate discovery only. Requires python-flint==0.8.0."""
from pathlib import Path
from collections import deque
from itertools import combinations
from functools import reduce
from math import gcd,lcm
import argparse,hashlib,json
from flint import fmpq,fmpq_mat,nmod_mat
D=Path(__file__).resolve().parent
SOURCE=D.parent/'hadwiger_nelson_h516_k23free_edge_repair/graph.json'
def oddwheel(adj):
    for hub in sorted(adj):
        S=adj[hub];col={};par={}
        for root in sorted(S):
            if root in col:continue
            col[root]=0;par[root]=None;queue=deque([root])
            while queue:
                u=queue.popleft()
                for v in sorted(adj[u]&S):
                    if v not in col:col[v]=1-col[u];par[v]=u;queue.append(v)
                    elif col[v]==col[u]:
                        pu=[];pv=[];a=u;b=v
                        while a is not None:pu.append(a);a=par[a]
                        while b is not None:pv.append(b);b=par[b]
                        z=next(x for x in pu if x in pv)
                        return {'type':'odd_wheel','hub':hub,'rim':pu[:pu.index(z)+1]+list(reversed(pv[:pv.index(z)]))}
    return None
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    G=json.loads(SOURCE.read_text());V=G['labels'];ix={v:i for i,v in enumerate(V)};E={tuple(e) for e in G['edges']};A={v:set() for v in V}
    for u,v in E:A[u].add(v);A[v].add(u)
    cycles=set()
    for u,v in combinations(V,2):
        for b,d in combinations(sorted(A[u]&A[v]),2):
            q=[u,b,v,d];cycles.add(min(tuple(r[i:]+r[:i]) for r in (q,list(reversed(q))) for i in range(4)))
    pairs=sorted({tuple(sorted((q[i],q[i+2]))) for q in cycles for i in range(2)})
    blocked={}
    for u,v in pairs:
        key=f'{u},{v}'
        if (u,v) in E:blocked[key]={'type':'edge'};continue
        B={x:{u if y==v else y for y in A[x]} for x in V if x!=v};B[u]|=A[v]
        w=oddwheel(B)
        if w:blocked[key]=w
    C=[q for q in sorted(cycles) if all(','.join(map(str,sorted((q[i],q[i+2])))) in blocked for i in range(2))]
    rows=[]
    for q in C:
        r=[0]*len(V)
        for j,v in enumerate(q):r[ix[v]]=(-1)**j
        rows.append(r)
    rows.append([int(v==0) for v in V]);M,rk=fmpq_mat(rows).rref()
    piv=[next(j for j in range(len(V)) if M[r,j]) for r in range(rk)];free=[j for j in range(len(V)) if j not in piv];k=len(free)
    sig={j:[fmpq(int(j==h)) for h in free] for j in free}
    for r,j in enumerate(piv):sig[j]=[-M[r,h] for h in free]
    gram=[]
    for u,v in G['edges']:
        diff=[x-y for x,y in zip(sig[ix[u]],sig[ix[v]])]
        gram.append([(1 if i==j else 2)*diff[i]*diff[j] for i in range(k) for j in range(i,k)])
    p=1000000007
    def mod(x):return int(x.numerator)%p*pow(int(x.denominator),-1,p)%p
    aug=nmod_mat([[mod(x) for x in r]+[1] for r in gram],p);N,ar=aug.transpose().rref()
    select=[next(j for j in range(len(gram)) if N[r,j]) for r in range(ar)]
    F,rank=fmpq_mat([gram[j] for j in select]).transpose().rref()
    ip=[next(j for j in range(len(select)) if F[r,j]) for r in range(rank)];jf=next(j for j in range(len(select)) if j not in ip)
    lam=[fmpq(0) for _ in select];lam[jf]=fmpq(1)
    for r,j in enumerate(ip):lam[j]=-F[r,jf]
    den=lcm(*(int(x.denominator) for x in lam));ints=[int(x*den) for x in lam];g=reduce(gcd,ints);ints=[x//g for x in ints]
    if sum(ints)<0:ints=[-x for x in ints]
    support=[(idx,val) for idx,val in zip(select,ints) if val]
    if not sum(ints) or any(sum(val*gram[idx][j] for idx,val in support) for j in range(len(gram[0]))):raise ValueError('no exact contradictory norm identity')
    used={','.join(map(str,sorted((q[i],q[i+2])))) for q in C for i in range(2)}
    out={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'cycles':C,
        'diagonal_obstructions':{key:blocked[key] for key in sorted(used)},'translation_anchor':0,
        'rank_prime':p,'affine_rank':rk,'free_labels':[V[j] for j in free],
        'parametrization':[[[h,int(x.numerator),int(x.denominator)] for h,x in enumerate(sig[j]) if x] for j in range(len(V))],
        'norm_weights':[[G['edges'][idx][0],G['edges'][idx][1],val] for idx,val in support],'weight_sum':sum(ints)}
    a.output.write_text(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n')
    print(json.dumps({'written':str(a.output),'cycles':len(C),'norm_support':len(support),'unit_sum':sum(ints),'bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
