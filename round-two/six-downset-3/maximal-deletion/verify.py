"""Stdlib exact reconstruction of the 22 unbounded signs and original matrices."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import argparse,json,time,resource,tempfile
import bootstrap
from symbolic import R,recover,sector,positive_minors,DEGREES,serial,require,ff_eliminate
from literal import potentials,check,construct,verify_full
from poly import exact_divide
from exact import digest,schur_psd,polynomial_psd

HERE=Path(__file__).resolve().parent

def coefficient_polynomial(values):
 require(isinstance(values,list) and values and all(isinstance(x,str) for x in values),'malformed coefficient list')
 coefficients=[F(x) for x in values]
 require(coefficients[0]>0 and all(x>=0 for x in coefficients),'nonpositive coefficient certificate')

def check_evidence(data):
 require(data.get('q')=='4+u','wrong symbolic domain')
 normal=data.get('weighted_normal_minors',[])
 require(len(normal)==9,'missing normal minors')
 for rec in normal:
  coefficient_polynomial(rec['numerator'])
  require(rec['denominator']==['1'],'normal minor must be polynomial')
 blocks=data.get('sectors',[])
 require(len(blocks)==5,'missing complete sector')
 total=0
 for b,degree,size in zip(blocks,DEGREES,[4,2,3,1,1]):
  require(b['degree']==list(degree),'wrong sector order')
  for name in ['lower','upper']:
   signs=b[name+'_signs'];coefficient_polynomial(signs['common_positive_denominator'])
   require(len(signs['minors'])==size,'missing leading minor')
   for order,rec in enumerate(signs['minors'],1):
    require(rec['order']==order and rec['coefficient_positive'] is True and rec['negative_coefficient_count']==0,'misstated polynomial sign')
    coefficient_polynomial(rec['numerator']);total+=1
 require(total==22,'incomplete 22-sign coverage')

def symbolic_certificate():
 q=R((4,1));p,r,normal=recover(q)
 for minor in normal:minor.coefficients_positive()
 result={'agent':'six-downset-3','role':'researcher','q':'4+u',
  'potentials_p':p,'potentials_r':r,'weighted_normal_minors':normal,'sectors':[]}
 for j,ell in DEGREES:
  b=sector(q,p,r,j,ell)
  record={k:b[k] for k in ['degree','S_types','Q_types','S_norms','Q_norms']}
  for name in ['lower','upper']:
   g=b[name]
   if j==ell==0:g=[row[1:] for row in g[1:]]
   record[name+'_signs']=positive_minors(g)
  result['sectors'].append(record)
  print(json.dumps({'symbolic_sector':[j,ell],'leading_signs':2*len(g)}),flush=True)
 result=serial(result);check_evidence(result)
 return result,p,r

def rejection_controls(signs,p,r):
 rejected=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,TypeError,ZeroDivisionError):rejected.append(label)
  else:raise ValueError('failed rejection control: '+label)
 reject('float_field',lambda:R(0.5))
 reject('zero_field_denominator',lambda:R(1,0))
 reject('nonexact_polynomial_division',lambda:exact_divide((F(1),F(0),F(1)),(F(1),F(1))))
 reject('zero_leading_pivot',lambda:ff_eliminate([[R(0)]]))
 reject('nonsquare_symbolic_Gram',lambda:positive_minors([[R(1),R(0)]]))
 reject('asymmetric_symbolic_Gram',lambda:positive_minors([[R(1),R(1)],[R(0),R(1)]]))
 reject('negative_symbolic_Gram',lambda:positive_minors([[R(-1)]]))
 reject('corrupt_symbolic_potential',lambda:sector(R((4,1)),[p[0]+1]+p[1:],r,0,0))
 bad=deepcopy(signs);bad['sectors'][0]['lower_signs']['minors'][0]['numerator'][0]='-1'
 reject('negative_stored_sign',lambda:check_evidence(bad))
 bad=deepcopy(signs);bad['sectors'][0]['upper_signs']['common_positive_denominator'][0]='-1'
 reject('negative_stored_denominator',lambda:check_evidence(bad))
 bad=deepcopy(signs);bad['sectors'].pop()
 reject('missing_sector',lambda:check_evidence(bad))
 reject('below_literal_domain',lambda:potentials(3))
 reject('float_literal_domain',lambda:potentials(4.0))
 reject('bool_literal_domain',lambda:potentials(True))
 reject('zero_repair',lambda:construct(4,F(0)))
 reject('negative_repair',lambda:construct(4,F(-1)))
 reject('above_sufficient_repair',lambda:construct(4,F(1,720)))
 reject('float_repair',lambda:construct(4,1/1440))
 for label,matrix in [
  ('indefinite',[[1,2],[2,1]]),('zero_pivot_nonzero_row',[[0,1],[1,0]]),
  ('nonsquare',[[1,0]]),('asymmetric',[[1,0],[1,1]]),('float',[[1.0]])]:
  reject(label,lambda a=matrix:schur_psd(a))
 X,L=construct(4,F(1,1440))
 bad=deepcopy(L);bad[0][0]+=1
 reject('wrong_original_empty_loop',lambda:verify_full(4,X,bad))
 bad=deepcopy(L);bad[1][1]+=1
 reject('wrong_original_diagonal',lambda:verify_full(4,X,bad))
 with tempfile.TemporaryDirectory(prefix='maximal-deletion-control-') as tmp:
  base=Path(tmp)
  for name in bootstrap.EXPECTED:(base/name).write_bytes((bootstrap.BASE/name).read_bytes())
  (base/'poly.py').write_bytes((base/'poly.py').read_bytes()+b'\n# damaged control\n')
  reject('damaged_public_helper',lambda:bootstrap.setup(base))
 for rank,matrix in [(0,[[0]]),(1,[[1,0],[0,0]]),(2,[[2,-1],[-1,2]])]:
  require(schur_psd(matrix)==rank and polynomial_psd(matrix)[0]==rank,'positive matrix control')
 return rejected

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 start=time.monotonic();signs,p,r=symbolic_certificate()
 path=HERE/'SIGNS.json'
 if args.write:path.write_text(json.dumps(signs,indent=2,sort_keys=True)+'\n')
 else:require(json.loads(path.read_text())==signs,'stored infinite certificate differs')
 records=[]
 for q in [4,5,6,8]:
  pp,rr=potentials(q);rec=check(q,pp,rr,p,r);records.append(rec)
  print(json.dumps({'literal_q':q,'N':rec['N'],'rank_L':rec['rank_L'],'rank_upper':rec['rank_upper'],'action_columns':rec['action_columns']}),flush=True)
 # A second point inside the closed interval; all real points are covered by the proof.
 X,L=construct(4,F(1,2880));verify_full(4,X,L)
 controls=rejection_controls(signs,p,r)
 results={'agent':'six-downset-3','role':'researcher','proof_status':'author-checked ordinary unformalized proof; independent review pending',
  'unbounded_floor_signs':22,'normal_minors':9,'literal_cases':records,
  'literal_action_columns':sum(x['action_columns'] for x in records),
  'secondary_characteristic_forms':sum(x['secondary_characteristic_forms'] for x in records),
  'mid_interval_q4':True,'rejection_controls':controls,'positive_matrix_controls':3,
  'SIGNS_sha256':digest(signs),'records_sha256':digest(records)}
 path=HERE/'RESULTS.json'
 if args.write:path.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
 else:require(json.loads(path.read_text())==results,'stored results differ')
 print(json.dumps({'passed':True,'unbounded_signs':22,'literal_action_columns':88,'rejections':len(controls),
  'SIGNS_sha256':results['SIGNS_sha256'],'records_sha256':results['records_sha256'],
  'seconds':round(time.monotonic()-start,3),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)

if __name__=='__main__':main()
