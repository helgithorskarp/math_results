#!/usr/bin/env python3
"""Portable serial author checks. Default reads frozen source; --seal writes it."""
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

FILES=['.gitignore','PROOF.md','README.md','LITERATURE.md',
       'verify.py','validate.py','EXPECTED.json']
NATIVE=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']

def require(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest={'schema':'mean-square-routing-source-v1',
              'agent':'six-sendov-1','role':'researcher',
              'sha256':{f:sha256((root/f).read_bytes()).hexdigest() for f in FILES},
              'bytes':{f:(root/f).stat().st_size for f in FILES}}
    path=root/'MANIFEST.json'
    if args.seal:path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    else:require(json.loads(path.read_text())==manifest,'entire sealed source manifest differs')
    env=dict(os.environ,**{k:'1' for k in NATIVE})
    def run(script,optimized=False,fixture=None):
        cmd=[sys.executable,'-I','-B']
        if optimized:cmd+=['-O']
        cmd+=[str(script)]
        if fixture:cmd+=['--fixture',str(fixture)]
        start=time.monotonic()
        child=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45)
        return child,time.monotonic()-start

    positive=[]
    for optimized in [False,True]:
        child,seconds=run(root/'verify.py',optimized)
        require(child.returncode==0,'positive checker failed: '+child.stderr[:400])
        positive.append({'optimized':optimized,'seconds':seconds,'whole_output':json.loads(child.stdout)})
    require(positive[0]['whole_output']==positive[1]['whole_output'],'normal/optimized whole outputs differ')
    expected=json.loads((root/'EXPECTED.json').read_text())
    damages=[
      ('extra_field',lambda x:x.__setitem__('not_a_proof_field',1)),
      ('missing_radial_face',lambda x:x['whole_radial_faces'].pop()),
      ('changed_mean_square',lambda x:x['whole_mean_square_coefficients'].__setitem__('(0, 2)','0')),
      ('missing_sector',lambda x:x['whole_envelopes']['7:1']['all_sectors'].pop()),
      ('truncated_polynomial',lambda x:x['whole_envelopes']['6:2']['all_sectors'][2]['whole_polynomial'].pop()),
      ('floating_integer',lambda x:x.__setitem__('version',1.0)),
      ('integer_boolean',lambda x:x['whole_envelopes']['7:1']['all_sectors'][0].__setitem__('k',False)),
      ('wrong_endpoint',lambda x:x.__setitem__('eta_endpoint','1/16384')),
      ('damaged_polar_stream',lambda x:x['whole_polar']['scalar_certificates']['mean']['polynomial'].__setitem__(3,'0')),
      ('lost_skew_control',lambda x:x['whole_skew_controls'].pop()),
      ('changed_normal_constant',lambda x:x['local_basic_coefficients'].__setitem__('kappa','0')),
      ('missing_majorant',lambda x:x['first_majorant_polynomials'].pop('7')),
      ('missing_hessian_row',lambda x:x['whole_literal_controls'][0]['whole_ordered_hessian'].pop()),
      ('changed_complete_trace',lambda x:x['whole_literal_controls'][4]['all_centered_traces'][8].__setitem__(1,'1')),
      ('changed_strict_margin',lambda x:x['strict_full_window_margins'].__setitem__('first_signed_gradient3over40','0')),
    ]
    rejected=[];source_rejected=[]
    with tempfile.TemporaryDirectory(prefix='sendov-mean-square-check-') as tmp:
        work=Path(tmp);fixtures=[]
        for label,mutate in damages:
            bad=deepcopy(expected);mutate(bad)
            f=work/(label+'.json');f.write_text(json.dumps(bad,sort_keys=True))
            fixtures.append((label,f))
        for label,text in [('truncated_json','{"version":'),
                           ('duplicate_key','{"version":1,"version":1}'),
                           ('nonfinite_number','{"version":NaN}')]:
            f=work/(label+'.json');f.write_text(text);fixtures.append((label,f))
        fixtures.append(('absent_fixture',work/'absent.json'))
        for optimized in [False,True]:
            for label,f in fixtures:
                child,seconds=run(root/'verify.py',optimized,f)
                require(child.returncode!=0,'external damage accepted: '+label)
                rejected.append({'label':label,'optimized':optimized,'returncode':child.returncode})
        copied=work/'source-copy';copied.mkdir()
        for f in FILES+['MANIFEST.json']:shutil.copyfile(root/f,copied/f)
        for damaged in ['verify.py','PROOF.md']:
            original=(copied/damaged).read_bytes()
            (copied/damaged).write_bytes(original+b'\n')
            for optimized in [False,True]:
                child,seconds=run(copied/'verify.py',optimized)
                require(child.returncode!=0 and 'source pin manifest' in child.stderr,
                        'copied source pin damage accepted: '+damaged)
                source_rejected.append({'file':damaged,'optimized':optimized,'returncode':child.returncode})
            (copied/damaged).write_bytes(original)
    evidence={'agent':'six-sendov-1','role':'researcher',
              'status':'ordinary author proof and finite checks; unformalized and independently unreviewed',
              'python':sys.version.split()[0],'third_party_packages':[],
              'serial_math_children':True,'native_threads':{k:1 for k in NATIVE},
              'child_guard_seconds':45,
              'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'positive':positive,'external_fixture_rejections':rejected,
              'copied_source_pin_rejections':source_rejected,
              'manifest_sha256':sha256(path.read_bytes()).hexdigest()}
    if args.seal:(root/'VALIDATION.json').write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','positive_runs':2,
                      'external_fixture_rejections':len(rejected),
                      'copied_source_pin_rejections':len(source_rejected),
                      'whole_record_sha256':positive[0]['whole_output']['whole_record_sha256'],
                      'peak_child_rss_kib':evidence['peak_child_rss_kib']},sort_keys=True))

if __name__=='__main__':main()
