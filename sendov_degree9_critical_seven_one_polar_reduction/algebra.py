"""Exact 7+1 weighted-mean origin algebra over Q[t,c,x,K].

Author six-sendov-1, role researcher, 2026-09-30.
Weighted-mean coordinates and sparse arithmetic are author reuse from
source d02716775d595df93bb338e533323db8717b3185 (critical6+2);
all multiplicity-dependent 7+1 coefficients are regenerated here.

Here c in [0,1] parametrizes squared mean radius q=K^2+(1-K^2)c.
The quadratic extension is i*delta with delta^2=c(1-c).
All dictionaries are sparse rational polynomials in the listed order.
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb

ZERO=(0,)*4
ONE={ZERO:F(1)}

def add(*items):
 out=defaultdict(F)
 for p in items:
  for e,v in p.items():out[e]+=v
 return {e:v for e,v in out.items() if v}

def scale(p,v):return {e:k*v for e,k in p.items() if k*v}

def mul(p,r):
 out=defaultdict(F)
 for e,v in p.items():
  for f,k in r.items():out[tuple(a+b for a,b in zip(e,f))]+=v*k
 return {e:v for e,v in out.items() if v}

def power(p,n):
 out=ONE
 while n:
  if n&1:out=mul(out,p)
  n//=2
  if n:p=mul(p,p)
 return out

def variable(i):
 e=list(ZERO);e[i]=1
 return {tuple(e):F(1)}

def pairmul(p,r,B):
 a,b=p;c,d=r
 return (add(mul(a,c),scale(mul(B,mul(b,d)),-1)),
         add(mul(a,d),mul(b,c)))

def pairpower(p,n,B):
 out=(ONE,{})
 for _ in range(n):out=pairmul(out,p,B)
 return out

def coefficients():
 """Independent-binomial powers of heavy and light linear factors."""
 t,c,x,K=[variable(i) for i in range(4)]
 D=add(ONE,scale(power(K,2),-1));q=add(power(K,2),mul(D,c))
 B=mul(c,add(ONE,scale(c,-1)))
 U=(scale(add(q,K),F(4,7)),scale(D,F(4,7)))
 V=(scale(add(q,scale(K,-1)),F(4)),scale(D,F(-4)))
 up=[pairpower(U,j,B) for j in range(8)]
 vp=[pairpower(V,j,B) for j in range(2)]
 P=[{} for _ in range(9)];Q=[{} for _ in range(9)]
 for i in range(8):
  for j in range(2):
   n=i+j;u,v=pairmul(up[i],vp[j],B)
   k=F(9*(-1)**n*comb(7,i)*comb(1,j),n+1)
   monomial={(n,0,n,0):k}
   P[n]=add(P[n],mul(monomial,u));Q[n]=add(Q[n],mul(monomial,v))
 return P,Q

def alternate_coefficients():
 """One paired quadratic followed by six heavy linear factors."""
 t,c,x,K=[variable(i) for i in range(4)]
 D=add(ONE,scale(power(K,2),-1));q=add(power(K,2),mul(D,c))
 B=mul(c,add(ONE,scale(c,-1)))
 U=(scale(add(q,K),F(-4,7)),scale(D,F(-4,7)))
 V=(scale(add(q,scale(K,-1)),F(-4)),scale(D,F(4)))
 paired=[(ONE,{}),(add(U[0],V[0]),add(U[1],V[1])),pairmul(U,V,B)]
 terms=[(ONE,{})]
 for factor in [paired]+[[(ONE,{}),U]]*6:
  out=[({},{}) for _ in range(len(terms)+len(factor)-1)]
  for i,p in enumerate(terms):
   for j,r in enumerate(factor):
    a,b=pairmul(p,r,B)
    out[i+j]=(add(out[i+j][0],a),add(out[i+j][1],b))
  terms=out
 return ([mul({(n,0,n,0):F(9,n+1)},a) for n,(a,b) in enumerate(terms)],
         [mul({(n,0,n,0):F(9,n+1)},b) for n,(a,b) in enumerate(terms)])

def chebyshev():
 x=variable(2);T=[ONE,x];U=[ONE,scale(x,2)]
 for _ in range(7):
  T.append(add(scale(mul(x,T[-1]),2),scale(T[-2],-1)))
  U.append(add(scale(mul(x,U[-1]),2),scale(U[-2],-1)))
 return T,U

def norm(P,Q):
 c=variable(1);B=mul(c,add(ONE,scale(c,-1)))
 T,U=chebyshev();E={};J={}
 for j in range(9):
  E=add(E,mul(P[j],P[j]),mul(B,mul(Q[j],Q[j])))
  for k in range(j):
   pair=add(mul(P[j],P[k]),mul(B,mul(Q[j],Q[k])))
   E=add(E,scale(mul(pair,T[j-k]),2))
   skew=add(mul(Q[j],P[k]),scale(mul(P[j],Q[k]),-1))
   J=add(J,scale(mul(skew,U[j-k-1]),2))
 return E,J

def alternate_norm(P,Q):
 c=variable(1);x=variable(2)
 B=mul(c,add(ONE,scale(c,-1)));Y=add(ONE,scale(power(x,2),-1))
 T,U=chebyshev()
 A=add(*(mul(P[j],T[j]) for j in range(9)))
 G=add(*(mul(Q[j],T[j]) for j in range(9)))
 D=add(*(mul(Q[j],U[j-1]) for j in range(1,9)))
 H=add(*(mul(P[j],U[j-1]) for j in range(1,9)))
 E=add(mul(A,A),mul(B,mul(G,G)),mul(Y,add(mul(H,H),mul(B,mul(D,D)))))
 J=scale(add(mul(A,D),scale(mul(G,H),-1)),2)
 return E,J

def origin_data():
 P,Q=coefficients();E,J=norm(P,Q);K=variable(3)
 R=scale(mul(power(add(ONE,K),14),power(add(ONE,scale(K,-1)),2)),F(4,7)**14*F(4)**2)
 D=add(E,scale(R,-1));return P,Q,E,J,R,D

def gauss_lucas():
 t,c,x,K=[variable(i) for i in range(4)]
 radial=add(ONE,scale(power(K,2),-1));q=add(power(K,2),mul(radial,c))
 r2=scale(power(add(ONE,K),2),F(16,49));s2=scale(power(add(ONE,scale(K,-1)),2),16)
 b2=mul(power(t,2),mul(q,power(x,2)))
 U0=add(r2,scale(ONE,-1),scale(mul(b2,r2),-1),scale(mul(t,mul(power(x,2),add(q,K))),F(8,7)))
 V0=add(s2,scale(ONE,-1),scale(mul(b2,s2),-1),scale(mul(t,mul(power(x,2),add(q,scale(K,-1)))),8))
 U1=scale(mul(t,mul(x,radial)),F(8,7));V1=scale(mul(t,mul(x,radial)),-8)
 return (U0,U1),(V0,V1)

def canonical(p):return [[list(e),str(v)] for e,v in sorted(p.items())]

def evaluate(p,values):
 out=F(0)
 powers=[[values[i]**j for j in range(max(e[i] for e in p)+1)] for i in range(4)]
 for e,v in p.items():
  for i in range(4):v*=powers[i][e[i]]
  out+=v
 return out
