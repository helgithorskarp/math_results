"""Exact 5+3 weighted-mean origin algebra over Q[t,c,x,K].

Author six-sendov-1, role researcher, 2026-09-30.

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
 U=(scale(add(q,K),F(4,5)),scale(D,F(4,5)))
 V=(scale(add(q,scale(K,-1)),F(4,3)),scale(D,F(-4,3)))
 up=[pairpower(U,j,B) for j in range(6)]
 vp=[pairpower(V,j,B) for j in range(4)]
 P=[{} for _ in range(9)];Q=[{} for _ in range(9)]
 for i in range(6):
  for j in range(4):
   n=i+j;u,v=pairmul(up[i],vp[j],B)
   k=F(9*(-1)**n*comb(5,i)*comb(3,j),n+1)
   monomial={(n,0,n,0):k}
   P[n]=add(P[n],mul(monomial,u));Q[n]=add(Q[n],mul(monomial,v))
 return P,Q

def alternate_coefficients():
 """Three paired quadratics followed by two heavy linear factors."""
 t,c,x,K=[variable(i) for i in range(4)]
 D=add(ONE,scale(power(K,2),-1));q=add(power(K,2),mul(D,c))
 B=mul(c,add(ONE,scale(c,-1)))
 U=(scale(add(q,K),F(-4,5)),scale(D,F(-4,5)))
 V=(scale(add(q,scale(K,-1)),F(-4,3)),scale(D,F(4,3)))
 paired=[(ONE,{}),(add(U[0],V[0]),add(U[1],V[1])),pairmul(U,V,B)]
 terms=[(ONE,{})]
 for factor in [paired]*3+[[(ONE,{}),U]]*2:
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

def margins():
 P,Q=coefficients();E,J=norm(P,Q)
 c=variable(1);x=variable(2);K=variable(3)
 R=scale(mul(power(add(ONE,K),10),power(add(ONE,scale(K,-1)),6)),F(4,5)**10*F(4,3)**6)
 D=add(E,scale(R,-1))
 s=add(ONE,scale(mul(c,power(x,2)),-1))
 h=mul(mul(c,add(ONE,scale(c,-1))),add(ONE,scale(power(x,2),-1)))
 H=[add(scale(mul(s,D),4),scale(mul(add(power(s,2),scale(h,4)),J),sign)) for sign in [-1,1]]
 return E,J,D,H

def canonical(p):return [[list(e),str(v)] for e,v in sorted(p.items())]

def evaluate(p,values):
 out=F(0)
 powers=[[values[i]**j for j in range(max(e[i] for e in p)+1)] for i in range(4)]
 for e,v in p.items():
  for i in range(4):v*=powers[i][e[i]]
  out+=v
 return out
