"""Reproduce the complete 105-edge C3 exclusion with a compact stable manifest."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def compact(work):
    roots = json.loads((work/'local_roots.json').read_text())
    incidence = json.loads((work/'incidences.json').read_text())
    completion = json.loads((work/'completions.json').read_text())
    independent = json.loads((work/'independent.json').read_text())
    controls = json.loads((work/'controls.json').read_text())
    optimized_controls = json.loads((work/'controls_optimized.json').read_text())
    require(controls==optimized_controls,'optimized Python bypassed a guard or changed a predicate')
    require(completion['status']=='COMPLETE' and completion['outside_complete'] and not completion['valid_completions'],
            'producer completion is incomplete or has a valid graph')
    require(independent['status']=='EXACT_INDEPENDENT_EXCLUSION' and independent['mathematical_exclusion'] and
            independent['valid_completions']==0,'independent exclusion did not pass')
    require(all(case['status']=='COMPLETE' for case in incidence),'incidence enumeration incomplete')
    require(completion['cross_assignments']==8**6,'outside cross-word coverage incomplete')
    root_summary = [{k:v for k,v in case.items() if k not in ('pair_groups','triple_groups')} for case in roots]
    incidence_summary = []
    for case in incidence:
        record = {k:v for k,v in case.items() if k not in ('incidence_representatives','nodes')}
        normalized = sorted(case['incidence_representatives'])
        record['template_sha256']=digest(normalized)
        incidence_summary.append(record)
    completion_summary = [{k:v for k,v in case.items() if k!='per_incidence'} for case in completion['cases']]
    independent_summary = [{k:v for k,v in case.items() if k!='per_incidence'} for case in independent['cases']]
    return dict(schema=1,claim='No ordinary valid 22-vertex C3 graph with 105 edges, maximum red degree 10, and fixed red degree 9',
                roots=root_summary,incidences=incidence_summary,outside_profiles=completion['outside_profiles'],
                completion_cases=completion_summary,independent_cases=independent_summary,
                controls=controls,totals=dict(degree_placements=len(roots),canonical_local_roots=len(incidence),
                incidence_representatives=sum(case['representatives'] for case in incidence),
                outside_degree_profiles=len(completion['outside_profiles']),
                outside_cross_assignments=completion['cross_assignments'],
                completions_considered=sum(case['completions_considered'] for case in completion['cases']),
                producer_forced_rejections=sum(case['forced_rejected'] for case in completion['cases']),
                producer_literal_rejections=sum(case['completions_rejected'] for case in completion['cases']),
                independent_completions_tested=sum(case['completions_tested'] for case in independent['cases']),
                independent_completions_rejected=sum(case['completions_rejected'] for case in independent['cases']),
                valid_completions=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--resume',action='store_true',help='resume natural primary root/incidence checkpoints; independent verification is always fresh')
    parser.add_argument('--write-expected',action='store_true',help='maintainer-only: write the compact manifest after all checks pass')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    work = args.work.resolve()
    generated = ('local_roots.json','incidences.json','completions.json','independent.json','controls.json','controls_optimized.json')
    require(args.resume or not any((work/name).exists() for name in generated),'use a fresh work directory or explicit --resume')
    work.mkdir(parents=True,exist_ok=True)
    environment = dict(os.environ)
    for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        environment[variable]='1'
    def run(file,arguments,optimized=False):
        command = [sys.executable]+(['-O'] if optimized else [])+[str(directory/file)]+[str(x) for x in arguments]
        subprocess.run(command,env=environment,check=True)
    started = time.monotonic()
    run('local_roots.py',['--output',work/'local_roots.json'])
    run('incidence.py',['--roots',work/'local_roots.json','--output',work/'incidences.json','--seconds','30']+
        (['--resume-incomplete'] if args.resume else []))
    run('controls.py',['--roots',work/'local_roots.json','--incidences',work/'incidences.json','--output',work/'controls.json'])
    run('controls.py',['--roots',work/'local_roots.json','--incidences',work/'incidences.json','--output',work/'controls_optimized.json'],optimized=True)
    run('complete.py',['--incidences',work/'incidences.json','--output',work/'completions.json','--seconds','30'])
    run('independent.py',['--roots',work/'local_roots.json','--incidences',work/'incidences.json',
                         '--expected',work/'completions.json','--output',work/'independent.json','--seconds','30'])
    result = compact(work)
    expected = directory/'expected.json'
    if args.write_expected:
        expected.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        require(result==json.loads(expected.read_text()),'reproduction differs from compact expected manifest')
    (work/'manifest.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='REPRODUCTION_PASS',totals=result['totals'],
                         expected_sha256=hashlib.sha256(expected.read_bytes()).hexdigest(),
                         seconds=time.monotonic()-started),indent=2))


if __name__=='__main__':
    main()
