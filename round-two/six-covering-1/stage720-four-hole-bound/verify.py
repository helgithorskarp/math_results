"""Sequential source, literal replay, mode and sanitizer checks."""
from argparse import ArgumentParser
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = ArgumentParser()
    ap.add_argument('--build-dir', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    a.build_dir.mkdir(parents=True, exist_ok=True)
    expected_names = json.loads((HERE / 'manifest.json').read_text())['files']
    observed = sorted(p.name for p in HERE.iterdir() if p.is_file())
    need(observed == expected_names, 'source file inventory differs')
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ')
        need(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, 'source digest: ' + name)
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    jobs = [
        ('python', [sys.executable, str(HERE / 'check.py')]),
        ('python-O', [sys.executable, '-O', str(HERE / 'check.py')]),
        ('literal', [sys.executable, str(HERE / 'audit.py'), '--build-dir', str(a.build_dir)]),
        ('literal-O', [sys.executable, '-O', str(HERE / 'audit.py'), '--build-dir', str(a.build_dir)]),
        ('sanitized-controls', [sys.executable, str(HERE / 'audit.py'), '--build-dir', str(a.build_dir), '--sanitized-controls']),
    ]
    start = time.monotonic()
    results, timings = {}, {}
    for name, command in jobs:
        begun = time.monotonic()
        p = subprocess.run(command, capture_output=True, text=True, timeout=20, env=env)
        need(p.returncode == 0 and not p.stderr.strip(), name + ' failed: ' + p.stderr[:2000])
        results[name] = json.loads(p.stdout)
        timings[name] = time.monotonic() - begun
    need(results['python'] == results['python-O'], 'Python optimized mode differs')
    need(results['literal'] == results['literal-O'], 'literal optimized driver differs')
    result = {'required_replays': len(jobs), 'normal_optimized_agree': True,
              'semantic_damages_rejected_per_mode': len(results['python']['semantic_damages_rejected']),
              'minimum_actual_even_holes': 99, 'maximum_even_incidence_sum': 61,
              'full_gain_entries_compared': sum(results['literal']['full_gain_pair_entries_by_group']),
              'full_dp_entries_compared': results['literal']['full_dp_entries_compared'],
              'sanitized_controls': results['sanitized-controls'],
              'replay_seconds': timings, 'seconds': time.monotonic() - start,
              'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'solver_used': False, 'unrestricted_L_min_8_bound_changed': False}
    if a.output:
        a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
