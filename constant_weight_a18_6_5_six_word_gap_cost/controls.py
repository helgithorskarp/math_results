"""Input-normalization and resource-status controls. six-code-2, researcher."""
from copy import deepcopy
from pathlib import Path
import json
import time

import verify
from common import guard, require, STATE_LIMIT, SECONDS_LIMIT


def main():
    base = json.loads((Path(__file__).parent / 'input.json').read_text())
    cases = []
    def add(name, mutate):
        value = deepcopy(base)
        mutate(value)
        cases.append((name, value))
    add('duplicate_circle', lambda d: d['design_circles'].__setitem__(1, d['design_circles'][0]))
    add('missing_circle', lambda d: d['design_circles'].pop())
    add('wrong_block_weight', lambda d: d['design_circles'].__setitem__(0, d['design_circles'][0]
                                                                   & (d['design_circles'][0] - 1)))
    add('out_of_carrier_mask', lambda d: d['design_circles'].__setitem__(0, 1 << 17))
    add('duplicate_map_image', lambda d: d['actual_transport_generators'][0].__setitem__(1,
                                                   d['actual_transport_generators'][0][0]))
    add('non_design_permutation', lambda d: d['actual_transport_generators'].__setitem__(0,
                                                   [1, 0, *range(2, 17)]))
    add('incomplete_transport', lambda d: d['actual_transport_generators'].pop(2))
    add('contained_root', lambda d: d.__setitem__('root_word', d['design_circles'][0]
                                                           & (d['design_circles'][0] - 1)))
    add('duplicate_sharp_part', lambda d: d['sharp_four_parts'].__setitem__(1, d['sharp_four_parts'][0]))
    rejected = []
    for name, value in cases:
        try:
            verify.run(value)
        except ValueError as error:
            require('INCOMPLETE' not in str(error), 'corruption hit a guard instead of rejection')
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: ' + name)
    incomplete = []
    for name, args in [('state_guard', (time.monotonic(), STATE_LIMIT + 1)),
                       ('expired_time_guard', (time.monotonic() - SECONDS_LIMIT - 1, 0))]:
        try:
            guard(*args)
        except ValueError as error:
            require('INCOMPLETE' in str(error) and 'UNKNOWN' in str(error), 'wrong resource status')
            incomplete.append(name)
        else:
            raise ValueError('resource guard silently accepted: ' + name)
    require(len(rejected) == 9 and len(incomplete) == 2, 'controls incomplete')
    print(json.dumps({'agent': 'six-code-2', 'role': 'researcher',
                      'rejected_corruptions': rejected, 'resource_controls_unknown': incomplete,
                      'all_passed': True}, indent=2))


if __name__ == '__main__':
    main()
