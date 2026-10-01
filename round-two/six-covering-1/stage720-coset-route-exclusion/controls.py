"""Reject meaningful damaged scope/phase/bound data, including under -O."""
from copy import deepcopy
import json

from check import HERE, compute, validate


def main():
    c = json.loads((HERE / 'certificate.json').read_text())
    first, second, _ = compute(c)
    validate(c, first, second)
    damages = {}

    def add(name, mutate):
        bad = deepcopy(c)
        mutate(bad)
        damages[name] = bad

    add('retain_consumed_original12', lambda d: d['free_after12'].append(12))
    add('retain_consumed_original16', lambda d: d['free_after12_16'].append(16))
    add('omit_original720', lambda d: d['original_labels'].pop())
    add('omit_twelve_phase', lambda d: d['first_rows'].pop())
    add('repeat_twelve_phase', lambda d: d['first_rows'].__setitem__(11, d['first_rows'][10]))
    add('omit_sixteen_phase', lambda d: d['second_rows'].pop())
    add('alter_actual_odd_demand', lambda d: d['first_rows'][0].__setitem__(-3, 239))
    add('alter_even_upper', lambda d: d['second_rows'][0].__setitem__(-1, d['second_rows'][0][-1] + 1))
    add('change_target_divisor', lambda d: d.__setitem__('target_divisors', [18, 4]))
    add('change_dependency_pin', lambda d: d['dependency'].__setitem__('certificate_sha256', '0' * 64))
    add('use_nonunit_affine_map', lambda d: d.__setitem__('affine_map', [6, 48]))
    add('remove_one_child_parent', lambda d: d['second_parent_prefixes'].pop())
    for name, bad in damages.items():
        try:
            validate(bad, first, second)
        except RuntimeError:
            continue
        raise RuntimeError('damaged certificate accepted: ' + name)
    print(json.dumps({'agent': 'six-covering-1', 'role': 'researcher', 'status': 'CONTROLS_PASSED',
                      'semantic_damages_rejected': len(damages), 'damages': list(damages)}, sort_keys=True))


if __name__ == '__main__':
    main()
