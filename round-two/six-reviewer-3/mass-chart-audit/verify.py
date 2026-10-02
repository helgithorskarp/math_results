"""Recompute the whole independent audit; reject malformed or altered evidence."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
import argparse,hashlib,json,signal,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from algebra import audit as algebra_audit
from controls import audit as controls_audit

def parse(text):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('duplicate JSON key')
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON constant')))

def typed_equal(a,b):
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def build():return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','algebra':algebra_audit(),'controls':controls_audit()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));ap.add_argument('--emit',action='store_true');args=ap.parse_args()
    if hasattr(signal,'alarm'):signal.alarm(45)
    got=build();canonical=json.dumps(got,sort_keys=True,separators=(',',':')).encode()
    if not typed_equal(got,parse(args.expected.read_text())):raise ValueError('entire typed independent fixture mismatch')
    if args.emit:sys.stdout.buffer.write(canonical+b'\n')
    else:print('PASS independent real stationary-chart audit '+hashlib.sha256(canonical).hexdigest());print(json.dumps({'whole_universal_identities':len(got['algebra']['checks']),'actual_moving_derivatives':got['controls']['actual_derivative_count'],'math_damage_rejections':len(got['algebra']['mathematical_damage_rejections'])+len(got['controls']['mathematical_domain_damage_rejections']),'canonical_bytes':len(canonical)},sort_keys=True))

if __name__=='__main__':main()
