#!/usr/bin/env python3
"""Direct all-pairs geometry at both roots of the 23-contact example.

Independent integer basis 1,z,alpha,alpha*z,r,z*r,alpha*r,alpha*z*r,
z^2=33, alpha^2=-3, r^2=-408+72*z, with real z,r and imaginary alpha.
"""
from pathlib import Path
from hashlib import sha256
from itertools import permutations
import json
HERE=Path(__file__).resolve().parent
ZERO=(0,)*8
ONE=(1,)+(0,)*7

def require(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,t):return tuple(t*x for x in a)
def conjugate(a):return tuple(-x if i&2 else x for i,x in enumerate(a))
def multiply(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   common=i&j;k=i^j;v=x*y*(33 if common&1 else 1)*(-3 if common&2 else 1)
   if common&4:
    out[k]-=408*v
    out[k^1]+=72*v*(33 if k&1 else 1)
   else:out[k]+=v
 return tuple(out)
def norm(a):return multiply(a,conjugate(a))
def digest(a):return sha256(json.dumps(a,separators=(',',':')).encode()).hexdigest()
def read(n):
 pin={159:'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',214:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}[n]
 raw=(HERE.parent/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes()
 require(sha256(raw).hexdigest()==pin,'source pin mismatch')
 rows=[]
 for line in raw.decode().splitlines():
  if not line or line.startswith('#'):continue
  a=tuple(map(int,line.split()));require(len(a)==16 and not any(a[i] for i in range(16) if i not in (0,5,9,12)),'wrong basis')
  rows.append((3*a[0],3*a[5],3*a[9],a[12],0,0,0,0))
 require(len(rows)==len(set(rows))==n,'bad source count')
 return rows

def main():
 # Positive in the selected real embedding; its other real conjugate is negative.
 require(408**2 < 72**2*33,'radicand is not positive')
 z=(0,1,0,0,0,0,0,0);alpha=(0,0,1,0,0,0,0,0);r=(0,0,0,0,1,0,0,0)
 require(multiply(z,z)==scale(ONE,33) and multiply(alpha,alpha)==scale(ONE,-3),'base relation failed')
 require(multiply(r,r)==(-408,72,0,0,0,0,0,0),'extension relation failed')
 A,V=read(159),read(214)
 t=(15,3,15,-1,0,0,0,0) # 36 times the inner translation.
 B=list(dict.fromkeys(A+[add(conjugate(a),t) for a in A]))
 require(len(B)==293 and B[0]==ZERO,'incorrect inner assembly')
 example=json.loads((HERE/'maximum_example.json').read_text());q=example['anchor']
 require(q==10 and V[q]==(0,0,6,0,0,0,0,0),'incorrect anchor')
 H=[add(v,scale(V[q],-1)) for v in V];labels=[j for j in range(214) if j!=q]
 lb,lv=([tuple(map(int,l)) for l in (HERE/f'colors_{name}.txt').read_text().splitlines()] for name in ('B','V'))
 require(all(len(c)==293 and c[0]==0 and set(c)<=set(range(4)) for c in lb),'invalid B colour domain')
 require(all(len(c)==214 and set(c)<=set(range(4)) for c in lv),'invalid V colour domain')
 perms=[(0,)+p for p in permutations((1,2,3))]
 # Polynomial X^2-TX+W. These are 6*T and 6*W in this basis.
 T=(-3,-1,-5,1,0,0,0,0);W=(0,1,-1,0,0,0,0,0)
 results=[]
 for epsilon in (-1,1):
  u=(-18,-6,-30,6,3*epsilon,0,6*epsilon,epsilon)
  require(norm(u)==scale(ONE,72**2),'rotation is not unit')
  require(add(add(multiply(u,u),scale(multiply(T,u),-12)),scale(W,864))==ZERO,'rotation fails quadratic')
  image=[multiply(u,h) for h in H]
  points=[scale(b,72) for b in B]+[image[j] for j in labels]
  require(len(points)==len(set(points))==506,'unexpected coincidence')
  edges=[];cross=[];left=right=0
  for i,a in enumerate(points):
   for j in range(i+1,len(points)):
    if norm(add(a,scale(points[j],-1)))!=scale(ONE,2592**2):continue
    edges.append((i,j))
    if j<293:left+=1
    elif i==0 or i>=293:right+=1
    else:cross.append((i,labels[j-293]))
  require((left,right,len(cross),len(edges))==(1389,977,23,2389),'incorrect strict edge census')
  require(sorted(cross)==sorted(map(tuple,example['cross_edges'])),'incorrect projected edges')
  selected=next(((i,j,k) for i,cb in enumerate(lb) for j,cv in enumerate(lv) for k,p in enumerate(perms) if all(cb[b]!=p[cv[v]^cv[q]] for b,v in cross)),None)
  require(selected is not None,'no full colouring')
  i,j,k=selected;colors=lb[i]+tuple(perms[k][lv[j][v]^lv[j][q]] for v in labels)
  require(all(colors[a]!=colors[b] for a,b in edges),'invalid full colouring')
  bad=list(colors);bad[edges[0][1]]=bad[edges[0][0]]
  require(not all(bad[a]!=bad[b] for a,b in edges),'colour mutation not detected')
  results.append({'epsilon':epsilon,'vertices':506,'strict_edges':len(edges),'cross_edges':len(cross),'witness':selected,'edge_sha256':digest(edges),'colour_sha256':digest(colors)})
 print(json.dumps({'coordinate_scale':2592,'pairs_per_root':127765,'both_real_roots_checked':True,'unit_and_quadratic_checked':True,'colour_mutation_rejected':True,'realizations':results},indent=2))
if __name__=='__main__':main()
