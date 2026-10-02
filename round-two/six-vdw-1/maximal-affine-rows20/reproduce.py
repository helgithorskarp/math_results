"""Standalone exact regeneration and independent checks, one serial child at a time."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('work', type=Path); a = p.parse_args()
    source = Path(__file__).resolve().parent
    work = a.work.resolve()
    require(not work.exists() or (work.is_dir() and not any(work.iterdir())), 'use an empty output directory')
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((source / 'EXPECTED.json').read_text())
    pins = json.loads((source / 'SOURCE_PINS.json').read_text())
    for name, digest in pins.items():
        require(sha(source / name) == digest, 'changed core source/input ' + name)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    receipts = []
    started = time.monotonic()

    def call(name, script, args, optimized=False):
        command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(source / script)] + list(map(str, args))
        before = time.monotonic()
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        try:
            out, err = child.communicate(timeout=35)
        except subprocess.TimeoutExpired:
            child.kill(); out, err = child.communicate()
            (work / 'INCOMPLETE.json').write_text(json.dumps({'status': 'INCOMPLETE_TIMEOUT', 'stage': name,
                                                             'mathematical_exclusion': False}, indent=2) + '\n')
            raise RuntimeError('incomplete child; no mathematical conclusion')
        require(child.returncode == 0, 'child rejected: ' + name + '\n' + err)
        value = json.loads(out)
        receipts.append({'stage': name, 'seconds': time.monotonic() - before,
                         'stdout_sha256': hashlib.sha256(out.encode()).hexdigest()})
        return value

    catalogue = work / 'catalogue.json'
    call('generate', 'generate.py', [catalogue])
    require(catalogue.read_bytes() == (source / 'catalogue.json').read_bytes(), 'entire regenerated catalogue bytes differ')
    require(sha(catalogue) == expected['catalogue_sha256'], 'frozen catalogue hash differs')
    for label, script in [('catalogue', 'check_catalogue.py'), ('maximal', 'check_maximal.py')]:
        values = [call(label + '-' + mode, script, [catalogue], mode == 'optimized')
                  for mode in ['normal', 'optimized']]
        require(values[0] == values[1] == expected[label], 'complete expected mathematical objects differ: ' + label)
    record = {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'COMPLETE_STANDALONE_LOCAL64_SOURCE_REPLAY',
              'python': sys.version.split()[0], 'catalogue_sha256': sha(catalogue),
              'source_pins_sha256': sha(source / 'SOURCE_PINS.json'),
              'normal_optimized_full_objects_identical': True, 'generated_catalogue_bytes_identical': True,
              'catalogue': expected['catalogue'], 'maximal': expected['maximal'],
              'serial_child_receipts': receipts, 'elapsed_seconds': time.monotonic() - started,
              'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'full_field_or_interval_witness': False,
              'trust': 'Same-author separate exact mechanisms and ordinary affine argument; no external review/formalization.'}
    (work / 'verification.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k not in ['serial_child_receipts', 'catalogue', 'maximal']}, sort_keys=True))
