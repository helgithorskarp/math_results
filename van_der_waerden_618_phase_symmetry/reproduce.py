"""Reproduce the finite cut and independent check with one child at a time."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

from check import bridge_controls,controls,replay


def require(ok,message):
    if not ok: raise RuntimeError(message)


def main():
    root=Path(__file__).resolve().parent
    build=root/'build'
    build.mkdir(exist_ok=True)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    start=time.monotonic()
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wconversion','-Wshadow',str(root/'enumerate.cpp'),'-o',str(build/'enumerate')],check=True,env=env,timeout=30)
    def run(path,seconds):
        return subprocess.run([str(build/'enumerate'),str(path),str(seconds)],text=True,capture_output=True,env=env,timeout=35)
    first=run(build/'obstructions.bin',30)
    require(first.returncode==0,first.stderr)
    native=json.loads(first.stdout)
    require(native['status']=='COMPLETE_H17_PHASE_FAMILY_OBSTRUCTIONS','native computation incomplete')
    native.pop('seconds')
    second=run(build/'replay.bin',30)
    require(second.returncode==0,second.stderr)
    raw=(build/'obstructions.bin').read_bytes()
    require(raw==(build/'replay.bin').read_bytes(),'nondeterministic certificate')
    verification=replay(raw)
    verification['bridge_controls']=bridge_controls()
    verification['negative_controls_rejected']=controls(raw)
    partial=run(build/'incomplete.bin',1e-12)
    require(partial.returncode==2 and json.loads(partial.stdout)['status']=='INCOMPLETE','budget exhaustion did not fail closed')
    try: replay((build/'incomplete.bin').read_bytes())
    except ValueError: pass
    else: raise RuntimeError('incomplete certificate accepted')
    actual={'native':native,'independent_verification':verification,'fail_closed_time_control':True,'deterministic_certificate_replay':True}
    expected=json.loads((root/'expected.json').read_text())
    require(actual==expected,'entry-level deterministic summary mismatch')
    print(json.dumps({'status':'VERIFIED','normalized_assignments':native['checked'],
                      'affine_stabilizer_order_divides':12,'phase_stabilizer_order_divides':6,
                      'certificate_sha256':hashlib.sha256(raw).hexdigest(),
                      'seconds':time.monotonic()-start,
                      'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}))


if __name__=='__main__': main()
