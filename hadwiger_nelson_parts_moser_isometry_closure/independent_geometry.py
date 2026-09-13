"""Re-enumerate with Q(t,r,s), t²=-3,r²=-11,s²=5, as complex coordinates.

Imports neither geometry.py nor verify.py. Inversion uses rational linear
systems, replacing the producer's product of real-field conjugates. Compare
complete coordinate sets, placements, incidences and base edges entry by entry.
"""
import argparse,hashlib,json,math
from collections import defaultdict,Counter
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
HERE=Path(__file__).resolve().parent
FACTORS=(1,-3,-11,33,5,-15,-55,165)
ZERO=(0,)*8;ONE=(1,)+(0,)*7

def require(ok,msg):
 if not ok:raise ValueError(msg)
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))
def times(x,y):
 z=[0]*8
 for i,a in enumerate(x):
  for j,b in enumerate(y):
   if a and b:z[i^j]+=a*b*FACTORS[i&j]
 return tuple(z)
def scalar(x,a):return tuple(c*a for c in x)
def conjugate(x):return tuple((-c if (i&3).bit_count()%2 else c)for i,c in enumerate(x))
def squared(x):return times(x,conjugate(x))
def inverse(x):
 cols=[times(x,tuple(int(i==j)for i in range(8)))for j in range(8)]
 A=[[F(cols[j][i])for j in range(8)]+[F(i==0)]for i in range(8)]
 for j in range(8):
  pivot=next(i for i in range(j,8)if A[i][j]);A[j],A[pivot]=A[pivot],A[j]
  q=A[j][j];A[j]=[c/q for c in A[j]]
  for i in range(8):
   if i!=j:
    q=A[i][j];A[i]=[c-q*d for c,d in zip(A[i],A[j])]
 z=tuple(A[i][8]for i in range(8));require(times(x,z)==ONE,'inverse');return z

def readpoint(p):
 require(len(p)==16 and all(p[i]==0 for i in [1,3,4,6,8,10,13,15]),'complex coordinate subspace')
 return (p[0],p[9],p[12],-p[5],p[2],p[11],p[14],-p[7])
def writepoint(p):return (p[0],0,p[4],0,0,-p[3],0,-p[7],0,p[1],0,p[5],p[2],0,p[6],0)

def audit(path):
 data=json.loads(path.read_text());g=data['geometry'];D=g['scale'];require(D==6912,'coordinate scale')
 raw=(HERE.parent/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_bytes()
 require(hashlib.sha256(raw).hexdigest()=='f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50','coordinate hash')
 P=[readpoint(tuple(map(int,l.split())))for l in raw.decode().splitlines()if not l.startswith('#')]
 require([list(writepoint(p))for p in P]==g['base_points'],'original point entries')
 omega=(F(1,2),F(1,2),0,0,0,0,0,0);rho=(F(5,6),0,F(1,6),0,0,0,0,0)
 M=[ZERO,ONE,omega,plus(ONE,omega),rho,times(rho,omega),times(rho,plus(ONE,omega))]
 templates=defaultdict(set)
 for i,j in permutations(range(7),2):
  inv=inverse(minus(M[j],M[i]));length=squared(minus(M[j],M[i]))
  for flip in [False,True]:
   sh=[times(minus(m,M[i]),inv)for m in M]
   if flip:sh=list(map(conjugate,sh))
   templates[length].add(tuple(sorted(sh)))
 L=math.lcm(*(F(c).denominator for shapes in templates.values()for sh in shapes for p in sh for c in p));require(96*L==D,'normalization scale')
 T={scalar(k,96**2):[tuple(tuple(int(c*L)for c in p)for p in sh)for sh in ss]for k,ss in templates.items()}
 require(all(all(F(c*96**2).denominator==1 for c in k)for k in templates),'exact distance scaling')
 Ps=set(scalar(p,L)for p in P);shapes=set();edges=[];route_count=0;matched=Counter()
 for i,j in combinations(range(509),2):
  d=minus(P[j],P[i]);n=squared(d)
  if n==scalar(ONE,96**2):edges.append([i,j])
  if n in T:
   matched[n]+=1
   for sh in T[n]:
    shapes.add(tuple(sorted(plus(scalar(P[i],L),times(d,p))for p in sh)));route_count+=1
 require(edges==g['base_edges'],'complete base-edge entries')
 fresh={p for sh in shapes for p in sh if p not in Ps};published={readpoint(p)for p in g['points']}
 require(fresh==published,'complete external-point set')
 actual={tuple(sorted(writepoint(p)for p in sh))for sh in shapes if any(p not in Ps for p in sh)}
 declared=set()
 for a in g['assemblies']:
  out=[tuple(g['points'][q])for q in a['fresh']]+[tuple(scalar(g['base_points'][v],L))for v in a['overlap']]
  declared.add(tuple(sorted(out)))
 require(actual==declared,'complete placement entries')
 prime=1000081;root_i=next(pow(a,(prime-1)//4,prime)for a in range(2,100)if pow(pow(a,(prime-1)//4,prime),2,prime)==prime-1)
 roots=(964569*root_i%prime,970601*root_i%prime,816716)
 require(all(roots[i]**2%prime==(-3,-11,5)[i]%prime for i in range(3)),'residue map')
 vals=[math.prod(roots[j]for j in range(3)if i>>j&1)%prime for i in range(8)]
 def ev(p):return sum(a*b for a,b in zip(p,vals))%prime
 pp=[(ev(p)*pow(96,-1,prime)%prime,ev(conjugate(p))*pow(96,-1,prime)%prime)for p in P]
 incidence=0;mod_survivors=0
 for qi,row in enumerate(g['points']):
  p=readpoint(row);z=ev(p)*pow(D,-1,prime)%prime;cz=ev(conjugate(p))*pow(D,-1,prime)%prime;ns=[]
  for j,(w,cw)in enumerate(pp):
   if ((z-w)*(cz-cw)-1)%prime==0:
    mod_survivors+=1
    if squared(minus(p,scalar(P[j],L)))==scalar(ONE,D**2):ns.append(j)
  require(ns==g['neighbours'][qi],'complete unit-neighbour entries');incidence+=len(ns)
 # Check every internal edge manifest by the independent complex norm as well.
 inside_checks=0
 for a in g['assemblies']:
  q=[readpoint(g['points'][i])for i in a['fresh']]
  es=[[i,j]for i,j in combinations(range(len(q)),2)if squared(minus(q[i],q[j]))==scalar(ONE,D**2)]
  require(es==a['edges'],'fresh internal edges');inside_checks+=len(es)
 return {'placements':len(shapes),'routes':route_count,'overlap_histogram':dict(Counter(sum(p in Ps for p in sh)for sh in shapes)),'external_points':len(fresh),'external_original_unit_pairs':incidence,'modular_survivors':mod_survivors,'internal_edge_manifest_checks':inside_checks,'entrywise_geometry_agreement':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('frontier',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=audit(a.frontier);s=json.dumps(r,indent=2,sort_keys=True)+'\n';print(s)
 if a.output:a.output.write_text(s)
