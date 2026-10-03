"""Portable SOURCE-ONLY serial reproduction of the variable-q author lemma.

Every mathematical child exits before the next is launched. Every entire
generated certificate byte is compared with the compact frozen source.
The original full controls and separate coefficient checker are retained.
"""
import os
NATIVE=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for name in NATIVE:os.environ[name]='1'
from pathlib import Path
import sys,json,subprocess,time,argparse
from hashlib import sha256

def require(ok,msg):
    if not ok:raise ValueError(msg)

def barriers():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--record');args=ap.parse_args()
    root=Path(__file__).resolve().parent;work=root/'work';work.mkdir(exist_ok=True)
    barriers();start=time.monotonic();children=[]
    prefix=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
    def run(script,*arguments):
        barriers();t=time.monotonic()
        child=subprocess.run(prefix+[str(root/script),*map(str,arguments)],cwd=root,text=True,capture_output=True,timeout=62)
        children.append(dict(script=script,arguments=list(map(str,arguments)),seconds=time.monotonic()-t,returncode=child.returncode))
        require(child.returncode==0,'mathematical child failed, not a theorem: '+script+'\n'+child.stderr[-4000:])
        print(json.dumps(dict(stage='serial mathematical child complete',script=script,seconds=children[-1]['seconds'])),flush=True)
    run('gaussian.py')
    producer=json.loads((work/f'gaussian-O{sys.flags.optimize}.json').read_text())
    require(producer['status'].startswith('ALL20 RATIONAL GAUSSIAN PIVOTS'),'producer STOPPED/incomplete is not a proof')
    compact={key:producer[key] for key in ('domain','guards','forms','rows','updates')}
    generated=(json.dumps(compact,separators=(',',':'),sort_keys=True)+'\n').encode()
    source=(root/'GAUSSIAN.json').read_bytes()
    require(generated==source,'EVERY generated original form/pivot/update byte equals entire compact frozen source')
    run('check_gaussian.py',root/'GAUSSIAN.json')
    checker=json.loads((work/f'checked-gaussian-O{sys.flags.optimize}.json').read_text())
    require(checker['result']['complete'],'full separate exact coefficient reconstruction')
    controls=[]
    for h in (2,3):
        run('sector_control.py','--n','4','--h',str(h))
        controls.append(json.loads((work/f'sectors-n4-h{h}-O{sys.flags.optimize}.json').read_text())['result'])
    run('damages.py',root/'GAUSSIAN.json')
    damages=json.loads((work/f'damages-O{sys.flags.optimize}.json').read_text())
    require(damages['complete'] and len(damages['cases'])==8 and all(z['rejected'] for z in damages['cases']),'all eight semantic damages rejected, no timeout/kill counted')
    record=dict(agent='six-downset-1',role='researcher',domain=producer['domain'],certificate_bytes=len(source),certificate_sha256=sha256(source).hexdigest(),whole_generated_certificate_bytes_equal=True,coefficient_reconstruction=checker['result'],original_complete_controls=controls,semantic_rejections=damages['cases'],trust='Author ordinary proof with separate same-author exact computation; geometric/full-space/Schur bridges unformalized; independent review pending.')
    output=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
    if (root/'RESULTS.json').exists():require(output==(root/'RESULTS.json').read_bytes(),'ENTIRE mathematical record equals frozen RESULTS, not a digest/prefix')
    destination=Path(args.record or work/f'verification-O{sys.flags.optimize}.json');destination.write_bytes(output)
    execution=dict(agent='six-downset-1',role='researcher',complete=True,one_serial_mathematical_child=True,native_threads={name:os.environ[name] for name in NATIVE},optimized=sys.flags.optimize,children=children,total_seconds=time.monotonic()-start,mathematical_record_bytes=len(output),mathematical_record_sha256=sha256(output).hexdigest(),guards=producer['guards'])
    (work/f'execution-O{sys.flags.optimize}.json').write_text(json.dumps(execution,indent=2)+'\n')
    print(json.dumps(execution),flush=True)
if __name__=='__main__':main()
