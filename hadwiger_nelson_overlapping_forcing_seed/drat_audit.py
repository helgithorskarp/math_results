"""Optional independent SAT/DRAT audit of the equal-pair obstruction."""
import argparse,json,hashlib,subprocess,time
from pathlib import Path
from itertools import combinations
from verify import edges
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--checker',type=Path,required=True);args=parser.parse_args()
    from pysat.solvers import Glucose3
    x=json.loads((ROOT/'certificate.json').read_text())['equal'];n=len(x['points']);es=edges(x['points'],x['denominator'])
    clauses=[]
    for v in range(n):
        clauses.append([4*v+c+1 for c in range(4)])
        for c,d in combinations(range(4),2):clauses.append([-4*v-c-1,-4*v-d-1])
    for a,b in es:
        for c in range(4):clauses.append([-4*a-c-1,-4*b-c-1])
    clauses.extend([[1],[6]])
    data=f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    w=ROOT/'out';w.mkdir(exist_ok=True);cnf=w/'equal.cnf';proof=w/'equal.drat';cnf.write_text(data);t=time.monotonic()
    s=Glucose3(bootstrap_with=clauses,with_proof=True);s.conf_budget(1500000)
    if s.solve_limited(expect_interrupt=True) is not False:raise ValueError('No completed UNSAT proof')
    proof.write_text('\n'.join(s.get_proof())+'\n');s.delete()
    with (w/'drat_check.log').open('w') as f:
        p=subprocess.run([str(args.checker.resolve()),str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
    if p.returncode!=0 or 's VERIFIED' not in (w/'drat_check.log').read_text():raise ValueError('Proof checker rejected trace')
    sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    print(json.dumps({'vertices':n,'edges':len(es),'variables':4*n,'clauses':len(clauses),'cnf_sha256':sha(cnf),'drat_sha256':sha(proof),'drat_bytes':proof.stat().st_size,'status':'UNSAT_DRAT_VERIFIED','seconds':time.monotonic()-t},sort_keys=True))
if __name__=='__main__':main()
