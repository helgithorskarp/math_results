"""Run four disjoint archived-proof ranges, wait, and checkpoint honestly.

This POSIX orchestration helper does not establish any mathematical fact
on its own. The frozen check_saved.py validates each proof and checkpoint.
Never start overlapping workers in the same output directory manually.
"""
from pathlib import Path
import argparse
import datetime
import fcntl
import hashlib
import json
import subprocess
import sys
import time


def main():
    p=argparse.ArgumentParser()
    for name in ('domain','manifest','corpus','checker','checker-source','out'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=float,default=1200)
    a=p.parse_args()
    if a.seconds<0:p.error('seconds must be nonnegative')
    a.out.mkdir(parents=True,exist_ok=True)
    lock=(a.out/'replay.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    source=Path(__file__).with_name('check_saved.py')
    common=[sys.executable,str(source)]
    for name in ('domain','manifest','corpus','checker','checker-source','out'):
        common.extend(['--'+name,str(getattr(a,name.replace('-','_')).resolve())])
    ranges=[(0,27419),(27419,54838),(54838,82257),(82257,109676)]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    processes=[]
    try:
        for lo,hi in ranges:
            with (a.out/f'worker_{lo}_{hi}.log').open('ab') as log:
                processes.append(subprocess.Popen(common+['--start',str(lo),'--stop',str(hi),
                                  '--seconds',str(a.seconds)],stdout=log,stderr=subprocess.STDOUT))
        print('Four bounded, disjoint proof replays started.',flush=True)
        while True:
            codes=[proc.poll() for proc in processes]
            if any(code is not None and code!=0 for code in codes):
                raise RuntimeError('worker failed; inspect range logs; no acceptance')
            if all(code is not None for code in codes):break
            time.sleep(1)
        manifest=json.loads(a.manifest.read_text())
        completed=sum((a.out/f"block_{b['start']:06d}_{b['stop']:06d}.json").exists()
                      for b in manifest['blocks'])
        complete=completed==len(manifest['blocks'])
        if complete:subprocess.run(common+['--summarize'],check=True)
        result={'status':'COMPLETE_INDEPENDENT_REPLAY_FINISHED' if complete
                        else 'INCOMPLETE_DURABLE_CHECKPOINT',
                'complete_family':complete,'completed_block_files':completed,
                'expected_block_files':len(manifest['blocks']),
                'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'ranges':ranges,'seconds_limit_per_worker':a.seconds,
                'runner_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'dispatcher_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        temp=a.out/'bounded_run.json.tmp';temp.write_text(json.dumps(result,indent=2)+'\n')
        temp.replace(a.out/'bounded_run.json')
        print(json.dumps(result,indent=2),flush=True)
    finally:
        for proc in processes:
            if proc.poll() is None:proc.terminate()
        for proc in processes:
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()


if __name__=='__main__':main()
