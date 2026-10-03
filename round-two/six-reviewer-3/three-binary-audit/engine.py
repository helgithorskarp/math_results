"""Independent exact original-domain bit-cube evaluator, six-reviewer-3.
No target code, certificate, expected records or external imports were read.
"""
from itertools import combinations
from hashlib import sha256
import json
N=13
Q=((0,11),(1,7),(2,4),(3,5),(8,9),(10,12),(0,2),(3,6),(4,12),(5,7),(8,10),(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),(9,11),(11,12),(3,6),(6,7),(5,7),(9,10),(10,11),(7,11),(3,4))
DEAD=(4,5,6,7,9,10)
EARLY=((4,7),(4,10),(5,7),(6,7),(6,10),(7,10),(9,10))
FLOOR={9:25,10:29,11:35,12:39}
def require(test, why):
    if not test: raise ValueError(why)
def encode(obj): return json.dumps(obj,separators=(",",":"),sort_keys=True).encode()
def digest(obj): return sha256(encode(obj)).hexdigest()
def gates(word):
    word=tuple(tuple(g) for g in word)
    require(all(len(g)==2 and type(g[0]) is int and type(g[1]) is int and 0<=g[0]<g[1]<N for g in word),'nonstandard gate')
    return word
def columns(k):
    rows=1<<k
    return tuple(sum(1<<r for r in range(rows) if (r>>j)&1) for j in range(k))
COL={k:columns(k) for k in (9,10,11,12,13)}
def start(low,high):
    require(type(low)is int and type(high)is int and low>=0 and high>=0 and low<1<<N and high<1<<N and not low&high,'original masks')
    ls=[i for i in range(N) if low>>i&1];hs=[i for i in range(N) if high>>i&1]
    free=[i for i in range(N) if not (low|high)>>i&1]; k=len(free)
    require(k in COL,'unsupported original family')
    # Each tuple is (extreme rank or None, complete ordered Boolean column).
    x=[None]*N
    for rank,i in enumerate(ls):x[i]=(rank-len(ls),0)
    for rank,i in enumerate(hs):x[i]=(rank+2,0)
    for j,i in enumerate(free):x[i]=(None,COL[k][j])
    return x,free

def push(x,word,D=0,R=0,positions=0,offset=0):
    x=list(x)
    for t,(a,b) in enumerate(word,offset):
        u,v=x[a],x[b]
        if u[0] is not None or v[0] is not None:
            D+=1
            swap=(u[0]>v[0]) if u[0] is not None and v[0] is not None else (u[0]>=2 if u[0] is not None else v[0]<0)
            if swap:x[a],x[b]=v,u
        else:
            if not u[1]&~v[1]: R+=1;positions|=1<<t
            x[a]=(None,u[1]&v[1]);x[b]=(None,u[1]|v[1])
    return x,D,R,positions

def replay(word,low,high):
    x,free=start(low,high);x,D,R,pos=push(x,gates(word))
    cl=sum(1<<i for i,v in enumerate(x) if v[0] is not None and v[0]<0)
    ch=sum(1<<i for i,v in enumerate(x) if v[0] is not None and v[0]>=2)
    return [low,high,cl,ch,D,R,pos],x,free

def rows(x,k):
    for r in range(1<<k):yield [v[0] if v[0] is not None else (v[1]>>r)&1 for v in x]

def scalar(word,low,high):
    word=gates(word);initial,free=start(low,high);k=len(free);Ds=[];identity=(1<<len(word))-1;marked=(1<<len(word))-1;out=[];tags=None
    for r in range(1<<k):
        x=[v[0] if v[0] is not None else (v[1]>>r)&1 for v in initial];D=0;markbits=0
        for t,(a,b) in enumerate(word):
            u,v=x[a],x[b]
            if u<0 or u>=2 or v<0 or v>=2:D+=1;markbits|=1<<t
            if u>v:identity&=~(1<<t);x[a],x[b]=v,u
        marked&=markbits;Ds.append(D);out.append(x)
        z=(sum(1<<i for i,v in enumerate(x) if v<0),sum(1<<i for i,v in enumerate(x) if v>=2))
        if tags is None:tags=z
        require(z==tags,'scalar tag depends on assignment')
    require(min(Ds)==max(Ds),'scalar marked history depends on assignment')
    positions=identity&~marked
    return [low,high,*tags,Ds[0],positions.bit_count(),positions],out

def boolean(word):
    word=gates(word);x=[(None,v) for v in COL[N]];x,_,_,_=push(x,word)
    return tuple(v[1] for v in x)
def binary_output(word,input_mask):
    x=[input_mask>>i&1 for i in range(N)]
    for a,b in gates(word):
        if x[a]>x[b]:x[a],x[b]=x[b],x[a]
    return sum(v<<i for i,v in enumerate(x))
def family(l,h):
    for lows in combinations(range(N),l):
        low=sum(1<<i for i in lows)
        for highs in combinations([i for i in range(N) if not low>>i&1],h):yield low,sum(1<<i for i in highs)
def profile(word,l,h):
    classes={};records=[]
    for low,high in family(l,h):
        rec,_,_=replay(word,low,high);records.append(rec);tag=tuple(rec[2:4]);classes[tag]=max(classes.get(tag,-1),rec[4])
    return records,sorted((lo,hi,d) for (lo,hi),d in classes.items()),sum(1<<d for d in classes.values())
def tails(q):
    r=sorted((1,2,3,min(8,q)));out=[]
    for a,b in combinations(r,2):
        c,d=sorted(set(r)-{a,b})
        if (a,b)>(c,d):continue
        out.append(((a,b),(c,d),tuple(sorted((min(a,b),min(c,d))))))
    return tuple(sorted(out))
def assess(word,w):
    """Generic independently normalized sufficient certificate, no native format.
    kind cost/marked/cut/mass. Each own record checked in full, original masks.
    """
    word=gates(word);kind=w['kind']
    if kind=='mass':
        tags=set();total=0;fam=None;recout=[]
        require(len(w['records'])>0,'empty mass')
        for rec in w['records']:
            require(len(rec)==7,'record length');actual,_,_=replay(word,rec[0],rec[1]);require(actual==rec,'false mass record')
            this=(rec[0].bit_count(),rec[1].bit_count());fam=this if fam is None else fam;require(this==fam,'mixed families')
            tag=tuple(rec[2:4]);require(tag not in tags,'duplicate tag');tags.add(tag);total+=1<<(rec[4]+rec[5]);recout.append(actual)
        k=N-sum(fam);require(k in FLOOR and total>1<<(44-FLOOR[k]),'non-strict mass');return {'kind':kind,'records':recout,'mass':total,'ceiling':1<<(44-FLOOR[k])}
    rec=w['record'];require(len(rec)==7,'record length');actual,x,free=replay(word,rec[0],rec[1]);require(actual==rec,'false original record');k=len(free);require(k in FLOOR,'floor absent');cost=rec[4]+rec[5]+FLOOR[k]
    if kind=='cost':require(cost>44,'non-strict cost');return {'kind':kind,'record':actual,'cost':cost}
    require(kind in ('marked','cut'),'unknown witness');q=w['port'];require(type(q)is int and 0<=q<N,'physical port');require(cost==44,'non-tight lock')
    inp=w['input'];require(type(inp)is int and 0<=inp<1<<N,'rank input');out=binary_output(word,inp);expected=((1<<inp.bit_count())-1)<<(N-inp.bit_count());require(((out^expected)>>q)&1,'right rank already')
    if kind=='marked':require(x[q][0] is not None,'port not marked')
    else:
        require(x[q][0] is None,'cut port not free')
        for i in free_output(x):
            if i<q:require(not x[i][1]&~x[q][1],'left cut fails')
            elif i>q:require(not x[q][1]&~x[i][1],'right cut fails')
    return {'kind':kind,'record':actual,'port':q,'input':inp,'output':out,'cost':cost}
def free_output(x):return [i for i,v in enumerate(x) if v[0] is None]
