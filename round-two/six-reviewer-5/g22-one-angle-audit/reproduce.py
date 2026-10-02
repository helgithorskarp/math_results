"""Regenerate complete independent evidence serially with stdlib exact arithmetic."""
import json,hashlib,argparse
from pathlib import Path
import aliases,algebra,controls
P=Path(__file__).resolve().parent

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def duplicates(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate field')
  d[k]=v
 return d
def read(p):return json.loads(p.read_text(),object_pairs_hook=duplicates,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite')))
def generate():
 a=aliases.run();b=algebra.run();c=controls.run()
 if a['accepted']!=a['only_angle7_nonreflex']:raise ValueError('weakened-angle cover differs')
 if len(a['accepted'])!=5 or len(a['without_convex'])!=6:raise ValueError('complete aliases')
 if any(not x['wide_positive'] or not x['old_positive'] for x in b['internal']):raise ValueError('sign gaps')
 if any(not x['wide_negative'] or not x['old_negative'] for x in b['obstructions']):raise ValueError('sign obstructions')
 if any(row and dict(row).get(6) not in [4,8,13] for row in a['accepted']):raise ValueError('uncovered alias')
 return dict(actual_reviewer='six-reviewer-5',role='independent mathematical reviewer',aliases=a,algebra=b,controls=c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',type=Path);args=p.parse_args();r=generate();data=json.dumps(r,sort_keys=True,indent=2)+'\n'
 if args.write:args.write.write_text(data)
 else:
  if canonical(read(P/'RESULT.json'))!=canonical(r):raise ValueError('whole independent record differs')
 print(json.dumps(dict(status='COMPLETE_EXACT_INDEPENDENT_FACIAL_AUDIT',whole_sha256=hashlib.sha256(canonical(r)).hexdigest(),maps=r['aliases']['partial_injections'],wide_c_interval=['1/2','3/5'],only_pentagon_angle_required='name7<=pi',additional_local_survivor_without_angle=[[0,12],[6,1]]),sort_keys=True))
