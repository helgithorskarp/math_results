"""Exact independent-source-rectangle forms; no search output is a premise."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent
PINS=json.loads((HERE/'DEPENDENCIES.json').read_text())
for name,digest in PINS['sha256'].items():
 if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:raise ValueError('before-import named source fingerprint: '+name)
spec=importlib.util.spec_from_file_location('j74_gated_original_forms',HERE.parent/'phase_crossing_box/forms.py')
old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
c,a,Q=old.c,old.a,old.Q
M=Q(F(15,4))
# Proper Sy homogeneous lift (1,-1,0,0) acting on (1,MU,MV,w).
B=((Q(1),M,Q(),Q()),(Q(-1),M,Q(),Q()),(Q(),Q(),M,Q(1)),(Q(),Q(),-M,Q(1)))
def congruence(A):return c.matmul(c.matmul(tuple(zip(*B)),A),B)
def outer(x,y):return tuple(tuple(u*v for v in y) for u in x)
def combine(*xs):return tuple(tuple(sum((x[i][j] for x in xs),Q()) for j in range(4)) for i in range(4))
def gauge_components(raw,which):
 X,Y,_=raw;E=tuple(tuple(Q(int(i==0 and j==0)) for j in range(4)) for i in range(4))
 def subtract(A,t):return tuple(tuple(A[i][j]-t*E[i][j] for j in range(4)) for i in range(4))
 if which==0:v=((-X,Q(),M*Y,Q(-1)),(Q(-1),Q(),Q(),Q()),(Q(),Q(),M,Q()))
 elif which==1:v=((Q(-1),-M*Y,Q(),X),(Q(),Q(),Q(),Q(1)),(Q(),-M,Q(),Q()))
 else:raise ValueError('actual closed scalar gauge index')
 z,x,y=v
 return [subtract(outer(z,z),X*X+Y*Y+1),subtract(combine(outer(z,x),outer(x,z)),2*X),subtract(combine(outer(z,y),outer(y,z)),2*Y),subtract(outer(x,x),1),combine(outer(x,y),outer(y,x)),subtract(outer(y,y),1)]
class Forms:
 def __init__(self):
  self.original=old.Forms();self.raw=self.original.raw;self.eta=self.original.eta;self.cache={}
  s=Q(0,1);aa=(s-1)/4;bb=(s+1)/4;half=Q(F(1,2))
  H=((Q(-1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
  A=((bb,aa,half),(-aa,-half,bb),(half,-bb,-aa));BB=((-aa,-half,-bb),(half,-bb,aa),(-bb,-aa,half))
  poses=[c.matrix(x['proper_matrix_rows']) for x in self.original.data['poses']]
  self.original_hole_indices=[2*poses.index(H)+1,2*poses.index(A),2*poses.index(BB)+1]
  self.holes={i:congruence(self.original.point_holes[i]) for i in self.original_hole_indices}
  self.gauges=[old.j.receiver_controls(gauge_components(self.raw,i),self.eta) for i in range(2)]
  for i,matrices in enumerate(self.gauges):
   unused=1 if i==0 else 2
   c.require(all(A[unused][j]==0 and A[j][unused]==0 for A in matrices for j in range(4)),'actual gauge unused source coordinate')
 def physical_controls(self,ci,ks):
  key=(ci,*ks)
  if key not in self.cache:self.cache[key]=[congruence(A) for A in self.original.receiver_control_forms(ci,ks)]
  return self.cache[key]
 def moments(self,depth,code):
  lo,hi=c.box(depth,code);return old.j.quaternion_moments(0,lo,hi)
 def coefficients(self,leaf):
  depth,code,kind=leaf[:3];W=self.moments(depth,code)
  if kind=='H':
   c.require(len(leaf)==4 and leaf[3] in self.holes,'actual one of three canonical physical equality holes')
   return old.j.moment_coefficients(self.holes[leaf[3]],W)
  if kind=='G':
   c.require(len(leaf)==4 and type(leaf[3]) is int and leaf[3] in (0,1),'one of two exact closed gauge rejects')
   unused=0 if leaf[3]==0 else 1
   chosen=[row for ijk,row in zip(product(range(3),repeat=3),W) if ijk[unused]==0]
   return [v for A in self.gauges[leaf[3]] for v in old.j.moment_coefficients(A,chosen)]
  c.require(kind=='C' and len(leaf)>=5,'actual positive common-support source cut')
  ci=leaf[3];ks=leaf[4:]
  c.require(type(ci) is int and ci in range(108),'actual common-support stress index')
  return [v for A in self.physical_controls(ci,ks) for v in old.j.moment_coefficients(A,W)]
