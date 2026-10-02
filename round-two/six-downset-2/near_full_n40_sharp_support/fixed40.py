"""Separate fixed n40 full-star Gaussian audit and ordinary8106 reference.

six-downset-2, researcher. The credited9365 old RREF guard is unchanged.
This new finite-domain audit solves all399 supported coordinates/38rows.
"""
from fractions import Fraction as Q
import model,affine

def fixed_rref():
 """Independent Gaussian elimination of EVERY original n40 star row."""
 n=40;r,N,s=model.parameters(n);pairs=affine.supported_pairs(n);rows=[]
 for a in range(1,r+1):
  coefficients=[]
  for i,j in pairs:
   b=j if a==i else i if a==j else None
   coefficients.append(Q(b*model.choose(n-a,b)) if b is not None else Q(0))
  rows.append(coefficients+[Q((n-a)*s)])
 pos=0;pivots=[]
 for col in range(len(pairs)):
  hit=next((i for i in range(pos,len(rows)) if rows[i][col]),None)
  if hit is None:continue
  rows[pos],rows[hit]=rows[hit],rows[pos];p=rows[pos][col]
  rows[pos]=[v/p for v in rows[pos]]
  for i in range(len(rows)):
   if i!=pos and rows[i][col]:
    c=rows[i][col];rows[i]=[v-c*w for v,w in zip(rows[i],rows[pos])]
  pivots.append(col);pos+=1
 free=[i for i in range(len(pairs)) if i not in pivots]
 freepairs=[pairs[i] for i in free]
 model.require(len(pivots)==38 and len(pairs)==399 and len(freepairs)==361,
               'Fixedn40 full supported/star/free dimensions')
 model.require(freepairs==[p for p in pairs if p[0]>=2],'Full unrestricted-star coordinates')
 def recover(values):
  model.require(len(values)==361 and all(type(v) is Q for v in values),'All361 exact free values')
  z=[Q(0)]*len(pairs)
  for i,v in zip(free,values):z[i]=v
  for row,col in zip(rows,pivots):z[col]=row[-1]-sum(row[i]*z[i] for i in free)
  B=[[Q(0)]*(r+1) for _ in range(r+1)]
  for (a,b),v in zip(pairs,z):B[a][b]=B[b][a]=v
  affine.check_stars(n,B);return B
 return freepairs,recover

def ordinary_reference():
 """Exact8106 z1 table; its cap FAILS, hence it is not an S11 cap seed."""
 n=40;r,N,s=model.parameters(n);q=2**(n-2)-2
 pairs=[p for p in affine.supported_pairs(n) if p[0]>=2]
 values=[Q(s-1 if a+b==n else 0) for a,b in pairs]
 B=affine.direct(n,values);free,recover=fixed_rref()
 model.require(free==pairs and recover(values)==B,'All-row ordinary reference decoder agreement')
 model.require(B[1][1]==s-q and all(B[1][a]==1 for a in range(2,r+1)),
               'Published8106 z1 singleton/complement table')
 return pairs,values,B
