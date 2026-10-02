"""Later referee scalar extension, developed after the sealed author replay.

Reuses only the referee's frozen sparse-polynomial core. It is not a new
pre-author-code independence seal. No author program is imported.
"""
from fractions import Fraction as F
import json
import signal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import add, build, const, digest, need, norm_polynomials, pack, scale, same_typed, substitute, var
from math import comb


def profile(H, Y, C, t3, initial_x, radius):
    e, E, d = F(1, 65536), F(1, 256), F(1, 1000)
    kap = F(1, 4) - F(5, 4) * radius
    alpha = F(7, 2) * kap - F(5, 8)
    eta = var(18)
    margins = {}
    def margin(name, value):
        need(value > 0, name)
        margins[name] = str(value)
    margin('radius_with_anchor_squared', (radius / E * F(255, 256)) ** 2 - H)
    margin('radius_below_one_sixth', F(1, 6) - radius)
    margin('square_tail_coefficient', kap)
    margin('phase_feedback_coefficient', alpha)
    margin('initial_c8_squared', initial_x ** 2 - F(81, 8) * H)
    margin('initial_maclaurin_scale_squared', F(9, 4) ** 2 - F(H, 8))
    lower = [F(9, k) * comb(8, 9-k) * F(9, 4) ** (9-k) * E ** (7-k) for k in range(1, 7)]
    margin('initial_lower_sum_below4', 4 - sum(lower))
    margin('c1_below_delta', d - lower[0]); margin('c2_below_delta', d - lower[1])
    rows = [add(r, scale(var(20), F(151, 1024) - alpha)) for r in norm_polynomials()]
    # Only the retained negative coefficient changes with the radius.
    positive = [add(r, scale(var(20), alpha)) for r in rows]
    need(all(v >= 0 for r in positive for v in r.values()), 'entire monotone envelope')
    coarse = substitute(positive[0], {20: scale(eta, F(9, 2)*H), 21: scale(eta, 4), 22: scale(eta, d)})
    need(set(coarse) <= {(18,), (19,), (18, 18), (18, 19), (19, 19)}, 'coarse monomial coverage')
    K0 = coarse.get((18, 18), 0)
    b0 = coarse.get((18,), 0) + e * K0
    lam = coarse.get((19,), 0) + e * coarse.get((18, 19), 0) + initial_x * E * coarse.get((19, 19), 0)
    margin('coarse_constant_below16', 16 - b0)
    margin('coarse_feedback_below_one_quarter', F(1, 4) - lam)
    margin('first_mean_bound_below22', 22 - F(64, 3))
    margin('second_coefficient_belowY', Y - F(9, 14) * (H + F(64, 81) * 22**2 * e))
    margin('first_trace_below20', 20 - F(8, 9) * 22)
    need(t3**2 >= H**3, 'third-moment majorant squared')
    if t3**2 > H**3:margin('third_moment_squared', t3**2 - H**3)
    refined_lower = sum(lower[:5]) + 2000 * e**2 + 15 * H * e + F(t3, 2) * E
    margin('refined_lower_sum', C - refined_lower)
    finals = [substitute(r, {19:scale(eta,22),20:scale(eta,Y),21:scale(eta,C),22:scale(eta,d),23:scale(eta,d)}) for r in positive]
    need(all(set(r) == {(18,), (18, 18)} for r in finals), 'complete final scalar polynomials')
    need(finals[0][(18,)] == finals[1][(18,)], 'same linear cost')
    base = finals[0][(18,)]
    Ks = [r[(18, 18)] for r in finals]
    for j,K in enumerate(Ks):margin('quadratic_below3000_'+str(j), 3000-K)
    mu = base + 3000*e
    margin('entry_below8', 8-mu)
    margin('c7_below7', 7-mu/(1+alpha))
    cap = F(63,8) if H==36 else F(127,16)
    margin('named_coefficient_cap', cap-mu)
    return {'H':H,'Y':Y,'lower_cap':str(C),'initial_c8_sqrt_eta_cap':initial_x,
            'critical_radius':str(radius),'square_tail_kappa':str(kap),'phase_alpha':str(alpha),
            'initial_lower_bounds':[str(q) for q in lower],'coarse_K0':str(K0),
            'coarse_constant':str(b0),'coarse_feedback':str(lam),'first_c8_eta_cap':22,
            'first_mean_eta_cap':20,'third_moment_majorant':t3,
            'third_moment_majorant_can_be_equal':t3**2==H**3,
            'refined_lower_sum':str(refined_lower),'final_linear':str(base),
            'final_quadratics':[str(q) for q in Ks],'coefficient_mu':str(mu),
            'c7_mu':str(mu/(1+alpha)),'named_coefficient_cap':str(cap),
            'entire_norm_polynomials':[pack(r) for r in rows],'strict_margins':margins}


def without_disk():
    eta, t = F(1,65536), F(1,256)
    a=1-eta
    need(t*t==eta,'square-root parameter control')
    # p=z^9+t z^8-a^9-t a^8; p'=z^7(9z+8t).
    H=F(64,81)*eta
    objective=7/a+1/(a+F(8,9)*t)
    pminus=-1+t-a**9-t*a**8
    derivative_minus=9-8*t
    unit_weight=-2*derivative_minus*pminus-9*pminus*pminus
    need(H<=40*eta and objective<8+3*eta,'cap-free nondisk sublevel control')
    need(t>F(127,16)*eta,'violated coefficient cap without disk hypothesis')
    need(unit_weight<0,'unit weight certifies an original outside the disk')
    return {'eta':str(eta),'c8':str(t),'H':str(H),'objective':str(objective),
            'sublevel_slack':str(8+3*eta-objective),'unit_weight_at_minus_one':str(unit_weight),
            'critical_multiplicities':[7,1],'scope':'removing ONLY original disk-root hypothesis fails; this is not an actual feasible competitor'}


def extension():
    return {'schema':'six-reviewer-1-later-energy-extension-v1',
            'independent_pre_author_core_record':digest(build()),
            'post_author_replay_extension':True,
            'profiles':[profile(36,24,F(1,2),216,20,F(25,1024)),
                        profile(40,26,F(9,16),254,21,F(13,512))],
            'disk_hypothesis_control':without_disk()}


if __name__=='__main__':
    signal.alarm(45)
    result=extension()
    expected=Path(sys.argv[1]) if len(sys.argv)==2 else Path(__file__).with_name('extension.json')
    same_typed(result,json.loads(expected.read_text()))
    print(json.dumps({'status':'PASS','extension_sha256':digest(result),
                      'energy_thresholds':[q['H'] for q in result['profiles']]}))
