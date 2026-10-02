#!/usr/bin/env python3
"""One mathematical child at a time, native1, fixed20s guard."""
from pathlib import Path
import argparse,os,json,subprocess,sys,time,resource,hashlib,signal
ROOT=Path(__file__).resolve().parent

def child(args):
 env=dict(os.environ);env.update({k:'1'for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')});env['PYTHONDONTWRITEBYTECODE']='1';t=time.monotonic()
 p=subprocess.Popen(list(map(str,args)),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 try:out,err=p.communicate(timeout=20)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.communicate();raise RuntimeError('INCOMPLETE fixed20s child guard; no exclusion')
 if p.returncode:raise RuntimeError('INCOMPLETE child failure: '+err.decode())
 return out,{'seconds':round(time.monotonic()-t,6),'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
 if a.work.exists():raise RuntimeError('fresh work directory required')
 a.work.mkdir(parents=True);flags=['-O','-B']if sys.flags.optimize else ['-B'];records={};runs={}
 for name in ['algebra','full','physical']:
  raw,runs[name]=child([sys.executable,*flags,ROOT/(name+'.py'),'--work',a.work.resolve()]);records[name]=json.loads(raw);(a.work/(name+'-record.json')).write_bytes(raw)
 raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(a.work/'MATHEMATICS.json').write_bytes(raw)
 if (ROOT/'RESULTS.json').exists()and raw!=(ROOT/'RESULTS.json').read_bytes():raise RuntimeError('whole frozen mathematical record differs')
 report={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','complete':True,'python':sys.version.split()[0],'optimized':bool(sys.flags.optimize),'native_threads':1,'serial_mathematical_children':1,'fixed_child_guard_seconds':20,'whole_math_bytes':len(raw),'whole_math_sha256':hashlib.sha256(raw).hexdigest(),'runs':runs};(a.work/'run.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
