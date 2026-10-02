"""Check valid alternate normalization and damaged mathematical certificates."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('standalone_facial_auditor', Path(__file__).with_name('audit.py'))
auditor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auditor)


def main():
    base = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    positive = auditor.audit(base)
    alternate = deepcopy(base)
    for row in alternate['closure_cases']:
        row['content'] //= 2
        row['reduced_coefficients'] = [str(2 * Fraction(x)) for x in row['reduced_coefficients']]
        row['reduced_bernstein'] = [str(2 * Fraction(x)) for x in row['reduced_bernstein']]
    other = auditor.audit(alternate)
    if positive['certificate_sha256'] == other['certificate_sha256']:
        raise ValueError('alternate valid normalization must change bytes')
    cases = []

    def damage(name, edit):
        altered = deepcopy(base)
        edit(altered)
        try:
            auditor.audit(altered)
        except (ValueError, KeyError, TypeError, IndexError) as error:
            cases.append({'damage': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('damaged certificate accepted: ' + name)

    damage('omitted_local_survivor', lambda d: d['aliases']['complete_local_survivors'].pop())
    damage('added_false_local_survivor', lambda d: d['aliases']['complete_local_survivors'].append({'0': 1}))
    damage('altered_one_map_digest', lambda d: d['aliases'].__setitem__('all_map_decision_sha256', '0' * 64))
    damage('altered_intrinsic_Gram_polynomial', lambda d: d['intrinsic_pair_table'][0]['numerator'].__setitem__(0, '1'))
    def gap_damage(d):
        row = next(x for x in d['intrinsic_pair_table'] if not x['contact'])
        row['gap_bernstein'][0] = '-1'
    damage('nonpositive_intrinsic_gap', gap_damage)
    damage('altered_reduced_polynomial', lambda d: d['closure_cases'][0]['reduced_coefficients'].__setitem__(0, '-17'))
    def negative_bernstein(d):
        row = d['closure_cases'][1]
        row['reduced_bernstein'][0] = str(Fraction(row['reduced_bernstein'][0]) - 1)
    damage('altered_still_negative_Bernstein_coefficient', negative_bernstein)
    damage('altered_factor_content', lambda d: d['closure_cases'][0].__setitem__('content', 4097))
    damage('omitted_Gram_case', lambda d: d['closure_cases'].pop())
    damage('altered_actual_face_pattern', lambda d: d['pentagonal_face'].__setitem__(0, 11))
    damage('altered_closed_domain', lambda d: d['closed_c_interval'].__setitem__(1, '592/1000'))
    def multiplicity_damage(d):
        row = d['closure_cases'][2]
        row['linear_factors'][0]['multiplicity'] -= 1
        row['closure_degree'] -= 1
    damage('altered_factor_with_repaired_degree', multiplicity_damage)
    print(json.dumps({'status': 'CHECKED_FACIAL_CERTIFICATE_CONTROLS',
                      'valid_original_accepted': True, 'valid_alternate_normalization_accepted': True,
                      'byte_hash_is_not_acceptance_predicate': True,
                      'damaged_certificates_rejected': len(cases), 'damage_results': cases,
                      'independent_person_review': False}, sort_keys=True))


if __name__ == '__main__':
    main()
