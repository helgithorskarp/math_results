"""Fresh serial unmodified native replay, with whole target source byte gates."""
import sys,json,argparse,hashlib,subprocess,time,os,resource,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--target-directory',type=Path,default=P.parent.parent/'six-downset-3/core-edge-five-cutoff');parser.add_argument('--receipt',type=Path);args=parser.parse_args();folder=args.target_directory.resolve()
 data=json.loads((P/'TARGET_ACCESS.json').read_text())
 for name,pin in data['whole_files'].items():
  raw=(folder/Path(name).name).read_bytes()
  if len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('entire target byte gate '+name)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**{x:'1' for x in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']});env.pop('PYTHONPATH',None)
 runs=[]
 with tempfile.TemporaryDirectory() as td:
  for mode,flags in [('normal',[]),('optimized',['-O']),('fresh_full_validator',[])]:
   start=time.monotonic();cmd=[sys.executable,'-B',*flags,str(folder/('validate.py' if mode=='fresh_full_validator' else 'verify.py'))]
   if mode=='fresh_full_validator':cmd+=['--receipt',str(Path(td)/'native-receipt.json')]
   r=subprocess.run(cmd,cwd=folder,env=env,capture_output=True,text=True,timeout=45)
   if r.returncode:raise ValueError(r.stderr+r.stdout)
   summary=json.loads(r.stdout);runs.append({'mode':mode,'seconds':round(time.monotonic()-start,6),'summary':summary})
 result={'unmodified_source':True,'runs':runs,'target_complete_record_sha256':runs[0]['summary']['record_sha256'],'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'guard_seconds':45,'native_threads':1,'serial_math_children':True,'scope':'unchanged1CPU2GiB','ordinary_bridges_not_formalized':True,'whole_source_checked_before_import':True}
 if args.receipt:
  if args.receipt.exists():raise ValueError('refuse to overwrite replay receipt')
  args.receipt.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'complete_record_sha256':result['target_complete_record_sha256'],'native_runs':len(runs),'peak_child_rss_kib':result['peak_child_rss_kib'],'whole_source_checked_before_import':True}))
if __name__=='__main__':main()
