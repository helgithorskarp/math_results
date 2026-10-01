"""Cold full reproduction, one CPU job at a time; bulky data stays local.

Resume accepts only local complete source/executable-bound orientations.
Neither a missing orientation nor a guard failure becomes a zero case.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from bindings import HERE, v
from collect_fast import load
from controls_full import run as controls
from fast_run import run_case
from residual_fast import collect, run
from verify_full import check


def reproduce(work, resume=False):
    begun = time.monotonic()
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
        os.environ[name] = '1'
    dependencies = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    for item in dependencies['imported_sources']:
        path = (HERE / item['path']).resolve()
        v.check(hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'],
                'public prerequisite changed: ' + item['path'])
    work.mkdir(parents=True, exist_ok=True)
    executables = [work / 'fast-0', work / 'fast-1']
    for engine, executable in enumerate(executables):
        command = ['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion',
                   '-Wshadow', f'-DFAST_ENGINE={engine}', str(HERE / 'fast_census.cpp'),
                   '-lcrypto', '-o', str(executable)]
        subprocess.run(command, check=True)
        result = subprocess.run([str(executable.resolve()), '--controls'], check=True,
                                capture_output=True, text=True, timeout=60)
        print(result.stdout, end='', flush=True)
    census_work, color_work = work / 'census', work / 'residual'
    for case in range(46):
        for orientation in (0, 1):
            run_case(case, orientation, census_work, executables, resume=resume)
    cores, manifest = load(census_work, executables)
    mathematical = {k: value for k, value in manifest.items() if k != 'binding'}
    expected = json.loads((HERE / 'expected.json').read_text())
    v.compare(mathematical, expected, 'complete cold census expected manifest')
    for first in range(0, len(cores), 100):
        run(census_work, color_work, executables, first, 100)
    result = collect(census_work, color_work, executables)
    residual_expected = json.loads((HERE / 'RESIDUAL_SUMMARY.json').read_text())
    v.compare(result, residual_expected, 'all residual expected capacities/certificate')
    witness = json.loads((HERE / 'witness67.json').read_text())
    print(json.dumps(check(census_work, color_work, expected, residual_expected, witness)), flush=True)
    print(json.dumps(controls(census_work, color_work, executables, witness)), flush=True)
    subprocess.run([sys.executable, '-O', str(HERE / 'verify_full.py'),
                    '--census-work', str(census_work), '--color-work', str(color_work)], check=True)
    subprocess.run([sys.executable, '-O', str(HERE / 'controls_full.py'),
                    '--census-work', str(census_work), '--color-work', str(color_work),
                    '--include-executable', str(executables[0]),
                    '--color-executable', str(executables[1])], check=True)
    print(json.dumps({'status': 'COMPLETE_REPRODUCTION_SHARP67_MIXED19',
                      'orientations': 92, 'cores': 4871, 'maximum_capacity': 23,
                      'upper_bound': 67, 'literal_attainment': 67,
                      'seconds': time.monotonic() - begun}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    reproduce(args.work, args.resume)
