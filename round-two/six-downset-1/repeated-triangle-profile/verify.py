"""Reconstruct ALL exact mathematical fields; normal/-O and compact comparison.

One serial job, six native thread variables1, unchanged60s/512terms/
32MiB/n6/N80. Full generated corpus stays local when --record is used.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse,copy,json,signal,time,resource,sys
from certificate import generate
from check_certificate import check as certificate_check
from original import build,whole_lift
from baseline import replay
from model import construct
from exact import require,psd_rank,check,lift
from bivariate import P

def canonical(a):return json.dumps(a,sort_keys=True,separators=(',',':'),default=str)
def compact(record):
 d=record['mathematics'];return {'agent':d['agent'],'role':d['role'],'scope':d['scope'],'record_sha256':record['record_sha256'],'counts':d['counts'],'uniform_sign_table':d['checking']['checks'],'original_fixtures':[row['validation'] for row in d['fixtures']],'baseline9361':d['baseline'],'scalar_controls':d['scalar_controls'],'semantic_damages':d['damages'],'independent_review':False,'formalization':False}

def signed_controls():
 records=[]
 for label,degree,two in [('small',5,False),('packed',18,False),('two-dimensional',20,True),('large-signed',21,False)]:
  terms={((i//4,i%4) if two else (0,i)):((-1)**i)*(3*i+5)*((1<<90) if label=='large-signed' else 1) for i in range(degree)}
  second={((i//4,i%4) if two else (0,i)):((-1)**(i+1))*(2*i+7) for i in range(degree-1)}
  a,b=P(terms,7),P(second,11);product=a*b;expected={}
  for e,x in terms.items():
   for f,y in second.items():
    ex=tuple(e[j]+f[j] for j in range(2));expected[ex]=expected.get(ex,F(0))+F(x*y,77)
  require(product==P.fractions(expected),'EVERY independent signed convolution coefficient')
  quotient=product.exact_div(b);require(quotient==a,'EVERY independent exact quotient coefficient')
  require((product+1).exact_div(b) is None,'strict nondivision rejection')
  records.append({'label':label,'product_denominator':product.den,'every_product_coefficient':[[list(e),str(c)] for e,c in sorted(product.a.items())],'whole_quotient_fingerprint':quotient.fingerprint(),'nondivisor_rejected':True})
 return records

def damages(cert,family,C,MS):
 labels=[]
 def reject(label,fn):
  try:fn()
  except ValueError:labels.append(label);return
  raise ValueError('semantic damage accepted: '+label)
 def damage(label,fn):
  bad=copy.deepcopy(cert);fn(bad);reject(label,lambda:certificate_check(bad))
 damage('negative shifted constant',lambda d:d['rows'][0]['shifted']['terms'][0].__setitem__(1,'-1'))
 damage('wrong complete original polynomial',lambda d:d['rows'][0]['original']['terms'][0].__setitem__(1,str(int(d['rows'][0]['original']['terms'][0][1])+1)))
 damage('duplicate whole monomial',lambda d:d['rows'][0]['shifted']['terms'].append(d['rows'][0]['shifted']['terms'][0]))
 damage('negative coefficient denominator',lambda d:d['rows'][0]['original'].__setitem__('denominator',-1))
 damage('missing final fixed10 minor',lambda d:d['rows'].pop())
 damage('wrong whole obligation order',lambda d:d['rows'].reverse())
 damage('incomplete original scalar matrix',lambda d:d['forms']['alphaH']['raw_original'][0].clear())
 damage('negative original row multiplier',lambda d:d['forms']['alphaH']['constants'].__setitem__(0,'-1'))
 damage('wrong leading prefix',lambda d:d['rows'][0]['cleared_original_matrix'][0][0]['terms'][0].__setitem__(1,'100000'))
 damage('false physical dimension',lambda d:d['identities'].__setitem__('physical_change_rank',19))
 damage('missing heavy anti multiplicity',lambda d:d['identities'].__setitem__('heavy_anti_equal_positions',4))
 damage('wrong original support identity count',lambda d:d['identities'].__setitem__('original_field_positions',98))
 damage('wrong entire uniform domain',lambda d:d.__setitem__('domain','realq>=8'))
 s=F(10);seed=lift(C,s);bad=[row[:] for row in MS]
 for j in range(len(bad)):bad[0][j]=seed[0][j];bad[j][0]=seed[j][0]
 reject('retaining seed empty row and loop after repair',lambda:check(family,bad,s))
 bad=[row[:] for row in MS];bad[1][1]=1
 reject('original intersecting diagonal nonzero',lambda:check(family,bad,s))
 reject('omitted actual empty vertex',lambda:check(family[1:],[row[1:] for row in MS[1:]],s))
 reject('unsupported altered parameter recipe',lambda:construct(4,'mean',F(1,4),F(-2,5)))
 reject('q2 outside proved real domain',lambda:construct(2))
 return labels

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--check',type=Path);args=parser.parse_args()
 def alarm(signum,frame):raise TimeoutError('fixed60s integrated stage guard')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic();cert=generate();checking=certificate_check(cert)
 baseline=[replay(n) for n in [3,4,5]];fixtures=[];first=None
 for n in [3,4,5]:
  fam,C,MS,status=build(n);fixtures.append({'validation':status,'all_original_sets':fam,'all_seed_core_positions':C,'all_sharp_original_positions':MS})
  if first is None:first=(fam,C,MS)
 scalar=[]
 for q in [F(4),F(9,2),F(5),F(7),F(8),F(9),F(10),F(11),F(12),F(16),F(32),F(1000)]:
  p,G,S,cap,_=construct(q);require(psd_rank(G)==20 and psd_rank(cap)==20,'whole exact scalar control')
  scalar.append({'q':str(q),'muH':str(p['muH']),'muL':str(p['muL']),'nu':str(p['nu']),'alphaH':str(p['alphaH']),'betaH':str(p['betaH']),'alphaL':str(p['alphaL']),'betaL':str(p['betaL'])})
 signs=signed_controls();bad=damages(cert,*first)
 counts={'uniform_obligations':len(cert['rows']),'positive_coefficients':checking['positive_coefficients'],'whole_original_form_positions':checking['whole_original_form_positions'],'full_determinant_identity_points':checking['full_determinant_identity_points'],'full_shift_points':checking['full_shift_points'],'positive_clearing_factor_shift_points':checking['positive_clearing_factor_shift_points'],'full_original_entry_identity_points':checking['full_original_entry_identity_points'],'live_original_fraction_bindings':checking['live_original_fraction_bindings'],'cross_sector_positions':cert['identities']['cross_sector_positions'],'original_field_positions':99,'actual_fixtures':3,'all_original_positions_per_seed_or_sharp':sum(row['validation']['original_positions'] for row in fixtures),'whole_original_Gram_positions':1200,'whole_original_frame_positions':1200,'all_whole_repair_positions':sum(row['validation']['all_whole_repair_entries'] for row in fixtures),'actual_untouched_high':22,'actual_untouched_low':19,'actual_forced_star_kernels':3,'baseline9361_core_positions':sum(row['ordered_core_positions'] for row in baseline),'scalar_controls':len(scalar),'semantic_damages':len(bad),'signed_arithmetic_controls':3*len(signs)}
 data={'agent':'six-downset-1','role':'researcher','scope':'every n>=3, two private triangles atx and one atdistincty; realauxq>=4; ordinary bridges unformalized; not generalH/I','certificate':cert,'checking':checking,'baseline':baseline,'fixtures':fixtures,'scalar_controls':scalar,'signed_controls':signs,'damages':bad,'counts':counts}
 # Whole canonical Fraction/tuple normalization precedes every hash and comparison.
 data=json.loads(canonical(data));digest=sha256(canonical(data).encode()).hexdigest();record={'mathematics':data,'record_sha256':digest}
 if args.record:args.record.write_text(json.dumps(record,indent=2)+'\n')
 if args.check:require(json.loads(args.check.read_text())==record,'ENTIRE regenerated full mathematical record agrees')
 expected=Path(__file__).with_name('RESULTS.json')
 if expected.exists():require(json.loads(expected.read_text())==compact(record),'ENTIRE compact record and full hash agree')
 elif not args.record:raise FileNotFoundError('RESULTS missing; use --record for first full reconstruction')
 signal.alarm(0)
 print(json.dumps({'agent':'six-downset-1','role':'researcher','status':'PASS','record_sha256':digest,'counts':counts,'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':bool(sys.flags.optimize),'whole_record_compared':bool(args.check),'independent_review':False,'formalization':False},sort_keys=True))
if __name__=='__main__':main()
