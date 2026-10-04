"""PRIVATE successor: same-author adaptation of LEMMA10322/source d8eb0d1b908151a1ad1a67c92238860f9fbaf3d4.
Published contour prior art: Roos1203.2871 Lemma2.2; Han--Niles-Weed2408.09341 Theorem4.3(1),2607.23836 section1.1.
Unformalized and independently unreviewed; no new radius from this module alone.
"""
"""Exact payments for actual origin products and the annular clipping gap.

The logarithm, zero-sum Cauchy, exponential and clipping arguments are
ordinary mathematics in PROOF.md; these rational checks pay their inputs.
No ancestor, private record, reviewer program or sampled search is used.
"""
from fractions import Fraction as Q
from math import comb, factorial

DAMAGES=('product-floor-endpoint','product-F-endpoint',
         'product-variance-endpoint','product-root-underpay','product-log-last',
         'product-exp-drop-fourth','product-exp-sign',
         )

def payment(kernel,tight,radial,damage=''):
    al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight)
    tl,th=map(Q,radial)
    kernel.require(0<al<=ah<1 and 0<fl<=fh<=8 and 0<=tl<=th,
                   'whole actual radial-product domain')
    m=1/(1+ah)
    if damage=='product-floor-endpoint':m=1/(1+al)
    kernel.require(m*(1+ah)==1,'whole per-box floor endpoint')
    sum_cap=fh-7*m
    if damage=='product-F-endpoint':sum_cap=fl-7*m
    kernel.require(sum_cap+7*m==fh,'whole radius sum upper endpoint')
    variance_cap=th-(8-fh)**2/8
    if damage=='product-variance-endpoint':variance_cap=th-(8-fl)**2/8
    kernel.require(variance_cap==th-8+2*fh-fh**2/8 and variance_cap>=0,
                   'whole centered variance upper endpoint')
    root_cap=kernel.ceiling(Q(7,8)*variance_cap,4096)
    if damage=='product-root-underpay':root_cap-=Q(1,4096)
    kernel.require(root_cap>=0 and root_cap**2>=Q(7,8)*variance_cap,
                   'whole centered coordinate square-root payment')
    centered_cap=fh/8+root_cap
    radius=max(Q(1),min(sum_cap,centered_cap))
    kernel.require(centered_cap-fh/8==root_cap and sum_cap>0,
                   'whole independent radius caps')
    derivative=[-radius,radius+1,Q(-1)]
    if damage=='product-log-last':derivative[-1]+=Q(1,1000)
    factored=kernel.mul([Q(-1),Q(1)],[radius,Q(-1)])
    kernel.require(derivative==factored,'whole logarithmic derivative coefficient identity')
    z=8-fh+tl/(2*radius)
    if damage=='product-exp-sign' and z>0:z=-z
    kernel.require(radius>=1 and z>=0,'whole logarithmic and exponential comparison signs')
    terms=[z**j/factorial(j) for j in range(5)]
    if damage=='product-exp-drop-fourth' and z>0:terms[-1]=Q(0)
    denominator=sum(terms,Q(0))
    horner=Q(1,24)
    for j in (3,2,1,0):horner=Q(1,factorial(j))+z*horner
    kernel.require(horner==denominator and denominator>=1,
                   'ALL FIVE positive exponential terms and Horner payment')
    return kernel.clean(dict(status='bounded-actual-origin-product',
        marked_interval=[al,ah],F=[fl,fh],T=[tl,th],per_a_floor=m,
        sum_radius_cap=sum_cap,centered_variance_cap=variance_cap,
        centered_coordinate_root_upper=root_cap,centered_radius_cap=centered_cap,R_upper=radius,
        full_logarithmic_derivative_coefficients=derivative,z_lower=z,
        exponential_terms=terms,exponential_denominator=denominator,horner_denominator=horner,
        actual_origin_product_upper=1/denominator,
        ordinary_inputs='logarithmic derivative signs on(0,R], zero-sum radial Cauchy, '
                        'exp(z)>=all five terms; |O|<=product of actual radii',
        no_converse_to_original_root_feasibility=True))
