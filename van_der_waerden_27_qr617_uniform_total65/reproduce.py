#!/usr/bin/env python3
"""Regenerate70 primitives and check194 audit partitions, serially with90s caps."""
import argparse
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path
import verify as v

HERE = Path(__file__).resolve().parent
CASES = v.CASES
BASIC = ['Boolean_endpoint','wrong_endpoint','wrong_root','same_total_wrong_original_caps',
         'enlarged_original_budget','extra_initial_hypothesis','supplied_parent_state',
         'false_terminal','incomplete_terminal']
SPLIT = ['missing_child','duplicate_child','Boolean_child','child_outside_full_petal',
         'nonmandatory_split','wrong_child_budget','wrong_child_root','extra_child_hypothesis','supplied_child_state']


def tasks(case):
    return ([('root',r) for r in case['roots']] + [('controls',r) for r in case['roots']] +
            ([('split',None)] if case['split_root'] is not None else []) + [('coverage',None)])


def pause_guard():
    # Optional host campaign flags; ordinary readers need no campaign directory.
    team = Path('/scratch/research-team-sol61-six-20260929')
    v.require(not any((team/name).exists() for name in
        ['PAUSED.json','HANDOVER.json','state/PAUSED.json','state/HANDOVER.json']), 'Pause/handover: preserve pending jobs')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--resume',action='store_true')
    a = p.parse_args()
    work = a.output_dir.resolve()
    v.require(not work.is_relative_to(HERE.parent.resolve()), 'Generated proof data must stay outside the repository')
    if work.exists() and not a.resume:
        p.error('Choose a fresh directory or explicitly resume checked completed jobs')
    work.mkdir(parents=True,exist_ok=True)
    jobs, proofs, parts = [work/name for name in ['jobs','proofs','partitions']]
    for directory in [jobs,proofs,parts]: directory.mkdir(exist_ok=True)
    pins = {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(HERE.glob('*.py'))}
    pins.update({name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['expected.json','provenance.json']})
    pin_path = work/'source-pins.json'
    if pin_path.exists(): v.require(json.loads(pin_path.read_text()) == pins,'Saved computation used different source')
    else: pin_path.write_text(json.dumps(pins,indent=2)+'\n')
    expected = json.loads((HERE/'expected.json').read_text())
    v.require(expected['cases'] == CASES,'Changed full case list')
    env = os.environ.copy()
    env.update({name:'1' for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS','OMP_THREAD_LIMIT','NUMBA_NUM_THREADS']})
    start = time.monotonic()
    completed, fresh = [], []

    def run_stage(token,command):
        pause_guard()
        record = jobs/(token+'.json')
        if record.exists():
            saved = json.loads(record.read_text())
            v.require(a.resume and saved['status'] == 'FINISHED' and saved['returncode'] == 0 and
                      saved['command'] == command and saved['cap_seconds'] == 90 and saved['threads'] == 1,
                      'Interrupted or failed saved job: no automatic retry')
            completed.append(token)
            return
        row = {'agent':'six-vdw-2','role':'researcher','token':token,'command':command,
               'status':'STARTED','returncode':None,'threads':1,'cap_seconds':90}
        record.write_text(json.dumps(row,indent=2)+'\n')
        begin = time.monotonic()
        with (jobs/(token+'.log')).open('w') as stdout, (jobs/(token+'.err')).open('w') as stderr:
            try:
                result = subprocess.run(command,env=env,stdout=stdout,stderr=stderr,timeout=90)
                row.update(status='FINISHED',returncode=result.returncode)
            except subprocess.TimeoutExpired:
                row.update(status='TIME_LIMIT')
        row.update(seconds=round(time.monotonic()-begin,3),
                   max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        record.write_text(json.dumps(row,indent=2)+'\n')
        v.require(row['status'] == 'FINISHED' and row['returncode'] == 0,
                  'Bounded job failed or timed out: preserve progress; no automatic retry or exclusion')
        completed.append(token);fresh.append(token)
        print(json.dumps({'completed':token,'seconds':row['seconds'],'clean_exit':True}),flush=True)

    for e,B in CASES:
        case = v.case_spec(e,B)
        for root in case['roots']:
            token = f'generate-e{e}-{B[0]}-{B[1]}-root{root}'
            command = [sys.executable,str(HERE/'generate.py'),'--output',str(proofs),
                       '--endpoint',str(e),'--budget',*map(str,B),'--root',str(root),'--seconds','90']
            run_stage(token+'-parent',command)
            if root == case['split_root']:
                for child in case['children']:
                    run_stage(token+f'-child{child}',command+['--child',str(child)])
    expected_names = {row['file'] for box in expected['boxes'] for row in box['certificates']}
    v.require({path.name for path in proofs.glob('tree-*.json')} == expected_names,'Incomplete full forest file coverage')
    for box in expected['boxes']:
        for row in box['certificates']:
            raw = (proofs/row['file']).read_bytes()
            v.require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                      'Fresh canonical certificate differs from the frozen proof')
    for mode in ['normal','optimized']:
        interpreter = [sys.executable]+(['-O'] if mode == 'optimized' else [])
        for e,B in CASES:
            case = v.case_spec(e,B)
            for task,root in tasks(case):
                token = f'{mode}-e{e}-{B[0]}-{B[1]}-{task}'+('' if root is None else f'-{root}')
                command = interpreter+[str(HERE/'verify.py'),str(proofs),'--endpoint',str(e),
                    '--budget',*map(str,B),'--task',task,'--output',str(parts/(token+'.json'))]
                if root is not None: command += ['--root',str(root)]
                run_stage(token,command)
        run_stage(mode+'-arithmetic',interpreter+[str(HERE/'verify.py'),str(proofs),
            '--task','arithmetic','--output',str(parts/(mode+'-arithmetic.json'))])
    v.require(len(completed) == len(set(completed)) == 264,'Incomplete exact70/194 primitive/partition coverage')
    names, results = set(), []
    for e,B in CASES:
        case = v.case_spec(e,B);loaded = {}
        for task,root in tasks(case):
            suffix = f'-e{e}-{B[0]}-{B[1]}-{task}'+('' if root is None else f'-{root}')
            paths = [parts/(mode+suffix+'.json') for mode in ['normal','optimized']]
            v.require(paths[0].read_bytes() == paths[1].read_bytes(),'Normal/O partition bytes differ')
            row = json.loads(paths[0].read_text())
            v.require((row['endpoint'],row['budget'],row['task'],row['root']) == (e,B,task,root),
                      'Wrong audit partition quantifiers')
            loaded[(task,root)] = row['result']
            for mode in ['normal','optimized']:
                names.add(mode+suffix+'.json')
                log = json.loads((jobs/(mode+suffix+'.log')).read_text())
                v.require((log['endpoint'],log['budget'],log['task'],log['root'],log['optimized_flag']) ==
                          (e,B,task,root,1 if mode == 'optimized' else 0),'Wrong actual interpreter mode')
        root_parts = [loaded[('root',root)] for root in case['roots']]
        controls = [item for root in case['roots'] for item in loaded[('controls',root)]['rejected']]
        controls += (loaded[('split',None)]['rejected'] if case['split_root'] is not None else [])
        controls += loaded[('coverage',None)]['rejected']
        controls_expected = [(root,name) for root in case['roots'] for name in BASIC]
        controls_expected += ([(case['split_root'],name) for name in SPLIT] if case['split_root'] is not None else [])
        controls_expected += [(root,'missing_mandatory_root') for root in case['roots']]+[(None,'unexpected_root')]
        v.require(len(controls_expected) == len(set(controls_expected)) == (70 if case['split_root'] is not None else 61) and
                  [(x.get('root'),x['name']) for x in controls] == controls_expected,
                  'Incomplete meaningful corruption-control coverage')
        box = next(row for row in expected['boxes'] if (row['endpoint'],row['budget']) == (e,B))
        v.require([x['certificate'] for x in root_parts] == box['certificates'] and
                  [x['root_result'] for x in root_parts] == box['verification']['root_results'] and
                  [x['parent_state'] for x in root_parts] == box['parent_states'],
                  'Full independent root/state/canonical results differ')
        results.append({'endpoint':e,'budget':B,'root_cases':6,'controls_rejected':len(controls)})
    v.require((parts/'normal-arithmetic.json').read_bytes() == (parts/'optimized-arithmetic.json').read_bytes(),
              'Normal/O arithmetic bytes differ')
    for mode in ['normal','optimized']:
        names.add(mode+'-arithmetic.json')
        log = json.loads((jobs/(mode+'-arithmetic.log')).read_text())
        v.require((log['endpoint'],log['budget'],log['task'],log['root'],log['optimized_flag']) ==
                  (None,None,'arithmetic',None,1 if mode == 'optimized' else 0),'Wrong arithmetic mode')
    v.require({path.name for path in parts.glob('*.json')} == names and len(names) == 194,
              'Missing or extra audit partition')
    summary = {'agent':'six-vdw-2','role':'researcher','status':'UNIFORM65_SEVEN_BOX_FULL_REPRODUCTION_PASSED',
        'generation_primitives':70,'validation_partitions':194,'root_cases':42,'nodes':70,'splits':5,'closed_leaves':65,
        'corruption_controls_per_mode':472,'normal_optimized_identical_pairs':97,'full_parent_state_comparisons':42,
        'certificate_bytes':expected['certificate_bytes'],'all_canonical_certificate_bytes_match':True,
        'all_mode_partition_bytes_identical':True,'cases':results,
        'arithmetic':json.loads((parts/'normal-arithmetic.json').read_text())['result'],
        'threads':1,'primitive_caps_seconds':90,'fresh_jobs_this_invocation':len(fresh),
        'seconds':round(time.monotonic()-start,3),'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'witness_or_global_W_bound_asserted':False}
    target = work/('resume-summary.json' if (work/'summary.json').exists() else 'summary.json')
    target.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:value for k,value in summary.items() if k != 'arithmetic'}),flush=True)


if __name__ == '__main__':
    main()
