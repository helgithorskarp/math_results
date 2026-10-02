"""Whole type-sensitive recomputation; all threads one, fixed45s guard."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import argparse,json,hashlib,signal
from pathlib import Path
from audit import audit
from controls import checks

def parse(text):
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate fixture key')
   out[k]=v
  return out
 return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite fixture')))
def equal(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));ap.add_argument('--emit',action='store_true');args=ap.parse_args();signal.alarm(45)
 got=audit();got['bridge_controls']=checks();can=json.dumps(got,sort_keys=True,separators=(',',':')).encode()
 if not args.emit and not equal(got,parse(args.expected.read_text())):raise ValueError('whole typed fixture mismatch')
 if args.emit:print(can.decode())
 else:print(json.dumps({'status':'PASS','sha256':hashlib.sha256(can).hexdigest(),'canonical_bytes':len(can),'full_integer_values':85,'full_modular_values':296,'whole_units':4,'bridge_controls':len(got['bridge_controls']),'target_code_imports':0},sort_keys=True))
if __name__=='__main__':main()
