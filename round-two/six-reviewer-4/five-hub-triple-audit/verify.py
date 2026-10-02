"""Fully offline reviewer proof reconstruction; serial fixed-deadline children."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
def require(condition,message):
    if not condition:raise ValueError(message)
def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def main():
    seal=json.loads((ROOT/'FIRST_SEAL.json').read_text())
    update=json.loads((ROOT/'CONTROL_UPDATE.json').read_text())
    for name,sha in seal['source_sha256'].items():
        if name=='controls.py':sha=update['current_controls_sha256']
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,'changed sealed source '+name)
    env=dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    values={}
    for key,script in [('core','audit.py'),('controls','controls.py')]:
        flags=['-O'] if sys.flags.optimize else []
        result=subprocess.run([sys.executable]+flags+[str(ROOT/script)],capture_output=True,env=env,timeout=30)
        require(result.returncode==0,result.stderr.decode())
        values[key]=json.loads(result.stdout)
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    require(canonical(values)==canonical(expected),'complete independent mathematical output mismatch')
    require(hashlib.sha256(canonical(values['core'])).hexdigest()==seal['core_sha256'],'core seal')
    require(hashlib.sha256(canonical(values['controls'])).hexdigest()==update['runs'][0]['sha256'],'updated control seal')
    print(json.dumps({'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer',
                      'status':'COMPLETE_CONDITIONAL_FIVE_HUB_P37_AUDIT',
                      'full_math_bytes':len(canonical(values)),
                      'full_math_sha256':hashlib.sha256(canonical(values)).hexdigest(),
                      'population_count':values['core']['population_count'],
                      'certificates':values['core']['certificates'],
                      'scope':'Imported classification/selector; ordinary unformalized bridges; no packing or global upper70.',
                      'controls':values['controls']},sort_keys=True))

if __name__=='__main__':main()
