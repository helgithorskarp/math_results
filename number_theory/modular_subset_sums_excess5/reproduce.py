#!/usr/bin/env python3
"""Replay exact controls and compare every entry to compact expected evidence."""
import copy
import hashlib
import json
from pathlib import Path
import generate
import verify


def main():
    here = Path(__file__).resolve().parent
    expected_path = here / 'expected.json'
    expected = json.loads(expected_path.read_text())
    actual = json.loads(json.dumps(generate.build()))
    if actual != expected:
        raise AssertionError('Entry-level generated evidence differs from expected.json')
    forms = json.loads((here / 'normal_forms.json').read_text())
    independent = verify.check(actual, forms)

    # A deliberately false unit identity must be rejected by the semantic checker.
    bad = copy.deepcopy(forms)
    bad['rows'][2]['multiplier'] = 3
    try:
        verify.check(actual, bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Corrupted normal-form certificate was accepted')

    print(json.dumps({'status': 'EXCESS_FIVE_CHAIN_PACKAGE_VERIFIED',
                      'normal_forms': len(forms['rows']),
                      'uniform_claim_basis': 'proof.md',
                      'expected_sha256': hashlib.sha256(expected_path.read_bytes()).hexdigest(),
                      'finite_control_n': [5, 6, 7, 8, 9, 10],
                      'complete_census_projective_counts': [54, 66],
                      'complete_census_subset_counts': [1728, 4224],
                      'independent': independent,
                      'corrupted_certificate_rejected': True},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
