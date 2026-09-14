"""Separate contact-polynomial geometry and transposed colour-word audit.

No imports from model, producer, or main verifier. Geometry is calculated in
Q(sqrt(2),sqrt(3)), using independence of sqrt(7) for contact decisions.
"""
from itertools import combinations,product
from math import gcd,isqrt
from pathlib import Path
from hashlib import sha256
import json

D=(1,2,3,6)
def need(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(k*x for x in a)
def mul(a,b):
 out={d:0 for d in D}
 for d,x in zip(D,a):
  for e,y in zip(D,b):
   g=gcd(d,e);out[d*e//(g*g)]+=x*y*g
 return tuple(out[d] for d in D)
def digest(obj):return sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def audit():
 # Six times the atom coordinates, specified independently in four real radicals.
 A=[((0,0,0,0),(0,0,0,0)),((6,0,0,0),(0,0,0,0)),
    ((0,0,0,0),(0,6,0,0)),((6,0,0,0),(0,6,0,0)),
    ((0,-3,0,0),(0,3,0,0)),((6,-3,0,0),(0,3,0,0))]
 A += [((3,0,0,s),(0,3,t,0)) for s,t in product((-1,1),repeat=2)]
 norms=[];edges=[]
 for i,j in combinations(range(100),2):
  ia,ib=divmod(i,10);ja,jb=divmod(j,10)
  ax,ay=(sub(A[ia][k],A[ja][k]) for k in range(2))
  bx,by=(sub(A[ib][k],A[jb][k]) for k in range(2))
  aa=add(mul(ax,ax),mul(ay,ay));bb=add(mul(bx,bx),mul(by,by))
  dot=add(mul(ax,bx),mul(ay,by));cross=sub(mul(ax,by),mul(ay,bx))
  # 72*(squared physical distance) = 2*aa+2*bb-3*dot-sqrt(7)*cross.
  real=sub(scale(add(aa,bb),2),scale(dot,3))
  norms.append(scale(real,8)+scale(cross,-8))
  if real==(72,0,0,0) and cross==(0,0,0,0):edges.append((i,j))
 need(len(edges)==344 and len(norms)==4950,'complete contact-polynomial graph')
 # Independent rational-enclosure signs for every distance-half bridge gate.
 ds=(1,2,3,6,7,14,21,42);den=1<<64
 lows=[isqrt(d*den*den) for d in ds]
 highs=[a if a*a==d*den*den else a+1 for a,d in zip(lows,ds)]
 bridge=0;boundary=0;positive=0
 for n in norms:
  for offset in (0,144):
   m=(n[0]-offset,)+n[1:]
   if not any(m):
    need(offset==144,'no physical collision');boundary+=1;bridge+=1;continue
   lo=sum(c*(a if c>=0 else b) for c,a,b in zip(m,lows,highs))
   hi=sum(c*(b if c>=0 else a) for c,a,b in zip(m,lows,highs))
   need(lo>0 or hi<0,'rational sign enclosure decides exact sign')
   if offset==0:need(lo>0,'physical point separation');positive+=1
   elif lo>0:bridge+=1
 words=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())['words']
 need(all(type(w) is str and len(w)==100 and set(w)<=set('0123') for w in words),'word format')
 bits=[[0]*4 for _ in range(100)]
 for k,w in enumerate(words):
  need(all(w[a]!=w[b] for a,b in edges),'proper word against alternate geometry')
  for i,c in enumerate(w):bits[i][int(c)]|=1<<k
 full=(1<<len(words))-1;same=[];different=[]
 for i,j in combinations(range(100),2):
  equal_mask=0
  for c in range(4):equal_mask|=bits[i][c]&bits[j][c]
  if equal_mask:same.append((i,j))
  if equal_mask!=full:different.append((i,j))
 need(set(same)==set(combinations(range(100),2))-set(edges),'all nonunit equality witnesses')
 need(len(different)==4950,'all distinct pairs separated')
 return {'status':'CONTACT-POLYNOMIAL AND TRANSPOSED AUDIT PASS',
         'points':100,'strict_unit_edges':344,'all_pair_norms':4950,
         'strictly_positive_squared_distances':positive,'distance_at_least_half_pairs':bridge,
         'distance_exactly_half_pairs':boundary,'same_colour_nonunit_pairs':len(same),
         'different_colour_pairs':len(different),'edge_sha256':digest(edges),
         'norm_sha256':digest(norms),'relation_sha256':digest([same,different])}

if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
