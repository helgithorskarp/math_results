#!/usr/bin/env python3
"""Exact finite curvature audit for the raw-coordinate half-gap obstruction.

This verifies the joint eta^3/delta^2 jet and its real embedding. The
existence of an exact disk-root family, analytic division and transport
to the true minimum are ordinary written mathematics in PROOF.md.
No previous checker, fixture, or analytic theorem is imported.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


ar = load('arithmetic')
sr = load('series')
K, Z, require, AlgebraError = ar.K, ar.Z, ar.require, ar.AlgebraError


class Audit:
    def __init__(self):
        self.checks = []
        self.damages = []

    def check(self, ok, label):
        require(ok, label)
        self.checks.append(label)

    def reject(self, function, label):
        try:
            function()
        except AlgebraError:
            self.damages.append(label)
        else:
            raise AlgebraError('mathematical damage accepted: ' + label)


def constants():
    c = K((0, 1, 0))
    d = 2*c*c - 1
    y = 1/(3*(1+c))
    H = 14*y
    U = -8*(F(2, 3)-y)
    rho = (c-5)/3
    uz = (U+rho*H)/8
    up = (U-6*uz)/2
    w4 = 1/(c+d)
    w3 = F(2, 3)*(7-(1-d)*w4)
    v = 2*d*d-1
    sigma = F(3, 8)-(F(3, 2)*w3+(1-v)*w4)/20
    K0 = K((-F(2609, 405), -F(2000, 81), F(12964, 405)))
    Bstar = K((F(2311, 108), F(4934, 27), -F(1976, 9)))
    C3 = K((-F(60800959, 17496), -F(307083769, 17496), F(10980067, 486)))
    ell = K((-F(4441, 540), F(7046, 135), -F(2288, 45)))
    return locals()


def evaluate(poly, value):
    result = type(value)(0)
    for row in reversed(poly):
        result = result*value+row
    return result


def factor_integrate(eta, small, pair, opening):
    """Definition-level derivative factor multiplication and exact anchoring."""
    S = type(eta)
    factors = [[-eta*u, S(1)] for u in small]
    factors.append([(eta*pair)**2+eta*opening, -2*eta*pair, S(1)])
    derivative = [S(9)]
    for factor in factors:
        out = [S(0) for _ in range(len(derivative)+len(factor)-1)]
        for i, x in enumerate(derivative):
            for j, y in enumerate(factor):
                out[i+j] += x*y
        derivative = out
    poly = [S(0)] + [value*F(1, j+1) for j, value in enumerate(derivative)]
    poly[0] -= evaluate(poly, 1-eta)
    return poly, derivative


def circle(poly, t):
    """Imaginary/sine quotient and real evaluation on the unit circle."""
    S = type(t)
    U = [S(1), 2*t]
    T = [S(1), t]
    for j in range(2, 10):
        U.append(2*t*U[-1]-U[-2])
        T.append(2*t*T[-1]-T[-2])
    imaginary = sum((poly[j]*U[j-1] for j in range(1, 10)), S(0))
    real = sum((poly[j]*T[j] for j in range(10)), S(0))
    return imaginary, real


def complex_root(poly, cosine, q, sine, audit, index):
    """Actual complex residual root; no Chebyshev equations are used here."""
    zcoef = lambda v: Z(v, q=q)
    Dz = sr.series_ring(2, zcoef)
    Ez = sr.series_ring(3, Dz)
    omega = Z((cosine, 0, 0, sine), q=q)
    audit.check(omega**9 == 1, 'independent ninth root k' + str(index))
    audit.check(omega*omega.conj() == 1, 'unit reference root k' + str(index))
    coefficients = [Ez([Dz([zcoef(v) for v in row.a]) for row in p.a]) for p in poly]
    root = Ez(omega)
    for n in range(1, 4):
        residual = evaluate(coefficients, root)
        # p_0'(omega)=9 omega^8 and omega^9=1, so its inverse is omega/9.
        root = root.with_coefficient(n, -Dz(omega)*residual.a[n]*F(1, 9))
        audit.check(all(v == 0 for v in evaluate(coefficients, root).a[:n+1]),
                    'complete direct root residual through eta' + str(n) + ' k' + str(index))
    conjugate = Ez([Dz([v.conj() for v in row.a]) for row in root.a])
    radius = (root*conjugate-1)*F(1, 2)
    audit.check(radius == 0, 'all actual half-radials eta3/delta2 vanish k' + str(index))
    real_rows = []
    for n, row in enumerate(root.a):
        real_values = []
        for m, v in enumerate(row.a):
            real = (v+v.conj())*F(1, 2)
            audit.check(all(a == 0 for a in real.a[1:]),
                        'actual root abscissa descends k' + str(index) + ' eta' + str(n) + ' delta' + str(m))
            real_values.append(real.a[0])
        real_rows.append(tuple(real_values))
    return root, radius, tuple(real_rows), coefficients


def embedding():
    lo, hi = F(3, 4), F(1)
    f = lambda x: 8*x*x*x-6*x-1
    require(f(lo) < 0 < f(hi), 'initial real embedding bracket')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    require(f(lo) < 0 < f(hi) and 24*lo*lo > 6,
            'unique largest real cubic root in the rational bracket')
    return lo, hi


def run():
    audit = Audit()
    C = constants()
    c, d = C['c'], C['d']
    lo, hi = embedding()
    audit.check(8*c**3-6*c-1 == 0, 'exact cubic defining relation')
    audit.check(C['H'].interval(lo, hi)[0] > 0, 'positive conjugate pair opening')
    D = sr.series_ring(2, K)
    S = sr.series_ring(3, D)
    eta = S([0, 1])
    small = [S(D([C['uz'], 1])), S(D([C['uz'], -1]))] + [S(C['uz']) for _ in range(4)]
    pair = S((D(C['U'])-sum((x.a[0] for x in small), D(0)))/2)
    opening = S(C['H']/2)
    ts = [S(-F(1, 2)), S(-c)]
    A = [D(F(3, 2)), D(1+c)]
    B = [D(F(3, 2)), D(1-d)]
    M = [[a*F(9, 4), -b*F(9, 7)] for a, b in zip(A, B)]
    determinant = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    normal_det = 3*(c+d)/56
    audit.check(determinant == 81*D(normal_det), 'unscaled versus scaled two-normal determinant')
    audit.check(normal_det.interval(lo, hi)[0] > 0, 'nonzero positive scaled normal determinant')
    inactive = []
    for index, cosine in [(1, d), (2, 2*d*d-1)]:
        slope = -1-(1-cosine)*C['U']/8+(1-(2*cosine*cosine-1))*C['H']/14
        audit.check(slope.interval(lo, hi)[1] < 0,
                    'strict inactive original-root half-radial slope k' + str(index))
        inactive.append({'index': index, 'slope': slope.record()})
    phase = [D(-9)/(1-t.a[0]*t.a[0]) for t in ts]
    trace = []
    for j in range(1, 4):
        poly, _ = factor_integrate(eta, small, pair, opening)
        residuals = [circle(poly, t)[1].a[j] for t in ts]
        if j == 1:
            audit.check(all(x == 0 for x in residuals), 'complete leading actual-unit-root normals')
        else:
            pair = pair.with_coefficient(j-1,
                (-residuals[0]*M[1][1]+residuals[1]*M[0][1])/determinant)
            opening = opening.with_coefficient(j-1,
                (-M[0][0]*residuals[1]+M[1][0]*residuals[0])/determinant)
            poly, _ = factor_integrate(eta, small, pair, opening)
        for k in range(2):
            ts[k] = ts[k].with_coefficient(j, -circle(poly, ts[k])[0].a[j]/phase[k])
        for k, t in enumerate(ts):
            imaginary, real = circle(poly, t)
            audit.check(all(imaginary.a[n] == 0 for n in range(j+1)),
                        'all joint phase coefficients through eta' + str(j) + ' k' + str(k+3))
            audit.check(all(real.a[n] == 0 for n in range(j+1)),
                        'all joint unit-root coefficients through eta' + str(j) + ' k' + str(k+3))
        trace.append({'order': j, 'pair': pair.a[j-1].record(),
            'opening': opening.a[j-1].record(), 't3': ts[0].a[j].record(),
            't4': ts[1].a[j].record()})
    poly, derivative = factor_integrate(eta, small, pair, opening)
    audit.check(poly[9] == 1, 'monic original polynomial')
    audit.check(evaluate(poly, 1-eta) == 0, 'exact marked-root anchoring eta3/delta2')
    audit.check(all((j+1)*poly[j+1] == derivative[j] for j in range(9)),
                'integrated polynomial has the eight prescribed critical points')
    cost = sum(((1-eta*(1+u)).inv() for u in small), S(0))
    pair_distance = (1-eta*(1+pair))**2+eta*opening
    cost += 2*sr.binomial_series(pair_distance, F(-1, 2))
    audit.check(cost.a[0] == 8, 'constant objective eight')
    audit.check(cost.a[1] == F(8, 3)+C['H']/14, 'prior first objective coefficient reproduced')
    audit.check(cost.a[2].a == (C['Bstar'], K(0), K(1)),
                'complete centered-real second cost Bstar+delta squared')
    audit.check(cost.a[3].a[0] == C['C3'], 'prior cubic value reproduced')
    audit.check(cost.a[3].a[1] == 0, 'cubic objective evenness')
    audit.check(cost.a[3].a[2] == C['ell'], 'displayed exact eta3 delta2 coefficient')
    bounds = C['ell'].interval(lo, hi)
    audit.check(F(-4075854243, 10**9) < bounds[0] <= bounds[1] < F(-4075854241, 10**9),
                'certified negative curvature enclosure')
    audit.check(bounds[1] < 0, 'first weak-curvature correction strictly negative')

    # The attributed limiting cost is a degree-two polynomial in the six
    # small real coordinates on hsmall=0. This check includes a variable
    # common coordinate, not just its minimizing value.
    X = sr.series_ring(2, D)
    common = X([C['uz'], 1])
    delta = X(D([0, 1]))
    small_u = [common+delta, common-delta]+[common for _ in range(4)]
    big_u = (X(C['U'])-sum(small_u, X(0)))/2
    leading = X(C['K0'])+sum((u*u*F(1, 2) for u in small_u), X(0))+big_u**2
    leading += big_u*C['rho']*C['H']+X(C['sigma']*C['H']**2/2)
    expected_leading = X(C['Bstar'])+12*X([0, 1])**2+delta**2
    audit.check(leading == expected_leading,
                'full leading cost for all common real coordinates and centered splits')
    norm = sum(((u-common)**2 for u in small_u), X(0))
    audit.check(norm == 2*delta**2, 'literal raw twelve-free-coordinate distance is twice delta squared')

    roots = []
    for index, cosine, q, sine in [(3, K(-F(1, 2)), K(3), F(1, 2)),
                                   (4, -c, 1-c*c, F(1))]:
        root, radius, real, coefficients = complex_root(poly, cosine, q, sine, audit, index)
        audit.check(real == tuple(row.a for row in ts[index-3].a),
                    'actual root abscissa equals solved unit-circle phase k' + str(index))
        roots.append({'index': index, 'root': root.record(), 'half_radial': radius.record()})
        if index == 4:
            final_root, final_radius, final_coefficients = root, radius, coefficients

    audit.reject(lambda: require(cost.a[3].a[2] == C['ell']+1, 'changed curvature coefficient'),
                 'unit change in first curvature correction')
    audit.reject(lambda: require(cost.a[2].a[2] == F(1, 2), 'wrong leading split value'),
                 'half the true centered-split leading value')
    audit.reject(lambda: require(norm == delta**2, 'wrong raw distance normalization'),
                 'lost factor two in raw free-coordinate distance')
    audit.reject(lambda: require(evaluate(poly, 1-2*eta) == 0, 'wrong marked-root anchor'),
                 'wrong marked original root')
    audit.reject(lambda: require(-normal_det == 3*(c+d)/56, 'reversed normal determinant'),
                 'reversed scaled normal determinant')
    bad_pair = pair.with_coefficient(2, pair.a[2]+D([0, 0, 1]))
    bad_poly, _ = factor_integrate(eta, small, bad_pair, opening)
    audit.reject(lambda: require(circle(bad_poly, ts[0])[1] == 0, 'damaged pair correction'),
                 'changed eta2 delta2 pair normal correction')
    Ez, Dz = type(final_root), type(final_root.a[0])
    zcoef = lambda v: Z(v, q=1-c*c)
    bad_root = final_root.with_coefficient(3, final_root.a[3]+Dz([0, 0, zcoef(1)]))
    audit.reject(lambda: require(evaluate(final_coefficients, bad_root) == 0, 'damaged complex root'),
                 'changed eta3 delta2 actual complex root')
    badphase = ts[1].with_coefficient(0, D(c))
    audit.reject(lambda: require(circle(poly, badphase)[1].a[0] == 0, 'wrong original-root branch'),
                 'wrong fourth original-root branch')

    return {'agent': 'six-sendov-3', 'role': 'researcher',
        'exact_checks': audit.checks, 'rejected_mathematical_damages': audit.damages,
        'objective_eta_delta_jet': cost.record(),
        'parameters': {'pair': pair.record(), 'opening': opening.record(),
                       't3': ts[0].record(), 't4': ts[1].record()},
        'normal_trace': trace, 'scaled_normal_determinant': normal_det.record(),
        'embedding_interval': [str(lo), str(hi)],
        'ell': C['ell'].record(), 'ell_interval': [str(x) for x in bounds],
        'variable_common_leading_cost': leading.record(), 'raw_free_distance': norm.record(),
        'active_actual_complex_roots': roots, 'inactive_first_half_radials': inactive}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', type=Path, default=BASE/'expected.json')
    parser.add_argument('--emit-fixture', type=Path)
    args = parser.parse_args()
    actual = run()
    if args.emit_fixture is not None:
        args.emit_fixture.write_text(json.dumps(actual, indent=2)+'\n')
    else:
        expected = json.loads(args.fixture.read_text())
        require(canonical(actual) == canonical(expected), 'complete frozen fixture including JSON types')
    print('PASS', len(actual['exact_checks']), 'exact checks;',
          len(actual['rejected_mathematical_damages']), 'mathematical damages rejected; full-record SHA256',
          sha256(canonical(actual)).hexdigest())


if __name__ == '__main__':
    main()
