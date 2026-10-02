#!/usr/bin/env python3
"""Regenerate all quantitative domains independently of author code/data."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from budgets import Q, Certificates, ETA, DELTA, U, box, power2, domains, certificate, controls, need
from kernel import radial_record


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def parent_bounds(module, parent):
    checks = []
    for name in ['whole_original_cube', 'review9174_19eta_cover']:
        p = parent[name]
        def passed(condition, description):
            need(condition, description)
            checks.append(name + ': ' + description)
        passed(all(max(abs(Q(x)) for x in entry) < 1 for key in ['even_matrix', 'odd_matrix'] for row in p[key] for entry in row), 'every even/odd matrix entry modulus<1')
        passed(Q(p['even_determinant'][0]) > Q(9, 100), 'even determinant>9/100')
        passed(Q(p['odd_determinant'][1]) < -Q(3, 200), 'odd determinant<-3/200')
        passed(all(Q(row[0]) > Q(1, 9) for row in p['original_root_sine_squared']), 'both original-root sines>1/3')
        passed(all(max(abs(Q(x)) for x in p['parameter_box'][j]) < 2 for j in [0, 1]), 'branch x/y modulus<2')
        passed(1 < Q(p['parameter_box'][2][0]) <= Q(p['parameter_box'][2][1]) < 2, 'branch opening1<T<2')
    derivatives = parent['review9174_19eta_cover']['full_eta_derivative_certificate']['individual_multiplier_eta_derivatives']
    need(4 < Q(derivatives[0][0]) <= Q(derivatives[0][1]) < 17, 'credited full actual-cover third multiplier derivative')
    need(-8 < Q(derivatives[1][0]) <= Q(derivatives[1][1]) < -6, 'credited full actual-cover fourth multiplier derivative')
    c = module.embedding()
    constants = [module.enclose(module.K(row), c) for row in parent['exact_initial_normal_and_dual']['individual_root_multipliers']]
    need(constants[0].lo - Q(1, 32768) > Q(9, 4), 'entire explicit pair3 numerical-box margin')
    need(constants[1].lo - Q(8, 65536) - Q(1, 32768) > Q(75, 256), 'entire explicit pair4 numerical-box margin')
    selected = {name: {key: parent[name][key] for key in ['parameter_box', 'even_matrix', 'odd_matrix', 'even_determinant', 'odd_determinant', 'original_root_sine_squared', 'full_eta_derivative_certificate']} for name in ['whole_original_cube', 'review9174_19eta_cover']}
    return {'complete_regenerated_covering_inputs': selected, 'input_margin_checks': checks, 'limiting_weights': [x.record() for x in constants], 'pair4_uniform_fixed_weight_gap_after_loss': (constants[1] - Q(8, 65536) - Q(1, 32768) - Q(75, 256)).record(), 'inverse_bound_derivation': {'even_inverse_norm_upper': '200/9', 'odd_inverse_norm_upper': '400/3', 'sine_reciprocals_upper': '3', 'raw_normal_inverse_upper': '400*eta^-3/2', 'chosen_raw_inverse_majorant': '512*eta^-3/2'}}


def record():
    module, parent, digest, count = radial_record()
    inputs = parent_bounds(module, parent)
    old, new = domains(True), domains(False)
    a, b = certificate(old), certificate(new)
    identities = Certificates()
    for name, expected in [('tail', power2(-82, 3)), ('target', power2(-131, 6)), ('radial', power2(-293, 12)), ('free', power2(-413, 22, 1)), ('raw', power2(-415, 22, 1)), ('critical', power2(-425, 25, 1)), ('coefficient', power2(-2557, 152, 6))]:
        identities.equal('new full symbolic ' + name, getattr(new, name), expected)
    identities.equal('whole symbolic coefficient-radius enlargement', new.coefficient / old.coefficient, power2(1836, -42))
    fixed = new.coefficient / DELTA**6 / 2**18
    identities.equal('k1/4 conservative coefficient radius', fixed, power2(-2575, 152))
    need(Q(1, 4) - Q(33, 16 * 65536) > Q(1, 8), 'all eta k1/4 gap>1/8')
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer', 'eta_domain': ['positive', '1/65536'], 'k_domain': ['nonnegative', 'strictly below1/2-33eta/16'], 'method': 'Own source-bound radial regeneration; independent literal weighted critical motion/original-root contour bounds and exact nonnegative-monomial ratios on the full sqrt-eta/k-gap rectangle; no target code/data imported', 'own_input_files_verified': count, 'whole_parent_canonical_sha256': digest, 'parent_inputs': inputs, 'original9315_budgets': a, 'new_budgets': b, 'all_symbolic_exponent_identities': identities.rows, 'controls': controls(), 'proved_refinements': {'coefficient_max_radius': 'delta^6*2^-2557*eta^76', 'k1quarter_coefficient_radius': '2^-2575*eta^76', 'enlargement_over_both_original_radii': '2^1836*eta^-21', 'fixed_individual_pair_weights': ['9/4', '75/256'], 'common_slack_weight': '75/256', 'strict_minimum_at_k1quarter': True, 'all_nonlinear_radii': 'explicit, eta/k-dependent; no uniform positive eta0 or global competitor entry'}, 'trust_boundary': 'Exact budget certificates and previous independently reviewed kernels. Complexified actual-root labels, scalar/operator Cauchy, nonlinear contraction/holomorphic tail, actual feasible signed paths and collision-safe coefficient Rouche/moment recovery remain ordinary unformalized analytic bridges.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fixture', type=Path, default=HERE / 'EXPECTED.json')
    p.add_argument('--emit-fixture', type=Path)
    args = p.parse_args()
    expected = None if args.emit_fixture else json.loads(args.fixture.read_text())
    actual = record()
    if args.emit_fixture:
        args.emit_fixture.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        need(canonical(actual) == canonical(expected), 'complete independent neighborhood record')
    print('PASS independent numerical-neighborhood audit', hashlib.sha256(canonical(actual)).hexdigest())
    print(json.dumps(actual['proved_refinements'], sort_keys=True))


if __name__ == '__main__':
    main()
