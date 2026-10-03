"""Cold source-only normal/O whole-byte replay, serial children, 45s guard.

Outputs are written only to the explicitly supplied scratch directory.
No native target executable, solver, network, or earlier kernel is needed.
"""
from pathlib import Path
import os,sys,json,subprocess,time,hashlib,resource,shutil,argparse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--scratch',type=Path,required=True)
    args=parser.parse_args();dest=args.scratch.resolve();dest.mkdir(parents=True,exist_ok=True)
    source=Path(__file__).resolve().parent
    seal=json.loads((source/'PRIMARY_SEAL.json').read_text())
    for name,wanted in seal['files'].items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=wanted:
            raise ValueError('primary source seal '+name)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    receipts=[]
    for mode in ('primary','profile-0','profile-1','profile-2','profile-3'):
        streams=[]
        for optimize in (False,True):
            record=dest/(mode+('-O'if optimize else '-normal')+'.json')
            command=[sys.executable,'-I','-B']+(['-O']if optimize else [])+[str(source/'check.py')]
            if mode!='primary':command+=['--profile',mode.split('-')[-1]]
            command+=['--record',str(record)]
            start=time.monotonic()
            p=subprocess.run(command,capture_output=True,text=True,env=env,timeout=45,cwd=dest)
            if p.returncode:raise ValueError('audit child '+mode+'\n'+p.stderr)
            receipt=json.loads(p.stdout);receipt.update(optimized=optimize,
                elapsed_seconds=round(time.monotonic()-start,6),
                peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            receipts.append(receipt);streams.append(record.read_bytes())
            print(json.dumps({'completed':mode,'optimized':optimize,'seconds':receipt['elapsed_seconds']}),flush=True)
        if streams[0]!=streams[1]:raise ValueError('whole normal/O record bytes '+mode)
    # Only this compact audit source, without campaign files, in a cold directory.
    cold=dest/'cold-source';cold.mkdir(exist_ok=True)
    for name in list(seal['files'])+['PRIMARY_SEAL.json','expected.json']:
        shutil.copy2(source/name,cold/name)
    record=dest/'primary-cold.json';start=time.monotonic()
    p=subprocess.run([sys.executable,'-I','-B',str(cold/'check.py'),'--record',str(record)],
                     capture_output=True,text=True,env=env,timeout=45,cwd=dest)
    if p.returncode:raise ValueError('cold primary\n'+p.stderr)
    if record.read_bytes()!=(dest/'primary-normal.json').read_bytes():raise ValueError('cold whole primary bytes')
    receipts.append(dict(json.loads(p.stdout),cold=True,elapsed_seconds=round(time.monotonic()-start,6),
                         peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
    # External fixture damage; no mathematical check is skipped to run these.
    fixture=json.loads((source/'expected.json').read_text());damage=[]
    variants=[('absent',None),('malformed','{'),('wrong-hash','hash'),('missing-mode','mode')]
    for label,value in variants:
        f=dest/('damaged-'+label+'.json')
        if value is None:
            if f.exists():f.unlink()
        elif value=='{':f.write_text(value)
        else:
            altered=json.loads(json.dumps(fixture))
            if value=='hash':altered['modes']['primary']['record_sha256']='0'*64
            else:del altered['modes']['primary']
            f.write_text(json.dumps(altered))
        for optimize in (False,True):
            cmd=[sys.executable,'-I','-B']+(['-O']if optimize else [])+[str(source/'check.py'),'--expected',str(f)]
            start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45,cwd=dest)
            if p.returncode==0:raise ValueError('external fixture damage survived '+label)
            damage.append({'damage':label,'optimized':optimize,'exit':p.returncode,
                           'seconds':round(time.monotonic()-start,6)})
            print(json.dumps({'rejected_fixture':label,'optimized':optimize}),flush=True)
    out={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
         'native_threads':1,'serial_children':True,'unchanged_child_guard_seconds':45,
         'whole_normal_O_and_cold_comparison':True,'positive_children':receipts,'external_damages':damage,
         'all_primary_source_seals_match':True,'no_native_target_or_earlier_executable_import':True}
    (dest/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'validation':str(dest/'validation.json'),'positive_children':len(receipts),
                      'fixture_damages_rejected':len(damage)}),flush=True)


if __name__=='__main__':main()
