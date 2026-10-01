#!/usr/bin/env python3
"""Independent rational-circle reconstruction of Sendov claim 9033.

No researcher code is imported. Author fixtures are optional cross-comparison
inputs; ordinary analytic existence/global coverage remain outside this code.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('half_endpoint_exact', BASE/'exact.py')
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)
E, J, Z, require, binomial = ex.E, ex.J, ex.Z, ex.require, ex.binomial
ETA, DELTA = J.term(1, 0), J.term(0, 1)


class Audit:
    def __init__(self):
        self.checks, self.damages = [], []
    def check(self, ok, label):
        require(ok, label)
        self.checks.append(label)
    def reject(self, function, label):
        try:
            function()
        except ValueError:
            self.damages.append(label)
        else:
            raise ValueError('mathematical damage accepted: '+label)


def constants():
    c = E([0, 1])
    d = 2*c*c-1
    y0 = 1/(3*(1+c))
    H, U = 14*y0, -8*(F(2, 3)-y0)
    rho = (c-5)/3
    uz = (U+rho*H)/8
    B = E([F(2311, 108), F(4934, 27), -F(1976, 9)])
    C3 = E([-F(60800959, 17496), -F(307083769, 17496), F(10980067, 486)])
    ell = E([-F(4441, 540), F(7046, 135), -F(2288, 45)])
    return locals()


def evaluate(poly, z):
    out = Z(q=z.q) if isinstance(z, Z) else J(0)
    for a in reversed(poly):
        out = out*z+a
    return out


def multiply(a, b):
    out = [J(0) for _ in range(len(a)+len(b)-1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def primitive(small, pair, opening):
    derivative = [J(9)]
    for u in small:
        derivative = multiply(derivative, [-ETA*u, J(1)])
    derivative = multiply(derivative, [(ETA*pair)**2+ETA*opening, -2*ETA*pair, J(1)])
    poly = [J(0)]+[a*F(1, k+1) for k, a in enumerate(derivative)]
    poly[0] = -evaluate(poly, 1-ETA)
    return poly, derivative


def circle(t, q, phase):
    """omega*(1+i sin(theta)*phase)/(1-i sin(theta)*phase)."""
    denominator = (1+q*phase**2).inv()
    return Z(t, 1, q)*Z((1-q*phase**2)*denominator, 2*phase*denominator, q)


def family(common, vector, checks, prefix):
    C = constants()
    c, d = C['c'], C['d']
    require(len(vector) == 6 and sum(vector) == 0, 'literal six-coordinate centered vector')
    small = [J(common)+v*DELTA for v in vector]
    pair, opening = J((C['U']-6*common)/2), J(C['H']/2)
    bases = [(-F(1, 2), E(F(3, 4))), (-c, 1-c*c)]
    phases = [J(0), J(0)]
    leading_poly, _ = primitive(small, pair, opening)
    # Derive both normal columns from literal anchored polynomial evaluations.
    normals = []
    for t, q in bases:
        root = circle(t, q, J(0))
        value = evaluate(leading_poly, root).real.at(1)
        shifted_y = evaluate(primitive(small, pair+1, opening)[0], root).real.at(1)-value
        shifted_Y = evaluate(primitive(small, pair, opening+1)[0], root).real.at(1)-value
        normals.append((shifted_y, shifted_Y))
    expected_normals = [(E(F(27, 8)), E(-F(27, 14))), (9*(1+c)/4, -9*(1-d)/7)]
    checks.check(normals == expected_normals, prefix+' literal two normal columns')
    determinant = normals[0][0]*normals[1][1]-normals[1][0]*normals[0][1]
    checks.check(determinant == 243*(c+d)/56, prefix+' actual normal determinant')
    trace = []
    for n in range(1, 4):
        poly, _ = primitive(small, pair, opening)
        roots = [circle(t, q, phase) for (t, q), phase in zip(bases, phases)]
        residual = [evaluate(poly, root) for root in roots]
        if n == 1:
            checks.check(all(r.real.at(n, m) == 0 for r in residual for m in range(3)), prefix+' leading zero real normals')
        else:
            for m in range(3):
                r, s = residual[0].real.at(n, m), residual[1].real.at(n, m)
                dy = (-r*normals[1][1]+s*normals[0][1])/determinant
                dY = (-normals[0][0]*s+normals[1][0]*r)/determinant
                pair += J.term(n-1, m, dy)
                opening += J.term(n-1, m, dY)
            poly, _ = primitive(small, pair, opening)
        for k, (t, q) in enumerate(bases):
            root = circle(t, q, phases[k])
            residual_imag = evaluate(poly, root).imag
            phases[k] += sum((J.term(n, m, -residual_imag.at(n, m)/18) for m in range(3)), J(0))
        roots = [circle(t, q, phase) for (t, q), phase in zip(bases, phases)]
        for k, root in enumerate(roots):
            residual = evaluate(poly, root)
            checks.check(all(residual.real.at(i,m) == 0 and residual.imag.at(i,m) == 0
                             for i in range(n+1) for m in range(3)), prefix+' complete root constraints eta'+str(n)+' k'+str(k+3))
            checks.check(root*root.conj() == 1, prefix+' identity unit radius eta'+str(n)+' k'+str(k+3))
        trace.append({'order': n, 'pair': [pair.at(n-1,m).record() for m in range(3)],
                      'opening': [opening.at(n-1,m).record() for m in range(3)],
                      't3': [roots[0].real.at(n,m).record() for m in range(3)],
                      't4': [roots[1].real.at(n,m).record() for m in range(3)]})
    poly, derivative = primitive(small, pair, opening)
    checks.check(poly[9] == 1 and evaluate(poly, 1-ETA) == 0, prefix+' monic exact marked-root anchor')
    checks.check(all((j+1)*poly[j+1] == derivative[j] for j in range(9)), prefix+' original polynomial derivative equals eight critical factors')
    cost = sum(((1-ETA*(1+u)).inv() for u in small), J(0))
    cost += 2*binomial((1-ETA*(1+pair))**2+ETA*opening, F(-1, 2))
    norm2 = sum((v*v for v in vector), 0)
    checks.check(cost.at(0) == 8 and cost.at(1) == F(8, 3)+C['y0'], prefix+' constant and first coefficients')
    checks.check(cost.at(2) == C['B']+12*(common-C['uz'])**2 and cost.at(2,1) == 0 and cost.at(2,2) == F(norm2, 2), prefix+' complete second objective coefficient')
    checks.check(pair.at(1,2) == 0 and opening.at(1,2) == F(norm2, 2), prefix+' all-common centered normal correction')
    if common == C['uz']:
        checks.check(cost.at(3) == C['C3'] and cost.at(3,1) == 0 and cost.at(3,2) == C['ell']*F(norm2, 2), prefix+' cubic baseline and normalized centered curvature')
    return {'cost': cost, 'pair': pair, 'opening': opening, 'roots': roots,
            'phases': phases, 'trace': trace, 'poly': poly, 'small': small,
            'norm2': norm2, 'determinant': determinant}


def run():
    audit, C = Audit(), constants()
    c = C['c']
    audit.check(8*c**3-6*c-1 == 0, 'cubic defining relation')
    candidates = {F(sign, 2**k) for sign in (-1,1) for k in range(4)}
    audit.check(all(8*x**3-6*x-1 != 0 for x in candidates), 'rational root test and cubic irreducibility')
    for element in (c, 1+c, 2*c*c-1, C['ell']):
        audit.check(element*element.inv() == 1, 'extended Euclid field inverse '+str(element.record()))
    lo, hi = F(3,4), F(1)
    polynomial = lambda x: 8*x**3-6*x-1
    for _ in range(96):
        mid = (lo+hi)/2
        if polynomial(mid) < 0:
            lo = mid
        else:
            hi = mid
    audit.check(polynomial(lo)<0<polynomial(hi) and 24*lo*lo>6, 'unique positive embedding isolator')
    bounds = C['ell'].interval(lo, hi)
    audit.check(F(-4075854243,10**9) < bounds[0] <= bounds[1] < F(-4075854241,10**9), 'certified strictly negative curvature enclosure')
    audit.check(C['H'].interval(lo,hi)[0] > 0 and (3*(c+C['d'])/56).interval(lo,hi)[0] > 0, 'positive opening and invertible two normal equations')
    v = (1,-1,0,0,0,0)
    main = family(C['uz'], v, audit, 'split')
    shifted = [family(C['uz']+shift, v, audit, 'common'+str(shift)) for shift in (-1,1)]
    # Degree <=2 in common is justified in REVIEW.md, so these are complete
    # polynomial interpolation, not a finite feasibility sample.
    audit.check((shifted[1]['cost'].at(2)-shifted[0]['cost'].at(2))/2 == 0 and
                (shifted[1]['cost'].at(2)+shifted[0]['cost'].at(2)-2*main['cost'].at(2))/2 == 12,
                'complete degree-two common-coordinate interpolation')
    directions = [(0,0,1,0,-1,0), (1,1,-2,0,0,0), (1,2,3,-1,-2,-3)]
    controls = []
    for vector in directions:
        result = family(C['uz'], vector, audit, 'vector'+str(vector))
        controls.append({'vector': list(vector), 'squared_norm': result['norm2'],
                         'eta2_delta2': result['cost'].at(2,2).record(),
                         'eta3_delta2': result['cost'].at(3,2).record()})
    norm = sum(((u-C['uz'])**2 for u in main['small']), J(0))
    audit.check(norm == 2*DELTA**2, 'literal raw twelve-coordinate squared distance')
    inactive = []
    for index, t in [(1, C['d']), (2, 2*C['d']**2-1)]:
        slope = -1-(1-t)*C['U']/8+(1-(2*t*t-1))*C['H']/14
        audit.check(slope.interval(lo,hi)[1] < 0, 'strict inactive original-root radial slope '+str(index))
        inactive.append({'index':index, 'slope':slope.record()})
    main_poly = main['poly']
    audit.reject(lambda: require(evaluate(main_poly, 1-2*ETA) == 0, 'wrong marked root'), 'changed marked original-root anchor')
    audit.reject(lambda: require(main['cost'].at(3,2) == C['ell']+1, 'wrong curvature'), 'changed first curvature correction')
    audit.reject(lambda: require(norm == DELTA**2, 'wrong raw norm'), 'lost raw distance factor two')
    audit.reject(lambda: require(main['determinant'] == -243*(c+C['d'])/56, 'wrong determinant'), 'reversed normal determinant')
    badpoly = primitive(main['small'], main['pair']+ETA**2*DELTA**2, main['opening'])[0]
    audit.reject(lambda: require(evaluate(badpoly, main['roots'][0]) == 0, 'wrong pair correction'), 'changed pair eta2 delta2 coefficient')
    badpoly = primitive(main['small'], main['pair'], main['opening']+ETA**2*DELTA**2)[0]
    audit.reject(lambda: require(evaluate(badpoly, main['roots'][1]) == 0, 'wrong opening correction'), 'changed opening eta2 delta2 coefficient')
    badroot = circle(-c, 1-c*c, main['phases'][1]+ETA**3*DELTA**2)
    audit.reject(lambda: require(evaluate(main_poly, badroot) == 0, 'wrong phase'), 'changed rational phase eta3 delta2 coefficient')
    badroot = circle(c, 1-c*c, main['phases'][1])
    audit.reject(lambda: require(evaluate(main_poly, badroot) == 0, 'wrong active root branch'), 'changed fourth original-root branch')
    audit.reject(lambda: require(main['cost'].at(2,2) == F(1,2), 'wrong split coefficient'), 'half leading centered split cost')
    audit.reject(lambda: E(0).inv(), 'zero field inverse')
    audit.reject(lambda: ETA.inv(), 'nonunit flat jet inverse')
    audit.reject(lambda: J({(4,0):1}), 'out-of-domain flat jet degree')
    audit.reject(lambda: E(True), 'malformed field boolean')
    zero = E(0).record()
    expected_common = [[C['B'].record(),zero,E(1).record()], [zero,zero,zero], [E(12).record(),zero,zero]]
    expected_norm = [[zero,zero,E(2).record()], [zero,zero,zero], [zero,zero,zero]]
    roots = []
    for k, root in enumerate(main['roots']):
        sine_scale = F(1,2) if k == 0 else F(1)
        roots.append({'index':k+3, 'root':root.author_record(sine_scale), 'half_radial':Z(q=root.q).author_record(sine_scale)})
    shared = {'objective_eta_delta_jet': main['cost'].record(),
              'parameters': {'pair':main['pair'].record(), 'opening':main['opening'].record(),
                             't3':main['roots'][0].real.record(), 't4':main['roots'][1].real.record()},
              'normal_trace':main['trace'], 'scaled_normal_determinant':(3*(c+C['d'])/56).record(),
              'ell':C['ell'].record(), 'variable_common_leading_cost':expected_common,
              'raw_free_distance':expected_norm, 'active_actual_complex_roots':roots,
              'inactive_first_half_radials':inactive}
    return {'actual_agent':'six-reviewer-3', 'role':'independent mathematical reviewer',
            'method':'extended polynomial Euclid; flat sparse eta/delta jets; rational unit-circle phases; literal centered vector factors',
            'shared_math':shared, 'rational_phase_jets':[p.record() for p in main['phases']],
            'centered_vector_controls':controls, 'embedding_interval':[str(lo),str(hi)],
            'ell_interval':[str(x) for x in bounds], 'exact_checks':audit.checks, 'rejected_damages':audit.damages}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',',':')).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=BASE/'EXPECTED.json')
    parser.add_argument('--emit-fixture',type=Path)
    parser.add_argument('--author-fixture',type=Path)
    args = parser.parse_args()
    result = run()
    if args.emit_fixture is not None:
        args.emit_fixture.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(canonical(result) == canonical(json.loads(args.fixture.read_text())), 'complete independent frozen fixture including JSON types')
    if args.author_fixture is not None:
        author = json.loads(args.author_fixture.read_text())
        for key, value in result['shared_math'].items():
            require(canonical(value) == canonical(author[key]), 'complete author mathematical field '+key)
    print('PASS',len(result['exact_checks']),'exact checks;',len(result['rejected_damages']),
          'damages rejected; full-record SHA256',sha256(canonical(result)).hexdigest())


if __name__ == '__main__':
    main()
