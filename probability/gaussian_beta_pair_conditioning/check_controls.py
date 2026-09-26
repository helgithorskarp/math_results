#!/usr/bin/env python3
"""Reject false extensions, incomplete residual lists and damaged witnesses."""
from copy import deepcopy
import json
from pathlib import Path
from verify import audit, compact_bound, require


def main():
    original = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    audit(original)
    tests = []
    data = deepcopy(original)
    data['maximum_complement'] = 7
    tests.append(('unsupported seventh difference', data, 'proved dimension and complement range'))
    data = deepcopy(original)
    data['remaining_patterns'].pop()
    tests.append(('omitted residual partition', data, 'complete first residual cases'))
    data = deepcopy(original)
    data['boundary_paired_determinant'] = '512'
    tests.append(('wrong affine determinant', data, 'rank-six boundary determinant'))
    data = deepcopy(original)
    data['boundary_distinguished_labels'] = [0, 1]
    tests.append(('pair does not leave seven labels', data, 'remaining seven distinct labels'))
    data = deepcopy(original)
    data['boundary_pair_loss'] = '0'
    tests.append(('false zero-loss pair', data, 'boundary distinguished pair loss'))
    rejected = []
    for name, data, expected in tests:
        try:
            audit(data)
        except ValueError as exc:
            require(str(exc) == expected, name + ': wrong rejection boundary')
            rejected.append(name)
        else:
            raise ValueError('Accepted damaged certificate: ' + name)
    try:
        compact_bound(3, 7, 0)
    except ValueError as exc:
        require(str(exc) == 'outside proved complement range', 'wrong coefficient rejection')
        rejected.append('b_(7,0) is outside this certificate')
    else:
        raise ValueError('Unproved coefficient accepted')
    print(json.dumps({'status': 'BETA_CONDITIONING_DAMAGE_CONTROLS_PASS',
                      'rejected': rejected}, indent=2))


if __name__ == '__main__':
    main()
