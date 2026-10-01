"""Dense cap from a rational three-layer positive-definite comparison.

Integerq=v-2-l>=0,v>=12,3v>=7q+10. Whole real0<eta<=1/(8v^2)
has upper gap>mk/(2v^2); parent lower maximal rank is unchanged.
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
    assert v>=12 and 3*v>=7*q+10
    return data


def cap_gap(v,lam):
    parameters(v,lam)
    return F((v-1)*(v-2)*(v-3),4*v)


def cap_bound(v,lam):return parameters(v,lam)[4]-cap_gap(v,lam)


def comparison_data(v,lam):
    """Scalar sufficient comparison; domain assertion is in parameters.

    This helper also permits exact investigation of excluded v>=12 inputs;
    no positivity theorem is asserted for those inputs.
    """
    _,_,_,s,N=ordinary_parameters(v,lam);assert v>=12
    q=v-2-lam;ww=weights(v,lam);c,d,t=[ww[key]for key in ('c','d','t')]
    diagonal=[F(s)+F(lam,3)+t*F(q*(q-1)*v,2),s+c,s+t*(v-5)]
    a12=F(v+2,4)+d*F(q*(v+7),8)
    a13=lam+F(v-3,2)+t*q*(v-2)
    a23=d*F((v-4)*(v+5),8)
    tau=N-F((v-1)*(v-2)*(v-3),4*v)
    G=[[diagonal[0],a12,a13],[a12,diagonal[1],a23],[a13,a23,diagonal[2]]]
    C=[[F(tau if i==j else 0)-G[i][j]for j in range(3)]for i in range(3)]
    a,b,z=[C[i][i]for i in range(3)];p,h,f=a12,a13,a23
    minors=[a,a*b-p*p,a*b*z-a*f*f-b*h*h-z*p*p-2*p*h*f]
    return G,C,minors,tau


def centered_certificate(v,lam,blocks):
    parameters(v,lam)
    return ordinary_centered(v,lam,blocks)


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    parameters(v,lam)
    if eta is None:eta=F(1,8*v*v)
    return ordinary_maximal(v,lam,blocks,centered,eta)


def fixtures():
    """One complement from a retained generator, not a design census."""
    from uniform_lambda import fixtures as parent_fixtures
    name,v,q,missing,generation=next(z for z in parent_fixtures()if z[0]=='cyclic_lambda4_13')
    blocks=sorted({mask(p)for p in combinations(range(v),3)}-set(missing))
    yield 'complement_cyclic_fourfold13',v,v-2-q,blocks,{
        'kind':'complement of retained cyclic simple fourfold13',
        'missing_name':name,'missing_blocks':missing,'missing_generation':generation}
