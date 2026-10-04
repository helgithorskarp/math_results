"""Serial fixed45s local/cold normal/optimized complete-record validation."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time

def run(cas_lib,scratch):
    here=Path(__file__).resolve().parent;seal=json.loads((here/'PRIMARY_SEAL.json').read_text())
    for name,pin in seal['primary_files'].items():
        data=(here/name).read_bytes()
        if len(data)!=pin['bytes']or hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('whole primary seal '+name)
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[name]='1'
    bootstrap='import runpy,sys;from pathlib import Path;p=Path(sys.argv[1]).resolve();lib=sys.argv[2];sys.path.insert(0,str(p.parent));sys.path.insert(0,lib)if lib else None;sys.argv=[str(p)]+sys.argv[3:];runpy.run_path(str(p),run_name="__main__")'
    rows=[];records={};scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='two-double-independent-',dir=scratch)as temp:
        temp=Path(temp);cold=temp/'cold';cold.mkdir()
        for name in seal['primary_files']:shutil.copyfile(here/name,cold/name)
        def child(root,name,opt,damage=None):
            dest=temp/('record-'+str(len(rows))+'.json');args=['--record',str(dest)]
            if damage:args+=['--damage',damage]
            command=[sys.executable,'-I','-B']+(['-O']if opt else[])+['-c',bootstrap,str(root/name),str(cas_lib.resolve())if cas_lib and name=='derive.py'else'',*args]
            start=time.monotonic();p=subprocess.run(command,capture_output=True,env=env,timeout=45)
            if damage:
                if p.returncode==0 or b'ValueError:'not in p.stderr:raise ValueError('defect accepted or unrelated failure '+damage)
                data=b''
            else:
                if p.returncode or p.stderr:raise ValueError('positive child '+name+': '+p.stderr.decode())
                data=dest.read_bytes();json.loads(data)
            rows.append({'script':name,'source':'local'if root==here else'cold','optimized':opt,'mathematical_defect':damage,'exit':p.returncode,'seconds':round(time.monotonic()-start,6),'record_bytes':len(data),'record_sha256':hashlib.sha256(data).hexdigest(),'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
            return data
        for name in ['derive.py','check.py','literal.py']:
            outputs=[child(root,name,opt)for root in [here,cold]for opt in [False,True]]
            if any(data!=outputs[0]or json.loads(data)!=json.loads(outputs[0])for data in outputs):raise ValueError('whole isolated record disagreement '+name)
            records[name]={'bytes':len(outputs[0]),'sha256':hashlib.sha256(outputs[0]).hexdigest(),'all_four_whole_records_equal':True}
            if name=='derive.py':
                if json.loads(outputs[0])!=json.loads((here/'POLYNOMIALS.json').read_text()):raise ValueError('whole fresh CAS polynomial record differs from own fixture')
        for k,damage in enumerate(['lost-mass-factor','lost-terminal-num','lost-tensor-coefficient']):child(here,'check.py',bool(k%2),damage)
        for k,damage in enumerate(['lost-critical-slot','lost-mass-factor','lost-angular-normalization']):child(here,'literal.py',bool(k%2),damage)
    for name,pin in seal['primary_files'].items():
        if hashlib.sha256((here/name).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('primary bytes changed during validation')
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'agent':'six-reviewer-1','role':'independent mathematical reviewer','python':sys.version.split()[0],'all5_primary_files_unchanged':True,'positive_children':12,'mathematical_rejections':6,'records':records,'runs':rows,'native_threads':1,'serial_children':True,'fixed_child_seconds':45,'total_child_seconds':round(sum(r['seconds']for r in rows),6),'max_child_seconds':max(r['seconds']for r in rows),'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--cas-lib',type=Path);cli.add_argument('--scratch',type=Path,default=Path('scratch'));args=cli.parse_args()
    print(json.dumps(run(args.cas_lib,args.scratch),sort_keys=True,indent=2))
