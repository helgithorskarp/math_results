"""New serial journal, unchanged resource/time bounds, stop on first incomplete."""
import json
import os
import resource
import signal
import subprocess
import time
from symbolic6_common import ROOT, pins, write
from eleven_run6_six_operations import operations_check

ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
         BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
JOURNAL=ROOT/'symbolic6-stage-ledger.json'


def stage(label,arguments,seconds):
    operations_check();pins()
    data=json.loads(JOURNAL.read_text()) if JOURNAL.exists() else dict(agent='six-vdw-2',role='researcher',stages=[])
    if any(s['label']==label for s in data['stages']) or any(s['status']!='COMPLETE' for s in data['stages']):
        raise ValueError('prior identical or incomplete symbolic stage; no retry')
    item=dict(label=label,status='RUNNING_INCOMPLETE',wall_limit_seconds=seconds,started=time.time())
    data['stages'].append(item);write(JOURNAL,data)
    stdout=ROOT/('symbolic6-'+label+'.stdout');stderr=ROOT/('symbolic6-'+label+'.stderr')
    began=time.monotonic();child=None
    try:
        with stdout.open('w') as out,stderr.open('w') as err:
            child=subprocess.Popen(list(map(str,arguments)),stdout=out,stderr=err,env=ENV,start_new_session=True)
            while child.poll() is None:
                remaining=seconds-(time.monotonic()-began)
                if remaining<=0:raise subprocess.TimeoutExpired(arguments,seconds)
                try:child.wait(timeout=min(5,remaining))
                except subprocess.TimeoutExpired:operations_check()
        item.update(returncode=child.returncode,status='COMPLETE' if child.returncode==0 else 'FAILED_INCOMPLETE')
        if child.returncode:raise RuntimeError('bounded symbolic child failed: '+label+' '+stderr.read_text()[-900:])
    except BaseException as error:
        if child is not None and child.poll() is None:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=2)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=2)
        item.update(status='TIMEOUT_INCOMPLETE' if isinstance(error,subprocess.TimeoutExpired)
                    else 'FAILED_OR_BARRIER_INCOMPLETE',failure=type(error).__name__)
        raise
    finally:
        item.update(finished=time.time(),seconds=time.monotonic()-began,
                    maxrss_children_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        write(JOURNAL,data)
    print(json.dumps(dict(label=label,status=item['status'],seconds=item['seconds'])),flush=True)
    return stdout.read_text()
