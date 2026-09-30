#!/usr/bin/env python3
"""Check positive evidence and nine corrupt proofs or coverage hypotheses."""
import argparse
import copy
import json
from pathlib import Path
import verify


def rejected(name, action):
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return name
    raise AssertionError(f"Corrupted proof accepted: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path, default=Path('build'))
    args = parser.parse_args()
    bundle = {name: json.loads((args.directory / name).read_text()) for name in verify.required_names()}
    assert verify.verify_suite(bundle)['verified']
    passed = []

    case = copy.deepcopy(bundle['branch-0-1852.json'])
    case['budget'][0] = 28
    passed.append(rejected('wrong edited-class budget', lambda: verify.verify_branch(case)))

    case = copy.deepcopy(bundle['branch-0-1852.json'])
    row = next(r for r in case['records'] if r[0] == 'f' and len(r[2]) > 1)
    row[2][-1] = row[2][0].copy()
    passed.append(rejected('intersecting petal packing', lambda: verify.verify_branch(case)))

    case = copy.deepcopy(bundle['branch-0-1852.json'])
    case['records'] = []
    passed.append(rejected('final contradiction without deductions', lambda: verify.verify_branch(case)))

    case = copy.deepcopy(bundle['branch-0-1.json'])
    forcing = next(r.copy() for r in case['records'] if r[0] == 't')
    case['records'].insert(0, forcing)
    passed.append(rejected('premature singleton forcing', lambda: verify.verify_branch(case)))

    case = copy.deepcopy(bundle['branch-0-1.json'])
    case['records'].insert(0, ['budget', 0])
    passed.append(rejected('unexhausted class budget', lambda: verify.verify_branch(case)))

    missing = bundle.copy()
    del missing['branch-1-3656.json']
    passed.append(rejected('missing covering root', lambda: verify.verify_suite(missing)))

    missing = {name: data for name, data in bundle.items() if not name.startswith('branch-1-')}
    passed.append(rejected('missing endpoint color', lambda: verify.verify_suite(missing)))

    narrower = copy.deepcopy(bundle)
    narrower['branch-0-1.json']['budget'][1] = 1847
    passed.append(rejected('opposite class restricted instead of free', lambda: verify.verify_suite(narrower)))

    wrong = copy.deepcopy(bundle)
    wrong['branch-0-1852.json']['root'] = 1235
    passed.append(rejected('substituted root hypothesis', lambda: verify.verify_suite(wrong)))

    print(json.dumps({'positive_control': True, 'rejected_controls': passed}, sort_keys=True))


if __name__ == '__main__':
    main()
