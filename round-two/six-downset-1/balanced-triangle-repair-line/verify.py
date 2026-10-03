"""PRIVATE serial complete source-only replay for the original repair line."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
from pathlib import Path
import sys, json, subprocess, time
from hashlib import sha256
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact import require


def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')), 'operational barrier')
    directory=Path(__file__).resolve().parent; (directory/'work').mkdir(exist_ok=True)
    mode=sys.flags.optimize; started=time.monotonic(); executions=[]
    phases=[('symbolic.py',[]),('check_inverse.py',[str(directory/'INVERSE.json')]),
            ('original_control.py',['--h','2']),('original_control.py',['--h','3']),('damages.py',[])]
    for program,args in phases:
        command=[sys.executable]+(['-O'] if mode else [])+[str(directory/program)]+args
        # A true subprocess wait precedes each next mathematical child.
        p=subprocess.run(command,cwd=directory,text=True,capture_output=True,timeout=65)
        require(p.returncode==0,'source-only child failed: '+program+'\n'+p.stdout+'\n'+p.stderr)
        executions.append(dict(program=program,args=args,returncode=p.returncode))
        print(json.dumps(dict(phase=program,args=args,complete=True)),flush=True)
    raw=json.loads((directory/'work'/f'symbolic-O{mode}.json').read_text())
    require(raw['status'].startswith('ALL compact'),'entire symbolic solve must complete, not a stopped record')
    regenerated={k:v for k,v in raw['certificate'].items() if k!='pivots'}
    encoded=(json.dumps(regenerated,sort_keys=True,separators=(',',':'))+'\n').encode()
    require(encoded==(directory/'INVERSE.json').read_bytes(),'EVERY regenerated compact certificate byte')
    checked=json.loads((directory/'work'/f'checked-inverse-O{mode}.json').read_text())
    literal=[json.loads((directory/'work'/f'original-n4-h{h}-O{mode}.json').read_text()) for h in (2,3)]
    damaged=json.loads((directory/'work'/f'damages-O{mode}.json').read_text())
    math=dict(agent='six-downset-1',role='researcher',status='PASS complete source-only coefficient and original controls; uniform theorem remains ordinary unformalized/unreviewed',
              domain=regenerated['domain'],certificate_bytes=len(encoded),certificate_sha256=sha256(encoded).hexdigest(),
              separate_inverse=checked['result'],original_controls=[z['result'] for z in literal],
              damages=damaged['semantic_cases'],no_uniform_endpoint_ordering_claim=True)
    mathematical=(json.dumps(math,sort_keys=True,separators=(',',':'))+'\n').encode()
    expected=directory/'RESULTS.json'
    if expected.exists():
        require(mathematical==expected.read_bytes(),'EVERY full source-bound mathematical result byte')
    output=directory/'work'/f'MATH-O{mode}.json'; output.write_bytes(mathematical)
    observed=[raw,checked]+literal+[damaged]
    execution=dict(agent='six-downset-1',role='researcher',optimized=mode,complete=True,seconds=time.monotonic()-started,
                   math_sha256=sha256(mathematical).hexdigest(),math_bytes=len(mathematical),children=executions,
                   max_child_seconds=max(z['seconds'] for z in observed),max_child_peak_KiB=max(z['peak_KiB'] for z in observed),
                   native_threads=1,serial_math_child=1,child_seconds_guard=60,polynomial_terms_guard=512,packing_bytes_guard=33554432)
    (directory/'work'/f'REPLAY-O{mode}.json').write_text(json.dumps(execution,indent=2)+'\n')
    print(json.dumps(execution),flush=True)


if __name__=='__main__':
    main()
