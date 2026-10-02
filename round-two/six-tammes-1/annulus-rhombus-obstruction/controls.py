"""Meaningful certificate damage tests and valid representation controls."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import json
from audit import verify


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    original = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    verify(original)
    damages = {}

    def add(label, mutate):
        changed = deepcopy(original)
        mutate(changed)
        require(changed != original, 'damage must change the object')
        try:
            verify(changed)
        except ValueError as error:
            damages[label] = str(error)
        else:
            raise ValueError('damage accepted: ' + label)

    def change_coefficient(data, field):
        value = data['star_cases'][0][field]['numerator']
        value[0] = str(F(value[0]) + 1)

    add('missing_star', lambda d: d['star_cases'].pop())
    add('duplicate_star', lambda d: d['star_cases'].__setitem__(2, deepcopy(d['star_cases'][0])))
    for field in ('B_over_A', 'S_over_A', 'P', 'Delta', 'solver_divisor_over_A'):
        add('changed_' + field, lambda d, field=field: change_coefficient(d, field))
    add('wrong_discriminant_Bernstein', lambda d: d['star_cases'][2]['Delta_numerator_Bernstein'].__setitem__(0, '0'))
    add('wrong_divisor_Bernstein', lambda d: d['star_cases'][1]['solver_divisor_numerator_Bernstein'].__setitem__(0, '0'))
    add('physical_endpoint_one_included', lambda d: d.__setitem__('physical_upper_endpoint_excluded', False))
    add('unsupported_lower_band', lambda d: d['algebraic_closed_band'].__setitem__(0, '2/5'))
    add('missing_ring', lambda d: d['rings'].pop())
    add('duplicate_ring', lambda d: d['rings'].__setitem__(1, deepcopy(d['rings'][0])))
    add('overlapping_ports', lambda d: d['rings'][0]['ports'].__setitem__(0, 1))
    add('deleted_quotient_vertex', lambda d: d['rings'][0]['classes'][0].pop())
    add('missing_boundary_arc', lambda d: d['rings'][0]['boundary_arcs'].pop())
    add('collapsed_boundary_cycle', lambda d: d['rings'][0]['boundary_cycles'][0].__setitem__(1, d['rings'][0]['boundary_cycles'][0][0]))
    add('missing_seam', lambda d: d['rings'][0]['seams'].pop())
    add('wrong_seam_endpoint', lambda d: d['rings'][0]['seams'][0]['endpoints'].__setitem__(1, d['rings'][0]['seams'][0]['endpoints'][0]))
    add('wrong_mixed_count', lambda d: d['rings'][0]['mixed_corners_per_boundary'].__setitem__(0, 2))
    add('wrong_prism_Gram', lambda d: d['prism_calibration']['Gram'][0].__setitem__(0, '6/7'))
    add('missing_prism_contact', lambda d: d['prism_calibration']['contact_pairs'].pop())
    add('wrong_adjacent_angle_identity', lambda d: d['adjacent_angle_factorization']['left'].__setitem__(0, '0'))
    positives = {}

    def valid(label, mutate):
        changed = deepcopy(original)
        mutate(changed)
        require(changed != original, 'positive control must change the object')
        verify(changed)
        positives[label] = 'accepted'

    def scale(data):
        for row in data['star_cases']:
            for part in ('numerator', 'denominator'):
                row['Delta'][part] = [str(2 * F(x)) for x in row['Delta'][part]]
            for part in ('Delta_numerator_Bernstein', 'Delta_denominator_Bernstein'):
                row[part] = [str(2 * F(x)) for x in row[part]]

    def cycles(data):
        for row in data['rings']:
            row['boundary_cycles'] = [(cycle[1:] + cycle[:1])[::-1] for cycle in row['boundary_cycles'][::-1]]

    def classes(data):
        for row in data['rings']:
            row['classes'] = [group[::-1] for group in row['classes'][::-1]]

    valid('positive_rational_rescaling', scale)
    valid('cycle_rotation_reversal_and_order', cycles)
    valid('class_and_member_order', classes)
    valid('complete_row_order', lambda d: (d['star_cases'].reverse(), d['rings'].reverse()))
    valid('prism_face_cyclic_rotation', lambda d: d['prism_calibration'].__setitem__('faces', [f[1:] + f[:1] for f in d['prism_calibration']['faces']]))
    require(len(damages) == 23 and len(positives) == 5, 'whole control census')
    print(json.dumps({'damages_rejected': len(damages), 'damage_reasons': damages,
                      'valid_controls_accepted': len(positives), 'valid_controls': positives,
                      'outside_band_calibration': 'c=1/7 is a feasible TQQ prism, not excluded'}, sort_keys=True))


if __name__ == '__main__':
    main()
