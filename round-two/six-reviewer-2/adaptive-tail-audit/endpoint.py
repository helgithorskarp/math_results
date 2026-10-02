"""Own complete harmonic Gram decoder as exact Q(u), q=4+u.

Credited incidence mathematics8757/own9488 finite sectors; no new9195
executable, decoder, EXPECTED or RESULTS consulted. Original table formulas
are explicit prior mathematics. Universal proof uses coefficients.
"""
from fractions import Fraction as F
from math import comb
import json,signal
from polynomial import Rat,determinant
from linear import need,canonical,digest
from affine import table as literal

def alarm(*unused):raise TimeoutError('fixed60s endpoint guard; incomplete is not exclusion')
signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
q=Rat([4,1]);s=3*q+4
TYPES=[(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)]
def choose(n,r):
 if isinstance(n,int):return Rat(comb(n,r)if 0<=r<=n else 0)
 if r<0:return Rat(0)
 out=Rat(1)
 for j in range(r):out=out*(n-j)/(j+1)
 return out

def table():
 o,p,a,b,c,d,e=TYPES;Q={}
 def put(x,y,v):Q[tuple(sorted((x,y)))]=Rat(v)
 g=1+6/q
 put(o,o,(g-1+2*q-s)/(q-1));put(o,p,q*(q-3)/((q-1)*(q-2)))
 put(p,p,(g-1+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2))
 for x,aa,bb in [(o,1-1/q,1+1/q),(p,Rat(1),1+2*(q-1)/(q*(q-2)))]:
  for y in [a,c]:put(x,y,aa)
  for y in [b,d]:put(x,y,bb)
  put(x,e,g)
 for x,y in [(a,a),(a,b),(b,b)]:put(x,y,0)
 put(a,c,2);put(a,d,3+2/q);put(b,c,3+2/q);put(b,d,(s-3-2/q)/(q-1))
 need(len(Q)==20,'whole symbolic prior table')
 for qq in [4,5,7,12,23]:
  L=literal(qq,0);need({key:v.value(qq-4)for key,v in Q.items()}==L,'all20 symbolic entries against credited own literal path')
 return Q

def run():
 Q=table();mult=2*q*(q-1)*(q-2)*(q-3);need(mult.sign()==1,'positive denominator multiplier');out=[];allminors=[];margins=[]
 for j,l in [(0,0),(1,0),(0,1),(1,1),(0,2)]:
  kept=[t for t in TYPES if j<=t[0]<=3-j and l<=t[1]]
  weights=[choose(3-2*j,a-j)*choose(q-2*l,b-l)for a,b in kept];G=[];H=[]
  for i,(a,b)in enumerate(kept):
   row=[]
   for m,(c,d)in enumerate(kept):
    number=choose(3-a-j,c-j)*choose(q-b-l,d-l)
    z=s*int(i==m)+Q.get(tuple(sorted(((a,b),(c,d)))),Rat(0))*((-1)**(j+l))*number
    if j==l==0:z-=weights[m]
    row.append(z)
   H.append(row);G.append([weights[i]*v for v in row])
  need(all(G[i][m]==G[m][i]for i in range(len(kept))for m in range(len(kept))),'symbolic entire harmonic Gram symmetry')
  kernels=[];anchors=[]
  if j==l==0:
   kernels=[[a for a,b in kept],[int(a>=2)for a,b in kept],[1]*len(kept)];anchors=[kept.index(t)for t in [(0,1),(1,0),(2,0)]]
  elif j==1 and l==0:kernels=[[1]*len(kept)];anchors=[kept.index((1,0))]
  for v in kernels:need(all(sum(row[m]*v[m]for m in range(len(kept)))==0 for row in G),'symbolic kernel action')
  if kernels:
   anchor=[[F(v[i])for v in kernels]for i in anchors]
   need(determinant([[(v,)for v in row]for row in anchor])!=(F(0),)and determinant([[(v,)for v in row]for row in anchor])!=(),'actual kernel anchor independence')
  ix=[i for i in range(len(kept))if i not in anchors]
  quotient=[[(mult*G[i][m]).polynomial()for m in ix]for i in ix]
  minors=[]
  for n in range(1,len(ix)+1):
   z=determinant([row[:n]for row in quotient[:n]]);need(z and z[0]>0 and all(v>=0 for v in z),'unbounded quotient minor positivity');minors.append(z);allminors.append(z)
  v=[]
  for a,b in kept:
   if j==l==0:v.append(4/(3*q)if a==0 else 2+1/q if a==3 else Rat(1))
   elif(j,l)==(0,1):v.append(Rat(1)if a==0 else Rat(F(9,10)))
   else:v.append(Rat(1))
  signs=[];sector_margins=[]
  for i,row in enumerate(H):
   signed=[z.sign()for z in row];signs.append(signed)
   margin=2*s-sum(signed[m]*z*v[m]/v[i]for m,z in enumerate(row))
   need(margin.sign()in [0,1],'all-order weighted infinity margin');sector_margins.append(margin.record());margins.append(margin.record())
  out.append({'sector':[j,l],'types':kept,'kernel_columns':kernels,'deleted_anchors':anchors,'quotient_dimension':len(ix),'quotient_polynomial_entries':[[list(map(str,z))for z in row]for row in quotient],'leading_determinant_coefficients':[[str(v)for v in z]for z in minors],'entry_signs':signs,'positive_weights':[w.record()for w in v],'upper_margins':sector_margins})
 need(len(allminors)==14 and len(margins)==18,'full endpoint certificates')
 record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','q':'4+u, ALL REAL u>=0 for arithmetic signs; family integers q>=4','sectors':out,'minor_degrees':[len(z)-1 for z in allminors],'minor_count':14,'upper_margin_count':18,'whole_sector_dimension':'7+2*4+(q-1)*4+2*(q-1)*2+q*(q-3)/2=N0-1','whole_kernel_dimension':5,'symbolic_table_calibration_entries':100,'trust':'ordinary complete layer/kernel-anchor/weighted-norm bridges credited8757; universal coefficient proof, no sampled fit'}
 print(json.dumps(record,sort_keys=True,separators=(',',':')))
if __name__=='__main__':run()
