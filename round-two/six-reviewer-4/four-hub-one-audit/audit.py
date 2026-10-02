"""Independent labelled necessary-image audit, exact Boolean row factors.
The columns use fixed support sizes and an individual-row product, without
weak-composition factors, min/max requirements, or target expected data.
"""
from itertools import combinations, product, permutations
from collections import Counter
from pathlib import Path
from functools import lru_cache
import json, hashlib, time, argparse
from rows import encoded,need
from populations import prefix_product, endpoints,weights

PAIRS=tuple(combinations(range(4),2))
TRIPLES=tuple(combinations(range(4),3))

def populations(types, allowed):
    start=time.monotonic(); out=[]
    for tau in range(3):
        for x in range(5):
            for q in range(9):
                slack=8-q-2*x-4*tau
                if slack<0: continue
                e=16-q-2*tau; k=24-e+2*x
                small,cost=prefix_product([types[i] for i in allowed],e,k,q,x,3*slack)
                vectors=[]
                for v in small:
                    full=[0]*len(types)
                    for i,n in zip(allowed,v):full[i]=n
                    vectors.append(full)
                records=[]
                for v in vectors:
                    got=[sum(c*w[d] for c,t in zip(v,types) for w in [weights(t)]) for d in range(6)]
                    need(got[:5]==[14,e,k,q,2*x] and got[5]<=3*slack,'all recovered charges')
                    need(sum(c*t[5] for c,t in zip(v,types))<=0,'selector capacity')
                    records.append({'counts':v,'failure':endpoints(types,v),'K':k})
                out.append({'tau':tau,'X':x,'Q':q,'E':e,'K':k,'records':records,'cost':cost})
                need(time.monotonic()-start<60,'INCOMPLETE population60s guard')
    return out

def carriers():
    labelled=[]; canonical=set()
    for selected in combinations(range(4),2):
        mask=sum(1<<i for i in selected)
        t=tuple(sum(set(pair)<=set(TRIPLES[i]) for i in selected) for pair in PAIRS)
        ranges=[range(ti,(14+ti)//3+1) for ti in t]
        for lambdas in product(*ranges):
            if sum(lambdas)!=22: continue
            d=tuple(sum(lam for pair,lam in zip(PAIRS,lambdas) if a in pair)-(2 if a==0 else 6) for a in range(4))
            if not (5<=d[0]<=12 and all(1<=x<=9 for x in d[1:])): continue
            if any(not 8<=d[a]+d[b]<=13 for a,b in combinations((1,2,3),2)): continue
            if any(d[0]+d[a]>16 for a in (1,2,3)): continue
            row=(mask,lambdas,d,t)
            labelled.append(row)
            orbit=[]
            for perm in permutations((1,2,3)):
                p=(0,)+perm
                mm=sum(1<<i for i,tr in enumerate(TRIPLES)
                       if mask>>(TRIPLES.index(tuple(sorted(p[a] for a in tr))))&1)
                ll=tuple(lambdas[PAIRS.index(tuple(sorted((p[a],p[b]))))] for a,b in PAIRS)
                orbit.append((mm,ll))
            if (mask,lambdas)==min(orbit): canonical.add(row)
    need(len(labelled)==len(set(labelled)),'unique labelled carriers')
    return sorted(labelled),sorted(canonical)

def column_choices(vector, options, mask, a, deficit):
    choices=[]
    for tid,multiplicity in enumerate(vector):
        if not multiplicity:continue
        local=set()
        for mm in (0,1,2,4,8):
            if mm & mask == mm: local.update(options.get((tid,mm,a),()))
        if not local:return ()
        choices.extend([tuple(sorted(local))]*multiplicity)
    accepted=[]
    for n in range(1,deficit+1):
        state={(0,0,0)}
        for local in choices:
            factor={(d,int(d>0),l&1) for d,l in local if not d or l<n}
            nextstate=set()
            for w,k,parity in state:
                for d,positive,l in factor:
                    if w+d<=deficit and k+positive<=n:
                        nextstate.add((w+d,k+positive,parity^l))
            state=nextstate
            if not state:break
        if (deficit,n,0) in state:accepted.append(n)
    return tuple(accepted)

def joint(ns,k,lambdas,t):
    # Derive the fourth coordinate, then check all six conditions together.
    if any(not s for s in ns):return ()
    out=[]
    for n0,n1,n2 in product(*ns[:3]):
        n=(n0,n1,n2,k-n0-n1-n2)
        if n[3] not in ns[3]:continue
        if all(14-3*lam+ta <= n[a]+n[b] for (a,b),lam,ta in zip(PAIRS,lambdas,t)):
            out.append(n)
    return tuple(sorted(out))

def run(physical):
    types=[(t[0],t[1],t[2],t[3],tuple(t[4]),t[5],t[6]) for t in physical['types']]
    options={tuple(key):tuple(tuple(x) for x in vals) for key,vals in physical['options']}
    branches=populations(types,[i for i,n in physical['frequency']])
    passed=[(b,r) for b in branches for r in b['records'] if r['failure'] is None]
    labelled,normal=carriers()
    stream=hashlib.sha256(); histogram=Counter(); survivors=[]; total=0;start=time.monotonic()
    @lru_cache(None)
    def cached(index,mask,a,d):
        return column_choices(passed[index][1]['counts'],options,mask,a,d)
    for index,(b,r) in enumerate(passed):
        for mask,lams,d,t in normal:
            ns=tuple(cached(index,mask,a,d[a]) for a in range(4))
            accepted=joint(ns,r['K'],lams,t)
            row=[index,mask,lams,d,t,ns,accepted]
            stream.update(encoded(row));total+=1
            histogram['accepted' if accepted else 'empty-coordinate' if any(not n for n in ns) else 'coupled-empty']+=1
            if accepted:survivors.append(row)
        need(time.monotonic()-start < 60,'INCOMPLETE joint60s guard')
    return {'raw_types':types,'branches':branches,'preliminary':len(passed),'labelled_carriers':len(labelled),
            'canonical_carriers':len(normal),'carriers_sha256':hashlib.sha256(encoded(normal)).hexdigest(),
            'joint_records':total,'joint_sha256':stream.hexdigest(),'histogram':dict(histogram),'survivors':survivors}

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--physical',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    z=run(json.loads(a.physical.read_bytes()));a.out.write_bytes(encoded(z))
    print(json.dumps({k:z[k] for k in ('preliminary','labelled_carriers','canonical_carriers','joint_records','joint_sha256','histogram')},sort_keys=True))
