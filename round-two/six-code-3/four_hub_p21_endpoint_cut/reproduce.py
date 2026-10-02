"""Complete sequential producer, independent reconstruction, and physical cuts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import produce
import cuts
import verify_cuts
import controls

def need(condition,message):
    if not condition:raise ValueError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    need(not args.work.exists(),'fresh scratch directory required')
    args.work.mkdir(parents=True)
    here=Path(__file__).resolve().parent
    opts=['-O'] if sys.flags.optimize else []
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    for program,output in (('produce.py','producer.json'),('verify.py','independent.json')):
        subprocess.run([sys.executable,*opts,str(here/program),'--out',str(args.work/output)],check=True,timeout=60,env=env)
    first=(args.work/'producer.json').read_bytes();second=(args.work/'independent.json').read_bytes()
    need(first==second,'all physical rows, types, branches and populations differ')
    result=json.loads(first);inventory=result['inventory']
    need(produce.canonical(inventory)==produce.canonical(json.loads((here/'expected.json').read_text())),'frozen full inventory mismatch')
    actual=cuts.certificates(inventory)
    certificate=json.loads((here/'certificate.json').read_text())
    need(produce.canonical(actual)==produce.canonical(certificate),'all frozen physical cut records differ')
    independent=verify_cuts.verify_all(inventory,certificate)
    controlled=controls.run(json.loads((here/'fixtures.json').read_text()),inventory,certificate)
    summary=dict(agent='six-code-3',role='researcher',status='AUTHOR_CHECKED_CONDITIONAL_EXACT_CERTIFICATE',
                 physical_rows=len(result['rows']),statistic_types=len(inventory['types']),
                 full_producer_independent_sha256=hashlib.sha256(first).hexdigest(),
                 inventory_sha256=produce.digest(inventory),certificate_sha256=cuts.digest(certificate),
                 independent_physical_check=independent,controls=controlled)
    encoded=json.dumps(summary,sort_keys=True,indent=2).encode()+b'\n'
    (args.work/'RESULT.json').write_bytes(encoded)
    print(json.dumps(dict(RESULT_sha256=hashlib.sha256(encoded).hexdigest(),
                         four_hub_pair_total_lower_bound=21,
                         examined_unit_graphs=independent['examined_unit_graphs'],
                         controls=controlled['checks_count'])))

if __name__=='__main__':main()
