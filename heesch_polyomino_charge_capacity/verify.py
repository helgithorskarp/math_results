"""Regenerate all27 conditional exclusions and the final capacity contradiction."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import time

from atlas import BASE,ROOT,pool,formula
from corner_selector import corner_formula
from oracle import require,run_geometry,boundary_disc,translated


def unit_contradiction(clauses):
    remaining=[set(c) for c in clauses];assigned={}
    while True:
        if any(not c for c in remaining):return True
        units=[next(iter(c)) for c in remaining if len(c)==1]
        if not units:return False
        for literal in units:
            variable=abs(literal);truth=literal>0
            if variable in assigned and assigned[variable]!=truth:return True
            assigned[variable]=truth
        following=[]
        for clause in remaining:
            if any(abs(z) in assigned and assigned[abs(z)]==(z>0) for z in clause):continue
            following.append({z for z in clause if abs(z) not in assigned})
        remaining=following


def check_unsat(nv,clauses,expected,work,checker):
    work.mkdir(parents=True,exist_ok=True)
    cnf,trace=work/'formula.cnf',work/'proof.drat'
    cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    digest=hashlib.sha256(cnf.read_bytes()).hexdigest()
    require((nv,len(clauses),digest)==(expected['nv'],expected['clauses'],expected['cnf_sha256']),
            'regenerated formula differs from the compact certificate')
    from pysat.solvers import Solver
    with Solver(name='glucose4',bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(10000);decision=solver.solve_limited()
        require(decision is False,'native decision is SAT or UNKNOWN; no exclusion')
        trace.write_text('\n'.join(solver.get_proof() or ['0'])+'\n');stats=solver.accum_stats()
    if trace.read_text()=='0\n':require(unit_contradiction(clauses),'trivial native trace lacks input unit contradiction')
    checked=subprocess.run([str(checker.resolve()),str(cnf),str(trace)],capture_output=True,text=True,timeout=30)
    log=checked.stdout.replace('\r','\n');(work/'checker.log').write_text(log+checked.stderr)
    require(checked.returncode in (0,1) and 's VERIFIED' in log.splitlines(),'DRAT contradiction was not independently verified')
    return {'nv':nv,'clauses':len(clauses),'cnf_sha256':digest,'status':'UNSAT VERIFIED',
            'proof_bytes':trace.stat().st_size,'proof_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),
            'native_stats':stats}


def halo_instance(tile,codes):
    from extension import inventory,independent_inventory,build_formula,scale_cells,load_dependencies
    from corners import footprint,variants
    shapes=variants(tile);root=sorted({p for i,x,y in codes for p in footprint(shapes[i],(x,y))})
    require(boundary_disc(root),'half-grid theorem requires a disc fixed union')
    cover,motion=load_dependencies(ROOT/'heesch_polyomino_euler_cnf',ROOT/'heesch_polyomino_motion_bridge')
    root2,tile2=scale_cells(root),scale_cells(tile)
    candidates,halo,owners,stats=inventory(root2,tile2,cover,motion)
    separate_halo,separate_candidates=independent_inventory(root2,tile2,motion)
    require(halo==separate_halo and {(q['shape'],q['tx'],q['ty']) for q in candidates}==separate_candidates,
            'complete doubled-grid inventories disagree')
    circuit=build_formula(candidates,halo,owners)
    return circuit,stats


def native_phase(work,checker):
    directory=Path(__file__).resolve().parent
    expected=json.loads((directory/'expected.json').read_text())
    data=json.loads((BASE/'pairs.json').read_text());atlas=pool(data)
    require(expected['tile']==data['tile'],'tile provenance mismatch')
    require((len(atlas['incoming_codes']),len(atlas['root_excluded']),len(atlas['conflicts']))
            ==(expected['incoming_count'],expected['root_excluded'],expected['conflicts']),'atlas summary mismatch')
    nv,clauses=formula(atlas,expected['threshold']);results=[]
    for index,record in enumerate(expected['cases']):
        providers=record['providers']
        require(providers==sorted(set(providers)) and all(type(i) is int and 0<=i<56 for i in providers),'invalid conditional selector')
        codes=[(atlas['root_orientation'],0,0)]+[atlas['incoming_codes'][i] for i in providers]
        if record['mode']=='corners':
            candidates,_,_,instance=corner_formula(atlas['tile'],codes);variables=len(candidates)
        elif record['mode']=='halo':
            circuit,stats=halo_instance(atlas['tile'],codes);variables,instance=circuit.nv,circuit.clauses
            require((stats['candidates'],stats['candidate_sha256'],stats['required_halo_cells'])
                    ==(record['candidates'],record['candidate_sha256'],record['required_halo_cells']),
                    'doubled-grid inventory summary changed')
        else:raise ValueError('unknown conditional exclusion mode')
        result=check_unsat(variables,instance,record,work/f'case_{index:02d}',checker)
        results.append({'providers':providers,'mode':record['mode'],**result})
        # This cut is legal only after the whole simultaneous surrounding relaxation is refuted.
        clauses.append([-i-1 for i in providers])
    final=check_unsat(nv,clauses,expected['outer_final'],work/'outer_final',checker)
    return {'agent':'six-heesch-1','role':'researcher','conditional_exclusions':results,
            'outer_final':final,'checked_contradictions':len(results)+1,
            'claim':'root and all incoming providers interior implies c(root)<=6'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=('geometry','native'),required=True)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--checker',type=Path)
    args=parser.parse_args();start=time.monotonic()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name]='1'
    if args.phase=='geometry':summary=run_geometry()
    else:
        require(args.checker is not None and args.checker.is_file(),'provide the independent checker binary')
        summary=native_phase(args.work,args.checker)
    summary.update({'agent':'six-heesch-1','role':'researcher','phase':args.phase,
                    'seconds':round(time.monotonic()-start,3),'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    args.work.mkdir(parents=True,exist_ok=True)
    (args.work/(args.phase+'_summary.json')).write_text(json.dumps(summary,indent=2)+'\n')
    if args.phase=='native':print(json.dumps({k:v for k,v in summary.items() if k!='conditional_exclusions'},indent=2))
    else:print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
