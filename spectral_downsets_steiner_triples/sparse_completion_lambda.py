"""Direct-completion upper cap for any existing simple triple design.

Integerl>=2,v>=3l+8. Unchanged reviewed parent lower matrix; upper
gap delta/2 for every real0<eta<=1/(8v^2), delta=N-max(comparison rows).
The literal cyclic21 input is a fixed validation design, not a census.
six-downset-2, researcher.
"""
from fractions import Fraction as F
from certificates import mask
from uniform_lambda_small import parameters as ordinary_parameters,weights
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal


def parameters(v,lam):
    data=ordinary_parameters(v,lam);assert v>=3*lam+8
    return data


def comparison_data(v,lam):
    _,_,_,s,_=ordinary_parameters(v,lam);assert v>=14
    c,d,t,w,h=[weights(v,lam)[key]for key in ('c','d','t','w','h')]
    a12=w*F(v+2,4)+d*lam*F(v+7,8)
    a13=h*F(2*lam+v-3,4)+t*(lam-1)*F(6*lam+v-1,4)
    a23=d*F((v-4)*(v+5),8)
    diag=[s+F(lam,3)+t*F(lam*(lam-1)*v,2),s+c,s+t*(v-5)]
    G=[[diag[0],a12,a13],[a12,diag[1],a23],[a13,a23,diag[2]]]
    return G,[sum(row)for row in G]


def cap_bound(v,lam):
    parameters(v,lam);return max(comparison_data(v,lam)[1])


def cap_gap(v,lam):
    delta=parameters(v,lam)[4]-cap_bound(v,lam)
    g=F((v-1)*(v-2)*(v-3),4*v);assert delta>g>0
    return delta


def centered_certificate(v,lam,blocks):
    parameters(v,lam);return ordinary_centered(v,lam,blocks)


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    parameters(v,lam)
    if eta is None:eta=F(1,8*v*v)
    return ordinary_maximal(v,lam,blocks,centered,eta)


def fixtures():
    v=21;lam=4
    seeds=[(0,1,2),(0,1,3),(0,1,19),(0,2,6),(0,4,9),(0,5,10),
        (0,5,11),(0,3,12),(0,4,12),(0,6,13),(0,6,14),(0,3,11),(0,4,11),(0,7,14)]
    blocks=sorted({mask((x+j)%v for x in seed)for seed in seeds for j in range(v)})
    yield 'cyclic_fourfold21',v,lam,blocks,{
        'modulus':v,'seeds':[list(p)for p in seeds],
        'interpretation':'Fixed first-witness cyclic simple fourfold design; no design novelty or exhaustive cohort claim.'}
