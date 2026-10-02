#!/usr/bin/env python3
"""Independent full complex response certificate with exact rational intervals."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from complex_sector import initial, certify, F, need
from literal_checks import run

HERE = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def separation():
    a0, radius = F(65535, 65536), F(255, 256)
    phase_square_cap = F(3, 1280000)
    cosine_floor = 1 - phase_square_cap / 2
    hcap = 1 / ((1 + a0) * cosine_floor)
    radius_floor = 1 / (1 + radius)
    slack_floor = radius_floor - hcap
    margin = 7 * slack_floor - F(3, 512)
    need(cosine_floor > 0 and slack_floor > 0 and margin > 0, 'expanded seven-small-critical separated domain')
    need(margin == F(12028703059311, 12541194125030912), 'whole exact expanded separation margin')
    return {'marked_real_root_closed_interval': [str(a0), '1'],
        'seven_selected_small_critical_modulus_upper': str(radius),
        'heavy_critical_modulus_restriction': None,
        'full_phase_norm_squared_cap': 'gamma/160000',
        'cosine_lower': str(cosine_floor), 'threshold_h_upper': str(hcap),
        'reciprocal_radius_lower': str(radius_floor), 'individual_slack_lower': str(slack_floor),
        'seven_slack_minus_maximum_budget_positive_margin': str(margin),
        'conclusion': 'phase/slack domain impossible when all seven labelled small critical moduli<=255/256; some selected small critical has modulus>255/256 if that domain holds'}


def record():
    controls = run()
    values, Y, w0, w1, tstar, exact = initial()
    full = certify(values, Y, w0, w1, tstar, F(1, 1024))
    tight = certify(values, Y, w0, w1, tstar, F(19, 65536))
    for which, lower, upper, clower, cupper in [(full, F(17, 4), F(9, 2), F(500), F(560)), (tight, F(13, 3), F(53, 12), F(510), F(550))]:
        need(F(which['odd_determinant'][1]) < -F(3, 200), 'stronger odd determinant margin')
        need(lower < F(which['centered_imaginary_eta2_eigenvalue'][0]) <= F(which['centered_imaginary_eta2_eigenvalue'][1]) < upper, 'sharper centered imaginary eigenvalue')
        need(clower < F(which['common_imaginary_eta2_directional_coefficient'][0]) <= F(which['common_imaginary_eta2_directional_coefficient'][1]) < cupper, 'sharper common imaginary eigenvalue')
    prior = json.loads((HERE.parent / 'centered-sector-audit' / 'EXPECTED.json').read_text())
    need(exact['parent_initial'] == prior['exact_initial_split'], 'entire previous independently audited exact initial record')
    need(full['parent_real_certificate'] == prior['full_parent_cube'], 'entire previous full-box real certificate regenerated')
    need(tight['parent_real_certificate'] == prior['review9174_certified19eta_box'], 'entire previous sharper real certificate regenerated')
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
        'method': 'literal anchored critical products; divided-sine real circle arithmetic; exact Fraction intervals; own full symmetric third tensor; nonnegative componentwise resolvent; separate individual-root Gaussian Taylor controls',
        'eta_domain': ['positive', '1/65536'], 'controls': controls,
        'exact_initial_complex_response': exact, 'full_original_cube': full,
        'review9174_19eta_box': tight, 'expanded_reciprocal_domain_separation': separation(),
        'proved_strengthenings': {'whole_original_cube_odd_determinant_upper': '-3/200',
            'whole_original_cube_centered_imaginary_eta2_window': ['17/4', '9/2'],
            'whole_original_cube_common_imaginary_eta2_window': ['500/3', '560/3'],
            'actual_branch_centered_imaginary_eta2_window': ['13/3', '53/12'],
            'actual_branch_common_imaginary_eta2_window': ['170', '550/3'],
            'full_Hessian_eta2_lower_on_centered_real_orthogonal_complement': '15/4',
            'full_Hessian_eta2_gap_above_least_on_orthogonal_complement': '11/4',
            'pointwise_anisotropic_local_energy_coefficients': {'centered_real': '1/2-(33/16)*eta', 'common_real': '15/8', 'centered_imaginary': '13/6', 'common_imaginary': '85'},
            'all_displacement_radii': 'existential at each fixed positive eta; no uniform or numerical radius'},
        'necessary_math_dependencies': ['9113/9174 actual branch, simple legal roots and scalar common-real curvature', '9164/9203 previously independently audited even five-block, centered real response and real least eigenvalue'],
        'trust_boundary': 'hash-bound own reviewed parent arithmetic plus new Gaussian/circle/response code; no researcher executable or expected data supplies independent calculations; ordinary full real Jacobian, IFT, root continuity, conjugation/permutation Hessian, mean-value normalization and Taylor/separation inequalities unformalized'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', type=Path, default=HERE / 'EXPECTED.json')
    parser.add_argument('--emit-fixture', type=Path)
    args = parser.parse_args()
    expected = None if args.emit_fixture else json.loads(args.fixture.read_text())
    actual = record()
    if args.emit_fixture:
        args.emit_fixture.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        need(canonical(actual) == canonical(expected), 'entire independent complex frozen record')
    print('PASS independent full complex certificate', hashlib.sha256(canonical(actual)).hexdigest())
    print(json.dumps(actual['proved_strengthenings'], sort_keys=True))


if __name__ == '__main__':
    main()
