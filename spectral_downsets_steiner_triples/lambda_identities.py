"""Portable Q(v,l) identities and two-variable strict sign certificates.

Base domain v>=13,l>=2. Cap domain v>=24l,l>=2. These are scalar
certificates; UNIFORM_LAMBDA_PROOF.md supplies every incidence/PSD bridge.
CPython3.11+ standard library, assertions enabled. six-downset-2, researcher.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from bivariate_certificates import RF,positive,terms


def run():
    v,l=RF({(1,0):1}),RF({(0,1):1})
    m,b,r,u=v*(v-1)/2,l*v*(v-1)/6,l*(v-1)/2,l*(l-1)/2
    s,N=v+r,1+v+m+b
    D=l*(v*v-10*v+27)-6
    E=3*l*v*v-3*l*v-16*l+6*v
    a=-l/3
    c=(v*v-(l+3)*v+11*l/3)/((v-2)*(v-3))
    d=(v*v-v-4)/((v-4)*(v-3))
    t=(v-1)*(l*(v-3)-6)/D
    w=(l*v*v+11*l*v-36*l+3*v**3-21*v*v+36*v)/(3*(v-4)*(v-3)*(v-2))
    h=(3*l*l*(v-1)*(v-3)+l*(v**3-12*v*v+11*v+36)+12*v-24)/((v-3)*D)
    alpha1=E/(6*(v-2));alpha2=s+c
    beta=t-d*d/alpha2
    gamma=t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    red=t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu=s-t-(r-l)*red
    P=(l**4*(3*v**5-15*v**4+5*v**3+55*v*v-48*v)
       +l**3*(-19*v**5+127*v**4-203*v**3-235*v*v+618*v)
       +l*l*(3*v**6-12*v**5-68*v**4+438*v**3-223*v*v-2034*v+2592)
       +l*(-6*v**5+108*v**4-642*v**3+1452*v*v-816*v-576)
       +36*v**3-180*v*v+216*v)
    A=(r-l)*d*d*(v-4)**2/(v-2)
    eqs={
        'triple_star':h+(v-4)*d+(r-3*l)*t-s,
        'triple_row':1+s+(v-3)*h-3*(l-1)*t+(v-3)*(v-4)*d/2+(b-3*r+3*l-1)*t-N,
        'pair_star':w+(v-3)*c+(r-2*l)*d-s,
        'pair_row':1+s+(v-2)*w-l*d+(v-2)*(v-3)*c/2+(b-2*r+l)*d-N,
        'point_star':a+(v-2)*w-l*d+(r-l)*h-3*u*t-s,
        'point_row':1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-(l-1)*r*t-N,
        'constant_pair':s+c-2*c*(v-1)+(c-1)*m-4*l/3,
        'constant_cross':l*d-2*d*r+(d-1)*b+2*l/3,
        'constant_triple':s+(3*l-1)*t-3*r*t+(t-1)*b-1,
        'constant_trace':s-a+(a-1)*v+4*l/3+1-(l*(v+7)/6+1),
        'alpha1':s-c*(v-3)-alpha1,
        'Schur_reduction':gamma-4*beta/(v-2)-red,
        'Schur_margin':mu-1/l-P/(l*(v-3)*(v-2)*D*E),
        'density':N-2*s-(v-1)*((v-2)/2+l*(v-6)/6),
        'point_triple_norm_scalar':F(3,2)+F(5,3)*(l-1)-(5*l/3-RF(F(1,6))),
    }
    # Exact regression against the previously proved centered formulas.
    old2={'a':RF(F(-2,3)), 'w':1+4*v*(2*v-5)/(3*(v-2)*(v-3)*(v-4)),
          'c':1+4/(3*(v-2)*(v-3)), 'd':d, 'h':(v*v-7)/((v-3)*(v-4)), 't':(v-1)/(v-4)}
    old3={'a':RF(-1),'w':(v**3-6*v*v+23*v-36)/((v-4)*(v-3)*(v-2)),
          'c':(v*v-6*v+11)/((v-3)*(v-2)), 'd':d,
          'h':(v*v+2*v-11)/((v-5)*(v-3)), 't':(v-1)/(v-5)}
    for ll,old in ((2,old2),(3,old3)):
        for key,new in {'a':a,'w':w,'c':c,'d':d,'h':h,'t':t}.items():
            eqs['degree'+str(ll)+'_'+key]=new.substitute_l(ll)-old[key]
    for name,eq in eqs.items():assert eq.is_zero(),name
    base={'D_positive':D,'E_positive':E,'Schur_P_positive':P,
          'alpha1_gt_lv_over_2':alpha1-l*v/2,'alpha2_gt_v':alpha2-v,
          't_gt_1':t-1,'t_lt_2':2-t,'d_positive':d,'d_lt_2':2-d,
          'w_positive':w,'h_positive':h,'A_lt_2lv2':2*l*v*v-A,
          'c_lt_4_over_3':RF(F(4,3))-c,'beta_comparison_positive':v-4,
          'repair_comparison_positive':v-2,
          'c_lower_from_simplicity':(8*v-22)/(3*(v-2)*(v-3))}
    cap={'w_lt_3_over_2':RF(F(3,2))-w,'d_lt_3_over_2':RF(F(3,2))-d,
         'h_lt_2':2-h,'t_lt_4_over_3':RF(F(4,3))-t,
         'diag1_lt_l2v':l*l*v-(s+l/3+RF(F(4,3))*u*v),
         'diag2_lt_l2v':l*l*v-(s+RF(F(4,3))),
         'diag3_lt_l2v':l*l*v-(s+RF(F(4,3))*(3*l-1)),
         'constant_lt_2l2v':2*l*l*v-(l*(v+7)/6+1),
         'gap_gt_v2_over_4':N-2*l*l*v-v*v/4,
         'pair_cross_comparison':l*l-l-1,
         'point_triple_cross_comparison':3*l-5,
         'pair_triple_cross_comparison':2*l-3,
         'sqrtv_rational_comparison':v-36,'sqrtlv_rational_comparison':v-16*l}
    records={}
    for domain,collection in (('base',base),('cap',cap)):
        for name,expr in collection.items():
            shifted_n=positive(expr.n,domain);shifted_d=positive(expr.d,domain)
            serial=json.dumps([terms(shifted_n),terms(shifted_d)],separators=(',',':'))
            records[domain+'_'+name]={'num_terms':len(shifted_n),'den_terms':len(shifted_d),
                'num_constant':str(shifted_n[(0,0)]),'den_constant':str(shifted_d[(0,0)]),
                'coefficient_sha256':sha256(serial.encode()).hexdigest()}
    assert F(3,4)**2>F(1,2)
    assert F(5,4)**2>F(3,2)
    assert F(5,2)**2>6
    return {'agent':'six-downset-2','role':'researcher','arithmetic':'Q(v,l) sparse Fraction polynomial cross-multiplication',
            'base_domain':'v=13+x,l=2+y; x,y>=0','cap_domain':'v=24l+x,l=2+y; x,y>=0',
            'zero_identities':len(eqs),'identity_names':list(eqs),'strict_certificates':records,
            'Schur_P_shifted_coefficients':terms(positive(P.n)),
            'Schur_denominator_factors':['l','v-3','v-2','D=l(v^2-10v+27)-6','E=3lv^2-3lv-16l+6v'],
            'radical_bounds':['sqrt(1/2)<3/4','sqrt(3/2)<5/4','sqrt6<5/2']}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
