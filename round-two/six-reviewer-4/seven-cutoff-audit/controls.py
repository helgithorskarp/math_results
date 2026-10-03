"""Actual semantic rejection controls, after all complete positive checks."""
import copy,json,sys
from pathlib import Path
from fractions import Fraction as F
from exact import need,canon,ldlt,polynomial_psd
from check import run
from produce import positive
def main(work):
 w=json.loads(Path(__file__).with_name('INPUT.json').read_text());n=json.loads((work/'q26-produce.json').read_text());p=json.loads((work/'q27-produce.json').read_text());run(w,n);run(w,p);rejected=[]
 def bad(name,which,change):
  a=copy.deepcopy(w);b=copy.deepcopy(n if which=='negative'else p);change(a,b)
  try:run(a,b)
  except(ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):rejected.append(name);return
  raise ValueError('accepted semantic damage '+name)
 idx=next(i for i,c in enumerate(w['negative_cases'])if c['q']==26)
 bad('zero-positive-weight','negative',lambda a,b:a['negative_cases'][idx]['weights'].__setitem__(0,'0'))
 bad('one-integer-vector-coordinate','negative',lambda a,b:a['negative_cases'][idx]['planes'][0]['coordinates'].__setitem__(0,a['negative_cases'][idx]['planes'][0]['coordinates'][0]+1))
 bad('wrong-actual-endpoint','negative',lambda a,b:a['negative_cases'][idx]['planes'][0].__setitem__('endpoint','cap'))
 bad('boolean-coordinate','negative',lambda a,b:a['negative_cases'][idx]['planes'][0]['coordinates'].__setitem__(0,True))
 bad('missing-entire-order','negative',lambda a,b:a['negative_cases'].pop(0))
 bad('wrong-physical-orbit-size','negative',lambda a,b:b['weights'].__setitem__(0,b['weights'][0]+1))
 bad('swapped-physical-keys','negative',lambda a,b:b['keys'].reverse())
 bad('wrong-kappa-orientation','negative',lambda a,b:b['orientation'].__setitem__(1,'-1'))
 bad('uncancelled-independent-tb','negative',lambda a,b:b['planes'][0]['coefficients'].__setitem__(2,'1'))
 bad('uncancelled-independent-tc','negative',lambda a,b:b['planes'][0]['coefficients'].__setitem__(3,'1'))
 def decoy(a,b):b['planes'][0]['coefficients'][2]='1';b['planes'][0]['coefficients'][3]='-1'
 bad('equal-trade-sum-preserving-decoy','negative',decoy)
 bad('uncancelled-BC','negative',lambda a,b:b['dual_sum'].__setitem__(4,'1'))
 bad('false-spectral-separation','negative',lambda a,b:b.__setitem__('dyadic_spectral_separation','1'))
 bad('wrong-original-vector-norm','negative',lambda a,b:b.__setitem__('weighted_vector_norm_squared','1'))
 bad('changed-one-actual-affine-entry','positive',lambda a,b:b['forms'][0][0].__setitem__(0,str(F(b['forms'][0][0][0])+1)))
 bad('changed-one-floored-entry','positive',lambda a,b:b['positive_forms'][2][0].__setitem__(0,str(F(b['positive_forms'][2][0][0])+1)))
 bad('zero-to-positive-rank','positive',lambda a,b:b['congruence_certificates'][0].__setitem__('rank',23))
 bad('false-full-original-rank','positive',lambda a,b:b.__setitem__('whole_lower_rank',541))
 bad('dropped-empty-loop','positive',lambda a,b:b.__setitem__('original_empty_M_loop','0'))
 bad('unproved-stronger-unit-gap','positive',lambda a,b:b.__setitem__('unit_gap','1'))
 # An actual failed sufficient floor is separate from mere record corruption.
 c=copy.deepcopy(w['positive']);c['upper_floor']='542'
 try:positive(c)
 except ValueError:rejected.append('actual-false-upper-floor')
 else:raise ValueError('false physical cap floor accepted')
 for a,r in [([[F(0),F(0)],[F(0),F(2)]],1),([[F(2),F(1)],[F(1),F(2)]],2),([[F(1),F(-1)],[F(-1),F(1)]],1)]:
  need(ldlt(a)[0]==polynomial_psd(a)[0]==r,'singular/nonsingular positive controls')
 need(len(rejected)==21,'all actual damages');return dict(semantic_damages=rejected,singular_positive_controls=3)
if __name__=='__main__':
 v=main(Path(sys.argv[1]));Path(sys.argv[2]).write_bytes(canon(v));print('21 semantic damages rejected; three exact positive controls pass.')
