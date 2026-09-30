"""Exact asymmetric-slice refinement after the independent full audit.

Run audit.py against expected.json first. This short checker verifies the
constants used in the written proof; it does not regenerate large tensors.
Actual author six-reviewer-3, independent mathematical reviewer.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def derive(record):
    canonical = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
    need(hashlib.sha256(canonical).hexdigest() ==
         'bb180f3d7dfbc70e82b03d03af5309eea9a799df65424e2dff0276461de3dad0',
         'Full independently regenerated audit record differs')
    cells = record['target_cells']
    need(len(cells) == 6 and record['target_coefficients'] == 923763,
         'Incorrect weighted certificate inventory')
    gamma = F(1, 16)
    for cell in cells[:2]:
        need(F(cell['minimum']) >= gamma, 'Low-phase even margin too small')
    need(cells[2]['zeros'] == 1 and F(cells[2]['minimum_positive']) >= gamma,
         'Corner even margin too small')
    need(all(F(cells[2][key]) >= gamma for key in
             ('zeroth_c_minimum', 'zeroth_x_minimum')), 'Even strict slice too small')
    A_c, A_x = (F(cells[3][key]) for key in
                 ('zeroth_c_minimum', 'zeroth_x_minimum'))
    theta = F(4, 7)
    candidates = [A_c*theta**19, A_x*(2*(1-theta))**19,
                  F(cells[4]['minimum']), F(cells[5]['minimum'])]
    C = min(candidates)
    need(C == A_x*F(6, 7)**19, 'Different controlling asymmetric slice')
    kappa = C/8
    need(0 < kappa < gamma, 'Endpoint comparison constant fails')
    previous = A_x/2**22
    ratio = kappa/previous
    need(ratio == F(12, 7)**19 and ratio > 28000, 'Claimed improvement fails')
    return {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'split_fraction': str(theta), 'zeroth_c_slice': str(A_c),
            'zeroth_x_slice': str(A_x),
            'envelope_phase_constant': str(C), 'weighted_margin_constant': str(kappa),
            'previous_review5_margin_constant': str(previous),
            'improvement_factor': str(ratio), 'improvement_factor_formula': '(12/7)^19',
            'new_inequality': 'N(b) >= 1 + kappa*(1-c*x)^16',
            'scope': 'positive-skew weighted domain of7833; not all weighted parameters',
            'full_tensor_regeneration_required': 'audit.py --expected expected.json',
            'kernel_independent_record_sha256': hashlib.sha256(canonical).hexdigest()}


def main():
    actual = derive(json.loads((ROOT/'expected.json').read_text()))
    need(actual == json.loads((ROOT/'phase_margin_expected.json').read_text()),
         'Asymmetric margin manifest differs')
    print(json.dumps({'result': 'PASS',
          'weighted_margin_constant': actual['weighted_margin_constant'],
          'improvement_factor': actual['improvement_factor'],
          'improvement_greater_than_28000': True}, sort_keys=True))


if __name__ == '__main__':
    main()
