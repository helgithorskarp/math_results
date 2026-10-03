"""Whole compact-source proof/control replay, serial normal and optimized modes."""
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


def need(ok, message):
    if not ok:
        raise ValueError(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'fresh completed replay output only')
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'MANIFEST.json').read_bytes())
    for name, pin in manifest['files'].items():
        need(Path(name).name == name, 'local compact source file pin')
        raw = (here/name).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'changed whole compact source/evidence file:'+name)
    expected = json.loads((here/'EXPECTED.json').read_bytes())['whole_mathematical_records']
    scripts = ['check_kernel.py', 'check_rows.py', 'check_seed.py',
               'controls_kernel.py', 'controls_rup.py', 'controls_rows.py']
    need(set(expected) == set(scripts), 'entire expected source proof/control domain')
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        env[name] = '1'
    started = time.monotonic()
    receipts, records = [], {}
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        for script in scripts:
            command = [sys.executable]+flags+[str(here/script)]
            stage_start = time.monotonic()
            child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, env=env, start_new_session=True)
            try:
                stdout, stderr = child.communicate(timeout=35)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                stdout, stderr = child.communicate()
                raise RuntimeError('incomplete fixed35s proof/control child:'+script+':'+mode)
            need(child.returncode == 0 and stderr == '', 'failed full proof/control child:'+script+':'+mode)
            record = json.loads(stdout)
            need(record == expected[script], 'entire actual mathematical record differs:'+script+':'+mode)
            need(mode != 'optimized' or record == records[script], 'whole normal/O mathematical equality:'+script)
            records[script] = record
            receipts.append({'mode': mode, 'script': script,
                             'seconds': time.monotonic()-stage_start,
                             'whole_output_sha256': hashlib.sha256(stdout.encode()).hexdigest()})
    mathematical = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'EXACT_FIXED_PHASE617_PROJECTION632_AND_MAXIMUM3703_REPRODUCED',
              'serial_children': len(receipts), 'whole_normal_O_pairs': len(scripts),
              'semantic_damage_rejections_per_mode': 10+9+9+2,
              'all_whole_mathematical_records_sha256': hashlib.sha256(mathematical).hexdigest(),
              'source_manifest_sha256': hashlib.sha256((here/'MANIFEST.json').read_bytes()).hexdigest(),
              'elapsed_seconds': time.monotonic()-started,
              'maximum_child_seconds': max(r['seconds'] for r in receipts),
              'peak_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'fixed_child_guard_seconds': 35, 'numerical_threads': 1,
              'receipts': receipts, 'whole_mathematical_records': records,
              'new_unrestricted_W_bound': False, 'valid3704_coloring': False,
              'external_review_claimed': False}
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['whole_mathematical_records', 'receipts']},
                     sort_keys=True))
