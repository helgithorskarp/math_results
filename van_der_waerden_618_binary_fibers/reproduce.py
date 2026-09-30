"""Sequential exact reproduction; all generated corpora remain in build/."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import urllib.request

from check_coloring import cyclic_report, interval_report
from check_rup_lrat import verify
from encode import candidate, encoding, local_table, static_cost
from rup_controls import controls as rup_controls

ROOT=Path(__file__).resolve().parent
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def require(ok,message):
    if not ok:raise RuntimeError(message)


def run(args,stdin=None,seconds=30,expected=0):
    result=subprocess.run(list(map(str,args)),input=stdin,text=True,capture_output=True,env=ENV,timeout=seconds)
    require(result.returncode==expected,f'child failed: {args}: {result.stderr}')
    return result.stdout


def solve(name,build,conflicts,stem):
    from pysat.solvers import Solver
    case=json.loads((ROOT/'cases.json').read_text())[name]
    lines=(build/f'{name}.cnf').read_text().splitlines()
    clauses=[list(map(int,line.split()[:-1])) for line in lines[1:]]
    preferences=[(i+1)*(1 if bit else -1) for i,bit in enumerate(case['initial_u'])]
    with Solver(name='cadical195',bootstrap_with=clauses,with_proof=True) as solver:
        solver.set_phases(preferences);solver.conf_budget(conflicts)
        status=solver.solve_limited();statistics=solver.accum_stats()
        proof=model=None
        if status is False:
            libc=ctypes.CDLL(None);libc.fflush.argtypes=[ctypes.c_void_p];libc.fflush.restype=ctypes.c_int
            require(libc.fflush(None)==0,'proof stream flush failed');proof=solver.get_proof()
        elif status is True:model=solver.get_model()
    if proof is not None:(build/f'{stem}.drat').write_text('\n'.join(proof)+'\n')
    if model is not None:
        values={abs(v):int(v>0) for v in model}
        require(all(any(values[abs(v)]==int(v>0) for v in c) for c in clauses),'bad solver assignment')
        (build/f'{stem}.u.bits').write_text(''.join(str(values[i]) for i in range(1,104))+'\n')
    print(json.dumps({'status':'UNSAT_PENDING_CHECK' if status is False else 'SAT_PENDING_CHECK' if status is True else 'UNKNOWN',
                      'statistics':statistics,'conflict_budget':conflicts,'mathematical_exclusion':False}))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--builddir',type=Path,default=ROOT/'build')
    parser.add_argument('--converter-source',type=Path)
    parser.add_argument('--sanitizers',action='store_true')
    parser.add_argument('--solve',choices=['product','one_exception','dense622'])
    parser.add_argument('--conflicts',type=int,default=50000)
    parser.add_argument('--stem')
    args=parser.parse_args();build=args.builddir.resolve();build.mkdir(parents=True,exist_ok=True)
    if args.solve:solve(args.solve,build,args.conflicts,args.stem or args.solve);return
    start=time.monotonic();expected=json.loads((ROOT/'expected.json').read_text());cases=json.loads((ROOT/'cases.json').read_text())
    proof_controls=rup_controls()
    require(proof_controls['status']=='RUP_TRUTH_TABLE_AND_REJECTION_CONTROLS_PASSED','RUP controls failed')
    flags=['-O1','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if args.sanitizers else ['-O2']
    for name in ['direct_skeleton_profiles','direct_encode']:
        run(['g++','-std=c++17','-Wall','-Wextra','-Wconversion','-Wshadow',*flags,ROOT/f'{name}.cpp','-o',build/name])
    table,table_meta=local_table();native=run([build/'direct_skeleton_profiles']).encode()
    require(table==native,'complete2187*64 local table differs')
    require(sha(table)==expected['local_table_sha256'] and table_meta['profiles']==expected['local_profiles'],'local reference changed')
    summaries={}
    for name,case in cases.items():
        cnf,weighted,meta=encoding(case['tau'])
        stdin='103\n'+' '.join(map(str,case['tau']))+'\n'
        require(cnf==run([build/'direct_encode','cnf'],stdin).encode(),'complete independent CNF differs')
        require(weighted==run([build/'direct_encode','weighted'],stdin).encode(),'complete independent weighted edges differ')
        (build/f'{name}.cnf').write_bytes(cnf);(build/f'{name}.weighted').write_bytes(weighted)
        want=expected['expected_cases'][name]
        require(meta['nae_edges']==want['nae_edges'],'edge reference changed')
        u=case['candidate_u'];count,cost=static_cost(weighted,u)
        require((count,cost)==(want['unweighted_violations'],want['static_cost']),'candidate reference cost changed')
        period=candidate(case['tau'],u)
        require(period[309:]==[1-v for v in period[:309]],'decoder lost anti-period')
        cyclic=cyclic_report(period);integer=interval_report([period[t%618] for t in range(3704)])
        require(cyclic['cyclic_progression_pairs_checked']==381306 and integer['interval_progressions_checked']==1141450,'incomplete checker coverage')
        require(cyclic['monochromatic_cyclic_pairs']==4*cost==want['cyclic_pairs'],'cyclic objective identity failed')
        require(integer['monochromatic_interval_progressions']==want['interval_APs'] and not integer['verified'],'candidate status/reference changed')
        summaries[name]={**meta,'cnf_sha256':sha(cnf),'weighted_sha256':sha(weighted),
                         'candidate_static_cost':cost,'candidate_unweighted_violations':count,
                         'cyclic_check':cyclic,'integer_check':integer,'candidate_status':'INVALID'}
        print(json.dumps({'case':name,'status':'EXACT_FULL_ENTRY_COMPARISON_PASSED','nae_edges':meta['nae_edges'],'candidate_static_cost':cost}),flush=True)
    for stdin,message in [('2\n','header'),('103\n0\n','truncated'),('103\n'+'3 '*103+'\n','invalid'),
                          ('103\n'+'0 '*103+'\nextra\n','trailing')]:
        result=subprocess.run([str(build/'direct_encode'),'cnf'],input=stdin,text=True,capture_output=True,env=ENV,timeout=30)
        require(result.returncode==2 and message in result.stderr and not result.stdout,'malformed tau accepted')
    converter=expected['drat_converter']['files']['drat-trim.c'];source=build/'drat-trim.c'
    if args.converter_source:source.write_bytes(args.converter_source.read_bytes())
    elif not source.exists():source.write_bytes(urllib.request.urlopen(converter['url'],timeout=15).read())
    require(sha(source.read_bytes())==converter['sha256'],'wrong pinned converter source')
    run(['gcc','-O2','-std=gnu99',source,'-o',build/'drat-trim'])
    discovery=json.loads(run([sys.executable,ROOT/'reproduce.py','--solve','dense622','--builddir',build]))
    require(discovery['status']=='UNSAT_PENDING_CHECK','no complete proof; no exclusion')
    output=run([build/'drat-trim',build/'dense622.cnf',build/'dense622.drat','-t','30','-L',build/'dense622.lrat'])
    require('s VERIFIED' in output,'proof conversion/check failed')
    checked=verify(build/'dense622.cnf',build/'dense622.lrat')
    require(checked['cnf_sha256']==expected['dense622_RUP']['cnf_sha256'],'proof uses different fiber')
    checked['reference_proof_byte_match']=checked['proof_sha256']==expected['dense622_RUP']['proof_sha256']
    partial=json.loads(run([sys.executable,ROOT/'reproduce.py','--solve','dense622','--builddir',build,'--conflicts','1','--stem','dense622-incomplete']))
    require(partial['status']=='UNKNOWN' and not (build/'dense622-incomplete.drat').exists(),'budget control supplied a false certificate')
    result={'agent':'six-vdw-1','role':'researcher','status':'VERIFIED_ALL_BINARY_FIBER_CLAIMS',
            'local_classification':table_meta,'local_table_sha256':sha(table),'cases':summaries,
            'dense622_exclusion':checked,'malformed_tau_rejections':4,'RUP_controls':proof_controls,
            'budget_control_UNKNOWN':True,'generic_constraint_bounds':[42024,94554],
            'nonconstant_skeleton_constraint_lower_bound':43044,'length3704_witness':False,
            'product_excluded':False,'one_exception_excluded':False,'sanitizers':args.sanitizers,
            'seconds':time.monotonic()-start,'peak_parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (build/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','local_classification','RUP_controls']}))


if __name__=='__main__':main()
