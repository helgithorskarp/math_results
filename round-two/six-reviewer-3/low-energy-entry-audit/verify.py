"""Rebuild all independent identities and reject entire malformed fixtures."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[key]='1'
import argparse,hashlib,json,signal,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import audit

def parse(text):
    def pairs(xs):
        out={}
        for k,v in xs:
            if k in out:raise ValueError('duplicate JSON key')
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON constant')))

def same(a,b):
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def build():return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','audit':audit()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));ap.add_argument('--emit',action='store_true');ap.add_argument('--generate',action='store_true');args=ap.parse_args()
    signal.alarm(45)
    got=build();raw=json.dumps(got,sort_keys=True,separators=(',',':')).encode()
    if args.generate:args.expected.write_text(json.dumps(got,indent=2,sort_keys=True)+'\n')
    if not same(got,parse(args.expected.read_text())):raise ValueError('entire typed independent fixture mismatch')
    if args.emit:sys.stdout.buffer.write(raw+b'\n')
    else:print('PASS independent low-energy entry '+hashlib.sha256(raw).hexdigest());print(json.dumps({'whole_identities':len(got['audit']['checks']),'literal_root_control_pairs':36,'math_damage_rejections':len(got['audit']['damage_rejections']),'canonical_bytes':len(raw),'energy_cutoffs':[30,32]},sort_keys=True))

if __name__=='__main__':main()
