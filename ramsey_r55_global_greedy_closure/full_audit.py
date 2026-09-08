"""Seven complete physical CNFs, independently reconstructed literal by literal."""
from pathlib import Path
import argparse,json,time
import base,strengthen,check_global
HERE=Path(__file__).resolve().parent
BRANCHES=[[5,1,0],[5,4,3],[6,2,1],[6,3,2],[7,1,2],[7,4,0],[5,1,2]]

def run(parent_path,work):
 parent=base.load(parent_path);work=Path(work);work.mkdir(parents=True,exist_ok=True);records=[];started=time.monotonic()
 for branch in BRANCHES:
  path=work/('branch-'+'-'.join(map(str,branch))+'.cnf');t=time.monotonic();produced=strengthen.write(parent['model'].Packing(branch),path);checked=check_global.audit_file(branch,path)
  for field in ('variables','clauses','bytes','sha256'):
   if produced[field]!=checked[field]:raise ValueError(('Full formula mismatch',field))
  records.append({'producer':produced,'independent_audit':checked,'seconds':time.monotonic()-t});print(json.dumps({'branch':branch,'clauses':produced['clauses'],'extra':produced['extra_clauses'],'seconds':records[-1]['seconds'],'status':checked['status']}),flush=True)
 result={'status':'VERIFIED_SEVEN_COMPLETE_STRENGTHENED_PHYSICAL_CNFS','records':records,'total_clauses':sum(x['producer']['clauses'] for x in records),'total_extra_clauses':sum(x['producer']['extra_clauses'] for x in records),'total_bytes':sum(x['producer']['bytes'] for x in records),'seconds':time.monotonic()-started,'solver_calls':0}
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=base.DEFAULT);p.add_argument('--work',type=Path,required=True);a=p.parse_args();d=run(a.base.resolve(),a.work);(HERE/'FULL_AUDIT.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='records'}))
