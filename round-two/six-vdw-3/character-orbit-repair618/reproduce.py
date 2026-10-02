#!/usr/bin/env python3
"""Fresh source-pinned, serial stdlib reconstruction and exact both-mode checks."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path


def need(ok,message):
    if not ok:
        raise ValueError(message)


def main(work):
    started=time.monotonic();root=Path(__file__).resolve().parent
    pins=json.loads((root/'SOURCE_PINS.json').read_text())
    for name,digest in pins['files'].items():
        need(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'Changed source: '+name)
    work.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
             BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    expected=json.loads((root/'expected.json').read_text());checked=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        target=work/('certificate-'+mode+'.json')
        for script,args in [('generate.py',['--output',target]),('check.py',[target])]:
            r=subprocess.run([sys.executable,*flags,str(root/script),*map(str,args)],
                             capture_output=True,text=True,env=env,timeout=20)
            need(r.returncode==0,r.stdout+r.stderr)
            if script=='generate.py':
                need(target.read_bytes()==(root/'certificate.json').read_bytes(),'Changed full certificate bytes')
            else:
                value=json.loads(r.stdout);need(value==expected,'Changed exact check result')
                checked.append(value)
                (work/('check-'+mode+'.json')).write_text(json.dumps(value,indent=2)+'\n')
    need(checked[0]==checked[1],'Normal/O complete results differ')
    result={'agent':'six-vdw-3','role':'researcher','status':'FRESH_COMPLETE_AUTHOR_RECONSTRUCTION',
            'certificate_sha256':expected['certificate_sha256'],'orbit_transcript_sha256':expected['orbit_transcript_sha256'],
            'checkers_completed':2,'damaged_certificates_rejected_per_mode':9,
            'regular_column_edit_lower_bound':15,'numerical_threads':1,'max_CPU_intensive_jobs':1,
            'native_solver_invoked':False,'W_bound_improved':False,
            'seconds':time.monotonic()-started,'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    a=p.parse_args();main(a.work)
