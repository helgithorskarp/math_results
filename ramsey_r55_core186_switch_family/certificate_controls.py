#!/usr/bin/env python3
"""Corruptions of the actual compact physical obstruction and proof."""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from check_certificate import physical_core
from drat import require, verify_proof


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('damaged certificate accepted')


def audit(core, proof):
    database, _ = physical_core(core)
    lines = proof.read_text().splitlines()
    require(lines and lines[-1] == '0', 'final physical proof line')
    with TemporaryDirectory(prefix='core186-proof-controls-') as tmp:
        path = Path(tmp)/'damaged.txt'
        physical = core.read_text().splitlines()
        altered = physical.copy()
        row = altered[1].split()
        row[0] = str(-int(row[0]))
        altered[1] = ' '.join(row)
        path.write_text('\n'.join(altered)+'\n')
        rejected(lambda: physical_core(path))  # well formed, wrong physical spin
        path.write_text('0\n')
        rejected(lambda: verify_proof(database, path))
        path.write_text('\n'.join(lines[:-1])+'\n')
        rejected(lambda: verify_proof(database, path))
        path.write_text('\n'.join(lines)+'\n1 0\n')
        rejected(lambda: verify_proof(database, path))
    return {'status': 'PASS', 'actual_certificate_rejections':
            ['flipped_physical_literal', 'unsupported_empty_clause', 'truncated_final_empty', 'continued_after_empty']}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('core', type=Path)
    p.add_argument('proof', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.core, a.proof)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
