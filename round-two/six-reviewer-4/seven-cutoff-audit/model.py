"""Orbit counting producer, rebuilt from the written disjoint table of8757."""
from fractions import Fraction as F
from math import comb
from exact import need

def choose(n,k):return comb(n,k)if 0<=k<=n else 0
def keys(q):
 out=[]
 for c in range(8):
  for z in range(3):
   for w in range(3):
    size=c.bit_count()+z+w
    if not choose(7,z)*choose(q-7,w):continue
    if size not in (1,2)and not(size==3 and c.bit_count()>=2):continue
    if (c,z,w)==(6,1,0):continue
    out.append((c,z,w))
 return out
def weight(q,x,y,kappa):
 order=[(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)]
 if order.index(x)>order.index(y):x,y=y,x
 s=3*q+4;u=kappa/F(3*q+5)
 if x[0]==y[0]==0:
  if x==y==(0,1):return (kappa+F(6,q)+q-(s-q))/(q-1)
  if x!=y:return F(q*(q-3),(q-1)*(q-2))
  return (kappa+F(6,q)-6*u*F(q+1,q*(q-1))+F(2*q,q-1)-s+F(q*(q-1),2))*F(2,(q-2)*(q-3))
 if x[0]==0:
  i=x[1]
  alpha=1-F(1,q)if i==1 else 1+2*u/F(q*(q-1))
  beta=1+F(1,q)if i==1 else 1+2*(u+F((q-1)**2,q))/F((q-1)*(q-2))
  gamma=1+F(6,q)if i==1 else 1+F(6,q)-6*u*F(q+1,q*(q-1))
  return gamma if y==(3,0)else beta if y[1]else alpha
 t=3+F(2,q)
 return {((1,0),(1,0)):F(0),((1,0),(1,1)):F(0),((1,1),(1,1)):F(0),((1,0),(2,0)):F(2),((1,0),(2,1)):t,((1,1),(2,0)):t,((1,1),(2,1)):(s-t)/(q-1)}[(x,y)]
def build(q):
 kk=keys(q);weights=[choose(7,z)*choose(q-7,w)for c,z,w in kk];d=len(kk);N=(q*q+13*q+16)//2-7;s=3*q+4
 forms=[[[F(0)]*d for _ in range(d)]for _ in range(5)]
 for i,(c,z,w)in enumerate(kk):
  x=(c.bit_count(),z+w)
  for j,(e,v,t)in enumerate(kk):
   forms[0][i][j]=(s*weights[i]if i==j else 0)-weights[i]*weights[j]
   if c&e:continue
   count=weights[i]*choose(7-z,v)*choose(q-7-w,t)
   if not count:continue
   a=weight(q,x,(e.bit_count(),v+t),F(0));b=weight(q,x,(e.bit_count(),v+t),F(1))
   forms[0][i][j]+=count*a;forms[1][i][j]=count*(b-a)
 for a,b,idx,value in [(1,2,2,1),(2,5,2,-1),(1,4,3,1),(4,3,3,-1),(2,4,4,1)]:
  i=kk.index((a,0,0));j=kk.index((b,0,0));forms[idx][i][j]=forms[idx][j][i]=F(value)
 U=[[F(N*weights[i]if i==j else 0)-weights[i]*weights[j]-forms[0][i][j]for j in range(d)]for i in range(d)]
 need(sum(weights)==N-1,'full orbit domain');need(all(a[i][j]==a[j][i]for a in forms+[U]for i in range(d)for j in range(d)),'physical symmetry')
 return dict(q=q,N=N,s=s,keys=kk,weights=weights,forms=forms+[U])
