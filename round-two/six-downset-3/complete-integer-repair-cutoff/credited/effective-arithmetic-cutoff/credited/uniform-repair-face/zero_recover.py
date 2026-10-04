"""Exact original recovery for a new, explicitly noncanonical repair.

The whole-space floors are derived separately for the supplied t,sigma.
No canonical recovery margin is substituted for this repair's margin.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import input as inputs
from types import SimpleNamespace
z=SimpleNamespace(r=inputs.r,require=inputs.require,recovery=inputs.recovery,
                  coefficient=inputs.coefficient,SOURCE=inputs.SOURCE)
r,require,v=z.r,z.require,z.recovery


def recover(q,k,t,sigma):
    require(k>=3 and q>=3*k,'credited original untouched and complement bridge domain')
    a0,nu,tau=v.zero_coefficients(q,k);b=r.odd_coefficient(q)
    require(z.coefficient.direct(q,k,F(0))==a0,'whole original lower zero coefficient')
    left=2*t*t/a0-2*t
    margin=sigma-left
    require(margin>0 and r.lower_cone(a0,b,t,sigma),'BOTH strict lower zero parity blocks')
    D=r.forms(q,k);C0,U0=r.evaluate(D,F(0),t,sigma)
    T=[D['keys'].index(key) for key in r.T_KEYS];O=[i for i in range(len(D['keys'])) if i not in T]
    S,B,Y=r.schur(U0,T,O);even,odd=v.cap_parts(S)
    checks={'zero_even':v.both_positive(even,'new repair whole zero even cap')}
    etaU=r.cap_margin(q,k)/D['N'];etaOdd=r.automatic_odd_cap_floor(q,k)
    require(etaU>0 and etaOdd>0,'credited complete-domain untouched and automatic odd floors')
    checks['untouched_weighted_floor']=v.both_positive(
        [[B[i][j]-etaU*D['sizes'][O[i]]*int(i==j) for j in range(len(O))] for i in range(len(O))],
        'new whole untouched cap weighted floor')
    checks['odd_floor']=v.both_positive(
        [[odd[i][j]-etaOdd*int(i==j) for j in range(2)] for i in range(2)],
        'new full automatic odd cap floor')
    det=v.z.det_fraction(even);trace=sum(even[i][i] for i in range(3))
    require(det>0 and trace>0,'new repaired even determinant and trace')
    etaEven=det/(trace*trace);etaS=min(etaEven,etaOdd)/2
    checks['full_five_floor']=v.both_positive(
        [[S[i][j]-etaS*int(i==j) for j in range(5)] for i in range(5)],
        'new repaired complete cap Schur floor')
    frobenius=F(len(D['keys']))+sum(x*x for row in Y for x in row)
    ceiling=F((frobenius.numerator+frobenius.denominator-1)//frobenius.denominator)
    beta=min(etaU,etaS)/ceiling
    exactFloor=min(F(D['N']-2*D['s']),beta/D['N'])
    epsilon=v.dyadic_floor(exactFloor)
    W=[[F(D['sizes'][i]*int(i==j)) for j in range(len(D['keys']))] for i in range(len(D['keys']))]
    require(r.schur_psd([[U0[i][j]-epsilon*W[i][j] for j in range(len(W))] for i in range(len(W))])==len(W),
            'EVERY original counted zero cap weighted-floor position')
    # Complete original endpoint perturbation bound ||Delta||<=16s.
    # B=2t^2/a0 and kappa<=m/[32(B+m)] imply
    # B*8kappa/(1-8kappa)<m/2 when kappa<=1/16.
    curvature=2*t*t/a0
    bound=min(F(1,16),margin/(32*(curvature+margin)),epsilon/(32*D['s']))
    kap=v.dyadic_floor(bound)
    require(0<kap<=F(1,16) and
            curvature*8*kap/(1-8*kap)<margin/2 and
            16*D['s']*kap<=epsilon/2,
            'new repair-specific lower and full original upper perturbation bounds')
    a,coefficient_record=z.coefficient.separated(q,k,kap)
    require(z.coefficient.direct(q,k,kap)==a and a>=(1-8*kap)*a0,
            'complete original recovered positive coefficient and interpolation floor')
    DD,SL,SU,reduction=r.reduced(q,k,kap,t,t,sigma)
    require(DD==D,'complete parameterized original forms unchanged')
    parts=r.parity(SL,SU)
    checks['positive_four_blocks']={name:v.both_positive(G,'new positive repair '+name) for name,G in parts.items()}
    require(r.lower_cone(a,b,t,sigma) and sigma-(2*t*t/a-2*t)>margin/2,
            'new repair has explicit strictly positive recovered lower margin')
    C,U=r.evaluate(D,kap,t,sigma)
    star=r.vectors(D)['star']
    require(not any(r.action(C,star)) and r.schur_psd(C)==len(W)-1 and r.schur_psd(U)==len(W),
            'new whole original counted star, lower greatest fixed rank and cap')
    checks['full_positive_lower_characteristic']=r.polynomial_psd(C)
    checks['full_positive_cap_characteristic']=r.polynomial_psd(U)
    require(checks['full_positive_lower_characteristic'][0]==len(W)-1 and
            checks['full_positive_cap_characteristic'][0]==len(W),
            'separate complete characteristic algorithm has same PSD ranks')
    require(r.schur_psd([[U[i][j]-epsilon*W[i][j]/2 for j in range(len(W))] for i in range(len(W))])==len(W),
            'ENTIRE original recovered cap weighted floor')
    zeta=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+
            int(core.bit_count()>=2)) for core,_,_ in D['keys']]
    require(not any(r.action(C0,star)) and not any(r.action(C0,zeta)) and r.schur_psd(C0)==len(W)-2,
            'zero has actual two kernels and is not a greatest-rank witness')
    return {'q':q,'k':k,'t':t,'sigma':sigma,'kappa':kap,'N':D['N'],'s':D['s'],
            'a0':a0,'a_positive':a,'b':b,'zero_lower_left_margin':margin,
            'positive_lower_left_margin':sigma-(2*t*t/a-2*t),
            'general_lower_curvature_2t2_over_a0':curvature,
            'positive_kappa_upper_bound':bound,'full_Delta_norm_bound':16*D['s'],
            'eta_even':etaEven,'eta_odd':etaOdd,'eta_U':etaU,'eta_S':etaS,
            'whole_counted_congruence_frobenius_ceiling':ceiling,
            'zero_original_cap_floor_before_dyadic':exactFloor,
            'zero_original_cap_floor':epsilon,'positive_original_cap_floor':epsilon/2,
            'whole_M_unit_gap_lower_bound':epsilon/(2*(D['N']-D['s'])),
            'original_H_lower_rank':D['N']-1,'original_H_cap_rank':D['N']-1,
            'internal_C_and_LminusJ_rank':D['N']-2,
            'all_original_solve_congruence_weighted_floor_positions_checked':True,
            'full_zero_even':even,'full_zero_odd':odd,'full_positive_parity':parts,
            'full_positive_C_sha256':r.exact.digest(r.encode(C)),
            'full_positive_U_sha256':r.exact.digest(r.encode(U)),
            'checks':checks,'coefficient_record':coefficient_record,'reduction':reduction,
            'source_gate':z.SOURCE,'independent_review':False,'unformalized':True,
            'ordinary_full_original_complement_star_lift_rank_bridges_credited9980':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    a0,_,_=v.zero_coefficients(100,20)
    row=recover(100,20,a0/2,-a0/2+F(1,4))
    args.out.write_text(json.dumps(r.encode(row),indent=2,sort_keys=True)+'\n')
    print(json.dumps(r.encode({key:row[key] for key in ('q','k','t','sigma','kappa','N',
        's','zero_original_cap_floor','whole_M_unit_gap_lower_bound','original_H_lower_rank','original_H_cap_rank')})))
