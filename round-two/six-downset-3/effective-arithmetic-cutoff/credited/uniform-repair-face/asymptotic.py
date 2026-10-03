"""Whole homogeneous-layer proof for the original-face asymptotic threshold."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import dual
lower,cs,z,require=dual.lower,dual.cs,dual.z,dual.require
BASE=Path(__file__).resolve().parent


def pair_add(a,b):return a[0]+b[0],a[1]+b[1]
def pair_scale(a,t):return a[0]*t,a[1]*t
def pair_mul(a,b):return a[0]*b[0]+7*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def pair_div(a,b):
    den=b[0]*b[0]-7*b[1]*b[1]
    require(den!=0, 'nonzero entire quadratic-field denominator')
    return pair_scale(pair_mul(a,(b[0],-b[1])),F(1,den))


def homogeneous(poly,degree):return {power:v for power,v in poly.items() if sum(power)==degree}
def derivative(poly):return {(i-1,j):i*v for (i,j),v in poly.items() if i}


def at_rho(poly):
    powers=[(F(1),F(0))]
    for _ in range(max((i for i,j in poly),default=0)):powers.append(pair_mul(powers[-1],(F(3),F(1))))
    out=(F(0),F(0))
    for (i,j),v in poly.items():out=pair_add(out,pair_scale(powers[i],v))
    return out


def verify():
    sealed=dual.source_gate();source=dual.zero_generator.generated()
    N,D=(cs.decode(source[name]) for name in ('joint_residual_numerator','joint_residual_denominator'))
    nd=max(sum(power) for power in N);dd=max(sum(power) for power in D)
    require((nd,dd)==(64,62), 'ENTIRE residual homogeneous degree normalization')
    N0,N1,N2=(homogeneous(N,nd-i) for i in range(3))
    D0,D1=(homogeneous(D,dd-i) for i in range(2))
    F2={(2,0):1,(1,1):-6,(0,2):2}
    identity=z.add(z.scale(N0,2),z.scale(z.mul(F2,D0),-1))
    leading_identity=not identity
    # The simpler half-quadratic proposal may fail. The exact monic
    # quadratic factor and its positive quotient are sufficient.
    quotient=z.divide(N0,F2)
    quotient_shift=lower.shifted({(i,0):v for (i,j),v in quotient.items()},3)
    quotient_positive=bool(quotient_shift) and all(v>=0 for v in quotient_shift.values())
    quotient_positive=quotient_positive and quotient_shift.get((0,0),0)>0
    alpha_den={(i,0):v for (i,j),v in D0.items()}
    shifted=lower.shifted(alpha_den,3)
    positive=bool(shifted) and all(v>=0 for v in shifted.values()) and shifted.get((0,0),0)>0
    nv,dv=at_rho(N0),at_rho(D0)
    require(nv==(0,0) and z.surd_sign(*dv)>0, 'ENTIRE leading root and denominator at3+sqrt7')
    slope=pair_div(at_rho(derivative(N0)),dv)
    intercept=pair_div(at_rho(N1),dv)
    require(slope==(F(0),F(1)) and intercept==(F(0),F(14)),
            'ENTIRE previous optimized first-order asymptotic is reproduced')
    beta=F(-14)
    constant_num=pair_add(pair_add(pair_scale(at_rho(derivative(derivative(N0))),beta*beta/2),
                                 pair_scale(at_rho(derivative(N1)),beta)),at_rho(N2))
    constant=pair_div(constant_num,dv)
    correction=pair_div(pair_scale(constant,-1),(F(0),F(1)))
    # Vanishing of the k coefficient removes the first denominator correction.
    require(pair_add(pair_scale(at_rho(derivative(N0)),beta),at_rho(N1))==(0,0),
            'ENTIRE critical-intercept numerator layer vanishes exactly')
    require(pair_add(constant,pair_mul(correction,(F(0),F(1))))==(0,0),
            'ENTIRE next real-root correction equation')
    return {'actual_agent':'six-downset-3','role':'researcher','field':'QQ(sqrt7), positive real embedding',
            'residual_degrees':[nd,dd],
            'complete_first_three_numerator_layers':[lower.record(poly) for poly in (N0,N1,N2)],
            'complete_first_two_denominator_layers':[lower.record(poly) for poly in (D0,D1)],
            'complete_leading_identity_remainder':lower.record(identity),
            'leading_R_is_half_q2_minus6qk_plus2k2_proved':leading_identity,
            'failed_half_quadratic_proposal_is_retained':not leading_identity,
            'complete_leading_numerator_quadratic_quotient':lower.record(quotient),
            'complete_quadratic_quotient_alpha_shift3':lower.record(quotient_shift),
            'whole_leading_quadratic_quotient_positive_alpha_ge3':quotient_positive,
            'complete_leading_denominator_alpha_shift3':lower.record(shifted),
            'whole_leading_denominator_positive_for_all_alpha_ge3':positive,
            'exact_residual_slope':dual.r.encode(slope),'exact_intercept_term':dual.r.encode(intercept),
            'exact_constant_at_beta_minus14':dual.r.encode(constant),
            'exact_root_correction_over_k':dual.r.encode(correction),
            'constant_sign_at_beta_minus14':z.surd_sign(*constant),
            'global_asymptotic_absence_bridge_available':quotient_positive and positive,
            'current_complete_source_gate':sealed,
            'ordinary_uniform_compact_and_real_root_bridges_unformalized':True,
            'no_explicit_K_epsilon_or_all_small_counts_threshold':True,
            'CAS_imported':False,'independent_review':False}


def pell(offset=-14):
    sealed=dual.source_gate();source=dual.zero_generator.generated()
    N=cs.decode(source['joint_residual_numerator'])
    degree=max(i for i,j in N)
    by_q=[{} for _ in range(degree+1)]
    for (i,j),v in N.items():by_q[i][(j,0)]=v
    require(offset in (-14,-13), 'exact two adjacent Pell-frontier offsets')
    # Work in Z[k,m]/(m^2-(7k^2+1)), substituting q=3k+offset+m.
    L={(1,0):3,(0,0):offset};B={(2,0):7,(0,0):1}
    A,H=by_q[degree],{}
    for i in range(degree-1,-1,-1):
        A,H=z.add(z.mul(L,A),z.mul(B,H),by_q[i]),z.add(A,z.mul(L,H))
    Hshift=lower.shifted(H,48)
    Hpositive=bool(Hshift) and all(v>=0 for v in Hshift.values()) and Hshift.get((0,0),0)>0
    Hnegative=bool(Hshift) and all(v<=0 for v in Hshift.values()) and Hshift.get((0,0),0)<0
    proposals={}
    # m<sqrt7*k+1/(2sqrt7*k). If H>=0, multiply the upper
    # bound by the positive 2sqrt7*k to remove the denominator.
    candidates=(
        ('positive_H_upper',z.mul({(2,0):14,(0,0):1},H),z.scale(z.mul({(1,0):1},A),2),Hpositive),
        ('negative_H_upper',A,z.mul({(1,0):1},H),Hnegative)) if offset==-14 else (
        ('positive_H_lower',A,z.mul({(1,0):1},H),Hpositive),
        ('negative_H_lower',z.mul({(2,0):14,(0,0):1},H),z.scale(z.mul({(1,0):1},A),2),Hnegative))
    goal=-1 if offset==-14 else 1
    for name,aa,bb,applicable in candidates:
        aa,bb=lower.shifted(aa,48),lower.shifted(bb,48)
        powers=set(aa)|set(bb)
        all_correct=all(goal*z.surd_sign(aa.get(power,0),bb.get(power,0))>=0 for power in powers)
        strict=goal*z.surd_sign(aa.get((0,0),0),bb.get((0,0),0))>0
        proposals[name]={'applicable_H_sign_proved':applicable,
                         'complete_shifted_rational_part':lower.record(aa),
                         'complete_shifted_sqrt7_part':lower.record(bb),
                         'wrong_sign_coefficient_count':sum(goal*z.surd_sign(aa.get(power,0),bb.get(power,0))<0 for power in powers),
                         'constant_has_strict_goal_sign':strict,'completed_strict_certificate':applicable and all_correct and strict}
    controls=[]
    m,k=8,3
    for n in range(1,4):
        require(m*m-7*k*k==1, 'ENTIRE integer Pell relation')
        q=3*k+m+offset
        actual=z.evaluate(N,q,k);reduced=z.evaluate(A,k,0)+m*z.evaluate(H,k,0)
        require(actual==reduced, 'ENTIRE original residual and Pell quotient-ring control')
        if n>=2:
            require(k>=48 and q>=3*k, 'actual infinite-family count domain')
            require(goal*actual>0, 'exact first whole adjacent Pell residual control signs')
        controls.append({'n':n,'m':m,'k':k,'q':q,'whole_original_numerator':str(actual),
                         'in_uniform_face_domain':n>=2})
        m,k=8*m+21*k,3*m+8*k
    return {'actual_agent':'six-downset-3','role':'researcher',
            'exact_domain':'ALL real k>=48,m=sqrt(7k^2+1); original integer carriers when m,k integers',
            'substitution':'q=3k'+str(offset)+'+m, m^2=7k^2+1','offset':offset,'goal_residual_sign':goal,
            'entire_reduced_rational_part':lower.record(A),'entire_reduced_m_part':lower.record(H),
            'entire_H_shift48':lower.record(Hshift),'H_positive_shift_proved':Hpositive,'H_negative_shift_proved':Hnegative,
            'whole_sign_proposals':proposals,
            'all_k_ge48_original_residual_goal_sign_proved':any(row['completed_strict_certificate'] for row in proposals.values()),
            'exact_integer_family':'m_n+k_n sqrt7=(8+3sqrt7)^n, ALL integer n>=2; q_n=3k_n+m_n'+str(offset),
            'all_integer_controls':controls,'current_complete_source_gate':sealed,
            'ordinary_Pell_ceiling_and_original_dual_bridges_unformalized':True,'CAS_imported':False,'independent_review':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('layers','pell'),nargs='?',default='layers')
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result={'actual_agent':'six-downset-3','role':'researcher','negative_frontier':pell(-14),
            'positive_adjacent_frontier':pell(-13)} if args.phase=='pell' else verify()
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    if args.phase=='pell':
        print(json.dumps({key:{'goal_sign':row['goal_residual_sign'],
                               'all_Pell_k_ge48_goal_sign_proved':row['all_k_ge48_original_residual_goal_sign_proved'],
                               'H_positive':row['H_positive_shift_proved'],'H_negative':row['H_negative_shift_proved'],
                               'signs':{key:{name:value for name,value in sign.items()
                                            if not name.startswith('complete_shifted')}
                                        for key,sign in row['whole_sign_proposals'].items()}}
                          for key,row in result.items() if key in ('negative_frontier','positive_adjacent_frontier')}))
        raise SystemExit(0)
    print(json.dumps({'leading_identity_proved':result['leading_R_is_half_q2_minus6qk_plus2k2_proved'],
                      'leading_quadratic_quotient_positive_alpha_ge3':result['whole_leading_quadratic_quotient_positive_alpha_ge3'],
                      'leading_denominator_positive_alpha_ge3':result['whole_leading_denominator_positive_for_all_alpha_ge3'],
                      'exact_constant_at_beta_minus14':result['exact_constant_at_beta_minus14'],
                      'exact_root_correction_over_k':result['exact_root_correction_over_k']}))
