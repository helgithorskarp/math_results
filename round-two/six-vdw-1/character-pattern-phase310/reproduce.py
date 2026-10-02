"""Pin source, replay exact certificates serially and compare entire records."""
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(sys.version_info >= (3,11), 'CPython3.11+ required')
    source = Path(__file__).resolve().parent
    work = args.work.resolve()
    need(work != source and source not in work.parents, 'work must be outside source')
    need(not work.exists(), 'fresh reproduction directory required')
    manifest = json.loads((source / 'SOURCE_MANIFEST.json').read_text())
    need(manifest['schema'] == 'CHARACTER_PATTERN_PHASE310_SOURCE_V1', 'exact manifest schema')
    entries = manifest['files']
    need({p.name for p in source.iterdir() if p.is_file()} == set(entries) | {'SOURCE_MANIFEST.json'},
         'entire source file inventory')
    for name, pin in entries.items():
        need(Path(name).name == name and not (source / name).is_symlink(), 'literal source filename')
        raw = (source / name).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'source bytes differ: ' + name)
    expected_raw = (source / 'EXPECTED.json').read_bytes()
    expected = json.loads(expected_raw)
    need(expected['schema'] == 'CHARACTER_PATTERN_PHASE310_EXPECTED_V1', 'entire record schema')
    need(set(expected['records']) == {'kernel','transports','controls'}, 'all three expected checks')
    work.mkdir(parents=True)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    observed = {}
    receipts = []
    started = time.monotonic()
    for mode in ['normal','optimized']:
        interpreter = [sys.executable,'-B'] + (['-O'] if mode == 'optimized' else [])
        stages = [
            ('kernel', ['check_kernel.py', str(source / 'AP_KERNEL.json'), str(source / 'kernel.lrat'),
                        '--cnf-out', str(work / (mode + '.cnf'))]),
            ('transports', ['check_transports.py']),
            ('controls', ['controls.py','--source',str(source)])]
        for name, tail in stages:
            command = interpreter + [str(source / tail[0])] + tail[1:]
            before = time.monotonic()
            child = subprocess.Popen(command, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
            timeout = False
            try:
                stdout, stderr = child.communicate(timeout=35)
            except subprocess.TimeoutExpired:
                timeout = True
                os.killpg(child.pid, signal.SIGKILL)
                stdout, stderr = child.communicate()
            label = mode + '.' + name
            (work / (label + '.stdout')).write_bytes(stdout)
            (work / (label + '.stderr')).write_bytes(stderr)
            receipt = {'stage':label, 'returncode':child.returncode, 'timeout':timeout,
                       'guard_seconds':35, 'elapsed_seconds':time.monotonic()-before,
                       'peak_children_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                       'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
                       'stderr_sha256':hashlib.sha256(stderr).hexdigest()}
            receipts.append(receipt)
            (work / 'receipts.json').write_text(json.dumps(receipts,indent=2,sort_keys=True)+'\n')
            need(not timeout and child.returncode == 0 and stderr == b'', 'incomplete or failed stage: ' + label)
            record = json.loads(stdout)
            need(record == expected['records'][name], 'ENTIRE mathematical record differs: ' + label)
            if mode == 'normal':
                observed[name] = stdout
            else:
                need(stdout == observed[name], 'WHOLE normal/optimized output bytes differ: ' + name)
        cnf = (work / (mode + '.cnf')).read_bytes()
        need(hashlib.sha256(cnf).hexdigest() == expected['records']['kernel']['cnf_sha256'],
             'entire reconstructed actual-AP CNF differs')
    need((work / 'normal.cnf').read_bytes() == (work / 'optimized.cnf').read_bytes(), 'all CNF bytes agree')
    result = {'author':'six-vdw-1', 'role':'researcher',
              'status':'ORIGINAL_AP_RUP_TRANSPORTS_AND_CONTROLS_PASSED',
              'entire_expected_sha256':hashlib.sha256(expected_raw).hexdigest(),
              'records':expected['records'], 'normal_optimized_all_bytes_equal':True,
              'source_files_checked':len(entries)+1, 'serial_children':len(receipts),
              'child_guard_seconds':35, 'elapsed_seconds':time.monotonic()-started,
              'peak_children_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'external_review':False, 'formalized':False}
    (work / 'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
