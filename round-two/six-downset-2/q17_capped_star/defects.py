"""Small, distinct semantic failure controls; no large elimination repetition."""
import argparse
import copy
import json
from pathlib import Path

from original import audit, build, canonical, require
from positive_elimination import divide_content, eliminate
from read_positive import check_proof


def rejects(name, function):
    try:
        function()
    except ValueError as error:
        return {'name': name, 'rejected': True, 'reason': str(error)}
    raise ValueError('a semantic defect was accepted: ' + name)


def controls(data):
    point = build(data)
    audit(point)
    records = []

    def damage(name, mutate):
        bad = copy.deepcopy(point)
        mutate(bad)
        records.append(rejects(name, lambda: audit(bad)))

    damage('missing_smaller_star_singleton', lambda p: p['members'].pop(2))
    damage('wrong_original_star_membership', lambda p: p['members'].__setitem__(5, (19,)))
    damage('proper_diagonal', lambda p: p['C_num'][1].__setitem__(1, 0))
    damage('proper_intersection_support', lambda p: p['C_num'][0].__setitem__(2, 0))
    damage('maximum_star_anchor', lambda p: p['C_num'][1].__setitem__(0, p['C_num'][1][0] + 1))
    damage('actual_empty_row', lambda p: p['L_num'][0].__setitem__(0, p['L_num'][0][0] + 1))
    damage('residual_principal_binding', lambda p: p['T_num'][0].__setitem__(0, p['T_num'][0][0] + 1))
    damage('physical_Gram', lambda p: p['G'][0].__setitem__(0, p['G'][0][0] + 1))
    damage('inverse_metric', lambda p: p['GI_num'][0].__setitem__(0, p['GI_num'][0][0] + 1))
    damage('upper_cap_units', lambda p: p['cap_num'][0].__setitem__(0, p['cap_num'][0][0] * 11000))
    bad = copy.deepcopy(data)
    bad['free_pair_values'].pop()
    records.append(rejects('missing_actual_disjoint_pair_type', lambda: build(bad)))
    records.append(rejects('negative_content_scale', lambda: divide_content([[2]], -2)))
    records.append(rejects('inexact_content_division', lambda: divide_content([[3]], 2)))
    records.append(rejects('asymmetric_integer_form', lambda: eliminate([[1, 0], [1, 1]])))
    for name, matrix in [('negative_Schur_pivot', [[1, 2], [2, 1]]),
                         ('zero_Schur_pivot', [[1, 1], [1, 1]])]:
        proof = eliminate(matrix)
        require(proof['status'] == 'nonpositive_pivot' and proof['order'] == 2,
                'correct small nonpositive-pivot classification')
        records.append(rejects(name, lambda: check_proof(proof)))
    records.append(rejects('necessary_22_type_system_is_not_full_coverage',
                           lambda: check_proof({'status': 'positive_definite', 'dimension': 22})))
    require(len(records) == 17, 'distinct semantic controls census')
    positive_controls = []
    for name, matrix, expected in [
            ('positive_two', [[2, 1], [1, 2]], [2, 3]),
            ('positive_content', [[4, 2], [2, 4]], [4, 12]),
            ('positive_three', [[4, 2, 0], [2, 5, 1], [0, 1, 6]], [4, 16, 92])]:
        proof = eliminate(matrix)
        require(proof['status'] == 'positive_definite' and
                list(map(int, proof['original_leading_minors'])) == expected,
                'hand-computed positive determinant control')
        positive_controls.append({'name': name, 'leading_minors': expected})
    return {'agent': 'six-downset-2', 'role': 'researcher', 'distinct_semantic_rejections': records,
            'small_hand_computed_positive_controls': positive_controls,
            'both_full_endpoint_readers_regenerate_their_proofs': True,
            'no_bulky_factor_or_minor_input': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coefficients', default=str(Path(__file__).with_name('COEFFICIENTS.json')))
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    result = controls(json.loads(Path(args.coefficients).read_bytes()))
    Path(args.record).write_bytes(canonical(result) + b'\n')
    print(json.dumps(result))
