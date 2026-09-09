"""One fixed four-leaf physical verdict, with no retry or neighboring task."""
import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations, product
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'ramsey_r55_q8_assumption_queue'
UNIT=HERE.parent/'ramsey_r55_q8_root_unit'
sys.path[:0]=[str(PARENT),str(UNIT)]
import basis
import certificate
import task_queue
import worker
import bridge

SOLVER=Path('/scratch/cadical-package/usr/bin/cadical')
CHECKER=Path('/scratch/drat-trim-package/usr/bin/drat-trim')
SOLVER_SHA='c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7'
CHECKER_SHA='bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021'
GUARD=[-810,-819,-824,-832,-833,-836,-842,-856]
ROOT_SHA='326d54a4a9b2abb26c5865536c7bb42d20696c5a59c6c8e1a0d1477465f21c67'
CONFLICTS=100000
WALL_SECONDS=240


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def write_json(path, data):
    with Path(path).open('x') as f:f.write(json.dumps(data,indent=2)+'\n')


def check_dependencies():
    dep=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for p in (PARENT,UNIT):
        if sha(p/'SHA256SUMS')!=dep['source_manifests'][p.name]:
            raise ValueError('Parent manifest identity')
        for line in (p/'SHA256SUMS').read_text().splitlines():
            h,name=line.split('  ',1)
            if sha(p/name)!=h:raise ValueError('Parent source bytes: '+name)
    if sha(SOLVER)!=SOLVER_SHA or sha(CHECKER)!=CHECKER_SHA:
        raise ValueError('Pinned solver/checker executable identity')


def classify(returncode, text):
    statuses=re.findall(r'^s (\S+)\s*$',text,re.M)
    if returncode==10 and statuses==['SATISFIABLE']:return 'SAT'
    if returncode==20 and statuses==['UNSATISFIABLE']:return 'UNSAT'
    if returncode==0 and (statuses in ([],['UNKNOWN'])) and 'UNKNOWN' in text:return 'UNKNOWN'
    raise ValueError('Unrecognized solver exit/status combination')


def solve(cnf, directory, conflicts=CONFLICTS, seconds=WALL_SECONDS):
    """Exclusive STARTED marker prevents automatic re-execution on recovery."""
    d=Path(directory);d.mkdir(exist_ok=False)
    cnf=Path(cnf).resolve()
    command=[str(SOLVER),'--plain','--seed=0','-c',str(conflicts),'-t',str(seconds),str(cnf),str((d/'proof.drat').resolve())]
    write_json(d/'STARTED.json',dict(started_at=datetime.now(timezone.utc).isoformat(),
        command=command,input_sha256=sha(cnf),conflict_limit=conflicts,wall_limit=seconds,
        warning='A STARTED leaf must never be automatically retried'))
    environment={k:v for k,v in os.environ.items() if not k.startswith('CADICAL_')}
    start=time.monotonic()
    with (d/'solver.log').open('x') as log:
        proc=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=environment)
        write_json(d/'PROCESS.json',dict(pid=proc.pid))
        pid,status,usage=os.wait4(proc.pid,0)
        if pid!=proc.pid:raise ValueError('Wrong waited child')
        proc.returncode=os.waitstatus_to_exitcode(status)
    elapsed=time.monotonic()-start
    text=(d/'solver.log').read_text()
    result=classify(proc.returncode,text)
    statistics={}
    for label in ('conflicts','decisions','propagations','restarts'):
        values=re.findall(r'^c '+label+r':\s*([0-9]+)',text,re.M)
        if values:statistics[label]=int(values[-1])
    receipt=dict(status=result,returncode=proc.returncode,wall_seconds=elapsed,
        user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,peak_rss_kib=usage.ru_maxrss,
        input_sha256=sha(cnf),solver_sha256=SOLVER_SHA,command=command,statistics=statistics,
        proof_bytes=(d/'proof.drat').stat().st_size,proof_sha256=sha(d/'proof.drat'),
        proof_status='UNVERIFIED_COMPLETE_TRACE' if result=='UNSAT' else 'NOT_AN_UNSAT_CERTIFICATE')
    write_json(d/'SOLVER_RECEIPT.json',receipt)
    return receipt


def checked_lrat(cnf, directory, nc, assumptions):
    d=Path(directory)
    command=[str(CHECKER),str(cnf),str(d/'proof.drat'),'-i','-U','-t','120','-L',str(d/'proof.lrat')]
    with (d/'checker.log').open('x') as log:
        r=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
    if r.returncode!=0 or 's VERIFIED' not in (d/'checker.log').read_text():
        raise ValueError('No independently verified RUP-only DRAT refutation')
    steps=worker.lrat_steps((d/'proof.lrat').read_text(),nc,len(assumptions))
    write_json(d/'PROOF_RECEIPT.json',dict(status='DRAT_VERIFIED_AND_POSITIVE_HINT_LRAT_PARSED',
        command=command,checker_sha256=CHECKER_SHA,lrat_sha256=sha(d/'proof.lrat'),steps=len(steps)))
    return steps


def mixed_cover(directory, unit_certificate, positive):
    """F entails x, F & A & x entails false, so F & A entails false."""
    if positive.get('r')!=8 or positive.get('edge_cube')!=[119]:
        raise ValueError('Exactly the positive r8 root worker is required')
    unit_receipt=bridge.verify(directory,unit_certificate)
    worker.verify(directory,positive)
    if positive['base_sha256']!=unit_certificate['base_sha256']:
        raise ValueError('Premises must concern the same complete physical base')
    expected=json.loads((PARENT/'EXPECTED.json').read_text())
    stream=Path(directory)/'cores.u64le'
    if sha(stream)!=expected['queue']['files']['cores.u64le']['sha256']:
        raise ValueError('Original catalog stream identity')
    indices=task_queue.matching(task_queue.read_words(stream),positive['core_assumptions'])
    names=[f'bo1-q8-r8-c{k:06d}' for k in indices]
    return dict(format='q8-r8-mixed-original-cover-v1',
        status='CERTIFIED_ORIGINAL_TASK_COVER_WITH_IMPORTED_R45' if names else 'VERIFIED_EMPTY_ORIGINAL_COVER',
        base_sha256=positive['base_sha256'],assumptions=positive['core_assumptions'],
        original_tasks=len(names),task_ids_sha256=hashlib.sha256(''.join(x+'\n' for x in names).encode()).hexdigest(),
        unit_theorem_receipt=unit_receipt,unit_theorem=unit_certificate,positive_refutation=positive,
        trust='R(4,5)<=25 is an explicit premise. This is not a pure-RUP original-task cover.')


def select_edges(directory):
    units={abs(x):x>0 for x in GUARD+[1,119]}
    pos=[0]*857;neg=[0]*857;remaining=0
    for clause in basis.read_cnf(Path(directory)/'q8-r8.cnf'):
        if any(abs(x) in units and units[abs(x)]==(x>0) for x in clause):continue
        c=[x for x in clause if abs(x) not in units]
        if not c:raise ValueError('Unexpected immediate conditioned contradiction')
        remaining+=1;weight=1<<(10-len(c))
        for x in c:
            if 2<=abs(x)<=801 and abs(x) not in units:
                (pos if x>0 else neg)[abs(x)]+=weight
    physical={v:e for e,v in basis.VARIABLES.items()}
    candidates=sorted((v for v in range(2,802) if v not in units),
        key=lambda v:(-min(pos[v],neg[v]),-pos[v]-neg[v],v))
    first=candidates[0]
    second=next(v for v in candidates if not set(physical[v])&set(physical[first]))
    return dict(variables=[first,second],edges=[list(physical[first]),list(physical[second])],
        scores=[dict(variable=v,positive=pos[v],negative=neg[v]) for v in (first,second)],
        remaining_clauses_after_explicit_units=remaining,method='Declared integer short-clause score; a heuristic only')


def prepare(directory, original_positive, output):
    check_dependencies()
    d,out=Path(directory),Path(output);out.mkdir(exist_ok=False)
    if sha(original_positive)!=ROOT_SHA:raise ValueError('Previously prepared positive worker identity')
    words=task_queue.read_words(d/'cores.u64le')
    members=task_queue.matching(words,GUARD)
    if len(members)!=2184:raise ValueError('Declared nonempty original cohort membership')
    selection=select_edges(d);x,y=selection['variables']
    root_raw=Path(original_positive).read_bytes();root_header,root_body=root_raw.split(b'\n',1)
    if root_header!=b'p cnf 946 1502530':raise ValueError('Declared root header')
    leaves=[]
    for i,(sx,sy) in enumerate(product((1,-1),repeat=2)):
        job=dict(r=8,core_assumptions=GUARD,edge_cube=[119,sx*x,sy*y])
        cnf=out/f'leaf-{i}.cnf';receipt=worker.materialize(d,job,cnf)
        expected=b'p cnf 946 1502532\n'+root_body+f'{sx*x} 0\n{sy*y} 0\n'.encode()
        if cnf.read_bytes()!=expected:raise ValueError('Full physical leaf differs from parent plus branch units')
        write_json(out/f'leaf-{i}.job.json',job)
        leaves.append(dict(index=i,job=job,cnf=cnf.name,sha256=receipt['worker_sha256'],status='PENDING'))
    for assignment in product((False,True),repeat=2):
        hits=sum(all(value==(lit>0) for value,lit in zip(assignment,l['job']['edge_cube'][1:])) for l in leaves)
        if hits!=1:raise ValueError('Physical sign partition is not disjoint and exhaustive')
    result=dict(format='q8-r8-cohort0-four-leaf-v1',selection=selection,original_members=len(members),
        original_ids_sha256=hashlib.sha256(''.join(f'bo1-q8-r8-c{k:06d}\n' for k in members).encode()).hexdigest(),
        root_job=dict(r=8,core_assumptions=GUARD,edge_cube=[119]),leaves=leaves,
        partition_assignments_checked=4,all_original_statuses='UNKNOWN',target_solver_calls=0)
    write_json(out/'PREPARED.json',result)
    return result


def small_controls(directory, unit_certificate, output):
    check_dependencies()
    out=Path(output);out.mkdir(exist_ok=False);receipts={}
    for n,conflicts in ((5,1000),(6,1000),(6,1)):
        label=f'r33-{n}-c{conflicts}';edges=list(combinations(range(n),2));variables={e:i+1 for i,e in enumerate(edges)}
        clauses=[]
        for triple in combinations(range(n),3):
            c=[variables[e] for e in combinations(triple,2)];clauses.extend([c,[-x for x in c]])
        cnf=out/(label+'.cnf')
        cnf.write_text(f'p cnf {len(edges)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
        d=out/label;r=solve(cnf,d,conflicts,20)
        want='SAT' if n==5 else 'UNSAT' if conflicts==1000 else 'UNKNOWN'
        if r['status']!=want:raise ValueError('Actual backend control status: '+label)
        if want=='UNSAT':
            proof=checked_lrat(cnf,d,len(clauses),[])
            certificate.checked_transfer(dict(enumerate(clauses,1)),len(clauses),len(edges),[],proof)
        if want=='SAT':
            values={}
            for line in (d/'solver.log').read_text().splitlines():
                if line.startswith('v '):
                    for s in line[2:].split():
                        x=int(s)
                        if x:values[abs(x)]=x>0
            if set(values)!=set(range(1,len(edges)+1)) or not all(any(values[abs(x)]==(x>0) for x in c) for c in clauses):
                raise ValueError('Actual small SAT model failed literal constraints')
        receipts[label]=r
    # Full-base protocol control only: this impossible core K4 matches zero
    # listed original cores. It must never count as an actual cohort closure.
    a=[802,803,804,812,813,821];wanted=[-x for x in a];ident=None
    for i,c in enumerate(basis.read_cnf(Path(directory)/'q8-r8.cnf'),1):
        if c==wanted:ident=i;break
    if ident is None:raise ValueError('Missing exact core-K4 clause')
    meta=worker.metadata(8)
    proof=[dict(clause=[],hints=list(range(meta['clauses']+1,meta['clauses']+7))+[ident])]
    pos=worker.wrap(dict(r=8,core_assumptions=a,edge_cube=[119]),proof)
    cover=mixed_cover(directory,unit_certificate,pos)
    if cover['status']!='VERIFIED_EMPTY_ORIGINAL_COVER' or cover['original_tasks']!=0:
        raise ValueError('An impossible core control must not close actual tasks')
    write_json(out/'EMPTY_COVER_CONTROL.json',cover)
    rejected=0
    for cube in ([],[-119],[119,120]):
        bad=dict(pos,edge_cube=cube)
        try:mixed_cover(directory,unit_certificate,bad)
        except ValueError:rejected+=1
        else:raise ValueError('Wrong physical scope admitted')
    for bad in (dict(pos,r=7),dict(pos,proof=[])):
        try:mixed_cover(directory,unit_certificate,bad)
        except ValueError:rejected+=1
        else:raise ValueError('Invalid positive evidence admitted')
    result=dict(status='PRE_TARGET_CONTROLS_PASSED',actual_small_solver_calls=3,
        checked_small_statuses=['SAT','UNSAT','UNKNOWN'],actual_rup_only_drat_and_lrat_checked=True,
        empty_cover_control_tasks=0,rejected_mixed_admissions=rejected,solver_receipts=receipts)
    write_json(out/'CONTROLS.json',result);return result


def execute(directory, unit_certificate, prepared, controls_directory):
    check_dependencies()
    p=Path(prepared);plan=json.loads((p/'PREPARED.json').read_text())
    controls=json.loads((Path(controls_directory)/'CONTROLS.json').read_text())
    if controls['status']!='PRE_TARGET_CONTROLS_PASSED':raise ValueError('Target calls require completed controls')
    audit=json.loads((p/'AUDIT.json').read_text())
    if audit['status']!='PRE_TARGET_INDEPENDENT_AUDIT_PASSED':raise ValueError('Target calls require the independent full-input audit')
    # Recheck exact partition and job schema immediately before the first solve.
    x,y=plan['selection']['variables']
    if x==y or any(not 2<=v<=801 or v==119 for v in (x,y)):
        raise ValueError('Distinct actual physical split variables')
    if [l['job'] for l in plan['leaves']]!=[dict(r=8,core_assumptions=GUARD,edge_cube=[119,sx*x,sy*y]) for sx,sy in product((1,-1),repeat=2)]:
        raise ValueError('Four complete complementary worker scopes')
    _,raw=worker.base_bytes(directory,8);_,body=raw.split(b'\n',1)
    for leaf in plan['leaves']:
        a=worker.checked_job(leaf['job'])
        expected=f'p cnf 946 {1502521+len(a)}\n'.encode()+body+''.join(f'{v} 0\n' for v in a).encode()
        if (p/leaf['cnf']).read_bytes()!=expected:raise ValueError('Target input is not the exact complete base plus its units')
    del raw,body,expected
    write_json(p/'EXECUTION_SOURCE.json',{name:sha(HERE/name) for name in ['gate.py','audit.py','DEPENDENCIES.json','DECLARED_GATE.json']})
    results=[];proofs={};start=time.monotonic()
    for leaf in plan['leaves']:
        i=leaf['index'];cnf=p/leaf['cnf'];job=leaf['job']
        if sha(cnf)!=leaf['sha256']:raise ValueError('Prepared full input changed')
        d=p/f'solve-{i}';r=solve(cnf,d)
        if r['status']=='SAT':
            candidate=worker.target(directory,job,d/'solver.log')
            write_json(d/'TARGET.json',candidate)
            results.append(dict(index=i,solver=r,verified='GOOD43'))
            break
        if r['status']=='UNSAT':
            steps=checked_lrat(cnf,d,worker.metadata(8)['clauses'],worker.checked_job(job))
            proof=worker.wrap(job,steps);worker.verify(directory,proof)
            write_json(d/'WORKER_CERTIFICATE.json',proof);proofs[i]=proof
        results.append(dict(index=i,solver=r,verified='UNSAT' if i in proofs else 'UNKNOWN'))
        print(json.dumps(dict(completed_leaf=i,status=results[-1]['verified'],wall_seconds=r['wall_seconds'],statistics=r['statistics'])),flush=True)
    outcome='UNKNOWN';original_exclusions=0
    if any(r['verified']=='GOOD43' for r in results):outcome='VERIFIED_GOOD43'
    elif len(proofs)==4:
        first=worker.join(directory,proofs[0],proofs[1]);second=worker.join(directory,proofs[2],proofs[3])
        positive=worker.join(directory,first,second)
        cover=mixed_cover(directory,unit_certificate,positive)
        if cover['original_tasks']!=2184 or cover['task_ids_sha256']!=plan['original_ids_sha256']:
            raise ValueError('Complete cohort original task cover identity')
        write_json(p/'ORIGINAL_COVER.json',cover);outcome=cover['status'];original_exclusions=2184
    result=dict(status=outcome,target_solver_calls=len(results),leaf_results=results,
        certified_unsat_leaves=len(proofs),unresolved_leaves=[r['index'] for r in results if r['verified']=='UNKNOWN'],
        original_task_exclusions=original_exclusions,candidates=int(outcome=='VERIFIED_GOOD43'),
        complete_cohort_members=2184,wall_seconds=time.monotonic()-start,
        total_conflicts=sum(r['solver']['statistics'].get('conflicts',0) for r in results),
        total_solver_wall_seconds=sum(r['solver']['wall_seconds'] for r in results),
        retries=0,next_phase_started=False,scope='Only the existing q8,r8 positive cohort 0, four exhaustive physical leaves')
    write_json(p/'VERDICT.json',result);return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['controls','prepare','execute'])
    parser.add_argument('directory');parser.add_argument('input');parser.add_argument('output');parser.add_argument('--controls')
    args=parser.parse_args()
    if args.command=='prepare':result=prepare(args.directory,args.input,args.output)
    elif args.command=='controls':result=small_controls(args.directory,json.loads(Path(args.input).read_text()),args.output)
    else:result=execute(args.directory,json.loads(Path(args.input).read_text()),args.output,args.controls)
    print(json.dumps(result,indent=2))
