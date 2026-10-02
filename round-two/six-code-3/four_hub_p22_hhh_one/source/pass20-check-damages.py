"""Five semantic damages to actual complete records, checked serially."""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path

S=Path('round-two/six-code-3/scratch')
def need(c,m):
    if not c:raise ValueError(m)
author_path=S/'pass20-full-T2-N-producer.json'
data=json.loads(author_path.read_text())
baseline=json.loads((S/'pass20-independent-full-T2-N.json').read_text())
need(baseline['status']=='PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_CANDIDATE_LIST','valid original independent audit required')
need(baseline['author_result_sha256']==hashlib.sha256(author_path.read_bytes()).hexdigest(),'original raw provenance binding')
interpreter=[sys.executable]+(['-O'] if sys.flags.optimize else [])
env=dict(os.environ)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[k]='1'
tests=[('missing_population','all complete preliminary T2 populations'),
       ('missing_carrier','entire independent carrier stream'),
       ('wrong_population_input_digest','actual whole population input'),
       ('forged_coordinate_support','every coordinate N set, joint N4 tuple and failure agrees'),
       ('forged_coupled_tuple','every coordinate N set, joint N4 tuple and failure agrees')]
out=[]
folder=S/'pass20-damages';need(not folder.exists(),'fresh damage namespace');folder.mkdir()
for name,message in tests:
    damaged=copy.deepcopy(data)
    if name=='missing_population':damaged['records'].pop()
    elif name=='missing_carrier':damaged['canonical_carriers'].pop()
    elif name=='wrong_population_input_digest':damaged['input_populations_sha256']='0'*64
    elif name=='forged_coordinate_support':damaged['records'][0]['carrier_results'][0]['coordinate_N_sets']=[[99]]*4
    else:damaged['records'][0]['carrier_results'][0]['coupled_N4']=[[99]*4]
    candidate=folder/(name+'.json');target=folder/(name+'-check.json')
    candidate.write_text(json.dumps(damaged,sort_keys=True,separators=(',',':'))+'\n')
    completed=subprocess.run(interpreter+[str(S/'pass20-check-full-T2-N.py'),'--author',str(candidate),'--output',str(target)],env=env,capture_output=True,text=True,timeout=60)
    need(completed.returncode!=0 and ('ValueError: '+message) in completed.stderr,'intended damage rejected for mathematical reason: '+name)
    out.append(dict(damage=name,rejected=True,intended_reason=message))
    candidate.unlink()
result=dict(agent='six-code-3',role='researcher',status='ACTUAL_RECORD_SEMANTIC_DAMAGE_AUDIT_PASS',valid_original_accepted=True,damages=out,serial_children=True,native_threads=1,independent_person_review=False)
(S/'pass20-certificate-damages.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,sort_keys=True))
