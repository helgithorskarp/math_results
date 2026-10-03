#!/usr/bin/env python3
"""Serial, isolated normal/optimized reproducibility and whole-record damage.

Actual six-sendov-3 / researcher. This is not independent review.
"""
from pathlib import Path
import sys
import json
import os
import copy
import hashlib
import subprocess
import tempfile
import time
import resource

HERE=Path(__file__).resolve().parent
NATIVE=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')

def batch_child(path):
    sys.path.insert(0,str(HERE))
    from verify import check_source,build,check_fixture,CertificateError,canonical,sha256
    check_source();record=build();rows=[]
    for case in json.loads(path.read_text()):
        try:check_fixture(record,Path(case['path']))
        except CertificateError as e:
            if str(e)!=case['reason']:raise RuntimeError('unexpected external rejection '+case['name'])
            rows.append({'name':case['name'],'reason':str(e)})
        else:raise RuntimeError('bad external full record accepted '+case['name'])
    print(json.dumps({'status':'PASS','whole_record_sha256':sha256(canonical(record)).hexdigest(),'rejections':rows},sort_keys=True))

def main():
    env=os.environ.copy()
    for name in NATIVE:env[name]='1'
    fixture=json.loads((HERE/'EXPECTED.json').read_text());cases=[]
    for name in ('missing_ninth_root','missing_ninth_normal','missing_last_primitive_degree',
      'changed_last_root_coefficient','changed_last_normal_coefficient','missing_last_critical_moment',
      'false_objective_coefficient','omitted_parameter_row','false_analytic_scope',
      'bool_type_alias','omitted_embedding_budget'):
        row=copy.deepcopy(fixture)
        if name=='missing_ninth_root':row['all_nine_parameter_root_jets'].pop()
        elif name=='missing_ninth_normal':row['all_nine_parameter_half_normals'].pop()
        elif name=='missing_last_primitive_degree':row['full_primitive_coefficients'].pop()
        elif name=='changed_last_root_coefficient':row['all_nine_fixed_root_jets'][-1][-1][1][0][1][0][0]='1'
        elif name=='changed_last_normal_coefficient':row['all_nine_fixed_half_normals'][-1][-1][1][0][1][0][0]='1'
        elif name=='missing_last_critical_moment':row['centered_moments']['U3'].pop()
        elif name=='false_objective_coefficient':row['constants']['K_eta'][0][0]='0'
        elif name=='omitted_parameter_row':row['all_nine_parameter_half_normals'][4][-1][1].pop()
        elif name=='false_analytic_scope':row['scope']='full explicit interval, no analytic bridge required'
        elif name=='bool_type_alias':row['order']=True
        else:row['strict_embedding_budgets'].pop('K_upper_to_10_gap')
        cases.append({'name':name,'body':json.dumps(row),'reason':'complete typed record mismatch'})
    cases.extend([{'name':'duplicate_key','body':'{"agent":0,"agent":1}','reason':'duplicate JSON key'},
                  {'name':'nonfinite','body':'{"v":NaN}','reason':'nonfinite JSON constant'}])
    runs=[];positive=None;start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='.validation-',dir=HERE) as tmp:
        temp=Path(tmp);cold=temp/'isolated';cold.mkdir()
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            _,name=line.split('  ',1);(cold/name).write_bytes((HERE/name).read_bytes())
        (cold/'SHA256SUMS').write_bytes((HERE/'SHA256SUMS').read_bytes())
        for optimized in (False,True):
            for directory,mode in ((HERE,'normal-source'),(cold,'isolated-source-only')):
                argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(directory/'verify.py')]
                t=time.monotonic();p=subprocess.run(argv,cwd=directory,env=env,capture_output=True,text=True,timeout=45)
                if p.returncode:raise RuntimeError('positive verifier failed '+p.stderr)
                result=json.loads(p.stdout)
                if positive is not None and result!=positive:raise RuntimeError('normal/O isolated summaries differ')
                positive=result;runs.append({'mode':mode,'optimized':optimized,'case':'positive','seconds':time.monotonic()-t,'output':result})
            batch=[]
            for case in cases:
                path=temp/(case['name']+'.json');path.write_text(case['body'])
                batch.append({'name':case['name'],'path':str(path),'reason':case['reason']})
            batch_path=temp/'batch.json';batch_path.write_text(json.dumps(batch))
            argv=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(HERE/'validate.py'),'--batch-child',str(batch_path)]
            t=time.monotonic();p=subprocess.run(argv,cwd=HERE,env=env,capture_output=True,text=True,timeout=45)
            if p.returncode:raise RuntimeError('whole external-fixture batch failed '+p.stderr)
            result=json.loads(p.stdout)
            if result['whole_record_sha256']!=positive['whole_record_sha256'] or len(result['rejections'])!=len(cases):raise RuntimeError('whole batch coverage differs')
            runs.append({'mode':'normal-source','optimized':optimized,'case':'external-fixtures','seconds':time.monotonic()-t,'output':result})
        # Source-byte guard rejects a changed source before any mathematical check.
        changed=cold/'jets.py';changed.write_bytes(changed.read_bytes()+b'\n# deliberately altered source\n')
        p=subprocess.run([sys.executable,'-I','-B',str(cold/'verify.py')],cwd=cold,env=env,capture_output=True,text=True,timeout=45)
        if p.returncode==0 or 'source-byte mismatch jets.py' not in p.stderr:raise RuntimeError('changed source was not rejected')
        runs.append({'mode':'isolated-source-only','case':'changed_source_byte','returncode':p.returncode,'expected_reason':'source-byte mismatch jets.py'})
    result={'agent':'six-sendov-3','role':'researcher','status':'PASS','ordinary_proof_unformalized':True,
      'independent_review':False,'python':sys.version,'native_threads':1,'serial_math_children':True,
      'child_guard_seconds':45,'positive_modes':4,'mathematical_damage_cases_per_positive':10,
      'whole_external_fixture_rejections':2*len(cases),'source_byte_rejections':1,
      'whole_seconds':time.monotonic()-start,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
      'whole_summary':positive,'whole_runs':runs,'manifest_sha256':hashlib.sha256((HERE/'SHA256SUMS').read_bytes()).hexdigest()}
    destination=Path(sys.argv[2]) if len(sys.argv)==3 and sys.argv[1]=='--output' else HERE/'VALIDATION.json'
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='whole_runs'},sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--batch-child':batch_child(Path(sys.argv[2]))
    else:main()
