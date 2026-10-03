"""New P22/T0 charge enumeration; explicitly reused prior426 physical engines.
No target9884 executable, expectation or compact certificate has been read.
"""
import collections,functools,itertools as it,json,time
from independent import local,expand_vertices,potential,old_failures,enc,P,need

def branches():
    return [dict(Q=q,X=x,tau=t,E=18-q-2*t,K=6+q+2*x+2*t,
                 budget=3*(12-q-2*x-4*t))
            for t in range(4) for x in range(7) for q in range(13)
            if q+2*x+4*t<=12]

def vectors(types,accepted,b):
    C=[(1,t[0],t[1],t[2],t[6],t[8]) for t in types]
    target=(14,b['E'],b['K'],b['Q'],2*b['X'],b['budget'])
    need(C[0]==(1,0,0,0,0,0) and C[1]==(1,0,1,0,0,1),'unit completion')
    order=sorted([i for i in accepted if i not in (0,1) and all(C[i][j]<=target[j] for j in range(1,6))],
                 key=lambda i:(C[i][3]+C[i][4]>0,C[i][3],C[i][4],C[i][1],C[i][2]),reverse=True)
    columns=[C[i] for i in order]
    suffix=[[(min(a[j] for a in columns[p:]+C[:2]),max(a[j] for a in columns[p:]+C[:2]))
             for j in range(1,6)] for p in range(len(order)+1)]
    started=time.monotonic();states=0
    @functools.cache
    def coeff(p,s):
        nonlocal states
        states+=1
        if states>100000 or time.monotonic()-started>10:
            raise RuntimeError('INCOMPLETE unchanged100000-state/10-second branch guard')
        if p==len(order):return int(s[1]==s[3]==s[4]==0 and 0<=s[2]<=min(s[0],s[5]))
        if s[0]==0:return int(s[1]==s[2]==s[3]==s[4]==0)
        for j,(lo,hi) in enumerate(suffix[p],1):
            if s[j]<s[0]*lo or (j<5 and s[j]>s[0]*hi):return 0
        a=columns[p]
        if any(s[j]==0 and a[j]>0 for j in (1,2,3,4,5)):
            return coeff(p+1,s) # all positive multiplicities of this factor impossible
        M=min([s[0]]+[s[j]//a[j] for j in range(1,6) if a[j]])
        return sum(coeff(p+1,tuple(s[j]-m*a[j] for j in range(6))) for m in range(M+1))
    total=coeff(0,target);out=[]
    def expand(p,s,path):
        if p==len(order):
            v=[0]*len(types);v[1]=s[2];v[0]=s[0]-s[2]
            for i,m in zip(order,path):v[i]=m
            out.append(v);return
        a=columns[p];M=min([s[0]]+[s[j]//a[j] for j in range(1,6) if a[j]])
        for m in range(M+1):
            child=tuple(s[j]-m*a[j] for j in range(6))
            if coeff(p+1,child):expand(p+1,child,path+[m])
    if total:expand(0,target,[])
    need(total==len(out)==len({tuple(v) for v in out}),'complete coefficients vs positive-path vector census')
    for v in out:
        totals=[sum(n*a[j] for n,a in zip(v,C)) for j in range(6)]
        need(totals[:5]==list(target[:5]) and totals[5]<=target[5],'exact vector charges')
    return sorted(out),states

def main():
    stars,rows,types,hist=local()
    data=json.loads((P/'physical22.json').read_text());accepted=data['accepted_types']
    records=[];survivors=[];counts=collections.Counter();start=time.monotonic()
    for ordinal,b in enumerate(branches()):
        vs,states=vectors(types,accepted,b);tests=[]
        for v in vs:
            V=expand_vertices(types,hist,v);fail=old_failures(V,potential(V))
            tests.append(dict(counts=v,all_failures=fail));counts['vectors']+=1
            counts[fail[0] if fail else 'preliminary_survivors']+=1
            if not fail:survivors.append(dict(branch=b,counts=v))
        records.append(dict(branch=b,states=states,complete_vectors=tests))
        print(json.dumps(dict(branch=ordinal,states=states,vectors=len(vs),seconds=time.monotonic()-start)),flush=True)
    result=dict(fields=('e','k','q','eligible','h','g1','sigma','psi','margin'),
                types=types,histograms=hist,branches=records,survivors=survivors,summary=counts)
    (P/'census22.json').write_bytes(enc(result));print(json.dumps(dict(summary=counts,branches=len(records)),sort_keys=True),flush=True)

if __name__=='__main__':main()
