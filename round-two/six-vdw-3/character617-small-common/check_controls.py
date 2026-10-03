"""Expected semantic rejection controls for physical tail checking and coverage."""
import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('canonical', 'part', 'producer', 'checker', 'optimized', 'work', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--barrier-file', action='append', type=Path, default=[])
    o = p.parse_args()
    source = Path(__file__).resolve().parent
    if o.work.exists():
        raise ValueError('Preserve previous control outputs; work must be new')
    o.work.mkdir(parents=True)
    parent = json.loads(o.part.read_text())
    if parent['start'] != 0 or not parent['records']:
        raise ValueError('Controls require the first genuine physical tail part')
    good = copy.deepcopy(parent)
    good['records'] = [good['records'][0]]
    good['stop'] = 1
    good['survivors'] = int(good['records'][0]['tail_gate_pass'])
    canonical = json.loads(o.canonical.read_text())
    a = canonical['records'][0]['A']
    columns = sorted(set(range(1, 617)) - {q * q % 617 for q in range(1, 617)})
    rows = sorted({q * q % 617 for q in range(1, 617)})
    outside_row = next(q for q in rows if q not in a)
    mutations = {}

    def damage(name, fn):
        d = copy.deepcopy(good)
        fn(d)
        mutations[name] = d

    def replace_physical(d):
        b = d['records'][0]['B']
        b[0] = next(t for t in columns if t not in b)
        b.sort()

    damage('changed_physical_column', replace_physical)
    damage('duplicate_physical_column', lambda d: d['records'][0]['B'].append(d['records'][0]['B'][-1]))
    damage('erased_tail2_row_or_injected_row', lambda d: d['records'][0].update(tail2=[] if d['records'][0]['tail2'] else [[outside_row, 0]]))
    damage('changed_tail3_membership', lambda d: d['records'][0].update(tail3_good=[] if d['records'][0]['tail3_good'] else [outside_row]))
    damage('changed_actual_prefix_bad_count', lambda d: d['records'][0].update(prefix_bad=d['records'][0]['prefix_bad'] + 1))
    damage('changed_actual_prefix_deficit', lambda d: d['records'][0].update(prefix_deficit=d['records'][0]['prefix_deficit'] + 1))
    damage('forged_tail_gate', lambda d: (d['records'][0].update(tail_gate_pass=not d['records'][0]['tail_gate_pass']), d.update(survivors=int(d['records'][0]['tail_gate_pass']))))
    damage('wrong_physical_case', lambda d: d['records'][0].update(case_id=d['records'][0]['case_id'] + 1))
    damage('wrong_physical_rank', lambda d: d['records'][0].update(rank=1))
    damage('missing_physical_incidence', lambda d: d.update(records=[]))
    damage('changed_canonical_dependency', lambda d: d.update(canonical_records_sha256='0' * 64))
    damage('forged_tail_bad_minimum', lambda d: d['records'][0].update(near_min_bad=0 if d['records'][0]['near_min_bad'] is None else d['records'][0]['near_min_bad'] + 1))
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    results = []

    def check(name, program, args, accepts, mode):
        if any(q.exists() for q in o.barrier_file):
            raise ValueError('Operations barrier; preserve partial controls')
        output = o.work / (name + '-' + mode + '-result.json')
        command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(source / program), *map(str, args), '--output', str(output)]
        begin = time.monotonic()
        with (o.work / (name + '-' + mode + '.stdout')).open('w') as stdout, (o.work / (name + '-' + mode + '.stderr')).open('w') as stderr:
            run = subprocess.run(command, env=env, stdout=stdout, stderr=stderr, timeout=20)
        if (run.returncode == 0) != accepts or (accepts and not output.exists()):
            raise ValueError('Unexpected semantic control outcome; no mathematical exclusion')
        record = {'name': name, 'mode': mode, 'expected_accept': accepts, 'returncode': run.returncode,
                  'seconds': time.monotonic() - begin, 'program_sha256': sha(source / program)}
        if accepts:
            record['output_sha256'] = sha(output)
        results.append(record)

    for name, d in [('undamaged_physical_incidence', good), *mutations.items()]:
        input_path = o.work / (name + '.json')
        input_path.write_text(json.dumps(d, sort_keys=True, separators=(',', ':')) + '\n')
        for mode in ('normal', 'optimized'):
            check(name, 'check_tail_cases.py', ['--input', input_path, '--canonical', o.canonical], name == 'undamaged_physical_incidence', mode)
    full_args = ['--producer', o.producer, '--checker', o.checker, '--optimized', o.optimized, '--canonical', o.canonical]
    for mode in ('normal', 'optimized'):
        check('undamaged_complete_coverage', 'merge_tail_cases.py', full_args, True, mode)
    raw = o.part.read_bytes()
    for name, copies in [('truncated_domain', 1), ('overlapping_domain', 2), ('empty_domain', 0)]:
        parent_dir = o.work / name
        dirs = []
        for mode in ('producer', 'checker', 'optimized'):
            directory = parent_dir / mode
            directory.mkdir(parents=True)
            for index in range(copies):
                (directory / f'range-{index:05d}.json').write_bytes(raw)
            dirs.append(directory)
        for mode in ('normal', 'optimized'):
            check(name, 'merge_tail_cases.py', ['--producer', dirs[0], '--checker', dirs[1], '--optimized', dirs[2], '--canonical', o.canonical], False, mode)
    for name in ('undamaged_physical_incidence', 'undamaged_complete_coverage'):
        if (o.work / (name + '-normal-result.json')).read_bytes() != (o.work / (name + '-optimized-result.json')).read_bytes():
            raise ValueError('Positive normal/optimized entire control records differ')
    result = {'schema': 'character617-small-common-semantic-controls-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
              'guard_seconds': 20, 'threads': 1, 'positive_controls_per_mode': 2,
              'negative_controls_per_mode': 15, 'all_expected': True, 'children': results,
              'canonical_sha256': sha(o.canonical), 'genuine_first_part_sha256': sha(o.part)}
    o.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'children'}, sort_keys=True))


if __name__ == '__main__':
    main()
