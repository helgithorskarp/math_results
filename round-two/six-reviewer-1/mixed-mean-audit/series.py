"""Fresh sparse, separately indexed Q(zeta36)[mu,t][epsilon] jets."""
from fractions import Fraction as Q
from field import E,need
from math import comb
def pc(x):return {(0,0):E(x)}if x else{}
ONE=pc(1);MU={(1,0):E(1)};T={(0,1):E(1)}
def pa(*args):
    out={}
    for p in args:
        for e,v in p.items():
            out[e]=out.get(e,E(0))+v
            if not out[e]:del out[e]
    return out
def ps(p,v):return {e:x*v for e,x in p.items()if x*v}
def pm(p,q):
    out={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():
            e=(i+k,j+l);out[e]=out.get(e,E(0))+v*w
    return {e:v for e,v in out.items()if v}
def pp(p,n):
    out=ONE
    for _ in range(n):out=pm(out,p)
    return out
def sa(*args,n=10):return [pa(*(s[j]if j<len(s)else{}for s in args))for j in range(n+1)]
def ss(s,v):return [ps(p,v)for p in s]
def sm(s,t,n=10):return [pa(*(pm(s[i],t[j-i])for i in range(j+1)if i<len(s)and j-i<len(t)))for j in range(n+1)]
def sp(s,k,n=10):
    out=[ONE]+[{}]*n
    for _ in range(k):out=sm(out,s,n)
    return out
def sj(x,n=10):return [pc(x)]+[{}]*n
def conj(s):return [{e:v.conjugate()for e,v in p.items()}for p in s]
def put(s,j,p):s[j]=pa(s[j],p)
def record(s):return [[[list(e),v.record()]for e,v in sorted(p.items())]for p in s]
def value(primitive,root,n=10):
    out=[{}]*(n+1)
    for row in reversed(primitive):out=sa(sm(out,root,n),row,n=n)
    return out
def inverse(s,n=10):
    need(s[0].keys()=={(0,0)},'constant series divisor')
    c=1/s[0][0,0];out=[pc(c)]+[{}]*n
    for j in range(1,n+1):out[j]=ps(pa(*(pm(s[k],out[j-k])for k in range(1,j+1)if k<len(s))),-c)
    need(sm(s,out,n)==sj(1,n),'entire series inverse')
    return out
