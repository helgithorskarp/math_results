"""Public exact replay; optionally audit or regenerate complete physical CNFs."""
from pathlib import Path
import argparse,json,time
import base,audit,check_global,full_audit,accept_model,carrier
HERE=Path(__file__).resolve().parent

def replay(parent_path,cnfs=None):
 result=audit.audit(parent_path)
 expected=json.loads((HERE/'INTERFACE_AUDIT.json').read_text())
 if result!=expected:raise ValueError('Expected interface audit differs')
 b=result['global_bound']
 if not 6*b['new_representation_count']<b['parent_physical_count'] or b['new_representation_count']>=1<<785:raise ValueError('Exact final inequalities')
 parent=base.load(parent_path);bad=0
 for text in ('s UNKNOWN\n','s UNSATISFIABLE\n','s SATISFIABLE\nv 1 0\n'):
  try:accept_model.accept([5,1,2],text,parent)
  except ValueError:bad+=1
  else:raise ValueError('Invalid target accepted')
 family=carrier.Carrier(parent);example=family.unrank(0);p=parent['model'].Packing(example['parameters']['branch']);a=parent['verify_target'].adjacency(example['graph']);values=[1]+[v if a[u][w] else -v for (u,w),v in p.variables.items()];text='s SATISFIABLE\nv '+' '.join(map(str,values))+' 0\n'
 try:accept_model.accept(example['parameters']['branch'],text,parent)
 except ValueError:bad+=1
 else:raise ValueError('Known nontarget accepted')
 formula_records=[]
 if cnfs is not None:
  records=json.loads((HERE/'FULL_AUDIT.json').read_text())['records']
  for row in records:
   branch=row['producer']['branch'];path=Path(cnfs)/('branch-'+'-'.join(map(str,branch))+'.cnf');checked=check_global.audit_file(branch,path)
   if checked!=row['independent_audit']:raise ValueError('Full public CNF replay mismatch')
   formula_records.append(checked)
 return {'status':'VERIFIED_GLOBAL_GREEDY_CLOSURE_PUBLIC_REPLAY','branches':39,'target_decoder_negative_controls':bad,'interface_audit':result,'full_formulas_audited':len(formula_records),'full_clauses_audited':sum(x['clauses'] for x in formula_records),'target_found':False,'target_solver_calls':0}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=base.DEFAULT);p.add_argument('--cnfs',type=Path);p.add_argument('--generate-cnfs',type=Path);p.add_argument('--record',type=Path);a=p.parse_args();start=time.monotonic()
 if a.generate_cnfs:
  d=full_audit.run(a.base.resolve(),a.generate_cnfs);wanted=json.loads((HERE/'FULL_AUDIT.json').read_text())
  if [r['independent_audit'] for r in d['records']]!=[r['independent_audit'] for r in wanted['records']]:raise ValueError('Regenerated full formulas differ')
 result=replay(a.base.resolve(),a.cnfs);record={'seconds':time.monotonic()-start,'result':result}
 if a.record:
  if a.record.exists():raise ValueError('Replay record exists')
  a.record.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'seconds':record['seconds'],**{k:v for k,v in result.items() if k!='interface_audit'}},sort_keys=True))
