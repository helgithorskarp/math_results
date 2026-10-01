"""Regenerate both omitted traces and independently check their reductions."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repository-root', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    a = p.parse_args()
    output = a.output_dir.resolve()
    if output.exists():
        raise RuntimeError('Output directory already exists')
    output.mkdir(parents=True)
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    if importlib.metadata.version('python-sat') != '1.8.dev24':
        raise RuntimeError('Pinned python-sat 1.8.dev24 required')
    upstream = a.repository_root.resolve()
    for relative, expected in manifest['source_sha256'].items():
        if digest(upstream / relative) != expected:
            raise RuntimeError('Upstream input changed: ' + relative)
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', TMPDIR=str(output))
    began = time.monotonic()
    stages = []

    def stage(name, command):
        started = time.monotonic()
        process = subprocess.Popen(command, env=env, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            (output / 'incomplete.json').write_text(json.dumps(
                {'status': 'TIMEOUT_NO_VERDICT', 'stage': name, 'completed': stages}, indent=2))
            raise RuntimeError('30-second child guard: ' + name)
        if process.returncode != 0:
            (output / 'incomplete.json').write_text(json.dumps(
                {'status': 'FAILED_NO_VERDICT', 'stage': name, 'completed': stages}, indent=2))
            raise RuntimeError(name + ': ' + stderr[-2000:] + stdout[-1000:])
        elapsed = time.monotonic() - started
        stages.append({'stage': name, 'seconds': elapsed})
        print(name + ': completed', flush=True)
        return stdout

    tool = output / 'drat-trim'
    three = upstream / 'van_der_waerden_27_three_interval_inversions'
    stage('compile-untrusted-transformer', ['cc', '-O2', str(three / 'drat-trim.c'), '-o', str(tool)])
    results = {}
    for runs, relative in [(2, 'van_der_waerden_27_two_interval_inversions'),
                           (3, 'van_der_waerden_27_three_interval_inversions')]:
        source = upstream / relative
        model = output / f'model-{runs}'
        proof = output / f'proof-{runs}.lrat'
        stage(f'build-{runs}', [sys.executable, str(source / 'build_instance.py'),
                               '--output-dir', str(model)])
        stage(f'proposal-{runs}', [sys.executable, str(source / 'solve.py'), '--model-dir', str(model)])
        proposal = json.loads((model / 'solver.json').read_text())
        if not proposal['status'].startswith('UNSAT_UNCHECKED_PROOF'):
            raise RuntimeError('No proof proposal; no verdict')
        transformed = stage(f'transform-{runs}', [str(tool), str(model / 'instance.cnf'),
                                                str(model / 'unchecked-proof.drat'), '-L', str(proof), '-t', '20'])
        if 's VERIFIED' not in transformed or '0 RAT lemmas in core' not in transformed:
            raise RuntimeError('No positive-hint proposal; no verdict')
        checks = []
        for mode in [0, 1]:
            result = output / f'check-{runs}-mode-{mode}.json'
            stage(f'independent-check-{runs}-mode-{mode}', [sys.executable] + (['-O'] if mode else []) +
                  [str(HERE / 'audit.py'), '--source', str(source), '--CNF', str(model / 'instance.cnf'),
                   '--LRAT', str(proof), '--runs', str(runs), '--output', str(result)])
            check = json.loads(result.read_text())
            expected = manifest['expected'][str(runs)]
            for key, value in expected.items():
                if check['proof'][key] != value:
                    raise RuntimeError('Unexpected proof result: ' + key)
            checks.append(check)
        results[str(runs)] = checks
    controls = []
    for mode in [0, 1]:
        controls.append(json.loads(stage(f'controls-mode-{mode}', [sys.executable] +
                      (['-O'] if mode else []) + [str(HERE / 'controls.py'),
                       '--source', str(three), '--CNF', str(output / 'model-3' / 'instance.cnf')])))
    report = {'status': 'BOTH_RUN_BARRIERS_INDEPENDENTLY_CHECKED',
              'agent': 'six-reviewer-5', 'role': 'independent reviewer',
              'method': 'Definition-level exact clause multisets and signed-set RUP checking',
              'python': sys.version.split()[0], 'python_sat': '1.8.dev24',
              'threads': 1, 'simultaneous_CPU_jobs': 1,
              'checks': results, 'controls': controls, 'stages': stages,
              'seconds': time.monotonic() - began,
              'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'trusted_native_solver_or_transformer_status': False,
              'proof_assistant_formalization': False,
              'new_W_bound': None}
    (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['checks', 'controls', 'stages']}, indent=2))


if __name__ == '__main__':
    main()
