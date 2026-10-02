#!/usr/bin/env python3
"""Regenerate the complete finite census and explicit proofs, then check them.

Only standard Python and one byte-pinned credited RUP helper are required.
All models, proof streams and progress receipts remain in --workdir.
"""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def require(condition,message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--checker',type=Path)
    parser.add_argument('--cases',type=int,nargs='+')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    work = args.workdir.resolve()
    require(work != source and source not in work.parents,'Generated data must be outside the source directory')
    work.mkdir(parents=True,exist_ok=True)
    expected = json.loads((source/'expected.json').read_text())
    fixture = json.loads((source/'census.json').read_text())
    representatives = fixture['representatives']
    selected = representatives if args.cases is None else args.cases
    require(selected == sorted(set(selected)) and set(selected) <= set(representatives) and 2 in selected,
            'Selected cases must be sorted, unique, known and include 2 for production controls')
    checker = args.checker.resolve() if args.checker else work/'check_rup_lrat.py'
    pin = expected['sources']['rup_checker']
    if args.checker is None:
        raw = urllib.request.urlopen(pin['url'],timeout=25).read()
        require(hashlib.sha256(raw).hexdigest() == pin['sha256'],'Changed downloaded checker pin')
        checker.write_bytes(raw)
    require(hashlib.sha256(checker.read_bytes()).hexdigest() == pin['sha256'],'Changed checker pin')
    require(hashlib.sha256((source/'census.json').read_bytes()).hexdigest() == expected['census_sha256'],'Changed census fixture bytes')
    require(hashlib.sha256((source/'witnesses.json').read_bytes()).hexdigest() == expected['witnesses_sha256'],'Changed witness fixture bytes')
    env = dict(os.environ)
    env.update({k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS')})
    started = time.monotonic()
    result = {'agent':'six-vdw-3','role':'researcher','status':'INCOMPLETE','cases':[],
              'selected_cases':selected,'uniform_18_case_coverage_verified':False,
              'native_solver_invoked':False,'threads':1,'child_stage_seconds_guard':35,
              'empty_clause_checked':False,'mathematical_exclusion_claimed':False,'W_bound_improved':False}
    def save():
        result['pipeline_seconds'] = time.monotonic()-started
        result['child_peak_KiB'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        (work/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    def run(script,arguments,optimized=False):
        command = [sys.executable] + (['-O'] if optimized else []) + [str(source/script)] + list(map(str,arguments))
        completed = subprocess.run(command,env=env,capture_output=True,text=True,timeout=35)
        require(completed.returncode == 0,completed.stdout[-1500:]+completed.stderr[-1500:])
        return json.loads(completed.stdout)
    try:
        census = work/'census.json'
        run('generate.py',['--output',census])
        require(census.read_bytes() == (source/'census.json').read_bytes(),'Fresh census differs from frozen bytes')
        census_replays = []
        for optimized in (False,True):
            audit = run('check.py',['--census',census],optimized)
            require(audit == expected['census_audit'],'Complete census replay differs')
            census_replays.append(audit)
        result['census_replays'] = census_replays
        save()
        print(json.dumps({'stage':'complete census checked','cores':fixture['total_distinct_regular_cores']}),flush=True)
        expected_cases = {case['lambda']:case for case in expected['extensions']}
        for lam in selected:
            directory = work/('lambda-'+str(lam))
            proposal = run('compress.py',['--census',census,'--lambda',lam,'--output-directory',directory])
            replays = []
            for optimized in (False,True):
                audit = run('check_extension.py',['--directory',directory,'--lambda',lam,'--checker',checker],optimized)
                require({k:v for k,v in audit.items() if k != 'seconds'} == expected_cases[lam],'Fresh strict extension differs')
                replays.append(audit)
            result['cases'].append({'lambda':lam,'proposal':proposal,'replays':replays})
            save()
            print(json.dumps({'stage':'strict model equivalence checked','lambda':lam,
                              'cuts':replays[0]['derived_local_cuts_required']}),flush=True)
        fixtures = json.loads((source/'witnesses.json').read_text())
        witness_replays = []
        for index,fixture in enumerate(fixtures):
            path = work/('witness-'+str(index)+'.json')
            path.write_text(json.dumps(fixture,indent=2)+'\n')
            for optimized in (False,True):
                audit = run('check_witness.py',['--witness',path],optimized)
                require(audit == expected['witness_audits'][index],'Constructive witness replay differs')
            witness_replays.append(audit)
        result['witness_replays'] = witness_replays
        result['controls'] = {}
        for category in ('generic','census','witness','extension'):
            replays = []
            for optimized in (False,True):
                audit = run('controls.py',['--category',category,'--source',source,'--checker',checker,
                                          '--directory',work/'lambda-2','--workdir',work/('damage-'+category)],optimized)
                replays.append(audit)
            require(replays[0] == replays[1],'Optimized damage/positive control differs')
            result['controls'][category] = replays[0]
            save()
            print(json.dumps({'stage':'controls checked','category':category,**replays[0]}),flush=True)
        full = selected == representatives
        result['uniform_18_case_coverage_verified'] = full
        result['status'] = 'COMPLETE_18_CASE_CENSUS_EXTENSIONS_AND_IRREDUNDANCY_CHECKED' if full else 'SELECTED_EXTENSIONS_AND_COMPLETE_CENSUS_IRREDUNDANCY_CHECKED'
        result['summary'] = {key:sum(c['replays'][0][key] for c in result['cases']) for key in expected['summary']}
        if full:
            require(result['summary'] == expected['summary'],'Uniform summary changed')
        save()
    except (ValueError,subprocess.TimeoutExpired) as error:
        result['blocker'] = str(error)
        save()
        raise
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','census_replays','witness_replays')}),flush=True)


if __name__ == '__main__':
    main()
