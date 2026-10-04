"""Independent full-parameter literal-factor / root-composition audit.

Written target formulas were exposed. Target executables and data were not.
Every equality compares every rational field/parameter coordinate.
"""
from fractions import Fraction as Q
from math import comb
import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import F, R, J, W, I, C, S, zproduct, zeval, zderivative, inverse_sqrt


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def equal(got, wanted, label):
    require(got == wanted, label)


def cube_coordinates(v):
    """Recover and check all 12 coordinates in the subfield Q[c]."""
    columns = [F(1), C, C*C]
    a = [[x.v[j] for x in columns]+[v.v[j]] for j in range(12)]
    row = 0
    for k in range(3):
        p = next(j for j in range(row, 12) if a[j][k])
        a[row], a[p] = a[p], a[row]
        d = a[row][k]
        a[row] = [x/d for x in a[row]]
        for j in range(12):
            if j != row and a[j][k]:
                d = a[j][k]
                a[j] = [x-d*y for x, y in zip(a[j], a[row])]
        row += 1
    q = [a[k][3] for k in range(3)]
    equal(sum((columns[k]*q[k] for k in range(3)), F()), v,
          'complete cubic-subfield reconstruction')
    return q


def physical_interval():
    lo, hi = Q(15, 16), Q(47, 50)
    f = lambda t: 8*t**3-6*t-1
    require(f(lo) < 0 < f(hi) and lo > Q(1, 2), 'initial root bracket')
    for _ in range(48):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def bound(v):
    q = cube_coordinates(v)
    lo, hi = physical_interval()
    a = b = Q(0)
    for j, x in enumerate(q):
        u, t = x*lo**j, x*hi**j
        a += min(u, t)
        b += max(u, t)
    return a, b


def ratio(q):
    return [q.numerator, q.denominator]


def audit(damage='none'):
    equal(W**12-W**6+1, F(), 'field polynomial')
    equal(W**18, F(-1), 'w^18=-1')
    equal(W**36, F(1), 'w^36=1')
    equal(I*I, F(-1), 'imaginary unit')
    equal(8*C**3-6*C-1, F(), 'physical cubic')
    equal(C*C+S*S, F(1), 'cosine/sine pair')
    r = R([0, 1])
    eta = J([0, 1])
    y = 1/(3*(1+C))
    x = F(Q(2, 3))-y
    H = 14*y
    k = -7*(1+2*C)/18
    rho = (C-5)/3
    d = 3*k+rho
    uz = -F(Q(37, 36))+20*C/9-20*C*C/9
    up = uz-rho*H/2
    alpha = -F(Q(527, 360))+41*C/90+13*C*C/90
    kappa = (k+rho)**2/2+10*alpha/27
    wstar = F(Q(2512, 27))+5840*C/9-21392*C*C/27
    dstar = -F(Q(4270, 27))-29492*C/27+4012*C*C/3
    gamma = F(Q(13, 36))+1253*C/72-50*C*C/3
    bstar = F(Q(2311, 108))+4934*C/27-1976*C*C/9
    tstar = -F(Q(60800959, 17496))-307083769*C/17496+10980067*C*C/486
    w2 = wstar/8
    mu0 = -F(Q(17403419, 34992))-45702565*C/17496+180635*C*C/54
    mu2 = F(Q(35, 81))-2086*C/81+616*C*C/27
    beta0 = -F(Q(1162307, 23328))-5484833*C/11664+52426519*C*C/93312
    beta2 = F(Q(14537, 1512))-3889*C/756-1661*C*C/756
    beta4 = -F(Q(2, 49))-4*C/49-2*C*C/49
    nu1 = -F(Q(17983, 972))-25711*C/486+4564*C*C/81
    nu3 = F(Q(28, 81))+56*C/81
    sigma1 = -F(Q(1967, 81))+5479*C/432-5375*C*C/162
    sigma3 = -F(Q(55, 189))+11*C/63+88*C*C/189
    if damage == 'mu':
        mu2 += 1
    if damage == 'nu':
        nu1 += 1
    if damage == 'sigma':
        sigma1 += 1
    mu = R(mu0)+(r*r)*mu2
    beta = R(beta0)+(r*r)*beta2+(r**4)*beta4
    nu = r*nu1+(r**3)*nu3
    sigma = r*sigma1+(r**3)*sigma3
    q1 = R(gamma)-(r*r)*(4/(3*H))
    if damage == 'q1':
        q1 = R(gamma)
    v2 = r*(3*k*H/7)
    acrit = J([0, R(uz)-r*(I/3), R(w2)+v2*I, mu+nu*I])
    bcrit = J([0, R(up)+r*I, R(w2)+v2*I, mu+nu*I])
    splitting = r*d
    if damage == 'split':
        splitting = R()
    kval = J([I, q1*I+splitting, beta*I+sigma])
    # Full z product from the literal derivative, not power sums.
    derivative = [J(1)]
    for _ in range(6):
        derivative = zproduct(derivative, [-acrit, J(1)])
    pair = [bcrit*bcrit-eta*(H/2)*kval*kval, -2*bcrit, J(1)]
    derivative = [9*v for v in zproduct(derivative, pair)]
    equal(len(derivative), 9, 'degree eight derivative including six copies')
    primitive = [J()]+[v/(j+1) for j, v in enumerate(derivative)]
    anchor = 1-eta
    if damage == 'anchor':
        anchor = 1-2*eta
    primitive[0] = -zeval(primitive, anchor)
    equal(zeval(primitive, 1-eta), J(), 'exact marked anchor through eta3')
    equal(primitive[9], J(1), 'monic degree nine')
    for j in range(10):
        equal(primitive[j].v[0], R((j == 9)-(j == 0)), 'entire base polynomial')
    coefficients = [[primitive[j].v[n] for j in range(10)] for n in range(4)]
    g2 = [R()] * 10
    g2[0], g2[7], g2[8] = R(9-9*x-9*y), R(9*y), R(9*x)
    for j in range(10):
        equal(coefficients[1][j], g2[j], 'entire eta coefficient')
    g40 = [R()] * 10
    g40[8] = R(-9*wstar/8)
    g40[7] = R(9*(64*x*x-dstar)/14)
    g40[6] = R(6*x*H+3*H*up/2)
    g40[0] = R(-36+72*x+9*H/2)-sum(g40[1:], R())
    qpoly = [R()] * 10
    qpoly[8] = qpoly[7] = R(I*(1+2*C)/2)
    qpoly[6] = R(I/2)
    qpoly[0] = -sum(qpoly[1:], R())
    for j in range(10):
        equal(coefficients[2][j], g40[j]+qpoly[j]*r*(3*H), 'entire skew quartic jet')
    roots, normals, shift, squared = [], [], [], []
    norms_expected = {0:F(-1), 1:-(2+4*C-4*C*C)/3,
                      2:-(2*C-1)**2/3, 3:F(), 4:F(), 5:F(), 6:F(),
                      7:-(2*C-1)**2/3, 8:-(2+4*C-4*C*C)/3}
    for j in range(9):
        omega = W**(4*j)
        z = J(omega)
        # Solve each full coefficient equation by composing p(Z),
        # using only the original simple derivative 9*omega^8.
        inverse_derivative = (omega.conjugate()**8)/9
        for n in range(1, 4):
            residual = zeval(primitive, z).v[n]
            v = list(z.v)
            v[n] = -residual*inverse_derivative
            z = J(v)
        equal(zeval(primitive, z), J(), 'all four composed equations for root '+str(j))
        L = -omega/3-x-y*omega.conjugate()
        equal(z.v[1], R(L), 'first drift '+str(j))
        fixed = -(zeval(g40, omega)
                  +zeval(zderivative(g2), omega)*L+36*(omega**7)*L*L)*inverse_derivative
        harmonic = I*( (3+4*C)*omega-(1+2*C)*(1+omega.conjugate())
                        -omega.conjugate()**2)/18
        equal(z.v[2], fixed+r*(3*H)*harmonic, 'complete quadratic drift '+str(j))
        njet = (z*z.conjugate()-1)/2
        equal(njet.v[0], R(), 'unit limiting original '+str(j))
        equal(njet.v[1], R(norms_expected[j]), 'first individual half-normal '+str(j))
        if j in [3, 4, 5, 6]:
            equal(njet.v[2], R(), 'second individual active half-normal '+str(j))
            equal(njet.v[3], R(), 'third individual active half-normal '+str(j))
        # The epsilon7 coefficient comes from translating ALL critical
        # factors: -9(z8-1). Recompose its root linear response.
        response = (omega**8-1)*(omega.conjugate()**8)
        equal(response, 1-omega, 'all-nine seventh-order root response '+str(j))
        halfnormal7 = (response/omega).real()
        equal(halfnormal7, (omega-1).real(), 'seventh-order individual normal '+str(j))
        if j in [3, 6]:
            equal(halfnormal7, F(Q(-3, 2)), 'active seventh coefficient '+str(j))
        if j in [4, 5]:
            equal(halfnormal7, -1-C, 'active seventh coefficient '+str(j))
        if damage == 'shift' and j == 3:
            require(bound(-halfnormal7)[1] < 0, 'reversed shift fails containment')
        roots.append(z.record())
        normals.append(njet.record())
        shift.append({'root':response.record(), 'half_normal':halfnormal7.record()})
        ds = fixed.v[0]
        squared.append([ (ds*ds.conjugate()).real(),
                         (ds*harmonic.conjugate()+harmonic*ds.conjugate()).real(),
                         (harmonic*harmonic.conjugate()).real() ])
    # Direct squared critical distances, not the displayed target t_j.
    dist_a = (1-eta-acrit)*(1-eta-acrit).conjugate()
    center = 1-eta-bcrit
    V = center*center.conjugate()+eta*(H/2)*kval*kval.conjugate()
    cross_real = (center*kval.conjugate()).real()
    X2 = eta*(2*H)*cross_real*cross_real
    equal(X2.v[0], R(), 'pair squared splitting starts late0')
    equal(X2.v[1], R(), 'pair squared splitting starts late1')
    equal(X2.v[2], R(), 'pair squared splitting starts late2')
    objective = 6*inverse_sqrt(dist_a)+2*inverse_sqrt(V)+X2*Q(3, 4)
    if damage == 'cost-split':
        objective = 6*inverse_sqrt(dist_a)+2*inverse_sqrt(V)
    wanted = J([8, F(Q(8, 3))+y, bstar, R(tstar)+(r*r)*(9*H*kappa)])
    equal(objective, wanted, 'complete first-power objective including every r power')
    # Cubic imaginary critical sum, with six repeated points and pair.
    cubic = 6*acrit.imag()**3+2*bcrit.imag()**3+3*H*eta*bcrit.imag()*kval.imag()**2
    equal(cubic.v[0], R(), 'cubic skew zero-order')
    equal(cubic.v[1], R(), 'cubic skew first-order')
    equal(cubic.v[2], r*(3*H), 'whole actual leading cubic skew')
    # All four independent defining-variable response rows, not averages.
    responses = []
    for j in [3, 4, 5, 6]:
        omega = W**(4*j)
        sin1 = omega.imag()
        row = [ (omega-1).real(), (1-omega**2).real()*H/7,
                sin1, (omega**2).imag()*H/7 ]
        perturbations = [ -9*(omega**8-1), 9*H*(omega**7-1)/7,
                          -9*I*(omega**8-1), -9*I*H*(omega**7-1)/7 ]
        for col in range(4):
            direct = (-perturbations[col]*(omega.conjugate()**8)/9/omega).real()
            equal(direct, row[col], 'full defining-variable sensitivity '+str(j)+','+str(col))
        responses.append([v.record() for v in row])
    det_even = (-F(Q(3, 2)))*(2-2*C*C)*H/7+(1+C)*3*H/14
    det_odd = -H*(2*C-1)/7
    equal(det_even, 2*C-1, 'even repair determinant')
    equal(det_odd, H*(1-2*C)/7, 'odd repair determinant')
    # Derive all nine squared affine norms and prove entire real-line
    # winner domination with exact physical coefficient signs.
    AA = -F(Q(13638695, 972))-16011613*C/243+20901119*C*C/243
    BM_over_s = (1448+6982*C-8224*C*C)/243
    QQ = (8+25*C+20*C*C)/162
    equal(squared[7][0], AA, 'motion constant A')
    equal(squared[7][1], S*BM_over_s, 'motion positive linear coefficient')
    equal(squared[7][2], QQ, 'motion quadratic coefficient')
    for j in range(1, 5):
        other = 9-j
        equal(squared[j][0], squared[other][0], 'all reflected squared constant')
        equal(squared[j][1], -squared[other][1], 'all reflected cross terms')
        equal(squared[j][2], squared[other][2], 'all reflected square terms')
    signs = {'H':H,'minus-alpha':-alpha,'kappa':kappa,
             'even-determinant':2*C-1,'minus-odd-determinant':-det_odd,
             'minus-Tstar-minus18':-tstar-18,'Tstar-plus19':tstar+19,
             'motion-A':AA, 'motion-B-over-s':BM_over_s, 'motion-Q':QQ}
    for j in [0, 1, 2]:
        signs['minus-first-normal'+str(j)] = -norms_expected[j]
    for j in [0, 1, 3, 4]:
        signs['constant-dominance'+str(j)] = AA-squared[j][0]
        signs['quadratic-dominance'+str(j)] = QQ-squared[j][2]
        bj = squared[j][1]/S
        signs['cross-plus-dominance'+str(j)] = BM_over_s+bj
        signs['cross-minus-dominance'+str(j)] = BM_over_s-bj
    bounds = {}
    for name, v in signs.items():
        lo, hi = bound(v)
        require(lo > 0, 'positive physical bound '+name)
        bounds[name] = {'cubic':list(map(ratio,cube_coordinates(v))),
                        'lower':ratio(lo),'upper':ratio(hi)}
    return {'schema':1, 'field':'Q[w]/(w^12-w^6+1), w=exp(i*pi/18)',
            'parameter':'whole unrestricted real r polynomial',
            'derivative_z_columns':[v.record() for v in derivative],
            'anchored_polynomial_z_columns':[v.record() for v in primitive],
            'all_nine_root_eta_jets':roots, 'all_nine_half_normal_eta_jets':normals,
            'all_nine_epsilon7_responses':shift,
            'all_four_individual_repair_rows':responses,
            'all_nine_squared_affine_norms':[[v.record() for v in row] for row in squared],
            'first_power_objective':objective.record(), 'actual_cubic_skew':cubic.record(),
            'squared_critical_distances':{'six_equal':dist_a.record(),
                                         'pair_center':V.record(),'pair_split_square':X2.record()},
            'positive_physical_bounds':bounds,
            'physical_cosine_interval':list(map(ratio,physical_interval()))}


def canonical(record):
    return json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()+b'\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    ap.add_argument('--damage', choices=['none','mu','nu','sigma','q1','split','anchor','shift','cost-split'], default='none')
    args = ap.parse_args()
    try:
        data = canonical(audit(args.damage))
    except (ArithmeticError, ValueError, TypeError, ZeroDivisionError) as exc:
        print('REJECT: '+str(exc), file=sys.stderr)
        sys.exit(2)
    if args.output:
        args.output.write_bytes(data)
    print(json.dumps({'verdict':'PASS','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                      'root_labels':9,'individual_active_roots':4,'unrestricted_parameter':True},sort_keys=True))
