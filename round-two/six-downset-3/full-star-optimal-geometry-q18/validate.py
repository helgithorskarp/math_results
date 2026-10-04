"""Whole source checked before serial normal/optimized/cold geometry replay."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
import sourcecheck


def run():
    seal=sourcecheck.check_bundle(BASE);env=os.environ.copy();receipts=[];start=time.monotonic()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    expected=(BASE/'EXPECTED.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='q18-geometry-source-replay-') as td:
        td=Path(td);cold=td/'cold';cold.mkdir()
        for name in sorted(sourcecheck.REQUIRED|{'BUNDLE.json','SHA256SUMS'}):
            shutil.copyfile(BASE/name,cold/name)
        for mode,root,opt in (('normal',BASE,False),('optimized',BASE,True),('cold',cold,False)):
            out=td/(mode+'.json');cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])
            cmd += [str(root/'check.py'),'--out',str(out)]
            t=time.monotonic();r=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=45)
            if r.returncode or not out.exists() or out.read_bytes()!=expected:
                raise ValueError('whole mathematical geometry replay failed: '+mode+' '+r.stderr)
            receipts.append(dict(mode=mode,exit_code=0,whole_expected_record_equal=True,seconds=time.monotonic()-t))
    return dict(actual_agent='six-downset-3',role='researcher',**seal,
        complete_record_bytes=len(expected),complete_record_SHA256=hashlib.sha256(expected).hexdigest(),
        geometry_SHA256=hashlib.sha256((BASE/'GEOMETRY.json').read_bytes()).hexdigest(),positive_receipts=receipts,
        PSD_mathematical_dependency_not_rechecked_here=True,native_threads=1,serial_children=1,
        child_guard_seconds=45,timeout_or_incomplete_is_not_mathematical_evidence=True,
        seconds=time.monotonic()-start,peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run()
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='positive_receipts'},sort_keys=True))
    print('normal/optimized/cold whole geometry records equal')


if __name__=='__main__':main()
