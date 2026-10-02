#!/usr/bin/env python3
"""Optional whole author corroboration, isolated from the independent verifier."""
import json,os,subprocess,sys,tempfile,time,hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fetch_inputs import restore
HERE=Path(__file__).resolve().parent

def same(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def main():
 manifest=json.loads((HERE/'AUTHOR_INPUTS.json').read_text());rows=manifest['files']
 if len(rows)!=83 or len({r['path'] for r in rows})!=83:raise ValueError('complete83 source/input files required')
 env=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 (HERE/'.generated').mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(dir=HERE/'.generated') as tmp:
  root=Path(tmp)/'repo'
  # Network-only restoration can overlap; the mathematical children are serial.
  with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda row:restore(root,row),rows))
  target=root/'round-two/six-sendov-3/moment-entry';expected=json.loads((target/'expected.json').read_text())
  for label,flags in [('normal',[]),('optimized',['-O'])]:
   out=Path(tmp)/(label+'.json');start=time.monotonic()
   r=subprocess.run([sys.executable,'-I','-B',*flags,str(target/'verify.py'),'--freeze','--fixture',str(out)],env=env,capture_output=True,text=True,timeout=45)
   if r.returncode:raise ValueError('author child '+r.stdout+r.stderr)
   actual=json.loads(out.read_text());digest=hashlib.sha256(json.dumps(actual,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   if not same(actual,expected) or digest!=manifest['whole_original_record_sha256']:raise ValueError('complete typed original fixture differs')
   print('PASS author corroboration',label,digest,'seconds',round(time.monotonic()-start,3),flush=True)
if __name__=='__main__':main()
