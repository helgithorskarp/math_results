"""Generate locally when requested, then literally check the phase restriction."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from check import check_tree,transport

HERE=Path(__file__).resolve().parent
A=((8,0),(9,0),(10,1),(14,1),(12,3))
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--generate',action='store_true')
ap.add_argument('--generated',type=Path,default=HERE/'generated');args=ap.parse_args()
args.generated.mkdir(parents=True,exist_ok=True)
expected=json.loads((HERE/'manifest.json').read_text());results={}
env=os.environ.copy()
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
for phase in (0,1,2,3):
    path=args.generated/f'tree-16-{phase}.json'
    if args.generate:
        for batch in range(3):
            command=[sys.executable,'-B',str(HERE/'generate.py'),'--prefix',
                     '8:0,9:0,10:1,14:1,12:3,16:'+str(phase),'--seconds','180','--nodes','700','--out',str(path)]
            outcome=subprocess.run(command,env=env)
            if outcome.returncode not in (0,2):raise SystemExit(outcome.returncode)
            if path.exists() and json.loads(path.read_text()).get('complete'):break
        else:raise SystemExit('INCOMPLETE: batch allowance exhausted; no exclusion asserted')
    tree=json.loads(path.read_text())
    if tuple(tuple(v) for v in tree['root_anchors'])!=A+((16,phase),):raise ValueError('Wrong conditional root')
    result=json.loads(json.dumps(check_tree(tree)))
    if result!=expected[str(phase)]:raise ValueError('Manifest mismatch; inspect the actual exact proof')
    results[str(phase)]=result
bins={b:[a for a in range(16) if transport(10080,A,16,a,b) is not None] for b in (0,1,2,3,4)}
if bins!={0:[0,8],1:[1,5,9,13],2:[2,6,10,14],3:[3,7,11,15],4:[4,12]}:
    raise ValueError('Incomplete phase classification')
print(json.dumps({'proved':'specified five-class prefix forces modulus16 with phase4 or12',
                  'period':10080,'nodes':sum(r['nodes'] for r in results.values()),
                  'raw_phases':sum(r['raw_branch_phases'] for r in results.values()),
                  'positive_transports':sum(r['positive_transports'] for r in results.values()),
                  'pair_entries':sum(r['pair_phase_entries'] for r in results.values())},sort_keys=True))
