"""Conditional zero-endpoint recovery, exact rational original-space floors.

Theorem domain: integer k>=3,q>=3k, arbitrary k-subset of deleted bcx.
The remaining hypothesis is positivity of the canonical zero-limit even
3x3 cap Schur block. A failed canonical block is not face infeasibility.
Ordinary full-space bridges and credited premises are in COEFFICIENT-RECOVERY.md.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import coefficient as c
import portable_zero as z
r, require = c.r, c.require


def dyadic_floor(value):
    """Exact compact positive lower bound; no logarithms or limit changes."""
    require(value>0,'positive dyadic-bound input')
    value=min(F(1),value)
    exponent=max(0,value.denominator.bit_length()-value.numerator.bit_length()+1)
    out=F(1,1<<exponent)
    while out>value:
        out/=2
    while 2*out<=value:
        out*=2
    require(0<out<=value<2*out,'ENTIRE exact dyadic lower-bound inequality')
    return out


def both_positive(G, message):
    rank = r.schur_psd(G)
    other, digest, denominator = r.polynomial_psd(G)
    require(rank == other == len(G), message)
    return {'dimension':len(G),'rank_both_algorithms':rank,
            'full_characteristic_coefficients_sha256':digest,
            'integral_denominator':denominator}


def zero_coefficients(q,k):
    require(type(q) is int and type(k) is int and q>=4 and 1<=k<=q,
            'closed lower coefficient domain: integerq>=4,1<=k<=q')
    closed = json.loads(Path(__file__).with_name('CLOSED-ZERO.json').read_text())
    values = {}
    for row in closed['rows']:
        numerator = sum(F(v)*q**j for j,v in enumerate(row['numerator']))
        denominator = sum(F(v)*q**j for j,v in enumerate(row['denominator']))
        require(numerator>0 and denominator>0,'closed positive rational coefficients')
        values[row['name']] = numerator/denominator
    nu,tau = values['nu0'],values['tau0']
    a = F(q*k)*nu*tau/((q-k)*tau+k*nu)
    require(a>0,'closed positive deletion-count coefficient')
    return a,nu,tau


def cap_parts(S):
    V = [[F(x) for x in row] for row in
         [[1,0,0,0,0],[0,1,0,1,0],[0,1,0,-1,0],
          [0,0,1,0,1],[0,0,1,0,-1]]]
    G = r.congruence(S,V)
    require(all(G[i][j]==0 for i in range(3) for j in (3,4)),
            'EVERY canonical cap parity cross position')
    return r.submatrix(G,[0,1,2]),r.submatrix(G,[3,4])


def canonical(q,k):
    require(type(q) is int and type(k) is int and k>=3 and q>=3*k,
            'conditional full recovery domain: integerk>=3,q>=3k')
    a0,nu0,tau0 = zero_coefficients(q,k)
    b = r.odd_coefficient(q)
    delta = min(F(1,4),a0/8)
    t, sigma = a0/4,-3*a0/8+delta
    require(a0<b/2 and sigma<0 and r.lower_cone(a0,b,t,sigma),
            'strict canonical zero-endpoint lower four-block')
    D = r.forms(q,k)
    C0,U0 = r.evaluate(D,F(0),t,sigma)
    T = [D['keys'].index(key) for key in r.T_KEYS]
    O = [i for i in range(23) if i not in T]
    require(len(T)==5 and len(O)==18,'entire canonical physical partition')
    S,B,Y = r.schur(U0,T,O)
    even,odd = cap_parts(S)
    # This is the explicit conditional hypothesis, never a necessity assertion.
    checks = {'canonical_even':both_positive(even,'canonical zero-limit even cap condition failed')}
    etaU = r.cap_margin(q,k)/D['N']
    etaOdd = r.automatic_odd_cap_floor(q,k)
    require(etaU>0 and etaOdd>0,'whole-domain credited untouched and odd cap floors')
    weights = [D['sizes'][i] for i in O]
    checks['untouched_floor'] = both_positive(
        [[B[i][j]-etaU*weights[i]*int(i==j) for j in range(18)] for i in range(18)],
        'original weighted untouched cap floor')
    checks['automatic_odd'] = both_positive(
        [[odd[i][j]-etaOdd*int(i==j) for j in range(2)] for i in range(2)],
        'complete automatic original odd cap floor')
    determinant = z.det_fraction(even)
    trace = sum(even[i][i] for i in range(3))
    require(determinant>0 and trace>0,'canonical even determinant and trace')
    etaEven = determinant/(trace*trace)
    etaS = min(etaEven,etaOdd)/2
    checks['five_schur_floor'] = both_positive(
        [[S[i][j]-etaS*int(i==j) for j in range(5)] for i in range(5)],
        'full five-dimensional cap Schur floor')
    actual_frobenius = F(23)+sum(v*v for row in Y for v in row)
    norm_bound = F((actual_frobenius.numerator+actual_frobenius.denominator-1)//actual_frobenius.denominator)
    require(norm_bound>=actual_frobenius,'integer upper bound on complete Schur Frobenius norm')
    beta = min(etaU,etaS)/norm_bound
    exact_gap0 = min(F(D['N']-2*D['s']),beta/D['N'])
    gap0 = dyadic_floor(exact_gap0)
    require(gap0>0,'rational original-space cap floor at zero')
    W = [[F(D['sizes'][i]*int(i==j)) for j in range(23)] for i in range(23)]
    require(r.schur_psd([[U0[i][j]-gap0*W[i][j] for j in range(23)] for i in range(23)])==23,
            'EVERY original counted zero-cap weighted floor position')
    star = r.vectors(D)['star']
    zeta = [F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2))
            for core,_,_ in D['keys']]
    require(not any(r.action(C0,star)) and not any(r.action(C0,zeta)) and r.schur_psd(C0)==21,
            'zero endpoint has BOTH original kernels and cannot have greatest lower rank')
    kappa_bound = min(F(1,16),delta/(2*(a0+8*delta)),gap0/(32*D['s']))
    kap = dyadic_floor(kappa_bound)
    require(0<kap<=F(1,16) and 16*D['s']*kap<=gap0/2 and
            a0*kap/(1-8*kap)<delta/2,
            'all exact lower interpolation and whole cap perturbation choices')
    return D,{'q':q,'k':k,'a0':a0,'nu0':nu0,'tau0':tau0,'b':b,
              'canonical_delta':delta,'t':t,'sigma':sigma,'kappa':kap,
              'canonical_even':even,'canonical_odd':odd,
              'even_determinant':determinant,'even_trace':trace,
              'eta_even':etaEven,'eta_odd':etaOdd,'eta_U':etaU,'eta_S':etaS,
              'whole_counted_congruence_frobenius_squared':norm_bound,
              'frobenius_bound_is_integer_ceiling':True,
              'zero_cap_rational_floor_before_compact_dyadic':exact_gap0,
              'exact_kappa_upper_bound_before_compact_dyadic':kappa_bound,
              'zero_original_cap_floor':gap0,'positive_original_cap_floor':gap0/2,
              'whole_unit_gap_lower_bound':gap0/(2*(D['N']-D['s'])),
              'original_parameter_Delta_norm_bound':16*D['s'],
              'original_lower_rank_zero_fixed':21,'original_lower_rank_positive_fixed':22,
              'condition_is_sufficient_not_full_face_classification':True,'checks':checks,
              'complete_zero_cap_matrix_sha256':r.exact.digest(r.encode(U0)),
              'complete_zero_cap_solve_sha256':r.exact.digest(r.encode(Y))}


def verify_positive(q,k):
    D,value = canonical(q,k)
    a0,t,sigma,kap = (value[key] for key in ('a0','t','sigma','kappa'))
    require(c.direct(q,k,F(0))==a0,'closed coefficient equals entire original zero lower shorting')
    a,record = c.separated(q,k,kap)
    require(c.direct(q,k,kap)==a and a>=(1-8*kap)*a0,
            'original positive lower reciprocal coefficient and interpolation floor')
    _,SL,SU,receipt = r.reduced(q,k,kap,t,t,sigma)
    parts = r.parity(SL,SU)
    checks = {name:both_positive(G,'complete positive recovered '+name) for name,G in parts.items()}
    require(r.lower_cone(a,value['b'],t,sigma) and sigma-(2*t*t/a-2*t)>value['canonical_delta']/2,
            'strict positive-kappa lower compatibility, with explicit even margin')
    C,U = r.evaluate(D,kap,t,sigma)
    require(not any(r.action(C,r.vectors(D)['star'])) and r.schur_psd(C)==22 and r.schur_psd(U)==23,
            'complete original counted positive-kappa star, greatest fixed ranks and cap')
    floor = value['positive_original_cap_floor']
    require(r.schur_psd([[U[i][j]-floor*D['sizes'][i]*int(i==j) for j in range(23)] for i in range(23)])==23,
            'ENTIRE recovered original counted weighted cap floor')
    value.update({'a_positive':a,'strict_four_small_positive_checks':checks,
                  'positive_reduction':receipt,
                  'full_positive_C_sha256':r.exact.digest(r.encode(C)),
                  'full_positive_U_sha256':r.exact.digest(r.encode(U)),
                  'all_counted_solves_congruences_and_weighted_floors_checked':True,
                  'ordinary_unbounded_spectral_complement_lift_rank_bridges_unformalized':True,
                  'independent_review':False})
    return value


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('q',type=int);ap.add_argument('k',type=int)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=verify_positive(args.q,args.k)
    args.out.write_text(json.dumps(r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'q':args.q,'k':args.k,'explicit_positive_kappa_recovery':True,
                      'all_original_weighted_floor_checks':True,'independent_review':False}))
