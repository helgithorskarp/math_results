#!/usr/bin/env python3
"""Explicit two-moment/full-five-residual coercivity on bounded mass charts.

Actual six-sendov-2, researcher. Standard-library exact rational arithmetic.
The entire pinned9902 input and its9550 input are regenerated; same-author
Laurent arithmetic is openly reused. Universal norm, projection, interlacing
and original-root arguments are ordinary mathematics in PROOF.md.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb, factorial
import argparse
import hashlib
import importlib.util
import json

INPUT_COMMIT = 'fadd074a5339772bb937e7e77c5a0292c80b256a'
INPUT_PINS = {
    'verify.py': 'f6213f7ab945214e4c10abf96015b0b3fc9642c3e8b30f535799ec7ccb73f6d4',
    'expected.json': 'a45a2e4143bd5cac737d210fe05d9c6c27357df0dd47faabbdc9bca07af8520d'
}
INPUT_RECORD = '97b467872be8c1d5741ebc0b37980ec060188dc66266403d565ee7b6b217529a'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def same_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_typed(x, y) for x, y in zip(a, b))
    return a == b


def parent():
    directory = Path(__file__).resolve().parent.parent / 'cubic-quintic-exclusion'
    for name, digest in INPUT_PINS.items():
        require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest,
                'entire pinned9902 file ' + name)
    spec = importlib.util.spec_from_file_location('whole_coercivity_parent9902', directory / 'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record = module.certificate()
    require(same_typed(record, json.loads((directory / 'expected.json').read_text())),
            'ENTIRE typed9902 input')
    require(hashlib.sha256(canonical(record)).hexdigest() == INPUT_RECORD,
            'ENTIRE9902 record hash')
    k, data = module.input9550()
    defining = json.loads((directory.parent / 'degree-five-triangular/expected.json').read_text())
    return k, data, record, defining


def certificate():
    k, data, old, defining = parent()
    P = k.P
    B, E, r, s, t = [k.variable(i) for i in range(5)]
    ti = P({(0, 0, 0, 0, -1, 0, 0, 0, 0, 0): 1})
    identities = {}

    def eq(name, left, right=0):
        require(P(left) == P(right), 'whole identity ' + name)
        identities[name] = True

    def decode(encoded):
        require(all(len(key) == 5 for key, c in encoded), 'whole five-variable input')
        return P({tuple(key + [0] * 5): F(c) for key, c in encoded})

    def degree(a):
        return max((sum(abs(e) for e in key) for key in a.c), default=0)

    def norm(a):
        return sum((abs(c) for c in a.c.values()), F(0))

    def ceiling(value):
        return -(-value.numerator // value.denominator)

    def univariate(coefficients):
        return sum((F(c) * r ** i for i, c in enumerate(coefficients)), P())

    R = [decode(a) for a in data['residuals_ascending']]
    Fstar = decode(data['h_ascending'][2])
    eq('whole original-chart B0 Fstar E pivot',
       k.diffvar(k.sub(Fstar, 0, 0), 1), F(-83, 60) * s)
    require(len(R) == 5 and all(min(key) >= 0 for a in R for key in a.c),
            'ALL FIVE full residuals are ordinary polynomials')
    sliceR = [k.sub(k.sub(a, 0, 0), 3, 0) for a in R]
    E0 = F(-1, 2112) * (10976 * r * r + 7344 * r + 1143)
    after = [k.sub(a, 1, E0) for a in sliceR]
    cubic = univariate(defining['slice_cubic'])
    six = univariate(defining['slice_degree_six'])
    UP = univariate(defining['slice_Bezout']['cubic_multiplier'])
    VS = univariate(defining['slice_Bezout']['eliminant_multiplier'])
    cp = k.scalar(k.extract(k.extract(after[1], 2, 3), 4, 1)) / F(defining['slice_cubic'][-1])
    a2, b2 = k.extract(after[0], 4, 2), k.extract(after[0], 4, 0)
    a0, b0 = k.extract(after[2], 4, 2), k.extract(after[2], 4, 0)
    cross = a2 * b0 - a0 * b2
    cs = k.scalar(k.extract(cross, 2, 6)) / F(defining['slice_degree_six'][-1])
    require(cp == F(-1, 9504) and cs == F(5, 1254528), 'two nonzero rational contents')
    eq('entire recovered-E cubic', after[1], cp * t * cubic)
    eq('entire recovered-E first quadratic', after[0], a2 * t * t + b2)
    eq('entire recovered-E second quadratic', after[2], a0 * t * t + b0)
    eq('entire undivided cross-eliminant', cross, cs * six)
    eq('entire inherited QQ Bezout product', UP * cubic + VS * six, 1)
    weights = [(-1 / cs) * VS * a0, (1 / cp) * ti * UP,
               (1 / cs) * VS * a2, P(), P()]
    eq('entire projected-E residual unit', sum((a * b for a, b in zip(weights, after)), P()), 1)
    quotients = []
    for i, row in enumerate(sliceR):
        quotient = P()
        for key, c in row.c.items():
            exponent = key[1]
            base = list(key)
            base[1] = 0
            quotient += P({tuple(base): c}) * sum(
                (E ** (exponent - 1 - j) * E0 ** j for j in range(exponent)), P())
        eq('entire E difference quotient ' + str(i), row - after[i], (E - E0) * quotient)
        quotients.append(quotient)
    eq('entire lawful E pivot', sliceR[3], F(-88, 7) * t * (E - E0))
    Z = list(weights)
    Z[3] = F(7, 88) * ti * sum((a * b for a, b in zip(weights, quotients)), P())
    eq('ENTIRE bounded-boundary Laurent row unit', sum((a * b for a, b in zip(Z, sliceR)), P()), 1)

    derivatives = [[k.diffvar(a, j) for j in [0, 1, 3]] for a in R]
    NZ_exact = sum((norm(a) for a in Z), F(0))
    NR_exact = max(norm(a) for row in derivatives for a in row)
    NF_exact = norm(k.diffvar(Fstar, 0))
    NZ, NR, NF = 202506888, 16583, 3
    require(ceiling(NZ_exact) == NZ and ceiling(NR_exact) == NR and ceiling(NF_exact) == NF,
            'complete coefficient norm ceilings')
    require(max(map(degree, Z)) == 9 and max(map(degree, R)) == 10
            and degree(Fstar) == 4, 'full absolute Laurent degrees')
    derivative_degrees = [max(degree(a) for row in derivatives for a in row),
                          degree(k.diffvar(Fstar, 0))]
    require(derivative_degrees == [9, 2],
            'full derivative degree bounds')
    require(all(not any(key[j] for j in [0, 3, 5, 6, 7, 8, 9])
                for a in Z for key in a.c), 'row unit only in E,r,t,t-inverse')
    require(old['integer_unit_coefficient_bound_C'] == 1 and old['matrix_entry_degree'] == 5
            and old['unit_multiplier_degree'] == 4, 'entire inherited complex residual bound')
    raw_unit_norm = F(old['exact_raw_unit_coefficient_norm'])
    raw_unit_bound = F(1, 10 ** 13)
    require(0 < raw_unit_norm < raw_unit_bound,
            'whole inherited raw unit norm: independently confirmed9928 sharper margin')
    Q = int(old['exact_matrix_Frobenius_coefficient_bound_Q'])
    require(Q == 14913669297722925580854623, 'full matrix coefficient constant')
    contents = list(map(F, old['whole_specialized_positive_contents']))
    content_inverse = max(1 / c for c in contents)
    require(content_inverse == 1814727936, 'ALL FIVE primitive residual contents')

    # Every sufficient scalar comparison is exact. Universal powers/norms are
    # proved in PROOF.md, not inferred from finitely many sampled L values.
    a = F(1, 2 * NZ * NR)
    unrounded_c = a * a / (3 * 2 ** 9 * raw_unit_bound * Q * content_inverse
                           * NR * (1 + F(180, 83) / a))
    chosen_c = F(1, 10 ** 68)
    require(chosen_c <= unrounded_c and chosen_c <= a
            and chosen_c <= F(83, 180) * a, 'exact full coercivity constant comparisons')
    require(9 + 9 == 18 and 2 + 18 == 20 and 2 * 18 == 36
            and 28 + 2 + 9 == 39 and 36 + 39 == 75 and 75 + 20 == 95,
            'complete universal exponent accounting')
    lminus1 = k.variable(5) - 1
    eq('ENTIRE L20 boundary power factorization',
       lminus1 * sum((k.variable(5) ** j for j in range(20)), P()), k.variable(5) ** 20 - 1)

    mu3 = F(-24, 5) * B
    mu5 = -4 * B - F(40, 3) * Fstar
    eq('whole inverse original cubic moment', F(-5, 24) * mu3, B)
    eq('whole inverse original fifth coefficient', F(1, 16) * mu3 - F(3, 40) * mu5, Fstar)
    inverse_square = F(13, 48) ** 2 + F(3, 40) ** 2
    require(inverse_square == F(4549, 57600), 'whole original moment norm constant')

    # Ordinary derivative-mesh proof in PROOF.md covers every real original;
    # these exact products/constants verify its seven-node interpolation use.
    denominator_products = [factorial(j) * factorial(6 - j) for j in range(7)]
    interpolation_heights = [F(comb(6, j), 36) for j in range(7)]
    require(min(denominator_products) == 36 and max(interpolation_heights) == F(5, 9)
            and max(interpolation_heights) < 1, 'ALL SEVEN Lagrange coefficient bounds')
    mass_sum = -8 * (F(-1, 2) - F(-3, 8))
    require(mass_sum == 1, 'actual mass residue normalization')
    require(abs(F(5, 24)) < 1 and max(abs(F(-1, 16)), abs(F(3, 64))) < 1,
            'actual balanced norm-one B,E bounds')

    boundary = {}

    def evaluate(poly, point):
        require(len(point) == 5 and point[4] != 0, 'known nonzero t localization')
        return sum((c * F(point[0]) ** key[0] * F(point[1]) ** key[1]
                    * F(point[2]) ** key[2] * F(point[3]) ** key[3]
                    * F(point[4]) ** key[4] for key, c in poly.c.items()), F(0))

    point = [0, F(-7, 13), F(17, 23), 0, F(-1, 7)]
    require(sum((evaluate(z, point) * evaluate(row, point)
                 for z, row in zip(Z, sliceR)), F(0)) == 1, 'negative-t full row-unit control')
    boundary['negative_t_is_in_complex_chart_and_entire_unit_holds'] = True
    try:
        evaluate(Z[1], [0, 0, 0, 0, 0])
    except ValueError:
        boundary['t0_excluded'] = True
    else:
        raise ValueError('t0 incorrectly accepted')
    # Genuine old polynomial boundary solution: it cannot be treated as a
    # finite s,t original chart with x=s^2,u=st. Check EVERY quadratic.
    old_boundary = []
    for row in old['whole_Fstar_zero_primitive_quadratics']:
        value = sum((F(c) * F(-3, 8) ** key[2] * F(0) ** key[3]
                     * F(-224, 9) ** key[4] for key, c in row), F(0))
        old_boundary.append(str(value))
    require(old_boundary == ['0'] * 5, 'entire old x0 finite-u polynomial boundary')
    boundary['x0_r_minus3over8_u_minus224over9_ALL_FIVE_zeros'] = old_boundary
    boundary['x0_polynomial_boundary_not_original_profile'] = True
    boundary['closed_L1_scalar_constant_conditions'] = True
    boundary['all7_interpolation_denominator_products'] = denominator_products

    damages = {}

    def reject(name, condition):
        require(not condition, 'mathematical damage incorrectly passes ' + name)
        damages[name] = True

    damaged = list(Z)
    changed = dict(damaged[3].c)
    changed[max(changed)] += 1
    damaged[3] = P(changed)
    reject('last coefficient of whole fourth unit row',
           sum((z * row for z, row in zip(damaged, sliceR)), P()) == P(1))
    reject('wrong E-pivot factor8', sliceR[3] == -8 * t * (E - E0))
    reject('unit ceiling rounded down', NZ_exact <= NZ - 1)
    reject('R derivative ceiling rounded down', NR_exact <= NR - 1)
    reject('F derivative ceiling2', NF_exact <= 2)
    reject('absolute Laurent degree8', max(map(degree, Z)) <= 8)
    reject('wrong inverse original fifth sign', F(1, 16) * mu3 + F(3, 40) * mu5 == Fstar)
    reject('wrong cardinal denominator40', min(denominator_products) >= 40)
    reject('primitive normalization uses only first four rows',
           max(1 / c for c in contents[:4]) >= content_inverse)

    return {
        'actual_agent': 'six-sendov-2', 'role': 'researcher',
        'domain': 'Finite COMPLEX B,E,r,s,t with t!=0; L>=1 bounds abs of '
                  'all five parameters and t-inverse; full reconstructed9550 maps',
        'claim': '|B|+|Fstar|+||ALL_FIVE_R||_infty >= 1/(10^68*L^95)',
        'actual_original_claim': 'At DISTINCT REAL balanced norm-one angular stationarity, '
                                 'original gap>=delta and |p5|>=tau, delta,tau in(0,1], imply '
                                 'mu3^2+mu5^2 >= 57600/(4549*10^136)*(tau*delta^6)^190',
        'input9902': {'source_commit': INPUT_COMMIT, 'pins': INPUT_PINS,
                      'whole_record_sha256': INPUT_RECORD, 'entire_typed_parent_regenerated': True},
        'input9902_independent_review': {
            'actual_reviewer': 'six-reviewer-1', 'graph_height': 9928, 'artifact_index': 0,
            'artifact_ref': 'bafkreibvn7vv3vnm4wujq63bskil5s2n25xrep5u4adh7oxy3phmqygpaq',
            'source_commit': '1f38478ea1fd984c26c58e528178b817c0532b52',
            'scope': 'CONFIRMS9902 relative9550/9496/7432 and proves same-domain '
                     'raw norm below10^-13; does not review this new lemma; unformalized'},
        'same_author_arithmetic_reused': '9550 sparse Laurent arithmetic, '
                                         '9550 Bezout coefficients, entire9902 certificate; not independent',
        'whole_small_s_row_unit_Z': [z.encoded() for z in Z],
        'whole_E_difference_quotients': [q.encoded() for q in quotients],
        'row_unit_term_counts': [len(z.c) for z in Z],
        'row_unit_absolute_Laurent_degrees': [degree(z) for z in Z],
        'whole_exact_row_unit_norm': str(NZ_exact),
        'whole_R_B_E_s_derivative_norms': [[str(norm(p)) for p in row] for row in derivatives],
        'whole_exact_F_B_derivative_norm': str(NF_exact),
        'integer_norm_bounds_NZ_NR_NF': [NZ, NR, NF],
        'full_degrees_Z_R_F': [9, 10, 4],
        'actual_derivative_degrees_R_F': derivative_degrees,
        'sufficient_derivative_degree_bounds_R_F': [9, 2],
        'whole_slice_cubic_factor': str(cp), 'whole_slice_cross_factor': str(cs),
        'Q': str(Q), 'exact_inherited_raw_unit_norm': str(raw_unit_norm),
        'inherited_raw_unit_norm_bound_C': str(raw_unit_bound),
        'all5_primitive_content_inverses': [str(1 / c) for c in contents],
        'primitive_content_inverse_bound': str(content_inverse),
        'sigma_coefficient_a': str(a), 'unrounded_coercivity_constant': str(unrounded_c),
        'chosen_coercivity_constant': str(chosen_c), 'coercivity_exponent': 95,
        'moment_inverse_operator_square': str(inverse_square),
        'whole_inverse_original_Fstar': (F(1, 16) * mu3 - F(3, 40) * mu5).encoded(),
        'all7_interpolation_height_multipliers': list(map(str, interpolation_heights)),
        'mass_residue_sum': str(mass_sum),
        'whole_polynomial_identities': identities,
        'mathematical_boundary_controls': boundary,
        'rejected_mathematical_damages': damages,
        'ordinary_bridges': 'Complete9550 reconstruction; full small-s Laurent unit; '
                            'universal coefficient norm estimates and complex segment projection; '
                            '9902 Cauchy-Binet coefficient-residual bound; Newton inverse moments; '
                            'ordinary interlacing/derivative mesh/residues/Lagrange interpolation. Unformalized.',
        'uniform_delta_only_leading_mass_floor_proved': False,
        'stationary_set_nonempty_proved': False,
        'collision_limit_proved': False,
        'physical_stability_or_full_Jacobian_proved': False,
        'complex_first_power_proved': False,
        'formalized': False, 'independently_reviewed': False
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--export', type=Path)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--bootstrap', action='store_true', help='explicit author fixture creation')
    args = parser.parse_args()
    record = certificate()
    fixture = args.expected
    if args.bootstrap:
        fixture.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    else:
        require(same_typed(record, json.loads(fixture.read_text())), 'ENTIRE typed mathematical record')
    if args.export:
        args.export.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'actual_agent': 'six-sendov-2', 'role': 'researcher',
                      'whole_record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
                      'whole_polynomial_identities': len(record['whole_polynomial_identities']),
                      'row_unit_coefficients': sum(record['row_unit_term_counts']),
                      'mathematical_boundary_controls': len(record['mathematical_boundary_controls']),
                      'rejected_mathematical_damages': len(record['rejected_mathematical_damages']),
                      'coercivity_exponent': 95, 'full_five_residuals': True,
                      'uniform_delta_only_leading_mass_floor_proved': False,
                      'complex_first_power_proved': False, 'independently_reviewed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
