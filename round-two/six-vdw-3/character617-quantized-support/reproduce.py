#!/usr/bin/env python3
"""Fixed-cap serial source replay and whole semantic-certificate checks."""
import argparse
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
GUARD = 20


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def repair(data):
    """Repair data digests so negative tests concern mathematics, not hashing."""
    if 'records' in data:
        data['records_sha256'] = sha(canonical(data['records']))
    if 'five_records' in data:
        data['five_records_sha256'] = sha(canonical(data['five_records']))
    if 'survivors' in data:
        data['survivor_records_sha256'] = sha(canonical(data['survivors']))
    for case in data.get('cases', []):
        case['records_sha256'] = sha(canonical(case['records']))
    return data


def mutations(stage, data):
    result = []
    def add(name, action):
        value = copy.deepcopy(data)
        action(value)
        result.append((name, repair(value)))
    if stage == 'lattice':
        add('prime', lambda v: v.update(prime=619))
        add('missing_reachable_state', lambda v: v['records'].pop())
        add('incomplete_square_closure', lambda v: v['records'][0]['A'].pop())
        add('wrong_threshold', lambda v: v.update(threshold=7))
        add('wrong_normalization', lambda v: v.update(normalized_vertex=4))
        add('missing_endpoint_point', lambda v: v['endpoint_supports'][0]['support'].pop())
        add('wrong_retained_transition_count', lambda v: v.update(retained_transitions=v['retained_transitions']-1))
    elif stage == 'cores':
        add('missing_five_set', lambda v: v['five_records'].pop())
        add('missing_balanced_core', lambda v: v['cases'][1]['records'].pop())
        add('missing_surviving_core', lambda v: v['survivors'].pop())
        add('wrong_missing_budget', lambda v: v['cases'][1].update(missing_budget=18))
        add('wrong_common_guarantee', lambda v: v['cases'][1].update(guaranteed_common=6))
        add('wrong_weighted_bound', lambda v: v['cases'][1]['records'][0].update(weighted_lower=17))
        add('wrong_coefficient_count', lambda v: v['survivors'][0].update(row_choices=1))
    else:
        add('missing_entire_core', lambda v: v['records'].pop())
        add('wrong_extra_row', lambda v: v['records'][0]['records'][0]['Aextra'].__setitem__(0, 0))
        add('duplicate_extra_row', lambda v: v['records'][0]['records'][0]['Aextra'].__setitem__(1, v['records'][0]['records'][0]['Aextra'][0]))
        add('wrong_outside_column', lambda v: v['records'][0]['records'][0]['best_outside'][0].__setitem__(1, 0))
        add('wrong_core_cost', lambda v: v['records'][0]['records'][0].update(core_cost=0))
        add('wrong_missing_minimum', lambda v: v.update(minimum_missing=17))
        add('missing_extension', lambda v: v['records'][0]['records'].pop())
        add('wrong_total_choices', lambda v: v.update(row_choices=v['row_choices']-1))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE/'results')
    parser.add_argument('--barrier-file', type=Path, action='append', default=[])
    args = parser.parse_args()
    out = args.output.resolve()
    need(not out.exists() or not any(out.iterdir()), 'fresh result directory required')
    out.mkdir(parents=True, exist_ok=True)
    pins = HERE/'SOURCE_PINS.json'
    if pins.exists():
        for name, pin in json.loads(pins.read_text())['files'].items():
            raw = (HERE/name).read_bytes()
            need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'source pin '+name)
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    began, execution = time.monotonic(), []
    def child(label, argv, should_pass=True):
        for barrier in args.barrier_file:
            need(not barrier.exists(), 'operations barrier '+str(barrier))
        started = time.monotonic()
        try:
            r = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=GUARD)
        except subprocess.TimeoutExpired:
            execution.append({'label': label, 'status': 'TIMEOUT_INCOMPLETE_NO_EXCLUSION', 'seconds': time.monotonic()-started})
            (out/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
            raise SystemExit('Preserve incomplete instance; no guard increase or exclusion')
        row = {'label': label, 'exit_code': r.returncode, 'seconds': time.monotonic()-started}
        execution.append(row)
        (out/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
        need((r.returncode == 0) if should_pass else (r.returncode != 0 and 'ValueError:' in r.stderr), label+'\n'+r.stderr[-2500:])
        print(json.dumps(row), flush=True)
    damages = {}
    for mode, flags in (('normal', []), ('optimized', ['-O'])):
        folder = out/mode
        folder.mkdir()
        paths = {stage: folder/(stage+'.json') for stage in ('lattice', 'cores', 'extend')}
        for stage in paths:
            argv = [sys.executable, *flags, str(HERE/'generate.py'), stage, '--output', str(paths[stage])]
            if stage != 'lattice':
                argv += ['--input', str(paths['lattice' if stage == 'cores' else 'cores'])]
            child(mode+'-'+stage+'-generate', argv)
            argv = [sys.executable, *flags, str(HERE/'check.py'), '--input', str(paths[stage]), '--output', str(folder/(stage+'-checked.json'))]
            if stage != 'lattice':
                argv += ['--lattice', str(paths['lattice'])]
            if stage == 'extend':
                argv += ['--cores', str(paths['cores'])]
            child(mode+'-'+stage+'-check', argv)
        child(mode+'-small-controls', [sys.executable, *flags, str(HERE/'check.py'), '--controls', '--output', str(folder/'controls.json')])
        number = 0
        for stage, path in paths.items():
            for name, data in mutations(stage, json.loads(path.read_text())):
                bad = folder/('damage-'+stage+'-'+name+'.json')
                bad.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
                argv = [sys.executable, *flags, str(HERE/'check.py'), '--input', str(bad)]
                if stage != 'lattice':
                    argv += ['--lattice', str(paths['lattice'])]
                if stage == 'extend':
                    argv += ['--cores', str(paths['cores'])]
                child(mode+'-damage-'+stage+'-'+name, argv, should_pass=False)
                number += 1
        damages[mode] = number
    inventory, pairs = [], 0
    for name in ('lattice.json', 'lattice-checked.json', 'cores.json', 'cores-checked.json', 'extend.json', 'extend-checked.json', 'controls.json'):
        raw = (out/'normal'/name).read_bytes()
        need(raw == (out/'optimized'/name).read_bytes(), 'whole normal/-O equality '+name)
        inventory.append([name, sha(raw)])
        pairs += 1
    lattice = json.loads((out/'normal/lattice.json').read_text())
    cores = json.loads((out/'normal/cores.json').read_text())
    extension = json.loads((out/'normal/extend.json').read_text())
    summary = {'schema': 'character617-quantized-summary-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
               'prime': 617, 'dependency_lemma_heights': [9880, 9904],
               'states': lattice['states'], 'tested_transitions': lattice['tested_transitions'], 'retained_transitions': lattice['retained_transitions'],
               'lattice_records_sha256': lattice['records_sha256'], 'five_sets': cores['five_sets'], 'five_records_sha256': cores['five_records_sha256'],
               'cases': [{k: v for k, v in case.items() if k != 'records'} for case in cores['cases']],
               'surviving_cores': cores['surviving_cores'], 'survivor_records_sha256': cores['survivor_records_sha256'],
               'row_choices': extension['row_choices'], 'minimum_conditional_missing': extension['minimum_missing'],
               'conditional_missing_histogram': extension['missing_histogram'], 'extension_records_sha256': extension['records_sha256'],
               'whole_normal_optimized_pairs': pairs, 'semantic_damages_per_mode': damages,
               'small_control_cases_per_mode': 77, 'mathematical_children': len(execution), 'guard_seconds': GUARD,
               'generated_inventory_sha256': sha(canonical(inventory)),
               'claim': 'No 23-vertex flip support: every nonempty actual single-character617 flip set has at least24 columns for N>=3702, using lemmas9880 and9904.'}
    expected = HERE/'expected.json'
    if expected.exists():
        need(summary == json.loads(expected.read_text()), 'entire compact expected result')
    (out/'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2)+'\n')
    run = {'status': 'COMPLETE_ALL_DOMAIN_CHECKED', 'seconds': time.monotonic()-began,
           'maximum_child_seconds': max(r['seconds'] for r in execution),
           'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
           'children': len(execution), 'summary_sha256': sha(canonical(summary))}
    (out/'run.json').write_text(json.dumps(run, sort_keys=True, indent=2)+'\n')
    print(json.dumps(run), flush=True)


if __name__ == '__main__':
    main()
