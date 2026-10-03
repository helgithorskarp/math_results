#!/usr/bin/env python3
"""Serial portable replay and rejection controls; same-author validation."""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FILES=('.gitignore','PROOF.md','LITERATURE.md','README.md','verify.py',
       'validate.py','COVER.json','EXPECTED.json')
GUARD=45

def require(ok,msg):
    if not ok:raise ValueError(msg)
def hashes(directory):
    return {name:dict(bytes=len((directory/name).read_bytes()),
                      sha256=hashlib.sha256((directory/name).read_bytes()).hexdigest())
            for name in FILES}
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    before=hashes(HERE)
    if args.seal:
        manifest=dict(agent='six-sendov-1',role='researcher',files=before,
                      trust='Byte pins detect changes, not joint source/evidence replacement')
        (HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads((HERE/'MANIFEST.json').read_text())['files']==before,
                'whole source manifest')
    env=dict(os.environ)
    for key in THREADS:env[key]='1'
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    sha=expected['full_checked_record_sha256']
    runs=[];positives=[];negative=[]
    def run(directory,options,mode,success,label):
        flags=['-I','-B']+(['-O'] if mode=='optimized' else [])
        cmd=[sys.executable,*flags,str(directory/'verify.py'),*options]
        start=time.monotonic()
        result=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=GUARD)
        seconds=time.monotonic()-start
        require((result.returncode==0)==success,'unexpected child outcome '+label)
        if success:
            record=json.loads(result.stdout)
            require(record['result']=='PASS' and record['record_sha256']==sha,
                    'whole checked replay '+label)
            positives.append(label)
        else:
            require(result.returncode==1 and result.stderr.startswith('FAIL: '),
                    'rejection must be a controlled failed check '+label)
            negative.append(label)
        runs.append(dict(label=label,mode=mode,seconds=seconds,
                         exit_code=result.returncode,positive=success))
    with tempfile.TemporaryDirectory(prefix='sendov-eleven-twentieths-') as td:
        root=Path(td)
        cold=root/'cold';cold.mkdir()
        for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,cold/name)
        for mode in ('normal','optimized'):
            run(HERE,[],mode,True,'local-'+mode)
            run(cold,[],mode,True,'cold-'+mode)
        damages=('last-polar-coefficient','drop-polar-series','newton-eighth',
                 'origin-drop-eighth','origin-odd-root','uncouple-energy','omit-leaf')
        for mode in ('normal','optimized'):
            for damage in damages:
                run(HERE,['--damage',damage],mode,False,'math-'+damage+'-'+mode)
        fixtures=[]
        x=deepcopy(expected);x['worst_polar']['integral']='0';fixtures.append(('wrong-polar-integral',x))
        x=deepcopy(expected);x['least_origin']['terms'].pop();fixtures.append(('missing-eighth',x))
        x=deepcopy(expected);x['full_checked_record_sha256']='0'*64;fixtures.append(('wrong-full-fingerprint',x))
        x=deepcopy(expected);x['polar_cells']=True;fixtures.append(('wrong-type',x))
        x=deepcopy(expected);x['unexpected']=True;fixtures.append(('extra-key',x))
        for label,x in fixtures:
            file=root/(label+'.json');file.write_text(json.dumps(x))
            for mode in ('normal','optimized'):
                run(HERE,['--expected',str(file)],mode,False,'fixture-'+label+'-'+mode)
        for mode in ('normal','optimized'):
            damaged=root/('source-'+mode);damaged.mkdir()
            for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,damaged/name)
            with (damaged/'PROOF.md').open('a') as file:file.write('\nchanged source byte\n')
            run(damaged,[],mode,False,'source-pin-'+mode)
    require(hashes(HERE)==before,'source bytes changed during verification')
    record=dict(agent='six-sendov-1',role='researcher',result='PASS',
                checked_at=datetime.now(timezone.utc).isoformat(),
                python=sys.version.split()[0],interpreter='CPython standard library',
                record_sha256=sha,guard_seconds=GUARD,serial=True,
                native_threads={key:1 for key in THREADS},
                resource_scope='unchanged one CPU/two GiB; no escalation',
                max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                max_child_seconds=max(r['seconds'] for r in runs),
                full_typed_positives=positives,rejections=negative,runs=runs,
                source_unchanged=True,independent_review=False,formalized=False,
                omitted_large_artifact=True,omission='Private verbose pilot coefficient corpora; ALL defining inputs and exact whole-case comparisons regenerate from source')
    if args.seal:
        (HERE/'VALIDATION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        archived=json.loads((HERE/'VALIDATION.json').read_text())
        require(archived['result']=='PASS' and archived['record_sha256']==sha,
                'archived validation evidence')
    print(json.dumps(dict(result='PASS',record_sha256=sha,
                          full_typed_positives=len(positives),rejections=len(negative),
                          max_child_seconds=record['max_child_seconds'],
                          max_child_rss_kib=record['max_child_rss_kib'])))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
