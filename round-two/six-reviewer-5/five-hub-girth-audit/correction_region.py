"""Exact all-real coefficient/correction region for the stated encoding."""
from fractions import Fraction
import rows

def compute(proof):
    ordinary=[r for r in proof['rows'] if not r['I5']]
    exceptions=[r for r in proof['rows'] if r['I5']]
    a=lambda r:r['k']-r['e']-r['q']
    lower=max(Fraction(r['psi'],a(r)) for r in ordinary if a(r)<0)
    upper=min(Fraction(r['psi'],a(r)) for r in ordinary if a(r)>0)
    rows.need(lower==3 and upper==4,'complete418 coefficient interval')
    rows.need(all(r['psi']>=c*a(r) for r in ordinary for c in [lower,upper]),'all actual interval corner inequalities')
    rows.need(len(exceptions)==8 and all(a(r)==1 and r['psi']==0 for r in exceptions),'actual exceptional correction coefficient')
    # For I5=0 the exact feasible c interval follows from these ratios.
    # For I5=1 the remaining inequality is c*(1-b)<=0. Since c>=3,
    # it holds iff b>=1. Affinity in c proves sufficiency at every real c.
    def literal(r):return {'star':r['star'],'hubs':r['hubs'],'e':r['e'],'k':r['k'],'q':r['q'],'psi':r['psi'],'I5':r['I5']}
    low=[literal(r) for r in ordinary if a(r)<0 and Fraction(r['psi'],a(r))==lower]
    high=[literal(r) for r in ordinary if a(r)>0 and Fraction(r['psi'],a(r))==upper]
    rows.need(low and high and exceptions,'actual all-real necessity witnesses')
    return {'encoding':'psi >= c*(k-e-q-b*I5)','quantifiers':'One common real c and b over all426 actual local marks; complete coefficient region for this encoding only.',
            'complete_feasible_region':{'c_closed_interval':[3,4],'b_closed_ray_minimum':1},
            'I5_minimum_unit_correction_is_sharp_for_this_encoding':True,'lower_corner_attaining_marks':low,'upper_corner_attaining_marks':high,
            'one_correction_necessity_witness':literal(exceptions[0]),'historical_scope':'418 interval previously proved by peer9375; all426 corrected two-parameter region independently checked here. No globally optimal packing inequality or sharpP35 claim.'}
