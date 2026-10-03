"""Fresh full function cover; literal rows and physical forests.
Independent of target data/native catalogue. No imported expected hashes.
"""
import json,sys
from collections import deque,Counter
from itertools import combinations
from engine import *
def local(word,k):
    result=[]
    for r in range(1<<k):
        x=[r>>i&1 for i in range(k)]
        for a,b in word:
            if x[a]>x[b]:x[a],x[b]=x[b],x[a]
        result.append(sum(v<<i for i,v in enumerate(x)))
    return tuple(result)
def semigroup():
    gens=tuple(combinations(range(3),2));ident=tuple(range(8));words={ident:()};todo=deque((ident,));edges=[]
    while todo:
        f=todo.popleft();w=words[f]
        for a,b in gens:
            target=tuple(v^((1<<a)|(1<<b)) if (v>>a&1)>(v>>b&1) else v for v in f)
            edges.append((f,(a,b),target))
            if target not in words:words[target]=w+((a,b),);todo.append(target)
    return sorted((w,f) for f,w in words.items()),edges

def forest(word):
    e={a:d for a,d in zip(DEAD,(11,11,11,13,11,12))};components={a:(a,) for a in DEAD};states=[]
    for a,b in word:
        require(a in e and b in e,'not a live binary');e[b]=max(e.pop(a),e[b])+1;components[b]=tuple(sorted(components.pop(a)+components[b]));states.append((tuple(sorted(e.items())),tuple(sorted(components.items()))))
    return e,states

def build(first_indices=None):
    base=[]
    for l,h in ((2,0),(0,2),(0,3)):
        records,classes,mass=profile(Q,l,h);base.append({'family':[l,h],'records':records,'classes':classes,'mass':mass})
    sem,edges=semigroup();projected=set()
    qcols=boolean(Q)
    for r in range(1<<N):projected.add(sum(((qcols[a]>>r)&1)<<j for j,a in enumerate(DEAD)))
    projected=tuple(sorted(projected));projection_bits={r:0 for r in projected}
    for inp in range(1<<N):
        r=sum(((qcols[a]>>inp)&1)<<j for j,a in enumerate(DEAD));projection_bits[r]|=1<<inp
    allhistory=[];kept=[];classes={};raw=[]
    def go(w,live):
        if len(w)<3:
            for gate_index,(a,b) in enumerate(combinations(live,2)):
                if not w and first_indices is not None and gate_index not in first_indices:continue
                go(w+((a,b),),tuple(x for x in live if x!=a))
            return
        e,states=forest(w);mass=sum(1<<d for d in e.values());status='mass' if mass>32768 else 'early' if w[0] in EARLY else 'kept'
        # Independent original-domain HIGH triple maxima, not recurrence.
        records,physical,pmass=profile(Q+w,0,3)
        actual={(hi&~((1<<11)|(1<<12))).bit_length()-1:d for lo,hi,d in physical}
        require(actual==e and pmass==mass,'physical original forest mismatch')
        allhistory.append({'word':w,'e':sorted(e.items()),'states':states,'mass':mass,'status':status,'records':records})
        if status!='kept':return
        kept.append(w);free=tuple(x for x in DEAD if x not in e)
        for g,_ in sem:
            G=tuple((free[a],free[b]) for a,b in g);word=w+G;lf=local(tuple((DEAD.index(a),DEAD.index(b)) for a,b in word),6)
            key=tuple(lf[r] for r in projected);candidate=(len(word),word)
            if key not in classes or candidate<classes[key]:classes[key]=candidate
            raw.append({'word':word,'function64':lf,'projected':key})
    go((),DEAD)
    representatives=[]
    for key,(length,w) in sorted(classes.items(),key=lambda kv:(kv[1][0],kv[1][1])):
        e,_=forest(w[:3]);full=boolean(Q+w)
        for j,a in enumerate(DEAD):
            lifted=sum(projection_bits[r] for r,value in zip(projected,key) if value>>j&1)
            require(full[a]==lifted,'wrong whole8192 original embedding')
        require(all(full[a]==qcols[a] for a in range(N) if a not in DEAD),'outside outputs changed')
        representatives.append({'word':w,'live':sorted(e),'function36':key,'full_columns_sha256':digest(full),'tails':{str(q):tails(q) for q in DEAD}})
    return {'base':base,'semigroup':sem,'semigroup_edges':edges,'projected36':projected,'histories':allhistory,'raw':raw,'representatives':representatives,'census':{'histories':len(allhistory),'statuses':dict(Counter(h['status'] for h in allhistory)),'semigroup':len(sem),'edges':len(edges),'projection':len(projected),'raw':len(raw),'classes':len(representatives)}}
if __name__=='__main__':
    first=set(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else None
    data=build(first);open(sys.argv[1],'w').write(json.dumps(data,separators=(",",":"),sort_keys=True)+'\n');print(json.dumps({'census':data['census'],'record_sha256':digest(data)}))
