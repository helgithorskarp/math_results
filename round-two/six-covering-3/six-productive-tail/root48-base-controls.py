"""Damaged normalized branch-domain/threshold records; each AP child guarded20s."""
from pathlib import Path
import argparse,json,os,resource,shutil,struct,subprocess,sys,time

p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--optimized',action='store_true')
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
cases=[('early_cutoff','Every-stage coverage cutoff differs'),
       ('preceding_omission','Preceding qualifying tuple domain omitted/duplicated/reordered'),
       ('preceding_duplicate','Preceding qualifying tuple domain omitted/duplicated/reordered'),
       ('first_extension_phase','Complete physical original row differs'),
       ('last_extension_upper','Complete physical original row differs'),
       ('truncated_final','Incomplete/extra original phase stream'),
       ('canonical_root_omission','Complete normalized root domain/fields differ')]
env=os.environ.copy()
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[name]='1'
records=[]
for name,reason in cases:
    dest=a.out/name;shutil.copytree(a.data,dest,dirs_exist_ok=False)
    result=json.loads((dest/'result.json').read_text());last=result['stages'][-1]['fixed_originals'][-1]
    if name=='early_cutoff':result['stages'][1]['target']=1272
    elif name=='preceding_omission':result['stages'][1]['previous_tuples'].pop()
    elif name=='preceding_duplicate':result['stages'][1]['previous_tuples'].append(result['stages'][1]['previous_tuples'][-1])
    elif name=='first_extension_phase':
        n=result['stages'][1]['fixed_originals'][-1];path=dest/('stage'+str(n)+'.bin');raw=bytearray(path.read_bytes())
        pos=2*(len(result['stages'][1]['fixed_originals'])-1);struct.pack_into('<H',raw,pos,1);path.write_bytes(raw)
    elif name=='last_extension_upper':
        path=dest/('stage'+str(last)+'.bin');raw=bytearray(path.read_bytes());v=struct.unpack_from('<H',raw,len(raw)-2)[0]
        struct.pack_into('<H',raw,len(raw)-2,v-1);path.write_bytes(raw)
    elif name=='truncated_final':
        path=dest/('stage'+str(last)+'.bin');path.write_bytes(path.read_bytes()[:-76])
    elif name=='canonical_root_omission':
        path=dest/'root.bin';path.write_bytes(path.read_bytes()[:-76])
    (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    command=[sys.executable,*(['-O'] if a.optimized else []),'-B','scratch/root48-base-check.py','--data',str(dest)]
    start=time.monotonic()
    try:r=subprocess.run(command,capture_output=True,text=True,env=env,timeout=20)
    except subprocess.TimeoutExpired:raise RuntimeError('Semantic control timeout: no verdict/no limit increase')
    if r.returncode==0 or reason not in r.stderr:raise ValueError('Damage did not reject for intended reason: '+name+' '+r.stderr)
    record={'damage':name,'expected_reason':reason,'exit':r.returncode,'intended_reason_present':True,'seconds':time.monotonic()-start}
    records.append(record);print(json.dumps(record),flush=True)
result={'agent':'six-covering-3','role':'researcher','mode':'optimized' if a.optimized else 'normal','damages':records,
        'all_intended_reason_rejections':True,'guard_seconds_per_child':20,'threads':1,'one_CPU_child':True,
        'RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='damages'},indent=2))
