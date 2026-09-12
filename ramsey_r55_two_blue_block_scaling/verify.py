"""Complete receiving check: all positive graphs and actual negative LRAT."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,subprocess,sys
import model
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(model.PRIOR))
import check_lrat

def need(x,s):
 if not x:raise ValueError(s)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dependencies():
 specs=json.loads((HERE/'DEPENDENCIES.json').read_text())
 for row in specs:
  directory=HERE.parent/row['directory'];need(sha(directory/'SHA256SUMS')==row['manifest_sha256'],'dependency manifest')
  for line in (directory/'SHA256SUMS').read_text().splitlines():
   digest,name=line.split('  ',1);need(sha(directory/name)==digest,'dependency source changed')

def negative(catalog,output):
 """Lift the existing actual 15-vertex proof to the current complete 19 input."""
 output=Path(output);output.mkdir(exist_ok=False)
 record=model.catalog(catalog)[516166]
 cnf=output/'input.cnf';cnf.write_bytes(model.dimacs(record))
 local_rows=model.prior.formula(record);rows=[c for _,_,c in model.physical(record)]
 need(len(rows)==len({tuple(sorted(c)) for c in rows}),'duplicate new clauses')
 indices={tuple(sorted(c)):i+1 for i,c in enumerate(rows)}
 variable_map={v:model.VARIABLE[p] for p,v in model.prior.VARIABLE.items()}
 clause_map={}
 for i,clause in enumerate(local_rows,1):
  mapped=tuple(sorted((1 if x>0 else -1)*variable_map[abs(x)] for x in clause))
  need(mapped in indices,'old forbidden set absent from full current formula');clause_map[i]=indices[mapped]
 def rename(i):return clause_map[i] if i<=285 else len(rows)+i-285
 proof=output/'proof.lrat'
 with proof.open('w') as out:
  for label,clause,hints in check_lrat.steps(model.PRIOR/'obstruction.lrat'):
   if clause is None:continue
   out.write(' '.join([str(rename(label))]+[str((1 if x>0 else -1)*variable_map[abs(x)]) for x in clause]+['0']+[str(rename(h)) for h in hints]+['0'])+'\n')
 result=check_lrat.check(cnf,proof)
 result.update(core=516166,scope='complete 19-vertex two-blue-block input',injection=list(range(15)),variable_map=variable_map,clause_map=clause_map)
 (output/'NEGATIVE.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return result

def run(catalog,classification,output,checker=None):
 dependencies();records=model.catalog(catalog);classification=Path(classification);output=Path(output);output.mkdir(parents=True,exist_ok=False)
 blocked=[int(x) for x in (classification/'BLOCKED_IDS.txt').read_text().split()]
 need(blocked==[516166],'any additional blocked core requires a new checked refutation')
 need((classification/'witnesses.u112le').stat().st_size==14*len(records),'witness stream size')
 if checker is None:
  checker=output/'check_witnesses'
  subprocess.run(['g++','-O2','-std=c++17','-Wall','-Wextra','-Wpedantic',str(HERE/'check_witnesses.cpp'),'-o',str(checker)],check=True)
 proc=subprocess.run([str(checker),str(catalog),str(classification/'witnesses.u112le'),str(classification/'BLOCKED_IDS.txt')],capture_output=True,text=True,check=True)
 positive=json.loads(proc.stdout);need(positive['sat']==546355 and positive['unsat_requiring_certificates']==1,'positive complete coverage')
 neg=negative(catalog,output/'negative')
 current={f'bo1-q8-r{r}-c{c:06d}' for r in (5,6) for c in blocked}
 old=json.loads((model.PRIOR/'ORIGINALS.json').read_text())
 previous={r['task'] for r in old['new_original_exclusions']}
 new=sorted(current-previous);need(not new,'unexpected new original exclusion requires separate parent admission')
 result=dict(status='COMPLETE_TWO_BLUE_BLOCK_CLASSIFICATION_NO_NEW_ORIGINAL_EXCLUSIONS',positive=positive,negative=neg,blocked_cores=blocked,witness_sha256=sha(classification/'witnesses.u112le'),witness_bytes=14*len(records),original_scope=dict(parameters=['q8,r5','q8,r6'],all_original_ids=2*len(records),excluded_by_fragment=sorted(current),already_source_certified=sorted(current&previous),new_exclusions=new,retained_original_ids_with_verified_necessary_fragments=2*positive['sat'],physical_cohorts_retired=0),scaling_gate='FAILED_NO_ADDITIONAL_ORIGINAL_REDUCTION',original_registry_source_certified_exclusions=521,original_registry_source_certified_unknown=2188657,ramsey_bounds_changed=False)
 (output/'VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('classification');p.add_argument('output');p.add_argument('--checker');a=p.parse_args();r=run(a.catalog,a.classification,a.output,a.checker);print(json.dumps(dict(status=r['status'],new_original_exclusions=len(r['original_scope']['new_exclusions']),positive=r['positive']),indent=2))
