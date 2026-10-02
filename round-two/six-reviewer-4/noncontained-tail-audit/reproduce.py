#!/usr/bin/env python3
"""One exact mathematical child at a time, fixed60s guard, native1."""
from pathlib import Path
import argparse,json,hashlib,os,resource,signal,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
def child(args):
 env=dict(os.environ);env.update({k:'1'for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')});env['PYTHONDONTWRITEBYTECODE']='1';t=time.monotonic()
 p=subprocess.Popen(list(map(str,args)),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 try:out,err=p.communicate(timeout=60)
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGKILL);p.communicate();raise RuntimeError('INCOMPLETE fixed60s child guard')
 if p.returncode:raise RuntimeError('INCOMPLETE failed child: '+err.decode())
 return out,{'seconds':round(time.monotonic()-t,6),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True);records={};runs={};mode=['-O']if sys.flags.optimize else []
 for name in ('core','graph','transport'):
  raw,runs[name]=child([sys.executable,*mode,ROOT/(name+'.py'),'--work',a.work.resolve()]);(a.work/(name+'-record.json')).write_bytes(raw);records[name]=json.loads(raw)
 raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(a.work/'MATHEMATICS.json').write_bytes(raw)
 expected=ROOT/'RESULTS.json'
 if expected.exists()and raw!=expected.read_bytes():raise RuntimeError('Entire frozen mathematical record differs')
 report={'complete':True,'python':sys.version.split()[0],'optimized':bool(sys.flags.optimize),'guard_seconds':60,'native_threads':1,'math_bytes':len(raw),'math_sha256':hashlib.sha256(raw).hexdigest(),'runs':runs};(a.work/'run.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
