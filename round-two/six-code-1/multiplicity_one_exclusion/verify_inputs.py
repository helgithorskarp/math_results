"""Replay published inputs; this does not formalize the new counting proof."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
THREAD_VARS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')

def require(ok,message):
    if not ok:raise ValueError(message)

def baseline(data):
    require(hashlib.sha256(data).hexdigest()==
            'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d',
            'ACL69 source bytes differ')
    words=[]
    for line in data.decode('ascii').splitlines():
        require(len(line)==18 and set(line)<=set('01'),'invalid binary word')
        word=frozenset(i for i,c in enumerate(line) if c=='1')
        require(len(word)==5,'wrong weight')
        words.append(word)
    require(len(words)==69 and len(set(words))==69,'wrong distinct word count')
    hist={}
    for a,b in itertools.combinations(words,2):
        require(len(a&b)<=2,'baseline intersection exceeds two')
        d=len(a^b);hist[d]=hist.get(d,0)+1
    require(hist=={6:1264,8:637,10:445},'baseline full distance histogram differs')
    return {'words':69,'literal_pairs':sum(hist.values()),'distances':hist,
            'point_degrees':[sum(i in w for w in words) for i in range(18)]}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository-root',type=Path,default=HERE.parents[2],
                   help='root of the public repository or an exact public-input mirror')
    args=p.parse_args()
    root=args.repository_root.resolve()
    deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
    pins=deps['dependencies']+deps['runtime_files']
    for pin in pins:
        relative=pin.get('source',pin.get('path'))
        expected=pin.get('proof_sha256',pin.get('sha256'))
        data=(root/relative).read_bytes()
        require(hashlib.sha256(data).hexdigest()==expected,'pinned source differs: '+relative)
    known=baseline((HERE/'acl69.txt').read_bytes())
    env=os.environ.copy();env.update({k:'1' for k in THREAD_VARS})
    flags=['-B']+(['-O'] if sys.flags.optimize else [])
    prefix=[sys.executable,*flags]
    d='constant_weight_upper71_review1/'
    commands=[
        ['produce.py','--certificate',d+'certificate.json'],
        ['verify.py','--certificate',d+'certificate.json','--baseline',str(HERE/'acl69.txt'),
         '--controls','--expected',d+'expected.json']]
    commands=[[d+cmd[0],*cmd[1:]] for cmd in commands]
    d='constant_weight_18_6_5_equality_structure/'
    unit='coding_theory/a18_6_5_one_unsaturated_at_71/expected.json'
    mixed='coding_theory/a18_6_5_2111_star_classification/expected.json'
    for name in ('common_mixed','common_unit','common_mixed_unit'):
        extra=[]
        if name!='common_mixed':extra+=['--source-expected',unit]
        if name=='common_mixed_unit':extra+=['--mixed-source-expected',mixed]
        commands.append([d+'check_'+name+'.py',*extra])
        commands.append([d+'verify_'+name+'.py','--compare-primary'])
    records=[]
    for cmd in commands:
        start=time.monotonic()
        result=subprocess.run([*prefix,*cmd],cwd=root,env=env,text=True,
                              capture_output=True,timeout=45)
        require(result.returncode==0,'input replay failed: '+repr(cmd)+'\n'+result.stderr)
        record={'command':cmd,'exit_code':result.returncode,
                'seconds':round(time.monotonic()-start,6),'result':json.loads(result.stdout)}
        records.append(record)
        print(json.dumps({'checked':cmd[0],'seconds':record['seconds']}),file=sys.stderr,flush=True)
    print(json.dumps({'actual_agent':'six-code-1','role':'researcher',
        'status':'PUBLISHED_INPUTS_REPLAYED_AND_PRIMARY_BASELINE_CHECKED',
        'new_counting_bridge':'ordinary proof in PROOF.md; not machine checked',
        'source_pins_checked':len(pins),'optimized_python':bool(sys.flags.optimize),
        'thread_limits':{k:'1' for k in THREAD_VARS},'sequential_child_processes':True,
        'baseline69':known,'replays':records,
        'maxrss_children_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},
        indent=2,sort_keys=True))

if __name__=='__main__':main()
