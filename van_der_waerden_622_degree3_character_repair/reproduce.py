"""Run independent certificate checking, arithmetic audits and rejection controls.

One CPU child at a time, one thread, timeout 30 seconds per child. This wrapper
does not turn a timeout or failure into a mathematical exclusion.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def run_child(script, *arguments):
    result = subprocess.run([sys.executable, str(ROOT/script), *map(str, arguments)],
                            capture_output=True, text=True, timeout=30,
                            env={**os.environ, 'OMP_NUM_THREADS': '1',
                                 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
                                 'NUMEXPR_NUM_THREADS': '1'})
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    began = time.monotonic()
    results = {'packings': run_child('check_packings.py'),
               'field': run_child('audit_reduction.py', '--mode', 'field'),
               'shifts': run_child('audit_reduction.py', '--mode', 'shifts')}
    # These controls fail in the first canonical case or at schema coverage,
    # so the control child remains below the same 200000-case budget.
    controls = run_child('reject_controls.py')
    results['controls'] = controls
    results.update({'agent': 'six-vdw-1', 'role': 'researcher',
                    'status': 'PACKING_CERTIFICATE_AND_REDUCTION_AUDITS_PASSED',
                    'seconds': time.monotonic()-began,
                    'threads': 1, 'simultaneous_CPU_children': 1,
                    'child_seconds_cap': 30, 'child_arithmetic_case_cap': 200000,
                    'trust_boundary': 'PROOF.md plus exact standard-library checkers; no peer audit or formalization',
                    'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(ROOT.iterdir()) if p.is_file()},
                    'new_W_bound': None})
    output = args.output_dir / 'result.json'
    if output.exists():
        raise ValueError('Choose a fresh output directory')
    output.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, sort_keys=True))


if __name__ == '__main__':
    main()
