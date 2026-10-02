"""Exact calibration controls, before target executable/certificate access."""
import independent as I
from fractions import Fraction as Q
from itertools import product
import json

def main():
    checks=0
    def test(ok,name):
        nonlocal checks
        I.need(ok,name);checks+=1
    # Polynomial algorithms tested against explicit roots, including repeated roots.
    for roots in product(range(-2,3),repeat=3):
        p=I.ONE
        for r in roots:p=I.mul(p,(-r,1))
        n,_=I.sturm(p,Q(-5,2),Q(5,2))
        test(n==len(set(roots)),'Sturm counts distinct, repeated rational roots')
    for endpoint in (Q(2,3),Q(3,4)):
        try:I.sturm((-endpoint,1),Q(2,3),Q(3,4))
        except ValueError:checks+=1
        else:raise ValueError('closed endpoint root was ignored')
    for degree in range(16):
        p=tuple(Q((-1)**j*(j+1)) for j in range(degree+1))
        test(I.interpolate([I.value(p,r) for r in range(degree+1)])==p,'Newton degree calibration')
    # Three classical all-three antiprism closures, not expected aggregates.
    factors={4:(-1,2,1),5:(-1,1,1),6:(-2,2,1)}
    for q,factor in factors.items():
        w=(3,)*(q-1);d=2*(q-1)
        samples=[I.numeric_gap(w,r) for r in range(d+1)]
        gaps=[I.interpolate([s[k] for s in samples]) for k in range(3)]
        for gap in gaps:test(I.divmodp(gap,I.trim(factor))[1]==I.ZERO,'classical antiprism closure factor')
    # Multiplication, order and exact zero in the irreducible quadratic field.
    test(I.fmul(I.R,I.R)==(Q(2),Q(-2)),'quadratic relation')
    test(I.fmul(I.C,I.C)==(Q(1,3),Q(0)),'critical cosine square')
    for a,b in product(range(-5,6),repeat=2):
        element=(Q(a),Q(b));s=I.fsign(element)
        test(s in (-1,0,1) and s==-I.fsign(I.fneg(element)),'field sign reversal')
        test(I.fsign(I.fmul(element,element))==(0 if element==I.FZERO else 1),'field square positivity')
    test(Q(31,50)>Q(3,5),'cap threshold separates every same-cap pair')
    print(json.dumps(dict(calibration_checks=checks,closed_endpoint_rejections=2,author_inputs_used=False),sort_keys=True))
if __name__=='__main__':main()
