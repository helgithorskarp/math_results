#!/usr/bin/env python3
"""Regenerate the whole certificate and compare its compact fixed record."""
import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import regenerate_record, digest, require
from origin import canonical


def compare(expected, actual):
    require(canonical(expected) == canonical(actual), 'complete canonical fixture mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    actual = regenerate_record()
    expected = json.loads(args.expected.read_text())
    compare(expected, actual)
    rejected = []
    for label in ('missing-field', 'changed-weight', 'omitted-coefficient', 'wrong-type'):
        bad = copy.deepcopy(expected)
        if label == 'missing-field':
            bad.pop('whole_interval_bounds')
        elif label == 'changed-weight':
            bad['fixed_weight'] = '1'
        elif label == 'omitted-coefficient':
            bad['whole_interval_bounds']['shifted_collective_determinant']['bernstein'].pop()
        else:
            bad['bernstein_coefficient_count'] = 85.0
        try:
            compare(bad, actual)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('fixture damage accepted: '+label)
    print(json.dumps({'status':'PASS','record_sha256':digest(actual),
                      'fixed_weight':actual['fixed_weight'], 'cutoff':actual['cutoff'],
                      'origin_phase_identities':actual['origin_phase_identity_count'],
                      'polar_phase_identities':actual['polar_phase_identity_count'],
                      'integral_polynomial_identities':actual['integral_polynomial_identity_count'],
                      'positive_bernstein_coefficients':actual['bernstein_coefficient_count'],
                      'mathematical_damage_rejections':len(actual['mathematical_damage_rejections']),
                      'fixture_damage_rejections':rejected},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as error:
        print('FAIL: '+str(error),file=sys.stderr)
        raise SystemExit(1)
