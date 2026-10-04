"""Bounded source-only final gates, serial original math children, no publication.

six-downset-1 / researcher; same author, not independent review.
Each math child has the unchanged60s limit and native threads1.
Original n<=6/h<=10/N<=80 preflight lives in BOTH producer and reader.
No predecessor program, expected certificate or data is imported.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
from pathlib import Path
from hashlib import sha256
import argparse
import json
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
FILES=('geometry.py','reader.py','adverse.py','reproduce.py','PROOF.md','SCALAR-BOUNDS.md','README.md')
CASES=(('asymmetric',[4,3,2]),('minimum-light',[5,2,2]),('four-baseline',[3,2,2,2]))
MAX_BYTES=32*1024*1024

def require(ok,message):
    if not ok:
        raise ValueError(message)

def barrier():
    state=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state)/n).exists() for n in
            ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    barrier();require(not out.exists(),'unique source-only gate output')
    out.mkdir(parents=True)
    frozen={name:(HERE/name).read_bytes() for name in FILES}
    manifest={name:dict(bytes=len(raw),sha256=sha256(raw).hexdigest()) for name,raw in frozen.items()}
    require(sum(len(x) for x in frozen.values())<=MAX_BYTES,'unchanged32MiB source guard')
    cold=out/'cold-source';cold.mkdir()
    for name,raw in frozen.items():
        (cold/name).write_bytes(raw)
    env=dict(os.environ);children=[];mathematics={};observational={'observed_seconds','peak_RSS_KiB','optimized'}
    def child(source,optimized,argv):
        barrier();require(all((HERE/k).read_bytes()==v for k,v in frozen.items()),'frozen whole source before child')
        command=[sys.executable,'-I']+(['-O'] if optimized else [])+[str(source),*argv]
        started=time.monotonic()
        try:
            completed=subprocess.run(command,env=env,capture_output=True,text=True,timeout=60,check=False)
        except subprocess.TimeoutExpired:
            raise TimeoutError('unchanged60s child timeout; incomplete, not mathematical absence') from None
        receipt=dict(child=len(children)+1,source=source.name,cold=source.parent==cold,
                     optimized=optimized,returncode=completed.returncode,
                     seconds=time.monotonic()-started,stdout=completed.stdout,stderr=completed.stderr)
        children.append(receipt)
        (out/'CHILDREN.json').write_text(json.dumps(children,indent=2)+'\n')
        require(completed.returncode==0,'actual child failed; inspect CHILDREN.json')
        require(all((HERE/k).read_bytes()==v for k,v in frozen.items()),'frozen whole source after child')
    for label,source,optimized in (('normal',HERE,False),('optimized',HERE,True),('cold',cold,False)):
        lane=out/label;lane.mkdir()
        records={}
        for name,counts in CASES:
            produced=lane/(name+'-input.json');read=lane/(name+'-read.json')
            child(source/'geometry.py',optimized,['--n','4','--counts',','.join(map(str,counts)),'--out',str(produced)])
            child(source/'reader.py',optimized,['--input',str(produced),'--out',str(read)])
            require(produced.stat().st_size<=MAX_BYTES and read.stat().st_size<=MAX_BYTES,'unchanged32MiB records')
            raw=json.loads(read.read_text());body={k:v for k,v in raw.items() if k not in observational}
            records[name]=dict(input_bytes=produced.stat().st_size,
                input_sha256=sha256(produced.read_bytes()).hexdigest(),whole_math=body)
        adverse=lane/'adverse.json'
        child(source/'adverse.py',optimized,['--input',str(lane/'asymmetric-input.json'),'--out',str(adverse)])
        records['adverse']=json.loads(adverse.read_text())
        if mathematics:
            require(records==mathematics,'ENTIRE mathematics/input/adverse records agree normal/O/cold')
        else:
            mathematics=records
        (out/'MATHEMATICS.json').write_text(json.dumps(mathematics,indent=2)+'\n')
    require(all((HERE/k).read_bytes()==v for k,v in frozen.items()),'ENTIRE final frozen source')
    expected=HERE/'EXPECTED.json'
    if expected.exists():
        require(json.loads(expected.read_text())==mathematics,'WHOLE frozen reader-facing EXPECTED record')
    result=dict(agent='six-downset-1',role='researcher',status='COMPLETE FROZEN SOURCE-ONLY GATES',
        source_manifest=manifest,actual_math_children=len(children),all_children_exit_zero=True,
        cases=[dict(n=4,counts=c,N=16+6*sum(c)) for name,c in CASES],
        lanes=['normal','optimized','cold'],whole_lane_comparisons=2,
        semantic_rejections_per_lane=mathematics['adverse']['rejection_count'],
        whole_mathematics_bytes=(out/'MATHEMATICS.json').stat().st_size,
        whole_mathematics_sha256=sha256((out/'MATHEMATICS.json').read_bytes()).hexdigest(),
        new_source_commit=None,new_graph_ref=None,independent_review=False,formalized=False,
        controls_are_not_infinite_enumeration=True,large_original_constructed=False)
    (out/'GATES.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in
        ('status','actual_math_children','semantic_rejections_per_lane','whole_mathematics_bytes','whole_mathematics_sha256')}))

if __name__=='__main__':
    main()
