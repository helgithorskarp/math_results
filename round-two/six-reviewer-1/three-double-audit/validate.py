"""Fixed45s serial/cold/O exact matrix and literal verification."""
import datetime, hashlib, json, os, resource, shutil, subprocess, sys, tempfile, time
from pathlib import Path


def run():
    here=Path(__file__).resolve().parent;seal=json.loads((here/'PRIMARY_SEAL.json').read_text())
    for n,row in seal['primary_files'].items():
        b=(here/n).read_bytes()
        if hashlib.sha256(b).hexdigest()!=row['sha256']or len(b)!=row['bytes']:raise ValueError('whole primary seal '+n)
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[n]='1'
    rows=[];records={}
    bootstrap='import runpy,sys;from pathlib import Path;p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p.parent));sys.argv=[str(p)]+sys.argv[2:];runpy.run_path(str(p),run_name="__main__")'
    with tempfile.TemporaryDirectory(prefix='three-double-independent-')as temp:
        temp=Path(temp);cold=temp/'cold';cold.mkdir()
        for n in seal['primary_files']:shutil.copyfile(here/n,cold/n)
        def child(root,script,opt,extra=(),negative=False,label=None):
            dest=temp/('record-'+str(len(rows))+'.json')
            args=['--record',str(dest)]if script=='check.py'and not negative else[]
            t=time.monotonic();p=subprocess.run([sys.executable,'-I','-B']+(['-O']if opt else[])+['-c',bootstrap,str(root/script),*args,*extra],capture_output=True,env=env,timeout=45)
            if negative:
                if p.returncode==0 or b'ValueError:'not in p.stderr:raise ValueError('defect accepted or unrecognized '+str(label))
                data=b''
            else:
                if p.returncode or p.stderr:raise ValueError('positive child failure '+p.stderr.decode())
                data=dest.read_bytes()if script=='check.py'else p.stdout;json.loads(data)
            rows.append({'script':script,'source':'local'if root==here else'cold','optimized':opt,'negative':negative,'label':label,'exit':p.returncode,'seconds':round(time.monotonic()-t,6),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
            return data
        for script in ['check.py','literal.py']:
            outputs=[child(root,script,opt)for root in [here,cold]for opt in [False,True]]
            if any(x!=outputs[0]or json.loads(x)!=json.loads(outputs[0])for x in outputs):raise ValueError('full normal/O/cold disagreement '+script)
            records[script]={'bytes':len(outputs[0]),'sha256':hashlib.sha256(outputs[0]).hexdigest(),'whole_bytes_and_parse_equal_in_four_modes':True}
        for i,label in enumerate(['lost-mass-factor','lost-terminal-num','wrong-rigidity-constant']):
            child(here,'check.py',bool(i%2),['--damage',label],True,label)
        for i,label in enumerate(['lost-critical-slot','lost-mass-factor','lost-angular-normalization']):
            child(here,'literal.py',bool(i%2),['--damage',label],True,label)
    for n,row in seal['primary_files'].items():
        if hashlib.sha256((here/n).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('primary bytes changed during verification')
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'agent':'six-reviewer-1','role':'independent mathematical reviewer','python':sys.version.split()[0],'primary_files':len(seal['primary_files']),'all_primary_files_unchanged':True,'records':records,'runs':rows,'positive_children':8,'generic_method_rejections':3,'literal_method_rejections':3,'native_threads':1,'serial_children':True,'fixed_per_child_seconds':45,'total_child_seconds':round(sum(r['seconds']for r in rows),6),'max_child_seconds':max(r['seconds']for r in rows),'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
