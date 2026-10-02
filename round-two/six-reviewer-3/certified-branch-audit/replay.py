#!/usr/bin/env python3
"""Pinned source replay; downloaded author code runs only as corroboration."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE=Path(__file__).resolve().parent


def need(ok,label):
    if not ok:raise ValueError(label)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input-directory',type=Path,help='already fetched, hashed inputs; otherwise fetch the public pinned URLs')
    parser.add_argument('--write-validation',type=Path)
    args=parser.parse_args()
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='sendov-effective-independent-') as temp:
        root=Path(temp);original=root/'original';original.mkdir();inputs={}
        for row in manifest['files']:
            if args.input_directory:raw=(args.input_directory/row['label']).read_bytes()
            else:
                request=urllib.request.Request(row['raw_url'],headers={'User-Agent':'independent-math-review/1.0'})
                with urllib.request.urlopen(request,timeout=25) as response:
                    need(response.status==200,'public input response');raw=response.read(400001)
            need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'complete pinned input '+row['label'])
            inputs[row['label']]=raw
            if row['label'].startswith('author-'):(original/Path(row['path']).name).write_bytes(raw)
        runs=[]
        def child(label,script,flags=(),extra=(),accept=True):
            start=time.monotonic();p=subprocess.run([sys.executable,'-I','-B',*flags,str(script),*extra],env=env,capture_output=True,text=True,timeout=45)
            need((p.returncode==0)==accept,'child status '+label)
            if accept:need(not p.stderr,'accepted child stderr '+label)
            r={'label':label,'elapsed_seconds':round(time.monotonic()-start,6),'exit':p.returncode,
               'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_nonempty':bool(p.stderr)}
            runs.append(r);print(json.dumps(r),flush=True);return p.stdout
        fixture=original/'expected.json'
        source_outputs=[]
        for flags in ((),('-O',)):
            text=child('original-'+('O' if flags else 'normal'),original/'verify.py',flags)
            source_outputs.append(text)
            need(json.loads(text)==manifest['original_stdout'],'entire original output and embedded whole fixture checks')
        need(source_outputs[0]==source_outputs[1],'whole original normal/O output')
        outputs=[]
        for flags in ((),('-O',)):
            outputs.append(child('independent-'+('O' if flags else 'normal'),HERE/'audit.py',flags,('--author-fixture',str(fixture))))
        need(outputs[0]==outputs[1],'whole independent normal/O output')
        bad=json.loads((HERE/'EXPECTED.json').read_text());del bad['full_cube_certificate']['rouche_margin_lower']
        (root/'missing.json').write_text(json.dumps(bad))
        bad=json.loads((HERE/'EXPECTED.json').read_text());bad['certified19eta_tube']['symmetric_curvature_lower']='-1'
        (root/'altered.json').write_text(json.dumps(bad))
        (root/'malformed.json').write_text('{')
        for flags in ((),('-O',)):
            for name in ('missing','altered','malformed'):
                child('rejected-'+name+'-'+('O' if flags else 'normal'),HERE/'audit.py',flags,('--fixture',str(root/(name+'.json'))),False)
        record={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','status':'PASS',
                'python':sys.version.split()[0],'native_threads':1,'child_guard_seconds':45,'local_math_children_serial':True,
                'inputs_verified':len(inputs),'independent_full_fixture_sha256':hashlib.sha256(json.dumps(json.loads((HERE/'EXPECTED.json').read_text()),sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                'original_full_fixture_verified_by_original':True,'entire_initial_original_record_independently_equal':True,
                'whole_outputs_normal_O_equal':True,'external_fixture_rejections':6,
                'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'runs':runs,
                'trust_boundary':'independent checker imports only its newly written exact_numbers and controls; author replay is separate, source-bound corroboration; ordinary analytic bridges and explicitly scoped prior collapsed/minimum-germ theorems are unformalized'}
        if args.write_validation:args.write_validation.write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record),flush=True)


if __name__=='__main__':main()
