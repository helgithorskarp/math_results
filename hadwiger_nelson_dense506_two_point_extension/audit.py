"""Independent determinant scan in the original eight-coefficient complex algebra."""
from pathlib import Path
from fractions import Fraction
from math import lcm,gcd,comb
from collections import defaultdict,Counter
from hashlib import sha256
import importlib.util,json,time,argparse,struct,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
SOURCE=ROOT/'hadwiger_nelson_dense506_origin_attachment/controls.py'
if sha256(SOURCE.read_bytes()).hexdigest()!='b73d839cdfd72ed8020e0122124f7768cc62852289f1e4d6db74079add47a1c4':raise ValueError('source pin mismatch')
s=importlib.util.spec_from_file_location('C',SOURCE);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
D=2592;unit=C.scale(C.ONE,D*D)
def inverse(a):
 b=C.conjugate(a);c=tuple(-x if i&4 else x for i,x in enumerate(a));d=C.conjugate(c)
 numerator=C.multiply(C.multiply(b,c),d);n=C.multiply(a,numerator)
 assert not any(n[2:]);den=n[0]*n[0]-33*n[1]*n[1];assert den
 top=C.multiply(numerator,(n[0],-n[1],0,0,0,0,0,0))
 return tuple(Fraction(x,den) for x in top)
def key(a):
 nums=tuple(Fraction(a[i],D) for i in (0,1,4,5,2,3,6,7));den=lcm(*(x.denominator for x in nums));ints=tuple(int(x*den) for x in nums);g=gcd(den,*ints)
 return (den//g,)+tuple(x//g for x in ints)
def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
 start=time.monotonic();A,V=C.read(159),C.read(214);translation=(15,3,15,-1,0,0,0,0);u=(-18,-6,-30,6,3,0,6,1)
 B=list(dict.fromkeys(A+[C.add(C.conjugate(a),translation) for a in A]));P=[C.scale(b,72) for b in B]+[C.multiply(u,C.add(V[j],C.scale(V[10],-1))) for j in range(214) if j!=10]
 assert len(P)==len(set(P))==506
 p,z,r=5281,126,3928;assert z*z%p==33 and r*r%p==(-408+72*z)%p
 iv=pow(D,-1,p);XY=[(sum(a[i]*t for i,t in zip((0,1,4,5),(1,z,r,z*r)))*iv%p,sum(a[i]*t for i,t in zip((2,3,6,7),(1,z,r,z*r)))*iv%p) for a in P]
 nd=[[None]*506 for _ in P];md=[[0]*506 for _ in P];ee=[]
 for i,a in enumerate(P):
  for j in range(i+1,506):
   d=C.add(P[j],C.scale(a,-1));n=C.norm(d);nd[i][j]=nd[j][i]=n
   X,Y=XY[i][0]-XY[j][0],XY[i][1]-XY[j][1];md[i][j]=md[j][i]=(X*X+3*Y*Y)%p
   if n==unit:ee.append((i,j))
 assert len(ee)==2389
 print('geometry ready',time.monotonic()-start,file=sys.stderr,flush=True)
 retained=[]
 for i in range(506):
  xi,yi=XY[i]
  for j in range(i+1,506):
   dx,dy=XY[j][0]-xi,XY[j][1]-yi;a=md[i][j]
   for k in range(j+1,506):
    ex,ey=XY[k][0]-xi,XY[k][1]-yi;det=(dx*ey-ex*dy)%p
    if (a*md[i][k]*md[j][k]-12*det*det)%p==0:retained.append((i,j,k))
 print('modular retained',len(retained),'seconds',time.monotonic()-start,file=sys.stderr,flush=True)
 actual={tuple(Fraction(x) for x in a) for a in P};centres=defaultdict(list);known=0;positive=[]
 for i,j,k in retained:
  d=C.add(P[j],C.scale(P[i],-1));e=C.add(P[k],C.scale(P[i],-1))
  determinant=C.add(C.multiply(C.conjugate(d),e),C.scale(C.multiply(C.conjugate(e),d),-1))
  product=C.multiply(C.multiply(nd[i][j],nd[i][k]),nd[j][k])
  if C.add(product,C.scale(C.multiply(determinant,determinant),D*D))!=C.ZERO:continue
  assert determinant!=C.ZERO
  numerator=C.add(C.multiply(nd[i][j],e),C.scale(C.multiply(nd[i][k],d),-1))
  v=C.multiply(numerator,inverse(determinant));h=C.add(P[i],v)
  assert C.norm(v)==unit
  if h in actual:known+=1;continue
  hk=key(h);centres[hk].append((i,j,k));positive.append((i,j,k))
 print('exact centres',len(centres),'known',known,'seconds',time.monotonic()-start,file=sys.stderr,flush=True)
 pts=sorted(centres);nn=[sorted({x for t in centres[h] for x in t}) for h in pts]
 original=json.loads((args.work/'candidates.json').read_text())
 assert pts==list(map(tuple,original['points'])) and nn==original['neighbors'] and positive==list(map(tuple,original['positive_triples']))
 assert all(len(centres[h])==comb(len(n),3) for h,n in zip(pts,nn))

 # Independent adjacency: direct eight-basis norm, using a different modulus.
 def decode(h):return (h[1],h[2],h[5],h[6],h[3],h[4],h[7],h[8]),h[0]
 def modpoint(h):
  a,d=h
  if d%p==0:return None
  iv=pow(d,-1,p)
  return (sum(a[i]*t for i,t in zip((0,1,4,5),(1,z,r,z*r)))*iv%p,sum(a[i]*t for i,t in zip((2,3,6,7),(1,z,r,z*r)))*iv%p)
 def unit_pair(h,k):
  a,d=h;b,e=k
  return C.norm(C.add(C.scale(a,e),C.scale(b,-d)))==C.scale(C.ONE,(d*e)**2)
 def maybe(a,b):return a is None or b is None or ((a[0]-b[0])**2+3*(a[1]-b[1])**2-1)%p==0
 hc=[(a,D) for a in P];cc=[decode(h) for h in pts];mh=list(map(modpoint,hc));mc=list(map(modpoint,cc))
 rebuilt=[];host_exact=pair_exact=0
 for a,ma in zip(cc,mc):
  neighbors=[]
  for j,(b,mb) in enumerate(zip(hc,mh)):
   if maybe(ma,mb):
    host_exact+=1
    if unit_pair(a,b):neighbors.append(j)
  rebuilt.append(neighbors)
 assert rebuilt==nn
 cedges=[]
 for i in range(len(cc)):
  for j in range(i+1,len(cc)):
   if maybe(mc[i],mc[j]):
    pair_exact+=1
    if unit_pair(cc[i],cc[j]):cedges.append((i,j))
 assert cedges==list(map(tuple,original['candidate_edges']))
 rows=(HERE/'host_colors.txt').read_text().splitlines();assert len(rows)==1
 color=tuple(map(int,rows[0]));assert len(color)==506 and set(color)<=set(range(4)) and all(color[i]!=color[j] for i,j in ee)
 allowed=[tuple(c for c in range(4) if all(color[v]!=c for v in ns)) for ns in nn]
 assert all(allowed)
 av=[sum(1<<c for c in ls) for ls in allowed];assert av==original['available_masks']
 adj=set(cedges);wh=sha256();checked=0
 for i in range(len(cc)):
  for j in range(i+1,len(cc)):
   witness=next(((a,b) for a in allowed[i] for b in allowed[j] if (i,j) not in adj or a!=b),None)
   assert witness is not None
   wh.update(struct.pack('<HHBB',i,j,*witness));checked+=1
 assert checked==comb(len(cc),2)
 out={'independent_modular_prime':p,'root_z':z,'root_r':r,'triples':comb(506,3),'modular_survivors_including_host_centres':len(retained),'exact_known_host_centre_triples':known,'exact_new_centre_triples':len(positive),'candidate_points':len(pts),'every_candidate_and_neighbor_and_positive_triple_match':True,'positive_triple_sha256':digest(positive),'candidate_point_sha256':digest(pts),'neighbor_sha256':digest(nn),'independent_host_candidate_exact_tests':host_exact,'independent_candidate_pair_exact_tests':pair_exact,'host_candidate_edges':sum(map(len,nn)),'candidate_edges':len(cedges),'candidate_edge_sha256':digest(cedges),'available_masks_match':True,'all_pairs_explicitly_coloured':checked,'pair_witness_sha256':wh.hexdigest(),'uncovered':0}
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
