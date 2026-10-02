#!/usr/bin/env python3
"""Serial exact checks, fixed60-second owned-child guards, native threads1."""
from pathlib import Path
import argparse,hashlib,json,os,resource,signal,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
def child(args):
 env=dict(os.environ);env.update({k:'1' for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1'
 start=time.monotonic();p=subprocess.Popen(list(map(str,args)),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 try:out,err=p.communicate(timeout=60)
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGKILL);p.communicate();raise RuntimeError('INCOMPLETE: fixed60-second child guard')
 if p.returncode:raise RuntimeError('INCOMPLETE child failed: '+err.decode())
 return out,{'seconds':round(time.monotonic()-start,6),'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'stderr':err.decode()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--author-source',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 mode=['-O'] if sys.flags.optimize else [];records={};runs={}
 for name,expected in (('core','RESULTS.json'),('strengthening','STRENGTHENING.json'),('controls','CONTROLS.json')):
  data,runs[name]=child([sys.executable,*mode,ROOT/(name+'.py')]);(a.out/(name+'.json')).write_bytes(data)
  if data!=(ROOT/expected).read_bytes():raise RuntimeError('Whole independent '+name+' record differs')
  records[name]=json.loads(data)
 if a.author_source:
  manifest=json.loads((ROOT/'AUTHOR_SOURCE.json').read_text())
  for f in manifest['files']:
   raw=(a.author_source/Path(f['path']).name).read_bytes()
   if len(raw)!=f['bytes'] or hashlib.sha256(raw).hexdigest()!=f['sha256']:raise RuntimeError('Author source byte manifest mismatch')
  work=a.out.resolve()/'author'
  data,runs['author']=child([sys.executable,*mode,a.author_source.resolve()/'reproduce.py','--work',work,'--worker'])
  (a.out/'author-receipt.json').write_bytes(data)
  need_expected=(a.author_source/'EXPECTED.json').read_bytes()
  if (work/'MATHEMATICAL.json').read_bytes()!=need_expected:raise RuntimeError('Whole author frozen record differs')
  data,runs['compare']=child([sys.executable,*mode,ROOT/'compare.py','--author-work',work])
  if data!=(ROOT/'COMPARISON.json').read_bytes():raise RuntimeError('Whole post-seal comparison record differs')
  (a.out/'comparison.json').write_bytes(data);records['comparison']=json.loads(data)
 combined=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(a.out/'mathematics.json').write_bytes(combined)
 result={'complete':True,'python_version':sys.version.split()[0],'python_optimized':bool(sys.flags.optimize),'guard_seconds':60,'native_threads':1,'one_mathematical_child_at_a_time':True,'mathematics_bytes':len(combined),'mathematics_sha256':hashlib.sha256(combined).hexdigest(),'runs':runs}
 (a.out/'run.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
