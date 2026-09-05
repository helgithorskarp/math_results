#!/usr/bin/env python3
"""Direct exact 506-point realizations attaining ten contacts at either hub."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations
from collections import Counter
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parent.parent
RAD=(2,3,11);Z=(0,)*8;ONE=(1,)+(0,)*7
TABLE=[]
for i in range(8):
 row=[]
 for j in range(8):
  c=1
  for k,p in enumerate(RAD):
   if (i&j)&(1<<k):c*=p
  row.append((i^j,c))
 TABLE.append(row)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 o=[0]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if y:
    k,c=TABLE[i][j];o[k]+=x*y*c
 return tuple(o)
def cmul(a,b):
 x,y=a;u,v=b;return (add(mul(x,u),neg(mul(y,v))),add(mul(x,v),mul(y,u)))
def cadd(a,b):return (add(a[0],b[0]),add(a[1],b[1]))
def cscale(a,k):return tuple(tuple(k*x for x in row) for row in a)
def csub(a,b):return cadd(a,cscale(b,-1))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def e(a,b,c,d):
 x=[0]*8;y=[0]*8;x[0]=a;x[6]=b;y[2]=c;y[4]=d;return (tuple(x),tuple(y))
def read(n):
 pin={159:'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',214:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}[n]
 raw=(ROOT/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes();assert sha256(raw).hexdigest()==pin
 pts=[]
 for line in raw.decode().splitlines():
  if not line or line.startswith('#'):continue
  x=list(map(int,line.split()));assert len(x)==16 and all(x[i]==0 for i in range(16) if i not in (0,5,9,12));pts.append(e(*(x[i] for i in (0,5,9,12))))
 assert len(pts)==len(set(pts))==n;return pts

def main():
 A,V=read(159),read(214);B=list(dict.fromkeys([cscale(a,6) for a in A]+[cmul(e(5,0,0,1),a) for a in A]));assert len(B)==292
 # u=(sqrt(3)+i sqrt(6))/3 has unit norm and degree four over E.
 ux=[0]*8;uy=[0]*8;ux[2]=1;uy[3]=1;u=(tuple(ux),tuple(uy));assert norm(u)==(9,)+(0,)*7
 # Verify 3*u_actual^4+2*u_actual^2+3=0 after multiplying by 27.
 u2=cmul(u,u);u4=cmul(u2,u2);assert cadd(cadd(u4,cscale(u2,6)),((81,)+(0,)*7,Z))==(Z,Z)
 paths=[('hadwiger_nelson_nonmono159_moser_triple/colors_B.txt','b9285f2967686bf5458588c6f949173ac8795412a7ffd94a60d687e5a8c260a3'),('hadwiger_nelson_mixed505_anchor0/colors_H.txt','25a072d1c55cef2318b76cd849ce3096091d25b37981c83bc11d00c416393b58')]
 colors=[]
 for path,pin in paths:
  raw=(ROOT/path).read_bytes();assert sha256(raw).hexdigest()==pin;colors.append(tuple(map(int,raw.decode().splitlines()[0])))
 cB,cV=colors;assert len(cB)==292 and len(cV)==214 and all(c in range(4) for c in cB+cV)
 rB=e(-48,8,-4,12) # scale 72, outside B; ten B neighbours
 sV=e(-3,-1,-5,-3) # scale 12, outside V; ten V neighbours
 cases=[('hub_in_V',[cadd(rB,cscale(cmul(u,csub(v,V[0])),2)) for v in V],[(b,0) for b in (74,191,193,205,210,229,232,257,264,266)]),('hub_in_B',[cscale(cmul(u,csub(v,sV)),2) for v in V],[(0,v) for v in (68,72,89,90,125,127,163,176,189,194)])]
 output=[]
 for name,W,expected in cases:
  pts=B+W;assert len(pts)==len(set(pts))==506
  edges=[(i,j) for i in range(506) for j in range(i+1,506) if norm(csub(pts[i],pts[j]))==(5184,)+(0,)*7]
  cross=[(i,j-292) for i,j in edges if i<292<=j];assert cross==expected
  assert sum(j<292 for i,j in edges)==1251 and sum(i>=292 for i,j in edges)==977
  perm=next(p for p in permutations(range(4)) if all(cB[b]!=p[cV[v]] for b,v in cross))
  cc=cB+tuple(perm[c] for c in cV);assert all(cc[i]!=cc[j] for i,j in edges)
  deg=Counter(i for e in cross for i in (e[0],292+e[1]))
  out={'case':name,'vertices':506,'pairs_checked':127765,'strict_edges':len(edges),'cross_edges':cross,'cross_degree_histogram':dict(sorted(Counter(deg.values()).items())),'color_permutation':perm,'proper_four_coloring':True,'edge_sha256':sha256(''.join(f'{i},{j}\n' for i,j in edges).encode()).hexdigest(),'color_sha256':sha256((''.join(map(str,cc))+'\n').encode()).hexdigest()};output.append(out)
 print(json.dumps({'rotation_unit_norm':True,'rotation_quartic_identity':True,'examples':output},indent=2))
if __name__=='__main__':main()
