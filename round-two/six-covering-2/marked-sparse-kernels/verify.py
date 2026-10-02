"""Four serial normal/O checks with20s guards and one numerical thread."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument('--manifest', type=Path)
args = ap.parse_args()
root = Path(__file__).resolve().parent
expected = json.loads((root / 'expected.json').read_text())
environment = dict(os.environ)
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    environment[name] = '1'
records, start = [], time.monotonic()
for engine, flags, controls in [
        ('check.py', [], True), ('audit.py', [], True),
        ('check.py', ['-O'], False), ('audit.py', ['-O'], False)]:
    command = [sys.executable, *flags, '-B', engine, '--expected', 'expected.json']
    if controls:
        command.append('--controls')
    t = time.monotonic()
    result = subprocess.run(command, cwd=root, env=environment,
                            timeout=20, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(engine + ' rejected: ' + result.stderr)
    output = json.loads(result.stdout)
    if output['manifest'] != expected:
        raise ValueError('Entry-level manifests differ')
    if output['semantic_damages_rejected'] != (17 if controls else 0):
        raise ValueError('Semantic rejection count differs')
    records.append({'command': ['python3', *command[1:]],
                    'seconds': time.monotonic()-t,
                    'semantic_damages_rejected': output['semantic_damages_rejected'],
                    'exact_manifest_match': True})
report = {
    'agent':'six-covering-2','role':'researcher','python':platform.python_version(),
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'records':records,'elapsed_seconds':time.monotonic()-start,
    'max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    'certificate_sha256':expected['certificate_sha256'],
    'expected_file_sha256':hashlib.sha256((root/'expected.json').read_bytes()).hexdigest(),
    'all_four_replays_passed':True,'one_numerical_thread':True,'guard_seconds':20,
    'same_author_algorithms':True,'independent_reviewer':False,
}
if args.manifest:
    args.manifest.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,sort_keys=True))
