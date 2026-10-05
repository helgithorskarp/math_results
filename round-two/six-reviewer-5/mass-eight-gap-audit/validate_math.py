"""Serial whole-record replay of the NEW face checker; no closed entry replay."""
import hashlib
import json
import os
import pathlib
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
NAMES = ('face.py', 'base.py', 'COVER.json')
ENV = os.environ.copy()
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    ENV[name] = '1'

def seal(directory):
    return {name: hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in NAMES}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    original = seal(HERE)
    records, runs, rejections = [], [], []
    with tempfile.TemporaryDirectory(prefix='r5-new-face-') as temporary:
        cold = pathlib.Path(temporary)
        for name in NAMES:
            shutil.copyfile(HERE/name, cold/name)
        for label, directory in (('local', HERE), ('cold', cold)):
            for optimized in (False, True):
                require(seal(directory) == seal(HERE) == original, 'entire source before replay')
                started = time.monotonic()
                command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(directory/'face.py')]
                completed = subprocess.run(command, env=ENV, capture_output=True, timeout=45, check=True)
                elapsed = time.monotonic()-started
                require(seal(directory) == seal(HERE) == original and not completed.stderr, 'entire source after replay/clean stderr')
                value = json.loads(completed.stdout)
                require(value['status'].startswith('Complete exact original mass-eight face arithmetic'), 'whole record scope')
                require(len(value['all_leaf_attempts']) == 139 and len(value['semantic_controls']) == 6 and len(value['quartic_formal_controls']) == 4, 'whole record census')
                roles = {name: sum(row['role']==name for row in value['all_leaf_attempts']) for name in ('scalar-product-origin','retained-mean-product-origin','standard-polar','joint-energy-polar')}
                require(list(roles.values()) == [79,9,2,49], 'complete four-role census')
                for row in value['all_leaf_attempts']:
                    require(len(row['scalar_origin']['all_seven_remainders'])==7 and all(len(r['full_ten_coefficients'])==10 for r in row['scalar_origin']['all_seven_remainders']), 'all scalar vectors')
                    if row['role']=='joint-energy-polar':
                        require(len(row['joint_polar']['full_thirteen_by_nineteen_matrix'])==13 and all(len(r)==19 for r in row['joint_polar']['full_thirteen_by_nineteen_matrix']) and len(row['joint_polar']['bernstein']['controls'])==13, 'all joint matrices and controls')
                    if row['role']=='retained-mean-product-origin':
                        require([r['family'] for r in row['retained_mean']]==['E','T'], 'both mean families')
                        for r in row['retained_mean']:
                            require(len(r['all_seven_remainder_matrices'])==7 and len(r['nine_controls']['controls'])==9 and len(r['ten_controls']['controls'])==10, 'complete mean controls')
                require(value['refinement']['epsilon']=='1/340' and Fraction(value['refinement']['polar_strict_margin'])>0 and Fraction(value['refinement']['origin_strict_margin'])>0, 'actual stronger gap strict margins')
                records.append(completed.stdout)
                runs.append(dict(directory=label, optimized=optimized, seconds=elapsed, complete_record_bytes=len(completed.stdout), complete_record_sha256=hashlib.sha256(completed.stdout).hexdigest(), roles=roles))
        require(all(raw == records[0] for raw in records), 'ENTIRE local/cold normal/optimized records agree')
        for name, reason in (('base.py','owned pure helper pin BEFORE import'),('COVER.json','defining cover before parse')):
            saved = (cold/name).read_bytes()
            (cold/name).write_bytes(saved+b'\n')
            for optimized in (False, True):
                command = [sys.executable,'-I','-B'] + (['-O'] if optimized else []) + [str(cold/'face.py')]
                completed = subprocess.run(command, env=ENV, capture_output=True, timeout=45)
                require(completed.returncode != 0 and reason.encode() in completed.stderr and not completed.stdout, 'preimport/input rejection')
                rejections.append(dict(name=name, optimized=optimized, reason=reason, exit_code=completed.returncode))
            (cold/name).write_bytes(saved)
        require(seal(cold)==seal(HERE)==original, 'ENTIRE inputs restored')
    (HERE/'RECORD.json').write_bytes(records[0])
    result = dict(status='PASS NEW full face arithmetic and1/340 sufficient refinement', agent='six-reviewer-5', role='independent reviewer', whole_math_record_equal=True, source_pins=original, child_guard_seconds=45, native_threads=1, serial_children=True, shared_and_individual_limits_unchanged=True, maximum_children_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, replays=runs, preimport_rejections=rejections, scope='NEW original139 face inequalities; closed73-shell/old continuity not rerun. Ordinary universal bridges separately written. No source publication or graph verdict claimed by replay.')
    (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
