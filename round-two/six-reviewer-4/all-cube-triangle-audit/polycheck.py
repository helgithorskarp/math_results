"""Portable coefficient checks using independent Fraction sparse arithmetic."""
from fractions import Fraction as F
from math import comb
import json,sys
from pathlib import Path
class P:
 def __init__(self,terms):self.t={tuple(k):F(v)for k,v in terms.items()if v}
 def __add__(self,o):
  t=self.t.copy()
  for m,c in o.t.items():t[m]=t.get(m,0)+c
  return P(t)
 def __neg__(self):return P({m:-c for m,c in self.t.items()})
 def __sub__(self,o):return self+-o
 def __mul__(self,o):
  t={}
  for (a,b),c in self.t.items():
   for (d,e),f in o.t.items():
    m=(a+d,b+e);t[m]=t.get(m,0)+c*f
  return P(t)
 def shift(self):
  t={}
  for (a,b),c in self.t.items():
   for i in range(a+1):
    for j in range(b+1):
     m=(i,j);t[m]=t.get(m,0)+c*comb(a,i)*comb(b,j)*2**(a-i)*4**(b-j)
  return P(t)
 def positive(self):
  t=self.shift().t
  if not t or min(t.values())<=0 or t.get((0,0),0)<=0:raise ValueError('shift is not strictly coefficient-positive')
  return dict(coefficients=len(t),total_degree=max(sum(m)for m in t),bidegree=[max(m[i]for m in t)for i in range(2)],constant=str(t[(0,0)]))
 def evaluate(self,h,q):return sum(c*h**m[0]*q**m[1]for m,c in self.t.items())
def loadpoly(data):
 if type(data)is not list or any(type(x)is not list or len(x)!=2 or type(x[0])is not list or len(x[0])!=2 or any(type(z)is not int or z<0 for z in x[0])or type(x[1])is not list or len(x[1])!=2 or any(type(z)is not int for z in x[1])or x[1][1]<=0 or not x[1][0]for x in data):raise ValueError('typed exact polynomial')
 if len({tuple(m)for m,c in data})!=len(data):raise ValueError('duplicate monomial')
 return P({tuple(m):F(*c)for m,c in data})
def pair(r):return loadpoly(r['n']),loadpoly(r['d'])
def prove_update(u):
 nP,dP=pair(u['pivot']);nB,dB=pair(u['before']);nA,dA=pair(u['after']);nL,dL=pair(u['left']);nR,dR=pair(u['right'])
 z=nP*(nB*dA-nA*dB)*dL*dR-nL*nR*dP*dB*dA
 if z.t:raise ValueError('Gaussian identity failed')
def check(data):
 A=[[r for r in row]for row in data['original']];updates=iter(data['updates']);signs=[]
 if len(data['pivots'])!=len(A) or any(len(row)!=len(A)for row in A):raise ValueError('complete square pivot chain')
 for k,piv in enumerate(data['pivots']):
  if piv!=A[k][k]:raise ValueError('pivot not original current matrix')
  n,d=pair(piv);signs.append(dict(n=n.positive(),d=d.positive()))
  for i in range(k+1,len(A)):
   for j in range(k+1,len(A)):
    u=next(updates)
    if (u['k'],u['i'],u['j'])!=(k,i,j)or [u['pivot'],u['before'],u['left'],u['right']]!=[piv,A[i][j],A[i][k],A[k][j]]:raise ValueError('detached elimination')
    prove_update(u);A[i][j]=u['after']
 try:next(updates);raise ValueError('extra elimination')
 except StopIteration:pass
 return dict(name=data['name'],signs=signs,pivots=len(signs),identities=len(data['updates']))
if __name__=='__main__':
 data=json.loads(Path(sys.argv[1]).read_text());print(json.dumps(check(data),sort_keys=True))
