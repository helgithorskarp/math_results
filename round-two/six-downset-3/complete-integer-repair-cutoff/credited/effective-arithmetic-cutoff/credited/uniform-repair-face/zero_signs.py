"""Exact new all-count sign probes and quadratic-field asymptotic coefficients.

Every failed coefficient test is retained as a failed proof proposal.
Finite controls and asymptotic coefficients do not prove a global cutoff.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import argparse, json
import zero_check as c
import zero_generator
BASE=Path(__file__).resolve().parent
z=c.integer_tools()


def quadrant(poly, k0):
    # Exact binomial substitution q=3k+u, followed by k=k0+x.
    first={}
    for (i,j),value in poly.items():
        for m in range(i+1):
            power=m,i-m+j
            first[power]=first.get(power,0)+value*comb(i,m)*3**(i-m)
    return z.shift_k(z.clean(first),k0)


def sign(poly):
    shifted=quadrant(poly,7)
    negative=[(power,value) for power,value in sorted(shifted.items()) if value<0]
    return {'exact_domain':'ALL real k>=7,q>=3k by q=3(7+x)+u, x,u>=0',
            'entire_shifted_coefficients':c.record(shifted),
            'negative_count':len(negative),'positive_constant':shifted.get((0,0),0)>0,
            'completed_positive_certificate':not negative and shifted.get((0,0),0)>0,
            'failed_proposal_is_not_mathematical_absence':bool(negative)}


def new_polynomials():
    data=zero_generator.generated()
    P=c.matrix_decode(data['complete_zero_cap_numerator']);T=c.decode(data['cap_target'])
    an,ad=(c.decode(data[n]) for n in ('lower_numerator','lower_denominator'))
    den=c.decode(data['optimizer_common_denominator'])
    hx,hz=(c.decode(data[n]) for n in ('optimizer_a_numerator','optimizer_abac_numerator'))
    PH=z.divide(z.add(z.mul(P[0][0],P[2][2]),z.scale(z.mul(P[0][2],P[0][2]),-1)),T)
    first=z.add(den,hz,z.scale(hx,-1))
    # b=bn/bd, a0=an/ad. The vertex is a0*(den+hz-hx)/(2den).
    bn={(i,0):value for i,value in enumerate((-16,12,42,18)) if value}
    bd={(i,0):value for i,value in enumerate((-2,5,6)) if value}
    # The independently known b has numerator2(3q+4)(3q^2+3q-2).
    c.require(all(F(z.evaluate(bn,q,0),z.evaluate(bd,q,0))==c.r.odd_coefficient(q) for q in (4,9,27)),
              'exact b rational normalization controls')
    right=z.add(z.scale(z.mul(z.mul(bn,ad),den),4),
                z.scale(z.mul(z.add(z.mul(an,bd),z.mul(bn,ad)),first),-1))
    return {'H00':P[0][0],'H_determinant':PH,'vertex_positive':first,'vertex_below_lower_right':right,
            'compact_joint_gcd':c.decode(data['joint_gcd'])}


def pair_add(a,b): return a[0]+b[0],a[1]+b[1]
def pair_scale(a,n): return a[0]*n,a[1]*n
def pair_mul(a,b): return a[0]*b[0]+7*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def pair_div(a,b):
    denominator=b[0]*b[0]-7*b[1]*b[1]
    if not denominator:raise ValueError('zero quadratic-field denominator')
    return pair_scale(pair_mul(a,(b[0],-b[1])),F(1,denominator))
def pair_sign(a): return z.surd_sign(a[0],a[1])


def asymptotic():
    data=zero_generator.generated();n=c.decode(data['joint_residual_numerator'])
    d=c.decode(data['joint_residual_denominator']);degree=max(i+j for i,j in n)
    leading={i:sum(v for (ii,j),v in n.items() if ii==i and ii+j==degree) for i in range(degree+1)}
    next_term={i:sum(v for (ii,j),v in n.items() if ii==i and ii+j==degree-1) for i in range(degree)}
    rho=[(F(1),F(0))]
    for _ in range(degree+1):rho.append(pair_mul(rho[-1],(F(3),F(1))))
    def at(values):
        out=(F(0),F(0))
        for i,v in values.items():
            while i>=len(rho):rho.append(pair_mul(rho[-1],(F(3),F(1))))
            out=pair_add(out,pair_scale(rho[i],v))
        return out
    A=at(leading);Aprime=at({i-1:i*v for i,v in leading.items() if i})
    B=at(next_term)
    c.require(A==(0,0) and pair_sign(Aprime)>0,'ENTIRE leading homogeneous term vanishes at3+sqrt7 with positive derivative')
    beta=pair_div(pair_scale(B,-1),Aprime)
    ddegree=max(i+j for i,j in d)
    D=at({i:sum(v for (ii,j),v in d.items() if ii==i and ii+j==ddegree) for i in range(ddegree+1)})
    c.require(pair_sign(D)>0,'ENTIRE leading denominator positive at3+sqrt7')
    # Written ordinary large-k statement requires the optimizer and cap branch too.
    derivative_ratio=pair_div(Aprime,D)
    c.require(beta==(F(-14),F(0)) and derivative_ratio==(F(0),F(1)),
              'ENTIRE exact optimized residual leading term sqrt7*(beta+14)*k')
    def field_leading(poly):
        deg=max(i+j for i,j in poly)
        val=at({i:sum(v for (ii,j),v in poly.items() if ii==i and ii+j==deg) for i in range(deg+1)})
        return deg,val
    P=c.matrix_decode(data['complete_zero_cap_numerator']);T=c.decode(data['cap_target'])
    an,ad=(c.decode(data[name]) for name in ('lower_numerator','lower_denominator'))
    hd=c.decode(data['optimizer_common_denominator'])
    hx,hz=(c.decode(data[name]) for name in ('optimizer_a_numerator','optimizer_abac_numerator'))
    PH=z.divide(z.add(z.mul(P[0][0],P[2][2]),z.scale(z.mul(P[0][2],P[0][2]),-1)),T)
    fields={}
    for name,num,den0 in (('a0',an,ad),('H00',P[0][0],z.scale(T,4)),
                         ('H_determinant',PH,z.scale(T,16)),
                         ('w_Hinverse_w',z.scale(z.add(P[0][0],P[2][2],z.scale(P[0][2],2)),4),PH),
                         ('ell',z.add(hz,z.scale(hx,-1)),hd)):
        nd,nv=field_leading(num);dd,dv=field_leading(den0)
        c.require(pair_sign(dv)>0, 'positive asymptotic field denominator '+name)
        fields[name]={'numerator_total_degree':nd,'denominator_total_degree':dd,
                      'leading_numerator_at_rho':nv,'leading_denominator_at_rho':dv,
                      'upper_power_of_k':nd-dd if nv!=(0,0) else nd-dd-1,
                      'leading_ratio':pair_div(nv,dv)}
    c.require(fields['a0']['upper_power_of_k']==1 and
              fields['H00']['upper_power_of_k']==2 and pair_sign(fields['H00']['leading_ratio'])>0 and
              fields['H_determinant']['upper_power_of_k']==4 and pair_sign(fields['H_determinant']['leading_ratio'])>0 and
              fields['w_Hinverse_w']['upper_power_of_k']<=-2 and fields['ell']['upper_power_of_k']<=-1,
              'ENTIRE anchor and half-repair loss asymptotic powers')
    return {'actual_agent':'six-downset-3','role':'researcher','field':'QQ(sqrt7), positive real embedding',
            'substitution':'q=(3+sqrt7)k+beta with fixed real beta; k->positive infinity',
            'complete_leading_numerator_coefficients':[[i,str(v)] for i,v in leading.items() if v],
            'complete_next_numerator_coefficients':[[i,str(v)] for i,v in next_term.items() if v],
            'numerator_total_degree':degree,'denominator_total_degree':ddegree,
            'leading_numerator_at_rho':A,'leading_derivative_at_rho':Aprime,'next_numerator_at_rho':B,
            'leading_denominator_at_rho':D,'critical_intercept':beta,
            'residual_leading_scale_power':degree-1-ddegree,'positive_residual_slope':derivative_ratio,
            'complete_asymptotic_auxiliary_fields':fields,
            'half_repair_loss_identity':'R_half=R-a0*ell^2*(1+a0*w^T H^-1 w)-2delta',
            'half_repair_loss_power_of_k':-1,
            'entire_first_two_homogeneous_layers_compared':True,
            'not_a_global_cutoff':True,'original_kappa_slope_not_proved':True,'independent_review':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['H00','H_determinant','vertex_positive','vertex_below_lower_right','compact_joint_gcd','asymptotic'])
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=asymptotic() if args.phase=='asymptotic' else {'actual_agent':'six-downset-3','role':'researcher',
        'obligation':args.phase,'sign':sign(new_polynomials()[args.phase])}
    args.out.write_text(json.dumps(c.r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase':args.phase,'completed':True,
        'sign_proved':value.get('sign',{}).get('completed_positive_certificate'),
        'negative_count':value.get('sign',{}).get('negative_count'),
        'critical_intercept':c.r.encode(value.get('critical_intercept'))}))
