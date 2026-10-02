"""Bounded serial normal/optimized production and search-free replay."""
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
import deps

H=Path(__file__).absolute().parent

def main():
    start=time.monotonic()
    expected=json.loads((H/'expected.json').read_text())
    for relative,pin in expected['source_pins'].items():
        p=H.parent/relative
        if hashlib.sha256(p.read_bytes()).hexdigest()!=pin:
            raise ValueError('Changed source/dependency bytes: '+relative)
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    jobs=[]
    for mode,options in [('normal',[]),('optimized',['-O'])]:
        for script,output in [('prove.py','produced'),('check.py','checked')]:
            if deps.paused():raise RuntimeError('Operations pause barrier')
            run=subprocess.run([sys.executable,*options,str(H/script)],cwd=H,env=env,
                               text=True,capture_output=True,timeout=47)
            if run.returncode:raise RuntimeError(f'{script} failed: {run.stderr}')
            record=json.loads((H/'generated'/f'{output}-{mode}.json').read_text())
            if not record['complete'] or record['mathematics_sha256']!=expected['mathematics_sha256'][output]:
                raise ValueError('Incomplete or changed mathematics')
            if output=='produced' and len(record['damaged_wedge_controls'])!=3:
                raise ValueError('Missing false-wedge controls')
            if output=='checked' and len(record['evidence']['damaged_controls'])!=7:
                raise ValueError('Missing reader damage controls')
            jobs.append({'mode':mode,'script':script,'seconds':record['seconds'],
                         'mathematics_sha256':record['mathematics_sha256'],
                         'max_rss_kib':record['max_rss_kib']})
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'serial_jobs':4,
            'E2_identity_U4_empty':True,'E1_identity_U4_b3_empty':True,
            'all_k_minimum':6,'Heesch_number_conclusion':False,
            'normal_optimized_agree':True,'cap_suppliers':[4,4],
            'cap_parameter_cuts':[6],'collision_parameter_cuts':[6,7],
            'material_parameters':[6,7,8,9,12,40],
            'producer_damage_controls':3,'reader_damage_controls':7,
            'mathematics_sha256':expected['mathematics_sha256'],
            'seconds':round(time.monotonic()-start,3),
            'max_child_rss_kib':max(j['max_rss_kib'] for j in jobs),
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
