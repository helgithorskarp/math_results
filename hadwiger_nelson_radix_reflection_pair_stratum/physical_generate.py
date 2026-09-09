#!/usr/bin/env python3
"""FLINT Eisenstein-basis generator for both real quartic embeddings."""
from pathlib import Path
import sys,json,math,time,itertools
from fractions import Fraction as F
from flint import fmpq_poly as Q,fmpq,nmod_poly
import argparse
import colour as C
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
V=C.V;X=C.X
q=[-8,-5,22,-3,3]
ts=['-103/225','193/225','-4/25','1/75']
rs=['103/225','32/225','4/25','-1/75']
mod=Q(q)
T=Q([fmpq(s) for s in ts]);R=Q([fmpq(s) for s in rs]);D=(4*R-T*T)/12%mod
one=Q([1]);zero=Q([])
def add(a,b,scale=1):return tuple((x+scale*y)%mod for x,y in zip(a,b))
def mul(a,b):return ((a[0]*b[0]+D*a[1]*b[1])%mod,(a[0]*b[1]+a[1]*b[0])%mod)
def emul(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]),-1),add(add(mul(a[0],b[1]),mul(a[1],b[0])),mul(a[1],b[1]))
z=((T/2,-one),(zero,2*one));powers=[((one,zero),(zero,zero))]
for _ in range(4):powers.append(emul(powers[-1],z))
points=[];packed=[]
for word in V.LABELS:
 out=((zero,zero),(zero,zero))
 for j,d in enumerate(word):
  term=emul(powers[j],((Q([int(d==1)]),zero),(Q([int(d==2)]),zero)))
  out=(add(out[0],term[0]),add(out[1],term[1]))
 points.append(out)
 vals=[F(str(poly[i])) for pair in out for poly in pair for i in range(4)];den=math.lcm(*(v.denominator for v in vals));packed.append([int(v*den) for v in vals]+[den])
prime=next(p for p in (2,5,7,11,13,17,19,23,29,31,37,41,43,47,53) if q[-1]%p and len(nmod_poly(q,p).factor()[1])==1 and nmod_poly(q,p).factor()[1][0][0].degree()==4)
print('irreducible prime',prime,flush=True)
intervals=[['-155/322','-142/295'],['116/157','133/180']]
def peval(q,x):
 y=F(0)
 for c in reversed(q):y=y*x+F(str(c))
 return y
class Emb:
 def __init__(self,I):self.I=list(map(F,I));self.sign_calls=0;self.bisections=0
 def sign(self,poly):
  cs=[F(str(c)) for c in poly]
  if not cs:return 0
  self.sign_calls+=1
  while True:
   lo=hi=F(0);a,b=self.I
   for c in reversed(cs):
    ps=[lo*a,lo*b,hi*a,hi*b];lo,hi=min(ps)+c,max(ps)+c
   if lo>0:return 1
   if hi<0:return -1
   mid=(a+b)/2
   if peval(q,a)*peval(q,mid)<0:self.I[1]=mid
   else:self.I[0]=mid
   self.bisections+=1
 def iszero(self,n):
  a,b=n
  if not b:return not a
  if (a*a-D*b*b)%mod:return False
  return self.sign((a*b)%mod)<0
emb=[Emb(I) for I in intervals];edges=[[],[]];collisions=[[],[]];active=[set(),set()]
_,fs,circle,monos,rowids=V.reconstruct_inventory();col=[sum(a*b for a,b in zip(C.weights[14],w))%3 for w in V.LABELS]
for E in emb:
 X.need(E.sign(R)>0 and E.sign(D)>0 and E.sign(R-one)!=0 and E.sign(4*R-T*T)!=0 and E.sign(R-T*T)!=0,'physical embedding outside radial and reflection loci')
 for v in (R*R-T*T,R*R+R*T+T*T-3*R,R*R-R*T+T*T-3*R):X.need(E.sign(v%mod)!=0,'outside six anchor curves')
start=time.monotonic()
for i,j in itertools.combinations(range(243),2):
 a,b=(add(points[i][k],points[j][k],-1) for k in (0,1));N=add(add(mul(a,a),mul(a,b)),mul(b,b));Nm=add(N,(one,zero),-1)
 for k,E in enumerate(emb):
  if E.iszero(N):collisions[k].append((i,j))
  if E.iszero(Nm):
   X.need(col[i]!=col[j],'proper physical unit edge');edges[k].append((i,j));owner=V.edge_owner(i,j,monos,rowids,circle)
   if owner!='base':active[k].add(owner)
res={'schema':'hn-radix-reflection-pair-physical-v1','q':q,'trace':ts,'radius':rs,'irreducibility_prime':prime,'colour_word':list(C.weights[14]),'vertices':packed,'embeddings':[]}
for k,E in enumerate(emb):
 X.need(not collisions[k],'distinct vertices');X.need(all(v in edges[k] for v in ((0,81),(0,162),(81,162))),'unit triangle')
 res['embeddings'].append({'isolating_interval':intervals[k],'unit_edges':len(edges[k]),'edge_sha256':X.digest(edges[k]),'active_curves':sorted(active[k]),'chromatic_number':3})
 print('embedding',k,'edges',len(edges[k]),'active',sorted(active[k]),'sign calls',E.sign_calls,'bisections',E.bisections,flush=True)
with args.out.open('x') as file:json.dump(res,file,sort_keys=True,separators=(',',':'));file.write('\n')
print('completed exact physical generation',flush=True)
