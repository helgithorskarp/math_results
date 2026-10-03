"""Separate bounded SERIAL phases; no parallel math and no native author access."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from verify import DAMAGES
ERRORS={
 'newton':'Whole third coefficient',
 'mean_payment':'Whole third coefficient',
 'norm_payment':'Whole third coefficient',
 'freeze_moving':'Complete third root map retained',
 'critical_multiplicity':'Every original base root equation',
 'anchor':'Whole fixed first/second witness columns',
 'repair':'All4 active roots zero then strictly inward',
 'power':'Complete actual FIRST-power through3',
 'tangent':'Whole balanced quadratic nonnegative form',
 'equality_cap':'NEW equality-cap all4 inward originals'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['positive','early','late_a','late_b','fixtures'],required=True);ap.add_argument('--optimized',action='store_true');args=ap.parse_args()
    env=dict(os.environ,**{n:'1' for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']});start=time.monotonic();runs=[]
    temporary_base=Path(os.environ.get('AUDIT_SCRATCH',str(ROOT/'scratch')))
    temporary_base.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='six-reviewer-4-third-',dir=temporary_base) as tmpname:
        tmp=Path(tmpname)
        def child(script=ROOT/'verify.py',extra=(),error=None):
            cmd=[sys.executable,'-I','-B']+(['-O'] if args.optimized else [])+[str(script),*extra];t=time.monotonic()
            p=subprocess.run(cmd,cwd=tmp,env=env,capture_output=True,timeout=30)
            if bool(p.returncode)==bool(error is None):raise ValueError('Wrong control outcome: '+p.stderr.decode()[-1000:])
            if error and error not in p.stderr.decode():raise ValueError('Wrong rejection path: '+p.stderr.decode()[-1000:])
            runs.append(dict(args=list(extra),exit_code=p.returncode,seconds=time.monotonic()-t,stdout_bytes=len(p.stdout),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),intended_rejection=error))
            return p.stdout
        if args.phase=='positive':
            live=child(extra=('--record',));cold=tmp/'EMPTY';cold.mkdir();m=json.loads((ROOT/'MANIFEST.json').read_text())
            for n in list(m['core_files'])+['MANIFEST.json']:shutil.copyfile(ROOT/n,cold/n)
            empty=child(cold/'verify.py',('--record',))
            if live!=empty:raise ValueError('Whole EMPTY source-only mismatch')
        elif args.phase in ['early','late_a','late_b']:
            selected=DAMAGES[:5] if args.phase=='early' else DAMAGES[5:8] if args.phase=='late_a' else DAMAGES[8:]
            for d in selected:child(extra=('--damage',d),error=ERRORS[d])
        else:
            original=json.loads((ROOT/'EXPECTED.json').read_text())
            child(extra=('--expected',str(tmp/'absent')),error='No such file')
            p=tmp/'malformed';p.write_text('{');child(extra=('--expected',str(p)),error='JSONDecodeError')
            for d in ['bool_label','delete_root','changed_payment','delete_new_family','extra','duplicate_key']:
                v=json.loads(json.dumps(original))
                if d=='bool_label':v['actual_witness']['all9_root_jets'][0]['j']=True
                elif d=='delete_root':v['actual_witness']['all9_root_jets'].pop()
                elif d=='changed_payment':v['third_offsets']['mean_payment'][0]='0'
                elif d=='delete_new_family':del v['actual_witness']['NEW_equality_cap']
                elif d=='extra':v['extra']=True
                p=tmp/d
                if d=='duplicate_key':p.write_text('{"extra":1,"extra":2}')
                else:p.write_text(json.dumps(v))
                child(extra=('--expected',str(p)),error='Duplicate JSON key' if d=='duplicate_key' else 'Entire typed fixture mismatch before import')
            cold=tmp/'source_damage';cold.mkdir();m=json.loads((ROOT/'MANIFEST.json').read_text())
            for n in list(m['core_files'])+['MANIFEST.json']:shutil.copyfile(ROOT/n,cold/n)
            with (cold/'exact.py').open('a') as f:f.write('\n# actual preimport source damage\n')
            child(cold/'verify.py',error='Core source seal mismatch: exact.py')
    print(json.dumps(dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',phase=args.phase,optimized=args.optimized,runs=runs,elapsed_seconds=time.monotonic()-start,threads=1,serial=True,child_guard_seconds=30),sort_keys=True))

if __name__=='__main__':main()
