"""One independent exact phase per guarded serial child; no native imports."""
import sys,json,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import need
import reconstruct as R

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def run(phase,joint_input=None):
 if phase=='uniform':
  from bivar import derive
  return derive()
 if phase=='generic':
  from generic import derive
  return derive()
 kind,q=phase.split('-');q=int(q);d=R.build(q,6)
 if kind=='joint':
  from joint_input import load,decode
  need(joint_input is not None,'explicit external literal input')
  obj=load(joint_input);vectors,weights=decode(d,obj)
  result=R.joint(d,vectors,weights)
  need(result['all_original_affine_dual_coefficients']==['-27349198384700972029/6278424954053565874176','-23607718427935883702131303/213466448437821239721984','0','0','0'],'all five exact claimed coefficients')
  return {'input':obj,'physical_weights':d['weights'],'joint':result}
 if kind=='negative':return R.moments(d)
 if kind=='positive':return {'moments':R.moments(d),'positive':R.positive(d)}
 raise ValueError('unknown exact phase')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('phase');ap.add_argument('--emit',type=Path);ap.add_argument('--fixture',type=Path);ap.add_argument('--joint-input',type=Path);args=ap.parse_args();x=run(args.phase,args.joint_input);b=canonical(x)
 if args.emit:args.emit.write_bytes(b+b'\n')
 if args.fixture:
  def unique(pairs):
   out={}
   for k,v in pairs:need(k not in out,'duplicate external input');out[k]=v
   return out
  other=json.loads(args.fixture.read_text(),object_pairs_hook=unique)
  need(canonical(other)==b,'entire typed independent phase record')
 print(json.dumps({'phase':args.phase,'record_bytes':len(b),'whole_record_sha256':hashlib.sha256(b).hexdigest()}))
