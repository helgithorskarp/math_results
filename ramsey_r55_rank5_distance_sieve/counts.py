"""Exact all-pattern count by the number of repeated row classes."""
from functools import lru_cache
from fractions import Fraction
from math import comb
import base_counts as prior


@lru_cache(None)
def marked_bins(length,letters,cap=3):
    states={(0,0):1}
    for _ in range(letters):
        new={}
        for (k,j),value in states.items():
            for t in range(min(cap,length-k)+1):
                key=(k+t,j+int(t>=2))
                new[key]=new.get(key,0)+comb(k+t,t)*value
        states=new
    return [states.get((length,j),0) for j in range(length//2+1)]


def span_polynomial(length,rank,affine=False):
    result=[0]*(length//2+1)
    dim=rank-1 if affine else rank
    for k in range(dim+1):
        coeff=prior.gaussian(dim,k)*(-1)**(dim-k)*2**comb(dim-k,2)
        if affine:coeff*=2**(dim-k)
        values=marked_bins(length,2**k if affine else 2**k-1)
        for j,value in enumerate(values):result[j]+=coeff*value
    return result


def strata(m=20,n=23,r=5):
    a0=span_polynomial(m,r);a1=span_polynomial(m-1,r)
    affine=span_polynomial(m,r,True)
    b0=prior.nonzero_span(n,r,5)
    b= sum(comb(n,z)*prior.nonzero_span(n-z,r,5) for z in range(min(2,n)+1))
    lb=prior.affine_span(n,r,5)
    gl=prior.group_order(r)
    records=[]
    for j in range(m//2+1):
        raw=a0[j]*b+(m*a1[j]*b0 if j<len(a1) else 0)
        low=(2**r-1)*2**(r-1)*affine[j]*lb
        if raw%gl or low%gl:raise ArithmeticError('nonintegral stratum quotient')
        records.append({'repeated_row_classes':j,'raw':raw//gl,'blue_rank_four':low//gl,'cross_matrices':(raw-low)//gl})
    if (m,n,r)==(20,23,5) and sum(v['cross_matrices'] for v in records)!=prior.compute()['remaining']:
        raise ArithmeticError('wrong baseline partition')
    return records


def compute():
    from distance import grouped_transfer
    rows=strata()
    transfers=[]
    for p in range(11):
        q,states=grouped_transfer(pairs=p)
        transfers.append({'pairs':p,'keep_fraction':[q.numerator,q.denominator],
                          'signed_states':states})
    probabilities=[Fraction(*r['keep_fraction']) for r in transfers]
    scale=max(q.denominator for q in probabilities)
    if scale&(scale-1) or any(scale%q.denominator for q in probabilities):
        raise ArithmeticError('non-dyadic transfer')
    baseline=sum(r['cross_matrices'] for r in rows)
    remaining=sum(r['cross_matrices']*probabilities[r['repeated_row_classes']]*scale for r in rows)
    if remaining.denominator!=1:raise ArithmeticError('nonintegral full-graph unit')
    units=baseline*scale;removed=units-remaining.numerator;fraction=Fraction(removed,units)
    return {'status':'EXACT_RANK5_DISTANCE_SIEVE_COUNTS','strata':rows,
            'cross_baseline':baseline,'transfers':transfers,
            'unit_exponent':443-(scale.bit_length()-1),'baseline_units':units,
            'remaining_units':remaining.numerator,'removed_units':removed,
            'removed_fraction':[fraction.numerator,fraction.denominator],
            'internal_pairs_before_sieve':443,'maximum_selected_pairs':10}


if __name__=='__main__':
    import json
    print(json.dumps(compute(),indent=2,sort_keys=True))
