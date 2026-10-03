#!/usr/bin/env python3
"""Serial source-only reproduction with fixed guards and semantic damages."""
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
CHUNK = 32


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def mutations(stage, data):
    result = []
    def add(name, action):
        value = copy.deepcopy(data)
        action(value)
        result.append((name, value))
    if stage == 'lattice':
        add('prime', lambda v: v.update(prime=619))
        add('missing_state', lambda v: v['records'].pop())
        add('missing_closure_vertex', lambda v: v['records'][0]['A'].pop())
        add('invalid_column', lambda v: v['records'][0]['B'].insert(0, 0))
        add('threshold', lambda v: v.update(threshold=7))
    elif stage == 'cores':
        add('missing_five_set', lambda v: v['five_records'].pop())
        add('missing_balanced_core', lambda v: v['balanced_records'].pop())
        add('wrong_missing_bound', lambda v: v['part_cases'][0].update(minimum_lower_missing=12))
        add('wrong_domain_digest', lambda v: v.update(balanced_records_sha256='0'*64))
    else:
        add('missing_case', lambda v: v['records'].pop())
        add('wrong_transcript', lambda v: v['records'][0].update(extension_transcript_sha256='0'*64))
        add('wrong_extension_count', lambda v: v.update(extensions=v['extensions']-1))
        add('wrong_missing_minimum', lambda v: v.update(minimum_missing=11))
        add('missing_range', lambda v: v.update(stop=v['stop']-1))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=HERE/'results')
    ap.add_argument('--barrier-file', type=Path, action='append', default=[])
    args = ap.parse_args()
    out = args.output.resolve()
    need(not out.exists() or not any(out.iterdir()), 'fresh result directory required')
    out.mkdir(parents=True, exist_ok=True)
    pins = HERE/'SOURCE_PINS.json'
    if pins.exists():
        for name, pin in json.loads(pins.read_text())['files'].items():
            raw = (HERE/name).read_bytes()
            need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'source pin '+name)
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    execution, began = [], time.monotonic()
    def child(label, command, should_pass=True):
        for barrier in args.barrier_file:
            need(not barrier.exists(), 'operations barrier '+str(barrier))
        started = time.monotonic()
        try:
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=GUARD)
        except subprocess.TimeoutExpired:
            execution.append({'label': label, 'status': 'TIMEOUT_INCOMPLETE_NO_EXCLUSION',
                              'seconds': time.monotonic()-started})
            (out/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
            raise SystemExit('Preserve incomplete instance; do not raise guard or infer exclusion')
        row = {'label': label, 'exit_code': result.returncode, 'seconds': time.monotonic()-started}
        execution.append(row)
        (out/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
        if should_pass:
            need(result.returncode == 0, label+'\n'+result.stderr[-2500:])
        else:
            need(result.returncode != 0 and 'ValueError:' in result.stderr,
                 'damaged semantic certificate must be rejected '+label)
        print(json.dumps(row), flush=True)
    modes, damage_count = [], {}
    for mode, flags in (('normal', []), ('optimized', ['-O'])):
        folder = out/mode
        folder.mkdir()
        lattice, cores = folder/'lattice.json', folder/'cores.json'
        labels = ['lattice', 'cores']
        child(mode+'-lattice-generate', [sys.executable, *flags, str(HERE/'generate.py'), 'lattice', '--output', str(lattice)])
        child(mode+'-lattice-check', [sys.executable, *flags, str(HERE/'check.py'), '--input', str(lattice), '--output', str(folder/'lattice-checked.json')])
        child(mode+'-cores-generate', [sys.executable, *flags, str(HERE/'generate.py'), 'cores', '--input', str(lattice), '--output', str(cores)])
        child(mode+'-cores-check', [sys.executable, *flags, str(HERE/'check.py'), '--input', str(cores), '--lattice', str(lattice), '--output', str(folder/'cores-checked.json')])
        count = json.loads(cores.read_text())['surviving_balanced_cores']
        first_extension = None
        for start in range(0, count, CHUNK):
            stop = min(count, start+CHUNK)
            label = f'extend-{start}-{stop}'
            labels.append(label)
            path = folder/(label+'.json')
            first_extension = first_extension or path
            child(mode+'-'+label+'-generate', [sys.executable, *flags, str(HERE/'generate.py'), 'extend', '--input', str(cores), '--start', str(start), '--stop', str(stop), '--output', str(path)])
            child(mode+'-'+label+'-check', [sys.executable, *flags, str(HERE/'check.py'), '--input', str(path), '--cores', str(cores), '--lattice', str(lattice), '--output', str(folder/(label+'-checked.json'))])
        damages = 0
        for stage, path in (('lattice', lattice), ('cores', cores), ('extend', first_extension)):
            for name, data in mutations(stage, json.loads(path.read_text())):
                damaged = folder/('damage-'+stage+'-'+name+'.json')
                damaged.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
                command = [sys.executable, *flags, str(HERE/'check.py'), '--input', str(damaged)]
                if stage != 'lattice':
                    command += ['--lattice', str(lattice)]
                if stage == 'extend':
                    command += ['--cores', str(cores)]
                child(mode+'-damage-'+stage+'-'+name, command, should_pass=False)
                damages += 1
        modes.append(labels)
        damage_count[mode] = damages
    need(modes[0] == modes[1], 'entire mode stage coverage')
    inventory, pairs = [], 0
    for label in modes[0]:
        for suffix in ('.json', '-checked.json'):
            first = (out/'normal'/(label+suffix)).read_bytes()
            other = (out/'optimized'/(label+suffix)).read_bytes()
            need(first == other, 'whole-file normal/-O equality '+label+suffix)
            pairs += 1
        inventory.append([label, sha((out/'normal'/(label+'.json')).read_bytes())])
    lattice = json.loads((out/'normal/lattice.json').read_text())
    cores = json.loads((out/'normal/cores.json').read_text())
    extensions = [json.loads((out/'normal'/(label+'.json')).read_text()) for label in modes[0][2:]]
    need(extensions[0]['start'] == 0 and extensions[-1]['stop'] == cores['surviving_balanced_cores']
         and all(a['stop'] == b['start'] for a,b in zip(extensions, extensions[1:])), 'full disjoint contiguous extension coverage')
    rows = [row for data in extensions for row in data['records']]
    hist = Counter()
    for row in rows:
        hist.update(dict(row['missing_histogram']))
    summary = {'schema': 'character617-dense-summary-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
               'prime': 617, 'dependency_lemma_height': 9880,
               'states': lattice['states'], 'tested_transitions': lattice['tested_transitions'],
               'retained_transitions': lattice['retained_transitions'], 'maximum_A': lattice['maximum_A'],
               'state_records_sha256': lattice['state_records_sha256'],
               'normalized_five_sets': cores['normalized_five_sets'], 'five_records_sha256': cores['five_records_sha256'],
               'part_cases': cores['part_cases'], 'balanced_cores': cores['surviving_balanced_cores'],
               'balanced_records_sha256': cores['balanced_records_sha256'], 'extension_chunks': len(extensions),
               'extensions': sum(r['extensions'] for r in rows), 'minimum_balanced_missing': min(hist),
               'balanced_missing_histogram': [[k,n] for k,n in sorted(hist.items())],
               'checked_biclique_absences': [[5, 9], [6, 7], [7, 6]],
               'necessary_class_sizes_at_23': [[10, 13], [11, 12]],
               'all_extension_records_sha256': sha(canonical(rows)),
               'whole_normal_optimized_pairs': pairs, 'semantic_damages_per_mode': damage_count,
               'mathematical_children': len(execution), 'guard_seconds': GUARD,
               'generated_file_inventory_sha256': sha(canonical(inventory)),
               'claim': 'No directed-minimum-outdegree-five flip set of size22; every nonempty actual flip set has at least23 columns using lemma9880; size23 permits only class sizes10/13 or11/12.'}
    need(all(not (len(r['A']) >= a and len(r['B']) >= b)
             for a,b in summary['checked_biclique_absences'] for r in lattice['records']),
         'whole closed-family biclique exclusions')
    expected = HERE/'expected.json'
    if expected.exists():
        need(summary == json.loads(expected.read_text()), 'entire compact expected result')
    (out/'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2)+'\n')
    run = {'status': 'COMPLETE_ALL_DOMAIN_CHECKED', 'seconds': time.monotonic()-began,
           'maximum_child_seconds': max(r['seconds'] for r in execution),
           'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
           'children': len(execution), 'summary_sha256': sha(canonical(summary))}
    (out/'run.json').write_text(json.dumps(run, sort_keys=True, indent=2)+'\n')
    print(json.dumps(run, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
