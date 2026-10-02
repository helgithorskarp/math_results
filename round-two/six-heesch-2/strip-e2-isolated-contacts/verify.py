"""Four serial guarded jobs, exact source pins and normal/optimized agreement."""
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
import deps

HERE=Path(__file__).resolve().parent
def main():
    start=time.monotonic();expected=json.loads((HERE/'expected.json').read_text())
    for relative,pin in expected['source_pins'].items():
        if hashlib.sha256((HERE.parent/relative).read_bytes()).hexdigest()!=pin:
            raise ValueError('Changed source: '+relative)
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    env['PYTHONDONTWRITEBYTECODE']='1';jobs=[]
    for mode,options in [('normal',[]),('optimized',['-O'])]:
        for script,output in [('prove.py','produced'),('check.py','checked')]:
            if deps.paused():raise RuntimeError('Operations pause barrier')
            process=subprocess.run([sys.executable,*options,str(HERE/script)],cwd=HERE,
                env=env,text=True,capture_output=True,timeout=47)
            if process.returncode:raise RuntimeError(script+' failed: '+process.stderr)
            data=json.loads((HERE/'generated'/f'{output}-{mode}.json').read_text())
            if not data['complete'] or data['mathematics_sha256']!=expected['mathematics_sha256'][output]:
                raise ValueError('Incomplete or changed mathematics')
            if output=='checked' and len(data['evidence']['damaged_controls'])!=8:
                raise ValueError('Missing damage controls')
            jobs.append({'mode':mode,'script':script,'seconds':data['seconds'],
                         'max_rss_kib':data['max_rss_kib']})
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'serial_jobs':4,
            'E2_exclusions':['U0','U1','U3upper'],'all_k_minimum':6,
            'tree_nodes':[5,20,10],'blocked_supplier_transports':26,
            'E1_premises':16,'normal_optimized_agree':True,
            'reader_damage_controls':8,'material_parameters':[6,7,8,9,12,40],
            'Heesch_number_conclusion':False,'mathematics_sha256':expected['mathematics_sha256'],
            'seconds':round(time.monotonic()-start,3),
            'max_child_rss_kib':max(j['max_rss_kib'] for j in jobs),
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (HERE/'generated'/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
