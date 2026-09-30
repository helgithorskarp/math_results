#!/usr/bin/env python3
"""Reject damaged proof trees even when their diagnostic hashes are updated.

Author: six-books-2, role researcher. Run after generating the full traces.
These are rejection controls, not a substitute for the complete replay.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def run(traces, scratch):
    traces, scratch = Path(traces).resolve(), Path(scratch).resolve()
    if scratch == HERE or HERE in scratch.parents:
        raise ValueError('controls require scratch outside the source directory')
    scratch.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location(
        'fixed_core_checker', HERE/'independent_core_extension.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    original = (traces/'0.trace').read_text().splitlines()
    root = next(i for i, line in enumerate(original) if line.startswith('D '))
    rows = original[:root]
    root_tokens = original[root].split()
    if root_tokens[1] != '0' or int(root_tokens[3]) < 2:
        raise AssertionError('unexpected zero-edge root')
    omitted = root_tokens[:-1]
    omitted[3] = str(int(omitted[3])-1)
    child_tokens = original[root+1].split()
    child_tokens[3] = root_tokens[-1]
    cases = [
        ('missing_row', 0, rows[1:]+original[root:],
         'incomplete/wrong one-row list'),
        ('omitted_candidate', 0, rows+[' '.join(omitted)],
         'incomplete/wrong row domain'),
        ('wrong_context', 0, rows+[original[root], ' '.join(child_tokens)],
         'missing/reordered branch'),
        ('truncated_branch', 0, rows+[original[root]],
         'truncated proof tree'),
    ]
    internal = (traces/'32767.trace').read_text().split()
    if internal[0] != 'I':
        raise AssertionError('expected a direct internal book')
    internal[-1] = internal[-2]
    cases.append(('repeated_internal_page', 32767, [' '.join(internal)],
                  'internal pages not four distinct roles'))
    passed = []
    for name, mask, damaged, reason in cases:
        package = scratch/name
        if package.exists():
            raise ValueError('use fresh control scratch; prior evidence is preserved')
        package.mkdir()
        for filename in ['core16.edges', 'search_core_extension.cpp',
                         'core_extension_types.json', 'core_extension_expected.json']:
            shutil.copyfile(HERE/filename, package/filename)
        types = json.loads((package/'core_extension_types.json').read_text())
        types['types'].sort(key=lambda case: case['mask'] != mask)
        (package/'core_extension_types.json').write_text(json.dumps(types)+'\n')
        data = ('\n'.join(damaged)+'\n').encode()
        (package/f'{mask}.trace').write_bytes(data)
        diagnostics = json.loads((package/'core_extension_expected.json').read_text())
        target = next(c for c in diagnostics['cases'] if c['mask'] == mask)
        target['trace_sha256'] = sha256(data).hexdigest()
        target['trace_bytes'] = len(data)
        (package/'core_extension_expected.json').write_text(json.dumps(diagnostics)+'\n')
        checker.HERE = package
        try:
            checker.compute(package, package/'progress.json', None)
        except AssertionError as error:
            if str(error) != reason:
                raise AssertionError(f'{name}: wrong rejection reason: {error}') from error
            passed.append(name)
        else:
            raise AssertionError(f'{name}: damaged proof accepted')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    executable = traces/'search_core_extension'
    for index, text in enumerate(['32768', '4294967296',
                                  '18446744073709551616', '-1', '+1',
                                  '1junk', '', ' 1']):
        trace = scratch/f'bad-mask-{index}.trace'
        result = subprocess.run([str(executable), str(HERE/'core16.edges'),
                                 str(trace), text], capture_output=True,
                                text=True, env=env, timeout=5)
        if result.returncode == 0 or trace.exists():
            raise AssertionError(f'invalid decimal mask accepted: {text!r}')
    bad_core = scratch/'truncated-core.edges'
    bad_core.write_bytes((HERE/'core16.edges').read_bytes()+b'7\n')
    result = subprocess.run([str(executable), str(bad_core),
                             str(scratch/'bad-core.trace'), '0'],
                            capture_output=True, text=True, env=env, timeout=5)
    if result.returncode == 0:
        raise AssertionError('incomplete fixture edge accepted')
    result = subprocess.run([sys.executable, '-O',
                             str(HERE/'independent_core_extension.py'), str(traces)],
                            capture_output=True, text=True, env=env, timeout=5)
    if result.returncode == 0 or 'assertions enabled' not in result.stderr:
        raise AssertionError('assertions-disabled checker was not rejected')
    return {'agent': 'six-books-2', 'role': 'researcher',
            'semantic_tree_rejections': passed, 'invalid_mask_rejections': 8,
            'incomplete_fixture_rejected': True,
            'assertions_disabled_rejected': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trace_directory')
    parser.add_argument('--scratch', default='scratch/books_core_controls')
    args = parser.parse_args()
    print(json.dumps(run(args.trace_directory, args.scratch), indent=2, sort_keys=True))
