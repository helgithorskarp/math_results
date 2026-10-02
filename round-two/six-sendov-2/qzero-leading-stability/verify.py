#!/usr/bin/env python3
"""An exact polynomial module unit and a quantitative q=0 stability tube.

Actual six-sendov-2, researcher. Python standard library only. Regenerates
the complete pinned same-author 9743 input, then reconstructs one fixed
21-by-26 rational coefficient system and multiplies its whole polynomial unit.
This is author validation, not independent review or formalization.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm
import argparse
import hashlib
import importlib.util
import json

INPUT_COMMIT = '9daf6c448bddfe865cc348709f517c95afc65fbb'
INPUT_PINS = {
    'verify.py': '73d58f38b87bfccfb6a19f9cffb43ee2c706caeb9f3c86f2b5cdd246c6d3dc34',
    'expected.json': '4d2db07efd3d124d96499c26d9f3864c848a2a11a96c7c28631379bed6bd5550'}
INPUT_RECORD = 'f176edb31a2d9c4b5964b05eaafb977478f99b74b4b2d28bef1ae7a32916a0a7'
ZERO = (0, 0, 0, 0)  # All polynomials in this checker use (q,r,x,u).


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = value.c.copy()
        elif isinstance(value, dict):
            require(all(isinstance(k, tuple) and len(k) == 4 and
                        all(type(e) is int and e >= 0 for e in k) for k in value),
                    'complete polynomial exponent domain')
            require(all(type(c) in (int, F) for c in value.values()),
                    'rational polynomial coefficients only')
            self.c = {k: F(c) for k, c in value.items() if c}
        else:
            require(type(value) in (int, F), 'exact scalar only')
            self.c = {ZERO: F(value)} if value else {}

    def __add__(self, other):
        d = self.c.copy()
        for k, c in P(other).c.items():
            d[k] = d.get(k, F(0)) + c
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -c for k, c in self.c.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, other):
        d = {}
        for k, c in self.c.items():
            for j, b in P(other).c.items():
                key = tuple(a + z for a, z in zip(k, j))
                d[key] = d.get(key, F(0)) + c*b
        return P(d)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'nonnegative integral power')
        ans, base = P(1), self
        while n:
            if n % 2:
                ans = ans*base
            base = base*base
            n //= 2
        return ans

    def __eq__(self, other):
        return self.c == P(other).c

    def degree(self, i=None):
        return max((sum(k) if i is None else k[i] for k in self.c), default=-1)

    def encoded(self):
        return [[list(k), str(c)] for k, c in sorted(self.c.items())]


def variable(i):
    key = list(ZERO)
    key[i] = 1
    return P({tuple(key): F(1)})


def extract(a, index, degree):
    out = {}
    for k, c in P(a).c.items():
        if k[index] == degree:
            key = list(k)
            key[index] = 0
            out[tuple(key)] = c
    return P(out)


def qzero(a):
    return extract(a, 0, 0)


def primitive(a):
    a = P(a)
    require(bool(a.c), 'nonzero polynomial primitive part')
    den = lcm(*(c.denominator for c in a.c.values()))
    common = 0
    for c in a.c.values():
        common = gcd(common, abs(int(c*den)))
    content = F(common, den)
    return (1/content)*a, content


def decode_input(a):
    out = {}
    for key, coefficient in a:
        require(len(key) == 10 and not any(key[i] for i in (1, 5, 6, 7, 8, 9)),
                'entire9743 coefficient domain; no E or auxiliary variables')
        new = tuple(key[i] for i in (0, 2, 3, 4))
        require(new not in out, 'no duplicate monomials in input')
        out[new] = F(coefficient)
    return P(out)


def input9743():
    directory = Path(__file__).resolve().parent.parent / 'critical-coefficient-recovery'
    for name, digest in INPUT_PINS.items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
                'pinned whole9743 file ' + name)
    spec = importlib.util.spec_from_file_location('qzero_input9743', directory/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data, same_typed = module.certificate()
    require(same_typed(data, json.loads((directory/'expected.json').read_text())),
            'whole typed9743 record regenerated, including its parents')
    require(hashlib.sha256(canonical(data)).hexdigest() == INPUT_RECORD,
            'complete9743 input record digest')
    return data, same_typed


def monomials(degree):
    return [(i,j) for i in range(degree+1) for j in range(degree+1-i)]


def solve_rational_system(matrix, rhs):
    """Constant rational pivots only; every solution is multiplied back."""
    nrows, ncols = len(matrix), len(matrix[0])
    require(len(rhs) == nrows and all(len(row) == ncols for row in matrix),
            'whole rational system dimensions')
    a = [list(map(F,row))+[F(b)] for row,b in zip(matrix,rhs)]
    pivots = []
    for column in range(ncols):
        row = next((i for i in range(len(pivots),nrows) if a[i][column]),None)
        if row is None:
            continue
        pivot = len(pivots)
        a[row],a[pivot] = a[pivot],a[row]
        divisor = a[pivot][column]
        require(divisor != 0, 'nonzero CONSTANT rational pivot')
        a[pivot] = [c/divisor for c in a[pivot]]
        for i in range(nrows):
            if i != pivot and a[i][column]:
                factor = a[i][column]
                a[i] = [c-factor*b for c,b in zip(a[i],a[pivot])]
        pivots.append(column)
        if len(pivots) == nrows:
            break
    require(all(any(row[:ncols]) or row[-1] == 0 for row in a),
            'consistent COMPLETE augmented rational system')
    solution = [F(0)]*ncols  # The five free coordinates are set to zero.
    for row,column in enumerate(pivots):
        solution[column] = a[row][-1]
    require(all(sum((c*z for c,z in zip(row,solution)),F(0)) == b
                for row,b in zip(matrix,rhs)), 'all complete coefficient equations multiplied')
    return solution,pivots


def value(a, values):
    ans = F(0)
    for k, c in a.c.items():
        term = c
        for z, exponent in zip(values, k):
            term *= z**exponent
        ans += term
    return ans


def certificate():
    data, same_typed = input9743()
    q, r, x, u = [variable(i) for i in range(4)]
    checks = {}

    def eq(label, left, right=0):
        require(P(left) == P(right), 'whole polynomial identity ' + label)
        checks[label] = True

    alpha = [decode_input(a) for a in data['complete_Elinear_coefficients_alpha']]
    A = [decode_input(a) for a in data['primitive_E_leading_polynomials_A']]
    constants = list(map(F, data['A_normalization_contents']))
    require(constants == [F(1,16934400), F(1,4515840), F(1,9408), F(1,2257920)],
            'all four original normalization constants')
    for i in range(4):
        eq('alpha normalization ' + str(i), alpha[i], constants[i]*u*A[i])
    Aq0 = [qzero(a) for a in A]
    require(all(a.degree(3) == 1 for a in Aq0), 'all four q0 leading rows affine in u')
    slopes = [extract(a, 3, 1) for a in Aq0]
    intercepts = [extract(a, 3, 0) for a in Aq0]
    d, K = 31304*r+1162*x+6165, F(118272)
    eq('constant-pivot entire A2', A[2], (d+7200*q)*u-K)
    small, contents = [], []
    order = [0, 3, 1]
    for i in order:
        p, c = primitive(K*slopes[i]+d*intercepts[i])
        small.append(p)
        contents.append(c)
        eq('undivided complete leading clear ' + str(i), d*Aq0[i]-slopes[i]*Aq0[2], c*p)
    require(contents == [62720, 87808, 62720], 'whole leading-clear contents')
    expected_small = [
        -205919616*r*r-798759752*r*x-142966224*r+697198838*x*x-311351805*x-26263980,
        -7983360*r*r+26141800*r*x-5013360*r-14207110*x*x+8925849*x-727650,
        -68124672*r**3+211172864*r*r*x-68656896*r*r-123748352*r*x*x+
        162619640*r*x-22453200*r+4629408*x**3-53825666*x*x+31300875*x-2349270]
    for i in range(3):
        eq('entire explicitly displayed polynomial ' + str(i), small[i], expected_small[i])
    row_monomials = monomials(5)
    columns = [(i,a,b) for i,degree in enumerate([2,2,3])
               for a,b in monomials(5-degree)]
    column_polynomials = [r**a*x**b*small[i] for i,a,b in columns]
    matrix = [[p.c.get((0,a,b,0),F(0)) for p in column_polynomials]
              for a,b in row_monomials]
    rhs = [F(int(a == b == 0)) for a,b in row_monomials]
    require(len(matrix) == 21 and len(columns) == 26,
            'full fixed21-by26 coefficient system')
    require(all(all(k[0] == k[3] == 0 and k[1]+k[2] <= 5 for k in p.c)
                for p in column_polynomials), 'all monomials retained in full degree5 system')
    solution,pivots = solve_rational_system(matrix,rhs)
    require(len(pivots) == 21, 'full row rank and five free constant coordinates')
    Hs = [P() for i in range(3)]
    for (i,a,b),c in zip(columns,solution):
        Hs[i] = Hs[i]+c*r**a*x**b
    eq('whole bivariate unit', sum((h*a for h,a in zip(Hs,small)),P()), 1)
    C = [P() for i in range(4)]
    for i, h, c in zip(order,Hs,contents):
        C[i] = C[i] + (1/c)*d*h
        C[2] = C[2] - (1/c)*slopes[i]*h
    eq('whole q0 primitive leading module unit', sum((c*a for c,a in zip(C,Aq0)),P()),1)
    L = [(1/c)*a for c,a in zip(constants,C)]
    require(all(all(k[0] == k[3] == 0 for k in a.c) for a in L), 'all multipliers only depend on r,x')
    eq('whole q0 original leading module u', sum((l*qzero(a) for l,a in zip(L,alpha)),P()),u)
    full = sum((l*a for l,a in zip(L,alpha)),P())
    defect = full-u
    require(bool(defect.c) and all(k[0] >= 1 and k[3] >= 1 for k in defect.c),
            'entire polynomial defect divisible by the KNOWN q*u monomial')
    Z = P({(k[0]-1,k[1],k[2],k[3]-1):c for k,c in defect.c.items()})
    eq('whole general q relative module identity',full,u*(1+q*Z))
    heights = [sum((abs(c) for c in l.c.values()),F(0)) for l in L]
    ceilings = [-(-h.numerator//h.denominator) for h in heights]
    zheight = sum((abs(c) for c in Z.c.values()),F(0))
    zceil = -(-zheight.numerator//zheight.denominator)
    require(max(l.degree() for l in L) == 5, 'total multiplier degree5')
    require(sum(h*h for h in ceilings) < (4*10**5)**2,
            'exact squared coefficient-height budget below (4e5)^2')
    require(zheight < 10**6, 'entire full defect coefficient-height budget below1e6')
    require(all(k[0] <= 1 and k[1]+k[2] <= 5 and k[3] <= 1 for k in Z.c),
            'entire defect weighted degree budgets q1,(r+x)5,u1')

    # Exact boundary controls and deliberate mathematical damage checks.
    controls = {}
    controls['u0 remains excluded and all alpha vanish there'] = all(extract(a,3,0) == 0 for a in alpha)
    vals = [F(0),-F(6165,31304),F(0),F(-2)]
    controls['d0 x0 signed-u polynomial boundary retained'] = (
        value(d,vals) == 0 and value(A[2],vals) == -K and
        sum(value(l,vals)*value(a,vals) for l,a in zip(L,alpha)) == vals[3])
    controls['no r x q or u polynomial inverted'] = all(type(c) is F for c in solution)
    damages = {}
    changed_solution = solution.copy()
    changed_solution[-1] += 1
    damages['last whole coefficient-system coordinate changed'] = any(
        sum((c*z for c,z in zip(row,changed_solution)),F(0)) != b for row,b in zip(matrix,rhs))
    damages['whole bivariate unit coefficient changed'] = sum(
        ((h+(x*x if i == 2 else 0))*a for i,(h,a) in enumerate(zip(Hs,small))),P()) != 1
    damages['whole original module multiplier changed'] = full+alpha[0] != u*(1+q*Z)
    damages['entire q defect coefficient changed'] = full != u*(1+q*(Z+x**5))
    require(all(controls.values()), 'all mathematical boundary controls')
    require(all(damages.values()), 'all coefficient damages rejected')
    record = {
        'actual_agent':'six-sendov-2','role':'researcher',
        'domain':'QQ[q,r,x,u]; all finite complex r,x; u!=0; q0 or the explicitly bounded q tube',
        'input9743':{'source_commit':INPUT_COMMIT,'file_pins':INPUT_PINS,
                     'whole_record_sha256':INPUT_RECORD,'complete_typed_record_and_parents_regenerated':True},
        'whole_q0_primitive_A':[a.encoded() for a in Aq0],
        'whole_primitive_leading_clears_F_G_J':[a.encoded() for a in small],
        'clear_order_A_indices':order,'normalization_contents':list(map(str,contents)),
        'fixed_coefficient_system':{'degree_budget':5,'row_monomials':[list(m) for m in row_monomials],
             'column_descriptors':[list(c) for c in columns],'complete_integer_matrix':[[str(c) for c in row] for row in matrix],
             'complete_rhs':list(map(str,rhs)),'whole_rational_solution':list(map(str,solution)),
             'pivot_columns':pivots,'free_coordinates_set_to_zero':True},
        'whole_QQ_r_x_Bezout_unit':[a.encoded() for a in Hs],
        'whole_q0_primitive_A_module_unit':[a.encoded() for a in C],
        'whole_original_alpha_module_L':[a.encoded() for a in L],
        'whole_full_q_relative_defect_Z':Z.encoded(),
        'L_term_counts':[len(a.c) for a in L], 'L_total_degrees':[a.degree() for a in L],
        'L_exact_coefficient_heights':list(map(str,heights)), 'L_height_integer_ceilings':ceilings,
        'Z_term_count':len(Z.c),'Z_total_degree':Z.degree(),
        'Z_exact_coefficient_height':str(zheight),'Z_height_integer_ceiling':zceil,
        'quantitative_budgets':{'L_degree':5,'L_norm_constant':4*10**5,
                                'Z_r_x_degree':5,'Z_u_degree':1,'Z_q_degree':1,
                                'Z_height_constant':10**6,
                                'tube_q_denominator_constant':2*10**6},
        'whole_polynomial_identities':checks,'boundary_controls':controls,
        'rejected_mathematical_damages':damages,
        'identity':'sum_i L_i(r,x)*alpha_i(q,r,x,u)=u*(1+q*Z(q,r,x,u))',
        'q0_bound':'||alpha|| >= |u|/(400000*M^5) for M>=1, |r|,|x|<=M; no upper bound on u',
        'tube_bound':'||alpha|| >= |u|/(800000*M^5) for M,U>=1, |r|,|x|<=M, 0<|u|<=U, |q|<=1/(2000000*M^5*U)',
        'full_residual_E_control':'Divide either bound by sqrt(1+(367/360)^2+(M/3+13/96)^2+1/2304) for all E derivatives and fixed-tuple secants from a common E0.',
        'ordinary_bridges':'Complete QQ coefficient-system solution multiplied as a polynomial unit; Hermitian Cauchy-Schwarz and triangle inequalities; inherited9743 fixed linear row operation; not formally verified',
        'full_stationary_equations_required_for_profiles':True,
        'strict_simple_real_original_feasibility_required':True,
        'x0_actual_chart_claimed':False,'u0_nonvanishing_claimed':False,
        'unrestricted_q_nonvanishing_claimed':False,
        'full_Jacobian_rank_two_asserted':False,'profile_existence_or_classification_proved':False,
        'original_collision_limits_proved':False,'complex_first_power_proved':False,
        'independently_reviewed':False}
    return record,same_typed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    record,same_typed = certificate()
    if args.write_expected:
        args.expected.write_bytes(canonical(record)+b'\n')
    else:
        require(same_typed(record,json.loads(args.expected.read_text())),'ENTIRE typed expected certificate')
    print(json.dumps({'whole_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
                      'whole_polynomial_identities':len(record['whole_polynomial_identities']),
                      'fixed_coefficient_system_shape':[21,26],
                      'L_terms':record['L_term_counts'],'L_degrees':record['L_total_degrees'],
                      'Z_terms':record['Z_term_count'],'Z_total_degree':record['Z_total_degree'],
                      'L_height_ceilings':record['L_height_integer_ceilings'],
                      'Z_height_ceiling':record['Z_height_integer_ceiling'],
                      'q0_leading_nonvanishing_unconditional':True,
                      'explicit_bounded_complex_q_tube':True,
                      'complex_first_power_proved':False,'independently_reviewed':False},sort_keys=True))


if __name__ == '__main__':
    main()
