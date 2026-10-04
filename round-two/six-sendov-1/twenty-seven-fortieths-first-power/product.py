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
         'gap-product-last-coefficient','gap-polar-lipschitz','gap-origin-lipschitz')

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

def gap_payment(kernel,damage=''):
    lo,hi=kernel.LOW,kernel.H;eps=Q(1,2**25)
    bplus=1-lo**2;m=1/(1+hi)
    LJ=bplus/2*(hi+bplus*(8+eps)/7)**7
    LO=9*hi/2*(1+hi*(8+eps)/7)**7
    if damage=='gap-polar-lipschitz':LJ*=Q(999,1000)
    if damage=='gap-origin-lipschitz':LO*=Q(999,1000)
    jpol=kernel.power([hi,bplus/7],7);opol=kernel.power([Q(1),hi/7],7)
    jdirect=sum((comb(7,k)*hi**(7-k)*(bplus/7)**k*(8+eps)**k for k in range(8)),Q(0))
    odirect=sum((comb(7,k)*(hi/7)**k*(8+eps)**k for k in range(8)),Q(0))
    kernel.require(jpol==[comb(7,k)*hi**(7-k)*(bplus/7)**k for k in range(8)]
                   and LJ==bplus*jdirect/2 and LJ<2,
                   'whole fresh J Lipschitz endpoint payment')
    kernel.require(opol==[comb(7,k)*(hi/7)**k for k in range(8)]
                   and LO==9*hi*odirect/2 and LO<171,
                   'whole fresh O Lipschitz endpoint payment')
    ratio_coefficients=kernel.power([Q(1),1/(8*m)],8)
    if damage=='gap-product-last-coefficient':ratio_coefficients[-1]=Q(0)
    alternate=[comb(8,k)/(8*m)**k for k in range(9)]
    kernel.require(len(ratio_coefficients)==9 and ratio_coefficients==alternate,
                   'ALL9 clipping product ratio coefficients')
    ratio=sum((x*eps**k for k,x in enumerate(ratio_coefficients)),Q(0))
    kernel.require(ratio==(1+eps/(8*m))**8,'whole clipping eighth-power evaluation')
    product_loss=ratio-1+171*eps;polar_loss=2*eps
    kernel.require(product_loss<kernel.PRODUCT_MARGIN and polar_loss<1-kernel.POLAR_TARGET
                   and 1-polar_loss>kernel.ENTRY_TARGET,
                   'whole strict annular channel and entry gaps')
    return kernel.clean(dict(marked_interval=[lo,hi],epsilon=eps,floor=m,
        J_Lipschitz_coefficients=jpol,O_Lipschitz_coefficients=opol,
        J_Lipschitz_exact=LJ,O_Lipschitz_exact=LO,J_Lipschitz_upper=Q(2),O_Lipschitz_upper=Q(171),
        all9_clipped_product_ratio_coefficients=ratio_coefficients,
        full_eighth_power=ratio,product_ratio_loss=ratio-1,
        O_minus_clipped_product_loss_upper=product_loss,J_loss_upper=polar_loss,
        strict_product_margin=kernel.PRODUCT_MARGIN,polar_target=kernel.POLAR_TARGET,
        origin_target=kernel.ORIGIN_TARGET,entry_target=kernel.ENTRY_TARGET,
        floor_preserved=True,clipped_actual_tuple_feasibility_asserted=False,
        whole_lower_disk_numeric_gap_asserted=False,
        ordinary_inputs='floor-preserving radial clipping; full eight-factor communication '
                        'and seven-factor Lipschitz; full product-ratio AM-GM; entire closed cover',
        formalized=False,independent_review=False))
