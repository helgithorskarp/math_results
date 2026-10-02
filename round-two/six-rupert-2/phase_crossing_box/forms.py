"""Exact actual common-support stress and quaternion coefficient forms.

Every selected stress is strictly positive across the whole closed box and
cancels all three original spatial translation components identically.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import importlib.util,json,sys
HERE=Path(__file__).resolve().parent
name='j74_cross_local'
if name in sys.modules:l=sys.modules[name]
else:
 spec=importlib.util.spec_from_file_location(name,HERE/'local.py')
 l=importlib.util.module_from_spec(spec);sys.modules[name]=l;spec.loader.exec_module(l)
j,c,a,Q,p=l.parent,l.c,l.a,l.Q,l.p
class Forms(j.Forms):
 def __init__(self):
  self.eta=Q(F(1,1000));self.data=json.loads((c.HERE/'certificate.json').read_text())
  u,cycle,oldN,self.R2=c.original_geometry();s=Q(0,1);tau=(-3994+1792*s)/899
  self.raw=a.add(a.scale(-1/u[2],u),(-tau,tau,Q()))
  self.edges=[(i,k) for n,(i,k) in enumerate(zip(cycle,cycle[1:]+cycle[:1])) if n not in (14,15)]
  self.cycle=[x[0] for x in self.edges];self.E=[a.sub(c.V[k],c.V[i]) for i,k in self.edges]
  self.M=[[a.cross(e,r) for e in self.E] for r in (self.raw,p.EX,p.EY)]
  self.h=[[a.dot(m,c.V[i]) for m,(i,k) in zip(ms,self.edges)] for ms in self.M]
  self.N=[a.scale(1/h,m) for m,h in zip(self.M[0],self.h[0])]
  corners=[a.add(self.raw,(x*self.eta,y*self.eta,Q())) for x,y in product((-1,1),repeat=2)]
  candidates=[]
  for i,k in combinations(range(15),2):
   if a.add(self.E[i],self.E[k])==c.ZERO:candidates.append(([i,k],[[Q(1),Q(1)],[Q(),Q()],[Q(),Q()]]))
  for i,k,l in combinations(range(15),3):
   vectors=[a.cross(self.E[k],self.E[l]),a.cross(self.E[l],self.E[i]),a.cross(self.E[i],self.E[k])]
   point=[a.dot(v,self.raw) for v in vectors]
   if all(x<0 for x in point):sign=-1
   elif all(x>0 for x in point):sign=1
   else:continue
   if not all(sign*a.dot(v,r)>0 for v in vectors for r in corners):continue
   candidates.append(([i,k,l],[[sign*a.dot(v,r) for v in vectors] for r in (self.raw,p.EX,p.EY)]))
  self.beta=[];self.circuits=[]
  terms=[[(0,0)],[(0,1),(1,0)],[(0,2),(2,0)],[(1,1)],[(1,2),(2,1)],[(2,2)]]
  for indices,coeff in candidates:
   total=sum((x*self.h[0][i] for x,i in zip(coeff[0],indices)),Q());c.require(total>0,'positive constant point stress normalization')
   beta=[[x/total for x in row] for row in coeff]
   c.require(all(beta[0][k]+dx*beta[1][k]+dy*beta[2][k]>0
                 for dx,dy in product((-self.eta,self.eta),repeat=2) for k in range(len(indices))), 'all raw positive stress corner weights')
   weights=[x*self.h[0][i] for x,i in zip(beta[0],indices)]
   c.require(sum(weights,Q())==1 and min(weights)>0,'exact point normalized positive stress')
   for ts in terms:
    force=tuple(sum((beta[bi][k]*self.M[mi][i][axis] for bi,mi in ts for k,i in enumerate(indices)),Q()) for axis in range(3))
    c.require(force==c.ZERO,'all actual spatial receiver-polynomial force identities')
   self.beta.append(beta);self.circuits.append((indices,weights))
  c.require(len(self.circuits)==108,'literal common-support stress inventory')
  Mn=tuple(tuple(c.IDENTITY[i][k]-2*self.raw[i]*self.raw[k]/a.dot(self.raw,self.raw) for k in range(3)) for i in range(3))
  Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
  self.hole_gate=Q(F(1,33));local_gate=Q(F(1,30))
  move=2*self.hole_gate+6*self.eta
  c.require(move*move<4*local_gate*local_gate/(1+local_gate*local_gate), 'point holes enter whole-box local1/30 collar')
  threshold=(3-self.hole_gate*self.hole_gate)/(1+self.hole_gate*self.hole_gate)
  self.point_holes=[]
  for item in self.data['poses']:
   g=c.matrix(item['proper_matrix_rows'])
   for ref in (g,c.matmul(c.matmul(Mn,g),Mx)):
    H=[[Q() for k in range(4)] for i in range(4)]
    for axis in range(3):
     L=c.rotation_form(c.IDENTITY[axis],ref[axis])
     for i in range(4):
      for k in range(4):H[i][k]+=L[i][k]
    for i in range(4):H[i][i]-=threshold
    self.point_holes.append(H)
  self.cache={}
