"""Reconstruct VND case10 in Q(zeta24,sqrt5), independently of the source parser."""
from pathlib import Path
from itertools import combinations_with_replacement
from math import isqrt
from functools import lru_cache
import json,hashlib,time
from flint import fmpz_poly
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()
F=fmpz_poly([1,0,0,0,-1,0,0,0,1]);T=fmpz_poly([0,1]);ONE=fmpz_poly([1]);ZERO=fmpz_poly([])
pw=[T**k%F for k in range(24)];I=pw[6]
rad=[ONE,pw[3]+pw[21],pw[2]+pw[22],(pw[3]+pw[21])*(pw[2]+pw[22])%F]
def require(x,msg):
 if not x:raise ValueError(msg)
def key(p):return tuple(int(p[i]) for i in range(8))
def mul(a,b):return a*b%F
def conj(a):return sum((int(a[i])*pw[-i%24] for i in range(len(a))),ZERO)
def norm(a):return mul(a,conj(a))
def real_sign(p):
 # 2p=a+b sqrt2+c sqrt3+d sqrt6. All arithmetic below is integer enclosure.
 v=key(p);coeff=(2*v[0],v[1]-v[5],-2*v[6],v[1]+v[5])
 require(2*p==sum((x*b for x,b in zip(coeff,rad)),ZERO),'real-subfield representation')
 if not any(coeff):return 0
 for digits in (15,30,60):
  scale=10**digits;lo=hi=coeff[0]*scale
  for c,r in zip(coeff[1:],(2,3,6)):
   a=isqrt(r*scale*scale);b=a+1
   lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
  if lo>0:return 1
  if hi<0:return -1
 raise ValueError('unseparated clipping comparison')
def main():
 start=time.monotonic();require(pw[0]==ONE and T**24%F==ONE and all(T**(24//q)%F!=ONE for q in (2,3)),'root order')
 require(mul(I,I)==-ONE and all(mul(b,b)==r*ONE for b,r in zip(rad,(1,2,3,6))),'radical bridge')
 a=3*ONE+rad[3]+mul(I,3*rad[1]-rad[2]);require(norm(a)==36*ONE,'second generator')
 require(a==mul(pw[4],2*rad[3]-2*mul(I,rad[2])),'a/6 equals zeta24^4 times conjugate of paper phi1')
 m1={key(ZERO)}
 for j in range(24):
  for b in (6*ONE,a,conj(a)):m1.add(key(mul(pw[j],b)))
 require(len(m1)==73,'M1');m1=[fmpz_poly(list(q)) for q in sorted(m1)];m2=set()
 for u,v in combinations_with_replacement(m1,2):
  s=u+v
  if real_sign(norm(s)-36*ONE)<=0:m2.add(key(s))
 require(len(m2)==865,'M2');m2=[fmpz_poly(list(q)) for q in sorted(m2)];m3={key(u+v) for u in m2 for v in m1};require(len(m3)==32257,'M3')
 data=json.loads((P/'exact_points.json').read_text());require(data['denominator']==96,'source scale');rows=data['points'];mapped=[]
 for row in rows:
  pol=[]
  for offset in (0,4):
   x=sum((row[offset+k]*rad[k] for k in range(4)),ZERO)
   y=sum((row[8+offset+k]*rad[k] for k in range(4)),ZERO)
   pol.append(key(x+mul(I,y)))
  mapped.append(tuple(pol))
 require(len(set(mapped))==64513,'independent source distinctness')
 first={(tuple(16*x for x in q),(0,)*8) for q in m3}
 require(set(mapped[:32257])==first,'independent M3 source alignment')
 second=set()
 for q in m3:
  z=fmpz_poly(list(q));second.add((key(-14*z),key(2*mul(I,mul(rad[2],z)))))
 require(set(mapped[32257:])==second-{((0,)*8,(0,)*8)},'independent second half alignment')
 edges=json.loads((P/'exact_edges.json').read_text());differences=set()
 for u,v in edges:
  d=tuple(x-y for a,b in zip(mapped[u],mapped[v]) for x,y in zip(a,b));differences.add(min(d,tuple(-x for x in d)))
 for d in differences:
  a,b=fmpz_poly(list(d[:8])),fmpz_poly(list(d[8:]));A,B=conj(a),conj(b)
  require(mul(a,A)+5*mul(b,B)==96**2*ONE and mul(a,B)+mul(b,A)==ZERO,'cyclotomic unit norm')
 result={'verified':True,'independent_field':'Q[t]/(t^8-t^4+1), adjoining sqrt5','M1_M2_M3_counts':[73,865,32257],'complete_generated_source_point_set_equal':True,'source_points':len(rows),'all_declared_unit_edges_checked':len(edges),'exact_direction_classes_checked':len(differences),'coordinate_scale':96,'clipping':'integer radical enclosures, exact equality retained','mapped_points_sha256':hashlib.sha256(json.dumps(mapped,separators=(',',':')).encode()).hexdigest(),'nonedges_checked':False,'chromatic_lower_bound_reproved':False,'elapsed_seconds':time.monotonic()-start}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
