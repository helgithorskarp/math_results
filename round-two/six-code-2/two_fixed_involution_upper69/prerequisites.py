"""Offline replay of byte-pinned reviewed prerequisites; upper57 is imported."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def verify_pins(directory=None):
    directory = Path(directory) if directory is not None else HERE/'prerequisites'
    record = json.loads((HERE/'DEPENDENCIES.json').read_text())
    for item in record['runtime_files']:
        raw = (directory/item['path']).read_bytes()
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('changed prerequisite: '+item['path'])
    return len(record['runtime_files'])


def replay(work):
    count = verify_pins()
    work = Path(work).resolve(); work.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        environment[key] = '1'
    python = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    commands = [
        ('universal20', ['constant_weight_upper71_review1/verify.py',
         '--certificate', 'constant_weight_upper71_review1/certificate.json',
         '--baseline', 'constant_weight_upper71_review1/baseline69.txt', '--controls',
         '--expected', 'constant_weight_upper71_review1/expected.json']),
        ('absent_pair', ['constant_weight_absent_pair_review1/audit.py',
         '--check', 'constant_weight_absent_pair_review1/expected.json']),
        ('multiplicity_two', ['constant_weight_pair_two_review2/reproduce.py',
         '--work', str(work/'pair-two-generated')])]
    results = []; started = time.monotonic()
    for name, command in commands:
        run = subprocess.run(python+command, cwd=HERE/'prerequisites', env=environment,
                             capture_output=True, text=True, timeout=60)
        (work/(name+'.stdout')).write_text(run.stdout)
        (work/(name+'.stderr')).write_text(run.stderr)
        if run.returncode != 0:
            raise RuntimeError('INCOMPLETE prerequisite replay: '+name)
        results.append({'name': name, 'complete': True})
        print('dependency COMPLETE '+name, flush=True)
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_PUBLIC_PREREQUISITE_REPLAY',
              'replays': results, 'runtime_files': count,
              'transitive_upper57_census_rerun': False,
              'seconds': time.monotonic()-started,
              'scope': 'Universal pointcap20/absent-pair56/pair-two60 pinned validators; upper57 complete census remains an explicitly imported reviewed premise, not rerun.'}
    (work/'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    print(json.dumps(replay(parser.parse_args().work), sort_keys=True))
