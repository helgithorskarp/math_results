"""Semantic certificate damage controls; both checkers must reject each."""
from copy import deepcopy
from pathlib import Path
import json
import check
import audit


def main():
    source = json.loads((Path(__file__).resolve().parent / 'CERTIFICATE.json').read_text())
    changes = []

    def add(label, mutate):
        data = deepcopy(source)
        mutate(data)
        changes.append((label, data))

    for name in source['parameter_checks']:
        add('scalar-' + name, lambda d, n=name: d['parameter_checks'].__setitem__(n, '-1'))
    add('omit-cross-contact', lambda d: d['G20_edges'].remove([7, 12]))
    add('aliased-core-corner', lambda d: d['patch_A']['faces'][1].__setitem__(1, 5))
    add('omit-triangle-adjacency', lambda d: d['patch_B']['tree_edges'].pop())
    add('change-long-boundary', lambda d: d['R'].__setitem__(3, 5))
    add('change-region-pairing', lambda d: d['boundary_pairings'][1]['lengths'].__setitem__(0, 5))
    add('missing-diagonal-subset', lambda d: d['all_diagonal_subsets'].pop())
    add('allow-U', lambda d: d['all_diagonal_subsets'][1].__setitem__('retained', True))
    add('omit-7-9-strictness', lambda d: d['all_diagonal_subsets'][3].__setitem__('reason', 'possible-empty'))
    add('allow-degree12-five', lambda d: d['V_degree_restrictions'][3].__setitem__('maximum_degree', 5))
    add('allow-degree9-five', lambda d: d['V_degree_restrictions'][1].__setitem__('maximum_degree', 5))
    add('alter-forced-triangle', lambda d: d['V_degree10_five_forced_faces'][0].__setitem__(0, 4))
    add('omit-whole-profile', lambda d: d['separated_profiles'].pop())
    add('omit-oriented-assignment', lambda d: d['oriented_component_assignments'].pop())
    add('allow-V-with-A-four', lambda d: next(q for q in d['oriented_component_assignments']
                                            if q['A'] == 4).__setitem__('V_branch_retained', True))
    add('force-profile-four-seven', lambda d: next(q for q in d['oriented_component_assignments']
                                                 if q['profile'] == [4, 7]).__setitem__('V_degree10_five_retained', True))
    add('erase-interior-edge', lambda d: d['disk_allocations'][0].__setitem__('interior_edges', 9))
    add('alter-face-allocation', lambda d: d['disk_allocations'][1]['TQP'].__setitem__(2, 2))
    add('wrong-Euler-data', lambda d: d['G20_VEF'].__setitem__(2, 9))
    add('erase-freshness-case', lambda d: d['V_degree10_five_noncore_check'].pop())
    add('erase-forced-TT-edge', lambda d: d['V_degree10_five_required_G24']['full_TT_edges'].pop())
    add('alter-forced-core-contact', lambda d: d['V_degree10_five_required_G24']['edges'][0].__setitem__(0, 3))
    add('widen-profile-band', lambda d: d['separated_profile_band'].__setitem__(0, '1/2'))
    add('unknown-field', lambda d: d.__setitem__('unsupported_extension', True))
    add('boolean-for-integer', lambda d: d['G20_VEF'].__setitem__(0, True))
    rejected = []
    for label, data in changes:
        for module in (check, audit):
            try:
                module.verify_data(data)
            except ValueError:
                pass
            else:
                raise ValueError('unrejected semantic damage: ' + label + '/' + module.__name__)
        rejected.append(label)
    valid = [deepcopy(source),
             json.loads(json.dumps(source, indent=3)),
             json.loads(json.dumps(source, sort_keys=True))]
    for data in valid:
        for module in (check, audit):
            module.verify_data(data)
    print(json.dumps({'semantic_damages_rejected_by_both': len(rejected),
                      'damages': rejected, 'valid_representations_accepted_by_both': len(valid)},
                     sort_keys=True))


if __name__ == '__main__':
    main()
