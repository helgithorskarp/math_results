"""One complete, restart-safe 362-case pass. Does not rerun completed cases."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time
from encode import catalogue, formula, dimacs, witness, require

HERE = Path(__file__).resolve().parent

def write_json(path, value):
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    temporary.replace(path)

def case(index, args, rows):
    out = args.out/f'{index:06d}'
    out.mkdir(exist_ok=True)
    final = out/'case.json'
    if final.exists():
        return json.loads(final.read_text())
    # A prior started invocation without a final receipt is not restarted.
    # Its possibly completed solver.json can still be independently verified.
    started = out/'STARTED.json'
    recovered = started.exists()
    if not recovered:
        write_json(started,{'index':index,'started_unix':time.time()})
        command = [str(args.python),'-B',str(HERE/'solve_one.py'),str(args.data),str(out),str(index)]
        with (out/'solver.log').open('wb') as log:
            try:
                process = subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=30)
                rc = process.returncode
            except subprocess.TimeoutExpired:
                rc = 'WALL_LIMIT'
        write_json(out/'PROCESS.json',{'returncode':rc,'command':command,'wall_limit':30})
    else:
        rc = 'RECOVERY_NO_RETRY'
    cnf = dimacs(formula(rows[index])[2])
    # This deterministic reconstruction also supplies timeout-case inputs.
    if (out/'input.cnf').exists():
        require((out/'input.cnf').read_bytes()==cnf, 'solver CNF mismatch')
    else:
        (out/'input.cnf').write_bytes(cnf)
    result = {'index':index,'task':f'bo1-q9-r5-c{index:06d}',
              'residual_status':'UNKNOWN','whole_task_status':'UNKNOWN',
              'cnf_sha256':hashlib.sha256(cnf).hexdigest(), 'process_returncode':rc}
    solver_file = out/'solver.json'
    if solver_file.exists():
        s = json.loads(solver_file.read_text())
        require(s['index']==index and s['cnf_sha256']==result['cnf_sha256'],'solver receipt')
        result['solver']=s
        if s['solver_status']=='SAT':
            result['witness_check']=witness(rows[index],s['residual_edgeword'])
            result['residual_status']='SAT'
        elif s['solver_status']=='UNSAT':
            proof = out/'proof.drat'
            require(hashlib.sha256(proof.read_bytes()).hexdigest()==s['proof_sha256'],'proof hash')
            command = [str(args.drat),str(out/'input.cnf'),str(proof),'-i','-t','120',
                       '-c',str(out/'core.cnf'),'-l',str(out/'lemmas.drat')]
            try:
                p = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=125)
                (out/'proof-check.log').write_bytes(p.stdout)
                result['proof_check_returncode']=p.returncode
                if p.returncode==0 and b's VERIFIED' in p.stdout:
                    result['residual_status']='UNSAT_CERTIFIED'
                    result['whole_task_status']='UNSAT_CERTIFIED'
                else:
                    result['proof_check_failure']=True
            except subprocess.TimeoutExpired as e:
                (out/'proof-check.log').write_bytes(e.stdout or b'')
                result['proof_check_failure']='CHECKER_WALL_LIMIT'
    write_json(final,result)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--python',type=Path,default=Path(sys.executable))
    parser.add_argument('--drat',type=Path,required=True)
    args=parser.parse_args()
    args.data=args.data.resolve();args.out=args.out.resolve()
    args.out.mkdir(exist_ok=True)
    rows=catalogue(args.data)
    cases=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs=[pool.submit(case,i,args,rows) for i in range(362)]
        for future in as_completed(jobs):
            r=future.result();cases.append(r)
            print(json.dumps({'done':len(cases),'index':r['index'],'residual':r['residual_status'],
                              'closures':sum(x['whole_task_status']=='UNSAT_CERTIFIED' for x in cases)},sort_keys=True),flush=True)
    cases.sort(key=lambda r:r['index'])
    require([x['index'] for x in cases]==list(range(362)),'complete registry')
    counts={s:sum(x['residual_status']==s for x in cases) for s in ('SAT','UNSAT_CERTIFIED','UNKNOWN')}
    result={'family':'all 362 bo1-q9-r5 tasks','counts':counts,'whole_task_closures':counts['UNSAT_CERTIFIED'],
            'gate_pass':counts['UNSAT_CERTIFIED']>0,'good43_found':False,
            'whole_registry_total':2189178,'prior_q7_r5_closures':518,
            'whole_registry_unknown':2189178-518-counts['UNSAT_CERTIFIED'],'cases':cases}
    write_json(args.out/'RESULT.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},sort_keys=True),flush=True)

if __name__=='__main__':
    main()
