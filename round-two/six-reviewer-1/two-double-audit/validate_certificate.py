"""Full local/cold normal/optimized supplementary mathematical-input replay."""
from pathlib import Path
import datetime,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time

def run():
    here=Path(__file__).resolve().parent
    primary=json.loads((here/'PRIMARY_SEAL.json').read_text())['primary_files']
    supplement=json.loads((here/'CERTIFICATE_SEAL.json').read_text())['supplementary_files']
    for n,v in dict(primary,**supplement).items():
        b=(here/n).read_bytes()
        if len(b)!=v['bytes']or hashlib.sha256(b).hexdigest()!=v['sha256']:raise ValueError('whole unchanged source seal '+n)
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[name]='1'
    bootstrap='import runpy,sys;from pathlib import Path;p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p.parent));sys.argv=[str(p)]+sys.argv[2:];runpy.run_path(str(p),run_name="__main__")'
    rows=[];outputs=[]
    scratch=Path('scratch');scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='two-double-certificate-validation-',dir=scratch)as temp:
        temp=Path(temp);cold=temp/'cold';cold.mkdir()
        for n in dict(primary,**supplement):shutil.copyfile(here/n,cold/n)
        for root in [here,cold]:
            for opt in [False,True]:
                dest=temp/('record-'+str(len(rows))+'.json');start=time.monotonic()
                r=subprocess.run([sys.executable,'-I','-B']+(['-O']if opt else[])+['-c',bootstrap,str(root/'certificate.py'),'--record',str(dest)],capture_output=True,timeout=45,env=env)
                if r.returncode or r.stderr:raise ValueError('certificate replay failure '+r.stderr.decode())
                data=dest.read_bytes();parsed=json.loads(data)
                if not parsed['all16_meaningful_damages_rejected']:raise ValueError('incomplete negative controls')
                outputs.append(data);rows.append({'source':'local'if root==here else'cold','optimized':opt,'seconds':round(time.monotonic()-start,6),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    if any(data!=outputs[0]or json.loads(data)!=json.loads(outputs[0])for data in outputs):raise ValueError('whole supplementary mode discrepancy')
    for n,v in dict(primary,**supplement).items():
        if hashlib.sha256((here/n).read_bytes()).hexdigest()!=v['sha256']:raise ValueError('source changed during supplementary validation')
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'agent':'six-reviewer-1','role':'independent mathematical reviewer','all5_primary_and3_supplementary_seals_unchanged':True,'all_four_whole_records_equal':True,'whole_record_bytes':len(outputs[0]),'whole_record_sha256':hashlib.sha256(outputs[0]).hexdigest(),'mathematical_rejections_each':16,'runs':rows,'native_threads':1,'serial_children':True,'fixed_child_seconds':45,'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
