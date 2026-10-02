#!/usr/bin/env python3
"""Serial normal/optimized exact replay and explicit malformed fixture rejection."""
import copy,hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
THREADS=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
env=dict(os.environ,**{k:'1' for k in THREADS})
env['PYTHONDONTWRITEBYTECODE']='1'

def require(ok,reason):
    if not ok:raise ValueError(reason)

def run(script,mode,fixture=None):
    args=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(script)]
    if fixture is not None:args+=['--fixture',str(fixture)]
    start=time.monotonic()
    result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,timeout=45)
    return result,time.monotonic()-start

def main():
    fixture=json.loads((ROOT/'EXPECTED.json').read_text())
    record=[];positive=[]
    with tempfile.TemporaryDirectory(prefix='cube-fixtures-',dir=ROOT) as tmp:
        tmp=Path(tmp)
        mutations=[]
        def modify(label,path,value,reason='complete typed fixture mismatch'):
            x=copy.deepcopy(fixture);target=x
            for key in path[:-1]:target=target[key]
            target[path[-1]]=value
            mutations.append((label,json.dumps(x),reason))
        modify('wrong-schema',['schema'],'damaged')
        modify('extra-control',['controls','extra'],{'wrong':True})
        modify('coefficient-digest',['controls','entire-top-three-coefficient-reduction','sha256'],'0'*64)
        modify('false-margin',['positive_margins','energy-feedback-H25'],'-1')
        modify('float-control-count',['internal_damage_controls'],12.0,'invalid fixture type')
        modify('bool-control-count',['internal_damage_controls'],True)
        modify('wrong-controls-type',['controls'],[])
        x=copy.deepcopy(fixture);del x['controls']['whole-fourth-newton'];mutations.append(('missing-whole-identity',json.dumps(x),'complete typed fixture mismatch'))
        body=json.dumps(fixture)
        mutations.append(('duplicate-key','{"schema": "paired-cube-energy-v1",'+body[1:],'duplicate fixture key'))
        mutations.append(('nan-number','{"value":NaN}','invalid JSON constant'))
        for mode in ['normal','optimized']:
            result,elapsed=run(ROOT/'verify.py',mode)
            require(result.returncode==0,'positive replay failed: '+result.stderr)
            decoded=json.loads(result.stdout)
            require(decoded.get('status')=='PASS','missing positive PASS')
            positive.append({'mode':mode,'seconds':elapsed,'output':decoded})
            for label,body,reason in mutations:
                path=tmp/(label+'.json');path.write_text(body)
                result,elapsed=run(ROOT/'verify.py',mode,path)
                require(result.returncode==1 and ('FAIL: '+reason) in result.stderr,'external damage escaped or failed for wrong reason: '+label+' '+result.stderr)
                record.append({'mode':mode,'case':label,'rejected':True,'reason':reason})
            changed=tmp/'changed-entry.py'
            changed.write_text((ROOT/'verify.py').read_text()+'\n# harmless edit tests the full source pin\n')
            result,elapsed=run(changed,mode,ROOT/'EXPECTED.json')
            require(result.returncode==1 and 'FAIL: complete typed fixture mismatch' in result.stderr,'source-pin damage escaped')
            record.append({'mode':mode,'case':'changed-source-pin','rejected':True,'reason':'complete typed fixture mismatch'})
    require(positive[0]['output']==positive[1]['output'],'normal/optimized complete output diverged')
    report={'schema':'paired-cube-validation-v1','python_version':sys.version.split()[0],
            'positive_replays':positive,'external_rejections':record,'external_fixture_rejections':20,'external_source_pin_rejections':2,
            'serial':True,'native_thread_counts':{k:'1' for k in THREADS},'child_timeout_seconds':45,
            'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'scope':'same-author finite exact corroboration, not formal proof or independent review'}
    (ROOT/'VALIDATION.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','whole_controls':positive[0]['output']['whole_controls'],'strict_margins':positive[0]['output']['strict_margins'],
         'internal_damage_controls':positive[0]['output']['internal_damage_controls'],'external_fixture_rejections':20,'external_source_pin_rejections':2,
         'record_sha256':positive[0]['output']['record_sha256'],'child_peak_rss_kib':report['child_peak_rss_kib']},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
