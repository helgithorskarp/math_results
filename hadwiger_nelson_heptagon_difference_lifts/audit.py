"""Independent Z[zeta7,omega6] arithmetic, denominator7, no producer imports."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,time
Z=(0,)*12;O=(1,)+Z[1:]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(k*x for x in a)
def monomial(i,j):
 # omega²=omega-1, zeta7^6=-(1+...+zeta7^5)
 terms={}
 for jj,v in ([(0,1)] if j==0 else [(1,1)] if j==1 else [(1,1),(0,-1)]):
  ii=i%7
  for k,c in ([(ii,v)] if ii<6 else [(k,-v) for k in range(6)]):terms[k+6*jj]=c
 return terms
TABLE=[[monomial(i%6+j%6,i//6+j//6) for j in range(12)] for i in range(12)]
def mul(a,b):
 out=[0]*12
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:
     for k,c in TABLE[i][j].items():out[k]+=c*x*y
 return tuple(out)
def zp(i):
 i%=7
 return tuple(int(k==i) for k in range(12)) if i<6 else (-1,)*6+(0,)*6
W=(0,)*6+(1,)+(0,)*5
T=mul(zp(6),W);TP=[O]
for _ in range(41):TP.append(mul(TP[-1],T))
def conjugate(a):
 out=Z
 for j,v in enumerate(a):
  b=zp(-j) if j<6 else mul(zp(-(j-6)),sub(O,W))
  out=add(out,scale(b,v))
 return out
def norm(a):return mul(a,conjugate(a))
def inv_sine_numerator(k):
 out=Z
 for j in range(7):out=add(out,scale(zp(k+2*k*j),j))
 assert mul(sub(zp(k),zp(-k)),out)==scale(O,7)
 return out
p=inv_sine_numerator(4);q=scale(mul(sub(O,W),inv_sine_numerator(1)),-1);r=scale(mul(W,inv_sine_numerator(2)),-1)
h=[mul(a,zp(j)) for a in [p,q,r] for j in range(7)];D=sorted({sub(a,b) for a in h for b in h})
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();w=args.work;x=json.loads((w/'graph.json').read_text());start=time.perf_counter()
def decode(row):
 out=Z
 for i,v in enumerate(row):out=add(out,scale(TP[i],v))
 return out
assert x['denominator']==7 and [decode(a) for a in x['host']]==h
points=list(map(decode,x['points']));assert len(points)==len(set(points))==421 and sorted(points)==D
ed=[];p3=[];p7=[];pS3=[]
for i,j in combinations(range(len(points)),2):
 d=norm(sub(points[i],points[j]))
 if d==scale(O,49):ed.append([i,j])
 if d==scale(O,441):p3.append([i,j])
 if d==scale(O,343):p7.append([i,j])
 if d==scale(O,147):pS3.append([i,j])
assert ed==x['edges'] and p3==x['distance3_pairs'] and pS3==x['sqrt3_pairs']
look={a:i for i,a in enumerate(points)};tri=[]
for i,j in p7:
 for rr in [W,sub(O,W)]:
  k=look.get(add(points[i],mul(sub(points[j],points[i]),rr)))
  if k is not None and k>j:tri.append([i,j,k])
assert sorted(tri)==sorted(x['sqrt7_triangles'])

# Build every edge constraint independently in this basis.
index={p:i for i,p in enumerate(points)};origin=index[Z];rep={origin:set()}
for a,b in combinations(range(21),2):
 for pt in [sub(h[a],h[b]),sub(h[b],h[a])]:
  j=index[pt];assert j not in rep;rep[j]={a,b}
cs=sorted({tuple(sorted(rep[a]^rep[b])) for a,b in ed})
assert Counter(map(len,cs))=={2:42,4:42}
fixed={0:0,7:1,14:2};order=[i for i in range(21) if i not in fixed];rank={a:j for j,a in enumerate(order)}
ending=[[] for _ in order]
for row in cs:
 free=[i for i in row if i not in fixed]
 if free:ending[max(rank[i] for i in free)].append(row)
 else:
  val=0
  for i in row:val^=fixed[i]
  assert val
c=[fixed.get(i,-1) for i in range(21)];lifts=[];nodes=0
def rec(j):
 global nodes
 nodes+=1
 if j==len(order):lifts.append(c.copy());return
 a=order[j]
 for v in range(4):
  c[a]=v;good=True
  for row in ending[j]:
   val=0
   for b in row:val^=c[b]
   if not val:good=False;break
  if good:rec(j+1)
 c[a]=-1
rec(0)
expected=json.loads((Path(__file__).resolve().parent/'potentials.json').read_text())
assert sorted(lifts)==expected==sorted(json.loads((w/'normalized_lifts.json').read_text()))
colours=[]
for row in lifts:
 colour=[]
 for i in range(421):
  val=0
  for a in rep[i]:val^=row[a]
  colour.append(val)
 assert all(colour[i]!=colour[j] for i,j in ed)
 assert all(colour[i]!=colour[j] for i,j in pS3)
 colours.append(colour)
# These84 prescribed dihedral candidates contain exactly14 actual isometries;
# we assert their orbits, not completeness among all possible isometries.
perms=[]
for reflect in [False,True]:
 for k in range(42):
  image=[mul(TP[k],conjugate(a) if reflect else a) for a in points]
  if set(image)==set(points):perms.append([index[a] for a in image])
left=set(map(tuple,pS3));orbits=[]
while left:
 a,b=min(left);orbit=sorted({tuple(sorted((perm[a],perm[b]))) for perm in perms})
 assert set(orbit)<=left;left-=set(orbit);orbits.append(orbit)
assert len(perms)==14 and [len(a) for a in orbits]==[14]*9
# Cyclic rotations of the seven indices in each of the three motif rings.
remaining={tuple(row) for row in lifts};potential_orbits=[]
while remaining:
 seed=min(remaining);orbit=set()
 for shift in range(7):
  row=[seed[(i//7)*7+(i+shift)%7] for i in range(21)]
  anchors=[row[i] for i in [0,7,14]];assert len(set(anchors))==3
  rename={v:j for j,v in enumerate(anchors)}
  rename[next(iter(set(range(4))-set(anchors)))]=3
  normalized=tuple(rename[v] for v in row);orbit.add(normalized)
 assert orbit<=remaining;remaining-=orbit;potential_orbits.append(sorted(orbit))
assert [len(o) for o in potential_orbits]==[7]*6
out={'points':len(points),'unordered_pairs':88410,'unit_edges':len(ed),'distance3_pairs':len(p3),'sqrt7_pairs':len(p7),'sqrt7_triangles':len(tri),'sqrt3_pairs':len(pS3),'constraints_by_size':dict(Counter(map(len,cs))),'complete_normalized_potentials':len(lifts),'potential_rotation_orbit_sizes':[len(o) for o in potential_orbits],'fixed_order_nodes':nodes,'all_lifted_edges_checked':len(lifts)*len(ed),'all_lifted_sqrt3_pairs_distinct':len(lifts)*len(pS3),'tested_isometries':len(perms),'sqrt3_orbit_sizes':[len(a) for a in orbits],'seconds':time.perf_counter()-start}
(w/'audit_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
