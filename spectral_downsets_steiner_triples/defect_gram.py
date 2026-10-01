"""Completion-defect Gram cap criterion for the reviewed triple-design matrix.

Any existing simple2-(v,3,lambda),v>=7,lambda>=2. The theorem allows
gamma K_v-Z PSD; this constructor verifies the sufficient absolute-row
bound instead. Neither a scalar comparison nor failed bound alone decides
H feasibility. DEFECT_GRAM_CAP.md gives the full ordinary bridge.
six-downset-2, researcher. Standard library; assertions enabled.
"""
from fractions import Fraction as F
from math import isqrt
from uniform_lambda_small import parameters as ordinary_parameters, weights
from uniform_lambda_small import design_data
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal


def parameters(v,lam):
    data=ordinary_parameters(v,lam);assert v>=7
    return data


def strict_root_upper(q):
    """Smallest positive integer strictly above sqrt of a nonnegative rational."""
    q=F(q);assert q>=0
    z=F(isqrt(q.numerator//q.denominator)+1)
    assert z>0 and z*z>q
    return z


def scalar_data(v,lam,gamma):
    """Conditional scalar comparison; the Z bound is a separate hypothesis."""
    m,b,r,s,N=parameters(v,lam);gamma=F(gamma);assert gamma>=0
    ww=weights(v,lam);c,d,t,w,h=[ww[k]for k in ('c','d','t','w','h')]
    assert c>0 and d>0 and t>0 and h>0
    u=F(lam*(lam-1),2)
    mu12=w*w*(v-2)+d*d*(r-u)-2*w*d*lam
    nu12=w*w+d*d*u+2*w*d*lam
    alphaH=(v-5)*r-(v-6)*u+3*lam*lam-lam
    betaH=(v-6)*u+lam*lam*(v-4)+lam
    mu13=h*h*(r-lam)-6*h*t*u+t*t*alphaH
    zcoef13=2*h*t+t*t*(v-6)
    nu13=h*h*lam+6*h*t*u+t*t*betaH
    assert zcoef13>0
    rho12=mu12+d*d*gamma
    rho13=mu13+zcoef13*gamma
    rho23=d*d*F((v-4)**2*(2*v-6),4)
    assert rho12>=0 and rho13>=0
    a12,a13,a23=[strict_root_upper(z)for z in (rho12,rho13,rho23)]
    diagonal=[s+F(lam,3)+t*gamma,s+c,s+t*(v-5)]
    G=[[diagonal[0],a12,a13],[a12,diagonal[1],a23],[a13,a23,diagonal[2]]]
    rows=[sum(row)for row in G];bound=max(rows);delta=N-bound
    g=F((v-1)*(v-2)*(v-3),4*v)
    return {'v':v,'lambda':lam,'m':m,'b':b,'r':r,'s':s,'N':N,'gamma':gamma,
        'u':u,'mu12':mu12,'nu12':nu12,'alphaH':alphaH,'betaH':betaH,
        'mu13':mu13,'zcoef13':zcoef13,'nu13':nu13,
        'rho':[rho12,rho13,rho23],'crosses':[a12,a13,a23],
        'root_square_margins':[a12*a12-rho12,a13*a13-rho13,a23*a23-rho23],
        'diagonal':diagonal,'G':G,'rows':rows,'B':bound,'delta':delta,'g':g,
        'delta_minus_g':delta-g,'half_gap_margin':(delta-g)/2,
        'whole_interval_sufficient':delta>g>0}


def row_defect_data(v,lam,blocks,gamma):
    """Validate the design and sufficient full-row completion-defect bound."""
    parameters(v,lam);_,_,codegrees,_=design_data(v,lam,blocks)
    u=lam*(lam-1)//2
    Z=[[0 if x==y else codegrees[(1<<x)|(1<<y)]-u for y in range(v)]for x in range(v)]
    assert all(sum(row)==0 for row in Z)
    actual=max(sum(abs(z)for z in row)for row in Z)
    assert F(gamma)>=actual,'Absolute-row defect certificate exceeds the supplied bound'
    data=scalar_data(v,lam,gamma)
    assert data['whole_interval_sufficient'],'Conditional row cap did not establish the full repair interval'
    return data,Z,actual


def centered_certificate(v,lam,blocks,gamma=28):
    row_defect_data(v,lam,blocks,gamma)
    return ordinary_centered(v,lam,blocks)


def maximal_certificate(v,lam,blocks,centered=None,eta=None,gamma=28):
    row_defect_data(v,lam,blocks,gamma)
    if eta is None:eta=F(1,8*v*v)
    return ordinary_maximal(v,lam,blocks,centered,eta)


def compact_scalars(data):
    keys=('gamma','mu12','nu12','alphaH','betaH','mu13','zcoef13','nu13',
          'rho','crosses','root_square_margins','diagonal','rows','B','delta',
          'g','delta_minus_g','half_gap_margin')
    return {k:[str(x)for x in data[k]]if isinstance(data[k],list)else str(data[k])for k in keys}
