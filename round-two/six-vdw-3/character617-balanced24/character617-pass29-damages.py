"""Repaired-digest semantic probes of the new exact necessary reductions."""
import copy
import hashlib
import json
import os
import resource
import subprocess
import time
from pathlib import Path

h=Path(__file__).resolve().parent
work=h/'character617-pass29-damages'
if work.exists():raise SystemExit('Preserve existing damage run')
work.mkdir()
env=os.environ.copy()
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
sources={'capacity':h/'character617-size24-capacity.json','four':h/'character617-size24-common-four.json','five':h/'character617-size24-common-five.json'}
base={k:json.loads(p.read_text()) for k,p in sources.items()}
capacity_index=next(i for i,r in enumerate(base['capacity']['records']) if r['surviving_core_sizes'])
children=[];started=time.monotonic()

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def run(mode,kind,label,data,expected):
    if any(Path('/scratch/research-team-sol61-six-20260929/state',k).exists() for k in ('PAUSED','PAUSED.json','HANDOVER.json')):raise SystemExit('Operations barrier')
    if data is not None:
        data['records_sha256']=hashlib.sha256(canon(data['records'])).hexdigest()
        path=work/'current-semantic-input.json';path.write_bytes(canon(data)+b'\n')
    else:path=sources[kind]
    dest=work/f'{mode}-{label}-unexpected-or-positive.json'
    cmd=[str(h/'solver-env/bin/python')]
    if mode=='optimized':cmd.append('-O')
    if kind=='capacity':cmd += [str(h/'check-character617-size24-capacity.py'),'--input',str(path),'--domain',str(h/'character617-threshold-four.json'),'--output',str(dest),'--start',str(capacity_index),'--stop',str(capacity_index+1)]
    elif kind=='four':cmd += [str(h/'check-character617-size24-common-four.py'),'--input',str(path),'--capacity',str(sources['capacity']),'--output',str(dest)]
    else:cmd += [str(h/'check-character617-size24-common-five.py'),'--input',str(path),'--capacity-checked',str(h/'character617-size24-capacity-checks/normal/checked.json'),'--output',str(dest)]
    s=time.monotonic();record={'mode':mode,'kind':kind,'label':label,'guard_seconds':20,'threads':1,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'command':cmd}
    try:
        p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=20)
        valid=p.returncode==0 if expected is None else p.returncode!=0 and expected in p.stderr
        record.update(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,status='EXPECTED_POSITIVE_OR_SEMANTIC_REJECTION' if valid else 'FAILED_NO_EXCLUSION')
    except subprocess.TimeoutExpired:record['status']='TIMEOUT_INCOMPLETE_NO_EXCLUSION'
    record.update(seconds=time.monotonic()-s,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    children.append(record);(work/'execution.json').write_text(json.dumps(children,indent=2)+'\n')
    if record['status']!='EXPECTED_POSITIVE_OR_SEMANTIC_REJECTION':
        (work/'failed.json').write_text(json.dumps(record,indent=2)+'\n');raise SystemExit('Unexpected semantic or guard failure preserved')

def mutate(kind,label):
    data=copy.deepcopy(base[kind]);r=data['records'][capacity_index if kind=='capacity' else 0]
    if label=='singleton':r['singleton_counts'][0]+=1
    elif label=='maximum':r['exact_outside_maximum']+=1
    elif label=='omit-core':r['surviving_core_sizes']=[]
    elif label=='wrong-premise':data['first_five_maximum_missing_per_row']=3
    elif label=='omit-column-case':r['records'].pop(0)
    elif label=='false-added-row':r['records'][0]['cost_two_added_rows'].append(1)
    elif label=='duplicate-column-case':r['records'].append(copy.deepcopy(r['records'][0]))
    elif label=='wrong-minimum':r['records'][0]['minimum_missing']-=1
    elif label=='wrong-row-label':r['records'][0]['best_added_rows'][0][1]=1
    elif label=='wrong-common':r['C'][0]=1
    else:raise ValueError(label)
    return data

probes=[('capacity','singleton','full row-capacity maximum and every core size'),
        ('capacity','maximum','full row-capacity maximum and every core size'),
        ('capacity','omit-core','full row-capacity maximum and every core size'),
        ('capacity','wrong-premise','exact size24 row-capacity premises'),
        ('four','omit-column-case','every full original column/row record'),
        ('four','false-added-row','every full original column/row record'),
        ('five','omit-column-case','exact coefficient count separately'),
        ('five','duplicate-column-case','all full labeled column sets distinct and legal'),
        ('five','wrong-minimum','complete bit-sliced degree/minimizer record'),
        ('five','wrong-row-label','complete bit-sliced degree/minimizer record'),
        ('five','wrong-common','entire340-prefix family')]
for mode in ('normal','optimized'):
    for kind in sources:run(mode,kind,'positive-'+kind,None,None)
    for kind,label,expected in probes:run(mode,kind,kind+'-'+label,mutate(kind,label),expected)
    print(json.dumps({'mode':mode,'semantic_damages':len(probes),'all_rejected_for_intended_reason':True}),flush=True)
(work/'current-semantic-input.json').unlink()
record={'agent':'six-vdw-3','role':'researcher','children':len(children),'positive_whole_pairs':3,'semantic_damages_per_mode':len(probes),
        'seconds':time.monotonic()-started,'maximum_child_seconds':max(r['seconds'] for r in children),'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'status':'COMPLETE_PRIVATE_PASS29_POSITIVES_AND_SEMANTIC_DAMAGES_CHECKED'}
(work/'run.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
