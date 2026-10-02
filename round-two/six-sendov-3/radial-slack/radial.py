"""Whole-box radial Jacobian and individual-root objective multipliers.

The interpretation as actual original-root coordinates is an ordinary analytic
bridge in PROOF.md. Hash-bound arithmetic is reused from9225/9164, unchanged.
"""
from pathlib import Path
from fractions import Fraction as F
import sys

SIBLING=Path(__file__).resolve().parent.parent/'complex-sector'
sys.path.insert(0,str(SIBLING))
from sector import cpow,K,I,C,exact,embedding,enclose,require


def certificate(damage=None):
    values,_,_,_,_=exact();c=embedding()
    box=[enclose(v,c)+I.bounds(-F(1,1024),F(1,1024)) for v in values]
    eta=I.bounds(0,F(1,65536));x,y,T,xi3,xi4,omega=box
    r=eta*x;s=eta*y;A=1-eta-r;D=1-eta-s;W=1+eta*omega;Delta=r-s
    require(all(v.lo>0 for v in (A,D,W,T)),'positive distance and opening domains')
    even=[];odd=[];sines=[];denominators=[]
    for t in (-I(F(1,2))+eta*xi3,-c+eta*xi4):
        sine=(1-t.square()).sqrt();z=C(t,sine);X=z-r
        pz=9*cpow(X,6)*(cpow(z-s,2)+eta*T)
        qy=-F(9,4)*(cpow(X,8)-A**8)+(cpow(X,7)-A**7)*(-F(18,7)*Delta)
        qT=F(9,7)*(cpow(X,7)-A**7)
        qV=-F(9,8)*(cpow(X,8)-A**8)+(cpow(X,7)-A**7)*(-F(9,7)*(r-2*s))
        qM=-F(9,7)*(cpow(X,7)-A**7)
        even.append([-(q/(z*pz)).re for q in (qy,qT)])
        odd.append([(q/(z*pz)).im/sine for q in (qV,qM)])
        denominator=z*pz
        denominator_norm=denominator.re.square()+denominator.im.square()
        require(sine.lo>I(F(1,4)).hi and denominator_norm.lo>0,'sine and original-root derivative domains')
        sines.append(sine);denominators.append(denominator_norm)
    if damage=='even-normal-sign':even[0][0]=-even[0][0]
    if damage=='odd-normal-sign':odd[0][0]=-odd[0][0]
    det=lambda a:a[0][0]*a[1][1]-a[0][1]*a[1][0]
    detE,detO=det(even),det(odd)
    require(detE.lo>I(F(1,16)).hi,'divided even-radial determinant above1/16')
    require(detO.hi<I(-F(1,100)).lo,'divided odd-radial determinant below-minus1/100')
    # Rows of the actual four-root normal map are upper3,upper4,lower3,lower4.
    full_normalized=4*detE*detO*sines[0]*sines[1]
    require(full_normalized.hi<I(-F(1,6400)).lo,'full signed radial determinant div eta5 below-minus1/6400')
    rhs=[-D/W**3,1/(2*W**3)]
    if damage=='objective-pair-factor':rhs=[2*v for v in rhs]
    mu=[(rhs[0]*even[1][1]-even[1][0]*rhs[1])/detE,
        (even[0][0]*rhs[1]-rhs[0]*even[0][1])/detE]
    require(all(v.lo>I(F(1,4)).hi and v.hi<I(3).lo for v in mu),'all individual original-root multipliers in(1/4,3)')
    cc=K((0,1,0));dd=2*cc*cc-1
    E0=[[K(-F(3,8)),K(F(3,14))],[-(1+cc)/4,(1-dd)/7]]
    O0=[[K(F(1,8)),K(-F(1,7))],[K(F(1,8)),-2*cc/7]]
    de0,do0=det(E0),det(O0)
    require(de0==3*(cc+dd)/56 and do0==(1-2*cc)/56,'both exact initial determinants')
    mu0=[(-E0[1][1]-E0[1][0]/2)/de0,(E0[0][0]/2+E0[0][1])/de0]
    require(mu0==[K((F(26,9),-F(2,9),-F(4,9))),K((-F(1,3),F(2,3),0))],
            'initial individual weights agree with credited8921 half-duals')
    require(all(sum((E0[k][j]*mu0[k] for k in range(2)),K(0))==(-1 if j==0 else F(1,2)) for j in range(2)),
            'both initial individual-root dual equations')
    return {'agent':'six-sendov-3','role':'researcher','status':'exact whole-box certificate; ordinary analytic bridges in PROOF.md',
            'eta_max':'1/65536','cube_radius':'1/1024','even_radial_div_eta':[[v.record() for v in row] for row in even],
            'odd_radial_div_eta3half_sine':[[v.record() for v in row] for row in odd],
            'even_determinant':detE.record(),'odd_determinant':detO.record(),
            'upper_root_sines':[v.record() for v in sines],
            'original_root_derivative_norm_squared':[v.record() for v in denominators],
            'signed_four_radial_determinant_div_eta5':full_normalized.record(),
            'individual_root_dual_rhs':[v.record() for v in rhs],
            'individual_root_multipliers':[v.record() for v in mu],
            'initial_even_radial':[[v.record() for v in row] for row in E0],
            'initial_odd_radial':[[v.record() for v in row] for row in O0],
            'initial_individual_root_multipliers':[v.record() for v in mu0],
            'radial_metric':'alpha_k_plus/minus=(|Z_k_plus/minus|^2-1)/2',
            'gradient_at_branch':'dF/dalpha_k_plus=dF/dalpha_k_minus=-mu_k in(-3,-1/4)',
            'native_threads':1,'math_jobs':1}
