"""Independent abstract tables and Euclidean field maps; no author imports."""
from itertools import permutations,product
from functools import lru_cache
import json

SIG=(0,0,0,1,1,1)

def need(ok,message):
    if not ok:raise ValueError(message)

def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()

def inverse(a,p):
    a%=p;need(a!=0,'zero inverse')
    oldr,r=p,a;oldx,x=0,1
    while r:
        q=oldr//r;oldr,r=r,oldr-q*r;oldx,x=x,oldx-q*x
    need(oldr==1,'nonunit field element');return oldx%p

@lru_cache(None)
def squares(p):return frozenset(x*x%p for x in range(1,p))

def character(x,p):
    x%=p;need(x!=0,'character undefined at original root')
    return int(x not in squares(p))

def roots(state):
    r,t,w=state
    return (0,)if r==1 else (0,1)if r==2 else (0,1,t)

def truth(word,r):return tuple((word>>i)&1 for i in range(1<<r))

def word(values):return sum(v<<i for i,v in enumerate(values))

def cube(r):return tuple(tuple((i>>j)&1 for j in range(r))for i in range(1<<r))

@lru_cache(None)
def map_basis(r,t,order,p):
    R=roots((r,t,0))
    if r==1:return 0,1,0,(0,1)
    delta=(R[order[1]]-R[order[0]])%p
    alpha=inverse(delta,p);beta=-alpha*R[order[0]]%p
    target_t=1 if r==2 else (alpha*R[order[2]]+beta)%p
    sign=character(delta,p);pull=[]
    for newbits in cube(r):
        oldbits=[0]*r
        for j,i in enumerate(order):oldbits[i]=newbits[j]^sign
        pull.append(sum(b<<i for i,b in enumerate(oldbits)))
    return target_t,alpha,beta,tuple(pull)

def orders(r):return ((0,),)if r==1 else tuple(permutations(range(r)))

@lru_cache(None)
def actions(state,p):
    r,t,w=state;F=truth(w,r);out=[]
    for order in orders(r):
        tp,a,b,pull=map_basis(r,t,order,p)
        raw=tuple(F[i]for i in pull);flip=raw[0]
        target=(r,tp,word(tuple(z^flip for z in raw)))
        out.append((target,a,b,flip))
    return tuple(out)

def states(p):
    return [(1,0,w)for w in (0,2)]+[(2,1,w)for w in range(0,16,2)]+[
        (3,t,w)for t in range(2,p)for w in range(0,256,2)]

def orbit_cover(p):
    left=set(states(p));classes=[]
    while left:
        seed=min(left);orb={z[0]for z in actions(seed,p)}
        need(seed in orb and orb<=left,'complete nonoverlapping orbit')
        need(all({v[0]for v in actions(z,p)}==orb for z in orb),'whole orbit closure')
        left-=orb;classes.append(tuple(sorted(orb)))
    return tuple(classes)

def essential(word0,r):
    F=truth(word0,r)
    return sum(any(F[i]!=F[i^(1<<j)]for i in range(1<<r))for j in range(r))

def color(state,n,p=103):
    R=roots(state);r,t,w=state;x=n%p
    bits=tuple(character(x-a,p)for a in R)
    return truth(w,r)[sum(b<<i for i,b in enumerate(bits))]^SIG[n%6]

def crt(x,row,p=103):
    out=next(n for n in range(x%p,6*p,p)if n%6==row%6)
    need(out%p==x%p and out%6==row%6,'literal CRT coordinates');return out

def inverse_transport(source,target,p=103):
    matches=[(a,b,flip)for s,a,b,flip in actions(source,p)if s==target]
    need(matches,'representative outside parameter orbit')
    a,b,flip=min(matches);aa=inverse(a,p);bb=-aa*b%p
    return crt(aa,1,p),crt(bb,0,p),flip
