#!/usr/bin/env python3
"""Reject damaged finite certificates with assertions disabled."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    data = json.loads((HERE/'CERTIFICATE.json').read_text())
    cases = []
    broken = copy.deepcopy(data)
    target = next(c for b in broken['angles']['branches'] for c in b['farkas_coefficients'] if c)
    target[0][1] = '-1'
    cases.append(('negative_farkas_multiplier', broken, ['verify.py']))
    broken = copy.deepcopy(data)
    broken['hemisphere']['hemisphere_vector'] = [1, 1, 1]
    cases.append(('false_hemisphere_witness', broken, ['verify.py']))
    broken = copy.deepcopy(data)
    broken['icosahedron']['faces'].pop()
    cases.append(('missing_icosahedral_triangle', broken, ['verify.py', 'independent_check.py']))
    broken = copy.deepcopy(data)
    broken['icosahedron']['cycle'][0], broken['icosahedron']['cycle'][1] = broken['icosahedron']['cycle'][1], broken['icosahedron']['cycle'][0]
    cases.append(('broken_antipodal_cycle', broken, ['verify.py', 'independent_check.py']))
    rejected = []
    with tempfile.TemporaryDirectory(prefix='cap-certificate-controls-') as directory:
        for name, certificate, checkers in cases:
            path = Path(directory)/(name+'.json')
            path.write_text(json.dumps(certificate))
            for checker in checkers:
                result = subprocess.run([sys.executable, '-O', str(HERE/checker),
                                         '--certificate', str(path)],
                                        capture_output=True, text=True, timeout=30)
                if result.returncode == 0 or 'ValueError:' not in result.stderr:
                    raise RuntimeError(f'Unexpected rejection behavior for {name}, {checker}')
                rejected.append([name, checker])
    print(json.dumps({'status': 'DAMAGED_CAP_CERTIFICATES_REJECTED',
                      'rejections': len(rejected), 'cases': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()
