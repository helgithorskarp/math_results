"""Whole independent record, exact typed comparison, fixed45s guard."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import json,hashlib,argparse,signal
from pathlib import Path
from audit import audit
from controls import checks
def parse(s):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate expected key')
   d[k]=v
  return d
 return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda z:(_ for _ in ()).throw(ValueError('nonfinite expected value')))
def equal(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
def main():
 p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');p.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));a=p.parse_args();signal.alarm(45)
 d=audit();d['boundary_controls']=checks();raw=json.dumps(d,sort_keys=True,separators=(',',':')).encode()
 if a.emit:print(raw.decode());return
 if not equal(d,parse(a.expected.read_text())):raise ValueError('whole typed independent fixture mismatch')
 print(json.dumps({'status':'PASS','sha256':hashlib.sha256(raw).hexdigest(),'canonical_bytes':len(raw),'whole_new_identities':len(d['whole_checks']),'whole_symmetric_gaussian_values':sum(len(x['nodes']) for x in d['resultants']),'prime':263,'boundary_controls':len(d['boundary_controls']),'producer_code_imports':0},sort_keys=True))
if __name__=='__main__':main()
