"""Checked original-task bridge. No proof-free receipt retires a parent or child."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,sys
import problem,verify

def map_parent(root,catalog,records):
    root=Path(root).resolve();specs=json.loads((problem.HERE/'DEPENDENCIES.json').read_text())['parent_sources']
    for spec in specs:
        directory=root/spec['directory'];raw=(directory/'SHA256SUMS').read_bytes();problem.require(hashlib.sha256(raw).hexdigest()==spec['manifest_sha256'],'parent manifest')
        for line in raw.decode().splitlines():
            if not line:continue
            h,name=line.split(maxsplit=1);name=name.lstrip('* ');problem.require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==h,'parent source')
    raw=Path(catalog).read_bytes();definition=json.loads((problem.HERE/'CORE.json').read_text());problem.require(hashlib.sha256(raw).hexdigest()==definition['catalog_sha256'] and raw.decode().splitlines()[4]==definition['graph6'],'original core record')
    directory=root/'ramsey_r55_global_maximal_packing';sys.path.insert(0,str(directory));import family
    problem.require(Path(family.__file__).resolve().parent==directory,'wrong original encoder')
    task=family.Task('mp1-q7-r5-c000004',Path(catalog).parent);embedding=list(range(28,43))+list(range(20,28));total=0
    problem.require(set(task.domain(5,6))=={w for w in range(65536) if problem.allowed(w)},'original blue-pair coordinate')
    for record in records:
        rep=record['representative'];fixed,free,var=verify.geometry(rep);raw,rows,supports=verify.literal_formula(rep)
        units={task.variables[20+i,24+j]:rep>>(4*i+j)&1 for i in range(4) for j in range(4)}
        for (u,v),c in fixed.items():
            pair=tuple(sorted([embedding[u],embedding[v]]))
            problem.require((task.fixed[pair] if pair in task.fixed else units[task.variables[pair]])==c,'fixed edge bridge')
        for row,(S,color) in zip(rows,supports):
            physical=sorted(embedding[v] for v in S);source=task.forbid(physical,color);problem.require(source is not None,'missing original physical clause')
            problem.require(len(S)==5 or min(physical)>=20,'original maximality region')
            problem.require(not any(abs(l) in units and units[abs(l)]==int(l>0) for l in source),'incorrect constant substitution')
            reduced=[l for l in source if abs(l) not in units]
            transported=[(1 if l>0 else -1)*task.variables[tuple(sorted(embedding[v] for v in free[abs(l)-1]))] for l in row]
            problem.require(sorted(reduced)==sorted(transported),'original clause image mismatch');total+=1
    return {'original_task':problem.TASK,'all_orbit_types':97,'source_clauses_mapped':total,'blue_matrix_units_per_case':16,'physical_vertices':embedding,'old_root_order_not_added_to_new_formulas':True,'logical_bridge':'Original model -> permissible blue-block relabeling -> a complete tail formula; a checked tail refutation excludes that physical orbit class.'}

def emit(rep,path):
    expected=json.loads((problem.HERE/'EXPECTED.json').read_text());retained=[r['representative'] for r in expected['results'] if r['status'] in ['SAT_TAIL_ONLY','TAIL_UNDECIDED']];problem.require(rep in retained,'not a retained physical unit')
    raw=problem.dimacs(rep,full=True)
    with Path(path).open('xb') as f:f.write(raw)
    return {'original_task':problem.TASK,'representative':rep,'order':43,'bytes':len(raw),'cnf_sha256':hashlib.sha256(raw).hexdigest(),'status':'UNKNOWN','full_physical_edges':903,'input':'All physical K5 prohibitions, entire tail red-K4 exclusion, fixed core/blocks/pair matrix; core-signature order only on the five red blocks.'}

def join(run,checker,root,catalog,full_dir=None):
    checked=verify.verify(run,checker);records=json.loads((problem.HERE/'EXPECTED.json').read_text())['results'];mapped=map_parent(root,catalog,records);unknown=[];closed=[]
    for rep in checked['retained_representatives']:
        directory=None if full_dir is None else Path(full_dir)/f'pair-{rep}'
        if directory is None or not(directory/'proof.drat').exists():unknown.append(rep);continue
        actual=directory/'input.cnf';problem.require(actual.read_bytes()==problem.dimacs(rep,full=True),'full input changed')
        from verify_full import audit
        audit(rep,actual)
        proof=verify.checked_proof(actual,directory/'proof.drat',checker);closed.append({'representative':rep,**proof})
    return {'status':'CERTIFIED_ORIGINAL_TASK_UNSAT' if not unknown else 'CERTIFIED_SUBDIVISION_PARENT_UNKNOWN','original_task':problem.TASK,'original_tasks_excluded':int(not unknown),'physical_tail_refutations':checked['negative_proofs_checked'],'additional_full43_refutations':closed,'unknown_full43_representatives':unknown,'bridge':mapped,'subdivision_verification':checked,'full43_candidate':False,'global_registry_rule':'Subtract one original ID only if status is CERTIFIED_ORIGINAL_TASK_UNSAT; never add physical children to original exclusion counts.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    e=sub.add_parser('emit');e.add_argument('--representative',type=int,required=True);e.add_argument('--output',required=True)
    j=sub.add_parser('join');j.add_argument('--run',required=True);j.add_argument('--drat-trim',required=True);j.add_argument('--parent-root',required=True);j.add_argument('--catalog',required=True);j.add_argument('--full-dir');j.add_argument('--output')
    a=p.parse_args();r=emit(a.representative,a.output) if a.command=='emit' else join(a.run,a.drat_trim,a.parent_root,a.catalog,a.full_dir)
    if a.command=='join' and a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
