#!/usr/bin/env python3
"""Reject corruptions of the actual addition-only physical certificate."""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from check_rup import physical, proof


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('bad certificate accepted')


def run(core, certificate):
    database, _ = physical(core)
    lines = certificate.read_text().splitlines()
    names = []
    with TemporaryDirectory(prefix='moving33-rup-controls-') as tmp:
        path = Path(tmp)/'bad.txt'
        altered = core.read_text().splitlines()
        row = altered[1].split()
        row[0] = str(-int(row[0]))
        altered[1] = ' '.join(row)
        path.write_text('\n'.join(altered)+'\n')
        rejected(lambda: physical(path))
        names.append('flipped_physical_literal')
        for name, text in [('unsupported_empty', '0\n'),
                           ('missing_final_empty', '\n'.join(lines[:-1])+'\n'),
                           ('continued_after_empty', '\n'.join(lines)+'\n1 0\n'),
                           ('deletion_not_allowed', 'd 1 0\n'+ '\n'.join(lines)+'\n')]:
            path.write_text(text)
            rejected(lambda: proof(database, path))
            names.append(name)
    return {'status': 'PASS', 'actual_RUP_certificate_rejections': names}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('core', type=Path)
    p.add_argument('certificate', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run(a.core, a.certificate)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
