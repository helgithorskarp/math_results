"""Independent exact univariate Euclid; full Bezout and divisibility certificates."""
from owned_algebra import P,Q,var,ZERO

def trim(a):
 while a and not a[-1]:a.pop()
 return a

def add(a,b):return trim([(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([v*c for v in a])
def multiply(a,b):
 c=[Q(0)]*max(0,len(a)+len(b)-1)
 for i,v in enumerate(a):
  for k,w in enumerate(b):c[i+k]+=v*w
 return trim(c)
def div(a,b):
 a=a.copy();q=[Q(0)]*max(0,len(a)-len(b)+1)
 while a and len(a)>=len(b):
  d=len(a)-len(b);c=a[-1]/b[-1];q[d]=c;a=add(a,[Q(0)]*d+scale(b,-c))
 return trim(q),a
def gcd(a,b):
 while b:a,b=b,div(a,b)[1]
 return scale(a,1/a[-1]) if a else []
def stream(a,slot):
 if any(any(k[i] for i in range(8) if i!=slot) for k in a.d):raise ValueError('not univariate')
 return trim([a.coeff(slot,d).d.get(ZERO,Q(0)) for d in range(a.degree(slot)+1)])

def xgcd(a,b):
    old,new=a.copy(),b.copy();s,ss=[Q(1)],[];t,tt=[],[Q(1)]
    while new:
        q,rem=div(old,new);old,new=new,rem
        s,ss=ss,add(s,scale(multiply(q,ss),-1))
        t,tt=tt,add(t,scale(multiply(q,tt),-1))
    if not old:return [],[],[]
    c=1/old[-1]
    return scale(old,c),scale(s,c),scale(t,c)

def many_gcd(streams):
    g=[];coeff=[]
    for a in streams:
        g,u,v=xgcd(g,a)
        coeff=[multiply(u,c) for c in coeff]+[v]
    product=[]
    for a,c in zip(streams,coeff):product=add(product,multiply(a,c))
    if product!=g:raise ValueError('whole Bezout product')
    quotients=[]
    for a in streams:
        q,rem=div(a,g)
        if rem:raise ValueError('whole gcd divisibility')
        quotients.append(q)
    encode=lambda p:list(map(str,p))
    return {'gcd':encode(g),'input':list(map(encode,streams)),
            'multipliers':list(map(encode,coeff)),'quotients':list(map(encode,quotients)),
            'whole_product':encode(product)}
