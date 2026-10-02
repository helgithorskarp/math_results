"""Serial source-only cold normal/-O audit and three whole-record controls."""
import argparse,hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args();base=Path(__file__).resolve().parent
    args.work.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    seals=json.loads((base/'INDEPENDENCE.json').read_text())['files']
    for n,pin in seals.items():
        need(hashlib.sha256((base/n).read_bytes()).hexdigest()==pin['sha256'],'initial source seal '+n)
    receipts=[]
    for opt in (False,True):
        with tempfile.TemporaryDirectory(dir=args.work,prefix='source-only-')as work:
            p=Path(work)
            for n in seals:shutil.copyfile(base/n,p/n)
            cmd=['python3']+(['-O']if opt else[])+['audit.py','--output','fresh.json','--check','RESULTS.json']
            start=time.monotonic();r=subprocess.run(cmd,cwd=p,env=env,capture_output=True,text=True,timeout=60)
            need(r.returncode==0,r.stdout+r.stderr)
            need((p/'fresh.json').read_bytes()==(base/'RESULTS.json').read_bytes(),'whole source-only output')
            for damage in ('cover_rows','scalar_shapes','terminal_scans'):
                obj=json.loads((p/'RESULTS.json').read_text())
                if damage=='terminal_scans':obj[damage][0]['degree_SY0']=9
                else:obj[damage]=obj[damage][1:]
                (p/'damaged.json').write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
                d=subprocess.run(cmd[:-1]+['damaged.json'],cwd=p,env=env,capture_output=True,text=True,timeout=60)
                need(d.returncode!=0 and 'entire mathematical record mismatch' in d.stderr,'damage rejection '+damage)
            receipts.append({'mode':'optimized'if opt else'normal','seconds':time.monotonic()-start,'all_three_record_damages_rejected':True,'complete_record_sha256':hashlib.sha256((p/'fresh.json').read_bytes()).hexdigest()})
    (args.work/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print(json.dumps({'status':'PASS','source_only':True,'whole_record_bytes':(base/'RESULTS.json').stat().st_size,'modes':receipts},sort_keys=True))
if __name__=='__main__':main()
