"""Hash-pinned public input extraction and sequential local-premise replay.

Actual agent six-code-1, researcher. This does not formalize PROOF.md.
The universal/shared-hub replays are optional because unchanged normal/-O
replays in the preceding publication remain credited validation.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
THREAD_VARS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,default=HERE.parents[2])
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--all-shared',action='store_true')
    args=p.parse_args();repo=args.repository.resolve();work=args.work.resolve()
    require(work!=HERE and HERE not in work.parents and not work.exists(),'work must be new and outside source')
    work.mkdir(parents=True);root=work/'inputs';root.mkdir();start=time.monotonic()
    dep=json.loads((HERE/'DEPENDENCIES.json').read_text());pins=dep['dependencies']+dep['runtime_files']
    for pin in pins:
        path=pin.get('source',pin.get('path'));expected=pin.get('proof_sha256',pin.get('sha256'))
        raw=subprocess.check_output(['git','show',pin['source_commit']+':'+path],cwd=repo,timeout=20)
        require(sha256(raw).hexdigest()==expected,'published bytes differ: '+path)
        target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    env=os.environ.copy();env.update({k:'1' for k in THREAD_VARS})
    flags=['-B']+(['-O'] if sys.flags.optimize else []);prefix=[sys.executable,*flags]
    d='round-two/six-code-1/multiplicity_four_exclusion/'
    commands=[[d+'primary.py'],[d+'verify.py','--compare-primary']]
    if args.all_shared:
        d='constant_weight_upper71_review1/'
        commands += [[d+'produce.py','--certificate',d+'certificate.json'],
                     [d+'verify.py','--certificate',d+'certificate.json','--baseline',str(HERE/'acl69.txt'),
                      '--controls','--expected',d+'expected.json']]
        d='constant_weight_18_6_5_equality_structure/'
        unit='coding_theory/a18_6_5_one_unsaturated_at_71/expected.json'
        mixed='coding_theory/a18_6_5_2111_star_classification/expected.json'
        for name in ('common_mixed','common_unit','common_mixed_unit'):
            extra=[]
            if name!='common_mixed':extra+=['--source-expected',unit]
            if name=='common_mixed_unit':extra+=['--mixed-source-expected',mixed]
            commands += [[d+'check_'+name+'.py',*extra],[d+'verify_'+name+'.py','--compare-primary']]
    records=[]
    for cmd in commands:
        t=time.monotonic()
        result=subprocess.run([*prefix,*cmd],cwd=root,env=env,text=True,capture_output=True,timeout=45)
        require(result.returncode==0,'input replay failed: '+repr(cmd)+'\n'+result.stderr)
        records.append(dict(command=cmd,exit_code=0,seconds=time.monotonic()-t,result=json.loads(result.stdout)))
    record=dict(actual_agent='six-code-1',role='researcher',status='COMPLETE_PINNED_INPUT_AND_LOCAL_REPLAY',
                source_pins_checked=len(pins),optimized_python=bool(sys.flags.optimize),all_shared=args.all_shared,
                thread_limits={k:'1' for k in THREAD_VARS},one_cpu_intensive_child_at_a_time=True,
                counting_bridge='Ordinary unformalized proof in PROOF.md; not machine verified',replays=records)
    (work/'result.json').write_text(json.dumps(record,sort_keys=True)+'\n')
    print(json.dumps(dict(**record,seconds=time.monotonic()-start,
                          maxrss_children_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)),flush=True)


if __name__=='__main__':main()
