"""Standalone CLOSED[7/10,29/40] exact coupled kernels.
Own c1cf4584119f20ac6c6447541429eaa6717e48de method provenance; no ancestor, peer, reviewer or discovery corpus runtime input.
Unformalized and independently unreviewed; ordinary proof/trust in PROOF.md.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import datetime
import json
import resource
import time


HERE=Path(__file__).resolve().parent
EPS=Q(1,10000)


def need(condition,message):
    if not condition:raise ValueError(message)


def multiply(a,b):
    result=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return result


def payment(damage=''):
    lo,hi,b,m=Q(7,10),Q(29,40),Q(51,100),Q(40,69)
    if damage=='floor-endpoint':m=1/(1+lo)
    need(m*(1+hi)==1,'actual smallest radius floor endpoint')
    S=8+EPS; R=S-7*m
    if damage=='radius-seven-floors':R=S-8*m
    need(R+7*m==S,'all seven other radius floors')
    sigma=(S-m)/7
    if damage=='J-omit-differentiated-floor':sigma=(S-m)/8
    need(7*sigma+m==S,'exact seven-factor mass excluding differentiated slot')
    jterms=[b*comb(7,k)*hi**(7-k)*(b*sigma)**k/Q(k+2) for k in range(8)]
    if damage=='J-integral-denominator':jterms[-1]*=Q(9,10)
    # Different representation: exact antiderivative after x=hi+b*sigma*t.
    d=b*sigma
    jint=b*((hi+d)**9/9-hi*(hi+d)**8/8+hi**9/72)/d**2
    LJ=sum(jterms,Q(0))
    need(LJ==jint,'all eight J derivative integrals and antiderivative')
    jc=Q(2,3)
    if damage=='J-underpaid-bound':jc=Q(1,2)
    need(LJ<jc,'fresh J Lipschitz bound')
    energy=Q(23,5); base_u=1-energy/16
    need(base_u==Q(57,80),'fresh energy-derived mean floor')
    u=base_u-EPS/8
    e=energy+2*(R+1)*EPS
    if damage=='E-path-underpayment':e=energy+(R+1)*EPS
    need(e-energy==2*(R+1)*EPS,'whole squared-norm path loss')
    if damage=='mean-path-underpayment':u=base_u-EPS/16
    need(base_u-u==EPS/8 and u>0,'whole real mean path loss')
    A=e+16*u-8
    need(A==8+2*R*EPS and A>0,'complete mean-energy compensation')
    B=[Q(8,7),-16*lo*u/7,hi**2*A/7]
    if damage=='O-missing-slot-square':B[0]=Q(1)
    if damage=='O-linear-marked-endpoint':B[1]=-16*hi*u/7
    need(B==[Q(8,7),-16*lo*u/7,hi**2*A/7],
         'full squared-modulus AM-GM coefficients and marked endpoints')
    slot=[Q(0),Q(2),Q(-1)]
    if damage=='slot-square-coefficient':slot[-1]=Q(0)
    squared=multiply([Q(1),Q(-1)],[Q(1),Q(-1)])
    need(slot==[Q(1)-squared[0],-squared[1],-squared[2]],
         'whole removed-slot nonpositive-square identity')
    lower_controls=[B[0],B[0]+B[1]/2,sum(B,Q(0))]
    reconstructed=[lower_controls[0],2*(lower_controls[1]-lower_controls[0]),
                   lower_controls[0]-2*lower_controls[1]+lower_controls[2]]
    need(reconstructed==B and min(lower_controls)>0 and B[2]>0
         and sum(B,Q(0))<=B[0],
         'whole positive convex quadratic majorant and maximum endpoint')
    norm=Q(107,100)
    if damage=='O-drop-odd-norm-factor':norm=Q(1)
    need(norm>=0 and norm**2>=Q(8,7),'full seventh-product odd norm factor')
    coefficients=multiply(B,multiply(B,B))
    if damage=='O-drop-last-cubic-coefficient':coefficients[-1]=Q(0)
    alternate=[Q(0)]*7
    for j in range(4):
        for k in range(4-j):
            n=3-j-k
            alternate[j+2*k]+=Q(factorial(3),factorial(j)*factorial(k)*factorial(n))*B[0]**n*B[1]**j*B[2]**k
    need(len(coefficients)==7 and coefficients==alternate,
         'all seven cubic majorant coefficients by two representations')
    weights=[Q(1,k+2) for k in range(7)]
    if damage=='O-weighted-integral-underpayment':weights[-1]=Q(1,9)
    area=sum((c*w for c,w in zip(coefficients,weights)),Q(0))
    need(area==sum((c/Q(k+2) for k,c in enumerate(alternate)),Q(0)) and area>0,
         'entire weighted cubic integral with all signed coefficients')
    LO=9*hi*norm*area; oc=Q(5,4)
    if damage=='O-underpaid-bound':oc=Q(1)
    need(LO<oc,'fresh coupled origin Lipschitz bound')
    coeff=[comb(8,k)/(8*m)**k for k in range(9)]
    if damage=='ratio-last-coefficient':coeff[-1]=Q(0)
    literal=[Q(1)]
    for _ in range(8):literal=multiply(literal,[Q(1),1/(8*m)])
    need(coeff==literal,'all nine clipping product ratio coefficients')
    ratio=sum((c*EPS**k for k,c in enumerate(coeff)),Q(0))
    need(ratio==(1+EPS/(8*m))**8,'complete clipping eighth power')
    origin_loss=ratio-1+oc*EPS;polar_loss=jc*EPS
    need(origin_loss<Q(1,3100) and polar_loss<Q(1,2200)
         and 1-polar_loss>Q(2199,2200),'full entry and face channel losses')
    return dict(epsilon=EPS,floor=m,total_mass_upper=S,radius_upper=R,
        other_seven_mean_radius_upper=sigma,
        full_J_integral_terms=jterms,J_antiderivative=jint,J_exact=LJ,J_upper=jc,
        path_real_mean_lower=u,path_energy_upper=e,mean_energy_compensation=A,
        all_quadratic_majorant_coefficients=B,quadratic_endpoint=sum(B,Q(0)),
        quadratic_maximum=Q(8,7),quadratic_endpoint_derivative=B[1]+2*B[2],
        all_positive_quadratic_Bernstein_controls=lower_controls,
        all_reconstructed_quadratic_coefficients=reconstructed,
        removed_slot_square_coefficients=slot,odd_product_norm_upper=norm,
        all_cubic_majorant_coefficients=coefficients,all_weighted_integral_weights=weights,
        whole_weighted_cubic_integral=area,O_exact=LO,O_upper=oc,
        all_eighth_power_coefficients=coeff,entire_product_ratio=ratio,
        origin_product_loss=origin_loss,polar_loss=polar_loss,
        origin_margin=Q(1,3100),polar_margin=Q(1,2200),entry_target=Q(2199,2200))


DAMAGES=(('floor-endpoint','floor endpoint'),
 ('radius-seven-floors','other radius floors'),
 ('J-omit-differentiated-floor','excluding differentiated slot'),
 ('J-integral-denominator','derivative integrals'),
 ('J-underpaid-bound','J Lipschitz'),
 ('E-path-underpayment','squared-norm path'),
 ('mean-path-underpayment','mean path'),
 ('O-missing-slot-square','AM-GM coefficients'),
 ('O-linear-marked-endpoint','AM-GM coefficients'),
 ('slot-square-coefficient','removed-slot'),
 ('O-drop-odd-norm-factor','odd norm factor'),
 ('O-drop-last-cubic-coefficient','cubic majorant coefficients'),
 ('O-weighted-integral-underpayment','weighted cubic integral'),
 ('O-underpaid-bound','origin Lipschitz'),
 ('ratio-last-coefficient','ratio coefficients'))


def clean(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list):return [clean(v) for v in x]
    return x
