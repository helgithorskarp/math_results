"""Actual coefficient-binding, determinant and closed-boundary damages."""
import json
from fractions import Fraction as F
from derive import rebuild, polynomial
from digit import T, Z, prove_zero
from signs import bound
from check import LARGER


def reject_zero(p):
    try:prove_zero(p)
    except ValueError:return True
    raise ValueError('actual nonzero polynomial corruption accepted')


def strict_certificate(p):
    lo,hi=bound(p,LARGER)
    if lo<=0:raise ValueError('not a strict whole CLOSED rectangle certificate')
    return str(lo),str(hi)


def check():
    m, factors, records=rebuild()
    t,z=T,Z;a,b,c,D,C,K,J,O,R=(m[k] for k in ['a','b','c','D','C','K','J','Omega','R'])
    Q=a*D*z*z-2*D*z+2*t*t-t+1;L=7*t*t+2*t-1;Y=m['Y']
    originals={};multipliers={}
    for name,central,i,j,normal,rhs,F0 in [
        ('067',0,6,7,[-5,-14,20],15,a**6*b*b*c*c*(3*t-1)*(b*z+1)),
        ('579',5,7,9,m['N'][10],t*a*a,t*a**10*b*b*c*c*(3*t-1)*(b*z+1)**2*Q),
        ('6911',11,6,9,[-8,12,-5],9,a**5*b*b*c*c*(3*t-1)*(b*z+1))]:
        from geometry import dot
        v=[((Y[i][k]+Y[j][k])*a*a-Y[central][k]*L)*t for k in range(3)]
        raw=dot(v,normal)-O*b*b*c*rhs
        originals['A'+name],originals['B'+name]=raw.p,raw.q
        multipliers['A'+name]=multipliers['B'+name]=F0
    for name,F0 in [('067',a*b**4*c*c*J*Q),('579',4*a*a*b**4*c*c*J)]:
        originals['H'+name]=polynomial(factors['B'+name])**2*R-polynomial(factors['A'+name])**2
        multipliers['H'+name]=F0
    damages=[]
    for name,coeffs in factors.items():
        # Real integral coefficient change, checked against original coordinates.
        bad=dict(coeffs);power=min(bad);bad[power]+=1
        reject_zero(originals[name]-multipliers[name]*polynomial(bad))
        error=sum(F(v-coeffs.get((i,j),0))*F(29,50)**i*F(5400,3973)**j for (i,j),v in bad.items())
        if error==0:raise ValueError('direct rational arithmetic did not detect coefficient change')
        damages.append({'factor':name,'altered_monomial':list(power),'actual_integer_image_binding_rejected':True,
                        'separate_direct_rational_error':str(error)})
        # A genuine neutral reordering remains the same whole polynomial.
        reordered=dict(reversed(list(coeffs.items())))
        prove_zero(originals[name]-multipliers[name]*polynomial(reordered))
    det=a**4-2*t*t*a**4+2*t*t*K*a*a-K*K
    reject_zero(det-b**4*c*(3*t+1)**2+1)
    ta,tb,za,zb=map(F,LARGER)
    closed=[{(1,0):25,(0,0):-14},{(1,0):-5,(0,0):3},
            {(0,1):5,(0,0):-6},{(0,1):-5,(0,0):7}]
    zero_endpoints=[]
    for p,point in zip(closed,[(ta,za),(tb,za),(ta,za),(ta,zb)]):
        exact=sum(F(v)*point[0]**i*point[1]**j for (i,j),v in p.items())
        if exact!=0:raise ValueError('claimed closed endpoint zero differs')
        try:strict_certificate(p)
        except ValueError:zero_endpoints.append({'full_literal_rows':[[i,j,v] for (i,j),v in sorted(p.items())],
                                                'actual_closed_zero':[str(q) for q in point],'strict_claim_rejected':True})
        else:raise ValueError('closed endpoint wrongly certified strict')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'actual_original_coordinate_coefficient_damages':damages,
            'neutral_whole_coefficient_reorder_controls':8,
            'actual_false_Gram_determinant_rejected':True,
            'all4_closed_endpoint_zero_claims_rejected':zero_endpoints,
            'hash_only_damage_checks':False,'new_target_native_input':False}


if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
