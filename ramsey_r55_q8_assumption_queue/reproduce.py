"""Solver-free replay in a fresh output directory, with optional sanitizers."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import urllib.request

import basis
import task_queue


def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items() if k not in ['seconds', 'generation_seconds', 'preparation_seconds', 'note']}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value


def main():
    p = argparse.ArgumentParser()
    p.add_argument('catalog_directory'); p.add_argument('fresh_output')
    p.add_argument('--download', action='store_true'); p.add_argument('--sanitizers', action='store_true')
    a = p.parse_args()
    start = time.monotonic()
    out = Path(a.fresh_output); out.mkdir(parents=True, exist_ok=False)
    cache = Path(a.catalog_directory); catalog = cache/task_queue.specs()['name']
    if a.download and not catalog.exists():
        cache.mkdir(parents=True, exist_ok=True)
        s = task_queue.specs()
        wire = urllib.request.urlopen(s['url'], timeout=60).read()
        if hashlib.sha256(wire).hexdigest() != s['download_sha256']:
            raise ValueError('Downloaded catalog identity')
        catalog.write_bytes(gzip.decompress(wire))
    expected = json.loads((basis.HERE/'EXPECTED.json').read_text())
    flags = ['-O'] if sys.flags.optimize else []
    py = [sys.executable]+flags+['-B']
    def run(args):
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError('Command failed: '+repr(args)+'\n'+result.stdout+'\n'+result.stderr)
        return result.stdout
    def execute(name, args):
        t = time.monotonic(); result = json.loads(run(args))
        (out/name).write_text(json.dumps(result, indent=2)+'\n')
        print(name, 'verified in', round(time.monotonic()-t, 3), 'seconds', flush=True)
        return result
    compiler = ['g++', '-std=c++17', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
    run(compiler+['-O2', str(basis.HERE/'audit.cpp'), '-o', str(out/'audit')])
    bases, audits = {}, {}
    for r in range(5, 9):
        meta = basis.write(r, out/f'q8-r{r}.cnf')
        if stable(meta) != expected['bases'][str(r)]:
            raise ValueError('Base changed')
        bases[str(r)] = meta
        audits[str(r)] = json.loads(run([str(out/'audit'), 'base', str(r), str(out/f'q8-r{r}.cnf')]))
        print('Complete base', r, 'generated and audited', flush=True)
    (out/'BASES.json').write_text(json.dumps(bases, indent=2)+'\n')
    (out/'BASE_AUDIT.json').write_text(json.dumps(audits, indent=2)+'\n')
    queue = task_queue.prepare(catalog, out)
    if stable(queue) != expected['queue']:
        raise ValueError('Entire queue changed')
    (out/'QUEUE.json').write_text(json.dumps(queue, indent=2)+'\n')
    execute('QUEUE_AUDIT.json', [str(out/'audit'), 'queue', str(catalog), str(out/'cores.u64le'), str(out/'queue.records')])
    c = execute('COHORTS.json', py+[str(basis.HERE/'cohorts.py'), str(out)])
    if stable(c) != expected['cohorts']:
        raise ValueError('Entire cohort partition changed')
    execute('PROJECTION.json', py+[str(basis.HERE/'projection_check.py'), str(cache), str(out)])
    execute('CONTROLS.json', py+[str(basis.HERE/'controls.py'), '--directory', str(out)])
    execute('INTEGRATION.json', py+[str(basis.HERE/'integration_check.py'), str(out)])
    execute('COHORT_JOB.json', py+[str(basis.HERE/'cohorts.py'), str(out), '--r', '5', '--leaf', '0'])
    if a.sanitizers:
        run(compiler+['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', str(basis.HERE/'audit.cpp'), '-o', str(out/'audit-san')])
        for r in range(5, 9):
            execute(f'SAN_BASE_{r}.json', [str(out/'audit-san'), 'base', str(r), str(out/f'q8-r{r}.cnf')])
        execute('SAN_QUEUE.json', [str(out/'audit-san'), 'queue', str(catalog), str(out/'cores.u64le'), str(out/'queue.records')])
    summary = dict(status='VERIFIED_MECHANISM', python=platform.python_version(), optimize=sys.flags.optimize,
                   compiler=run(['g++', '--version']).splitlines()[0], elapsed_seconds=time.monotonic()-start,
                   sanitizers=a.sanitizers, target_solver_calls=0, original_q8_tasks=2185424,
                   pending_cohort_jobs=expected['cohorts']['pending_cohort_jobs'],
                   certified_task_exclusions=0, physical_candidates=0,
                   reviewer_status='Author checks only; independent review pending')
    (out/'REPLAY.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
