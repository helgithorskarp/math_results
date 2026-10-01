"""Run independent signed-set RUP replay and compare exact reference counts."""
import argparse
import json
from pathlib import Path
import resource
import sys
import time

from rup import need, verify


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--case-dir',type=Path,required=True)
    p.add_argument('--author-expected',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();began=time.monotonic()
    rows=json.loads(args.author_expected.read_text())['cases']
    need([z['length'] for z in rows]==list(range(2,19)),'Complete seventeen-case cover')
    results=[]
    for reference in rows:
        length=reference['length']
        cnf,proof=[args.case_dir/f'run-{length}.{suffix}' for suffix in ['cnf','lrat']]
        result=verify(cnf,proof)
        for ours,theirs in [('variables','variables'),('input_clauses','initial_clauses'),
                           ('RUP_additions','checked_additions'),('deletions','deleted_clauses'),
                           ('hint_reads','propagation_hints_checked'),('CNF_sha256','cnf_sha256')]:
            need(result[ours]==reference[theirs],'Exact reference result: '+ours)
        result['length']=length
        result['reference_proof_byte_match']=result['LRAT_sha256']==reference['proof_sha256']
        results.append(result)
        print('Case '+str(length)+' independent RUP verified',flush=True)
    result={'agent':'six-reviewer-5','role':'independent reviewer',
            'status':'ALL_SEVENTEEN_SIGNED_SET_RUP_REFUTATIONS_VERIFIED',
            'cases':results,'RUP_additions':sum(z['RUP_additions'] for z in results),
            'hint_reads':sum(z['hint_reads'] for z in results),'optimization':sys.flags.optimize,
            'python':sys.version.split()[0],'seconds':time.monotonic()-began,
            'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':
    main()
