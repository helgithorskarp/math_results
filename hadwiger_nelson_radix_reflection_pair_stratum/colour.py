"""Exact bivariate projections and actual-edge colour obligations."""
from pathlib import Path
import importlib.util,math
from fractions import Fraction as F
from itertools import product,combinations
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
V=load('reflection_pair_reviewer_inventory',ROOT/'hadwiger_nelson_radix_four_active_closure_review1/independent_check.py')
X=load('reflection_pair_polynomial_arithmetic',ROOT/'hadwiger_nelson_radix_reflection_axes/exact.py')
weights=[(1,)+w for w in product(range(3),repeat=4)]
def add(a,b,scale=1):
 out=dict(a)
 for m,c in b.items():out[m]=out.get(m,F(0))+scale*c
 return {m:c for m,c in out.items() if c}
def mul(a,b):
 out={}
 for (i,j),aij in a.items():
  for (k,l),bkl in b.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+aij*bkl
 return {m:c for m,c in out.items() if c}
def project(f):
 powers=[{(0,0):F(1)}]
 for _ in range(4):powers.append(mul(powers[-1],{(0,1):F(1,3),(2,0):F(-1,12)}))
 E={};O={}
 for i,j,c in f:
  term={(i+a,b):v*F(c,2**i) for (a,b),v in powers[j//2].items()}
  if j%2:O=add(O,term)
  else:E=add(E,term)
 den=math.lcm(*(v.denominator for v in list(E.values())+list(O.values())))
 E={m:int(c*den) for m,c in E.items()};O={m:int(c*den) for m,c in O.items()}
 g=math.gcd(*list(E.values()),*list(O.values()));g=g or 1
 es=tuple((i,j,c//g) for (i,j),c in sorted(E.items()));os=tuple((i,j,c//g) for (i,j),c in sorted(O.items()))
 es,os=min((es,os),(tuple((i,j,-c) for i,j,c in es),tuple((i,j,-c) for i,j,c in os)))
 os=min(os,tuple((i,j,-c) for i,j,c in os))
 return es,os
def inventory():
 _,fs,circle,monos,rowids=V.reconstruct_inventory();bad=[set() for _ in weights]
 colours=[[sum(w*a for w,a in zip(word,label))%3 for label in V.LABELS] for word in weights]
 for a,b in combinations(range(243),2):
  owner=V.edge_owner(a,b,monos,rowids,circle)
  for i,colour in enumerate(colours):
   if colour[a]==colour[b]:
    X.need(owner!='base','proper universal edge');bad[i].add(owner)
 projections=list(map(project,fs));return [[p for p in sorted({projections[c] for c in cs})] for cs in bad]
def trim(a):
 while a and not a[-1]:a.pop()
 return a
class Ring:
 def __init__(self,q,p):
  self.p=p;inv=pow(q[-1]%p,-1,p);self.q=[x*inv%p for x in q];self.n=len(q)-1
 def red(self,a):
  p=self.p;q=self.q;n=self.n;a=[v%p for v in a]
  for k in range(len(a)-1,n-1,-1):
   v=a[k]
   if v:
    for j in range(n):a[k-n+j]=(a[k-n+j]-v*q[j])%p
  return trim(a[:n])
 def mul(self,a,b):
  out=[0]*max(0,len(a)+len(b)-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):out[i+j]+=x*y
  return self.red(out)
 def scalar(self,a,c):return trim([c*v%self.p for v in a])
 def add(self,a,b,scale=1):
  out=a[:]+[0]*max(0,len(b)-len(a))
  for i,v in enumerate(b):out[i]=(out[i]+scale*v)%self.p
  return trim(out)
 def rational(self,cs):return self.red([F(v).numerator%self.p*pow(F(v).denominator%self.p,-1,self.p)%self.p for v in cs])
def check(component,case,allbad):
 q,ts,rs=component;p=case['prime'];X.need(q[-1]%p,'parameter degree survives modulo prime');A=Ring(q,p);T=A.rational(ts);R=A.rational(rs)
 tp=[[1]];rp=[[1]]
 for _ in range(4):tp.append(A.mul(tp[-1],T));rp.append(A.mul(rp[-1],R))
 mon={(i,j):A.mul(tp[i],rp[j]) for i in range(5) for j in range(5-i)};delta=A.add(A.scalar(R,4),A.mul(T,T),-1)
 def ev(es):
  out=[]
  for i,j,c in es:out=A.add(out,mon[i,j],c)
  return out
 for es,os in allbad[case['colour']]:
  E,O=ev(es),ev(os);h=A.add(A.scalar(A.mul(E,E),12),A.mul(delta,A.mul(O,O)),-1)
  X.need(X.gcd_is_one(A.q,h,p),'every colour-bad actual edge excluded on the whole algebraic component')
