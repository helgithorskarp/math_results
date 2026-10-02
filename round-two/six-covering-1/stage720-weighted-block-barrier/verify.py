"""Five sequential certificate checks within the standing resource scope."""
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    start=time.monotonic();env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
    commands=[[sys.executable,str(HERE/'check.py')],[sys.executable,'-O',str(HERE/'check.py')],
              [sys.executable,str(HERE/'audit.py')],[sys.executable,'-O',str(HERE/'audit.py')],
              [sys.executable,str(HERE/'audit.py'),'--sanitizers']]
    results=[]
    for cmd in commands:
        p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=20)
        if p.returncode:raise RuntimeError('certificate replay failed: '+p.stderr)
        results.append(json.loads(p.stdout))
    if results[0]!=results[1]:raise RuntimeError('normal/O Python evidence differs')
    if results[2]!=results[3]:raise RuntimeError('normal/O C++ evidence differs')
    a,b=results[2].copy(),results[4].copy();a.pop('sanitizers');b.pop('sanitizers')
    if a!=b:raise RuntimeError('sanitizer evidence differs')
    print(json.dumps({'status':'ALL_FIVE_REPLAYS_PASSED','replays':len(commands),'seconds':time.monotonic()-start,
                      'max_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      'python':results[0],'cpp':results[2]}))
