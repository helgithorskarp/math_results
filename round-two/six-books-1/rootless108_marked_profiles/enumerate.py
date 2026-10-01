from itertools import combinations,permutations
from pathlib import Path
import json,time,hashlib
START=time.monotonic();DEADLINE=START+45;CANON_NODES=0
BASE=Path(__file__).resolve().parent
def require(v,msg):
    if not v:raise ValueError(msg)
def decode(n,mask):
    g=[0]*n
    for k,(i,j) in enumerate(combinations(range(n),2)):
        if mask>>k&1:g[i]|=1<<j;g[j]|=1<<i
    return tuple(g)
def encode(g,order):
    return sum(1<<k for k,(i,j) in enumerate(combinations(order,2)) if g[i]>>j&1)
def canon(g,marked=None):
    global CANON_NODES
    n=len(g);cells=[]
    if marked is not None:cells.append((marked,))
    for d in range(4):
        cell=tuple(i for i in range(n) if i!=marked and g[i].bit_count()==d)
        if cell:cells.append(cell)
    def visit(cells):
        global CANON_NODES
        CANON_NODES+=1
        if CANON_NODES%10000==0 and time.monotonic()>DEADLINE:raise TimeoutError('INCOMPLETE canonical augmentation')
        while True:
            masks=[sum(1<<i for i in c) for c in cells];refined=[]
            for cell in cells:
                buckets={}
                for i in cell:
                    sig=tuple((g[i]&m).bit_count() for m in masks)
                    buckets.setdefault(sig,[]).append(i)
                for sig in sorted(buckets):refined.append(tuple(buckets[sig]))
            if len(refined)==len(cells):break
            cells=refined
        split=next((i for i,c in enumerate(cells) if len(c)>1),None)
        if split is None:return encode(g,tuple(c[0] for c in cells))
        cell=cells[split];best=None;previous=[]
        for v in cell:
            if any(g[v]&~((1<<v)|(1<<w))==g[w]&~((1<<v)|(1<<w)) for w in previous):continue
            previous.append(v)
            part=cells[:split]+[(v,),tuple(w for w in cell if w!=v)]+cells[split+1:]
            value=visit(part)
            if best is None or value<best:best=value
        return best
    return visit(cells)
def good(g):
    return max((x.bit_count() for x in g),default=0)<=3 and all(not(g[i]>>j&1 and g[i]&g[j]) and (g[i]&g[j]).bit_count()<=1 for i,j in combinations(range(len(g)),2))
def augment(g):
    n=len(g);available=[i for i,row in enumerate(g) if row.bit_count()<3]
    for size in range(4):
        for chosen in combinations(available,size):
            if any(g[i]>>j&1 or g[i]&g[j] for i,j in combinations(chosen,2)):continue
            mask=sum(1<<i for i in chosen);h=tuple(row|((1<<n) if mask>>i&1 else 0) for i,row in enumerate(g))+(mask,)
            yield h

def run():
    global DEADLINE
    DEADLINE=time.monotonic()+45
    models=[0];levels=[];small={}
    for n in range(1,10):
        new={0} if n==1 else {canon(h) for key in models for h in augment(decode(n-1,key))}
        models=sorted(new)
        require(all(good(decode(n,m)) for m in models),'invalid generated graph')
        levels.append(len(models))
        if n<=5:small[n]=list(models)
        if time.monotonic()>DEADLINE:raise TimeoutError('INCOMPLETE vertex augmentation')
    def brute(g):return min(encode(g,p) for p in permutations(range(len(g))))
    for n in (3,4,5):
        actual={brute(decode(n,m)) for m in range(1<<(n*(n-1)//2)) if good(decode(n,m))}
        require(actual=={brute(decode(n,m)) for m in small[n]},'small complete enumeration mismatch')
    dense=[m for m in models if sum(r.bit_count() for r in decode(9,m))>=20]
    raw=set();records=[]
    for mask in dense:
        F=decode(9,mask);edges=sum(r.bit_count() for r in F)//2
        available=[i for i,row in enumerate(F) if row.bit_count()<3]
        for size in range(4):
            if edges+size not in (13,14,15):continue
            for S in combinations(available,size):
                if any(F[i]>>j&1 for i,j in combinations(S,2)):continue
                J=(sum(1<<(i+1) for i in S),)+tuple((r<<1)|(i in S) for i,r in enumerate(F))
                key=canon(J,0)
                if key in raw:continue
                raw.add(key);g=decode(10,key);h=[r.bit_count() for r in g];w=[h[i]+2+(i==0) for i in range(10)]
                cap={}
                for i,j in combinations(range(10),2):
                    cap[i,j]=h[i]+h[j]-2-(g[i]&g[j]).bit_count()-(3-(i==0)-(j==0) if g[i]>>j&1 else 0)
                witness=None
                for sizeT in range(2,11):
                    for T in combinations(range(10),sizeT):
                        total=sum(w[i] for i in T);q,r=divmod(total,11)
                        low=11*q*(q-1)//2+r*q;up=sum(cap[i,j] for i,j in combinations(T,2))
                        if up<low:witness={'subset':list(T),'column_incidences':total,'lower':low,'upper':up};break
                    if witness:break
                records.append({'key':key,'edges':sum(h)//2,'local_degrees':h,'marked_degree':h[0],'packing_rejection':witness})
    records.sort(key=lambda r:r['key'])
    require(records==json.loads((BASE/'model.json').read_text()),'complete canonical records mismatch')
    require(levels==[1,2,3,6,10,20,38,83,183],'unmarked level mismatch')
    survivors=[r for r in records if r['packing_rejection'] is None]
    P=[sum(1<<j for j,y in enumerate(combinations(range(5),2)) if not(set(x)&set(y))) for x in combinations(range(5),2)]
    require(canon(P,0)==next(r['key'] for r in survivors if r['edges']==15),'Petersen identity mismatch')
    result={'complete':True,'unmarked_levels':levels,'dense9_classes':len(dense),'marked_classes':len(records),'packing_rejected':len(records)-len(survivors),'survivor_keys':[r['key'] for r in survivors],'edge_distribution':{str(e):sum(r['edges']==e for r in survivors) for e in (13,14,15)},'small_all_label_controls':[3,4,5],'petersen_positive_control':True}
    require(result==json.loads((BASE/'expected.json').read_text())['producer'],'expected producer result mismatch')
    return result
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
