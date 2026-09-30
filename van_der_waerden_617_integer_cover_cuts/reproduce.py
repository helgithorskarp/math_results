"""One child at a time, with bounded single-thread numerical rediscovery."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser(); p.add_argument('--rediscover', action='store_true')
    p.add_argument('--builddir', type=Path, default=Path('build'))
    args = p.parse_args(); root = Path(__file__).resolve().parent
    build = args.builddir.resolve(); build.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    begin = time.monotonic(); jobs = []

    def run(script, *arguments):
        r = subprocess.run([sys.executable, str(root/script), *map(str, arguments)],
                           cwd=root, env=env, text=True, capture_output=True, timeout=30)
        if r.returncode:
            raise RuntimeError(r.stderr[-2500:] or r.stdout[-2500:])
        if r.stdout.strip(): jobs.append(json.loads(r.stdout))

    run('check_all.py', '--output', build/'checked.json')
    if args.rediscover:
        run('discover_cover2.py', '--cuts', root/'cuts.json', '--certificate', build/'fresh-cover2.json',
            '--guidance', build/'fresh-cover2-guidance.json')
        run('verify.py', build/'fresh-cover2.json', '--output', build/'fresh-cover2-check.json')
        run('discover_fractional.py', '--work', build/'fractional')
        run('verify_fractional.py', build/'fractional/fractional-witness.json',
            '--output', build/'fresh-fractional-check.json')
    print(json.dumps({'agent':'six-vdw-3', 'role':'researcher', 'sequential_math_jobs':True,
          'threads':1, 'seconds':time.monotonic()-begin,
          'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
          'rediscovery':args.rediscover, 'jobs':jobs}))


if __name__ == '__main__': main()
