"""Credited 9201/9269 mathematical formulas, independently implemented."""
from exact import F,comb,need,dot,energy

def params(n):return 2**(n-1),2**n-n-1,2**(n-1)-n,2**(n-1)-1

def base(n):
 T,N,s,h=params(n);b={}
 def put(a,c,x):b[tuple(sorted((a,c)))]=F(x)
 for a in range(3,n-2):
  put(a,n-a,s);put(1,a,F(2*(n-2),n-a));put(2,a,F(-2*(n-2),(n-a)*(n-a-1)))
 put(1,n-2,n-2);put(2,n-2,s-(n-2))
 put(1,1,F(T*n*n-9*T*n+16*T-n**3+9*n*n-8*n-16,n*(n-1)))
 put(1,2,F(2*(-T*n+4*T+2*n*n-4*n-4),n*(n-1)))
 put(2,2,F(-4*(-T*n+2*T+2*n*n-2*n-2),n*(n-3)*(n-1)))
 return b

def weight(b,a,c):return b.get(tuple(sorted((a,c))),F(0))

def profiles(n,k):
 p=[];q=[];r=[];f=[];g=[];c=F(2,n);d=F(-(2*n+5),n*n)
 for a in range(1,n-1):
  if a<=k:P,Q=F(1),c+d*a
  elif n-a<=k:P,Q=F(-1),c+d*(n-a)
  else:
   t=F((2*n+5)*(2*a-n),4*n*n);P=2*t**3/(1+t*t);Q=-F(1,2*n)+2*t*t/(1+t*t)
  p.append(P);q.append(Q);r.append(2*P-4*(Q+F(1,2*n))/n);f.append(P-1);g.append(Q-c-d*a)
 return p,q,r,f,g

def physical(n,b):
 T,N,s,h=params(n);sizes=range(1,n-1);K=[];U=[]
 for a in sizes:
  row=[];up=[]
  for c in sizes:
   cou=weight(b,a,c)*comb(n-a,c) if c<=n-a else F(0)
   row.append(comb(n,a)*(s*(a==c)-comb(n,c)+cou));up.append(comb(n,a)*(h*(a==c)-cou))
  K.append(row);U.append(up)
 return K,U

def scalar(n,k):
 T,N,s,h=params(n);b=base(n);p,q,_,_,_=profiles(n,k);q1=-F(5,n*n);q2=-F(2*n+10,n*n);c=F(2,n)
 phi=(n*h-n*(n-1)*weight(b,1,1))*q1*q1
 phi+=(n*(n-1)*(2*n-3)-F(n*(n-1)*(n-2)*(n-3),4)*weight(b,2,2))*q2*q2
 phi-=(n*(n-1)*(n-2)*weight(b,1,2)+2*n*(n-1)*(n-2))*q1*q2
 return 4*(T-n-1)+phi+sum(comb(n,a)*((n-1)*q[a-1]**2-2*(n-2)*c*q[a-1]) for a in range(3,n-2))

def debias(n):
 """Positive rational coefficient; exact cubic numerator orthogonalization."""
 ell=2*n+5;A=F(ell**3,16*n**6);B=F(ell**2,16*n**4);c1=3*n-2
 return A*c1/(1+c1*B)

def residual(n,k,a,b):
 p,q,r,f,g=profiles(n,k)
 return f[a-1]*f[b-1]-g[a-1]*g[b-1]
