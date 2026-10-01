"""Reject changed pinned source dependencies in normal and optimized Python."""
import argparse,json,shutil,subprocess,sys
from pathlib import Path

here=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
args=ap.parse_args();root=args.work.absolute()
if root.exists():raise ValueError('fresh control work directory required')
root.mkdir(parents=True)
packet=root/here.name;helpers=root/'order7-geometric-cut'
packet.mkdir();helpers.mkdir()
for name in ['run.py','SOURCE_PINS.json','expected.json']:
    shutil.copyfile(here/name,packet/name)
for name in ['encode.py','sign_audit.py','check_rup_lrat.py','solve.py']:
    shutil.copyfile(here.parent/'order7-geometric-cut'/name,helpers/name)
helper=helpers/'encode.py'
helper.write_text(helper.read_text()+'\n# injected dependency corruption\n')
records=[]
for flags in [[],['-O']]:
    work=root/('attempt-O' if flags else 'attempt')
    p=subprocess.run([sys.executable]+flags+[str(packet/'run.py'),'--kind','opposed','--work',str(work),'--audit-only'],capture_output=True,text=True,timeout=10)
    if p.returncode==0 or 'changed committed source dependency' not in p.stderr:
        raise ValueError('corrupted source dependency was not rejected')
    records.append({'mode':'optimized' if flags else 'normal','status':'CORRUPTED_DEPENDENCY_REJECTED','native_solver_run':False})
(root/'result.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records))
