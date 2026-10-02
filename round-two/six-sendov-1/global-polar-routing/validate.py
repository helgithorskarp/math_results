#!/usr/bin/env python3
"""Serial external evidence checks; CPython3.10+ standard library.

Default verifies an existing sealed manifest and reads only source. --seal
explicitly writes MANIFEST.json and the compact VALIDATION.json run record.
All child/native threads1,45s per mathematical child, one child at a time.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time

FILES=['.gitignore','PROOF.md','README.md','LITERATURE.md','verify.py',
       'validate.py','EXPECTED.json']
NATIVE=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']

def require(ok,message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return {'bytes':path.stat().st_size,'sha256':sha256(path.read_bytes()).hexdigest()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest={'schema':'global-polar-routing-source-v1','agent':'six-sendov-1',
              'role':'researcher','files':{f:digest(root/f) for f in FILES}}
    path=root/'MANIFEST.json'
    if args.seal:
        path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads(path.read_text())==manifest,'entire sealed source manifest differs')
    env=dict(os.environ,**{k:'1' for k in NATIVE})
    def run(script,optimized=False,fixture=None):
        cmd=[sys.executable,'-I','-B']
        if optimized:cmd+=['-O']
        cmd+=[str(script)]
        if fixture:cmd+=['--fixture',str(fixture)]
        t=time.monotonic()
        result=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45)
        return result,time.monotonic()-t

    positive=[]
    for optimized in [False,True]:
        child,seconds=run(root/'verify.py',optimized)
        require(child.returncode==0,'positive checker failed: '+child.stderr[:500])
        record=json.loads(child.stdout)
        positive.append({'optimized':optimized,'seconds':seconds,'complete_output':record})
    require(positive[0]['complete_output']==positive[1]['complete_output'],'normal/optimized full outputs differ')

    expected=json.loads((root/'EXPECTED.json').read_text())
    damages=[
      ('extra_field',lambda x:x.__setitem__('not_a_proof_field',1)),
      ('missing_full_tail',lambda x:x.pop('complete_tail')),
      ('truncated_polynomial',lambda x:x['scalar_certificates']['mean']['polynomial'].pop()),
      ('rational_float',lambda x:x['scalar_certificates']['mean']['head'].__setitem__('numerator',4.0)),
      ('integer_boolean',lambda x:x['variance_budgets'].__setitem__('normalized',True)),
      ('zero_boolean',lambda x:x['complete_tail'][0].__setitem__('numerator',False)),
      ('wrong_denominator',lambda x:x['routed_eta_endpoint'].__setitem__('denominator',2**36)),
      ('complex_coefficient',lambda x:x['gaussian_controls'][0]['polar'][1].__setitem__('numerator',19)),
      ('missing_critical_multiplicity',lambda x:x['actual_controls'][0]['critical_multiplicities'].pop()),
      ('source_identity_changed',lambda x:x.__setitem__('agent','someone_else')),
    ]
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='sendov-polar-external-') as tmp:
        work=Path(tmp)
        fixtures=[]
        for label,mutate in damages:
            bad=deepcopy(expected);mutate(bad)
            f=work/(label+'.json')
            f.write_text(json.dumps(bad,sort_keys=True))
            fixtures.append((label,f))
        for label,text in [('truncated_json','{"schema":'),
                           ('duplicate_key','{"schema":"one","schema":"two"}'),
                           ('nonfinite_number','{"unexpected":NaN}')]:
            f=work/(label+'.json');f.write_text(text);fixtures.append((label,f))
        fixtures.append(('absent_fixture',work/'absent.json'))
        for optimized in [False,True]:
            for label,f in fixtures:
                child,seconds=run(root/'verify.py',optimized,f)
                require(child.returncode!=0,'external fixture damage accepted '+label)
                rejected.append({'label':label,'optimized':optimized,'returncode':child.returncode})
        copied=work/'source-copy';copied.mkdir()
        for f in FILES+['MANIFEST.json']:shutil.copyfile(root/f,copied/f)
        source_rejected=[]
        for damaged in ['verify.py','README.md']:
            original=(copied/damaged).read_bytes()
            (copied/damaged).write_bytes(original+b'\n')
            for optimized in [False,True]:
                child,seconds=run(copied/'verify.py',optimized)
                require(child.returncode!=0 and 'source manifest' in child.stderr,
                        'copied source pin damage accepted '+damaged)
                source_rejected.append({'file':damaged,'optimized':optimized,'returncode':child.returncode})
            (copied/damaged).write_bytes(original)
    evidence={'agent':'six-sendov-1','role':'researcher',
              'status':'ordinary author algebra and checks; unformalized and independently unreviewed',
              'python':sys.version.split()[0],'third_party_packages':[],
              'serial_math_children':True,'native_threads':{k:1 for k in NATIVE},
              'child_guard_seconds':45,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'positive':positive,'external_fixture_rejections':rejected,
              'copied_source_pin_rejections':source_rejected,
              'manifest_sha256':sha256(path.read_bytes()).hexdigest()}
    if args.seal:
        (root/'VALIDATION.json').write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','positive_runs':2,'external_fixture_rejections':len(rejected),
                      'copied_source_pin_rejections':len(source_rejected),
                      'whole_record_sha256':positive[0]['complete_output']['whole_record_sha256'],
                      'peak_child_rss_kib':evidence['peak_child_rss_kib']},sort_keys=True))

if __name__=='__main__':
    main()
