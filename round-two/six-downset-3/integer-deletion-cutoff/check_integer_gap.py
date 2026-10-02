"""Portable whole identities for the unbounded integer-gap extension."""
from pathlib import Path
import sys,json,time
SOURCE=Path(__file__).resolve().parent
import source_pins
if Path(source_pins.__file__).resolve().parent!=SOURCE:raise ValueError('Wrong source-local pin helper')
source_pins.check(optional=False)
public=SOURCE.parent/'three-vector-residual-cap'
sys.path.insert(0,str(public))
import residual,check_coefficients as cc
for helper in (residual,cc):
 if Path(helper.__file__).resolve().parent!=public:raise ValueError('Wrong defining parent helper: '+helper.__name__)
from algebra import mul,add,scale,constant,Q,K,ONE
F,require=residual.F,residual.require


def derivative_certificate(n,d,certificate):
 # Independent monomial derivative and multiplication; independent substitution
 # expansion, rather than the generator's direct binomial coefficient shift.
 def derivative(p):
  result={}
  for exponent,value in p.items():
   degree,kk=exponent
   if degree:result[(degree-1,kk)]=value*degree
  return result
 numerator=add(mul(derivative(n),d),scale(mul(n,derivative(d)),-1))
 replace=add(Q,scale(K,5),constant(125));shift=add(K,constant(25))
 actual=cc.substitute(numerator,replace,shift)
 actual={(x,u):c for (u,x),c in actual.items()}
 wanted=cc.decode(certificate['coefficients'])
 require(actual==wanted,'every complete derivative coefficient from independent substitution')
 require(certificate['coefficient_count']==len(actual) and certificate['negative_count']==0 and actual[(0,0)]>0 and all(c>=0 for c in actual.values()),'entire unbounded derivative sign')
 return len(actual)


def norm57_certificate(n,certificate):
 require(certificate['minimum_k']==25 and certificate['norm_constant']==57,'norm57 entire claimed domain')
 norm=add(mul(Q,Q),scale(mul(K,K),-28),scale(K,-36),constant(-57))
 replace=add(scale(K,3),scale(Q,F(1,2)),constant(F(-25,2)))
 quotient=cc.decode(certificate['quotient_coefficients']);rem=cc.decode(certificate['remainder_coefficients'])
 require(cc.substitute(scale(n,-1),replace,K)==add(mul(quotient,norm),rem),'entire negative-Q norm57 quotient identity')
 require(all(i<=1 for i,j in rem),'linear norm57 remainder')
 ff={p:c for p,c in rem.items() if p[0]==0};hh={(0,j):c for (i,j),c in rem.items() if i==1}
 shift=add(K,constant(25));f=cc.substitute(ff,Q,shift);h=cc.substitute(hh,Q,shift)
 stored=lambda x:{(0,p[0]):F(c) for p,c in x if F(c)}
 require(f==stored(certificate['shifted_f']) and h==stored(certificate['shifted_g']),'entire norm57 shifted coefficients')
 pos={p:c for p,c in h.items() if c>0};neg={p:c for p,c in h.items() if c<0}
 low=add(scale(shift,5),constant(9));high=add(scale(shift,F(16,3)),constant(3))
 result=add(f,mul(pos,low),mul(neg,high))
 require(result==stored(certificate['coefficient_sandwich']) and result[(0,0)]>0 and all(c>=0 for c in result.values()),'entire norm57 negative-Q sandwich')
 return len(result)


def modular_exclusions(records):
 require(len(records)==2,'both modular exclusions retained')
 for record,(norm,prime,forced) in zip(records,((65,11,(8,0)),(73,5,(4,0)))):
  require(record['norm']==norm and record['prime']==prime and record['squared_modulus']==prime*prime,'exact claimed modulus')
  pairs=[(k,p) for k in range(prime) for p in range(prime) if (p*p-28*k*k-36*k-norm)%prime==0]
  require(pairs==[forced] and [list(x) for x in pairs]==record['entire_prime_solutions'],'every original prime residue')
  pp=prime*prime
  large=[(k,p) for k in range(pp) for p in range(pp) if (p*p-28*k*k-36*k-norm)%pp==0]
  require(large==record['entire_squared_solutions']==[],'every original squared-modulus residue')


def run():
 start=time.perf_counter();public=SOURCE.parent/'three-vector-residual-cap'
 raw=json.loads((public/'POLYNOMIAL-SLACK.json').read_text());saved=raw.pop('record_sha256');require(residual.digest(raw)==saved=='9accb1e7993765314f92a27597b05a44e6701f03d0fd42aee9aec4be068e2ac6','entire published Q form')
 data=json.loads(Path(__file__).with_name('INTEGER-GAP.json').read_text());saved=data.pop('record_sha256');require(residual.digest(data)==saved=='bfdd4eca312d7b205b561d7beb36ff6c0755018516f3504316d84e98f1912cb1','entire source generator freeze')
 n,d=(cc.decode(raw['forms'][name]) for name in ('Q_numerator','Q_denominator'))
 counts=[derivative_certificate(n,d,data['derivative']),norm57_certificate(n,data['negative_norm57'])];modular_exclusions(data['modular_exclusions'])
 damages=[]
 from copy import deepcopy
 def reject(name,call):
  try:call()
  except ValueError:damages.append(name)
  else:raise ValueError('Semantic damage accepted: '+name)
 bad=deepcopy(data['derivative']);bad['coefficients'][0][1]=str(F(bad['coefficients'][0][1])+1)
 reject('changed derivative coefficient',lambda:derivative_certificate(n,d,bad))
 reject('negated derivative numerator',lambda:derivative_certificate(scale(n,-1),d,data['derivative']))
 bad=deepcopy(data['negative_norm57']);bad['quotient_coefficients'][0][1]=str(F(bad['quotient_coefficients'][0][1])+1)
 reject('changed norm57 quotient',lambda:norm57_certificate(n,bad))
 bad=deepcopy(data['negative_norm57']);bad['coefficient_sandwich'][0][1]=str(F(bad['coefficient_sandwich'][0][1])+1)
 reject('changed norm57 sandwich',lambda:norm57_certificate(n,bad))
 bad=deepcopy(data['modular_exclusions']);bad[0]['entire_prime_solutions']=[]
 reject('omitted forced norm65 residue',lambda:modular_exclusions(bad))
 bad=deepcopy(data['modular_exclusions']);bad[1]['entire_squared_solutions']=[[4,0]]
 reject('invented norm73 residue',lambda:modular_exclusions(bad))
 # The frozen parent classification supplies ALL-q coverage for finite k.
 parent=public.parent/'remaining-deletion-orders/EXPECTED.json'
 frozen=json.loads(parent.read_text());frozen_digest=frozen.pop('record_sha256')
 require(residual.digest(frozen)==frozen_digest=='e21cefee85249a02ab731ba74b42e436c4b1c46768002bc55db5a04b2ce71715','entire credited9582 classification freeze')
 partition=frozen['complete_classification']
 positives=set(partition['positive_boundary_cutoff_b_minus5']);negatives=set(partition['negative_boundary_cutoff_b_minus4'])
 require(positives.isdisjoint(negatives) and positives|negatives==set(range(5,25)),'complete credited finite partition')
 from variance import bound
 finite=[]
 for kk in range(5,25):
  qq=bound(kk)-5;pp=2*qq-6*kk+25;nn=pp*pp-28*kk*kk-36*kk
  predicted=nn>=81 and (kk,qq)!=(5,18)
  from math import isqrt
  rr=isqrt(28*kk*kk+36*kk+81)
  if rr*rr<28*kk*kk+36*kk+81:rr+=1
  if rr%2==0:rr+=1
  cutoff=(6*kk-25+rr)//2
  if kk==5:cutoff=19
  require(cutoff==bound(kk)-(5 if kk in positives else 4),'closed cutoff matches every finite all-q parent')
  require(predicted==(kk in positives),'new norm expression matches every finite boundary decision')
  finite.append({'k':kk,'q':qq,'norm':nn,'credited_positive':kk in positives})
 result={'agent':'six-downset-3','role':'researcher','status':'whole exact certificate checks; ordinary proof supplied; independent review and formalization pending','coefficient_counts':counts,'complete_modular_squared_positions':121**2+25**2,'semantic_damages_rejected':damages,'hash_only_damages':0,'credited_finite_parent_record_sha256':frozen_digest,'all_twenty_boundary_norms_match':finite}
 result['record_sha256']=residual.digest(result)
 Path(__file__).with_name('CHECK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'seconds':time.perf_counter()-start,'digest':result['record_sha256'],'counts':counts,'damages':len(damages)}))
 return result


if __name__=='__main__':run()
