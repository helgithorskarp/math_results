"""Exact Parts coordinates and the all-scale inversion reduction."""
import hashlib,json
from fractions import Fraction as F
from math import isqrt,lcm
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json'
SOURCE_SHA='41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729'
P=1000000271
ROOT5=838613109
ROOT33=767568613
RAD=(1,5,33,165)
ZERO=(0,)*4
ONE=(1,0,0,0)
def require(c,message):
    if not c:raise ValueError(message)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(k*x for x in a)
def mul(a,b):
    out=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i^j]+=x*y*RAD[i&j]
    return tuple(out)
def norm(a,b):
    x,y=(sub(t,u) for t,u in zip(a,b))
    return add(mul(x,x),scale(mul(y,y),3))
def inverse(a):
    b=ONE
    for mask in (1,2,3):b=mul(b,tuple(-x if (i&mask).bit_count()%2 else x for i,x in enumerate(a)))
    d=mul(a,b);require(d[0]!=0 and d[1:]==(0,0,0),'field inverse failed')
    return tuple(F(x,d[0]) for x in b)
def source():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA,'source changed')
    raw=json.loads(SOURCE.read_text())['coordinates'];out=[]
    for i in range(509):
        x,y=[[F(s) for s in row] for row in raw[str(i)]]
        require(all(x[k]==0 for k in (1,3,4,6)) and all(y[k]==0 for k in (0,2,5,7)),'source parity')
        out.append(((x[0],x[2],x[5],x[7]),(y[1],y[3],y[4]/3,y[6]/3)))
    require(len(set(out))==509,'source collision')
    return out

def projection(p=P,r5=ROOT5,r33=ROOT33):
    require(p>=2 and all(p%d for d in range(2,isqrt(p)+1)),'not prime')
    require(r5*r5%p==5 and r33*r33%p==33,'invalid radical images')
    def rat(x):
        x=F(x);return x.numerator*pow(x.denominator,-1,p)%p
    return lambda a:sum(rat(x)*r for x,r in zip(a,(1,r5,r33,r5*r33%p)))%p

def projected():
    ev=projection();return [(ev(x),ev(y)) for x,y in source()]

def peel(edges,k=3):
    """Peel all nonisolated labels; verify the resulting greedy word."""
    adj={}
    for i,j in edges:adj.setdefault(i,[]).append(j);adj.setdefault(j,[]).append(i)
    degree={v:len(row) for v,row in adj.items()};queue=[v for v in adj if degree[v]<=k]
    for v in queue:
        degree[v]=-1
        for u in adj[v]:
            if degree[u]>=0:
                degree[u]-=1
                if degree[u]==k:queue.append(u)
    if len(queue)!=len(adj):return None
    word=[0]*508
    for v in reversed(queue):
        used={word[u] for u in adj[v] if degree[u]>=0};word[v]=next(c for c in range(k+1) if c not in used);degree[v]=0
    require(all(word[i]!=word[j] for i,j in edges),'invalid reverse peel')
    return ''.join(map(str,word))

def word_check(word,edges):
    require(isinstance(word,str) and len(word)==508 and set(word)<=set('0123'),'malformed colour word')
    require(all(word[i]!=word[j] for i,j in edges),'improper colour word')
