"""Compile the separate CRT-fiber audit and compare every certificate row."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from verify import need


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sanitizers', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'certificate.json').read_text())
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    flags = ['-std=c++17', '-Wall', '-Wextra', '-Wconversion', '-Werror']
    flags += ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if args.sanitizers else ['-O2']
    build = root / 'build'
    build.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=build) as directory:
        binary = Path(directory) / 'audit'
        subprocess.run(['g++', *flags, str(root / 'audit.cpp'), '-o', str(binary)],
                       check=True, env=env, timeout=12)
        command = [str(binary)] + (['controls'] if args.sanitizers else [])
        p = subprocess.run(command, check=True, capture_output=True, text=True, env=env, timeout=10)
    if args.sanitizers:
        need(p.stdout.strip() == 'CONTROLS 2160000 497664 120 10368000', 'sanitizer controls incomplete')
        print(json.dumps({'status': 'SANITIZER_CRT_FIBER_CONTROLS_PASSED',
                          'control_counts': p.stdout.strip(), 'seconds': time.monotonic() - start}))
        return
    weights, pairs, rows, first, caps = [], [], [], {}, {}
    counts = None
    for line in p.stdout.splitlines():
        fields = line.split()
        kind = fields.pop(0)
        if kind == 'WEIGHT': weights.append(list(map(int, fields)))
        elif kind == 'PAIR': pairs.append(list(map(int, fields)))
        elif kind == 'TAIL':
            need(len(fields) == 9, 'bad tail audit row')
            rows.append([*map(int, fields[:4]), fields[4], *map(int, fields[5:])])
        elif kind == 'TAILCOUNTS':
            need(counts is None, 'duplicate counts')
            counts = list(map(int, fields))
        elif kind == 'CAP':
            values = list(map(int, fields))
            identifier, index, length = values[:3]
            need(len(values) == 5 + length, 'bad original block row')
            need((identifier, index) not in caps, 'duplicate original block row')
            caps[identifier, index] = {'moduli': values[3:3 + length],
                                       'raw_phase_tuples': values[-2], 'maximum': values[-1]}
        elif kind == 'FIRST':
            identifier = int(fields[0])
            need(identifier not in first, 'duplicate first shape')
            first[identifier] = {'shape_id': identifier, 'union_hex': fields[1],
                                  'union_count': int(fields[2]), 'compulsory_count': int(fields[3]),
                                  'total_capacity': int(fields[4])}
        else:
            raise RuntimeError('unknown audit record ' + kind)
    need(weights == expected['weights'] and pairs == expected['candidate_original_pairs'],
         'original inventory/weight/pair mismatch')
    need(sorted(rows) == expected['large_union_rows'], 'complete tail row mismatch')
    need(counts == [expected['raw_tail_phase_pairs'], expected['effective_tail_phase_pairs'], len(rows)],
         'complete original/effective tail phase count mismatch')
    need(set(first) == set(range(5)), 'incomplete first shapes')
    need(len(caps) == sum(len(row['groups']) for row in expected['first_complement_bounds']),
         'incomplete first original blocks')
    for row in expected['first_complement_bounds']:
        observed = first[row['shape_id']]
        observed['groups'] = [caps[row['shape_id'], i] for i in range(len(row['groups']))]
        need(observed == row, 'complete original first block comparison failed')
    print(json.dumps({'status': 'CPP_CRT_FIBER_AUDIT_MATCHES_ALL_ENTRIES',
                      'tail_entries': len(rows), 'first_original_blocks': len(caps),
                      'core_profile_pairs': 414720, 'covered_raw_core_phase_tuples': 10368000,
                      'seconds': time.monotonic() - start}))


if __name__ == '__main__':
    main()
