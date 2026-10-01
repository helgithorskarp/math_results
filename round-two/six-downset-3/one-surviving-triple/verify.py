"""Rebuild every polynomial coefficient and all literal boundary checks."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import argparse,json,time,resource,tempfile
import bootstrap
from systems import R,recover,sector,DEGREES,serial,require,ff_eliminate
from polynomials import forms,integer_minors,idiv,evaluate
from matrices import construct,verify_full,solve_potentials
from bridge import check
from exact import digest,schur_psd,polynomial_psd

HERE=Path(__file__).resolve().parent

def coefficient_polynomial(values):
 require(isinstance(values,list) and values and all(isinstance(x,str) for x in values),'malformed coefficient list')
 v=[F(x) for x in values]
 require(v[0]>0 and all(x>=0 for x in v),'nonpositive coefficient certificate')

def polynomial_summary(x):
 require(x.d==(F(1),),'non-polynomial normal minor')
 x.coefficients_positive();v=x.record()['numerator']
 return {'degree':len(v)-1,'constant':v[0],'coefficient_positive':True,'polynomial_sha256':digest(v)}

def check_evidence(data):
 require(data.get('q')=='5+u' and data.get('boundary_q')==4,'wrong symbolic domain')
 require([len(data[k]) for k in ['p','r','d']]==[7,9,9],'wrong potential coverage')
 for k in ['p','r','d']:
  for rec in data[k]:coefficient_polynomial(rec['denominator'])
 for key,size in [('cross_normal_minors',15),('internal_normal_minors',9)]:
  require(len(data[key])==size,'missing normal minor')
  for rec in data[key]:require(rec['coefficient_positive'] is True and F(rec['constant'])>0,'wrong normal sign')
 blocks=data.get('sectors',[]);require(len(blocks)==5,'missing complete sector');total=0
 for b,degree,size in zip(blocks,DEGREES,[8,3,4,1,1]):
  require(b['degree']==list(degree),'wrong sector order')
  for name in ['lower','upper']:
   coefficient_polynomial(b[name+'_denominator'])
   signs=b[name+'_signs'];require(int(signs['positive_coefficient_scale'])>0,'nonpositive integer scale')
   require(len(signs['minors'])==size,'missing floor determinant')
   for order,rec in enumerate(signs['minors'],1):
    require(rec['order']==order and rec['coefficient_positive'] is True and rec['negative_coefficients']==0 and int(rec['constant'])>0,'misstated generated sign');total+=1
 require(total==34,'incomplete floor coverage')

def symbolic_certificate():
 q=R((5,1));p,r,d,cross,internal=recover(q)
 data={'agent':'six-downset-3','role':'researcher','q':'5+u','boundary_q':4,'p':p,'r':r,'d':d,
  'cross_normal_minors':[polynomial_summary(x) for x in cross],
  'internal_normal_minors':[polynomial_summary(x) for x in internal],'sectors':[]}
 for degree in DEGREES:
  b=forms(q,p,r,d,degree)
  rec={k:b[k] for k in ['degree','S_types','Q_types']}
  for name in ['lower','upper']:
   rec[name+'_denominator']=[str(x) for x in b[name+'_denominator']]
   matrix=b[name]
   if degree==(0,0):matrix=[row[1:] for row in matrix[1:]]
   rec[name+'_signs']=integer_minors(matrix)
  data['sectors'].append(rec)
  print(json.dumps({'symbolic_sector':degree,'leading_signs':2*len(matrix)}),flush=True)
 data=serial(data);check_evidence(data)
 return data,p,r,d

def controls(signs,p,r,d):
 rejected=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,TypeError,ZeroDivisionError):rejected.append(label)
  else:raise ValueError('failed rejection control: '+label)
 reject('float_field',lambda:R(0.5))
 reject('zero_field_denominator',lambda:R(1,0))
 reject('zero_integer_divisor',lambda:idiv((1,),(0,)))
 reject('nonexact_integer_division',lambda:idiv((1,0,1),(1,1)))
 reject('nonintegral_integer_division',lambda:idiv((1,),(2,)))
 reject('zero_symbolic_pivot',lambda:ff_eliminate([[R(0)]]))
 reject('nonsquare_polynomial_matrix',lambda:integer_minors([[(F(1),),(F(0),)]]))
 reject('asymmetric_polynomial_matrix',lambda:integer_minors([[(F(1),),(F(1),)],[(F(0),),(F(1),)]]))
 reject('inexact_polynomial_matrix',lambda:integer_minors([[(1.0,)]]))
 reject('negative_generated_coefficient',lambda:integer_minors([[(F(1),F(-1))]]))
 pp,rr,dd=[[R(x.at(0)) for x in values] for values in [p,r,d]]
 reject('corrupt_cross_potential',lambda:sector(R(5),[pp[0]+1]+pp[1:],rr,dd,0,0))
 bad=deepcopy(signs);bad['sectors'][0]['lower_signs']['minors'][0]['constant']='-1'
 reject('negative_stored_summary',lambda:check_evidence(bad))
 bad=deepcopy(signs);bad['sectors'][0]['upper_denominator'][0]='-1'
 reject('negative_stored_denominator',lambda:check_evidence(bad))
 bad=deepcopy(signs);bad['sectors'].pop()
 reject('missing_sector',lambda:check_evidence(bad))
 for label,q in [('below_domain',3),('float_domain',4.0),('bool_domain',True)]:
  reject(label,lambda x=q:solve_potentials(x))
 for label,t in [('zero_repair',F(0)),('negative_repair',F(-1)),('above_interval',F(1,720)),('float_repair',1/1440)]:
  reject(label,lambda x=t:construct(4,x))
 for label,a in [('indefinite',[[1,2],[2,1]]),('zero_pivot_nonzero_row',[[0,1],[1,0]]),('nonsquare',[[1,0]]),('asymmetric',[[1,0],[1,1]]),('inexact',[[1.0]])]:
  reject(label,lambda x=a:schur_psd(x))
 X,L=construct(4,F(1,1440))
 for label,i in [('wrong_empty_loop',0),('wrong_nonempty_diagonal',1)]:
  bad=deepcopy(L);bad[i][i]+=1
  reject(label,lambda x=bad:verify_full(4,X,x))
 with tempfile.TemporaryDirectory(prefix='survivor-control-') as tmp:
  base=Path(tmp)
  for path in bootstrap.PINS:
   target=base/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((bootstrap.BASE/path).read_bytes())
  path=base/next(iter(bootstrap.PINS));path.write_bytes(path.read_bytes()+b'\n# damage control\n')
  reject('damaged_public_helper',lambda:bootstrap.setup(base))
 for rank,a in [(0,[[0]]),(1,[[1,0],[0,0]]),(2,[[2,-1],[-1,2]])]:
  require(schur_psd(a)==rank and polynomial_psd(a)[0]==rank,'positive matrix control')
 # Two implementations: Z[u] symmetric Bareiss versus Q[u] field helper.
 tiny=[[R((5,1)),R(1),R(0)],[R(1),R((4,1)),R(1)],[R(0),R(1),R((3,1))]]
 a=integer_minors([[x.n for x in row] for row in tiny]);b=ff_eliminate(tiny)
 require(a['positive_coefficient_scale']=='1','tiny control scale')
 for rec,x in zip(a['minors'],b):require(rec['polynomial_sha256']==digest(x.record()['numerator']),'independent Bareiss control')
 return rejected

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 start=time.monotonic();signs,p,r,d=symbolic_certificate();path=HERE/'EXPECTED.json'
 if args.write:path.write_text(json.dumps(signs,sort_keys=True,indent=2)+'\n')
 else:require(json.loads(path.read_text())==signs,'stored expected polynomial records differ')
 records=[]
 for q in [4,5,6]:
  rec=check(q,p,r,d);records.append(rec)
  print(json.dumps({'literal_q':q,'N':rec['N'],'rank_L':rec['rank_L'],'rank_upper':rec['rank_upper'],'action_columns':rec['literal_action_columns']}),flush=True)
 X,L=construct(4,F(1,2880));verify_full(4,X,L)
 rejected=controls(signs,p,r,d)
 result={'agent':'six-downset-3','role':'researcher','proof_status':'author-checked ordinary unformalized proof; independent review pending',
  'unbounded_floor_signs':34,'normal_minors':24,'literal_cases':records,'literal_action_columns':sum(x['literal_action_columns'] for x in records),
  'secondary_characteristic_forms':8,'mid_interval_q4':True,'rejection_controls':rejected,'positive_matrix_controls':3,'separate_Bareiss_control':True,
  'EXPECTED_sha256':digest(signs),'records_sha256':digest(records)}
 path=HERE/'RESULTS.json'
 if args.write:path.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 else:require(json.loads(path.read_text())==result,'stored finite results differ')
 print(json.dumps({'passed':True,'unbounded_signs':34,'normal_minors':24,'literal_action_columns':92,'rejections':len(rejected),
  'EXPECTED_sha256':result['EXPECTED_sha256'],'records_sha256':result['records_sha256'],
  'seconds':round(time.monotonic()-start,3),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)

if __name__=='__main__':main()
