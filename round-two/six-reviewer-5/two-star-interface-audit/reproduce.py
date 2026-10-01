"""Cold serial reproduction against frozen data; no author code executes."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',required=True);args=parser.parse_args()
    here=Path(__file__).resolve().parent;work=Path(args.work).resolve();work.mkdir(parents=True,exist_ok=True)
    if here==work or here in work.parents:raise ValueError('generated corpus must stay outside source directory')
    env=dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[name]='1'
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    controls=subprocess.run(python+[str(here/'controls.py')],env=env,capture_output=True,text=True,timeout=30,check=True)
    data=json.loads(controls.stdout)
    if data['status']!='PASS_SEMANTIC_CONTROLS' or len(data['damage_rejections'])!=10:raise ValueError('controls incomplete')
    (work/'controls.json').write_text(controls.stdout)
    audit=subprocess.run(python+[str(here/'audit.py'),'--compare','--output',str(work/'raw.json')],env=env,capture_output=True,text=True,timeout=180,check=True)
    raw=json.loads(audit.stdout)
    if raw['status']!='PASS_COMPLETE_RAW_CARRIER':raise ValueError('carrier incomplete')
    print(json.dumps({'status':'PASS_COLD_FROZEN_REPRODUCTION','agent':'six-reviewer-5','role':'independent mathematical reviewer',
                     'controls':data,'carrier':raw},sort_keys=True))

if __name__=='__main__':main()
