#!/usr/bin/env python3
"""Ensure both exact audits reject four mathematically damaged certificates."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    baseline = json.loads((HERE/'CERTIFICATE.json').read_text())
    changes = {}
    damaged = copy.deepcopy(baseline)
    damaged['maximal_faces'][1]['reflection'][0][0] = '1/17'
    changes['nonorthogonal_reflection'] = damaged
    damaged = copy.deepcopy(baseline)
    damaged['maximal_faces'].pop()
    changes['missing_maximal_face'] = damaged
    damaged = copy.deepcopy(baseline)
    damaged['strict_cross_edges'].pop()
    changes['missing_strict_pair'] = damaged
    damaged = copy.deepcopy(baseline)
    damaged['contrast_bound'] = '1/2'
    changes['false_sharp_constant'] = damaged
    rejected = []
    with tempfile.TemporaryDirectory(prefix='minimax-faces-controls-') as temporary:
        for name, certificate in changes.items():
            path = Path(temporary)/(name+'.json')
            path.write_text(json.dumps(certificate))
            for checker in ('verify.py', 'independent_check.py'):
                # -O makes rejection independent of Python assert statements.
                result = subprocess.run([sys.executable, '-O', str(HERE/checker),
                                         '--certificate', str(path)],
                                        capture_output=True, text=True, timeout=30)
                if result.returncode == 0 or 'ValueError:' not in result.stderr:
                    raise RuntimeError(f'Wrong rejection behavior: {name}, {checker}')
                rejected.append([name, checker])
    print(json.dumps({'status': 'DAMAGED_CERTIFICATES_REJECTED',
                      'rejections': len(rejected), 'cases': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()
