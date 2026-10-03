#!/usr/bin/env python3
"""Serial whole-record validation, isolated replay and damaged inputs.

Actual six-sendov-3 / researcher. No independent review or formalization.
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


def fixture_child(path):
    # ONE independently regenerated whole record per normal/O batch;
    # the exact same external-input API is used by verify.py's main.
    sys.path.insert(0,str(HERE))
    from verify import build_record,check_fixture
    from arithmetic import CertificateError,canonical,sha256
    record=build_record();rows=[]
    for case in json.loads(path.read_text()):
        try:check_fixture(record,Path(case['path']))
        except CertificateError as e:
            if case['reason'] not in str(e):raise RuntimeError('wrong whole-record rejection '+case['name'])
            rows.append({'case':case['name'],'expected_reason':case['reason'],'observed':str(e)})
        else:raise RuntimeError('malformed whole record accepted '+case['name'])
    print(json.dumps({'status':'PASS','whole_record_sha256':sha256(canonical(record)).hexdigest(),
      'all_whole_record_rejections':rows},sort_keys=True))


def main():
    original=json.loads((HERE/'EXPECTED.json').read_text())
    cases=[]
    for name in ('omit_last_phase','omit_last_lower_coefficient','drop_whole_map',
                 'false_actual_domain','endpoint_transport','physical_objective_swap',
                 'omit_last_budget','omit_critical_multiplicity','bool_type_alias','last_control_motion',
                 'omit_last_bootstrap_margin','omit_early_stage'):
        obj=copy.deepcopy(original)
        if name=='omit_last_phase':obj['whole_phase_maps']['whole_nine_phase_tables'].pop()
        elif name=='omit_last_lower_coefficient':obj['whole_phase_maps']['whole_nine_phase_tables'][-1]['all_seven_lower_degrees'].pop()
        elif name=='drop_whole_map':obj['whole_phase_maps']['whole_maps'].pop()
        elif name=='false_actual_domain':obj['scope']='no original disk or genuine entry needed'
        elif name=='endpoint_transport':obj['fresh_complete_budgets']['actual_unconditional_endpoint']='1/10000'
        elif name=='physical_objective_swap':obj['fresh_complete_budgets']['physical_error']='175'
        elif name=='omit_last_budget':obj['fresh_complete_budgets']['rows'].pop()
        elif name=='omit_critical_multiplicity':obj['complete_arbitrary_critical_controls'][-1]['complete_critical_multiset'].pop()
        elif name=='bool_type_alias':obj['complete_arbitrary_critical_controls'][0]['index']=False
        elif name=='last_control_motion':obj['complete_arbitrary_critical_controls'][-1]['all_nine_linear_motions'][-1]['FULL_clear_r16_displacement'][0].pop()
        elif name=='omit_last_bootstrap_margin':obj['complete_actual_entry_to_LC_budgets']['all_complete_margins'].pop()
        else:obj['complete_actual_entry_to_LC_budgets']['two_square_forward_stages'].pop(0)
        cases.append((name,json.dumps(obj),'complete typed record mismatch'))
    cases.append(('duplicate_key','{"agent":0,"agent":1}','duplicate JSON key'))
    cases.append(('nonfinite','{"v":NaN}','nonfinite JSON constant'))
    env=os.environ.copy()
    for name in NATIVE:env[name]='1'
    runs=[];summary=None;start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='.receiving-validation-',dir=HERE) as tmp:
        cold=Path(tmp)/'cold';cold.mkdir()
        for n in ('arithmetic.py','budgets.py','bootstrap.py','verify.py','EXPECTED.json'):(cold/n).write_bytes((HERE/n).read_bytes())
        for optimized in (False,True):
            for directory,mode in ((HERE,'normal-source'),(cold,'isolated-five-file-copy')):
                argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(directory/'verify.py')]
                t=time.monotonic();p=subprocess.run(argv,cwd=directory,env=env,capture_output=True,text=True,timeout=45)
                if p.returncode:raise RuntimeError('whole positive validation failed: '+p.stderr)
                result=json.loads(p.stdout)
                if summary is not None and result!=summary:raise RuntimeError('whole record summary differs')
                summary=result;runs.append({'mode':mode,'optimized':optimized,'case':'positive','seconds':time.monotonic()-t,'output':result})
            argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(HERE/'verify.py')]
            batch=[]
            for name,body,reason in cases:
                path=Path(tmp)/(name+'.json');path.write_text(body)
                batch.append({'name':name,'path':str(path),'reason':reason})
            batch_path=Path(tmp)/'batch.json';batch_path.write_text(json.dumps(batch))
            argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(HERE/'validate.py'),'--fixture-child',str(batch_path)]
            t=time.monotonic();p=subprocess.run(argv,cwd=HERE,env=env,capture_output=True,text=True,timeout=45)
            if p.returncode:raise RuntimeError('whole record fixture batch failed: '+p.stderr)
            result=json.loads(p.stdout)
            if result['whole_record_sha256']!=summary['whole_record_sha256'] or len(result['all_whole_record_rejections'])!=len(cases):raise RuntimeError('whole batch coverage differs')
            runs.append({'mode':'normal-source','optimized':optimized,'case':'all_external_fixtures','seconds':time.monotonic()-t,'output':result})
    source={}
    for name in ('arithmetic.py','budgets.py','bootstrap.py','verify.py','EXPECTED.json','validate.py','PROOF.md','BOOTSTRAP.md','README.md','LITERATURE.md'):
        b=(HERE/name).read_bytes();source[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    result={'agent':'six-sendov-3','role':'researcher','status':'PASS',
      'ordinary_proof_unformalized':True,'independent_review':False,
      'python':sys.version,'native_threads':1,'serial_math_children':True,'child_guard_seconds':45,
      'positive_modes':4,'intended_external_fixture_rejections':len(cases)*2,
      'whole_seconds':time.monotonic()-start,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
      'whole_summary':summary,'whole_runs':runs,'source_bytes_sha256':source}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('whole_runs','source_bytes_sha256')},sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--fixture-child':fixture_child(Path(sys.argv[2]))
    else:main()
