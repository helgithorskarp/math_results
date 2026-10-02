"""Credited unchanged owned exact kernel from REVIEW9663, source84b336a5009d8f3c9940e08dc56faeb7e22997ba. No target executable import."""
from fractions import Fraction as Q
def need(condition,message):
    if not condition: raise ValueError(message)

def trim(p):
    p=list(map(Q,p))
    while len(p)>1 and p[-1]==0: p.pop()
    return tuple(p)

ZERO=(Q(0),)
ONE=(Q(1),)
def add(p,q): return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])
def neg(p): return tuple(-x for x in p)
def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return trim(out)
def divmodp(p,q):
    need(q!=ZERO,'zero divisor'); p=list(p); quo=[Q(0)]*max(1,len(p)-len(q)+1)
    while trim(p)!=ZERO and len(trim(p))>=len(q):
        p=list(trim(p)); k=len(p)-len(q); a=p[-1]/q[-1]; quo[k]+=a
        for j,b in enumerate(q):p[k+j]-=a*b
    return trim(quo),trim(p)
def gcd(p,q):
    while q!=ZERO: p,q=q,divmodp(p,q)[1]
    return trim([x/p[-1] for x in p]) if p!=ZERO else ZERO
def value(p,x):
    ans=Q(0)
    for a in reversed(p):ans=ans*x+a
    return ans
def derivative(p):return trim([i*p[i] for i in range(1,len(p))] or [0])
def sturm(p,left,right):
    need(value(p,left)!=0 and value(p,right)!=0,'root at closed endpoint')
    seq=[p,derivative(p)]
    if seq[-1]==ZERO:seq.pop()
    while len(seq)>1:
        rem=neg(divmodp(seq[-2],seq[-1])[1])
        if rem==ZERO:break
        seq.append(rem)
    def variation(x):
        signs=[1 if value(s,x)>0 else -1 for s in seq if value(s,x)!=0]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variation(left)-variation(right),seq

def fan_at(r,m,state):
    previous,current,outside=state
    neighbors=[previous,outside]
    for _ in range(1,m):
        neighbors.append(tuple(r*(current[k]+neighbors[-1][k])-neighbors[-2][k] for k in range(3)))
    return current,neighbors[m],neighbors[m-1]

E=((1,0,0),(0,1,0),(0,0,1))
def numeric_gap(word,r):
    state=E
    for m in word:state=fan_at(r,m,state)
    return tuple(state[1][k]-E[0][k] for k in range(3))

def interpolate(values):
    # Newton forward differences at consecutive integer abscissas.
    diffs=list(map(Q,values)); result=ZERO; binomial=ONE
    for k in range(len(values)):
        result=add(result,tuple(diffs[0]*a for a in binomial))
        diffs=[b-a for a,b in zip(diffs,diffs[1:])]
        binomial=tuple(a/Q(k+1) for a in mul(binomial,(-k,1)))
    return result

