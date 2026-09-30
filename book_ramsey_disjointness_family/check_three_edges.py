#!/usr/bin/env python3
"""Compile and completely run the five exact internal three-edge cases."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
PLACEMENTS = {'triangle': 20, 'star': 60, 'p4': 180,
              'p3k2': 180, '3k2': 15}


def run(directory):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    executable = directory/'search_three_edges'
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    subprocess.run(['c++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                    str(HERE/'search_three_edges.cpp'), '-o', str(executable)],
                   check=True, env=env, timeout=60)
    output = {'agent': 'six-books-2', 'role': 'researcher',
              'scope': 'All cross assignments with the fixed labeled core and exactly three internal red edges.',
              'degree_or_edge_bounds_used': False,
              'labeled_placements': PLACEMENTS, 'patterns': {}}
    for pattern in PLACEMENTS:
        trace = directory/f'{pattern}.trace'
        result = subprocess.run([str(executable), str(HERE/'core16.edges'),
                                 str(trace), pattern], check=True,
                                capture_output=True, text=True,
                                env=env, timeout=60)
        counts = json.loads(result.stdout)
        if counts.get('complete') is not True or counts.get('full_valid') != 0:
            raise AssertionError('the exclusion is not established')
        row_sizes = Counter()
        leaf_sizes = Counter()
        for line in trace.read_text().splitlines():
            if line.startswith('R '):
                row_sizes[str(int(line[2:]).bit_count())] += 1
            elif pattern == 'star' and line.startswith('E '):
                values = list(map(int, line.split()[1:]))
                leaf_sizes[str(values[2*values[0]+1])] += 1
        output['patterns'][pattern] = {
            'counts': counts, 'row_sizes': dict(row_sizes),
            'trace_bytes': trace.stat().st_size,
            'trace_sha256': sha256(trace.read_bytes()).hexdigest()}
        if pattern == 'star':
            output['patterns'][pattern]['center_leaf_domain_sizes'] = dict(leaf_sizes)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', default='scratch/books_three_edges')
    args = parser.parse_args()
    output = run(args.scratch)
    expected = json.loads((HERE/'three_edges_expected.json').read_text())
    if output != expected:
        raise AssertionError('compact diagnostics mismatch')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
