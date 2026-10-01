"""Capped maximal-rank H for dense simple triple designs.

q=v-2-lambda>=0, v>=12, v>=4(q+1). DENSE_COMPLEMENT_CAP.md proves
the centered bound B and strict repaired gap delta/2 for every real
0<eta<=1/(8v^2). Construction reuses the all-orders ordinary H formula.
Standard library only. Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from itertools import combinations
from certificates import mask
from uniform_lambda_small import parameters as ordinary_parameters
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal


def parameters(v,lam):
    data=ordinary_parameters(v,lam);q=v-2-lam
    assert v>=12 and v>=4*(q+1)
    return data


def cap_bound(v,lam):
    parameters(v,lam);q=v-2-lam;s=ordinary_parameters(v,lam)[3]
    return F(s)+F(v*v,2)+(q*q+2*q+F(3,2))*v-10


def cap_gap(v,lam):
    N=parameters(v,lam)[4];delta=N-cap_bound(v,lam);assert delta>0
    return delta


def centered_certificate(v,lam,blocks):
    parameters(v,lam)
    return ordinary_centered(v,lam,blocks)


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    parameters(v,lam)
    if eta is None:eta=F(1,8*v*v)
    return ordinary_maximal(v,lam,blocks,centered,eta)


def fixtures():
    """Three literal dense inputs, not a design census or new designs."""
    v=12
    yield 'complete12',v,10,[mask(p) for p in combinations(range(v),3)],{'kind':'all triples','complement_degree':0}
    from certificates import cyclic_sts13
    v=13;missing=cyclic_sts13()
    blocks=sorted({mask(p) for p in combinations(range(v),3)}-set(missing))
    yield 'complement_STS13',v,10,blocks,{'kind':'complement of retained cyclic STS13','complement_degree':1,'missing_blocks':missing}
    from small_twofold import fixtures as twofold_fixtures
    _,v,missing,generation=next(row for row in twofold_fixtures() if row[1]==12)
    blocks=sorted({mask(p) for p in combinations(range(v),3)}-set(missing))
    yield 'complement_twofold12',v,8,blocks,{'kind':'complement of retained rotational twofold12','complement_degree':2,'missing_blocks':missing,'missing_generation':generation}
