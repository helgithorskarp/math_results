"""Independent definition-level controls, no target input or code."""
import itertools,json,hashlib
from fractions import Fraction as Q
from aliases import rotation_count,test,cube
from algebra import determinant,value,bernstein,run as algebra_run

def run():
 counts={};digest=hashlib.sha256()
 for n in range(2,6):
  total=0
  for p in itertools.product(range(-1,n),repeat=n):
   arcs=[(i,j) for i,j in enumerate(p) if j!=-1]
   if any(i==j for i,j in arcs):continue
   brute=0
   if len({j for i,j in arcs})==len(arcs):
    for order in itertools.permutations(range(1,n)):
     cycle=(0,)+order;edges=set(zip(cycle,cycle[1:]+cycle[:1]))
     brute+=all(a in edges for a in arcs)
   actual=rotation_count(set(range(n)),arcs)
   if actual!=brute:raise ValueError(('DP rotation',n,p,actual,brute))
   digest.update(json.dumps([n,p,actual],separators=(',',':')).encode()+b'\n');total+=1
  counts[n]=total
 if rotation_count({0,1,2},[(0,1),(0,1)])!=0:raise ValueError('duplicate sector accepted')
 if rotation_count({0,1,2,3},[(0,1),(1,0)])!=0:raise ValueError('proper closed star accepted')
 if rotation_count({0,1,2,3},[(0,1),(1,2)])!=1:raise ValueError('path completion')
 points=list(itertools.product(range(-1,2),repeat=2));normal=0;zero=0;damaged_nonzero=0;gram_digest=hashlib.sha256()
 def dot(a,b):return sum(x*y for x,y in zip(a,b))
 for a,b,u,v in itertools.product(points,repeat=4):
  P=dot(a,a);QQ=dot(b,b);U=dot(a,b);R=dot(u,u);S=dot(v,v);V=dot(u,v);W=dot(b,u);Z=dot(a,v)
  # General projected vectors need different lengths R,S. f uses u;g uses v.
  # For our theorem u and v both have squared length R, so calibrate this stratum.
  if R!=S:continue
  def resultant(w):
   f=[(QQ,),(-2*U*w,),(P*w*w+R*U*U-P*QQ*R,)]
   g=[(R,),(-2*V*Z,),(R*Z*Z+P*V*V-P*R*R,)]
   return determinant([f+[(0,)],[(0,)]+f,g+[(0,)],[(0,)]+g])[0]
  res=resultant(W)
  if res!=0:raise ValueError('true planar Gram rejected')
  normal+=1;zero+=(P*QQ-U*U==0 or R*R-V*V==0)
  alter=resultant(W+1);damaged_nonzero+=(alter!=0)
  gram_digest.update(json.dumps([a,b,u,v,alter],separators=(',',':')).encode()+b'\n')
 alg=algebra_run();identity_controls=0
 for record in alg['internal']:
  p=record['gap'];coeff=record['wide'];n=len(p)-1
  for j in range(n+1):
   t=Q(j,n) if n else Q(0);lo=Q(2,3);hi=Q(3,4)
   from math import comb
   rhs=sum(Q(coeff[k])*comb(n,k)*t**k*(1-t)**(n-k) for k in range(n+1))
   if rhs!=value(p,lo+(hi-lo)*t):raise ValueError('Bernstein identity')
   identity_controls+=1
 return dict(rotation_cases=counts,rotation_total=sum(counts.values()),rotation_sha256=digest.hexdigest(),duplicate_corner_and_proper_cycle_rejected=True,planar_Gram_cases=normal,degenerate_Gram_cases=zero,altered_Gram_detected=damaged_nonzero,Gram_sha256=gram_digest.hexdigest(),independent_Bernstein_identity_points=identity_controls)
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
