"""Serial, guarded whole-result comparisons and mathematical rejection controls."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time


def run():
    here = Path(__file__).resolve().parent
    seal = json.loads((here/'PRIMARY_SEAL.json').read_text())
    for name, expected in seal['primary_files'].items():
        data = (here/name).read_bytes()
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise ValueError('changed primary seal '+name)
    env = os.environ.copy()
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS']:
        env[name] = '1'
    rows, records = [], {}
    with tempfile.TemporaryDirectory(prefix='eleven-twentieths-review-') as tmp:
        cold = Path(tmp)/'cold'; cold.mkdir()
        for name in seal['primary_files']:
            shutil.copyfile(here/name, cold/name)
        env['TMPDIR'] = tmp
        def child(root, script, optimized, extra=(), rejected=False):
            cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
            # Explicitly add this sealed program's path under isolated Python.
            bootstrap = ('import runpy,sys;from pathlib import Path;'
                         'p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p.parent));'
                         'sys.argv=[str(p)]+sys.argv[2:];runpy.run_path(str(p),run_name="__main__")')
            t = time.monotonic()
            proc = subprocess.run(cmd+['-c', bootstrap, str(root/script), *extra],
                                  env=env, capture_output=True, timeout=45)
            elapsed = time.monotonic()-t
            if rejected:
                if proc.returncode == 0 or b'ValueError:' not in proc.stderr:
                    raise ValueError('mathematical damage not decisively rejected '+repr(extra))
            elif proc.returncode or proc.stderr:
                raise ValueError('positive child failed '+proc.stderr.decode(errors='replace'))
            if not rejected:
                json.loads(proc.stdout)
            rows.append(dict(source='local' if root == here else 'cold', script=script,
                             optimized=optimized, extra=list(extra), rejected=rejected,
                             returncode=proc.returncode, seconds=round(elapsed, 6),
                             bytes=len(proc.stdout), sha256=hashlib.sha256(proc.stdout).hexdigest(),
                             cumulative_peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
            return proc.stdout
        for script in ['check.py', 'literal.py']:
            outputs = [child(root, script, opt) for root in [here, cold] for opt in [False, True]]
            if any(raw != outputs[0] for raw in outputs):
                raise ValueError('entire local/cold/normal/optimized output disagreement '+script)
            records[script] = dict(bytes=len(outputs[0]), sha256=hashlib.sha256(outputs[0]).hexdigest(),
                                   all_four_entire_byte_comparisons=True)
        for opt in [False, True]:
            for damage in ['ceiling', 'reciprocal', 'polar-term', 'missing-leaf',
                           'split-axis', 'origin-integral', 'origin-threshold']:
                child(here, 'check.py', opt, ['--damage', damage], rejected=True)
    return dict(agent='six-reviewer-1', role='independent mathematical reviewer',
                all_five_primary_seals_unchanged=True, records=records, rows=rows,
                positive_children=8, mathematical_rejection_children=14,
                serial=True, native_threads=1, fixed_child_guard_seconds=45,
                total_child_seconds=round(sum(r['seconds'] for r in rows), 6),
                maximum_child_seconds=max(r['seconds'] for r in rows),
                no_timeout_unknown_kill_or_incomplete_inference=True)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
