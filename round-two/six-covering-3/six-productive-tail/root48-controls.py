"""Eight semantic domain/trace damages; each checker child has the same20s guard."""
from pathlib import Path
from hashlib import sha256
import argparse,json,os,resource,shutil,struct,subprocess,sys,time

p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--optimized',action='store_true')
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
cases=[('missing_group','Generator closure not complete Cartesian stabilizer'),
       ('physical_first','Physical point map differs'),
       ('phase_last','Original phase-stream field differs'),
       ('missing_orbit','Wrong original orbit inventory'),
       ('duplicate_orbit','Orbit overlap/representative ambiguity'),
       ('parity_pooled','Full raw orbit fields differ'),
       ('retained_omission','Normalized target frontier differs'),
       ('other_P14','Original physical domain differs')]
env=os.environ.copy()
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
records=[]
for name,reason in cases:
    target=a.out/name;shutil.copytree(a.data,target,dirs_exist_ok=False)
    result=json.loads((target/'result.json').read_text())
    if name=='missing_group':
        path=target/'coordinate-group.bin';path.write_bytes(path.read_bytes()[:-14])
    elif name=='physical_first':
        path=target/'physical-generators.bin';raw=bytearray(path.read_bytes());struct.pack_into('<H',raw,0,1);path.write_bytes(raw)
    elif name=='phase_last':
        path=target/'original-phase-maps.bin';raw=bytearray(path.read_bytes());v=struct.unpack_from('<H',raw,len(raw)-2)[0];struct.pack_into('<H',raw,len(raw)-2,(v+1)%10080);path.write_bytes(raw)
    elif name=='missing_orbit':result['complete_orbits'].pop()
    elif name=='duplicate_orbit':result['complete_orbits'][-1]=result['complete_orbits'][0]
    elif name=='parity_pooled':
        row=next(x for x in result['complete_orbits'] if x['representative']==[0,3]);row['members'][-1]=[0,12]
    elif name=='retained_omission':result['retained_representatives_cutoff1237'].pop()
    elif name=='other_P14':result['literal_P'][3]=[14,0]
    (target/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    command=[sys.executable,*(['-O'] if a.optimized else []),'-B','scratch/root48-check.py','--data',str(target)]
    start=time.monotonic()
    try:r=subprocess.run(command,capture_output=True,text=True,env=env,timeout=20)
    except subprocess.TimeoutExpired:
        raise RuntimeError('Control timeout, no verdict; do not increase limits')
    if r.returncode==0 or reason not in r.stderr:raise ValueError('Damage failed to reject for intended reason: '+name+'; '+r.stderr)
    record={'damage':name,'expected_reason':reason,'exit':r.returncode,'intended_reason_present':True,'seconds':time.monotonic()-start}
    records.append(record);print(json.dumps(record),flush=True)
summary={'agent':'six-covering-3','role':'researcher','mode':'optimized' if a.optimized else 'normal',
         'damages':records,'all_intended_reason_rejections':True,'guard_seconds_per_child':20,'threads':1,'one_CPU_child':True,
         'RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'universal_BASE162_claimed':False}
(a.out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='damages'},indent=2))
