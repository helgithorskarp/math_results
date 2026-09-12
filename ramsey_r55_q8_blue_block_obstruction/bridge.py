"""Check the local refutation as an actual full original-task LRAT refutation."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,importlib.util,json,sys
import encode,reference
from check_lrat import check,steps,require
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dependencies():
 specs=json.loads((HERE/'DEPENDENCIES.json').read_text())
 for spec in specs:
  path=HERE.parent/spec['directory'];require(sha(path/'SHA256SUMS')==spec['manifest_sha256'],'dependency manifest changed')
  for line in (path/'SHA256SUMS').read_text().splitlines():
   digest,name=line.split('  ',1);require(sha(path/name)==digest,'dependency source changed')
 return specs

def run(cache,output):
 dependencies();output=Path(output);output.mkdir(parents=True,exist_ok=False)
 records=encode.catalog(Path(cache)/'r44_11.g6');record=records[516166]
 expected=encode.dimacs(record);require(expected==(HERE/'obstruction.cnf').read_bytes(),'local input mismatch')
 reduced,kinds=reference.formula(record)
 require(reduced==sorted(tuple(sorted(row)) for row in encode.formula(record)),'independent factorized grounding mismatch')
 local=check(HERE/'obstruction.cnf',HERE/'obstruction.lrat')
 parent_dir=HERE.parent/'ramsey_r55_maximal_block_order';sys.path.insert(0,str(parent_dir))
 spec=importlib.util.spec_from_file_location('_q8_blue_ordered',parent_dir/'ordered.py');ordered=importlib.util.module_from_spec(spec);spec.loader.exec_module(ordered)
 rows=[]
 for r in (5,6,7):
  name=f'bo1-q8-r{r}-c516166';directory=output/name;directory.mkdir()
  task,plan,meta=ordered.build(name,cache)
  embedding=list(range(32,43))+list(range(4*r,4*r+4))
  require(len(set(embedding))==15 and min(embedding)>=4*r,'invalid residual injection')
  variable_map={v:task.variables[tuple(sorted((embedding[u],embedding[w])))] for (u,w),v in encode.VARIABLE.items()}
  require(len(set(variable_map.values()))==44,'variable injection')
  for (u,w),color in encode.fixed(record).items():require(task.fixed[tuple(sorted((embedding[u],embedding[w])))]==color,'fixed edge mismatch')
  local_rows=encode.formula(record)
  mapped=[tuple((1 if x>0 else -1)*variable_map[abs(x)] for x in row) for row in local_rows]
  wanted={tuple(sorted(row)) for row in mapped};require(len(wanted)==285,'local duplicate clause')
  for vertices,color,row in encode.physical(record):
   vs=sorted(embedding[v] for v in vertices)
   require(tuple(sorted(task.forbid(vs,color)))==tuple(sorted((1 if x>0 else -1)*variable_map[abs(x)] for x in row)),'literal forbidden-set pullback')
  cnf=directory/'input.cnf';lookup={};h=hashlib.sha256();count=0
  with cnf.open('wb') as out:
   def write(raw):out.write(raw);h.update(raw)
   write(f"p cnf {meta['variables']} {meta['clauses']}\n".encode())
   for count,clause in enumerate(ordered.clauses(task,plan,meta),1):
    key=tuple(sorted(clause))
    if key in wanted and key not in lookup:lookup[key]=count
    write((' '.join(map(str,clause))+' 0\n').encode())
  require(count==meta['clauses'] and len(lookup)==285,'full input dimensions or missing mapped input')
  base_map={i+1:lookup[tuple(sorted(row))] for i,row in enumerate(mapped)}
  def clause_id(i):return base_map[i] if i<=285 else count+i-285
  proof=directory/'proof.lrat'
  with proof.open('w') as out:
   for label,clause,hints in steps(HERE/'obstruction.lrat'):
    # Retaining deleted clauses is sound; omitting deletions avoids touching unrelated parent clauses.
    if clause is None:continue
    line=[str(clause_id(label))]+[str((1 if x>0 else -1)*variable_map[abs(x)]) for x in clause]+['0']+[str(clause_id(i)) for i in hints]+['0']
    out.write(' '.join(line)+'\n')
  receipt=check(cnf,proof)
  require(receipt['input_sha256']==h.hexdigest(),'input changed')
  row=dict(receipt,task=name,status='CERTIFIED_ORIGINAL_TASK_UNSAT',embedding=embedding,variable_map=variable_map,clause_map=base_map,cnf_bytes=cnf.stat().st_size,proof_bytes=proof.stat().st_size)
  row['status']='CERTIFIED_ORIGINAL_TASK_UNSAT';rows.append(row)
  (directory/'JOIN.json').write_text(json.dumps(row,sort_keys=True,indent=2)+'\n')
 result=dict(status='THREE_COMPLETE_ORIGINAL_TASKS_LRAT_REFUTED',original_tasks=rows,new_original_exclusions=3,inherited_exclusions=518,total_exclusions=521,original_registry=2189178,remaining_original_unknown=2188657,physical_q8_jobs_retired=0,local_certificate=local,independent_grounding=kinds,obstruction_structure=reference.wagner_join(record),ramsey_number_decided=False)
 (output/'BRIDGE.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('output');a=p.parse_args();print(json.dumps(run(a.cache,a.output),sort_keys=True,indent=2))
