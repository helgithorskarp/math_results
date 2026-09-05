"""Full pair traversal in E[u], with u^2=W, and independent auxiliary colorings."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from math import lcm
from itertools import product
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
def module(name,path,pin):
 assert sha256(path.read_bytes()).hexdigest()==pin,'dependency pin mismatch'
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=module('radical_coordinates',ROOT/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py','8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f')
K=module('rational_field',ROOT/'hadwiger_nelson_nonmono_field_obstruction/coloring.py','a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e')
C=module('rational_square',ROOT/'hadwiger_nelson_nonmono159_origin_pencil/census.py','31d1cf2e93b7b0cd6903425acbe6d30dcc0c089226bd7e588720327121bd1b43')
Z=(0,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def scale(x,k):return tuple(k*a for a in x)
def bar(x):return (x[0],x[1],-x[2],-x[3])
def mul(x,y):
 a,b,c,d=x;A,B,C,D=y
 return (a*A+33*b*B-3*c*C-11*d*D,a*B+b*A-c*D-d*C,a*C+c*A+11*(b*D+d*B),a*D+d*A+3*(b*C+c*B))
def norm(x):
 a,b,c,d=x;return (a*a+33*b*b+3*c*c+11*d*d,2*(a*b+c*d),0,0)
def inputs():
 A,V=R.read(159),R.read(214)
 B=list(dict.fromkeys([R.cscale(x,6) for x in A]+[R.cmul(R.e(5,0,0,1),x) for x in A]))
 def extract(P):
  out=[]
  for x,y in P:
   assert all(x[i]==0 for i in range(8) if i not in (0,6));assert all(y[i]==0 for i in range(8) if i not in (2,4))
   out.append((x[0],x[6],y[2],y[4]))
  return out
 return extract(B),extract(V)

def audit_case(B,V,row):
 i,j,k,l=row['seed'];BP=[K.element(*(Q(x,72) for x in b)) for b in B];VP=[K.element(*(Q(x,12) for x in v)) for v in V]
 db,dv=sub(BP[j],BP[i]),sub(VP[l],VP[k]);nb,nv=norm(db),norm(dv);assert add(nb,nv)==K.element(4)
 assert not C.real_square(tuple(x/3 for x in mul(nb,nv)[:2]))
 W=K.negate(K.multiply(K.multiply(db,K.conjugate(dv)),K.inverse(K.multiply(K.conjugate(db),dv))))
 assert K.multiply(W,K.conjugate(W))==K.ONE
 den=lcm(*(x.denominator for x in W));Wbar=tuple(int(x*den) for x in K.conjugate(W))
 mb,mv=scale(add(BP[i],BP[j]),Q(1,2)),scale(add(VP[k],VP[l]),Q(1,2))
 if K.color(db):
  assert row['branch']=='unit_diagonals' and K.color(dv)
  omega=K.element(Q(-1,2),0,Q(1,2));roots=[K.ONE,omega,K.multiply(omega,omega)]
  matches=[r for r in roots if K.color(sub(db,K.multiply(r,dv)))==0];assert len(matches)==1;rho=matches[0]
  cb=[K.color(sub(b,BP[i])) for b in BP]
  cv=[K.color(add(K.multiply(rho,sub(v,mv)),scale(db,Q(1,2)))) for v in VP]
 else:
  assert row['branch']=='even_diagonals' and K.color(dv)==0
  cb=[K.color(sub(b,mb)) for b in BP];cv=[K.color(sub(v,mv)) for v in VP]
 assert sha256((''.join(map(str,cb+cv))+'\n').encode()).hexdigest()==row['colors_sha256']
 # Each coordinate is (A+B*u)/144. Both roots are treated by the irreducible quotient.
 pts=[(tuple(int(x*144) for x in sub(b,mb)),Z) for b in BP]+[(Z,tuple(int(x*144) for x in sub(v,mv))) for v in VP]
 first={};aliases=[]
 for idx,p in enumerate(pts):aliases.append(first.setdefault(p,idx))
 assert len(first)==row['vertices'];assert all((cb+cv)[i]==(cb+cv)[aliases[i]] for i in range(len(pts)))
 edges=set();cross=[];tests=0
 for i in range(len(pts)):
  for j in range(i+1,len(pts)):
   tests+=1;A,Bb=sub(pts[i][0],pts[j][0]),sub(pts[i][1],pts[j][1])
   if add(norm(A),norm(Bb))!=(20736,0,0,0):continue
   # Coefficient of u in (A+B*u)*conjugate(A+B*u), multiplied by den.
   if add(mul(mul(A,bar(Bb)),Wbar),scale(mul(Bb,bar(A)),den))!=Z:continue
   aa,bb=sorted((aliases[i],aliases[j]));assert aa!=bb and (cb+cv)[aa]!=(cb+cv)[bb];edges.add((aa,bb))
   if i<len(B)<=j:cross.append((i,j-len(B)))
 h=sha256(''.join(f'{a},{b}\n' for a,b in sorted(edges)).encode()).hexdigest();ch=sha256(''.join(f'{a},{b}\n' for a,b in cross).encode()).hexdigest()
 assert h==row['union_edges_sha256'] and ch==row['cross_sha256'];assert len(edges)==row['strict_edges'] and len(cross)==row['cross_edges']
 return {'seed':row['seed'],'vertices':len(first),'pairs_checked':tests,'strict_edges':len(edges),'union_edges_sha256':h,'geometry_and_coloring_match':True}

def diagonal_census(B,V):
 from collections import Counter
 def lengths(P):
  return Counter(norm(sub(P[j],P[i])) for i in range(len(P)) for j in range(i+1,len(P)))
 bcounts,vcounts=lengths(B),lengths(V);out=Counter()
 for nv,vcount in sorted(vcounts.items()):
  nb=(20736-36*nv[0],-36*nv[1],0,0);bcount=bcounts.get(nb,0)
  if not bcount:continue
  squared=C.real_square(tuple(Q(x,3) for x in mul(nb,nv)[:2]))
  branch='in_E' if squared else 'outside_E'
  out[branch+'_norm_pairs']+=1;out[branch+'_segment_pairs']+=bcount*vcount
 assert out=={'in_E_norm_pairs':26,'in_E_segment_pairs':2551052,'outside_E_norm_pairs':51,'outside_E_segment_pairs':1748914}
 return dict(out)

def finite_rings():
 def m(x,y,q):
  a,b=x;c,d=y;return ((a*c-b*d)%q,(a*d+b*c-b*d)%q)
 def N(x,q):a,b=x;return (a*a-a*b+b*b)%q
 f2=list(product(range(2),repeat=2));f4=list(product(range(4),repeat=2))
 even=0;unit=0;roots=[(1,0),(0,1),(3,3)]
 assert [tuple(x%2 for x in r) for r in roots]==[(1,0),(0,1),(1,1)]
 assert all(N(r,4)==1 for r in roots)
 for x in f2:
  assert N(x,2)==int(x!=(0,0))
  for y in f2:
   if (N(x,2)+N(y,2))%2==1:assert x!=y;even+=1
 for x in f4:
  if N(x,4)%2==0:continue
  for y in f4:
   if N(y,4)%2==0 or (N(x,4)+N(y,4))%4:continue
   for r in roots:assert x!=m(r,y,4);unit+=1
 assert (even,unit)==(6,216)
 return {'mod2_cases':even,'mod4_cases':unit,'all_collision_exclusions_passed':True}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--cases',type=Path,default=HERE/'calibration.json')
 args=parser.parse_args();rows=json.loads(args.cases.read_text());assert len(rows)==51
 B,V=inputs();results=[audit_case(B,V,r) for r in rows]
 stream=json.dumps(results,separators=(',',':'))+'\n'
 out={'diagonal_census':diagonal_census(B,V),'finite_rings':finite_rings(),'selected_exact_cases':len(results),'pairs_checked_total':sum(r['pairs_checked'] for r in results),'all_geometry_and_colorings_match':all(r['geometry_and_coloring_match'] for r in results),'case_audit_sha256':sha256(stream.encode()).hexdigest()}
 print(json.dumps(out,indent=2))
