"""Serial source-pinned reproduction; four children with fixed 20-second guards."""
import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

FILES={'.gitignore','PROOF.md','README.md','VALIDATION.md','SOURCE_PINS.json',
       'generate.py','check.py','certificate.csv','expected.json','reproduce.py','verification.json'}

def need(condition,message):
    if not condition:raise ValueError(message)

def verify_source(source):
    pins=json.loads((source/'SOURCE_PINS.json').read_text())
    need(pins['schema']==1 and pins['algorithm']=='sha256','source pin format')
    need(set(pins['files'])==FILES-{'SOURCE_PINS.json'},'complete source inventory')
    for name,wanted in pins['files'].items():
        path=source/name
        need(path.is_file() and not path.is_symlink(),'regular pinned file: '+name)
        need(hashlib.sha256(path.read_bytes()).hexdigest()==wanted,'source pin mismatch: '+name)

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    args=p.parse_args();source=Path(__file__).resolve().parent;verify_source(source)
    work=args.work.resolve()
    need(work!=source and source not in work.parents,'work must be outside the source directory')
    work.mkdir(parents=True,exist_ok=True)
    need(not any(work.iterdir()),'work directory must be empty')
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','BLIS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    certificate=(source/'certificate.csv').read_bytes();expected=(source/'expected.json').read_bytes()
    record={'status':'INCOMPLETE','python':platform.python_version(),'dependencies':'stdlib only',
            'source_pins_checked_before_helpers':True,'numerical_threads':1,'children':[]}
    started=time.monotonic()
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal'
        generated=work/(mode+'.csv');checked=work/(mode+'.json')
        flags=['-O'] if optimized else []
        stages=[('generate',[str(source/'generate.py'),'--out',str(generated)]),
                ('check',[str(source/'check.py'),'--certificate',str(generated),'--out',str(checked)])]
        for stage,arguments in stages:
            command=[sys.executable,*flags,*arguments];begin=time.monotonic()
            try:r=subprocess.run(command,env=env,capture_output=True,text=True,timeout=20)
            except subprocess.TimeoutExpired as e:
                record['failure']='20s child timeout; evidence incomplete'
                (work/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
                raise ValueError(record['failure']) from e
            record['children'].append({'mode':mode,'stage':stage,'exit_code':r.returncode,
                'seconds':time.monotonic()-begin,'timeout_seconds':20})
            need(r.returncode==0,'child failed; evidence incomplete: '+r.stdout+r.stderr)
            if stage=='generate':need(generated.read_bytes()==certificate,'entire certificate bytes differ')
            else:need(checked.read_bytes()==expected,'entire independent checker record differs')
    need((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/O full records differ')
    record.update({'status':'FRESH_COMPLETE_MAJORITY618_SOURCE_RECONSTRUCTION',
        'generators_completed':2,'checkers_completed':2,'entire_certificate_bytes_match':True,
        'entire_expected_records_match':True,'normal_optimized_records_identical':True,
        'certificate_sha256':hashlib.sha256(certificate).hexdigest(),
        'expected_record_sha256':hashlib.sha256(expected).hexdigest(),
        'seconds':time.monotonic()-started,
        'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    (work/'verification.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))

if __name__=='__main__':main()
