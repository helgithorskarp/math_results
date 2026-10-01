"""Exact 23-contact classification and all-pair packing certificate checker."""
from fractions import Fraction as Q
from pathlib import Path
from functools import lru_cache
from math import isqrt
import argparse,hashlib,importlib.util,json,sys
import models

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LO,HI=Q(14,25),Q(593,1000)
F=(-1,-3,2,6,-1,13)
EDGES=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),
       (2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,11),
       (7,12),(8,13),(9,10),(9,11),(9,13),(10,12))
FACT_BOUNDS={
 'kappa':('-3/10','-1/5'),'mu':('-3/5','-11/20'),
 'common_w':('1/3','2/5'),'common_height2':('49/100','3/5'),
 'plane_gram':('9/10','1'),'normal_squared_norm':('2','3'),
 'rho':('9/50','23/100'),'detH':('3/10','1/2'),
 'reflection_determinant':('1','2'),'Fprime':('10','14'),
 '-1_-1_1_7_a':('-1/10','-1/50'),'-1_-1_1_7_b':('9/10','6/5'),
 '-1_-1_1_7_square':('-1/4','-1/5'),
 '1_1_10_11_a':('1/10','3/20'),'1_1_10_11_b':('1/2','2/3'),
 '1_-1_6_8_a':('-3/4','-2/5'),'1_-1_6_8_b':('4/3','8/5'),
 'packing_threshold_factor':('1/2','4/5')}

def require(ok,message):
 if not ok:raise ValueError(message)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(c):
 require(c['format']==1 and c['interval']==[[14,25],[593,1000]],'fixed closed domain')
 require(c['edges']==[list(e) for e in EDGES],'literal retained twenty-three-edge graph')
 require(c['bernstein_pieces']==8 and c['noncontact_pieces']==16,'complete fixed uniform partitions')
 require(c['sqrt_scale']==10**6,'fixed outward square-root scale')
 require(0<Q(c['noncontact_upper'])<=Q(1,2),'sufficient noncontact gap')
 a,z=map(Q,c['root_bracket'])
 require(LO<a<z<HI,'bracket inside the proved domain')
 require(value(F,a)<0<value(F,z),'incumbent root bracket')
def value(p,t):return sum(Q(a)*t**i for i,a in enumerate(p))
def load(prerequisite_root):
 item=json.loads((HERE/'INPUTS.json').read_text())['core']
 directory=Path(prerequisite_root)/item['directory']
 for name,want in item['files_sha256'].items():
  require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==want,'pinned core source '+name)
 spec=importlib.util.spec_from_file_location('verify',directory/'verify.py')
 base=importlib.util.module_from_spec(spec);sys.modules['verify']=base;spec.loader.exec_module(base)
 spec=importlib.util.spec_from_file_location('twenty_three_prerequisite',directory/'verify_contact_core.py')
 core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
 return base,core
def derive(prerequisite_root):
 base,core=load(prerequisite_root)
 funcs,gaps,geometry,H=models.derive(base,core)
 return funcs,base
def manifest(funcs):return {n:{'n':list(f.n),'d':list(f.d)} for n,f in sorted(funcs.items())}
def enclosures(base):
 @lru_cache(maxsize=None)
 def polynomial(p,left,right):
  coeff=base.bernstein(p,left,right) or (Q(0),)
  return min(coeff),max(coeff)
 def interval(f,left,right):
  nl,nh=polynomial(tuple(f['n']),left,right)
  dl,dh=polynomial(tuple(f['d']),left,right)
  require(not dl<=0<=dh,'every denominator has strict sign')
  choices=(nl/dl,nl/dh,nh/dl,nh/dh)
  return min(choices),max(choices)
 return interval
def whole(f,interval,pieces):
 bounds=[interval(f,LO+(HI-LO)*k/pieces,LO+(HI-LO)*(k+1)/pieces) for k in range(pieces)]
 return min(a for a,b in bounds),max(b for a,b in bounds)
def sqrt_enclosure(low,high,scale):
 require(0<low<=high,'positive continuous radical')
 a=Q(isqrt((low.numerator*scale*scale)//low.denominator),scale)
 z=Q(isqrt((high.numerator*scale*scale)//high.denominator)+1,scale)
 require(a*a<=low and z*z>=high,'outward rational square-root rounding')
 return a,z
def prove_bounds(c,interval):
 raw=c['functions']
 for name,(low,high) in FACT_BOUNDS.items():
  a,z=whole(raw[name],interval,c['bernstein_pieces'])
  require(Q(low)<=a<=z<=Q(high),'rational branch bound '+name)
 noncontacts=sorted(n for n in raw if n.startswith('noncontact_') and n.endswith('_a'))
 require(len(noncontacts)==54,'all fifty-four remaining noncontacts')
 worst=Q(-10);pair=None
 for name in noncontacts:
  for k in range(c['noncontact_pieces']):
   left=LO+(HI-LO)*k/c['noncontact_pieces'];right=LO+(HI-LO)*(k+1)/c['noncontact_pieces']
   a=interval(raw[name],left,right);d=interval(raw[name[:-1]+'b'],left,right)
   theta=sqrt_enclosure(*interval(raw['rho'],left,right),c['sqrt_scale'])
   upper=a[1]+max(q*z for q in d for z in theta)
   require(upper<Q(c['noncontact_upper']),'all-pair noncontact upper gap '+name)
   if upper>worst:worst,pair=upper,name
 return {'rational_branch_bounds':len(FACT_BOUNDS),'noncontact_pairs':54,
         'noncontact_closed_pieces':c['noncontact_pieces'],'sqrt_scale':c['sqrt_scale'],
         'noncontact_upper':c['noncontact_upper'],'worst_noncontact_pair':pair,
         'worst_noncontact_upper':str(worst)}
def verify(c,prerequisite_root=ROOT,derived=None):
 validate(c)
 funcs,base=derived if derived is not None else derive(prerequisite_root)
 require(c['functions']==manifest(funcs),'exact function table regenerated from every branch')
 return {'status':'VERIFIED','core_vertices':13,'retained_edges':23,'complete_orientation_branches':4,
         'rejected_branches':3,'surviving_branch':[1,-1],
         'functions':len(funcs),'canonical_certificate_sha256':digest(c),**prove_bounds(c,enclosures(base))}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
 parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
 args=parser.parse_args()
 print(json.dumps(verify(json.loads(args.certificate.read_text()),args.prerequisite_root),sort_keys=True))
