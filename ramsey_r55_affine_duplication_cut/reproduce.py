#!/usr/bin/env python3
"""Regenerate every physical proof in a fresh directory, then verify them all."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import time
import geometry
import project
import runtime
import verify


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2*1024**3, 2*1024**3))


def reproduce(args):
    for line in (runtime.SOURCE/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ')
        if runtime.sha(runtime.SOURCE/name) != digest:
            raise ValueError('source manifest '+name)
    cadical = runtime.check_tool(args.cadical, 'cadical')
    checker = runtime.check_tool(args.drat_trim, 'drat-trim')
    work = runtime.external(args.work)
    work.mkdir(parents=True, exist_ok=False)
    t = time.monotonic()
    for i, entry in enumerate(geometry.orbits()[0]):
        for c in (0, 1):
            name = f'o{i:02d}c{c}'
            p = work/'runs'/name
            p.mkdir(parents=True)
            body, report = project.build(entry['representative'], c)
            (p/'input.cnf').write_text(body)
            command = [str(cadical),'--seed=0','-c','500000','-t','600',
                       str(p/'input.cnf'),str(p/'proof.drat')]
            with (p/'solver.log').open('w') as log:
                r = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                   preexec_fn=limits, timeout=620)
            (p/'production.json').write_text(json.dumps({'command':command,'formula':report,
                                                       'exit_code':r.returncode},indent=2)+'\n')
            if r.returncode != 20:
                raise RuntimeError('branch not UNSAT; global gate remains open: '+name)
            print(name+' SOLVER_UNSAT_PENDING_PROOF_CHECK', flush=True)
    result = verify.verify_all(work, checker)
    result['replay_seconds'] = time.monotonic()-t
    result['child_peak_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    (work/'reproduction.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('work')
    p.add_argument('--cadical', required=True)
    p.add_argument('--drat-trim', required=True)
    reproduce(p.parse_args())
