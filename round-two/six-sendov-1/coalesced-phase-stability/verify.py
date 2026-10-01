#!/usr/bin/env python3
"""Regenerate the complete algebra and compare a fixed compact record."""
import argparse
import copy
import json
from pathlib import Path
import sys

# Explicit own-directory import also works under python -I.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import canonical, digest, regenerate, require


def compare(expected, actual):
    require(canonical(expected) == canonical(actual), 'complete canonical fixture mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    actual = regenerate()
    expected = json.loads(args.expected.read_text())
    compare(expected, actual)
    damages = []
    for label in ('missing-field', 'changed-bound', 'omitted-coefficient', 'wrong-type'):
        bad = copy.deepcopy(expected)
        if label == 'missing-field':
            bad.pop('threshold')
        elif label == 'changed-bound':
            bad['threshold']['lo'] = '0'
        elif label == 'omitted-coefficient':
            bad['bounds']['c_ge_half']['bernstein'].pop()
        else:
            bad['bernstein_count'] = 72.0
        try:
            compare(bad, actual)
        except ValueError:
            damages.append(label)
        else:
            raise ValueError('fixture damage accepted: '+label)
    print(json.dumps({'status': 'PASS', 'record_sha256': digest(actual),
                      'full_phase_polynomial_identities': actual['directional_identity_count'],
                      'positive_bernstein_coefficients': actual['bernstein_count'],
                      'mathematical_damage_rejections': len(actual['mathematical_damage_rejections']),
                      'fixture_damage_rejections': damages,
                      'threshold': actual['threshold']}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as error:
        print('FAIL: '+str(error), file=sys.stderr)
        raise SystemExit(1)
