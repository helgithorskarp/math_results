#!/usr/bin/env python3
"""Serial, fixed-20-second-child reproduction, normal/-O and corruptions."""
import argparse
import copy
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD = 20


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def mutations(stage, value):
    result = []
    def add(name, operation):
        other = copy.deepcopy(value)
        operation(other)
        result.append((name, other))
    if stage == 'base':
        add('prime', lambda d: d.update(prime=619))
        add('missing_endpoint', lambda d: d['endpoint_unit_supports'].pop())
        add('repeated_pack', lambda d: d.update(five_disjoint_support_indices=[0, 0, 2, 3, 4]))
        add('character_digest', lambda d: d.update(character_ascii_sha256='0' * 64))
        add('reciprocal_claim', lambda d: d.update(reciprocal_overlap=[1]))
        add('field_coverage', lambda d: d.update(field_start_step_pairs=380071))
    elif stage == 'lattice':
        add('missing_state', lambda d: d['records'].pop())
        add('missing_closure_vertex', lambda d: d['records'][0]['A'].pop())
        add('invalid_vertex', lambda d: d['records'][0]['B'].insert(0, 0))
        add('wrong_threshold', lambda d: d.update(minimum_B_size=11))
        add('state_digest', lambda d: d.update(state_records_sha256='0' * 64))
    elif stage == 'lift':
        add('below_threshold', lambda d: d.update(interval=3701))
        add('wrong_digest', lambda d: d.update(actual_lifts_sha256='0' * 64))
        add('missing_pair', lambda d: d.update(actual_endpoint_pairs=d['actual_endpoint_pairs'] - 1))
        add('wrong_orientation_count', lambda d: d.update(forward_APs=d['forward_APs'] + 1))
    else:
        add('prime', lambda d: d.update(prime=619))
        add('wrong_digest', lambda d: d.update(transport_sha256='0' * 64))
        add('missing_column', lambda d: d.update(literal_support_columns=d['literal_support_columns'] - 1))
        add('missing_parameter', lambda d: d.update(root_target_parameters=d['root_target_parameters'] - 1))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'results')
    parser.add_argument('--barrier-file', type=Path, action='append', default=[])
    args = parser.parse_args()
    out = args.output.resolve()
    need(not out.exists() or not any(out.iterdir()), 'use a fresh output directory; preserve old receipts')
    out.mkdir(parents=True, exist_ok=True)
    pins = HERE / 'SOURCE_PINS.json'
    if pins.exists():
        for name, expected in json.loads(pins.read_text())['files'].items():
            need(sha((HERE / name).read_bytes()) == expected['sha256'], 'source pin ' + name)
            need(len((HERE / name).read_bytes()) == expected['bytes'], 'source byte length ' + name)
    env = os.environ.copy()
    for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                     'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[variable] = '1'
    execution = []
    began = time.monotonic()
    def child(label, command, should_pass=True):
        for barrier in args.barrier_file:
            need(not barrier.exists(), 'operations barrier ' + str(barrier))
        started = time.monotonic()
        try:
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=GUARD)
        except subprocess.TimeoutExpired:
            execution.append({'label': label, 'status': 'TIMEOUT_INCOMPLETE_NO_EXCLUSION',
                              'seconds': time.monotonic() - started})
            (out / 'execution.json').write_text(json.dumps({'children': execution}, indent=2) + '\n')
            raise SystemExit('Incomplete; preserve receipt, do not raise the guard or infer exclusion')
        row = {'label': label, 'exit_code': result.returncode, 'seconds': time.monotonic() - started}
        execution.append(row)
        (out / 'execution.json').write_text(json.dumps({'children': execution}, indent=2) + '\n')
        if should_pass:
            need(result.returncode == 0, label + '\n' + result.stderr[-3000:])
        else:
            need(result.returncode != 0 and 'ValueError:' in result.stderr, 'damaged certificate must be rejected')
        print(json.dumps(row), flush=True)
    stages = [('base', [], 'base'), ('lattice', [], 'lattice')]
    for n in (3702, 3704):
        for start in range(1, n + 1, 256):
            stop = min(n, start + 255)
            stages.append((f'lift-{n}-{start}-{stop}',
                           ['--interval', str(n), '--start', str(start), '--stop', str(stop)], 'lift'))
    for start in range(0, 617, 32):
        stop = min(616, start + 31)
        stages.append((f'transport-{start}-{stop}', ['--start', str(start), '--stop', str(stop)], 'transport'))
    damage_counts = {}
    for mode, flag in (('normal', []), ('optimized', ['-O'])):
        folder = out / mode
        folder.mkdir()
        first = {}
        for label, options, stage in stages:
            data = folder / (label + '.json')
            checked = folder / (label + '-checked.json')
            first.setdefault(stage, data)
            child(mode + '-' + label + '-generate',
                  [sys.executable, *flag, str(HERE / 'generate.py'), stage, *options, '--output', str(data)])
            child(mode + '-' + label + '-check',
                  [sys.executable, *flag, str(HERE / 'check.py'), '--input', str(data), '--output', str(checked)])
        count = 0
        for stage, path in first.items():
            for label, data in mutations(stage, json.loads(path.read_text())):
                damaged = folder / ('damage-' + stage + '-' + label + '.json')
                damaged.write_text(json.dumps(data, sort_keys=True, indent=2) + '\n')
                child(mode + '-damage-' + stage + '-' + label,
                      [sys.executable, *flag, str(HERE / 'check.py'), '--input', str(damaged)], should_pass=False)
                count += 1
        damage_counts[mode] = count
    files = []
    checked_pairs = 0
    for label, options, stage in stages:
        for suffix in ('.json', '-checked.json'):
            first = (out / 'normal' / (label + suffix)).read_bytes()
            second = (out / 'optimized' / (label + suffix)).read_bytes()
            need(first == second, 'normal/-O whole-file equality ' + label + suffix)
            checked_pairs += 1
        files.append([label, sha((out / 'normal' / (label + '.json')).read_bytes())])
    base = json.loads((out / 'normal/base.json').read_text())
    lattice = json.loads((out / 'normal/lattice.json').read_text())
    lifts = [json.loads((out / 'normal' / (label + '.json')).read_text())
             for label, _, stage in stages if stage == 'lift']
    transports = [json.loads((out / 'normal' / (label + '.json')).read_text())
                  for label, _, stage in stages if stage == 'transport']
    for n in (3702, 3704):
        rows = [v for v in lifts if v['interval'] == n]
        need(rows[0]['start'] == 1 and rows[-1]['stop'] == n
             and all(x['stop'] + 1 == y['start'] for x, y in zip(rows, rows[1:])), 'contiguous full lift coverage')
    need(transports[0]['start'] == 0 and transports[-1]['stop'] == 616
         and all(x['stop'] + 1 == y['start'] for x, y in zip(transports, transports[1:])), 'contiguous full root coverage')
    summary = {'schema': 'character617-final-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
               'prime': 617, 'complete_endpoint_steps': base['endpoint_steps_examined'],
               'opposite_endpoint_supports': len(base['endpoint_unit_supports']),
               'pairwise_disjoint_pack': len(base['five_disjoint_support_indices']),
               'directed_support_degree': len(base['support_union']), 'reciprocal_support_pairs': 0,
               'undirected_ratio_degree': len(base['undirected_ratio_set']),
               'minimum_endpoint_covers': base['minimum_covers'],
               'minimum_endpoint_covers_sha256': base['minimum_covers_sha256'],
               'complete_field_start_step_pairs': base['field_start_step_pairs'],
               'partial_monochromatic_field_pairs': base['partial_monochromatic_pairs'],
               'normalized_intersection_states': lattice['states'],
               'retained_intersection_transitions': lattice['retained_transitions'],
               'intersection_A_histogram': lattice['A_histogram'],
               'maximum_A_at_B_size_at_least10': lattice['maximum_A'],
               'closed_family_state_records_sha256': lattice['state_records_sha256'],
               'literal_lift_pairs': sum(x['actual_endpoint_pairs'] for x in lifts),
               'literal_lift_intervals': [3702, 3704],
               'transport_root_target_parameters': sum(x['root_target_parameters'] for x in transports),
               'transport_support_columns': sum(x['literal_support_columns'] for x in transports),
               'whole_generated_file_record_sha256': sha(canonical(files)),
               'whole_mode_record_pairs': checked_pairs,
               'damages_rejected_each_mode': damage_counts['normal'],
               'mathematical_children': len(execution), 'child_guard_seconds': GUARD, 'threads': 1,
               'ordinary_bridge_nonzero_flip_column_lower_bound': 22,
               'actual_restricted_3703_colorings': base['actual_restricted_3703_colorings'],
               'new_3704_coloring': False, 'numerical_W_bound_improved': False}
    need(damage_counts['normal'] == damage_counts['optimized'] == 19, 'damage coverage')
    expected = HERE / 'expected.json'
    if expected.exists():
        need(summary == json.loads(expected.read_text()), 'compact expected summary')
    (out / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n')
    receipt = {'status': 'COMPLETE', 'agent': 'six-vdw-3', 'role': 'researcher',
               'elapsed_seconds': time.monotonic() - began,
               'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'max_child_seconds': max(x['seconds'] for x in execution),
               'summary_sha256': sha((out / 'summary.json').read_bytes()), 'children': execution}
    (out / 'execution.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(summary, sort_keys=True), flush=True)
    print(json.dumps({k: v for k, v in receipt.items() if k != 'children'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
