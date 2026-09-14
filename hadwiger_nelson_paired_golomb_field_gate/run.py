"""Reproduce in a new work directory; optionally reuse a hash-checked parent census."""
from pathlib import Path
import argparse,subprocess,sys,os,shutil
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--parent-census',type=Path);ap.add_argument('--sanitize',action='store_true');args=ap.parse_args()
W=args.work.resolve();W.mkdir(parents=True,exist_ok=True)
if any(W.iterdir()):raise ValueError('use an empty work directory')
D=Path(__file__).resolve().parent;P=D.parent/'hadwiger_nelson_single_anchor_field_gate';flags=['-std=c++17','-O2','-Wall','-Wextra']
if args.sanitize:flags+=['-fsanitize=undefined','-fno-sanitize-recover=all']
if args.parent_census:shutil.copy2(args.parent_census,W/'G_census.json')
else:
 subprocess.run(['c++',*flags,str(P/'mod_census.cpp'),'-o',str(W/'parent_census')],check=True)
 sys.path.insert(0,str(P));from census import run
 run('G',W,W/'parent_census',True)
subprocess.run(['c++',*flags,str(D/'within.cpp'),'-o',str(W/'within')],check=True)
env=dict(os.environ);env['HN_PAIR_RUN_DIR']=str(W)
for script in ['prepare.py','geometry.py','verify.py']:
 subprocess.run([sys.executable,'-O','-B',str(D/script)],env=env,check=True)
