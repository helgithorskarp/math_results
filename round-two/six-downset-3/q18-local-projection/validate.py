"""Bounded serial whole-record replays; same-author tool, not a review."""
from pathlib import Path
from time import monotonic
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']


def validate():
    start=monotonic();env=os.environ.copy();env.update({k:'1' for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1'
    spec=importlib.util.spec_from_file_location('sourcecheck',BASE/'sourcecheck.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    closure=gate.check_bundle(BASE);expected=(BASE/'EXPECTED.json').read_bytes()
    certificate=(BASE/'CERTIFICATE.json').read_bytes();runs=[]
    def child(mode,base,out,producer=False):
        budget=min(45,60-(monotonic()-start))
        if budget<=0:raise ValueError('60s serial validation driver guard')
        cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])
        cmd+=[str(base/('produce.py' if producer else 'check.py')),'--out',str(out)]
        t=monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=budget)
        if r.returncode:raise ValueError(mode+' child failed: '+r.stderr.decode()[-2000:])
        if out.read_bytes()!=(certificate if producer else expected):
            raise ValueError(mode+' WHOLE original certificate/record mismatch')
        runs.append({'mode':mode,'seconds':monotonic()-t,
                     'whole_certificate_equal':producer,'whole_expected_record_equal':not producer})
    with tempfile.TemporaryDirectory(prefix='q18-local-projection-') as td:
        root=Path(td);child('normal',BASE,root/'normal.json');child('optimized',BASE,root/'optimized.json')
        cold=root/'cold';cold.mkdir()
        for p in BASE.iterdir():
            if p.is_file():shutil.copyfile(p,cold/p.name)
        child('cold',cold,root/'cold.json');child('cold-producer',cold,root/'produced.json',True)
    return {'actual_agent':'six-downset-3','role':'researcher','source_closure':closure,
            'positive_serial_children':runs,'expected_bytes':len(expected),
            'expected_SHA256':hashlib.sha256(expected).hexdigest(),
            'certificate_bytes':len(certificate),'certificate_SHA256':hashlib.sha256(certificate).hexdigest(),
            'whole_records_and_cold_certificate_equal':True,'elapsed_seconds':monotonic()-start,
            'native_threads':1,'per_child_guard_seconds':45,'driver_guard_seconds':60,
            'independent_review_claimed':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.parent.mkdir(parents=True,exist_ok=True);result=validate()
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
