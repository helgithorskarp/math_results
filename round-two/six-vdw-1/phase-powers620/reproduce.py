"""Pinned source, fresh catalogue, and five bounded sequential child checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    work = args.work.resolve()
    require(not work.exists() or (work.is_dir() and not any(work.iterdir())), 'use an empty output directory')
    work.mkdir(parents=True, exist_ok=True)
    pins = json.loads((source / 'SOURCE_PINS.json').read_text())
    names = {'.gitignore', 'README.md', 'PROOF.md', 'VALIDATION.md', 'EXPECTED.json',
             'catalogue.csv', 'generate.py', 'check.py', 'controls.py', 'reproduce.py'}
    require(type(pins) is dict and set(pins) == names, 'complete intended source pin set')
    for name, digest in pins.items():
        require(sha(source / name) == digest, 'changed source/input ' + name)
    expected = json.loads((source / 'EXPECTED.json').read_text())
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    started = time.monotonic()
    receipts = []

    def call(label, script, arguments, optimized=False):
        command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(source / script)] + list(map(str, arguments))
        before = time.monotonic()
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                 start_new_session=True, env=env, cwd=work)
        try:
            out, err = child.communicate(timeout=35)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            out, err = child.communicate()
            (work / 'INCOMPLETE.json').write_text(json.dumps({'status': 'INCOMPLETE_TIMEOUT', 'stage': label,
                                                             'mathematical_exclusion': False}, indent=2) + '\n')
            raise RuntimeError('incomplete child; no mathematical conclusion')
        require(child.returncode == 0, 'child rejected: ' + label + '\n' + err)
        value = json.loads(out)
        receipts.append({'stage': label, 'seconds': time.monotonic() - before,
                         'stdout_sha256': hashlib.sha256(out.encode()).hexdigest()})
        return value

    catalogue = work / 'catalogue.csv'
    generated = call('generate', 'generate.py', [catalogue])
    require(generated == expected['generate'], 'whole generator result differs')
    require(catalogue.read_bytes() == (source / 'catalogue.csv').read_bytes(), 'whole regenerated catalogue bytes differ')
    require(sha(catalogue) == expected['catalogue_sha256'], 'catalogue digest differs')
    for name in ['check', 'controls']:
        normal = call(name + '-normal', name + '.py', [catalogue])
        optimized = call(name + '-optimized', name + '.py', [catalogue], True)
        require(normal == optimized == expected[name], 'whole normal/optimized expected objects differ: ' + name)
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'COMPLETE_STANDALONE_CANONICAL_PHASE_POWER_REPLAY',
              'python': sys.version.split()[0], 'catalogue_sha256': sha(catalogue),
              'source_pins_sha256': sha(source / 'SOURCE_PINS.json'),
              'generated_catalogue_bytes_identical': True, 'normal_optimized_full_objects_identical': True,
              'actual_bad_APs': expected['check']['actual_bad_APs'],
              'admissible_parameter_pairs_covered': expected['check']['unquotiented_admissible_base_generator_inputs'],
              'serial_child_receipts': receipts, 'elapsed_seconds': time.monotonic() - started,
              'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'interval_coloring_or_new_W_bound': False,
              'trust': 'Same-author separate exact algorithms and ordinary proofs; no external review/formalization.'}
    (work / 'verification.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'serial_child_receipts'}, sort_keys=True), flush=True)
