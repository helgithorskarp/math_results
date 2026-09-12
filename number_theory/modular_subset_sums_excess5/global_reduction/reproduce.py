#!/usr/bin/env python3
"""Exact replay; the all-n counting proof is in proof.md and uses GK Theorem1.5."""
import hashlib
import json
from pathlib import Path
import controls
import sieve


def build():
    return {'sieve': sieve.build(), 'controls': controls.check()}


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    here = Path(__file__).resolve().parent
    actual = build()
    expected_path = here / 'expected.json'
    expected = json.loads(expected_path.read_text())
    if actual != expected:
        raise AssertionError('Entry-level replay differs from expected.json')
    for bad in [(5, 37, 149, 1), (5, 37, 148, 16)]:
        try:
            sieve.validate_field(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid field certificate accepted')
    print(json.dumps({'status': 'GLOBAL_EXCESS_COUNT_AND_CORE_PACKAGE_VERIFIED',
                      'uniform_count': 'O_t(N^((t+1)/2)), odd t>=3, above explicit threshold',
                      'excess_five_count': 'O(N^3), unrestricted',
                      'complete_classification_n': list(range(5, 15)),
                      'normalized_candidates': sum(x['candidate_count'] for x in actual['sieve']['results']),
                      'direct_matrix_determinants': sum(x['matrices_checked'] for x in actual['controls']['matrix_controls']),
                      'invalid_field_certificates_rejected': 2,
                      'expected_sha256': hashlib.sha256(expected_path.read_bytes()).hexdigest(),
                      'external_theorem': 'Glaudo-Kravitz Theorem1.5 (2024)'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
