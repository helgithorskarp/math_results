"""Bounded serial whole-output replay and independent semantic rejection gates."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
FAULTS = {'inverse':'left inverse', 'bad_degree':'bad degree equations',
          'good_mass':'good mass equation', 'anchor':'proper star kernel',
          'missing_column':'all independent columns', 'empty_lift':'complete actual lift'}


def source_gate(root):
    seal = json.loads((root/'PRIMARY_SEAL.json').read_text())
    for name, digest in seal['files'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError('primary source integrity: '+name)


def run(root, optimized=False, fault=None):
    source_gate(root)
    env = dict(os.environ)
    env.update({v:'1' for v in THREADS})
    cmd = [sys.executable,'-I','-B'] + (['-O'] if optimized else [])
    cmd += [str(root/'check.py')] + (['--damage',fault] if fault else [])
    start = time.monotonic()
    p = subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=45)
    elapsed = time.monotonic()-start
    if fault:
        if p.returncode == 0 or p.stdout or ('ValueError: '+FAULTS[fault]).encode() not in p.stderr:
            raise ValueError('unpaid designated rejection: '+fault)
    elif p.returncode or p.stderr:
        raise ValueError('incomplete positive replay: '+p.stderr.decode())
    return p.stdout, {'optimized':optimized,'damage':fault,'seconds':elapsed,
                      'exit_code':p.returncode,'designated_math_rejection':bool(fault)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    positives, controls = [], []
    baseline = None
    with tempfile.TemporaryDirectory(prefix='q18-chart-review-') as td:
        cold = Path(td)
        for p in ROOT.iterdir():
            if p.is_file():
                (cold/p.name).write_bytes(p.read_bytes())
        for root in (ROOT,cold):
            for opt in (False,True):
                data, row = run(root,opt)
                row['cold_copy'] = root == cold
                if baseline is None:
                    baseline = data
                if data != baseline:
                    raise ValueError('whole canonical output mismatch')
                positives.append(row)
        for fault in FAULTS:
            for opt in (False,True):
                _, row = run(ROOT,opt,fault)
                controls.append(row)
    import resource
    report = {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
              'python':sys.version, 'python_executable':sys.executable,
              'canonical_bytes':len(baseline),'canonical_sha256':hashlib.sha256(baseline).hexdigest(),
              'whole_math_record':json.loads(baseline),
              'positives':positives,'semantic_controls':controls,
              'maximum_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'one_serial_child':True,'six_native_threads_one':True,'fixed_child_timeout_seconds':45,
              'ordinary_infinite_bridges_unformalized':True}
    Path(args.out).write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in
                      ('whole_math_record','positives','semantic_controls')},indent=2))


if __name__ == '__main__':
    main()
