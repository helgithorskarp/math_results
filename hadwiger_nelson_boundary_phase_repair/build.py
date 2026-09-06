"""Exact finite boundary-phase repair for one quartic paired-circle support."""
from fractions import Fraction as F
from itertools import combinations,product
from collections import deque
import json,hashlib,argparse,time
from pathlib import Path
N=4
Z=(F(0),)*4
O=(F(1),F(0),F(0),F(0))
def scalar(v):return (F(v),F(0),F(0),F(0))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 c=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[(i+j)%4]+=x*y*(12 if i+j>=4 else 1)
 return tuple(c)
def sub(a,b):return plus(a,neg(b))
def scale(a,b):return tuple(b*x for x in a)
def ca(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def cn(a):return neg(a[0]),neg(a[1])
def cs(a,b):return ca(a,cn(b))
def cm(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),plus(mul(a[0],b[1]),mul(a[1],b[0]))
def cscale(a,b):return scale(a[0],b),scale(a[1],b)
def norm(a,b):
 x,y=cs(a,b);return plus(mul(x,x),mul(y,y))
def orbit(a):
 vs=[cm(a,u) for u in U];rep=min(vs);return rep,next(k for k,u in enumerate(U) if cm(rep,u)==a)
zero=(Z,Z);one=(O,Z);sqrt3=(F(0),F(0),F(1,2),F(0));eta=(F(0),F(1),F(0),F(0))
omega=(scalar(F(1,2)),scale(sqrt3,F(1,2)));U=[one]
for k in range(5):U.append(cm(U[-1],omega))
zeta=U[2];a1=U[4];u=(scale(sqrt3,F(1,2)),scalar(F(-1,2)))
y=cm(u,(scale(sub(O,sqrt3),F(1,2)),scale(eta,F(1,2))))
z=cm(u,(scale(sub(O,sqrt3),F(1,2)),scale(eta,F(-1,2))))
def encode(point):return [[[v.numerator,v.denominator] for v in axis] for axis in point]
def raw(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(data):return hashlib.sha256(raw(data)).hexdigest()
def check(ok,msg):
 if not ok:raise ValueError(msg)

from functools import lru_cache
COLOUR='01010122302113022330101030103102122010122032230112010110001122013303132101'
@lru_cache(None)
def sign(a):
 if a==Z:return 0
 lo,hi=F(1),F(2)
 while True:
  lower=upper=F(0)
  for c in reversed(a):
   v=[lower*lo,lower*hi,upper*lo,upper*hi]
   lower,upper=min(v)+c,max(v)+c
  if lower>0:return 1
  if upper<0:return -1
  mid=(lo+hi)/2
  if mid**4<12:lo=mid
  else:hi=mid

def det(v,w):return sub(mul(v[0],w[1]),mul(v[1],w[0]))
@lru_cache(None)
def rotated(v,k):return cm(v,U[k])
@lru_cache(None)
def length(v):return norm(v,zero)
@lru_cache(None)
def root_equal(v,s,w,t):
 """Compare unit chord roots via the exact intersection of two lines."""
 if v==w:return s==t
 d=det(v,w)
 if d==Z:return False
 q,r=length(v),length(w)
 n=(sub(mul(q,w[1]),mul(r,v[1])),sub(mul(r,v[0]),mul(q,w[0])))
 if length(n)!=scale(mul(d,d),4):return False
 sd=sign(d)
 return sign(det(v,n))*sd==s and sign(det(w,n))*sd==t

def geometry():
 D=[zero,a1,cs(cn(one),y),ca(cn(zeta),z)]
 cross=[(0,2),(0,3),(1,2),(1,3)]
 I=[[t,cs(ca(D[a],D[b]),t)] for a,b in cross for t in [[cn(one),cn(zeta)][b-2]]]
 S=[set(),set()]
 for g in range(2):
  seeds=[cs(D[2*g+1],D[2*g])]
  for (a,b),row in zip(cross,I):seeds.extend(cs(x,D[a if g==0 else b]) for x in row)
  for v in seeds:S[g].update(cm(v,u) for u in U)
 V=sorted({ca(d,s) for h,d in enumerate(D) for s in S[h//2]})
 E=[(i,j) for i,j in combinations(range(len(V)),2) if norm(V[i],V[j])==O]
 ci=[V.index(d) for d in D]
 owners=[{h for h,d in enumerate(D) if norm(v,d)==O} for v in V]
 return D,S,V,E,ci,owners

def boundary(D,V,ci,owners):
 rows=[];summary={'candidate_circle_pairs':0,'empty_circle_pairs':0,'two_root_circle_pairs':0,'internal_root_incidences':0}
 for i,x in enumerate(V):
  if i in ci:continue
  groups={h//2 for h in owners[i]}
  for h,b in enumerate(D):
   if h//2 in groups:continue
   summary['candidate_circle_pairs']+=1
   v=cs(x,b);q=length(v);check(sign(q)>0,'nonzero displacement')
   sq=sign(sub(q,scalar(4)));check(sq!=0,'this certificate excludes boundary tangencies')
   if sq>0:summary['empty_circle_pairs']+=1;continue
   summary['two_root_circle_pairs']+=1
   inside={sign(det(v,cs(p,b))) for p in V if norm(p,b)==norm(p,x)==O}
   check(inside<={-1,1},'non-tangent internal root signs')
   summary['internal_root_incidences']+=len(inside)
   for s in [-1,1]:
    if s not in inside:rows.append((i,h,s,v))
 return rows,summary

def build():
 D,S,V,E,ci,owners=geometry();col=list(map(int,COLOUR))
 check(len(V)==74 and len(E)==198 and len(col)==len(V),'fixed kernel')
 check([col[i] for i in ci]==[2,3,0,1],'centre pins')
 check(all(col[i]!=col[j] for i,j in E),'kernel colour inequalities')
 rows,summary=boundary(D,V,ci,owners);reps=[[],[]];labels=[]
 for i,h,s,v in rows:
  g=h//2;matches=[]
  for j,(w,t) in enumerate(reps[g]):
   matches.extend((j,k) for k in range(6) if root_equal(v,s,rotated(w,k),t))
  check(len(matches)<=1,'one label per nonzero direction')
  if matches:j,k=matches[0]
  else:j=len(reps[g]);k=0;reps[g].append((v,s))
  labels.append((g,j,k%2))
 bits=[[None]*len(group) for group in reps]
 for (i,h,s,v),(g,j,k) in zip(rows,labels):
  if col[i]//2==g:
   want=1^(col[i]%2)^(h%2)^k
   check(bits[g][j] in (None,want),'incompatible boundary phase pins')
   bits[g][j]=want
 free=sum(x is None for row in bits for x in row)
 bits=[[0 if x is None else x for x in row] for row in bits]
 certrows=[[i,h,s,bits[g][j]^k] for (i,h,s,v),(g,j,k) in zip(rows,labels)]
 check(all(col[i]!=2*(h//2)+(bit^(h%2)) for i,h,s,bit in certrows),'all external edge inequalities')
 outside_lists=[i for i,c in enumerate(col) if i not in ci and (owners[i]<={0,1} and c>=2 or owners[i]<={2,3} and c<2)]
 data={'schema':1,'field':'eta^4=12, eta>0','kernel_colour':COLOUR,'boundary_direction_bits':certrows,'point_sha256':digest(list(map(encode,V))),'edge_sha256':digest(E),'full_support_four_colourable':True,'target_found':False}
 summary.update({'vertices':len(V),'edges':len(E),'direction_sizes':list(map(len,S)),'boundary_root_incidences':len(rows),'residual_orbits':list(map(len,reps)),'free_residual_orbits':free,'kernel_colour_outside_old_lists':len(outside_lists),'centre_indices':ci,'kernel_colour_outside_old_list_indices':outside_lists})
 return data,summary

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args()
 out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();data,report=build();blob=raw(data)
 if not args.discover:check(blob==(Path(__file__).parent/'certificate.json').read_bytes(),'published certificate mismatch')
 (out/'certificate.json').write_bytes(blob)
 report.update({'status':'PASS','certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-start})
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
