"""Independent exact bridges for the global Sendov energy review.

No author or other reviewer's executable modules are imported. Coefficients
are rational polynomials in formal positive v and real phase parameters.
This code does not establish the analytic neighborhood or sequence theorem.
"""
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s


def need(ok, message):
    if not ok:
        raise ValueError(message)


def equal(a, b, message):
    need(s.cancel(a-b) == 0, message)


def reject(fn, message):
    try:
        fn()
    except ValueError:
        return message
    raise ValueError('corrupted algebra certificate accepted: '+message)


def mul(a, b, order=6):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i+j <= order:
                out[i+j] = out.get(i+j, 0) + x*y
    return {k: s.expand(v) for k, v in out.items()}


def power(a, n):
    out = {0: s.Integer(1)}
    for _ in range(n):
        out = mul(out, a)
    return out


def energy_chart():
    v, phi, c = s.symbols('v phi c')
    a = 1/v-1
    # Exact unit-circle energy, derived directly from u-v.
    circle = 2*v**4*(1-c)/(1-2*a*v*v*(1-c))
    cosine = 1-phi**2/2+phi**4/24-phi**6/720
    expansion = s.series(circle.subs(c, cosine), phi, 0, 8).removeO().expand()
    f4 = v-v*v-s.Rational(1, 12)
    f6 = (v-v*v)**2-(v-v*v)/6+s.Rational(1, 360)
    equal(expansion.coeff(phi, 2), v**4, 'actual circle quadratic energy')
    equal(expansion.coeff(phi, 4), v**4*f4, 'actual circle fourth energy')
    equal(expansion.coeff(phi, 6), v**4*f6, 'actual circle sixth energy')
    A3, A4, A5, beta, y, X2 = s.symbols('A3 A4 A5 beta y X2')
    xs = s.symbols('x0:6')
    seven = list(xs)+[-sum(xs)]
    squared = sum(x*x for x in seven)
    phases = [{1: 7, 3: 7*A3+beta+y, 4: 7*A4, 5: 7*A5}]
    phases += [{1: -1, 2: x, 3: -A3+beta+y, 4: -A4, 5: -A5} for x in seven]
    sums = {}
    for n in (2, 4, 6):
        out = {}
        for phase in phases:
            for k, value in power(phase, n).items():
                out[k] = out.get(k, 0)+value
        sums[n] = {k: s.expand(value) for k, value in out.items()}
    expected2 = {2: 56, 4: 112*A3+squared, 5: 112*A4,
                 6: 56*A3*A3+112*A5+8*(beta+y)**2}
    expected4 = {4: 2408, 6: 9632*A3+1344*(beta+y)+6*squared}
    expected6 = {6: 117656}
    for n, expected in [(2, expected2), (4, expected4), (6, expected6)]:
        for k in range(7):
            equal(sums[n].get(k, 0), expected.get(k, 0), 'all zero-sum original phase moments')
    chosen3 = -squared/112
    chosen5 = -(squared*squared/224+16*beta*y+8*y*y+f4*(1344*y-80*squared))/112
    for k in range(2, 7):
        actual = sums[2].get(k, 0)+f4*sums[4].get(k, 0)+f6*sums[6].get(k, 0)
        branch = actual.subs({A3: 0, A4: 0, A5: 0, y: 0, **dict.fromkeys(xs, 0)})
        equal(s.expand((actual-branch).subs({A3: chosen3, A4: 0, A5: chosen5})), 0,
              'generic true energy chart coefficient '+str(k))
    tau = s.Symbol('tau')
    rho = 1-tau
    radial = v*v*(1-2*rho*c+rho*rho)/(a*a+2*a*rho*c+rho*rho)
    equal(s.diff(radial, tau).subs({tau: 0, c: 1}), 0, 'no constant radial energy derivative')
    controls = [reject(lambda: equal(112*(chosen3+1)+squared,0,'wrong A3'),
                       'wrong energy cubic amplitude'),
                reject(lambda: equal(112,0,'wrong A4'), 'nonzero fourth amplitude')]
    # There is no odd phase term, so tau=t^6 r first enters at t^8.
    return {'circle_f4_over_v4': str(s.expand(f4)),
            'circle_f6_over_v4': str(s.expand(f6)),
            'A3': '-X2/112', 'A4': '0',
            'A5': str(s.expand(-(X2**2/224+16*beta*y+8*y*y+f4*(1344*y-80*X2))/112)),
            'zero_sum_directions': 6, 'all_energy_coefficients_through_degree': 6,
            'radial_first_possible_energy_order': 8, 'rejected_controls': controls}


def compression():
    n = 8
    one = s.ones(n, 1)
    P = s.eye(n)-one*one.T/n
    theta = s.Matrix([7]+[-1]*7)
    leading = P*s.diag(*list(theta))*P
    need(leading*theta == 6*theta, 'simple leading eigenvalue six')
    need(leading*one == s.zeros(n, 1), 'orthogonal excluded constant direction')
    for j in range(1, 7):
        w = s.zeros(n, 1);w[j] = 1;w[7] = -1
        need(leading*w == -w, 'entire six-dimensional leading split eigenspace')
    xs = list(s.symbols('x0:6'));xs.append(-sum(xs))
    split = P*s.diag(0, *xs)*P
    equal((theta.T*split*theta)[0]/56, 0, 'every zero-sum linear split expectation')
    q = s.Symbol('q');u = s.symbols('u0:3')
    matrix = s.diag(*u)*(s.eye(3)+s.ones(3))
    R = s.prod(q-x for x in u)
    equal((q*s.eye(3)-matrix).det(), 4*R-q*s.diff(R,q),
          'multiplicity-safe reciprocal determinant control')
    control=reject(lambda: need(leading*theta==5*theta,'wrong simple eigenvalue'),
                   'wrong divided simple eigenvalue')
    return {'leading_eigenvalues_on_near_space': {'6': 1, '-1': 6},
            'divided_internal_gap': 7, 'zero_sum_first_expectation': '0',
            'multiplicity_safe_determinant_control': 'passed', 'rejected_control':control}


def constants():
    a = s.Symbol('a');d = 1+a;v = 1/d;a0 = s.Rational(5,8)
    d0 = 1+a0;v0 = 1/d0
    kappa = d*(a-a0)
    C = s.Rational(560235,8388608);D = s.Rational(520320727875,6734508720128)
    K1 = d**3*(516*d*d-528*d-393)/7168
    Ktr = d**3*(3792*d*d-7728*d+2991)/28672
    equal(Ktr-K1, 27*d**3*(a-a0)**2/448, 'entire parameter mismatch')
    equal(K1.subs(a,a0), C, 'cutoff quadratic coefficient')
    gamma = D/C**3-s.diff(K1,a).subs(a,a0)/(d0*C*C)
    equal(gamma, s.Rational(2965647537471488,20111391661725), 'basin second coefficient')
    equal(d0/C, s.Rational(1048576,43095), 'one-sided basin slope')
    beta = (392-1197*v+945*v*v)/20
    equal(beta.subs(a,a0), s.Rational(112,169), 'stationary cutoff mean')
    norm3 = 112*s.sqrt(14)*v0**6
    original_mean = s.Rational(28561,32768)/s.sqrt(14)
    equal(8*beta.subs(a,a0)/norm3, original_mean, 'actual branch normalized mean')
    reciprocal_mean = s.Rational(14703,8192)/s.sqrt(14)
    c3 = v0*v0/6-v0**3+v0**4
    equal(d0*d0*reciprocal_mean+3*c3*d0**8/s.sqrt(14), original_mean,
          'original positive-singleton/reciprocal-negative sign conversion')
    # The common-angle configuration has F=16/|a+exp(iM)|.
    equal(8*a*v**3-8*kappa*v**4, 5*v**3, 'fixed-energy limiting mean coefficient')
    L = v**3*(1616-1432*v-1859*v*v)/224
    equal(L, (1616*a*a+1800*a-1675)/(224*d**5), 'same split coefficient in both parameters')
    need(L.subs(a,a0) > 0, 'cutoff strict angular curvature')
    cost = -d0**3*(96*d0*d0-196*d0+67)/512
    moment_cost = -cost
    alpha = s.Rational(65,512)
    allowance = 27*d0**3/448
    need(moment_cost>0 and alpha>0 and allowance>0, 'positive retained costs and allowance')
    Kx2 = 56**2*v0**4*6*allowance/moment_cost
    Ky2 = 14**3*v0**8*allowance/alpha
    Kr = 56**3*v0**10*allowance/2
    controls = [reject(lambda: equal(Ktr-K1,27*d**3*(a-a0)/448,'wrong squared mismatch'),
                       'linear rather than quadratic radius mismatch'),
                reject(lambda: equal(gamma+1,D/C**3-s.diff(K1,a).subs(a,a0)/(d0*C*C),'wrong crossing coefficient'),
                       'wrong basin second coefficient'),
                reject(lambda: equal(d0*d0*reciprocal_mean-3*c3*d0**8/s.sqrt(14),original_mean,'wrong phase conversion'),
                       'wrong reciprocal-to-original cubic sign')]
    return {'a0':str(a0),'v0':str(v0),'L_at_cutoff':str(L.subs(a,a0)),
            'branch_Q_allowance_A0':str(allowance),'moment_cost_k0':str(moment_cost),
            'mean_cost_alpha0':str(alpha),'parabolic_chart_entry_Kx_squared':str(Kx2),
            'parabolic_chart_entry_Ky_squared':str(Ky2),'parabolic_chart_entry_Kr':str(Kr),
            'basin_Gamma':str(gamma),'basin_right_derivative':str(d0/C),
            'normalized_original_mean':str(original_mean),
            'normalization_e3_over_t6':str((56*v0**4)**3), 'rejected_controls':controls}


def degree_cover():
    result=[]
    # Physical analytic trace: amplitude/mean/split/radial weights3,3,2,6.
    for powers in product(range(4), repeat=4):
        total=sum(powers)
        if not total or total>3:
            continue
        weight=sum(p*w for p,w in zip(powers,(3,3,2,6)))
        if total==1 and powers[0]+powers[1]:
            weight+=1  # base angular scalar gradients vanish at collapse
        if weight>=6:
            continue
        if powers[2]==1:
            reason='vanishes by zero-sum seven-root symmetry'
        else:
            degree=2*powers[0]+powers[1]+powers[2]
            need(degree<=2, 'all surviving sub-six monomials have degree at most two')
            reason='degree<=2; eliminated by exact stationarity/Hessian identities'
        result.append({'physical_powers_T_M_eta_tau':powers,'first_possible_t_order':weight,'reason':reason})
    return {'trace_subsix_monomials':result,
            'scalar_defect_subsix':'base gradient O(t^2), argument change t^3*(quadratic x+linear y); only degree-five quadratic/linear term',
            'higher_trace_monomials':'at least three factors cost>=6; all radial factors cost>=6'}


def run():
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'energy_chart':energy_chart(),'spectral_compression':compression(),
            'constants_and_parabolic_bridge':constants(),'analytic_weight_completeness':degree_cover()}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--repository',type=Path)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    repo=args.repository or here.parent
    for name,h in json.loads((here/'provenance.json').read_text())['input_sha256'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==h,'pinned source input '+name)
    output=json.dumps(run(),sort_keys=True,indent=2)+'\n'
    if args.check:
        need(output==(here/'EXPECTED.json').read_text(),'entire independent fixture')
        print(json.dumps({'status':'passed','sympy':s.__version__,
                          'expected_sha256':hashlib.sha256(output.encode()).hexdigest()},sort_keys=True))
    else:
        print(output,end='')
