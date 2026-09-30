#!/usr/bin/env python3
"""Generate every exact fixed-core exclusion tree and check its diagnostics.

Author: six-books-2, role researcher. Traces and the executable stay in scratch.
Run independent_core_extension.py separately for full entrywise checking.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent


def digest(path):
    h = sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def run(directory, timeout):
    directory = Path(directory).resolve()
    if directory == HERE or HERE in directory.parents:
        raise ValueError('use a scratch directory outside the source directory')
    directory.mkdir(parents=True, exist_ok=True)
    executable = directory/'search_core_extension'
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    subprocess.run(['c++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                    str(HERE/'search_core_extension.cpp'), '-o', str(executable)],
                   check=True, env=env, timeout=60)
    expected = json.loads((HERE/'core_extension_expected.json').read_text())
    types = json.loads((HERE/'core_extension_types.json').read_text())['types']
    by_mask = {case['mask']: case for case in expected['cases']}
    if len(by_mask) != 156 or {t['mask'] for t in types} != set(by_mask):
        raise AssertionError('incomplete or duplicate type diagnostics')
    records = 0
    total_bytes = 0
    direct_books = 0
    for t in types:
        mask = t['mask']
        trace = directory/f'{mask}.trace'
        result = subprocess.run([str(executable), str(HERE/'core16.edges'),
                                 str(trace), str(mask)], check=True,
                                capture_output=True, text=True,
                                env=env, timeout=timeout)
        counts = json.loads(result.stdout)
        if counts.get('complete') is not True or counts.get('full_valid') != 0:
            raise AssertionError('the exclusion is not established')
        actual = {'mask': mask, 'counts': counts,
                  'trace_bytes': trace.stat().st_size,
                  'trace_sha256': digest(trace)}
        if actual != by_mask[mask]:
            raise AssertionError(f'case {mask}: compact diagnostics mismatch')
        records += sum(counts.get('records_by_depth', []))
        total_bytes += actual['trace_bytes']
        direct_books += counts['internal_book']
    return {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
            'types': len(types), 'labeled_internal_graphs': 32768,
            'direct_internal_books': direct_books, 'tree_records': records,
            'trace_bytes': total_bytes, 'valid_extensions': 0,
            'peer_degree_or_edge_cuts_used': False,
            'independent_check': 'run independent_core_extension.py'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', default='scratch/books_core_extension')
    parser.add_argument('--case-timeout', type=float, default=600,
                        help='seconds per type; timeout proves nothing')
    args = parser.parse_args()
    print(json.dumps(run(args.scratch, args.case_timeout), indent=2, sort_keys=True))
