"""Small exact homogeneous triangular polynomial and matrix operations.
Only the previously pinned ordered field is imported; no floating arithmetic.
"""
from fractions import Fraction as F
from math import factorial
from q5 import Q

def require(ok,message):
 if not ok:raise ValueError(message)

ZERO=(0,0,0)
def add(p,q):
 r=p.copy()
 for e,x in q.items():
  r[e]=r.get(e,Q())+x
  if r[e]==0:del r[e]
 return r

def scale(p,x):return {e:x*y for e,y in p.items() if x*y!=0}

def mul(p,q):
 r={}
 for e,x in p.items():
  for f,y in q.items():
   g=tuple(i+k for i,k in zip(e,f));r[g]=r.get(g,Q())+x*y
 return {e:x for e,x in r.items() if x!=0}

def linear(values):return {tuple(int(i==k) for i in range(3)):v for k,v in enumerate(values) if v!=0}

def det(M):
 states={0:{ZERO:Q(1)}}
 for row in range(5):
  nxt={}
  for mask,p in states.items():
   for k in range(5):
    if mask>>k&1:continue
    sign=(-1)**sum(mask>>i&1 for i in range(k+1,5));q=scale(mul(p,M[row][k]),sign);key=mask|(1<<k)
    nxt[key]=add(nxt.get(key,{}),q)
  states=nxt
 return states[31]

def controls(p,d):
 require(all(sum(e)==d for e in p),'literal homogeneous triangular degree')
 es=[(i,k,d-i-k) for i in range(d+1) for k in range(d-i+1)]
 return [(e,p.get(e,Q())/Q(F(factorial(d),factorial(e[0])*factorial(e[1])*factorial(e[2])))) for e in es]

def encode(p):return [[list(e),c.enc(x)] for e,x in sorted(p.items())]

def value(p,t):return sum((x*__import__('functools').reduce(lambda u,v:u*v,(s**k if not isinstance(s,Q) else powq(s,k) for s,k in zip(t,e)),Q(1)) for e,x in p.items()),Q())
def powq(x,k):
 r=Q(1)
 for i in range(k):r=r*x
 return r

def directdet(A):
 M=[list(row) for row in A];out=Q(1)
 for k in range(5):
  pivot=next((r for r in range(k,5) if M[r][k]!=0),None)
  if pivot is None:return Q()
  if pivot!=k:M[k],M[pivot]=M[pivot],M[k];out=-out
  v=M[k][k];out=out*v
  for r in range(k+1,5):
   f=M[r][k]/v
   for i in range(k+1,5):M[r][i]=M[r][i]-f*M[k][i]
 return out

def inverse(A):
 n=len(A);M=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
 for k in range(n):
  pivot=next((r for r in range(k,n) if M[r][k]!=0),None)
  if pivot is None:raise ZeroDivisionError('singular literal ordered-field matrix')
  M[k],M[pivot]=M[pivot],M[k];v=M[k][k];M[k]=[x/v for x in M[k]]
  for r in range(n):
   if r==k:continue
   v=M[r][k]
   if v!=0:M[r]=[x-v*y for x,y in zip(M[r],M[k])]
 out=tuple(tuple(row[n:]) for row in M)
 require(all(sum((A[i][k]*out[k][j] for k in range(n)),Q())==int(i==j) for i in range(n) for j in range(n)),'independent full exact inverse product')
 return out
