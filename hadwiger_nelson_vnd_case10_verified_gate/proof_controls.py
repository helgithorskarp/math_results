"""Truth-table and mutation controls for the strict checker, with no SAT queries."""
from pathlib import Path
from itertools import combinations,permutations,product
import argparse,subprocess,json,hashlib,time

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--checker',type=Path,required=True);a=ap.parse_args();w=a.work.resolve();p=w/'strict_proof_controls';p.mkdir(parents=True,exist_ok=True);checker=a.checker.resolve();start=time.monotonic()
 def run(cnf,proof):
  c=p/'control.cnf';l=p/'control.lrat';c.write_text(cnf);l.write_text(proof)
  r=subprocess.run([str(checker),str(c),str(l)],capture_output=True,text=True,timeout=10)
  if r.returncode not in (0,1):raise ValueError('checker crash')
  return r.returncode==0 and 'VERIFIED_STRICT_RUP_LRAT' in r.stdout.splitlines()
 square='p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n'
 cases=[('valid_original_units','p cnf 1 2\n1 0\n-1 0\n','3 0 1 2 0\n',True),('valid_derived_unit',square,'5 1 0 1 2 0\n6 0 5 3 4 0\n',True),('invalid_RUP_step',square,'5 1 0 1 0\n6 0 5 3 4 0\n',False),('false_refutation_of_SAT','p cnf 1 1\n1 0\n','2 0 1 0\n',False),('empty_hint_false_refutation','p cnf 1 1\n1 0\n','2 0 0\n',False),('deleted_hint','p cnf 1 2\n1 0\n-1 0\n','2 d 2 0\n3 0 1 2 0\n',False),('negative_RAT_hint','p cnf 1 1\n1 0\n','2 0 -1 0\n',False),('missing_final_empty',square,'5 1 0 1 2 0\n',False)]
 for name,c,f,want in cases:
  if run(c,f)!=want:raise ValueError('wrong result '+name)
 base=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)];total=sat_count=accepted=0
 for m in range(5):
  for subset in combinations(base,m):
   sat=any(all(any(bits[abs(x)-1]==(x>0) for x in c) for c in subset) for bits in product((False,True),repeat=2))
   cnf=f'p cnf 2 {m}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in subset)
   for order in permutations(range(1,m+1)):
    f=f'{m+1} 0 '+(' '.join(map(str,order))+' ' if order else '')+'0\n';good=run(cnf,f);total+=1;sat_count+=sat;accepted+=good
    if sat and good:raise ValueError('accepted refutation of satisfiable truth-table instance')
 out={'verified':True,'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'named_controls':len(cases),'named_positive_controls':2,'named_negative_controls':6,'truth_table_instances_and_hint_orders':total,'satisfiable_cases_all_rejected':sat_count,'accepted_cases_all_truth_table_UNSAT':accepted,'SAT_queries':0,'elapsed_seconds':time.monotonic()-start};(w/'proof_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
