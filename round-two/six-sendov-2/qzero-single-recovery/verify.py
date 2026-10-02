#!/usr/bin/env python3
"""A single E-recovery pivot at every q0 affine-stationary solution.

Actual six-sendov-2, researcher. Standard library only. Whole input and
parent records are regenerated. Same-author 9550 sparse Laurent arithmetic
and 9695 determinant/interpolation/finite-unit routines are explicitly reused.
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
PRIME = 257


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def input9743():
    directory = Path(__file__).resolve().parent.parent / 'critical-coefficient-recovery'
    for name, digest in INPUT_PINS.items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
                'whole pinned9743 source ' + name)
    spec = importlib.util.spec_from_file_location('single_recovery_input9743', directory/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data, same_typed = module.certificate()
    require(same_typed(data, json.loads((directory/'expected.json').read_text())),
            'whole typed9743 record, including all parents')
    require(hashlib.sha256(canonical(data)).hexdigest() == INPUT_RECORD,
            'whole9743 mathematical record')
    h, k, parent_data = module.input_parent()
    return data, same_typed, h, k


def certificate():
    data, same_typed, h, k = input9743()
    P = k.P
    q, E, r, x, u = [k.variable(i) for i in range(5)]
    v, z = k.variable(5), k.variable(6)
    inverse_u = P({(0,0,0,0,-1,0,0,0,0,0):F(1)})
    checks = {}

    def eq(label, left, right=0):
        require(P(left) == P(right), 'whole polynomial identity ' + label)
        checks[label] = True

    def degree(a, index):
        return max((key[index] for key in a.c), default=-1)

    def primitive(a):
        a = P(a)
        require(bool(a.c), 'nonzero rational polynomial primitive part')
        denominator = lcm(*(c.denominator for c in a.c.values()))
        common = 0
        for c in a.c.values():
            common = gcd(common, abs(int(c*denominator)))
        content = F(common, denominator)  # Positive; all signs retained.
        result = (1/content)*a
        require(all(c.denominator == 1 for c in result.c.values()),
                'whole primitive integer coefficients')
        eq('primitive reconstruction ' + str(len(checks)), a, content*result)
        return result, content

    def decode(encoded):
        require(all(len(key) == 10 and key[1] == 0 and not any(key[5:])
                    for key, c in encoded), 'entire9743 coefficient domain')
        return k.extract(P({tuple(key):F(c) for key,c in encoded}),0,0)

    alpha = [decode(a) for a in data['complete_Elinear_coefficients_alpha']]
    beta = [decode(a) for a in data['complete_Elinear_constants_beta']]
    a0, ell0, c0 = [decode(a) for a in data['complete_remaining_R0_E_coefficients']]
    d, K = 31304*r+1162*x+6165, F(118272)
    A2 = d*u-K
    eq('entire q0 alpha2 simple pivot', alpha[2], F(1,9408)*u*A2)
    eq('entire remaining quadratic coefficient', a0, 2*u*u)
    original = [a*E+b for a,b in zip(alpha,beta)]

    # u is the only inverted variable. v=xu, z=u^2E, and A2=0 gives
    # r=(118272-1162v-6165u)/(31304u), with a CONSTANT31304 pivot.
    rs = F(1,31304)*(K-1162*v-6165*u)*inverse_u

    def transform(a):
        a = k.sub(a,2,rs)
        a = k.sub(a,3,v*inverse_u)
        return k.sub(a,1,z*inverse_u**2)

    def encoded_new(a):
        require(all(not any(key[i] for i in (0,1,2,3,7,8,9)) and
                    key[4] >= 0 for key in a.c), 'complete QQ[v,u,z] domain')
        return [[list((key[5],key[4],key[6])),str(c)] for key,c in sorted(
            a.c.items(), key=lambda item:(item[0][5],item[0][4],item[0][6]))]

    def divide_r(a):
        """Divide by A2 in QQ[E,x,u,u^-1][r]; only u and31304 inverted."""
        quotient, remainder = P(), P(a)
        while remainder != 0 and degree(remainder,2) >= 1:
            shift = degree(remainder,2)-1
            leading = k.extract(remainder,2,shift+1)
            term = F(1,31304)*leading*inverse_u*r**shift
            quotient += term
            remainder -= term*A2
        eq('entire legal A2 division ' + str(len(checks)), a, quotient*A2+remainder)
        return quotient,remainder

    H, hcontent = primitive(u*transform(beta[2]))
    require(degree(H,5) == 3, 'whole lower beta2 is cubic in v')
    hlead = k.scalar(k.extract(H,5,3))
    require(hlead == -232008115500, 'nonzero CONSTANT v-cubic pivot')
    expected_H = (-690386204884992+35497291382784*u+13574437701216*u*u+
                  402972239385*u**3-58441189015552*v-42624262534336*v*u-
                  2065325180940*v*u*u+33667298577920*v*v+
                  2037538724550*v*v*u-232008115500*v**3)
    eq('whole displayed cubic H',H,expected_H)
    eq('entire A2 leading cancellation',transform(alpha[2]),0)
    lower_back = k.sub(H,5,x*u)
    lower_quotient, lower_remainder = divide_r(hcontent*lower_back-u*beta[2])
    require(lower_remainder == 0, 'whole lower pullback modulo A2')

    rows, saved_rows, pullbacks = {}, [], []
    for i, power in [(0,2),(1,3),(3,2)]:
        row, content = primitive(u**power*transform(original[i]))
        encoded_new(row)
        ai, bi = k.extract(row,6,1), k.extract(row,6,0)
        eq('whole linear z row ' + str(i),row,ai*z+bi)
        back = k.sub(k.sub(row,5,x*u),6,u*u*E)
        quotient,remainder = divide_r(content*back-u**power*original[i])
        require(remainder == 0, 'entire original row pullback modulo A2 ' + str(i))
        rows[i] = (ai,bi)
        saved_rows.append({'index':i,'known_u_multiplier':power,'positive_content':str(content),
                           'whole_row':encoded_new(row),'whole_a':encoded_new(ai),
                           'whole_b':encoded_new(bi)})
        pullbacks.append({'index':i,'whole_A2_multiplier':quotient.encoded()})

    def divide_v(a):
        """Entire QQ[u][v] division by H; only its nonzero rational pivot."""
        quotient, remainder = P(), P(a)
        require(all(key[6] == 0 and key[4] >= 0 for key in a.c),
                'ordinary bivariate wedge before constant division')
        while remainder != 0 and degree(remainder,5) >= 3:
            shift = degree(remainder,5)-3
            term = (1/hlead)*k.extract(remainder,5,shift+3)*v**shift
            quotient += term
            remainder -= term*H
        eq('whole constant-pivot v division ' + str(len(checks)), a, quotient*H+remainder)
        return quotient, remainder

    def integer_u_series(a):
        require(all(not any(e for i,e in enumerate(key) if i != 4) and key[4] >= 0
                    for key in a.c), 'entire ordinary integer QQ[u] coefficient')
        out = [0]*max(1,degree(a,4)+1)
        for key,c in a.c.items():
            require(c.denominator == 1, 'whole integer Sylvester coefficient')
            out[key[4]] = int(c)
        return out

    def arrays_v(a):
        encoded_new(a)
        require(all(key[6] == 0 for key in a.c), 'entire bivariate v,u polynomial')
        return [integer_u_series(k.extract(a,5,j)) for j in range(degree(a,5)+1)]

    necessary, resultants = [], []
    hc = arrays_v(H)
    for i,j in [(0,3),(0,1)]:
        ai,bi = rows[i]
        aj,bj = rows[j]
        wedge, content = primitive(ai*bj-aj*bi)
        eq('whole undivided linear z wedge '+str(i)+str(j),
           content*wedge, ai*(aj*z+bj)-aj*(ai*z+bi))
        quotient, remainder = divide_v(wedge)
        remainder_integer,rcontent = primitive(remainder)
        eq('complete constant-pivot wedge '+str(i)+str(j),
           wedge,quotient*H+rcontent*remainder_integer)
        rc = arrays_v(remainder_integer)
        m,n = len(hc)-1,len(rc)-1
        require((m,n) == (3,2), 'fixed formal cubic/quadratic degrees')
        bound = n*max(len(c)-1 for c in hc)+m*max(len(c)-1 for c in rc)
        values = []
        for point in range(bound+1):
            matrix = h.fixed_sylvester(hc,rc,point)
            value = h.determinant_integer(matrix)
            require(h.determinant_fraction(matrix) == value,
                    'every fixed node Fraction Gaussian corroboration')
            values.append(value)
        entire = h.interpolate_rational(values)
        primitive_coefficients, determinant_content = h.integer_primitive(entire)
        necessary.append({'pair':[i,j],'positive_wedge_content':str(content),
                          'whole_wedge':encoded_new(wedge),'whole_H_quotient':encoded_new(quotient),
                          'whole_remainder':encoded_new(remainder),
                          'positive_remainder_content':str(rcontent),
                          'whole_integer_remainder':encoded_new(remainder_integer)})
        resultants.append({'pair':[i,j],'formal_v_degrees':[m,n],'fixed_matrix_size':m+n,
                           'whole_left_coefficient_arrays':hc,'whole_right_coefficient_arrays':rc,
                           'proved_u_degree_bound':bound,'all_integer_evaluations':values,
                           'whole_determinant_coefficients':entire,
                           'primitive_coefficients':primitive_coefficients,
                           'determinant_content':str(determinant_content),
                           'actual_u_degree':len(entire)-1,'every_Gaussian_value_matches':True})
    unit = h.finite_unit(resultants[0]['primitive_coefficients'],
                         resultants[1]['primitive_coefficients'],PRIME)
    require([a['proved_u_degree_bound'] for a in resultants] == [24,27] and
            [a['actual_u_degree'] for a in resultants] == [18,21], 'all determinant degree budgets')

    # Keep the COMPLETE remaining equation and all three affine compatibility
    # equations. Never replace five residuals by a partial wedge test.
    a,b = alpha[2],beta[2]
    reduced = [a*beta[i]-alpha[i]*b for i in (0,1,3)]
    reduced += [a0*b*b-ell0*a*b+c0*a*a]
    reduced_saved = []
    for i,p in enumerate(reduced):
        power = min(key[4] for key in p.c)
        require(power >= 1, 'known nonzero u content of reduced equation')
        stripped = p*inverse_u**power
        primitive_row,content = primitive(stripped)
        eq('entire reduced equation reconstruction '+str(i),p,content*u**power*primitive_row)
        reduced_saved.append({'index':i,'known_u_power':power,'positive_content':str(content),
                              'whole_primitive_coefficients':primitive_row.encoded()})
    eq('whole full quadratic recovery identity',
       a*a*(a0*E*E+ell0*E+c0)-(a0*b*b-ell0*a*b+c0*a*a),
       (a*E+b)*(a0*(a*E-b)+ell0*a))

    def evaluate(a, values):
        answer = F(0)
        for key,c in a.c.items():
            term = c
            for value,exponent in zip(values,key):
                term *= value**exponent
            answer += term
        return answer

    controls = {}
    controls['u0 alpha2 remains zero and excluded'] = k.extract(alpha[2],4,0) == P()
    for label,xvalue in [('positive x',F(3)),('x0 polynomial extension',F(0))]:
        values = [F(0),F(1,32),(K/F(-2)-1162*xvalue-6165)/31304,
                  xvalue,F(-2)]+[F(0)]*5
        controls[label+' offsolution alpha2 zero but lower row nonzero'] = (
            evaluate(A2,values) == 0 and evaluate(alpha[2],values) == 0 and
            evaluate(beta[2],values) != 0)
    controls['finite common root with formal quadratic degree loss retained'] = (
        h.determinant_integer(h.fixed_sylvester([[-1],[0],[0],[1]],[[-1],[1],[0,1]],0)) == 0)
    controls['identically zero specialized lower polynomial retained'] = (
        h.determinant_integer(h.fixed_sylvester([[-1],[0],[0],[1]],[[0,1],[0,2],[0,3]],0)) == 0)
    try:
        h.finite_unit([-1,257],[-1,257],257)
    except ValueError as ex:
        controls['modular leading-degree loss rejected'] = 'leading degrees preserved' in str(ex)
    require(all(controls.values()), 'all mathematical domain controls')
    damages = {}
    damages['highest v cubic coefficient changed'] = H+v**3 != expected_H
    damages['entire high linear row constant changed'] = rows[1][0]*z+rows[1][1]+1 != (
        u**3*transform(original[1])*(1/F(saved_rows[1]['positive_content'])))
    qtest = necessary[1]
    damages['whole high-u remainder coefficient changed'] = (
        qtest['whole_remainder'] != encoded_new(remainder+u**7))
    damaged = list(resultants[1]['whole_determinant_coefficients'])
    damaged[-1] += 1
    damages['last full determinant coefficient changed'] = any(
        h.evaluate(damaged,point) != value for point,value in enumerate(resultants[1]['all_integer_evaluations']))
    damaged_multiplier = list(unit['left_multiplier'])
    damaged_multiplier[-1] = (damaged_multiplier[-1]+1)%PRIME
    damages['trailing finite unit multiplier changed'] = h.add(
        h.multiply(unit['left'],damaged_multiplier,PRIME),
        h.multiply(unit['right'],unit['right_multiplier'],PRIME),PRIME) != [1]
    require(all(damages.values()), 'all mathematical coefficient damages rejected')

    record = {
        'actual_agent':'six-sendov-2','role':'researcher',
        'domain':'q=0; every finite COMPLEX common E of all FOUR affine rows; u!=0; arbitrary complex r,x',
        'input9743':{'source_commit':INPUT_COMMIT,'pins':INPUT_PINS,
                     'whole_record_sha256':INPUT_RECORD,'all_parents_and_whole_typed_input_regenerated':True},
        'same_author_arithmetic_reuse':'9550 sparse Laurent kernel and9695 exact Bareiss/Fraction Gaussian/interpolation/modular unit',
        'selected_pivot':'alpha2=u*((31304*r+1162*x+6165)*u-118272)/9408',
        'known_chart':'v=xu,z=u^2E,r=(118272-1162v-6165u)/(31304u); only u and nonzero rational constants inverted',
        'lower_beta2_positive_content':str(hcontent),'whole_lower_cubic_H':encoded_new(H),
        'constant_v_cubic_pivot':str(hlead),'whole_lower_pullback_A2_multiplier':lower_quotient.encoded(),
        'whole_three_linear_z_rows':saved_rows,'whole_three_pullback_A2_multipliers':pullbacks,
        'whole_undivided_wedges_and_constant_remainders':necessary,
        'whole_fixed_resultants':resultants,'whole_univariate_modular_unit':unit,
        'whole_q0_alpha':[a.encoded() for a in alpha],'whole_q0_beta':[b.encoded() for b in beta],
        'whole_q0_remaining_quadratic_coefficients':[a0.encoded(),ell0.encoded(),c0.encoded()],
        'whole_complete_reduced_predicate':reduced_saved,
        'whole_polynomial_identities':checks,'mathematical_boundary_controls':controls,
        'rejected_mathematical_damages':damages,
        'claim':'Every covered common affine E has alpha2!=0. At q0 one chart E=-9408*beta2/(u*((31304r+1162x+6165)u-118272)) covers every full stationary solution.',
        'complete_complex_predicate':'alpha2!=0; alpha2*beta_i-alpha_i*beta2=0 for ALL i=0,1,3; 2u^2*beta2^2-ell0*alpha2*beta2+c0*alpha2^2=0',
        'ordinary_bridges':'Legal known-u Laurent substitution; undivided affine wedges; CONSTANT-pivot cubic division; finite-root fixed Sylvester evaluation vectors; full degree-bounded interpolation; primitive integer Gauss plus degree-preserving finite-field coprimality; inherited complete row operation and actual strict feasibility. Unformalized.',
        'unconditional_selected_pivot_nonvanishing_claimed':False,
        'x0_actual_profile_interpretation_claimed':False,'u0_nonvanishing_claimed':False,
        'unrestricted_q_extension_claimed':False,'full_Jacobian_rank_claimed':False,
        'profile_existence_or_classification_proved':False,'original_collisions_included':False,
        'complex_first_power_proved':False,'independently_reviewed':False}
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
        require(same_typed(record,json.loads(args.expected.read_text())), 'ENTIRE typed expected certificate')
    print(json.dumps({'whole_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
                      'whole_polynomial_identities':len(record['whole_polynomial_identities']),
                      'all_fixed_integer_nodes':sum(len(a['all_integer_evaluations'])for a in record['whole_fixed_resultants']),
                      'fixed_matrices':[a['fixed_matrix_size']for a in record['whole_fixed_resultants']],
                      'proved_degree_bounds':[a['proved_u_degree_bound']for a in record['whole_fixed_resultants']],
                      'actual_degrees':[a['actual_u_degree']for a in record['whole_fixed_resultants']],
                      'retained_field_degrees':record['whole_univariate_modular_unit']['integer_degrees_preserved'],
                      'single_pivot_nonvanishing_at_q0_solutions':True,
                      'complex_first_power_proved':False,'independently_reviewed':False},sort_keys=True))


if __name__ == '__main__':
    main()
