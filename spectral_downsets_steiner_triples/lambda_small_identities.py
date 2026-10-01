"""Portable exact certificates extending the ordinary H proof to all orders.

Generic quadrant v>=7,l>=2; Schur margin splits integer l=2 from l>=3.
The only feasible v=5,6 cases are checked over Fraction, including the
two singular free parameters. No CAS, sampling or polynomial GCD.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from bivariate_certificates import RF,poly,terms
from lambda_identities import run as previous_identities
from uniform_lambda_small import parameters,weights


def shifted(p,v0=7,l0=2):
    out={}
    for (pv,pl),c in p.items():
        for i in range(pv+1):
            for j in range(pl+1):
                key=(i,j)
                out[key]=out.get(key,F(0))+c*comb(pv,i)*v0**(pv-i)*comb(pl,j)*l0**(pl-j)
    return poly(out)


def certificate(expr,v0=7,l0=2,weak=False):
    num,den=shifted(expr.n,v0,l0),shifted(expr.d,v0,l0)
    assert den.get((0,0),F(0))>0 and all(z>=0 for z in den.values())
    assert all(z>=0 for z in num.values())
    assert num.get((0,0),F(0))>=0 if weak else num.get((0,0),F(0))>0
    serial=json.dumps([terms(num),terms(den)],separators=(',',':'))
    return {'v_shift':v0,'l_shift':l0,'num_terms':len(num),'den_terms':len(den),
            'num_constant':str(num.get((0,0),F(0))),'den_constant':str(den[(0,0)]),
            'coefficient_sha256':sha256(serial.encode()).hexdigest()}


def finite_equations(v,l,tau):
    m,b,r,s,N=parameters(v,l);u=F(l*(l-1),2)
    z=weights(v,l);a,c,d=z['a'],z['c'],z['d']
    w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*tau
    return [h+(v-4)*d+(r-3*l)*tau-s,
        1+s+(v-3)*h-3*(l-1)*tau+F((v-3)*(v-4),2)*d+(b-3*r+3*l-1)*tau-N,
        w+(v-3)*c+(r-2*l)*d-s,
        1+s+(v-2)*w-l*d+F((v-2)*(v-3),2)*c+(b-2*r+l)*d-N,
        a+(v-2)*w-l*d+(r-l)*h-3*u*tau-s,
        1+s+(v-1)*a+F((v-1)*(v-2),2)*w-r*d+(b-r)*h-(l-1)*r*tau-N,
        s+c-2*c*(v-1)+(c-1)*m-F(4*l,3),
        l*d-2*d*r+(d-1)*b+F(2*l,3),
        s+(3*l-1)*tau-3*r*tau+(tau-1)*b-1]


def run():
    prior=previous_identities()
    assert prior['zero_identities']==27 and len(prior['strict_certificates'])==30
    v,l=RF({(1,0):1}),RF({(0,1):1})
    r=l*(v-1)/2;s=v+r
    D=l*(v*v-10*v+27)-6;E=3*l*v*v-3*l*v-16*l+6*v
    c=(v*v-(l+3)*v+11*l/3)/((v-2)*(v-3))
    d=(v*v-v-4)/((v-4)*(v-3))
    t=(v-1)*(l*(v-3)-6)/D
    alpha1=E/(6*(v-2));alpha2=s+c
    red=t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu=s-t-(r-l)*red;A=(r-l)*d*d*(v-4)**2/(v-2)
    P=(l**4*(3*v**5-15*v**4+5*v**3+55*v*v-48*v)
       +l**3*(-19*v**5+127*v**4-203*v**3-235*v*v+618*v)
       +l*l*(3*v**6-12*v**5-68*v**4+438*v**3-223*v*v-2034*v+2592)
       +l*(-6*v**5+108*v**4-642*v**3+1452*v*v-816*v-576)
       +36*v**3-180*v*v+216*v)
    assert (s-c*(v-3)-alpha1).is_zero()
    assert (mu-1/l-P/(l*(v-3)*(v-2)*D*E)).is_zero()
    mu2=v*(3*v**3-13*v*v+32)/((v-3)*(v-2)*(3*v*v-16))
    margin2=2*(v-4)*(v*v+3*v-12)/((v-3)*(v-2)*(3*v*v-16))
    assert (mu.substitute_l(2)-mu2).is_zero()
    assert (mu2-1-margin2).is_zero()
    strict={
        'D_positive':D,'E_positive':E,'alpha1_gt_lv_over_2':alpha1-l*v/2,
        'A_lt_2lv2':2*l*v*v-A,'t_gt_1':t-1,'d_positive':d,
        'c_legal_lower':(8*v-22)/(3*(v-2)*(v-3)),
        'beta_lower_positive':1-RF(F(361,36))/(2*v-1)}
    records={name:certificate(expr) for name,expr in strict.items()}
    records['l2_mu_gt_1']=certificate(margin2)
    records['l3plus_Schur_P_positive']=certificate(P,l0=3)
    weak={'d_le_19_over_6':certificate(RF(F(19,6))-d,weak=True),
          's_ge_2v_minus1':certificate(s-(2*v-1),weak=True)}
    finite=[]
    for vv,ll in ((5,3),(6,2),(6,4)):
        z=weights(vv,ll);aa1=parameters(vv,ll)[3]-z['c']*(vv-3)
        aa2=parameters(vv,ll)[3]+z['c'];dd,tt=z['d'],z['t']
        bb=tt-dd*dd/aa2
        rr=tt*F(vv-6,vv-2)+dd*dd*F((vv-4)**2,vv-2)/aa1
        mm=parameters(vv,ll)[3]-tt-(F(ll*(vv-1),2)-ll)*rr
        AA=(F(ll*(vv-1),2)-ll)*dd*dd*F((vv-4)**2,vv-2)
        assert aa1>F(ll*vv,2) and aa2>0 and bb>0 and rr>0 and mm>F(1,ll)
        assert AA<2*ll*vv*vv and all(eq==0 for eq in finite_equations(vv,ll,tt))
        free=(vv,ll) in ((5,3),(6,2))
        if free:
            # All nine equations are affine in tau: vanishing at0,1 proves
            # the singular equations impose no restriction on that parameter.
            assert all(eq==0 for tau in (F(0),F(1)) for eq in finite_equations(vv,ll,tau))
        finite.append({'v':vv,'lambda':ll,'weights':{key:str(val) for key,val in z.items()},
            'alpha1':str(aa1),'alpha2':str(aa2),'beta':str(bb),'red':str(rr),
            'mu':str(mm),'A':str(AA),'zero_identities':9,'singular_free_parameter':free})
    table=terms(shifted(P.n,l0=3))
    assert len(table)==33 and shifted(P.n,l0=3)[(0,0)]==89136
    return {'agent':'six-downset-2','role':'researcher','arithmetic':'Q(v,l) sparse Fraction polynomials; finite Fraction substitution',
        'inherited_generic_zero_identities':prior['zero_identities'],'new_generic_zero_identities':4,
        'base_domain':'v=7+x,l=2+y; x,y>=0','Schur_domain':'l=2 or v=7+x,l=3+y; x,y>=0',
        'strict_certificates':records,'weak_certificates':weak,'finite':finite,
        'Schur_P_shifted_coefficients':table,
        'Schur_denominator_factors':['l','v-3','v-2','D=l(v^2-10v+27)-6','E=3lv^2-3lv-16l+6v']}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
