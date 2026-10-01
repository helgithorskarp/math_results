"""Cold complete proof reproduction; generated state stays in WORK."""
import json
import os
import resource
import subprocess
import sys
import time
from paths import BASE, WORK


def run():
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    WORK.mkdir(parents=True, exist_ok=True)
    os.environ['CWC2111_PAIR_WORK'] = str(WORK)
    started = time.monotonic()
    record = dict(agent='six-code-3', role='researcher', status='INCOMPLETE', stages=[])
    path = WORK/'proof_run.json'
    path.write_text(json.dumps(record, indent=2)+'\n')
    steps = [
        ('literal automorphisms', [sys.executable,'-B',str(BASE/'automorphisms.py'),'--output',str(WORK/'automorphism_audit.json')]),
        ('shared-tail orbits', [sys.executable,'-B',str(BASE/'tail_carrier.py')]),
        ('actual mapping matrices', [sys.executable,'-B',str(BASE/'mapping.py')]),
        ('native build', ['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(BASE/'pair_fibers.cpp'),'-o',str(WORK/'pair_fibers.exe')]),
        ('both complete mapping censuses', [sys.executable,'-B',str(BASE/'census.py')]),
        ('ordered joint-star orbits', [sys.executable,'-B',str(BASE/'classify_pairs.py')]),
        ('literal coloring certificates', [sys.executable,'-B',str(BASE/'color_bounds.py')]),
    ]
    for name, command in steps:
        subprocess.run(command, cwd=BASE, check=True)
        record['stages'].append(name)
        path.write_text(json.dumps(record, indent=2)+'\n')
    record['status'] = 'COMPLETE mathematical stages; independent certificate verification pending'
    path.write_text(json.dumps(record, indent=2)+'\n')
    subprocess.run([sys.executable,'-B',str(BASE/'verify.py')], cwd=BASE, check=True)
    record.update(status='COMPLETE and all compact certificates verified',
                  seconds=round(time.monotonic()-started, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    path.write_text(json.dumps(record, indent=2)+'\n')
    print(record)
    return record


if __name__ == '__main__':
    run()
