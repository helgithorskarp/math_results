#!/usr/bin/env python3
"""Optional comparison of independently regenerated data to public target files."""
import argparse
import json
from pathlib import Path
import audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--author', type=Path, required=True)
    args = ap.parse_args()
    own = json.loads(Path(__file__).with_name('expected.json').read_text())
    certificate = json.loads((args.author/'POSITIVITY_CERTIFICATE.json').read_text())
    target = json.loads((args.author/'RESULTS.json').read_text())
    for name, v in own['symbolic']['positive_margins'].items():
        q = certificate['margins'][name]
        audit.need(audit.mul(audit.poly(v['numerator_ascending']), audit.poly(q['denominator_ascending']))
                   == audit.mul(audit.poly(q['numerator_ascending']), audit.poly(v['denominator_ascending'])),
                   'coefficient identity mismatch: '+name)
    for v in own['finite']:
        if v['n'] > 8:
            continue
        q = next(x for x in target['finite_validation'] if x['n'] == v['n'])
        audit.need(v['centered_core_sha256'] == q['centered_core_sha256'], 'centered core mismatch')
        audit.need(v['parameters'][0]['full_L_sha256'] == q['repaired_full_L_sha256'], 'repaired full matrix mismatch')
    audit.need(own['boundary_four']['full_L_sha256'] == target['boundary_four']['full_L_sha256'],
               'four-point matrix mismatch')
    audit.need(own['separate_five']['gap_one_margins'] == list(target['finite_validation'][0]['gap_one_margins'][k]
               for k in ['C0_gap1', 'U0_gap1', 'C1_shift_trace', 'C1_shift_det',
                         'U1_shift_trace', 'U1_shift_det', 'C2_shift_diag', 'C2_shift_det',
                         'U2_shift_diag', 'U2_shift_det']), 'five-point margins mismatch')
    print('All 12 coefficient identities, 9 matrix hashes and 10 five-point margins match the public target')


if __name__ == '__main__':
    main()
