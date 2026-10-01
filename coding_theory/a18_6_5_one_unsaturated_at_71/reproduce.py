"""Sequential production, literal verification and controls; no external input."""
from pathlib import Path
import json
import os
import resource
import subprocess
import sys
import time

from common import HERE, WORK, require


def main():
    env=dict(os.environ)
    env.update({k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
    WORK.mkdir(parents=True,exist_ok=True)
    started=time.monotonic();children=[]
    for script,args in (('producer.py',[]),('verify.py',['--compare-primary']),('controls.py',[])):
        result=subprocess.run([sys.executable,'-B',str(HERE/script)]+args,env=env,capture_output=True,text=True)
        if result.returncode:
            print(result.stdout+result.stderr);raise SystemExit(result.returncode)
        report=json.loads(result.stdout);require(report['status']=='COMPLETE','child incomplete')
        children.append({'script':script,'seconds':report['seconds'],'maxrss_kib':report['maxrss_kib']})
    report={'agent':'six-code-3','role':'researcher','status':'COMPLETE','seconds':time.monotonic()-started,
            'python':sys.version,'children':children,'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'child_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (WORK/'proof_run.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
