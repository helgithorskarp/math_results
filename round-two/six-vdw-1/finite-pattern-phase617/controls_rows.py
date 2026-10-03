"""Actual positive row classification and damaged literal row/AP controls."""
from copy import deepcopy
import json
from pathlib import Path

from check_rows import check, need


if __name__ == '__main__':
    record = json.loads((Path(__file__).resolve().parent/'phase-rows-v2.json').read_bytes())
    positive = check(record)
    damaged = []

    def reject(name, mutation, reason):
        bad = deepcopy(record)
        mutation(bad)
        need(bad != record, 'actual changed row certificate:'+name)
        try:
            check(bad)
        except ValueError as error:
            need(str(error) == reason, 'wrong row rejection:'+name+':'+str(error))
            damaged.append({'name': name, 'rejection': str(error)})
        else:
            raise ValueError('damaged actual row certificate accepted:'+name)

    reject('wrong_original_roots', lambda r: r.__setitem__('roots', [0, 1, 5]),
           'chosen actual same-phase original family')
    reject('missing_actual_truth_table', lambda r: r['all256_table_obstruction_APs_by_phase'][0].pop(),
           'entire six times256 original truth tables')
    reject('missing_actual_nonprojection_obstruction',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0].__setitem__(0, None),
           'every actual nonprojection table has a literal obstruction')
    reject('fake_positive_projection_obstruction',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0].__setitem__(15, [6, 6]),
           'actual surviving projection rows are positive controls')
    reject('actual_zero_step',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0][0].__setitem__(1, 0),
           'actual nonconstant row AP belongs to original finite interval')
    reject('actual_wrong_phase',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0][0].__setitem__(0, 7),
           'every actual row AP has its declared original phase')
    reject('actual_original_root_included',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0].__setitem__(0, [0, 6]),
           'actual row obstruction avoids every original root occurrence')
    # A literal square-set control independently finds a nonmonochromatic
    # root-free same-phase AP for the nonprojection truth table00000001.
    squares = {x*x % 617 for x in range(1, 617)}
    counter = None
    for a in range(6, 600, 6):
        ns = [a+j*6 for j in range(7)]
        if any(n % 617 in (0, 1, 4) for n in ns):
            continue
        keys = [4*int(n % 617 not in squares)+2*int((n-1) % 617 not in squares)
                +int((n-4) % 617 not in squares) for n in ns]
        if len({(1 >> key) & 1 for key in keys}) == 2:
            counter = [a, 6]
            break
    need(counter is not None, 'genuine literal nonmonochromatic damaged word image')
    reject('actual_obstruction_colors_not_constant',
           lambda r: r['all256_table_obstruction_APs_by_phase'][0].__setitem__(1, counter),
           'actual seven-point obstruction is monochromatic for its whole truth table')
    reject('unsupported_prefix_bound', lambda r: r.__setitem__('necessary_projection_only_prefix_length', 631),
           'literal quantified projection-only prefix bound')
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'ACTUAL_PHASE_ROW_POSITIVE_AND_SEMANTIC_DAMAGE_CONTROLS_PASS',
                      'positive_entire_row_classification': positive,
                      'semantic_damage_rejections': len(damaged), 'damages': damaged,
                      'external_review_claimed': False}, sort_keys=True))
