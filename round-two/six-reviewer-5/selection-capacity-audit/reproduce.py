"""Two serial, guarded cold replays against the whole frozen record."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')


def main():
    expected = (ROOT/'final-record.json').read_bytes(); records = []
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}
    for flag in [[],['-O']]:
        command = [sys.executable]+flag+[str(ROOT/'final_check.py'),'--check',str(ROOT/'final-record.json')]
        start = time.monotonic()
        result = subprocess.run(command,env=ENV,capture_output=True,timeout=45)
        if result.returncode: raise RuntimeError(result.stderr.decode())
        if result.stdout != expected or result.stderr: raise ValueError('whole frozen bytes or empty stderr differ')
        if sources != {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}: raise ValueError('source changed during cold replay')
        records.append({'mode':'optimized' if flag else 'normal','seconds':time.monotonic()-start,
                        'peak_math_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                        'whole_record_sha256':hashlib.sha256(result.stdout).hexdigest(),'whole_bytes_equal':True,
                        'native_threads':1,'timeout_seconds':45})
    print(json.dumps({'agent':'six-reviewer-5','role':'independent mathematical reviewer',
                      'python':sys.version,'serial_cold_replays':records,'mathematical_source_sha256':sources},indent=2))


if __name__ == '__main__': main()
