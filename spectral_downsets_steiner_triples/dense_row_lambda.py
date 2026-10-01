"""Maximum-row cap for dense simple triple designs.

q=v-2-l>=0, v>=12, 2v>=5q+10. DENSE_ROW_CAP.md proves strict
upper gap (N-max(R1,R2,R3))/2 for every real 0<eta<=1/(8v^2).
The parent ordinary H formula and lower maximal rank are reused.
Standard library only. six-downset-2, researcher.
"""
from fractions import Fraction as F
from itertools import combinations
from certificates import mask
from uniform_lambda_small import parameters as ordinary_parameters,weights
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal


def parameters(v,lam):
    data=ordinary_parameters(v,lam);q=v-2-lam
    assert v>=12 and 2*v>=5*q+10
    return data


def comparison_rows(v,lam):
    s=parameters(v,lam)[3];q=v-2-lam;t=weights(v,lam)['t'];u=F(q*(q-1),2)
    return [F(s)+F(lam,3)+t*u*v+F(v,3)+F(q*v,2)+(F(3,2)+2*q)*v,
        F(s)+F(4,3)+F(v,3)+F(q*v,2)+F(v*(v-4),2),
        F(s)+F(v*v,2)+(2*q+F(3,2))*v-10]


def cap_bound(v,lam):return max(comparison_rows(v,lam))


def cap_gap(v,lam):
    delta=parameters(v,lam)[4]-cap_bound(v,lam);assert delta>0
    return delta


def centered_certificate(v,lam,blocks):
    parameters(v,lam)
    return ordinary_centered(v,lam,blocks)


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    parameters(v,lam)
    if eta is None:eta=F(1,8*v*v)
    return ordinary_maximal(v,lam,blocks,centered,eta)


def fixtures():
    """One new cap-boundary input, from a retained generator; no census."""
    from uniform_threefold import fixtures as threefold_fixtures
    name,v,missing,generation=next(z for z in threefold_fixtures()if z[0]=='nondecomposable13')
    blocks=sorted({mask(p)for p in combinations(range(v),3)}-set(missing))
    yield 'complement_nondecomposable_threefold13',v,v-2-3,blocks,{
        'kind':'complement of retained nondecomposable threefold13',
        'missing_name':name,'missing_blocks':missing,'missing_generation':generation}
