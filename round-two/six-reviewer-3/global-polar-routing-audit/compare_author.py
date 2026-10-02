"""Late data-only whole coefficient/control comparison, no producer-code import."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from audit import build,communication,scalar,norm2,product,need
from polys import cast,symbol
from radial import coefficients,WINDOW

def decode(x):
 if type(x) is dict and set(x)=={'numerator','denominator'}:
  need(type(x['numerator']) is int and type(x['denominator']) is int and x['denominator']>0,'typed rational')
  return F(x['numerator'],x['denominator'])
 if type(x) is dict:return {k:decode(v) for k,v in x.items()}
 if type(x) is list:return [decode(v) for v in x]
 return x
def whole(p):return coefficients(p,'eta')
def from_record(record):
 from polys import Poly
 out={}
 for key,v in record.items():
  m=() if key=='1' else tuple((x.split('^')[0],int(x.split('^')[1]) if '^' in x else 1) for x in key.split('*'))
  out[m]=(F(v[0]),F(v[1]))
 return Poly(out)
def main():
 p=argparse.ArgumentParser();p.add_argument('--author-fixture',type=Path,required=True);args=p.parse_args()
 raw=args.author_fixture.read_bytes();r=decode(json.loads(raw));own=build();e=WINDOW
 need(r['schema']=='global-polar-routing-exact-v1' and r['eta_endpoint']==e,'source schema/domain')
 for author,mine in [('mean','mean'),('modulus','modulus'),('variance','variance_old')]:
  x=r['scalar_certificates'][author];y=own['polar'][mine]['certificate']
  need(x['polynomial']==list(map(F,y['coefficients'])),'EVERY coefficient '+author)
  need(x['head']==F(y['leading']) and x['absolute_tail_at_endpoint']==F(y['absolute_tail']) and
   x['uniform_lower_bound_after_eta_squared']==F(y['lower_after_factoring']) and x['threshold']==F(own['polar'][mine]['claimed_factored_floor']),'whole certificate '+author)
 need(r['complete_tail']==whole(from_record(own['balanced']['T'])),'whole T')
 need(r['complete_balanced_integral']==whole(from_record(own['balanced']['B'])),'whole B')
 for name,mine in [('K1','K1'),('K2','K2'),('K9','K9'),('P9','product_gradient')]:need(r['derivatives'][name]==F(own['scalars'][mine]),'whole derivative '+name)
 need(r['variance_budgets']=={'normalized':24576000,'transferred':24960000},'original budgets')
 need(r['routed_eta_endpoint']==F(1,2**37) and r['routed_energy_endpoint']==F(1,512),'original endpoint equality')
 K1=F(own['scalars']['K1']);K2=F(own['scalars']['K2']);K9=F(own['scalars']['K9']);P9=F(own['scalars']['product_gradient'])
 margins={'scalar_'+n:F(own['polar'][m]['certificate']['lower_after_factoring'])-F(own['polar'][m]['claimed_factored_floor']) for n,m in [('mean','mean'),('modulus','modulus'),('variance','variance_old')]}
 margins.update({'derivative350':350-K1,'hessian_ordered_pairs':2*K1-K2,'origin_lipschitz600':600-K9,
  'product_lipschitz6':6-P9,'radial_normalization_phase10':10-9*(1+3*e/2),
  'normalized_second_symmetric_7over4':28*(1-e)**2-26-F(7,4),
  'variance_transfer65over64':F(65,64)-F(256,255)**2,'mean_modulus_positive':8-6*e,
  'individual_left_of_mark':1-165*e,'weighted_original_radial10':2-10*e-81*e*e,
  'origin_radial_gap60000':60000-(350*160+600*6+6*6),
  'energy_carrier2pow28':2**28-(199680144+52*e),'linear13over5':F(8,3)-F(13,5)-F(4,3)*e})
 need(r['strict_margins']==margins and len(margins)==16,'ALL original strict margins')
 for row in r['gaussian_controls']:
  q=[cast(tuple(x)) for x in row['reciprocals']];rs=row['radii'];a=row['a'];C,O=communication(q,a)
  need(scalar(C)==tuple(row['polar']) and scalar(O)==tuple(row['origin']),'full Gaussian C/O control')
  need(all(norm2(x)==rr*rr for x,rr in zip(q,rs)),'all Gaussian radii')
  mean=sum(rs)/8;V=sum((x-mean)**2 for x in rs);delta=sum(rr-scalar(x)[0] for x,rr in zip(q,rs))
  need(V==row['variance'] and delta==row['angular_defect'],'full Gaussian moments')
 for row in r['actual_controls']:
  a=1-row['eta'];qs=[cast(1/(1+a))]*7+[cast(9/(1+a))];C,O=communication(qs,a)
  need(scalar(C)==tuple(row['polar']) and scalar(O)==tuple(row['origin']) and row['F']==16/(1+a) and row['critical_multiplicities']==[7,1],'full actual multiplicity control')
 print(json.dumps({'status':'PASS','producer_fixture_sha256':hashlib.sha256(raw).hexdigest(),
  'whole_original_polar_polynomials':3,'whole_B_and_T':2,'original_strict_margins':16,
  'full_derivative_constants':4,'complete_gaussian_controls':len(r['gaussian_controls']),
  'actual_multiplicity_controls':len(r['actual_controls']),'producer_executable_imported':False,
  'scope':'late data-only corroboration; new radial39/5 and energy82m come from sealed own proof'},sort_keys=True))
if __name__=='__main__':main()
