"""Complete default regeneration; optional saved-record comparison is explicit."""
from pathlib import Path
import argparse,hashlib,json
import audit,controls,refinements
import cores as c
HERE=Path(__file__).resolve().parent

def run(work,target,record=None,control_record=None):
 audit.inputs(target)
 if record is None:
  result=audit.run(work/'audit',target);checks=controls.controlled(work/'controls',target)
 else:
  c.need(control_record is not None,'a saved control record is required')
  result=json.loads(record.read_text());checks=json.loads(control_record.read_text())
 value=dict(audit=result,controls=checks,refinements=refinements.run())
 expected=json.loads((HERE/'expected.json').read_text())
 c.need(value==expected,'independent complete proof record differs')
 print(json.dumps(dict(status='PASS complete evidence record',record_sha256=c.sha(value),classes=result['core']['profiles'],row_pairs=result['row_pairs'],states=result['states'],saved_record_comparison_only=record is not None),indent=2))
 return value
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--target',type=Path,default=HERE.parent/'book_ramsey_b4_b7_regular110_neighborhood_floor14');p.add_argument('--record',type=Path);p.add_argument('--control-record',type=Path);a=p.parse_args();run(a.work.resolve(),a.target.resolve(),a.record,a.control_record)
