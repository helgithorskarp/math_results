"""Full complex degree-nine critical7+1: exact author proof evidence.

Fresh opposite-order signs and independent substitution identities are
checked before replaying the credited complete positive-sector/polar
source2831f4c23f848429d95b23310e57fb109705409d. Python3.10+ standard library.
No assert-based guards, numerical signs, external corpus or source import.
The ordinary geometric/theorem deductions are in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import importlib.util,json,copy
ROOT=Path(__file__).resolve().parent
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,ROOT/file)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
OLD=module('credited71_positive','positive_verify.py')
N=module('fresh71_negative','negative.py')
A=OLD.A;B=OLD.B;ARC=OLD.ARC
require=OLD.require;digest=OLD.digest;tensor_hash=OLD.tensor_hash
BASELINE_DIGEST='40ef9f2414ffbcffdcc027f2c9a72b5c38414a43268138444c931710f80585e2'
CELLS=[
 ((F(0),F(1,2)),(F(1,2),F(1)),'disk'),
 ((F(1,2),F(1)),(F(1,2),F(3,4)),'disk'),
 ((F(1,2),F(1)),(F(3,4),F(1)),'mean')]
DEGREES={'H':(16,32,7,0),'disk':(32,36,14,0),'mean':(32,64,14,0)}
CLEAR={'H':16,'disk':4,'mean':32}

def coverage():
 require(CELLS==[
  ((F(0),F(1,2)),(F(1,2),F(1)),'disk'),
  ((F(1,2),F(1)),(F(1,2),F(3,4)),'disk'),
  ((F(1,2),F(1)),(F(3,4),F(1)),'mean')],'Wrong radial cover')
 require(sum((yh-yl)*(rh-rl) for (yl,yh),(rl,rh),choice in CELLS)==F(1,2),
  'Wrong full radial volume')
 for i,((yl,yh),(rl,rh),choice) in enumerate(CELLS):
  require(0<=yl<yh<=1 and F(1,2)<=rl<rh<=1 and choice in ['mean','disk'],
   'Radial cell outside domain')
  for (al,ah),(bl,bh),other in CELLS[:i]:
   require(not(max(yl,al)<min(yh,ah) and max(rl,bl)<min(rh,bh)),
    'Radial cell interiors overlap')

def cell_tensor(whole,cell):
 vals,d,deg=whole
 left,right=B.split(vals,d,deg,0)
 if cell==0:return *left,deg
 low,high=B.split(*right,deg,1)
 return *(low if cell==1 else high),deg

def certify(mapped,progress=None):
 coverage();whole={}
 for name,(p,clear) in mapped.items():
  q=B.affine_cell_integer(p,1,F(1,2),F(1))
  vals,d,deg=B.bernstein(q)
  require(deg==DEGREES[name] and clear==CLEAR[name],'Wrong map degree/clearing power')
  require(B.invert(vals,d,deg)==q,'Complete global radial tensor inverse fails')
  whole[name]=(vals,d,deg)
 records=[];fraction_references=0
 for cell,((yl,yh),(rl,rh),choice) in enumerate(CELLS):
  for name in ['H',choice]:
   vals,d,deg=cell_tensor(whole[name],cell)
   p,clear=mapped[name]
   direct=B.affine_cell_integer(B.affine_cell_integer(p,1,rl,rh),0,yl,yh)
   if (cell,name) in [(0,'disk'),(2,'H')]:
    slow=B.affine_cell(B.affine_cell(p,1,rl,rh),0,yl,yh)
    require(slow==direct,'Complete Fraction/integer affine reference fails')
    fraction_references+=1
   require(B.invert(vals,d,deg)==direct,'Complete radial cell inverse fails')
   alternative,dd,ddeg=B.bernstein(direct,deg)
   require(ddeg==deg and len(alternative)==len(vals)==prod(v+1 for v in deg),
    'Incomplete radial tensor entries')
   require(all(v*dd==w*d for v,w in zip(vals,alternative)),
    'Every-entry radial affine/de Casteljau comparison fails')
   require(min(vals)>=0,'Negative radial coefficient')
   shape=[v+1 for v in deg];stride=[prod(shape[j+1:]) for j in range(4)]
   zeros={tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(vals) if not v}
   if name=='H':
    expected=set() if cell<2 else {(16,32,k,0) for k in range(8)}
   elif name=='disk':
    expected={(i,0,k,0) for i in range(33) for k in range(15)}
   else:expected={(32,j,k,0) for j in [63,64] for k in range(15)}
   require(zeros==expected,'Wrong exact equality support '+name+' cell'+str(cell)+
    '; extras '+str(sorted(zeros-expected)[:40])+' missing '+str(sorted(expected-zeros)[:40]))
   records.append({'cell':cell,'target':name,'y':[str(yl),str(yh)],'r':[str(rl),str(rh)],
    'phase':['0','1'],'degrees':list(deg),'clear_r_power':clear,'coefficients':len(vals),
    'minimum':str(F(min(vals),d)),'minimum_positive':str(F(min(v for v in vals if v>0),d)),
    'zeros':len(zeros),'zero_indices_sha256':digest(sorted(zeros)),
    'sha256':tensor_hash(vals,d)})
  if progress:progress('radial cell'+str(cell)+' complete signs, inverse, affine and equality support pass')
 require(fraction_references==2,'Missing complete Fraction affine references')
 require(sum(row['coefficients'] for row in records)==82269,'Incomplete opposite-order sign inventory')
 return records

def gaussian_controls(data,mapped):
 gadd=OLD.gadd;gscale=OLD.gscale;gmul=OLD.gmul;gnorm=OLD.gnorm;gpower=OLD.gpower
 factors=list(map(OLD.exact_evaluator,data['factors']))
 polynomials={name:OLD.exact_evaluator(p) for name,(p,clear) in mapped.items()}
 rows=[];map_rows=[];count=0
 for r in [F(1,2),F(5,8),F(3,4),F(7,8),F(1)]:
  s=8-7*r;lower=1/r-1
  for b in sorted(set([lower,(lower+1)/2,F(1)])):
   if not b:continue
   disk=(1-(1-b*b)*r*r)/(2*b*r)
   mean=1-F(8,7)*(1-b)/r
   for chi,y0 in [(F(1),F(0)),(F(99,101),F(20,101)),
    (F(3,5),F(4,5)),(F(5,13),F(12,13))]:
    if chi<max(disk,mean):continue
    require(chi*chi+y0*y0==1,'Bad heavy Gaussian phase')
    for sign in [-1,1]:
     y=sign*y0;u=(chi,y);values=[b,r,chi,F(0)]
     AA=(factors[0](values),y*factors[1](values))
     BB=(factors[2](values),y*factors[3](values))
     T=gadd((F(1),F(0)),gscale(u,-b*r))
     powers=[gpower(T,j) for j in range(8)]
     directA=gscale(tuple(sum(p[k] for p in powers) for k in range(2)),F(9,8))
     directB=tuple(sum(F(b*(j+1),8)*p[k] for j,p in enumerate(powers)) for k in range(2))
     require(AA==directA and BB==directB,'Gaussian endpoint/arc factors differ')
     PA=gnorm(AA);PB=gnorm(BB);R=r**14*s*s
     L=PA+s*s*PB-R;FF=L*L-4*s*s*PA*PB
     require(L>=F(9,32)*R and FF>=0,'Exact free-phase first/squared sign control fails')
     require((FF==0)==(b==chi==1 and r in [F(1,2),F(1)]),'Exact free-phase corner control fails')
     radial=(b*r-1+r)/(2*r-1) if r>F(1,2) else F(0)
     zm=F(7,8)*r*(1-chi)/(1-b) if b<1 else F(0)
     zd=(chi-disk)/(1-disk) if disk<1 else F(0)
     require(0<=radial<=1 and 0<=zm<=1 and 0<=zd<=1,'Original-to-box control outside unit range')
     for name,z in [('H',zm),('mean',zm),('disk',zd)]:
      actual=polynomials[name]([radial,r,z,F(0)])
      raw=L-F(9,32)*R if name=='H' else FF
      require(actual==r**CLEAR[name]*raw,'Gaussian cleared phase/radial map mismatch')
      map_rows.append([name,*map(str,[radial,r,z,actual])])
     for v in [(F(1),F(0)),(F(-1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5))]:
      ii=gadd(AA,gscale(gmul(v,BB),-s))
      raw=OLD.direct_integral(gscale(u,r),gscale(v,s),slope=-b)
      require(ii==raw,'Gaussian full original integral differs')
      ratio=gnorm(ii)/R
      require(ratio>=1,'Gaussian opposite-order origin minimum fails')
      equality=(b==1 and r in [F(1,2),F(1)] and u==v==(F(1),F(0)))
      require((ratio==1)==equality,'Gaussian opposite-order equality fails')
      rows.append([*map(str,[b,r,chi,y,*v,*ii,ratio])]);count+=1
 require(count>=100 and len(map_rows)>=75,'Insufficient exact Gaussian/map controls')
 return {'count':count,'sha256':digest(rows),'map_count':len(map_rows),'map_sha256':digest(map_rows)}

def build_negative(progress=None):
 data=N.data(A,ARC)
 require(data['factors']==N.endpoint_factors(A),'Complete endpoint/binomial factor constructions differ')
 require(data['factors']==ARC.alternate(A),'Complete endpoint/linear-product factor constructions differ')
 mapped={}
 for name in ['H','mean','disk']:
  mapped[name]=N.mapped(A,data['targets'][name],data['numerators'][name],name=='disk',require)
  if progress:progress('complete phase and radial independent Horner identities pass for '+name)
 records=certify(mapped,progress)
 controls=gaussian_controls(data,mapped)
 return {'agent':'six-sendov-1','role':'researcher','proof_status':'ordinary author opposite-order proof with exact finite evidence; independent review pending',
  'abstract_domain':'0<b<=1,1/(1+b)<=r<=1,s=8-7r,chi>=max(disk heavy floor,necessary mean floor); any light unit phase',
  'first_sign_constant':'9/32','new_sign_coefficients':82269,'complete_Horner_identities':6,
  'kernel_sha256':digest([A.canonical(data[k]) for k in ['R','L']]+
    [A.canonical(data['targets'][k]) for k in ['H','mean']]),
  'mapped_sha256':{name:digest(A.canonical(p)) for name,(p,clear) in mapped.items()},
  'cells':records,'Gaussian_controls':controls,
  'equality':'b=1,r=1/2 or1,heavy=light unit phase1','light_arc_or_disk_not_needed':True}

def build(progress=None):
 negative=build_negative(progress)
 baseline=OLD.build(progress)
 require(digest(baseline)==BASELINE_DIGEST,'Credited complete positive/polar baseline changed')
 require(baseline['certified_coefficients']==449764,'Wrong credited baseline inventory')
 return {'agent':'six-sendov-1','role':'researcher',
  'proof_status':'complete ordinary author full complex critical7+1 proof with exact finite evidence; unformalized; independent review pending',
  'negative':negative,'positive_baseline_source':'2831f4c23f848429d95b23310e57fb109705409d',
  'positive_baseline_digest':BASELINE_DIGEST,'positive_baseline':baseline,
  'certified_coefficients':negative['new_sign_coefficients']+baseline['certified_coefficients'],
  'full_seven_one_case_claimed':True,'unrestricted_degree_nine_claimed':False}

def accept(actual,expected):require(actual==expected,'Complete compact manifest mismatch')
def rejection_controls(actual):
 rejected=0
 for change in range(12):
  bad=copy.deepcopy(actual)
  if change==0:bad['negative']['new_sign_coefficients']-=1
  elif change==1:bad['negative']['first_sign_constant']='0'
  elif change==2:bad['negative']['complete_Horner_identities']-=1
  elif change==3:bad['negative']['cells'].pop()
  elif change==4:bad['negative']['cells'][0]['minimum']='-1'
  elif change==5:bad['negative']['cells'][1]['zeros']+=1
  elif change==6:bad['negative']['mapped_sha256']['disk']='0'*64
  elif change==7:bad['negative']['Gaussian_controls']['sha256']='0'*64
  elif change==8:bad['positive_baseline_digest']='0'*64
  elif change==9:bad['positive_baseline']['envelope_cells'].pop()
  elif change==10:bad['negative']['equality']='binomial only'
  else:bad['unrestricted_degree_nine_claimed']=True
  try:accept(actual,bad)
  except ArithmeticError:rejected+=1
  else:raise ArithmeticError('Malformed manifest accepted')
 return rejected

def main():
 actual=build();expected=json.loads((ROOT/'expected.json').read_text());accept(actual,expected)
 rejected=rejection_controls(actual)
 print(json.dumps({'result':'PASS','new_opposite_order_sign_coefficients':82269,
  'credited_positive_and_polar_coefficients':449764,'certified_coefficients':actual['certified_coefficients'],
  'radial_boxes':3,'complete_Horner_identities':6,
  'all_global_cell_inverses_and_independent_affine_entries_checked':True,
  'negative_kernel_sha256':actual['negative']['kernel_sha256'],
  'Gaussian_controls':actual['negative']['Gaussian_controls']['count'],
  'Gaussian_map_controls':actual['negative']['Gaussian_controls']['map_count'],
  'full_seven_one_case_claimed':True,'unrestricted_degree_nine_claimed':False,
  'rejected_corruptions':rejected},sort_keys=True))
if __name__=='__main__':main()
