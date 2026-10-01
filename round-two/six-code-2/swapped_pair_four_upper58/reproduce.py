"""Cold offline replay. A failed stage is INCOMPLETE, never nonexistence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--sanitized', action='store_true')
    args = parser.parse_args(); here = Path(__file__).resolve().parent
    work = args.work.resolve()
    if work.exists() and any(work.iterdir()):
        raise ValueError('cold work directory must be empty')
    work.mkdir(parents=True, exist_ok=True)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[key] = '1'
    os.environ['SWAPPED69_WORK'] = str(work)
    from bootstrap import ensure_runtime
    ensure_runtime()
    started = time.monotonic(); stages = []
    def run(script, *argv):
        begin = time.monotonic()
        command = [sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(here/script)]+list(map(str, argv))
        print('RUN '+script, flush=True)
        with (work/(script+'.log')).open('w') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError('INCOMPLETE '+script+'; inspect local log')
        stages.append({'script': script, 'seconds': time.monotonic()-begin})
        print(json.dumps(stages[-1]), flush=True)
    run('run.py', '--work', work/'swapped-m4-full')
    run('replay_groups.py')
    run('quotient4.py', '--inventory', work/'swapped-m4-full', '--output', work/'swapped-m4-roots.json')
    run('complete4.py', '--roots', work/'swapped-m4-roots.json', '--work', work/'swapped-m4-completions')
    run('native4.py', '--roots', work/'swapped-m4-roots.json', '--color', work/'swapped-m4-completions/summary.json',
        '--work', work/'swapped-m4-native', *(['--sanitized'] if args.sanitized else []))
    (work/'swapped-m4-witness58.json').write_bytes((here/'WITNESS58.json').read_bytes())
    run('check_coverage.py')
    from evidence58 import collect, encoded
    record = json.loads(encoded(collect(work)))
    expected = json.loads((here/'EXPECTED.json').read_text())
    if record != expected:
        (work/'ACTUAL.json').write_bytes(encoded(record))
        raise ValueError('replay differs from frozen experimental evidence')
    (work/'RESULT.json').write_bytes(encoded(record))
    validation = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE',
                  'optimized_python': bool(sys.flags.optimize), 'sanitized_native': args.sanitized,
                  'seconds': time.monotonic()-started, 'stages': stages,
                  'expected_sha256': hashlib.sha256((here/'EXPECTED.json').read_bytes()).hexdigest(),
                  'own_peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  'child_peak_RSS_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  'python': sys.version.split()[0]}
    (work/'VALIDATION.json').write_text(json.dumps(validation, indent=2)+'\n')
    print(json.dumps(validation, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
