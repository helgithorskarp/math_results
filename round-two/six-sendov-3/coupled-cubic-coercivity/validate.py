#!/usr/bin/env python3
"""Serial complete-map and damaged external-fixture validation.

Actual six-sendov-3 / researcher. Same-author validation, no formalization
or independent review. Native threads1, child45s, no ceiling increases.
"""
from pathlib import Path
import copy
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
NATIVE=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')


def main():
    original=json.loads((HERE/'EXPECTED.json').read_text())
    cases=[]
    for name in ('last_variance_map','whole_signed_map','actual_hypothesis',
                 'endpoint','last_stability_margin','critical_multiplicity',
                 'physical_objective_swap','bool_int_alias'):
        obj=copy.deepcopy(original)
        if name=='last_variance_map':obj['whole_variance_and_absorption_maps'].pop()
        elif name=='whole_signed_map':obj['whole_signed_and_dual_maps'][-1]['all_twelve_field_polynomial_maps_sha256']='0'*64
        elif name=='actual_hypothesis':obj['scope']='arbitrary critical tuple,no actual closed original disk'
        elif name=='endpoint':obj['budgets']['eta_endpoint']='1/16384'
        elif name=='last_stability_margin':obj['budgets']['rows'].pop()
        elif name=='critical_multiplicity':obj['complete_arbitrary_critical_controls'][0]['complete_critical_multiset'].pop()
        elif name=='physical_objective_swap':obj['budgets']['physical_error']='230'
        else:obj['complete_arbitrary_critical_controls'][0]['index']=False
        cases.append((name,json.dumps(obj),'complete typed record mismatch'))
    cases.append(('duplicate_key','{"agent":0,"agent":1}','duplicate JSON key'))
    cases.append(('nonfinite','{"value":NaN}','nonfinite JSON constant'))
    env=os.environ.copy()
    for name in NATIVE:env[name]='1'
    rows=[];summary=None;start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='.coupled-fixtures-',dir=HERE) as tmp:
        for optimized in (False,True):
            argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(HERE/'verify.py')]
            t=time.monotonic();p=subprocess.run(argv,cwd=HERE,env=env,capture_output=True,text=True,timeout=45)
            if p.returncode:raise RuntimeError('positive verification failed: '+p.stderr)
            result=json.loads(p.stdout)
            if summary is not None and result!=summary:raise RuntimeError('normal/optimized whole summary differs')
            summary=result;rows.append({'mode':'optimized' if optimized else 'normal','case':'positive','seconds':time.monotonic()-t,'output':result})
            for name,body,reason in cases:
                path=Path(tmp)/(name+'.json');path.write_text(body)
                t=time.monotonic();p=subprocess.run(argv+['--fixture',str(path)],cwd=HERE,env=env,capture_output=True,text=True,timeout=45)
                if p.returncode!=1 or reason not in p.stderr:raise RuntimeError('intended fixture rejection failed: '+name+' '+p.stderr)
                rows.append({'mode':'optimized' if optimized else 'normal','case':name,'seconds':time.monotonic()-t,'expected_reason':reason,'observed':p.stderr.strip()})
    source={}
    for name in ('PROOF.md','README.md','LITERATURE.md','arithmetic.py','budgets.py','verify.py','EXPECTED.json','validate.py'):
        data=(HERE/name).read_bytes();source[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    result={'agent':'six-sendov-3','role':'researcher','status':'PASS',
      'ordinary_proof_unformalized':True,'independent_review':False,
      'python':sys.version,'native_threads':1,'serial_children':True,
      'child_guard_seconds':45,'whole_seconds':time.monotonic()-start,
      'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
      'positive_modes':2,'intended_external_fixture_rejections':len(cases)*2,
      'summary':summary,'whole_runs':rows,'source_bytes_sha256':source}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('whole_runs','source_bytes_sha256')},sort_keys=True))


if __name__=='__main__':main()
