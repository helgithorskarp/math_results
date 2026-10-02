"""Portable late comparison: all7 complete records, separate from primary."""
import argparse,pathlib,subprocess,sys,os,json,hashlib,time
ROOT=pathlib.Path(__file__).resolve().parent
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native-dir',type=pathlib.Path,required=True);p.add_argument('--check',type=pathlib.Path,default=ROOT/'COMPARISON.json');a=p.parse_args();env=dict(os.environ)
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 modes=[['symbolic']]+[['original','--n',str(n),'--l',str(l)]for n,l in [(3,2),(4,2),(4,3),(5,4),(6,2),(6,5)]];rows=[]
 for mode in modes:
  start=time.monotonic();r=subprocess.run([sys.executable,'-B']+(['-O']if sys.flags.optimize else [])+[str(ROOT/'corroborate.py'),'--native-dir',str(a.native_dir),*mode],capture_output=True,timeout=55,env=env)
  if r.returncode:sys.stderr.buffer.write(r.stderr);raise RuntimeError('late common phase failed '+repr(mode))
  rows.append(json.loads(r.stdout));print(repr(mode)+' '+format(time.monotonic()-start,'.3f')+'s',file=sys.stderr,flush=True)
 raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()+b'\n'
 if raw!=a.check.read_bytes():raise ValueError('WHOLE7 complete common records differ')
 print(json.dumps({'entire_common_match':True,'whole_common_bytes':len(raw),'whole_common_sha256':hashlib.sha256(raw).hexdigest(),'phases':len(rows)},sort_keys=True))
