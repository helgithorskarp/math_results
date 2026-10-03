"""Fresh complete serial normal/O proof replay; bulky generated packs stay private."""
import argparse,datetime,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
def require(test,reason):
    if not test:raise ValueError(reason)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);require(not out.exists(),'output must be new');out.mkdir(parents=True)
    env=os.environ.copy();env.update({k:'1' for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1'
    modes=[];journal=[];start=time.monotonic()
    for mode in ('normal','O'):
        dest=out/mode;dest.mkdir();records=[];counter=0
        def run(script,arguments):
            nonlocal counter
            counter+=1;t=time.monotonic();cmd=[sys.executable]+(['-O'] if mode=='O' else [])+[str(HERE/script),*map(str,arguments)]
            try:r=subprocess.run(cmd,env=env,capture_output=True,timeout=30)
            except subprocess.TimeoutExpired as e:
                (dest/f'{counter}-timeout.txt').write_text(str(e));raise RuntimeError('INCOMPLETE child timeout; no absence inference')
            (dest/f'{counter}-stdout.txt').write_bytes(r.stdout);(dest/f'{counter}-stderr.txt').write_bytes(r.stderr)
            require(r.returncode==0,f'child failed {script} {r.returncode}; preserve output')
            record=json.loads(r.stdout);records.append(record)
            journal.append({'mode':mode,'script':script,'seconds':time.monotonic()-t,'command':cmd})
            print(f'{mode} {counter}: {script} complete',flush=True)
            return record
        packs=[]
        for lo in range(1,103,8):
            hi=min(103,lo+8);path=dest/f'pack-{lo}-{hi}.csv';packs.append(path)
            run('generate.py',['--lo',lo,'--hi',hi,'--output',path])
            run('check.py',['--lo',lo,'--hi',hi,'--input',path])
        for lo in range(0,103,13):run('basis.py',['--lo',lo,'--hi',min(103,lo+13)])
        run('controls.py',['--input',packs[0]])
        whole=b''.join(p.read_bytes() for p in packs)
        (dest/'whole-packs.csv').write_bytes(whole)
        modes.append({'records':records,'whole_pack_bytes':len(whole),'whole_pack_sha256':hashlib.sha256(whole).hexdigest()})
        if mode=='normal':normal=whole
        else:require(whole==normal,'WHOLE normal/O positive corpus mismatch')
    require(modes[0]==modes[1],'WHOLE normal/O mathematical records mismatch')
    result={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','q':103,'max_oriented_ordinal_step':50,'positive_cases':102*128,'positive_aps':102*128*5,'positive_points':102*128*35,'actual_phase6_integer_aps':102*128*30,'actual_phase6_integer_points':102*128*210,'original_affine_configurations':103*102,'original_character_entries':103*102*99*3,'original_kernel_aps':103*102*4,'column_interval_coefficient':402,'all_phase_interval_coefficient':403,**modes[0]}
    raw=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode();(out/'RESULT.json').write_bytes(raw)
    expected=HERE/'EXPECTED.json'
    if expected.exists():require(raw==expected.read_bytes(),'WHOLE expected result mismatch')
    receipt={'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'child_guard_seconds':30,'serial_children':len(journal),'whole_mode_pairs':len(modes[0]['records']),'wall_seconds':time.monotonic()-start,'max_child_seconds':max(j['seconds'] for j in journal),'result_sha256':hashlib.sha256(raw).hexdigest(),'result_bytes':len(raw),'normal_O_whole_equal':True,'numerical_threads':1,'children':journal}
    (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='children'},sort_keys=True),flush=True)
if __name__=='__main__':main()
